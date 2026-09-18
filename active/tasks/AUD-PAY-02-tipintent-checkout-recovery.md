# AUD-PAY-02 — Durable TipIntent checkout recovery and browser idempotency

**Status:** `Conditionally complete — locally verified; external checkout/deployment evidence pending`  
**Owner:** **Sukhdev Singh**  
**Authority:** `../launch/08_AUDIT_REMEDIATION_AUTHORITY.md` (AUD-PAY-02)  
**Acceptance record:** `../../tests/TC-AUD-PAY-02-tipintent-checkout-recovery.md`  
**Review record:** `../../reviews/2026-09-18-aud-pay-02-tipintent-checkout-recovery.md`

## Scope

Correct the audited checkout ordering defect. A TipIntent must reserve one stable
local payment intent and its validated idempotency key before dispatch to the payment
service, but receives `consumed_at` only after that same provider/order service call
returns a validated order. A retry with the same key must reuse its reservation and
the payment service's own durable order idempotency; a different key is refused while
the reservation is open, preventing duplicate provider orders. A same-key retry after
an ambiguous/lost successful HTTP response may recover exactly that completed local
order; a different key receives no order or tip data. A successful order is then
finalized against exactly the reserved order/key. Used, expired, unknown and
single-use links retain their existing public states.

Repair the direct `/tips/:handle` browser form so a Razorpay open/dismiss/failure does
not clear the current idempotency key. A prepared direct order locks mutable fields
and may reopen its existing provider checkout without allocating a second order; a
retryable order-endpoint failure reuses the in-memory key. It clears that key only on
an explicit data-changing edit before an order exists or terminal confirmed state.
The short-link form follows the same mounted-page retry semantics without persisting
either key in browser storage. The pre-existing session-scoped pending-order reference
remains limited to order ID and amount; it never contains an idempotency key.

## Data, security, failure behaviour and boundaries

- Add only the minimum TipIntent reservation metadata needed to bind an open checkout
  to its UUID/order and idempotency key. Raw token remains absent from SQL; no card,
  UPI, provider secret, new cookie, account or identity data is stored or returned.
- New SECURITY DEFINER functions use canonical search path, `bsa_app`-only execute,
  opaque token hash and row locking. They validate non-null UUID/key inputs and never
  grant raw table access. Existing order/payment ledger truth remains owned by the
  payment service and verified webhook path.
- Provider error, timeout or unknown result does not mark a TipIntent used. It leaves
  the reservation intact for the same key, which leads to the existing payment-order
  idempotency/claim/reconciliation mechanism. A second/different key cannot obtain
  its own reservation; no provider call occurs from that request.
- Once the order response is validated, finalization is tied to the exact reserved
  UUID/key. A failure to finalize returns retryable error and must never silently
  claim success; a payment service result remains reconciled through the existing
  order/webhook workflow. No refund/capture or provider action is added here.
- Boundaries remain browser → public API → authenticated payment service → provider;
  the browser never calls provider order APIs directly and other services never read
  TipIntent tables directly.

## Migration, rollback and deployment

Create one forward-only migration after `0163`; never alter `0097`. Migration `0164`
adds compatible
reservation metadata and replaces/extends only TipIntent private functions, preserving
legacy consumed records. Rollback is a new forward migration that preserves every
already-reserved order binding until its existing order is reconciled/expired; reverting
source alone after the migration is unsafe and prohibited. Deployment is normal API and
payment-service compatible rollout; no provider, secret, production or migration
execution is authorised by this task.

## Required verification

- SQL proves reserve/same-key replay/different-key refusal/finalize/used/expiry/race,
  RLS/grants/search path and no raw token/value leak.
- API tests prove provider failure leaves the link ready for the same-key retry,
  different-key retry makes no provider call, provider success finalizes, finalization
  failure is retryable, and old used/expired/unknown/public response contracts hold.
