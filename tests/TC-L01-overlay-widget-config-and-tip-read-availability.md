# TC-L01 — Overlay widget configuration and tip-read availability

**Status:** `Pass — locally reproducible 2026-09-09; external evidence pending`  
**Task:** [`../tasks/L01-overlay-widget-config-and-tip-read-availability.md`](../tasks/L01-overlay-widget-config-and-tip-read-availability.md)

| ID | Action | Expected result |
| --- | --- | --- |
| L01-OWA-01 | Request all five endpoints without bearer | 401 without a dependency probe. |
| L01-OWA-02 | Request with bearer and absent/rejected dependency | Redacted retryable 503. |
| L01-OWA-03 | Return a polluted widget config | Exact top-level projection omits internal/account/payment/provider fields. |
| L01-OWA-04 | Run full local verifier and diff audit | Reproducible local result recorded. |

**Evidence:** focused tests cover missing bearer, unwired dependency, rejected
store/query, success, and polluted config branches for all five reads. They
prove retryable 503s do not contain the synthetic database failure. Full local
verifier exit 0: contracts 38/64/71, SQL 46/46, API/web 293/293, builds,
race/vet, and image checks green.
