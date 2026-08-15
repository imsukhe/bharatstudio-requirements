# L03 — Alerts web and Creator API

**Status:** `Local implementation slices passing — browser/accessibility, cross-replica, provider, staging and independent review gates pending`  
**Level:** L3  
**Owner:** Web / API / UX  
**Depends on:** L01, L02  
**Blocks:** L04, L05, L07

## Authority and evidence

- **Authority:** [`active/launch/00_LAUNCH_SCOPE_AUTHORITY.md`](../active/launch/00_LAUNCH_SCOPE_AUTHORITY.md)
- **Pending v1 slices:** [`pending/launch/PENDING-03-MIGRATION-CROSS-CUTTING-GAPS.md`](../pending/launch/PENDING-03-MIGRATION-CROSS-CUTTING-GAPS.md)
- **Acceptance record:** [`tests/TC-L03-alerts-web-and-creator-api.md`](../tests/TC-L03-alerts-web-and-creator-api.md)
- **Review/decision record:** [`reviews/2026-08-14-L03-definition-review.md`](../reviews/2026-08-14-L03-definition-review.md)

L03 cannot implement domain behaviour against an unapproved endpoint or event shape. The owner approved the L03 scope on 2026-08-14. L01 contract verification and L02 security evidence remain prerequisites for final closure; the current implementation includes the safe public-channel projection, authenticated creator controls, Companion command/state routes and overlay session lifecycle. Overlay SSE delivery/replay remains shared L03/L05 work.

### Launch-scope definition — template library

The launch authority names **approved template library integration** as part of
Alerts v1. The active contract is now
`../active/launch/04_TEMPLATE_LIBRARY_AUTHORITY.md`, backed by the catalogue
manifest and L03-09 acceptance record. The implementation therefore exposes
only the approved FRD-011 core presentation configuration until a runtime
package is verified; it does not invent branding/template/HTML fields. L03-09
is implementation- and visual-verification blocked by the deferred runtime
package completion and browser/accessibility evidence, not by an unresolved
definition gap.

## Objective

Deliver the v1 Alerts experience on the final REST contract: creator onboarding/dashboard, public tip pages, overlay setup, configuration, queues, moderation, billing view, roles, and Web Companion Console.

## Tasks

1. Split legacy Next web routes into Marketing versus Alerts. Copy only approved Alerts UI and test code; remove all in-app API/database route handlers.
2. Build TypeScript Creator API modules for auth, creator/channel, configuration, overlay, alert event control, entitlements, billing view, support/admin control plane and private job endpoints.
3. Implement Google sign-in/auth/session/device revoke without YouTube scopes; enforce server-side role/entitlement checks.
4. Implement creator onboarding, public tip page, payment status screen, browser-source setup/test flow, alert settings, queue controls, moderation and history.
5. Implement overlay secure URL/session lifecycle, SSE reconnect cursor/resync, rotation/revocation, token non-leakage and OBS browser source guidance.
6. Implement long message and multi-line layout contract: configurable display area, truncation/continuation rules, preview at configured size/placement, localisation, reduced motion and no text overlap/clipping.
7. Implement Web Companion Console only for authorised v1 operational views and command/session state; no direct OBS connection from browser.
8. Remove/hide all v1-excluded YouTube and Enterprise UI, navigation, routes, APIs and marketing claims.

## Exact implementation boundary

### Alerts repository

- `bharatstudio-alerts/apps/web/` — Alerts dashboard, public tip page, overlay setup/test UI, queue/configuration/moderation/history views and the authorised Web Companion Console surface.
- `bharatstudio-alerts/apps/api/` — TypeScript REST composition, authentication/session adapters, channel/RBAC checks, public tip-page reads/order initiation, configuration, overlay session control, queue/moderation/history views, entitlements and safe internal-handler ingress.
- `bharatstudio-alerts/contracts/openapi/v1.yaml` — only the reviewed L03 endpoint additions/field clarifications; no undocumented client route.
- `bharatstudio-alerts/contracts/json-schema/` and `bharatstudio-alerts/contracts/fixtures/` — only contract examples required by L03; preserve L01 schema/version rules.
- `bharatstudio-alerts/tests/` — web/API contract, security and browser-source integration tests, using synthetic data only.

### Implemented L03 API slices

