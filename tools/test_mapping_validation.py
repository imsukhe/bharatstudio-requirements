#!/usr/bin/env python3
"""Hostile deterministic tests for the Step 0 mapping parser."""
from __future__ import annotations
import inspect
import re
import os, pathlib, subprocess, tempfile, shutil
from concurrent.futures import ThreadPoolExecutor

ROOT = pathlib.Path(__file__).resolve().parent.parent
MAP = ROOT / "active/traceability/register-map.tsv"
CHECK = ROOT / "tools/traceability.py"
AUDIT = ROOT / "active/traceability/semantic-mapping-audit.md"

def data(lines):
    return [i for i, line in enumerate(lines) if line and not line.startswith("#")]

def run(mutator):
    with tempfile.NamedTemporaryFile(prefix="bharatstudio-map-", suffix=".tsv", mode="w", delete=False) as f:
        path = pathlib.Path(f.name)
    try:
        lines = MAP.read_text(encoding="utf-8").splitlines()
        mutated = mutator(lines)
        if mutated == lines:
            raise SystemExit(
                "hostile fixture mutated nothing -- its target row or phrase has changed "
                "in the register, so it no longer tests the rule it names")
        path.write_text("\n".join(mutated) + "\n", encoding="utf-8")
        env = os.environ.copy()
        env["BHARATSTUDIO_MAPPING_PATH"] = str(path)
        env["BHARATSTUDIO_TRACEABILITY_VALIDATE_ONLY"] = "1"
        p = subprocess.run(["python3", str(CHECK)], cwd=ROOT, env=env, text=True, capture_output=True)
        return p.returncode, p.stdout + p.stderr
    finally:
        path.unlink(missing_ok=True)

def first(lines, fn):
    out = list(lines); i = data(out)[0]; out[i] = fn(out[i]); return out

def for_id(lines, rid, fn):
    out = list(lines)
    i = next(i for i, line in enumerate(out) if line.startswith(rid + "\t"))
    out[i] = fn(out[i])
    return out

def set_field(lines, rid, field, value):
    return for_id(lines, rid, lambda x: "\t".join(x.split("\t")[:field] + [value] + x.split("\t")[field + 1:]))

def set_fields(lines, rid, values):
    return for_id(lines, rid, lambda x: "\t".join(x.split("\t")[:6] + list(values)))

def replace_columns(lines, rid, changes):
    def mutate(x):
        fields = x.split("\t")
        for index, value in changes.items():
            fields[index] = value
        return "\t".join(fields)
    return for_id(lines, rid, mutate)

def downgrade_documented(lines, rid):
    return replace_columns(for_id(lines, rid, lambda x: x.replace("mapped-existing", "new-record-required", 1)), rid,
                           {5: "Missing from reviewed L-track evidence: temporary", 6: "-", 7: "-", 8: "-"})

def expect_fail(name, mutator, needle):
    code, output = run(mutator)
    assert code != 0, f"{name}: malformed mapping unexpectedly passed"
    assert needle in output, f"{name}: missing diagnostic {needle!r}: {output[-300:]}"

