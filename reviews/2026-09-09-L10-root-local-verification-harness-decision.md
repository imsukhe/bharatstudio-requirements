# Decision — L10 root local verification harness

**Decision:** Approve the bounded local QA-harness correction.

The root test command currently omits the web suite even though the repository
contains the web application. That is a local regression-detection gap, not a
release gate. The approved remedy keeps application tests under `pnpm test` and
adds a separate one-command local verifier for database, contract, deployment,
Go and container evidence. It must preserve fail-fast behavior and make no
claim about external/provider/staging readiness.

## Implementation review — 2026-09-09

The root test now executes both application suites. `pnpm verify:local` uses
strict `&&` chaining to combine contract and deployment negatives, the
isolated full SQL suite, the fresh role-separated SQL/service/overlay harness,
deterministic L09 load/fault checks,
application tests/builds, all Go race/vet suites, and all declared image builds.
The command completed successfully. The evidence is local only, correctly
leaving provider, staging, deployment, device, store, capacity and rollback
gates outside its claim.
