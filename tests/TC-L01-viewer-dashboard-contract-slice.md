# TC-L01 — Viewer dashboard contract slice

**Status:** `Pass — local contract and application evidence`  
**Task:** [`../tasks/L01-viewer-dashboard-contract-slice.md`](../tasks/L01-viewer-dashboard-contract-slice.md)

| ID | Action | Expected result |
| --- | --- | --- |
| L01-VD-01 | Request dashboard without and with a viewer token | No token is rejected; own response follows the narrow v1 projection. |
| L01-VD-02 | Validate fixture and inject account/payment/provider identity fields | Fixture passes; each hostile widening fails strict validation. |
| L01-VD-03 | Run SQL and root local verifier | The 100-row database bound/isolation proof and full deterministic suite pass. |

## Evidence — 2026-09-09

L01-VD-01 passed: `apps/api/test/viewer-routes.test.ts` **8/8** rejects a
missing viewer bearer token and proves the authorised route returns only the
approved row fields. L01-VD-02 passed: `pnpm contracts:validate` validates the
new fixture and rejects account and payment identifier injection. L01-VD-03
passed: the root verifier completed with isolated **44/44** and role-separated
**19/19** SQL proofs, including the synthetic 101-relation dashboard-bound and
cross-viewer-isolation test. No real-user/provider/staging data was used.
