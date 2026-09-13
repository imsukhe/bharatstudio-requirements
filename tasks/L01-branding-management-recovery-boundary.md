# L01 — Branding management recovery boundary

**Status:** `Locally verified; external deployment evidence remains open`
**Level:** L3
**Parent authority:** `L01-contracts-and-database-baseline.md`; `L03-alerts-web-and-creator-api.md`
**Test record:** [`../tests/TC-L01-branding-management-recovery-boundary.md`](../tests/TC-L01-branding-management-recovery-boundary.md)
**Review:** [`../reviews/2026-09-12-L01-branding-management-recovery-boundary-decision.md`](../reviews/2026-09-12-L01-branding-management-recovery-boundary-decision.md)

## Scope and acceptance

Make the authenticated Lottie management list and delete reads fail as a
redacted retryable 503 when their durable store rejects, matching the existing
upload behavior. Preserve 401/404/403 semantics and do not change storage,
authorization, assets, or deployment. Add deterministic outage tests and run
the full local verifier.

## Reproducible local evidence — 2026-09-12

- `apps/api/src/routes/branding.ts` now catches list and delete store
  rejections, logs only approved operational context, and returns the existing
  redacted `branding_store_unavailable` retryable 503 envelope.
- The focused route test injects secret-shaped database failure text into both
  operations and proves status 503, `retryable: true`, and no secret leakage.
- `pnpm --filter @bharatstudio/alerts-api exec tsx --test
  test/branding-routes.test.ts` passed 9/9; API TypeScript build passed.
- `pnpm verify:local` passed: contract/deployment checks, 116 migrations, 46
  SQL proofs, load/fault checks, API/web tests, builds, Go race/vet checks,
  and the three command-image builds.

This is local failure-mode evidence only. Deployment readiness still requires
staging database and browser rehearsal.
