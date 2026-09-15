# STEP-−1 — Approve and link the external-evidence register

**Authority:** [`../launch/07_BUILD_BOOTSTRAP_AUTHORITY.md`](../launch/07_BUILD_BOOTSTRAP_AUTHORITY.md) §2
**Status:** `Verified — owner approval and linkage recorded 2026-09-15`

| Field | Value |
|---|---|
| **Scope phase** | `v1` — governance bootstrap before Step 0 and all v1 lanes |
| **Owner** | **Sukhdev Singh** |
| **Tier and gate** | None. Governance work; it establishes the external-evidence gate, not a release approval |
| **Personal-data class** | None. Only evidence ownership/status metadata is recorded |
| **Provider or legal dependency** | The register records provider/legal evidence requirements but does not self-approve them |
| **Failure behaviour** | If the register is not effective, external evidence can be misfiled or treated as release proof. Fail closed: keep master release blocked and do not make external claims |
| **Kill switch** | Mark the register superseded and stop all external-evidence status transitions until a replacement is approved and linked |
| **Acceptance test** | Master authority links the register with an effective-status line; every evidence row names Sukhdev Singh as accountable owner; no release gate is promoted by this change |
| **Evidence location** | `active/launch/01_MASTER_RELEASE_AUTHORITY.md`, `active/launch/05_SUPPORT_AND_EXTERNAL_EVIDENCE_REGISTER.md`, `tests/TC-STEP-MINUS-1-external-evidence-register.md`, review record |
| **Rollback** | Revert the linkage/status amendment and restore `Proposed`; retain the review/evidence record as historical governance evidence |

## Scope and decision

The owner approved the existing support and external-evidence register as the effective
operational register. Sukhdev Singh is accountable for every row; specialist reviewers
remain mandatory. This approval does not assert provider, legal, tax, store, staging or
production evidence and does not change the master release block.

## Implementation evidence

The linked authority files were updated in one change, then checked with
`python3 tools/doc_consistency.py`, `python3 tools/traceability.py`, and
`git diff --check`. No runtime, provider, production, secret or personal data was touched.
