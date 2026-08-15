# Phase 2 — Enterprise

**Status:** `Deferred / not in v1`  
**Legacy authority:** `requirements/28_ENTERPRISE_PAYMENT_ACCOUNTS_ROUTE_ALLOCATION_AND_SETTLEMENT.md` and `tasks/payments/P28-enterprise-payment-accounts-route-allocation-and-settlement.md`.

Phase 2 owns every Enterprise capability: organisation roles, invitations, bulk allocation, reporting, Razorpay Route, creator/enterprise split policy, settlement scheduling, finance/refund authority, transfers, reversals and audit views.

Before implementation, obtain written Razorpay capability confirmation and counsel/CA advice for the actual money model. Use immutable payment-policy snapshots; never recompute historical allocation from current policy. No Enterprise label, role, UI, allocation or fund movement may appear in v1.
