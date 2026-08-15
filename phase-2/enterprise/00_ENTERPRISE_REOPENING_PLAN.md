# Phase 2 Enterprise — reopening plan

**Status:** `Deferred`  
**Not a v1 task or implementation authority**  
**Legacy sources:**

- `/Users/sukhdevsingh/Workspace/Personal /bharatstudio-alerts/repositories/bharatstudio-alerts/requirements/28_ENTERPRISE_PAYMENT_ACCOUNTS_ROUTE_ALLOCATION_AND_SETTLEMENT.md`
- `/Users/sukhdevsingh/Workspace/Personal /bharatstudio-alerts/repositories/bharatstudio-alerts/tasks/payments/P28-enterprise-payment-accounts-route-allocation-and-settlement.md`

## Reopening gate

Before any Enterprise UI, role, allocation or payment code, obtain written provider and professional evidence for:

1. Razorpay Route/linked-account onboarding, account/KYC requirements, order attribution, transfer/reversal/refund/dispute behaviour, settlement controls, currencies and test mode.
2. Merchant-of-record and funds-flow model, TDS/GST/KYC/AML/FCRA/consumer/refund/privacy obligations, contracts and regional limits.
3. Product scope: enterprise seats, invitation/acceptance, automatic allocation at login, channel relationship, roles, reporting, billing ownership and support model.
4. Immutable effective-dated payment account/binding/policy snapshot model. Current policy can never change an old tip's split.
5. Finance access, step-up authentication, data visibility, export/audit, refund/release/reversal authority and emergency controls.

## Work sequence

| ID | Work | Required evidence |
|---|---|---|
| EN-00 | Approve commercial/legal/provider model | written provider + counsel/CA disposition |
| EN-01 | Define organisation, invitations, roles, allocations and lifecycle | privacy/RBAC acceptance matrix |
| EN-02 | Define immutable account/binding/policy/snapshot/transfer schema | migration/rollback/history tests |
| EN-03 | Implement creator-direct, enterprise-retained and Route adapters behind flags | adapter and negative-path tests |
| EN-04 | Implement pre-order effective-dated snapshot resolver | concurrency/historical-policy tests |
| EN-05 | Implement visibility and finance-control APIs | field filtering/step-up/audit tests |
| EN-06 | Implement transfers, scheduled release, refunds/reversals and reconciliation handlers | provider test-mode full/partial/reversal/dispute tests |
| EN-07 | Add scheduler definitions for private idempotent handlers | OIDC/retry/duplicate/recovery tests |
| EN-08 | Build enterprise dashboard/companion views | role/plan/visibility/accessibility tests |
| EN-09 | Pilot with controlled accounts, reconcile and review | explicit approval/rollback evidence |

## Critical historic-policy rule

For every payment, store the applied account binding and allocation policy version at order creation. Example: a ₹1,000 tip under Channel Alpha policy version 4 permanently retains its 85/15 split even if version 5 later becomes 70/30. Refunds/reversals read the stored snapshot, never the current channel/enterprise configuration.