- Authenticated channel/configuration/queue/binding API foundation.
- Test-alert acceptance, bounded history, moderation action recording, billing view and Companion state/action endpoints.
- Server-resolved entitlement view with versioned values; clients do not calculate tier permissions locally.
- Overlay session create/revoke/rotate with hashed short-lived token storage and atomic rotation. The browser-source token transport is still subject to the L03/L05 log-redaction and reconnect security proof; it is not production-approved by this implementation alone.
- Fresh PostgreSQL 16 behavioral harness for the v1 migration chain: session lifecycle, channel creation, atomic alert/outbox acceptance, history, moderation, Companion idempotency, overlay state and cross-tenant RLS denial pass. Re-run with `pnpm db:test:l03`.
- The same harness now proves token-scoped overlay cursor acknowledgement and durable cursor-row creation. The acknowledgement helper rejects a valid-token request unless the cursor/event pair is an actual non-quarantined delivery for that overlay's channel.
- Added a bounded continuous SSE adapter: short-lived token fingerprint lookup, scoped event projection, `Last-Event-ID` cursor parsing, bounded replay, no-store headers and redacted request URLs. It uses a dedicated direct-endpoint listener only as a wake-up optimization and polls durable replay when notifications are unavailable; the stream closes at its bounded window so the client reconnects safely.
- Added token-authenticated overlay cursor acknowledgement with an append/update-safe database function and API contract. Acknowledgement records are scoped to the active overlay session and do not make live notifications the correctness path.
- Added API coverage for the bounded continuous SSE loop using the wake-up interface, followed by durable replay and clean bounded close; cross-replica notification-outage evidence remains a staging gate.
- Added fail-fast staging/production configuration validation that rejects using the pooled application endpoint as `DATABASE_URL_DIRECT`; the direct listener path remains a wake-up optimisation and durable replay remains authoritative.
- Tightened the direct-listener configuration gate: staging/production now reject invalid database URL schemes and known pooled Neon endpoint forms (including `-pooler` hosts and `pgbouncer=true`) for `DATABASE_URL_DIRECT`, not only an endpoint identical to `DATABASE_URL_APP`. This prevents a second pooled URL from silently becoming the session-scoped `LISTEN` connection; the API regression suite covers the rejection.
- Added a shared browser API-origin guard at `apps/web/app/lib/api-origin.ts`: development/test may use the local `localhost:4100` default, while staging/production require an explicit non-local HTTPS origin. Invalid or missing production configuration fails closed instead of silently sending dashboard, tip or overlay requests to a user's localhost. The focused origin tests pass 3/3 and the web build passes.
- Added direct-listener reconnect with bounded exponential backoff, explicit listener health state and Prometheus gauges/counters for connected, reconnect and failure state. A listener failure cannot stop durable cursor replay, and shutdown cancels reconnect work.
- Replaced the unconditional `503 /readyz` placeholder with a fail-closed readiness probe: unconfigured dependencies remain not-ready, while the production bootstrap runs a real `select 1` database probe and returns ready only after it succeeds. Probe errors expose no connection details.
- Added the initial Alerts web route surfaces: sign-in entry, dashboard summary shell, overlay setup guidance and public handle page. The public page renders only the approved channel projection; order creation now uses the L04 private payment boundary when configured and fails closed otherwise.
- Replaced the public tip-page placeholder form with a client-side order-initiation flow: ₹10 validation, bounded donor name/message fields, explicit on-stream alert consent, idempotency-key generation, retry-safe error/status messaging and no provider/payment success fabricated in the browser. Razorpay checkout handoff remains gated on provider/public-key staging configuration.
- Connected the dashboard to the API session/channel/queue/history/billing flows, added channel creation, queue creation and test-alert submission, and added browser-safe environment configuration. New channels now receive an initial config and free entitlement version atomically.
- Added the worker-only `resolve_queue_bindings` database function. It resolves `(source_type, source_id)` before priority and returns each permitted queue’s independent binding and override values; the isolated harness proves two queues resolve independently and in priority order. Delivery execution remains L05/L31/L32 work.
- Added the reserved `__channel_default__` payment source binding. New and existing active queues receive a durable default payment binding before any provider payment ID exists; an exact provider payment binding takes precedence when present. This closes the onboarding gap where a tip could be accepted without any creator-configured payment route, while preserving explicit multi-queue consent and immutable delivery snapshots. `pnpm db:test:l03` proves default resolution and exact-source precedence; live provider/staging evidence remains open.
- Added the binding lifecycle control slice: authenticated operators can list active and closed bindings and update duplicate consent, priority, presentation-safe overrides or active state through the staged `PATCH /v1/channels/{channelId}/bindings/{bindingId}` contract. The gated dashboard exposes approved style, anchor, scale and priority controls without arbitrary HTML/template input. The reserved `__channel_default__` payment binding cannot be closed, and migration `0037_v1_l03_binding_identity_guard.sql` makes channel/queue/source identity immutable at the SQL boundary. Accepted delivery snapshots remain unchanged after any future binding edit. The dashboard surface is behind `NEXT_PUBLIC_ENABLE_BINDINGS_UI=true` until L-31/L-32 staging verification; it is not enabled by default.
- Added migration `0038_v1_l03_open_binding_queue_guard.sql`: a new binding cannot target a closed queue at the RLS boundary, while existing binding rows remain retained for audit/snapshot integrity and can become usable again when the queue reopens. The disposable harness proves the rejection.
- Added the first Go worker routing slice under `services/alert-worker-go`: source correlation precedes priority, matching queues remain independently represented, tie ordering is deterministic, and per-source overrides are copied safely. Durable delivery progression and staging proof remain L05 work.
- Removed the remaining global-outbox-status gate from overlay replay and cursor acknowledgement. A terminal status on the shared event row can no longer hide or block a valid per-queue delivery; the isolated harness now proves replay and acknowledgement still work in that condition.
- Added the worker-owned outbox projection refresh so history and Companion pending counts converge after per-queue completion without reintroducing the global event status as an overlay dispatch gate.
- Added the first durable L05 delivery protocol in migration `0004_v1_l05_delivery_leases.sql`: per-delivery lease token, lease expiry, attempt count, state version, retry transition and terminal completion. The harness proves duplicate claim rejection, retry reclaim, terminal completion and no re-claim after completion.
- Changed the direct SSE listener to treat `NOTIFY` as a broadcast wake-up rather than requiring an overlay ID in the payload; every stream still performs token-scoped durable replay. Added worker-only `notify_overlay_wakeup` in migration `0005_v1_l05_overlay_wakeup.sql`; notification content cannot grant access or determine correctness.
- Added migration `0017_v1_l03_moderation_event_scope.sql`: moderation inserts now require the referenced alert event to belong to the requested channel, in addition to the operator-role check. The disposable harness rejects a cross-channel moderation action.
- Added migration `0018_v1_l03_binding_queue_scope.sql`: binding writes now require the referenced queue to belong to the binding channel. The disposable harness rejects a cross-channel queue reference.
- Wired the Overlay Setup web surface to the authenticated session API: create, copy, rotate and revoke are now real actions with expiry/status feedback. The public tip form now launches Razorpay Checkout only when `NEXT_PUBLIC_RAZORPAY_KEY_ID` is configured; the browser callback remains informational and cannot mark payment captured.
- Added the actual OBS browser-source runtime at `apps/web/app/overlay/[overlayId]/page.tsx`. Session URLs now open this HTML page instead of exposing the raw SSE response as an OBS source; the page reads the short-lived token from the URL fragment (so the web server does not receive it), then sends it only in an Authorization header for the API stream and cursor acknowledgement. The stream reconnects with the last acknowledged cursor, so an event received but not displayed/acknowledged is replayed after reconnect. The page accepts custom SSE event types, queues eligible alerts, renders long/multiline text safely, and waits for a successful acknowledgement with bounded retry before advancing the display queue. Provider/staging browser-source evidence remains open.
- Added migration `0055_v1_l03_unacknowledged_replay_guard.sql`: the overlay cursor is now an acknowledgement checkpoint rather than a hard eligibility lower bound. Every still-unacknowledged `ready`/`held`/`displayed` delivery remains replayable, so out-of-order Cloud Tasks publication cannot let a later acknowledged cursor permanently hide an older durable alert. This preserves no-drop behavior under concurrent enqueue, worker delay and reconnect; local regression evidence is recorded in the L03 test harness.
- Formalized the approved FRD-011 core configuration contract in `contracts/json-schema/channel-config.schema.json` and the API route schema: ₹10 minimum, bounded brackets, display style/timing, locale, reduced motion, TTS overflow, placement/scale and queue controls. Unknown fields are rejected rather than silently removed, and semantic bracket gaps/overlaps return explicit configuration errors. Creator-authored branding and template fields remain gated behind the separate FRD-013 approval.
- Completed the authenticated creator configuration editor for the full approved v1 core surface: minimum tip, locale/reduced motion, placement and sizing, amount brackets, per-bracket display/TTS policy, TTS fallback, queue mode/stack/aggregation/rate policy, approval and quiet mode. Empty optional voice IDs are omitted rather than sent as invalid empty values. `pnpm build`, `pnpm test` (53 API tests) and `pnpm contracts:validate` pass.
- Added the authenticated dashboard editor for the approved core configuration: minimum tip, default display time/style, locale, reduced motion, screen anchor, overlay scale, queue mode and visible-alert limit. Saves use the server version (`if-match-version`) and the UI reports a conflict instead of overwriting a newer configuration. Branding, templates and AI generation remain intentionally unavailable until their separate authority and preview evidence are approved.
- Added a safe client-side core-config preview that reflects the selected style, anchor, scale, locale and reduced-motion setting with bounded sample text. It renders fixed text through the reviewed DOM/CSS surface; it does not accept arbitrary HTML, branding assets or template code.
- Expanded the authenticated editor to cover all approved FRD-011 core fields: contiguous amount brackets, per-bracket character/display/TTS rules, TTS voice/locale/overflow/padding, placement offsets and width, queue aggregation/rate/approval settings and quiet-mode schedule. The editor sends only the reviewed schema and leaves branding, templates and AI controls out of scope.
- Completed the overlay's approved presentation-policy slice in `apps/web/app/overlay/overlay-policy.ts` and `apps/web/app/overlay/[overlayId]/page.tsx`: versioned `configSnapshot` is projected by migration `0029_v1_l05_overlay_config_snapshot.sql`, the browser applies bounded bracket timing/character limits, nine safe anchors, scale/width/reduced-motion settings, FIFO/priority/stacked/pills/aggregated presentation and safe override whitelisting. Priority can reorder only within a contiguous visible frontier; acknowledgements remain in arrival order so `Last-Event-ID` cannot skip an earlier unacknowledged delivery. TTS/audio is an optional side effect: a same-origin approved audio path is attempted when present, playback is hard-bounded at 1.5 seconds by `apps/web/app/overlay/tts-runtime.ts`, unavailable/rejected/stuck audio falls back to a short browser chime, and neither blocks visual display or durable acknowledgement. Cursor acknowledgement remains retryable and occurs only after the whole displayed group is confirmed; no presentation limit deletes or acknowledges an undelivered item. Local policy and timeout tests pass, the web production build passes and the PostgreSQL harness proves the versioned snapshot projection.
- Hardened the web API client to preserve only short, server-authored error messages for configuration conflicts/validation while keeping generic bounded fallback text for non-JSON failures; it never renders response payloads as markup.
- Hardened overlay rotation so it requires the authenticated user to have access to the overlay's channel, matching revoke/create authorization; overlay IDs alone cannot rotate another channel's session. This is locally code-reviewed; cross-tenant staging evidence remains required.
- Wired dashboard queue pause/resume controls to the authenticated queue update endpoint, with server-returned state rendered after each change; queue-target authorization remains enforced by RLS and the Companion command idempotency path.
- Wired recent-alert moderation controls in the dashboard to the authenticated approve/hold/suppress/replay route; authorization and event/channel scope remain server/RLS-enforced.
- Added role-aware dashboard visibility for queue/test-alert controls and moderation actions; this is a UX reduction only, never a replacement for server-side role/RLS enforcement.
- Added migration `0039_v1_l03_role_scoped_financial_reads.sql`: owner/admin may read financial history fields and raw payment/refund rows; operator/moderator may see alert content needed for operations without financial amounts; viewer receives status-only history. The database projection and `bsa_app` RLS policies enforce the privacy boundary, so UI visibility is not the only control. The disposable harness covers all four roles.
- Added migration `0040_v1_l03_overlay_companion_role_guards.sql`: overlay session credentials can be created/read/rotated/revoked only by owner/admin/operator roles, and Companion queue-command insertion is restricted to those operational roles; moderator remains eligible for the separate moderation route but cannot issue Companion queue controls. The disposable harness covers viewer/moderator denial and operator allowance.
- Added server-side enforcement for the versioned `queueCount` entitlement during queue creation. The check counts all channel queue records, including soft-closed queues, so closing/reopening cannot bypass the entitlement. It rejects only the new queue operation; it never deletes, suppresses, acknowledges or delays accepted payment/alert evidence. Other tier dimensions remain unavailable until their approved entitlement keys and values are carried into the active authority.
- Closed the Companion command no-op gap: v1 now accepts only `pause_queue`, `resume_queue` and `send_test_alert`; every accepted command requires a queue target. `send_test_alert` creates one durable manual alert/outbox/delivery transaction and returns its event ID, while idempotent retries return the original event without creating another delivery. Approve/hold/replay remain on the separately implemented moderation endpoint until Companion-specific target/transition semantics are implemented.
- Added migration `0019_v1_l03_manual_alert_deliveries.sql`: manual/test alerts now create ready per-queue delivery rows atomically with the alert event and outbox. The SQL store resolves active queues when the caller does not specify them and fails closed when no active queue exists; a test alert can no longer be accepted as an outbox-only record.
- Added migration `0025_v1_l03_default_alert_queue.sql`: new channels create an atomic `Main alerts` queue, and existing active channels without an open queue receive a deterministic backfilled queue. This prevents a newly created public tip page from accepting a payment before any alert destination exists.
- Added migration `0026_v1_l03_open_queue_delivery_guard.sql`: closed queues cannot receive new delivery rows, the final open queue cannot be closed, and payment binding resolution filters closed queues before provider persistence.
- Added migration `0020_v1_l32_overlay_delivery_projection.sql`: overlay replay now merges each delivery's immutable queue, binding, sequence, source-priority and override snapshot into the projected payload. The shared event payload remains unchanged; a two-queue replay assertion proves each queue receives its own accepted override after later binding edits.
- Added migration `0022_v1_l05_overlay_ack_release.sql`: worker publication releases the delivery lease back to `ready`; the browser acknowledges only after its display interval, which moves the delivery to `acknowledged` and removes it from fresh replay. This keeps an accepted alert replayable across a disconnect before acknowledgement and prevents a worker `displayed` transition from hiding the alert from the browser source.
- Added migration `0030_v1_l05_publication_marker.sql`: a successful worker release records `published_at` while keeping the delivery `ready` for browser replay; the ready-delivery pump excludes already-published/unacknowledged rows so offline overlays do not cause repeated task enqueueing. Initial pending rows and overlay replay remain eligible, and the disposable harness proves the marker/re-enqueue boundary.
- Added migration `0032_v1_l32_source_rate_limit_and_publication_claim_guard.sql` and the matching binding contract: per-source rate limits delay accepted deliveries without a drop path, and stale tasks cannot reclaim a published delivery. The browser applies bounded per-bracket overrides only to the amount-selected bracket; API/OpenAPI validation rejects unknown executable/script-like fields and amount-range changes.
- Added a 64 KiB API request envelope and 128-property cap for provisional configuration and per-binding override objects. This limits abuse while preserving arbitrary values only as a temporary transport shape; it does not approve undocumented configuration keys or enable an arbitrary configuration editor.
- Added bounded parser-error handling for the API envelope: malformed JSON returns a redacted 400 response, and the 64 KiB body limit returns a redacted 413 response instead of falling through to a generic 500. The API suite now has 36 passing tests covering parser, exact-origin CORS, binding updates, cursor, wake-up lifecycle and Companion command cases.
- Corrected credentialed CORS to evaluate the request origin instead of emitting the configured allow-origin value for every caller. Same-origin/non-CORS requests remain usable; explicit unapproved origins receive no credentialed CORS headers. The API suite covers the allowed and denied origins.
- Hardened the web API client boundary: all identifier path segments are encoded before REST URL construction, and Companion commands use the finite server-approved action union with a secure-random idempotency key requirement. This is client safety/type evidence only; server validation and authorization remain authoritative.
- Corrected the unknown-route envelope to carry the Fastify request trace ID instead of the literal `unassigned` placeholder; the API regression test now verifies that the returned trace can be correlated with the request.
- Extended overlay setup for accounts with multiple authorized channels: the dashboard hands off an encoded channel ID, the setup surface validates it against the authenticated channel list, and session create/rotate/revoke remains server-authorized. The default remains the first channel when no selection is supplied.
- Replaced timestamp-only alert-history pagination with a deterministic composite cursor in migration `0027_v1_l03_history_cursor_tiebreak.sql`: the API now emits `createdAt|eventId`, the database orders by `created_at desc, id desc`, and the tie-break predicate prevents same-timestamp events from being skipped or repeated. Timestamp-only cursors remain readable during migration.
- Added channel-specific minimum-tip propagation and enforcement in migration `0043_v1_l03_l04_channel_tip_minimum.sql`: the narrow public-channel projection exposes the configured minimum, the public form displays and validates it, the Creator API rejects below-channel-minimum orders before payment-service use, and a database trigger rechecks the immutable payment-intent boundary. The ₹10 platform floor remains the lower bound.
- Added the donor-safe payment status surface required by L03-05: `GET /v1/public/tip-orders/{orderId}/status` reads a narrow SQL projection and returns only the local order UUID, amount, INR currency, server-confirmed pending/paid/expired/failed state and update time. The public tip form polls it after Razorpay checkout; it never exposes provider IDs, donor fields, channel data or client-declared payment success. Migration `0044_v1_l03_public_payment_status.sql` and API/web tests pass locally.
- Aligned the browser Razorpay Checkout configuration with the approved fifteen-minute local intent lifetime by sending `timeout: 900` seconds. This only closes the checkout UI after the bounded window; provider webhooks and reconciliation remain the financial source of truth. Web production build passes; provider/staging checkout validation remains open.

