# Pending v1 slice — migration cross-cutting blockers

**Status:** `Approved requirement slice; local implementation/evidence complete; staging verification pending`  
**Owner:** Project owner; Architecture, Payments, Alerts and SRE implement  
**Scope:** v1 migration only  
**Created:** 2026-08-14

This file extracts only three still-agreed, unfinished requirements from the legacy evidence. It does not replace or bulk-copy the legacy FRDs.

## 1. Pooler-safe SSE fan-out and entitlement invalidation

**Legacy evidence:** `INFRASTRUCTURE_ROADMAP.md` Phase 4 and P0-1; `OVERLAY_FANOUT.md`; Neon load/fan-out evidence.  
**Decision:** Durable outbox plus per-overlay cursor/replay is the correctness mechanism. Live notification is an optimisation. A transaction-pooled connection must never be used for session-scoped `LISTEN`.

**v1 implementation:** use a dedicated direct database listener for `LISTEN/NOTIFY`, with same-session startup assertion, reconnect, listener health metrics and a pooler-misconfiguration failure test. Count one listener connection per API instance in capacity sizing. A listener is only a best-effort wake-up; disabling it must fall back to outbox/cursor replay. Do not add a broker in v1 unless measured staging capacity proves the direct-listener design insufficient and a separate cost/architecture decision is approved.

Overlay replay and entitlement version/TTL revalidation must converge after missed notifications. Cross-replica delivery must be tested: commit through replica A, deliver to an overlay connected to replica B.

**Acceptance:** no accepted overlay event depends solely on `NOTIFY`; reconnect/resync, cross-replica fan-out, notification outage, listener reconnect and cache-staleness tests pass.

## 2. Razorpay webhook delivery identity

