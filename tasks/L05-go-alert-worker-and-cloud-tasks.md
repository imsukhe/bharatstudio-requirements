# L05 — Go alert worker and Cloud Tasks dispatch

**Status:** `Local routing, lease, handler and enqueue slices passing — live Cloud Tasks, capacity, staging and independent review gates pending`  
**Level:** L3  
**Owner:** Go / Alerts / SRE  
**Depends on:** L01–L04  
**Blocks:** v1 alert delivery and L10

## Objective

Replace the legacy polling/timer dispatch worker with task-driven Go delivery while preserving the platform-wide guarantee: accepted alerts are never dropped because of subscription tier, queue limit, display capacity, disconnection, TTS failure, or worker failure. Ship the approved D-2 multi-queue source-routing behaviour with independent per-queue progress.

## Current implementation evidence — 2026-08-14

- Added `bharatstudio-alerts/services/alert-worker-go`, a standalone Go module for worker logic.
- Implemented deterministic source correlation before priority ordering, with stable created-time/binding-ID tie-breakers.
- Preserved one independent delivery plan per matching queue and copied per-source override values without mutating the binding projection.
- Added tests proving two queues remain independently represented, nonmatching source bindings are excluded, tie ordering is stable, and overrides are not shared mutably; `go test ./...` passes.
- Added migration `0004_v1_l05_delivery_leases.sql` with worker-only claim, retry and completion functions. Each delivery has a lease token, expiry and state version; the shared event row is never used as the per-queue claim state. The disposable PostgreSQL harness proves duplicate claim rejection, retry reclaim, terminal completion and no re-claim after completion.
- Added a validated Cloud Tasks command envelope with event/outbox/delivery identity, expected state version, attempt number, creation timestamp, deadline, trace ID and deterministic retry idempotency key. This is transport validation only; it does not acknowledge or mutate delivery state.
- Added the Go `DeliveryStore` adapter. It calls only the worker-owned PostgreSQL functions for claim, retry and completion, maps no-row results to safe idempotent no-ops, and performs no direct table writes. Adapter tests pass without production credentials.
- Added the private Cloud Tasks handler boundary: strict command decoding, required internal authorizer, durable claim before publish, retryable response on publish failure, and completion only after publication succeeds. Stale claims are acknowledged as safe no-ops; handler tests cover authorization, validation, retry and completion paths.
- Added the worker-only `notify_overlay_wakeup` database function and changed the API direct listener to broadcast wake-ups to all current streams. Each stream still filters through its own token/session and durable cursor replay, so channel/event notification payloads cannot cross tenant boundaries or cause data delivery by themselves.
- Added channel/event identity to the claimed delivery projection and wired a best-effort Go wake-up notifier after durable completion. Notification failure cannot trigger a duplicate task because completion has already been committed; durable replay remains authoritative.
- Added a fail-closed OIDC authorizer boundary for the private task handler: Bearer extraction, required audience and delegated token verification. Added the concrete Google `idtoken.Validator` adapter; Cloud Run service-account binding, audience value and staging token evidence remain deployment gates.
- Added `database/sql` production adapters for the worker delivery store and wake-up notifier. They preserve the private-function-only boundary; the worker process still requires an approved PostgreSQL driver, connection configuration and real publisher wiring before deployment.
- Added a Cloud Tasks enqueue contract with strict `deliver_overlay` action validation, stable SHA-256 task names from delivery/version/attempt, bounded command JSON, OIDC target metadata and idempotent handling of provider `AlreadyExists`; adapter tests pass without GCP credentials.
- Added the language-neutral Cloud Tasks command contract: `contracts/json-schema/cloud-task-command.schema.json` and its golden fixture require the v1 action, durable delivery identities, trace, creation timestamp and deadline. The Go command producer now stamps `createdAt`, validates the lifecycle timestamps, and has a fixture-compatibility test so cross-language envelope drift fails locally.
- Added strict Go compatibility coverage for the committed multi-queue, per-queue delivery, overlay SSE and payment webhook fixtures in `internal/contracts/fixture_compatibility_test.go`. The test uses `DisallowUnknownFields`, validates schema identity, UUID/date-time fields, source/queue identity, independent queue status/priority, immutable override presence and payment delivery identity. It complements the TypeScript/Ajv validator; it does not claim React Native, C# or Swift consumer evidence.
- Added local method-boundary regression coverage for both private HTTP handlers: non-POST requests return `405` with `Allow: POST` before authorization, delivery claim or task enqueue. Worker unit tests, race tests and vet pass; this is local HTTP hardening only and does not prove deployed ingress behavior.
- Tightened the Go command validator to require canonical UUID event, outbox and delivery IDs, matching the v1 JSON Schema instead of accepting arbitrary non-empty strings; malformed IDs now fail before task enqueue or claim.
- Added a production adapter around the official `cloud.google.com/go/cloudtasks/apiv2` client. It creates POST tasks with JSON content type, configured HTTPS target, ADC-backed OIDC service-account token generation and safe `AlreadyExists` classification; the adapter is compile/test verified only, with no live queue or credential evidence.
- Hardened the Cloud Tasks OIDC contract: the token audience is now an explicit `ALERT_WORKER_PRIVATE_AUDIENCE` value shared with the worker verifier, never inferred from `ALERT_WORKER_TASK_TARGET_URL`. The infrastructure manifest uses the same canonical audience placeholder. This prevents a target-path/verification-audience mismatch; live IAM/token evidence remains a deployment gate.
- Added the deployment-level OIDC relationship for the payment-to-worker pump: `ALERT_WORKER_PUMP_AUDIENCE` must equal the worker verifier's `ALERT_WORKER_PRIVATE_AUDIENCE`. The infra contract test enforces this relationship as metadata; actual environment values and IAM negative tests remain deployment gates.
- Added `internal/db.Open` with pgx/database/sql, fail-fast DSN/Ping and bounded worker connection-pool configuration; missing configuration is tested to fail closed.
- Extended the disposable database proof to persist one captured payment into two permitted queue deliveries and complete only the first; the second remains ready and independently claimable.
- Added `DurableReplayPublisher`: worker publication is the durable PostgreSQL delivery already created by the payment boundary, followed by a best-effort overlay wake-up. Wake-up failure is retryable; replay/cursor state remains authoritative and no task is acknowledged on a failed wake-up.
- Added `cmd/alert-worker/main.go`: fail-fast direct worker DB configuration, Google OIDC audience validation, private Cloud Tasks handler, bounded connection/HTTP settings, health endpoint and no auto-migration behaviour.
- Added database-backed `/readyz` and graceful SIGTERM/SIGINT shutdown to the worker runtime. Readiness returns `503` when the worker DB probe fails, while `/healthz` remains a process liveness check; shutdown drains in-flight task/pump requests within a bounded window. This is compile/test evidence only until deployed Cloud Run probe, retry and drain behavior is exercised.
- Corrected the runtime delivery-lease token generator to emit UUID v4 values required by the worker SQL functions; a plain hexadecimal token would have passed handler mocks but failed at the real `uuid` database parameter boundary.
- Bound every claim to the complete command identity and optimistic state: delivery ID, event ID, outbox ID, expected attempt number and expected state version are now checked atomically by `app_private.claim_event_delivery`. A stale or cross-wired command therefore becomes a no-op before it can mutate the current delivery; the SQL harness includes a mismatched-event negative case.
- Added migration `0009_v1_l05_ready_delivery_listing.sql`, a read-only worker delivery store and a task pump. The pump converts bounded ready-delivery rows into stable Cloud Tasks commands and treats enqueue failures as retryable without acknowledging or mutating the durable delivery. The disposable SQL harness proves the ready-list projection includes attempt/version/trace identity.
- Added durable L31/L32 routing snapshots to `event_outbox_deliveries`: accepted deliveries persist `source_priority` and `override_values` before dispatch. The claim projection and Go worker store carry those frozen values, and a disposable SQL regression proves a later binding edit cannot rewrite an already-accepted delivery. The columns are introduced in `0004_v1_l05_delivery_leases.sql` before the claim function is created; `0010_v1_l31_l32_delivery_snapshots.sql` remains idempotent for databases that already have the lease migration.
- Added the private `/internal/v1/tasks/pump` worker endpoint. It authenticates the payment service, scans a bounded ready-delivery batch, creates stable Cloud Tasks commands and returns retryable failure on any enqueue error without mutating the durable delivery. The payment webhook calls this endpoint after persistence; the pump is a wake-up path, while repeated scans remain safe recovery.
- Closed a lease-stranding path in the Cloud Tasks handler: if overlay publication succeeds but durable completion is unavailable or returns no row, the handler now transitions the delivery to `failed_retriable` before returning `503`. The next task/recovery scan can claim it instead of receiving `200 ignored` against an active lease.
- Restricted the task envelope to the only approved v1 action, `deliver_overlay`; unsupported actions are rejected before claim and cannot mutate a delivery.
- Corrected the runtime durable replay publisher so it does not send a pre-completion wake-up. The handler now completes durable delivery state first and emits one best-effort wake-up afterward; cursor replay remains authoritative and notification failure cannot cause duplicate wake-ups or financial replay.
- Added migration `0015_v1_l05_outbox_projection_refresh.sql`: completion/retry transitions lock and refresh the global `event_outbox.status` read-model from independent delivery rows. This projection cannot block dispatch; it keeps history and Companion pending counts accurate while preserving per-queue authority.
- Added migration `0020_v1_l32_overlay_delivery_projection.sql`: the overlay replay function now projects the immutable per-delivery queue/binding/priority/override snapshot alongside the shared event payload, so later binding edits cannot change what each queue renders. The L03 database harness asserts distinct styles for both payment deliveries.
- Added migration `0022_v1_l05_overlay_ack_release.sql` to separate worker publication from viewer acknowledgement. The worker now releases its lease back to `ready` after durable publication; the overlay acknowledges only after display, transitions the delivery to `acknowledged`, refreshes the outbox projection, and removes acknowledged rows from a fresh overlay replay. This prevents a successful worker task from producing an `alert.complete` frame that the browser would not render, and preserves replay when the browser disconnects before acknowledgement. Go handler/store tests and the disposable database harness cover the release boundary; live Cloud Tasks/overlay evidence remains open.
- Added migration `0030_v1_l05_publication_marker.sql` to separate worker wake-up scheduling from browser acknowledgement. A successful release records `published_at` but leaves the delivery `ready` and replayable; subsequent pump scans exclude that published row until the overlay acknowledges it. This prevents duplicate Cloud Tasks work during offline/slow-overlay periods without making a presentation limit a data-loss path. The disposable harness proves the marker and ready-list exclusion; explicit manual replay/reset semantics remain governed by the operator runbook and are not inferred here.
- Added migration `0032_v1_l32_source_rate_limit_and_publication_claim_guard.sql`. Per-source `rateLimitPerMinute`/legacy `rateLimitPerMin` snapshots are enforced atomically at the worker claim boundary with a binding-level one-minute counter. An exhausted window only advances `next_action_at` and `state_version`; it never drops, suppresses, acknowledges or removes the accepted delivery. The same claim boundary rejects a stale task after `published_at` is set, while browser replay remains available until acknowledgement. The disposable harness proves delay-only limiting, window rollover and stale-task no-op behaviour.
- Added bounded binding override validation in the API/OpenAPI contract. Presentation-safe fields (including bounded bracket timing/character/TTS overrides) and the source rate-limit aliases are accepted; unknown executable/script-like fields, amount-range changes and unbounded objects are rejected before persistence. The overlay applies bracket overrides only to the amount-selected bracket and never permits a delivery to change its amount routing.
- Extracted and unit-tested the worker `/readyz` contract: GET-only, bounded DB probe and generic not-ready response. `/healthz` remains process liveness, and graceful shutdown drains HTTP work; deployed Cloud Run probe/drain evidence remains open.
- Added migration `0023_v1_l05_queue_pause_dispatch_guard.sql`: the ready-delivery listing, per-task claim and overlay replay all re-check that the target queue is active and unpaused. A queued task or reconnect becomes a safe no-op while paused; the accepted delivery remains durable and is visible again after resume. The disposable PostgreSQL harness covers pause → no-claim/replay suppression → resume behavior.
- Added the operator recovery runbook at `services/alert-worker-go/docs/CLOUD_TASKS_OPERATIONS.md`. It defines retry/dead-letter/manual-replay handling, queue pause and notification-outage recovery, monitoring, rollback and the required deployment values without treating a transport dead letter as permission to discard an accepted delivery.
- Hardened the worker pump to reject a non-positive batch limit instead of returning a false-success empty scan; `ErrInvalidPumpLimit` is covered by a focused Go test.
- Added a reproducible multi-stage `services/alert-worker-go/Dockerfile`: Go 1.26 build stage, static Linux binary, distroless non-root runtime, and a service-local `.dockerignore`. The image builds locally as `bsa-alert-worker:local`; this is container-packaging evidence only and does not establish Cloud Run/IAM/Cloud Tasks/overlay readiness.
- Pinned the worker's Go build and distroless runtime stages to the exact digests used by the verified local build, removing floating base-image resolution from the worker artifact. The pinned image rebuild passes; this does not close Cloud Run, IAM, Cloud Tasks, dead-letter or staging evidence.
- Added `.env`/`.env.*` exclusions to the worker Docker build context so local environment files cannot be sent to the container builder; the worker image contains only the compiled static binary in its runtime stage.
- Added a disposable PostgreSQL integration test for the real `database/sql` worker store. It inserts a synthetic pending delivery, claims it through `app_private.claim_event_delivery`, verifies channel/source-priority/JSONB override projection, releases it back to `ready`, and proves a stale command cannot reclaim it. The test runs with the `integration` tag from the L03 database harness.
- Added the browser-side presentation policy slice shared with L05: `apps/web/app/overlay/overlay-policy.ts` and `apps/web/app/overlay/[overlayId]/page.tsx` consume the immutable `configSnapshot` from migration `0029_v1_l05_overlay_config_snapshot.sql`, apply bounded bracket timing/character rules and the approved FIFO/priority/stacked/pills/aggregated display modes, preserve acknowledgement order within priority batches, and acknowledge every displayed delivery only after the group is shown. Optional same-origin audio falls back to a non-blocking browser chime when unavailable; visual delivery never depends on TTS. Local policy tests pass (6/6), the web build passes and the disposable PostgreSQL harness proves snapshot projection. This is local presentation evidence only; provider TTS generation, worker capacity, cross-replica fan-out and live staging remain open.
- The shared disposable PostgreSQL harness now opens two independent listener connections and a separate publisher, proving one committed `pg_notify` wakes both overlay waiters. The listener wrapper matches `postgres.js` registration semantics and treats notification as best-effort; durable cursor replay remains the correctness path. Direct Neon endpoint, cross-replica staging and load/reconnect evidence remain open.
- The shared overlay SSE route now catches a transient durable-replay failure after headers are committed, emits only a bounded comment, closes cleanly and lets the browser reconnect with its last acknowledged cursor. No worker publication or browser acknowledgement occurs in this failure path. The current API suite passes 54/54 and the web build passes; deployed fault-injection evidence remains open.
- Added the browser TTS playback boundary in `apps/web/app/overlay/tts-runtime.ts`. Audio playback is capped by a hard 1.5-second timeout; rejection or a stuck `HTMLAudioElement.play()` promise returns control to the non-blocking chime path. The visual alert, durable delivery and cursor acknowledgement do not wait for TTS. Focused timeout/rejection/success tests pass; this is provider-neutral playback evidence and does not claim Sarvam/provider generation or live audio validation.
- Added a bounded synthetic burst proof for the ready-delivery pump. A 1,000-candidate batch produces one stable command per durable delivery; a deterministic subset of enqueue failures returns retryable partial status without acknowledgement, and a later healthy scan recovers every candidate. This is pump-boundary correctness evidence only, not Cloud Tasks or production throughput evidence.

