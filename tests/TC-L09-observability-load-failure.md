# L09 acceptance and test record — observability, load, failure and recovery

**Status:** `Local instrumentation/regression slices passing — final topology and staging proof pending`
**Task:** [`../tasks/L09-observability-load-failure.md`](../tasks/L09-observability-load-failure.md)
**Repository:** `/Users/sukhdevsingh/Workspace/Bharat Studio/bharatstudio-alerts`

| ID | Setup/action | Expected result | Evidence |
|---|---|---|---|
| L09-01 | Request `/internal/metrics` without service identity | The endpoint returns 401 and no metrics payload | `apps/api/test/app.test.ts`; pass |
| L09-02 | Request a health route with a query containing a synthetic user identifier, then scrape metrics with service identity | Metrics use the normalized route template and method/status labels; query strings, request IDs, authorization values and payment data are absent | `apps/api/src/observability/metrics.ts`, `apps/api/test/app.test.ts`; 54 API tests/build pass |
| L09-02a | Scrape payment and alert-worker metrics without identity, then with a synthetic authorized identity after requests containing UUID path segments and query strings | Unauthenticated scrapes return 401; authorized output contains only normalized route/method/status/duration metrics with UUIDs and query strings removed | `services/payment-webhook-go/internal/observability/*`, `services/alert-worker-go/internal/observability/*`; `go test ./...` and `go vet ./...`; pass |
| L09-02b | Accept a verified payment webhook and inspect the private worker-pump request | A bounded server-derived trace ID crosses the internal hop; client-provided trace values are not trusted or emitted | `services/payment-webhook-go/internal/ingress/trace.go`, `worker_pump.go`, ingress tests; `go test ./...`; pass |
| L09-02c | Record a payment checkout request with a query string and scrape metrics | The real `/internal/v1/tips/orders` route remains a bounded actionable label while query data is removed | `services/payment-webhook-go/internal/observability/metrics.go`, `metrics_test.go`; `go test ./...`; pass |
| L09-02d | Record accepted, ignored, invalid, retryable and partial worker outcomes, including an unrecognized synthetic outcome | Authenticated metrics expose only allowlisted task/pump outcome labels; identifiers and unknown labels are not emitted | `services/alert-worker-go/internal/observability/metrics.go`, `metrics_test.go`, `handler/*.go`; `go test ./...` and `go vet ./...`; pass |
| L09-02e | Exercise accepted, duplicate, invalid and retryable payment webhook outcomes, including an unrecognized synthetic outcome | Authenticated metrics expose only fixed webhook outcome labels; provider event IDs, order IDs, account references and payload values are not emitted | `services/payment-webhook-go/internal/observability/metrics.go`, `metrics_test.go`, `internal/ingress/handler.go`; `go test ./...` and `go vet ./...`; pass |
| L09-02f | Record checkout and payment/refund reconciliation outcomes, including an unrecognized synthetic kind/outcome | Authenticated metrics expose only fixed kinds/outcomes for checkout and reconciliation; unknown values collapse to bounded categories | `services/payment-webhook-go/internal/checkout/handler.go`, `internal/reconcile/*handler.go`, `internal/observability/metrics.go`, `metrics_test.go`; `go test ./...` and `go vet ./...`; pass |
| L09-02g | Persist a verified synthetic Razorpay webhook, project it to two queue deliveries, enqueue a worker command, and replay through the overlay projection | The server-derived `razorpay:<provider-event-id>` value is preserved across payment persistence, both independent delivery rows, and overlay replay; malformed/unbounded worker trace values are rejected and valid command JSON round-trips unchanged | `docs/architecture/OBSERVABILITY_TRACE_CONTRACT.md`, `services/alert-worker-go/internal/tasks/command_test.go`, `packages/db/tests/l03_application_behavior.sql`; local Go tests and disposable PostgreSQL L03 harness; pass |
| L09-02h | Emit payment/worker boundary events with a valid and an invalid synthetic trace | JSON records contain only bounded component/outcome/time and a valid trace; invalid/control-character traces and arbitrary payload-like tokens are omitted or collapsed | `services/payment-webhook-go/internal/observability/structured_log_test.go`, `services/alert-worker-go/internal/observability/structured_log_test.go`, wired ingress/task handlers; `go test ./...`, `go vet ./...`, `go test -race ./...`; pass |
| L09-02i | Build the current payment and alert-worker service boundaries from their Dockerfiles | Both produce static Linux binaries in non-root distroless runtime images without embedded credentials | `services/payment-webhook-go/Dockerfile`, `services/alert-worker-go/Dockerfile`; `docker build --file Dockerfile --tag bsa-payment-webhook:local .` and `docker build --file Dockerfile --tag bsa-alert-worker:local .`; pass locally |
| L09-02j | Exercise the API safe-error logger with an error containing synthetic donor text, SQL text and a stack, and audit all API error-log call sites | Logs contain only bounded event/trace/error-category fields; provider/database/user-controlled messages, stacks and arbitrary error objects are absent | `apps/api/src/observability/safe-log.ts`, `apps/api/test/safe-log.test.ts`; API suite 54/54 and `rg` source audit; pass locally |
| L09-02k | Commit an overlay delivery through one SQL/API replica, replay and acknowledge it through a second replica, and include an unrelated channel delivery in the same database | Shared durable state is visible across replicas, acknowledgement is observed by the first replica, and the session-channel predicate prevents cross-channel replay | `integration/overlay-cross-replica.integration.ts`, `packages/db/migrations/0054_v1_l03_overlay_event_channel_guard.sql`; disposable PostgreSQL harness; pass locally; Neon/Cloud Run/OBS staging evidence pending |
| L09-03 | Run the final API/payment/worker topology in staging and scrape all declared service metrics | All critical lanes expose actionable counters and latency/error signals with trace correlation | Not run; staging topology and target declarations pending |
| L09-04 | Run cross-replica, duplicate webhook, task retry, provider outage, SSE reconnect and database failure scenarios | Durable evidence reconciles without payment duplication or alert loss; each failure has an owner/runbook | Not run; L04/L05/L07/L08 dependencies pending |
| L09-05 | Inspect the disabled infrastructure observability contract | Private metrics targets, dashboard categories, alert owners/actions and forbidden identifier/payload labels are declared; thresholds remain explicit deployment inputs and no monitoring resource is enabled by the template | `bharatstudio-infra/deployment/v1/observability.template.json`, `manifest.template.json`, infrastructure contract test; local pass; deployed scrape/dashboard/alert rehearsal pending |

