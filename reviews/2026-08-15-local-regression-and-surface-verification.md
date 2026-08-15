# Local regression and product-surface verification — 2026-08-15

**Scope:** local code and contract verification across the v1 repositories. This record is evidence for implementation progress only; it is not staging, provider, legal, store, production, or capacity approval.

## Executed checks

| Surface | Command/check | Result |
|---|---|---|
| Alerts API | `pnpm test` | 62 tests passed |
| Alerts contracts | `pnpm contracts:validate` | 11 fixture mappings, 35 OpenAPI paths and executable v1 capability exclusion scan passed |
| Alerts web/API | `pnpm build` | TypeScript/API build and Next production build passed |
| Alerts database | `pnpm db:test:l03` | L02 security, L03 application behaviour, payment ingress and worker-store integration passed in disposable PostgreSQL |
| Overlay policy | `pnpm --filter @bharatstudio/alerts-api exec tsx --test ../../apps/web/app/overlay/overlay-policy.test.ts` | 6 tests passed |
| Payment service | `go test ./... && go vet ./... && go test -race ./...` | Passed |
| Alert worker | `go test ./... && go vet ./... && go test -race ./...` | Passed |
| Scheduler repository | `npm test` | 2 tests passed; all v1 schedules remain disabled |
| Infrastructure repository | `npm test` | 8 deployment-contract tests passed; manifest remains `not-deployable` and contains no credentials |
| Marketing repository | `npm test` | 5 tests passed |
| Companion mobile | `npm run test:dependencies && npm test -- --runInBand && npm run lint && npm run typecheck` | Dependency hardening 2/2, Jest 52/52, lint and TypeScript passed; native/provider/device evidence remains open |
| Companion macOS | `swift test` | 12 tests passed |
| Payment container | service-local `docker build --file Dockerfile --tag bsa-payment-webhook:local .` | Static distroless image built; runtime identity is declared non-root; container runtime smoke not run |
| Alert-worker container | service-local `docker build --file Dockerfile --tag bsa-alert-worker:local .` | Static distroless image built; runtime identity is declared non-root; container runtime smoke not run |

The scheduler/maintenance slice was re-run after the L06 ownership correction:
the disposable PostgreSQL harness passed `L02_SECURITY_REMEDIATIONS=PASS` and
`L03_APPLICATION_BEHAVIOR=PASS`, including idempotent maintenance-run handling,
overlay-session expiry/retry, cross-service job rejection, multi-queue delivery
projection and Companion durable test-alert creation. This is local evidence;
Cloud Scheduler, OIDC audience bindings, deployed private handlers and staging
recovery remain open.

The latest rerun after the L02 privilege-audit hardening again passed both
database markers. In addition to the role/grant assertions, the run now checks
every current `app_private` `SECURITY DEFINER` helper for a fixed
`search_path` and denial of `PUBLIC` `EXECUTE`. This is isolated PostgreSQL
evidence only; independent security review and deployed-role verification
remain open.

### Companion control-session lease slice — 2026-08-15

Migration `0053_v1_l07_companion_control_sessions.sql` adds the server-owned
operational lease boundary for Web/Mobile/Desktop Companion clients. The
transaction-scoped channel lock makes expiry, same-client renewal and Free-tier
single-session admission deterministic on pooled connections. The request role
has no direct insert/update/delete permission; revoked and expired rows remain
stored for audit. The lease path is explicitly independent of payments,
queues, outbox and alert delivery.

Result: PASS in the disposable PostgreSQL 16 harness. First acquisition,
idempotent renewal, competing Free client rejection, revocation, reacquisition
and direct-write denial passed. Native pairing, OBS authentication, device
matrix, store/signing and deployed evidence remain open.

The authenticated API and mobile client were then aligned to the lease
boundary. Alerts exposes channel-scoped POST acquire and DELETE revoke routes;
the database revoke function checks the supplied channel against the stored
session before changing state. The mobile `CompanionApi` validates the finite
client types and 16–128-character instance identity, exposes acquire/revoke,
and treats HTTP 204 as a successful empty response. API tests passed 52/52,
the Alerts API/web build passed, OpenAPI validation passed with 32 paths, and
mobile Jest passed 16/16 with lint and TypeScript passing. This remains local
contract evidence only: no authenticated device, native helper, OBS pairing,
Cloud Run, IAM or store-release evidence is claimed.

## Browser smoke evidence

With the production web build served locally at `http://localhost:3100`, the
routes `/`, `/dashboard`, `/tips/demo_creator`, `/overlay/setup`, `/login`,
and `/companion` rendered without browser console errors.

- Unauthenticated dashboard and overlay setup fail closed with an explicit
  authentication state.
- The public tip page shows a safe closed/disabled state when its approved
  public-channel API is unavailable; it does not fabricate payment success.
- The overlay without a credential remains in the reconnecting state and does
  not expose a token in the URL.
- Companion renders read-only state when authentication/API state is absent and
  does not attempt a localhost OBS connection.

This is local browser smoke evidence only, not authenticated
Google/Razorpay/OBS or cross-replica staging evidence.

The same local production build was rechecked on 2026-08-15 across `/`,
`/dashboard`, `/tips/demo_creator`, `/overlay/setup`, `/login` and
`/companion`: all six returned the expected main content with zero captured
browser error logs. On the unauthenticated dashboard surface, the basic
accessibility/overflow scan found one `main`, one `h1`, no missing image alt
attributes, no unlabeled form controls, no unnamed buttons and no horizontal
overflow. This is a smoke check, not a WCAG conformance audit or authenticated
device/browser matrix.

The browser API-origin guard was also verified locally: focused tests pass 3/3
for development fallback, missing/invalid production configuration,
localhost/non-HTTPS rejection and valid HTTPS normalization. The web
production build passes. This prevents a missing production build variable
from silently targeting a viewer's localhost; it does not prove the deployed
origin, certificate or reverse-proxy configuration.

### API burst limiter correction — 2026-08-15

The API burst test initially exposed that Fastify's rate-limit error was being
converted by the generic error handler into HTTP 500. The handler now maps a
429 to the versioned `rate_limited` envelope, preserves the plugin's
`Retry-After` header and marks the response retryable. A synthetic 120-request
burst followed by request 121 now passes with 120 successful responses and one
bounded 429. This protects the API ingress only; the durable per-source alert
rate policy remains delay-only and cannot drop an accepted alert.

## Companion action no-op remediation

## Full local regression sweep — 2026-08-15

After the Companion channel/queue targeting changes, the complete local sweep passed:

- Alerts API: 48 tests; web/API production build; 11 contract fixtures and 29 OpenAPI paths.
- PostgreSQL disposable harness: `L02_SECURITY_REMEDIATIONS=PASS`, `L03_APPLICATION_BEHAVIOR=PASS`, including payment/worker integration assertions.
- Payment Go service: `go test ./...`, `go vet ./...`, `go test -race ./...`.
- Alert-worker Go service: `go test ./...`, `go vet ./...`, `go test -race ./...`.
- Companion mobile: 16 Jest tests, lint and TypeScript; current audit remains 8 high transitive findings with no safe automated fix.
- macOS shell: `swift test`; crons: one schedule-contract test; marketing: three static-site tests.

These are local/synthetic results only. They do not substitute for Razorpay approval/sandbox/live evidence, deployed Cloud Run/Cloud Tasks/IAM, cross-replica SSE/no-loss staging, Windows build/signing, mobile store/device review, or legal/support/independent review.

### Companion action-layout completion — 2026-08-15

The approved tiered Companion configuration slice is now implemented locally. Migration `0042_v1_l07_companion_action_layout.sql` stores append-only layout versions, uses RLS for member reads, permits writes only through a `SECURITY DEFINER` validation function for owner/admin/operator roles, and serializes version creation transactionally. It enforces the approved Free/Pro/Creator/Studio limits of 8/16/32/64 slots, page sizes of 4/8/16 only when within the tier allocation, unique slot indexes, finite action names and active same-channel queue targets. A rejected layout cannot modify accepted payment, event, outbox or delivery evidence.

The API exposes `GET/PATCH /v1/channels/{channelId}/companion/layout` with strict schemas and optimistic `If-Match-Version`; the Web Companion page can add/remove only approved actions and save a server-owned layout; the mobile client reads/saves the same contract. Local evidence: `pnpm db:test:l03` passes with Creator 32-slot persistence, operator save, moderator denial, 33-slot rejection and durable test-alert preservation; Alerts API tests pass 48/48; web build passes; contract validation passes with 29 OpenAPI paths; mobile Jest passes 16/16 plus lint and TypeScript.

This closes the local implementation slice of L07-04/L07-11. It does not close device/store, Windows, authenticated browser, cross-tier device, accessibility, pairing/revocation, or independent-review gates.

The local review found that the original six-value Companion action type could
accept `approve_alert`, `hold_alert` and `replay_alert` even though the command
store only changed queue state for pause/resume. That was unsafe because a
successful response could imply an effect that did not occur.

The v1 contract is now narrowed to `pause_queue`, `resume_queue` and
`send_test_alert`. The API rejects a missing queue target before persistence.
`send_test_alert` creates the manual alert, outbox row and per-queue delivery in
the same transaction as the idempotent command, stores `result_event_id`, and
returns that event on retries. Approve/hold/replay continue through the
authenticated moderation endpoint until their Companion target and transition
semantics are implemented. This preserves a truthful command contract and
cannot remove or mutate a payment record.

Evidence: `pnpm test` (50 API tests), `pnpm db:test:l03` (L02 security and L03
application behavior PASS, including one-event/one-delivery Companion test),
`pnpm contracts:validate`, and mobile Jest/lint/typecheck all pass locally on
2026-08-15.

## Entitlement enforcement correction

The API queue store now reads the server-owned `values.queueCount` entitlement
and rejects only new queue creation once the channel has reached that count.
The count includes soft-closed queues so close/reopen cannot bypass a plan
limit. Missing limits remain explicitly unlimited until the active authority
publishes final tier values. This check cannot delete, acknowledge, delay or
otherwise alter an already accepted payment, alert, delivery or outbox row.
The API unit suite covers valid, absent and malformed entitlement values; the
queue route remains covered by the SQL/RLS path and the Companion acceptance
record now names this server-side guard.

Evidence: `pnpm test` (50 API tests), `pnpm build`, `pnpm contracts:validate`,
and the disposable PostgreSQL harness passed locally on 2026-08-15. Cross-tier
staging/device evidence and final entitlement values remain release gates.

## Security and stale-readiness scan

- No stale `READY FOR LAUNCH`, `production deployment ready`, `launch same day`, `security checklist passed`, or `1000 concurrent` claim remains in the active product repositories.
- The only matching operational wording is an explicit statement that the worker runbook does **not** claim production readiness.
- Razorpay webhook identity is explicitly `x-razorpay-event-id`; no timestamp/random fallback is used for provider-event deduplication.
- Production/staging configuration requires a separate `DATABASE_URL_DIRECT`; the overlay listener uses a single direct connection and is never configured against the pooled app endpoint.
- The production/staging config test also rejects invalid PostgreSQL URL schemes and known pooled Neon forms for `DATABASE_URL_DIRECT`, including `-pooler` hosts and `pgbouncer=true`; this is startup hardening, not live endpoint proof.
- The Alerts maintenance HTTP boundary rejects payment/refund, outbox and archive jobs before invoking the API store; those jobs cannot return a false success through the wrong service.
- The infrastructure contract test now enforces service-specific database secret references, registered Alerts API route prefixes and explicit Alerts web build variables (`API_ORIGIN`, `NEXT_PUBLIC_API_ORIGIN`, Google client ID and public Razorpay key): only the Alerts API receives the direct listener secret, while payment and worker services receive their own database references. `bharatstudio-infra` passes 7/7; no secret values are present.
- The same contract enumerates the required runtime environment names for all three bootstraps, including payment-to-worker pump configuration and Cloud Tasks target inputs; values remain deployment placeholders and are not treated as provisioned.
- Cloud Tasks OIDC audience wiring was audited and corrected locally. The worker now passes the canonical `ALERT_WORKER_PRIVATE_AUDIENCE` explicitly into task creation, and the Google adapter uses that value instead of deriving an audience from the target URL. The infrastructure manifest and deployment test require the same canonical placeholder. Alert-worker Go tests, race tests and `bharatstudio-infra` 7/7 contract tests pass; live token, IAM and private-route evidence remain open.
- The payment-to-worker pump relationship is now explicit in the infrastructure contract: `ALERT_WORKER_PUMP_AUDIENCE` must match `ALERT_WORKER_PRIVATE_AUDIENCE`. This prevents a caller/verifier audience mismatch from being hidden in deployment variables; values and IAM still require live negative testing.
- The Companion action contract was audited against the database as well as the API. Migration `0041_v1_l07_companion_action_contract.sql` now rejects the three removed legacy action names for new rows while preserving historical command evidence; the L03 disposable harness applies it.
- Migration `0042_v1_l07_companion_action_layout.sql` now provides append-only, RLS-protected layout snapshots with server-owned 8/16/32/64 tier limits, approved 4/8/16 page sizes, optimistic versioning, same-channel active-queue validation and no arbitrary commands. The harness proves Creator 32-slot persistence, operator save, moderator denial, over-limit rejection and preservation of the durable Companion test alert. The Web Companion editor and OpenAPI path use the same contract.
- Companion client parity was also corrected: the mobile API enforces the server's 16–128-character idempotency-key contract and reads/saves the versioned layout contract before network use. Mobile Jest passes 16/16, lint and TypeScript pass; this is client-contract evidence, not device/store evidence.

