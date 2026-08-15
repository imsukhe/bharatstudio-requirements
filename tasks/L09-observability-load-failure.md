# L09 — Observability, load, failure and recovery proof

**Status:** `Local instrumentation and regression slices passing — final topology/load/failure proof pending`  
**Level:** L3  
**Owner:** SRE / QA / security  
**Depends on:** L03–L08  
**Blocks:** L10
**Test record:** `../tests/TC-L09-observability-load-failure.md`
**Local regression record:** [`../reviews/2026-08-15-local-regression-and-surface-verification.md`](../reviews/2026-08-15-local-regression-and-surface-verification.md)

## Objective

Prove the final topology, rather than legacy measurements, can sustain declared v1 load and fail safely.

## Current implementation evidence — 2026-08-15

- Added an internal Prometheus-compatible API metrics endpoint at `/internal/metrics`, protected by the existing service-identity verifier. It reports only normalized route templates, method, status and duration totals; it does not expose request URLs, IDs, authorization headers, payloads or payment data.
- Added API tests for unauthenticated rejection, authenticated scrape, normalized route labels and secret/request-identifier absence; 53 API tests and the API build pass.
- Added authenticated direct-overlay-listener health metrics for connection state, reconnect attempts and listener failures, with local failure/reconnect tests; the current API suite passes 54/54. This remains instrumentation and local fault evidence, not a staging topology or capacity result.
- Added authenticated Prometheus-compatible metrics endpoints to the Go payment and alert-worker services. Both services instrument HTTP method, normalized route, status and duration totals; UUID path segments and query strings are removed before emission. The endpoints use the existing private OIDC authorizer and never emit request URLs, tokens, headers, provider payloads or payment identifiers. Each service's `go test ./...` and `go vet ./...` pass.
- Added the first internal trace-propagation slice: a verified Razorpay webhook derives `razorpay:<provider-event-id>` and carries it as bounded `X-BSA-Trace-Id` to the private worker-pump hop. The value is never taken from a client-supplied trace header; ingress tests cover propagation and sanitisation. Full web/API/provider/task/SSE correlation remains a staging integration task.
- Added the local trace contract at [`OBSERVABILITY_TRACE_CONTRACT.md`](../../bharatstudio-alerts/docs/architecture/OBSERVABILITY_TRACE_CONTRACT.md): worker task envelopes now reject unbounded/control-character trace values, JSON round-trip tests preserve the correlation fields, and the disposable PostgreSQL L03 harness verifies the server-derived Razorpay trace reaches both independently routed overlay deliveries and overlay replay. This closes the local contract slice only; deployed structured logs and collection remain pending.
- Added bounded JSON structured operational events to the payment and alert-worker runtimes. The logger is wired to webhook/task boundary outcomes and can emit only timestamp, allowlisted component/outcome and a validated trace ID; it accepts no arbitrary fields or error/payload object. Unit tests prove invalid trace/control data is omitted. This is local redaction evidence only; deployed log sink permissions, retention, dashboards and alert routing remain pending.
- Rebuilt both current Go service containers from their Dockerfiles as static, non-root distroless images (`bsa-payment-webhook:local` and `bsa-alert-worker:local`); both builds passed. This proves reproducible image construction only, not registry provenance, deployment IAM, runtime probes or production rollout.
- Re-ran the real local web surfaces: unauthenticated overlay stayed in `Overlay reconnecting` with no fabricated result or browser errors, and unauthenticated Companion showed bounded sign-in-required state with no direct OBS/localhost command path. The API SSE route also now closes cleanly after a post-headers replay failure and leaves reconnect/cursor recovery to the browser. Authenticated event rendering and OBS-source evidence remain open.
- Added a real shared-PostgreSQL cross-replica API proof: separate SQL clients and Fastify instances commit/replay/acknowledge the same durable delivery across replicas, and migration `0054_v1_l03_overlay_event_channel_guard.sql` prevents a valid overlay session from enumerating another channel's deliveries. This closes the local tenant-boundary and shared-database replay slice; Neon/Cloud Run network, capacity and OBS staging evidence remain open.
- Corrected payment metrics route normalization to retain `/internal/v1/tips/orders` as an actionable checkout lane instead of collapsing it into `/_other`; a regression test protects the route label while still removing query strings.
- Added bounded alert-worker business counters for task outcomes (`accepted`, `ignored`, `invalid`, `retryable`, `unauthorized`, `not_configured`) and pump outcomes (`completed`, `partial`, `retryable`, `invalid`, `unauthorized`, `not_configured`). No delivery, event, queue, payment or user identifiers are emitted; unit tests cover allowlisted labels and unknown-outcome collapse.
- Added bounded payment-webhook business counters for `accepted`, `duplicate`, `invalid`, `retryable` and `not_configured` outcomes. They are emitted only after the corresponding boundary decision and contain no provider event, order, account, payment or donor identifiers.
- Added bounded payment checkout and payment/refund reconciliation outcome counters. They distinguish accepted/invalid/retryable checkout and completed/retryable/unauthorized/not-configured reconciliation without exposing provider or financial identifiers.
- Added database-backed readiness and bounded graceful shutdown to the Go payment and worker runtimes. Readiness is distinct from liveness and fails closed on DB loss; shutdown behavior is locally compile/vet verified but still requires deployed Cloud Run probe/drain and fault-injection evidence.
- This is local instrumentation only. It does not claim deployed dashboards, alert policies, log sink controls, load capacity or failure-recovery proof.
- Replaced raw TypeScript API error-object logging with an allowlisted safe logger. API routes now record only a bounded event name, request trace ID, sanitized error category and explicitly supplied bounded labels; provider/database/user-controlled messages and stacks are never serialized. The API test suite includes secret/message/stack redaction assertions, and source audit finds no remaining raw error-object logging in API routes.
- Added the disabled infrastructure observability contract at `bharatstudio-infra/deployment/v1/observability.template.json`. It defines private scrape targets, dashboards and alert categories for payments, dispatch, overlay fan-out, platform health, Companion and security, with forbidden identifier/payload labels and explicit deployment-threshold placeholders. The infrastructure test covers the contract; live dashboards, alert routing and staging thresholds remain open.

