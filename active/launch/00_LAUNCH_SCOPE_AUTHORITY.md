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

> **AMENDED 2026-09-17 — YouTube moves into v1.** The exclusion bullet above is
> **narrowed**. **YouTube chat ingestion, Super Chat / Super Sticker ingestion, and channel
> and live-stream lookup are in v1.** **Membership views and catch-up summaries remain
> excluded from v1** — the amending instruction named the first three and not the last two,
> and widening later is the safe direction. Live polling is admitted only as the cadence
> those three require under the §4.4.2 budget, not as a general-purpose poller.
>
> The Google Sign-In sentence above **stands unchanged and is not superseded**. Sign-in
> remains authentication only and still must not request YouTube data scopes. Connecting
> YouTube is a **separate, deliberate OAuth grant** the creator makes, with its own consent,
> and it is never folded into sign-in.
>
> **Two token rules are binding on everything built under this amendment.** First, the
> creator's Google refresh and access tokens **never leave the server**: no web, Android,
> iPad, Moderator Console or tip-page client ever receives a Google credential, and the
> backend issues its own narrow, short-lived, role-scoped BharatStudio token instead. This
> preserves central revocation, audit, quota control and scope enforcement, all four of which
> are lost the moment a provider token is copied to a device. Second, **BharatStudio never
> posts to YouTube chat as the creator on anyone else's behalf**; a viewer who posts must
> authorise their own account, and no viewer-posting path ships in v1.
>
> **What this costs, recorded rather than discovered later.** v1 now depends on two external
> approvals that are **Unfiled** in `05_SUPPORT_AND_EXTERNAL_EVIDENCE_REGISTER.md` — Google
> OAuth app verification (the read scopes **and** the high-sensitivity chat-write scope) and
> the YouTube Data API quota grant. Neither can be filed or accelerated from inside this
> repository, so **v1's ship date is now partly Google's**. Both are promoted from Phase-4
> gates to **v1 launch blockers** in `tasks/L10-release-readiness-and-rollout.md`. The
> standing rule in `FULL-PRODUCT-DEFINITION.md` §4.4.6 is unchanged and still binding: the
> YouTube connector is **locally proven only**, and nothing built under this amendment may be
> represented as provider-ready, quota-verified or production-ready.
>
> Requested by the owner 2026-09-17; recorded in
> `reviews/2026-09-17-remaining-eight-modules-and-youtube-v1-amendment.md`.

## Binding v1 decisions

- Creator-direct Razorpay payment model only. Technology Partner approval and production test evidence remain launch gates.
- Prices: Free ₹0, Pro ₹199/month, Creator ₹399/month, Studio ₹499/month; annual is ten months paid for twelve months service. Auto-renew requires clear consent, notice and self-serve cancellation. Grandfathering is approved for paid launch: an early paid subscriber keeps the subscribed tier price for 12 months while continuously subscribed; a payment failure preserves price protection for a 30-day grace period, while access follows the existing dunning/suspension rules; explicit cancellation ends protection immediately; a later rejoin uses the then-current price. The stored subscription price, not the current tier lookup, is authoritative for protected renewals. The protection-period end-date field and the exact reconciliation with Razorpay's own halt/dunning window remain implementation/provider-validation work and must not be inferred.

  > **AMENDED 2026-09-07 (Part 12 item 1, `BharatStudio-MASTER-PLAN.md` v3.0 decision 3 and §3.1).** Studio is **₹599/month**, GST-inclusive at 18% (net ₹507.63). The **₹799 list price and the ₹499 founder SKU above are dropped** — there are zero paying subscribers today, so no grandfathering obligation is triggered by this change. Free ₹0, Pro ₹199, Creator ₹399 are unchanged. This supersedes only the Studio figure and the founder-SKU sentence in the paragraph above; the annual/grandfathering/dunning rules in that paragraph stand as written. The superseded ₹499/₹799 text is left in place above as the record of what was originally approved.
- No alert event may be dropped because of queue, plan, session, delivery, or display limits. Limits hold, aggregate where the approved rule allows, or require operator action; they never discard accepted payment/alert evidence.
- REST/JSON + OpenAPI is the public/client contract. SSE drives one-way overlay updates. Cloud Tasks drives alert dispatch. Cloud Scheduler uses private OIDC endpoints.
- Multi-queue source routing is approved for v1. A source event may be delivered to multiple configured queues only when the binding explicitly allows duplicates; each queue must have independent durable delivery state. `P11-1` source/priority correlation and `P11-3` per-source override enforcement are launch blockers, tracked as `L-31` and `L-32`. The bindings UI cannot be released until both are verified.
- v1 channel read permissions are role-scoped: owner/admin may view financial amounts and raw payment/refund records; operator/moderator may view alert content needed for operations/moderation but not financial amounts; viewer may view delivery/status metadata only. Billing plan/entitlement metadata may be shown to channel members, but it is not a grant of payment-ledger access. Database projections and RLS enforce this boundary; UI hiding alone is insufficient.
- SSE live push is an optimisation; durable outbox state plus overlay cursor/replay is the correctness path. v1 may use one dedicated direct database listener per API instance as a best-effort wake-up, with that connection counted in the database budget. `LISTEN/NOTIFY` through a transaction-pooled connection is prohibited. If the direct listener is unavailable, the system falls back to replay without losing accepted events; entitlement invalidation must also work through version/TTL or database revalidation. A broker is deferred unless measured staging capacity proves it necessary.
- The Companion mobile implementation uses React Native for iOS and Android. The owner-approved launch floors are iOS 15.1+ and Android API 26+. Exact React Native patch pinning, release accounts, signing and store evidence remain L07 gates.
- Windows is WinUI 3 + C# + XAML. macOS is SwiftUI + Swift.
  > **AMENDED 2026-09-14 — queue-count ladder.** The approved `queueCount` ladder is **1 / 2 / 3 / 5** (Free / Pro / Creator / Studio). The **1 / 3 / 5 / 10** figure previously carried in this authority and in L03's retier note is **superseded**. This matches what migration already enforces and what `06_BACKEND_GAP_REMEDIATION_AUTHORITY.md` records, so no migration, billing change, entitlement-API change or creator impact follows from this amendment; it removes a live conflict between two authorities. Raising a limit later is a safe change; lowering one breaks creators, so the conservative enforced value is the one that stands. Requested by `FULL-PRODUCT-DEFINITION.md` §30.2 and recorded here because a product document may not overrule a launch authority.

- Companion action entitlements are server-owned and tiered as **Free 8, Pro 16, Creator 32, Studio 64** approved action slots. The Companion UI may let a user choose a page size of 4, 8 or 16 within the server-provided allocation; Free includes only the approved one-tap action set. No arbitrary commands are permitted. These limits may reject only new Companion configuration/action-slot creation and must never delay, delete, suppress, acknowledge or otherwise affect accepted payments, queues, alert ingestion, alert delivery or replay.

## Source precedence

This authority supersedes earlier repository-bound scope statements when they conflict with the v1/Phase 2 boundary above. Detailed evidence remains in the legacy repository until its precise extraction is approved in `pending/launch/`.
