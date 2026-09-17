# GOA-04/GOA-09/GOA-18/GOA-19/GOA-20/GOA-21 — goal trigger engine spine: implementation record

**Date:** 2026-09-17
**Owner:** **Sukhdev Singh**
**Authority:** `../FULL-PRODUCT-DEFINITION.md` §31 rows GOA-04, GOA-09, GOA-18, GOA-19, GOA-20, GOA-21; §23.3; §5.4
**Task:** `../active/tasks/GOA-04-trigger-engine-spine.md`
**Acceptance:** `../tests/TC-GOA-04-trigger-engine-spine.md`

---

## What this task is

Migration `0150` gave goal completion its own identity — a latched, audited event that a refund
can never un-write. §23.3.1's own words are explicit that this is a precondition for a trigger
engine, not an end in itself: "Actions fire from that event, never from the boolean." This task
builds the engine that consumes events like that one: rule configuration (GOA-04/GOA-09), ordered
per-step-delay sequencing (GOA-18), conditions (GOA-19), the two checkable non-configurable safety
interlocks (GOA-20), and the prepare-vs-fire default (GOA-21) — the SPINE, not the action catalogue
(`GOA-10`..`GOA-17`) and not the other trigger classes (`GOA-05`..`GOA-08`).

## The design decision this task did not make, and did not revisit

The task brief pre-decided the shape (fire from events, not booleans; interlocks structural, not
data; prepare is the default). One design choice was genuinely open and is resolved here,
conservatively: **how per-trigger idempotency ("once per stream") should be scoped when this
schema has no stream-session entity.** `0102`'s own header already established the precedent for
`support_goals.goal_window = 'stream'` — the goal's own lifecycle stands in for a stream boundary,
because no better signal exists. This task reuses that exact precedent rather than inventing a
second, divergent stand-in: `once_per_stream` is enforced by a partial unique index scoped to
`(rule_id)`, i.e. at most one evaluation ever per rule per goal lifecycle. `first_contribution` is
additionally hard-pinned to fire at most once regardless of the rule's configured `repeat_mode`
(its dedupe key is fixed to the rule's own id, not the caller's source event), because "the first
contribution" is a singular fact by definition and an `every_time` setting on that trigger type
would otherwise silently misbehave rather than erroring — this is documented in both the migration
and the domain layer rather than left to be discovered.

## Why GOA-19's `not_in_clutch` condition and GOA-20's interlock are two different things that share a name

Both ultimately gate on Clutch Mode, which does not exist. They are kept structurally separate on
purpose: `not_in_clutch` is one of four condition TYPES a creator may optionally attach to a rule
(`goal_trigger_conditions`, ordinary data, GOA-19) — a creator who never adds it is unaffected by
it. The loud/full-screen interlock (GOA-20) is NOT a condition row at all; it is unconditional
logic inside `dispatch_goal_trigger_sequence`, reached purely from `action_type` via an immutable
lookup, that applies to every loud/full-screen action on every rule regardless of what conditions
that rule carries. Collapsing the two into one mechanism would have made the interlock
creator-removable by simply never adding the condition — exactly what GOA-20 forbids. Both
currently fail safe for the same underlying reason (Clutch state is unknowable), so their observed
behaviour looks identical today; they will diverge the day Clutch Mode ships and `not_in_clutch`
becomes optional again while the interlock stays mandatory.

## Why the crossing/evaluation latch does not duplicate `0150`'s table

`0150` built exactly one latch, for exactly one fact ("goal completion"). GOA-04 additionally
needs idempotent crossing-detection for percentage thresholds, absolute thresholds and first
contribution — facts `0150` was never asked to track. Rather than extending `support_goal_
completions` with unrelated columns (which the task's own constraints forbid — `0150` is not to be
modified), this task adds its own table, `goal_trigger_evaluations`, reusing `0150`'s exact
mechanism (a partial unique index plus an exception-caught insert) rather than its data. For
`reached_100` specifically, the new table's `source_event_id` is set to `0150`'s own completion row
id — so a reopen-and-recomplete (a genuinely new completion id) is correctly treated as a new
crossing, while a retried call against an unchanged completion is correctly treated as the same
one. This was verified directly (`GTE-6` in the SQL test), not merely reasoned about.

## Why no `required-queries.json`/EXPLAIN-plan entry was added

`scan-required-queries.mjs`'s three rules cover: (1) `app_private.list_overlay_*` naming, (2) files
under `apps/api/src/db/` with `overlay`/`master-canvas` in the basename, (3) any store factory
`apps/api/src/index.ts` constructs with `derivedReadSql`. `db/goal-trigger-store.ts` matches none
of the three — it is wired to the main `sql` pool (creator configuration, not an overlay-facing
derived read), and none of its functions is named `list_overlay_*`. Running
`node packages/db/explain-plans/scan-required-queries.mjs` is green with the manifest's entry count
unchanged (31, same as baseline), confirming this is structurally out of scope for the scan — the
identical position `db/sponsor-card-store.ts`'s creator-facing functions already occupy (see that
slice's own explain-plan artifact header for the same reasoning, restated here rather than
re-litigated). No EXPLAIN artifact was captured for this task's functions.