This remains an implementation slice. It now covers the local durable dispatch protocol, executable worker bootstrap and enqueue/handler contracts, but does not claim live Cloud Tasks delivery, overlay publication under load, retry/dead-letter recovery, capacity guarantees, crash recovery or deployment readiness.

### L05 local completion audit — 2026-08-15

A fresh acceptance audit found no remaining local worker correctness gap in the
approved L05 scope. The worker Go module passes unit tests, race tests and
`go vet`; contract validation passes 11 fixture mappings and 32 OpenAPI paths;
the disposable L02/L03 PostgreSQL harness passes; and the two-listener direct
PostgreSQL wake-up integration passes. The audit deliberately did not generate
or modify BSA visual packages. L05 remains open only for live Cloud Tasks,
deployed OIDC/IAM, cross-replica overlay, capacity/fault-injection, retry/DLQ
rehearsal, OBS and independent-review evidence.

## SQL ready-row pump adapter evidence — 2026-08-15

Extended services/alert-worker-go/internal/store/sql_store_integration_test.go
to exercise the real database/sql ready-delivery adapter together with the
task pump. The disposable PostgreSQL run now:

- inserts a synthetic pending delivery;
- lists it through app_private.list_ready_event_deliveries;
- emits a command carrying the exact delivery/event/outbox/attempt/version
  identity and stable idempotency key; and
