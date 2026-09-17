# GOA-01/GOA-02/GOA-03 — goal completion semantics: implementation record

**Date:** 2026-09-17
**Owner:** **Sukhdev Singh**
**Authority:** `../FULL-PRODUCT-DEFINITION.md` §31 rows GOA-01, GOA-02, GOA-03
**Task:** `../active/tasks/GOA-01-goal-completion-semantics.md`
**Acceptance:** `../tests/TC-GOA-01-goal-completion-semantics.md`

---

## What this task is

Support goals (L16, migration `0102`) derive both progress AND completion live, on every read:
`support_goal_reached(goal_id)` is exactly `progress_paise >= target_amount_paise`. That is correct
for progress (§19.6, derive-don't-store) and was the concrete, live defect for completion: a
processed refund reduces progress the very next time it is read, which silently flips a genuinely
reached goal back to "not reached," with nothing recording that it was ever reached at all.

This task closes that defect by giving completion its own identity, separate from the progress
comparison: `public.support_goal_completions`, a row written once, the first time progress crosses
the target (GOA-01), never rewritten by a later refund (GOA-02), and only ever moved out of its
active state by an explicit, reason-required, audited action (GOA-03).

## Reuse anchors, named as the task requires

| Value / shape | Reused from |
|---|---|
| Reopen reason bound, 1-500 characters | `packages/db/migrations/0059_v1_l04_reconciliation_manual_review_quarantine.sql`'s `reason` check constraint |
| "Resolve an audited record in place, never delete it" | Same 0059 migration's `payment_reconciliation_manual_reviews` open→resolved transition — the identical shape this task's completed→reopened transition uses |
| Idempotent latch via partial unique index + `ON CONFLICT ... DO NOTHING` | The same mechanical shape 0059's `quarantine_payment_reconciliation`/`quarantine_refund_reconciliation` use for their own open-row-per-target uniqueness |
| "Not found and not authorized are the same P0002 answer" | `0135`'s `end_stream_mission`, already the pattern `0102`'s own goal functions sit alongside |
| Declared-result-type + live-materialised-table double privacy proof | `prf02_slice6_lobby_status.sql`'s `list_overlay_lobby_status` check |
| `app_private.current_user_id()`, `app_private.has_channel_role()` | `0002`, reused throughout `0102` and this migration |

## The design decision this task did not make, and did not revisit

The task brief pre-decided the shape: progress stays derived, completion becomes a latched event, a
refund is recorded against the completion rather than un-writing it, reopen is manual-only. This
implementation follows that shape exactly. The one design choice left open — how a re-completion
after a manual reopen should behave — was resolved conservatively and in the direction the
append-only instruction points: a new `completed` row, not a rewrite of the reopened one, so a
goal's full completion/reopen history is always reconstructable, never overwritten. This required
no schema flexibility beyond what the partial unique index already gives (one ACTIVE completion at
a time, not one completion ever).

## Why no `required-queries.json` entry was added despite the task listing one as a minimum

`app_private.get_channel_goal_completion` lives in `apps/api/src/db/goal-store.ts`, which is
neither one of the seven overlay-facing store files the scan's rule 2 names, nor routed through
`derivedReadSql` (rule 3), nor named `list_overlay_*` (rule 1). Running
`node packages/db/explain-plans/scan-required-queries.mjs` before and after this migration is
green both times with an unchanged manifest-entry count — confirming the function is not in scope
for the scan, the same structural position `list_channel_payments`,
`get_channel_revenue_kpis` and `get_creator_activation_state` already occupy per that file's own
"2026-09-16, scan blind-spot closure" comment. Adding a manifest entry anyway would have
contradicted that file's own stated convention (several existing entries explicitly note that a
sibling creator-facing function is "deliberately NOT listed here"). A real EXPLAIN artifact was
still captured and committed at `packages/db/explain-plans/goal-completion.explain.md` — this
task's own explicit instruction — documenting both the query and why it sits outside the manifest.

## `app.ts` / `index.ts` — zero hunks

Both files were already fully wired for the pre-existing goal routes: `dependencies.goals` is
`GoalStore | undefined`, constructed by `createSqlGoalStore(sql)`, and `registerGoalRoutes` already
receives it. This task's two new methods (`getCompletion`, `reopenCompletion`) were added to the
SAME `GoalStore` interface, implemented in the SAME `createSqlGoalStore` factory, and consumed by
two new routes inside the SAME `registerGoalRoutes` function — so TypeScript's structural typing
picked them up with no change to either shared file. This was verified, not assumed: `git diff`
against `apps/api/src/app.ts` and `apps/api/src/index.ts` is empty for this task's changes.

## Verification run

| Command | Result |
|---|---|
| Full SQL suite (`sh packages/db/tests/run-sql-suite.sh`, all 73 files incl. `goa_completion_latch.sql`) | pass=73 fail=0 |
| `apps/api` route/unit suite (`tsx --test test/**/*.test.ts`) | tests 786, pass 786, fail 0 (11 of which are this task's own completion/reopen route tests) |
| `apps/web` suite (`tsx --test --experimental-test-module-mocks --import ./app/test-support/dom-env.ts app/**/*.test.ts app/**/*.test.tsx`) | tests 644, pass 644, fail 0 (unchanged — this task touches no web file) |
| `apps/api` TypeScript typecheck (`tsc -p tsconfig.json --noEmit`) | 0 errors |
| `apps/web` TypeScript typecheck (`tsc -p tsconfig.json --noEmit`) | 0 errors |
| `node contracts/validate-fixtures.mjs` | Validated 64 fixtures (was 63) plus the v1 template catalogue contract |
| `node contracts/validate-openapi.mjs` | Validated OpenAPI 3.1 document with 106 paths (was 104), 123 operation contracts (was 121) |
| `node contracts/test-openapi-validator.mjs` | Validated 3 negative OpenAPI operation-contract cases |
| `node packages/db/explain-plans/scan-required-queries.mjs` | OK — 26 manifest entries, 9 exemptions (unchanged from baseline; this task's read is out of scan scope, see above) |
| `node packages/db/explain-plans/check-plans.mjs` | OK: 26/26 plans current (unchanged — no manifest entry added) |
| `node .github/scripts/api-test-harness-check.mjs` | API test harness check: all checks passed against current code |

Baseline at `7d8682f` (this task's own base-fix target): sql 72/0 · api 775/0 · web 644/0 ·
contracts 63 fixtures/104 paths/121 operations · explain 26/26 · harness pass. Every delta above is
this task's own additions; nothing pre-existing regressed.

## Fixture id range

`...5f00-...5fff`, chosen after the registry's stated "next free block" (`...1720`) was found
already collided with two other files (`l04_l14_anonymous_payment_identity.sql`,
`l16d_public_paid_vote_catalogue.sql`) by grepping `packages/db/tests/*.sql` for the literal suffix
before trusting the note — exactly what the registry's own header instructs. `...5f00-...5fff` was
verified free the same way, and `fixtures/00_base_world.sql`'s registry comment was corrected in
place (not just appended to) to record both the collision and the real next-free block
(`...6900`), so the next task does not walk into the same trap.

## Subscriber count

`apps/web/app/overlay/canvas/` was not touched by this task (confirmed: `git diff --stat` against
that path for this task's changes is empty). `getSubscriberCount()` is unaffected.
