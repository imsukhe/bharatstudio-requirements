# TC-L16 — Interaction menu, goals and widgets acceptance

**Status:** `Local acceptance complete through migration 0119 — all L16 rows plus external-contribution aggregation and the shared SSE-invalidation widget transport have executable local and application-composition evidence; staging/browser/OBS and independent review remain open`

## Batch 10 addendum — 2026-09-13

External-contribution union verified in `apps/api/test/l16c-contribution-source-routes.test.ts` and `packages/db/tests/l16c-external-contribution-aggregation.sql` (part of the 49/49 SQL suite). Overlay SSE-transport behavior verified in `apps/web/.../overlay-transport-snapshot.test.tsx` and `overlay-transport-widget-poller.test.tsx`. Local counts re-run 2026-09-13: API 465/465, web 312/312, SQL 49/49 across 120 migrations. See `../tasks/L16-interaction-menu-goals-and-widgets.md` batch 10 section for the read-time union formula and the SSE-as-invalidation-signal design.

## L16-08 — Public paid-vote reachability correction — 2026-09-14

| Setup and action | Expected result | Required local evidence |
|---|---|---|
| Load a channel with active paid and free/closed/other-channel vote definitions | The public catalogue returns only the active paid definition id, label and its bounded options; it returns no queues, JSON configuration, vote amounts/tallies, identities, or another channel's entries | Isolated SQL proof for the `0126` function plus API projection/negative tests |
| Select a catalogue option and create an order | The request serializes both tags; the durable tag is accepted exactly once before order creation | API composition test and browser request test |
| Submit a stale, closed, cross-channel, unknown, or database-error selected tag | A redacted client error is returned and the provider/order service is never called; the donor can correct the selection | API negative/race tests |
| Submit an ordinary unselected tip or encounter a malformed/unavailable catalogue | Ordinary tips retain their behavior; malformed/unavailable optional catalogue hides the picker and cannot manufacture a tag | Existing/public-order regression plus browser parser tests |
**Task:** [`../tasks/L16-interaction-menu-goals-and-widgets.md`](../tasks/L16-interaction-menu-goals-and-widgets.md)
**Authority:** `bharatstudio-alerts/docs/BharatStudio-MASTER-PLAN.md` Part 6 (L16) and Part 7 §7.6
**Repository:** `/Users/sukhdevsingh/Workspace/Bharat Studio/bharatstudio-alerts`
**Data:** Synthetic channel/payment/support-goal fixtures only. No production database is used.

## Preconditions

1. L14's `creator_supporter_relations` exists for leaderboard identity (or is stubbed for this suite if L14 has not yet landed — record which).
2. L20's widget visual layer is available or stubbed.
3. Disposable PostgreSQL test harness available for `interaction_definitions`, `support_goals`, `widget_configs`.

## Acceptance cases

| ID | Setup and action | Expected result | Failure/retry and evidence |
|---|---|---|---|
| L16-01 | Define each of the eight non-challenge interaction types on a channel and bind each to a queue | Each type is retrievable per channel and correctly bound; the picker/config reflects all eight | **Not built.** No `interaction_definitions` table exists anywhere in `packages/db/migrations`. Only the community-support-goal type has a working slice (`support_goals`, migration 0102); the other seven (tip, TTS tip, sticker/reaction, mega alert, priority question, support vote, hype mode) are unbuilt. Remains not run |
| L16-02 | Send a confirmed payment event toward an active support goal, then send an unconfirmed platform (Super Chat) event of the same amount | Goal's `current` value updates only from the confirmed payment event, not from the platform event alone | Pass by construction: `packages/db/migrations/0102_v1_l16_support_goals.sql` stores no progress column at all — `app_private.support_goal_progress_paise()` computes it live as a windowed sum over `payments`/`refunds` rows, so there is no write path a platform event could reach |
| L16-03 | Load a widget browser source and inspect its network/event path | Widget consumes the existing overlay session/cursor/replay SSE path; no second delivery mechanism is present | Pass, local evidence: `apps/web/app/overlay/widgets/goal/[overlayId]/page.tsx` reuses the existing overlay fragment-token auth; no separate SSE/delivery endpoint was found for the goal widget. Only the goal widget exists — no other widget type to check |
| L16-04 | Request a leaderboard widget on a channel with default (private) privacy settings | Response withholds exact lifetime spend; only rank/badge-level data is exposed | **Not built.** No leaderboard route, table or widget type exists. Remains not run |
| L16-05 | Request the same leaderboard scoped to channel A while the viewer also supports channel B | Channel B's data is absent from the response | **Not built** — no leaderboard to query. Remains not run |
| L16-06 | Run a hype-mode cycle: start, cross threshold, decay to zero, end | Each state transition is deterministic and asserted by test | **Not built.** No hype-mode code found anywhere in `apps/` or `packages/db/migrations`. Remains not run |
| L16-07 | Attempt to submit viewer-supplied media through any of the eight interaction types | Submission is rejected before reaching the overlay | Not directly tested; satisfied vacuously for the one type that exists (`support_goals` accepts only a title/target/window, no media field), but seven of the eight interaction types this row is meant to cover don't exist yet to test against |

## Batch 8 addendum — 2026-09-07 (post-reconciliation)