- forces an enqueue outage, then verifies the durable ready row remains
  available for a later scan.

The fixture also contains other synthetic ready rows, so the assertion checks
the target delivery within the bounded batch rather than assuming a single
candidate. This is local adapter/retry evidence only; live Cloud Tasks,
dead-letter, IAM, deployment, capacity and staging rehearsal remain open.

## Bounded concurrent Cloud Tasks pump — 2026-08-15

The ready-row pump previously called the Cloud Tasks enqueuer serially for
every candidate. It now builds and validates all stable commands first, then
enqueues them through a bounded worker pool. The default concurrency is 8 and
the runtime accepts the positive `ALERT_WORKER_PUMP_CONCURRENCY` setting; the
handler remains bounded by its ready-row batch limit.

This improves provider round-trip throughput without changing delivery
ordering authority, task idempotency names, or durable state. A partial
provider failure returns a retryable result and leaves every failed candidate
untouched for a later scan; context cancellation also returns non-success
rather than claiming completion. The burst regression verifies 24 candidates,
maximum concurrency of 4, and no missing command; existing 1,000-row
partial-failure/retry coverage remains green. This is local concurrency
evidence only; Cloud Tasks quotas, deployed throughput and staging capacity
remain open.

## Deployment-boundary evidence — 2026-08-15