## Local implementation evidence update — 2026-08-15

- API test suite: 54/54 tests pass after the exact-origin CORS, bounded parser, strict configuration schema, trace-envelope, client-boundary, binding-update, multi-channel setup, history-cursor, Companion command, entitlement-limit, overlay-wake-up, channel-minimum, donor-safe payment-status, global burst-rate-limit, channel-serialization, authenticated subscription-route and subscription-client response-validation changes, including HTTP-level SSE arrival-after-replay, clean post-headers replay-failure closure, `Last-Event-ID` resume, replica-B replay after a replica-A commit, no-wakeup durable polling coverage and immediate disconnected-waiter cancellation. The separate browser API-origin guard tests pass 3/3.
- API route tests now pass 54/54. The continuous SSE route closes cleanly after a post-headers durable-replay failure, emits no stack/error payload, and leaves cursor acknowledgement to the browser's reconnect path; API and web production builds pass. Contract validation remains green: 11 fixture mappings and the OpenAPI 3.1 document with 32 paths and resolved local references. The paid-subscription route is implemented as an L04 private payment boundary and does not accept provider plan/account values from the browser.
- Added a real PostgreSQL `LISTEN/NOTIFY` integration check with two independent listener connections plus a separate publisher in the disposable L03 harness. It proves both listener instances receive the same committed notification; this remains an optimisation check only, and does not replace durable cursor replay or staging cross-replica evidence.
- Corrected the listener wrapper to match `postgres.js` semantics: successful `listen()` registration resolves normally and is not treated as a disconnect; only registration rejection enters the bounded failure path. The real PostgreSQL integration check caught this mismatch that mock listener tests could not model.
- The dashboard now loads and saves the versioned approved core configuration through the authenticated API; web production build passes after the editor integration.
- The latest disposable PostgreSQL L03 behavior harness passes, including RLS isolation, queue lifecycle safety, multi-queue immutable snapshots, overlay acknowledgement/replay, payment-to-alert persistence and deterministic same-timestamp history pagination.
- Added `integration/channel-store-concurrency.integration.ts` to the disposable PostgreSQL harness. Two independent database clients now race queue creation and configuration updates: exactly one queue creation is accepted within the allocation, and exactly one caller receives the next configuration version. This is real multi-connection database evidence; cross-replica/staging capacity proof remains separate.
- The same harness now also proves Companion test-alert durability and idempotency: one command produces one event and one delivery, and a duplicate command key produces no second event.
- Payment and alert-worker Go tests, race tests and `go vet` pass. Cron contract tests, mobile tests/lint/typecheck and macOS tests also pass in their respective repositories.
- These are local implementation results only. L03 remains open for deferred template runtime packages, browser/accessibility evidence, cross-replica SSE/replay, provider checkout and final staging/independent review.

