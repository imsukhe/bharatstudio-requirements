# TC-RT-06 — budget histograms

**Task:** `../active/tasks/RT-06.md`
**Owner:** Sukhdev Singh
**Status:** `Conditionally complete — local verification passed; external release evidence not applicable`

| Case | Control | Expected evidence |
|---|---|---|
| RT-06.1 | Every §19.4 budget a path carries appears as an exact bucket boundary for that path | TS: `READ_DURATION_BUCKETS_MS.includes(200)` and `TIP_ORDER_DURATION_BUCKETS_MS.includes(500)`, plus exposition assertions `bsa_api_read_duration_ms_bucket{le="200"}` and `bsa_api_tip_order_duration_ms_bucket{le="500"}` (`rt06-budget-histograms.test.ts`). Go: `TestBudgetedPathsCarryTheirExactBucketBoundary` (`bsa_payment_tip_order_duration_ms_bucket{le="500"}`, `bsa_payment_webhook_ack_duration_ms_bucket{le="500"}`) and `TestPumpPathCarriesTheReadClassBoundary` (`bsa_worker_pump_duration_ms_bucket{le="200"}`) in both Go services' `histogram_test.go` |
| RT-06.2 | A known set of observations yields the arithmetically correct bucket counts | TS `observeHistogram produces exact bucket counts for a known set of observations`; Go `TestHistogramObserveProducesExactBucketCounts` (identical 10-value distribution, both languages, hand-verified bucket assignment in the test's own comment) |
| RT-06.3 | The p95/p99 read-out is correct for a known distribution, and its documented error bound holds | TS `estimateQuantile matches a known distribution within the bound of the bucket containing the true value`; Go `TestEstimateQuantileMatchesKnownDistributionWithinItsBucketBound` (both languages: a 100-observation distribution with a known nearest-rank p95/p99, asserting the interpolated estimate falls within the bucket that actually contains the true value — the documented bound, not an exact-value assertion). Both languages also assert an empty histogram reports "no observations" rather than a fabricated 0 |
| RT-06.4 | Per-instance histograms sum correctly — the additive property cross-instance aggregation depends on | TS `mergeHistograms sums two independently observed histograms arithmetically correctly` and its mismatched-bucket rejection case; Go `TestMergeHistogramsIsArithmeticallyAdditive` and `TestMergeHistogramsRejectsMismatchedBuckets`, both services |
| RT-06.5 | Labels stay bounded and low-cardinality: no payment, order, event, channel or donor identifier can reach a label | TS `the budgeted histograms carry no labels of any kind`; Go `TestBudgetedHistogramsCarryNoIdentifyingLabels` (payment-webhook-go) and `TestPumpHistogramCarriesNoIdentifyingLabels` (alert-worker-go) — every rendered `_bucket` line for the four new histograms is asserted to carry only `le=`, never a second label |
| RT-06.6 | A metrics failure or slow scrape never delays or alters a request, a payment or a delivery | TS `observeHistogram never throws on a pathological value...`, `metrics.observe never throws even for a pathological duration...`, and the durable-read-failure route test (`a durable-read failure never fails the scrape`); Go `TestHistogramObserveNeverPanicsOnPathologicalInput` (both services, including a nil-receiver call). Design-level guarantee stated in `active/tasks/RT-06.md`'s Failure behaviour field: every histogram mutation is synchronous, in-memory, no I/O; the durable reconciliation write/read are each independently wrapped so a database failure degrades cross-instance freshness only, never the response |
| RT-06.7 | The Prometheus exposition output parses and keeps its existing shape for existing metrics | TS `existing counters and gauges keep their pre-RT-06 shape` (every pre-RT-06 metric name/HELP/TYPE line reasserted, plus a per-line exposition-syntax parse check over the whole output); the full pre-existing `l09-metrics-routes.test.ts` suite re-run unmodified and still green |
| RT-06.8 | Reconciliation snapshot correctness across more than one process | TS `rt06-reconciliation-snapshot-store.test.ts`: two independent `Sql` handles over one shared fake durable table prove a snapshot persisted by one "process" is read back exactly by a second; a later run from a different "process" replaces the snapshot wholesale; `GET /internal/metrics` on an instance with **no in-memory snapshot of its own** still renders the durably recorded values. SQL: `packages/db/tests/rt06_reliability_reconciliation_snapshot.sql` proves the same property against real Postgres using **separate `\connect` sessions** (not merely separate transactions) — session A records, a fresh session B reads back the exact values; a later record from a third session replaces the singleton row, read by a fourth; a negative input is clamped to zero, never stored negative or raising; direct table access is denied even to `bsa_app` |
| RT-06.9 | Go `-race` clean on any new shared metric state | `TestHistogramsAreRaceCleanUnderConcurrentObserveAndScrape` (payment-webhook-go) and `TestHistogramIsRaceCleanUnderConcurrentObserveAndScrape` (alert-worker-go): 50 concurrent goroutines each call `Observe` on both/the new histogram(s) and `WritePrometheus` concurrently; the full `go test -race ./...` run of both modules (see "Recorded local evidence") is clean including every pre-existing package |
| RT-06.SQL | Migration `0130` invariants | `packages/db/tests/rt06_reliability_reconciliation_snapshot.sql` (five cases, detailed in its own header comment): no row before the first run; cross-session read-your-write; wholesale replace on a later run (never a merge, never more than one row); a pathological negative input clamped to zero; direct table access denied to `bsa_app` even though it holds `EXECUTE` on both functions |

**Commands (from `bharatstudio-alerts`):**
`pnpm --filter @bharatstudio/alerts-api build` · `pnpm --filter @bharatstudio/alerts-api test` · `pnpm --filter @bharatstudio/alerts-web test` · `pnpm contracts:validate` · `pnpm db:test:all` · `pnpm db:test:l03` · `pnpm measurement:test` · `(cd services/alert-worker-go && go build ./... && go test -race ./... && go vet ./...)` · `(cd services/payment-webhook-go && go build ./... && go test -race ./... && go vet ./...)` · `git diff --check`

**Commands (from `bharatstudio-crons`):** `node --test tests/*.test.mjs` — unaffected by this task; re-run only to confirm the baseline is untouched (see "Referred to Opus" in the review record for why `schedules/v1.json` was not modified)

**Commands (from `bharatstudio-requirements`):** `python3 tools/doc_consistency.py` · `python3 tools/traceability.py`

**Security/data boundary:** no new personal-data field or retention rule. The four new budgeted histograms (`bsa_api_read_duration_ms`, `bsa_api_tip_order_duration_ms` in TS; `bsa_payment_tip_order_duration_ms`, `bsa_payment_webhook_ack_duration_ms` in `payment-webhook-go`; `bsa_worker_pump_duration_ms` in `alert-worker-go`) carry zero labels. The durable reconciliation snapshot (migration `0130`) persists only the same seven bounded L09 counts/timestamp the in-memory `ReconciliationSnapshot` already carried, reachable only through two `SECURITY DEFINER` functions granted to `bsa_app`, with direct table access denied and proven denied by `rt06_reliability_reconciliation_snapshot.sql` case 5.

**External evidence:** none claimed. No provider, staging, OBS, device, network or production evidence is asserted by this record. This task builds the instrument; it produces no readings (RT-06's own scope statement, restated in `active/tasks/RT-06.md`). A local histogram, a local `-race` run, or a local Postgres SQL suite is never cited here as evidence that any §19.4 budget number is met — that is RT-07, and RT-07 is `Blocked`. Cross-instance histogram aggregation via a real Prometheus/Cloud Monitoring backend (as opposed to the local additive-property proof, RT-06.4) is explicitly not claimed — see the review record's §3 for exactly what is proven locally and what requires a deployed environment.

## Recorded local evidence

- `pnpm --filter @bharatstudio/alerts-api build` — clean.
- `pnpm --filter @bharatstudio/alerts-api test` — **547 passed, 0 failed** (530 baseline + 17 new: 12 in `rt06-budget-histograms.test.ts`, 5 in `rt06-reconciliation-snapshot-store.test.ts`).
- `pnpm --filter @bharatstudio/alerts-web test` — **332 passed, 0 failed** (unchanged; this task touched no web code).
- `pnpm contracts:validate` — 40 fixtures + the v1 template catalogue contract, 68 OpenAPI paths/75 operation contracts, 3 negative cases — unchanged; this task touched no contract.
- `pnpm db:test:all` — **57 passed, 0 failed** (56 baseline + `rt06_reliability_reconciliation_snapshot`).
- `pnpm db:test:l03` — 23 SQL files plus the Go/TS integration legs, all passed; `rt06_reliability_reconciliation_snapshot.sql` included via the added `run_sql_test` line.
- `pnpm measurement:test` — **5 passed, 0 failed** (unchanged).
- `(cd services/payment-webhook-go && go build ./... && go test -race ./... && go vet ./...)` — build clean, **10 packages `ok`** under `-race`, vet clean.
- `(cd services/alert-worker-go && go build ./... && go test -race ./... && go vet ./...)` — build clean including `cmd/`, **10 packages `ok`** under `-race`, vet clean.
- `git diff --check` — clean.
- `(cd bharatstudio-crons && node --test tests/*.test.mjs)` — **2 passed, 0 failed**, unchanged (this repository was not modified by this task).

## Independent Opus verification — 2026-09-16

Changed files read directly; checks re-run rather than the report taken at face value.

- `pnpm --filter @bharatstudio/alerts-api test` — **547 passed, 0 failed** (baseline 530).
- `pnpm --filter @bharatstudio/alerts-web test` — **332 passed, 0 failed**.
- `pnpm db:test:all` — **57 passed, 0 failed** (baseline 56).
- `pnpm contracts:validate` — clean.
- Both Go services: `go build ./...` clean, **10 packages `ok`** each under `-race`, vet clean.
- `python3 tools/doc_consistency.py` — 17 checks, 0 errors, 0 warnings.

**The quantile estimator is honest, and better than the command asked for.** It is the
standard linear-interpolation-within-the-containing-bucket method, documented as an
*estimate* whose error is bounded by one bucket's width — and it draws the conclusion that
matters: **CI must check the boundary bucket's own cumulative count**, which is an exact
non-interpolated fact, rather than the interpolated quantile. That is why placing every
§19.4 number as an exact boundary is load-bearing rather than tidy. The `+Inf` case is
handled separately and labelled a lower bound rather than silently reported as an estimate.

**Measurement cannot affect behaviour (RT-06.6).** The durable snapshot read on the scrape
path and the persist on the reconcile path are both wrapped and non-fatal, logged through
`logSafeError`. A database failure degrades the metric, never the request.

**The borrowed measurement grid is labelled in the metric itself, not only in a record.**
Two paths §19.4 gives no duration number to — the webhook acknowledgement and the
dispatcher pump — are measured on buckets borrowed from a budgeted class. Each metric's
help text states in those words that no §19.4 row names that path with its own number. That
matters: a future reader seeing `le="500"` on the webhook acknowledgement must not conclude
500ms is its budget, because no authority states one. Verified present in both services.

### Finding the implementation surfaced, and it is a defect in the authority

**§19.0 RT-06 named the wrong reconciler.** Its defect text said "the reconciler schedule is
unwired". `payment-reconciliation` is a real, implemented schedule — but it targets
`payment-webhook-go`'s Razorpay provider-status recovery, which is a different thing. The
**L09 reliability reconciler** at `/internal/metrics/reconcile`, which is what this row is
actually about, has **no schedule pointing at it at all**. Nothing was unwired; a schedule
was never written. `FULL-PRODUCT-DEFINITION.md` §19.0 RT-06 now carries the correction.

The right call was made on it: `payment-reconciliation` was **left disabled** rather than
enabled to make a row look closed. A schedule pointing at the wrong reconciler would have
been worse than none.

### Why the row is P and not U

Two things named by the row are not closed. Cross-instance aggregation is proven only as
the additive merge property — never against a real scrape, which needs a deployed
environment. And the L09 reconciler still has no schedule. The instrument exists; two of
its stated properties do not.

**What this evidence is not.** **This task built the instrument and produced no readings.**
No §19.4 budget is claimed met by anything here. That is RT-07, and it is Blocked. Nothing
local is production, provider, store, legal, tax, staging, OBS, device, network, quota or
release evidence, and none of it is performance evidence (§35.1 rule 6).