## Remaining findings and gates

### Companion dependency audit recheck — 2026-08-15

`npm audit --omit=dev --audit-level=high --json` was rerun against the current
React Native 0.87.0 / Community CLI 20.2.0 scaffold. It reports 8 high
findings across React Native, Metro and `image-size`, with no critical
findings. npm's only automatic fix is an incompatible React Native 0.72.17
downgrade; it was not applied. A narrow `patch-package` hardening patch now
guards malformed zero-length HEIF/ICNS/JXL parser boxes and is verified after
a clean install, including a fail-fast malformed-ICNS regression (2/2
dependency checks). The patch is mitigation evidence, not a cleared registry
audit; release still requires an upstream fixed dependency or an explicit
security risk decision with mitigation.

1. The mobile dependency audit now reports eight high-severity transitive findings in the React Native/Metro/image-size graph after removing the unused template screen package. The only automated React Native fix offered by the audit is an unsafe major downgrade; this requires remediation or explicit risk acceptance before release.
2. Windows cannot be built or signed in this macOS-only workspace. WinUI 3/C# implementation and the Windows device/security matrix remain open.
3. macOS is a shell only; pairing, Keychain session storage, OBS WebSocket authentication, revocation and notarised distribution remain open.
4. Mobile device matrices, store accounts, package identifiers, signing, privacy declarations and store review remain open.
5. Razorpay Technology Partner/creator-direct connected-account approval and sandbox/live evidence remain open.

### Mobile multi-channel Companion correction

The mobile shell previously selected `channels[0]` unconditionally and exposed pause/resume callbacks without the queue target required by the server contract. It now uses the server-provided `companionState.channelId` when available, renders every authorised channel, loads the documented queue-list contract through `CompanionApi`, renders active queue selection, and emits channel/queue callbacks. Queue controls remain enabled only for the selected channel's operator-capable role and an active queue; the shell does not invent metrics or imply a target for an unloaded channel.

Evidence: mobile Jest (16 tests), lint and TypeScript checks pass locally on 2026-08-15. Native device, authentication, reconnect and store evidence remain open.

The Web Companion Console had the same unsafe default: it loaded only the first channel and always used `queues[0]` as the command target. It now loads the selected authorised channel, refreshes its state and queues on channel change, selects an active queue explicitly, and disables commands when no valid target exists. The web build, 48 API tests and OpenAPI/fixture validation pass; browser multi-channel and deployed API evidence remain open.

### Overlay SSE replay boundary — 2026-08-15

The API test suite now includes an HTTP-level replay case proving that an event
arriving after the initial replay is emitted during the same bounded SSE
window, and that a reconnect carrying `Last-Event-ID` resumes after the
acknowledged cursor without re-emitting the earlier event. This is synthetic
store/wakeup evidence. It now also runs two API instances with separate wake-up
paths over one shared durable replay model: an event committed through the
replica-A model is delivered exactly once to the replica-B stream. This is
cross-instance application evidence, not cross-replica database, notification-
outage or live OBS evidence; those remain open. A separate no-wakeup test also
proves the bounded polling/replay path still emits a durable event when the
notification optimisation is unavailable.

### Web Companion browser smoke — 2026-08-15

The local Web Companion route was opened at `http://localhost:3100/companion`
without an authenticated session. It rendered the bounded Authentication
required state, did not fabricate a channel, queue, overlay or payment value,
and exposed no direct OBS/localhost command path. Browser diagnostics contained
no warning or error entries. This proves only the unauthenticated safety
surface; authenticated multi-channel selection, queue targeting and command
authorization still require an authenticated browser/API run.

### Local overlay browser smoke — 2026-08-15

The web development build was served at `http://localhost:3100` and the public
home route loaded with the expected bounded foundation state. The overlay route
loaded without a credential and stayed in the safe `Overlay reconnecting` state;
it did not render a fabricated alert, expose a provider error, or create a
client-side delivery. The browser console contained no warning or error entries,
and the rendered overlay DOM exposed an accessible connection-status label. This
is only a shell/safety smoke check: a real scoped session, event rendering,
multiline/Indic text, reduced-motion, acknowledgement retry, accessibility
matrix and OBS browser-source run still require authenticated staging evidence.

### API error-log privacy hardening — 2026-08-15

The API previously passed raw caught errors to Fastify logging from channel,
queue, binding, alert, overlay, Companion, maintenance and public payment
routes, as well as from the unhandled-error handler. That could serialize a
database/provider message or stack containing identifiers, SQL details or
user-controlled text. `apps/api/src/observability/safe-log.ts` now reduces
errors to a fixed type category and records only bounded event, trace and
explicit context labels. `apps/api/test/safe-log.test.ts` proves synthetic
donor/SQL text and stack content are absent, and a source audit found no raw
error-object API logging call sites. The API suite passes 48/48. This is local
code-level redaction evidence; deployed log sink IAM, retention, collection
and alert-policy verification remain open.

### Payment account-routing correction

The local payment schema resolves a Razorpay account per channel, but the first Go runtime slice used one global `RAZORPAY_CONNECTED_ACCOUNT_REF`. That would have allowed a multi-creator deployment to create or read provider resources under the wrong account. The runtime now carries the immutable intent account into `X-Razorpay-Account`, uses account-scoped provider reads for reconciliation, derives webhook account attribution from the signed `account_id`, and fails closed when it is absent. Migrations `0034_v1_l04_reconciliation_account_attribution.sql` and `0035_v1_l04_refund_account_attribution.sql` extend reconciliation candidates. This is locally tested; provider approval, sandbox/live evidence, and deployed validation remain open.

### Payment routing before provider ID assignment

The clean v1 flow now provisions a reserved `__channel_default__` payment
binding for every active queue, including queues created after migration. This
allows a creator to configure routing before Razorpay has generated a payment
ID. The payment ingress query and both persistence functions use the default
only when no exact provider-payment binding exists; exact source bindings stay
authoritative, and a stale default route is rejected at persistence. Migration
`0036_v1_l03_default_payment_binding.sql`, the queue-creation transaction and
the disposable PostgreSQL harness cover this locally. This does not prove live
Razorpay delivery, Cloud Tasks, or cross-replica staging behavior.

### L05 ready-delivery burst boundary — 2026-08-15

The alert-worker pump now has a synthetic 1,000-candidate burst test. A healthy
pass creates one stable command per candidate; a deterministic subset of
enqueue failures returns retryable partial status without acknowledgement, and
a later healthy scan recovers every candidate. `go test ./...`, `go vet ./...`
and `go test -race ./...` pass. This proves local pump-boundary no-drop and
retry behavior only; it is not Cloud Tasks, database, overlay, or production
capacity evidence.

### Bounded TTS playback boundary — 2026-08-15

The browser overlay now uses `apps/web/app/overlay/tts-runtime.ts` to cap
audio playback start at 1.5 seconds. Resolved playback succeeds, rejected
playback returns failure, and a permanently pending playback promise pauses
and returns failure so the overlay can invoke its non-blocking chime. The
visual group and durable cursor acknowledgement remain independent of this
side effect. Focused tests pass; this does not verify Sarvam or another live
provider, browser autoplay policy, audio asset quality, or OBS behavior.

Focused command evidence: `../bharatstudio-alerts/apps/api/node_modules/.bin/tsx
--test apps/web/app/overlay/tts-runtime.test.ts` passed 3/3 and the existing
overlay policy test passed 6/6. The web TypeScript check and production build
passed. The broader regression also passed: Alerts API 48/48, contract
validation (11 fixtures plus template catalogue and 29 OpenAPI paths),
disposable PostgreSQL L02/L03 harness, payment Go tests/vet/race, worker Go
tests/vet/race, crons 1/1 and infra 7/7.

### Binding lifecycle and identity guard

The staged binding control slice now exposes authenticated update semantics for
future duplicate consent, priority, safe override values and active state. The
reserved `__channel_default__` payment binding cannot be closed. Migration
`0037_v1_l03_binding_identity_guard.sql` additionally rejects rewriting a
binding's channel, queue or source identity through a broad SQL write path, so
future routing edits cannot invalidate the identity used by audit and accepted
delivery snapshots. The dashboard controls are disabled unless
`NEXT_PUBLIC_ENABLE_BINDINGS_UI=true`; L-31/L-32 staging verification remains a
release gate.

Migration `0038_v1_l03_open_binding_queue_guard.sql` additionally rejects a new
binding whose queue is already closed. Existing rows are retained for audit and
snapshot integrity; reopening the queue remains the explicit path to future
routing. The disposable L03 harness covers this negative case.

### L09 local trace-correlation contract — 2026-08-15

The local observability contract is recorded at
`bharatstudio-alerts/docs/architecture/OBSERVABILITY_TRACE_CONTRACT.md`.
Worker task validation now rejects blank, over-128-character and
control/separator-containing trace values; a valid task preserves its trace,
event and delivery identifiers through JSON serialization. The disposable
PostgreSQL L03 harness now asserts that a verified synthetic Razorpay event's
server-derived `razorpay:provider-event-1` trace remains on the alert event,
both independently routed delivery rows, and `get_overlay_events` replay.
Worker Go tests/vet and the L03 harness passed.

This closes only the local trace-contract slice. Deployed structured-log
collection, dashboards, alert routing, cross-replica listener proof,
capacity/load measurement and fault-injection rehearsal remain L09 staging
gates.

The payment and alert-worker runtimes also now emit bounded JSON operational
events at webhook/task boundaries. The event logger has no arbitrary-field or
error/payload parameter and omits invalid trace values. Both service test,
vet and race suites pass. This verifies local redaction behavior, not the
production log sink's IAM, retention, dashboard or alert-policy configuration.

### Local browser safety rerun — 2026-08-15

With the web development server on `127.0.0.1:3100`, the real overlay route
`/overlay/test` was opened without a credential. It remained in the bounded
`Overlay reconnecting` state, did not fabricate an alert/provider result, and
reported no browser warning or error entries. The real `/companion` route was
also opened unauthenticated: it rendered the sign-in-required state, no
channel/payment/queue value was fabricated, and its visible policy states
that the web surface has no direct OBS or localhost command path. No browser
warning or error entries were recorded. This is local unauthenticated safety
evidence only; authenticated staging, real overlay sessions, event rendering,
OBS browser-source, accessibility and cross-replica tests remain open.

6. Cloud deployment, IAM/OIDC, domain/certificate/WAF/secrets, database plan/region, backup/restore and measured capacity remain open.
7. Cross-replica SSE replay, notification outage, Cloud Tasks retry, failure injection, rollback and no-loss rehearsal remain staging gates.
8. Legal/CA/privacy/provider/support approval and public policy publication remain open.

9. The launch authority includes approved template-library integration. The
   active catalogue contract is now present, but runtime package completion,
   visual verification and browser/accessibility evidence remain open. The
   implementation correctly keeps branding/template/HTML inputs unavailable
   until the approved catalogue and package checks pass.

### Template catalogue contract audit — 2026-08-15

The active catalogue contract is now recorded at
`active/launch/04_TEMPLATE_LIBRARY_AUTHORITY.md` and
`bharatstudio-alerts/contracts/template-catalogue.json`. Read-only inspection
of the source library found 600 metadata records across 30 families and 12
event types, but only 241 complete runtime packages. The BSA-037 metadata
exception (`v37` instead of the approved family sequence) was corrected to
`v17`; L03-09 remains implementation/visual-verification blocked until the
359 missing packages are resolved.

### Current-state reproducibility rerun — 2026-08-15 (superseded snapshot retained)

The two Go service Dockerfiles were rebuilt from the current source using
multi-stage static builds and non-root distroless runtime images:
`bsa-payment-webhook:local` and `bsa-alert-worker:local`; both builds passed.
That earlier snapshot recorded the API suite as 41/41. The current suite is
47/47; the older numbers are retained only as historical evidence and must not
be used as the current status. The current API suite, OpenAPI/fixture
validation (10 fixtures and 29 paths), web production build, disposable
L02/L03 PostgreSQL harness, payment and worker Go test/vet/race suites, infra
contract (7/7) and crons contract (1/1) also passed. This confirms
reproducibility of local evidence only; it does not convert the deployment,
provider, browser-source, capacity or independent-review gates into passes.

### Role-scoped financial read hardening — 2026-08-15

