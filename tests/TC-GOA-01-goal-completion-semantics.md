# TC-GOA-01 — goal completion semantics: acceptance record

**Date:** 2026-09-17
**Owner:** **Sukhdev Singh**
**Task:** `../active/tasks/GOA-01-goal-completion-semantics.md`
**Decision:** `../reviews/2026-09-17-goa-completion-latch-implementation.md`

Written **before** implementation began, per `governance/AGENTS.md`. The "Commands run" table is
filled in after the run, from actual output, and is the single place this task's numbers live.

---

## Acceptance criteria

### A. The latch (`packages/db/migrations/0150_v1_goa_goal_completion_latch.sql`)

| ID | Criterion |
|---|---|
| GOA1.1 | `app_private.latch_support_goal_completion(goal_id)` returns `null` and writes nothing while live progress is below the goal's target |
| GOA1.2 | Once progress crosses the target, calling the latch writes exactly one `support_goal_completions` row with `status='completed'` |
| GOA1.3 | Calling the latch a second time (same goal, still completed) returns the SAME completion id and writes no second row — proven by calling it twice in the same test and asserting identity, not merely a row count |
| GOA1.4 | The idempotency lever is a partial unique index (`goal_id` where `status='completed'`), not an application-side check-then-insert race |
| GOA1.5 | `app_private.support_goal_progress_paise` and `app_private.support_goal_reached` (0102) are byte-for-byte unchanged by this migration — no stored progress counter is added anywhere |

### B. GOA-02 — a refund never un-completes a goal

| ID | Criterion |
|---|---|
| GOA2.1 | After a completion latches, a processed refund reduces live `progress_paise` on the very next read (proves progress is still derived, not frozen) |
| GOA2.2 | The SAME refund leaves `completed=true`, `completed_at`, and `completed_progress_paise` on the completion row completely unchanged |
| GOA2.3 | The old, purely-derived `support_goal_reached` flag is still allowed (expected) to flip back to `false` after the refund — this is documented as pre-existing 0102 behaviour, deliberately not touched, and is asserted explicitly so a future edit cannot "fix" it into breaking GOA-02 |
| GOA2.4 | The completion read (`get_channel_goal_completion`) surfaces frozen and live figures side by side in one response, so a creator's "why does this say completed at 94%?" has a complete answer without a second audit table |

### C. GOA-03 — manual reopen is explicit, reason-required and audited

| ID | Criterion |
|---|---|
| GOA3.1 | A viewer (non owner/admin) cannot reopen a completion — `42501`, nothing changed |
| GOA3.2 | A `null`, empty, or whitespace-only reason is rejected (`22023`); the completion row is untouched by every rejected attempt |
| GOA3.3 | A reason over 500 characters is rejected (`22023`) — bound reused from migration `0059` |
| GOA3.4 | A goal that was never completed cannot be reopened (`22023`, distinct error text from "not found") |
| GOA3.5 | A successful reopen is audited: `reopened_by_user_id` is the ACTING user, `reopen_reason` is the exact text supplied, `reopened_at` is set — all three asserted directly against the row, not only through the read projection |
| GOA3.6 | Reopening an already-reopened (currently not-completed) goal is rejected (`22023`) — reopen is not a toggle |
| GOA3.7 | Progress re-crossing the target after a manual reopen creates a SECOND, NEW `completed` row — the original `reopened` row is neither deleted nor rewritten (append-only history) |

### D. Authorization / not-found parity and privacy

| ID | Criterion |
|---|---|
| GOA-D.1 | A non-member reading a channel's goal completion gets the identical `P0002` answer a wrong channel/goal id would — never a distinguishing error |
| GOA-D.2 | `get_channel_goal_completion`'s declared result type is asserted exactly via `pg_get_function_result`, AND the actual columns from a live call are asserted exactly via `information_schema.columns` on a materialised temp table — neither a payment id nor a refund id may appear |
| GOA-D.3 | The API's `additionalProperties: false` route schemas and OpenAPI `GoalCompletion`/`ReopenGoalCompletionRequest` components reject a `paymentId` or `refundId` field, proven in `contracts/validate-fixtures.mjs` |

### E. API routes

| ID | Criterion |
|---|---|
| GOA-E.1 | `GET /v1/channels/:channelId/goals/:goalId/completion` requires session auth (401 without it) and returns the store's completion object verbatim on success |
| GOA-E.2 | The same route maps `not_found` to a 404 `not_found` envelope |
| GOA-E.3 | `POST /v1/channels/:channelId/goals/:goalId/reopen` requires session auth and a `reason` (1-500 chars) rejected at the schema layer BEFORE the store is ever called for both a missing and an over-long reason |
| GOA-E.4 | The route maps `not_completed` to 409 `goal_not_completed`, `forbidden`/`not_found` to 404 `not_found` (never a leaking 403), and a store throw to a redacted, retryable 503 |

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
