# L04 provider-boundary review — Go payment service

**Date:** 2026-08-14  
**Reviewer:** Codex self-review  
**Independent reviewer:** Not performed in this pass  
**Decision state:** `Implementation slice complete; L04 remains open`  
**Task:** [`../tasks/L04-go-payment-boundary.md`](../tasks/L04-go-payment-boundary.md)  
**Acceptance:** [`../tests/TC-L04-go-payment-boundary.md`](../tests/TC-L04-go-payment-boundary.md)

## Scope reviewed

- Raw-body Razorpay webhook verification and provider delivery identity.
- Server-only Razorpay Orders API adapter.
- Request validation, response bounding, mismatch rejection, retry classification and secret/error redaction.
- Boundary between provider calls and BharatStudio's append-only financial persistence.
- Public Creator API to private Go checkout order contract, including fail-closed behaviour when payment wiring is absent.
- Executable payment-service bootstrap, configuration boundary and private Google OIDC handler wiring.

## Findings and dispositions

| ID | Finding | Severity | Disposition | Owner/follow-up |
|---|---|---:|---|---|
| L04-R1 | The provider adapter could be mistaken for idempotent financial persistence if its receipt guard is treated as the system key | High | Fixed in docs/code comments: local database uniqueness and atomic persistence remain authoritative; Razorpay receipt is only an additional provider guard | Payments; before public order route |
| L04-R2 | Provider response content could leak into application errors or logs | High | Fixed: bounded response reads and generic `ProviderError`; provider body is not included | Payments/security; regression in provider tests |
| L04-R3 | Amount/currency/receipt mismatch could allow persisting a response for a different local intent | High | Fixed: successful create responses must match all requested immutable fields | Payments; retain test |
| L04-R4 | The adapter is not connected to an atomic payment database transaction | High | Open by design; no public checkout or production readiness claim until L04 persistence task is implemented | Payments/DB; L04 acceptance gate |
| L04-R5 | Razorpay Technology Partner and connected-account capabilities are external gates | High | Open and explicitly not inferred from local tests | Owner; obtain dated provider evidence |
| L04-R6 | Independent review is unavailable in this pass | Process | Recorded; L04 remains conditional/open | Owner; fresh review before Verified |
| L04-R7 | The baseline had no durable pre-provider order-intent state, so a provider timeout could leave a client without a recoverable local intent | High | Fixed in migration 0006 with local idempotency, receipt/account binding, expiry and repeat-safe provider-order attachment; full provider-call/persistence integration remains open | Payments/DB; public order route and reconciliation |
| L04-R8 | The webhook handler needed a server-owned adapter to resolve order/account/binding context before atomic persistence | High | Fixed in `ingress.SQLStore`; it uses configured environment/account, generates IDs and calls the private function; driver/bootstrap and live evidence remain open | Payments; service bootstrap |
| L04-R9 | Concurrent replicas could both observe a pending intent and call the provider | High | Fixed with a short provider-creation claim lease in migration 0006; lease expiry permits crash recovery without a second active caller | Payments/DB; checkout integration |
| L04-R10 | A database adapter could silently construct an unconnected pool and fail later in a payment path | High | Fixed with `db.Open`: missing DSN and failed Ping return startup errors; pool limits are explicit configuration | Payments/SRE; deploy configuration |
| L04-R11 | Checkout input could attempt to select a different provider environment than the running payment service | High | Fixed: `SQLStore` rejects any request whose environment differs from its deployment-configured environment | Payments; retain unit/integration coverage |
| L04-R12 | Local donor text would be lost if only the Razorpay webhook payload were stored | High | Fixed: bounded display-name/message fields live on the local intent and are copied into the immutable alert payload during atomic persistence | Payments/product; moderation and tier-limit integration |
| L04-R13 | Public order creation could accidentally become a browser/provider shortcut or expose provider authority | High | Fixed locally: API resolves the channel, owns the idempotency-to-receipt derivation, requires the payment boundary dependency, and returns 503 when it is absent; private Go handler requires injected service authorization and never accepts provider-captured state | Payments/API; private deployment wiring and staging proof remain open |
| L04-R14 | The SQL lease functions require UUID claim tokens while the Go checkout token generator returned plain hex | High | Fixed: claim tokens now use UUID v4 format; SQL integration must still exercise claim/attach through `database/sql` | Payments/DB; retain L04-20 |
| L04-R15 | Strict internal checkout JSON could accept malformed trailing bytes | Medium | Fixed: the handler now requires the second decoder read to return `io.EOF`; regression test covers the boundary | Payments/security; retain test |
| L04-R16 | Correct code without an executable service could still leave the verified slices unreachable | High | Fixed locally: `cmd/payment-webhook/main.go` mounts webhook and private checkout handlers, opens the bounded DB pool, validates OIDC audience and fails fast on missing runtime configuration; deployed IAM/secret/provider proof remains open | Payments/SRE; staging deployment |
| L04-R17 | Provider notes were taken from a mutable request but were not part of the durable intent/idempotency record | Medium | Fixed: checkout sends only a server-derived `bsa_intent_id` note; retry-specific metadata cannot alter provider state | Payments; retain L04-22 |
| L04-R18 | A public route dependency without a runtime client could remain permanently fail-closed or trust an unvalidated internal response | High | Fixed locally: API creates a Google OIDC client, enforces HTTPS outside development, uses a fixed private path/timeout and validates the v1 response; staging IAM and provider evidence remain open | API/Payments/SRE; deployment proof |
| L04-R19 | Public `alertConsent` existed in the contract but was not persisted, so a donor's no-on-stream-alert choice could be lost or ignored | High | Fixed locally: consent is required at the private checkout boundary, stored on the immutable intent, included in idempotency matching, and gates only alert/outbox projection while preserving payment history | Payments/API/DB; retain L04-24 and verify in staging |
| L04-R20 | A provider order can be paid while the capture webhook is delayed or lost; marking local payment paid from order status alone would bypass payment-level identity and amount evidence | High | Fixed locally in the reconciliation policy: validate immutable order fields, queue payment-level recovery for a fully paid order, expire only unpaid local intents after expiry, and route unknown/mismatched states to review | Payments/DB; durable adapter, payment-level fetch and staging evidence remain open |
| L04-R21 | Reconciliation needed a durable, idempotent boundary instead of an in-memory decision only | High | Fixed locally: migration 0008, SQL adapter and runner persist local expiry or a `payment-recovery` work item; provider failures return retryable partial results without mutation | Payments/DB/Scheduler; private endpoint, payment-level fetch and staging remain open |
| L04-R22 | Durable webhook persistence could return provider success while ready delivery rows had not been submitted to the Cloud Tasks path | Critical | Fixed locally: payment ingress invokes the private worker pump after persistence, including for deduplicated retries; pump failure returns retryable response, and stable task names make partial enqueue repeat-safe | Payments/Worker/SRE; live service IAM, queue and provider retry evidence remain open |
| L04-R23 | Scheduler payment reconciliation targeted an API ledger shell without provider credentials or payment-recovery authority | High | Fixed locally: the disabled schedule targets the payment service's OIDC-protected `/internal/v1/reconciliation/payments` route, which owns Razorpay status fetch and durable recovery actions | Payments/SRE; live service IAM, provider test mode and staging retry evidence |
| L04-R24 | A paid order could be reduced to a queued recovery item without fetching payment-level identity and amount evidence | High | Fixed locally: the payment service fetches the documented `/v1/orders/:id/payments` collection, selects only a matching captured payment, persists through the atomic payment/outbox function using a deterministic internal recovery key, and completes the recovery item only after durable evidence exists | Payments/DB/SRE; live provider test-mode, retry and staging proof |
| L04-R25 | Refund reconciliation existed only as a scheduler placeholder; a delayed refund webhook had no provider-status recovery path | High | Fixed locally: payment service exposes an OIDC-protected refund reconciliation route, fetches the refund by ID, validates linked payment/amount/currency, and applies only compensating status transitions through migration `0013` | Payments/DB/SRE; live provider test-mode, scheduler IAM and staging evidence |
| L04-R26 | A later distinct refund webhook for an existing provider refund could be ledgered while `refunds.status` remained stale because the original row insert used `ON CONFLICT DO NOTHING` | High | Fixed locally in `0014`: a security-definer trigger synchronizes monotonic processed/failed/reversed transitions and recomputes payment aggregate state; database regression covers created → processed and late-failure non-regression | Payments/DB; retain regression and verify with live provider event ordering |
| L04-R27 | The webhook handler could be constructed without a worker pump and still return success after persistence, leaving ready alert deliveries without a dispatch wake-up path | Critical | Fixed locally: the handler now requires `Pumper` before reading or persisting the request; missing pump returns retryable `503`, and `L04-34` covers the no-storage fail-closed case | Payments/Worker; retain regression and verify private IAM/pump behavior in staging |
| L04-R28 | `payment.dispute.*` events matched the broad `payment.*` parser branch and then fell through the persistence function, so dispute status was not durably recorded | High | Fixed locally: dispute-specific precedence is evaluated first; migration `0031` stores append-only dispute evidence with monotonic status transitions, duplicate provider-event suppression and optional payment linkage; no payment/refund/alert mutation is performed | Payments/DB; verify all six provider dispute events and late/out-of-order delivery in provider staging |

