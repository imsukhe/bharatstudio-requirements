# Decision — L01 health/readiness contract slice

**State:** `Locally accepted after full deterministic verification`

The manifest-declared liveness/readiness interface is an external operational
consumer and therefore needs an exact, privacy-minimal contract. This slice is
documentation/fixture hardening only; it cannot prove deployed probes, IAM,
staging dependency behavior, or production rollout.

## Post-change review — 2026-09-09

The published operational projections are deliberately smaller than the API
error envelope and contain no host, dependency, credential, account, payment,
or provider material. Existing runtime behavior was not changed. Exact fixture
and API proofs pass. L10 removed the redundant public Dockerfile frontend
dependency and the root verifier, including all image builds, subsequently
passed. This remains local evidence rather than a passing release check.
