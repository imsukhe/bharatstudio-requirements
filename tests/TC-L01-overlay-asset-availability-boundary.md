# TC-L01 — Overlay asset availability boundary

**Status:** `Pass — locally reproducible 2026-09-09; external evidence pending`  
**Task:** [`../tasks/L01-overlay-asset-availability-boundary.md`](../tasks/L01-overlay-asset-availability-boundary.md)

| ID | Action | Expected result |
| --- | --- | --- |
| L01-OAA-01 | Test no bearer, unwired store, and rejected store per asset read | 401 only for no bearer; otherwise redacted 503. |
| L01-OAA-02 | Test successful scoped artifacts and unknown IDs | Existing 200/404/no-store behavior persists. |
| L01-OAA-03 | Run full local verification | Reproducible evidence recorded. |

**Evidence:** absent stores and injected failures are 503 with no raw error;
missing bearer remains 401; success and unknown artifact cases retain 200/404
and private no-store caching. Full verifier exits 0 with SQL 46/46 and all
contract, API/web, deployment, load/fault, build, race/vet, and image checks.
