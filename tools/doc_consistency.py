#!/usr/bin/env python3
"""Consistency checks for FULL-PRODUCT-DEFINITION.md and the active launch authorities.

Implements the checks §35.3 requires. Exit code 1 on any ERROR; WARNs do not fail.
Run:  python3 tools/doc_consistency.py
"""
from __future__ import annotations
import re, sys, pathlib, collections

ROOT = pathlib.Path(__file__).resolve().parent.parent
DOC = ROOT / "FULL-PRODUCT-DEFINITION.md"
AUTH = sorted((ROOT / "active" / "launch").glob("*.md"))
TASKS = sorted((ROOT / "tasks").glob("*.md")) if (ROOT / "tasks").is_dir() else []

errors: list[str] = []
warns: list[str] = []


def err(check: str, msg: str) -> None:
    errors.append(f"ERROR [{check}] {msg}")


def warn(check: str, msg: str) -> None:
    warns.append(f"WARN  [{check}] {msg}")


text = DOC.read_text(encoding="utf-8")
lines = text.splitlines()

ROW_ID = re.compile(r"^\|\s*([A-Z]{2,4}-\d{1,3}[a-z]?)\s*\|")
PHASES = {"v1", "v1\u00b7G", "P2", "P2\u00b7G", "P3", "P3\u00b7G", "R", "N"}
HEADING = re.compile(r"^(#{2,4})\s+(\d+(?:\.\d+){0,3})[.\s]")


# 1 ── duplicate requirement IDs -------------------------------------------------
def check_duplicate_ids() -> None:
    seen: dict[str, list[int]] = collections.defaultdict(list)
    for n, line in enumerate(lines, 1):
        m = ROW_ID.match(line)
        if m:
            seen[m.group(1)].append(n)
    for rid, where in sorted(seen.items()):
        if len(where) > 1:
            err("duplicate-id", f"{rid} defined {len(where)} times at lines {where}")


# 2 ── duplicate section numbers -------------------------------------------------
def check_duplicate_sections() -> None:
    seen: dict[str, list[int]] = collections.defaultdict(list)
    for n, line in enumerate(lines, 1):
        m = HEADING.match(line)
        if m:
            seen[m.group(2)].append(n)
    for num, where in sorted(seen.items()):
        if len(where) > 1:
            err("duplicate-section", f"§{num} used {len(where)} times at lines {where}")


# 3 ── cross-reference validity --------------------------------------------------
def check_cross_refs() -> None:
    defined = set()
    for line in lines:
        m = HEADING.match(line)
        if m:
            defined.add(m.group(2))
    # a reference to §12.6 is satisfied by a heading 12.6 or by 12 existing with subsections
    for n, line in enumerate(lines, 1):
        for ref in re.findall(r"§(\d+(?:\.\d+){0,3})", line):
            if ref in defined:
                continue
            # allow a reference to a parent section that exists
            if any(d == ref or d.startswith(ref + ".") for d in defined):
                continue
            err("bad-xref", f"line {n} references §{ref}, which is not a heading")


# 4 ── register rows must carry a state letter and a priority --------------------
STATES = {"U", "X", "P", "A", "B", "N"}


def check_register_rows() -> None:
    for n, line in enumerate(lines, 1):
        if not ROW_ID.match(line):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) != 5:
            err("row-shape", f"line {n}: {cells[0]} has {len(cells)} cells, expected 5 (ID, Item, Phase, State, Pri)")
            continue
        rid, _item, phase, state_cell, pri = cells
        if phase not in PHASES:
            err("row-phase", f"line {n}: {rid} phase '{phase}' not in {sorted(PHASES)}")
        state = re.sub(r"[^A-Z]", "", state_cell.upper())
        state = state[-1:] if state else ""
        if state not in STATES:
            err("row-state", f"line {n}: {rid} state '{state_cell}' not in {sorted(STATES)}")
        if not pri:
            err("row-priority", f"line {n}: {rid} has an empty priority cell")


