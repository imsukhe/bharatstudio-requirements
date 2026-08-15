# L07 — Companion web, mobile and native desktop helper

**Status:** `Core Web/API/mobile Companion slices implemented — native product, device and external release gates pending`  
**Level:** L3  
**Owner:** Mobile / Windows / macOS / API / security  
**Depends on:** L01; the approved API/auth portions of L03; L05 control contracts before live control integration  
**Blocks:** full-product v1 launch
**Test record:** [`../tests/TC-L07-companion-web-mobile-desktop.md`](../tests/TC-L07-companion-web-mobile-desktop.md)
**Review record:** [`../reviews/2026-08-15-L07-L08-L10-release-surface-review.md`](../reviews/2026-08-15-L07-L08-L10-release-surface-review.md)
**Local regression record:** [`../reviews/2026-08-15-local-regression-and-surface-verification.md`](../reviews/2026-08-15-local-regression-and-surface-verification.md)

## Objective

Ship BharatStudio Companion as a separate product surface bundled with Alerts entitlements: Web Companion Console, iOS/Android companion, and an optional local native helper.

## Pre-implementation decision

The mobile framework is selected as **React Native 0.87.0**, using the bare React Native Community CLI and matching CLI/tooling `20.2.0`, pinned exactly in the repository. React Native's New Architecture and Hermes are the default runtime direction; native modules are limited to secure storage, push notifications, authentication and approved device integrations. The repository requires Node `>=22.13.0`. The project owner approved the proposed v1 floors: **iOS 15.1+** and **Android API 26+**. Apple Developer and Google Play release accounts, package identifiers, signing, privacy declarations and test tracks must still be provisioned before release work. Desktop is already locked: WinUI 3 + C# + XAML for Windows and SwiftUI + Swift for macOS.

## Current implementation evidence — 2026-08-15

