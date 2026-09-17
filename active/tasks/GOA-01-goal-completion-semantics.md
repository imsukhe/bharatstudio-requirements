# GOA-01/GOA-02/GOA-03 — Goal completion semantics

**Status:** `Conditionally complete — implemented and locally verified; independent review unavailable; no register state letter assigned`
**Owner:** **Sukhdev Singh**
**Classification:** L2 (a new database object plus two new writable audit paths on an existing,
money-adjacent domain; no schema is renamed and no existing function's signature or behaviour
changes)
**Authority:** `../../FULL-PRODUCT-DEFINITION.md` §31 rows GOA-01, GOA-02, GOA-03
**Acceptance record:** `../../tests/TC-GOA-01-goal-completion-semantics.md`
**Decision record:** `../../reviews/2026-09-17-goa-completion-latch-implementation.md`

**No register state letter is assigned by this task.** States are decided after audit, by the
owner, never by an implementer.

---

## What is being built

A complete vertical slice closing the concrete defect §31's GOA-01/02/03 rows describe: today,
`app_private.support_goal_reached` (migration `0102`) is entirely derived from live progress, so a
processed refund silently un-reaches a goal that genuinely crossed its target, with no record
anything happened.

| Layer | Object |
|---|---|
| Schema | `packages/db/migrations/0150_v1_goa_goal_completion_latch.sql` — **migration number assigned to this task**; `0149` is held concurrently by another agent (capability registry), never written here |
| New table | `public.support_goal_completions` — one active (`status='completed'`) row per goal at a time, enforced by a partial unique index; a manual reopen moves that row to `status='reopened'` in place; a later re-completion is a brand-new row, so full history survives |
| Write paths | `app_private.latch_support_goal_completion(uuid)` (GOA-01, idempotent), `app_private.reopen_support_goal_completion(channel, goal, reason)` (GOA-03) |
| Read path | `app_private.get_channel_goal_completion(channel, goal)` — opportunistically latches, then returns frozen completion fields next to live progress fields (GOA-02) |
| API | `GET /v1/channels/:channelId/goals/:goalId/completion`, `POST /v1/channels/:channelId/goals/:goalId/reopen` |
| Contracts | Two new OpenAPI paths, one new component schema (`GoalCompletion`) plus a request schema, one new JSON Schema + fixture, two new negative cases in `contracts/validate-fixtures.mjs` |
| Tests | `packages/db/tests/goa_completion_latch.sql` (real database), 11 new route tests in `apps/api/test/l16-goals-routes.test.ts` |

`app.ts` and `index.ts` needed **zero changes** — `GoalStore`, `createSqlGoalStore` and
`registerGoalRoutes` were already wired end to end for the existing goal routes, and the two new
methods slot into that same interface/factory/registrar, picked up automatically by TypeScript's
structural typing.

---

## The design this task builds, not redesigns

Quoted from the task brief, and reused verbatim rather than relitigated:

1. **Progress stays completely derived.** `app_private.support_goal_progress_paise` (0102) is not
   modified by one character. No stored progress counter is added anywhere. 0102's own reasoning —
   "a refund reduces progress the very next time progress is read" — is sound and untouched.
2. **Completion is a latched, audited EVENT** (GOA-01): a row written once, the first time live
   progress crosses the target, never a cached copy of the derived comparison. This is also what
   the register text ("actions fire from the event, never from a recomputed boolean") requires as
   a precondition for the future GOA-04+ trigger engine, which this task does not build.
3. **A later refund never un-writes the completion** (GOA-02): `completed_progress_paise` and
   `completed_at` freeze at the moment the latch fires; live `progress_paise` keeps moving. Both
   are returned side by side, so "why does this say completed at 94%?" has a complete, queryable
   answer without inventing a second audit table.
4. **Reopen is manual, reason-required and audited, never automatic** (GOA-03): the only caller of
   `reopen_support_goal_completion` anywhere in the migration is the function itself, invoked
   directly by an authenticated owner/admin action. Nothing in the latch, the refund path, or any
   read triggers a reopen as a side effect.

## Reuse anchors

| Value / shape | Reused from |
|---|---|
| Reopen reason bound, 1-500 characters | `packages/db/migrations/0059_v1_l04_reconciliation_manual_review_quarantine.sql`, `check (char_length(reason) between 1 and 500)` |
| "Resolve an audited record in place, never delete it" (open→resolved / completed→reopened) | Same 0059 migration's `payment_reconciliation_manual_reviews` open/resolved shape |
| "Not found and not authorized are the same P0002 answer" | `0135`'s `end_stream_mission`, already reused by this same file's `0102` neighbours |
| Owner/admin role check, `has_channel_role` | Used identically throughout — `0102`, `0109`, `0131`, `0135` |
| Double declared-result-type + live-materialised-table privacy proof | `prf02_slice6_lobby_status.sql`'s `list_overlay_lobby_status` check, reused in `goa_completion_latch.sql` for `get_channel_goal_completion` |
| `app_private.current_user_id()` | `0002`, reused by `0102`'s `create_support_goal` and by this migration's `reopen_support_goal_completion` |

## Out of scope, by explicit instruction

- `GOA-04`..`GOA-26` (the trigger/action/interlock engine) — waits for the capability registry
  (migration `0149`, a concurrent agent), so it does not hand-roll its own gates.
- Any change to `apps/web/app/overlay/canvas/` or a new canvas module — `getSubscriberCount()`
  stays 16, confirmed unchanged (this task touches no file under that path).
- Any change to `app_private.support_goal_progress_paise`, `support_goal_reached`,
  `list_channel_goals`, `get_channel_goal`, or `list_overlay_goal` (0102) — none of the five is
  modified by one character.
- Fixing the pre-existing gap where the *original* L16 goal CRUD routes
  (`POST/GET/PATCH /v1/channels/:channelId/goals`, `/end`) were never added to
  `contracts/openapi/v1.yaml`. That predates this task and is not this task's to fix; only the two
  new completion/reopen paths this task adds are documented in the contract.

## Verification run and reported by this implementer

Full SQL suite (`sh packages/db/tests/run-sql-suite.sh`), `apps/api` route/unit suite (`tsx --test
test/**/*.test.ts`), `apps/web` suite (`tsx --test --experimental-test-module-mocks --import
./app/test-support/dom-env.ts app/**/*.test.ts app/**/*.test.tsx`), both packages' TypeScript
typecheck (separate from the test runner), `node contracts/validate-fixtures.mjs`, `node
contracts/validate-openapi.mjs`, `node contracts/test-openapi-validator.mjs`, `node
packages/db/explain-plans/scan-required-queries.mjs`, `node packages/db/explain-plans/check-plans.mjs`,
and `node .github/scripts/api-test-harness-check.mjs`. Exact counts are in the decision record, not
restated here.
