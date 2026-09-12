# L01 — Public vote contract slice

**Status:** `Implemented and locally verified; remaining contract queue active`  
**Level:** L3  
**Authority:** L01 contract baseline and L16 interaction acceptance  
**Test record:** `../tests/TC-L01-public-vote-contract-slice.md`

## Scope

Publish only anonymous vote cast. Input is bounded option key plus opaque voter
fingerprint; output is only `counted`. No payment, account, raw IP, supporter
identity, tally or financial data is public. Server-side dedupe stays
authoritative. Rollback is OpenAPI-only.

## Evidence — 2026-09-09

`pnpm contracts:validate` passed with 18 fixtures, 42 paths and 49 operations.
The vote fixture rejects an injected viewer identity. Focused L16 route tests
passed 17/17; runtime inventory is 159/49/110/0
(literal/covered/pending/stale). Provider/device/staging and independent review
remain outside local evidence.
