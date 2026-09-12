# L01 — Public vote-cast recovery boundary

**Status:** `Locally verified; external deployment evidence pending`  
**Level:** L3  
**Parent authority:** `L01-contracts-and-database-baseline.md`; `L16-interaction-menu-goals-and-widgets.md`  
**Test record:** [`../tests/TC-L01-public-vote-cast-recovery-boundary.md`](../tests/TC-L01-public-vote-cast-recovery-boundary.md)  
**Review:** [`../reviews/2026-09-09-L01-public-vote-cast-recovery-boundary-decision.md`](../reviews/2026-09-09-L01-public-vote-cast-recovery-boundary-decision.md)

## Scope and acceptance

An unexpected public vote-store failure must return a redacted retryable 503,
not a raw 500 or an `invalid_vote` client error. Existing valid, duplicate, and
invalid vote outcomes remain unchanged. Add focused fault injection, run the
full local verifier, and record evidence. No vote accounting, schema, token,
privacy, product, provider, or deployment change is authorized.

## Local evidence — 2026-09-09

- Public vote-store exceptions are safely logged and return the existing
  versioned `interaction_store_unavailable` retryable 503 envelope. Valid,
  duplicate, and `invalid_vote` outcomes retain their prior behavior.
- Focused fault injection proves the synthetic database text cannot enter the
  response. API TypeScript, all API/web tests, and `pnpm verify:local` exit 0
  passed, including 116 migrations, 46 SQL proofs, deployment/load/fault,
  builds, Go race/vet, and images.