- Bootstrapped `/Users/sukhdevsingh/Workspace/Bharat Studio/bharatstudio-companion-mobile` from the official React Native Community CLI template and upgraded the exact supported line to React Native `0.87.0` with the matching Community CLI/tooling `20.2.0`, retaining New Architecture/Hermes defaults, iOS/Android native projects, TypeScript, Jest and lint configuration. Node is pinned to the package's supported `>=22.13.0` floor.
- Preserved the repository's Companion governance files and did not copy the generated debug signing key. The scaffold contains no production API origin, provider credentials, payment checkout, raw OBS credential, push provider, store signing identity or client-side entitlement authority.
- `npm test -- --runInBand`, `npm run lint` and the explicit `npm run typecheck` (`tsc --noEmit`) pass locally.
- The mobile lockfile pins compatible overrides for `fast-xml-parser@5.10.1` and `image-size@2.0.2`; the unused `@react-native/new-app-screen` dependency was removed. The exact RN/CLI upgrade passes mobile tests, lint and typecheck. The package now exposes the explicit `npm run typecheck` script (`tsc --noEmit`) so CI and the task record use one reproducible command. The registry audit still reports eight high findings because the current audit metadata propagates the `image-size@2.0.2` advisory through Metro/RN even after the upgrade. `patch-package` now applies a narrow local guard for zero-length HEIF/ICNS/JXL parser boxes, and the clean-install `postinstall` plus `test:dependencies` checks verify the patch after install (2/2 dependency checks). This is mitigation evidence, not a cleared audit: the residual must still be resolved by an upstream fixed release or formally risk-accepted before release; do not apply the audit tool's forced React Native 0.72 downgrade.
- Added the first signed-out Companion shell in `src/CompanionShell.tsx`: accessible account connection state, sign-in handoff placeholder, read-only feature cards and explicit boundaries around payment delivery, YouTube data and desktop-mediated OBS control. It contains no fabricated account metrics or client-side entitlement decisions. Jest, lint and TypeScript checks pass after the shell change.
- Added `src/api/CompanionApi.ts`, a contract-scoped REST client for `/v1/me`, Companion state, queue-list and Companion actions. It requires an injected access-token provider, enforces HTTPS outside localhost, validates idempotency-key bounds, uses the documented action allowlist at runtime and maps errors to bounded categories without exposing response bodies.
- Extended the mobile shell with a signed-in, server-state-driven home: authorised channel/role, overlay connection, pending-alert count and bounded pause/resume actions. It renders all server-authorised channels instead of assuming `channels[0]`, lets the host select the channel whose state is loaded, loads the documented queue list, lets the host select an active queue, and carries that queue ID with every action callback. It exposes no payment, YouTube or direct OBS operation and disables controls for non-operator roles or missing queue targets. Mobile tests, lint and TypeScript checks pass locally.
- Hardened the mobile shell against stale cross-channel inputs: state is used only when its channel is present in the authenticated channel list, and queue candidates are filtered to the selected channel before rendering or targeting an action. A regression test proves that an active queue and pending count from another channel cannot be displayed or invoked. The historical shell regression passed 19/19; the current suite passes 23/23 after the response-boundary tests below.
- Added the macOS SwiftUI executable shell under `bharatstudio-companion-desktop/macos/`, with a provisional macOS 11 package target, unpaired state and explicit Keychain/scoped-command boundaries. `swift test` passes. No OBS connection or pairing authority is wired.
- Added a dedicated `/companion` Web Companion Console using the existing server-owned state/action contract. It loads the selected authorised channel and its queue list, supports explicit channel/active-queue selection, carries the selected queue ID in every command, disables controls when no valid queue target exists, exposes the finite pause/resume/test actions only to operator roles, and explicitly has no direct OBS or localhost command path; the Alerts web production build passes.
- Narrowed the v1 Companion action contract to the three actions with implemented effects: queue pause, queue resume and durable test alert. Every action requires a queue target; test alerts are linked to their command for safe idempotent retries. Alert approve/hold/replay remain available through the authenticated moderation route, not as falsely accepted Companion commands.
- Added database enforcement for the Companion role boundary: queue controls are accepted only for owner/admin/operator roles. Moderators may still use the separately scoped moderation route, but cannot issue Companion pause/resume/test commands; UI role checks are backed by RLS in migration `0040_v1_l03_overlay_companion_role_guards.sql`.
- Added migration `0041_v1_l07_companion_action_contract.sql`: new Companion command rows are constrained to the three implemented actions (`pause_queue`, `resume_queue`, `send_test_alert`). The check is intentionally `NOT VALID` so historical unsupported command rows remain append-only evidence and are not deleted or rewritten. The disposable database harness applies the migration.
- Added migration `0042_v1_l07_companion_action_layout.sql`: Companion layouts are append-only, RLS-protected snapshots with server-owned Free/Pro/Creator/Studio allocations of 8/16/32/64 slots and page sizes restricted to 4/8/16. The database validates role, slot shape/index uniqueness, approved action names, active same-channel queue targets, optimistic versioning and tier limits. Invalid new layouts are rejected without touching accepted alert/payment evidence; historical rows are never rewritten.
- Hardened the mobile Companion response boundary against the full OpenAPI v1 shapes. `CompanionApi` now requires UUID identifiers for users, channels, queues, layouts, action results and control sessions; rejects unknown top-level and nested fields; enforces queue/label/page bounds; rejects duplicate or out-of-range layout slots; validates UUID action targets and event IDs; and returns newly constructed typed projections rather than forwarding untrusted response objects. This closes a client-side contract ambiguity without changing server authority or durable alert/payment state. Mobile tests, lint and TypeScript checks pass locally.
- Added the authenticated web `/companion` layout editor and REST/OpenAPI layout contract. It can add/remove only the three implemented actions, select a server-provided page size, and save with `If-Match-Version`; it does not expose arbitrary commands or client-owned tier authority. The mobile API now reads and updates the same server-owned layout contract. Alerts web build, API tests, contract validation and mobile tests/lint/typecheck pass locally.
- Aligned the mobile `CompanionApi` idempotency-key validation with the server contract: keys must be 16–128 characters, and the client rejects shorter keys before network access. The mobile API tests cover this negative path.
- Added the initial WinUI 3/C#/XAML project boundary under `bharatstudio-companion-desktop/windows/`, including the inactive/unpaired shell, fail-closed lease/command policy and support-log redactor. The project records a provisional `10.0.19041.0` build-agent minimum and pins the current Windows App SDK stable package line; the owner-approved Windows support floor is still pending. No OBS connection, credential storage, pairing transport, signing or packaging is included in this slice.

### Local verification rerun — 2026-08-15

