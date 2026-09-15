# TC-STEP-0 — Register mapping and fail-closed metadata validation

**Task:** [`../active/tasks/STEP-0-register-mapping.md`](../active/tasks/STEP-0-register-mapping.md)
**Status:** `Conditionally complete — semantic mapping/JIT validator checks pass; capability lifecycle records remain open`
**Owner:** Sukhdev Singh

| ID | Setup/action | Expected result | Failure/retry and evidence | Cleanup/rollback |
|---|---|---|---|---|
| MAP-01 | Run `python3 tools/bootstrap_check.py`. | Owner, effective register, bootstrap records and exact mapping coverage pass. | Non-zero output blocks Step 0; retain redacted output and fix the named record. | No runtime state. |
| MAP-02 | Run `python3 tools/traceability.py --validate-only`, then run `python3 tools/traceability.py` twice. | Validation emits no files; generation is byte-identical on consecutive runs and every §31 ID is emitted once with lifecycle and conservative targets. | Duplicate, unknown, missing or stale output fails closed; regenerate after correction. | Generated `TRACEABILITY.md` is reproducible. |
| MAP-03 | Run `python3 tools/test_mapping_validation.py`. | Duplicate, unknown, missing, unsafe-target, lifecycle, phase/state, missing-evidence, false-completion, missing mapped-existing triad, weak evidence basis, generic missing behavior, documented-coverage downgrade and Markdown audit parity/duplicate/missing-ID mutations are rejected by the real CLI validator. | Any mutation that passes is a P0 governance finding; fix validator before closure. | TSV and Markdown fixtures are disposable temporary files; `--validate-only` performs no repository writes and the repository audit remains unchanged. |
| MAP-04 | Run `python3 tools/doc_consistency.py`, `python3 -m py_compile tools/*.py`, `git diff --check`, and stale TRACEABILITY check. | Documentation, Python syntax and generated output are clean. | Any failure blocks closure; rerun after correction. | None. |

**Evidence boundary:** This proves document/traceability integrity only. It is not
provider, staging, legal, store, deployment, production or independent-review evidence.

## Recorded local run (2026-09-15)

From the requirements repository:

```text
python3 tools/traceability.py --validate-only
mapping validation: 783 IDs passed
python3 tools/bootstrap_check.py
bootstrap checks: 9 passed; owner=Sukhdev Singh; register=effective; release=blocked
python3 tools/test_mapping_validation.py
mapping hostile tests: 106 passed
mapping source regressions: 20 passed
mapping unresolved regressions: 30 passed
audit hostile tests: 3 passed
JIT lifecycle checks: mixed mapped-existing/new-record-required set accepted; active-record safety covered by hostile mutations
JIT active-record fixture checks: 3 passed (valid nine-field row, missing ten-field label, unsafe/non-ID target)
JIT all-active/doc-root hostile checks: 2 passed (isolated doc-root mutation adds a blanket all-row active-record policy while retaining JIT wording; doc_consistency rejects it with jit-policy)
Step 0 master-count hostile check: isolated doc-root mutation adds `66 mapped-existing` / `717 new-record-required`; doc_consistency rejects it with step0-master-counts.
python3 tools/doc_consistency.py
16 checks run · 0 errors · 0 warnings
PYTHONPYCACHEPREFIX=/tmp/bsa-step0-pycache python3 -m py_compile tools/*.py
git diff --check
traceability generated twice; cmp: PASS
```

Reconciliation is `66 mapped-existing + 717 new-record-required = 783`; active-record
eligibility is `0`. The exact redacted outputs above are reproducible; no generated
`__pycache__` remains in the repository.
