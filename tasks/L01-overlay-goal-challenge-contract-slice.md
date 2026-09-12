# L01 — Overlay goal and challenge read contract slice

**Status:** `Locally implemented and verified`  
**Level:** L3  
**Parent authority:** `L01-contracts-and-database-baseline.md`; `L16-interaction-menu-goals-and-widgets.md`; `L17-paid-challenges.md`  
**Test record:** [`../tests/TC-L01-overlay-goal-challenge-contract-slice.md`](../tests/TC-L01-overlay-goal-challenge-contract-slice.md)  
**Review:** [`../reviews/2026-09-09-L01-overlay-goal-challenge-contract-slice-decision.md`](../reviews/2026-09-09-L01-overlay-goal-challenge-contract-slice-decision.md)

## Scope

Publish strict v1 contracts and explicit API projections for existing
token-scoped overlay reads:

- `GET /v1/overlay-goals/{overlayId}`;
- `GET /v1/overlay-challenges/{overlayId}`.

Both require `overlayToken` bearer authorization and return only an exact
render-safe object or `null`. They must not expose channel/account/payment/
provider/credential/refund/description/internal lifecycle data. The server
must map named fields instead of returning raw store objects; browser widgets
remain the independent second validation boundary.

## Data/security/deployment/rollback

No migration, store query, token verification, public goal/challenge semantics,
payment/refund behavior, transport, provider, or deployment model changes are
authorized. This hardens response serialization and contracts only. Rollback
is a controlled contract/source revision and must not restore raw spreads.
Provider, staging, OBS/browser-device, deployed token, and production evidence
remain external gates.

## Acceptance

- OpenAPI and fixtures capture exact nullable read envelopes, overlay bearer
  auth, parameter constraints, and 401/503 outcomes.
- Hostile server/store fields are stripped; fixture negatives reject every
  sensitive/unknown field.
- Focused route/browser/contract checks and local verifier evidence are
  recorded accurately; no production readiness is claimed.

## Local evidence — 2026-09-09

- API routes now distinguish absent overlay credentials (401) from a missing
  overlay dependency (retryable 503), and explicitly project only the seven
  goal or eight challenge render fields. Injected channel/payment/access-token
  and provider/refund fields cannot cross the route boundary.
- Added OpenAPI paths, Draft 2020-12 schemas, positive fixtures and hostile
  fixture mutations. `pnpm contracts:validate` passed 34 fixtures, 60 paths,
  67 operations and three structural negatives.
- Focused API routes passed 27/27; the complete API/web suite subsequently
  passed 293/293. API TypeScript build and `git diff --check` passed. Inventory
  is 159 runtime operations, 67 published, 92 pending and zero stale
  operations.
- Full image verification remains held only by the separately recorded public
  Docker registry timeout; staged browser/OBS/device/provider/deployment
  evidence remains unperformed and is not claimed.
