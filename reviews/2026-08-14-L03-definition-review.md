# L03 definition review — Alerts web and Creator API

**Date:** 2026-08-14  
**Reviewer:** Codex self-review  
**Independent reviewer:** Not performed in this pass  
**Decision state:** `Implementation in progress — API foundation, public projection, creator controls, bounded SSE and durable replay; cross-replica fan-out, payment boundary and final acceptance remain open`
**Task:** [`tasks/L03-alerts-web-and-creator-api.md`](../tasks/L03-alerts-web-and-creator-api.md)  
**Acceptance:** [`tests/TC-L03-alerts-web-and-creator-api.md`](../tests/TC-L03-alerts-web-and-creator-api.md)

## Scope reviewed

- v1 launch authority and explicit YouTube/Enterprise exclusions.
- L01 contract baseline/OpenAPI draft and L02 security boundary.
- Pending pooler-safe SSE, Razorpay delivery identity and D-2 multi-queue requirements.
- L03 task completeness, implementation boundary, acceptance cases and rollback.

## Findings and dispositions

| ID | Finding | Severity | Disposition | Owner/follow-up |
|---|---|---:|---|---|
| L03-R1 | L03 task had no linked acceptance record, review record or exact affected-file boundary | High | Fixed in definition pass | Owner; confirm before implementation |
| L03-R2 | Draft OpenAPI did not yet describe the complete dashboard/configuration/payment-status surface required by L03 | High | Fixed in contract pass: expanded v1 draft now covers 24 route entries and added synthetic API examples; final contract review remains required before domain code | API owner; L01/L03 contract review |
| L03-R3 | Overlay correctness depended on SSE details that are shared with L05 and the pending pooler-safe fan-out slice | High | Carried as shared launch gate; L03 cannot close independently | Alerts/API + worker + SRE; cross-replica evidence |
| L03-R4 | D-2 multi-queue routing was approved but bindings UI could accidentally ship before L31/L32 proof | High | Fixed by explicit non-negotiable rule and acceptance case L03-08 | Alerts/API + worker; block UI release until verified |
| L03-R5 | L03 could accidentally absorb Companion mobile/desktop, YouTube or Enterprise work | Medium | Fixed by explicit exclusions and repository boundary | Owner; review every route/navigation change |
| L03-R6 | Public tip/payment screens could imply browser-side capture or expose internal payment data | High | Fixed by server-authority and data-minimisation rules plus L03-04/L03-05 | Payments/API; verify with L04 and legal evidence |
| L03-R7 | Independent review is not available in this pass | Process | Recorded; task remains conditional until a fresh independent review occurs | Owner; before `Verified` |
| L03-R8 | Current L02 `channels` policy is authenticated-membership-only, while public tip pages need a safe active-handle projection | High | Added as a precondition: implement a narrow reviewed projection/function and test field minimisation before public route code | Security/DB + API; before public tip-page route |

## Decision

The L03 definition is approved for the foundation and public-channel slice implemented on 2026-08-14. Remaining domain routes remain contract-gated because L01/L02 independent reviews are pending. The task is not implementation-complete and not production-approved.

## Required next evidence

1. Approve the expanded endpoint/field contract after the parser/reference check.
2. Implement remaining domain routes behind reversible flags with synthetic staging data.
3. Run `TC-L03` plus shared L02/L31/L32/SSE evidence.
4. Obtain independent fresh review and update the lifecycle state.

## Foundation implementation evidence — 2026-08-14

