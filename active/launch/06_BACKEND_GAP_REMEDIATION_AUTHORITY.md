# Backend gap remediation authority

**Status:** `Approved for implementation by project owner — verification remains required`
**Owner:** Project owner
**Scope:** Applicable BharatStudio v1 backend/runtime gaps found in the backend gap audit
**Phase 2 exclusions:** YouTube ingestion/polling and Enterprise workspaces/funds movement remain excluded.

## Objective

Close every applicable v1 runtime gap identified by the backend gap audit and the
follow-up review. A gap is not closed by a schema field or UI control alone: the
server, database, worker, deployment contract, tests and recovery evidence must
agree.

## Required outcomes

1. Creator payment-account onboarding and account attribution are explicit,
   server-authoritative and auditable. No money movement is performed without an
   approved provider contract and verified account state.
2. Accepted payment/alert evidence remains append-only and no-drop. Tier limits,
   queue capacity, moderation, quiet mode and provider delay may hold or require
   operator action, never discard accepted evidence.
3. Queue delivery state is independent per queue. Duplicate routing is explicit,
   idempotent and covered by concurrency tests.
4. Unknown payment/refund reconciliation states enter a durable manual-review
   quarantine and cannot poison every future reconciliation pass.
5. Account deactivation, export/access, privacy requests, Terms acceptance and
   retention controls are implemented or the public promise is blocked.
6. Public payment abuse controls, provider verification, CSP/CORS, IAM, secrets,
   Cloud Tasks, DLQ, SSE replay and deployment evidence are defined and tested.
7. Every completed item has dated test evidence, self-review and an independent
   review or an explicit conditional/blocker record.

## Implementation notes added during remediation

- Razorpay deduplication uses the verified `X-Razorpay-Event-Id` /
  `x-razorpay-event-id` header. It is never derived from request time or a
  browser value; payment/refund/dispute IDs remain separate business keys.
- Queue policy is enforced at the durable claim/list/projection boundary.
  Queue modes, priority ageing, approval, quiet windows, source rate limits,
  publication markers and out-of-order replay preserve accepted rows; limits
  may hold or delay a row but cannot turn it into a drop.
- Public tip creation has a production-required Cloudflare Turnstile boundary
  plus route-specific rate limiting. A verification failure occurs before the
  payment service call and remains retryable for the viewer.
- Sarvam TTS synthesis is an explicit provider adapter with a 1.5-second hard
  timeout, bounded Indic locale/text input, a durable cache/artifact path, an
  authenticated alert-worker enrichment caller and chime fallback. The worker
  never blocks or drops a visual alert when TTS fails. Credentials, provider
  sandbox evidence and production artifact-capacity validation remain external
  release gates.
- Deployment manifests pin the API/payment/worker split, direct-vs-pooled
  database endpoints, Cloud Run caps, OIDC audience equality, Cloud Tasks
  retries/DLQ and secret names. They are substitution templates, not proof
  that production has been provisioned.
- Terms/privacy acceptance is enforced as a server precondition for product
  mutations (channel, queue/binding/config, payment-account, alert, Companion,
  overlay-session and notification writes). Account acceptance, export, privacy
  request and closure routes remain available without that precondition. The
  staging/production API refuses to boot without the account enforcement
  adapter. If active legal documents are not seeded, the database gate fails
  closed instead of treating the absence of documents as implicit consent.
- Public-payment HTTP rate limits are defense in depth and are instance-local
  in the API process. Production must also attach a distributed edge/WAF rate
  limit keyed by the real client boundary; scaling Cloud Run instances must not
  be treated as a way to increase the public payment budget.

## Decision boundaries

- TTS playback/fallback is v1; provider synthesis is implemented behind a
  provider boundary but cannot be claimed live until provider credentials and
  sandbox evidence exist.
- Email delivery and referrals are implemented only where required by a current
  v1 promise; otherwise they remain explicitly deferred and must not be implied
  by public copy. **Superseded 2026-08-16**: 01_MASTER_RELEASE_AUTHORITY.md's
  "v1 scope addendum — 2026-08-16" makes both v1-required. See that document's
  entitlement-values-style addenda for the resolved design of each (referral
  credit mechanism in particular: owner-approved as a service-time credit —
  extends current_period_end, no refund, no recurring_price_paise mutation —
  not legacy's refund-based "free month," which is incompatible with this
  repo's payment-boundary invariants).
- The no-op replay publisher is intentional. Durable database publication plus
  SSE wake-up is the correctness design; staging must prove the complete path.
- Workspace/Enterprise and YouTube code must not be added to v1 remediation.

## Closure rule

The master release authority remains blocked until all applicable remediation
items are `Verified`, or have a named owner, expiry, mitigation and rollback under
an approved conditional exception. Razorpay approval, production credentials,
legal/CA advice, app-store review and deployed staging cannot be manufactured by
local code and remain external gates.
