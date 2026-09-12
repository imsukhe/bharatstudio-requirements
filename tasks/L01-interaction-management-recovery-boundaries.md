# L01 — Interaction-management recovery boundaries

**Status:** `Locally verified; external deployment evidence pending`  
**Level:** L3  
**Parent authority:** `L01-contracts-and-database-baseline.md`; `L16-interaction-menu-goals-and-widgets.md`  
**Test record:** [`../tests/TC-L01-interaction-management-recovery-boundaries.md`](../tests/TC-L01-interaction-management-recovery-boundaries.md)  
**Review:** [`../reviews/2026-09-09-L01-interaction-management-recovery-boundaries-decision.md`](../reviews/2026-09-09-L01-interaction-management-recovery-boundaries-decision.md)

## Scope

Map unexpected durable interaction-store failures on existing authenticated
management reads and mutations to redacted retryable 503 envelopes. Preserve
all established successful, authorization, validation, and business outcomes.

## Acceptance

Fault-inject each affected store operation, prove no raw error reaches a
response, rerun the full local verifier, and record evidence. No schema,
authorization, product, payment, provider, or deployment behavior changes.

## Local evidence — 2026-09-09

- Added redacted retryable 503 recovery for interaction-definition listing,
  vote option/tallies, paid tally, hype lifecycle/state, widget list/update/
  delete, and leaderboard reads. Existing success and domain outcomes are
  unchanged.
- One fault-injection test drives every changed route through a synthetic
  durable-store outage and proves a 503 with no underlying error text.
- API TypeScript, 293/293 API/web tests, and `pnpm verify:local` exit **0**
  pass; the verifier includes 116 migrations, 46 SQL proofs, contracts,
  deployment/load/fault/build, Go race/vet, and images.
