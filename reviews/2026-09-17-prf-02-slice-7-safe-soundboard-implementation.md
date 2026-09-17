# Review — PRF-02 slice 7 implementation (Safe Soundboard Alert, §6 module #6)

**Date:** 2026-09-17
**Owner:** Sukhdev Singh
**Reviewer:** Implementing agent, self-review. **Independent review unavailable** — no second
reviewer ran against this build, and per `governance/AGENTS.md` this slice is therefore left
`Conditionally complete`, not complete.
**Scope authority:** `2026-09-17-remaining-eight-modules-and-youtube-v1-amendment.md` Part 1 §1 —
a standalone, persisted owner decision, read before any code was written.
**Task record:** `../active/tasks/PRF-02-slice-7-safe-soundboard.md`
**Acceptance record:** `../tests/TC-PRF-02-slice-7-safe-soundboard.md`
**Register:** No state letter self-assigned.

## What was built

§6 module #6, **Safe Soundboard Alert**, as a complete vertical slice: migration `0143` (four
tables, ten functions), the creator-facing routes in `routes/safe-soundboard.ts`, the overlay
route wired into `routes/master-canvas.ts`, config-driven (and today unset) upload caps and CDN
base URL, OpenAPI/JSON-Schema/fixtures for all six operations, the RT-12 manifest entry and a
captured EXPLAIN artefact, and the canvas renderer registered on the one existing connection and
the one existing rAF loop. File list and per-case evidence live in the task and acceptance
records; not repeated here.

## The decision, and how each part is enforced rather than promised

1. **Two sources, one playback path.** `soundboard_catalogue_entries` (first-party) and
   `channel_soundboard_uploads` (creator's own) are separate tables with no shared status
   column; `trigger_soundboard_play` accepts exactly one of `catalogue_entry_id`/`upload_id` and
   the SQL test (case SB.C1) proves both-null and both-set are refused.
2. **No review step, proven behaviourally, not just by column absence.** Case SB.B4 uploads a
   clip and triggers it in the same transaction with no intervening call. There is no
   `status`/`moderationState`/`approved`/`reviewedAt` column on `channel_soundboard_uploads` at
   all -- asserted in case SB.B7's sibling column-name scan (SB.D2) -- so there is nothing for a
   future write to set to "pending" even by accident.
3. **The word ban.** Case SB.D1 scans every shipped `app_private` function's `pg_get_functiondef`
   output for `approved`, `checked_by`, `reviewed`, `vetted`, `curated`, `content_rating`,
   `moderation_state`, `takedown`, `report_`, `auto_scan`, `is_safe`. Case SB.D2 scans every
   column name on the four new tables for `rating`, `moderat`, `report`, `takedown`, `scan`,
   `approv`, `review`, `vett`, `curat`. Both pass today. The migration's own header prose DOES use
   words like "review" and "vetted" -- always to say what is absent, never to claim a clip is any
   of them, which is the distinction the 2026-09-17 decision draws.
4. **Caps configured but unset, and unset means inert, not unlimited.** Case SB.B1 calls
   `upload_channel_soundboard_clip` with a null duration cap and, separately, a null byte-size
   cap, each against a 1-byte/1-second clip -- both refused with `55000`. The route layer never
   even reaches the store when `SOUNDBOARD_UPLOAD_MAX_*` env vars are unset (`config.ts`'s
   `optionalPositiveInt`, no `??` fallback), so the inert behaviour is enforced twice.
5. **§30.3's upload count ladder and module gate are reused numbers, not invented ones.** Free
   0 / Pro 5 / Creator 25 / Studio 100 come from `FULL-PRODUCT-DEFINITION.md`'s §30.3 table row
   "Creator sound uploads" verbatim; "Sound Moments (catalogue)" being Pro+ is the same table's
   row for module availability. Case SB.B6 proves the Free-tier ladder floor; case SB.C4 proves
   the module gate against a channel that has genuinely triggered a play.
6. **§19.1 metadata-only, enforced structurally.** Case SB.B7 asserts no `bytea` column exists on
   any of the four tables. `gcs_object_key`'s check constraint keeps §9.1.1's "no field capable
   of carrying a third-party URL" true -- verified case SB.A2 against a traversal-shaped key.

## The negative test of the privacy property

Required by the task, run rather than reasoned about, same method the slice 5 and slice 6
implementation reviews used: temporarily widen `app_private.list_overlay_soundboard_play` to leak
a column, run the SQL suite, observe the failure, restore, re-run.

**The deliberate break.** The declared result type was widened to add
`leaked_channel_id uuid` and the select list extended with `play.channel_id` -- exactly the
class of thing this module forbids on the overlay path: a channel/session-correlating
identifier leaving the database over an aggregate-only read.

**Output with the break in place:**

    FAIL prf02_slice7_safe_soundboard
         ERROR:  the overlay soundboard read must return exactly the seven declared columns and
         nothing else. Declared result is "TABLE(play_id uuid, clip_kind text, display_name text,
         gcs_object_key text, mime_type text, duration_seconds integer, triggered_at timestamp
         with time zone, leaked_channel_id uuid)"
    SQL SUITE: pass=67 fail=1
    failed: prf02_slice7_safe_soundboard

