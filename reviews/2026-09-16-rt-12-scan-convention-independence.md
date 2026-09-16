# Review — RT-12 scan convention-independence, classification of the seven

**Date:** 2026-09-16
**Owner:** Sukhdev Singh
**Scope:** `bharatstudio-alerts` — `packages/db/explain-plans/`, `packages/db/tests/`. No
`apps/web/`, `.github/`, `scripts/`, or `apps/api/src/observability/` touched, per this task's
own boundary (concurrent review-only agents were running on the overlay frontend and on
CI/observability at the same time). `apps/api/src/db/` was read, not edited.

## The defect

`RT-12`'s row (`FULL-PRODUCT-DEFINITION.md` §31.18.0) asks for a checked-in `EXPLAIN` artefact
for "every widget-backing query." `packages/db/explain-plans/scan-required-queries.mjs`
enforced that only for functions named `app_private.list_overlay_*` — a naming-convention
scan, not a real analysis of what actually backs an overlay-facing surface.

Opus enumerated every distinct `app_private.*` call in the seven dedicated overlay-facing
store files:

```
apps/api/src/db/{challenge-overlay-store,goal-overlay-store,master-canvas-sql-store,
overlay-audio-store,overlay-branding-store,overlay-store,overlay-wakeup}.ts
```

Twelve distinct functions. Five in the manifest. Seven not, none matching `list_overlay_*`:
`ack_overlay_cursor`, `can_access_channel`, `get_overlay_events`, `get_overlay_lottie_asset`,
`get_overlay_tts_audio`, `lookup_overlay_token`, `upsert_master_canvas_module`. Verified
directly by grepping each of the seven files for `app_private\.` — the count and the seven
names both check out exactly as given.

## Why `get_overlay_events` had no artefact

It doesn't follow the `list_overlay_*` convention because
`packages/db/migrations/0127_v1_rt02_overlay_events_artifact_column.sql` had to
`DROP FUNCTION app_private.get_overlay_events(...)` and then `CREATE FUNCTION` it fresh (not
`CREATE OR REPLACE`) to add an OUT column, `tts_audio_artifact_id` — PostgreSQL refuses
`CREATE OR REPLACE FUNCTION` across an OUT-column change. The function's *name* never
changed; only how it had to be redefined did. A naming-convention scan was never going to
catch this — the function's name has always violated the convention it was measured against,
since well before this task existed.

This also broke `check-plans.mjs`'s extraction regex once `get_overlay_events` was added to
the manifest: it matched only `^create or replace function `, and 0127's definition line is
`create function app_private.get_overlay_events(`. Widened to
`^create (?:or replace )?function `. Verified the widening changes nothing for the other
fifteen artefacts — every one of their migration lines still starts with
`create or replace function `, and `pnpm explain:check` reports all fifteen unchanged plus the
new one current.

## The fix: two rules, not one

`scan-required-queries.mjs` now runs two independent checks:

1. **Convention scan (kept).** Every `app_private.list_overlay_*` call anywhere in
   `apps/api/src/db/*.ts` or `apps/api/src/routes/*.ts` must be manifested. This is still
   useful: `interaction-sql-store.ts` and `vote-payment-sql-store.ts` are mixed-purpose files
   (creator-facing config management *and* several `list_overlay_*` widget reads) that rule 2
   deliberately does not scan, since sweeping every `app_private` call in a file like
   `interaction-sql-store.ts` into scope would pull in a dozen unrelated creator-facing writes
   (`create_interaction_definition`, `start_hype_mode`, etc.) that this task was never asked
   to classify and that are not overlay-facing at all. Rule 1 is what keeps those files'
   genuinely overlay-facing functions covered without that blast radius.
2. **Convention-independent scan (new).** Within files under `apps/api/src/db/` whose
   basename matches `/overlay|master-canvas/i`, **every** `app_private.<fn>(` call, any name,
   must be in the manifest or a written-reason exemption. This is the rule that actually finds
   `get_overlay_events` and the other six, because it does not care what they are named.

**Why filename, not a hand-typed path list.** The task said not to hard-code the seven paths,
and to make the rule keep working when an eighth overlay store is added. The seven files
split cleanly on filename: six contain "overlay," and the seventh, `master-canvas-sql-store.ts`,
contains "master-canvas" — it exports both a channel-facing store
(`createSqlMasterCanvasStore`) and an overlay-facing one (`createSqlMasterCanvasOverlayStore`,
type `MasterCanvasOverlayStore`), and PRF-02's Master Canvas is specifically what the overlay
renders, so it belongs in the overlay-facing set even without "overlay" literally in its name.
Checked against every filename in `apps/api/src/db/` (57 files) — the regex matches exactly
these seven, no false positives, no false negatives, at the time this was written.

**Why rule 2 does not also scan `apps/api/src/routes/`.** Checked directly: `routes/master-canvas.ts`'s
only `app_private` text is a comment reference, not a call; `routes/overlay.ts`,
`routes/overlay-audio.ts`, `routes/overlay-lottie.ts` have zero `app_private` occurrences at
all. Every actual call lives in the store files. Extending rule 2 to routes/ today would find
nothing and would be untested breadth; if a future route ever calls `app_private` directly,
that is worth revisiting deliberately rather than defended against speculatively now.