### Overlay wake-up waiter cleanup — 2026-08-15

Hardened `apps/api/src/db/overlay-wakeup.ts` so a waiter clears its timeout
immediately when a notification or shutdown resolves it. Previously the
promise resolved correctly but its timer remained scheduled until the full
wait window elapsed, creating avoidable timer accumulation under many
concurrent overlays. This changes no durable replay, cursor, acknowledgement,
payment or delivery state; the wake-up remains only a best-effort optimisation.
The API/overlay wake-up suite is included in the 54/54 API pass and the production build passes.

### Overlay disconnect cancellation — 2026-08-15

Closed the remaining local SSE waiter-lifecycle gap. The overlay route now
owns an `AbortController` for each hijacked stream and aborts it when the raw
request closes. Both the PostgreSQL wake-up waiter and the polling fallback
accept that signal, resolve immediately on disconnect, clear their timeout,
and remove their abort listener. This prevents a disconnected OBS/browser
stream from retaining a parked waiter until the polling window expires.

The change is resource cleanup only: durable event replay, cursor
acknowledgement, delivery state and no-drop recovery are unchanged. The API
test suite passes 54/54 and the API/web production build passes. Deployed
Cloud Run connection churn, network fault injection and OBS/browser evidence
remain open launch gates.

### Current local boundary

