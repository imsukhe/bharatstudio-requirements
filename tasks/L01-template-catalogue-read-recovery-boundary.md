# L01 — Template catalogue read recovery boundary

**Status:** `Locally verified; external deployment evidence remains open`
**Level:** L3
**Parent authority:** `L01-contracts-and-database-baseline.md`; `L03-alerts-web-and-creator-api.md`
**Test record:** [`../tests/TC-L01-template-catalogue-read-recovery-boundary.md`](../tests/TC-L01-template-catalogue-read-recovery-boundary.md)
**Review:** [`../reviews/2026-09-14-L01-template-catalogue-read-recovery-boundary-decision.md`](../reviews/2026-09-14-L01-template-catalogue-read-recovery-boundary-decision.md)

## Scope and acceptance

Make the authenticated template catalogue list map a durable-store rejection to
the route's existing redacted retryable 503 envelope. Preserve its current
authentication, entitlement projection, data, and deferred template-runtime
scope. Add deterministic failure/redaction coverage and run full local
verification.

## Reproducible local evidence — 2026-09-14

- The authenticated list now catches a catalogue-store rejection, uses safe
  logging, and returns its existing `template_store_unavailable` retryable 503
  envelope rather than reaching the generic 500 handler.
- Focused tests pass 5/5, preserving successful, unauthenticated, malformed-ID,
  and absent-store results while proving a secret-shaped store exception is
  redacted as 503.
- API TypeScript build and `pnpm verify:local` pass, including contracts,
  deployment validation, 116 migrations, 46 SQL proofs, load/fault, API/web,
  Go race/vet, and command-image checks.

This is local evidence only. The deferred template runtime and deployment
rehearsal remain governed/open work, not production-readiness claims.