React Native mobile tests pass 23/23, ESLint passes, TypeScript typecheck
passes, `react-native config` resolves, and the dependency-hardening check
passes 2/2. The macOS Swift package test passes, and the marketing/static
surface test passes 5/5. These are repeatable local checks only. They do not
clear the eight high dependency-audit findings, establish Windows build/signing
evidence, prove native OBS pairing/security, or satisfy iOS/Android store
accounts, device matrix, signing, privacy declaration and review gates.

### Server-owned control-session lease slice — 2026-08-15

Added migration `0053_v1_l07_companion_control_sessions.sql`. Companion
control sessions are short-lived, append-preserving operational leases with
client type and client-instance identity. Acquisition is authorized by the
server-side channel role, serialized by a transaction-scoped channel lock and
safe for transaction-pooled connections. The same client instance renews its
existing lease instead of creating a second row. A Free channel admits one
active lease; paid-channel concurrency is intentionally not invented here and
remains a future entitlement decision. Expired and revoked rows remain stored
with reason/audit timestamps. The request role cannot write the table directly.

The disposable PostgreSQL harness proves first acquisition, same-instance
renewal, Free-tier second-client rejection, revocation, post-revocation
acquisition and direct-write denial. This local database slice does not claim
mobile/desktop pairing, OBS WebSocket authentication, secure-keychain storage,
device testing, signing or store evidence.

The authenticated Alerts API now exposes the same server-owned lease through
`POST /v1/channels/{channelId}/companion/control-session` and
`DELETE /v1/channels/{channelId}/companion/control-session/{sessionId}`. The
routes require the normal bearer session, validate client type/instance
identity, return a bounded busy response for an occupied Free channel, and
never return provider, OBS or credential material. The mobile `CompanionApi`
implements acquire/revoke for this contract and correctly handles the `204`
revocation response. API tests (54/54), TypeScript/web builds, OpenAPI
validation (32 paths), mobile tests (23/23), lint and the explicit TypeScript
typecheck script pass locally on 2026-08-15. Authenticated device, pairing, deployed and native
helper evidence remains pending.

### macOS native policy boundary — 2026-08-15

Added `CompanionPolicy.swift` to the macOS package as a deliberately
platform-neutral fail-closed boundary for the future native helper. It checks
that a command uses an active, non-revoked server-issued lease, matches the
leased session and channel, has a bounded command window, and has explicit
user confirmation. The action surface is finite (`pause_queue`,
`resume_queue`, `send_test_alert`); arbitrary local commands are not accepted.
The same package includes deterministic redaction for authorization, token,
secret, password, cookie and OBS credential-like log values before any future
support-bundle flow.

This slice does not claim pairing, cryptographic command signing, Keychain
storage, OBS WebSocket access, network transport, support upload, or native
device evidence. Those remain gated by the approved helper protocol and
platform security review. The macOS executable entry point was also renamed
from `main.swift` to `CompanionApp.swift` so the Swift `@main` entry point
builds correctly under Swift 6.

`swift test` passes 7/7 locally on 2026-08-15, including decoding of the
approved Companion REST state/layout/control-session response shapes and
rejection of an unsupported action name. No payment, queue, outbox, delivery
or alert visual package was changed.

### React Native response-boundary hardening — 2026-08-15

The mobile Companion API now decodes server responses at runtime instead of
casting `response.json()` directly. It validates the v1 user, state, queue,
layout, action-result and control-session envelopes; enforces the finite action
and role/tier sets; checks bounded counts and timestamps; and rejects malformed
state or unsupported server-provided actions as a bounded request failure.
Jest passes 23/23, lint passes and the TypeScript check passes. This is client
contract evidence only; it does not close native device/offline/reconnect,
signing/store, Windows or deployed API evidence.

### Windows C# response-boundary hardening — 2026-08-15

The Windows transport decoder had malformed-response paths that could throw a
`NullReferenceException` or accept default values instead of returning a
bounded contract failure. It now rejects missing/null slot arrays and slot
objects, requires the exact approved `8/16/32/64` `maxSlots` ladder, validates
the approved client-instance alphabet, and rejects missing/default timestamps
in state, control-session and action-result envelopes. This aligns the source
boundary with the OpenAPI contract and the stricter mobile/macOS consumers.
The change is source-audited only: the current environment has no
.NET/Windows SDK, so Windows compilation, runtime tests, packaging and signing
remain open and are not claimed as passed.

