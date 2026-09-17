# TC-GOA-04 — goal trigger engine spine: acceptance record

**Date:** 2026-09-17
**Owner:** **Sukhdev Singh**
**Task:** `../active/tasks/GOA-04-trigger-engine-spine.md`
**Decision:** `../reviews/2026-09-17-goa-trigger-engine-implementation.md`

Written **before** implementation began, per `governance/AGENTS.md`. The "Commands run" table is
filled in after the run, from actual output, and is the single place this task's numbers live.

---

## Acceptance criteria

### A. GOA-04 — trigger types (`packages/db/migrations/0158_v1_goa_trigger_engine_spine.sql`)

| ID | Criterion |
|---|---|
| GTE1.1 | `reached_100` fires FROM migration `0150`'s own `latch_support_goal_completion`, never a re-derived boolean — the evaluation's `source_event_id` equals `0150`'s completion row id |
| GTE1.2 | `threshold_percentage`/`threshold_absolute` fire only once live progress has crossed the configured threshold, and not before |
| GTE1.3 | `first_contribution` fires on the goal's first payment and never again, regardless of the rule's configured `repeat_mode` |
| GTE1.4 | Exactly one of `threshold_percentage`/`threshold_amount_paise` is set, and only for the trigger type that uses it — enforced by a database CHECK constraint, not application code alone |

### B. GOA-09 — per-trigger controls

| ID | Criterion |
|---|---|
| GTE2.1 | `enabled = false` prevents a rule from ever evaluating |
| GTE2.2 | `once_per_stream`: re-evaluating an already-crossed rule with a NEW, distinct source event is a no-op — no second evaluation row |
| GTE2.3 | `every_time`: a threshold rule may accumulate more than one evaluation row across distinct source events while the condition holds |

### C. GOA-18 — ordered sequences with per-step delays

| ID | Criterion |
|---|---|
| GTE3.1 | Actions inserted out of `step_order` are returned by dispatch in `step_order` ascending order, never insertion order |
| GTE3.2 | Each step's configured `delay_ms` is returned verbatim, unmodified |
| GTE3.3 | A second dispatch call for the same evaluation returns the identical ordering and delays, and does not duplicate action-run rows (idempotent, stable) |

### D. GOA-19 — conditions, honestly unevaluatable where the concept does not exist

