# L10 — Root local verification harness

**Status:** `Implemented locally — executable evidence recorded`
**Level:** L3
**Authority:** L10 release-readiness supporting evidence

## Scope

Make the Alerts root test surface truthful and provide one deterministic,
locally executable verification command. Before this slice, `pnpm test` ran the
API tests only and could report success while the web application regressed.

The new local verifier must run the published-contract and deployment checks,
the isolated full SQL proof suite, the disposable PostgreSQL
migration/integration harness, deterministic L09 load and fault scenarios, API
and web tests, both production builds, race/vet checks for every Go service,
and all declared service-image builds. It is supporting
local evidence only; it does not deploy, contact a payment provider, or
substitute for staging/device/provider evidence.

## Security, rollback, and limits

- The verifier uses existing disposable/local test harnesses and Docker builds;
  it must not take production credentials or issue provider requests.
- It exposes no new runtime endpoint, schema, or data model.
- Rollback is removal of the root script and restoration of the prior root test
  command. It cannot invalidate already recorded test evidence.
- Real provider sandbox, deployed IAM/database, Cloud Run rollout, device,
  store, capacity and rollback rehearsals remain explicit external gates.

## Acceptance

1. `pnpm test` executes API and web suites, failing if either fails.
2. `pnpm verify:local` runs every listed deterministic local proof in order and
   exits nonzero on the first failed proof.
3. A green execution records reproducible command output in its test/review
   records without claiming release readiness.

## Local evidence — 2026-09-09

From the Alerts repository root, `pnpm verify:local` completed successfully.
It passed 26 contract fixtures, 53 paths/60 OpenAPI operations and three
negative OpenAPI cases; deployment validation plus one positive/four hostile
negative manifest cases; 114 migrations and 44 isolated SQL proofs; fresh
migrations and 19 role-separated SQL proofs;
payment/worker SQL adapters; two-listener and cross-replica overlay replay;
L09 load/fault scenarios; API **402/402** and web **289/289** tests; both app
production builds; all three Go race/vet matrices; and API, payment, and worker
image builds.

This is a local deterministic regression proof, not a provider, staging,
production, device, store, capacity, or rollback rehearsal.
