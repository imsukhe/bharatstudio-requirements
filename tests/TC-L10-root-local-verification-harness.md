# TC-L10 — Root local verification harness

**Status:** `Pass — local executable evidence`
**Task:** [`../tasks/L10-root-local-verification-harness.md`](../tasks/L10-root-local-verification-harness.md)

| Case | Expected result | Evidence |
| --- | --- | --- |
| Root application test | `pnpm test` runs both Alerts API and Alerts web test suites. | Pass inside `pnpm verify:local`: API 402/402 and web 289/289. |
| Deterministic local verifier | Contracts, deployment negatives, isolated full SQL proof suite, fresh role-separated migrations/service integrations, L09 load/fault scenarios, app tests/builds, Go race/vet checks, and three declared image builds execute from one root command. | Pass: `pnpm verify:local` from Alerts root on 2026-09-09: 44/44 isolated SQL and 19/19 role-separated SQL proofs. |
| Failure semantics | No later proof is treated as passing if an earlier proof exits nonzero. | The root script chains every proof with `&&`; its complete successful execution proves every preceding command exited zero. |
| Boundary | No provider, deployed staging, production database, or device call is asserted by local execution. | Pass: only existing disposable/local Docker harnesses and builds were used; external gates remain open. |
