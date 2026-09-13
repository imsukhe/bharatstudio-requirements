# TC-L23 — AI assist, bounded acceptance

**Status:** `Executed 2026-09-13 — 13 SQL checks, 13 API route tests, 6 web page tests, all passing; see the evidence section appended below`
**Task:** [`../tasks/L23-ai-assist-bounded.md`](../tasks/L23-ai-assist-bounded.md)
**Authority:** `bharatstudio-alerts/docs/BharatStudio-MASTER-PLAN.md` Part 6 (L23)
**Repository:** `/Users/sukhdevsingh/Workspace/Bharat Studio/bharatstudio-alerts`
**Data:** Synthetic configuration/challenge/moderation fixtures only. No real payment or refund is invoked by any AI-assist code path in this suite — that is precisely what is being proven absent.

## Preconditions

1. Each of the five assist surfaces (configuration suggestions, challenge copy, translation/localisation, style proposals, moderation assistance) has, at minimum, a defined suggestion-object contract to test against.

## Acceptance cases

| ID | Setup and action | Expected result | Failure/retry and evidence |
|---|---|---|---|
| L23-01 | Invoke each of the five AI-assist surfaces and inspect the returned object | Each returns a suggestion object with no direct write path to `payments`, `refunds`, or `challenges` status tables | Not run — TODO |
| L23-02 | Attempt to call a payment-capture, refund, payment-destination-change, or challenge-complete action directly from the AI-assist code path | Fails by design — no such direct path exists | Not run — TODO |
| L23-03 | Apply an AI suggestion (e.g., a style proposal) to a live surface | A separate, auditable human-confirmation event is recorded (who confirmed, when, what was suggested vs. applied) before the change takes effect | Not run — TODO |
| L23-04 | Search any marketing copy or in-product messaging for AI positioned as the primary launch message | AI is not the launch message anywhere in scope | Not run — TODO |

## Closure rules

Closes only when every row has a real pass/fail result with inline evidence (file paths for each of the five surfaces and their suggestion/confirm split, negative-test pass count for L23-02) replacing "Not run — TODO." No artifact/screenshot directory exists or may be created.

## Cleanup and rollback

All fixtures are synthetic and run without touching any production financial table. No cleanup beyond standard test-run teardown is required, since no AI-assist code path may write to payments/refunds/challenges by this suite's own acceptance criteria.

## Execution record — 2026-09-13

Executed against `bharatstudio-alerts` commit `dac8fc4`, migration `0121_v1_l23_ai_assist_bounded.sql`.

This record said `TODO — not started, no evidence exists yet` after the tests had already been written, run and committed. Recorded rather than silently fixed.

| Suite | File | Cases | Result |
|---|---|---|---|
| SQL | `packages/db/tests/l23-ai-assist-bounded.sql` | 13 checks | pass, inside SQL suite 51/51 |
| API routes | `apps/api/test/l23-assist-routes.test.ts` | 13 tests | 13/13, full suite 496/496, tsc 0 |
| Web page | `apps/web/app/dashboard/assist/l23-assist-page.test.tsx` | 6 tests | 6/6, full suite 324/324, tsc 0 |

Commands, re-run on a quiet tree 2026-09-13:
`sh packages/db/tests/run-sql-suite.sh` → `SQL SUITE: pass=51 fail=0` (real Postgres 16, `ON_ERROR_STOP=1`)
`cd apps/api && npx tsc --noEmit -p . && npm test` → tsc 0, 496 pass / 0 fail
`cd apps/web && npx tsc --noEmit && npm test` → tsc 0, 324 pass / 0 fail

**L23-01 — no direct financial write path.** Satisfied structurally, not by inspection alone: neither `assist_suggestions` nor `assist_confirmations` references `payments`, `refunds` or `challenges`, and `decide_assist_suggestion` writes only to those two tables. The SQL suite asserts `select count(*) from public.challenges` is unchanged after an accept, so an accepted suggestion is proven not to have reached a live surface. Route-level equivalent at `apps/api/test/l23-assist-routes.test.ts:88`.

**Provider-seam privacy.** `apps/api/test/l23-assist-routes.test.ts:180` asserts the exact key set the seam received and the absence of donor-, message- and payment-shaped strings.

**Not covered by this evidence:** no model provider is integrated, so every privacy claim here holds for the local rule-based generator only and must be re-proven against any real provider before one is wired. Nothing is proven in a deployed environment.
