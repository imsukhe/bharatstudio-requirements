# AUD-MC-01 — Master Canvas bootstrap reconciliation retry

**Status:** `Conditionally complete — locally verified; independent review and external browser/OBS evidence pending`  
**Owner:** **Sukhdev Singh**  
**Authority:** `../launch/08_AUDIT_REMEDIATION_AUTHORITY.md` (AUD-MC-01)  
**Acceptance record:** `../../tests/TC-AUD-MC-01-master-canvas-bootstrap-retry.md`  
**Review record:** `../../reviews/2026-09-18-aud-mc-01-master-canvas-bootstrap-retry.md`

## Scope

Repair Master Canvas startup where the server-authoritative module-entitlement and
canvas-layout reads run once and never retry after a transient HTTP/JSON/network
failure. Add a small bounded bootstrap reconciler and a connection-lifecycle
subscription on the existing `MasterCanvasConnection`. The page performs an initial
reconcile and repeats it only after that same shared SSE transport establishes or
re-establishes a connection. Concurrent lifecycle signals coalesce; no timer polling,
per-module stream, second overlay token, or independent transport is allowed.

This covers `apps/web/app/overlay/canvas/[overlayId]/page.tsx`, the existing shared
connection, and deterministic unit/integration tests. It does not change module
definitions, overlay event delivery/acknowledgement, server entitlement decisions,
layout storage/API, data models, migrations, event contracts, or pricing.

## Security, privacy, and failure behaviour

- Reconciliation uses the existing fragment-token bearer request and existing scoped
  endpoints only. It creates no storage, telemetry, token copy, user data, or new
  query endpoint.
- Module entitlement remains fail-closed: a failed modules read never enables a module.
  A failed layout read preserves the last server-confirmed layout (or horizontal default
  before any confirmation); it never guesses vertical.
- A successful read applies only parsed server-authoritative values. A stale/late read
  after page teardown applies nothing. One failed read cannot prevent the other read's
  valid current result from applying.
- Reconnect storms cannot fan out unbounded reads: while a reconcile is in flight,
  lifecycle signals request at most one next reconciliation.

## Service boundary, deployment, kill switch, and rollback

This is client-side recovery on the existing API/SSE service boundary. The API remains
sole owner of entitlement and layout truth. No deployment variable, migration, feature
flag, or provider prerequisite is added. The existing standalone overlay continues as
the mid-stream rollback surface.

Rollback reverts the reconciler, lifecycle subscription, Canvas page call sites, and
tests together. No durable state requires repair. Disconnecting/disposing the page
removes the lifecycle subscriber and stops late application.

## Required verification

- Deterministic tests prove initial independent read failure, later shared-connection
  recovery, valid application, last-known-good retention, reconnect coalescing, and
  disposal safety.
- Connection tests prove the lifecycle listener shares the single existing transport,
  adds no event-payload parsing/subscriber, and tears down with the page listener.
- Run relevant Canvas/web suites, web typecheck/build, API regression, contract/harness
  checks, a source/diff hostile review, traceability regeneration, and doc consistency.

## External evidence gate

A safe browser/OBS rehearsal with network shaping must prove visible recovery after an
initial configuration-read failure or connection drop. Local tests prove only the
deterministic client state machine and one-transport invariant.

## Implementation and traceability reconciliation — 2026-09-18

Added a pure, bounded `canvas-bootstrap-reconciler` and a visibility-aware
`canvas-bootstrap-recovery` binding. Master Canvas now makes its existing immediate
modules/layout reads through the reconciler, then retries only when the existing shared
SSE connection reports a successful connection/reconnection. A new Canvas-page-only
lifecycle subscription is deliberately absent from the ordinary module interface, so a
module cannot obtain it or keep the transport alive accidentally. It is removed when
the source is hidden or the page disposes.

No data model, migration, API route/contract, module entitlement calculation, event
payload/acknowledgement rule, timer poll, storage path, provider call, or deployment
configuration changed. `git diff --check` passed. This corrective subtask leaves the
§31 register mapping unchanged and is linked through
`08_AUDIT_REMEDIATION_AUTHORITY.md`; `TRACEABILITY.md` is regenerated at closure.
