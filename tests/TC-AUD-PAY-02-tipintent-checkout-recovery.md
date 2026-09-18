# TC-AUD-PAY-02 — TipIntent checkout recovery acceptance

**Task:** `../active/tasks/AUD-PAY-02-tipintent-checkout-recovery.md`  
**Authority:** `../active/launch/08_AUDIT_REMEDIATION_AUTHORITY.md`  
**Owner:** **Sukhdev Singh**  
**Status:** `Passed locally — external evidence gates remain`

| ID | Acceptance criterion |
|---|---|
| PAY02.1 | A provider/order-service error leaves a ready TipIntent unconsumed but durably reserved to its original key/order ID; same-key retry reuses it. |
| PAY02.2 | A different idempotency key during an open reservation receives a safe conflict and performs no second provider call. Concurrent requests cannot create two reservations/orders. |
| PAY02.3 | Only a validated order result can finalize the matching reservation; used/expired/unknown states and no-data disclosure remain unchanged. Finalization failure is truthful/retryable. |
| PAY02.4 | Direct Razorpay dismissal/error preserves the in-memory idempotency key; explicit edit/success lifecycle and short-link retry are deterministic and never use browser storage. |
| PAY02.5 | Migration preserves RLS, role/grant/search-path constraints, old consumed rows and existing payment ledger/webhook authority; no new payment/provider/browser secret surface exists. |
| PAY02.6 | SQL/API/web/database integration/payment worker/build/contracts/harness, hostile audit, traceability and document consistency pass. |

## Result matrix — 2026-09-18

| ID | Local result | Evidence |
|---|---|---|
| PAY02.1 | Pass | API provider-error retry test preserves one stable order/key; SQL repeated reservation test passes. |
| PAY02.2 | Pass | API competing-key test makes one provider call; API/SQL different-key tests return only conflict state. |
| PAY02.3 | Pass | API mismatch and finalization-failure tests return retryable 503; SQL verifies exact key/order completion and same-key post-completion recovery. |
| PAY02.4 | Pass locally | Web tests prove dismissal reopens the existing provider order and retryable endpoint errors reuse the mounted-page key. Existing session storage contains only pending order ID/amount, never key. |
| PAY02.5 | Pass locally | Fresh `0001–0164` migration run and legacy TipIntent proof pass; new functions are SECURITY DEFINER, canonical-search-path, `bsa_app`-only, with no raw table grants. |
| PAY02.6 | Pass locally | Commands/results below; hostile self-review is recorded in the linked review. |

## Commands to record after implementation

```text
cd bharatstudio-alerts && pnpm db:test:all
cd bharatstudio-alerts && packages/db/tests/run-l03-application-behavior.sh
cd bharatstudio-alerts && pnpm --filter @bharatstudio/alerts-api test
cd bharatstudio-alerts && pnpm --filter @bharatstudio/alerts-web test
cd bharatstudio-alerts && pnpm --filter @bharatstudio/alerts-api build && pnpm --filter @bharatstudio/alerts-web build
cd bharatstudio-alerts && pnpm contracts:validate && pnpm harness:check && git diff --check
cd bharatstudio-requirements && python3 tools/traceability.py && python3 tools/doc_consistency.py
```

Provider sandbox and deployed migration/browser evidence remains external.

## Recorded execution

```text
pnpm db:test:all                                      # 87 pass, 0 fail
packages/db/tests/run-l03-application-behavior.sh    # 25 SQL files + integrations passed
pnpm --filter @bharatstudio/alerts-api test           # 939 pass, 0 fail
pnpm --filter @bharatstudio/alerts-web test           # 662 pass, 0 fail
pnpm --filter @bharatstudio/alerts-api build          # pass
pnpm --filter @bharatstudio/alerts-web build          # pass (34 routes)
pnpm contracts:validate && pnpm harness:check         # pass
git diff --check                                      # pass
pnpm verify:local                                     # full deterministic local gate, Go race/vet and three images passed
```
