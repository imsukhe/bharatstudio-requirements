# OPS-CI-01 — continuous integration for bharatstudio-alerts

**Authority:** [`../launch/00_LAUNCH_SCOPE_AUTHORITY.md`](../launch/00_LAUNCH_SCOPE_AUTHORITY.md), [`../launch/07_BUILD_BOOTSTRAP_AUTHORITY.md`](../launch/07_BUILD_BOOTSTRAP_AUTHORITY.md), `FULL-PRODUCT-DEFINITION.md` §31.18.1 PRF-01, §19.0 RT-06/RT-07, §19.4, §35.1 rule 6, §37.4, §31.0, §32 — scope review commanded and verified directly by Opus (this gap was diagnosed by Opus, not discovered independently)
**Status:** `Conditionally complete — local implementation and verification; independent review unavailable; the workflow has never executed on GitHub`

| Field | Value |
|---|---|
| **Scope phase** | `v1`; Phase 0.5 operational tooling — CI enforcement of checks that already exist and already pass under `pnpm verify:local`. No new product behaviour |
| **Owner** | **Sukhdev Singh** |
| **Tier and gate** | All tiers; no release claim. This is a build/test gate, not a runtime capability, and carries no capability-registry row |
| **Personal-data class** | None. No new data field, no new retention rule. Every database this workflow touches is a disposable, loopback-only Docker Postgres container the invoked scripts create and tear down themselves — the same containers `verify:local` already uses locally |
| **Provider or legal dependency** | None. §32 ("Deployment") requires resolved `REQUIRED_*` placeholders, IAM/OIDC, staging recovery, capacity and observability — none of that is exercised here. This workflow needs **no secret** to run (§32 hard rule) |
| **Failure behaviour** | A failing job blocks the GitHub merge/branch-protection surface once branch protection is configured to require it (that configuration is **not** part of this task — see Boundaries). Locally, nothing changes: `pnpm verify:local` remains the hand-run gate it always was. No accepted payment, alert, delivery or overlay record is affected by anything in this workflow — it runs against disposable containers and the checked-out source tree only |
| **Kill switch** | Delete or rename `.github/workflows/ci.yml`, or disable the workflow from the repository's GitHub Actions settings. No application code, migration, schedule or entitlement depends on this workflow existing |
| **Acceptance test** | `tests/TC-OPS-CI-01-alerts-continuous-integration.md` |
| **Evidence location** | `tests/TC-OPS-CI-01-alerts-continuous-integration.md`, `reviews/2026-09-16-ops-ci-01-alerts-continuous-integration.md`, and the workflow/scripts themselves in `bharatstudio-alerts/.github/` |
| **Rollback** | Delete `bharatstudio-alerts/.github/workflows/ci.yml`, `bharatstudio-alerts/.github/scripts/*`, and `bharatstudio-alerts/.github/ci/perf-baseline.local-load.json`. Nothing else in the repository references any of these paths; no migration, schedule or application code changes to revert |

## Why this exists