### Deployment-boundary evidence — 2026-08-15

The v1 infrastructure contract defines liveness/readiness endpoints for the
three runtime services and requires explicit service sizing, database plan,
region, IAM, Cloud Tasks and observability gates before deployment. Its local
validator passes 8/8. This remains a configuration contract, not a measured
capacity, dashboard, alert-policy or fault-injection result.

### Local regression rerun — 2026-08-15

The Alerts API suite (54/54), production build, contract validation,
disposable PostgreSQL L02/L03 harness, Go payment and alert-worker tests with
`go vet` and `go test -race`, cron contract, mobile tests/lint/typecheck and
macOS Swift tests all passed. This confirms the local instrumentation and
boundary slices compile and regress cleanly; it does not satisfy the deployed
metrics scrape, dashboard/alert, capacity or fault-injection acceptance cases.

## Fresh local audit — 2026-08-15

The L09 implementation, acceptance matrix, API/payment/worker metrics,
trace/logging contracts, cross-replica overlay integration, infrastructure
observability template and failure semantics were reviewed together. No new
locally verifiable correctness gap was found.

Confirmed locally:

- metrics endpoints are private and use bounded route/status/outcome labels;
- query strings, credentials, provider identifiers, donor/payment identifiers,
  raw payloads and arbitrary error text are excluded from the local telemetry
  contracts;
- payment-to-worker trace propagation is server-derived and bounded;
- durable overlay replay works across separate API/SQL replicas and remains
  correct when notification wake-up is unavailable;
- alert acceptance and payment persistence remain durable before asynchronous
  delivery work, so capacity limits cannot be implemented as silent drops;
- the infrastructure observability topology is declarative, disabled and
  explicitly requires private scrape access, thresholds, dashboards, owners and
  runbook rehearsal before enablement.

No production capacity number is declared from these checks. L09 remains open
for final-region/topology measurements, staged normal/peak load, deployed
dashboard and alert routing, provider/task/database/SSE fault injection,
backup/restore, rollback and incident rehearsal. Deferred visual alert package
generation is not part of this L09 work.

## Automatic continuation verification — 2026-08-15

The follow-up local gate rerun passed:

- alert-worker `go test ./...`, `go test -race ./...` and `go vet ./...`;
- cron contract `npm test` 2/2;
- infrastructure contract `npm test` 8/8;
- `pnpm db:test:l03`, including L02 security remediations, L03 application
  behaviour, payment/worker SQL integration, two-listener wake-up and shared
  PostgreSQL cross-replica replay.

These results strengthen local regression evidence only. They do not establish
the final Neon/Cloud Run region, throughput, SSE concurrency, provider/task
failure recovery, deployed telemetry, backup/restore or rollback evidence.

## Tasks

1. Declare staging targets before running tests: payment receipt acknowledgement/error budget, dispatch latency, queue age, overlay SSE concurrency, recovery time, database pool/CPU, request limits and donor/creator experience limits.
2. Complete the deployed trace path across web → Creator API → payment service → outbox → Cloud Tasks → alert worker → SSE overlay; the local payment/DB/task/overlay contract and service redaction tests are recorded above.
3. Define dashboards and alerts for payment mismatch, webhook verification failures, duplicate/missing Razorpay event IDs, outbox/task backlog, DLQ, SSE disconnect/resync, cross-replica fan-out lag, listener reconnects, entitlement-cache staleness, DB saturation, provider errors, failed schedules, helper health, crash rate and security anomalies.
4. Run staged load tests with final deployed region/database plan: normal/peak webhook ingestion, task dispatch, queue capacity, concurrent overlays, public tip traffic and Companion connections.
5. Run fault injection: database write failure, Cloud Tasks retry, duplicate/out-of-order webhook/task, alert worker crash, SSE disconnect, cross-replica notification/listener outage, pooled-endpoint misconfiguration, TTS/provider outage, Razorpay status delay, scheduler miss, rollback deployment and restore drill.
6. Verify no alert/purchase loss and no duplicate financial effect; reconcile durable ledger/outbox/task/overlay results.
7. Record results as measurement with date, environment, configuration, dataset, limitation and disposition; do not reuse the legacy Neon latency result as production proof.

## Acceptance criteria

- All declared targets are met or a documented capacity/mitigation decision is approved.
- Every critical alert has an actionable runbook and owner.
- Failure tests demonstrate safe retry/hold/recovery, not merely absence of crashes.
- An overlay connected to replica B receives an event committed through replica A; disabling live notification still allows cursor/replay recovery, and entitlement changes converge through the documented fallback.
- A duplicate Razorpay webhook with the same `x-razorpay-event-id` produces no second financial effect or alert.
- D-2 multi-queue tests prove no global event status prevents independent queue progress, with source/priority and per-source override results recorded.
- Backup/restore, rollback and incident communication exercises pass.

## Rollback

Tests run in isolated staging. Production load changes require explicit L4 approval, a capacity cap and rollback/traffic-shedding plan.
