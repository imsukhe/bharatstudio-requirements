# TC-L01 — Overlay interaction state contract slice

**Status:** `Pass — locally reproducible 2026-09-09; external evidence pending`  
**Task:** [`../tasks/L01-overlay-interaction-state-contract-slice.md`](../tasks/TC-L01-overlay-interaction-state-contract-slice.md)

| ID | Action | Expected result |
| --- | --- | --- |
| L01-OIS-01 | Request each state endpoint with missing token/dependency and valid token | 401, retryable 503, or exact scoped state. |
| L01-OIS-02 | Inject sensitive/unknown fields from fake stores | Named projection strips every non-contract field. |
| L01-OIS-03 | Validate positive and hostile fixtures/browser guards | Exact contract rejects widening and malformed data. |
| L01-OIS-04 | Run focused/full verification | Reproducible local pass recorded. |

**Evidence:** API tests inject account/channel/payment/provider/token/refund
fields into every typed overlay store response and prove exact projection;
missing and rejected stores return retryable 503 while missing bearer returns
401. Schema negatives reject payment/provider/refund widening, negative
counts/amounts, invalid timestamps, and zero rank. `pnpm verify:local` exit
0: contracts 38/64/71, SQL 46/46, API/web 293/293, builds/race/vet/images
green. No staging, provider, OBS, or browser-device claim is made.
