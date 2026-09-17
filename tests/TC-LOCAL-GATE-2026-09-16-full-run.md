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

---

# Second complete run — 2026-09-17, after PRF-02 slice 6

**Commits verified:** `bharatstudio-alerts` `932a87b` · `bharatstudio-requirements` `5fb2476` ·
`bharatstudio-crons` `e10628f`. Clean trees, zero agent worktrees, no background work in flight.

Re-run because the 2026-09-16 pass was at `4dac1aa` and five slices have landed since: safe mode,
Reaction Cloud, the per-sender rate-limit rework, Lobby Status and Giveaway/Tournament.

| Check | Result | Δ since 2026-09-16 |
|---|---|---|
| `pnpm contracts:validate` | 50 fixtures · 88 paths · 100 operation contracts · 3 negative cases | 42→50 · 74→88 · 82→100 |
| `pnpm explain:check` | 21 manifest + 9 exemptions · **21/21 plans current** | 18→21 |
| `pnpm harness:check` | pass (AJV options **and** body limit single-defined and shared) | body limit added |
| `pnpm deployment:test` | `BSA_DEPLOYMENT_MANIFESTS=PASS` · `MANIFEST_TESTS=PASS (1 positive, 4 negative)` | — |
| `pnpm db:test:all` | `SQL SUITE: pass=67 fail=0` | 63→67 |
| `pnpm db:test:l03` | `pass 2  fail 0` | — |
| `sh scripts/load/run-l09-load-self-test.sh` | pass · `duplicateLiveEvents: 0` | — |
| `sh scripts/load/run-l09-fault-self-test.sh` | `L09 FAULT SELF-TEST PASS 5/5` | — |
| `pnpm --filter @bharatstudio/alerts-api test` | `tests 692  pass 692  fail 0` | 617→692 |
| `pnpm --filter @bharatstudio/alerts-web test` | `tests 560  pass 560  fail 0` | 472→560 |
| `pnpm measurement:test` | `pass 5  fail 0` | — |
| `pnpm --filter @bharatstudio/alerts-api build` | clean | — |
| `pnpm --filter @bharatstudio/alerts-web build` | clean | — |
| `services/alert-worker-go` | build · vet clean · 10 packages ok, 0 fail | — |
| `services/payment-webhook-go` | build · vet clean · 10 packages ok, 0 fail | — |
| `services/youtube-poller-go` | build · vet clean · 7 packages ok, 0 fail | — |
| `docker build` ×3 | all three exit 0 | see note below |
| `node .github/scripts/canvas-static-check.mjs` | all checks passed | — |
| `node .github/scripts/budget-gate-check.mjs` | all checks passed | — |
| `python3 tools/doc_consistency.py` | 17 checks · 0 errors · 0 warnings | — |

## A note on the container images, because the timestamps look wrong and are not

The API image rebuilt and carries a fresh timestamp. The payment and worker images still report
their **previous** build times (11 and 20 hours). That was checked rather than assumed: `git log
4dac1aa..HEAD -- services/payment-webhook-go` and `-- services/alert-worker-go` are both **empty**,
so neither service changed since the run that built those images. Docker therefore hit full layer
cache and re-tagged the identical image, which is correct behaviour and not a stale build. Had
either service changed, the COPY layer hash would have changed and a new image with a new timestamp
would exist.

## Canvas state at this run

**Twelve of twenty** §6 catalogue modules, on **one** connection and **one** rAF loop — asserted
directly against the host page (`createMasterCanvasConnection` ×1, `createMasterCanvasRuntime` ×1,
`registerModule` ×12). **PRF-02's register row remains `A`.** A green gate is not a reason to move
a register letter and none was moved.

## What this run is not — unchanged from the first, and worth restating

Local only, one machine, pinned versions, synthetic data. The images were **built, never run, never
deployed, never scanned**. The CI workflow is committed and has **never executed on GitHub**;
branch protection is still off. The EXPLAIN artefacts are plan-shape change detectors on minimal
seeds, not §37.4 budget evidence. The load and fault self-tests exercise a mechanism; neither is a
load test. **RT-07 remains Blocked** and **GIV-07 remains Blocked** — so no speed claim, no
"one source replaces twelve" claim, and no chance-based giveaway becomes publishable or shippable,
and nothing in this run changes that.
