#!/usr/bin/env python3
"""Generate TRACEABILITY.md from the register in FULL-PRODUCT-DEFINITION.md.

Six columns per §35.4: requirement → task → acceptance record → review → evidence →
release gate. Generated, never hand-maintained. Gaps are shown as gaps.
Run:  python3 tools/traceability.py
"""
from __future__ import annotations
import re, pathlib, collections, datetime

ROOT = pathlib.Path(__file__).resolve().parent.parent
DOC = ROOT / "FULL-PRODUCT-DEFINITION.md"
OUT = ROOT / "TRACEABILITY.md"
TASK_DIR = ROOT / "tasks"
ACTIVE = ROOT / "active"

lines = DOC.read_text(encoding="utf-8").splitlines()
ROW = re.compile(r"^\|\s*([A-Z]{2,4}-\d{1,3})\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|\s*$")
HEAD = re.compile(r"^###\s+(31\.\d+)\s+(.*)$")

# §37.11 prefix → required suites
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
    "CUS": "DSH-E1..E5 · accessibility", "CST": "OVL-E1..E12 · HUB-E1..E5 · accessibility · +40% expansion",
    "SOC": "none — phase R or blocked", "RTE": "none — phase R or blocked",
    "ENT": "LIF-E1..E3 · isolation", "CON": "post-v1 (Phase 4)", "F": "per §3",
}

task_text = {p.name: p.read_text(encoding="utf-8") for p in sorted(TASK_DIR.glob("*.md"))} if TASK_DIR.is_dir() else {}
active_text = {p.name: p.read_text(encoding="utf-8") for p in sorted(ACTIVE.rglob("*.md"))} if ACTIVE.is_dir() else {}

section = "—"
rows: list[tuple[str, str, str, str, str]] = []
for line in lines:
    h = HEAD.match(line)
    if h:
        section = f"§{h.group(1)} {h.group(2)}"
        continue
    m = ROW.match(line)
    if not m or line.startswith("|---"):
        continue
    rid, item, state, pri = m.groups()
    if rid.split("-")[0] in {"C"}:
        continue
    rows.append((rid, item, state.strip(), pri.strip(), section))

by_prefix: dict[str, int] = collections.Counter(r[0].split("-")[0] for r in rows)

def find(rid: str, corpus: dict[str, str]) -> str:
    hits = [name for name, t in corpus.items() if rid in t]
    return " · ".join(hits) if hits else ""

out = [
    "# Traceability index",
    "",
    f"**Generated {datetime.date.today().isoformat()} by `tools/traceability.py`. Do not edit by hand.**",
    "",
    "Six columns per `FULL-PRODUCT-DEFINITION.md` §35.4:",
    "`requirement → task → acceptance record → review → evidence → release gate`.",
    "",
    "A blank cell is a real gap, not an omission. Per §37.2 a row with a gap in any",
    "column is not done, whatever its state letter says.",
    "",
    f"**{len(rows)} requirement rows across {len(by_prefix)} areas.**",
    "",
    "## Coverage summary",
    "",
    "| Column | Populated | Missing |",
    "|---|---:|---:|",
]

tasks_found = [r for r in rows if find(r[0], task_text) or find(r[0], active_text)]
out += [
    f"| Task file in `tasks/` or `active/` | {len(tasks_found)} | {len(rows) - len(tasks_found)} |",
    f"| Acceptance record (§37.3 scenarios) | 0 | {len(rows)} |",
    "| Review (who traced the user path) | 0 | %d |" % len(rows),
    "| Evidence artefact (§37.8) | 0 | %d |" % len(rows),
    "",
    "Acceptance, review and evidence are uniformly empty because **no build work has",
    "started**. The §37.11 suite column below states what each row will need; it is a",
    "requirement, not a claim that anything has been run.",
    "",
    "## Rows",
    "",
    "| ID | Section | State | Pri | Task file | Required suites (§37.11) | Acceptance | Review | Evidence | Release gate |",
    "|---|---|:-:|:-:|---|---|---|---|---|---|",
]

for rid, item, state, pri, section in rows:
    prefix = rid.split("-")[0]
    task = find(rid, task_text) or find(rid, active_text)
    suites = SUITES.get(prefix, "—")
    gate = "release" if pri.strip("* ") in {"P0", "P1"} else "none"
    out.append(f"| {rid} | {section} | {state} | {pri} | {task} | {suites} |  |  |  | {gate} |")

out += ["", "## Areas", "", "| Prefix | Rows |", "|---|---:|"]
for pre, n in sorted(by_prefix.items()):
    out.append(f"| {pre} | {n} |")
out.append("")

OUT.write_text("\n".join(out), encoding="utf-8")
print(f"wrote {OUT.name}: {len(rows)} rows, {len(tasks_found)} with a task file")