## Fresh local audit — 2026-08-15

The Companion web/API contract, mobile client, macOS shell, Windows contract,
database role/session guards and the L07 acceptance matrix were reviewed
together. No additional locally verifiable correctness gap was found.

The local boundary is explicit: Companion state and controls are server-owned,
channel/role/queue scoped and independently disableable; Companion limits never
modify accepted payments, durable ingestion, queues, outbox rows or alert
delivery. The mobile client has no YouTube/payment/OBS credential authority,
the web console has no localhost OBS path, and the macOS package remains an
unpaired shell. The Windows README correctly makes no build claim without a
Windows App SDK environment.

L07 remains open and must not be marked release-verified until the native
pairing/revocation and OBS authentication flow, secure platform storage,
offline/reconnect/crash behavior, Windows build/signing, macOS app
signing/notarisation, iOS/Android device and store tracks, privacy/accessibility
review, and the remaining mobile dependency-advisory disposition have real
evidence. No new visual alert packages are generated as part of L07.

### Mobile transport-boundary hardening — 2026-08-15

The mobile `CompanionApi` previously allowed a stalled fetch to remain pending
indefinitely and propagated raw transport or malformed-JSON errors to callers.
It now applies a bounded 10-second request timeout by default (configurable
only within 1–60 seconds), aborts supported requests, and maps transport and
response-decoding failures to the bounded `request_failed` error category.
The timeout is independent of Alerts ingestion, payment state and queue
delivery. Mobile tests now pass 23/23, lint/typecheck, dependency-hardening
2/2 and React Native config checks pass. This is local client evidence only;
device offline/reconnect/crash testing remains open.

### Mobile API projection slice — 2026-08-15

The React Native `CompanionApi` now has runtime-validated consumers for the
approved recent-history, billing/plan, and account-session projections. It
supports server-side session revocation and rejects malformed, cross-contract,
out-of-range or unknown response fields before the UI can consume them. The
implementation uses the existing HTTPS REST endpoints and does not store
credentials or introduce a client-side entitlement decision. Mobile tests
remain 24/24 with lint and TypeScript passing. Native Google sign-in, secure
platform storage, push registration, offline/background sync and real-device
evidence remain separate unfinished work.

### Mobile Companion screen-set implementation — 2026-08-15

The React Native Companion shell now has explicit Home, Activity, Health,
Settings, Sessions and Help screens. Activity, health, plan/lock, and session
views consume only the optional server projections passed by the controller;
notification preferences now use the authenticated server persistence
contract and remain explicitly unavailable only when that service is down.
Session revocation is surfaced as a server-owned callback, and the UI does not
invent OBS health or notification success. Tests remain 24/24 with lint and
TypeScript passing. Native Google
sign-in, secure platform storage, push/background behavior and device testing
remain open implementation/release work.

### Mobile Google exchange contract slice — 2026-08-15

The mobile `CompanionApi` now implements the documented Google identity
exchange endpoint. It validates the bounded identity-token/device-label input,
requires the v1 envelope, validates the opaque returned session token,
expiration and authenticated user projection, and maps provider/auth failures
to bounded client errors. It does not persist the token in plaintext or add a
client-side identity/entitlement authority; secure platform storage remains
the next native implementation slice. The current mobile suite is 26/26 with
lint and TypeScript passing.

### Mobile secure session storage slice — 2026-08-15

The mobile client now has a production-boundary session store using
`react-native-keychain` 10.x. The opaque BharatStudio session is written under
the versioned service identifier
`in.bharatstudio.companion.session.v1` with
`WHEN_UNLOCKED_THIS_DEVICE_ONLY`, which maps to the platform secure credential
store rather than application preferences. Reads validate the bounded token
and expiry, clear malformed or expired material, and return no session. Writes
reject expired/invalid values. Clear failures and unavailable secure storage
fail closed; there is no AsyncStorage, plaintext, or silent in-memory
credential fallback.

Focused store tests cover secure service/options, malformed and expired
cleanup, expiry rejection, and the absence of a fallback. Mobile tests pass
29/29 with lint and TypeScript passing. This is mocked/local contract evidence;
real iOS Keychain, Android Keystore, app restart, device lock, backup/restore,
revocation and release-signing evidence remain open. The session controller
and native Google credential acquisition are still pending implementation.

