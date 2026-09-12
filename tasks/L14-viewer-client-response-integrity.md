# L14 — Viewer client response-integrity hardening

**Status:** `Implemented and locally verified; external gates remain open`  
**Level:** L3  
**Parent authority:** `L14-viewer-identity-and-supporter-history.md`; `L01-viewer-dashboard-contract-slice.md`  
**Test record:** [`../tests/TC-L14-viewer-client-response-integrity.md`](../tests/TC-L14-viewer-client-response-integrity.md)  
**Review/decision:** [`../reviews/2026-09-09-L14-viewer-client-response-integrity-decision.md`](../reviews/2026-09-09-L14-viewer-client-response-integrity-decision.md)

## Scope

The viewer web API client currently casts nested dashboard/session/deletion
responses after only an array/top-level check. Replace those casts with strict
runtime parsers aligned to the published response contracts. Reject malformed,
privacy-expanding, or wrong-enum nested values before rendering or local state.

Add deterministic client tests for a valid response and malformed nested
dashboard/session/deletion cases. Do not change server routes, database data,
financial semantics, token storage, or API contracts.

## Security, rollback and acceptance

This is client-side trust-boundary hardening: server data is still untrusted at
the browser boundary. Parsers must accept only documented fields/types and
return the existing narrow client types. Rollback is source-only, but should
not be used to relax validation. Local acceptance requires focused web tests,
web typecheck/build, contract validation, and the root local verifier; provider,
staging, production, device, and legal evidence remain external.

## Local evidence — 2026-09-09

`apps/web/app/viewer/lib/viewer-api.ts` now validates exact nested object keys,
UUIDs, date-times, non-negative decimal strings, list bounds, member-state,
session fields, and deletion disclosure fields before returning typed values.
`viewer-api-integrity.test.ts` proves valid dashboard/session/deletion parsing
and rejects malformed, privacy-expanding, wrong-enum and false-disclosure data.
The test sets an explicit synthetic local origin only during its request helper;
the production `getApiOrigin` fail-closed behavior is unchanged.

Focused web typecheck plus the integrity test passed **2/2**. `pnpm
verify:local` also passed: 27 fixtures, 54 paths, 61 OpenAPI operations, 44/44
isolated SQL, 19/19 role-separated SQL, API 402/402, web 289/289, app builds,
Go race/vet, L09 load/fault, deployment negatives, and all declared images.
No provider, deployed staging, production, device, or legal result is claimed.