## Evidence

- Official Razorpay order documentation states `POST /v1/orders`, amount in currency subunits, INR currency, receipt max 40 characters, and provider-side duplicate rejection for a reused receipt. The adapter enforces the BharatStudio ₹10 platform floor and these documented request bounds.
- `go test ./...` passes for ingress, provider and webhook packages.
- Webhook payload tests pass for payment/order, refund, subscription and dispute projections, including `payment.dispute.*` precedence, extra provider fields and malformed/trailing JSON.
- `pnpm db:test:l03` passes after applying migrations through 0031, including duplicate local intent creation, provider-order attachment, captured-payment webhook persistence, refund webhook status synchronization, payment-recovery completion only after payment-level evidence and dispute evidence persistence.
- The same disposable PostgreSQL run now covers a second captured payment with `alertConsent=false`: payment/webhook state is processed, while no alert event is projected. The public API test confirms the explicit consent value reaches the payment boundary.
- The same run now covers a partial refund, replay of the same `x-razorpay-event-id`, and the remaining refund; only one refund row is created for the duplicate event, and the payment transitions from `partially_refunded` to `refunded` from processed totals.
- `ingress.SQLStore` compiles and is bounded to the private persistence function; no provider-supplied account/channel field is used as an authority.
- Public API tests pass for canonical handle resolution, stable receipt derivation, dependency fail-closed behaviour and the reviewed order response shape.
- Private checkout handler tests pass for authorization, idempotency header/body binding, strict JSON, expiry and generic provider-error mapping.
- Lease-token format was corrected to match the migration's UUID SQL contract; the current disposable PostgreSQL harness now exercises claim/attach through the real Go `database/sql` adapter (`L04-20`). Deployed provider/IAM evidence remains open.
- `cmd/payment-webhook` compiles and wires the verified ingress, checkout, DB and OIDC components without running migrations or exposing credential values.
- Creator API client tests pass for private-route construction and strict response validation; staging/production config rejects a missing payment origin or audience.
- `db.Open` tests pass for fail-closed missing DSN; pgx/database/sql dependencies are in the Go module.
- `TC-L04` records the exact local tests and remaining gates.
- Reconciliation policy tests pass for open, expired, paid-without-webhook, mismatched and unknown order states; the policy never directly marks a payment paid or creates an alert from order-level status alone.
- The Go reconciliation runner and SQL boundary pass local tests; the disposable PostgreSQL harness proves candidate listing, unpaid expiry and idempotent payment-recovery work-item creation.
- Payment ingress tests prove a worker-pump failure remains retryable and a duplicate event can re-run the pump before acknowledgement; worker tests prove the private pump endpoint scans ready rows and preserves them on partial enqueue.
- Razorpay order-payment adapter tests prove the documented order-payment path, payment projection bounds and mismatch rejection; reconciliation tests prove matching captured evidence is required before recovery completion; the disposable SQL harness covers migrations `0012`–`0014` and completion only after captured evidence.
- Refund adapter, runner and disposable SQL tests prove a requested refund can be reconciled only when provider identity/payment/amount/currency match; pending and mismatch paths do not mutate local state.
- Disposable PostgreSQL evidence now proves distinct later refund webhook IDs advance the existing refund row and cannot regress a processed refund on a late failed event (`L04-33`).
- Payment ingress tests now prove a missing worker pump fails before persistence and cannot produce provider success (`L04-34`).
- Payment binding resolution now excludes closed queues, and migration `0026` rejects race-created closed-queue deliveries while preserving one open destination; `L04-35` passes in the disposable PostgreSQL harness.
- The verified webhook now carries a bounded server-derived `X-BSA-Trace-Id` to the private worker pump; ingress tests prove the value is derived from the verified provider event and not accepted from request input (`L04-36`). Full cross-service trace correlation remains a staging/observability gate.
- `docker build --file Dockerfile --tag bsa-payment-webhook:local .` passes for the service-local multi-stage image. The final image is distroless/non-root and contains only the static payment binary; this verifies packaging, not Cloud Run probes, IAM, secret injection, provider approval or production traffic.
- Race-enabled local verification (`go test -race ./...`) passes for all payment packages; live provider, deployed IAM and staging evidence remain open.
- The disposable PostgreSQL harness passes through the current migration chain: dispute created and under-review evidence links the known payment, duplicate provider delivery is suppressed, and status does not regress. No live Razorpay dispute event or external provider state was used.