The implementation is intentionally not calling L03 complete yet. The approved FRD-011 core configuration schema, semantic validation, authenticated editor and bounded core preview are implemented. L03-09 now has an active catalogue contract in `../active/launch/04_TEMPLATE_LIBRARY_AUTHORITY.md`; it remains blocked on completion and visual verification of the 359 missing runtime packages and browser/accessibility evidence defined in `TC-L03`. By owner direction, generation of additional BSA packages is deferred to the final implementation pass after the non-visual v1 gates; this does not reduce the approved 600-design scope. No arbitrary config editor or unapproved branding keys are accepted. Cross-replica overlay replay, live provider checkout and staging/browser evidence also remain open.

### Explicitly outside L03

- Razorpay webhook/order/refund/reconciliation implementation: L04.
- Cloud Tasks alert dispatch, per-queue outbox progression, TTS and overlay fan-out implementation: L05.
- Scheduler ownership and cron repository: L06.
- React Native, WinUI 3, or SwiftUI clients: L07.
- Marketing content, support operations, legal/provider sign-off: L08.
- YouTube and Enterprise: Phase 2; no route, scope, navigation item, claim or database read may be added by L03.

## Non-negotiable implementation rules

- No browser/client direct database access, service credentials, provider secrets, raw webhook bodies, private audit records or internal topology.
- Google Sign-In is authentication only in v1; no YouTube scopes or channel-data requests.
- All channel actions are authorised server-side from the authenticated session and channel membership; client-supplied role, tier, channel, source or overlay ownership is never trusted.
- Public tip-page reads must use a reviewed narrow public projection/function that returns only approved presentation fields for an active handle. Never grant the public client or a general API query unrestricted `channels` table access; the projection must be covered by the L02 security review.
- Public tip order initiation is idempotent and rate-limited, but payment capture/settlement truth remains in the payment boundary. L03 must not mark a payment captured from a browser callback.
- Overlay credentials are short-lived, scoped and revocable. The credential is deliberately present only in the creator's copied OBS browser-source URL fragment and in-memory browser Authorization header; it must be absent from API request URLs, referrers, logs, analytics, rendered HTML and error messages. SSE is a wake-up optimisation; cursor/outbox replay is correctness-critical. Reconnect uses the last acknowledged cursor, not merely the last received frame.
- Multi-queue source routing is v1-approved. No bindings UI ships until L-31 source/priority correlation and L-32 per-source override enforcement are verified in staging. Local implementation evidence now covers source/priority resolution, immutable snapshots and per-queue overlay projection. Each permitted queue has independent durable delivery state.
- Duplicate routing consent is enforced at both boundaries: the Go payment router emits multiple binding-backed delivery rows only when every matching binding has `allow_duplicates=true`; mixed or absent consent falls back to the highest-priority binding. Migration `0021_v1_l03_duplicate_consent_guard.sql` rejects a second binding-backed delivery when either the new or existing binding lacks consent, while preserving explicit multi-queue manual/test selection that has no binding row. This is local evidence only; staging/cross-replica proof remains open.
- Limits may delay, hold, aggregate where approved, or request operator action; they may not drop an accepted payment/alert evidence record.
- Feature flags and reversible migrations isolate each surface. Never run two production writers for the same payment/queue state.

