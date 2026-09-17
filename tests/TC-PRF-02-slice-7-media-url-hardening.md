# TC-PRF-02 slice 7 follow-up — Media Queue URL hardening: acceptance record

**Date:** 2026-09-17
**Owner:** **Sukhdev Singh**
**Task:** `../active/tasks/PRF-02-slice-7-media-url-hardening.md`
**Implementation review:** `../reviews/2026-09-17-prf-02-media-url-hardening-implementation.md`
**Triggering review:** `../reviews/2026-09-17-slice-7-hostile-code-review.md` (F1, F4)

The "Commands run" table at the end is filled in from actual output; this is the single place
this task's numbers live.

---

## Acceptance criteria

### A. F1 — the object-key column shape (migration 0148, SQL layer)

| ID | Criterion |
|---|---|
| MUH.A1 | `public.media_queue_items.gcs_object_key` / `thumbnail_gcs_object_key` carry migration 0143's exact check-constraint shape: `^[A-Za-z0-9/_.-]{1,255}$` and never containing `..` |
| MUH.A2 | `enqueue_media_queue_item` called with a value shaped like a URL (`https://evil.example.net/payload.png` — carries a scheme and a host) is refused `22023`, because `:` and `//` are outside the allowed character set |
| MUH.A3 | `enqueue_media_queue_item` called with a `..` traversal segment (`ok/../../etc/passwd`) is refused `22023` even though every individual character matches the allowed set |
| MUH.A4 | `enqueue_media_queue_item` called with a key containing other disallowed characters (space, `!`) is refused `22023` |
| MUH.A5 | The same three rejections (URL-shaped, `..`, disallowed characters) apply identically to `thumbnail_gcs_object_key` |
| MUH.A6 | `list_overlay_media_queue`'s declared result type is exactly `queue_slot, title, media_kind, mime_type, gcs_object_key, thumbnail_gcs_object_key, duration_ms` — no `storage_url`/`thumbnail_url` column survives anywhere, asserted from both `pg_get_function_result` and a materialised live call |
| MUH.A7 | `list_channel_media_queue_items` returns `gcs_object_key`/`thumbnail_gcs_object_key`, not `storage_url`/`thumbnail_url` |
| MUH.A8 | Every other MED20.* assertion in `prf02_slice7_media_queue.sql` predating this task (role gates, tier-never-gates, FIFO current/next, cross-channel isolation, not-found shape, no-viewer-submission structural scan) still passes unmodified in substance |

### B. F1 — existing-row handling

| ID | Criterion |
|---|---|
| MUH.B1 | Migration 0148 deletes every existing `media_queue_items` row and announces the exact count via `RAISE NOTICE` before tightening the column shape — never silent |
| MUH.B2 | Applied against every environment this migration is meant to run against today (fresh schemas / SQL-suite template databases), the announced count is 0 |

### C. F1 — the API layer's second, independent narrowing

| ID | Criterion |
|---|---|
| MUH.C1 | `POST /v1/channels/:channelId/media-queue` with a `gcsObjectKey` carrying a scheme+host, a `..` segment, or disallowed characters is refused 400 before the store is ever called (AJV `pattern`) |
| MUH.C2 | The same enqueue route now requires `gcsObjectKey` (not `storageUrl`) and accepts `thumbnailGcsObjectKey` (not `thumbnailUrl`) |
| MUH.C3 | `GET /v1/overlay-widgets/:overlayId/media-queue` returns `playbackUrl`/`thumbnailPlaybackUrl` (never `storageUrl`/`thumbnailUrl`), re-validated https-or-null a second independent time by `projectOverlayMediaQueue` |
| MUH.C4 | A store handing up more than two overlay entries is still projected down to two (pre-existing behaviour, reconfirmed under the renamed fields) |
| MUH.C5 | `resolveMediaPlaybackUrl(cdnBaseUrl, objectKey)` returns `null` when `cdnBaseUrl` is undefined OR `objectKey` is null, and returns `${cdnBaseUrl}/${objectKey}` (trailing-slash-normalised) otherwise — proof no caller- or row-supplied value can become the origin, mirroring `resolveSoundboardPlaybackUrl` |
| MUH.C6 | `config.mediaCdnBaseUrl` is the only CDN-base config value read by the media-queue overlay store — no second config key introduced |

### D. F1 — the render layer renders nothing until a CDN base exists

| ID | Criterion |
|---|---|
| MUH.D1 | `hasSomethingToShow` returns `false` when the current entry's `playbackUrl` is null, even though a live entry exists |
| MUH.D2 | `createMediaQueueModule`'s `render()` never assigns a null/undefined value to `currentImgEl.src` / `currentVideoEl.src`, asserted directly against the DOM (`getAttribute('src') === null`) for a `playbackUrl: null` entry |
| MUH.D3 | The preload elements likewise receive no `src` when the "next" entry's `playbackUrl` is null |
| MUH.D4 | The closed mime allow-list and the `image/svg+xml` exclusion (migration 0146) are unchanged — confirmed by diff, not merely by absence of a failing test |

### E. F4 — the errcode seam, against a real database

| ID | Criterion |
|---|---|
| MUH.E1 | `integration/safe-soundboard-caps-not-configured.integration.ts`, run against a real Postgres instance with the real `createSqlSafeSoundboardStore`, calling `uploadClip` with `caps.maxDurationSeconds`/`caps.maxByteSize` genuinely `undefined`, asserts the outcome is `'caps_not_configured'` |
| MUH.E2 | The same real-database call inserts zero rows into `channel_soundboard_uploads` — the control is inert, not merely mis-reported |
| MUH.E3 | The test is wired into `packages/db/tests/run-l03-application-behavior.sh`'s Go/TS integration leg, alongside `overlay-wakeup`, `overlay-cross-replica` and `channel-store-concurrency` |

### F. Hard constraints preserved

| ID | Criterion |
|---|---|
| MUH.F1 | `registerMasterCanvasRoutes` positions 10-14 remain `overlayMediaQueue, overlaySafeSoundboard, overlaySponsorCard, overlayQrSmartCard, overlayCanvasLayout` |
| MUH.F2 | `getSubscriberCount()` is unchanged at 16 |
| MUH.F3 | `pnpm harness:check` passes — every route test still constructs Fastify only through `createTestFastify()` |

---

## Commands run

| Command | Result |
|---|---|
| `packages/db/roles/*.sql` + `packages/db/migrations/*.sql` (through 0148) applied to a fresh `postgres:16-alpine` container, then `packages/db/tests/prf02_slice7_media_queue.sql` | pass — "prf02_slice7_media_queue.sql: all assertions passed" |
| `pnpm db:test:all` | sql 72/0 |
| `cd apps/api && npx tsc -p tsconfig.json --noEmit` | 0 errors |
| `cd apps/web && npx tsc --noEmit -p tsconfig.json` | 0 errors |
| `pnpm --filter @bharatstudio/alerts-api test` | api 775/0 |
| `pnpm --filter @bharatstudio/alerts-web test` | web 644/0 |
| `pnpm contracts:validate` | 63 fixtures / 104 paths / 121 operations, 3 negative cases |
| `pnpm explain:check` | 26/26 plans current |
| `pnpm harness:check` | pass |
| `packages/db/tests/run-l03-application-behavior.sh` integration leg (`safe-soundboard-caps-not-configured.integration.ts`) against the throwaway container | see decision record for exact pass/fail — run separately from the numbers above |