The infrastructure repository now contains a non-deployable v1 topology
contract and validator. It requires the Alert Worker to have no public
ingress, requires OIDC for private task/pump routes, requires separate pooled
application and direct overlay-listener database secret references, and keeps
Cloud Tasks disabled until its queue, OIDC, retry/dead-letter and staging
values are approved. `bharatstudio-infra` `npm test` passes 8/8. No live queue,
Cloud Run service, IAM binding or staging capacity claim is made.

## Tasks

1. Characterize every legacy queue mode and state transition: FIFO, priority, approval, quiet, hold, aggregate, stacked display, replay, expiry, moderation and refund-after-display.
2. Define one Cloud Tasks command per next durable action with idempotency key, event/outbox ID, attempt number, trace ID, expected state/version, timeout and dead-letter handling.
3. Implement Go task handler: claim per-outbox delivery state, apply frozen configuration snapshot, reserve capacity, render delivery payload, publish overlay SSE, record attempt, schedule next action or recovery.
4. Implement D-2 source routing: resolve the source and binding before priority selection, persist a separate delivery/outbox row for each permitted queue, and apply per-source priority/style/bracket/rate-limit rules without changing another queue's state.
5. Implement queue capacity semantics: preserve accepted events, hold/delay/aggregate only under approved rules, display a clear creator state, and replay when capacity returns. No `drop` path.
6. Implement overlay session/reconnect cursors and server-side resync. A disconnected OBS/browser source must receive missed eligible events in correct policy order, including when the event was accepted by another API/worker replica.
7. Implement bounded TTS generation/playback coordination: text/visual path succeeds independently; provider timeout/error falls back to approved sound/chime; no delivery depends on TTS completion.
8. Use Cloud Tasks retry/dead-letter semantics and reconcile task state with durable outbox. Do not rely on process advisory locks or `setInterval` for alert work. Do not make pooled `LISTEN/NOTIFY` the correctness path for SSE publication.
9. Run unit, integration, fault injection, queue-burst, cross-replica fan-out, source-correlation and overlay-concurrency tests. Shadow-run against synthetic staging data before live traffic.
10. Preserve claim-command identity binding in migrations, worker store calls and the replay harness; reject mismatched event/outbox/attempt/version tuples without changing delivery state.
11. Pump ready delivery rows into Cloud Tasks using stable delivery/version/attempt task names; repeated scans must be harmless and enqueue failure must leave the durable row eligible for another scan.
12. Preserve L31/L32 routing snapshots on every accepted delivery: source priority and per-source override values must be immutable dispatch inputs, independent of later queue-binding edits.
13. Expose a private pump endpoint backed by the ready-delivery store and Cloud Tasks enqueuer; authenticate it with service identity and preserve ready rows when enqueue is partial or unavailable.
14. Reject unsupported task actions before any claim or publication attempt; keep the action allowlist explicit as new actions are introduced.
15. Keep durable publication and wake-up ordering explicit: no notification before completion, one best-effort wake-up after completion, and no correctness dependency on notification delivery.
16. Refresh the global outbox projection only as a read-model after per-queue transitions; lock the outbox row so concurrent queue completions cannot leave a stale aggregate status.
17. Publish and rehearse the Cloud Tasks/dead-letter/manual-replay runbook; transport limits must be recorded as deployment configuration and may not become a data-loss path.

