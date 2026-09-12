# TC-L17 — Paid challenges acceptance

**Status:** `Original refundable paid-challenge acceptance remains blocked; a separately documented non-refundable creator-goal alternative has local evidence through migration 0109`
**Task:** [`../tasks/L17-paid-challenges.md`](../tasks/L17-paid-challenges.md)
**Authority:** `bharatstudio-alerts/docs/BharatStudio-MASTER-PLAN.md` Part 6 (L17), Part 4 §4.8, Part 7 §7.7
**Repository:** `/Users/sukhdevsingh/Workspace/Bharat Studio/bharatstudio-alerts`
**Data:** Synthetic challenge/provider-capability fixtures and a sandbox/test-mode payment provider only. No live refund is executed against a real merchant account in this test suite.

## Preconditions

1. L19's `provider_capability_snapshots` is available or stubbed to report `refunds: true`/`false` for this suite.
2. L15's `!challenge` command is available or stubbed.
3. Disposable PostgreSQL test harness available for the five new challenge tables.

## Acceptance cases

| ID | Setup and action | Expected result | Failure/retry and evidence |
|---|---|---|---|
| L17-01 | Attempt to create a challenge on a channel whose provider capability snapshot reports `refunds: false` | Creation is rejected; challenges are invisible on that channel | Not run — TODO |
| L17-02 | Attempt to create a challenge on a channel whose snapshot reports `refunds: true` | Creation succeeds and the viewer-proposed flow becomes available | Not run — TODO |
| L17-03 | Walk the viewer-proposed flow: propose → moderator approves → payment link activates → viewer pays | State transitions to FUNDED in order; each transition is a distinct recorded `challenge_status_events` row | Not run — TODO |
| L17-04 | Propose a challenge, moderator rejects | Flow terminates at rejection; no payment link is ever activated | Not run — TODO |
| L17-05 | Simulate a failed/unconfirmed FUNDED challenge | Refund is initiated against the creator's merchant account (sandbox); refund status (initiated/pending/failed/completed) is surfaced to both creator and viewer | Not run — TODO |
| L17-06 | Simulate the sandbox refund failing (e.g., insufficient merchant balance) | Failure state is surfaced accurately to both parties; no product copy claims an unconditional or instant refund | Not run — TODO |
| L17-07 | Inspect all product-facing copy describing challenge refunds | Copy matches, verbatim: "Refund automatically initiated through the creator's connected payment provider." | Not run — TODO |
| L17-08 | Render the public challenge board with challenges in IN PROGRESS / NEXT / COMPLETED states, and load the OBS widget for the same channel | Both surfaces reflect identical state from `challenge_status_events`; OBS widget uses no second delivery path | Not run — TODO |
| L17-09 | Open a dispute on a refund-failed challenge, then resolve it | Dispute record is retained (append-only) after resolution; original challenge/refund history is unchanged | Not run — TODO |

## Closure rules

Closes only when every row has a real pass/fail result with inline evidence (migration filenames for the five tables, state-machine test file and pass count, refund-failure test) replacing "Not run — TODO." No artifact/screenshot directory exists or may be created. All refund evidence in this suite must come from a sandbox/test-mode provider — no live merchant refund is executed to close this record.

## Cleanup and rollback

All fixtures run against the disposable PostgreSQL harness and a sandbox payment-provider mode, torn down after the run. Challenge tables are new and additive; no production payment or refund is touched by this suite.

## 2026-09-08 reconciliation

The listed L17 cases remain **not passed**: the current implementation has no
refund capability snapshot, proposal/payment-link/dispute tables, provider
refund adapter, sandbox refund status, or `!challenge` connector. The missing
pieces are material, so this record deliberately does not convert them into
local passes.

Separately, the non-refundable alternative had reproducible local evidence at
the 2026-09-08 execution:
`sh packages/db/tests/run-sql-suite.sh` applies **110** migrations and passes
**44/44** isolated SQL proofs including `l17-paid-challenges`; `cd apps/api &&
npm test` passed **396/396** including `l17-challenges-routes`; `cd apps/web
&& npm test && npx tsc --noEmit && npm run build` passed **287/287**, typecheck,
and the challenge dashboard/overlay build routes. Its state machine and copy
are described in the associated L17 decision record, not substituted for the
original refund acceptance criteria.

**Regression recheck — 2026-09-09:** the dependency-installed full API and
web suites passed **398/398** and **289/289**, alongside SQL **44/44**. No
original refundable-challenge row has been promoted to pass.
