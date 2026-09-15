#!/usr/bin/env python3
"""Generate TRACEABILITY.md from the register and the records that exist in this repo.

Six columns per FULL-PRODUCT-DEFINITION.md §35.4:
requirement → task → acceptance record → review → evidence → release gate.

It reports what it can actually find. It asserts nothing it has not looked for.
Run:  python3 tools/traceability.py
"""
from __future__ import annotations
import re, pathlib, collections, datetime, os, argparse

ROOT = pathlib.Path(os.environ.get("BHARATSTUDIO_REQUIREMENTS_ROOT", str(pathlib.Path(__file__).resolve().parent.parent)))
DOC = ROOT / "FULL-PRODUCT-DEFINITION.md"
OUT = ROOT / "TRACEABILITY.md"
MAPPING = pathlib.Path(os.environ.get("BHARATSTUDIO_MAPPING_PATH", str(ROOT / "active" / "traceability" / "register-map.tsv")))
COVERAGE = ROOT / "active" / "traceability" / "coverage-index.tsv"
AUDIT = pathlib.Path(os.environ.get("BHARATSTUDIO_AUDIT_PATH", str(ROOT / "active" / "traceability" / "semantic-mapping-audit.md")))
ARGS = argparse.ArgumentParser(description="Validate or generate BharatStudio traceability")
ARGS.add_argument("--validate-only", action="store_true", help="validate mapping without loading corpora or writing output")
OPTIONS = ARGS.parse_args()

CORPORA = {
    "task": ROOT / "tasks",
    "acceptance": ROOT / "tests",
    "review": ROOT / "reviews",
    # Active-record coverage is task records only; launch authorities and the
    # mapping/audit files are governance, never ten-field implementation records.
    "active": ROOT / "active" / "tasks",
    "evidence": ROOT / "done",
    # the authoritative external evidence register lives here, not in done/
    "external": ROOT / "active" / "launch",
}

ROW = re.compile(r"^\|\s*([A-Z]{2,4}-\d{1,3}[a-z]?)\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|\s*$")
HEAD = re.compile(r"^###\s+(31\.\d+)\s+(.*)$")
LTRACK = re.compile(r"\bL\d{2}\b")

SUITES = {
    "PAY": "PAY-E1..E8 · raid burst · duplicate-webhook and dispatcher-down chaos · isolation",
    "VID": "PAY-E1..E8 · isolation", "ALQ": "PAY-E1..E8 · raid burst",
    "ENG": "OVL-E1..E12 · target concurrency · 8h soak · benchmark",
    "PRF": "OVL-E1..E12 · target concurrency · 8h soak · benchmark",
    "RT": "OVL-E1..E12 · target concurrency · 8h soak · benchmark",
    "WMK": "OVL-E8..E11", "HUB": "HUB-E1..E5 · 3G profile · accessibility",
    "DSH": "DSH-E1..E5 · isolation · role boundaries",
    "ADM": "DSH-E1..E5 · LIF-E4..E6 · isolation", "CTL": "LIF-E4..E6 · isolation",
    "CMP": "CMP-E1..E8 both platforms · localisation · crash-free gate",
    "TTS": "OVL-E6, OVL-E7 · TTS-down chaos · safety corpus on both routes",
    "INT": "INT-E1..E7 · package fuzz corpus",
    "BOT": "BOT-E1..E5 · rate-limit compliance · shared corpus with TTS",
    "LIF": "LIF-E1..E3 · DSH-E4 · durable-record access",
    "PCK": "LIF-E1..E3 · DSH-E4", "STO": "INT-E4 · asset serving · takedown drill",
    "MED": "INT-E4 · asset serving · takedown drill",
    "CUS": "DSH-E1..E5 · role-boundary suite",
    "CST": "OVL-E1..E12 · HUB-E1..E5 · accessibility · +40% expansion",
    "SOC": "none — phase R or blocked", "RTE": "none — phase R or blocked",
    "ENT": "LIF-E1..E3 · isolation", "CON": "post-v1 (Phase 4)",
}