## Acceptance criteria

- Entry, hold/update, exit, reset/replay and reconnect scenarios pass for every supported queue mode.
- Duplicate task execution is harmless; out-of-order/retried task cannot corrupt event state.
- A permitted event routed to two queues can progress independently when one queue is blocked; source/priority correlation and per-source overrides are correct and auditable (`L-31`/`L-32`).
- Multiple delivery rows are permitted only when every participating source binding explicitly opts into duplicates. The payment router selects the highest-priority route for mixed consent, and the database delivery-row trigger rejects stale or malformed multi-queue payloads that contain a non-consenting binding. A single binding remains valid with the default `false` value.
- Cross-replica overlay publication is tested; missed live notifications are recovered from the durable cursor/outbox path.
- Cloud Tasks retries and dead-letter path have operator runbooks.
- Full queue, offline overlay, process crash, TTS outage and provider delay preserve accepted alerts and show accurate state. Worker publication is not treated as viewer acknowledgement; the durable row remains replayable until the overlay cursor is acknowledged.
- No legacy worker timer/pooled advisory-lock dependency remains on the v1 dispatch path.
- A command carrying the wrong event, outbox, attempt or state version cannot claim or mutate another delivery; the correct command remains claimable after the rejected attempt.
- A ready-delivery scan emits a command with the exact delivery identity and optimistic state; failure to enqueue does not mark the delivery complete or remove it from the ready source.
- A binding priority/override edit after acceptance does not change the persisted delivery snapshot used by the worker.
- The pump endpoint is unavailable without internal authorization, and an enqueue failure returns retryable failure while leaving the ready delivery eligible for a later scan.
- A publication-release failure releases the lease into durable retry state before the task response is retryable; the delivery cannot be stranded behind an active lease.
- A command with an unsupported action is rejected before claim and cannot mutate, publish or acknowledge any delivery.
- The runtime publisher does not emit a pre-completion notification; a completed durable delivery remains replayable even if the post-completion wake-up fails.
- A delivery successfully published by the worker is marked `published_at` exactly once, remains eligible for overlay cursor replay/acknowledgement, and is not repeatedly returned by the ready pump while awaiting the browser. A publication-release failure leaves the marker unset and keeps retry recovery available.
- A per-source rate limit is delay-only: once the configured window is exhausted, accepted deliveries remain durable in `ready`/retryable state with a future `next_action_at` and can be claimed after rollover; the counter is updated atomically across worker replicas and no subscription tier or rate limit can create a drop path.
- A stale or duplicated task cannot reclaim a delivery after `published_at` is set, while the overlay can still replay and acknowledge that delivery. Binding override input is bounded at the API contract and browser bracket overrides cannot change amount ranges or select an unrelated bracket.
- After one of two permitted queue deliveries completes, the outbox remains pending; after both are terminal, it becomes completed, and neither projection state can prevent independent queue progress.
- The operator runbook names the redacted evidence, owner, replay guardrails, monitoring and rollback for task retry/dead-letter and notification outage; no recovery action deletes or silently acknowledges accepted evidence.