`bharatstudio-alerts` has **no `.github/workflows` directory** — verified directly, not assumed. Neither do `bharatstudio-crons`, `bharatstudio-infra`, `bharatstudio-platform` or `bharatstudio-admin`. Only `bharatstudio-requirements` has CI (`.github/workflows/doc-consistency.yml`). Every check this repository owns — 585 API tests, 386 web tests, 59 SQL tests (25 more under `db:test:l03`'s curated set plus Go/TS integration legs), both Go services' `-race`/`vet` suites, `contracts:validate`, `explain:check`, `measurement:test` — has run only when a human typed `pnpm verify:local` by hand. This is the §2 failure pattern at repository scale, and it is also why **PRF-01 ("CI-enforced budgets") described nothing**: there was no CI to enforce anything into.

## What this task built

### (a) `bharatstudio-alerts/.github/workflows/ci.yml`

Ten parallel jobs on `push: [master]` and `pull_request`, matching `doc-consistency.yml`'s shape (checkout → setup → named `run` steps, no `continue-on-error` on any correctness check) rather than importing a foreign convention:

| Job | Runs |
|---|---|
| `node-static-checks` | `contracts:validate`, `explain:check`, `deployment:test`, `git diff --check` |
| `unit-tests` | `alerts-api test` (585/0), `alerts-web test` (386/0), `measurement:test` (5 Node + 4 Python) |
| `build` | `pnpm build` (tsc + `next build`) |
| `go-tests` | `go test -race ./... && go vet ./...` for all three services, matrixed (`alert-worker-go`, `payment-webhook-go`, `youtube-poller-go` — Phase 2 per `bharatstudio-alerts/AGENTS.md`, tested here the same as `verify:local` already does) |
| `sql-tests` | `db:test:all` (59/0) and `db:test:l03` (25 curated SQL files + Go and TS integration legs) |
| `l09-self-tests` | `run-l09-load-self-test.sh`, `run-l09-fault-self-test.sh` |
| `docker-builds` | The same three `docker build` commands `verify:local` runs (API, payment-webhook, alert-worker; no push, no registry credential) |
| `budget-gate-mechanism` | RT-06/PRF-01 mechanism — see (b) |
| `canvas-static-check` | PRF-03/PRF-04 static discipline — see (c) |
| `relative-regression` | PRF-01 relative-regression gate — see (b), scope extended by the owner 2026-09-16 |

**Every item `pnpm verify:local` runs is accounted for — every single one runs in CI. Nothing needed a "cannot run" carve-out.** This was verified, not assumed: each check was read for external dependencies before being placed. None calls a live provider; every database is a disposable `docker run postgres:16-alpine` container the invoked script boots and tears down itself (no GitHub Actions `services:` block needed — Docker is preinstalled on `ubuntu-latest`, and the scripts already manage their own container lifecycle, identically to running them locally); the three `docker build` steps push nothing and need no registry credential; the Go toolchain installs via `actions/setup-go`. `git diff --check` is included for parity with `verify:local`'s exact command list, with an honest note in its own step: on a pristine CI checkout it diffs an unmodified tree against the index and is structurally a no-op — its teeth are in local development, exactly as it was used in `tests/TC-RT-02-overlay-channel-fanout.md`.

**Versions — every one read from a file already in the repository, not chosen:**

| Tool | Version | Source |
|---|---|---|
| Node | `22.17.0` | `apps/api/Dockerfile`'s pinned `node:22.17.0-alpine3.22@sha256:…` base image (the repository's own runtime contract; `apps/api/package.json`'s `@types/node@26.2.0` was considered and rejected as the source — a dev-time type-stub version, not a runtime pin, and it disagreed with the Dockerfile) |
| pnpm | `10.32.1` | `package.json` `"packageManager"` |
| Go | `1.26` | Every `services/*/go.mod` (`go 1.26`) and every `services/*/Dockerfile` (`golang:1.26-alpine`) |
| PostgreSQL | `16` (`postgres:16-alpine`) | Every existing `packages/db/tests/*.sh` and `scripts/load/*.sh` harness script |

### (b) PRF-01 budget gate — three parts, built in the order Opus decided

1. **Mechanism** (`.github/scripts/budget-gate-check.mjs`, job `budget-gate-mechanism`). Imports the real, built `apps/api/dist/src/observability/metrics.ts` (never re-implemented), renders its actual Prometheus text exposition, and **parses that text** to assert `bsa_api_read_duration_ms_bucket{le="200"}` and `bsa_api_tip_order_duration_ms_bucket{le="500"}` are on the wire — the two §19.4 boundary buckets. A self-test section feeds the same evaluator a deliberate synthetic breach (every observation past the boundary) and asserts it reports FAIL, proving the pass/fail mechanism can fail. Locally verified end to end, including deliberately breaking a boundary constant in a throwaway copy to prove the *whole script* exits non-zero on a real regression (not committed; the real script was never modified for that proof).
2. **Absolute thresholds, wired but inert** — the same part of this mechanism script. Reads `CI_PRF01_API_READ_P99_BUDGET_MS` / `CI_PRF01_TIP_ORDER_P99_BUDGET_MS`, which this workflow never sets. Unset is the default and the only state this workflow ever produces; the script says so explicitly and never fails on it — there is no live-traffic feed in any CI job for a threshold to check against. This is the same "configured but unset" pattern RT-02 (`OVERLAY_MAX_*_SUBSCRIBERS`), RT-10 and RT-11 already use, extended here rather than reinvented.
3. **Relative-regression** (`.github/scripts/relative-regression-check.sh` + `relative-regression-compare.mjs` + `relative-regression-selftest.mjs`, job `relative-regression`) — **scope extended mid-task by the owner, 2026-09-16, after this task began** (the job had originally been left as a marked, unbuilt placeholder per the operator's initial instruction; the owner's unblocking decision and full reasoning are recorded verbatim in this task's review record). Runs `scripts/load/load-harness.ts` three times against one disposable Postgres container (§37.4's own "three runs, worst is the result" discipline, reused rather than invented), takes the worst of `p50`/`p95`/`p99` across the three, and compares against a checked-in baseline (`.github/ci/perf-baseline.local-load.json`) with **zero tolerance** — any degradation fails the build. The baseline file carries a mandatory, non-empty `reason` field (enforced by `validateBaseline`), so a baseline change is never an incidental diff. A comparator self-test (no Docker needed) runs first in every CI invocation and proves the zero-tolerance evaluator can fail on a synthetic 1ms breach.

**The relative-regression job's real risk, stated plainly and not smoothed over:** with no tolerance band, this check can fail on ordinary CI-runner variance rather than a real regression — the owner chose this deliberately over inventing an unstated tolerance percentage. The documented response when it fires is: re-run first; treat a reproducing failure as a regression; never widen the baseline to make a flake go away. The baseline itself was seeded from **twelve** local establishing runs (not one worst-of-three sample) specifically because a single quiet sample would very likely have failed on the first real GitHub Actions run — full reasoning and the exact numbers are in the baseline file's own `reason` field and in the review record.

### (c) PRF-03 / PRF-04 canvas static check

`.github/scripts/canvas-static-check.mjs`, job `canvas-static-check`. Scans every non-test `.ts`/`.tsx` source under `apps/web/app/overlay/canvas/` (read-only — this task never modified anything under `apps/`), isolates each module's `render()` method (the per-frame method `CanvasModuleDefinition` in `master-canvas-runtime.ts` actually declares and the rAF loop actually calls — one-time `activate()`/`deactivate()` setup styles are deliberately **not** scanned, because declaring a layout property once at creation is not animating it, per §19.5's own wording), and fails if any CSS property other than `opacity`/`transform` is written inside that scope. Verified to **fail** correctly against a deliberately-injected violation in a scratch copy under this session's own scratchpad directory (never inside `apps/` — the real source tree was never touched for this proof). Also reports, but never fails on, a per-module `createElement()` call-site count against `CI_PRF04_MODULE_NODE_CEILING` — unset by default, since no authority states a per-module DOM-node ceiling; see this task's review record's `REFERRED:` section.

