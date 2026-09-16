# Full local verification gate — complete run, 2026-09-16

**Owner:** Sukhdev Singh
**Commit verified:** `bharatstudio-alerts` `4dac1aa` · `bharatstudio-requirements` `23aa840` · `bharatstudio-crons` `e10628f`
**Authority:** `FULL-PRODUCT-DEFINITION.md` §35.1, §37.2, §37.11

Every component of the repository's own `pnpm verify:local` gate, run end to end on a quiet
tree with no agents active. Recorded because the gate had not been run complete in this
session — individual checks had, which is not the same claim.

| Check | Result |
|---|---|
| `pnpm contracts:validate` | 42 fixtures · OpenAPI 3.1, 74 paths, 82 operation contracts · 3 negative operation-contract cases |
| `pnpm explain:check` | 18 manifest entries + 9 exemptions; **18/18 plans current**; rules 1, 2 and 3 all reporting |
| `pnpm harness:check` | pass (AJV options and body limit each single-defined and shared) |
| `pnpm deployment:test` | `BSA_DEPLOYMENT_MANIFESTS=PASS`; `BSA_DEPLOYMENT_MANIFEST_TESTS=PASS (1 positive, 4 negative)` |
| `pnpm db:test:all` | `SQL SUITE: pass=63 fail=0` |
| `pnpm db:test:l03` | `pass 2  fail 0` |
| `sh scripts/load/run-l09-load-self-test.sh` | pass — `capturedPaymentsWithoutLiveEvent: 0`, `duplicateLiveEvents: 0` |
| `sh scripts/load/run-l09-fault-self-test.sh` | `L09 FAULT SELF-TEST PASS 5/5` |
| `pnpm --filter @bharatstudio/alerts-api test` | `tests 617  pass 617  fail 0` |
| `pnpm --filter @bharatstudio/alerts-web test` | `tests 472  pass 472  fail 0` |
| `pnpm measurement:test` | `pass 5  fail 0` |
| `pnpm --filter @bharatstudio/alerts-api build` | clean (`tsc -p tsconfig.json`) |
| `pnpm --filter @bharatstudio/alerts-web build` | clean (Next.js build completed) |
| `services/alert-worker-go` | `go build` · `go vet` clean · `go test` 10 packages, 0 failures |
| `services/payment-webhook-go` | `go build` · `go vet` clean · `go test` 10 packages, 0 failures |
| `services/youtube-poller-go` | `go build` · `go vet` clean · `go test` 7 packages, 0 failures |
| `docker build` API image | built, tagged `bharatstudio-alerts-api:qa-local` |
| `docker build` payment image | built, tagged `bharatstudio-alerts-payment:qa-local` |
| `docker build` worker image | built, tagged `bharatstudio-alerts-worker:qa-local` |
| `node .github/scripts/canvas-static-check.mjs` | all checks passed |
| `node .github/scripts/budget-gate-check.mjs` | all checks passed |
| `python3 tools/doc_consistency.py` | 17 checks · 0 errors · 0 warnings |

## What this is, stated precisely

A complete pass of the **local** gate on one developer machine, at pinned tool versions,
against synthetic data. That is all it is.

It is **not** production, provider, payment-provider, app-store, legal, tax, staging, OBS,
device, browser, network, quota, load or release readiness, and it may not be cited as
performance evidence (§35.1 rule 6). In particular:

- The container images were **built**, never run, never deployed, never scanned.
- The CI workflow is committed and was **never executed on GitHub**; branch protection is
  still not enabled.
- The EXPLAIN plans are plan-shape change detectors on minimal seeds, not budget evidence at
  the §37.4 production-scale dataset.
- The load and fault self-tests exercise the mechanism locally; they are not a load test.
- **RT-07 remains Blocked.** No browser, OBS, low-end Android, 3G-profile or 8-hour soak
  evidence exists, so no speed claim and no "one source replaces twelve" claim is publishable,
  and nothing in this run changes that.

## Scope note

Master Canvas stands at nine of twenty §6 catalogue modules. PRF-02's register row remains
`A`; a green local gate is not a reason to move a register letter, and none was moved.