## Rollback

Disable task enqueue feature flag, stop task target, drain/inspect outbox via private recovery endpoint, and restore the last verified deployment. Never delete outstanding events to recover.

## Cross-replica replay security correction — 2026-08-15

The real shared-PostgreSQL API integration found that the replay projection
needed an explicit event-to-session-channel predicate. Migration
`0054_v1_l03_overlay_event_channel_guard.sql` now requires
`event.channel_id = session.channel_id`; a valid overlay token cannot enumerate
another channel's delivery rows. Separate SQL clients and Fastify instances
then prove commit-on-shared-database → replay-on-replica-B → acknowledge-on-B →
no-replay-on-A. This is local correctness evidence, not deployed Neon,
Cloud Run, capacity or OBS evidence.

## Shared overlay recovery regression — 2026-08-15

The browser-side acknowledgement path was rechecked against the L05 delivery
guarantee. If acknowledgement fails after a group is displayed, the client
now requeues only the unacknowledged suffix, aborts the active SSE connection,
reconnects from the last confirmed cursor and resumes without requeueing the
acknowledged prefix. The focused overlay policy/TTS suite passes 10/10, the
API suite passes 54/54, both Go services pass unit tests, `go vet` and race
checks, and the disposable PostgreSQL harness remains green. This closes a
local client recovery defect; it does not replace live Cloud Tasks, deployed
fan-out, capacity or OBS staging evidence.

