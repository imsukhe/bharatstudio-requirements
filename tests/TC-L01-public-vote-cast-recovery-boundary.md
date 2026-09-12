# TC-L01 — Public vote-cast recovery boundary

**Status:** `Pass — locally reproducible 2026-09-09; external evidence pending`  
**Task:** [`../tasks/L01-public-vote-cast-recovery-boundary.md`](../tasks/L01-public-vote-cast-recovery-boundary.md)

| ID | Action | Expected result |
| --- | --- | --- |
| L01-PVC-01 | Make the public vote store reject | Redacted retryable 503; no raw failure text. |
| L01-PVC-02 | Exercise valid/duplicate/invalid outcomes and full verifier | Existing public vote semantics remain intact. |

**Evidence:** injected rejection returns a redacted retryable 503, while the
existing valid/duplicate/invalid test cases stay green. Full verifier exit 0:
46/46 SQL and all API/web, contract, deployment, load/fault, build, race/vet,
and image checks pass.