- Added reproducible pnpm workspace metadata and lockfile for the Alerts web/API applications.
- Added Fastify API foundation with redacted logging, Helmet, exact-origin CORS, rate limiting, `/healthz`, fail-closed `/readyz`, and a versioned not-found envelope.
- Added API tests for the health, readiness, unknown-route, public-channel, payment-boundary, maintenance-boundary, fragment-only overlay URL, configuration-envelope, parser-boundary and exact-origin CORS behaviours; 27 tests pass.
- Added Next App Router web shell with accessible document metadata, responsive layout and no domain/payment/auth claims.
- Expanded the OpenAPI draft to 24 v1 route entries and added synthetic API examples; YAML parse and `$ref` checks pass.
- Added and isolated-tested the narrow `app_private.get_public_channel(text)` projection required by the public tip page; only approved active-channel fields are returned, and closed/unknown handles return no row.
- Added authenticated alert history/moderation/billing, Companion state/action and overlay create/revoke/rotate route adapters with synthetic route coverage.
- Added a disposable PostgreSQL 16 migration-0003 behavioral harness. It initially exposed missing `bsa_app` execute grants for RLS context helpers and an invalid append-only Companion `ON CONFLICT DO UPDATE`; both were corrected and the rerun passed session, channel, alert/outbox, history, moderation, Companion idempotency, overlay state and cross-tenant denial checks.
- The same harness now passes token-scoped overlay cursor acknowledgement and durable cursor-row creation.
- Cursor acknowledgement now rejects a valid-token request unless the cursor/event pair matches an actual non-quarantined delivery on that overlay's channel; the isolated harness covers the mismatched-event negative case.
- Added and route-tested the bounded continuous overlay SSE adapter with token fingerprint validation, cursor-bound event projection, direct-endpoint wake-up optimization, durable polling fallback and redacted request URLs. Full cross-replica notification/reconnect evidence remains a shared L05/L09 gate.
- Added direct-listener reconnect with bounded exponential backoff, shutdown cancellation and authenticated health metrics; application-level tests cover listener failure/reconnect without claiming live Neon/production reconnect evidence.
- Added and tested token-authenticated cursor acknowledgement. The migration stores acknowledgement state only through a scoped helper, preventing the overlay client from receiving direct cursor-table access. The API test exercises the wake-up path, durable replay and bounded stream close.
- Added and built the first web route surfaces: sign-in entry, dashboard shell, overlay setup guidance and public handle page. The public page is projection-only and does not enable payment capture.
- Hardened the browser-source credential transport after review found that a fragment token was being copied into API query strings. Overlay SSE and cursor acknowledgement now accept the credential only in an Authorization header; the browser reconnects from its last acknowledged cursor so a received-but-unacknowledged event remains replayable. API tests cover header-only authentication and query-token rejection; browser/staging evidence remains open.
- Added the authenticated versioned entitlement route, backed by the latest channel entitlement row and covered by the API route test.
- Added the public order route boundary and Google OIDC private payment client; staging/production config refuses to start without the private payment origin/audience, and invalid internal order responses are rejected before reaching the browser.
- Replaced the public tip-page placeholder with a browser-side order-initiation form that validates ₹10 minimum, bounds donor text, carries explicit on-stream alert consent, generates an idempotency key and renders only truthful order/error states. Provider checkout success is not fabricated before staging configuration.
- Added a fail-fast configuration test that rejects using the pooled application database URL as `DATABASE_URL_DIRECT`, protecting the direct LISTEN wake-up path.
- Added the six-path OIDC-protected maintenance route shell; it requires an idempotency key and returns retryable `503` until a transactional store is wired, preventing scheduler templates from creating false successful mutations.
- Replaced the unconditional readiness placeholder with a real fail-closed SQL probe: missing dependencies and probe errors remain `503`, while the configured runtime reports ready only after `select 1` succeeds.
- Connected the dashboard client to authenticated channel, queue, history, billing and test-alert operations; fresh migration proof now verifies initial config and free entitlement creation for a new channel.
- Added and isolated-tested the worker-only source-binding resolver for L31/L32: source correlation precedes priority ordering and per-source override values remain attached to each queue. Actual independent task progression still requires the Go worker proof.
- Added and tested the first Go L31/L32 routing slice: deterministic source-first correlation, independent plans per permitted queue, stable tie ordering and copied per-source overrides. Durable delivery rows now freeze source priority and overrides at acceptance; durable task progression and blocked-queue independence still require L05 staging evidence.
- Removed the global `event_outbox.status` filter from overlay replay/acknowledgement and added a regression case proving a ready queue delivery remains visible when the shared event row is terminal. Per-queue delivery status now controls overlay eligibility.
- Added and isolated-tested the first worker lease protocol: claim/retry/release/complete are per delivery, lease-token protected and state-versioned; duplicate task claims cannot acquire an active delivery and completed deliveries are not claimable again. Cloud Tasks and real worker publication remain open.
- `pnpm test` passed: 27 tests, including header-only overlay credential transport, fragment-only overlay session URLs, wake-up-driven bounded SSE, direct-listener reconnect/health, cursor validation, invalid-overlay replay, private payment-client validation, maintenance authorization, direct-endpoint separation, configured readiness-probe cases, configuration-envelope bounds, parser-error responses and exact-origin credentialed CORS.
- TypeScript API build passed.
- Next web production build passed.
- Generated `node_modules`, `dist` and `.next` outputs are excluded by `.gitignore`; they are not implementation artifacts.