def source_regression_checks():
    rows = {line.split("\t", 1)[0]: line.split("\t") for line in MAP.read_text().splitlines() if line and not line.startswith("#")}
    expected = {
        "VID-01": (("tasks/L04-L14-anonymous-payment-identity-attribution.md", "tests/TC-L04-L14-anonymous-payment-identity-attribution.md", "reviews/2026-09-14-L04-L14-anonymous-payment-identity-attribution-decision.md"), ("fingerprint", "webhook", "identity")),
        "VID-02": (("tasks/L04-L14-anonymous-payment-identity-attribution.md", "tests/TC-L04-L14-anonymous-payment-identity-attribution.md", "reviews/2026-09-14-L04-L14-anonymous-payment-identity-attribution-decision.md"), ("relation", "refund")),
        "VID-03": (("tasks/L14-viewer-identity-and-supporter-history.md", "tests/TC-L14-viewer-identity-and-supporter-history.md", "reviews/2026-09-08-L14-local-completion-and-claim-boundary-review.md"), ("receipt", "confirmation")),
        "VID-04": (("tasks/L14-viewer-identity-and-supporter-history.md", "tests/TC-L14-viewer-identity-and-supporter-history.md", "reviews/2026-09-08-L14-local-completion-and-claim-boundary-review.md"), ("SHA-256", "refund")),
        "VID-06": (("tasks/L14-viewer-identity-and-supporter-history.md", "tests/TC-L14-viewer-identity-and-supporter-history.md", "reviews/2026-09-08-L14-local-completion-and-claim-boundary-review.md"), ("claim", "contested", "verifier")),
        "VID-08": (("tasks/L14-public-viewer-privacy-and-bounds-hardening.md", "tests/TC-L14-public-viewer-privacy-and-bounds-hardening.md", "reviews/2026-09-09-L14-public-viewer-privacy-and-bounds-hardening-decision.md"), ("profile", "private")),
        "VID-09": (("tasks/L14-public-viewer-privacy-and-bounds-hardening.md", "tests/TC-L14-public-viewer-privacy-and-bounds-hardening.md", "reviews/2026-09-09-L14-public-viewer-privacy-and-bounds-hardening-decision.md"), ("newest-100", "deterministic")),
        "ENG-01": (("tasks/L16-interaction-menu-goals-and-widgets.md", "tests/TC-L16-interaction-menu-goals-and-widgets.md", "reviews/2026-09-08-L16-widget-completion-review.md"), ("interaction", "tier")),
        "ENG-02": (("tasks/L16-interaction-menu-goals-and-widgets.md", "tests/TC-L16-interaction-menu-goals-and-widgets.md", "reviews/2026-09-08-L16-widget-completion-review.md"), ("widget", "tier")),
        "ENG-03": (("tasks/L16-interaction-menu-goals-and-widgets.md", "tests/TC-L16-interaction-menu-goals-and-widgets.md", "reviews/2026-09-08-L16-widget-completion-review.md"), ("goal", "window")),
        "ENG-04": (("tasks/L16-interaction-menu-goals-and-widgets.md", "tests/TC-L16-interaction-menu-goals-and-widgets.md", "reviews/2026-09-08-L16-widget-completion-review.md"), ("pages", "mega-tip")),
        "ENG-05": (("tasks/L16-interaction-menu-goals-and-widgets.md", "tests/TC-L16-interaction-menu-goals-and-widgets.md", "reviews/2026-09-08-L16-widget-completion-review.md"), ("leaderboard", "coarse")),
        "ENG-06": (("tasks/L16-overlay-widget-response-integrity.md", "tests/TC-L16-overlay-widget-response-integrity.md", "reviews/2026-09-09-L16-overlay-widget-response-integrity-decision.md"), ("overlay", "SSE")),
        "ENG-07": (("tasks/L16-interaction-menu-goals-and-widgets.md", "tests/TC-L16-interaction-menu-goals-and-widgets.md", "reviews/2026-09-14-L16-public-paid-vote-reachability-decision.md"), ("payment", "refund")),
        "ENG-08": (("tasks/L16-vote-option-cardinality-and-overlay-contract-alignment.md", "tests/TC-L16-vote-option-cardinality-and-overlay-contract-alignment.md", "reviews/2026-09-09-L16-vote-option-cardinality-and-overlay-contract-alignment-decision.md"), ("option", "16")),
        "CHL-01": (("tasks/L17-paid-challenges.md", "tests/TC-L17-paid-challenges.md", "reviews/2026-09-08-L17-nonrefundable-challenge-decision.md"), ("non-refundable", "state", "progress", "overlay")),
        "MED-01": (("tasks/L01-public-sticker-contract-slice.md", "tests/TC-L01-public-sticker-contract-slice.md", "reviews/2026-09-09-L01-public-sticker-contract-slice-decision.md"), ("projection", "revalidation", "enablement")),
        "MED-07": (("tasks/L01-public-sticker-contract-slice.md", "tests/TC-L01-public-sticker-contract-slice.md", "reviews/2026-09-09-L01-public-sticker-contract-slice-decision.md"), ("opaque", "asset", "IDs")),
        "CMP-08": (("tasks/L07-companion-web-mobile-desktop.md", "tests/TC-L07-companion-web-mobile-desktop.md", "reviews/2026-08-15-L07-L08-L10-release-surface-review.md"), ("§31.8", "real OBS", "pairing", "Keychain", "staging")),
        "PRF-09": (("tasks/L03-alerts-web-and-creator-api.md", "tests/TC-L03-alerts-web-and-creator-api.md", "reviews/2026-08-16-L03-corrected-findings-remediation-review.md"), ("§31.18", "DATABASE_URL_DIRECT", "pool", "LISTEN", "replay")),
    }
    coverage = {line.split("\t", 1)[0]: tuple(line.split("\t")[2:5]) for line in (ROOT / "active/traceability/coverage-index.tsv").read_text().splitlines() if line and not line.startswith("#")}
    for rid, (triple, checks) in expected.items():
        assert tuple(rows[rid][6:9]) == triple
        assert coverage[rid] == triple
        basis = rows[rid][4].lower()
        assert all(token.lower() in basis for token in checks)
    print(f"mapping source regressions: {len(expected)} passed")

