# ENV-05 — measurement control review

**Task:** ../active/tasks/ENV-05.md
**Reviewer:** Sukhdev Singh (owner self-review; independent reviewer unavailable)
**Scope:** Android/iPhone floor declarations exist; named device lab execution is unavailable.
**Finding:** Android/iPhone floor declarations exist; named device lab execution is unavailable.
**Severity:** P0/P1 external gate
**Evidence:** `node ../bharatstudio-infra/tools/validate-measurement-manifest.mjs --template` validates Android/iPhone floor declarations; the named device lab is not-run and no external evidence is claimed.
**Disposition:** Blocked — local declaration/validator evidence only; named device lab remains open.
**Owner:** Sukhdev Singh
**Follow-up/release gate:** Run the approved Android/iPhone device matrix and record dated redacted evidence before release.
**Decision lifecycle:** `Blocked — local declaration/validator evidence only; named device lab remains open`
