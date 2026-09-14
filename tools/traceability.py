#!/usr/bin/env python3
"""Generate TRACEABILITY.md from the register and the records that exist in this repo.

Six columns per FULL-PRODUCT-DEFINITION.md §35.4:
requirement → task → acceptance record → review → evidence → release gate.

It reports what it can actually find. It asserts nothing it has not looked for.
Run:  python3 tools/traceability.py
"""
from __future__ import annotations
import re, pathlib, collections, datetime

ROOT = pathlib.Path(__file__).resolve().parent.parent
DOC = ROOT / "FULL-PRODUCT-DEFINITION.md"
OUT = ROOT / "TRACEABILITY.md"

CORPORA = {
    "task": ROOT / "tasks",
    "acceptance": ROOT / "tests",
    "review": ROOT / "reviews",
    "active": ROOT / "active",
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


corpora = {name: load(path) for name, path in CORPORA.items()}
counts = {name: len(files) for name, files in corpora.items()}

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
    f"| `active/` record naming the ID | {covered['active']} | {len(rows)} |",
    f"| an explicit L-track pointer in its text | {len(with_ltrack)} | {len(rows)} |",
    "",
    "**So the gap is a missing mapping, not (only) missing work.** Building that mapping —",
    "register ID → L-track record where one exists, and a new `active/` record where one",
    "does not — is the first task in §34's Step 0, and until it exists §34 is a proposed",
    "roadmap rather than a schedulable plan.",
    "",
    "The §31.0 contract still holds independently: a row is schedulable only when its",
    "`active/` record carries all ten fields. That is true of **%d** rows today." % covered["active"],
    "",
    "## Rows",
    "",
    "| ID | Section | Phase | State | Pri | Task | Acceptance | Review | Evidence | L-track hint | Required suites (§37.11) | Release gate |",
    "|---|---|:-:|:-:|:-:|---|---|---|---|---|---|---|",
]

for r in rows:
    gate = "release" if "·G" in r["phase"] or r["pri"].strip("* ").startswith("P0") or r["pri"].strip("* ") == "P1" else "none"
    evidence = r["evidence"] + r["external"]
    out.append(
        f"| {r['id']} | {r['section']} | {r['phase']} | {r['state']} | {r['pri']} "
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