def unresolved_regression_checks():
    rows = {line.split("\t", 1)[0]: line.split("\t") for line in MAP.read_text().splitlines() if line and not line.startswith("#")}
    # Rows live here only while they are UNRESOLVED. When a row earns its
    # task/test/review triad it is promoted to `active-record` and must leave
    # this dict -- its evidence, not its wording, is the guarantee from then on.
    # RT-02/03/04/05/06/08/12 left on 2026-09-18 for exactly that reason.
    required = {
        "MED-03": ("scan", "attestation", "pending_review", "Open/Not run", "ordering"),
        "MED-04": ("is_platform_admin", "E2E", "RLS", "verification pending", "audit-order"),
        "OPS-06": ("seven", "critical", "runbook", "owner", "tested"),
        "OPS-09": ("seven", "metrics", "synthetic", "scrape", "threshold"),
        "MKT-01": ("static", "alerts", "mirror", "stream", "301"),
        "MKT-02": ("CommissionCalculator", "provider-fee", "dual-sided", "Razorpay", "pending"),
        "CMP-09": ("Windows", "XML", "DPAPI", "pairing", "compiled"),
        "CMP-06": ("0082", "L07-03", "Not run", "pairing", "device"),
        "PRF-10": ("L03-22", "0027", "composite", "history", "universal", "bounded"),
        "PRF-19": ("64", "128", "projection", "selected", "every", "endpoint", "select"),
        "PRF-01": ("Prometheus", "normalized", "duration", "histogram", "buckets", "cross-instance", "p95", "p99", "CI-enforced", "L09-03", "Not run", "averages"),
        "PRF-11": ("0027", "created_at", "id", "ordering", "widget", "composite-index", "EXPLAIN ANALYZE", "every", "query-change", "PRF-11", "RT-12"),
        "WMK-01": ("0096", "Free-only", "watermark", "separate", "Master Canvas", "protected top layer", "every module", "error boundaries", "module failure", "WMK-01", "ALQ-18", "PRF-02", "OVL-E8"),
        "WMK-02": ("nine", "anchor", "placement", "scale", "width", "Master Canvas", "reserved", "fixed-corner", "refuses", "module", "overlap", "WMK-02", "OVL-E9"),
        "WMK-05": ("0096", "Free-only", "HTML/CSS/JS", "paid tier", "overlay", "widget", "tip page", "end-card", "QR", "TTS", "email", "issuer-identity", "carve-out", "WMK-05"),
        "PRF-17": ("public-channel", "cursor", "overlay", "normalised", "amount-free", "§12.7", "dashboard", "50", "virtual", "first paint", "Master Canvas", "aggregated", "capped", "Companion"),
        "PRF-04": ("bounded", "display", "timer", "unmount", "acknowledg", "DOM", "recycling", "Master Canvas", "8-hour", "flat", "node", "memory", "OVL-E1"),
        "PRF-08": ("captured payments", "processed refunds", "stored counter", "SSE", "REST snapshot", "read-through cache", "channel", "widget", "durable event", "WidgetPoller", "interval polling", "stampede", "§19.6"),
        "PRF-06": ("120-request", "429", "Retry-After", "delay-only", "aggregation", "server-side", "sampling", "reactions", "chat", "source-specific", "coalescing", "PRF-06"),
        "ALQ-18": ("fragment-token", "SSE", "REST snapshot invalidation", "Master Canvas", "one OBS browser source", "one connection", "requestAnimationFrame", "pure-module", "watermark", "OVL-E8", "OVL-E9", "OVL-E10"),
        "ALQ-16": ("Last-Event-ID", "acknowledged cursor", "bounded exponential backoff", "1-hour", "coalesces", "summary", "bounded catch-up", "OVL-E5"),
        "CMP-23": ("L07-21/22/30", "recent-tip", "payment-status", "refund-status", "web caller"),
        "CMP-25": ("L07-21/22", "0057", "six", "three", "matrix"),
    }
    for rid, terms in required.items():
        assert rows[rid][3] == "new-record-required" and rows[rid][6:9] == ["-", "-", "-"], (
            f"{rid} is no longer an unresolved row (lifecycle {rows[rid][3]}, evidence "
            f"{rows[rid][6:9]}) -- remove it from required{{}}; its triad now carries the guarantee")
        text = (rows[rid][4] + " " + rows[rid][5]).lower()
        assert all(term.lower() in text for term in terms), (rid, text)
    prf02 = rows["PRF-02"]
    assert prf02[3] == "new-record-required" and prf02[6:9] == ["-", "-", "-"]
    prf02_text = (prf02[4] + " " + prf02[5]).lower()
    assert all(term.lower() in prf02_text for term in required["ALQ-18"])
    # RT-12's negative-semantics guard lived here while RT-12 was unresolved: its
    # missing_behavior had to keep saying no EXPLAIN proof existed, so the row
    # could not be quietly softened into sounding done. RT-12 was completed and
    # promoted to active-record on the JIT track (active/tasks/RT-12.md,
    # tests/TC-RT-12-explain-plans.md, reviews/2026-09-16-rt-12-explain-plans.md)
    # and its missing_behavior is now "-", so the guard had nothing left to read.
    # PRF-11 still carries the equivalent unresolved phrasing and is still guarded
    # by prf11-positive-index-claim.
    print(f"mapping unresolved regressions: {len(required)} passed")

def jit_lifecycle_checks():
    rows = [line for line in MAP.read_text().splitlines() if line and not line.startswith("#")]
    lifecycles = {line.split("\t")[3] for line in rows}
    assert lifecycles == {"mapped-existing", "new-record-required", "active-record"}
    assert all(line.split("\t")[3] != "active-record" or line.split("\t")[6].startswith("active/tasks/") for line in rows)
    env_rows = {line.split("\t")[0]: line.split("\t") for line in rows if line.split("\t")[0].startswith("ENV-")}
    assert set(env_rows) == {f"ENV-0{i}" for i in range(1, 10)}
    assert all(row[3] == "active-record" and row[6] == f"active/tasks/{rid}.md" and row[7].startswith(f"tests/TC-{rid}-") and row[8].startswith("reviews/2026-09-15-") for rid, row in env_rows.items())
    print("JIT lifecycle checks: mapped-existing/new-record-required/active-record set accepted; ENV-01..09 exact targets verified")