The L03 audit found that the prior history projection returned gross amounts
and donor content to every channel member, while the base `bsa_app` payment
and refund policies allowed raw financial reads for every member. This did not
alter or delete financial/alert evidence, but it exceeded the approved
least-privilege boundary.

Migration `0039_v1_l03_role_scoped_financial_reads.sql` now enforces the
approved matrix in both the database projection and RLS policies:

- owner/admin: financial history fields, alert content and raw payment/refund
  rows;
- operator/moderator: alert content and moderation context, without financial
  amounts or raw payment/refund rows;
- viewer: delivery/status metadata only, without donor or financial details.

The disposable PostgreSQL L03 harness creates synthetic members for all four
roles and verifies the projection plus direct payment-read boundary. The full
L02/L03/L04/L05 harness passes after the migration; API 48/48, web build and
payment/worker Go test, vet and race suites also pass. Deployed RLS role
provisioning, authenticated browser evidence and independent review remain
open launch gates.

### Overlay and Companion role-boundary hardening — 2026-08-15

The follow-up audit found two policy/UI mismatches. The base overlay policy
allowed every channel member to manage an OBS session credential, and the base
Companion-command policy allowed moderators to insert queue-control commands
even though the approved Web/Mobile control surface exposes those controls only
to owner/admin/operator roles.

Migration `0040_v1_l03_overlay_companion_role_guards.sql` corrects both at the
database boundary:

- overlay session create/read/rotate/revoke is limited to owner/admin/operator;
- Companion queue commands are limited to owner/admin/operator;
- moderator access to the separate moderation route is unchanged;
- viewer and moderator UI restrictions are now backed by RLS rather than being
  client-only behavior.

The disposable harness proves operator allowance, viewer overlay-management
denial and moderator Companion-command denial. The local result is passing;
authenticated browser, cross-tenant staging and independent security review
remain open.

### Local browser surface rerun — 2026-08-15

With the Alerts web development server on `127.0.0.1:3100`, the actual home,
public tip, overlay, overlay setup and Web Companion routes were loaded without
credentials. The overlay stayed in the bounded `Overlay reconnecting` state;
the public tip page showed the closed-tip state and ₹10 minimum copy without
activating checkout; overlay setup left session creation disabled without an
authenticated channel; and Companion showed sign-in-required/read-only state
without fabricated channel, payment or queue data. The browser emitted no
warning/error entries on these routes. This is unauthenticated local smoke
evidence only; authenticated event rendering, accessibility/Indic/reduced-
motion matrices, OBS browser-source and cross-replica staging evidence remain
open.

### Current cross-repository regression rerun — 2026-08-15

From the current worktree, contract validation passed for 11 fixtures plus the
v1 template catalogue contract and the OpenAPI 3.1 document with 29 paths.
Payment and alert-worker Go suites passed with `go test`, `go vet` and
`go test -race`. The infrastructure validator passed 7/7 and the scheduler
contract passed 1/1 with schedules still disabled pending private endpoint/IAM
evidence. These results reconfirm local implementation health; they do not
close provider, deployment, capacity, store-review, legal or independent-review
gates.

The canonical `http://localhost:3100` browser rerun loaded the same five
surfaces with no browser warning/error entries. The overlay remained bounded
to `Overlay reconnecting`, while the other routes retained their safe
unauthenticated states. The earlier `127.0.0.1` run is retained as an initial
smoke only; this canonical-origin run is the preferred local browser evidence.

## Disposition

All locally executable implementation and regression checks above are recorded as passed. L00–L10 must remain short of `Verified` until the external and staging evidence listed above is attached to the relevant acceptance records. No local test result in this document authorises a production migration or public launch.

### Payment webhook permanent-error classification — 2026-08-15

The Go payment ingress now distinguishes permanent verified-payload errors from retryable infrastructure errors. Malformed/unsupported signed payloads return bounded 400 without invoking the worker pump. A persistence function that has durably recorded a quarantine returns 200 with status quarantined and does not invoke the pump. Database, provider, and pump availability failures remain retryable 503. Focused ingress/observability/webhook tests, go vet, and go test -race pass. This is local boundary evidence; provider retry semantics and deployed delivery remain staging/provider gates.

### Channel-specific minimum-tip enforcement — 2026-08-15

The public tip contract previously exposed only the platform ₹10 floor even
though approved channel configuration allows a creator to choose a higher
minimum. This is now fixed across the public projection, web form, API
boundary and database intent boundary. Migration
`0043_v1_l03_l04_channel_tip_minimum.sql` exposes the latest valid configured
minimum, the API rejects below-policy amounts before calling the payment
service, and a database trigger rechecks the value before inserting
`payment_order_intents`. The API suite and disposable PostgreSQL L03 harness
pass. This is local evidence only; deployed migration, provider sandbox and
staging checkout evidence remain open.

### Cloud Tasks cross-language command contract — 2026-08-15

The v1 contract tree now includes an explicit Cloud Tasks command schema and
golden fixture. The command requires the approved `deliver_overlay` action,
UUID event/outbox/delivery identities, trace, `createdAt` and `deadline`.
The Go worker stamps and validates those lifecycle fields and consumes the
committed fixture in a compatibility test. `pnpm contracts:validate` now
passes 11 fixture mappings and 29 OpenAPI paths; worker `go test`, `go vet`
and `go test -race` pass. This closes local envelope-drift evidence only;
Cloud Tasks queue/IAM, deployed retry/DLQ and staging no-loss rehearsal remain
open.

### Payment checkout lifetime hardening — 2026-08-15

The local public route continues to propose a fifteen-minute checkout intent.
The private Go checkout boundary now rejects an expiry beyond that maximum, and
migration `0045_v1_l04_payment_intent_expiry_cap.sql` applies the same rule in
the database security-definer write path plus a table constraint. The Razorpay
order adapter does not send `expire_by`; the browser now sends Razorpay's
documented `timeout: 900` seconds. Late-authorized-payment/refund behavior
remains provider/staging work. `go test ./...`, `go vet ./...`, and
`pnpm db:test:l03` pass after this change; the web production build remains
passing from the current local regression.

### Full local regression rerun — 2026-08-15

The current Alerts worktree was rerun after the checkout-lifetime change. The
API suite passed 48/48, the TypeScript production build and Next production
build passed, and contract validation passed for 11 fixtures plus the v1
template catalogue and OpenAPI 3.1 with 29 paths. The disposable PostgreSQL
harness passed both `L02_SECURITY_REMEDIATIONS` and
`L03_APPLICATION_BEHAVIOR`, including the new database rejection for an
overlong payment-intent expiry.

The payment-webhook Go service and alert-worker Go service both passed
`go test -race ./...` and `go vet ./...`. The scheduler repository passed
2/2 tests and the infrastructure repository passed 8/8 tests. The current
web build produced the expected public, dashboard, Companion, overlay and
tip routes. Mobile, macOS and marketing results remain covered by the earlier
same-day regression evidence and were not rerun in this command.

These are local implementation and regression results only. Razorpay partner
approval, provider sandbox/live behavior, deployed IAM/secrets, Cloud Tasks,
cross-replica SSE/overlay delivery, capacity, OBS, accessibility matrix,
store review, legal/compliance and independent review gates remain open.

### Retention-only archive correction — 2026-08-15

The first run of the new soft-archive migration exposed a missing RLS policy
for the `bsa_archive_owner` function owner. That role had the intended table
grants but could not read the archive row while running the security-definer
function. Migration `0047_v1_l02_soft_archive_only.sql` now grants only the
RLS paths required by the two whitelisted operational archive functions and
uses the source-row lock for concurrency; it does not grant archive-row
UPDATE/DELETE and does not physically delete source rows.

`pnpm db:test:l03` was rerun successfully after the correction. The run
passed `L02_SECURITY_REMEDIATIONS`, `L03_APPLICATION_BEHAVIOR`, payment
ingress SQL integration and alert-worker store SQL integration. The proof
asserts destination digest/identity, retained and marked source rows,
normal-read hiding, restore, repeat archival, no direct delete privileges and
no `PUBLIC` function execution. Production migration, role provisioning,
retention/legal approval and independent security review remain open.

### Webhook delivery-identity hardening — 2026-08-15

The required `x-razorpay-event-id` header is now restricted to bounded safe
identifier characters before it can be persisted as the provider delivery
deduplication key or used as trace input. Unsafe/control-character values are
rejected before persistence. The verifier is covered by the payment Go test,
race and vet suites; this remains local evidence and does not replace provider
delivery or deployed webhook testing.

The same invariant is now enforced for new database rows by migration `0046`
with a `NOT VALID` check constraint, preserving historical evidence while
rejecting unsafe new values at the SQL boundary. The disposable PostgreSQL
L02/L03 harness applies the migration successfully; production constraint
validation and provider/deployed evidence remain separate gates.

The audit also corrected the internal recovery evidence key, which previously
used colon separators incompatible with the new SQL format. Recovery now uses
the deterministic `recovery_<order>_<payment>` form, covered by a unit test;
the payment Go test, race and vet suites pass.

### Provider order identity hardening — 2026-08-15

The account-scoped Razorpay order fetch now rejects a provider response whose
order ID differs from the requested path ID before reconciliation evaluates
the provider status. The regression is covered by the Go provider test suite;
`go test ./...`, `go test -race ./...` and `go vet ./...` pass. This is a local
boundary guarantee only and does not replace provider sandbox or deployed
connected-account evidence.

### Scheduler operations contract — 2026-08-15

The scheduler-only repository now includes
`bharatstudio-crons/docs/SCHEDULER_OPERATIONS.md`. It maps all six disabled v1
schedules to their declared outcome/dead-letter signals, freshness/backlog
watch, owner-specific recovery, disable ordering, manual replay evidence and
data-protection rules. It explicitly keeps database credentials and business
mutation authority out of the scheduler and prohibits deleting or silently
acknowledging durable work during recovery.

The scheduler contract test passes 2/2, including coverage of every schedule's
declared monitoring and dead-letter signal. No schedule was enabled and no live
monitoring, IAM or recovery rehearsal is claimed.

### Observability deployment contract — 2026-08-15

The infrastructure repository now includes the disabled
`deployment/v1/observability.template.json`. It declares private metrics scrape
targets for Alerts API, payment and worker services; dashboard domains for
payment receipt, alert dispatch, overlay fan-out, platform health and
Companion/security; and eight owner-assigned alert categories. The contract
forbids user/channel/payment/provider identifiers, raw URLs, tokens and raw
errors as metric labels. Environment-specific thresholds, live routing,
dashboard queries and staging rehearsal remain required before enablement.

The infrastructure contract suite passes 8/8, including the observability
contract test. No monitoring resource was provisioned or enabled.

### Support and external-evidence register — 2026-08-15

Added `active/launch/05_SUPPORT_AND_EXTERNAL_EVIDENCE_REGISTER.md` as the
single working register for safe public support intake, internal P0–P3 triage,
payment/alert escalation, redaction, external provider/tax/privacy/app-store
evidence and public-launch gates. It explicitly states that internal response
targets are rehearsal targets rather than published contractual SLAs and that
legal/provider approval cannot be inferred from local implementation. L08-08 is
locally reviewed; external/support rehearsal remains pending.

### Master release authority reconciliation — 2026-08-15

Added `active/launch/01_MASTER_RELEASE_AUTHORITY.md` to the new requirements
repository. It binds the one-shot v1 launch scope to L00–L10, records the
non-negotiable no-loss/RLS/payment/overlay/scheduler invariants, maps each track
to its current evidence state, and lists external/deployment go/no-go gates.
It deliberately remains `Proposed`; it does not promote local checks to
production readiness or reintroduce YouTube/Enterprise work.

### Post-retention-change regression — 2026-08-15

After migration `0047_v1_l02_soft_archive_only.sql` and its RLS-policy fix,
the current local Alerts surface was rerun end to end. Results: API tests
48/48; API and web production builds pass; contract validation passes 11
fixtures, the template catalogue and 29 OpenAPI paths; disposable PostgreSQL
L02/L03 harness passes; payment-webhook Go `go test -race ./...` and `go vet
./...` pass; alert-worker Go `go test -race ./...` and `go vet ./...` pass;
`bharatstudio-crons` tests pass 2/2; `bharatstudio-infra` tests pass 8/8.

No visual package was generated. The 359 missing template runtime packages
remain deferred under `pending/launch/PENDING-04-TEMPLATE-RUNTIME-PACKAGE-COMPLETION.md`.
No production database, provider account, Cloud Tasks queue, IAM binding,
live scheduler or external release action was used by this regression.

### Subscription billing projection — 2026-08-15

Migration `0048_v1_l04_subscription_billing_projection.sql` was applied in the
same disposable PostgreSQL harness used by `pnpm db:test:l03`. The added
`L04-48` scenario passed: an annual Creator subscription stores the approved
₹399 monthly-equivalent price and ten-months-paid/twelve-months-service shape;
the initial protection window is recorded; `past_due` adds only the bounded
30-day grace period; an equal-timestamp replay is stale; cancellation ends
protection; a later rejoin uses current pricing; and a late predecessor event
cannot hide the newer active subscription from `get_billing_view`.