def load(dirpath: pathlib.Path) -> dict[str, str]:
    if not dirpath.is_dir():
        return {}
    return {
        str(p.relative_to(ROOT)): p.read_text(encoding="utf-8", errors="ignore")
        for p in sorted(dirpath.rglob("*.md"))
    }


lines = DOC.read_text(encoding="utf-8").splitlines()
section = "—"
rows: list[dict] = []
for line in lines:
    h = HEAD.match(line)
    if h:
        section = f"§{h.group(1)} {h.group(2)}"
        continue
    m = ROW.match(line)
    if not m or line.startswith("|---"):
        continue
    rid, item, phase, state, pri = m.groups()
    rows.append({
        "id": rid, "item": item, "phase": phase.strip(), "state": state.strip(),
        "pri": pri.strip(), "section": section,
        "ltracks": sorted(set(LTRACK.findall(item))),
    })


def hits(rid: str, corpus: dict[str, str]) -> list[str]:
    pat = re.compile(rf"(?<![A-Za-z0-9-]){re.escape(rid)}(?![0-9])")
    return [name for name, body in corpus.items() if pat.search(body)]


def load_mapping(expected: set[str]) -> dict[str, dict[str, str]]:
    """Strictly validate the Step 0 mapping before generating output."""
    if not MAPPING.exists():
        raise SystemExit(f"mapping validation failed: missing {MAPPING.relative_to(ROOT)}")
    result: dict[str, dict[str, str]] = {}
    documented: dict[str, tuple[str, str, str]] = {}
    if COVERAGE.exists():
        for raw in COVERAGE.read_text(encoding="utf-8").splitlines():
            if raw and not raw.startswith("#"):
                fields = raw.split("\t")
                if len(fields) != 5 or not all(fields):
                    raise SystemExit("mapping validation failed: malformed coverage-index entry")
                if fields[0] in documented:
                    raise SystemExit(f"mapping validation failed: duplicate coverage-index ID {fields[0]}")
                documented[fields[0]] = (fields[2], fields[3], fields[4])
    allowed = {"mapped-existing", "active-record", "new-record-required"}
    for lineno, raw in enumerate(MAPPING.read_text(encoding="utf-8").splitlines(), 1):
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        fields = raw.split("\t")
        if len(fields) != 9:
            raise SystemExit(f"mapping validation failed: line {lineno} has {len(fields)} fields, expected 9")
        rid, phase, state, lifecycle, basis, missing_behavior, task, acceptance, review = fields
        if rid in result:
            raise SystemExit(f"mapping validation failed: duplicate {rid} at line {lineno}")
        if rid not in expected:
            raise SystemExit(f"mapping validation failed: unknown requirement {rid} at line {lineno}")
        if lifecycle not in allowed:
            raise SystemExit(f"mapping validation failed: {rid} has invalid lifecycle {lifecycle!r}")
        if rid in documented and lifecycle != "mapped-existing":
            raise SystemExit(f"mapping validation failed: {rid} is documented in coverage-index but remains new-record-required")
        if not all((phase, state, basis, missing_behavior, task, acceptance, review)):
            raise SystemExit(f"mapping validation failed: {rid} has an empty field at line {lineno}")
        expected_row = next(r for r in rows if r["id"] == rid)
        if phase != expected_row["phase"] or state != expected_row["state"]:
            raise SystemExit(f"mapping validation failed: {rid} phase/state mismatch (mapping {phase}/{state}, register {expected_row['phase']}/{expected_row['state']})")
        if not basis:
            raise SystemExit(f"mapping validation failed: {rid} missing mapping-basis")
        if lifecycle == "new-record-required":
            detail = missing_behavior.split(":", 1)[1].strip() if missing_behavior.startswith("Missing from reviewed ") and ":" in missing_behavior else ""
            if not (basis.startswith("Manual inventory: ") or basis.startswith("Reviewed ")) or not detail or detail.lower().startswith("none-found"):
                raise SystemExit(f"mapping validation failed: {rid} new-record-required requires item-specific unfulfilled behavior")
            if not missing_behavior.startswith("Missing from reviewed ") or not detail or detail.lower().startswith("none-found"):
                raise SystemExit(f"mapping validation failed: {rid} missing item-specific missing_behavior")
            if rid == "RT-12":
                required_negative = ("no reviewed composite index proof", "EXPLAIN ANALYZE", "every widget-backing query", "recheck when changed", "history cursor/order proof")
                missing_negative = [term for term in required_negative if term.lower() not in missing_behavior.lower()]
                if missing_negative:
                    raise SystemExit(f"mapping validation failed: RT-12 missing required negative semantics: {', '.join(missing_negative)}")
            if rid == "PRF-11":
                required_negative = ("no reviewed composite-index inventory", "EXPLAIN ANALYZE", "every widget-backing query", "query-change recheck guard", "PRF-11/RT-12 universal proof")
                missing_negative = [term for term in required_negative if term.lower() not in missing_behavior.lower()]
                if missing_negative:
                    raise SystemExit(f"mapping validation failed: PRF-11 missing required negative semantics: {', '.join(missing_negative)}")
            if any(target != "-" for target in (task, acceptance, review)):
                raise SystemExit(f"mapping validation failed: {rid} new-record-required must have '-' evidence targets")
            result[rid] = {"phase": phase, "state": state, "lifecycle": lifecycle,
                           "basis": basis, "missing_behavior": missing_behavior,
                           "task": task, "acceptance": acceptance, "review": review}
            continue
        for label, target, prefix in (("task", task, "active/tasks/" if lifecycle == "active-record" else "tasks/"), ("acceptance", acceptance, "tests/"), ("review", review, "reviews/")):
            if target == "-":
                raise SystemExit(f"mapping validation failed: {rid} missing lifecycle evidence target")
            if target.startswith("/") or ".." in pathlib.PurePosixPath(target).parts or not target.startswith(prefix):
                raise SystemExit(f"mapping validation failed: {rid} {label} target is unsafe: {target!r}")
            if not (ROOT / target).is_file():
                raise SystemExit(f"mapping validation failed: {rid} {label} target does not exist: {target}")
        if rid in documented and tuple((task, acceptance, review)) != documented[rid]:
            raise SystemExit(f"mapping validation failed: {rid} mapping targets do not match coverage-index")
        if lifecycle == "active-record":
            task_file = ROOT / task
            if task_file.stem != rid:
                raise SystemExit(f"mapping validation failed: {rid} taken task target filename must be {rid}.md")
            task_text = task_file.read_text(encoding="utf-8")
            required = ("Scope phase", "Owner", "Tier and gate", "Personal-data class",
                        "Provider or legal dependency", "Failure behaviour", "Kill switch",
                        "Acceptance test", "Evidence location", "Rollback")
            if any(f"**{field}**" not in task_text for field in required):
                raise SystemExit(f"mapping validation failed: {rid} taken task lacks ten-field metadata")
        if lifecycle == "mapped-existing":
            low_basis = basis.lower()
            if len(basis.strip()) < 20 or "§" not in basis or not any(word in low_basis for word in ("covers", "maps", "evidence")):
                raise SystemExit(f"mapping validation failed: {rid} mapped-existing requires a human evidence basis")
        result[rid] = {"phase": phase, "state": state, "lifecycle": lifecycle,
                       "basis": basis, "missing_behavior": missing_behavior,
                       "task": task, "acceptance": acceptance, "review": review}
    missing = sorted(expected - result.keys())
    if missing:
        raise SystemExit(f"mapping validation failed: missing {len(missing)} IDs: {', '.join(missing)}")
    unknown_coverage = sorted(set(documented) - expected)
    if unknown_coverage:
        raise SystemExit(f"mapping validation failed: coverage-index unknown IDs: {', '.join(unknown_coverage)}")
    return result

