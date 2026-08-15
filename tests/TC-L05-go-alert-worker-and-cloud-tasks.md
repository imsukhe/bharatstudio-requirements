# L05 acceptance and test record — Go alert worker and Cloud Tasks

**Status:** `Implementation slices passing — live queue, overlay, capacity and fault-injection evidence remain open`  
**Task:** [`../tasks/L05-go-alert-worker-and-cloud-tasks.md`](../tasks/L05-go-alert-worker-and-cloud-tasks.md)  
**Repository:** `/Users/sukhdevsingh/Workspace/Bharat Studio/bharatstudio-alerts/services/alert-worker-go`

All local tests use synthetic IDs and fake stores/providers. No live Cloud Tasks queue, production database or OBS connection is used.

### Fresh L05 audit — 2026-08-15

Worker unit/race/vet checks, contract validation, the disposable L02/L03
PostgreSQL behavior harness, and the two-listener PostgreSQL wake-up integration
all pass. No new visual package was generated. This confirms the local worker
slice only; it does not close live Cloud Tasks, deployed IAM/OIDC,
cross-replica/OBS, capacity, dead-letter or staging gates.

### Deployment contract evidence — 2026-08-15

The v1 infrastructure contract and validator pass 8/8 in
`bharatstudio-infra`; they assert private worker ingress, OIDC-only task
routes, direct-listener separation and disabled Cloud Tasks placeholders. This
is not live Cloud Run/IAM/queue evidence.