The migration also rejects a wrong-tier annual price before persistence. The
API `getBilling` mapping, OpenAPI billing projection and fake contract were
updated and the API tests/build/contract validation remain passing.

Active subscription application also publishes an idempotent,
server-owned entitlement version containing the subscription identity,
interval and approved price. The local test confirms the active rejoin is the
current entitlement source; past-due and cancellation transitions do not
silently publish an access rewrite. Provider dunning/access policy and the
deployed reconciliation path remain external launch gates. Version allocation
is serialized per channel and the idempotency read occurs after the lock; the
local test also covers a later active reconciliation without a duplicate
entitlement version.

The authenticated Alerts dashboard now consumes and displays the complete
billing projection: interval, renewal state, auto-renew, annual service terms,
and grandfathered-price/grace metadata. The API suite remains 48/48, the
API/web production build passes, and contract validation remains green. The
current suite count is 50/50; earlier entries in this cumulative review retain
their historical run counts.

The disposable PostgreSQL harness now also opens separate listener and
publisher connections and proves a committed `pg_notify` wakes an overlay
waiter. This validates the local direct-listener mechanism only; notification
is still an optimisation, and direct Neon endpoint, cross-replica staging,
reconnect-under-load and replay-with-notification-disabled evidence remain
open. During this check, the wrapper was corrected so a successful
`postgres.js` `listen()` registration is not mistaken for a disconnect; only
registration rejection enters the retry path.

The same harness now applies migrations `0049` and `0050` and exercises the
subscription link-first boundary through the Go `SQLStore`: a linked activated event
projects one active Creator subscription, a replay of the same provider event
is deduplicated, unknown links and plan mismatches quarantine, incomplete
authenticated events cannot grant access, and the resulting billing state is
server-owned. It also proves the account boundary: a platform-scope link can
project a BharatStudio plan subscription without a creator `payment_accounts`
row, while connected scope still requires an active channel account. The Go
provider suite also covers the server-owned
`POST /v1/subscriptions` adapter, including connected-account routing, bounded
request validation, platform-scope header omission and response plan matching. Provider subscription creation
through an approved live/test plan catalogue, link-registration integration,
dunning reconciliation and staging evidence remain open.

The provider boundary now also has a local `POST /v1/subscriptions` adapter
slice. Its tests verify Basic Auth, the resolved `X-Razorpay-Account`, bounded
server-owned plan/count/quantity/notes fields, pre-network rejection of invalid
requests, omission of the connected-account header for platform scope and
rejection of a provider response for a different plan. Payment
`go test -race ./...` and `go vet ./...` pass after this addition. This remains
synthetic provider-contract evidence; it does not select live plan IDs, create
customer-facing checkout, register a returned subscription link, or prove
Razorpay sandbox/live behavior.

This evidence is local and synthetic. It does not prove Razorpay subscription
plan mapping, provider subscription webhook delivery, recurring charge/dunning
reconciliation, connected-account approval, deployed IAM/secrets, staging or
legal/tax readiness. No production or provider state was used.

### Companion and public-surface rerun — 2026-08-15

The Companion mobile repository passes Jest 16/16, ESLint, TypeScript
typecheck, React Native config resolution and dependency-hardening 2/2. The
macOS SwiftUI package test passes, and the static BharatStudio marketing test
passes 3/3. A watchman recrawl warning appeared during Jest but did not change
the result and is an environment warning, not a product failure.

The same cross-repository rerun also passes alert-worker Go race tests and vet,
the scheduler contract tests 2/2, the infrastructure contract tests 8/8, and
the payment Go race tests and vet after the subscription adapter addition.

These checks do not clear the remaining React Native/Metro/image-size audit
findings, create the unavailable Windows build/signing evidence, prove native
OBS pairing/security, or satisfy device/store/privacy/signing review. They also
do not promote L07 or L10 to Verified.

### Continued local verification — 2026-08-15

The platform-versus-connected subscription correction was re-run after
`0050_v1_l04_platform_subscription_account_boundary.sql` was added. The
disposable PostgreSQL harness passed the platform-scope case: a BharatStudio
plan subscription can be linked and projected for a channel without a creator
tip `payment_accounts` row; the connected-scope path remains account-gated.
The same run passed L02 security remediation, L03 application behaviour and
overlay PostgreSQL wake-up integration. Payment Go `go test -race ./...` and
`go vet ./...` passed.

The Alerts API suite passed 50/50, the API/web production build passed, and
contract validation passed for 11 fixtures, the template catalogue and the
OpenAPI document. Alert-worker Go race tests/vet, scheduler tests 2/2, infra
tests 8/8, Companion mobile tests 16/16 plus lint/typecheck, macOS Swift tests
and marketing tests 3/3 also passed. The mobile command initially received an
invalid Jest passthrough flag and was rerun with the repository's supported
command; the corrected run is the evidence recorded here. The Watchman
recrawl message remains an environment warning.

This remains local evidence. Provider plan catalogue/checkout-link integration,
Razorpay approval and sandbox/live behaviour, Cloud Run/IAM/Cloud Tasks,
cross-replica staging, Windows build/signing, store/privacy review, legal/tax
approval and independent review remain open. No visual BSA packages were
generated in this pass.

### Concurrency and boundary rerun — 2026-08-15

The disposable PostgreSQL L03 harness now includes
`integration/channel-store-concurrency.integration.ts`. Two independent
database clients race queue creation and configuration updates against the
same channel. The run passed with exactly one new queue within the server
allocation and exactly one next configuration version; the second callers
were rejected by the serialized channel-row lock/version check. This is real
multi-connection local evidence, not a mock query-order assertion. Cross-
replica and staging capacity evidence remains open.

After the platform-versus-connected Razorpay account change and the
concurrency change, the payment Go module passed `go test -race ./...` and
`go vet ./...`; the alert-worker Go module passed the same checks. The
infrastructure contract suite passed 8/8 and the scheduler-only repository
passed 2/2. These are local contract/regression results only; no provider,
Cloud Run, Cloud Tasks, IAM, Neon production or staging gate is promoted.

### Paid subscription checkout boundary rerun — 2026-08-15

The paid-plan creation slice is now locally implemented, without using real
Razorpay credentials or provider state. Migration `0051` persists a
server-owned creation intent before provider I/O; the Go subscription service
claims provider creation once, attaches a validated provider identity and
links through the canonical account-scoped registration function. Migration
`0052` allows an exact-hash replay of a previously quarantined early
subscription webhook after the local link is repaired, while retaining the
original evidence row.

The private Go route rejects missing/private authorization, unknown fields,
header/body idempotency mismatches, non-UUID identities, unsupported tiers and
intervals. Its catalog loader accepts only environment-specific Razorpay
account/plan identifiers; prices, count and annual 10-month-charge/12-month-
service terms remain code-owned. The Creator API adds an authenticated
`POST /v1/channels/{channelId}/billing/subscription` route and a private
OIDC client that sends only user/channel/tier/interval/idempotency data.

The annual mapping was checked against the existing billing projection: the
durable intent stores the monthly-equivalent tier price, while the response
also exposes the annual ten-month charge and 12-month service terms. The
annual Razorpay plan ID remains the provider-side charge authority; it is never
accepted from the browser.

Evidence: Go subscription tests pass, Go race/vet pass, API tests pass 52/52,
API build passes, OpenAPI validates with 32 paths, and the disposable
PostgreSQL L03 harness passes including early-webhook quarantine/replay. This
does not prove Razorpay sandbox/live creation, approved plan IDs, provider
approval, deployed OIDC/IAM/secrets, live dunning/reconciliation or staging
recovery. L04 remains implementation-passing rather than launch-verified.

### Paid subscription SQLStore adapter integration — 2026-08-15

Added local integration coverage for the Go payment service's subscription
creation adapter. Against the same disposable PostgreSQL migration chain, the
test performs server-owned intent creation, idempotent replay, provider claim,
synthetic provider attachment, canonical link registration and durable readback
of the linked intent. pnpm db:test:l03 passed, including the L02/L03 SQL
proofs, payment and worker SQL integration tests, overlay wake-up integration
and channel-store concurrency checks. This is local synthetic evidence only;
Razorpay approval, provider sandbox/live behavior, deployment IAM/secrets,
staging recovery and independent review remain open.

### Sequential launch-boundary regression — 2026-08-15

After the payment SQLStore adapter coverage was added, the alert-worker Go
module passed go test ./..., go test -race ./... and go vet ./.... The
scheduler-only repository passed npm test (2/2), and the infrastructure
contract suite passed npm test (8/8). These results confirm that the payment
adapter addition did not disturb worker task contracts, scheduler ownership,
private-route topology, event-ID deduplication or the disabled deployment
boundary. They remain local regression evidence; live Cloud Tasks, IAM,
provider, Neon, staging capacity and public release gates are not promoted.

### Payment reconciliation SQLStore account-attribution integration — 2026-08-15

The suspected reconciliation signature mismatch was checked against the
applied migration chain. Migrations `0034` and `0035` drop and recreate the
payment/refund candidate functions with `connected_account_ref`, matching the
Go `reconcile.SQLStore` scan order. A new disposable PostgreSQL integration
test now reads synthetic payment and refund candidates through the real
`database/sql` adapter and asserts the account/provider identity fields.

Result: PASS locally. Payment Go tests, race/vet and `pnpm db:test:l03` all
pass. This closes the local adapter-contract evidence gap; it does not claim
Razorpay provider, deployed IAM/secret, scheduler or staging evidence.

### Alert-worker SQL ready-pump integration — 2026-08-15

Added integration coverage for the worker's real SQL ready-row adapter and
task pump. The disposable PostgreSQL run lists a synthetic durable delivery,
emits the exact stable task identity, injects an enqueue failure and confirms
the delivery remains visible for retry. Worker unit tests, race tests and vet
remain green, and pnpm db:test:l03 passes across the L02/L03 SQL proof, payment
and worker integration, overlay wake-up and channel concurrency checks. Live
Cloud Tasks, dead-letter, OIDC/IAM, capacity and staging evidence remain open.

### Go runtime-fixture compatibility — 2026-08-15

Added `services/alert-worker-go/internal/contracts/fixture_compatibility_test.go`.
The Go worker now strictly consumes the committed multi-queue, per-queue
delivery, overlay SSE and payment webhook fixtures in addition to the existing
Cloud Tasks command fixture. The checks reject unknown fields and verify
schema identity, UUID/date-time fields, parent source identity, independent
queue status/priority and immutable override presence. Focused tests, race
tests and `go vet` pass locally. This closes the Go-consumer compatibility
slice only; React Native, C# and Swift consumer evidence, cross-language
code-generation review and independent review remain open.

### Marketing navigation integrity and cross-repository regression — 2026-08-15

The marketing static-site test now verifies that every root-relative link in
the BharatStudio home, Alerts, Companion, pricing, support and legal pages
resolves to a checked-in public file. The local marketing suite passes 4/4;
this protects the publication surface from broken product navigation but does
not prove Cloudflare deployment, DNS, certificates, search ranking,
accessibility audit, analytics consent or final copy/legal approval.

The subsequent local regression pass also completed:

- Alerts contracts: 11 fixtures plus the template catalogue and OpenAPI 3.1
  with 32 paths.
- Alerts API: 52/52 tests; API and web production builds pass.
- Disposable PostgreSQL L02/L03 harness: security remediations and application
  behavior pass, including payment, worker, overlay-wakeup, and channel
  concurrency integration.
- Go alert worker: unit tests, race tests and vet pass.
- Infrastructure contract: 8/8 tests pass; deployment remains explicitly
  `not-deployable` until provider, IAM, capacity, staging and rollback evidence
  exists.
- Scheduler contract: 2/2 tests pass while schedules remain disabled.
- Companion mobile: 16/16 Jest tests pass; dependency hardening tests pass 2/2.

These are local/regression results only. They do not close Razorpay approval or
provider behavior, deployed Cloud Run/Cloud Tasks/IAM/Secret Manager, Neon
region/plan/capacity, cross-replica SSE, OBS/browser staging, native desktop
and app-store gates, legal/CA/privacy/support sign-off, visual package
completion, or independent review.

### Private worker method-boundary regression — 2026-08-15

The Cloud Tasks delivery handler and ready-delivery pump now have explicit
tests proving that non-POST requests return `405` with `Allow: POST` before
authorization, lease claim or enqueue work. `go test ./...`, `go test -race
./...` and `go vet ./...` pass. This closes only the local HTTP method guard;
deployed private-ingress and IAM evidence remains open.

### L02 security and archive rerun — 2026-08-15

