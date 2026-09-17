# PRF-02 slice 7 — Safe Soundboard Alert (§6 catalogue module #6) and the minimum §18 schema

**Status:** `Conditionally complete — implemented and locally verified; independent review unavailable; no register state letter assigned`
**Owner:** **Sukhdev Singh**
**Classification:** L3 (new database objects, new creator write paths, a new overlay read path, a rights/liability-adjacent upload boundary)
**Authority:** `../../FULL-PRODUCT-DEFINITION.md` §6 module #6, §9.1.1, §12.6, §12.6.2, §12.7, §18 (in full — §18.1, §18.2), §19.1, §30.3, `AUD-03`, `AUD-06`
**Binding owner decision:** `../../reviews/2026-09-17-remaining-eight-modules-and-youtube-v1-amendment.md` Part 1 §1
**Acceptance record:** `../../tests/TC-PRF-02-slice-7-safe-soundboard.md`
**Implementation review:** `../../reviews/2026-09-17-prf-02-slice-7-safe-soundboard-implementation.md`

**No register state letter is assigned by this task.** Letters are decided after audit, by the
owner, never by an implementer.

---

## What is being built

A complete vertical slice of §6 catalogue module #6, **Safe Soundboard Alert**, plus the minimum
schema needed to source it from two places and render one trigger.

| Layer | Object |
|---|---|
| Schema | `packages/db/migrations/0143_v1_prf02_safe_soundboard.sql` — **migration number assigned to this task**; `0144`, `0145`, `0146` are held concurrently by other agents, never written here, nothing renumbered |
| Tables | `soundboard_catalogue_entries`, `channel_soundboard_disables`, `channel_soundboard_uploads`, `channel_soundboard_plays` — metadata only, no `bytea` column anywhere (§19.1) |
| Functions | `soundboard_tier_rank`, `soundboard_upload_tier_limit`, `soundboard_module_entitled`, `import_soundboard_catalogue_entry`, `list_soundboard_catalogue_for_channel`, `set_channel_soundboard_catalogue_enabled`, `list_channel_soundboard_uploads`, `upload_channel_soundboard_clip`, `trigger_soundboard_play`, `list_overlay_soundboard_play` |
| API domain | `apps/api/src/domain/safe-soundboard-store.ts` |
| API stores | `apps/api/src/db/safe-soundboard-store.ts` (main pool, creator writes/reads), `apps/api/src/db/safe-soundboard-overlay-store.ts` (derivedReadSql, overlay read + CDN URL resolution) |
| API routes | `apps/api/src/routes/safe-soundboard.ts` (catalogue list/toggle, upload list/create, trigger play); overlay read wired into `apps/api/src/routes/master-canvas.ts` |
| Config | `apps/api/src/config.ts` — `SOUNDBOARD_UPLOAD_MAX_DURATION_SECONDS`, `SOUNDBOARD_UPLOAD_MAX_BYTES`, `MEDIA_CDN_BASE_URL`, all configured-but-unset by default |
| Contracts | OpenAPI 6 operations (1 overlay + 5 creator), 4 JSON-Schemas, 4 fixtures |
| RT-12 | `packages/db/explain-plans/safe-soundboard.explain.md` and a `required-queries.json` entry |
| Canvas | `apps/web/app/overlay/canvas/modules/safe-soundboard-logic.ts` and `safe-soundboard-module.ts`, registered in `apps/web/app/overlay/canvas/[overlayId]/page.tsx` on the ONE existing connection and the ONE existing rAF loop |
| Tests | SQL (`packages/db/tests/prf02_slice7_safe_soundboard.sql`), API route (`apps/api/test/prf02-slice7-safe-soundboard-routes.test.ts`), pure-logic and renderer (both `.test.ts` files beside their source) |

---

## The decision this slice implements, quoted as constraints

None was decided by this implementer, none is extended, none is relitigated.

1. **Two sources.** A first-party clip set BharatStudio authors and imports, **and** creator
   uploads. Both play; neither is a placeholder for the other.
2. **No review step for a creator's own upload, ever.** A row in `channel_soundboard_uploads` is
   immediately triggerable. There is no `status`, `moderationState`, `approved` or `reviewedAt`
   column or field anywhere in this slice, and none may be added without a new decision.
3. **The name is about the broadcast, not the content.** No UI copy, schema comment (other than
   the migration's own explanatory prose, which discusses the ABSENCE of review), API field or
   test name may claim a clip is safe, approved, checked, reviewed, vetted or curated.
4. **Not authorised:** a takedown flow, a reporting surface, automated content scanning, any
   content-rating field. None exists; the SQL test asserts this structurally against every
   shipped function body and against every column name.
5. **Duration and file-size caps ship configured but unset.** No decided value exists anywhere in
   the register for a per-clip cap. `upload_channel_soundboard_clip` refuses every upload when
   either cap parameter is null — unset never means unlimited. First-party catalogue import takes
   no cap parameter and is unaffected.
6. **Cooldown ships configured-but-unset too**, because no cooldown value is decided anywhere in
   this repository. `trigger_soundboard_play` applies no rate limit.
7. **§12.6: never tier-gate the creator's own record.** Every creator-facing route in
   `routes/safe-soundboard.ts` is available at every tier. The §30.3 Pro+ module gate
   (`soundboard_module_entitled`) and the per-tier upload-count ladder (`soundboard_upload_tier_limit`,
   reused verbatim from the already-decided §30.3 "Creator sound uploads" row: Free 0 / Pro 5 /
   Creator 25 / Studio 100) live only where §30.3 actually says they apply.
8. **§19.1: GCS/CDN, metadata only.** No `bytea` column anywhere in this migration. `gcs_object_key`
   is a narrow-character-set, content-addressed key fragment; the API resolves it against the
   server's own configured CDN base, never a caller-supplied URL.
9. **AUD-06 / §18.2 reused, not invented.** A positive rights attestation with a recorded
   timestamp is required on every upload — a decided, cross-cutting requirement for creator audio
   uploads, applied here rather than re-litigated.

---

## What is deliberately NOT built, and why

- **Supporter-triggered playback (AUD-03).** The 2026-09-17 decision authorises sourcing and the
  no-review-upload rule for module #6; it does not authorise a new payment-attached trigger
  surface. Building one would be scope creep with real payment-adjacent consequences. Every
  trigger in this slice is the creator's own, session-authenticated action.
  `apps/api/src/routes/safe-soundboard.ts`'s `POST .../soundboard/play` and the SQL function
  `trigger_soundboard_play` are both structured so a future supporter-attach flow (mirroring
  0110's `attach_sticker_to_tip`) can be added beside them without a redesign, but nothing here
  builds it.
- **A never-drop multi-item queue.** `list_overlay_soundboard_play` returns the single most recent
  trigger, matching every other Master Canvas card's poll-based, non-mutating overlay-read shape
  (no write happens on the `derivedReadSql` pool). The overlay client de-duplicates by `playId`
  rather than consuming an acknowledged queue. Recorded as an open item in migration 0143's own
  header, not hidden.
- **Real GCS byte storage.** No object-storage SDK is wired in this repository at any layer, and
  none is added here. Because the upload caps are configured-but-unset, no upload can reach a byte
  -persistence step today regardless — the schema, the cap-gating mechanism and the metadata model
  are complete and correct; the actual `PUT` to GCS when caps are eventually set is a follow-up,
  named explicitly in the review record's blockers.