| ID | Setup/action | Expected result | Evidence |
|---|---|---|---|
| L05-01 | Resolve two permitted queue bindings for one source | Both queues are returned independently; source correlation precedes priority | `internal/routing/*_test.go`; pass |
| L05-02 | Serialize and validate a delivery task command | Canonical UUID IDs, state version, attempt, trace, creation time and deadline are enforced; unknown/trailing JSON is rejected | `contracts/json-schema/cloud-task-command.schema.json`, `contracts/fixtures/cloud-task-command.json`, `internal/tasks/command_test.go`, `internal/tasks/contract_fixture_test.go`; `pnpm contracts:validate` and Go tests/vet/race pass |
| L05-03 | Enqueue the same command twice | Task name remains stable from delivery/version/attempt; provider AlreadyExists is idempotent success | `internal/tasks/enqueuer_test.go`; pass |
| L05-04 | Build a production Cloud Tasks request | POST body, JSON content type, target URL, queue parent, explicit canonical OIDC audience and OIDC service-account metadata are mapped by the official client adapter | `internal/tasks/google_cloud_tasks.go`, `internal/tasks/enqueuer_test.go`; compile/test pass; no live credentials |
| L05-05 | Claim, publish, release and wake a delivery | Claim is lease-protected; publication failure returns retryable response; successful publication releases the lease before the best-effort wake-up | `internal/handler/*_test.go`, `internal/store/*_test.go`; pass |
| L05-06 | Run duplicate/stale/retried task commands | Active lease prevents duplicate work; stale claim is safe no-op; retry path remains durable | handler/store tests and migration harness; pass |
| L05-07 | Run delivery lease SQL against disposable PostgreSQL 16 | Duplicate claim, retry reclaim, invalid transition, terminal no-reclaim and current queue-state guard checks pass | `pnpm db:test:l03`; pass through migration 0030 |
| L05-08 | Open the worker database with missing DSN or configured pgx pool | Missing DSN fails closed; configured pool pings before use and applies bounded settings | `internal/db/postgres_test.go`; pass without external database |
| L05-09 | Persist one captured payment into two permitted queue deliveries and advance only queue A | Queue A can complete while queue B remains ready and claimable; no global event state blocks either queue | Disposable PostgreSQL 16 harness; pass |
| L05-10 | Construct the durable replay publisher and worker process entrypoint | A claimed delivery wakes its channel after durable state exists; missing worker DB/audience configuration fails before serving; the process mounts only the private task routes, `/readyz` is DB-backed, and `/healthz` is liveness-only | `internal/handler/replay_publisher.go`, `cmd/alert-worker/main.go`, `internal/observability/readiness_test.go`; `go test ./...` and `go vet ./...` pass; deployment/IAM/probe evidence pending |
| L05-11 | Generate a worker delivery lease token at runtime and pass it to the UUID SQL boundary | The token is UUID v4-shaped and cannot fail only after deployment because a mock accepted plain hex | `internal/handler/cloud_tasks.go`; `go test ./...` pass |
| L05-12 | Submit a claim command with the correct delivery ID but mismatched event ID, outbox ID, attempt or state version, then submit the current command | The mismatched command returns no row and changes no lease/state; the current command still claims exactly once | `packages/db/tests/l03_application_behavior.sql` through `pnpm db:test:l03`; pass |
| L05-13 | Scan ready delivery rows and pump them into the task enqueuer | Each command carries delivery/event/outbox/attempt/version/trace identity; task names remain stable across scans; enqueue failure returns a retryable partial result and does not acknowledge a delivery | `internal/tasks/pump_test.go`, `internal/store/ready_delivery_store.go`, `0009_v1_l05_ready_delivery_listing.sql`; Go tests and `pnpm db:test:l03`; pass |
| L05-14 | Persist one payment into two queue deliveries, edit a binding after acceptance, then claim and replay both deliveries | Each delivery retains and projects its accepted source priority and override snapshot; later binding edits do not rewrite either delivery; both queues remain independently claimable | `0004`/`0007`/`0010`/`0020`, `l03_application_behavior.sql`; `pnpm db:test:l03`; pass after 0020 |
| L05-15 | Attempt a second payment delivery with a binding that has not opted into duplicate routing; also submit an explicitly multi-queue manual alert | Binding-backed duplicate is rejected atomically; explicit manual queue selection remains durable for each selected queue | `0021_v1_l03_duplicate_consent_guard.sql`, `l03_application_behavior.sql`; `pnpm db:test:l03`; pass |
| L05-20 | Call the private pump with missing authorization, a partial Cloud Tasks failure and a successful bounded scan | Unauthorized calls fail; partial enqueue is retryable and does not acknowledge/remove ready rows; successful scan returns a bounded summary and stable commands | `internal/handler/pump_test.go`, `internal/tasks/pump_test.go`; `go test ./...` and `go vet ./...`; pass; live IAM/queue evidence pending |
| L05-16 | Publish an overlay event, then make durable completion return no row/error | Handler returns retryable failure and calls the durable retry transition before the lease expires; the next scan can reclaim the delivery | `internal/handler/cloud_tasks_test.go`, `internal/store/delivery_store.go`, `0004_v1_l05_delivery_leases.sql`; `go test ./...`; pass; staging crash/retry evidence pending |
| L05-17 | Submit a valid command with an unsupported action | Validation rejects it before claim, publication or acknowledgement; the approved `deliver_overlay` action remains accepted | `internal/tasks/command_test.go`; `go test ./...`; pass |
| L05-18 | Run the production durable replay publisher for a claimed delivery | It performs no pre-release notification; the handler releases the durable lease and emits one best-effort wake-up afterward, so notification failure cannot create duplicate publication | `internal/handler/replay_publisher.go`, `internal/handler/replay_publisher_test.go`; `go test ./...`; pass |
| L05-19 | Complete one of two permitted queue deliveries, then complete the second | Global outbox projection remains pending while one delivery is active and becomes completed only when all delivery rows are terminal; per-queue claimability remains independent | `0015_v1_l05_outbox_projection_refresh.sql`, `l03_application_behavior.sql`; `pnpm db:test:l03`; pass |
| L05-21 | Pause a queue after a delivery exists, attempt ready-list/claim/replay, then resume it | The paused queue is absent from the ready list, cannot be claimed, and is absent from overlay replay; its durable delivery remains ready and is claimable/replayable after resume | `0023_v1_l05_queue_pause_dispatch_guard.sql`, `l03_application_behavior.sql`; `pnpm db:test:l03`; pass |
| L05-22 | Exercise the task enqueue failure, worker crash/timeout, dead-letter and overlay notification-outage recovery procedures | Recovery preserves the durable delivery, uses stable delivery/version/attempt identity, does not delete or silently acknowledge evidence, and records the required redacted operator evidence | `services/alert-worker-go/docs/CLOUD_TASKS_OPERATIONS.md`; procedure defined; live queue/staging rehearsal pending |
| L05-23 | Invoke the local pump with a non-positive batch limit | The pump fails closed before querying or enqueueing and cannot report a false-success empty scan | `services/alert-worker-go/internal/tasks/pump.go`, `internal/tasks/pump_test.go`; `go test ./...`; pass |
| L05-24 | Build the alert-worker container from its service boundary | A reproducible multi-stage build uses pinned base-image digests, excludes local environment files from its build context, produces a static Linux binary in a distroless non-root image, and embeds no credentials or deployment values | `services/alert-worker-go/Dockerfile`, `.dockerignore`; pinned `docker build --file Dockerfile --tag bsa-alert-worker:local .`, non-root image inspection and missing-config smoke pass locally; Cloud Run/IAM/Cloud Tasks/overlay evidence remains open |
| L05-25 | Claim and release a synthetic delivery through the real worker `database/sql` store | The SQL adapter returns the correct event/channel/queue/source-priority/JSONB override projection, releases the lease to `ready`, and rejects a stale command without changing state | `internal/store/sql_store_integration_test.go`; disposable PostgreSQL 16 harness with `integration` tag; pass |
| L05-26 | Replay a versioned delivery through the browser overlay in each approved presentation mode, exercise TTS failure and then fail the acknowledgement request | The overlay consumes the immutable accepted config snapshot, applies bounded bracket timing/character/placement/reduced-motion rules, supports FIFO/priority/stacked/pills/aggregated presentation, keeps priority within a contiguous visible frontier, falls back from unavailable audio to a non-blocking chime, and retains every item until acknowledgement succeeds; no presentation limit drops a durable delivery | `apps/web/app/overlay/overlay-policy.ts`, `apps/web/app/overlay/[overlayId]/page.tsx`, `packages/db/migrations/0029_v1_l05_overlay_config_snapshot.sql`; policy tests 6/6, web build and `pnpm db:test:l03`; local pass, provider/audio, live cross-replica and OBS evidence pending |
| L05-27 | Publish a delivery, leave the overlay offline, then run another ready-delivery pump scan | Successful worker release records `published_at`, leaves the delivery replayable/acknowledgeable, and excludes it from repeated ready-task enqueueing; a release failure leaves it unpublished and retryable | `0030_v1_l05_publication_marker.sql`, `l03_application_behavior.sql`; `pnpm db:test:l03`; local pass; live pump/offline-overlay evidence pending |
| L05-28 | Configure a source binding at one delivery per minute, claim two accepted deliveries concurrently, then advance the window | The first claim consumes the binding counter; the second is delay-only with `rate_limited`, future `next_action_at` and a fresh state version; after rollover it is claimable and completes; no delivery is dropped or acknowledged | `0032_v1_l32_source_rate_limit_and_publication_claim_guard.sql`, `l03_application_behavior.sql`; `pnpm db:test:l03`; pass |
| L05-29 | Submit a stale task after a worker release has set `published_at`; submit bounded bracket and rate-limit overrides through the API/overlay policy | The stale task returns no claim, the published delivery remains replayable, API rejects unknown/unbounded override keys, and the overlay applies only bounded fields to the amount-selected bracket without changing amount routing | `0032_v1_l32_source_rate_limit_and_publication_claim_guard.sql`, `apps/api/src/routes/channels.ts`, `contracts/openapi/v1.yaml`, `apps/web/app/overlay/overlay-policy.ts`; API, policy and SQL tests pass; staging proof pending |
| L05-30 | Run a synthetic 1,000-candidate ready-delivery burst, fail a deterministic subset of enqueue calls, then rerun with a healthy enqueuer | Every candidate produces a stable command in the healthy pass; partial failures return retryable status, do not acknowledge/remove candidates, and the later scan recovers all failed candidates | `internal/tasks/pump_burst_test.go`; `go test ./...`; local pass; this is not Cloud Tasks or production capacity evidence |