## Definition gate

The owner approved the foundation implementation on 2026-08-14. Domain implementation still requires the final endpoint/field contract, synthetic test plan, privacy/security boundaries and rollback method recorded in the acceptance and review records.

## Acceptance criteria

- Every public/client request uses documented REST contract, not direct DB access.
- A creator can complete authenticated setup, create a tip page, add an overlay, test it and manage queues/configuration.
- Overlay reconnect resync proves no accepted alert is silently lost.
- Public pages disclose only approved information and expose no internal topology/security detail.
- Accessibility, responsive, localisation and browser-source acceptance cases pass.

## Evidence required for closure

- Dated contract-validation output for every L03 endpoint and payload.
- Dated browser/API integration evidence covering onboarding → tip page → test alert → overlay setup → queue/configuration management.
- Security evidence for authentication, RBAC/RLS context, CSRF/CORS/CSP, rate limits, SSRF-safe asset handling, overlay token lifecycle and secret/log redaction.
- Dated cross-replica overlay reconnect/resync evidence, including notification outage and independent multi-queue progression; these are shared L03/L05 gates.
- Accessibility/localisation/long-text/reduced-motion evidence with no clipping or overlap at configured preview and OBS sizes.
- Independent fresh review or an explicit conditional-complete record if unavailable.

## Rollback

Feature flags isolate each surface. Retain legacy UI only as a reference until final staging parity; do not route production traffic to both writers simultaneously.

## Shared-PostgreSQL cross-replica replay regression — 2026-08-15

