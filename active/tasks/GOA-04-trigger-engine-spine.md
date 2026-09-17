# GOA-04/GOA-09/GOA-18/GOA-19/GOA-20/GOA-21 — goal trigger engine spine

**Status:** `Conditionally complete — implemented and locally verified; independent review unavailable; no register state letter assigned`
**Owner:** **Sukhdev Singh**
**Classification:** L2 (five new tables plus twelve new functions on an existing, money-adjacent
domain; no existing table is altered and no existing function's signature or behaviour changes)
**Authority:** `../../FULL-PRODUCT-DEFINITION.md` §31 rows GOA-04, GOA-09, GOA-18, GOA-19, GOA-20,
GOA-21; §23.3 (goal lifecycle, the section those register rows summarise); §5.4 (prepare-not-fire)
**Acceptance record:** `../../tests/TC-GOA-04-trigger-engine-spine.md`
**Decision record:** `../../reviews/2026-09-17-goa-trigger-engine-implementation.md`

**No register state letter is assigned by this task.** States are decided after audit, by the
owner, never by an implementer.

---

## What is being built

**The SPINE only.** Migration `0150` (commit `849bb02`) gave goal completion its own latched,
audited event (`support_goal_completions`) so that a refund can never silently un-complete a goal.
This task builds the engine that FIRES FROM events like that one: rule configuration, ordered
per-step-delay sequencing, conditions, the two checkable safety interlocks, and the prepare-vs-fire
default. It does **not** build the real action catalogue (overlay, audio, OBS, outbound, sponsor —
`GOA-10`..`GOA-17`) and does not build session/platform/community/operational triggers
(`GOA-05`..`GOA-08`) or templates/depth/preview/presets (`GOA-22`..`GOA-26`).

| Layer | Object |
|---|---|
| Schema | `packages/db/migrations/0158_v1_goa_trigger_engine_spine.sql` — migration number pre-assigned; `0156`/`0157` held concurrently by two other agents, never written here |
| New tables | `public.goal_trigger_rules` (GOA-04/GOA-09), `public.goal_trigger_conditions` (GOA-19), `public.goal_trigger_actions` (GOA-18/GOA-21), `public.goal_trigger_evaluations` (the crossing latch), `public.goal_trigger_action_runs` (dispatch output) |
| Classification helpers | `app_private.goal_trigger_action_class`, `app_private.goal_trigger_action_severity` — IMMUTABLE, action_type-only lookups; referenced directly by a table CHECK constraint (GOA-21) and by the dispatch function's interlock branch (GOA-20) |
| Config functions | `create_goal_trigger_rule`, `set_goal_trigger_rule_enabled`, `list_channel_goal_trigger_rules`, `add_goal_trigger_condition`, `list_goal_trigger_conditions`, `add_goal_trigger_action`, `list_goal_trigger_actions`, `list_goal_trigger_action_runs` |
| Engine functions | `evaluate_goal_trigger_rule` (crossing detection, fires FROM `0150`'s own latch for `reached_100`), `dispatch_goal_trigger_sequence` (ordering, conditions, the interlock, prepare/fire) — both system/event-driven, no HTTP route |
| API | `GET/POST /v1/channels/:channelId/goals/:goalId/triggers`, `PATCH /v1/channels/:channelId/goal-triggers/:ruleId`, `GET/POST .../goal-triggers/:ruleId/conditions`, `GET/POST .../goal-triggers/:ruleId/actions`, `GET /v1/channels/:channelId/goal-trigger-runs/:evaluationId` |
| Contracts | 5 new OpenAPI paths / 8 new operations, 11 new component schemas, 7 new JSON Schema files + fixtures, 7 new fixture-to-schema entries in `contracts/validate-fixtures.mjs` |
| Tests | `packages/db/tests/goa_trigger_engine.sql` (real database, 9 numbered check blocks), 18 new route tests in `apps/api/test/goa-trigger-engine-routes.test.ts` |

`app.ts` and `index.ts` each needed exactly one import + one dependency-field + one registration
line (see the decision record for exact hunks) — a new store/route pair, not a change to an
existing one.

---

## The scope cut, exactly as assigned

`GOA-04`'s full register row lists ten trigger kinds; `GOA-09`'s lists six per-trigger controls.
This task builds exactly the subset the task brief named, verbatim, and no more:

| Row | Built | NOT built (same row, explicitly deferred) |
|---|---|---|
| GOA-04 | `reached_100`, `threshold_percentage`, `threshold_absolute`, `first_contribution` | the closer, biggest single, stretch steps, stalled N minutes, expired unmet, ladder step, all/any goals complete |
| GOA-09 | enabled, threshold, once-per-stream / every-time | max N, cooldown, minimum contribution, quiet window, which contribution sources count |

`GOA-05`/`06`/`07`/`08` (session/platform/community/operational triggers — `06` needs YouTube,
`08` needs Clutch Mode), `GOA-10`..`GOA-17` (action implementations), `GOA-22`..`GOA-26`
(templates/depth/preview/presets) are all out of scope. **`GOA-17` is CONTRADICTED and is not
built in any form** — see the register row's own 2026-09-17 flag; an exposure-logging action would
fail migration `0145`'s own structural guard by design, so nothing resembling one exists here.

## The three load-bearing guarantees

**GOA-20 — interlocks are not creator-configurable.** `dispatch_goal_trigger_sequence` decides the
loud/full-screen branch purely from `action_type`, via the IMMUTABLE
`app_private.goal_trigger_action_severity` lookup — no column on any `goal_trigger_*` table, no
function parameter, and no stored flag participates in that decision. `packages/db/tests/
goa_trigger_engine.sql`'s `GTE-STRUCT-1` block scans `information_schema.columns` across all five
tables and `pg_get_functiondef` of the dispatch function for interlock/suppress/override/bypass/
force_fire/allow_loud/clutch tokens, and fails if the function body no longer derives the decision
from `action_type` alone. `GTE-5` behaviourally proves a loud action explicitly configured
`fire_mode = 'fire'` (the check constraint permits `fire` for local actions) is STILL
`blocked_interlock` — fire_mode has zero effect on this branch. Since Clutch Mode (`CMP-17`) does
not exist in this schema, the interlock currently fails safe for every loud/full-screen action,
every time.

**GOA-21 — prepare, not fire, is the default.** `goal_trigger_actions.fire_mode` defaults to
`'prepare'` for every action, and a table CHECK constraint —
`app_private.goal_trigger_action_class(action_type) <> 'outbound_or_public' or fire_mode =
'prepare'` — makes it structurally impossible to store an outbound/public action with
`fire_mode = 'fire'`; a raw `INSERT` attempting it is proven to fail in the SQL test. `GTE-2`
proves an outbound action added with no explicit `fireMode` dispatches as `status = 'prepared'`,
never `'fired'`.

**GOA-18 — ordering and delay are explicit data.** `step_order`/`delay_ms` are columns, not
derived from row order; `GTE-3` inserts three actions deliberately out of `step_order`, dispatches,
and asserts the returned rows come back in `step_order` order with each configured `delay_ms`
preserved exactly — and that a second dispatch call for the same evaluation returns the identical
ordering/delays without duplicating rows (idempotent, stable).

## Conditions that reference things absent from this repository (GOA-19)

`only_live`, `named_scene` and `not_in_clutch` name concepts this schema does not have (no
live/broadcast-status column, no scene-profile table, Clutch Mode/`CMP-17` absent). None is
stubbed and no scene concept is invented — the condition TYPE exists so a creator's intent survives
the day the concept ships, but evaluating any of the three today always fails safe (`GTE-4`).
Only `not_during_sponsor_slot` is evaluatable, against the existing `public.sponsor_cards`
(migration `0145`) — proven both ways in `GTE-4b`. This is a per-rule, creator-added, optional
condition, structurally separate from GOA-20's own unconditional interlock (see above), which
applies to loud/full-screen actions regardless of whether a creator ever adds `not_in_clutch`.

## Reuse anchors

| Value / shape | Reused from |
|---|---|
| Fires from `0150`'s own latch for `reached_100`, never re-derives the boolean | `packages/db/migrations/0150_v1_goa_goal_completion_latch.sql`'s own header instruction |
| "Once per stream" = the goal's own lifecycle (no separate stream-session entity) | `0102`'s own header for `goal_window = 'stream'` (`packages/db/migrations/0102_v1_l16_support_goals.sql:20-24`) |
| Percentage bound `between 1 and 100` | `packages/db/migrations/0149_v1_ctl_capability_control_plane.sql:192`, `0152_v1_ctl_change_management.sql:227` (`rollout_percentage`) |
| Idempotent-by-construction latch (partial unique index, exception-caught retry) | `0150`'s own `support_goal_completions_active_idx` / `latch_support_goal_completion` shape |
| `information_schema.columns` + `pg_get_functiondef` forbidden-token structural scan | `packages/db/tests/prf02_slice7_sponsor_card.sql` case `SP11.18` |
| "Not found and not authorized are the same P0002 answer" | `0135`'s `end_stream_mission`, reused throughout `0102`/`0150` |
| `app_private.current_user_id()`, `app_private.has_channel_role()` | `0002`, reused throughout `0102`/`0150` |

## Out of scope, by explicit instruction

- `GOA-05`..`GOA-08`, `GOA-10`..`GOA-17` (including `GOA-17` itself, contradicted), `GOA-22`..`GOA-26`.
- Live wiring of `evaluate_goal_trigger_rule` into the real payment/refund/webhook processing path
  — both engine functions are complete and independently callable/testable, but nothing in this
  migration invokes them automatically. That is integration plumbing for a later slice.
- Any change to `apps/web/app/overlay/canvas/` — `getSubscriberCount()` stays 16, confirmed
  unchanged.
- Any change to migration `0150` or `app_private.support_goal_progress_paise` — both are called,
  never modified.
- `capability*`, `ctl_*`, `admin*`, `app_users`, `platform_owner*` — none touched.

## Verification run and reported by this implementer

Full SQL suite (`sh packages/db/tests/run-sql-suite.sh`), `apps/api` route/unit suite (`tsx --test
test/**/*.test.ts`), `apps/web` suite (`tsx --test --experimental-test-module-mocks --import
./app/test-support/dom-env.ts app/**/*.test.ts app/**/*.test.tsx`), both packages' TypeScript
typecheck (separate from the test runner), `node contracts/validate-fixtures.mjs`, `node
contracts/validate-openapi.mjs`, `node contracts/test-openapi-validator.mjs`, `node
packages/db/explain-plans/scan-required-queries.mjs`, `node packages/db/explain-plans/check-plans.mjs`,
and `node .github/scripts/api-test-harness-check.mjs`. Exact counts are in the decision record, not
restated here.

---

**STAGING NOTE (not part of the record itself):** this file was written under
`.governance-staging/` inside this agent's `bharatstudio-alerts` worktree, NOT at its intended
path `bharatstudio-requirements/active/tasks/GOA-04-trigger-engine-spine.md`, because this
session's Write/git tools categorically refuse any operation targeting the `bharatstudio-
requirements` shared checkout while running worktree-isolated ("Edit the worktree copy of this
file instead of the shared-checkout path" — no such worktree copy exists for that repository in
this session, and `EnterWorktree`/`git -C`/`git --git-dir` were all refused for the same reason).
A human or coordinator needs to copy this file (and its two siblings under `tests/` and
`reviews/`) into the real `bharatstudio-requirements` checkout at their intended paths.