### Local rerun evidence — 2026-08-15

The API 54-test suite/build, contracts, disposable PostgreSQL security and
application harness, payment/worker `go test`, `go vet` and race checks, cron
contract, mobile checks and macOS Swift tests passed. No staging target or
capacity number is inferred from this rerun; L09-03 and L09-04 still require
the final deployed topology and fault-injection evidence.

## Not yet satisfied

- Deployed cross-service trace propagation, structured-log sink controls/retention and collection; local trace and logger contracts are covered by L09-02g/L09-02h.
- Dashboards, actionable alert policies, runbooks and owners.
- Declared staging targets and measured capacity/load results.
- Fault injection, backup/restore, rollback and incident communication rehearsal.

### Fresh local audit evidence — 2026-08-15

The local L09 instrumentation and durability evidence was rechecked against the
acceptance criteria. No additional local failure was found. The existing
regression evidence remains valid: API 54/54 and build, contracts, disposable
PostgreSQL L02/L03 including cross-replica overlay replay, payment/worker Go
tests/vet/race, cron/infra contracts, mobile checks and macOS Swift tests.

These results do not establish capacity or production monitoring. L09-03 and
L09-04 remain pending until the final deployed topology is available for
metrics scrape, target load, timeout/retry/provider outage, SSE reconnect,
database failure, backup/restore and rollback rehearsal.