## Classification of the seven — judged individually, not as a batch

The task was explicit: judge each on what it does, exempt only with a reason, and manifest
anything uncertain rather than risk a false negative. Read each function's current migration
definition directly (not inferred from its name) before deciding:

| Function | Defined at | Disposition | Reason |
|---|---|---|---|
| `get_overlay_events` | `0127_v1_rt02_overlay_events_artifact_column.sql:33` | **Manifested** | Multi-join read (event_outbox_deliveries / event_outbox / alert_events / channel_configs / alert_tts_audio / overlay_sessions / alert_queues / channel_entitlement_versions) serving the alert stream — the query the overlay's SSE replay runs on every wake, for every session. The single hottest overlay read in the product; more load-bearing than any widget query already in the manifest. |
| `lookup_overlay_token` | `0003_v1_l03_application.sql:262` | Exempt | `select session.id, session.channel_id, session.expires_at from overlay_sessions where id = ... and token_fingerprint = ... and revoked_at is null and expires_at > now() limit 1` — a token-validity lookup, not a widget read. Called as the admission check before every overlay read (RT-02 §3.2(a)), returning session/channel identity only. |
| `can_access_channel` | `0002_v1_security_rls_archive.sql:67` | Exempt | `returns boolean`, delegates to `has_channel_role`. Used only in the WHERE clause of `overlay-store.ts`'s creator-facing session revoke/rotate mutations — an auth predicate gating a write, not a read serving overlay content. |
| `ack_overlay_cursor` | `0022_v1_l05_overlay_ack_release.sql:46` (latest; also defined 0003) | Exempt | `language plpgsql volatile` — inserts/updates `overlay_cursors`, transitions a delivery to `acknowledged`, calls `refresh_event_outbox_status`. A write; returns boolean, not rows a widget renders. |
| `upsert_master_canvas_module` | `0131_v1_prf02_master_canvas_modules.sql:86` | Exempt | `language plpgsql volatile` — owner/admin-gated insert-or-update of a module's `enabled` flag, returns the module id. A write. The read that renders from this state, `list_overlay_master_canvas_modules`, is already manifested (`master-canvas-modules-overlay.explain.md`). |
| `get_overlay_tts_audio` | `0067_v1_l03_tts_event_enrichment.sql:166` | Exempt | Single-row fetch keyed on `artifact.id = target_artifact_id` (plus session/token re-check) — the overlay's own separate byte-serving fetch for one delivery's TTS playback, not an aggregate or list a widget renders from. The read that surfaces which artifact id to fetch, `get_overlay_events`, is manifested above. |
| `get_overlay_lottie_asset` | `0077_v1_l03_lottie_branding_upload.sql:200` | Exempt | Single-row fetch keyed on `asset.id = target_artifact_id`, same shape as `get_overlay_tts_audio`. Its own migration comment calls it out explicitly: "The byte-serving path an individual overlay-lottie route fetches by artifact id" — distinguished by the migration's own author from the enumerating list, `list_overlay_lottie_assets`, which is already manifested (`lottie-assets.explain.md`). |

No function was exempted on a name-shape guess; each disposition above cites the actual `SELECT`/
mutation body read directly out of its migration file. `get_overlay_events` was the only one of
the seven judged to be a genuine widget-backing read; the other six split cleanly into two
auth/predicate lookups, two writes, and two single-row byte-serving fetches whose companion
list queries were already covered.

## Closed or narrowed

**Narrowed, not eliminated.** See `tests/TC-RT-12-explain-plans.md`'s 2026-09-16 update and
`scan-required-queries.mjs`'s own header for the full three-item list of what can still slip
past: (1) a genuinely overlay-facing function in a file whose name matches neither `overlay`
nor `master-canvas` and that also doesn't follow `list_overlay_*` — the filename-convention
descendant of the gap just closed; (2) a call reached only through indirection (none observed
today); (3) whether a function is genuinely widget-backing versus exempt-worthy remains a
human judgement made once per function, not machine-verified — the written-reason requirement
makes a bad exemption reviewable, not impossible.

## Checks run

From `bharatstudio-alerts`: `pnpm explain:check` — `OK` (16 manifest entries, 6 exemptions)
then `OK: 16/16 plans current`. `pnpm db:test:all` — 59/0 (baseline 59/0). `pnpm db:test:l03` —
passed. `pnpm --filter @bharatstudio/alerts-api build` — clean. `pnpm --filter
@bharatstudio/alerts-api test` — 585/0 (baseline 585/0). `git diff --check` — clean. Negative
cases (manifest-entry removal, unmanifested-call addition) both exercised and reverted; `git
status`/`git diff` confirmed the revert left no trace.

No migration was written or needed — the fix is entirely in the scan/check scripts and the
manifest; `get_overlay_events`'s SQL definition already existed and did not change.

Local plans are never performance evidence (§35.1 rule 6). RT-07 remains Blocked; nothing here
changes that.
