# L01 — Overlay asset availability boundary

**Status:** `Locally verified; external deployment evidence pending`  
**Level:** L3  
**Parent authority:** `L01-contracts-and-database-baseline.md`; `L16-interaction-menu-goals-and-widgets.md`  
**Test record:** [`../tests/TC-L01-overlay-asset-availability-boundary.md`](../tests/TC-L01-overlay-asset-availability-boundary.md)  
**Review:** [`../reviews/2026-09-09-L01-overlay-asset-availability-boundary-decision.md`](../reviews/2026-09-09-L01-overlay-asset-availability-boundary-decision.md)

## Scope and acceptance

For overlay Lottie listing/artifact and audio artifact reads, preserve missing
bearer as 401; map an absent/rejected backing store to a redacted retryable
503. Preserve scoped 404 and private no-store byte-serving behavior. Add
fault-injection tests and full local verification. No asset access, token,
privacy, schema, product, provider, or deployment semantics change.

## Local evidence — 2026-09-09

- Lottie list/artifact and audio artifact routes retain 401 only for a missing
  bearer, return their distinct redacted retryable 503 envelopes for absent or
  failed stores, and preserve scoped 404 plus `private, no-store` asset bytes.
- Tests inject a synthetic backing-store outage into all three reads and prove
  the failure text cannot escape. TypeScript, all API/web tests, and
  `pnpm verify:local` exit 0 pass, covering 116 migrations, 46 SQL proofs,
  deployment/load/fault, builds, Go race/vet, and images.