The first real two-client/two-Fastify-instance overlay integration exposed and
closed a tenant-boundary defect in the replay projection. The previous
`get_overlay_events` function validated the overlay session token but did not
also require `event.channel_id = session.channel_id`; a valid session could
therefore enumerate delivery rows from another channel. Migration
`0054_v1_l03_overlay_event_channel_guard.sql` adds that predicate while
preserving the immutable delivery/config projection. The disposable harness
now starts separate SQL clients and API instances against one PostgreSQL
database, commits the event through the shared database, serves it through
replica B, acknowledges it through replica B, and confirms replica A no longer
replays it. The integration prints
`OVERLAY_CROSS_REPLICA_SHARED_POSTGRES_INTEGRATION=PASS`.

This closes the local SQL/API cross-replica correctness slice only. Neon direct
endpoint behavior, Cloud Run multi-replica deployment, network failure and OBS
staging evidence remain launch gates. No BSA visual package was generated.

## Overlay acknowledgement recovery fix — 2026-08-15

The browser overlay previously left a displayed group permanently active when
cursor acknowledgement returned a non-retryable `400` or `401`: the selected
items had already been removed from the in-memory queue, while their cursors
remained pending and the stream did not reconnect. That could stall the visual
queue even though the durable delivery remained stored.

The overlay now requeues only the unacknowledged acknowledgement suffix,
aborts the active SSE stream, reconnects from the last cursor confirmed by the
server, and resumes the requeued items after the replacement stream connects.
Unmount cleanup also aborts the active stream. The already-acknowledged prefix
is never requeued, preventing duplicate display after reconnect.

`requeueUnacknowledged` is covered by a focused regression test; the overlay
policy/TTS suite passes 10/10 and the production API/web build passes. This is
local client reliability evidence; browser/OBS, deployed SSE and staging
acknowledgement-failure evidence remain open.

## Post-replay-guard regression rerun — 2026-08-15

After migration `0055_v1_l03_unacknowledged_replay_guard.sql` and its
out-of-order publication case were added, the current worktree was rerun:

- `pnpm db:test:l03` passed, including `L02_SECURITY_REMEDIATIONS=PASS`,
  `L03_APPLICATION_BEHAVIOR=PASS`, the newer-acknowledged/older-unacknowledged
  replay case, cross-replica wake-up and per-queue checks.
- `pnpm test` passed 54/54; `pnpm build` passed the API TypeScript and web
  production builds; `pnpm contracts:validate` passed 11 fixtures, the v1
  catalogue contract and the OpenAPI 3.1 document with 32 paths.
- Payment and alert-worker Go modules passed `go test ./...`,
  `go test -race ./...` and `go vet ./...`.

This strengthens local implementation evidence only. Provider, deployed
Neon/Cloud Run/Cloud Tasks, authenticated browser/OBS, capacity/fault,
independent-review, legal and deferred visual-runtime gates remain open.

## Public tip response-boundary validation — 2026-08-15

The public tip form now validates the complete OpenAPI order and status
responses before using them. The browser requires the v1 envelope, Razorpay
provider, UUID local order ID, bounded provider-order identifier, exact
server-requested INR amount, approved lifecycle state and currency. Public
status accepts only the donor-safe `pending`, `paid`, `expired` and `failed`
states, with its v1/order identity and timestamp; internal provider states are
not accepted by the donor client. Unknown fields fail closed. Invalid or
mismatched responses fail closed without opening Razorpay Checkout or
declaring payment success; only the server-confirmed status projection can
move the donor surface to paid. Focused Web/API contract tests pass 19/19 and
the Web TypeScript check/build pass. Provider sandbox/live and
browser/staging evidence remain open.

## Overlay event-envelope validation — 2026-08-15

The browser overlay now parses the server's v1 SSE event envelope before it
enters the in-memory presentation queue. It requires the approved schema
version, bounded cursor/trace fields, UUID event IDs, valid timestamps, an
approved event type and an object payload. Invalid or unsupported data is
ignored without acknowledgement; the durable server-side row therefore remains
replayable after reconnect. Focused overlay/TTS tests pass 11/11 and the Web
TypeScript check and production build pass. This closes only the local browser
input-boundary slice; deployed/browser/OBS failure and cross-replica evidence
remain open.

## Web response-boundary hardening — 2026-08-15

- Added strict runtime parsing for authenticated channel details and overlay
  session responses in `apps/web/app/lib/api.ts`. Channel IDs, handles,
  display names, roles and version numbers are bounded before UI use.
- Overlay session responses now require a valid v1 envelope, UUID overlay ID,
  valid expiry, an HTTP(S) browser-source URL with the expected overlay path,
  no query/user-info component and a non-empty fragment-only credential. A
  malformed response cannot redirect an OBS setup user to an arbitrary URL or
  expose a credential in a query string.
- `apiFetch` converts decoder failures to the generic `Server response was
  invalid` message rather than surfacing an internal parser error to the UI.
- Added `apps/web/app/lib/public-channel-contract.ts` and tests for the narrow
  public-channel projection. Unknown fields, invalid handles, blank names and
  out-of-range minimums fail closed before donor-facing rendering.
- Extended runtime validation to authenticated configuration, queue, binding,
  alert-history, moderation, billing, entitlement and test-alert responses.
  The client now rejects invalid UUIDs, versions, enums, dates, ranges,
  unknown presentation override keys and malformed financial/plan fields
  before they enter dashboard state.
- Queue, history and mutation parsers normalize only the documented v1 fields;
  missing optional history financial/content fields become `null` rather than
  being rendered as arbitrary values. Decoder failures remain bounded and do
  not expose parser details.