| L05-31 | Start overlay audio successfully, reject playback, and leave playback pending beyond the hard timeout | A successful audio start returns normally; provider/browser rejection or a stuck playback promise returns failure within the bounded 1.5-second policy and pauses the element; the caller can use the chime fallback without delaying visual rendering or durable acknowledgement | `apps/web/app/overlay/tts-runtime.ts`, `apps/web/app/overlay/tts-runtime.test.ts`, `apps/web/app/overlay/[overlayId]/page.tsx`; focused tests and web build pass; real provider/audio/OBS evidence remains pending |
| L05-32 | Commit a PostgreSQL notification from a separate publisher connection while two independent overlay wake-up listeners are active | Both direct listeners receive the committed wake-up without treating successful registration as disconnect; the worker/overlay correctness path remains durable replay, not notification delivery | `integration/overlay-wakeup.integration.ts`, `apps/api/src/db/overlay-wakeup.ts`, `packages/db/tests/run-l03-application-behavior.sh`; disposable PostgreSQL 16 harness; local two-listener pass; direct Neon and cross-replica staging evidence pending |
| L05-33 | Consume the committed runtime delivery fixtures with the Go worker contract types | Strict decoding rejects unknown fields; Cloud Tasks, multi-queue, per-queue delivery, overlay SSE and payment webhook fixtures preserve schema identity, UUID/date-time values, source/queue identity, override snapshots and independent queue status/priority | `internal/contracts/fixture_compatibility_test.go`; `go test ./internal/contracts ./internal/tasks ./internal/routing`, race and vet pass locally. This is Go compatibility evidence only; other-language consumer and independent review evidence remain pending |
| L05-34 | Call the private task and pump handlers with a non-POST method | Both endpoints return 405 with `Allow: POST` before authorization, claim or enqueue work | `internal/handler/cloud_tasks_test.go`, `internal/handler/pump_test.go`; `go test ./...`, race and vet pass locally |
| L05-35 | Let an already-open overlay stream encounter a transient durable replay failure after worker publication | The API closes the stream cleanly with a bounded comment; the browser reconnects using its last acknowledged cursor, and neither worker publication nor overlay acknowledgement is fabricated by the failure path | `apps/api/src/routes/overlay.ts`, `apps/api/test/app.test.ts`, `apps/web/app/overlay/[overlayId]/page.tsx`; API suite 54/54 and web build pass; deployed fault-injection/OBS evidence pending |
| L05-36 | Pump a bounded batch of ready deliveries through a delayed Cloud Tasks adapter with configured concurrency, then fail a subset and retry | Enqueues run concurrently but never above the configured bound; each command retains its stable delivery/version/attempt idempotency key; successful and failed rows remain independently recoverable, and a partial result is retryable rather than acknowledged | `services/alert-worker-go/internal/tasks/pump.go`, `pump_burst_test.go`, `cmd/alert-worker/main.go`; Go unit/race/vet pass; local 24-row concurrency/no-drop and 1,000-row partial-retry evidence pass; deployed Cloud Tasks quota/capacity evidence pending |

