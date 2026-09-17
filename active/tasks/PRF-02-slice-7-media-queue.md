# PRF-02 slice 7 — Media / Meme Queue (§6 catalogue module #20)

**Status:** `Conditionally complete — implemented and locally verified; independent review unavailable; no register state letter assigned`
**Owner:** **Sukhdev Singh**
**Classification:** L3 (new database objects, a new creator write path, a new overlay read path, a load-bearing product-safety boundary — no viewer submission)
**Authority:** `../../FULL-PRODUCT-DEFINITION.md` §6 module #20, §9.1.1, §12.6, §12.6.2, §12.7, §19.1, §30.3, `MED-20`, `MED-21`
**Binding owner decision:** `../../reviews/2026-09-17-remaining-eight-modules-and-youtube-v1-amendment.md` Part 1 §8 ("Media / Meme Queue (§6 #20): creator-only, and `MED-20` says so")
**Acceptance record:** `../../tests/TC-PRF-02-slice-7-media-queue.md`
**Decision record:** `../../reviews/2026-09-17-prf-02-slice-7-media-queue-implementation.md`
**Parent task:** `PRF-02.md`. Recorded in its own file, with `media-queue`/`slice-7` in every record
name, because this slice runs concurrent with other agents building other §6 modules.

**No register state letter is assigned by this task.** `PRF-02`'s and `MED-20`'s letters are decided
after audit, by the owner, never by an implementer. `MED-20` is written by this task's own migration
comment and this record — it previously carried no content.

---

## What is being built

A complete vertical slice of §6 catalogue module #20, **Media / Meme Queue**: the creator queues
their own media (images, GIFs, short video clips) and the overlay shows the current item, preloading
the next one. **Viewers cannot submit.** Nothing else — no approval queue, no viewer-facing surface
of any kind.