- This is a local client response-boundary slice only. API contract, provider,
  deployed, browser/OBS and staging evidence remain required. No BSA visual
  package was generated or modified.

## Companion layout mutation response hardening — 2026-08-15

The authenticated Web Companion layout update now uses the same bounded
`parseCompanionLayout` decoder as the layout read path. The generic `apiFetch`
identity-decoder default was removed, so every JSON response path must provide
an explicit parser; the expected `204` overlay-revocation path now rejects an
unexpected response body. Duplicate layout slot indexes and malformed server
layout envelopes therefore fail closed before reaching the editor. Focused
contract tests and the Web TypeScript/production build pass locally. This is
local client evidence only; authenticated browser, deployed and staging
evidence remain open.

## Companion action response hardening — 2026-08-15

The Web Companion action client now validates the complete server-owned
`CompanionActionResult` envelope: schema version, command UUID, accepted or
rejected status, acceptance timestamp and optional synthetic event UUID.
Unknown fields and malformed values fail closed. The returned type now retains
the command/event identity for UI tracing instead of reducing the result to an
arbitrary status string. Focused contract tests and the Web TypeScript/
production build pass locally. This is local client evidence only;
authenticated browser, deployed and staging evidence remain open.

## Strict authenticated projection completion — 2026-08-15

The remaining authenticated Web parsers now enforce the reviewed
`additionalProperties: false` boundary at runtime instead of validating only
selected values:

- identity and channel projections require UUIDs, approved roles and only
  documented fields; channel avatar URLs are restricted to safe HTTP(S)
  values;
- queue, binding, history, billing, entitlement and Companion state/layout
  envelopes reject unknown top-level and nested fields;
- Companion slot labels, nested binding overrides and list envelopes are
  bounded and normalized;
- the entitlement client preserves the server-authored `source` field rather
  than silently dropping it;
- the bindings list has a named parser and negative coverage for expanded
  server projections.

Focused Web/API contract tests pass 19/19; the Web TypeScript and production
build pass. This closes the local response-boundary slice only. Provider,
deployed, authenticated browser/OBS, staging, capacity, external review and
visual-runtime evidence remain open. No BSA visual package was generated or
modified.

### Overlay display-timer cleanup — 2026-08-15

The browser overlay now retains the active display-completion timer and clears
it when the page unmounts or the effect is cancelled. A closed OBS/browser
source therefore cannot leave a stale completion callback running for the
remaining display duration. This is lifecycle/resource cleanup only; durable
acknowledgement still occurs only through the server response and no accepted
delivery is deleted or acknowledged by the cleanup path. Web production build,
API tests (54/54) and contract validation pass after the change.

### Overlay connection-status accessibility correction — 2026-08-15

The browser-source connection indicator now exposes an explicit `role="status"`
with a polite live label for connected and reconnecting states. Previously the
label was attached to a generic element, which was not a reliable assistive
technology boundary. The change is markup-only and does not affect delivery,
acknowledgement or overlay security. Browser/OBS accessibility evidence still
requires the authenticated staging matrix.

### Bounded Razorpay browser-asset handoff — 2026-08-15

The public tip form now uses `apps/web/app/tips/[handle]/razorpay-loader.ts` for
the browser-only Razorpay Checkout asset. The loader accepts only the exact
`https://checkout.razorpay.com/v1/checkout.js` source, reuses an already-loaded
asset, rejects a conflicting marked script, and fails within an 8-second
bounded timeout when the asset stalls. This prevents the donor form from
remaining indefinitely in a submitting state. It does not create, confirm,
retry or mark a payment; the private service, verified webhook and durable
ledger remain authoritative. Focused loader tests pass 5/5 and the Web
production build passes. Provider CSP, browser and staging evidence remains
open.
### Public tip idempotency-key boundary — 2026-08-15

The public tip-order route now applies the same bounded idempotency-key
contract as authenticated subscription creation: 16–128 characters from
`A-Za-z0-9._:-`. A malformed key is rejected before channel/payment-service
work begins and cannot be used to create a provider receipt or payment intent.
Valid keys are unchanged. API route tests pass 40/40 and the API TypeScript
check passes. This is local request-boundary evidence; provider, deployed,
staging and retry/reconciliation evidence remain open.
### Cross-surface idempotency-key contract — 2026-08-15

The OpenAPI component, public tip route, authenticated subscription route,
private Go checkout/subscription handlers and Companion action route now share
the same safe 16–128 character alphabet (`A-Za-z0-9._:-`). Missing Companion
keys retain the established required-key error, while present unsafe values
fail before durable command insertion. API/Go tests and OpenAPI validation pass
locally; provider, deployed, device and staging evidence remain open.

## Public tip request timeout and retry-key hardening — 2026-08-15

The public tip form now bounds the browser-to-API order request to a 10-second
default (configurable only within 1–60 seconds). Status polling uses a bounded
5-second request timeout. A timeout is treated as ambiguous rather than failed
payment state: the form retains the same idempotency key for a retry so a
delayed server response cannot turn a donor retry into a second local intent.
The key is retained until the Razorpay checkout handoff succeeds, so a created
order whose browser asset/modal fails can be retried without creating another
intent. Definite client validation responses clear it; provider/webhook/ledger
truth is unchanged. The pure timeout, abort, key-reuse and retention policy
tests pass 4/4, and the Web production build passes. This is browser-boundary
evidence; provider, network, deployed and staging behavior remain open.
