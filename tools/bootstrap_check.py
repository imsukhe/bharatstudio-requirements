#!/usr/bin/env python3
"""Deterministic checks for the governance bootstrap records.

This is a documentation/governance check only. It never contacts providers,
creates infrastructure, reads secrets, or changes runtime state.
"""
from __future__ import annotations

import pathlib
import re
import sys
import subprocess
import os


ROOT = pathlib.Path(__file__).resolve().parent.parent


def require(path: pathlib.Path, pattern: str, label: str) -> None:
    text = path.read_text(encoding="utf-8")
    if not re.search(pattern, text, flags=re.MULTILINE | re.IGNORECASE):
        raise AssertionError(f"{label}: missing {pattern!r} in {path.relative_to(ROOT)}")


def main() -> int:
    authority = ROOT / "active" / "launch" / "07_BUILD_BOOTSTRAP_AUTHORITY.md"
    master = ROOT / "active" / "launch" / "01_MASTER_RELEASE_AUTHORITY.md"
    register = ROOT / "active" / "launch" / "05_SUPPORT_AND_EXTERNAL_EVIDENCE_REGISTER.md"
    step0 = ROOT / "active" / "tasks" / "STEP-0-register-mapping.md"
    stepm1 = ROOT / "active" / "tasks" / "STEP-MINUS-1-external-evidence-register.md"
    step025 = ROOT / "active" / "tasks" / "STEP-0.25-measurement-environment.md"
    tc_0 = ROOT / "tests" / "TC-STEP-0-register-mapping.md"
    tc_m1 = ROOT / "tests" / "TC-STEP-MINUS-1-external-evidence-register.md"
    tc_025 = ROOT / "tests" / "TC-STEP-0.25-measurement-environment.md"
    rv_m1 = ROOT / "reviews" / "2026-09-15-step-minus-1-register-approval.md"
    rv_025 = ROOT / "reviews" / "2026-09-15-step-0.25-measurement-environment.md"
    rv_0 = ROOT / "reviews" / "2026-09-15-step-0-register-mapping.md"
    mapping = pathlib.Path(os.environ.get("BHARATSTUDIO_MAPPING_PATH", ROOT / "active" / "traceability" / "register-map.tsv"))
    coverage = pathlib.Path(os.environ.get("BHARATSTUDIO_COVERAGE_PATH", ROOT / "active" / "traceability" / "coverage-index.tsv"))

    require(authority, r"\*\*Status:\*\* `Approved", "bootstrap authority")
    require(authority, r"\*\*Owner:\*\* Sukhdev Singh", "bootstrap authority owner")
    require(authority, r"Owner:\*\* Sukhdev Singh", "environment owner")
    require(master, r"05_SUPPORT_AND_EXTERNAL_EVIDENCE_REGISTER\.md", "master register link")
    require(master, r"effective operational evidence authority", "master adoption status")
    require(register, r"\*\*Status:\*\* `Effective operational evidence authority", "register status")

    for path in (step0, stepm1, step025):
        text = path.read_text(encoding="utf-8")
        for field in ("Scope phase", "Owner", "Tier and gate", "Personal-data class",
                      "Provider or legal dependency", "Failure behaviour", "Kill switch",
                      "Acceptance test", "Evidence location", "Rollback"):
            if f"**{field}**" not in text:
                raise AssertionError(f"{path.name}: missing ten-field metadata {field}")
        require(path, r"\*\*Owner\*\*\s*\|\s*\*{0,2}Sukhdev Singh", path.name + " owner")

    for path in (tc_0, tc_m1, tc_025, rv_0, rv_m1, rv_025):
        if not path.exists():
            raise AssertionError(f"missing bootstrap evidence record: {path.relative_to(ROOT)}")

    # Evidence-register table rows (after the header) must name the accountable owner.
    rows = []
    in_table = False
    for line in register.read_text(encoding="utf-8").splitlines():
        if line.startswith("| Evidence area |"):
            in_table = True
            continue
        if in_table and line.startswith("|---"):
            continue
        if in_table and line.startswith("|"):
            rows.append(line)
        elif in_table and line and not line.startswith("|"):
            break
    if len(rows) != 9:
        raise AssertionError(f"expected 9 external-evidence rows, found {len(rows)}")
    if any("Sukhdev Singh" not in row for row in rows):
        raise AssertionError("every external-evidence row must name Sukhdev Singh")

    # Step 0 mapping is structural and fail-closed: every §31 ID occurs once,
    # with nine fields and safe conservative targets.  Target files need not
    # exist until the row is actually taken.
    expected = set()
    for line in (ROOT / "FULL-PRODUCT-DEFINITION.md").read_text(encoding="utf-8").splitlines():
        m = re.match(r"^\|\s*([A-Z]{2,4}-\d{1,3}[a-z]?)\s*\|", line)
        if m:
            expected.add(m.group(1))
    if not mapping.exists():
        raise AssertionError("missing active/traceability/register-map.tsv")
    seen = {}
    documented = {line.split("\t", 1)[0] for line in coverage.read_text(encoding="utf-8").splitlines() if line and not line.startswith("#")}
    for lineno, raw in enumerate(mapping.read_text(encoding="utf-8").splitlines(), 1):
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        fields = raw.split("\t")
        if len(fields) != 9:
            raise AssertionError(f"mapping line {lineno}: expected 9 tab-separated fields")
        rid, phase, state, lifecycle, basis, missing_behavior, task, acceptance, review = fields
        if rid in seen:
            raise AssertionError(f"mapping duplicate: {rid}")
        if rid not in expected:
            raise AssertionError(f"mapping unknown ID: {rid}")
        if lifecycle not in {"mapped-existing", "active-record", "new-record-required"}:
            raise AssertionError(f"mapping {rid}: invalid lifecycle {lifecycle}")
        if rid in documented and lifecycle == "new-record-required":
            raise AssertionError(f"mapping {rid}: documented in coverage-index but downgraded")
        if not all((phase, state, basis, missing_behavior, task, acceptance, review)):
            raise AssertionError(f"mapping {rid}: empty field")
        if lifecycle == "mapped-existing" and (len(basis.strip()) < 20 or "§" not in basis or not any(word in basis.lower() for word in ("covers", "maps", "evidence"))):
            raise AssertionError(f"mapping {rid}: mapped-existing requires a human evidence basis")
        register_line = next(line for line in (ROOT / "FULL-PRODUCT-DEFINITION.md").read_text(encoding="utf-8").splitlines() if re.match(rf"^\|\s*{re.escape(rid)}\s*\|", line))
        cells = [c.strip() for c in register_line.strip().strip("|").split("|")]
        if phase != cells[2] or state != cells[3]:
            raise AssertionError(f"mapping {rid}: phase/state mismatch")
        for target, prefix in ((task, "active/tasks/" if lifecycle == "active-record" else "tasks/"), (acceptance, "tests/"), (review, "reviews/")):
            if target == "-":
                if lifecycle != "new-record-required":
                    raise AssertionError(f"mapping {rid}: missing lifecycle evidence target")
                continue
            if target.startswith("/") or ".." in pathlib.PurePosixPath(target).parts or not target.startswith(prefix):
                raise AssertionError(f"mapping {rid}: unsafe target {target}")
            if not (ROOT / target).is_file():
                raise AssertionError(f"mapping {rid}: target does not exist: {target}")
        if lifecycle == "new-record-required" and any(x != "-" for x in (task, acceptance, review)):
            raise AssertionError(f"mapping {rid}: new-record-required must have '-' evidence targets")
        detail = missing_behavior.split(":", 1)[1].strip() if missing_behavior.startswith("Missing from reviewed ") and ":" in missing_behavior else ""
        if lifecycle == "new-record-required" and (not (basis.startswith("Manual inventory: ") or basis.startswith("Reviewed ")) or not missing_behavior.startswith("Missing from reviewed ") or not detail or detail.lower().startswith("none-found")):
            raise AssertionError(f"mapping {rid}: item-specific unfulfilled behavior is required")
        seen[rid] = lifecycle
    if seen.keys() != expected:
        raise AssertionError(f"mapping coverage mismatch: missing={sorted(expected-seen.keys())} unknown={sorted(seen-expected)}")

    # Any row claimed as taken must point to a real ten-field task record.
    fields_required = ("Scope phase", "Owner", "Tier and gate", "Personal-data class",
                       "Provider or legal dependency", "Failure behaviour", "Kill switch",
                       "Acceptance test", "Evidence location", "Rollback")
    active_count = 0
    for raw in mapping.read_text(encoding="utf-8").splitlines():
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        parts = raw.split("\t")
        if len(parts) != 9 or parts[3] != "active-record":
            continue
        active_count += 1
        task_path = ROOT / parts[6]
        if (task_path.stem != parts[0] or not task_path.is_file() or
                not all(f"**{f}**" in task_path.read_text(encoding="utf-8") for f in fields_required)):
            raise AssertionError(f"taken mapping row {parts[0]} lacks a complete ten-field task record")
    if active_count > 0 and active_count == len(seen):
        raise AssertionError("all-rows-active policy is invalid; new-record-required rows are JIT")

    print("bootstrap checks: 9 passed; owner=Sukhdev Singh; register=effective; release=blocked")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (AssertionError, OSError) as exc:
        print(f"bootstrap checks: FAIL: {exc}", file=sys.stderr)
        raise SystemExit(1)