Migration `0105_v1_l16_interaction_definitions_and_widgets.sql` shipped after the table above was written. Updated rows, verified against the migration and its callers:

| ID | Result |
|---|---|
| L16-01 | **Pass, local evidence.** `interaction_definitions` (0105) now covers all eight types, role/tier-gated via `app_private.create_interaction_definition`. `apps/api/test/l16-interactions-routes.test.ts` + `l16-goals-routes.test.ts`, 28 cases total. |
| L16-04, L16-05 | **Pass, local evidence.** Leaderboard function (0105) returns rank + coarse tier bucket only, scoped to one `channel_id`, read-only over `payments`/`refunds`. `packages/db/tests/l16-interaction-widgets.sql` asserts no-exact-amount and cross-channel exclusion. Note: this is not merely "withheld by default" — no configuration exposes an amount at all, because L14 never built the opt-in public-profile column its own task promised, so there is no opt-in switch to honour. |
| L16-06 | **Pass, local evidence.** `hype_mode_activations` (0105) plus `app_private.hype_mode_state` (live decayed sum over captured payments minus processed refunds). Lifecycle (start/threshold/decay/end) asserted in `packages/db/tests/l16-interaction-widgets.sql`. |
| L16-03 (widgets generally) | **Pass for `goal`, `vote`, `leaderboard`, `hype` only.** `apps/web/app/overlay/widgets/{goal,vote,leaderboard,hype}/[overlayId]/page.tsx` all reuse the existing overlay fragment-token/SSE machinery — no second delivery path found. **Still not run** for `recent_tips`, `top_supporters`, `supporter_ticker`, `mega_tip_banner`: these are valid `widget_configs.widget_type` values with tier-gated config storage, but no overlay page exists for any of them (`apps/web/app/overlay/widgets/` has only the four directories above). |
| L16-07 | **Still open, and now more precisely: not fully vacuous.** Support votes (`interaction_vote_records`) accept only an `option_key` + `voter_fingerprint`, no media field — consistent with the no-arbitrary-media rule. But votes are also **not money-gated at all**: 0105's own header records that the real tip-order-creation route (`apps/api/src/routes/public.ts`) has no field to tag an order with a vote option, so a paid interaction is not currently possible for `support_vote`. This is a scope gap in the money-tied interaction types, distinct from the media-upload question this row was originally written to test. |

## Closure rules

Closes only when every row has a real pass/fail result with inline evidence (migration filenames for the three new tables, exact widget browser-source file path, test-suite pass counts) replacing "Not run — TODO." No artifact/screenshot directory exists or may be created.

## Cleanup and rollback

All fixtures run against the disposable PostgreSQL harness, torn down after the run. New tables are additive; no production database is touched by this suite.

## Completion execution — 2026-09-08

| ID | Result and reproducible evidence |
|---|---|
| L16-01 | **Pass, local.** Migration `0105_v1_l16_interaction_definitions_and_widgets.sql` supplies all configured interaction types; `0108_v1_l16_paid_votes_and_missing_widgets.sql` closes paid support-vote payment tagging. `apps/api/test/l16-runtime-composition.test.ts` proves `buildApp` passes the tag/tally/overlay dependencies instead of only route mocks. `cd apps/api && npm test` passes **398/398**. |
| L16-03 | **Pass, local.** The existing goal/vote/leaderboard/hype pages plus `recent-tips`, `top-supporters`, `supporter-ticker`, and `mega-tip-banner` pages use the existing fragment-token overlay API boundary. The latter four share `widgets/shared/WidgetPoller.tsx`; no new SSE/outbox/delivery endpoint exists. `cd apps/web && npm test && npx tsc --noEmit && npm run build` passes **287/287**, typecheck, and production build, which enumerates all four routes. |
| L16-04, L16-05 | **Pass, local.** `sh packages/db/tests/run-sql-suite.sh` applies **110** migrations to a fresh PostgreSQL 16 template and reports **44/44** proofs. `l16-interaction-widgets` and `l16b_paid_votes_and_widgets` prove scoped, amount-free leaderboard/top-supporter outputs and no cross-channel leakage. |
| L16-06 | **Pass, local.** The same isolated SQL run passes `l16-interaction-widgets`, including deterministic start/threshold/decay/end coverage for `hype_mode_activations`. |
| L16-07 | **Pass, local boundary evidence.** `l16-widget-data.test.ts` rejects unexpected/malformed widget payload shapes; API tests prove amount fields are absent from top-supporter/ticker responses. The four browser sources have no media input or upload path. Paid-vote tags accept a bounded configured option only. |

The local execution also ran `git diff --check` successfully. The required
deployed browser/OBS, staging, and independent-review records are intentionally
not represented as passed by this local evidence.

## Composition-audit execution — 2026-09-09

The 2026-09-09 self-audit initially failed L16’s runtime-composition boundary:
the `0108` stores were absent from `AppDependencies` and `index.ts`. That
finding was corrected before this record was updated. Reproducible local
results after the correction: API `npm test && npm run build` **398/398**;
web `npm test && npx tsc --noEmit && npm run build` **289/289** with **zero
React `act(...)` warnings**; SQL `sh packages/db/tests/run-sql-suite.sh`
**44/44** after **110** migrations; and `git diff --check` passed. These
results are self-review evidence only.