# ── phase-label integrity: an R or N row may not be scheduled in the build order ──
def check_phase_integrity() -> None:
    phase_of: dict[str, str] = {}
    for line in lines:
        if not ROW_ID.match(line):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) == 5:
            phase_of[cells[0]] = cells[2]
    try:
        start = next(i for i, l in enumerate(lines) if l.startswith("## 34. Build order"))
    except StopIteration:
        return
    end = next((i for i in range(start + 1, len(lines)) if l_starts_section(lines[i])), len(lines))
    # exclude the paragraphs that exist precisely to name unscheduled work
    kept, skip = [], False
    for l in lines[start:end]:
        if l.startswith("**Research-only track") or l.startswith("**Blocked track"):
            skip = True
        elif skip and not l.strip():
            skip = False
        if not skip:
            kept.append(l)
    body = "\n".join(kept)
    for rid, phase in phase_of.items():
        if phase in ("R", "N") and re.search(rf"(?<![A-Za-z0-9-]){re.escape(rid)}(?![0-9])", body):
            err("phase-integrity", f"§34 build order schedules {rid}, which is phase {phase}")


def l_starts_section(line: str) -> bool:
    return line.startswith("## ")


# ── every markdown table has a consistent column count ───────────────────────────
def check_table_shape() -> None:
    table: list[tuple[int, int]] = []

    def flush() -> None:
        if len(table) > 2:
            widths = {w for _, w in table}
            if len(widths) > 1:
                counts: dict[int, int] = {}
                for _, w in table:
                    counts[w] = counts.get(w, 0) + 1
                majority = max(counts, key=lambda k: counts[k])
                for ln, w in table:
                    if w != majority:
                        err("table-shape", f"line {ln}: row has {w} cells, table uses {majority}")
        table.clear()

    for n, line in enumerate(lines, 1):
        if line.startswith("|"):
            table.append((n, len([c for c in line.strip().strip("|").split("|")])))
        else:
            flush()
    flush()


# 5 ── ordered-list gaps (decision log completeness) -----------------------------
def check_list_gaps() -> None:
    run: list[tuple[int, int]] = []

    def flush() -> None:
        if len(run) > 1:
            nums = [k for k, _ in run]
            expect = list(range(nums[0], nums[0] + len(nums)))
            if nums != expect:
                err("list-gap", f"ordered list near line {run[0][1]} numbers {nums}, expected {expect}")
        run.clear()

    for n, line in enumerate(lines, 1):
        m = re.match(r"^(\d+)\.\s", line)
        if m:
            run.append((int(m.group(1)), n))
        elif line.strip() == "" or line.startswith(("   ", "\t", "    ")):
            continue
        else:
            flush()
    flush()


# 6 ── curated superseded-decision rules -----------------------------------------
# Each rule: a decision key, the phrase that must NOT appear as a live instruction,
# and phrases that mark a legitimate mention (a correction log or a prohibition).
SUPERSEDED = [
    ("amazon-pay", r"build under C1[–-]C7", ["never", "rejected", "corrected", "wrong", "previously"]),
    ("pack-launch", r"[Ff]our visible at first", ["corrected", "previously", "rejected", "no fixed"]),
    ("queue-ladder", r"1\s*/\s*3\s*/\s*5\s*/\s*10", ["supersed", "corrected", "previously", "not the approved"]),
    ("deletion", r"[Dd]eletion is archival, never destructive\s*—\s*decided", []),
    ("branding", r"[Zz]ero branding on every paid tier, everywhere", ["corrected", "previously"]),
    ("marketing-357", r"₹357", ["never", "rejected", "double-count", "corrected"]),
    ("raid-guarantee", r"raid-night guarantee", ["not usable", "never", "rejected"]),
]


def check_superseded() -> None:
    for name, pattern, allow in SUPERSEDED:
        for n, line in enumerate(lines, 1):
            if re.search(pattern, line):
                low = line.lower()
                if any(a in low for a in allow):
                    continue
                err("stale-decision", f"line {n}: '{name}' appears as a live statement — {line.strip()[:110]}")


