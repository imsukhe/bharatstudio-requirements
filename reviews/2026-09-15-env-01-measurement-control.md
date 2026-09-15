# ENV-01 — measurement control review

**Task:** ../active/tasks/ENV-01.md
**Reviewer:** Sukhdev Singh (owner self-review; independent reviewer unavailable)
**Scope:** Cloud Run-shaped ingress/service/image validator passes; Cloud Run/IAM is not-run.
**Finding:** Cloud Run-shaped ingress/service/image validator passes; Cloud Run/IAM is not-run.
**Severity:** P0/P1 external gate
**Evidence:** `node ../bharatstudio-infra/tools/validate-measurement-manifest.mjs --template` validates the Cloud Run-shaped service/ingress/image controls; Cloud Run/IAM is not-run and no external evidence is claimed.
**Disposition:** Conditionally complete — local evidence.
**Owner:** Sukhdev Singh
**Follow-up/release gate:** Run the Cloud Run/IAM staging deployment with approved identity and record dated redacted evidence before release.
**Decision lifecycle:** `Conditionally complete — local evidence`