### Mobile session-controller slice — 2026-08-15

`CompanionSessionController` now connects the Google exchange contract to the
secure session store. Sign-in persists the opaque session before exposing it
to API callers; secure-store failure leaves the controller signed out. Restore
loads only the secure session and deliberately does not invent a user
projection; the app must fetch the server-owned `/v1/me` projection before
rendering account state. Expired in-memory sessions are cleared before an API
request can use them, and sign-out clears the in-memory session before asking
the secure provider to clear persistent material.

The controller has five focused tests and the full mobile suite passes 34/34
with lint and TypeScript passing. This closes the local controller slice only.
Native Google credential acquisition, wiring into the app bootstrap, real
Keychain/Keystore behavior and offline/reconnect/device evidence remain open.

### Mobile runtime/bootstrap wiring slice — 2026-08-15

`CompanionRuntime` now composes `CompanionApi`, the session controller and the
secure store. The React Native app accepts an explicit API base URL and an
injected platform Google-credential provider; on startup it restores secure
session state and fetches `/v1/me` before treating the account as signed in.
Sign-in uses the injected provider, persists through the controller, and
surfaces a bounded recovery message on failure. The default scaffold remains
signed out when no production configuration is supplied.

Runtime tests cover secure restore followed by `/v1/me`, rejected-session
cleanup and injected sign-in. The full mobile suite passes 37/37 with lint and
TypeScript passing. Native Google SDK implementation/configuration, projection
loading beyond `/v1/me`, device and release evidence remain open.

The runtime also loads the server-owned state, queues, recent history, billing
projection and account sessions for the selected authorised channel, and
reloads that projection when the user changes channel. Mobile UI renders only
the returned projections; it does not derive entitlements or financial state
locally. The projection test is covered in the mobile suite, which now passes
46/46 with lint and TypeScript passing.

The rendered mobile session screen now calls the server revoke endpoint for a
non-current session and refreshes the server projection after success; it does
not mutate the session list locally or allow current-session self-revocation.
Projection loading also uses a latest-request guard so a slower response for a
previous channel selection cannot overwrite the newly selected channel.

### Mobile offline/reconnect policy slice — 2026-08-15

The mobile client now has a bounded recovery policy for Companion transport
operations. Transport/timeouts and server 5xx responses use exponential retry
delays from 1 second to a 60-second maximum and then enter an explicit offline
state. 401 requires re-authentication; 403, other client errors and conflicts
fail without retry. Recovery has no local payment, alert, queue or checkout
buffer and cannot claim delivery while offline. The online transition is
explicit and side-effect free.

The focused policy tests pass 4/4 and the full mobile suite passes 41/41 with
lint and TypeScript passing. Native connectivity listeners, background task
integration, push delivery and real device/offline evidence remain open.

### Mobile notification/background policy slice — 2026-08-15

The mobile client now validates a v1 privacy-minimised notification envelope
with only an opaque notification ID, operational kind and timestamp. Amounts,
donor names, donor messages, payment details and arbitrary payload keys are
rejected. Registration tokens are bounded and platform-labelled. Generic copy
is generated locally from the approved kind, and background refresh scheduling
is bounded to a 1-minute–24-hour interval with a 15-minute default. No push
provider call, notification preference persistence or financial/alert payload
buffering has been added.

Policy tests pass 3/3 and the full mobile suite passes 49/49 with lint and
TypeScript passing. Native APNs/FCM registration, server preference/dispatch
contract, background-task hooks and device evidence remain open.

### Native APNs/FCM and server notification-registration slices — 2026-08-15

The React Native client now uses the modular React Native Firebase Messaging
adapter, injected by the native app entry point, for explicit Android FCM and iOS FCM-over-APNs registration. Firebase
auto-init and automatic iOS remote-message registration are disabled; the
adapter requests permission, registers the device, obtains a platform-labelled
token, validates foreground/background envelopes and ignores malformed or
sensitive payloads. Provider credentials and release configuration remain
outside the repository and must be injected by the signed build pipeline.

