# Review — AUD-PAY-02 TipIntent checkout recovery

**Status:** `Conditionally complete — hostile self-review passed locally`  
**Reviewer:** Sukhdev Singh (self-review until independent review is available)  
**Scope:** `AUD-PAY-02-tipintent-checkout-recovery.md`

## Required review checklist

- Inspect reserve/finalize transaction semantics, same-key replay, concurrent and
  different-key paths, expiry and legacy consumed rows. A provider failure may not
  burn the link or widen it into a duplicate-charge path.
- Confirm exact order/key binding before finalization, order-service mismatch/error
  handling, payment ledger/webhook authority and truthfulness of every HTTP outcome.
- Inspect migration grants, SECURITY DEFINER/search path, RLS, data minimization and
  forward rollback treatment of live reservations.
- Exercise browser dismissal, error, retry, edit and success lifecycle. Verify no
  storage of idempotency or payment data and no client provider secret path.
- Record exact source paths/results, reproducible redacted evidence, rollback proof,
  findings/disposition and independent-review status.

## Required disposition

Do not claim provider sandbox, financial, migration deployment, browser, staging or
production evidence from mocks/disposable local database alone.

## Review performed — 2026-09-18

**Reviewed implementation paths:** `packages/db/migrations/0164_v1_aud_pay_tipintent_checkout_recovery.sql`; `apps/api/src/domain/tipintent-types.ts`; `apps/api/src/db/tipintent-store.ts`; `apps/api/src/routes/public.ts`; `apps/api/test/l15-tipintent-public-routes.test.ts`; `apps/web/app/tips/[handle]/TipForm.tsx`; `apps/web/app/t/[token]/TipIntentConfirm.tsx`; their component tests; `packages/db/tests/l15-tipintent-short-link.sql`; and `contracts/openapi/v1.yaml`.

### Hostile findings and disposition

| Finding | Disposition |
|---|---|
| Original defect: eager `consume_tip_intent` burned a link before payment service success. | Fixed: row-locked reservation precedes dispatch; `complete_tip_intent_checkout` is the only new path to `consumed_at`. Provider/order failure leaves reservation unconsumed. |
| A different request key could have produced a second order. | Fixed: same locked row carries original key/order; different key gets no value/order fields and never calls provider. API competing-key proof covers it. |
| A valid provider response containing a different local order ID could have finalized/returned a mismatched order. | Fixed: route rejects it as retryable 503 before completion; API proof verifies recovery. |
| Completion could fail after durable order creation. | Fixed: 503 is returned; same-key retry returns the service's same order and completes. API proof covers this. |
| A lost 201 response after completion was initially blocked by the public `used` precheck. | Found during this review and fixed before closure: matching key now receives only its already-completed reservation; different key still receives no data. SQL and API recovery proofs pass. |
| Direct dismiss/error could allocate a new order. | Fixed: prepared direct orders lock mutation, expose explicit reopen, and do not clear mounted key on retryable failure; component tests prove no second order request. |
| Privacy/RLS regression from storing a key. | No reproducible local finding: raw token remains SHA-256 fingerprint only; checkout key is not returned by resolution/conflict states; new private functions are SECURITY DEFINER with canonical path and `bsa_app` grant only; fresh SQL suite passed. |

### Reproducible local review evidence

```text
pnpm db:test:all                                      # 87 pass, 0 fail
packages/db/tests/run-l03-application-behavior.sh    # 25 SQL files + real local integrations passed
pnpm --filter @bharatstudio/alerts-api test           # 939 pass, 0 fail
pnpm --filter @bharatstudio/alerts-web test           # 662 pass, 0 fail
pnpm --filter @bharatstudio/alerts-api build && pnpm --filter @bharatstudio/alerts-web build  # pass
pnpm contracts:validate && pnpm harness:check && git diff --check  # pass
pnpm verify:local                                     # complete local gate, Go race/vet and three production images passed
```

The migration was also applied from a fresh disposable database through the repository
harness (migrations `0001–0164`); it passed the legacy TipIntent proof and the new
reservation/recovery proof. No deployment or provider request was made.

### Disposition and limits

All reproducible local findings identified in this review are fixed and the task is
**conditionally complete**. This is a self-review by Sukhdev Singh; no independent
review is claimed. It is not evidence of real Razorpay sandbox behavior, an actual
browser checkout under configured Cloudflare/Razorpay credentials, deployed migration
rollback, staging observability, financial correctness, or production readiness.
