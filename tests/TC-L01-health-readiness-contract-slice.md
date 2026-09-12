# TC-L01 — Health and readiness contract slice

**Status:** `Pass — full local verifier subsequently green`  
**Task:** [`../tasks/L01-health-readiness-contract-slice.md`](../tasks/L01-health-readiness-contract-slice.md)

| ID | Action | Expected result |
| --- | --- | --- |
| L01-HR-01 | Validate health and ready/unready responses | Exact small public operational projections only. **Pass:** focused API 49/49. |
| L01-HR-02 | Inject runtime/credential/account/unknown fields | Schema rejects every widening. **Pass:** contract validator. |
| L01-HR-03 | Run focused API and repository verification | Contract validation and route inventory pass; the full local verifier including images subsequently passed after L10 hardening. |
