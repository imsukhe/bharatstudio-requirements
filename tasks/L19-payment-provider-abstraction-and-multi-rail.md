# L19 — Payment provider abstraction and multi-rail

**Status:** `Partial — CreatorPaymentProvider interface extracted with a Razorpay implementation, wired only to a new read-only capabilities endpoint, not to the live tip-order flow; no provider_capability_snapshots table exists; refunds correctly report unsupported; nothing here is proven in a deployed environment`
**Level:** L3
**Owner:** [OWNER — payments/API, unassigned]
**Depends on:** L04 (existing Razorpay implementation to extract behind the interface)
**Blocks:** L17 (refund-capability gate), L20/desktop QR work referencing dynamic QR
**Test record:** [`../tests/TC-L19-payment-provider-abstraction-and-multi-rail.md`](../tests/TC-L19-payment-provider-abstraction-and-multi-rail.md)

## Authority and evidence

Master plan Part 6, "L19 — Payment provider abstraction and multi-rail" (lines ~1019–1097), including the `CreatorPaymentProvider` interface listing and the Paytm eight conditions; Part 7 §7.1 (rail-by-rail status table).

## Objective

Make the payment layer provider-neutral from day one, so a cheaper verified UPI rail can be added without touching the event model.

## Tasks

1. Extract the current Razorpay implementation behind the `CreatorPaymentProvider` interface (`connectionCapabilities`, `createPayment`, `createQr`, `fetchPayment`, `refund`, `verifyWebhook`, `supportsUpiIntent`, `supportsDynamicQr`, `supportsRefunds`, `supportsRecurringPayments`, `supportsCards`, `supportsInternationalPayments`).
2. `provider_capability_snapshots` — persist what a connection can do, so features gate on capability, not provider name.
3. Razorpay OAuth (Technology Partner) connection alongside the existing manual `acc_XXX` path; both supported, OAuth preferred.
4. Dynamic/order-bound QR for desktop.
5. Preferred-UPI-app local preference (non-sensitive, browser-scoped): first payment offers Google Pay / PhonePe / BHIM-Other; subsequent visits lead with the remembered choice. Never store banking credentials.
6. Per-rail integrations as each provider's conditions are met (Paytm only after its eight written conditions are confirmed; Cashfree and PhonePe only after partner confirmation).

## Exact implementation boundary

In scope: the interface extraction, capability snapshots, Razorpay OAuth alongside manual `acc_XXX`, dynamic QR, UPI-app preference memory.

Out of scope / explicitly blocked: a "Connect Paytm" button — forbidden until all eight conditions in the master plan are confirmed **in writing**; Cashfree and PhonePe integrations — blocked on partner confirmation of connection model, settlement, authorisation and refund/status APIs; the direct PSP-bank rail — strategic, unscheduled; automatic payment routing between rails — explicitly rejected by the master plan ("do not build automatic routing... let the creator choose").

## Non-negotiable implementation rules

- The creator UI exposes capabilities, never provider plumbing.
- Do not build automatic routing across rails. The model is provider-neutral; the creator chooses.
- Never store banking credentials for the UPI-app preference memory — it is a non-sensitive, browser-scoped, last-used-app hint only.
- If Paytm ultimately offers only MID + Merchant Key (no OAuth-style scoped grant), that must be an **advanced** connection behind a proper secret-vault design — never the primary onboarding path, because the Merchant Key is a raw secret.
- No rail beyond Razorpay's existing manual/OAuth paths ships until its blocking conditions are confirmed in writing (see Definition gate).

## Definition gate

Per `governance/AGENTS.md`, this L3 work stops after definition pending explicit approval. Owner unassigned: [OWNER]. **Open decisions — not decided here, require dated primary evidence or written provider confirmation before any implementation of the gated rail:**

1. Paytm's eight conditions (platform/technology-partner status; creator KYC directly with Paytm; merchant linking without BharatStudio collecting PAN/bank documents; scoped/tokenised authorisation; standard UPI 0% pricing preserved; order/intent/QR creation; server-side payment and refund status; creator-direct settlement).
2. Cashfree's Embedded Merchant Onboarding eligibility and pricing (the pre-31-July-2026 0% offer is not assumed to still apply).
3. PhonePe's PG Partner Program connection model, settlement, authorisation and refund/status API availability.

## Acceptance criteria