The disposable PostgreSQL 16 harness was rerun after the launch-authority
reconciliation. It returned `L02_SECURITY_REMEDIATIONS=PASS` and
`L03_APPLICATION_BEHAVIOR=PASS`. The run again covered transaction-scoped RLS
context reuse, soft archive/restore and append-only grants, concurrent
webhook deduplication, independent multi-queue delivery, overlay wake-up and
Companion session boundaries. This is isolated local evidence only; it does
not replace independent security review, production role provisioning or
deployed database proof.

### Post-headers SSE replay-failure hardening — 2026-08-15

The continuous overlay SSE route previously had no explicit handling for a
durable replay failure after response headers had been committed. It now logs
only the bounded safe error category, emits a comment-only
`replay-unavailable` marker and closes the stream cleanly. The browser can then
reconnect with its last acknowledged cursor; no delivery is acknowledged or
discarded by this path. A regression test exercises an initial event followed
by a replay failure. The Alerts API suite passes 53/53 and the API/web build
passes. This is local failure-boundary evidence only; deployed database
fault-injection, cross-replica and OBS staging evidence remains open.

### Two-listener PostgreSQL wake-up proof — 2026-08-15

The disposable PostgreSQL integration was strengthened from one listener to two
independent direct listener connections plus a separate publisher. One committed
`pg_notify` now has to wake both waiters before the test passes, while each
listener must remain healthy after `postgres.js` registration. This is evidence
that PostgreSQL broadcast wake-up works for two local listener instances; it is
still only a notification optimisation check. It does not prove Neon direct
endpoint behaviour, deployed cross-replica SSE delivery, durable replay,
acknowledgement, or OBS staging.
### Paid subscription identity-boundary regression — 2026-08-15

The private payment service receives an authenticated service-to-service request,
but that identity alone is not treated as permission to choose an arbitrary
`userId`/`channelId`. Migration `0051_v1_l04_subscription_creation_intents.sql`
checks that the supplied user is an active `owner` or `admin` member of the
supplied channel before an intent is persisted. The disposable L03 harness now
proves both negative directions: a non-member user cannot create an intent for
another channel, and an owner cannot use their identity with another channel.
Both fail with SQLSTATE `42501`; no intent row is created. This is local
database evidence only and does not replace deployed OIDC/IAM or provider
staging evidence.

### L05 fresh acceptance audit — 2026-08-15

The worker module passed `go test ./...`, `go test -race ./...` and `go vet
./...`. The shared contract validator passed 11 fixture mappings and 32
OpenAPI paths. `pnpm db:test:l03` passed the L02/L03 database behavior suite,
payment/worker SQL integration and the two-listener PostgreSQL wake-up proof.
No BSA visual package was generated. Live Cloud Tasks, deployed OIDC/IAM,
cross-replica overlay/OBS, capacity, retry/dead-letter rehearsal and staging
evidence remain open.

### Companion stale-channel-state hardening — 2026-08-15

The mobile Companion shell now accepts state only when its channel is in the
authenticated channel list and filters queue candidates to that channel before
rendering or invoking an action. A regression test proves an active queue and
pending count from another channel are neither shown nor targeted. Mobile Jest
now passes 17/17; lint, TypeScript and dependency-hardening checks pass. Native
device, signing/store and dependency-audit resolution remain open.

### L08/L09 local gate audit — 2026-08-15

The static marketing/support/legal surface and observability contracts were
audited against their current acceptance records. Marketing `npm test` passes
4/4, the API suite remains 53/53, and the infrastructure contract remains
8/8. No locally fixable public-secret, Phase-2 exposure, broken internal-link,
or metrics-redaction gap was found in this pass. L08/L09 remain open for dated
legal/provider/tax/support evidence, public hosting/SEO/accessibility scans,
deployed dashboards and alert routing, declared capacity targets, and
staging fault/restore/rollback rehearsal.

### Shared-PostgreSQL overlay security and replica proof — 2026-08-15

The new two-client/two-Fastify-instance integration initially exposed a real
replay isolation defect: `get_overlay_events` checked a valid overlay session
but lacked an explicit `event.channel_id = session.channel_id` predicate. A
valid session could therefore enumerate another channel's delivery rows. This
was corrected in migration `0054_v1_l03_overlay_event_channel_guard.sql`.

After the correction, the isolated harness passed L02 security remediation,
L03 application behavior, payment and worker SQL integration, the two-listener
PostgreSQL wake-up integration, the shared-PostgreSQL cross-replica API
integration, and both database concurrency tests. Replica B received a delivery
committed to the shared database, acknowledged it, and replica A observed the
durable replay state. This does not prove Neon direct endpoint behavior, Cloud
Run routing, network partitions, capacity, OBS behavior or production
readiness; those remain external/staging gates. No BSA visual package was
generated.

### Consolidated local regression after mobile transport hardening — 2026-08-15

The current local regression completed successfully after the Companion API
transport-boundary change: Alerts API 53/53, API/web production build,
contract validation (11 fixtures plus the template catalogue and 32 OpenAPI
paths), disposable PostgreSQL L02/L03 harness, payment and worker Go tests
with `go vet` and `go test -race`, scheduler contract 2/2, infrastructure
contract 8/8, marketing tests 4/4, mobile tests 19/19 with lint/typecheck,
dependency-hardening 2/2 and React Native config, and macOS `swift test`.
This is a fresh local/synthetic snapshot only. Razorpay/provider approval,
Neon/Cloud Run/Cloud Tasks/IAM deployment, authenticated OBS and native-device
testing, legal/support/store review, capacity/failure rehearsal, independent
review and the deferred 359 BSA runtime packages remain open. No new visual
package was generated.

### Overlay wake-up waiter lifecycle — 2026-08-15

The overlay wake-up adapter now cancels a waiter timeout as soon as a valid
notification or service shutdown resolves the waiter. This removes avoidable
timer accumulation during concurrent overlay activity while preserving the
durable replay path and all acknowledgement semantics. The API test suite
passes 53/53 and the API/web build passes. This is local resource-lifecycle
hardening only; Neon, Cloud Run, cross-replica, fault-injection and OBS
staging evidence remain open.

### Payment bootstrap fail-closed hardening — 2026-08-15

The payment service previously panicked with a stack trace when required
configuration was absent. `cmd/payment-webhook/main.go` now returns bounded
startup errors for missing required values and invalid positive-integer
settings, with command-level tests covering both paths. The rebuilt static
distroless image runs as `nonroot:nonroot`; an empty-environment container
smoke exits with only the bounded missing-environment message. Go tests,
race tests, vet and the Docker build pass. This does not prove Cloud Run,
IAM, Secret Manager, Razorpay or staging readiness.

### Overlay wake-up waiter lifecycle — 2026-08-15

The overlay wake-up adapter now cancels a waiter timeout as soon as a valid
notification or service shutdown resolves the waiter. This removes avoidable
timer accumulation during concurrent overlay activity while preserving the
durable replay path and all acknowledgement semantics. The API test suite
passes 53/53 and the API/web build passes. This is local resource-lifecycle
hardening only; Neon, Cloud Run, cross-replica, fault-injection and OBS
staging evidence remain open.

### macOS Companion policy boundary — 2026-08-15

The native macOS slice was advanced without inventing a pairing or OBS
protocol. `CompanionPolicy.swift` now fails closed for expired/revoked leases,
wrong sessions/channels, unbounded command windows and missing user
confirmation; it accepts only the finite v1 Companion action set and redacts
credential-like values from future support logs. The Swift 6 executable entry
point was renamed from `main.swift` to `CompanionApp.swift` to remove the
`@main` conflict. `swift test` passes 5/5. Pairing, Keychain, signed command
transport, OBS WebSocket authentication, Windows implementation, device and
distribution evidence remain release gates. No payment, queue, delivery or
visual alert package was changed.

### Go service container reproducibility — 2026-08-15

The payment and alert-worker Dockerfiles now pin both the Go build image and
distroless runtime image to the exact digests resolved by the verified local
build. Both images rebuilt successfully as non-root containers. The payment
container also exits with a bounded missing-environment error when started
without configuration. This improves artifact and startup safety but does not
establish Cloud Run, IAM, Secret Manager, Cloud Tasks, provider or staging
readiness.

### SSE disconnect waiter cancellation — 2026-08-15

The overlay SSE route now aborts its wake-up wait and polling fallback when the
raw request closes. The PostgreSQL wake-up adapter removes the parked waiter,
clears its timeout and removes its abort listener immediately; the fallback
waiter has the same cleanup behavior. The 54/54 API test suite and API/web
production build pass. This closes a local resource-lifecycle defect only; it
does not establish deployed Cloud Run connection churn, Neon direct-listener
behavior, network fault injection, browser/OBS behavior or staging capacity.

### Full local v1 regression after SSE and mobile verification — 2026-08-15

Fresh checks completed after the disconnect-cancellation and mobile tooling
changes:

- Alerts API: 54/54 tests; API TypeScript build and web production build pass.
- Disposable PostgreSQL L02/L03/L04/L05 harness: security and application
  behavior pass; two-listener wake-up, shared-PostgreSQL cross-replica replay,
  and both queue/configuration concurrency checks pass.
- Payment Go service: unit tests, race tests and `go vet` pass.
- Alert Worker Go service: unit tests, race tests and `go vet` pass.
- Contract validation: 11 fixtures plus the template catalogue and OpenAPI
  3.1 document with 32 paths pass.
- Marketing: 4/4 static-site tests pass; infra: 8/8 contract tests pass;
  scheduler: 2/2 contract tests pass.
- Mobile: 19/19 tests, ESLint, the explicit `npm run typecheck`, dependency
  hardening 2/2 and React Native iOS/Android config checks pass.
- macOS Companion policy: 5/5 Swift tests pass.

These results are local/synthetic evidence only. Razorpay approval and
provider sandbox/live behavior, deployed Neon/Cloud Run/Cloud Tasks/IAM,
authenticated browser/OBS and native-device testing, Windows build/signing,
legal/support/store review, capacity/failure/restore rehearsal, independent
review and the deferred 359 BSA runtime packages remain open. No new BSA
visual package was generated.

### Payment-to-worker pump timeout — 2026-08-15

The payment webhook's private worker-pump client now applies an independent
5-second deadline. A stalled worker call fails retryably before the outer
payment HTTP timeout, while the verified provider event has already been
persisted and remains recoverable through provider redelivery/reconciliation.
Focused ingress tests prove the bounded call and non-positive timeout
configuration is rejected. This is local network-boundary evidence only;
deployed worker latency, IAM, Cloud Run timeout configuration and Razorpay
retry behavior remain open.

The timeout regression was rerun with a 50 ms client deadline against a
500 ms stalled test server, followed by payment `go test ./...`,
`go test -race ./...` and `go vet ./...`; all passed. The test server is
closed cleanly after the stalled handler exits, so the evidence does not
depend on an orphaned test connection.

### Unacknowledged replay guard after out-of-order publication — 2026-08-15

The durable overlay replay projection previously applied the supplied cursor
as a hard lower bound even for rows that were still unacknowledged. With
concurrent task enqueue/worker completion, that could hide an older durable
delivery after a newer delivery had been acknowledged. Migration `0055` now
returns all eligible unacknowledged deliveries in stable creation order; the
cursor remains an acknowledgement identity/checkpoint, while acknowledged
rows are excluded by status. The disposable PostgreSQL harness includes the
older-unacknowledged/newer-cursor case and passes. Deployed cross-replica,
browser and OBS evidence remains open.

### Final local product-surface rerun — 2026-08-15

- Marketing site: 4/4 tests passed.
- Fresh follow-up on 2026-08-15: marketing site static checks pass 5/5 after adding Cloudflare-compatible security headers and a dated `security.txt` contact; prior 4/4 counts are retained as historical run evidence.

### L03 overlay accessibility markup correction — 2026-08-15

The browser-source overlay connection indicator was rechecked and corrected:
its connected/reconnecting label now uses an explicit `role="status"` and
polite live region rather than an `aria-label` on a generic element. The
focused overlay/TTS tests pass 11/11, the Alerts API suite passes 54/54 and the
production Web build passes. This improves the local accessibility boundary;
authenticated browser/assistive-technology/OBS staging evidence remains open.
- Scheduler-only repository: 2/2 tests passed; all v1 schedules remain
  disabled.
- Infrastructure contracts: 8/8 tests passed.
- Companion mobile: 19/19 tests, lint, TypeScript typecheck and 2/2
  dependency-hardening tests passed.
- macOS Companion policy package: 5/5 Swift tests passed.

These checks are local evidence only. Windows build/signing, iOS/Android
device and store review, deployed services/IAM/secrets, provider approval and
sandbox/live behavior, capacity/fault/restore rehearsal, legal/support
approval, independent review and the deferred visual runtime packages remain
open. No new BSA visual package was generated.

### Bounded Cloud Tasks pump concurrency — 2026-08-15

