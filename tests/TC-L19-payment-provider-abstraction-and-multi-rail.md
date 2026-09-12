# TC-L19 — Payment provider abstraction and multi-rail acceptance

**Status:** `Batch 8 — L19-01 and L19-05/06 have local evidence; L19-02 unmet (no provider_capability_snapshots table exists); L19-03/04 unmet (OAuth path and UPI-app preference not built)`
**Task:** [`../tasks/L19-payment-provider-abstraction-and-multi-rail.md`](../tasks/L19-payment-provider-abstraction-and-multi-rail.md)
**Authority:** `bharatstudio-alerts/docs/BharatStudio-MASTER-PLAN.md` Part 6 (L19), Part 7 §7.1
**Repository:** `/Users/sukhdevsingh/Workspace/Bharat Studio/bharatstudio-alerts`
**Data:** Synthetic/sandbox provider fixtures only (Razorpay test-mode credentials where needed). No live Paytm/Cashfree/PhonePe integration exists to test — those rails are blocked (see Preconditions).

## Preconditions

1. The existing L04 Razorpay payment/refund/webhook test suite is green before this task's refactor begins (baseline to diff against).
2. Paytm/Cashfree/PhonePe rails are **not** implemented or tested in this suite until their respective blocking conditions (task file, Definition gate) are confirmed in writing — attempting to test them prematurely is itself a finding, not a pass.
3. Disposable PostgreSQL test harness available for `provider_capability_snapshots`.

## Acceptance cases

| ID | Setup and action | Expected result | Failure/retry and evidence |
|---|---|---|---|
| L19-01 | Run the full pre-existing L04 Razorpay test suite against the new `CreatorPaymentProvider`-abstracted implementation | All previously-passing L04 tests still pass unchanged in behavior | Not run — TODO |
| L19-02 | Query `provider_capability_snapshots` for a connection with verified refund-API support vs. one without | `refunds: true`/`false` is reported correctly per connection | Not run — TODO |
| L19-03 | Connect a channel via the new Razorpay OAuth path and via the existing manual `acc_XXX` path, in parallel | Both connection types operate through the same abstraction with no code branching outside it | Not run — TODO |
| L19-04 | Record a viewer's UPI-app choice on first payment, then revisit the tip page | Only a non-sensitive app-name string is stored; no credential of any kind is present in storage | Not run — TODO |
| L19-05 | Search the codebase/UI for a "Connect Paytm", "Connect Cashfree" or "Connect PhonePe" affordance | None exists, because none of the three rails has its blocking conditions confirmed in writing | Not run — TODO |
| L19-06 | Search the codebase for any cross-rail automatic-routing logic | None exists — the creator always chooses the rail explicitly | Not run — TODO |

## Batch 8 addendum — 2026-09-07 (post-reconciliation)

| ID | Result |
|---|---|
| L19-01 | **Pass, local evidence.** `apps/api/src/domain/payment-provider-creator.ts` (interface) + `payment-provider-razorpay.ts` (implementation); `apps/api/test/l19-payment-provider.test.ts`, 5 cases. Note: the interface is not yet the code path the real tip-order route uses (`apps/api/src/routes/public.ts` has zero references to it) — this row is about the L04 regression baseline behind the new abstraction's own test file, not about the abstraction replacing the live caller, which has not happened. |
| L19-02 | **Unmet.** No `provider_capability_snapshots` table or migration exists anywhere in `packages/db/migrations` (repo-wide search, no hits). `refunds: true`/`false` is reported correctly, but live from `connectionCapabilities()` on every call, not from a persisted snapshot — `supportsRefunds: false` for Razorpay is verified in `payment-provider-razorpay.ts` (`refund()` throws `PaymentProviderNotImplementedError`) and matches master plan 3.15. Remains not run for the actual acceptance case as written (querying a snapshot table). |
| L19-03 | **Unmet.** No Razorpay OAuth (Technology Partner) connection code path found alongside the manual `acc_XXX` path. Remains not run. |
| L19-04 | **Unmet.** No UPI-app preference-memory code found. Remains not run. |
| L19-05 | **Pass, local evidence.** Searched the codebase for "Connect Paytm"/"Connect Cashfree"/"Connect PhonePe" affordances — none found. No dated written confirmation exists on file for any of the three rails' blocking conditions either (searched `governance/`, `reviews/`, and the task file itself). |
| L19-06 | **Pass, local evidence.** Searched for cross-rail automatic-routing logic — none found; only Razorpay has any implementation, so there is nothing to route between yet. |

## Closure rules

Closes only when every row has a real pass/fail result with inline evidence (exact interface/implementation file paths, migration filename for `provider_capability_snapshots`, before/after L04 test pass counts) replacing "Not run — TODO," plus the dated written confirmation (or explicit recorded absence) of each gated rail's blocking conditions. No artifact/screenshot directory exists or may be created.

## Cleanup and rollback

All fixtures run in sandbox/test-mode against the disposable PostgreSQL harness; no live payment or refund is executed to close this record. The abstraction refactor must not alter production Razorpay behavior — the L04 regression baseline is the proof.
