# TC-STEP-MINUS-1 — External-evidence register bootstrap

**Task:** [`../active/tasks/STEP-MINUS-1-external-evidence-register.md`](../active/tasks/STEP-MINUS-1-external-evidence-register.md)
**Status:** `Passed locally — governance/document evidence only`
**Owner:** Sukhdev Singh

| ID | Setup/action | Expected result | Failure/retry and evidence | Cleanup/rollback |
|---|---|---|---|---|
| STEP-−1-01 | Read the bootstrap authority and register. | Register scope, non-approval boundary and release gate are understood. | Any contradiction blocks closure; record the exact file/line. | Restore Proposed status and unlink from master. |
| STEP-−1-02 | Inspect master authority linkage. | Master links `05_SUPPORT_AND_EXTERNAL_EVIDENCE_REGISTER.md` and states effective date/owner. | Missing link or owner fails; fix authority before continuing. | Revert linkage amendment. |
| STEP-−1-03 | Inspect every register evidence row. | Each row has Sukhdev Singh as accountable owner plus required specialist reviewer. | Any role-only owner fails; update the row before closure. | Revert owner assignment only with a superseding decision. |
| STEP-−1-04 | Run `python3 tools/doc_consistency.py`, `python3 tools/traceability.py`, `git diff --check`. | All checks pass and traceability is regenerated without stale diff. | Non-zero output is a blocker; rerun after correction. | No runtime state to clean. |

**Evidence boundary:** this record proves governance linkage only. It is not provider,
legal, tax, store, staging, deployment or production evidence.