**Output after restoring the function unchanged:**

    PASS prf02_slice7_safe_soundboard
    SQL SUITE: pass=68 fail=0

`node packages/db/explain-plans/check-plans.mjs` was re-run after the restore and reported
`OK: 22/22 plans current`, which independently confirms the restored function body is
byte-identical to the one the captured EXPLAIN artefact hashes.

## Verification and what it is worth

Commands and counts are in `../tests/TC-PRF-02-slice-7-safe-soundboard.md`. Every one of them ran
locally -- the Node test runner, jsdom, and a local Dockerised PostgreSQL 16.

**None of it is production, provider, store, legal, device, network or release readiness, and
none of it may be represented as any of those.** The EXPLAIN artefact is a plan-shape change
detector captured on a locally-seeded database (101 channels, 500 plays); it says so in its own
body and is not evidence any §19.4 budget is met. RT-07 stays Blocked.

## Things a reader should be sceptical of, stated rather than buried

- **Self-review only.** Nobody independent looked at this.
- **No real object storage is wired.** No GCS/CDN SDK exists anywhere in this repository at any
  layer, before or after this slice. Because the upload caps are unset in every environment
  today, no request can reach a byte-persistence step regardless -- but when a cap value is
  eventually decided, `upload_channel_soundboard_clip`'s TypeScript caller
  (`safe-soundboard-store.ts`'s `uploadClip`) still needs an actual object-storage PUT wired in
  front of it before an upload can complete end to end. That wiring is not built here and is
  named as this slice's own primary blocker, not hidden inside "configured but unset."
- **AUD-03 (supporter-triggered playback) is explicitly not built.** The owner decision this
  slice implements authorises sourcing and the no-review-upload rule for module #6; it does not
  authorise a new payment-attached trigger. Every trigger in this slice is the creator's own. A
  future tip-attached trigger (mirroring 0110's attach_sticker_to_tip) was designed AROUND --
  trigger_soundboard_play takes a channel id and a source, not a caller identity -- but nothing
  here builds the supporter-facing half.
- **The "queue" is latest-supersedes, not a never-drop FIFO.** §6's catalogue row text says "with
  cooldown and queue". No cooldown value is decided anywhere in this repository, so none is
  applied. The queue is a single-most-recent-trigger overlay read, matching every other Master
  Canvas card's shape; a genuine multi-item, never-drop queue was not built and would need either
  a decided display-depth bound or a write path on the overlay's read-only derivedReadSql pool,
  neither of which exists today. Recorded in migration 0143's own header, not hidden here.
- **The CDN base URL is unset in every environment**, so playbackUrl is null for every clip on
  the live API today, first-party catalogue included. The schema, cap-gating and metadata model
  are complete; the URL only resolves once MEDIA_CDN_BASE_URL is provisioned.
- **Concurrency.** Three other agents own migrations 0144-0146 in parallel. This slice wrote
  0143 only, renumbered nothing, and did not read those migrations as authority.

## Word-ban check

Grepped this slice's own files for safe/approved/checked/reviewed/vetted/curated used as a truth
-claim. No match as a field, column, API value or user-facing copy. Every occurrence elsewhere in
these files is explanatory prose stating that a claim is NOT made (the module's own historical
name included) -- see the acceptance record's cases SB.D1/SB.D2 for the structural version of
this same check, run against the shipped SQL rather than grepped by hand.

## Referred to Opus

- **Real GCS/CDN wiring.** No object-storage SDK exists in this codebase. Standing this up (a
  bucket, tenant-scoped keys, signed-URL issuance, the actual PUT from the upload route) is
  infrastructure work outside a single migration slice's scope and needs its own decision on
  which provider client and credential model to use.
- **AUD-03, supporter-triggered playback.** A new decision, not an extension of this one -- needs
  its own review of the payment-attachment shape (mirroring 0110 or something new) and whether a
  cooldown value should be decided alongside it.
- **A cooldown value**, if and when one is decided, so trigger_soundboard_play can enforce it the
  same window-plus-counter shape channel_reaction_rate_limits (migration 0139) already uses.
