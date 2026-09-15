# ENV-04 — measurement environment lane

**Authority:** [`../launch/07_BUILD_BOOTSTRAP_AUTHORITY.md`](../launch/07_BUILD_BOOTSTRAP_AUTHORITY.md) §3
**Status:** `Blocked — OBS/Chromium harness unavailable`

| Field | Value |
|---|---|
| **Scope phase** | `v1` non-production measurement environment only |
| **Owner** | **Sukhdev Singh** |
| **Tier and gate** | None; Phase 0.5 prerequisite, not release evidence |
| **Personal-data class** | Synthetic only; no real identities or payment data |
| **Provider or legal dependency** | External prerequisite recorded; no credentials committed |
| **Failure behaviour** | Fail closed and mark blocked/not-run when prerequisite or proof is absent |
| **Kill switch** | Disable only named disposable local/non-production resources |
| **Acceptance test** | infra validator `../bharatstudio-infra/tools/validate-measurement-manifest.mjs --template` validates the manifest; Alerts runner `../bharatstudio-alerts/scripts/measurement/run-local-measurement.sh --artifact /tmp/ENV-04.json` emits the redacted artifact |
| **Evidence location** | `tests/TC-ENV-04-measurement-environment.md` and corresponding review |
| **Rollback** | Remove only disposable fixtures/resources; retain redacted artifact and logs |

## Boundary

This record does not claim cloud, provider, device, OBS, staging, or production evidence.

## Control-specific result

OBS/Chromium version and Windows harness declarations; OBS execution remains not-run.
