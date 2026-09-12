# L01 — Goal and challenge read recovery boundaries

**Status:** `Locally verified; external deployment evidence pending`  
**Level:** L3  
**Parent authority:** `L01-contracts-and-database-baseline.md`; `L16-interaction-menu-goals-and-widgets.md`; `L17-paid-challenges.md`  
**Test record:** [`../tests/TC-L01-goal-challenge-read-recovery-boundaries.md`](../tests/TC-L01-goal-challenge-read-recovery-boundaries.md)  
**Review:** [`../reviews/2026-09-09-L01-goal-challenge-read-recovery-boundaries-decision.md`](../reviews/2026-09-09-L01-goal-challenge-read-recovery-boundaries-decision.md)

## Scope and acceptance

Map unexpected failures in existing goal/challenge management list/get and
overlay render reads to their respective redacted retryable 503 envelopes.
Preserve 401, 404, success projections, and all mutation semantics. Add
fault-injection tests and full local verification. No schema, payment,
entitlement, token, privacy, product, provider, or deployment change.

## Local evidence — 2026-09-09

- Goal/challenge management list/get and their overlay reads safely log and
  return their distinct redacted retryable 503 envelopes on store rejection.
  Existing 401, 404, and successful render projections are retained.
- Focused tests inject synthetic store outages into all six reads and prove no
  backing-store text escapes. TypeScript, all API/web tests, and
  `pnpm verify:local` exit 0 pass, including 116 migrations, 46 SQL proofs,
  deployment/load/fault/build, Go race/vet, and images.