## `app.ts` / `index.ts` — the only shared-file hunks

Three lines added to each file, all additive:

**`apps/api/src/app.ts`**
- one import block (`GoalTriggerStore` type + `registerGoalTriggerRoutes`), placed after the
  sponsor-card import block
- one field on the dependencies type: `goalTriggers?: GoalTriggerStore;`, placed after
  `overlaySponsorCard`
- one registration call: `await registerGoalTriggerRoutes(app, dependencies.sessions,
  dependencies.goalTriggers, dependencies.account);`, placed after the sponsor-card registration

**`apps/api/src/index.ts`**
- one import (`createSqlGoalTriggerStore`), placed after the sponsor-card store imports
- one dependency construction line: `goalTriggers: sql ? createSqlGoalTriggerStore(sql) :
  undefined,`, placed after `overlaySponsorCard`

No existing line in either file was modified or reordered.

## `packages/db/tests/fixtures/00_base_world.sql` — the only other shared-file hunk

One line appended to the id-allocation registry note, after the existing "next free block" note
and before nothing else (no existing line changed):

```
--   ...7200-...72ff                           goa_trigger_engine OWN fixture (reuses base_world channel '...0011'; own payments) -- pre-assigned to this lane by the coordinator, not independently verified free
```

## `contracts/validate-fixtures.mjs` — the only other shared-file hunk

Seven lines added to the `fixtureToSchema` map, immediately after the two existing goal-completion
entries — no existing entry changed.

## Governance records could not be written to their real path

`bharatstudio-requirements/active/tasks/GOA-04-trigger-engine-spine.md`,
`bharatstudio-requirements/tests/TC-GOA-04-trigger-engine-spine.md` and this file's own real path
(`bharatstudio-requirements/reviews/2026-09-17-goa-trigger-engine-implementation.md`) could not be
written directly: this session's Write and git tools categorically refuse any operation against
the `bharatstudio-requirements` shared checkout while running worktree-isolated for
`bharatstudio-alerts`, and no worktree copy of `bharatstudio-requirements` was available to switch
into (`EnterWorktree` with that path, `git -C`, and `git --git-dir` were all refused with the
identical isolation message). All three documents were written in full under
`bharatstudio-alerts/.claude/worktrees/agent-a1b334735b18288b1/.governance-staging/` at their
intended relative paths, ready to be copied into the real checkout. This is reported as a blocker,
not worked around by weakening the isolation guard.

## Verification run

| Command | Result |
|---|---|
| Full SQL suite (`sh packages/db/tests/run-sql-suite.sh`, all 80 files incl. `goa_trigger_engine.sql`) | pass=80 fail=0 |
| `apps/api` route/unit suite (`tsx --test test/**/*.test.ts`) | tests 883, pass 883, fail 0 (18 of which are this task's own route tests) |
| `apps/web` suite (`tsx --test --experimental-test-module-mocks --import ./app/test-support/dom-env.ts app/**/*.test.ts app/**/*.test.tsx`) | tests 644, pass 644, fail 0 (unchanged — this task touches no web file) |
| `apps/api` TypeScript typecheck (`tsc -p tsconfig.json --noEmit`) | 0 errors |
| `apps/web` TypeScript typecheck (`tsc -p tsconfig.json --noEmit`) | 0 errors |
| `node contracts/validate-fixtures.mjs` | Validated 77 fixtures (was 70) plus the v1 template catalogue contract |
| `node contracts/validate-openapi.mjs` | Validated OpenAPI 3.1 document with 132 paths (was 127), 156 operation contracts (was 148), all local $ref targets resolve |
| `node contracts/test-openapi-validator.mjs` | 3 negative OpenAPI operation-contract cases, unchanged |
| `node packages/db/explain-plans/scan-required-queries.mjs` | OK — 31 manifest entries (unchanged), 13 exemptions (unchanged); this task's store is out of scope for the scan (see above) |
| `node packages/db/explain-plans/check-plans.mjs` | OK — 31/31 plans current (unchanged) |
| `node .github/scripts/api-test-harness-check.mjs` | All checks passed; 98 test files scanned (was 97), 41 referencing `createTestFastify` |

`measurement:test` was not run — the task instructions state it fails environmentally in agent
sandboxes and passes on `main`; not chased per that instruction.

## Confirmed unchanged

- `git diff` against `packages/db/migrations/0150_v1_goa_goal_completion_latch.sql` is empty.
- `apps/web/app/overlay/canvas/`'s `getSubscriberCount()` is still 16 (file not touched by this
  task; confirmed by `git diff` against that path being empty).
- No table, column or function named `capability*`, `ctl_*`, `admin*`, `app_users` or
  `platform_owner*` was created, altered, or referenced by a new object in migration `0158`.