The alert-worker ready-row pump no longer performs provider task creation
serially. It validates the full candidate batch before enqueueing, then uses a
bounded worker pool (default 8, explicitly configurable) while retaining the
stable delivery/version/attempt task name. A delayed fake enqueuer proved the
configured concurrency bound and that all 24 candidates produce commands;
the existing 1,000-row partial-failure test still proves failed candidates
remain recoverable and no durable row is acknowledged by the pump. Worker
unit tests, race tests and vet pass. This is local evidence only; deployed
Cloud Tasks quota, throughput, retry/DLQ and staging capacity remain open.

### Post-0055 full boundary rerun — 2026-08-15

The current worktree was rerun after the unacknowledged replay guard was
integrated. `pnpm test` passed 54/54, `pnpm build` passed the API and web
production builds, and `pnpm contracts:validate` passed all 11 fixture/schema
mappings plus OpenAPI 3.1 with 32 paths. `pnpm db:test:l03` passed both the L02
security remediation output and L03 application behavior, including the
newer-acknowledged/older-unacknowledged replay regression. Both Go services
passed `go test ./...`, `go test -race ./...` and `go vet ./...`. These are
local/synthetic results; no provider, deployed, browser/OBS or staging claim is
made by this rerun.

### Companion mobile runtime contract validation — 2026-08-15

The React Native Companion API client now validates v1 response envelopes at
runtime rather than casting untrusted JSON. The local suite covers valid state,
queue, layout, action-result and control-session shapes plus malformed counts,
dates and unsupported actions. Jest passes 21/21, ESLint passes and the
TypeScript check passes. This closes the local React Native response-boundary
slice only; device/offline/reconnect, Windows/C#, signing/store, deployed API
and independent review evidence remain open. No BSA visual package was
generated or modified.

### Web Companion runtime contract validation — 2026-08-15

The Web Companion client previously cast several authenticated JSON responses
directly to TypeScript types. `apps/web/app/lib/api.ts` now validates the v1
current-user, queue-list, Companion-state, Companion-layout and action-result
envelopes before returning them to the UI. Validation covers UUIDs, ISO dates,
non-negative counters, finite tier/action values, bounded page/slot values and
duplicate slot indexes. The Web TypeScript check and production build passed.
This is local client evidence only; it does not close authenticated browser,
deployed, cross-replica or native-device evidence. No BSA visual package was
generated or modified.

### Full cross-repository regression rerun — 2026-08-15

The current workspace was rerun after the Web Companion boundary hardening:

- Alerts database harness: `L02_SECURITY_REMEDIATIONS=PASS`,
  `L03_APPLICATION_BEHAVIOR=PASS`, including two-listener wake-up and shared
  PostgreSQL cross-replica replay.
- Alerts API: 54/54 tests passed; Web production build passed.
- Contract validator: 11 fixture/schema mappings and OpenAPI 3.1 with 32 paths
  passed.
- Payment and alert-worker Go services: `go test -race ./...` and `go vet ./...`
  passed.
- Companion mobile: Jest 21/21, lint and TypeScript passed.
- Companion macOS: Swift 7/7 passed.
- Infrastructure: 8/8 contract tests passed.
- Scheduler-only crons: 2/2 contract tests passed; all v1 schedules remain
  disabled.
- Marketing: 4/4 site tests passed.

These results are local/synthetic evidence only. They do not establish Razorpay
approval or sandbox/live behavior, deployed Neon/Cloud Run/Cloud Tasks/IAM,
cross-replica OBS/browser capacity, device/store signing, legal/support
approval, independent review, or the deferred 359 BSA visual runtime packages.
No BSA visual package was generated or modified.

### Web Companion screen-set implementation — 2026-08-15

The Web Companion page was extended using existing REST contracts only. It now
loads and renders recent alert history, server freshness and overlay state,
plan/slot entitlements, active account sessions with server-side revoke, and
bounded recovery guidance. The client validates the session projection and
uses explicit unavailable states when notification preferences are not part of
the approved v1 API. `apps/web` TypeScript and production build pass. This
closes the local screen-set implementation slice, not browser accessibility,
cross-replica, deployed, provider or independent-review evidence. No BSA visual
package was generated or modified.

### Public donor checkout response hardening — 2026-08-15

- **Reviewer:** Codex self-review; independent fresh reviewer not available in
  this run.
- **Finding:** the donor checkout parser accepted an incomplete order response,
  substituted the requested amount when the server omitted it, allowed unknown
  fields, and represented internal provider lifecycle states as donor-visible
  status values. This was weaker than the OpenAPI `CreateTipOrderResponse` and
  `PublicTipOrderStatus` contracts.
- **Disposition:** the parser now requires the complete v1 envelope, Razorpay
  provider, exact requested INR amount, bounded provider-order identity and
  strict donor-safe status values. Unknown fields, internal provider states and
  incomplete/mismatched responses fail closed before checkout or payment-success
  UI state.
- **Evidence:** focused Web/API contract suite remains 19/19 and Web
  TypeScript validation passes. No BSA visual package was generated or
  modified.
- **Residual gate:** provider sandbox/live, browser/OBS, deployed and staging
  evidence remain open; this local parser fix does not establish financial
  success or provider approval.

### Overlay SSE event-envelope hardening — 2026-08-15

The browser overlay now validates each decoded SSE event before adding it to
the presentation queue. Wrong schema versions, invalid UUIDs/dates/traces,
unsupported event types and non-object payloads are ignored without cursor
acknowledgement, preserving durable replay. The focused overlay/TTS suite
passes 11/11 and the Web TypeScript check and production build pass. This is
local client evidence only; deployed/browser/OBS and cross-replica failure
evidence remain open. No BSA visual package was generated or modified.

### L07/L08 continuation gate — 2026-08-15

The next local surface pass passed React Native Jest 23/23, lint, TypeScript
typecheck, dependency-hardening 2/2, React Native config, macOS Swift 7/7 and
marketing/static-site 5/5. These are local checks only. Windows build/signing,
native pairing/OBS, device/store, dependency-advisory disposition,
legal/provider/support, domain/analytics/SEO/accessibility and independent
review remain open. No BSA visual package was generated or modified.

### Public tip response-boundary hardening — 2026-08-15

The public tip form now validates server order/status envelopes before using a
provider order ID, amount or payment state. Invalid local IDs, provider IDs,
amounts, currencies, timestamps and lifecycle values fail closed; the browser
cannot declare payment success from an untrusted or malformed response. The
focused tip-contract suite passes 3/3 and the Web TypeScript check/build pass.
This remains local browser-boundary evidence only; provider sandbox/live and
staging checkout evidence remain open. No BSA visual package was generated or
modified.

### Alerts provider/runtime continuation — 2026-08-15

Payment webhook and alert-worker Go tests, vet and focused race tests passed.
The payment-webhook and alert-worker production-shaped Docker images also
built from their service-local contexts as pinned, static, non-root
distroless images. The Razorpay boundary continues to require raw-body
HMAC-SHA256 plus the provider `x-razorpay-event-id` deduplication identity.
No live provider credentials, Razorpay TP/connected-account approval, Cloud
Run IAM/secrets, sandbox checkout/webhook, refund or production evidence was
available; those gates remain open. No BSA visual package was generated or
modified.

### Desktop OBS boundary and Windows validation slice — 2026-08-15

The macOS helper now has a loopback-only OBS WebSocket v5 client boundary;
endpoint and challenge-response tests pass as part of `swift test` 12/12. The
Windows source boundary mirrors the same restrictions and the project,
manifest and app manifest parse as XML. This host has no `dotnet`, MSBuild or
Windows SDK, so Windows compile/MSIX/signing and real OBS/device evidence are
not claimed. Pairing transport remains blocked on the approved server pairing
contract and was not invented. No BSA visual package was generated or modified.

### Native push and server notification contract slice — 2026-08-15

Verified locally that the mobile notification adapter uses explicit modular
Firebase Messaging registration and never exposes raw tokens or sensitive
notification fields to the application policy layer. Verified locally that
the Alerts API preference/device routes are authenticated, reject unknown
fields, encrypt token material before the store boundary, return only safe
device metadata, and support soft revocation. Alerts API tests passed 60/60
and built successfully; mobile tests passed 52/52 with lint and TypeScript.

Not verified: physical iOS APNs permission and background delivery, Android
FCM delivery, provider credentials/key rotation, app-store configuration,
background task scheduling, or production dispatch. No push provider claim is
made from this local evidence. No BSA visual package was generated or modified.

### Notification dispatch policy and database behavior — 2026-08-15

The Alerts API now has a provider-neutral policy boundary for the four
approved operational notification kinds. It maps each kind to the server-side
preference, excludes disabled devices, normalizes the opaque v1 envelope and
rejects invalid IDs/timestamps. The envelope contains no donor, tip, payment,
payout, message or arbitrary payload fields. This is a policy boundary, not
live APNs/FCM delivery; provider adapters must consume it rather than build
their own payloads.

The disposable PostgreSQL chain also passed the new L07 notification SQL
behavior test: default and updated preferences, token-fingerprint idempotent
refresh, soft revocation and revoked-device list exclusion. The combined API
suite passed 62/62 and the API TypeScript build passed. Provider credentials,
delivery outbox/retry semantics, physical-device delivery, key rotation and
staging evidence remain open.

### Current disposable database-chain rerun — 2026-08-15

`pnpm db:test:l03` passed in the current worktree. The run applied the role
prerequisite and complete migration chain in an isolated PostgreSQL 16
container, then reported `L02_SECURITY_REMEDIATIONS=PASS` and
`L03_APPLICATION_BEHAVIOR=PASS`. It also passed the real Go SQLStore payment
and reconciliation integrations, worker lease integration, two-listener
overlay wake-up, shared-PostgreSQL cross-replica replay and channel-store
concurrency checks.

This is disposable local evidence only. It does not prove the Neon direct
endpoint, Cloud Run/Cloud Tasks IAM, provider sandbox/live behavior, browser/OBS
staging, capacity/failure rehearsal or independent review. No BSA visual
package was generated or modified.

### Current infrastructure and scheduler contract rerun — 2026-08-15

The scheduler-only repository passed its 2/2 contract tests with every v1
schedule still disabled. The infrastructure repository passed its 8/8
deployment/observability contract tests, including private worker ingress,
OIDC metadata, pooled-listener prohibition, secret-boundary checks and disabled
Cloud Tasks/scheduler placeholders. These are contract checks only; no live
Cloud Scheduler, Cloud Tasks, IAM binding or production deployment was
performed. No BSA visual package was generated or modified.

### Web response-boundary hardening — 2026-08-15

- **Reviewer:** Codex self-review; independent fresh reviewer not available in
  this run.
- **Scope:** authenticated channel/overlay-session client decoding and the
  public tip page's server projection boundary.
- **Finding:** TypeScript casts alone allowed malformed channel/session
  responses to reach UI code, and the public page accepted an unbounded numeric
  minimum. A malformed overlay response could also carry a query credential or
  unexpected URL path.
- **Disposition:** Implemented strict v1 parsers in
  `apps/web/app/lib/api.ts` and
  `apps/web/app/lib/public-channel-contract.ts`; decoder errors are converted
  to a bounded user-safe message; invalid public projections fail closed.
- **Evidence:** focused response-contract tests pass 3/3, the combined web
  overlay/tip/dashboard contract suite passes 17/17, the API suite passes 54/54, and the
  Web TypeScript check/production build pass.
- **Residual gate:** This is local evidence only. Authenticated browser/OBS,
  provider, deployed and staging evidence remain open. No BSA visual package
  was generated or modified.

### Authenticated dashboard response-boundary expansion — 2026-08-15

- **Reviewer:** Codex self-review; independent fresh reviewer not available in
  this run.
- **Scope:** configuration, queue, binding, history, moderation, billing,
  entitlement and test-alert response handling in the Web dashboard client.
- **Finding:** several API functions still returned TypeScript casts directly,
  allowing malformed values to enter dashboard state despite the server-owned
  contract.
- **Disposition:** Added bounded parsers and wired every affected `apiFetch`
  call to a parser. Validation covers UUIDs, dates, enums, ranges, plan/price
  fields, source overrides and optional history values; invalid responses fail
  closed with a generic message.
- **Evidence:** focused Web contract suite passes 17/17 and Web TypeScript
  validation passes. This remains local client evidence; authenticated browser,
  deployed and staging evidence remain open. No BSA visual package was generated
  or modified.

### Post-dashboard-parser regression rerun — 2026-08-15

After the authenticated dashboard parser expansion, the current worktree was
rerun without generating or modifying any BSA visual package:

- Web/API focused contract suite: 17/17 passed.
- Alerts API suite: 54/54 passed.
- Web production build: passed, including TypeScript validation and all seven
  generated routes.
- Contract validation: 11 fixture/schema mappings and OpenAPI 3.1 with 32
  paths passed.
- Disposable PostgreSQL harness: `L02_SECURITY_REMEDIATIONS=PASS` and
  `L03_APPLICATION_BEHAVIOR=PASS`; the two-listener wake-up and shared
  PostgreSQL cross-replica replay integration also passed.
- Payment webhook Go service: `go test ./...`, `go test -race ./...` and
  `go vet ./...` passed.
