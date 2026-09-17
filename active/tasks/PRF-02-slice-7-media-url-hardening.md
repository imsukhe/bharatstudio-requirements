# PRF-02 slice 7 follow-up — Media Queue URL hardening, and one untested seam

**Status:** `Conditionally complete — implemented and locally verified; independent review unavailable; no register state letter assigned`
**Owner:** **Sukhdev Singh**
**Classification:** L2 (a security-shaped schema/contract fix to an already-shipped table, plus one net-new integration test; no new product surface, no new module)
**Authority:** `../../FULL-PRODUCT-DEFINITION.md` §9.1.1, §19.1, §12.7
**Triggering review:** `../../reviews/2026-09-17-slice-7-hostile-code-review.md` — findings F1 (HIGH) and F4 (LOW). F2, F3 and F5 in that review are explicitly OUT OF SCOPE for this task.
**Acceptance record:** `../../tests/TC-PRF-02-slice-7-media-url-hardening.md`
**Decision record:** `../../reviews/2026-09-17-prf-02-media-url-hardening-implementation.md`
**Parent task:** `PRF-02-slice-7-media-queue.md` (the module this fix amends).

**No register state letter is assigned by this task**, for the same reason the parent slice's task
record names: letters are decided after audit, by the owner, never by an implementer.

---

## What is being fixed

### F1 (HIGH) — the Media Queue rendered arbitrary remote URLs on the Master Canvas

`public.media_queue_items.storage_url` / `thumbnail_url` (migration `0146`) were validated as only
`https://` prefix + length <= 2048 — no host allowlist, no CDN restriction, no signature. A creator
could queue a URL pointing at any host on the internet, and
`apps/web/app/overlay/canvas/modules/media-queue-module.ts` assigned it straight to `<img>`/`<video>`
`.src` at four sites. The `<img>`/`<video>` decode-only argument in that module's own header is
sound — this was never an XSS vector — but §9.1.1 and §19.1 govern *which origin* the canvas
contacts, not only whether that origin can execute code, and a remote host chosen by the creator
still degrades OBS reliability/performance, carries off-brand content, leaks the creator's IP on
every poll, and can swap served bytes after the creator queued them.

**Fix, migration `0148`:** mirrors migration `0143`'s soundboard pattern exactly.
`storage_url`/`thumbnail_url` are replaced by `gcs_object_key`/`thumbnail_gcs_object_key` — content-key
fragments matching `^[A-Za-z0-9/_.-]{1,255}$` with no `..`, a character set structurally incapable of
carrying a scheme or a host. The overlay read now returns the key; resolution to a playable URL
happens exclusively in `apps/api/src/db/media-queue-overlay-store.ts`'s new
`resolveMediaPlaybackUrl(cdnBaseUrl, objectKey)`, against `config.mediaCdnBaseUrl` — the SAME config
value the soundboard overlay store already reads, no second one introduced. That base is CONFIGURED
BUT UNSET in every environment today, so `playbackUrl`/`thumbnailPlaybackUrl` are null for every item
until it is provisioned, and the module renders nothing for a null `playbackUrl` — the Media Queue
now joins the Soundboard in the honest "cannot display media until GCS/CDN exists" posture.

Existing `media_queue_items` rows (a `storage_url` has no lossless mapping to a content-key fragment)
are deleted by migration `0148`, announced by `RAISE NOTICE` with the exact count — expected zero in
every environment this migration runs against today.

### F4 (LOW) — the soundboard's `errcode 55000` -> `caps_not_configured` mapping was untested

`apps/api/src/db/safe-soundboard-store.ts:138` maps Postgres errcode `55000` (raised by
`upload_channel_soundboard_clip` when either duration/byte-size cap is unset) to
`{ outcome: 'caps_not_configured' }`. Covered by neither the SQL suite (stops at SQL) nor the route
tests (stub the store entirely).

**Fix:** `integration/safe-soundboard-caps-not-configured.integration.ts`, following the exact
pattern `integration/channel-store-concurrency.integration.ts` already establishes in this
repository for store-against-real-database coverage — a `BSA_SAFE_SOUNDBOARD_SQL_DSN` env var, a
real `postgres()` connection, the real `createSqlSafeSoundboardStore`, seeded via raw SQL, asserted
with `node:test`. Wired into `packages/db/tests/run-l03-application-behavior.sh` alongside the three
existing Go/TS integration legs.

---

## Hard constraints this task is bound by

1. **Migration number `0148` only.** Nothing renumbered, no other migration touched. `0146`'s own
   text is unmodified — `0148` drops and recreates the three functions whose return shape changed
   (`enqueue_media_queue_item`, `list_channel_media_queue_items`, `list_overlay_media_queue`) and
   leaves `update_media_queue_item`/`set_media_queue_item_status` untouched (they never referenced
   `storage_url`/`thumbnail_url`).
2. **Never invent a numeric limit, price, provider behaviour, legal wording, retention window or
   deployment value.** `config.mediaCdnBaseUrl` is reused verbatim from the soundboard's own anchor
   (`apps/api/src/db/safe-soundboard-overlay-store.ts`); no second CDN-base config value exists.
3. **This is not an XSS fix.** The closed mime allow-list and the `image/svg+xml` exclusion
   (migration `0146`) are unchanged by `0148`.
4. **`registerMasterCanvasRoutes` stays positional**, unchanged shape: positions 10-14 are
   `overlayMediaQueue, overlaySafeSoundboard, overlaySponsorCard, overlayQrSmartCard,
   overlayCanvasLayout`. This task adds no new positional parameter.
5. **`getSubscriberCount()` stays 16.** This task touches no canvas-runtime transport code.

---

## What changed, by file

| Layer | Object |
|---|---|
| Schema | `packages/db/migrations/0148_v1_prf02_slice7_media_queue_url_hardening.sql` |
| SQL test | `packages/db/tests/prf02_slice7_media_queue.sql` (column/shape assertions updated; URL-shaped-value rejection cases added) |
| RT-12 | `packages/db/explain-plans/media-queue.explain.md` re-captured against `0148`'s function body; `required-queries.json`'s note updated |
| API domain | `apps/api/src/domain/media-queue-store.ts` (`gcsObjectKey`/`thumbnailGcsObjectKey` creator-facing, `playbackUrl`/`thumbnailPlaybackUrl` overlay-facing) |
| API db | `apps/api/src/db/media-queue-store.ts`, `apps/api/src/db/media-queue-overlay-store.ts` (new `resolveMediaPlaybackUrl`) |
| API routes | `apps/api/src/routes/media-queue.ts` (AJV `gcsObjectKey` pattern replaces the `storageUrl` https pattern) |
| API wiring | `apps/api/src/index.ts` (`config.mediaCdnBaseUrl` threaded into the media-queue overlay store) |
| API tests | `apps/api/test/prf02-slice7-media-queue-routes.test.ts` |
| Web logic/module | `apps/web/app/overlay/canvas/modules/media-queue-logic.ts`, `media-queue-module.ts`, and both `.test.ts` files |
| Contracts | `contracts/openapi/v1.yaml`, three JSON Schemas, three fixtures under `contracts/json-schema/` and `contracts/fixtures/` |
| Integration (F4) | `integration/safe-soundboard-caps-not-configured.integration.ts`; `packages/db/tests/run-l03-application-behavior.sh` wiring |

---

## Verification run for this task

See `../../tests/TC-PRF-02-slice-7-media-url-hardening.md` for the full criterion table and the
exact commands-run log.