| Layer | Object |
|---|---|
| Schema | `packages/db/migrations/0146_v1_prf02_media_queue.sql` — **migration number pre-assigned to this task**, never renumbered, migrations directory never globbed |
| Creator writes | `app_private.enqueue_media_queue_item`, `update_media_queue_item`, `set_media_queue_item_status` — all owner/admin, none tier-gated |
| Creator reads | `app_private.list_channel_media_queue_items(uuid, integer)` — any channel member, never tier-gated, paginated (cap 100, reused from migration `0137`'s cursor-safety ceiling) |
| Overlay read | `app_private.list_overlay_media_queue(uuid, text)` — **at most two rows** ("current"/"next"), no per-module entitlement gate (§30.3 names none for this module; only 0131's existing module-wide cap applies) |
| API | `GET/POST /v1/channels/:channelId/media-queue`, `PATCH .../media-queue/:itemId`, `PATCH .../media-queue/:itemId/status`, and `GET /v1/overlay-widgets/:overlayId/media-queue` |
| Contracts | OpenAPI paths + components, three JSON Schemas, three fixtures |
| RT-12 | `packages/db/explain-plans/media-queue.explain.md` and a `required-queries.json` entry |
| Canvas | `modules/media-queue-logic.ts` and `modules/media-queue-module.ts`, on the ONE existing connection and the ONE existing rAF loop; registered as module thirteen of thirteen |
| Tests | SQL (`packages/db/tests/prf02_slice7_media_queue.sql`), API route (`apps/api/test/prf02-slice7-media-queue-routes.test.ts`, via the shared `createTestFastify()`), pure-logic, renderer and canvas-integration layers |

---

## The load-bearing constraint this slice is bound by

Quoted from the owner decision, not relitigated:

> "The creator queues their own media. VIEWERS CANNOT SUBMIT." Viewer submission would make
> BharatStudio a host of viewer-supplied media at broadcast volume — the same rights, storage and
> takedown posture as the §6 #6 soundboard uploads, but at far higher volume and with no
> relationship to the person submitting. Creator-only has none of that.

**NOT AUTHORISED, and none of it exists anywhere in this slice:** a submission endpoint, an approval
queue, a viewer-facing surface of any kind, a moderation queue, a rejection reason, a submitter
identity field. Adding any of these is a NEW decision, not an extension.

**Proven structurally, not by convention.** `packages/db/tests/prf02_slice7_media_queue.sql`'s
`MED20.1` scans every function this migration ships for `submit`, `submission`, `submitter`,
`viewer_id`, `approve`, `approval` and `reject`, and separately scans `information_schema.columns`
and `information_schema.tables` for any matching column or a second submission table. A grep of this
slice's own diff for the same seven tokens finds them ONLY inside comments/documentation and inside
JSON-schema/AJV bodies that explicitly REJECT such a field with a 400 — never as an actual column,
function name, route path or object key. See the decision record for the exact grep output.

---

## Other hard constraints this slice is bound by

1. **§19.1, metadata only.** `storage_url` / `thumbnail_url` point at an already-hosted GCS/CDN
   asset; there is no `bytea` column anywhere in migration `0146` (`MED-21`: the `bytea` path is
   legacy, kept only as the rollback route, and this module never uses it).
2. **§9.1.1, no third-party code.** `mime_type` is a closed allow-list (image/png, image/jpeg,
   image/webp, image/gif, video/mp4, video/webm) — no `text/html`, no `image/svg+xml`, no
   `application/*`. The renderer hands `storageUrl`/`thumbnailUrl` only to an `<img>`/`<video>`
   `src`, never to a script, an iframe or a stylesheet.
3. **§12.6, never tier-gated.** Storing, viewing, editing and changing the status of a durable
   creator record is available at every tier; the only gate on any creator-facing function is the
   role gate (`app_private.has_channel_role`). What §30.3-style module caps decide is whether the
   Canvas renders the module — the existing, untouched, module-wide "Master Canvas modules active"
   cap from migration `0131`, which already listed `media_meme_queue` as one of its twenty catalogue
   keys before this slice touched anything.
4. **§12.6.2, uniform retention.** No per-row expiry, no tier-scoped retention window, no purchase of
   additional retention — a Storage Pack "sells space for new uploads only" and never buys back
   access to anything historical.
5. **§12.7, current and next, never a queue depth.** The overlay read returns AT MOST TWO rows,
   reusing the exact bound `apps/web/app/overlay/canvas/modules/support-theater-module.ts:68-72`
   already established for this codebase, rather than inventing a queue-depth number of its own.
6. **Never invent a numeric limit.** Title length reuses migration `0109`'s 1–120 bound verbatim.
   Media duration and the maximum number of items a channel may queue at once have no decided value
   and no honest reuse anchor, so both ship **configured but unset** (`apps/api/src/config.ts`'s
   `mediaQueueMaxItemDurationMs` / `mediaQueueMaxItemsPerChannel`, mirroring the existing
   `reactionCloudSampleMax` posture) — unset means today's behaviour, never a guessed default.

---

## Where the line against a larger §6 #20 surface was drawn

| Possible feature | In / out | Why |
|---|:-:|---|
| Creator queues their own media (image/gif/video) | **in** | The owner's decision names exactly this |
| Creator edits title / pauses an item (`enabled`) | **in** | A durable creator record the creator may always change (§12.6) |
| Creator marks an item played/skipped | **in** | Playback lifecycle only — never a moderation decision |
| Overlay shows the current item, preloads the next | **in** | §12.7's "current and next", reused from the existing bound |
| Viewer submission endpoint | **out** | Explicitly forbidden by the owner decision (`MED-20`) |
| Approval / moderation queue | **out** | Explicitly forbidden — "naming a queue nobody staffs" reasoning is the sibling Soundboard module's, applied here even more directly since there is no submission to approve at all |
| Rejection reason field | **out** | Explicitly forbidden |
| Reordering the queue | **out** | Not named in the owner decision; FIFO order by `created_at` is what ships, and reordering is a new product surface, not an extension |
| A queue-depth / total-count display | **out** | §12.7's reused bound is "current and next", not a count |
| A GCS upload pipeline of its own | **out** | §19.1's transcode/normalise/import pipeline is register item `INT-07` (`new-record-required`), a separate, unbuilt capability; this slice assumes an asset already has a URL by the time it reaches `enqueue_media_queue_item`, the same posture migration `0123`'s `attach_provider_qr` takes for an already-hosted QR image |

---

## Verification

Every command and its exact result line is recorded in the acceptance record
`../../tests/TC-PRF-02-slice-7-media-queue.md`.

**Local verification only.** Nothing here is production, provider, store, legal, device, network or
release readiness. `RT-07` remains `Blocked`; the EXPLAIN artefact is a plan-shape change detector
captured against a minimally-seeded local database (102 channels, 400 media queue items, 100 overlay
sessions), not §37.4 production-scale evidence.

---

## Referred to the owner

- **The two configured-but-unset caps (media duration, queue-item count) have no decided value.**
  Both ship as deployment configuration only, enforced when set and imposing no ceiling when unset.
  Deciding an actual number — and whether it should differ by tier, which §12.6 would forbid for
  storage but not necessarily for a canvas-render cap — is the owner's, not an implementer's.
- **Reordering the queue was not asked for and is not built.** If the product wants a creator to
  reorder queued items rather than only relying on FIFO order, that is a new decision.