The Alerts API now exposes authenticated v1 routes for account-scoped
notification preferences and device registration/list/revocation. Preferences
are limited to connection, security and action-failure categories. The API
never accepts tip, donor or payment content as a push category. Raw APNs/FCM
tokens are accepted only over the authenticated HTTPS boundary, encrypted with
an AES-256-GCM key before persistence, and never returned to clients or logs;
the database stores only encrypted material plus a SHA-256 fingerprint for
idempotent registration. Device revocation is a soft state transition.

Local evidence: Alerts API tests pass 62/62 and TypeScript build passes;
mobile tests pass 52/52 with lint and TypeScript passing. This is contract and
mock/provider-boundary evidence only. Physical iOS/Android permission,
background delivery, APNs/FCM provider credentials, production key rotation,
and end-to-end device evidence remain release gates. Notification delivery is
best-effort operational messaging and must never be used as the source of
truth for payments, alert queues or delivery state.

The server now also has a provider-neutral dispatch policy boundary. It maps
only the four approved operational kinds to their corresponding preference,
filters disabled devices, normalizes the opaque notification envelope, and
rejects invalid identifiers or timestamps. The envelope has no amount, donor,
message, payment, payout or arbitrary-data fields. A real APNs/FCM adapter,
encrypted-token retrieval boundary and outbox/retry handling still require
provider and staging work; those adapters must reuse this policy.

Migration `0057_v1_l07_notification_preferences_and_devices.sql` has
disposable PostgreSQL behavior coverage for defaults, preference updates,
token-fingerprint idempotency, soft revocation and list exclusion. The test
passed as part of `pnpm db:test:l03`.

### Mobile control-session lifecycle slice — 2026-08-15

`CompanionControlSessionManager` now handles the mobile client lifecycle for
the server-owned control lease: acquire, same-client renewal, expiry
inspection, and revocation. Renewal must return the same server session ID;
if a different session is returned, local control state is cleared and the
caller receives a bounded failure. Revocation clears local state before the
server call. The manager does not replace server role, entitlement, lease or
action authorization.

The focused lifecycle tests pass 4/4 and the full mobile suite passes 45/45
with lint and TypeScript passing. App UI callback wiring, cross-device conflict
testing, native helper pairing and deployed evidence remain open.

### macOS Keychain session-storage slice — 2026-08-15

The macOS helper now contains a Security-framework Keychain store for the
opaque Companion session. It uses the versioned service
`in.bharatstudio.companion.session.v1`, disables synchronisation, validates
bounded token/expiry values, deletes malformed or expired records, and has no
UserDefaults/plaintext fallback. The local Swift suite passes 10/10, including
the secure-session validation contract. Real Keychain access, app sandbox,
device lock/restart, signing/notarisation and integration with the pairing
flow remain open.

### Native OBS WebSocket security-boundary slice — 2026-08-15

The macOS helper now contains a local-only OBS WebSocket v5 client boundary.
It accepts only `ws`/`wss` loopback endpoints on port 4455, rejects userinfo,
query and fragment credentials, performs the OBS hello/identify
challenge-response, and sends only bounded request envelopes. The Windows
source boundary mirrors the same endpoint and challenge-response rules using
`ClientWebSocket`. Neither implementation opens a listener, forwards ports,
stores an OBS password, or logs raw frames. The server-issued Companion lease,
role checks, confirmation and audit remain authoritative over any local action.

macOS `swift test` passes 12/12 including endpoint and challenge-response
tests. Windows source/XML validation passes locally, but no Windows SDK/.NET
toolchain is installed on this host, so Windows compilation, OBS runtime,
Credential Manager/DPAPI storage, pairing transport, signed commands and
device evidence remain open. Pairing is not inferred or fabricated here: the
approved server pairing contract must exist before the helper can enable it.

## Tasks