def validate_audit(mapping: dict[str, dict[str, str]]) -> None:
    if not AUDIT.exists():
        raise SystemExit(f"audit validation failed: missing {AUDIT}")
    seen = {}
    for raw in AUDIT.read_text(encoding="utf-8").splitlines():
        if not raw.startswith("| ") or raw.startswith("|---") or raw.startswith("| ID "):
            continue
        cells = [x.strip() for x in raw.strip("|").split("|")]
        if len(cells) != 5 or cells[0] not in mapping:
            raise SystemExit("audit validation failed: malformed or unknown audit row")
        rid, _section, lifecycle, detail, targets = cells
        if rid in seen:
            raise SystemExit(f"audit validation failed: duplicate {rid}")
        m = mapping[rid]; expected_detail = m["basis"] if lifecycle == "mapped-existing" else m["missing_behavior"]
        expected_targets = ", ".join(x for x in (m["task"], m["acceptance"], m["review"]) if x != "-") or "-"
        if lifecycle != m["lifecycle"] or detail != expected_detail or targets != expected_targets:
            raise SystemExit(f"audit validation failed: {rid} parity mismatch")
        seen[rid] = True
    missing = sorted(set(mapping) - set(seen))
    if missing:
        raise SystemExit(f"audit validation failed: missing IDs: {', '.join(missing)}")