### Full local boundary rerun — 2026-08-15

The worker package passes `go test -race ./...`; the complete disposable
PostgreSQL runner passes the L02/L03/L04/L05 migration and worker-store slices,
including two-listener overlay wake-up, per-queue replay/acknowledgement,
delay-only rate limiting, stale-publication protection and Companion command
delivery. The Alerts API suite passes 54/54, the web/API production build
passes, and `pnpm contracts:validate` passes the 11 fixture mappings and 32
OpenAPI paths. Mobile and macOS Companion checks also pass locally (mobile
19/19 plus lint/typecheck; macOS 7/7). No BSA visual package was generated or
modified.

This remains local correctness evidence. Live Cloud Tasks queue/retry/DLQ,
deployed OIDC/IAM, cross-replica capacity and reconnect proof, OBS testing,
fault/recovery rehearsal and independent L05 review remain release gates.

## Automatic continuation verification — 2026-08-15

The follow-up local verification pass completed without a new implementation
gap:

- `go test ./...` passed for the alert-worker module;
- `go test -race ./...` passed for all worker packages;
- `go vet ./...` passed;
- `pnpm db:test:l03` passed the disposable L02–L05 PostgreSQL chain,
  including worker SQL integration, independent queue progress, publication /
  replay, delay-only rate limiting, two direct listeners and shared-database
  cross-replica checks.

The Cloud Tasks runbook was also checked against the command, pump, handler,
lease and readiness implementations; no local mismatch was found. This is
additional local evidence only and does not close live Cloud Tasks, OIDC/IAM,
retry/dead-letter execution, deployed capacity, OBS/staging or independent
review gates.
