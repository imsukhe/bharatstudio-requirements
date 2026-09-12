# TC-L01 — Viewer profile controls contract slice

**Status:** `Pass — synthetic/local evidence recorded 2026-09-09`  
**Task:** `../tasks/L01-viewer-profile-controls-contract-slice.md`

| ID | Action | Expected result |
| --- | --- | --- |
| L01-VP-01 | Request badges with and without viewer auth, including store-only account/payment/provider fields | 200 returns the exact narrow projection; unauthenticated returns 401; missing profile dependency returns retryable 503. **Pass:** focused API test 8/8. |
| L01-VP-02 | Set visibility with public/no-slug, private/slug, duplicate, unavailable and valid inputs | Coherent requests only; 400 for invalid shape, 409 only for SQL conflict/input validation, 503 for unknown store failure, and narrow response only. **Pass:** focused API test 8/8. |
| L01-VP-03 | Validate positive fixture and inject identity/payment/provider/unknown response fields | Draft 2020-12 schemas reject all widening and private-with-slug contradiction. **Pass:** `pnpm contracts:validate`, 29 fixtures / 56 paths / 63 operations / 3 negatives. |
| L01-VP-04 | Give browser client malformed/widened visibility responses | Browser rejects schema drift, account identity and contradictory visibility state. **Pass:** focused web test 2/2. |
| L01-VP-05 | Run deterministic local regression suite | SQL, API/web, load/fault, builds, Go race/vet and images pass. **Pass:** `pnpm verify:local`; 19 SQL files, 19 role proofs, 291 API/web tests, L09 5/5 load and fault each. |

No live provider, deployment, staging, browser-device, or production privacy
evidence is represented by these results.
