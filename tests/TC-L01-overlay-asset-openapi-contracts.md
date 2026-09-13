# TC-L01 — Overlay asset OpenAPI contracts

**Status:** `Pass — local evidence recorded 2026-09-12`
**Task:** [`../tasks/L01-overlay-asset-openapi-contracts.md`](../tasks/L01-overlay-asset-openapi-contracts.md)

| ID | Action | Expected result |
| --- | --- | --- |
| L01-OAC-01 | Validate list, binary, and error OpenAPI responses | Exact v1 runtime contract is published. |
| L01-OAC-02 | Run fixture negatives and full verifier | Contract widening/regression is rejected. |
| L01-OAC-03 | Exercise missing and malformed overlay bearer inputs | Asset reads reject both as 401 before a store call. |
| L01-OAC-04 | Exercise artifact cache headers | Both Lottie and WAV reads return `Cache-Control: private, no-store`. |

## Evidence

- `pnpm contracts:validate` — pass: 39 strict fixtures, including the new
  Lottie-list projection; both new negative fixture cases rejected.
- `pnpm --filter @bharatstudio/alerts-api test` — pass: 418 tests. The asset
  tests prove list/artifact authorization, scoped bytes, 404, unwired/rejected
  store 503 redaction, malformed bearer rejection, and no-store headers.
- `pnpm verify:local` — pass, including migration/SQL/load/fault/API/web/build/
  Go-race-and-vet/container-image stages.
