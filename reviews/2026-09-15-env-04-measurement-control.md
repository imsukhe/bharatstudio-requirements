# ENV-04 — measurement control review

**Task:** ../active/tasks/ENV-04.md
**Reviewer:** Sukhdev Singh (owner self-review; independent reviewer unavailable)
**Scope:** Pinned OBS/Chromium declarations pass; Windows OBS harness execution is unavailable.
**Finding:** Pinned OBS/Chromium declarations pass; Windows OBS harness execution is unavailable.
**Severity:** P0/P1 external gate
**Evidence:** `node ../bharatstudio-infra/tools/validate-measurement-manifest.mjs --template` validates pinned OBS/Chromium declarations; Windows OBS harness execution is not-run and no external evidence is claimed.
**Disposition:** Blocked — local declaration/validator evidence only; OBS/Chromium Windows harness remains open.
**Owner:** Sukhdev Singh
**Follow-up/release gate:** Run the named Windows OBS/Chromium harness on the approved host and record redacted evidence before release.
**Decision lifecycle:** `Blocked — local declaration/validator evidence only; OBS/Chromium Windows harness remains open`