## Commands and result

```text
cd /Users/sukhdevsingh/Workspace/Bharat Studio/bharatstudio-alerts/services/alert-worker-go
gofmt -w internal/**/*.go
go test ./...
ok   .../internal/auth
ok   .../internal/handler
ok   .../internal/routing
ok   .../internal/store
ok   .../internal/tasks
L02_SECURITY_REMEDIATIONS=PASS
L03_APPLICATION_BEHAVIOR=PASS (including L05-12 claim identity binding, L05-14 routing snapshots, L05-28 delay-only rate limiting and L05-29 stale-publication claim protection)
```

## Not yet satisfied

Race-enabled local verification (`go test -race ./...`) passes for all worker packages; this is concurrency-safety evidence only and does not substitute for live Cloud Tasks, overlay, capacity or staging evidence.

- Live Cloud Tasks queue configuration, retry/dead-letter policy and private OIDC invocation evidence.
- Production PostgreSQL driver/configuration and deployed worker process wiring (local bootstrap now exists; deployment evidence remains open).
- Real overlay publication/reconnect/resync under cross-replica load.
- Capacity, FIFO/priority/hold/aggregate/stacked-display, TTS outage and crash-recovery proof.
- Live API/payment-to-pump invocation, Cloud Tasks queue configuration, task retry/dead-letter policy and private OIDC invocation evidence; local payment and worker adapters are wired and tested without deployed credentials.
- Independent fresh L05 review and staging shadow run.
- The operational procedure is now defined, but live dead-letter, replay, backlog alert and incident-rehearsal evidence is still pending.
- Per-source rate-limit and stale-publication claim guards are locally verified; live multi-replica contention, window timing and offline-overlay recovery remain staging gates.

### L05-33 — SQL ready-row adapter to task pump

**Result:** PASS (local synthetic integration evidence, 2026-08-15)

The disposable PostgreSQL runner exercises ReadyDeliveryStore.ListReady with
the task Pump. It verifies a ready delivery produces the expected
delivery/event/outbox/attempt/version/trace command and stable idempotency key.
An injected enqueue failure returns retryable partial status and the same
durable ready row remains visible for a later scan. The test does not mutate
delivery state during pumping.

**Command:** pnpm db:test:l03

**Not proven:** live Cloud Tasks queue behavior, provider retry/dead-letter
execution, deployed OIDC/IAM, capacity or staging recovery.

### Full local boundary rerun — 2026-08-15

`go test -race ./...` passed for the worker. `pnpm db:test:l03` passed the
disposable L02/L03/L04/L05 chain, including worker SQL integration, two-listener
wake-up, per-queue independent progress, replay/acknowledgement and
delay-only rate limiting. The API suite passed 54/54, the API/web production
build passed, and contract validation passed all 11 fixture mappings and 32
OpenAPI paths. Mobile passed 19/19 with lint/typecheck, and macOS passed 7/7.
No BSA visual package was generated or modified. Live Cloud Tasks, deployed
OIDC/IAM, capacity/fault/recovery, OBS/staging and independent review remain
open.

### Automatic continuation rerun — 2026-08-15

`go test ./...`, `go test -race ./...` and `go vet ./...` passed for the worker.
`pnpm db:test:l03` passed the disposable L02–L05 chain, including the worker
SQL adapter, two-listener wake-up and shared-PostgreSQL cross-replica replay.
No BSA visual package was generated or modified. Live Cloud Tasks, deployed
OIDC/IAM, capacity/fault/recovery, OBS/staging and independent review remain
open.
