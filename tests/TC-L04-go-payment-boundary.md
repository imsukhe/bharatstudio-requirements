# L04 acceptance and test record — Go payment boundary

**Status:** `Implementation slice passing — persistence, provider approval and staging cutover remain open`  
**Task:** [`../tasks/L04-go-payment-boundary.md`](../tasks/L04-go-payment-boundary.md)  
**Repository:** `/Users/sukhdevsingh/Workspace/Bharat Studio/bharatstudio-alerts/services/payment-webhook-go`

All tests use synthetic values and local fake provider servers. No real Razorpay credentials, payment data or production endpoint is used.

### Deployment contract evidence — 2026-08-15

The infrastructure manifest maps the public Razorpay webhook and OIDC-
protected internal routes without embedding credentials. `npm test` in
`bharatstudio-infra` passes 8/8. This does not prove deployed IAM, Secret
Manager, provider approval or staging recovery.

| ID | Setup/action | Expected result | Evidence |
|---|---|---|---|
| L04-01 | Verify a Razorpay webhook against the exact raw body and valid HMAC | Delivery is accepted and the provider event ID is extracted | `internal/webhook/verifier_test.go`; pass |
| L04-02 | Change/reformat the signed body or omit/alter the signature | Verification fails closed; no persistence is attempted | verifier and ingress tests; pass |
| L04-03 | Omit, oversize or vary-case the `x-razorpay-event-id` header | Missing/invalid identity cannot enter the normal acknowledged path; valid case variants are handled | verifier tests; pass |
| L04-04 | Make the atomic store unavailable or return duplicate | Unavailable persistence returns retryable 503; durable duplicate returns 200 duplicate | ingress tests; pass |
| L04-05 | Create a ₹50 INR order against a fake HTTPS-equivalent provider contract | Server-owned amount/currency/receipt/notes are sent with Basic Auth, the server-resolved `X-Razorpay-Account` is present, and the order response is parsed | `internal/provider/razorpay_orders_test.go`; pass |
| L04-06 | Submit amount below ₹10, non-INR currency, oversized receipt or notes | Request is rejected before any provider call | provider tests; pass |
| L04-07 | Return provider 429/5xx/transport failure or a body above the response bound | Error is retryable, bounded and does not expose provider response content | provider tests; pass |
| L04-08 | Return an order with a different amount, currency or receipt | Response is rejected; caller cannot persist a mismatched order | provider tests; pass |
| L04-09 | Fetch a synthetic order by provider ID and linked-account reference | Account-scoped status response is bounded and parsed for later reconciliation; missing account attribution fails before provider I/O | provider tests; pass |
| L04-10 | Create the same local order intent twice, claim provider creation, attach a provider order, and retry after the intent exists | Exactly one local intent is returned; one claim owns provider I/O; attachment is repeat-safe and the state remains recoverable after lease expiry | `0006_v1_l04_payment_order_intents.sql` in disposable PostgreSQL 16 harness; pass |
| L04-11 | Normalize payment/order, refund, subscription and dispute webhook payloads with extra fields and trailing data | Only approved identity/amount/status fields are projected; `payment.dispute.*` is classified as dispute before the broad payment prefix; malformed/trailing/unsupported payloads fail closed | `internal/webhook/payload_test.go`; pass |
| L04-12 | Record one verified captured payment against the exact account/order, with one valid queue binding | Webhook delivery, payment, alert event, outbox and delivery row commit atomically; mismatched account/order/amount is quarantined | `0007_v1_l04_webhook_persistence.sql` in disposable PostgreSQL 16 harness; pass |
| L04-13 | Invoke the SQL store boundary with a channel-resolved account/environment and a synthetic signed payload, including a consented payment binding | The immutable local intent resolves the account/order/binding context; the verified signed payload's `account_id` must match that account; generated IDs, normalized projection and JSONB queue override are passed to the private persistence function; exactly one alert/delivery projection is created | `internal/ingress/sql_store.go`, integration test and disposable PostgreSQL 16 harness; pass with the real pgx/database/sql driver |
| L04-14 | Open the payment database with missing DSN or configured pgx pool | Missing DSN fails closed; configured pool pings before use and applies bounded settings | `internal/db/postgres_test.go`; pass without external database |
| L04-15 | Record a processed refund for an existing captured payment | Refund evidence is append-only, payment status becomes refunded/partially_refunded from processed totals, and no historical alert payload is rewritten | `0007_v1_l04_webhook_persistence.sql` in disposable PostgreSQL 16 harness; pass |
| L04-16 | Create an intent with bounded donor display name/message and persist a captured payment | The exact local donor fields are carried into the alert payload; provider webhook fields cannot replace them | `0006`/`0007` plus disposable PostgreSQL 16 harness; pass |
| L04-17 | Send a public tip-order request with a canonical handle and a valid idempotency key | The API resolves the channel server-side, derives a stable receipt, forwards bounded fields to the payment boundary and returns the reviewed order response | `apps/api/test/app.test.ts`; pass |
| L04-18 | Send a public order request without the payment service dependency | The API returns retryable `payment_unavailable`; no browser/provider state is fabricated | `apps/api/test/app.test.ts`; pass |
| L04-19 | Send an internal checkout request with missing/private authorization, mismatched idempotency header/body or trailing JSON | The private handler rejects it before the order service is called | `internal/checkout/handler_test.go`; pass |
| L04-20 | Run provider-order creation through the lease-token path against the SQL function contract | The claim token is UUID-shaped and can be accepted by the real `uuid` SQL parameters; mocked service tests remain green | `internal/checkout/service.go`, `internal/checkout/handler_test.go`, SQL-store integration test; pass against disposable PostgreSQL |
| L04-21 | Start the payment service with missing required configuration, or inspect its configured routes | Startup fails closed before serving; when configured, only the verified webhook and private OIDC checkout route are mounted, `/readyz` is DB-backed while `/healthz` remains liveness-only, with bounded HTTP timeouts and no auto-migration | `cmd/payment-webhook/main.go`, `internal/auth`, `internal/observability/readiness_test.go`; `go test ./...` and `go vet ./...` pass; deployment/IAM/probe evidence pending |
| L04-22 | Retry provider-order creation with mutable request metadata | Provider notes contain only the server-derived local intent reference; unpersisted retry metadata cannot change a provider order | `internal/checkout/service_test.go`; pass |
| L04-23 | Configure the Creator API payment client with a private origin/audience and validate a response | Non-development origins must be HTTPS; Google OIDC client calls the fixed private route and rejects an invalid provider/order response before returning it to the browser | `apps/api/src/db/payment-order-client.ts`, `apps/api/test/app.test.ts`, `apps/api/src/config.ts`; 53 API tests/build pass |
| L04-24 | Create and capture a tip with `alertConsent=false` | Payment and webhook evidence are processed normally, while no alert event, outbox record or queue delivery is created; changing consent on an idempotent retry is rejected | `0006`/`0007` plus disposable PostgreSQL 16 harness; pass; API forwarding and Go private-handler contract tests pass |
| L04-25 | Apply a partial refund, replay the same provider refund event, then apply the remaining refund | The first refund changes payment state to `partially_refunded`, the duplicate event creates no second refund, and the final aggregate changes state to `refunded` without rewriting the original tip or alert | `0007` plus disposable PostgreSQL 16 harness; pass |
| L04-26 | Evaluate fetched provider order states against an immutable local intent | Open/unexpired orders are no-op; unpaid expired orders expire only the local intent; fully paid orders queue payment-level recovery; mismatches and unknown states cannot create a payment or alert | `internal/reconcile/reconcile_test.go`; pass |
| L04-26a | Submit a checkout intent with a future expiry beyond the approved local lifetime | The private Go boundary and database security-definer function reject the request; no overlong intent is persisted and no unsupported provider `expire_by` field is sent | `internal/checkout/handler_test.go`, migration `0045_v1_l04_payment_intent_expiry_cap.sql`, `l03_application_behavior.sql`; Go tests and `pnpm db:test:l03`; pass |
| L04-27 | Run reconciliation against multiple candidates with a provider timeout and durable SQL actions | Expiry and recovery actions are applied only for validated provider responses; provider failures return a retryable partial result without mutating the candidate; SQL listing/expiry/recovery functions pass the disposable PostgreSQL harness | `internal/reconcile/runner_test.go`, `internal/reconcile/sql_store.go`, `0008_v1_l04_reconciliation.sql`; Go tests and `pnpm db:test:l03`; pass |
| L04-28 | Capture a payment routed to two queues, then edit one source binding after persistence | Both delivery rows retain the accepted source priority and override values; later binding edits cannot change the payment's already-created alert delivery plan | `0007` plus `0004`/`0010` snapshot columns and disposable PostgreSQL 16 harness; `pnpm db:test:l03`; pass |
| L04-28a | Capture a payment before an exact provider source binding exists | The reserved `__channel_default__` binding routes the payment; if an exact source binding exists, the default route is excluded; persisted delivery rows retain the resolved source snapshot | `0007`, `0028`, `0036`, payment ingress query and disposable PostgreSQL 16 harness; local pass; provider/staging evidence pending |
| L04-29 | Persist a verified webhook, fail the private worker-pump call, then retry the same provider event | The first attempt returns retryable failure after durable persistence; the retry is deduplicated, re-runs the idempotent pump, and returns success only after the worker pump responds successfully | `internal/ingress/handler_test.go`, `internal/ingress/worker_pump_test.go`; separate handler/client tests plus end-to-end local HTTPS and durable-dedup retry tests pass; live cross-service IAM/provider evidence pending |
| L04-30 | Invoke the private payment reconciliation route without authorization and with a bounded synthetic runner | Unauthorized calls fail; a complete bounded pass returns a summary; partial/provider failure returns retryable `503` without claiming unresolved candidates complete | `internal/reconcile/handler_test.go`, `internal/reconcile/runner_test.go`; `go test ./...` and `go vet ./...`; pass; live scheduler/OIDC/provider evidence pending |
| L04-31 | Fetch order payments and recover a paid order through payment-level evidence | Provider collection is bounded and rejects mismatched order/amount/currency; a matching captured payment is persisted through the atomic path and the recovery ledger can only complete after that evidence exists | `internal/provider/razorpay_orders_test.go`, `internal/reconcile/runner_test.go`, `0012_v1_l04_complete_payment_recovery.sql`, `l03_application_behavior.sql`; Go tests and `pnpm db:test:l03`; pass; live provider/staging evidence pending |
| L04-32 | Reconcile a requested refund through the private refund route | Provider refund identity, linked payment, amount and currency must match; processed/failed/reversed states update compensating refund/payment status, while pending remains a no-op and mismatches are retryable manual review | `internal/provider/razorpay_orders_test.go`, `internal/reconcile/refund_test.go`, `0013_v1_l04_refund_reconciliation.sql`, `l03_application_behavior.sql`; Go tests and `pnpm db:test:l03`; pass; live provider/staging evidence pending |
| L04-33 | Deliver distinct `refund.created`, `refund.processed`, then late `refund.failed` events for one provider refund ID | The existing refund row advances to processed once, the payment aggregate reflects the processed amount, and the late failed event cannot regress the processed refund or duplicate its amount | `0014_v1_l04_refund_webhook_status_sync.sql`, `l03_application_behavior.sql`; `pnpm db:test:l03`; pass; live provider/staging evidence pending |
| L04-34 | Start the webhook boundary without a worker pump | The handler fails closed before storage and returns retryable failure; it cannot acknowledge a payment while ready alert delivery has no wake-up path | `internal/ingress/handler.go`, `internal/ingress/handler_test.go`; `go test ./...`; pass |
| L04-35 | Close a queue during payment binding resolution and attempt a delivery insert | Closed queues are excluded before provider persistence; the database rejects a race-created delivery for a closed queue and preserves one open destination | `internal/ingress/sql_store.go`, `0026_v1_l03_open_queue_delivery_guard.sql`, `l03_application_behavior.sql`; `go test ./...`, `pnpm db:test:l03`; pass |
| L04-36a | Record accepted, duplicate, invalid and retryable webhook outcomes and scrape authenticated payment metrics | Webhook outcome counters are bounded and contain no provider/payment identifiers; unknown outcome values collapse to a safe category | `internal/ingress/handler.go`, `internal/observability/metrics.go`, `metrics_test.go`; `go test ./...` and `go vet ./...`; pass |
| L04-36b | Record checkout and payment/refund reconciliation outcomes and scrape authenticated payment metrics | Private handler outcomes are separately observable with bounded labels; unknown kinds/outcomes do not become metric cardinality or data leaks | `internal/checkout/handler.go`, `internal/reconcile/*handler.go`, `internal/observability/metrics.go`, `metrics_test.go`; `go test ./...` and `go vet ./...`; pass |
| L04-36 | Accept a verified webhook and invoke the worker pump | The private HTTP hop carries a bounded `X-BSA-Trace-Id` derived from `razorpay:<provider-event-id>`; no inbound client trace header is used | `internal/ingress/trace.go`, `handler.go`, `worker_pump.go`, ingress tests; `go test ./...`; pass |
| L04-37 | Build the payment service container from its service boundary | A reproducible multi-stage build uses pinned base-image digests, excludes local environment files from its build context, produces a static Linux binary in a distroless non-root image, and embeds no credentials or deployment values | `services/payment-webhook-go/Dockerfile`, `.dockerignore`; pinned `docker build --file Dockerfile --tag bsa-payment-webhook:local .`, non-root image inspection and missing-config smoke pass locally; Cloud Run/IAM/secret/provider evidence remains open |
| L04-38 | Deliver distinct `payment.captured` and `order.paid` events for the same captured payment | Both provider delivery IDs remain independently recorded and processed, but the payment-linked alert/outbox/delivery projection is created exactly once | `0007_v1_l04_webhook_persistence.sql`, `0028_v1_l04_capture_projection_dedup.sql`, `l03_application_behavior.sql`; disposable PostgreSQL harness; pass; provider event semantics cross-checked against Razorpay's payment webhook documentation |
| L04-39 | Deliver dispute created, under-review and duplicate webhook events for a known payment | Dispute evidence is persisted separately, links the known payment, advances monotonically, suppresses duplicate provider events and does not rewrite payment/refund/alert state | `0031_v1_l04_dispute_evidence.sql`, `internal/webhook/payload_test.go`, `l03_application_behavior.sql`; `go test ./...` and `pnpm db:test:l03`; pass; live provider dispute evidence pending |
| L04-40 | Create/reconcile orders and refunds for two channel-linked accounts, then replay a webhook with the wrong or missing `account_id` | Provider API calls carry only the requested channel account; reconciliation reads use the candidate account; wrong/missing webhook attribution fails closed and cannot persist or cross-link financial/alert state | `internal/provider/razorpay_orders_test.go`, `internal/ingress/sql_store.go`, migrations `0034`/`0035`; Go tests and disposable PostgreSQL harness; pass locally; live provider evidence pending |
| L04-41 | Return a permanently invalid signed payload or a durable quarantine result from the persistence boundary | Malformed/unsupported payloads return bounded `400` without invoking the worker pump; a durably quarantined provider event returns `200 quarantined` without invoking the pump; database/provider failures remain retryable `503` | `internal/ingress/handler.go`, `internal/ingress/sql_store.go`, `internal/ingress/handler_test.go`; focused Go tests; provider/deployed evidence remains pending |
| L04-42 | Configure a channel minimum above ₹10 and attempt a below-minimum order through the public and private boundaries | The API rejects early, and the SQL payment-intent boundary rejects a bypass attempt before a provider order can be created | `apps/api/test/app.test.ts`, migration `0043_v1_l03_l04_channel_tip_minimum.sql`, `pnpm db:test:l03`; local pass |
| L04-43 | Query a locally-created order through the public status projection before and after verified payment state changes | The projection returns only donor-safe order state/amount/time, is absent for unknown UUIDs, and never exposes provider or donor fields; payment state remains owned by webhook/reconciliation persistence | migration `0044_v1_l03_public_payment_status.sql`, API/SQL tests; local pass; deployed/provider evidence pending |
| L04-44 | Fetch a provider order through the account-scoped adapter and return an order object whose ID differs from the requested path ID | The provider adapter rejects the response before reconciliation can interpret its status or mutate local state | `internal/provider/razorpay_orders.go`, `internal/provider/razorpay_orders_test.go`; `go test ./...`, `go test -race ./...` and `go vet ./...`; local pass |
| L04-45 | Submit a signed webhook with a missing, oversized or unsafe `x-razorpay-event-id` value | The verifier rejects it before persistence, deduplication or trace emission; no control character or arbitrary separator enters the normal acknowledged path | `internal/webhook/verifier.go`, `internal/webhook/verifier_test.go`; `go test ./...`, `go test -race ./...` and `go vet ./...`; local pass |
| L04-46 | Invoke the verified webhook SQL boundary with an unsafe provider event ID | New webhook evidence is rejected by the database format constraint even if a trusted caller bypasses the Go parser; historical rows remain untouched because the constraint is `NOT VALID` | `0046_v1_l04_webhook_event_id_format.sql`, disposable PostgreSQL L02/L03 harness; local pass |
| L04-47 | Run payment recovery and construct its internal provider-event identity | The recovery key is deterministic and conforms to the same safe format as webhook delivery IDs, so recovery can persist through the shared atomic path after migration `0046` | `internal/ingress/sql_store.go`, `internal/ingress/sql_store_test.go`; `go test ./...`, `go test -race ./...` and `go vet ./...`; local pass |
| L04-48 | Create an annual Creator subscription, observe a first-seen cancelled subscription before its period starts, transition the annual plan to past-due, replay an equal-timestamp state, reprocess the same subscription as active, cancel it, rejoin, and query the customer billing projection | The server stores ₹399/month-equivalent as the authoritative price, records 10-months-paid/12-months-service, grants the approved initial protection window only for an active subscription, publishes one matching server-owned entitlement version even after active reconciliation, adds only the bounded 30-day grace period, ignores equal-timestamp replays, allows cancellation to end protection even before period start, prices a later rejoin at current price, and selects the newer active subscription over the cancelled predecessor; dunning/cancellation do not publish an unapproved access rewrite | `0048_v1_l04_subscription_billing_projection.sql`, `l03_application_behavior.sql`; `pnpm db:test:l03`; local pass; Razorpay subscription webhook/plan mapping, access-transition policy and deployed evidence pending |
| L04-49 | Register a server-owned subscription link, receive an activated subscription webhook, replay the same provider event, and inspect the billing projection | Only the linked channel/approved plan is used; provider plan mismatch, unknown link and incomplete authorization evidence cannot change access; the first event projects active state once and the duplicate delivery is suppressed | `0049_v1_l04_subscription_webhook_projection.sql`, `internal/webhook/payload.go`, `internal/ingress/sql_store.go`, `sql_store_integration_test.go`, `l03_application_behavior.sql`; `pnpm db:test:l03`, Go race/vet; local pass; provider creation/plan IDs, sandbox/live and deployed evidence pending |
| L04-50 | Create a subscription through the provider adapter using a server-selected plan/account and inspect mismatched/invalid responses | The adapter sends only bounded server-owned fields to `POST /v1/subscriptions`, includes `X-Razorpay-Account` only for `connected` scope, omits it for `platform` scope, rejects invalid input before network access and rejects a provider response whose subscription plan differs from the requested plan | `internal/provider/razorpay_subscriptions.go`, `internal/provider/razorpay_orders_test.go`; `go test ./...`, `go test -race ./...`, `go vet ./...`; local pass; approved live plan catalogue, checkout/link-registration integration, provider sandbox/live and deployed evidence pending |
| L04-51 | Register and project a platform-scope subscription for a channel that has no creator tipping account, then revoke the platform account and retry link registration | The server accepts the link only when the referenced platform payment account is active, stores immutable platform scope, projects the verified subscription through the existing link-first webhook path, rejects a revoked platform account, and preserves the platform account reference; connected scope still requires an active channel payment account | `0050_v1_l04_platform_subscription_account_boundary.sql`, `l03_application_behavior.sql`, `internal/ingress/sql_store.go`; `pnpm db:test:l03`, `go test -race ./...`, `go vet ./...`; local pass; production platform-account provisioning, provider approval and deployed secrets pending |
| L04-52 | Repeat paid-plan checkout with the same authenticated idempotency key, force a provider timeout after creation, fail link registration, and deliver a webhook before link repair | One durable subscription-creation intent is retained; no blind duplicate provider call is made after an ambiguous result; provider identity/link repair is retryable; early webhook is durably quarantined and cannot grant entitlement until the server-owned link exists | `0051_v1_l04_subscription_creation_intents.sql`, `0052_v1_l04_quarantined_subscription_replay.sql`, `internal/subscription/service{,_test}.go`, `internal/subscription/handler{,_test}.go`, `internal/ingress/sql_store.go`, `apps/api/src/db/payment-subscription-client.ts`, `apps/api/src/routes/alerts.ts`, `l03_application_behavior.sql`; Go race/vet, API 54/54, build, OpenAPI 32 paths and `pnpm db:test:l03` pass locally. Provider sandbox/live, approved plan catalogue, deployed OIDC/IAM/secrets, live retry/reconciliation and staging recovery remain open |
| L04-53 | Read payment and refund reconciliation candidates through the real Go SQLStore after account-attribution migrations | Both adapters return the immutable connected account reference together with provider identities, amount and currency; no process-wide account value is needed and the pre-0034/0035 function signatures cannot pass unnoticed | `internal/reconcile/sql_store_integration_test.go`, migrations `0034`/`0035`, `packages/db/tests/run-l03-application-behavior.sh`; `go test ./...`, `go test -race ./...`, `go vet ./...`, `pnpm db:test:l03`; local synthetic pass. Provider and deployed/staging evidence remain open |
| L04-54 | Invoke the subscription-creation SQL boundary with a valid payment-service role but a user/channel membership mismatch | The security-definer function rejects both a non-member user on an owned channel and an owned user on another channel with `42501`; a valid service identity cannot turn caller-supplied IDs into authorization | `0051_v1_l04_subscription_creation_intents.sql`, `l03_application_behavior.sql`; `pnpm db:test:l03`; local synthetic pass |
| L04-55 | Re-run the complete current L04 boundary after the overlay security migration and payment fixture-boundary correction | Payment/worker normal, race and vet checks, API/build/contracts, and the complete disposable PostgreSQL migration chain pass together; no new locally verifiable L04 gap remains | Fresh audit 2026-08-15; `pnpm db:test:l03`, Go tests/race/vet, `pnpm test`, `pnpm build`, `pnpm contracts:validate`; pass locally; provider/deployment/staging/independent review pending |
| L04-56 | Start the payment container without required configuration and inspect the runtime image | Startup returns one bounded missing-environment error without a panic stack; image runs as non-root with the intended static entrypoint | `cmd/payment-webhook/main.go`, `main_test.go`, `Dockerfile`; Go tests/race/vet pass; `docker build --tag bsa-payment-webhook:local .`, non-root image inspection and missing-config smoke pass on 2026-08-15. Cloud Run/IAM/secret/provider evidence remains pending |
| L04-57 | Stall the private worker-pump HTTP hop after durable webhook persistence | The payment-to-worker call is bounded by an independent 5-second client deadline and returns retryable failure; the durable provider event remains eligible for provider redelivery/recovery and is never acknowledged by the timeout path | `internal/ingress/worker_pump.go`, `worker_pump_test.go`; focused Go ingress tests pass; deployed latency, IAM and provider retry evidence remains pending |