# 7 ── authority conflict on values the authorities also carry -------------------
def check_authority_values() -> None:
    for path in AUTH:
        atext = path.read_text(encoding="utf-8")
        alines = atext.splitlines()
        for n, line in enumerate(alines, 1):
            if re.search(r"1\s*/\s*3\s*/\s*5\s*/\s*10", line):
                window = "\n".join(alines[max(0, n - 16): n]).lower()
                if "supersed" not in window:
                    err("authority-conflict", f"{path.name}:{n} carries the 1/3/5/10 ladder with no superseded marker within 15 lines")
        for n, line in enumerate(alines, 1):
            if re.match(r"^\|\s*Pro\s*\|\s*3\s*\|", line):
                window = "\n".join(alines[max(0, n - 20): n]).lower()
                if "supersed" not in window:
                    err("authority-conflict", f"{path.name}:{n} carries a queueCount table row 'Pro | 3' with no superseded marker")
        if re.search(r"store uploaded Lottie animations as `bytea`", atext):
            # must be marked superseded within the preceding 12 lines
            alines = atext.splitlines()
            idx = next(i for i, l in enumerate(alines) if "store uploaded Lottie animations as `bytea`" in l)
            window = "\n".join(alines[max(0, idx - 12): idx + 1]).lower()
            if "supersed" not in window:
                err("authority-conflict", f"{path.name}: the bytea decision is not marked superseded")


# 8 ── post-v1 references inside v1 sections -------------------------------------
POST_V1_TERMS = ["YouTube ingestion", "Enterprise workspace", "compatibility routing", "marketplace publishing"]


def check_v1_sections() -> None:
    in_phase0 = False
    for n, line in enumerate(lines, 1):
        if line.startswith("**Phase 0"):
            in_phase0 = True
        elif line.startswith("**Phase ") and not line.startswith("**Phase 0"):
            in_phase0 = False
        if in_phase0:
            for term in POST_V1_TERMS:
                if term.lower() in line.lower():
                    err("v1-scope-drift", f"line {n}: Phase 0 text references post-v1 '{term}'")


# 9 ── orphan corrections ---------------------------------------------------------
def check_orphan_corrections() -> None:
    inline = sum(1 for l in lines if re.search(r"[Cc]orrected 20\d\d-\d\d-\d\d", l))
    try:
        start = next(i for i, l in enumerate(lines) if l.startswith("### 35.2 Corrections applied"))
    except StopIteration:
        err("orphan-correction", "§35.2 corrections table is missing")
        return
    end = next((i for i in range(start + 1, len(lines)) if lines[i].startswith("### ")), len(lines))
    logged = sum(1 for l in lines[start:end] if l.startswith("| ") and not l.startswith("|---"))
    if inline > logged + 12:
        warn("orphan-correction", f"{inline} inline 'Corrected' markers vs {logged} rows in §35.2 — check for unlogged corrections")


# 10 ── prose must not restate generated counts -----------------------------------
def check_restated_counts() -> None:
    # a bare count near the words requirement / register / rows, ignoring years,
    # ISO dates and migration numbers
    NUM = r"(?<![-\d])(?!19\d\d|20\d\d)\d{3,4}(?![-\d])"
    near = re.compile(
        rf"({NUM}[^.|]{{0,45}}?(?:requirement|register|rows\b)"
        rf"|(?:requirement|register|\brows\b)[^.|]{{0,45}}?{NUM})", re.I)
    for n, line in enumerate(lines, 1):
        if near.search(line):
            err("restated-count", f"line {n}: a register row count is hard-coded in prose — cite TRACEABILITY.md instead")


CHECKS = [
    check_duplicate_ids, check_duplicate_sections, check_cross_refs,
    check_register_rows, check_list_gaps, check_superseded,
    check_authority_values, check_v1_sections, check_orphan_corrections,
    check_restated_counts, check_phase_integrity, check_table_shape,
]

for fn in CHECKS:
    fn()

for line in warns:
    print(line)
for line in errors:
    print(line)
print(f"\n{len(CHECKS)} checks run · {len(errors)} errors · {len(warns)} warnings")
sys.exit(1 if errors else 0)