def jit_active_fixture_checks():
    template = "\n".join(f"**{field}** | fixture" for field in ("Scope phase", "Owner", "Tier and gate", "Personal-data class", "Provider or legal dependency", "Failure behaviour", "Kill switch", "Acceptance test", "Evidence location", "Rollback"))
    with tempfile.TemporaryDirectory(prefix="bharatstudio-jit-", dir=ROOT / "active/tasks") as tmp:
        task_path = pathlib.Path(tmp) / "PAY-10.md"
        task_path.write_text(template, encoding="utf-8")
        def mutate(lines, task_target):
            out = list(lines); i = next(i for i, line in enumerate(out) if line.startswith("PAY-10\t")); fields = out[i].split("\t")
            fields[3] = "active-record"; fields[6] = task_target; fields[7] = "tests/TC-L04-go-payment-boundary.md"; fields[8] = "reviews/2026-08-14-L04-provider-boundary-review.md"; out[i] = "\t".join(fields); return out
        base = MAP.read_text(encoding="utf-8").splitlines()
        def check(lines, task_target, expected, label):
            with tempfile.NamedTemporaryFile(prefix="bharatstudio-jit-map-", suffix=".tsv", mode="w", delete=False) as f:
                path = pathlib.Path(f.name); path.write_text("\n".join(lines) + "\n", encoding="utf-8")
            try:
                env = os.environ.copy(); env["BHARATSTUDIO_MAPPING_PATH"] = str(path); env["BHARATSTUDIO_TRACEABILITY_VALIDATE_ONLY"] = "1"
                p = subprocess.run(["python3", str(ROOT / "tools/bootstrap_check.py")], cwd=ROOT, env=env, text=True, capture_output=True)
                assert (p.returncode == 0) == (expected == "pass"), (label, p.stdout + p.stderr)
                if expected != "pass": assert expected in p.stdout + p.stderr, (label, p.stdout + p.stderr)
            finally: path.unlink(missing_ok=True)
        check(mutate(base, "active/tasks/" + pathlib.Path(tmp).name + "/PAY-10.md"), "active/tasks/", "pass", "valid active fixture")
        bad = task_path.read_text(encoding="utf-8").replace("**Rollback**", "Rollback")
        task_path.write_text(bad, encoding="utf-8")
        check(mutate(base, "active/tasks/" + pathlib.Path(tmp).name + "/PAY-10.md"), "active/tasks/", "lacks a complete ten-field task record", "missing ten-field label")
        check(mutate(base, "active/tasks/../PAY-10.md"), "active/tasks/../", "unsafe target", "unsafe active target")
        with tempfile.TemporaryDirectory(prefix="bharatstudio-all-active-", dir=ROOT / "active/tasks") as all_tmp:
            all_dir = pathlib.Path(all_tmp)
            all_lines = []
            for line in base:
                if not line or line.startswith("#"):
                    all_lines.append(line); continue
                fields = line.split("\t"); rid = fields[0]
                (all_dir / f"{rid}.md").write_text(template, encoding="utf-8")
                fields[3] = "active-record"; fields[6] = f"active/tasks/{all_dir.name}/{rid}.md"
                fields[7] = "tests/TC-L04-go-payment-boundary.md"; fields[8] = "reviews/2026-08-14-L04-provider-boundary-review.md"
                all_lines.append("\t".join(fields))
            with tempfile.NamedTemporaryFile(prefix="bharatstudio-empty-coverage-", suffix=".tsv", mode="w", delete=False) as cf:
                coverage_path = pathlib.Path(cf.name)
            try:
                coverage_path.write_text("# disposable empty coverage\n", encoding="utf-8")
                with tempfile.NamedTemporaryFile(prefix="bharatstudio-all-active-map-", suffix=".tsv", mode="w", delete=False) as mf:
                    map_path = pathlib.Path(mf.name); map_path.write_text("\n".join(all_lines) + "\n", encoding="utf-8")
                try:
                    env = os.environ.copy(); env["BHARATSTUDIO_MAPPING_PATH"] = str(map_path); env["BHARATSTUDIO_COVERAGE_PATH"] = str(coverage_path)
                    p = subprocess.run(["python3", str(ROOT / "tools/bootstrap_check.py")], cwd=ROOT, env=env, text=True, capture_output=True)
                    assert p.returncode != 0 and "all-rows-active policy is invalid" in p.stdout + p.stderr
                finally: map_path.unlink(missing_ok=True)
            finally: coverage_path.unlink(missing_ok=True)
    with tempfile.TemporaryDirectory(prefix="bharatstudio-doc-root-") as tmp_root:
        doc_root = pathlib.Path(tmp_root) / "requirements"
        shutil.copytree(ROOT, doc_root)
        master = doc_root / "FULL-PRODUCT-DEFINITION.md"
        # Retain JIT wording while adding the prohibited blanket policy.
        body = master.read_text(encoding="utf-8") + "\nEvery register row carries an active record before any lane starts.\n"
        master.write_text(body, encoding="utf-8")
        env = os.environ.copy(); env["BHARATSTUDIO_DOC_ROOT"] = str(doc_root)
        p = subprocess.run(["python3", str(ROOT / "tools/doc_consistency.py")], cwd=ROOT, env=env, text=True, capture_output=True)
        assert p.returncode != 0 and "jit-policy" in p.stdout + p.stderr
    with tempfile.TemporaryDirectory(prefix="bharatstudio-step0-counts-") as tmp_root:
        doc_root = pathlib.Path(tmp_root) / "requirements"
        shutil.copytree(ROOT, doc_root)
        master = doc_root / "FULL-PRODUCT-DEFINITION.md"
        master.write_text(master.read_text(encoding="utf-8") +
                          "\nLive reconciliation: 66 mapped-existing + 717 new-record-required.\n",
                          encoding="utf-8")
        env = os.environ.copy(); env["BHARATSTUDIO_DOC_ROOT"] = str(doc_root)
        p = subprocess.run(["python3", str(ROOT / "tools/doc_consistency.py")], cwd=ROOT, env=env, text=True, capture_output=True)
        assert p.returncode != 0 and "step0-master-counts" in p.stdout + p.stderr
    print("JIT active-record fixture checks: 3 passed")
    print("JIT all-active/doc-root hostile checks: 2 passed")

def environment_review_hostile_checks():
    """Ensure review evidence cannot regress to vague or stale claims."""
    mutations = [
        ("execution remains open", "env-review"),
        ("validate-measurement-manifest.mjs", "env-review"),
    ]
    for needle, expected in mutations:
        with tempfile.TemporaryDirectory(prefix="bharatstudio-env-review-") as tmp:
            doc_root = pathlib.Path(tmp) / "requirements"
            shutil.copytree(ROOT, doc_root)
            review = doc_root / "reviews/2026-09-15-env-01-measurement-control.md"
            body = review.read_text(encoding="utf-8")
            if needle == "execution remains open":
                body = body.replace("Cloud Run/IAM is not-run", "Cloud Run/IAM execution remains open")
            else:
                body = body.replace("validate-measurement-manifest.mjs", "missing-command-token")
            review.write_text(body, encoding="utf-8")
            env = os.environ.copy(); env["BHARATSTUDIO_DOC_ROOT"] = str(doc_root)
            p = subprocess.run(["python3", str(ROOT / "tools/doc_consistency.py")], cwd=ROOT, env=env, text=True, capture_output=True)
            assert p.returncode != 0 and expected in p.stdout + p.stderr, (needle, p.stdout + p.stderr)
    print("environment review hostile checks: 2 passed")