- Alert worker Go service: `go test ./...`, `go test -race ./...` and
  `go vet ./...` passed.

This closes the latest local Web response-boundary slice and confirms that it
did not regress the local L03/L04/L05 contracts. It does not establish live
Razorpay/provider behavior, deployed Neon/Cloud Run/Cloud Tasks/IAM,
cross-replica OBS/browser capacity, staging fault/recovery rehearsal,
device/store/legal/support approval, independent review, or the deferred 359
BSA visual runtime packages.

### Companion layout mutation response hardening — 2026-08-15

- **Reviewer:** Codex self-review; independent fresh reviewer not available in
  this run.
- **Finding:** `updateCompanionLayout` used the Web API client's unchecked
  identity decoder even though `getCompanionLayout` validated the same response
  shape. The generic decoder fallback also allowed future authenticated calls to
  bypass runtime validation accidentally.
- **Disposition:** Wired the mutation response through `parseCompanionLayout`,
  removed the generic `apiFetch` decoder default, and made the expected 204
  overlay-revocation path reject unexpected response bodies.
- **Evidence:** Companion layout contract tests pass, Web TypeScript validation
  passes, and the Web production build passes. No BSA visual package was
  generated or modified.
- **Residual gate:** This is local client evidence only. Authenticated browser,
  deployed, staging and independent-review evidence remain open.

### Companion action response hardening — 2026-08-15

- **Reviewer:** Codex self-review; independent fresh reviewer not available in
  this run.
- **Finding:** The Web Companion action client reduced the server result to an
  arbitrary status string and did not validate the required command ID,
  accepted timestamp, schema version or optional event ID.
- **Disposition:** Added a strict `CompanionActionResult` parser, retained the
  command/event identity in the client type, and rejected unknown fields and
  malformed values before UI use.
- **Evidence:** Focused Web contract tests pass 5/5 and Web TypeScript/
  production build pass. No BSA visual package was generated or modified.
- **Residual gate:** This is local client evidence only. Authenticated browser,
  deployed, staging and independent-review evidence remain open.

### Post-Companion-action full regression — 2026-08-15

The current worktree was rerun after the full Companion action-result parser
was added:

- Web/API focused contract suite: 17/17 passed.
- Alerts API suite: 54/54 passed.
- Alerts API TypeScript and Web production builds: passed.
- Contract validation: 11 fixture/schema mappings and OpenAPI 3.1 with 32
  paths passed.
- Disposable PostgreSQL harness: `L02_SECURITY_REMEDIATIONS=PASS` and
  `L03_APPLICATION_BEHAVIOR=PASS`, including two-listener wake-up,
  cross-replica replay, per-queue progress and Companion assertions.

Payment webhook and alert-worker Go services had already passed the current
worktree's normal, race and vet suites during the same regression sequence;
the Web-only change cannot alter those packages. This remains local evidence,
not provider, deployment, browser/OBS, capacity, fault-recovery,
device/store, legal/support or independent-review evidence. The deferred 359
BSA visual runtime packages remain pending, and no BSA visual package was
generated or modified.

### Internal payment-service response hardening — 2026-08-15

- **Reviewer:** Codex self-review; independent fresh reviewer not available in
  this run.
- **Finding:** Creator API private payment and subscription clients validated
  only broad response fields. A malformed internal order ID, pricing number,
  checkout URL or unknown field could pass the boundary.
- **Disposition:** Added strict order/subscription response validation for
  UUID/provider identities, exact amount and currency, approved status/tier,
  positive integer pricing, annual ten-month relationship, HTTPS checkout URLs
  and unknown-field rejection.
- **Evidence:** Alerts API tests pass 54/54, including malformed internal
  response cases, and the API TypeScript build passes.
- **Residual gate:** This is local boundary evidence only. Deployed
  OIDC/IAM, provider sandbox/live behavior, staging recovery and independent
  review remain open.

### Post-payment-boundary full regression — 2026-08-15

After the private payment/subscription response validators were tightened, the
current worktree passed:

- Alerts API tests: 54/54.
- Alerts API and Web production build: passed.
- Web/API focused contract suite: 17/17.
- Contract validation: 11 fixture/schema mappings and OpenAPI 3.1 with 32
  paths.
- Disposable PostgreSQL harness: `L02_SECURITY_REMEDIATIONS=PASS` and
  `L03_APPLICATION_BEHAVIOR=PASS`.
- Payment webhook and alert-worker Go modules: `go test ./...`,
  `go test -race ./...` and `go vet ./...` passed.

These are local/synthetic results. Razorpay approval and sandbox/live behavior,
deployed OIDC/IAM/secrets, Cloud Run/Cloud Tasks, staging recovery/capacity,
browser/OBS, legal/support and independent-review evidence remain open. No BSA
visual package was generated or modified.

### Post-layout-mutation full regression — 2026-08-15

The current worktree was rerun after the Companion layout mutation boundary
was tightened:

- Web/API focused contract suite: 17/17 passed.
- Alerts API suite: 54/54 passed.
- Alerts API TypeScript and Web production builds: passed.
- Contract validation: 11 fixture/schema mappings and OpenAPI 3.1 with 32
  paths passed.
- Disposable PostgreSQL harness: `L02_SECURITY_REMEDIATIONS=PASS` and
  `L03_APPLICATION_BEHAVIOR=PASS`, including two-listener wake-up,
  cross-replica replay, per-queue progress and Companion layout/session
  assertions.
- Payment webhook and alert-worker Go services: `go test ./...`,
  `go test -race ./...` and `go vet ./...` passed for both services.

The local L03/L04/L05 implementation boundary remains green. This is not
provider, deployment, browser/OBS, capacity, fault-recovery, device/store,
legal/support or independent-review evidence, and the deferred 359 BSA visual
runtime packages remain pending. No BSA visual package was generated or
modified.

### Strict authenticated Web projection completion — 2026-08-15

- **Reviewer:** Codex self-review; independent fresh reviewer not available in
  this run.
- **Scope:** remaining authenticated Web response parsers, including identity,
  channel, queue, binding, Companion state/layout, history, billing and
  entitlement envelopes.
- **Finding:** several parsers validated individual values but still accepted
  unknown top-level or nested fields; the entitlement parser also omitted the
  server-authored `source` field from its returned client type. This weakened
  the `additionalProperties: false` API contract and could allow future
  server-only data to enter UI state unnoticed.
- **Disposition:** added strict top-level and nested allow-lists, UUID and role
  validation, safe avatar URL handling, bounded Companion labels, strict
  binding/history envelopes, and preserved the entitlement source field. The
  client now returns normalized objects rather than forwarding unchecked
  response records for these paths.
- **Evidence:** focused Web/API contract suite passes 19/19; Web TypeScript
  validation passes. The full API, build, contract, database and Go regression
  sequence is recorded below.
- **Residual gate:** this is local client evidence only. Authenticated browser,
  provider, deployed/staging, capacity/fault-recovery, device/store,
  legal/support and independent-review evidence remain open. No BSA visual
  package was generated or modified.

### Post-strict-projection full regression — 2026-08-15

After the authenticated Web projection allow-lists and normalized return types
were added, the current worktree passed:

- Web/API focused contract suite: 19/19.
- Alerts API tests: 54/54.
- Alerts API TypeScript build and Web production build: passed; all seven Web
  routes generated.
- Contract validation: 11 fixture/schema mappings plus the v1 template
  catalogue contract; OpenAPI 3.1 with 32 paths and all local references.
- Disposable PostgreSQL application harness: `L02_SECURITY_REMEDIATIONS=PASS`
  and `L03_APPLICATION_BEHAVIOR=PASS`, including the two-listener wake-up,
  cross-replica replay, per-queue delivery and Companion assertions.
- Payment webhook Go service: `go test ./...`, `go test -race ./...` and
  `go vet ./...` passed.
- Alert worker Go service: `go test ./...`, `go test -race ./...` and
  `go vet ./...` passed.

This is local/synthetic evidence only. It does not close provider approval or
sandbox/live behavior, deployed Neon/Cloud Run/Cloud Tasks/IAM/secrets,
authenticated browser/OBS, cross-replica capacity, staging fault/recovery,
device/store, legal/support or independent-review gates. The deferred 359 BSA
visual runtime packages remain pending, and no BSA visual package was
generated or modified.

### Cross-repository regression after strict Web projection hardening — 2026-08-15

The latest Web client boundary change was also checked against the adjacent
product repositories:

- `bharatstudio-crons`: scheduler contract tests 2/2 passed; all v1 schedules
  remain disabled and scheduler-only.
- `bharatstudio-companion-mobile`: Jest 21/21, ESLint, TypeScript typecheck,
  and dependency-hardening checks 2/2 passed. Watchman emitted an environment
  recrawl warning, but the test run completed successfully.
- `bharatstudio-marketing`: static-site tests 4/4 passed.
- `bharatstudio-companion-desktop/macos`: Swift tests 7/7 passed.

These checks confirm no adjacent local regression. They do not establish
Windows build/signing, native device/store, deployed network/IAM/provider,
staging capacity/fault recovery, legal/support or independent-review evidence.
No BSA visual package was generated or modified.

### Post-donor-checkout full local regression — 2026-08-15

After the public order/status response boundary was tightened, the current
Alerts worktree passed:

- Web/API focused contract suite: 19/19.
- Alerts API tests: 54/54.
- API TypeScript and Web production builds: passed; all seven Web routes
  generated.
- Contract validation: 11 fixture/schema mappings plus the v1 template
  catalogue contract; OpenAPI 3.1 with 32 paths and all local references.
- Disposable PostgreSQL application harness: `L02_SECURITY_REMEDIATIONS=PASS`
  and `L03_APPLICATION_BEHAVIOR=PASS`, including cross-replica replay,
  two-listener wake-up, independent queue progress and Companion assertions.

The Go services, mobile, marketing, macOS and scheduler suites had already
passed after the preceding Web-only changes and no files in those repositories
changed in this donor-checkout fix. This remains local/synthetic evidence; it
does not close Razorpay, deployment/IAM, browser/OBS, staging capacity/fault
recovery, store/device, legal/support or independent-review gates. No BSA
visual package was generated or modified.

### Continuation sweep and overlay cleanup — 2026-08-15

The continuation sweep re-ran the current local boundaries after the strict
Web projection work:

- Payment Go: unit tests, race tests and `go vet` passed.
- Alert-worker Go: unit tests, race tests and `go vet` passed.
- Disposable PostgreSQL L02/L03/L04/L05 harness passed, including security
  remediations, application behaviour, payment/worker SQL integration,
  two-listener wake-up and cross-replica replay.
- Alerts API: 54/54; Web production build; contract validation with 11 fixture
  mappings, template-catalogue validation and 32 OpenAPI paths passed.
- Crons: 2/2; infrastructure: 8/8; mobile: 23/23, lint, typecheck and
  dependency hardening 2/2; macOS: 7/7; marketing: 4/4.
- Both payment and worker images rebuilt as pinned, static, non-root distroless
  images; the corrected empty-environment smoke checks returned bounded
  missing-configuration errors.

The overlay runtime also now clears its display-completion timer on unmount,
preventing stale callbacks after an OBS/browser source closes. This does not
change durable delivery or acknowledgement semantics. The sweep remains local
evidence only: provider approval, deployed IAM/network/database configuration,
Cloud Tasks and Scheduler rehearsal, authenticated browser/OBS, capacity and
fault-injection, native/store, legal/support and independent review remain
open. No BSA visual package was generated or modified.

### Windows Companion source boundary — 2026-08-15

The Windows Companion now has a WinUI 3/C#/XAML source boundary with a
provisional build target, inactive/unpaired shell, strict Companion response
decoder and fail-closed lease/command/redaction policy. XML syntax checks pass
locally. The workspace has no Windows SDK/.NET toolchain, so no Windows build,
runtime test, package/signing, Credential Manager/DPAPI, pairing, OBS or device
evidence is claimed. The Windows support floor remains an owner decision.

### L06–L08 continuation verification — 2026-08-15

The scheduler/payment/Companion continuation checks were rerun after the
acceptance-record cleanup:

- `bharatstudio-crons`: schedule contract 2/2; all six v1 schedules remain
  disabled and contain no scheduler database/provider credentials.
- Payment webhook Go: `go test ./...`, `go test -race ./...` and `go vet ./...`
  passed, including the private payment/refund reconciliation handler slices.
- Alert worker Go: the same unit, race and vet checks passed.
- `bharatstudio-companion-mobile`: Jest 23/23, lint, TypeScript typecheck,
  dependency-hardening 2/2 and valid React Native config JSON passed.
- macOS Companion: `swift test` passed 7/7.
- `bharatstudio-infra`: deployment/observability contract 8/8.
- `bharatstudio-marketing`: static-site checks 5/5.

These are local checks only. Cloud Scheduler delivery, deployed OIDC/IAM,
provider behavior, Windows build/signing, native pairing/OBS, device/store,
legal/support, staging capacity/failure rehearsal and independent review
remain open. No BSA visual package was generated or modified.