This evidence closes the API foundation, migration-0003 behavior, control-plane, overlay lifecycle, bounded replay adapter, public-order boundary/client shell and initial web-surface slice only. It does not close the complete L03 domain acceptance set. Continuous SSE fan-out/reconnect, live payment/provider evidence, full dashboard controls, L31/L32 staging proof and independent review remain open.

## Implementation addendum — 2026-08-15

- Migration `0020_v1_l32_overlay_delivery_projection.sql` now merges the immutable per-delivery queue, binding, sequence, source-priority and override snapshot into the overlay payload. A shared event routed to two queues therefore produces two distinct render inputs without changing the event-level payload.
- Added provisional request-size/cardinality protection for configuration and binding overrides: API body limit is 64 KiB and each provisional values object is capped at 128 top-level properties. This is abuse protection only and does not close the approved configuration-schema/preview gate.
- The standalone queue-delivery contract and fixture now require `overrideValues`; the overlay SSE fixture carries the same delivery-level fields.
- Dashboard Web Companion controls are now hidden for roles that cannot operate queues; server-side authorization remains the source of truth.
- A local onboarding gap was fixed in `0025_v1_l03_default_alert_queue.sql`: channel creation now creates an active deterministic `Main alerts` queue, and existing active channels with no open queue are backfilled. The disposable harness asserts the new-channel invariant, preventing a public tip page from beginning with no alert destination.
- A queue-lifecycle race was fixed in `0026_v1_l03_open_queue_delivery_guard.sql`: closed queues cannot receive new delivery rows, the final open queue cannot be closed, and payment binding resolution filters closed queues before persistence. The disposable harness covers the database guards; live multi-replica and provider-timing evidence remain open.
- `pnpm db:test:l03`, API tests and API/web builds pass after the addendum. L31/L32 remain staging-verification gates; bindings UI remains unreleasable until those gates pass.
- API parser/CORS addendum: malformed JSON now returns a bounded 400, bodies over the 64 KiB envelope return a bounded 413 instead of an unclassified 500, and explicit unapproved origins receive no credentialed CORS headers. The API suite passes 27 tests; this closes only the local parser/CORS slice, not the full L03 security/browser/staging acceptance.

## Reliability follow-up — 2026-08-15

Fresh code review found a local browser-overlay failure mode: a non-retryable
cursor acknowledgement response could leave the in-memory display group
active forever after its items had been removed from the queue. The fix now
requeues only the unacknowledged suffix, aborts the active stream, reconnects
from the last confirmed cursor and resumes the queue after reconnection;
unmount also aborts the stream. A focused helper regression covers prefix/suffix
selection, and the overlay policy/TTS suite passes 10/10 with the production
build passing.

Disposition: fixed locally. This does not close deployed browser/OBS, Neon,
Cloud Run, cross-replica or staged acknowledgement-failure evidence.
