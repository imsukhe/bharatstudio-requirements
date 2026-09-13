# L01 — Overlay asset OpenAPI contracts

**Status:** `Locally verified; external deployment evidence remains open`
**Level:** L3  
**Parent authority:** `L01-contracts-and-database-baseline.md`; `L16-interaction-menu-goals-and-widgets.md`  
**Test record:** [`../tests/TC-L01-overlay-asset-openapi-contracts.md`](../tests/TC-L01-overlay-asset-openapi-contracts.md)  
**Review:** [`../reviews/2026-09-09-L01-overlay-asset-openapi-contracts-decision.md`](../reviews/2026-09-09-L01-overlay-asset-openapi-contracts-decision.md)

## Scope and acceptance

Publish v1 OpenAPI contracts for existing overlay Lottie list/artifact and
audio artifact routes, including bearer security, UUID parameters, JSON list,
binary response, 401/404/503, and private no-store behavior. Add fixture and
negative contract proof, then run full local verification. No runtime asset,
token, privacy, storage, or deployment behavior changes.

## Reproducible local evidence — 2026-09-12

- Added the three exact runtime operations to `contracts/openapi/v1.yaml`:
  Lottie list, Lottie artifact, and TTS audio artifact. Each requires the
  overlay bearer scheme and UUID path parameters; artifact reads declare the
  exact `Cache-Control: private, no-store` response invariant.
- Added a redacted Lottie-list fixture plus a strict Draft 2020-12 schema.
  Negative proofs reject an injected channel identifier and an unsupported
  display style, preventing projection widening and slot-enum drift.
- `pnpm contracts:validate` passed with 39 fixtures, 67 paths, 74 operations,
  local references resolved, and all three OpenAPI negative cases rejected.
- `pnpm contracts:route-inventory` found 159 literal runtime operations, 74
  covered by the approved OpenAPI, 85 intentionally outside its published
  surface, and zero stale published operations.
- `pnpm verify:local` passed: deployment checks, all 116 PostgreSQL migrations
  and 46 SQL proofs, load/fault checks, API/web tests, TypeScript builds, Go
  race/vet checks, and API/payment/worker image builds.

This is local evidence only. Deployed overlay/browser cache behavior and
provider/device evidence remain deployment gates and are not represented as
production readiness.
