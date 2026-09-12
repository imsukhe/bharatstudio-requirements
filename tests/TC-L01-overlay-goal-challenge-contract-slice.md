# TC-L01 — Overlay goal and challenge read contract slice

**Status:** `Pass — full local verifier subsequently green`  
**Task:** [`../tasks/L01-overlay-goal-challenge-contract-slice.md`](../tasks/L01-overlay-goal-challenge-contract-slice.md)

| ID | Action | Expected result |
| --- | --- | --- |
| L01-OGC-01 | Request each route with no token, empty state, and valid overlay token | 401, exact null envelope, or exact scoped render model; missing dependency is 503. **Pass:** focused API 27/27. |
| L01-OGC-02 | Return store objects containing account/payment/provider/token/refund/unknown fields | Response strips all non-contract fields. **Pass:** exact route projection tests. |
| L01-OGC-03 | Validate positive and hostile fixtures plus browser guards | Contract and existing independent browser guards reject widening. **Pass:** 34 fixtures / 60 paths / 67 operations. |
| L01-OGC-04 | Run focused/full local checks | Focused routes, API build and diff check pass. **Held:** declared image build awaits recovery of the recorded external Docker registry timeout. |