**Honest result against current code, run just now, not assumed:** **0 violations across 10 canvas source files.** Every `render()`-path style write in the current codebase already writes only `opacity` or `transform` — `goal-ladder-module.ts`, `boss-fight-module.ts`, `tug-of-war-vote-module.ts` and `supporter-ticker-module.ts` each declare `position`/`height`/`transformOrigin`/`transition` exactly once, in `create`/`ensureElements`, never in `render()`. This is a genuine finding, not a design assumption verified after the fact.

## Boundaries

**In scope:** the CI workflow and its supporting scripts/baseline file, all under `bharatstudio-alerts/.github/`; these three requirements records.

**Explicitly out of scope, not touched:** CI for any other repository; deployment, IAM, OIDC, secrets or environment configuration of any kind; enabling GitHub branch-protection rules to actually *require* these checks (this task creates the workflow; wiring it into branch protection is a separate, later, repository-settings action;  a workflow file committed to a repository is not a workflow that has ever run, and this task's review record says so explicitly); the relative-regression job's sample rule and tolerance were Opus's/the owner's call, not this task's own invention, and are recorded as such; RT-07 evidence; anything under `apps/`, `packages/`, `services/`, `scripts/` (read-only where read at all); the register-map and semantic-mapping-audit files; any `FULL-PRODUCT-DEFINITION.md` register state letter (RT-06/RT-07/PRF-01/PRF-03/PRF-04 are left exactly as they already read, for Opus to set after audit).

## A finding, not fixed

Running `python3 tools/traceability.py` in this repository just now (as this task's own required check) produced a **stale** `TRACEABILITY.md` — five rows out of date against current `active/`/`tests/`/`reviews/` content, almost certainly from concurrent in-flight work by the other agents running alongside this task. The regenerated file was **reverted** (`git checkout -- TRACEABILITY.md`) rather than left modified or committed — it is not this task's file to change, and Opus reconciling concurrent work is expected to regenerate it once every agent's records land. Recorded here so it is not mistaken for something this task broke.