## Commands and result

```text
cd /Users/sukhdevsingh/Workspace/Bharat Studio/bharatstudio-alerts/services/payment-webhook-go
gofmt -w internal/provider/razorpay_orders.go internal/provider/razorpay_orders_test.go
go test ./...
ok   .../internal/ingress
ok   .../internal/provider
ok   .../internal/webhook
```

## Not yet satisfied

Race-enabled local verification (`go test -race ./...`) passes for all payment packages; this is concurrency-safety evidence only and does not substitute for provider or deployed staging evidence.

- Deployed database evidence for the verified raw-payload path, provider sandbox and runtime service wiring; the disposable PostgreSQL integration test now exercises the real pgx/database/sql `SQLStore` path through `record_verified_payment_webhook`.
- Provider checkout handoff from the public client; the public order route and client initiation flow exist, while Razorpay public-key/provider test-mode configuration remains open.
- Deployed private checkout IAM/secret evidence and Razorpay/provider staging.
- Refund/reversal/dispute and payment-recovery paths are locally implemented and tested; live provider behavior, scheduler delivery and staging evidence remain open.
- Live payment-level fetch/verified persistence for a missed paid-order webhook, plus private endpoint/scheduler wiring and staging evidence.
- Razorpay Technology Partner/connected-account approval and provider test-mode evidence.
- Independent fresh L04 review and staging shadow comparison.