## Decision

The webhook verifier, provider adapter, normalized parser, public order contract, executable private service bootstrap, Creator API OIDC client and isolated SQL persistence function are acceptable implementation slices. They do not authorize production provider traffic, financial settlement, refunds, or a claim that the complete L04 task is implemented or verified; deployed IAM/secret wiring, refund/reconciliation coverage, provider approval, staging proof and independent review remain open.

## Follow-up review — subscription billing projection — 2026-08-15

| ID | Finding | Severity | Disposition | Owner/follow-up |
|---|---|---:|---|---|
| L04-R29 | The approved prices and grandfathering rule were documented, but the API billing view had no durable subscription price, annual mode, grace period or protection window. A mutable entitlement lookup could display the wrong renewal price after a plan change. | High | Fixed locally with migration `0048_v1_l04_subscription_billing_projection.sql`, server-side `get_billing_view`, API mapping and OpenAPI fields. | Payments/DB; provider subscription integration and staging |
| L04-R30 | Annual subscription events could otherwise carry a price for a different tier, and direct retries with an equal timestamp could reapply the state. | High | Fixed: the projection validates the approved monthly-equivalent price for every interval and treats equal-timestamp state as stale. Disposable PostgreSQL regression covers both. | Payments/DB; retain L04-48 |
| L04-R31 | A cancelled predecessor could win a naive latest-row billing query after a later rejoin, hiding the current subscription. | High | Fixed locally: billing projection prioritizes active/past-due rows, and the regression applies a late predecessor event after a newer active subscription. | Payments/DB; retain L04-48 and verify provider event ordering |
| L04-R32 | Subscription events were normalized but would fall through the generic payment persistence path, so a verified event could be recorded without applying the approved billing projection. | High | Fixed locally: migration `0049` adds a server-owned subscription link and dedicated webhook projection; the Go parser retains plan/period fields and `SQLStore` routes subscription events to the dedicated function. Unknown links, plan mismatches and incomplete authorization periods quarantine durably. A server-owned `POST /v1/subscriptions` provider adapter now validates the requested plan/account and provider response. | Payments/DB; implement approved plan catalogue, checkout/link-registration integration, verify Razorpay sandbox/live event ordering and reconciliation |
| L04-R33 | The first subscription adapter/link contract treated every subscription as connected-account revenue, which would block BharatStudio plan subscriptions for a channel that had not connected a tipping account and could blur platform versus creator settlement ownership. | High | Fixed locally: adapter requests now require explicit `platform` or `connected` scope; `X-Razorpay-Account` is emitted only for connected scope; migration `0050` adds an active platform-account registry and immutable link scope; the SQL regression proves a platform subscription projects without `payment_accounts` while connected links remain channel-account gated. | Payments/DB; provision the platform account mapping/secrets, use the canonical nine-argument registration function in checkout, verify provider sandbox/live behavior and retain separate gross revenue/creator-tip ledgers |

