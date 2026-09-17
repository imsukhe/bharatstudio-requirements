# TC-PRF-02 slice 7 — Safe Soundboard Alert (§6 #6) and the minimum §18 schema: acceptance record

**Date:** 2026-09-17
**Owner:** **Sukhdev Singh**
**Task:** `../active/tasks/PRF-02-slice-7-safe-soundboard.md`
**Implementation review:** `../reviews/2026-09-17-prf-02-slice-7-safe-soundboard-implementation.md`
**Binding owner decision:** `../reviews/2026-09-17-remaining-eight-modules-and-youtube-v1-amendment.md` Part 1 §1

The "Commands run" table at the end is filled in from actual output; this is the single place
this slice's numbers live.

---

## Acceptance criteria

### A. The catalogue half — first-party clips, never tier-gated on the creator's own record

| ID | Criterion |
|---|---|
| SB.A1 | Importing a new catalogue entry returns `created`; an identical re-import returns `skipped`; a changed one returns `updated` — the upsert-by-`external_key` shape 0110's sticker catalogue already established |
| SB.A2 | A malformed object key (a `..` traversal shape) or a non-`audio/*` mime type is refused (`22023`) by `import_soundboard_catalogue_entry` |
| SB.A3 | `list_soundboard_catalogue_for_channel` returns the full catalogue for a **Free-tier** channel — storing/viewing a durable creator record is never tier-gated (§12.6) |
| SB.A4 | Enabling/disabling one entry is owner/admin only (`42501` otherwise) and live on the very next read |

### B. The upload half — no review step, and inert when caps are unset

| ID | Criterion |
|---|---|
| SB.B1 | `upload_channel_soundboard_clip` called with a null duration cap OR a null byte-size cap is refused (`55000`), **regardless of how small the clip is** — unset never means unlimited |
| SB.B2 | A missing or false rights attestation is refused (`22023`) even when caps ARE configured — AUD-06/§18.2 |
| SB.B3 | With both caps configured and a compliant clip, the upload succeeds and its `gcs_object_key` is tenant-scoped and content-addressed (`soundboard/<channel_id>/<sha256>`) |
| SB.B4 | The just-created upload is immediately triggerable with **no intervening step** — proves the no-review-state property behaviourally, not just by column absence |
| SB.B5 | A clip over the configured duration or byte-size cap is refused (`22023`) |
| SB.B6 | A Free-tier channel's upload count limit is zero (§30.3's "Creator sound uploads" row) — refused (`42501`) even for a tiny, compliant clip |
| SB.B7 | No `bytea` column exists on any of the four tables this migration creates — asserted against `information_schema.columns` |

### C. Trigger and the overlay read — latest-supersedes, entitlement on the module only

| ID | Criterion |
|---|---|
| SB.C1 | `trigger_soundboard_play` is owner/admin only; a Studio-floor catalogue entry is refused on a Pro channel (`42501`); a disabled entry is refused (`42501`); exactly one of `catalogue_entry_id`/`upload_id` is required (`22023` for both-null or both-set) |
| SB.C2 | A **Free-tier** channel (unentitled to the module) can still trigger its own catalogue playback — §12.6 |
| SB.C3 | `list_overlay_soundboard_play` returns zero rows for an expired, revoked or mismatched-fingerprint token, and for a foreign channel's token |
| SB.C4 | An **unentitled (Free-tier) channel's** overlay read returns zero rows **even with a real play on record** — the §30.3 Pro+ gate is on the module, proven against a channel that has genuinely triggered something |
| SB.C5 | An entitled (Pro) channel with plays on record returns exactly one row: the most recent |
| SB.C6 | **The returned column set is exactly `{play_id, clip_kind, display_name, gcs_object_key, mime_type, duration_seconds, triggered_at}`** — asserted twice, from `pg_get_function_result` and from a table materialised out of a live call |
| SB.C7 | No viewer/supporter/participant/anonymous/ip/discord/email/phone token exists in the overlay function's own definition |

### D. The word ban — structural, not a comment audit