1. Approve the mobile OS floors, create Apple/Google release accounts, reserve package identifiers, configure signing/test tracks and record the store privacy/data declarations.
2. Define v1 Companion screens: direct Google sign-in, read-only home, recent alert activity, health, connection state, notification preferences, plan locks, device/session list and help. Preference state and device inventory must use the server routes; no client-only saved state is authoritative.
3. Build Web Companion Console inside Alerts web for second-monitor operations. It is not the full creator configuration dashboard.
4. Build the React Native iOS/Android client using final REST contracts; use secure platform session storage, push registration, accessible/offline/reconnect UX and privacy-minimised notification payloads.
5. Implement server-owned control-session leases and one active control session for Free; enforce action/page/plan limits server-side. Limits must never alter payment receipt, ingestion, queue or alert delivery.
6. Build Windows helper and macOS helper with explicit pairing, native secure storage, local OBS WebSocket authentication, signed/scoped commands, revocation, consented health collection and redacted support bundle.
7. Implement Free's bounded approved one-tap actions, configurable 4/8/16 page grids and the authoritative 8/16/32/64 unique action-slot ladder (Free/Pro/Creator/Studio); no arbitrary command execution. These limits apply only to new Companion action configuration and never to payment or alert delivery.
8. Implement health state: helper freshness, OBS connection, scene/source state, alert-delivery state and approved metrics. Exclude YouTube state from v1.
9. Perform mobile/device, desktop security, app-store policy, accessibility, crash/reconnect, pairing/revocation and privacy reviews.

## Acceptance criteria

- Same Google identity loads the authorised account immediately; QR/PIN pairing is restricted to approved co-host/moderator paths if included.
- React Native is pinned to a supported exact version; approved iOS/Android floors, signing identities, store accounts and release tracks are recorded before implementation proceeds.
- Mobile and desktop cannot bypass server roles/entitlements or expose OBS credentials.
- Desktop helper is local-only, consented, revocable, and has no general-purpose local/public API.
- Companion limitations never cause alert loss or payment/reconciliation impact.
- iOS/Android/Windows/macOS acceptance matrices and release checklists pass.

## Rollback

Disable Companion/control flags, revoke sessions/pairings, retain audit history, and preserve Alerts delivery independently.

### Web Companion response-boundary hardening — 2026-08-15

The Web Companion API client no longer trusts unvalidated JSON for the signed-in
user, queue list, Companion state, Companion layout or Companion action result.
Runtime decoders now require the v1 envelope, UUID and timestamp shapes,
non-negative bounded counters, approved tier/action values, valid page/slot
limits and unique slot indexes. Malformed server responses fail closed before
they reach the Companion UI. The web TypeScript check and production build pass.
This is local browser-client contract evidence only; authenticated browser,
cross-replica, deployed and device evidence remains open.

### Automatic continuation verification — 2026-08-15

The Companion local gate rerun passed: React Native Jest 23/23, ESLint,
TypeScript typecheck, dependency-hardening 2/2 and `react-native config`.
macOS `swift test` passed 7/7. These checks confirm local contract and policy
regressions only; they do not close the dependency-advisory disposition,
Windows build/signing, native pairing/OBS, device/offline/reconnect, store,
privacy or deployed API evidence.

### Web Companion screen-set implementation — 2026-08-15

The Web Companion Console now consumes the existing server-authoritative
projections for the approved v1 operational screen set. In addition to the
existing queue controls and action layout, it renders recent alert activity,
server freshness/overlay connection health, plan and slot entitlements,
account device/session inventory with server-side revoke, and bounded help and
recovery guidance. The web client validates the session projection before
rendering it. Notification preferences now use the approved authenticated
persistence/API contract; the surface shows an explicit unavailable state only
when that service cannot be loaded and never pretends a failed save succeeded.
`apps/web` tests and production build pass after this change.

This closes the local Web Companion screen-set implementation slice, but does
not close authenticated browser QA, accessibility/localisation evidence,
cross-replica/deployed health proof, provider staging, or independent review.

### Notification settings and foreground delivery remediation — 2026-08-15

The previous Web Companion copy incorrectly stated that notification
preferences were unavailable in v1 after the authenticated preference/device
API had been implemented. The web API client now validates the preference and
device projections, the Web Companion exposes server-backed operational
preference toggles, and the infrastructure manifest requires
`NOTIFICATION_TOKEN_ENCRYPTION_KEY` plus its secret reference for
staging/production. The mobile app now subscribes to the adapter's foreground
message hook and renders only locally generated operational copy; tip, donor,
payment and alert payload data is not accepted or displayed.

Evidence: web test script added with 35/35 tests, web production build passes;
infra deployment-contract tests pass 9/9; Alerts API tests pass 62/62;
mobile Jest remains 52/52 with lint, TypeScript and dependency-hardening 2/2.
Native APNs/FCM provider delivery, background OS behavior, key rotation,
physical-device and store evidence remain open. Push remains best-effort and
is never the correctness path for payments, queues or alert delivery.
