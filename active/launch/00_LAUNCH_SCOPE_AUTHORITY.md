# Launch scope authority

**Status:** `Approved for planning; implementation requires per-task approval`  
**Owner:** Project owner  
**Date:** 2026-08-14

## v1 public product

BharatStudio launches as one product with two connected offers:

1. **BharatStudio Alerts** — creator-direct tipping/payment, browser-source overlay, durable queues, creator dashboard, public tip page, alert configuration and approved template library integration.
2. **BharatStudio Companion** — web console, iOS/Android companion, and optional native desktop helper for authorised local OBS controls and consented diagnostics.

The BharatStudio marketing site presents the parent brand and separate Alerts/Companion pages, one coherent pricing model, support, documentation, and legal surfaces.

## Explicit v1 exclusions

- YouTube channel/data ingestion, live polling, SuperChat/membership views and catch-up summaries.
- Every Enterprise capability, including enterprise UI, roles, invites, reporting, allocations, payment routing, settlement, and finance controls.
- Any client-facing gRPC API, general-purpose desktop local API, client-owned entitlement enforcement, or in-app payment checkout in Companion.

Google Sign-In remains v1 authentication only. It must not request YouTube data scopes.

## Binding v1 decisions

- Creator-direct Razorpay payment model only. Technology Partner approval and production test evidence remain launch gates.
- Prices: Free ₹0, Pro ₹199/month, Creator ₹399/month, Studio ₹499/month; annual is ten months paid for twelve months service. Auto-renew requires clear consent, notice and self-serve cancellation. Grandfathering is approved for paid launch: an early paid subscriber keeps the subscribed tier price for 12 months while continuously subscribed; a payment failure preserves price protection for a 30-day grace period, while access follows the existing dunning/suspension rules; explicit cancellation ends protection immediately; a later rejoin uses the then-current price. The stored subscription price, not the current tier lookup, is authoritative for protected renewals. The protection-period end-date field and the exact reconciliation with Razorpay's own halt/dunning window remain implementation/provider-validation work and must not be inferred.
- No alert event may be dropped because of queue, plan, session, delivery, or display limits. Limits hold, aggregate where the approved rule allows, or require operator action; they never discard accepted payment/alert evidence.
- REST/JSON + OpenAPI is the public/client contract. SSE drives one-way overlay updates. Cloud Tasks drives alert dispatch. Cloud Scheduler uses private OIDC endpoints.
- Multi-queue source routing is approved for v1. A source event may be delivered to multiple configured queues only when the binding explicitly allows duplicates; each queue must have independent durable delivery state. `P11-1` source/priority correlation and `P11-3` per-source override enforcement are launch blockers, tracked as `L-31` and `L-32`. The bindings UI cannot be released until both are verified.
- v1 channel read permissions are role-scoped: owner/admin may view financial amounts and raw payment/refund records; operator/moderator may view alert content needed for operations/moderation but not financial amounts; viewer may view delivery/status metadata only. Billing plan/entitlement metadata may be shown to channel members, but it is not a grant of payment-ledger access. Database projections and RLS enforce this boundary; UI hiding alone is insufficient.
- SSE live push is an optimisation; durable outbox state plus overlay cursor/replay is the correctness path. v1 may use one dedicated direct database listener per API instance as a best-effort wake-up, with that connection counted in the database budget. `LISTEN/NOTIFY` through a transaction-pooled connection is prohibited. If the direct listener is unavailable, the system falls back to replay without losing accepted events; entitlement invalidation must also work through version/TTL or database revalidation. A broker is deferred unless measured staging capacity proves it necessary.
- The Companion mobile implementation uses React Native for iOS and Android. The owner-approved launch floors are iOS 15.1+ and Android API 26+. Exact React Native patch pinning, release accounts, signing and store evidence remain L07 gates.
- Windows is WinUI 3 + C# + XAML. macOS is SwiftUI + Swift.
- Companion action entitlements are server-owned and tiered as **Free 8, Pro 16, Creator 32, Studio 64** approved action slots. The Companion UI may let a user choose a page size of 4, 8 or 16 within the server-provided allocation; Free includes only the approved one-tap action set. No arbitrary commands are permitted. These limits may reject only new Companion configuration/action-slot creation and must never delay, delete, suppress, acknowledge or otherwise affect accepted payments, queues, alert ingestion, alert delivery or replay.

## Source precedence

This authority supersedes earlier repository-bound scope statements when they conflict with the v1/Phase 2 boundary above. Detailed evidence remains in the legacy repository until its precise extraction is approved in `pending/launch/`.