| ID | Criterion |
|---|---|
| SB.D1 | No shipped `app_private` function body contains `approved`, `checked_by`, `reviewed`, `vetted`, `curated`, `content_rating`, `moderation_state`, `takedown`, `report_`, `auto_scan` or `is_safe` |
| SB.D2 | No column on any of the four tables matches `rating`, `moderat`, `report`, `takedown`, `scan`, `approv`, `review`, `vett` or `curat` |

### E. API route narrowing (second, independent layer)

| ID | Criterion |
|---|---|
| SB.E1 | Overlay: missing bearer → 401; missing store → retryable 503; valid read → exactly `{schemaVersion, soundboardPlay}` with soundboardPlay's 8 declared fields; unrecognised token → 200 with `null`; store failure → retryable 503 |
| SB.E2 | A non-https `playbackUrl` from a (hypothetically polluted) store answer is stripped to `null` by `projectOverlaySoundboardPlay`, never reaches the response |
| SB.E3 | An unknown extra field (`viewerId`, `supporterName`) from a polluted store answer does not survive the projection |
| SB.E4 | An upload body carrying `status`/`moderationState`/`approved`/`reviewed`/`reviewedAt` is a 400 via `additionalProperties: false`, before the store is ever called |
| SB.E5 | With no caps threaded in, the upload route returns 400 `soundboard_uploads_not_configured` |
| SB.E6 | `rightsAttested: false` is schema-valid (a real, explicit request) and the store refuses it with `rights_attestation_required` |
| SB.E7 | A trigger body with both `catalogueEntryId` and `uploadId`, or neither, or a `supporterId` field, is a 400 via the `oneOf` schema |

### F. Canvas renderer — pure, bounded, composite-only

| ID | Criterion |
|---|---|
| SB.F1 | `isOverlaySoundboardPlay` rejects a non-https `playbackUrl` (any other scheme, including `javascript:`/`data:`) and any extra key |
| SB.F2 | A repeated poll of the same `playId` does not start a second `Audio` playback (`isNewPlay`) |
| SB.F3 | A different `playId` while the caption is showing supersedes the previous trigger |
| SB.F4 | A null `playbackUrl` (unconfigured CDN base) still shows the caption with zero audio calls |
| SB.F5 | An `Audio.play()` rejection (autoplay refusal) never throws past the module's `render()` |
| SB.F6 | `deactivate()` is idempotent and stops any current audio |
| SB.F7 | `canvas-static-check.mjs` finds a per-frame `render()` scope and only `transform`/`opacity`/text-content writes in it |

---

## Commands run

| Command | Result |
|---|---|
| `sh packages/db/tests/run-sql-suite.sh` | **68/0** (67 baseline + `prf02_slice7_safe_soundboard`) |
| `pnpm --filter @bharatstudio/alerts-api exec tsc -p tsconfig.json --noEmit` | **0 errors** |
| `pnpm --filter @bharatstudio/alerts-api test` | **709/0** (692 baseline + 17 new) |
| `npx tsc -p apps/web/tsconfig.json --noEmit` | **0 errors** |
| `pnpm --filter @bharatstudio/alerts-web test` | **577/0** (560 baseline + 17 new) |
| `node contracts/validate-fixtures.mjs` | **54 fixtures** (50 baseline + 4 new), pass |
| `node contracts/validate-openapi.mjs` | **93 paths / 106 operations** (88/100 baseline + 5 paths / 6 ops), pass |
| `node contracts/test-openapi-validator.mjs` | 3 negative cases, pass |
| `node packages/db/explain-plans/scan-required-queries.mjs` | pass, 22 manifest entries |
| `node packages/db/explain-plans/check-plans.mjs` | **22/22** plans current |
| `node .github/scripts/api-test-harness-check.mjs` | pass |
| `node .github/scripts/canvas-static-check.mjs` | pass |
| `pnpm harness:check` | pass |

All numbers above were run by the implementing agent on the merged local tree, not taken from
narration. **Independent review unavailable** — this slice stays `Conditionally complete`.
