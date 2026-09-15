# ENV-08 — measurement environment lane

**Authority:** [`../launch/07_BUILD_BOOTSTRAP_AUTHORITY.md`](../launch/07_BUILD_BOOTSTRAP_AUTHORITY.md) §3
**Status:** `Blocked — target-concurrency staging environment unavailable`

| Field | Value |
|---|---|
| **Scope phase** | `v1` non-production measurement environment only |
| **Owner** | **Sukhdev Singh** |
| **Tier and gate** | None; Phase 0.5 prerequisite, not release evidence |
| **Personal-data class** | Synthetic only; no real identities or payment data |
| **Provider or legal dependency** | External prerequisite recorded; no credentials committed |
| **Failure behaviour** | Fail closed and mark blocked/not-run when prerequisite or proof is absent |
| **Kill switch** | Disable only named disposable local/non-production resources |
| **Acceptance test** | infra validator `../bharatstudio-infra/tools/validate-measurement-manifest.mjs --template` validates the manifest; Alerts runner `../bharatstudio-alerts/scripts/measurement/run-local-measurement.sh --artifact /tmp/ENV-08.json` emits the redacted artifact |
| **Evidence location** | `tests/TC-ENV-08-measurement-environment.md` and corresponding review |
| **Rollback** | Remove only disposable fixtures/resources; retain redacted artifact and logs |

## Boundary

This record does not claim cloud, provider, device, OBS, staging, or production evidence.

## Control-specific result

Target-concurrency gate remains not-run; no Phase 0.5 metric is claimed.

## Downstream dependency recorded 2026-09-16

RT-02's per-instance and per-channel overlay subscriber **ceiling values** are blocked on
this task. The enforcement mechanism and its retryable `503 overlay_admission_limited`
rejection ship built and tested but **unset**, because no authority states a number and
none is derivable from the 2,000-concurrent-overlay design target. This staged run is what
would produce one. See `active/tasks/RT-02.md` — owner decision of 2026-09-16.