### L04-53 — Go SQLStore subscription-creation adapter round trip

**Result:** PASS (local synthetic integration evidence, 2026-08-15)

The disposable PostgreSQL runner now exercises the actual Go SQLStore methods
for the subscription-creation boundary. It proves create, idempotent replay,
provider claim, provider attachment and canonical link registration, then reads
back the durable linked intent and provider subscription identity. The
synthetic provider response is in-process; no Razorpay network or credentials
are used.

**Command:** pnpm db:test:l03

**Not proven by this case:** Razorpay TP approval, provider sandbox/live plans,
real recurring billing, deployed service identity/IAM/secrets, production
reconciliation, staging recovery or independent review.

### L04 local regression update — 2026-08-15

The payment service rerun after L04-57 passed `go test ./...`,
`go test -race ./...` and `go vet ./...`. The tightened stalled-call test
distinguishes the 50 ms synthetic client deadline from a 500 ms stalled
server response; this remains local boundary evidence and does not prove
deployed Cloud Run timeout, IAM or Razorpay retry behavior.

### Full local boundary rerun — 2026-08-15

`go test -race ./...` passed for the payment service. The disposable
`pnpm db:test:l03` run passed the payment, refund, subscription,
account-attribution and worker-store integration slices, together with
`L02_SECURITY_REMEDIATIONS=PASS` and `L03_APPLICATION_BEHAVIOR=PASS`.
The Alerts API suite passed 54/54, `pnpm contracts:validate` passed all 11
fixture mappings and the 32-path OpenAPI document, and `pnpm build` passed.
This is local synthetic evidence; Razorpay approval/provider sandbox or live
execution, deployed IAM/secrets, Cloud Run, scheduler, staging recovery and
independent review remain open.

