# L04 — Go payment boundary

**Status:** `Local implementation and persistence slices passing — provider approval, deployment, staging and independent review gates pending`  
**Level:** L3  
**Owner:** Payments / Go / security  
**Depends on:** L01–L03, Razorpay TP approval evidence  
**Blocks:** public paid tips and L10

## Objective

Rebuild the creator-direct Razorpay money boundary in Go without losing the proven correctness of the legacy TypeScript behaviour.

## Current implementation evidence — 2026-08-14

- Added `bharatstudio-alerts/services/payment-webhook-go`, a standalone Go module for the payment boundary.
- Implemented raw-body HMAC-SHA256 verification using `X-Razorpay-Signature`; parsed or reformatted request bodies fail verification.
- Implemented mandatory, case-insensitive `x-razorpay-event-id` extraction with bounded length; missing or oversized identities fail closed.
- Implemented fail-closed handling for missing webhook secret configuration and redacted-only `rawBodyHash` output.
- Added a fail-closed HTTP ingress adapter with bounded raw-body reads, no store call on invalid signatures, 503 + `Retry-After` when atomic persistence is unavailable, and 200 only after the store confirms durable acceptance or deduplication.
- Added pure and ingress tests for valid verification, changed-body rejection, missing identity, invalid signature, oversized identity/body, missing secret, persistence failure and duplicate delivery; `go test ./...` passes.
- Added a server-only Razorpay Orders API adapter with Basic Auth, INR/₹10 validation, receipt/notes bounds, HTTPS-only configuration, bounded responses, request/response amount-currency-receipt matching, `FetchOrder` support for later reconciliation, and retry classification for transport/timeout/429/5xx failures.
- Added provider contract tests using a local fake HTTP server for request shape/authentication, order parsing, pre-network validation, response mismatch rejection, bounded provider errors and fail-closed client configuration; `go test ./...` passes.
- Tightened Razorpay webhook delivery identity validation: the required `x-razorpay-event-id` is now restricted to bounded alphanumeric, underscore, hyphen and dot characters before it can become a deduplication key or trace input. Unsafe/control-character values fail closed and are covered by verifier tests.
- Added migration `0046_v1_l04_webhook_event_id_format.sql` as database defense-in-depth. New or updated webhook rows must satisfy the same safe event-ID format; the constraint is `NOT VALID` so existing evidence is preserved and no historical rows are rewritten.
- Updated the internal payment-recovery evidence key from colon-delimited `recovery:<order>:<payment>` to deterministic database-safe `recovery_<order>_<payment>`, matching the new webhook event-ID constraint. Added a unit regression for determinism and safe format.
- Hardened the provider fetch boundary so `FetchOrderForAccount` rejects a response whose order ID differs from the server-requested path ID before reconciliation can interpret its status. Added a regression test for the mismatched response; payment Go tests, race tests and vet pass.
- Added migration `0006_v1_l04_payment_order_intents.sql` with active creator payment-account context, local order-intent idempotency, provider receipt/order uniqueness, expiry/status fields, and separate app/payment security-definer functions for intent creation and provider-order attachment. The intent is durable before provider I/O; attaching a provider order is repeat-safe and leaves `payments` for captured provider payments only.
- Added a short provider-creation claim lease to `0006`: only one payment replica may call Razorpay for a pending local intent at a time; the lease is cleared on attachment and can be reclaimed after expiry for crash recovery.
- Added a tolerant Razorpay payload normalizer for payment/order, refund, subscription and dispute webhook families. It retains only state-machine fields, rejects malformed/trailing/unsupported payloads, and preserves the raw signed body as the evidence source; webhook parser tests pass.
- Corrected event-family precedence so Razorpay `payment.dispute.*` events are classified as disputes before the broader `payment.*` match. Added migration `0031_v1_l04_dispute_evidence.sql` with append-only, RLS-protected dispute evidence and monotonic status updates for created/under-review/action-required/won/lost/closed events. Dispute persistence links a known payment when available, retains evidence when it is not, and never changes the original payment, refund or alert ledger. The disposable PostgreSQL harness proves duplicate event suppression and non-regressing status.
- Added migration `0007_v1_l04_webhook_persistence.sql` with payment account/order matching, normalized provider-event recording, payment/refund state transitions, provider-event deduplication, amount/currency checks, and atomic alert event/outbox/per-queue delivery creation for captured payments. Disposable PostgreSQL evidence passes this path with synthetic data.
- Added `ingress.SQLStore`, which parses the verified raw body, resolves local intent/binding context using the service's configured environment/account, generates server-side IDs and delegates the financial/outbox write to the private atomic function. It never trusts webhook-supplied channel/account identity; package tests compile and pass.
- Corrected account routing for multi-channel creator-direct operation. The local intent's immutable `connected_account_ref` now travels through checkout into Razorpay's `X-Razorpay-Account` header; order/payment/refund reconciliation reads use the candidate's account; verified webhook attribution is derived from the signed payload `account_id` and no longer from one process-wide account variable. Migrations `0034` and `0035` carry account attribution into payment/refund reconciliation candidates. Missing webhook account attribution fails closed. Local Go tests and the disposable SQL harness pass; provider sandbox and Razorpay approval remain open.
- Added `internal/db.Open` with pgx/database/sql, fail-fast DSN/Ping and bounded connection-pool configuration; no production DSN is stored or tested.
- Added bounded donor display-name/message fields to the local payment intent and merged them into the immutable alert payload during captured-payment persistence; the Razorpay webhook is not treated as the source of local donor text.
- Added immutable `alertConsent` to the local payment intent and carried it through the public API, private Go checkout, SQL persistence and webhook projection. A paid tip with consent disabled remains in the payment ledger/history but is processed without creating an on-stream alert, outbox row or queue delivery; idempotency includes the consent choice.
- Added the channel-specific minimum-tip guard in migration `0043_v1_l03_l04_channel_tip_minimum.sql`. The public API carries the configured minimum to the donor surface and rejects below-minimum requests early; the payment database trigger independently rejects them at intent insertion so stale clients or direct private callers cannot bypass creator policy. The ₹10 platform floor and provider-side amount checks remain in force.
- Extended the disposable webhook evidence to cover partial-refund aggregation, duplicate refund-event suppression and final refund completion. Refunds remain append-only evidence and payment status is derived from processed refund totals.
- Added the public Creator API order boundary: it resolves the canonical channel by handle, requires an `Idempotency-Key`, refuses closed channels, creates a stable provider receipt from the channel/key pair, forwards only bounded order fields to the payment service contract, and fails closed when the payment service is not wired.
- Added the Creator API server-to-server payment client using Google OIDC ID tokens, HTTPS enforcement outside development, a fixed private route, timeout-bound requests and strict response validation. Staging/production configuration now fails startup if the private payment origin or audience is absent.
- Added the private Go checkout HTTP handler with OIDC authorization injection, strict JSON/trailing-data rejection, environment and header/body idempotency matching, expiry/₹10/INR checks, generic provider-error responses and the reviewed `CreateTipOrderResponse` shape.
- Added defense-in-depth for the approved 15-minute local checkout lifetime: the private Go boundary rejects future expiries beyond the platform maximum, and migration `0045_v1_l04_payment_intent_expiry_cap.sql` enforces the same cap in the security-definer database write path and table constraint. The provider request intentionally does not send Razorpay's unsupported `expire_by` field. Handler and disposable PostgreSQL regression tests pass.
- Corrected provider-creation lease tokens to UUID format. The SQL claim/attach functions accept UUID tokens; the previous hexadecimal token generator would have passed mocks but failed against the real database.
- Added a fail-safe reconciliation decision core. A fetched `paid` order queues payment-detail recovery rather than marking the local payment paid or creating an alert; an unpaid order past the local expiry can expire only the local intent; mismatched and unknown provider states go to retry/manual review. The core is provider-status policy only and is not a substitute for the verified webhook/payment-level persistence path.
- Added migration `0008_v1_l04_reconciliation.sql` and a Go SQL adapter/runner. It lists bounded candidates, atomically expires only unpaid local intents, and creates an idempotent `payment-recovery` work item for an observed paid order. Provider failures produce a retryable partial result; no candidate is silently discarded. Added private `POST /internal/v1/reconciliation/payments` runtime wiring in the payment service; the handler owns the provider client and returns retryable `503` on partial/provider failure. Cloud Scheduler now targets this route in the disabled template; IAM, provider test mode and staging evidence remain open.
- Added the provider-documented order-payment fetch (`GET /v1/orders/:id/payments`) with strict payment/order/amount/currency/status validation. The reconciliation runner can now fetch a matching captured payment, reuse the atomic payment/outbox persistence path with a deterministic internal recovery evidence key, and complete the durable recovery work item only after payment-level persistence succeeds. Migration `0012` enforces that completion cannot occur without captured/refunded payment evidence.
- Added private refund reconciliation at `POST /internal/v1/reconciliation/refunds`. It lists only local requested refunds, fetches each refund by provider ID, validates linked payment/amount/currency, and applies only processed/failed/reversed compensating state transitions through migration `0013`; migration `0014` also synchronizes webhook-driven state changes. It never creates refunds or rewrites historical tip/alert payloads.
- Added migration `0014_v1_l04_refund_webhook_status_sync.sql`: a later distinct refund webhook now advances the existing provider-refund row through a monotonic trigger (created/requested → processed, failed, or reversed) and recomputes the payment aggregate without creating a second refund or regressing a processed/reversed refund on a late failure event.
- Extended the captured-payment projection so each accepted queue delivery stores the resolved source priority and per-source override snapshot alongside its binding/sequence. This keeps the payment-to-alert boundary immutable even if a creator edits queue bindings after the payment is accepted; the disposable SQL proof covers the two-queue case and post-acceptance binding mutation.
- Payment routing now supports the reserved `__channel_default__` binding for a channel’s normal tip flow. The webhook boundary uses it only when no exact provider payment binding exists; exact bindings remain authoritative, and the persistence function rejects a stale default route if an exact route has since been configured. This makes pre-payment queue configuration usable without weakening L31/L32 source correlation.
- Added a private alert-worker pump client to the webhook ingress. After verified persistence, including a deduplicated retry, the payment service must successfully wake the bounded ready-delivery scan before returning provider success. A pump failure returns retryable `503`; stable Cloud Tasks names make partial enqueue safe on the provider retry. Production requires the worker pump URL/audience and service-account IAM; no live call was made here.
- Added `cmd/payment-webhook/main.go` and a private-service bootstrap: fail-fast required environment, bounded pgx pool, Google ID-token audience validation, Razorpay webhook ingress, private checkout route, health endpoint and HTTP timeouts. It does not run migrations or log credential values.
- Added database-backed `/readyz` and graceful SIGTERM/SIGINT shutdown to the payment runtime. Readiness returns `503` when the live DB probe fails, while `/healthz` remains a process liveness check; shutdown drains in-flight HTTP work within a bounded window. This is compile/test evidence only until deployed Cloud Run probe and drain behavior is exercised.
- Added an independent 5-second deadline to the private payment-to-worker pump client. A stalled worker hop returns retryable failure before the payment service's outer HTTP timeout; the previously durable verified event remains available for provider retry and recovery. The client timeout is bounded network protection, not an acknowledgement or deletion path; local ingress tests cover the stalled-call bound. Deployed latency tuning and Cloud Run/provider retry evidence remain open.
- Extracted the readiness contract into a tested observability handler: GET-only, bounded DB probe, generic `503` failure body and no dependency detail leakage. The payment service's `/readyz` and `/healthz` distinction is now unit-tested; deployed Cloud Run probe behavior remains open.
- Corrected the webhook receipt boundary to require the worker-pump dependency. A missing pump now fails closed before persistence, and the regression test proves the handler cannot return provider success while accepted alert delivery has no dispatch wake-up path.
- Added the closed-queue destination guard: payment binding resolution joins only open queues, while the database migration rejects race-created delivery rows for closed queues and prevents closing the final open queue.
- Added bounded server-derived trace propagation from a verified Razorpay event to the private worker-pump HTTP hop. The trace is derived from the verified provider event ID, validated before emission, and never accepted from a client header.
- Added authenticated, bounded webhook business metrics for accepted, duplicate, invalid, retryable and not-configured outcomes. The labels contain no provider event IDs, order IDs, account references, payment data or donor data; local ingress/metrics tests pass.
- Added bounded checkout and payment/refund reconciliation outcome metrics, wired at the private handlers. They are operational signals only; they do not change payment state or replace durable reconciliation evidence.
- Added a reproducible multi-stage `services/payment-webhook-go/Dockerfile`: Go 1.26 build stage, static Linux binary, distroless non-root runtime, and a service-local `.dockerignore`. The image builds locally as `bsa-payment-webhook:local`; this is container-packaging evidence only and does not establish Cloud Run/IAM/secret/provider readiness.
- Hardened the payment-service bootstrap so missing required environment and invalid positive-integer settings return bounded errors instead of panicking with a startup stack trace. Added command-level tests for missing configuration and helper validation. The rebuilt `bsa-payment-webhook:local` image runs as `nonroot:nonroot`, and an empty-environment smoke exits with only `missing required environment: PAYMENT_ENVIRONMENT`. This is local startup/container evidence only; Cloud Run, IAM, Secret Manager, provider and staging proof remain open.
- Pinned the Go build and distroless runtime stages to the exact digests used by the verified local build, removing floating base-image resolution from the payment artifact. The pinned image rebuild passes; patching the digest requires a deliberate dependency/security update and repeat of the image checks.
- Added `.env`/`.env.*` exclusions to the payment Docker build context so local environment files cannot be sent to the container builder; the checked-in `.env.example` remains documentation only and is not needed by the build.
- Added business-effect deduplication for distinct Razorpay capture webhook IDs. [Razorpay documents](https://razorpay.com/docs/webhooks/payments/) `order.paid` and `payment.captured` as event types for the same captured payment; both provider delivery records remain traceable, while migration `0028_v1_l04_capture_projection_dedup.sql` ensures only one payment-linked alert/outbox/delivery projection is created.
- Added a disposable PostgreSQL integration test for `ingress.SQLStore`. It opens the real pgx/database/sql driver, creates and claims an intent, attaches a provider order, persists a captured webhook through the private SQL function, and verifies the second delivery is deduplicated. The test is synthetic and runs only with the `integration` build tag from the L03 database harness.
- The SQLStore integration now also exercises the alert-consent=true path and a real payment binding. JSONB override values are preserved as JSON objects through the `database/sql` boundary, and the resulting alert/outbox/delivery projection is asserted as exactly one alert with one delivery before duplicate replay.
- Added local end-to-end HTTPS boundary tests between the payment webhook handler and its worker-pump client. They verify the actual handler/client composition, `X-BSA-Trace-Id` propagation derived from the verified Razorpay event ID, JSON POST contract, success handling, retryable `503` behavior when the worker endpoint is unavailable, and a provider-style retry that reuses durable deduplication after the first pump failure. This remains local synthetic evidence; Google OIDC/IAM, deployed worker behavior, Cloud Tasks and provider staging are still open.
- Added the subscription webhook projection boundary in migration `0049_v1_l04_subscription_webhook_projection.sql`. A server-created `channel_subscription_links` row binds the provider subscription/account/plan to the channel and approved tier/price; subscription webhooks must match that link and the provider plan ID before applying the existing subscription state machine. Authenticated events with null period fields, unknown links, plan mismatches or incomplete periods are durably recorded as quarantined and cannot grant/revoke access. The Go parser now retains `plan_id`, `current_start`, `current_end` and `charge_at`, and `SQLStore` routes subscription events to the dedicated function rather than the generic payment path. Local SQLStore integration and duplicate-webhook evidence pass; provider subscription creation, live plan IDs and deployed/reconciliation evidence remain open. The event fields are aligned to [Razorpay's subscription webhook entity](https://razorpay.com/docs/webhooks/subscriptions/).
- Added a server-owned Razorpay Subscription API adapter in `internal/provider/razorpay_subscriptions.go`. It validates the provider account reference, explicit `platform` versus `connected` account scope, provider plan identifier, bounded cycle/quantity values and notes before `POST /v1/subscriptions`; sends only server-selected fields with Basic Auth; sends `X-Razorpay-Account` only for connected-account subscriptions; and rejects a response whose entity, subscription ID, plan ID or status is invalid. Platform plan subscriptions therefore do not require a creator tipping account, while creator-direct subscriptions remain explicitly account-routed. Provider contract tests pass, but the adapter is not a live plan catalogue, checkout flow, subscription-link registration call or provider-approval evidence.
- Added migration `0050_v1_l04_platform_subscription_account_boundary.sql` to make that distinction durable. `platform_payment_accounts` is the server-owned registry for BharatStudio subscription revenue accounts; `channel_subscription_links.provider_account_scope` records the immutable scope for each link; and the canonical nine-argument link-registration function requires an active platform registry row for `platform` links or an active channel `payment_accounts` row for `connected` links. The existing eight-argument function remains a connected-account compatibility wrapper. The disposable SQL harness proves a platform subscription can be linked and projected without a channel tipping account, while connected links retain their account check.
- Classified persistence outcomes at the webhook boundary: permanently malformed/unsupported verified payloads return bounded `400` without waking dispatch, while a database-recorded quarantine returns `200 quarantined` without waking dispatch. Only retryable persistence/pump failures return `503`, preventing invalid signed deliveries from entering an endless provider-retry loop while preserving durable quarantine evidence.

### Paid-plan checkout integration — local boundary implemented; launch gates remain open

The provider `POST /v1/subscriptions` adapter and link-registration function
are now wrapped by a server-owned, authenticated boundary for the paid
Pro/Creator/Studio plans. The local implementation is deliberately not
considered launch-ready until provider, deployment, recovery and staging
evidence exists:

1. The Creator API accepts only an authenticated channel, approved tier and
   monthly/annual interval. It resolves the plan ID, price, account scope and
   billing terms from server configuration; the browser cannot select a
   Razorpay plan ID, account reference, account scope or price.
2. Before provider I/O, the payment service records a durable subscription
   creation intent keyed by channel, environment and an idempotency key. The
   intent stores the approved plan snapshot, requested interval, account scope,
   and lifecycle state. A repeated request returns the same in-progress or
   completed result rather than starting a second purchase.
3. After Razorpay returns a validated subscription, the service durably stores
   the provider subscription identity and registers the immutable
   `channel_subscription_links` row before returning a checkout projection.
   The link remains the only authority that allows a later signed webhook to
   change billing state.
4. If provider creation has an ambiguous transport result, the service must
   not blindly retry a non-idempotent provider call. It records a pending
   recovery state and reconciles by the server-owned intent/notes/provider
   lookup or sends the case to manual review. If link registration fails after
   provider creation, the provider identity remains durable and a private
   repair/reconciliation path retries link registration; the customer is shown
   pending rather than receiving an unlinked success.
5. A provider webhook that arrives before local link registration remains
   durably quarantined and is replayable after repair. It cannot grant access
   from provider payload fields alone.

The local slice is implemented in migration `0051_v1_l04_subscription_creation_intents.sql`,
the quarantined replay migration `0052_v1_l04_quarantined_subscription_replay.sql`,
`internal/subscription/service.go`, `internal/subscription/handler.go`,
`internal/subscription/catalog.go`, `internal/ingress/sql_store.go`, the
Creator API payment-subscription client and the authenticated billing route.
Local tests cover repeated idempotency, provider ambiguity without blind retry,
provider identity/link repair, link failure recovery, strict private request
validation, server-owned catalog resolution, and early-webhook quarantine and
replay. The slice is not yet launch-ready because approved Razorpay test/live
plan IDs, provider approval, deployed OIDC/IAM/secrets, sandbox/live provider
flows, production reconciliation and staging recovery evidence remain open.

These are still boundary slices. The package is executable locally, but it does not yet have deployed private-service/IAM evidence, live orders/events against production infrastructure, refund/reconciliation completion, or Razorpay Technology Partner/provider readiness.

## Scope

- Public order creation contract from Creator API to payment service.
- HMAC webhook verification, Razorpay delivery deduplication using `x-razorpay-event-id`, immutable event ledger/outbox, account attribution, receipt status and audit logging.
- Refund/dispute/reversal handling, payment-recovery work-item consumption and safe provider status recovery under the private scheduler route.
- Subscription mirror/webhook state, price protection fields and customer-visible billing state—not payment initiation from clients.

## Tasks

1. Turn legacy tips/webhook/refund tests into contract-level characterization cases; add duplicate, delayed, reordered, malformed, timeout and provider retry cases.
2. Implement Go provider adapter with exact raw-body HMAC handling, timestamp/replay controls where provider supports them, explicit `x-razorpay-event-id` extraction, server-resolved `X-Razorpay-Account` routing, idempotency rules and redacted logs.
3. Use the case-insensitive HTTP header `x-razorpay-event-id` as the webhook delivery key after signature verification. Persist it separately from payment, refund, subscription and dispute IDs. Enforce a database uniqueness constraint scoped to provider, connected account/environment and event ID. Never derive a deduplication key from `Date.now()`, randomness, request timing or a trace ID. Missing-header behaviour must be explicit: reject/retry or quarantine; never silently synthesize a timestamp key.
4. Persist verified payment events and outbox records atomically before returning success. If persistence cannot complete before deadline, return retryable failure; never acknowledge then promise to process later.
5. Separate immutable gross tip, provider fees, platform fee disclosure and creator-direct settlement attribution. Do not add Enterprise allocations/splits.
6. Implement refund/reversal/dispute state transitions as compensating evidence. Suppress/reconcile alerts as approved, never rewrite historical payment data. Disputes are stored separately from settlement state; no lost/won event may silently mutate a tip or alert.
7. Build private status/reconciliation endpoints with OIDC/service identity; scheduler invokes the payment-owned reconciliation route but does not mutate data itself.
8. Verify Razorpay Technology Partner, connected-account, webhook attribution, refund and reconciliation scenarios in provider test mode; record dated evidence.
9. Shadow compare Go results with legacy behaviour using synthetic/sandbox events before cutover; only one service may acknowledge a real provider webhook.
10. Keep the public API and private Go checkout contract aligned with `contracts/openapi/v1.yaml`; the API must never accept a provider order ID or payment-captured state from the browser.
11. Reconcile stale local intents by fetching the provider order, validating immutable amount/currency/order/receipt evidence, and applying the safe decision policy: no-op while open, expire only unpaid local intents after expiry, queue payment-level recovery for paid orders, and quarantine/manual-review unknown or mismatched states.
12. After durable webhook persistence, invoke the private alert-worker pump; return retryable failure when the pump is unavailable or partially fails so provider retry can repeat the stable, idempotent scan.
13. Keep later distinct refund webhook deliveries synchronized with the existing provider-refund row; do not let deduplication of the business refund entity suppress a legitimate state transition.
14. Resolve payment bindings only against open queues; a queue lifecycle race must fail retryably before a new delivery is persisted rather than creating a destination that dispatch will suppress.
15. Preserve a redacted trace identifier across the webhook-to-worker internal hop; trace headers are server-derived and bounded, never financial or personal data.
16. Use the server-owned Subscription adapter only after the account scope, provider account reference and approved tier/interval-to-Razorpay-plan mapping are resolved; use the canonical nine-argument `register_channel_subscription_link` contract to persist the returned provider subscription before any provider webhook can change billing state. Platform-scope links must resolve an active `platform_payment_accounts` row; connected-scope links must resolve an active channel `payment_accounts` row. Never let a browser select a provider plan ID, account scope, account reference or tier.
17. Implement the paid-plan creation/link-registration flow as a separate idempotent boundary. Persist a subscription creation intent before provider I/O, attach the returned provider identity and link it through the canonical function, and make ambiguous provider outcomes/early webhooks recoverable without blind duplicate creation or premature entitlement grant.
18. Expose that flow only through the private OIDC payment-service route and authenticated Creator API route. The browser supplies tier/interval and an idempotency key; the payment service owns account scope, plan IDs, monthly-equivalent price snapshots, annual 10-month charge/12-month service terms, provider identity attachment and recovery status. Annual Razorpay plan IDs carry the ten-month charge while the local billing projection stores the monthly-equivalent tier price; the response exposes both. Missing catalog entries fail closed; no provider credentials or account references cross the Creator API boundary.
19. Keep the database authorization boundary independent of the private service identity: the subscription-creation function must verify that the supplied user is an active `owner` or `admin` member of the supplied channel before persisting an intent. A valid `bsa_payment` caller, an arbitrary user ID, or an arbitrary channel ID must not bypass that membership check. The disposable L03 harness proves both mismatch directions are rejected with `42501`.

## Acceptance criteria

- Signature, duplicate, malformed, outage, retry, refund and reversal tests pass.
- Two deliveries carrying the same `x-razorpay-event-id` create one provider-event record and one financial effect, including concurrent delivery; distinct provider event IDs remain independently traceable even when they reference the same business entity.
- Missing or malformed provider event identity follows the documented quarantine/retry policy and cannot enter the normal acknowledged path.
- Verified event + ledger + outbox are atomic and traceable.
- No payment event is lost or double-applied under provider retry/concurrency.
- Distinct `order.paid` and `payment.captured` deliveries for the same payment remain separately traceable but cannot create duplicate alert/outbox effects.
- Creator-direct only; no Enterprise funds movement or split functionality.
- Every provider order, recovery read, refund read and webhook evidence row is scoped to the immutable channel-linked account; a missing or mismatched account cannot fall back to a global process account.
- Platform plan subscriptions and creator-direct tip payments remain separate account scopes: platform subscriptions require an active server-owned platform account registry row and do not require a creator tipping account; connected tip/subscription flows require the channel's active connected account. The scope and provider account reference are immutable in the subscription link used for webhook projection.
- Provider and legal/financial launch gates have evidence, not assumptions.
- Public checkout returns an order only after the private payment service confirms local intent/provider-order attachment; missing service wiring returns a retryable failure and cannot create a browser-only order.
- A reconciliation pass cannot directly create a payment or alert from an order-level `paid` status; it must produce a durable payment-recovery work item for payment-level evidence.
- A newly accepted webhook cannot receive a successful provider response while its ready delivery pump invocation has failed; duplicate webhook retries may safely re-run the pump.
- A payment cannot create a new delivery for a closed queue, including when queue closure races binding resolution; an active channel retains at least one open queue.
- Distinct later refund webhook IDs advance the same provider-refund record exactly once, preserve terminal processed/reversed state against a late failed event, and recompute the payment aggregate without duplicating the refund amount.
- Dispute webhook IDs are recorded exactly once in separate append-only dispute evidence; known payments are linked when available, dispute status transitions are monotonic, and dispute events never rewrite historical payment, refund or alert data.
- Paid-plan checkout is server-owned and idempotent: repeated authenticated requests cannot create duplicate local intents or silently create duplicate provider subscriptions; a provider timeout after creation remains pending/reconcilable, link-registration failure leaves durable repair state, and an early webhook cannot grant access before the server-owned link exists.

## Rollback

Keep the legacy path disabled-but-available in staging only. Production cutover uses one endpoint, a provider rollback plan, reconciliation comparison and an incident runbook.

## Deployment-boundary evidence — 2026-08-15

`/Users/sukhdevsingh/Workspace/Bharat Studio/bharatstudio-infra/deployment/v1/manifest.template.json`
records the payment service boundary: the Razorpay webhook is the only public
provider route, internal payment/reconciliation routes require OIDC, secret
values are references only, and Cloud Run sizing/region/service-account values
remain explicit `REQUIRED_*` decisions. The infrastructure contract test passes
(`npm test`, 5/5). This is local contract evidence only; Razorpay approval,
Secret Manager provisioning, deployed IAM, provider sandbox/live proof and
staging recovery remain unsatisfied.

## Subscription billing projection — 2026-08-15

Added migration `0048_v1_l04_subscription_billing_projection.sql` and the
server-side billing projection used by the Creator API. It stores the immutable
provider subscription/account identity, approved tier, monthly-equivalent price,
monthly versus annual interval, ten-months-paid/twelve-months-service fields,
auto-renew state, current period, cancellation, bounded past-due grace and
grandfathering source/protection dates. `getBilling` now reads this projection;
it no longer derives a paid price from a mutable current-tier lookup.

The local state machine implements the approved rule: an initial continuously
subscribed paid plan is protected for twelve months; a past-due state preserves
the stored price through a 30-day grace window; explicit cancellation ends
protection; and a later rejoin uses current pricing. Equal-timestamp replays are
treated as stale, and a newer active subscription is selected over a cancelled
predecessor. The approved tier price is validated for both monthly and annual
events; annual input uses the monthly-equivalent price while charging ten months
for twelve months of service.

An active subscription state also publishes a server-owned
`channel_entitlement_versions` row with the subscription identity, billing
interval and approved price. The helper is idempotent for a repeated active
state and cannot be called by the public role. `past_due` and `cancelled` do
not silently rewrite entitlement access; their access transition remains the
responsibility of the separately approved provider-reconciliation/calendar
path, so a provider event cannot accidentally grant or revoke product access
without that evidence.

The entitlement version allocation is serialized by the channel row and the
idempotency check runs after that lock, so concurrent/retried active
reconciliation cannot create duplicate versions for one subscription.

`L04-48` passes in the disposable PostgreSQL harness. This is a local
projection/state-machine slice only. It does not create Razorpay subscriptions,
map live Razorpay plan IDs, verify provider subscription webhooks, initiate
recurring charges, reconcile provider dunning, or establish deployed IAM,
secrets, provider approval, sandbox/live or legal evidence. Those remain L04/L08
launch gates.

## Go SQLStore subscription-creation adapter evidence — 2026-08-15

Extended services/payment-webhook-go/internal/ingress/sql_store_integration_test.go
to exercise the production-shaped adapter over the real database/sql driver:

- create a server-owned platform subscription intent;
- replay the same idempotency key with a different local UUID and receive the
  original immutable intent;
- claim provider creation with the UUID lease token;
- attach a synthetic provider subscription with the approved plan identity; and
- link it through the canonical subscription-link function, then verify the
  durable linked intent and provider subscription identity.

pnpm db:test:l03 passes, including this integration test, the L03 SQL behavior
proof, the alert-worker SQL integration, overlay wake-up integration and channel
store concurrency checks. This closes the local Go adapter evidence gap only;
Razorpay Technology Partner approval, real provider sandbox execution, deployed
OIDC/IAM/secrets, recurring-charge/reconciliation behavior, staging recovery and
independent review remain open.

## Subscription creation authorization regression — 2026-08-15

The same disposable database run now exercises two invalid identity pairs
through the real `bsa_payment` security-definer boundary: an unrelated user on
the owned channel, and the owner of one channel paired with another channel.
Both fail with SQLSTATE `42501` before an intent is written. The check is based
on active `owner`/`admin` membership, so a valid private service identity cannot
turn caller-supplied `userId`/`channelId` values into authorization.

This is local synthetic evidence only; deployed OIDC/IAM, Razorpay approval,
provider sandbox/live behavior and staging recovery remain open.

### Provider/runtime readiness continuation — 2026-08-15

Re-ran the payment service boundary after the companion and notification
changes: `go test ./...`, `go vet ./...`, and focused `go test -race` for
ingress, webhook verification, provider, checkout and reconciliation all pass.
Both production-shaped Go images also build successfully from their
service-local contexts as non-root distroless images:
`bsa-payment-webhook:local` and `bsa-alert-worker:local`.

The implementation is now explicit about the Razorpay delivery identity:
`X-Razorpay-Event-Id` is the deduplication key after raw-body HMAC validation;
it is never derived from time or randomness. The provider adapter remains
server-only, account-scoped and fail-closed on response mismatch. No live
Razorpay credential, Technology Partner approval, connected-account approval,
Cloud Run IAM, secret-manager provisioning, production webhook delivery,
refund or sandbox checkout evidence was available in this run. Those remain
launch gates rather than being inferred from local image/test success.

## Reconciliation SQLStore account-attribution integration — 2026-08-15

Added `services/payment-webhook-go/internal/reconcile/sql_store_integration_test.go`
and wired it into `packages/db/tests/run-l03-application-behavior.sh`. Against
the complete disposable migration chain, the test inserts synthetic payment and
refund candidates and reads them through the real Go `database/sql` adapter.
It verifies that both `0034` and `0035` expose the immutable
`connected_account_ref`, provider order/payment/refund identities, amount and
currency required by the account-scoped provider calls. This guards against
reverting to the pre-account-attribution function signatures.

`go test ./...`, `go test -race ./...`, `go vet ./...` and `pnpm db:test:l03`
pass. This is local synthetic adapter evidence only; provider sandbox/live,
deployed credentials/IAM, scheduler execution, staging recovery and independent
review remain open.

### Full local boundary rerun — 2026-08-15

The complete local boundary was rerun after the Companion macOS contract
consumer addition. `go test -race ./...` passes for the payment service;
`pnpm db:test:l03` passes the full disposable PostgreSQL migration chain,
including `L02_SECURITY_REMEDIATIONS=PASS`, payment persistence/reconciliation,
refund/subscription projections, worker SQL integration, overlay wake-up and
multi-queue behavior; the Alerts API suite passes 54/54; `pnpm contracts:validate`
passes all eleven fixture mappings and the OpenAPI 3.1 document; and `pnpm
build` passes for the API and web applications. No payment or alert evidence
was deleted or rewritten by this rerun.

This strengthens local evidence only. Razorpay TP/provider sandbox or live
behavior, deployed OIDC/IAM/secrets, Cloud Run/Cloud Tasks execution, staging
recovery, capacity proof and independent review remain open.

## Internal payment-service response hardening — 2026-08-15

The TypeScript Creator API clients now validate the complete private Go
payment-service responses before financial or subscription data reaches the
public API. Order responses require the v1 schema, UUID local order ID, bounded
printable provider order ID, exact expected INR amount, approved status and no
unknown fields. Subscription responses require bounded provider identity,
approved tier/interval, positive integer pricing with the ten-month charge
relationship, HTTPS-only checkout URLs, and no unknown fields. Malformed
responses fail closed before they can be returned to the browser. API tests
and the API TypeScript build pass locally; deployed OIDC/provider behavior
remains open.
## Payment-intent idempotency hardening — 2026-08-15

Migration `0056_v1_l04_payment_intent_idempotency_hardening.sql` corrects a
regression introduced by the `0045` expiry-cap function replacement. After an
`ON CONFLICT DO NOTHING` race, the function now rechecks amount, currency,
provider receipt, donor fields and alert consent before returning the canonical
intent. Reusing a key with different financial or donor inputs raises a
bounded `23505` error instead of returning the original intent. The migration
also adds a `NOT VALID` database check for the same bounded idempotency-key
format used by the HTTP boundaries, preserving historical rows while
protecting new writes. The disposable `pnpm db:test:l03` run proves the
mismatch is rejected. The disposable runner now applies all migration files
after the L02 security checkpoint in lexical version order, so a future
forward migration cannot silently fall outside this acceptance run. This is
local database evidence only; provider, deployed and staging evidence remains
open.