def audit_hostile_checks():
    original = AUDIT.read_text(encoding="utf-8")
    def run(mutator):
        with tempfile.NamedTemporaryFile(prefix="bharatstudio-audit-", suffix=".md", mode="w", delete=False) as f:
            path = pathlib.Path(f.name)
        try:
            mutated = mutator(original.splitlines())
            path.write_text("\n".join(mutated) + "\n", encoding="utf-8")
            env = os.environ.copy(); env["BHARATSTUDIO_AUDIT_PATH"] = str(path); env["BHARATSTUDIO_TRACEABILITY_VALIDATE_ONLY"] = "1"
            p = subprocess.run(["python3", str(CHECK), "--validate-only"], cwd=ROOT, env=env, text=True, capture_output=True)
            return p.returncode, p.stdout + p.stderr
        finally: path.unlink(missing_ok=True)
    def row_index(lines): return next(i for i,x in enumerate(lines) if x.startswith("| ENG-08 |"))
    cases = [
        (lambda ls: ls[:row_index(ls)] + [ls[row_index(ls)].replace("mapped-existing", "new-record-required", 1)] + ls[row_index(ls)+1:], "audit validation failed: ENG-08 parity mismatch"),
        (lambda ls: ls + [ls[row_index(ls)]], "audit validation failed: duplicate ENG-08"),
        (lambda ls: [x for i,x in enumerate(ls) if i != row_index(ls)], "audit validation failed: missing IDs: ENG-08"),
    ]
    for mutator, needle in cases:
        code, output = run(mutator); assert code != 0 and needle in output, output
    assert AUDIT.read_text(encoding="utf-8") == original
    print("audit hostile tests: 3 passed")

def case(spec):
    name, mutator, needle = spec
    code, output = run(mutator)
    assert code != 0, f"{name}: malformed mapping unexpectedly passed"
    assert needle in output, f"{name}: missing diagnostic {needle!r}: {output[-300:]}"

def genericization_fixture_freshness(cases):
    """A genericization fixture only exercises the generic-basis rule against a
    `new-record-required` row. Once a row is promoted to `active-record` the
    mutation trips audit parity first, and the suite reports a register
    mismatch instead of a stale fixture -- which is how seven of these rotted
    unnoticed until 2026-09-18. Check the targets before running anything."""
    lifecycles = {}
    for line in MAP.read_text(encoding="utf-8").splitlines():
        if not line or line.startswith("#"):
            continue
        fields = line.split("\t")
        if len(fields) > 3:
            lifecycles[fields[0]] = fields[3]
    stale = []
    for name, mutator, _needle in cases:
        if not name.endswith("-genericization"):
            continue
        for rid in re.findall(r'"([A-Z]{2,4}-\d+)"', inspect.getsource(mutator)):
            if lifecycles.get(rid) != "new-record-required":
                stale.append(f"{name} targets {rid}, now {lifecycles.get(rid, 'ABSENT')}")
    if stale:
        raise SystemExit(
            "stale genericization fixtures -- retarget them at rows that are still "
            "new-record-required, or remove them:\n  " + "\n  ".join(stale))


