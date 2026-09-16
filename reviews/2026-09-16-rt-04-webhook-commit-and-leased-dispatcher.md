# RT-04 — the webhook does one atomic commit then acknowledges: decision record

**Task:** `../active/tasks/RT-04.md`
**Reviewer:** Sukhdev Singh (owner self-review; independent reviewer unavailable)
**Scope:** The payment webhook's post-commit acknowledgement path becomes fire-and-forget dispatch (RT-04); the outbox dispatcher gains a single-row mutual-exclusion lease so concurrent dispatch runs never both scan and enqueue the same backlog (RT-05); the `outbox-recovery` cron schedule the dispatcher depends on is enabled (RT-08).

## 1. Product/market/provider review (§2 of the operator's command)

Bounded, official-documentation-only research into Razorpay's documented webhook retry/acknowledgement behaviour (the load-bearing question: is returning 2xx before dispatch correct provider behaviour), Stripe/PayPal's comparable commit-then-acknowledge pattern, and Google Cloud Tasks/Scheduler's at-least-once/deduplication guarantees. Sources and access dates below.

### Razorpay — the load-bearing finding

- **[Webhooks | Best Practices | Razorpay Docs](https://razorpay.com/docs/webhooks/best-practices/)** — accessed 2026-09-16. Quoted directly: *"Please make sure the API responds with 2xx when you successfully consume the event at your end."* A **5-second acknowledgement window** is documented: *"your server accepts the event but fails to respond in 5 seconds. In such cases, the session is marked timeout."* **Every non-2xx response or timeout is a delivery failure**: *"Every event that receives a non-2xx response is considered an event delivery failure by Razorpay's system."* Retries follow **exponential backoff for 24 hours after the event's creation timestamp**, and *"if the webhooks continue to fail for 24 hours, the webhook is disabled"* — a materially worse failure mode than a single delayed alert, since a disabled webhook stops *every* future payment notification until an operator manually re-enables it from the Dashboard.
- **[Webhooks | Razorpay Docs](https://razorpay.com/docs/webhooks/)** — accessed 2026-09-16. General webhook concepts only; no retry/acknowledgement detail (confirmed by direct fetch, not inferred).
- **[Webhooks | Validate & Test | Razorpay Docs](https://razorpay.com/docs/webhooks/validate-test/)** — accessed 2026-09-16. Confirms `x-razorpay-signature` verification and the `x-razorpay-event-id` dedup header (both already implemented, unchanged by this task) and documents out-of-order delivery as an expected condition webhook consumers must tolerate — consistent with this codebase's existing append-only, event-ID-deduplicated design.

**This settles the question the operator's command asked first.** Razorpay's own documented contract is a **5-second, 2xx-or-it's-a-failure** acknowledgement window, with the *worst* consequence of repeated failure being the webhook disabled outright. The pre-RT-04 code held the HTTP response open through a same-request call to the alert-worker's pump with its own 5-second timeout (`WorkerPumpClient`'s `defaultWorkerPumpTimeout`) — meaning, under a slow-but-not-failed dispatch, the webhook's *total* response time could approach or exceed Razorpay's 5-second window purely from database-commit time plus dispatch time stacked serially, with dispatch time being the larger and less predictable of the two. Returning 2xx immediately after the durable commit and deferring dispatch entirely removes dispatch latency from the number Razorpay is timing. **This is not an inference about what Razorpay prefers — it is the documented mechanics of the deadline this design was, and now is not, spending on the wrong work.**

### Stripe — direct comparator for the commit-then-acknowledge pattern

- **[Receive Stripe events in your webhook endpoint](https://docs.stripe.com/webhooks)** — accessed 2026-09-16. Quoted directly, under "Quickly return a 2xx response": *"Your endpoint must quickly return a successful status code (2xx) before any complex logic that could cause a timeout. For example, you must return a 200 response before updating a customer's invoice as paid in your accounting system."* Under "Handle events asynchronously": *"Configure your handler to process incoming events with an asynchronous queue... Asynchronous queues allow you to process the concurrent events at a rate your system can support."* Under "Automatic retries": *"Stripe attempts to deliver events to your destination for up to three days with an exponential backoff in live mode"* — and a **Timed-out** response is explicitly listed as a failure class requiring the same fix: *"Make sure you defer complex logic and return a successful response immediately in your webhook handling code."* Duplicate handling is by event ID, the same mechanism this codebase already uses: *"You can guard against duplicated event receipts by logging the event IDs you've processed."*

Stripe's own stated design is structurally identical to RT-04's target shape: acknowledge fast, queue the work, dedupe by event ID. This is independent, named-provider confirmation that "commit, then 2xx, then dispatch asynchronously" is the documented pattern for this exact class of integration — not an invention specific to this codebase.

### PayPal — not independently fetched this session

No PayPal webhook documentation was fetched this session (time-bounded review; Razorpay and Stripe alone already answer the operator's specific question with named, quoted, official text, and PayPal is not this codebase's payment provider). Recorded as a gap, not fabricated: this record does not claim any PayPal-specific finding.

### Google Cloud Tasks and Cloud Scheduler — the dispatcher's own foundation

- **[Cloud Tasks docs](https://docs.cloud.google.com/tasks/docs/dual-overview)** — accessed 2026-09-16. At-least-once delivery is documented, not exactly-once: *"if a task is successfully added, the queue will deliver it at least once,"* with the explicit caveat that *"multiple executions are possible in rare circumstances, requiring handlers to be idempotent."* Deduplication is by task name: *"If you attempt to create a task with a name that already exists in the queue, the creation request will fail,"* and this protection is time-bounded — *"Cloud Tasks remembers task names for up to 24 hours after the task has been deleted from the queue."* This is the exact mechanism RT-05's own defect description already named ("only deterministic Cloud Task names save correctness today") and confirms it is a real, documented, but time-bounded guarantee — not an assumption.
- **[Cloud Scheduler docs](https://docs.cloud.google.com/scheduler/docs/overview)** — accessed 2026-09-16. Also at-least-once, with the same rare-duplicate caveat: *"in some rare circumstances, it is possible for a job to run multiple times in association with a single instance of the schedule."* Retries use *"exponential backoff according to its configured retry policy"* (matching `outbox-recovery`'s own `retry.maxBackoffSeconds: 120`, unchanged by this task). Deduplication assistance is available via *"its name and the `X-CloudScheduler-ScheduleTime` header"*, and the documentation places the idempotency burden on the target explicitly: *"your code must ensure that there are no harmful side-effects of repeated execution."*

**This directly supports the RT-04/RT-05 design as specified, not merely as convenient.** Neither Cloud Tasks nor Cloud Scheduler promises exactly-once execution — both explicitly require the target to be idempotent against rare duplicate invocations. That is precisely why RT-05's dispatch lease exists at the *dispatcher* level (coordinating concurrent scans) rather than being treated as a substitute for the *delivery-level* idempotency that `claim_event_delivery`'s optimistic-concurrency check and Cloud Tasks' deterministic task naming already provide independently. The lease reduces redundant work; it is not, and was never claimed to be, the thing that makes duplicate delivery safe — that guarantee already existed and is untouched by this task.

### Creator-facing impact and comparator latency framing

The operator's command also asked what a creator sees if a wake-up is missed and recovery waits for the next scheduled tick, and how comparable products describe tip/alert latency.

- **What a creator/supporter sees on a missed wake-up:** nothing wrong, only slightly delayed. The payment is captured and durable (unchanged — RT-04 does not touch the commit). The alert's visual/audio delivery waits for the next `outbox-recovery` tick (every two minutes) instead of the sub-second wake-up path. No payment is lost, refunded, or double-charged; no duplicate alert fires (Cloud Tasks' deterministic naming plus `claim_event_delivery`'s optimistic concurrency, both unchanged, still govern that). This is explicitly **not** described as "no latency impact" anywhere in this record or the task record, per the operator's own instruction.
- **Comparator latency framing:** Stripe and Razorpay's own documentation, read above, describes webhook **acknowledgement** latency budgets (their side, 5s/best-effort), not **end-customer-visible** alert-latency SLAs — neither provider publishes a number for "how fast does the thing the payment triggered visibly happen," because that is downstream application behaviour, not a payment-webhook contract. No comparator was found (this session) that publishes a "tip-to-alert" latency figure to benchmark against, so none is asserted here. This absence is the honest finding, not a gap papered over with an invented number.

**Referred to Opus:** none. The research produced no finding requiring a product, pricing, legal, provider or scope decision beyond what `FULL-PRODUCT-DEFINITION.md` §19.0's RT-04/RT-05/RT-08 rows and the operator's command already specify and this task already implements.

**Independent review availability:** unavailable, same as RT-01/RT-02/RT-03. This is self-review by the implementing owner; no second reviewer inspected the worktree, diff, or evidence in this record.

## 2. Design decisions this command did not settle

See `active/tasks/RT-04.md`'s "Design decisions" section — reproduced here for the record's completeness rather than duplicated in full:

1. The dispatch lease is a **new single-row control table** (`app_private.outbox_dispatch_lease`, migration `0129`), not a second write to the per-delivery `event_outbox_deliveries.lease_token`/`lease_until` that `claim_event_delivery` already owns. Reusing that exact field at scan time would make the *real* per-delivery claim (fired by the enqueued Cloud Task, normally within milliseconds) wait out the *scan* lease's full TTL on every normal delivery — trading a rare, already-harmless-by-naming double-scan for a latency regression on the common path. The single coarser lease gives RT-05's safety property without that regression, using the identical acquire-if-unheld-or-expired discipline at a coarser grain.
2. Lease TTL (60s) and scan batch size (unchanged, still capped at 500 inside `list_ready_event_deliveries`) are both pre-existing numbers — the `outbox-recovery` schedule's own `timeoutSeconds` and 0063's existing cap — per the operator's explicit instruction to invent no new number.
3. The wake-up call's shape (an HTTP POST to `/internal/v1/tasks/pump`) is unchanged; only its position relative to the response changed. A narrower, per-delivery-targeted wake-up was considered and not built — flagged as a candidate follow-up, not implemented.
4. **RT-05 and RT-08's own `register-map.tsv`/`semantic-mapping-audit.md` rows are intentionally left `new-record-required`, unchanged.** `tools/traceability.py` requires an `active-record` lifecycle row's task-file stem to equal the requirement ID exactly, so pointing RT-05/RT-08 at `RT-04.md` while marking them `active-record` would fail validation outright, and fabricating `RT-05.md`/`RT-08.md` files whose entire content restates this same change would violate `governance/AGENTS.md`'s "do not create duplicate documents" rule. Only `RT-04`'s row moved. This is a traceability-tooling constraint, not a claim that RT-05/RT-08 are unaddressed — the "Boundaries" section of `active/tasks/RT-04.md` and this review both name exactly which files serve which of the three IDs.

## 3. What was implemented, mapped to RT-04/RT-05/RT-08

| Change | Serves |
|---|---|
| `handler.go`'s `ServeHTTP` returns its 2xx immediately after `Store.PersistVerified` succeeds; the old comment justifying "must remain retryable on a failed wake-up" is replaced with the RT-04 reasoning | RT-04 |
| `Handler.wakeUpDispatcher` — fire-and-forget goroutine, `context.Background()`-derived (survives the request context), bounded by `WorkerPumpClient`'s existing 5s timeout, logged/counted via `ObserveWakeupOutcome`/`Logger.Event("webhook_wakeup", ...)` on failure, never touches the response | RT-04 |
| `packages/db/migrations/0129...sql` — `app_private.outbox_dispatch_lease`, `acquire_outbox_dispatch_lease`, `release_outbox_dispatch_lease` | RT-05 |
| `tasks.Pump`'s optional `DispatchLeaser`/`LeaseDuration`/`NewLeaseToken`, wired in `cmd/alert-worker/main.go` for the real SQL-backed lease store | RT-05 |
| `handler/pump.go`'s `Skipped` outcome (200, `outcome="skipped"`, no enqueue attempt) when another run holds the lease | RT-05 |
| `bharatstudio-crons/schedules/v1.json`'s `outbox-recovery.enabled: true`, and the rewritten contract test plus the new "RT-08" section of `docs/SCHEDULER_OPERATIONS.md` | RT-08 |

## 4. Disposition

**Disposition:** `Conditionally complete — local evidence; independent review unavailable`
**Owner:** Sukhdev Singh
**Follow-up/release gate:** An independent reviewer must inspect the actual worktree diff against this record before any state change beyond `Conditionally complete`. No external (staging, OBS, device, network, provider) evidence is claimed; enabling `outbox-recovery` in `schedules/v1.json` is a repository-level code change, not deployment or IAM/OIDC evidence, per `bharatstudio-crons/docs/SCHEDULER_OPERATIONS.md`'s new "RT-08" section. The `FULL-PRODUCT-DEFINITION.md` §31.18.0 state letters for RT-04, RT-05 and RT-08 are left at `X` for Opus to set after audit, per the operator's explicit instruction — this task changed no register state letter.
**Decision lifecycle:** `Approved → Implemented → Verified` (conditionally complete pending independent review)