mapping = load_mapping({r["id"] for r in rows})
validate_audit(mapping)
if OPTIONS.validate_only or os.environ.get("BHARATSTUDIO_TRACEABILITY_VALIDATE_ONLY") == "1":
    print(f"mapping validation: {len(mapping)} IDs passed")
    raise SystemExit(0)

corpora = {name: load(path) for name, path in CORPORA.items()}
counts = {name: len(files) for name, files in corpora.items()}
for r in rows:
    for name, corpus in corpora.items():
        r[name] = hits(r["id"], corpus)

# how many register rows carry an explicit L-track pointer we could map through
with_ltrack = [r for r in rows if r["ltracks"]]
# what the existing corpus is keyed on
ltrack_files = collections.Counter()
for name in corpora["task"]:
    for t in LTRACK.findall(pathlib.Path(name).name):
        ltrack_files[t] += 1

covered = {name: sum(1 for r in rows if r[name]) for name in corpora}
active_record_count = sum(1 for r in mapping.values() if r["lifecycle"] == "active-record")

out: list[str] = [
    "# Traceability index",
    "",
    f"**Generated {datetime.date.today().isoformat()} by `tools/traceability.py`. Do not edit by hand.**",
    "",
    "Six columns per `FULL-PRODUCT-DEFINITION.md` §35.4:",
    "`requirement → task → acceptance record → review → evidence → release gate`.",
    "",
    "This file reports only what the generator can find by searching the repository for",
    "each requirement ID. A blank cell means **no file in that corpus mentions this ID** —",
    "which is not the same as no work existing. See the finding below.",
    "",
    "## What exists in this repository",
    "",
    "| Corpus | Files |",
    "|---|---:|",
    f"| `tasks/` task records | {counts['task']} |",
    f"| `tests/` test records | {counts['acceptance']} |",
    f"| `reviews/` reviews | {counts['review']} |",
    f"| `done/` legacy evidence | {counts['evidence']} |",
    f"| `active/` authority and task records | {counts['active']} |",
    f"| `active/launch/` external evidence register | {counts['external']} |",
    "",
    f"**{len(rows)} requirement rows in the register.**",
    "",
    "## The finding: two ID systems that do not meet",
    "",
    "Substantial prior work exists — task records, test records and reviews — but it is",
    "keyed on the **L-track** system (`L01`…`L32`, plus `WP-`, `FORM-`, `FRD-` work-package",
    "identifiers). The register in §31 is keyed on **area prefixes** (`PAY-`, `CMP-`, `RT-`,",
    "…). Almost nothing references both, so the two bodies of work cannot currently be",
    "joined.",
    "",
    "| Register rows with a … | Count | Of %d |" % len(rows),
    "|---|---:|---:|",
    f"| task record naming the ID | {covered['task']} | {len(rows)} |",
    f"| test record naming the ID | {covered['acceptance']} | {len(rows)} |",
    f"| review naming the ID | {covered['review']} | {len(rows)} |",
    f"| `done/` legacy evidence naming the ID | {covered['evidence']} | {len(rows)} |",
    f"| external evidence register naming the ID | {covered['external']} | {len(rows)} |",
    f"| `active/` corpus file mentioning the ID | {covered['active']} | {len(rows)} |",
    f"| an explicit L-track pointer in its text | {len(with_ltrack)} | {len(rows)} |",
    "",
    "## Step 0 mapping validation",
    "",
    f"`active/traceability/register-map.tsv` structurally enumerates {len(mapping)} unique known §31 IDs.",
    f"Semantic inventory: {sum(1 for x in mapping.values() if x['lifecycle'] == 'mapped-existing')} mapped-existing; {sum(1 for x in mapping.values() if x['lifecycle'] == 'new-record-required')} unresolved new-record-required.",
    "`new-record-required` is not completion evidence; it carries an item-specific missing_behavior and '-' targets until taken.",
    "",
    "**Step 0 semantic mapping is conditionally closed; capability implementation lifecycle remains open.** The map",
    "has %d mapped-existing rows and conservative `new-record-required` targets for every other row."
    % sum(1 for x in mapping.values() if x['lifecycle'] == 'mapped-existing'),
    "Rows marked `new-record-required` receive real ten-field records just in time when a lane",
    "takes them; until then they are not implementation or completion evidence.",
    "",
    "The §31.0 contract still holds independently: a row is schedulable only when its",
    "`active/` record carries all ten fields. That is true of **%d** active-record rows today." % active_record_count,
    "",
    "## Rows",
    "",
    "| ID | Section | Phase | State | Pri | Mapping | Task | Acceptance | Review | Evidence | L-track hint | Required suites (§37.11) | Release gate |",
    "|---|---|:-:|:-:|:-:|---|---|---|---|---|---|---|---|",
]