- The extracted `CreatorPaymentProvider` interface has a Razorpay implementation passing the existing L04 payment/refund/webhook test suite unchanged in behavior.
- `provider_capability_snapshots` correctly reports `refunds: true` only for a connection that has verified refund-API support, proven by test — this is the exact gate L17 depends on.
- Razorpay OAuth and manual `acc_XXX` connections coexist; a channel can be on either without code branching outside the provider abstraction.
- No "Connect Paytm"/"Connect Cashfree"/"Connect PhonePe" UI affordance exists in the codebase until its respective blocking conditions are marked confirmed-in-writing in this task's evidence trail.
- The UPI-app preference is proven by test to store only a non-sensitive app-name string, never credentials.

## Evidence required for closure

Inline prose citation: exact file path for the `CreatorPaymentProvider` interface and its Razorpay implementation; migration filename for `provider_capability_snapshots`; test-suite pass count proving capability-gated refund reporting; for each gated rail, the dated written confirmation (or its absence, stated plainly) of the blocking conditions above. No artifact/screenshot directory.

## Rollback

The interface extraction is a refactor of existing L04 code behind a new abstraction; the existing Razorpay manual-`acc_XXX` path must continue to pass all existing L04 tests unchanged, so this task is reversible by keeping the concrete Razorpay class importable directly if the abstraction is rolled back. `provider_capability_snapshots` is new and additive. No new rail is connected in production without separate explicit approval and its written conditions on file.

## Batch 8 implementation slice — 2026-09-07 reconciliation

Verified by reading the code. This corrects the map's "TODO — not started" and its "NOT wired to live callers" framing, which was directionally right but imprecise.

**Built and locally test-proven:**
- `apps/api/src/domain/payment-provider-creator.ts`: the `CreatorPaymentProvider` interface, matching this task's Tasks item 1 method list (`connectionCapabilities`/`createPayment`/`createQr`/`fetchPayment`/`refund`/`verifyWebhook`, plus the `supports*` capability flags).
- `apps/api/src/domain/payment-provider-razorpay.ts`: the Razorpay implementation. **`refund()` throws `PaymentProviderNotImplementedError`** — its own doc comment states plainly that `services/payment-webhook-go/internal/reconcile/refund.go` and `refund_handler.go` only fetch and reconcile refund status; no call anywhere in the codebase initiates a refund. `connectionCapabilities()` correctly reports `supportsRefunds: false` as a result. This matches master plan 3.15 and is recorded there as a correct consequence of the no-custody rule (1.4), not a gap.
- Test evidence: `apps/api/test/l19-payment-provider.test.ts`, 5 test cases.

**Wired, but only partially — stated precisely:**
- The interface IS live-wired: `apps/api/src/routes/payment-accounts.ts` imports `createRazorpayPaymentProvider` and serves it through a new authenticated read-only route, `GET /v1/channels/:channelId/payment-accounts/razorpay/capabilities`.
- It is NOT wired to the money-moving path. Grep of `apps/api/src/routes/public.ts` (the real tip-order-creation route) finds zero references to `razorpay` or the provider interface — that route and the Go `payment-webhook` service go straight to Razorpay via `apps/api/src/db/payment-order-client.ts` and `services/payment-webhook-go/internal/provider/razorpay_orders.go`, unrelated to and untouched by this abstraction. So `createPayment`/`createQr`/`fetchPayment`/`verifyWebhook` on the new interface have no caller anywhere in the codebase yet — only `connectionCapabilities` does, via the read-only endpoint above.

**Not built — do not record as done:**
- `provider_capability_snapshots` — no migration or table of this name exists anywhere in `packages/db/migrations` (repo-wide search, no hits). Capability is reported live from `connectionCapabilities()` on every request; nothing persists a snapshot. This is the task's own item 2 and is unmet.
- Razorpay OAuth (Technology Partner) connection — no OAuth code path found alongside the existing manual `acc_XXX` path; unbuilt.
- Dynamic/order-bound QR for desktop, and the preferred-UPI-app local preference memory — no corresponding code found; unbuilt.
- Paytm/Cashfree/PhonePe integrations remain unintegrated. No dated written confirmation exists on file for any of the three blocking-condition sets in this task's Definition gate (Paytm's eight conditions, Cashfree's Embedded Merchant Onboarding pricing, PhonePe's PG Partner Program terms). No "Connect Paytm/Cashfree/PhonePe" UI affordance exists, correct per this task's own non-negotiable rule.

Evidence: `apps/api/src/domain/payment-provider-creator.ts`, `apps/api/src/domain/payment-provider-razorpay.ts`, `apps/api/src/routes/payment-accounts.ts:19-29`, `apps/api/test/l19-payment-provider.test.ts` (5 cases); absence confirmed by repo-wide grep for `provider_capability_snapshots` (no hits) and for `razorpay`/provider-interface references in `apps/api/src/routes/public.ts` (no hits). Nothing here is proven in a deployed environment.