**Legacy evidence:** legacy `apps/api/src/routes/webhooks/razorpay.ts` timestamp-derived event key; [Razorpay webhook best practices](https://razorpay.com/docs/webhooks/best-practices/); [Razorpay webhook validation](https://razorpay.com/docs/webhooks/validate-test/?locale=en-US).  
**Decision:** After raw-body HMAC verification, the case-insensitive `x-razorpay-event-id` header is the provider delivery deduplication key.

Store it separately from payment, refund, subscription and dispute identifiers. Enforce uniqueness scoped to provider, connected account/environment and event ID. Missing-header behaviour must be explicit and must not create a timestamp/random fallback key.

**Acceptance:** concurrent duplicate delivery creates one provider-event record and one financial/alert effect; distinct delivery IDs remain separately traceable; malformed or missing identity follows the documented retry/quarantine path.

**Local evidence:** the Go verifier requires the case-insensitive `x-razorpay-event-id` header, verifies the raw-body HMAC-SHA256 before persistence, and the disposable PostgreSQL harness proves concurrent duplicate suppression and distinct-event traceability. Provider/staging delivery evidence remains open.

## 3. D-2 multi-queue source routing

**Legacy authority:** `tasks/MASTER-RELEASE-AUTHORITY.md` D-2; `tasks/alerts/P11-alert-config-queue-completion-plan.md`.  
**Decision:** `YES` — multi-queue source routing ships in v1.

`P11-1` source/priority correlation is tracked as `L-31`. `P11-3` per-source override enforcement is tracked as `L-32`. Both are launch blockers. The bindings UI cannot be released until both are verified.

The local binding control slice now exists but is feature-gated: `PATCH
/v1/channels/{channelId}/bindings/{bindingId}` can edit future routing policy,
while migration `0037_v1_l03_binding_identity_guard.sql` prevents identity
rewrites and closing the reserved `__channel_default__` payment route. The
dashboard controls are enabled only for staging verification; no accepted
delivery snapshot is rewritten by a binding edit.

Each permitted queue needs independent durable delivery/outbox state. A global event status must never prevent a second permitted queue from progressing. Source identity must be resolved before priority and per-source style, bracket and rate-limit rules are applied. Multiple delivery rows require explicit consent on every participating binding; mixed consent is a single-route case, resolved by highest priority, and is never silently duplicated.

For the normal payment path, a channel is provisioned with the reserved
`__channel_default__` payment binding before any Razorpay payment ID exists.
An exact provider payment binding takes precedence over that fallback. This
is a routing identity rule, not a duplicate-delivery permission: default
bindings still require explicit `allow_duplicates` consent before more than
one queue is selected.

**Acceptance:** simultaneous delivery to two queues progresses independently; blocked queue A does not block ready queue B; source/priority, per-source overrides, retries, replay, deduplication and audit history are correct.

## Implementation links

- Authority: `active/launch/00_LAUNCH_SCOPE_AUTHORITY.md`
- Migration: `migration/00_MIGRATION_AND_LAUNCH_PLAN.md`
- Contracts/database: `tasks/L01-contracts-and-database-baseline.md`
- Payment: `tasks/L04-go-payment-boundary.md`
- Alert worker: `tasks/L05-go-alert-worker-and-cloud-tasks.md`
- Proof: `tasks/L09-observability-load-failure.md`

## Lifecycle

The requirement decisions are approved for v1 planning. L31/L32 now have local implementation evidence: accepted delivery snapshots are persisted, worker claims carry them, overlay replay projects them per queue, D-2 duplicate consent is enforced in the payment router plus durable delivery-row trigger, the normal payment path has a durable channel-default binding with exact-source precedence, and the browser-source runtime consumes the projected events. Worker publication is released back to `ready` until browser acknowledgement, so a received-but-unacknowledged alert remains replayable and the outbox is not marked complete prematurely. Queue lifecycle safety is also covered locally: payment binding resolution excludes closed queues, the database rejects a race-created delivery for a closed queue, and the final open queue cannot be closed (`0026_v1_l03_open_queue_delivery_guard.sql`). The API now has a real disposable-PostgreSQL `LISTEN/NOTIFY` integration check with two independent listener connections plus a separate publisher; the wrapper correctly treats successful `postgres.js` listener registration as connected and durable replay remains authoritative. The slice is not `Verified` until dated cross-replica/staging evidence proves independent progression, retries, replay, deduplication, consent, browser-source rendering and audit behaviour. No legacy document is deleted or rewritten by this slice.

### Shared-PostgreSQL replay proof update — 2026-08-15

The local two-client/two-API-replica proof now passes through
`integration/overlay-cross-replica.integration.ts`. It exposed and closed the
missing `event.channel_id = session.channel_id` predicate in
`get_overlay_events`, via migration
`0054_v1_l03_overlay_event_channel_guard.sql`. This is active v1 security
evidence; deployed Neon/Cloud Run network, capacity, browser-source and OBS
staging evidence remain pending.

### Browser acknowledgement recovery update — 2026-08-15

The browser overlay now recovers when a cursor acknowledgement returns a
non-retryable response after a display group has already been removed from the
in-memory queue. It requeues only the unacknowledged suffix, aborts the active
SSE stream, reconnects from the last server-confirmed cursor and resumes the
requeued items after reconnection; the acknowledged prefix is not replayed.
Unmount cleanup also aborts the active stream. The focused overlay policy/TTS
suite passes 10/10, the API suite passes 54/54, the production API/web build
passes, and the disposable PostgreSQL L02/L03 harness reports
`L02_SECURITY_REMEDIATIONS=PASS` and `L03_APPLICATION_BEHAVIOR=PASS`.
This remains local evidence only; deployed browser/OBS acknowledgement-failure
and staging network-failure proof are still required before verification.

### Out-of-order publication replay guard — 2026-08-15

Concurrent task enqueueing, network delivery and worker execution can publish a
newer delivery before an older one. Migration
`packages/db/migrations/0055_v1_l03_unacknowledged_replay_guard.sql` therefore
treats the overlay cursor as an acknowledgement checkpoint rather than a hard
eligibility lower bound. `ready`, `held` and `displayed` deliveries remain
replayable until their own acknowledgement is recorded; acknowledged rows are
excluded by status and results remain ordered by `created_at, delivery.id`.
The L03 disposable PostgreSQL harness now reproduces the newer-acknowledged /
older-unacknowledged case and passes. This closes the local implementation gap
without closing the required deployed cross-replica, browser and OBS evidence.
