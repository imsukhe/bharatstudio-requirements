# TC-L01 — Interaction-management recovery boundaries

**Status:** `Pass — locally reproducible 2026-09-09; external evidence pending`  
**Task:** [`../tasks/L01-interaction-management-recovery-boundaries.md`](../tasks/L01-interaction-management-recovery-boundaries.md)

| ID | Action | Expected result |
| --- | --- | --- |
| L01-IMR-01 | Make each durable interaction store operation reject | Route returns redacted retryable 503, never 500. |
| L01-IMR-02 | Run full local verification | Existing successful and denial behavior remains green. |

**Evidence:** all injected management store failures return the versioned
`interaction_store_unavailable` envelope with `retryable: true`; the synthetic
database message is absent. Full verifier exit 0: SQL 46/46, API/web 293/293,
contracts, deployment, load/fault, builds, Go race/vet, and images green.