### L03 public checkout asset handoff — 2026-08-15

Added a bounded Razorpay Checkout browser-asset loader. It accepts only the
exact provider script origin, reuses a loaded asset, rejects a conflicting
marked script and returns a bounded failure when the asset stalls. Focused
tests pass 5/5 and the Web production build passes. This is browser-handoff
reliability evidence only; it does not prove provider checkout, CSP deployment,
webhook truth, network recovery or staging behavior. No visual package was
generated or modified.
### Public tip idempotency-key boundary — 2026-08-15

The public tip-order route previously validated only the idempotency-key
length, while the authenticated subscription route already constrained the
header to a safe bounded character set. The public route now rejects keys
outside `A-Za-z0-9._:-` before channel/payment-service work begins. The new
regression test confirms that malformed input does not invoke the payment
service; the complete API route suite passes 40/40 and the API TypeScript
check passes. This is local request-boundary evidence only. It does not close
Razorpay approval, provider sandbox/live behavior, deployment/IAM, staging
retry/reconciliation or browser/OBS evidence. No BSA visual package was
generated or modified.
### L04 payment-intent idempotency correction — 2026-08-15

The latest expiry-cap rewrite of the payment-intent function had omitted the
post-conflict comparison that rejects reuse of an idempotency key with changed
amount or donor inputs. Forward migration `0056_v1_l04_payment_intent_idempotency_hardening.sql`
restores that guard, adds a `NOT VALID` database format check for future keys,
and preserves historical rows. The disposable `pnpm db:test:l03` run passed,
including the mismatch regression. This is local database evidence only; it
does not establish deployed migration execution, Razorpay behavior, IAM,
staging concurrency or provider recovery. No BSA visual package was generated
or modified. The disposable migration runner was also changed to apply all
post-L02 migration files in lexical order, preventing the acceptance harness
from silently omitting a future forward migration.
### Cross-surface idempotency-key contract — 2026-08-15

The OpenAPI header component, Creator API public/subscription routes,
Companion action route and private Go checkout/subscription handlers now reject
present-but-unsafe idempotency keys using the same bounded alphabet. Missing
Companion keys retain the prior `idempotency_key_required` response. API tests
pass 55/55, Go unit/race/vet checks pass, and OpenAPI validation passes. This
is local contract evidence only; deployed provider, IAM, device and staging
evidence remain open. No BSA visual package was generated or modified.

### L05/L06/L09 continuation gate — 2026-08-15

The automatic continuation pass recorded the following additional local
evidence:

- alert-worker Go unit tests, race tests and `go vet` passed;
- `bharatstudio-crons` contract tests passed 2/2 with all schedules disabled;
- `bharatstudio-infra` deployment/observability contract tests passed 8/8;
- `pnpm db:test:l03` passed the disposable L02–L05 database and worker chain,
  including the two-listener wake-up and shared-PostgreSQL cross-replica proof.

The L05 runbook and implementation were reviewed together with no new local
mismatch. These results do not claim live Cloud Tasks, deployed OIDC/IAM,
capacity, provider, staging recovery, OBS, legal/support or independent-review
evidence. No BSA visual package was generated or modified.

### L03 public tip retry-boundary correction — 2026-08-15

The public tip form had an unbounded order request and generated a fresh
idempotency key on every submission. It now uses bounded order/status request
timeouts, retains the same key across retryable/ambiguous failures and keeps it
until the checkout handoff succeeds, including when the created order cannot
open its browser modal. Focused tests pass 4/4 and the Web production build
passes. This is local browser evidence only; provider, deployed network and
staging reconciliation remain open. No BSA visual package was generated or
modified.

### L04 payment-boundary focused audit — 2026-08-15

The Go payment boundary was re-read across webhook verification, payload
normalization, account-scoped Razorpay adapters, SQL persistence and recovery
entry points. No additional locally verifiable correctness gap was found:

- `x-razorpay-event-id` is required, bounded and restricted to the database-safe
  identity alphabet before it can become a deduplication key or trace value;
- HMAC-SHA256 is computed over the exact bounded raw request body before the
  store is called;
- linked-account order, payment and refund calls use server-resolved account
  references, while webhook account attribution must match the immutable local
  intent;
- payment, refund, subscription and dispute evidence is persisted through
  idempotent private SQL boundaries, with malformed or mismatched projections
  quarantined or rejected before worker wake-up; and
- payment-to-worker wake-up failure remains retryable after durable persistence,
  so the provider can retry without creating a second financial or alert
  projection.

`go test ./...`, `go test -race ./...` and `go vet ./...` passed in
`services/payment-webhook-go`. This is local implementation evidence only;
Razorpay approval/provider sandbox or live execution, deployed OIDC/IAM and
secrets, Cloud Run/Cloud Tasks behavior, staging recovery/capacity and
independent review remain open. No BSA visual package was generated or
modified.

### Current monorepo regression rerun — 2026-08-15

The current worktree was rechecked after the L01/L02 dependency audit. The
Alerts API suite passed 55/55, the API and Web production build passed, the
contract validator passed all 11 fixtures plus the 35-path OpenAPI document,
the Go payment service passed unit/race/vet checks, and the Go alert worker
passed unit/race/vet checks. The earlier root-level `go test ./...` invocation
was not treated as evidence because the monorepo root has no Go module; both Go
commands were then rerun from their respective service module directories and
passed.

The role prerequisite file and archive grants were also re-read: the
`bsa_*` role provisioning SQL is present, `archive_records` has explicit
append-only grants/policies, and the L02 checks assert the same. No additional
locally actionable L01/L02/L03/L04/L05 defect was found. Provider approval,
deployed infrastructure/IAM, Cloud Tasks, Neon direct-listener behavior,
browser/OBS staging, capacity/failure rehearsal, independent review and the
deferred BSA runtime packages remain open. No BSA visual package was generated
or modified.

### Current Companion consumer rerun — 2026-08-15

The React Native Companion suite passed 23/23 with lint and TypeScript checks.
The macOS native Companion suite passed 7/7 with `swift test`. Windows/C#
remains unverified because the current environment has no .NET/Windows SDK;
this is preserved as an explicit platform gate rather than inferred from source
inspection. No BSA visual package was generated or modified.

### Windows contract source correction — 2026-08-15

The Windows C# transport decoder was reviewed against the OpenAPI Companion
schemas and the stricter mobile/macOS consumers. Missing/null `slots` and
`clientInstanceId` values could otherwise reach null dereferences; a numeric
range check also accepted unsupported `maxSlots` values between the approved
8/16/32/64 choices. The source now rejects those cases and default/missing
timestamps before UI use. This is a source-level correction only: no .NET or
Windows SDK is available here, so compilation, runtime, signing and device
evidence remain open. No BSA visual package was generated or modified.

### Mobile API projection slice — 2026-08-15

The React Native `CompanionApi` now validates and exposes the existing
recent-history, billing/plan, account-session list and session-revocation
contracts. Tests remain 23/23, lint passes and TypeScript passes. This does not
claim native Google sign-in, secure token storage, push, offline/background
sync, or real-device evidence. No BSA visual package was generated or modified.

The follow-up mobile screen/API pass added one projection-routing regression
test; the current mobile suite is now 24/24 with lint and TypeScript passing.

### Post-surface regression rerun — 2026-08-15

After the Web Companion and mobile projection changes, Alerts API tests passed
55/55, OpenAPI/fixture validation passed (11 fixtures, 32 paths), and the API
and Web production builds passed. React Native tests passed 24/24 with lint
and TypeScript. This confirms local regression safety for the new surfaces; it
does not close native auth/storage/push/device work, provider execution,
deployed capacity/failure evidence, OBS/browser testing or independent review.

The cross-repository continuation pass also passed marketing 5/5, scheduler
contracts 2/2, infrastructure contracts 8/8, and macOS Swift tests 7/7. These
are local checks only; the scheduler remains disabled and Windows/native
pairing, provider, store, deployment and legal gates remain open.

### Mobile Google exchange contract slice — 2026-08-15

The mobile client now validates the documented Google identity exchange input
and opaque session response, including expiry and the authenticated user
projection. Negative input and provider failure mapping are covered. The
current mobile suite is 26/26 with lint and TypeScript passing. Native Google
SDK integration, Keychain/Keystore persistence, device testing and store
evidence remain open; no plaintext token storage was added.

### Mobile secure session storage slice — 2026-08-15

`KeychainCompanionSessionStore` was added to the React Native client using
`react-native-keychain` 10.x. It uses the versioned service
`in.bharatstudio.companion.session.v1` and the device-only unlocked storage
option, validates token length and expiry, clears malformed/expired values,
and fails closed when the secure provider is unavailable. No plaintext or
AsyncStorage fallback was introduced. Focused store tests pass 3/3 and the
complete mobile suite passes 29/29; lint and TypeScript also pass.

This does not yet prove native Keychain/Keystore behavior on physical devices,
device lock/restart, backup/restore, revocation, or signed release builds.
The session controller that connects the exchange response to this store and
native Google credential acquisition remain implementation work. No BSA visual
package was generated or modified.

### Mobile session-controller slice — 2026-08-15

`CompanionSessionController` now binds Google identity exchange to the secure
session store without exposing a token before persistence succeeds. It clears
in-memory authorization before persistent sign-out, clears expired sessions
before API use, and leaves restored account identity unset until `/v1/me`
provides the server-owned projection. The controller tests pass 5/5 and the
full mobile suite passes 34/34 with lint and TypeScript passing.

The controller is not yet wired into the React Native app bootstrap, and no
claim is made for native Google SDK, physical-device Keychain/Keystore,
restart/lock/backup/restore, offline/reconnect or signed-release evidence. No
BSA visual package was generated or modified.

### Mobile runtime/bootstrap wiring slice — 2026-08-15

`CompanionRuntime` now composes the API, session controller and secure store,
and `App.tsx` accepts explicit API/provider configuration. Startup restores a
secure session and requires a server `/v1/me` projection before rendering the
account as signed in. A rejected session is cleared, sign-in uses only the
injected platform credential provider, and failures render a bounded recovery
message. Runtime tests pass 3/3; the full mobile suite passes 37/37 with lint
and TypeScript passing.

Native Google SDK/configuration, physical-device storage, offline/reconnect,
remaining projection loading, app-store and signed-release evidence remain
open. No BSA visual package was generated or modified.

The same runtime now loads state, queues, history, billing and account-session
projections for the selected authorised channel and reloads on channel
selection. The mobile suite passes 46/46 with lint and TypeScript; this remains
local projection evidence only.

The rendered mobile Sessions screen also invokes server-side revocation for a
non-current session and reloads the server projection after success; it does
not perform local-only session deletion. Projection loading also ignores stale
responses after a rapid channel switch. Mobile tests remain 46/46 with lint
and TypeScript passing.

### Mobile offline/reconnect policy slice — 2026-08-15

The mobile client now has a bounded recovery policy: transport/timeouts and
5xx responses retry with exponential delays capped at 60 seconds, exhausted
retries enter an explicit offline state, 401 requests re-authentication, and
403/client/conflict responses fail without retry. The policy does not buffer
payments, alerts, queues or checkout and cannot claim delivery offline. Policy
tests pass 4/4; the full mobile suite passes 41/41 with lint and TypeScript.

Native connectivity/background integration, push behavior and physical-device
offline/reconnect evidence remain open. No BSA visual package was generated or
modified.

### Mobile notification/background policy slice — 2026-08-15

The mobile client now rejects notification payloads containing financial,
donor or arbitrary fields and accepts only bounded operational kinds, opaque
IDs and timestamps. Registration tokens are bounded and platform-labelled;
background refresh timing is bounded with a 15-minute default. Policy tests
pass 3/3 and the full mobile suite passes 49/49 with lint and TypeScript.
APNs/FCM, server preference persistence/dispatch, native background hooks and
device evidence remain open. No BSA visual package was generated or modified.

### Mobile control-session lifecycle slice — 2026-08-15

`CompanionControlSessionManager` now handles acquire, same-client renewal,
expiry inspection and revoke for the server-owned mobile control lease. A
replacement session ID fails closed, and revoke clears local state before the
server call. The manager does not claim to replace server authorization or
entitlement checks. Lifecycle tests pass 4/4; the full mobile suite passes
45/45 with lint and TypeScript passing.

UI callback wiring, cross-device conflict, native pairing and deployed
lease/action evidence remain open. No BSA visual package was generated or
modified.

### macOS Keychain session-storage slice — 2026-08-15

The macOS helper now includes a Security-framework Keychain store for the
opaque Companion session. The versioned service is non-synchronised; token
length and expiry are validated, malformed/expired records are removed, and
there is no UserDefaults/plaintext fallback. The complete Swift suite passes
10/10. Physical Keychain/sandbox, lock/restart, pairing, signing and
notarisation evidence remain open. No BSA visual package was generated or
modified.