### L04-58 — Internal payment-service response-boundary validation

**Result:** PASS (local synthetic API evidence, 2026-08-15)

The Creator API payment clients reject malformed private Go responses before
financial or subscription values reach public routes. The order client checks
the v1 envelope, UUID local order ID, bounded provider order ID, exact expected
INR amount, approved status and unknown-field rejection. The subscription
client checks provider identity, approved tier/interval, positive integer
pricing, the ten-month charge relationship and HTTPS-only checkout URLs.

**Command:** `pnpm --filter @bharatstudio/alerts-api test && pnpm --filter @bharatstudio/alerts-api build`

**Not proven by this case:** deployed OIDC/IAM, Razorpay provider behavior,
sandbox/live checkout, recurring billing, staging recovery or independent
review.
### L04-59 — Payment-intent idempotency mismatch after conflict

**Result:** PASS (disposable PostgreSQL evidence, 2026-08-15)

Calling `app_private.create_payment_order_intent` with an existing
`(channel, environment, idempotency_key)` and a changed amount/message now
fails with the documented `23505` mismatch error. The same migration also
rejects unsafe future idempotency-key formats while retaining historical rows
for later review. The test runs through the complete disposable migration
chain in `pnpm db:test:l03`.

The runner applies the complete post-L02 migration directory in version order,
including `0056`, rather than relying on a manually maintained final-migration
list.

