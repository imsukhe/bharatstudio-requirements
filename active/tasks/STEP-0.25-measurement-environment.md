# STEP-0.25 — Production-shaped non-production measurement environment

**Authority:** [`../launch/07_BUILD_BOOTSTRAP_AUTHORITY.md`](../launch/07_BUILD_BOOTSTRAP_AUTHORITY.md) §3
**Status:** `Conditionally complete — local controls and smoke evidence verified; external gates open; owner approval recorded 2026-09-15`

| Field | Value |
|---|---|
| **Scope phase** | `v1` — prerequisite for Phase 0.5 exit evidence; not production deployment |
| **Owner** | **Sukhdev Singh** |
| **Tier and gate** | None. Non-production measurement gate; production release remains separately blocked |
| **Personal-data class** | Synthetic only; no real identities, payments, provider tokens or receipts |
| **Provider or legal dependency** | Razorpay sandbox credentials may be supplied later; no live provider or production access |
| **Failure behaviour** | Any missing control, secret, capacity, network profile or artifact invalidates the run; fail closed and do not claim Phase 0.5 metrics |
| **Kill switch** | Disable the non-production deployment and revoke its synthetic credentials; no production impact |
| **Acceptance test** | Infra validator and Alerts runner validate the Cloud Run-shaped config, disposable PostgreSQL 16 smoke migrations/load, sandbox wiring, OBS/device declarations, 3G/4G profiles and redacted artifact; missing external prerequisites are explicit blocked/not-run states |
| **Evidence location** | `tests/TC-STEP-0.25-measurement-environment.md`, review record, redacted run artifact under requirements evidence (not secrets) |
| **Rollback** | Destroy only the named non-production resources and disposable database; restore prior local manifests; retain artifact and logs redacted |

## Scope boundary

This task defines and validates the safe measurement lane only. It does not deploy to
production, obtain provider approvals, use real customer data, or satisfy a release gate.
The implementation must use least-privilege non-production IAM, synthetic data, budget
limits, pinned harness versions and a deterministic pass/fail artifact.