| ID | Criterion |
|---|---|
| GTE4.1 | `only_live`, `named_scene`, `not_in_clutch` each fail SAFE (the whole rule's sequence is blocked, never silently allowed to proceed) when dispatched, and the reported reason says "unevaluatable" |
| GTE4.2 | `not_during_sponsor_slot` is the one evaluatable condition: it passes when no sponsor card is currently active for the channel, and blocks when one is (against `public.sponsor_cards`, migration `0145`) — both directions proven |
| GTE4.3 | An unevaluatable/failing condition blocks even an action explicitly configured `fire_mode = 'fire'` — the condition gate runs before the fire/prepare decision |

### E. GOA-20 — interlocks, not creator-configurable

| ID | Criterion |
|---|---|
| GTE5.1 | No column on any `goal_trigger_*` table carries a name that could plausibly disable, suppress, override or bypass the loud/full-screen interlock — asserted via an `information_schema.columns` scan for a forbidden-token pattern |
| GTE5.2 | `dispatch_goal_trigger_sequence`'s own function body (via `pg_get_functiondef`) contains no override/bypass/suppress-interlock token, and still derives the interlock decision from `action_type` alone via the immutable severity lookup |
| GTE5.3 | A `noop_local_loud_or_fullscreen` action explicitly configured `fire_mode = 'fire'` (permitted by the CHECK constraint — only outbound actions are barred from `fire`) is STILL `blocked_interlock` on dispatch — `fire_mode` has no effect on this branch |
| GTE5.4 | The interlock is scoped to loud/full-screen severity only: a quiet action on the SAME rule as a blocked loud action still fires |

### F. GOA-21 — prepare-not-fire default

| ID | Criterion |
|---|---|
| GTE6.1 | `goal_trigger_actions.fire_mode` defaults to `'prepare'` for every action, local or outbound |
| GTE6.2 | Inserting an outbound (`noop_outbound`) action with `fire_mode = 'fire'` is rejected by a database CHECK constraint — proven with a raw `INSERT` attempt, not only through the wrapper function |
| GTE6.3 | An outbound action added via `add_goal_trigger_action` with no explicit `fireMode` (relying purely on the default) dispatches with `status = 'prepared'`, never `'fired'` |
| GTE6.4 | The route layer rejects `fireMode: 'fire'` for `actionType: 'noop_outbound'` with a 400 BEFORE the store is ever called |

### G. `0150` untouched, and privacy

| ID | Criterion |
|---|---|
| GTE7.1 | `app_private.latch_support_goal_completion` remains idempotent after this migration (re-run of `0150`'s own idempotency shape against a goal this migration's own test completed) |
| GTE7.2 | `app_private.support_goal_progress_paise` and `0150`'s own functions are called, never modified — confirmed by `git diff` against migration `0150` being empty |
| GTE7.3 | `list_channel_goal_trigger_rules`'s declared column set is asserted exactly via `pg_proc`/`pg_attribute` introspection — no `source_event_id` or other internal bookkeeping column leaks |

### H. API routes

| ID | Criterion |
|---|---|
| GTE8.1 | Every route requires session auth (401 without it), and a missing store is a retryable 503 |
| GTE8.2 | A rule/condition/action/evaluation that does not belong to the caller's channel is 404, never a leaking 403 |
| GTE8.3 | `POST .../triggers` rejects a `triggerType`/threshold-field mismatch with 400 before the store is called |
| GTE8.4 | `POST .../conditions` rejects a `named_scene` with no `conditionValue`, and a non-`named_scene` condition carrying one, both with 400 before the store is called |
| GTE8.5 | `POST .../actions` round-trips `stepOrder`/`delayMs` exactly as sent, and rejects `fireMode: 'fire'` for `actionType: 'noop_outbound'` before the store is called |
| GTE8.6 | `GET .../goal-trigger-runs/:evaluationId` returns `blockedReason` intact, never summarised away |

---

## Commands run

| Command | Result |
|---|---|
| Full SQL suite (`sh packages/db/tests/run-sql-suite.sh`) | *(filled in from actual output — see decision record)* |
| `apps/api` route/unit suite (`tsx --test test/**/*.test.ts`) | *(filled in from actual output — see decision record)* |
| `apps/web` suite (`tsx --test --experimental-test-module-mocks --import ./app/test-support/dom-env.ts app/**/*.test.ts app/**/*.test.tsx`) | *(filled in from actual output — see decision record)* |
| `apps/api` TypeScript typecheck (`tsc -p tsconfig.json --noEmit`) | *(filled in from actual output — see decision record)* |
| `apps/web` TypeScript typecheck (`tsc -p tsconfig.json --noEmit`) | *(filled in from actual output — see decision record)* |
| `node contracts/validate-fixtures.mjs` | *(filled in from actual output — see decision record)* |
| `node contracts/validate-openapi.mjs` | *(filled in from actual output — see decision record)* |
| `node contracts/test-openapi-validator.mjs` | *(filled in from actual output — see decision record)* |
| `node packages/db/explain-plans/scan-required-queries.mjs` | *(filled in from actual output — see decision record)* |
| `node packages/db/explain-plans/check-plans.mjs` | *(filled in from actual output — see decision record)* |
| `node .github/scripts/api-test-harness-check.mjs` | *(filled in from actual output — see decision record)* |

---

**STAGING NOTE (not part of the record itself):** written under `.governance-staging/` in this
agent's `bharatstudio-alerts` worktree — see the sibling task record's own staging note for why,
and the intended real path (`bharatstudio-requirements/tests/TC-GOA-04-trigger-engine-spine.md`).
