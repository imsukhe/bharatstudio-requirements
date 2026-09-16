# TC-RT-04 — the webhook does one atomic commit then acknowledges

**Task:** `../active/tasks/RT-04.md`
**Owner:** Sukhdev Singh
**Status:** `Conditionally complete — local verification passed; external release evidence not applicable`

| Case | Control | Expected evidence |
|---|---|---|
| RT-04.1 | A slow or failing dispatch cannot change the webhook's status code | `services/payment-webhook-go/internal/ingress/handler.go`'s `ServeHTTP` writes the 2xx response immediately after `Store.PersistVerified` succeeds and calls `wakeUpDispatcher` without waiting on it. `TestHandlerAcknowledgesEvenWhenDeliveryWakeupFails`, `TestWebhookToWorkerPumpHTTPFailureStillAcknowledgesTheCommit`, `TestPaymentHandlerAcknowledgesEvenWhenWorkerBoundaryFails` each assert `200`/`{"status":"accepted"}` while the configured pumper/worker fails |
| RT-04.2 | A commit failure still returns 503 and is still retried by the provider | `TestHandlerRequestsProviderRetryWhenStoreFails` (unchanged) |
| RT-04.3 | The wake-up is never awaited on the acknowledgement path — assert ordering, not wall-clock | `TestWakeupIsNeverAwaitedOnTheAcknowledgementPath`: a `blockingPumper` that never returns proves `ServeHTTP` already returned its `200` response while `Pump` is still provably blocked, then confirms the wake-up was in fact attempted (not skipped) before releasing it |
| RT-04.4 | A dispatch that fails is logged and counted, and the accepted event remains durable and still dispatchable | `TestHandlerAcknowledgesEvenWhenDeliveryWakeupFails` asserts `bsa_payment_business_total{kind="wakeup",outcome="failed"} 1` and a `"component":"webhook_wakeup"`/`"outcome":"failed"` log line, alongside the unchanged `store.calls == 1` (the commit, and therefore the delivery, is untouched by the wake-up's own failure) |
| RT-04.5 | Dedup, quarantine, invalid-payload and duplicate outcomes are all unchanged | `TestHandlerRejectsPermanentlyInvalidVerifiedPayloadWithoutWakingWorker`, `TestHandlerAcknowledgesDurableQuarantineWithoutWakingWorker`, `TestHandlerReturnsDuplicateAfterDurableDeduplication`, `TestHandlerAcknowledgesRepeatedDeliveryRegardlessOfEitherWakeupOutcome` (unchanged pre-commit outcomes; the duplicate outcome now also survives a wake-up failure on either call) |
| RT-04.6 | A missed wake-up is recovered by the scheduled dispatcher, and the event is delivered exactly once — not duplicated by the recovery | Architectural, proven by composition rather than one new end-to-end test: (a) `TestHandlerAcknowledgesEvenWhenDeliveryWakeupFails` proves a failed wake-up leaves the delivery durable and unaffected; (b) the pre-existing `packages/db/tests` outbox/claim tests and `TestSQLDeliveryStoreClaimReleaseAgainstPostgres` prove a durable, unclaimed delivery is exactly what a later pump scan (the schedule) picks up; (c) `bharatstudio-crons`'s `outbox-recovery` schedule (now enabled) targets the same idempotent `/internal/v1/tasks/pump` endpoint the wake-up already calls, with Cloud Tasks' own deterministic task naming (unchanged, pre-existing) preventing a duplicate enqueue of the same delivery+attempt+version. No live Cloud Scheduler/Cloud Tasks run is claimed as evidence here — see "External evidence" below |
| RT-04.7 | Two concurrent dispatcher runs do not enqueue the same delivery twice (leasing) | `TestConcurrentDispatchRunsDoNotBothScanAndEnqueue` (in-memory fake leaser mirroring migration `0129`'s semantics) and `rt04_outbox_dispatch_lease.sql` case 2 (a second token cannot acquire while the first lease is active) |
| RT-04.8 | A dispatcher that dies mid-scan releases its lease and the work is picked up on a later tick | `TestExpiredLeaseFromACrashedRunIsPickedUpLater` and `rt04_outbox_dispatch_lease.sql` case 5 (an expired lease, simulating a crashed holder that never reached its release, is acquirable by a new run) |
| RT-04.9 | No request handler scans the backlog any more (RT-05) | `TestPumpHandlerSkipsCleanlyWhenAnotherDispatchRunHoldsTheLease`: the pump handler's own `Enqueuer` is never called when another run holds the lease — the same pump/dispatch code path (whether invoked by the webhook's wake-up or the scheduled tick) is the only scanner, and it is now lease-coordinated rather than unconditionally scanning on every invocation |
| RT-04.10 | Go `-race` clean, including the fire-and-forget path under a burst, with no goroutine leak per webhook | `TestBurstOfWebhooksDoesNotLeakWakeupGoroutines` (200 concurrent webhooks; `runtime.NumGoroutine()` returns to baseline once every wake-up completes) and the full `-race` run of both Go modules (see "Recorded local evidence") |
| RT-04.11 | `bharatstudio-crons`: `outbox-recovery` is enabled, still validates against the schedule contract, and the other five schedules are untouched | `tests/schedule-contract.test.mjs`'s rewritten first test: `outbox-recovery.enabled === true`, every other schedule `=== false`, and every existing per-schedule contract assertion (target, audience, idempotency key, timeout bounds, monitoring/dead-letter signal naming) still runs unconditionally over every schedule including `outbox-recovery` |
| RT-04.SQL | Dispatch-lease invariants | `packages/db/tests/rt04_outbox_dispatch_lease.sql`: unheld lease acquires; a second token cannot acquire while held; releasing with the wrong token is a no-op and does not release the real holder's lease; releasing with the correct token clears it and a new acquire immediately succeeds; an expired lease is acquirable without any release; direct table access is denied to `bsa_alert_worker` even though it holds `EXECUTE` on both functions |

**Commands (from `bharatstudio-alerts`):**
`pnpm --filter @bharatstudio/alerts-api build` · `pnpm --filter @bharatstudio/alerts-api test` · `pnpm --filter @bharatstudio/alerts-web test` · `pnpm contracts:validate` · `pnpm db:test:all` · `pnpm db:test:l03` · `pnpm measurement:test` · `(cd services/alert-worker-go && go build ./... && go test -race ./... && go vet ./...)` · `(cd services/payment-webhook-go && go build ./... && go test -race ./... && go vet ./...)` · `git diff --check`

**Commands (from `bharatstudio-crons`):** `npm test` (`node --test tests/*.test.mjs`); `schedules/v1.json` validated by hand against `contracts/schedule-contract.json`'s field-level rules (no `additionalProperties`, enum/pattern constraints) since no local JSON-Schema validator binary is available in this environment — `node --test` re-derives and checks every field the contract requires directly.

**Commands (from `bharatstudio-requirements`):** `python3 tools/doc_consistency.py` · `python3 tools/traceability.py`

**Security/data boundary:** no new personal-data field or retention rule. The two new bounded outcome counters (`kind="wakeup"` on the webhook, outcome `skipped` added to the existing `kind="pump"` on the worker) carry no payment identifier, provider event ID, account reference or amount — only the fixed outcome tokens listed in `services/payment-webhook-go/internal/observability/metrics.go`'s `ObserveWakeupOutcome` and `services/alert-worker-go/internal/observability/metrics.go`'s `ObservePumpOutcome`. `Logger.Event("webhook_wakeup", ...)` uses the existing bounded `component`/`outcome`/`trace_id` shape, same as every other call site.

**External evidence:** none claimed. No provider, staging, OBS, device, network or production evidence is asserted by this record. Enabling `outbox-recovery` in `schedules/v1.json` is a repository-level code change, not a deployment, and is not evidence that the Cloud Scheduler job, its OIDC binding, or the private `/internal/v1/tasks/pump` endpoint behave as this document assumes in a real environment — that remains open in `05_SUPPORT_AND_EXTERNAL_EVIDENCE_REGISTER.md`. No "lag-free"/"fast"/"smooth" claim is made anywhere in this record or the task record (§19.0's claim ban stands until RT-01..RT-07 all close).

## Independent Opus verification — 2026-09-16

Changed files read directly; checks re-run rather than the implementation report taken at
face value. This is the payment path, so the audit was aimed at what could lose money.

- `pnpm --filter @bharatstudio/alerts-api test` — **530 passed, 0 failed**.
- `(cd services/payment-webhook-go && go build ./... && go test -race ./...)` — build clean,
  **10 packages `ok`** under `-race`.
- `(cd services/alert-worker-go && go build ./... && go test -race ./... && go vet ./...)` —
  build clean including `cmd/`, **10 packages `ok`**, vet clean.
- `bharatstudio-crons` — exactly one schedule flipped: `outbox-recovery` true; the other
  five (`payment-reconciliation`, `refund-reconciliation`, `overlay-session-maintenance`,
  `event-archive-maintenance`, `audit-archive-maintenance`) remain false, as scoped.

**Every pre-commit guarantee survives.** The `invalid`, `quarantined` and commit-failure
paths are untouched above the change, and **RT-04.2 still asserts a commit failure returns
503 with `Retry-After: 5`** (`handler_test.go:516`). Only post-commit dispatch stopped being
able to fail the provider. The superseded reasoning was replaced in the comment rather than
left standing beside contradicting code.

**The fire-and-forget wake-up deliberately does not derive from `request.Context()`** — that
context is cancelled when `ServeHTTP` returns, which would cancel the very work that is
meant to outlive the request. It is bounded instead by `WorkerPumpClient`'s own timeout, and
guarded against a nil `Pumper`.

**The lease is correct under concurrency.** `acquire_outbox_dispatch_lease` is a single
atomic `UPDATE ... WHERE (lease_until is null or lease_until <= current_timestamp)` with the
guard inside the statement, so two concurrent acquires serialise on the row and the loser's
predicate re-evaluates false. Release matches on `lease_token`, so a run that already lost
its expired lease to a later holder cannot release someone else's.

**The choice not to reuse `event_outbox_deliveries.lease_token` is right and non-obvious.**
That pair means "this delivery is claimed for processing" and is set at Cloud-Task-fire
time. Reusing it as a scan lease would block the real claim for the scan lease's TTL on
every normal delivery — trading a dispatch bug for a latency bug. A separate coarse
single-row lease gives the same mutual exclusion without that.

**No new number was introduced.** The 60s lease TTL is the `outbox-recovery` schedule's own
`timeoutSeconds`; the 500 scan cap is `list_ready_event_deliveries`'s existing limit.

### Finding — recorded, NOT fixed, and deliberately not fixed here

**The post-commit wake-up spawns one goroutine per webhook with no coalescing.** Each lives
up to the pump client's timeout, so a burst produces roughly (webhooks/sec × timeout)
concurrent outbound calls into `alert-worker`. The lease means all but one return `skipped`
cheaply, but each still consumes an `alert-worker` request slot and one database round trip
— which is the same class of self-inflicted pressure RT-05 names, at smaller scale.

The fix is understood: coalesce to at most one in-flight wake-up plus one pending, so a
wake-up still always *starts after* every commit (dropping instead of queueing would let an
event committed mid-scan wait for the scheduled tick). It is not done here for two reasons,
both deliberate. It requires restructuring `ingress.Handler` from a plain struct literal to
a constructor holding shared state, which is new concurrency in the money path; and the
threshold at which it matters is a **load** property that cannot be measured locally —
ENV-08 and RT-07 are the rows that would measure it, and both are Blocked. Adding untested
concurrency to the payment service on an unmeasurable projection is the wrong trade. Raised
to the owner as a follow-up rather than performed.

**What this evidence is not.** All local. **Enabling a schedule in a JSON file is not
deploying it**, and nothing here is evidence that Razorpay behaves as its documentation
says. No production, provider, store, legal, tax, staging, OBS, device, network, quota or
release readiness is claimed, and none of it is performance evidence (§35.1 rule 6).