### Conditional review decision

The local subscription projection is an acceptable implementation slice, not a
complete recurring-billing approval. Razorpay plan-ID mapping, subscription
creation/checkout, provider event persistence beyond the local link boundary,
subscription dunning/status reconciliation, provider sandbox/live evidence,
connected-account approval, deployment IAM/secrets and legal/tax review remain
open. No L04 or release status is promoted from this note. Independent review
is still required before `Verified`.

## Fresh L04 local audit — 2026-08-15

The current L04 task and acceptance matrix were re-read against the payment
service, migrations and disposable harness. The locally verifiable slices are
implemented: raw-body/HMAC and `x-razorpay-event-id` verification, account
attribution, intent/claim/attach idempotency, atomic payment/refund/dispute and
subscription projections, consent handling, reconciliation, private OIDC
handlers, worker-pump retry semantics, metrics/redaction, and the Go SQLStore
integration paths. No new locally fixable L04 correctness gap was found in this
pass.

Current evidence includes payment and worker Go tests, race tests and vet, the
full disposable PostgreSQL L02/L03 harness through migration 0054, API 53/53,
the API/web production build and contract validation. The exact 15-minute
fixture boundary was also hardened to a 10-minute synthetic test expiry so
clock/round-trip skew cannot make a valid integration fixture fail at the
database cap.

L04 remains open for Razorpay Technology Partner/connected-account approval,
provider sandbox/live checkout, webhook/refund/dispute/subscription event
rehearsal, deployed OIDC/IAM/secrets, scheduler execution, legal/tax review,
staging failure/recovery evidence and independent review. No production or
provider readiness is inferred from this audit.
