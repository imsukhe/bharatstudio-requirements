# L01 — Viewer profile controls contract slice

**Status:** `Locally implemented and verified; external gates remain`  
**Level:** L3  
**Parent authority:** `L01-contracts-and-database-baseline.md`; `L14-viewer-identity-and-supporter-history.md`  
**Test record:** [`../tests/TC-L01-viewer-profile-controls-contract-slice.md`](../tests/TC-L01-viewer-profile-controls-contract-slice.md)  
**Review:** [`../reviews/2026-09-09-L01-viewer-profile-controls-contract-slice-decision.md`](../reviews/2026-09-09-L01-viewer-profile-controls-contract-slice-decision.md)

## Scope and security boundary

Publish strict v1 contracts for `GET /v1/viewer/channels/{channelId}/badges`
and `PUT /v1/viewer/profile-visibility`. Both require `viewerBearerAuth` and
must expose only the authenticated viewer's channel badges or their own
visibility/slug state. Contract fixtures and client parsers must reject account,
payment, provider, credential, and unknown fields. No provider, database,
financial, or public-profile behavior changes are authorized. The permitted
runtime change is fail-closed request validation/projection and accurate
conflict-versus-temporary-failure classification for this existing endpoint.

## Acceptance

- OpenAPI, fixtures and JSON schemas encode exact response/request bounds.
- Focused API tests prove authentication and narrow projections.
- Viewer client validates visibility response strictly.
- Contract validation, focused tests, and root verifier pass; evidence remains
  synthetic/local and external gates remain explicit.

## Delivered local evidence — 2026-09-09

- Added v1 OpenAPI operations, strict request/response schemas, positive
  fixtures, and hostile-field contract negatives for both routes. The OpenAPI
  contract now contains 56 paths and 63 operations; fixture validation covers
  29 fixtures.
- The API now narrows store results instead of spreading them into responses,
  rejects incoherent visibility requests (`public` without a slug and
  `private` with a slug), returns 503 rather than a misleading 401 when the
  authenticated profile dependency is absent, and distinguishes SQL conflict/
  invalid-input codes from unknown temporary store failures.
- Focused API proof: `pnpm --filter @bharatstudio/alerts-api exec tsx --test
  test/l14-viewer-profile-routes.test.ts` — 8/8 passed. It proves viewer auth,
  strict visibility requests, no leakage of injected account/payment/provider
  fields, conflict mapping, temporary-failure mapping, and missing-store
  fail-closed behavior.
- Focused browser proof: `pnpm --filter @bharatstudio/alerts-web exec tsx
  --test --experimental-test-module-mocks --import ./app/test-support/dom-env.ts
  app/viewer/lib/viewer-api-integrity.test.ts` — 2/2 passed. It rejects schema
  drift, identity fields, and contradictory visibility/slug results.
- Full deterministic local verifier: `pnpm verify:local` — pass. It completed
  contract and deployment negatives, 19 SQL files, 19 role-separated proofs,
  L09 load/fault 5/5 each, 291 API/web tests, production builds, Go race/vet
  for all declared services, and all three declared image builds.

This is synthetic/local evidence only. Provider, deployment, staging, device,
and production privacy/legal confirmation remain unproven and are not claimed.