- Browser tests prove direct Razorpay dismiss/error retains the same key, and an
  explicit edit/success changes it only when allowed; no local/session storage use.
- Run migration and disposable database integration, payment worker/API/web suites,
  contract/build/harness checks and hostile review covering provider timeout, concurrent
  requests, link expiry, replay, payment/order mismatch, privacy and forward rollback.

## External evidence gate

Real Razorpay sandbox timeout/ambiguous-outcome/retry, deployed migration rehearsal,
and browser checkout evidence remain external. Local tests cannot claim provider,
staging, financial, deployment or production readiness.

## Local implementation evidence — 2026-09-18

**Implemented paths**

- `bharatstudio-alerts/packages/db/migrations/0164_v1_aud_pay_tipintent_checkout_recovery.sql` adds a nullable validated checkout key, row-locked reserve/complete functions, same-key completed-order recovery, and a fail-closed legacy `consume_tip_intent` compatibility definition. It retains no raw token and grants new functions only to `bsa_app`.
- `apps/api/src/domain/tipintent-types.ts`, `apps/api/src/db/tipintent-store.ts`, and `apps/api/src/routes/public.ts` replace eager consumption with reserve → payment service → returned-local-order-ID check → exact completion. The route returns a retryable 503 on provider, mismatched-order, or completion failure and does not expose a completed order to another key.
- `apps/web/app/t/[token]/TipIntentConfirm.tsx` retains its in-memory key across retryable failures, reopens an already-prepared checkout without a second order request, and never stores the key. `apps/web/app/tips/[handle]/TipForm.tsx` prevents mutable edits/new requests while a prepared order is outstanding and reopens that existing provider order.
- `contracts/openapi/v1.yaml` documents the same-key ambiguous-response recovery and different-key conflict contract.

**Redacted reproducible commands and results** (Alerts checkout at baseline `d5cebc6` plus this uncommitted corrective slice)

```text
pnpm db:test:all
# SQL SUITE: pass=87 fail=0 (164 migrations, including 0164)

packages/db/tests/run-l03-application-behavior.sh
# DB_TESTS_SQL_SUITE: 25 file(s) passed
# payment ingress/reconcile + worker-store integrations passed
# Overlay PostgreSQL listener integrations passed

pnpm --filter @bharatstudio/alerts-api test
# 939 pass, 0 fail

pnpm --filter @bharatstudio/alerts-web test
# 662 pass, 0 fail

pnpm --filter @bharatstudio/alerts-api build
pnpm --filter @bharatstudio/alerts-web build
# both passed; web generated 34 routes

pnpm contracts:validate && pnpm harness:check && git diff --check
# 78 fixtures; 151 paths / 178 operations; 3 OpenAPI negatives; harness and diff checks passed

pnpm verify:local
# full deterministic local gate passed: contracts/explain/harness/deployment,
# SQL + role-separated integration + extra harnesses, load/fault self-tests,
# API/web tests and builds, Go race/vet suites, and API/payment/worker images
```

Focused API proofs include provider failure with same-key recovery, second-key refusal
with no second provider call, order-ID mismatch, finalization failure, competing-key
concurrency, and same-key recovery after a lost successful response. SQL proof covers
reservation/replay/conflict/privacy/finalization/legacy-consume blocking/completed
recovery; browser tests cover dismissal reopening and retryable failures retaining the
same page-only key.

**Rollback proof:** the disposable migration harness applied migrations `0001–0164`
from an empty database and passed legacy TipIntent tests plus the new reservation proof.
No destructive down migration or source-only production rollback was executed. A real
rollback remains a separately approved forward migration that preserves every existing
reservation/payment binding.

**Unresolved external gates:** real Razorpay sandbox timeout/ambiguous-outcome recovery,
deployed migration rehearsal/rollback, configured Cloudflare+Razorpay browser checkout,
and staging/production observability remain unperformed and are not implied by this
conditional local completion.