**Not proven by this case:** Razorpay provider behavior, deployed IAM/secrets,
staging concurrency or production migration execution.
### L04-60 — Private checkout and subscription idempotency-key format

**Result:** PASS (local Go handler evidence, 2026-08-15)

The private tip-checkout and paid-subscription handlers reject present-but-
unsafe idempotency keys before calling their service interfaces. Header/body
mismatch and missing-key behavior remain unchanged. `go test ./...`,
`go test -race ./...` and `go vet ./...` pass.

**Not proven by this case:** deployed OIDC/IAM, provider execution, staging
retry behavior or production migration rollout.

### L04-61 — Payment ingress to Alert Worker pump HTTP boundary

**Result:** PASS (local TLS HTTP boundary evidence, 2026-08-16)

The payment ingress handler was exercised with the real `WorkerPumpClient`
against a TLS test server. The test asserts the canonical private pump path,
propagates the server-derived Razorpay trace ID, persists the verified webhook
through the durable store, and returns success after the pump accepts the
request. A worker `503` is propagated as a retryable provider response with a
`Retry-After` value; the already-persisted webhook remains safe for replay.

**Not proven by this case:** deployed OIDC/IAM, Cloud Run routing, real Cloud
Tasks, Razorpay delivery, provider sandbox/live behavior or staging recovery.
