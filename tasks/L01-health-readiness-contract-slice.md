# L01 — Health and readiness contract slice

**Status:** `Locally implemented and verified`  
**Level:** L3  
**Parent authority:** `L01-contracts-and-database-baseline.md`; `L09-observability-load-failure.md`; `L10-release-readiness-and-rollout.md`  
**Test record:** [`../tests/TC-L01-health-readiness-contract-slice.md`](../tests/TC-L01-health-readiness-contract-slice.md)  
**Review:** [`../reviews/2026-09-09-L01-health-readiness-contract-slice-decision.md`](../reviews/2026-09-09-L01-health-readiness-contract-slice-decision.md)

## Scope

Publish exact operational contracts for existing unauthenticated `/healthz` and
`/readyz` probe routes used by the API deployment manifest. Health returns only
a bounded service identity and liveness status. Readiness returns either the
single ready projection or one of the two bounded non-secret reasons already
implemented for missing/unavailable runtime adapters.

No route behavior, IAM, database, payment, provider, user, deployment, or
monitoring configuration changes are authorized. Fixtures are synthetic and
must reject runtime, credential, database, account, and unknown fields.

## Acceptance

- OpenAPI has exact success and unready responses without an auth scheme.
- Positive fixture and hostile-field negatives validate under Draft 2020-12.
- Existing API health/readiness tests and the root verifier pass, or any
  external verification failure is recorded precisely rather than hidden.
- Deployment/staging/probe/IAM evidence remains an external gate.

## Local evidence — 2026-09-09

- Added exact unauthenticated OpenAPI operations, Draft 2020-12 schemas and
  three synthetic fixtures for liveness, ready, and unready states. The
  fixture validator injects database/runtime, credential, and account fields
  and rejects each widening.
- `pnpm contracts:validate` passed: 32 fixtures, 58 paths, 65 operations and
  three hostile OpenAPI mutations. Runtime inventory now reports 159 literal
  operations, 65 published, 94 pending, and zero stale published operations.
- Focused API health/readiness/security suite passed 49/49.
- The complete verifier subsequently passed after L10 removed the redundant
  frontend dependency. No staged/deployed probe, IAM, production, or
  monitoring proof is claimed.
