#!/usr/bin/env python3
"""One-off: add a Phase column to every register row in §31.

Phase values follow §1.9: v1 · P2 · P3 · R · N, with the suffix ·G marking a
release-gated row (build now, release waits on named external evidence).

Assignment is rule-based and printed for review — it is not hand-typed per row.
"""
import re, pathlib, collections

DOC = pathlib.Path(__file__).resolve().parent.parent / "FULL-PRODUCT-DEFINITION.md"

PREFIX_PHASE = {
    # v1 surfaces: alerts, payments, overlay, hub, dashboard, Companion, safety, ops
    "PAY": "v1", "VID": "v1", "ALQ": "v1", "ENG": "v1", "CHL": "v1", "WID": "v1",
    "MED": "v1", "HUB": "v1", "TTS": "v1", "CMP": "v1", "SEC": "v1", "MIG": "v1",
    "OPS": "v1", "MKT": "v1", "ENT": "v1", "ADM": "v1", "CTL": "v1", "CUS": "v1",
    "WMK": "v1", "PRF": "v1", "RT": "v1", "SND": "v1", "RUL": "v1", "STO": "v1",
    "LIF": "v1", "AUD": "v1",
    # post-v1
    "CON": "P2", "BOT": "P2", "INT": "P2", "CST": "P2",
    "SOC": "P3", "LOB": "P3", "GIV": "P3", "TRN": "P3", "COS": "P3",
    "PCK": "P3", "JOB": "P3",
    # research only
    "RTE": "R",
}

ROW_OVERRIDE = {
    "INT-17": "R", "INT-18": "R",
    # Enterprise rows live in the entitlements section but are governance-blocked
    **{f"ENT-{n:02d}": "R" for n in range(20, 30)},
}

# a row is release-gated when its text names an external party or filing
GATE = re.compile(
    r"razorpay|provider|partner|counsel|legal|\bCA\b|tax|GST|TDS|DPDP|privacy|terms|"
    r"store|apple|google|app-store|app store|scope approval|verification|evidence|"
    r"quota|declaration|OAuth", re.I)

ROW = re.compile(r"^\|\s*([A-Z]{2,4}-\d{1,3})\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|\s*$")
HDR = re.compile(r"^\|\s*ID\s*\|\s*Item\s*\|\s*State\s*\|\s*Pri\s*\|\s*$")
SEP = re.compile(r"^\|\s*-+\s*\|\s*-+\s*\|\s*-+\s*\|\s*-+\s*\|\s*$")

lines = DOC.read_text(encoding="utf-8").split("\n")
out, stats = [], collections.Counter()

for line in lines:
    if HDR.match(line):
        out.append("| ID | Item | Phase | State | Pri |")
        continue
    if SEP.match(line):
        out.append("|---|---|:-:|:-:|:-:|")
        continue
    m = ROW.match(line)
    if not m:
        out.append(line)
        continue
    rid, item, state, pri = m.groups()
    prefix = rid.split("-")[0]
    state_letter = re.sub(r"[^A-Z]", "", state.upper())[-1:] or ""
    if state_letter == "N":
        phase = "N"
    elif rid in ROW_OVERRIDE:
        phase = ROW_OVERRIDE[rid]
    else:
        phase = PREFIX_PHASE.get(prefix, "P3")
    if phase not in ("R", "N") and GATE.search(item):
        phase += "·G"
    stats[phase] += 1
    out.append(f"| {rid} | {item} | {phase} | {state} | {pri} |")

DOC.write_text("\n".join(out), encoding="utf-8")
print("phase distribution:", dict(sorted(stats.items())))