def main():
    cases = [
        ("duplicate", lambda ls: ls + [ls[data(ls)[0]]], "duplicate"),
        ("unknown", lambda ls: first(ls, lambda x: x.replace("PAY-01", "ZZZ-99", 1)), "unknown requirement"),
        ("missing", lambda ls: [x for i, x in enumerate(ls) if i != data(ls)[0]], "missing"),
        ("unsafe-target", lambda ls: first(ls, lambda x: x.replace("tasks/L04-go-payment-boundary.md", "tasks/../secrets.md", 1)), "unsafe"),
        ("unowned-taken", lambda ls: for_id(ls, "PAY-02", lambda x: x.replace("mapped-existing", "active-record", 1).replace("\ttasks/L04-go-payment-boundary.md\t", "\tactive/tasks/STEP-0-register-mapping.md\t", 1)), "documented in coverage-index"),
        ("phase-state", lambda ls: first(ls, lambda x: x.replace("\tv1\tU\t", "\tP2\tU\t", 1)), "phase/state mismatch"),
        ("missing-lifecycle-evidence", lambda ls: set_fields(for_id(ls, "PAY-02", lambda x: x.replace("mapped-existing", "active-record", 1)), "PAY-02", ("-", "-", "-")), "documented in coverage-index"),
        ("false-completion", lambda ls: set_fields(for_id(ls, "PAY-02", lambda x: x.replace("mapped-existing", "active-record", 1)), "PAY-02", ("active/tasks/STEP-0-register-mapping.md", "tests/TC-STEP-0-register-mapping.md", "reviews/2026-09-15-step-0-register-mapping.md")), "documented in coverage-index"),
        ("mapped-existing-missing-triad", lambda ls: first(ls, lambda x: x.replace("tasks/L04-go-payment-boundary.md", "tasks/missing.md", 1)), "target does not exist"),
        ("mapped-existing-basis", lambda ls: set_field(ls, "PAY-01", 4, "bad"), "human evidence basis"),
        ("generic-unresolved-basis", lambda ls: replace_columns(ls, "PAY-10", {4: "Manual inventory: none-found-after-exact-id-search", 5: "Missing from reviewed L-track evidence: none-found-after-exact-id-search", 6: "-", 7: "-", 8: "-"}), "item-specific unfulfilled behavior"),
        ("documented-coverage-cannot-downgrade", lambda ls: for_id(ls, "PAY-02", lambda x: x.replace("mapped-existing", "new-record-required", 1).replace("-\ttasks/L04-go-payment-boundary.md\ttests/TC-L04-go-payment-boundary.md\treviews/2026-08-14-L04-provider-boundary-review.md", "Missing from reviewed L-track evidence: temporary\t-\t-\t-", 1)), "documented in coverage-index"),
        ("alq01-coverage-cannot-downgrade", lambda ls: downgrade_documented(ls, "ALQ-01"), "documented in coverage-index"),
        ("alq02-coverage-cannot-downgrade", lambda ls: downgrade_documented(ls, "ALQ-02"), "documented in coverage-index"),
        ("alq03-coverage-cannot-downgrade", lambda ls: downgrade_documented(ls, "ALQ-03"), "documented in coverage-index"),
        ("alq07-coverage-cannot-downgrade", lambda ls: downgrade_documented(ls, "ALQ-07"), "documented in coverage-index"),
        ("alq08-coverage-cannot-downgrade", lambda ls: downgrade_documented(ls, "ALQ-08"), "documented in coverage-index"),
        ("alq09-coverage-cannot-downgrade", lambda ls: downgrade_documented(ls, "ALQ-09"), "documented in coverage-index"),
        ("tts05-coverage-cannot-downgrade", lambda ls: downgrade_documented(ls, "TTS-05"), "documented in coverage-index"),
        ("alq12-coverage-cannot-downgrade", lambda ls: downgrade_documented(ls, "ALQ-12"), "documented in coverage-index"),
        ("alq13-coverage-cannot-downgrade", lambda ls: downgrade_documented(ls, "ALQ-13"), "documented in coverage-index"),
        ("alq14-coverage-cannot-downgrade", lambda ls: downgrade_documented(ls, "ALQ-14"), "documented in coverage-index"),
        ("alq04-coverage-cannot-downgrade", lambda ls: downgrade_documented(ls, "ALQ-04"), "documented in coverage-index"),
        ("alq05-coverage-cannot-downgrade", lambda ls: downgrade_documented(ls, "ALQ-05"), "documented in coverage-index"),
        ("alq06-coverage-cannot-downgrade", lambda ls: downgrade_documented(ls, "ALQ-06"), "documented in coverage-index"),
        ("alq10-coverage-cannot-downgrade", lambda ls: downgrade_documented(ls, "ALQ-10"), "documented in coverage-index"),
        ("alq11-coverage-cannot-downgrade", lambda ls: downgrade_documented(ls, "ALQ-11"), "documented in coverage-index"),
        ("fresh-source-coverage-cannot-downgrade", lambda ls: downgrade_documented(ls, "TTS-02"), "documented in coverage-index"),
        ("ops-coverage-cannot-downgrade", lambda ls: downgrade_documented(ls, "OPS-01"), "documented in coverage-index"),
        ("mkt-coverage-cannot-downgrade", lambda ls: downgrade_documented(ls, "MKT-03"), "documented in coverage-index"),
        ("cmp05-coverage-cannot-downgrade", lambda ls: downgrade_documented(ls, "CMP-05"), "documented in coverage-index"),
        ("cmp37-coverage-cannot-downgrade", lambda ls: downgrade_documented(ls, "CMP-37"), "documented in coverage-index"),
        ("vid01-09-coverage-cannot-downgrade", lambda ls: downgrade_documented(ls, "VID-01"), "documented in coverage-index"),
        ("vid02-coverage-cannot-downgrade", lambda ls: downgrade_documented(ls, "VID-02"), "documented in coverage-index"),
        ("vid03-coverage-cannot-downgrade", lambda ls: downgrade_documented(ls, "VID-03"), "documented in coverage-index"),
        ("vid04-coverage-cannot-downgrade", lambda ls: downgrade_documented(ls, "VID-04"), "documented in coverage-index"),
        ("vid06-coverage-cannot-downgrade", lambda ls: downgrade_documented(ls, "VID-06"), "documented in coverage-index"),
        ("vid08-coverage-cannot-downgrade", lambda ls: downgrade_documented(ls, "VID-08"), "documented in coverage-index"),
        ("vid09-coverage-cannot-downgrade", lambda ls: downgrade_documented(ls, "VID-09"), "documented in coverage-index"),
        ("vid02-mispointed-target", lambda ls: for_id(ls, "VID-02", lambda x: x.replace("tasks/L04-L14-anonymous-payment-identity-attribution.md", "tasks/L14-viewer-identity-and-supporter-history.md", 1)), "mapping targets do not match coverage-index"),
        ("vid03-mispointed-target", lambda ls: for_id(ls, "VID-03", lambda x: x.replace("tasks/L14-viewer-identity-and-supporter-history.md", "tasks/L04-L14-anonymous-payment-identity-attribution.md", 1)), "mapping targets do not match coverage-index"),
        ("vid01-mispointed-target", lambda ls: for_id(ls, "VID-01", lambda x: x.replace("tasks/L04-L14-anonymous-payment-identity-attribution.md", "tasks/L03-alerts-web-and-creator-api.md", 1)), "mapping targets do not match coverage-index"),
        ("vid04-mispointed-target", lambda ls: for_id(ls, "VID-04", lambda x: x.replace("tasks/L14-viewer-identity-and-supporter-history.md", "tasks/L03-alerts-web-and-creator-api.md", 1)), "mapping targets do not match coverage-index"),
        ("vid06-mispointed-target", lambda ls: for_id(ls, "VID-06", lambda x: x.replace("tasks/L14-viewer-identity-and-supporter-history.md", "tasks/L03-alerts-web-and-creator-api.md", 1)), "mapping targets do not match coverage-index"),
        ("vid08-mispointed-target", lambda ls: for_id(ls, "VID-08", lambda x: x.replace("tasks/L14-public-viewer-privacy-and-bounds-hardening.md", "tasks/L14-viewer-identity-and-supporter-history.md", 1)), "mapping targets do not match coverage-index"),
        ("vid09-mispointed-target", lambda ls: for_id(ls, "VID-09", lambda x: x.replace("tasks/L14-public-viewer-privacy-and-bounds-hardening.md", "tasks/L14-viewer-identity-and-supporter-history.md", 1)), "mapping targets do not match coverage-index"),
        ("eng01-mispointed-target", lambda ls: for_id(ls, "ENG-01", lambda x: x.replace("tasks/L16-interaction-menu-goals-and-widgets.md", "tasks/L03-alerts-web-and-creator-api.md", 1)), "mapping targets do not match coverage-index"),
        ("eng02-mispointed-target", lambda ls: for_id(ls, "ENG-02", lambda x: x.replace("tasks/L16-interaction-menu-goals-and-widgets.md", "tasks/L03-alerts-web-and-creator-api.md", 1)), "mapping targets do not match coverage-index"),
        ("eng03-mispointed-target", lambda ls: for_id(ls, "ENG-03", lambda x: x.replace("tasks/L16-interaction-menu-goals-and-widgets.md", "tasks/L03-alerts-web-and-creator-api.md", 1)), "mapping targets do not match coverage-index"),
        ("eng04-mispointed-target", lambda ls: for_id(ls, "ENG-04", lambda x: x.replace("tasks/L16-interaction-menu-goals-and-widgets.md", "tasks/L03-alerts-web-and-creator-api.md", 1)), "mapping targets do not match coverage-index"),
        ("eng05-mispointed-target", lambda ls: for_id(ls, "ENG-05", lambda x: x.replace("tasks/L16-interaction-menu-goals-and-widgets.md", "tasks/L03-alerts-web-and-creator-api.md", 1)), "mapping targets do not match coverage-index"),
        ("eng06-mispointed-target", lambda ls: for_id(ls, "ENG-06", lambda x: x.replace("tasks/L16-overlay-widget-response-integrity.md", "tasks/L03-alerts-web-and-creator-api.md", 1)), "mapping targets do not match coverage-index"),
        ("eng07-mispointed-target", lambda ls: for_id(ls, "ENG-07", lambda x: x.replace("tasks/L16-interaction-menu-goals-and-widgets.md", "tasks/L03-alerts-web-and-creator-api.md", 1)), "mapping targets do not match coverage-index"),
        ("eng08-mispointed-target", lambda ls: for_id(ls, "ENG-08", lambda x: x.replace("tasks/L16-vote-option-cardinality-and-overlay-contract-alignment.md", "tasks/L03-alerts-web-and-creator-api.md", 1)), "mapping targets do not match coverage-index"),
        ("chl01-downgrade", lambda ls: downgrade_documented(ls, "CHL-01"), "documented in coverage-index"),
        ("chl01-mispointed-target", lambda ls: for_id(ls, "CHL-01", lambda x: x.replace("tasks/L17-paid-challenges.md", "tasks/L03-alerts-web-and-creator-api.md", 1)), "mapping targets do not match coverage-index"),
        ("eng01-coverage", lambda ls: downgrade_documented(ls, "ENG-01"), "documented in coverage-index"),
        ("eng02-coverage", lambda ls: downgrade_documented(ls, "ENG-02"), "documented in coverage-index"),
        ("eng03-coverage", lambda ls: downgrade_documented(ls, "ENG-03"), "documented in coverage-index"),
        ("eng04-coverage", lambda ls: downgrade_documented(ls, "ENG-04"), "documented in coverage-index"),
        ("eng05-coverage", lambda ls: downgrade_documented(ls, "ENG-05"), "documented in coverage-index"),
        ("eng06-coverage", lambda ls: downgrade_documented(ls, "ENG-06"), "documented in coverage-index"),
        ("eng07-coverage", lambda ls: downgrade_documented(ls, "ENG-07"), "documented in coverage-index"),
        ("eng08-coverage", lambda ls: downgrade_documented(ls, "ENG-08"), "documented in coverage-index"),
        ("med01-downgrade", lambda ls: downgrade_documented(ls, "MED-01"), "documented in coverage-index"),
        ("med07-downgrade", lambda ls: downgrade_documented(ls, "MED-07"), "documented in coverage-index"),
        ("med01-mispointed-target", lambda ls: for_id(ls, "MED-01", lambda x: x.replace("tasks/L01-public-sticker-contract-slice.md", "tasks/L03-alerts-web-and-creator-api.md", 1)), "mapping targets do not match coverage-index"),
        ("med07-mispointed-target", lambda ls: for_id(ls, "MED-07", lambda x: x.replace("tasks/L01-public-sticker-contract-slice.md", "tasks/L03-alerts-web-and-creator-api.md", 1)), "mapping targets do not match coverage-index"),
        ("med03-genericization", lambda ls: replace_columns(ls, "MED-03", {4: "Manual inventory: none-found", 5: "Missing from reviewed L-track evidence: none-found"}), "item-specific unfulfilled behavior"),
        ("med04-genericization", lambda ls: replace_columns(ls, "MED-04", {4: "Manual inventory: none-found", 5: "Missing from reviewed L-track evidence: none-found"}), "item-specific unfulfilled behavior"),
        ("ops06-genericization", lambda ls: replace_columns(ls, "OPS-06", {4: "Manual inventory: none-found", 5: "Missing from reviewed L-track evidence: none-found"}), "item-specific unfulfilled behavior"),
        ("ops09-genericization", lambda ls: replace_columns(ls, "OPS-09", {4: "Manual inventory: none-found", 5: "Missing from reviewed L-track evidence: none-found"}), "item-specific unfulfilled behavior"),
        ("mkt01-genericization", lambda ls: replace_columns(ls, "MKT-01", {4: "Manual inventory: none-found", 5: "Missing from reviewed L-track evidence: none-found"}), "item-specific unfulfilled behavior"),
        ("mkt02-genericization", lambda ls: replace_columns(ls, "MKT-02", {4: "Manual inventory: none-found", 5: "Missing from reviewed L-track evidence: none-found"}), "item-specific unfulfilled behavior"),
        ("cmp09-genericization", lambda ls: replace_columns(ls, "CMP-09", {4: "Manual inventory: none-found", 5: "Missing from reviewed L-track evidence: none-found"}), "item-specific unfulfilled behavior"),
        ("prf10-genericization", lambda ls: replace_columns(ls, "PRF-10", {4: "Manual inventory: none-found", 5: "Missing from reviewed L-track evidence: none-found"}), "item-specific unfulfilled behavior"),
        ("prf19-genericization", lambda ls: replace_columns(ls, "PRF-19", {4: "Manual inventory: none-found", 5: "Missing from reviewed L-track evidence: none-found"}), "item-specific unfulfilled behavior"),
        ("rt07-genericization", lambda ls: replace_columns(ls, "RT-07", {4: "Manual inventory: none-found", 5: "Missing from reviewed L-track evidence: none-found"}), "item-specific unfulfilled behavior"),
        ("rt09-genericization", lambda ls: replace_columns(ls, "RT-09", {4: "Manual inventory: none-found", 5: "Missing from reviewed L-track evidence: none-found"}), "item-specific unfulfilled behavior"),
        ("rt13-genericization", lambda ls: replace_columns(ls, "RT-13", {4: "Manual inventory: none-found", 5: "Missing from reviewed L-track evidence: none-found"}), "item-specific unfulfilled behavior"),
        ("alq18-prf02-genericization", lambda ls: replace_columns(replace_columns(ls, "ALQ-18", {4: "Manual inventory: none-found", 5: "Missing from reviewed L-track evidence: none-found"}), "PRF-02", {4: "Manual inventory: none-found", 5: "Missing from reviewed L-track evidence: none-found"}), "item-specific unfulfilled behavior"),
        ("prf01-genericization", lambda ls: replace_columns(ls, "PRF-01", {4: "Manual inventory: none-found", 5: "Missing from reviewed L-track evidence: none-found"}), "item-specific unfulfilled behavior"),
        ("prf11-positive-index-claim", lambda ls: for_id(ls, "PRF-11", lambda x: x.replace("no reviewed composite-index inventory", "reviewed composite-index inventory", 1)), "PRF-11 missing required negative semantics: no reviewed composite-index inventory"),
        ("wmk01-genericization", lambda ls: replace_columns(ls, "WMK-01", {4: "Manual inventory: none-found", 5: "Missing from reviewed L-track evidence: none-found"}), "item-specific unfulfilled behavior"),
        ("wmk02-genericization", lambda ls: replace_columns(ls, "WMK-02", {4: "Manual inventory: none-found", 5: "Missing from reviewed L-track evidence: none-found"}), "item-specific unfulfilled behavior"),
        ("wmk05-genericization", lambda ls: replace_columns(ls, "WMK-05", {4: "Manual inventory: none-found", 5: "Missing from reviewed L-track evidence: none-found"}), "item-specific unfulfilled behavior"),
        ("prf17-genericization", lambda ls: replace_columns(ls, "PRF-17", {4: "Manual inventory: none-found", 5: "Missing from reviewed L-track evidence: none-found"}), "item-specific unfulfilled behavior"),
        ("prf04-genericization", lambda ls: replace_columns(ls, "PRF-04", {4: "Manual inventory: none-found", 5: "Missing from reviewed L-track evidence: none-found"}), "item-specific unfulfilled behavior"),
        ("prf08-genericization", lambda ls: replace_columns(ls, "PRF-08", {4: "Manual inventory: none-found", 5: "Missing from reviewed L-track evidence: none-found"}), "item-specific unfulfilled behavior"),
        ("prf06-genericization", lambda ls: replace_columns(ls, "PRF-06", {4: "Manual inventory: none-found", 5: "Missing from reviewed L-track evidence: none-found"}), "item-specific unfulfilled behavior"),
        ("alq16-genericization", lambda ls: replace_columns(ls, "ALQ-16", {4: "Manual inventory: none-found", 5: "Missing from reviewed L-track evidence: none-found"}), "item-specific unfulfilled behavior"),
        ("cmp06-genericization", lambda ls: replace_columns(ls, "CMP-06", {4: "Manual inventory: none-found", 5: "Missing from reviewed L-track evidence: none-found"}), "item-specific unfulfilled behavior"),
        ("cmp23-genericization", lambda ls: replace_columns(ls, "CMP-23", {4: "Manual inventory: none-found", 5: "Missing from reviewed L-track evidence: none-found"}), "item-specific unfulfilled behavior"),
        ("cmp25-genericization", lambda ls: replace_columns(ls, "CMP-25", {4: "Manual inventory: none-found", 5: "Missing from reviewed L-track evidence: none-found"}), "item-specific unfulfilled behavior"),
        ("cmp08-downgrade", lambda ls: downgrade_documented(ls, "CMP-08"), "documented in coverage-index"),
        ("cmp08-mispointed-target", lambda ls: for_id(ls, "CMP-08", lambda x: x.replace("tasks/L07-companion-web-mobile-desktop.md", "tasks/L03-alerts-web-and-creator-api.md", 1)), "mapping targets do not match coverage-index"),
        ("prf09-downgrade", lambda ls: downgrade_documented(ls, "PRF-09"), "documented in coverage-index"),
        ("prf09-mispointed-target", lambda ls: for_id(ls, "PRF-09", lambda x: x.replace("tasks/L03-alerts-web-and-creator-api.md", "tasks/L07-companion-web-mobile-desktop.md", 1)), "mapping targets do not match coverage-index"),
    ]
    genericization_fixture_freshness(cases)
    with ThreadPoolExecutor(max_workers=len(cases)) as pool:
        list(pool.map(case, cases))
    print(f"mapping hostile tests: {len(cases) + 3} passed (duplicate, unknown, missing, unsafe, lifecycle, phase/state, missing-evidence, false-completion, missing-triad, basis-policy, generic-basis, coverage-index-downgrade, mapped-source regressions, audit parity)")
    source_regression_checks()
    unresolved_regression_checks()
    jit_lifecycle_checks()
    jit_active_fixture_checks()
    environment_review_hostile_checks()
    audit_hostile_checks()

if __name__ == "__main__": main()