for r in rows:
    gate = "release" if "·G" in r["phase"] or r["pri"].strip("* ").startswith("P0") or r["pri"].strip("* ") == "P1" else "none"
    evidence = r["evidence"] + r["external"]
    out.append(
        f"| {r['id']} | {r['section']} | {r['phase']} | {r['state']} | {r['pri']} "
        f"| {mapping[r['id']]['lifecycle']} · {mapping[r['id']]['missing_behavior']} → `{mapping[r['id']]['task']}` · `{mapping[r['id']]['acceptance']}` · `{mapping[r['id']]['review']}` "
        f"| {' · '.join(r['task'])} | {' · '.join(r['acceptance'])} | {' · '.join(r['review'])} "
        f"| {' · '.join(evidence)} | {' '.join(r['ltracks'])} "
        f"| {SUITES.get(r['id'].split('-')[0], '—')} | {gate} |"
    )

out += ["", "## Phase distribution", "", "| Phase | Count |", "|---|---:|"]
for ph, n in sorted(collections.Counter(r["phase"] for r in rows).items()):
    out.append(f"| {ph} | {n} |")
out += ["", "## Areas", "", "| Prefix | Rows |", "|---|---:|"]
for pre, n in sorted(collections.Counter(r["id"].split("-")[0] for r in rows).items()):
    out.append(f"| {pre} | {n} |")
out += ["", "## L-tracks with an existing task record", "",
        "These are the records the mapping above should be joined to.", "",
        "| L-track | Task files |", "|---|---:|"]
for t, n in sorted(ltrack_files.items()):
    out.append(f"| {t} | {n} |")
out.append("")

OUT.write_text("\n".join(out), encoding="utf-8")
print(f"wrote {OUT.name}: {len(rows)} rows · task {covered['task']} · acceptance "
      f"{covered['acceptance']} · review {covered['review']} · active {covered['active']}")
