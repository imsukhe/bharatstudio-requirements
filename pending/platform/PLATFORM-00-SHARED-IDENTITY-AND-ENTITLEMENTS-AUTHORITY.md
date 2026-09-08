# Platform 00 — Shared identity and mobile-store entitlement authority

**Decision status:** `Approved — implementation authorized by owner on 2026-08-28; verification remains required`
**Level:** L3
**Owner:** Project owner
**Date:** 2026-08-28
**Repository boundary:** `/Users/sukhdevsingh/Workspace/Bharat Studio/bharatstudio-platform/` (created for the approved local implementation on 2026-08-28)

## Source and why this slice is active

- Owner mission issued 2026-08-28: create the BharatStudio Platform as the sole owner of global identity and mobile-store entitlement truth.
- Product evidence, retained as evidence rather than copied authority:
  - `/Users/sukhdevsingh/Desktop/BharatStudio-Screen-Mirroring-Plan/153-Android-Live-Streaming-0-to-1-MASTER.md` — server-delivered packs require authenticated, short-lived delivery; local/free streaming must remain locally functional.
  - `/Users/sukhdevsingh/Desktop/BharatStudio-Screen-Mirroring-Plan/134-iOS-Live-Streaming-MASTER.md` — separate account, store, installation, and entitlement identities; server verification and signed capabilities are required for server-protected value.
- This is a new shared-platform boundary, not a change to Alerts, Android, or iOS. Existing Alerts launch authorities remain authoritative only for Alerts-owned behavior.

## Decision and non-negotiable scope

Platform owns one immutable `bharatstudio_user_id` per human account and is the only authoritative service for:

1. Apple, Google, and passkey authentication; explicit linking, unlinking, reauthentication, recovery, sessions/devices, and account lifecycle.
2. OAuth/OIDC-style short-lived access tokens, rotating refresh-token families with reuse detection, issuer/audience enforcement, global revocation, JWKS publishing, and signing-key rotation.
3. App Store and Google Play purchase verification; server notifications, refunds, revocations, voids, reconciliation, conflict handling, and an append-only normalized entitlement ledger.
4. Entitlement-gated pack authorization, short-lived signed broadcast capabilities, audit evidence, rate/abuse controls, observability, incident revocation, health, and readiness.

Locked product decisions:

- One BharatStudio account spans Android, iOS, web, and future products. Platform-specific accounts are prohibited.
- Free local streaming is account-free and must remain functional if Platform is unavailable. Platform is not in the free-stream start, encode, capture, RTMP, or broadcast transport path.
- Accounts are required only for server-delivered packs, cross-device restoration, and future cloud/relay value.
- Store storefront price is authoritative. The approved catalogue constants are ₹9/day, ₹19/week, ₹49/month, ₹139/3-month, ₹249/6-month, and ₹499/year. Clients display the store-provided localized price and must not calculate or enforce price from these constants.
- Deactivation is reversible. Deletion removes identity/profile/provider links, passkeys, credentials, sessions, tokens, stream keys, and user data. Only disclosed, necessary pseudonymous audit, fraud, and payment records may remain.
- Email equality is never an account-merge signal. A provider can link only after an explicit authenticated linking ceremony and fresh reauthentication for both the current session and provider assertion.
- Services validate Platform-issued access tokens locally through issuer, audience, expiry, signature, and JWKS rules. They never read Platform tables or use Platform database credentials.

Platform does **not** own RTMP/media/capture/encoding/relay/broadcast transport, Razorpay/UPI/tips/donor/payment events/Alerts queues or overlays, Alerts creator configuration, or any direct database access into Alerts, Android, or iOS.

## Service and deployment model

The approved-for-definition target is a new, isolated monorepo with a dedicated PostgreSQL 16 database and no shared schema/database role with Alerts. The service split adopts Alerts' proven operational conventions without coupling to Alerts:

| Service | Private/public boundary | Owns |
|---|---|---|
| `platform-api` | Public HTTPS REST/JSON; internal OIDC only for privileged operations | identity, sessions, JWKS, account lifecycle, entitlement reads, pack/capability authorization |
| `platform-store-ingress` | Store notification ingress only; provider signature/JWS verified before persistence | Apple ASSN V2 and Google RTDN ingestion, durable notification evidence |
| `platform-reconciler` | Private OIDC/scheduler/task ingress only | authoritative Store API lookups, repair and retry work |
| `platform-eraser` | Private OIDC/task ingress only | export production, deactivation/deletion workflow, cryptographic erasure, revocation propagation |

Each service is independently deployed to Cloud Run with a distinct service account, least-privilege database role, bounded database pool, structured redacted logs, `/healthz` and fail-closed `/readyz`. Cloud Tasks is an attempt/wake-up mechanism, not entitlement truth. Scheduler and task routes require exact OIDC audiences. Secrets, signing material, provider credentials, and HMAC keys are supplied through Secret Manager/KMS bindings only. Deployment manifests are release templates, not deployment evidence.

Public contracts are versioned HTTPS REST/JSON OpenAPI (`/v1`) plus versioned event schemas. All events include `schemaVersion`, `eventId`, `eventType`, `traceId`, `createdAt`, `producer`, and a typed payload. Additive changes require fixture compatibility checks; breaking changes require a new version and migration/deprecation decision.

## Exact security architecture

- `bharatstudio_user_id` is a server-generated UUIDv7, immutable, never recycled, and is the only cross-product subject identifier.
- Access tokens are asymmetric JWTs (`ES256`), 10-minute maximum lifetime, `iss`, exact `aud`, `sub`, `sid`, `jti`, `iat`, `nbf`, and `exp`; no email, provider subject, store token, or entitlement detail is embedded. Consumers cache JWKS only within a bounded TTL and retry on an unknown `kid` once before denial.
- Refresh tokens are opaque 256-bit random secrets, stored only as a keyed digest. They rotate on every successful use within a token family. Reuse of a rotated token revokes its entire family, records an audit event, and forces sign-in. Refresh expiry is 30 days idle / 90 days absolute; all values are server-side policy, not client claims.
- Browser sessions use secure, `HttpOnly`, `SameSite=Lax` refresh cookies with CSRF protection. Native apps store refresh tokens only in OS-protected credential storage. Access tokens are never put in URLs, logs, analytics, crash reports, or browser local storage.
- Passkeys use WebAuthn with a production RP ID/origin allowlist, challenge single-use/expiry, user-verification required for authentication and link/unlink/recovery, signature-counter handling, credential-ID uniqueness, and no attestation trust assertion beyond the approved verification policy.
- Apple/Google identity assertions are validated against issuer, client ID/audience, signature/JWKS, nonce, authorization code flow/PKCE where applicable, expiry, and replay state. Provider ID token email is optional profile data only; it cannot identify, merge, or link an account by itself.
- Unlink requires a recent reauthentication (maximum 10 minutes), leaves at least one usable sign-in/recovery method, and emits audit/revocation events. Recovery never reveals whether an email/provider account exists and is support-mediated when no verified method remains.
- Signing keys and keyed-HMAC keys reside in KMS/HSM. A JWK has `kid`, algorithm, created/activate/retire times, and status. New keys overlap published JWKS before activation; verification keys remain published until every maximum token/capability lifetime has elapsed. Private keys never leave KMS/HSM.
- Protected-pack download grants are one-time, audience- and artifact-scoped signed URLs with a 5-minute maximum lifetime. Broadcast capabilities are asymmetric signed JWTs with a 15-minute maximum lifetime, exact service audience, `sub`, device/session binding, entitlement-ledger version, `jti`, and no personal data. A consumer denies stale, revoked, wrongly-scoped, or unknown-key capabilities.
- Abuse controls apply per IP/device/session/provider subject and endpoint, with a privacy-preserving keyed network prefix digest where justified. Provider notification deduplication uses the provider's verified stable delivery identity; timestamps/random values are never substituted.

## Data model and retention

All timestamps are UTC. Append-only facts are corrected by linked compensating entries, never by mutation/deletion. Raw provider tokens, raw receipts, and identity assertions are not logged.

| Area | Minimum records and rule |
|---|---|
| Identity | `users` (`bharatstudio_user_id`, lifecycle state, created/deactivated/deleted timestamps); `user_profiles` holds only optional display data. No email uniqueness constraint exists. |
| Provider identities | `provider_identities` holds provider, issuer, opaque subject, encrypted optional email, link state, and timestamps; unique `(provider, issuer, subject)` while active. `identity_link_challenges` records short-lived explicit linking/re-auth state. |
| Passkeys/recovery | `webauthn_credentials` holds credential ID, public key, RP ID, sign counter, transports, and lifecycle; `recovery_methods` holds only verifiable recovery state. Neither holds a passkey private key. |
| Sessions/devices | `sessions`, `refresh_token_families`, `refresh_tokens`, `devices`, and `revocation_events`; token values are absent, keyed digests only. |
| Store truth | `store_notifications` (raw payload encrypted only for bounded reconciliation retention, signature-verification result and digest); `store_transactions`/`store_purchase_bindings` store provider stable IDs, encrypted current verification material where necessary, environment, account binding, and conflict state. |
| Entitlements | `entitlement_ledger` is append-only: grant, renewal, expiration, refund, revoke, void, restore, correction, and reconciliation events link to their store fact. `entitlement_snapshots` is a rebuildable read model with monotonic version. |
| Assets/capabilities | `pack_catalogue`, immutable `pack_artifacts`, `pack_grants`, `broadcast_capabilities`, and `capability_revocations`; revocation is an append-only event plus cache-safe projection. |
| Audit/operations | Append-only `audit_events`, `security_events`, `reconciliation_runs`, `deletion_requests`, `export_jobs`, `outbox_events`, and processing-attempt records. |
| Tombstones | `identity_tombstones` and `purchase_tombstones` contain purpose-separated HMAC-SHA-256 digests and key version only: e.g. `HMAC(K_identity_vN, canonical(provider, issuer, subject))` and `HMAC(K_purchase_vN, store, original_purchase_id)`. They contain no raw email, provider subject, credential, receipt, or purchase token. They prevent unsafe reassociation/replay after deletion and enable bounded fraud/payment retention. |

Retention defaults require legal/privacy approval before enforcement: authentication security/audit events 180 days, encrypted raw notification material 30 days after verified normalization, reconciliation evidence 7 years only where a finance/legal basis is documented, deletion/export job metadata 90 days, revoked-token/capability identifiers through their maximum expiry plus 30 days, and tombstones only for their documented fraud/payment purpose with an annually reviewed maximum. Data export is structured and authenticated; deletion first revokes access then asynchronously erases user-held data and cryptographic key references, while retaining only the approved pseudonymous records above.

## Purchase binding, conflicts, and entitlement rules

The account binding key is the provider's stable purchase root (Apple original transaction ID; Google purchase-token lineage/order identity as documented by Google), never email or a client-declared user ID. A verified purchase root may bind to exactly one active `bharatstudio_user_id`.

- The first verified authenticated claim creates the binding and ledger fact atomically.
- A claim for an existing binding by another account returns a non-enumerating `purchase_account_conflict` response, creates a security/audit record, and does not merge, transfer, or disclose the bound account.
- Resolution requires authenticated support recovery and fresh proof from the relevant store/provider; it is a reviewed compensating binding event, not an overwrite. Deactivation alone does not silently free a purchase. After deletion, tombstone policy determines whether a reviewed restoration is permitted.
- Apple App Store Server API/JWS and Google Play Developer API verification are server-to-server authoritative. A client receipt/JWS/token is untrusted input until signature/API verification succeeds.
- Store notifications are verified, deduplicated, persisted before projection, processed idempotently, and reconciled against provider APIs. Delayed, malformed, unknown, or contradictory events enter a durable quarantine/manual-review state; they must not fabricate an entitlement or erase prior payment evidence.
- Refund/revoke/void events create linked negative ledger facts, advance entitlement snapshot version, publish revocation events, and prevent issuance of new protected grants/capabilities. No client-provided premium boolean or expiry is trusted.

## Migration, testing, rollback, and operations plan

WP-0 through WP-6 are sequential gates. Every package requires implementation, automated tests, self-review, an independent fresh review when available, reproducible redacted evidence, and this ledger update before the next package starts.

| WP | Scope | Entry/exit gate | Status |
|---|---|---|---|
| WP-0 | Governance, threat model, architecture, contracts/migration decisions | This authority/task/test/review accepted; owner approves implementation scope | `Approved — implementation started` |
| WP-1 | OpenAPI/event contracts and verified generated fixtures | Contract compatibility and negative fixtures pass | `Implemented locally — self-review and external compatibility evidence pending` |
| WP-2 | Identity/providers/passkeys/linking/sessions/JWKS | Token replay, session revocation, key rotation, auth-flow tests pass | `Implemented locally — provider/device integration and independent review pending` |
| WP-3 | Deactivate/delete/export/audit/revocation propagation | Deletion/recovery and audit evidence pass | `Implemented locally — database/consumer propagation and independent review pending` |
| WP-4 | Stores/ledger/notifications/reconciliation | Sandbox purchase/refund/revoke/conflict evidence pass | `Implemented locally — real Apple/Google sandbox/reconciliation evidence pending` |
| WP-5 | Packs/capabilities/abuse/observability/deployment | Outage, authorization, readiness, and operational drills pass | `Implemented locally — distributed controls and staging operations pending` |
| WP-6 | Deterministic integration, staging rehearsal, hostile audit | Staging/provider/migration/rollback evidence and independent audit pass | `Local deterministic evidence complete — blocked on external staging/provider evidence and independent hostile audit` |

Migrations are forward-only, checksum-verified, individually reviewed, and run first against disposable PostgreSQL 16. `0001` creates the clean Platform baseline and database roles; later migrations are ordered and reversible only through new compensating migrations. No shared, staging, or production database is created, altered, or migrated in this definition pass. Alerts/Android/iOS data is integrated only via versioned APIs/events; no cross-database migration exists.

Deployment rollback uses immutable image digests, backward-compatible API/event rollout, dual-published JWKS during key rotation, feature flags that deny new protected grants while preserving free streaming, DLQ/quarantine replay through idempotent state machines, and forward corrective migrations. Rollback never deletes ledger facts or reuses revoked signing/HMAC keys. A failed Platform deployment must leave the mobile free-stream path operational; protected operations fail closed with actionable retry states.

## External prerequisites and non-claims

Before any provider/staging claim, obtain and record redacted evidence for: Apple Developer/App Store Connect account, bundle IDs, App Store Server API key/issuer/key ID, signed-notification endpoint, sandbox tester and notification delivery; Google Cloud OAuth client IDs/verified redirect origins, Play Console service account, Android package/signing registration, Play test track, RTDN Pub/Sub subscription and Play API access; production WebAuthn RP domains/origins; GCP project/region/DNS, Cloud Run service accounts/IAM, Secret Manager/KMS keys, dedicated PostgreSQL capacity/backups, WAF/rate-limit policy, monitoring/alert routing; product/privacy/retention/export/deletion notices and legal review; store product configuration for the exact catalogue.

This definition does not claim provider approval, App Review/Play approval, sandbox/staging operation, real migration, legal approval, production readiness, security certification, or independent review.

## Evidence ledger

### WP-1 — 2026-08-28

- Implemented versioned `/v1` OpenAPI inventory, versioned event-envelope schema, entitlement-change fixture, and redacted conflict fixture in the new Platform repository.
- Added clean dedicated PostgreSQL 16 baseline migration with separate identity/session/store/ledger/capability/audit/tombstone records; no migration was applied to any database.
- Local command: `go test ./...` from `bharatstudio-platform` passed. The test validates fixture JSON, the versioned contract surface, required JWKS/store paths, and absence of an RTMP/free-stream transport API.
- Self-review finding: the OpenAPI document is intentionally an inventory, not provider-generated protocol compatibility proof. Apple/Google/WebAuthn interoperability remains WP-2/WP-4 staging/provider evidence.

### WP-2 — 2026-08-28

- Implemented ES256 10-minute access tokens, local JWKS with overlap/activation/retirement behavior, and token validation of issuer, audience, expiry, `sub`, `sid`, and `jti`.
- Implemented opaque 256-bit refresh tokens with 30-day idle/90-day absolute policy, single-use rotation, entire-family reuse detection/revocation, session/device listing and global subject revocation.
- Implemented explicit provider identity creation/linking/unlinking with fresh-auth gating, no email input or equality merge path, final-method protection, and a standard-library RS256 OIDC assertion-verification boundary.
- Implemented single-use five-minute passkey challenge state, verified-user-presence requirement, credential ownership, and counter-regression protection behind a mandatory cryptographic verification interface.
- Local command: `gofmt -w internal && go test ./...` passed. No Apple/Google JWKS endpoint, WebAuthn ceremony, mobile keychain, or production key has been contacted.

### WP-3 — 2026-08-28

- Implemented reversible deactivation, recent-auth reactivation, authenticated export jobs, deletion requests, erasure of in-memory provider/passkey state, global session/refresh revocation, audit events, revocation outbox events, and purpose-separated HMAC tombstones.
- Local test proves revoked sessions/tokens cannot rotate, deletion removes identity fields, and deletion retains only a pseudonymous tombstone/audit trail.

### WP-4 — 2026-08-28

- Implemented a store-verifier boundary, HMAC-digested stable purchase roots, one-active-account binding, non-enumerating account conflict, append-only grant/refund/revoke/correction ledger facts, rebuildable entitlement snapshots, verified-notification deduplication, quarantine, and reconciliation correction.
- Local tests prove purchase conflict, duplicate delivery suppression, refund projection removal with preserved ledger history, and quarantine of an unbound notification. Apple ASSN V2, App Store Server API, Google RTDN, Play Developer API, and store sandbox behavior remain unverified external gates.

### WP-5 — 2026-08-28

- Implemented five-minute, account/pack-scoped one-time protected-pack grants and ES256 15-minute audience/session/device/entitlement-version-bound broadcast capabilities; tests prove cross-account/replay denial and non-entitled denial.
- Implemented bounded local rate limiter, no-secret JWKS, liveness/readiness routes, a production fail-closed local bootstrap, non-root distroless container build, and separate service/task deployment templates. Distributed WAF, KMS/HSM, Cloud Run/IAM, metrics backend, and incident exercise remain external operational gates.
- Local commands passed: `go test ./...`, `go vet ./...`, `go build ./cmd/platform-api`, and `docker build --file Dockerfile --tag bharatstudio-platform:local .`.

### WP-6 — 2026-08-28

- Local deterministic hostile-flow test passed: provider identity sign-in, refresh replay revocation, verified purchase binding/conflict, protected-grant replay denial, capability issuance, and deletion/tombstone/session-revocation path.
- A disposable local `postgres:16-alpine` container applied `0001_platform_baseline.sql` successfully with `ON_ERROR_STOP=1`; 24 public tables were created. The container was stopped and removed after the check.
- `go test ./... -count=1` passed for all local packages. This is not a staging rehearsal, provider/store sandbox run, independent hostile audit, or production approval.

### Security-audit remediation — 2026-08-28

- Fixed deleted-account reactivation, HMAC-keyed refresh-token digests, token/capability maximum lifetime checks, active-session token verification, RP/origin-bound passkey registration/assertion checks, issuer-bound OIDC key resolution, entitlement-expiry authorization, transaction idempotency, and notification-verifier-only ingress.
- Replaced protected artifact references returned to callers with five-minute signer-issued download URLs, and wired lifecycle deactivation/deletion to capability revocation/version/session checks.
- Added authenticated HTTP handlers for session, entitlement, lifecycle, pack, capability, and internal-store paths; unconfigured provider/KMS/database paths fail closed.
- Added migration `0002_platform_rls_and_erasure.sql`: least-privilege roles, tenant RLS policies, and a security-definer erasure procedure. A disposable PostgreSQL 16 run proved that a deletion-pending account transitions to `deleted` and profile/provider rows are removed.
- Local remediation commands passed: `go test ./... -count=1`, `go test -race ./... -count=1`, `go vet ./...`, clean PostgreSQL 16 migrations `0001` + `0002`, and `docker build --tag bharatstudio-platform:fix-audit`.

### Follow-up local remediation — 2026-08-28

- Pack authorization now issues an opaque five-minute grant only. The signed download URL is minted after authenticated, single-use redemption; no URL is exposed on the authorization response.
- Broadcast-capability minting derives the session/device pair from the verified bearer-token session rather than request JSON. Verification accepts an active exact session/subject/device binding.
- `gofmt`, `go test -race ./... -count=1`, `go vet ./...`, and `docker build --file Dockerfile --tag bharatstudio-platform:local-remediation .` passed. The evidence does not close durable persistence, distributed revocation, provider/store sandbox, staging, or production gates.

### Repair-and-reaudit loop — 2026-08-28

- Added a subject-checked PostgreSQL security-definer audit/outbox append function and proved it under the `bsp_platform_api` role from a clean database. Direct API-table writes remain ungranted.
- Added forward erasure cleanup for identity-linked auth challenges and entitlement snapshots; it removes capability subject references and tombstones active purchase bindings. Clean PostgreSQL proof used synthetic rows only.
- Logout now revokes the current refresh family; refresh-family identity cannot be rebound across subject/session; API errors emit a UUID trace ID. Local race tests, vet, and container build passed.

### Deployment-command remediation — 2026-08-28

- Added separate Platform worker commands and Docker build targets for store ingress, reconciliation, and erasure; each has a database-backed readiness gate and its template now receives a role-scoped database secret.
- All four local command targets build. This closes the missing-image artifact defect only; it does not claim durable task processing, provider integration, or staging operation.

### Runtime persistence precondition — 2026-08-28

- Corrected malformed session/token UUID generation before durable persistence wiring. Regression evidence confirms RFC 4122 v4 values acceptable to the PostgreSQL schema.

### Durable refresh and contract work — 2026-08-28

- Added atomic PostgreSQL refresh issue/rotation/reuse and revocation procedures with clean-database replay/revocation evidence. The auth backend and refresh API route use this durable boundary when configured.
- Added deterministic server-verifier-only purchase route coverage and claim-bound access-token session validation. Durable identity, session, ledger, pack, and lifecycle runtime wiring remain open implementation work.

### Durable identity and store claim work — 2026-08-28

- Added RLS-safe user/provider creation, linking, keyed pre-auth lookup, unlinking, and constrained lifecycle database executors with clean synthetic PostgreSQL proof.
- Added atomic database-backed product-catalogue purchase claims with stable binding, idempotency, append-only ledger fact, and versioned snapshot. Runtime integration remains in progress.

### Durable API session and entitlement wiring — 2026-08-28

- A database-configured API now selects durable session, refresh, purchase-claim, and entitlement-snapshot authorities. It fails closed on durable session failure rather than using a per-process fallback. Protected pack/capability reads use the durable snapshot through the existing manager boundary.
- Added the forward-only `0010_entitlement_snapshot_executor.sql` projection; direct API access to entitlement snapshots remains denied. A fresh synthetic PostgreSQL 16 run applied `0001`–`0010`; `go test -race ./...`, `go vet ./...`, and whitespace validation passed.
- This does not close the program: identity/lifecycle persistence, notification/reconciliation/erasure workers, KMS signer, concrete Apple/Google/WebAuthn adapters, deployment IAM, provider sandboxes, staging outage/migration/rollback drills, and an independent hostile audit remain required gates.

### Durable provider-identity runtime wiring — 2026-08-28

- A database-configured API selects a durable identity service. Provider subjects are persisted only as AES-GCM ciphertext and a distinct keyed digest; provider sign-in is an atomic digest-locked create-or-return operation, never an email merge. State reads/transitions and final-method unlink protection are durable.
- Forward migration `0011_durable_identity_runtime.sql` applied cleanly after `0001`–`0010`; local race tests and vet passed. It is still not evidence of Apple/Google live issuer integration, a WebAuthn ceremony, KMS-backed key retrieval, lifecycle completion, or a deployable production environment.

### Durable lifecycle and erasure task wiring — 2026-08-28

- `0012_durable_lifecycle_and_erasure.sql` adds atomic account lifecycle transitions, durable export/deletion job rows, audit/outbox facts, session/refresh revocation, and an eraser-only executor. The configured API selects this lifecycle backend; the eraser command implements strict deletion-task delivery with a configured tombstone key version.
- A clean synthetic role-separated PostgreSQL 16 proof performed provider sign-in, deactivation/reactivation, deletion request, and eraser completion. The result was `deleted`, one versioned provider-digest tombstone, and zero sessions. Tests/race/vet pass. Cloud Run task IAM/OIDC, real export object delivery, provider/staging deletion, backup/rollback, and KMS remain external gates.

### Durable verified store-notification ingestion — 2026-08-28

- `0013_durable_store_notification_ingress.sql` permits only the store role to record a cryptographically verified delivery fact. It uses provider delivery ID idempotency, quarantines unbound roots, appends ledger history, and updates versioned entitlement projections atomically.
- The clean synthetic API/store role proof claimed a configured product then processed a refund: snapshot version moved `1`→`2`, active products became empty, and both grant/refund facts remained. Apple ASSN V2 / Google RTDN verification, provider API reconciliation, actual worker IAM, and sandbox notification replay/order evidence remain explicit external prerequisites.

### Durable protected-pack grants — 2026-08-28

- `0014_durable_pack_grants.sql` moves opaque grant state out of API maps. It persists a keyed digest only, verifies the durable entitlement snapshot/catalogue, and atomically consumes exactly once before exposing an artifact reference to the signer boundary.
- A clean synthetic database proof created a catalogued entitlement, authorized a grant, redeemed it once, and retained one consumed digest row. KMS-backed object URL signing, catalogue deployment seed, cross-replica replay/revocation, and staging evidence remain explicit gates.

### Durable passkey state and versioned routes — 2026-08-28

- `0015_durable_passkeys.sql` owns challenge replay prevention, keyed credential lookup, account/RP binding, revocation, and monotonic counter state. The clean synthetic proof registered a credential and finished a bound assertion with counter `3` and two consumed challenges.
- The passkey options/verify API routes accept adapter results only and create a normal Platform session after verified account lookup. Concrete WebAuthn parser/attestation integration, live RP/origin values, device ceremony, and staging proof remain external prerequisites; client-selected account identity is never accepted.

### Native Apple/Google OIDC state and JWKS wiring — 2026-08-28

- `0016_durable_oidc_challenges.sql` persists only HMAC digests of state/nonce and consumes both exactly once. Configured runtime wires Google/Apple OIDC client IDs through an explicit HTTPS JWKS resolver and verifies provider token issuer/audience/nonce before identity/session creation.
- Synthetic signed-token replay tests and a clean API-role challenge proof pass. Production client registration, Apple/Google sandbox/device callbacks, issuer/JWKS rollover, and staging evidence remain external prerequisites; no provider success is claimed without them.

### Durable reconciliation corrections — 2026-08-28

- `0017_durable_reconciliation.sql` gives the dedicated reconciler role a locked purchase-root correction path. It determines ownership internally, appends a ledger correction/revoke, and advances the projection; it never overwrites prior facts.
- A clean API/reconciler role proof claimed an entitlement then reconciled it inactive, producing `corrected`, version `2`, no active products, and retained grant/revoke history. Concrete provider-query credentials, scheduler/task IAM, and sandbox reconciliation proof remain external prerequisites.

### Fresh reauthentication recovery and unlink guard — 2026-08-28

- `0018_durable_reauth_and_unlink_guard.sql` enforces final-method protection for identity-ID unlink. Configured runtime recognizes a fresh verified session (five minutes) for sensitive linked-session actions and provides a verifier-bound reactivation callback for deactivated accounts, which cannot otherwise have an active session.
- The regression proves the recovery callback transitions only a verified deactivated account back to active. Live device/provider reauth assurance, complete linked-provider ceremony, and staging unlink/deletion evidence remain external prerequisites.

### Restart-stable JWT and JWKS hardening — 2026-09-08

- A database-configured API now rejects ephemeral signing keys and requires a validated Secret-Manager supplied `PLATFORM_JWT_KEYRING_JSON`. The key ring has exactly one active P-256 PKCS#8 signing key and may retain P-256 public-only published keys for token-verification overlap and JWKS publication across a controlled staging restart.
- The HTTP JWKS resolver now rejects a key explicitly declared for encryption (`use: enc`); only an omitted use or `use: sig` may be used for RS256 identity-token verification. A TLS-backed resolver regression verifies the encryption-key rejection.
- `go test ./...`, `go vet ./...`, and `go test -race ./...` passed locally. This is synthetic implementation evidence only. KMS/HSM signing, secret rotation, deployed JWKS cache behavior, and real provider/staging key-rotation evidence remain release gates.

### Durable protected-operation revocation — 2026-09-08

- Forward migration `0019_durable_capability_subject_revocation.sql` persists a per-account revocation cutoff and revokes all outstanding one-time pack grants in the same lifecycle transaction as deactivation or deletion-pending transition. A capability issued at or before that cutoff now fails closed after API restart/replica change; a later reactivated session can receive a newly issued capability.
- Configured pack/capability verification consults this durable cutoff instead of its process-local subject-revocation map. Session revocation and entitlement-version checks remain independent defenses.
- Local race/vet tests and clean PostgreSQL 16 proof (`tests/sql/durable_capability_revocation.sql`) pass with only synthetic values. Consumer-side revocation-event propagation, Cloud Run/IAM, and staging outage/revocation rehearsal remain external gates.
- Forward migration `0020_erase_capability_subject_revocations.sql` corrects retention: actual deletion removes the direct account-linked capability cutoff after session revocation and erasure, while the justified provider HMAC tombstone remains. The clean eraser proof reports zero retained capability-subject revocation rows.

### Contract fixture hardening — 2026-09-08

- The versioned OpenAPI contract now defines reusable `Session`, `EntitlementProjection`, `JobAccepted`, and one-time `PackGrant` response shapes. A deterministic negative event fixture proves an unknown `schemaVersion` is not accepted as v1.
- Focused contract tests, full `go test ./...`, and `go vet ./...` pass. This validates checked-in contract shape only; consumer compatibility and deployed contract evidence remain pending.

### Private worker OIDC enforcement — 2026-09-08

- The eraser private task route now requires a Google-signed RS256 service OIDC bearer token whose issuer and exact audience match the configured private service audience. It resolves signing keys only from configured HTTPS Google JWKS endpoints; Cloud Run IAM remains a separate perimeter control.
- Synthetic signature/audience and unauthorized-handler regressions pass. This is not deployed Cloud Run/Cloud Tasks IAM evidence; the real service account, audience, token delivery, and staging replay evidence remain required.

### Discoverable WebAuthn assertion wiring — 2026-09-08

- Migrations `0021`–`0022` add keyed credential verifier lookup and unbound discoverable login challenge/atomic completion. Raw credential IDs remain absent from persistence; HMAC lookup occurs before COSE public-key verification.
- Configured API now returns standards-library discoverable assertion options and accepts only a challenge plus raw assertion/device ID. The verified credential selects the account; the SQL executor consumes the challenge and advances the counter atomically.
- Clean PostgreSQL migration `0001`–`0022`, full tests, vet, and race tests pass. Passkey registration/link ceremony and live device/RP configuration evidence remain active work/gates.

### WebAuthn registration/link ceremony wiring — 2026-09-08

- The configured API now exposes authenticated, recent-verified-session registration options and verification routes. Registration options use the immutable Platform subject only as the opaque WebAuthn user handle; the server persists the exact library-generated challenge under that already authenticated subject. The completion request cannot nominate an account.
- The WebAuthn adapter uses the maintained library's registration verifier with required user verification, configured RP ID/origin allowlist, challenge binding, and COSE public-key extraction. The existing PostgreSQL executor atomically consumes the account-bound challenge and stores only the keyed credential identifier and public key.
- Deterministic synthetic `none`-attestation coverage proves valid registration verification and challenge mismatch rejection. HTTP coverage proves no session, no recent verified session, or client-selected account can register a credential. `tests/run-local-verification.sh` passed on 2026-09-08: Go tests/vet/race, four local command-image builds, and all clean PostgreSQL 16 durable SQL proofs through `0022`.
- This is local synthetic evidence only. Production RP domain/origin configuration, real device ceremony, provider/store sandboxes, Cloud Run/IAM, migration upgrade/rollback, outage, and independent hostile-audit evidence remain mandatory release gates.

### Durable export-delivery boundary — 2026-09-08

- Migrations `0023–0024` add a role-scoped, retry-safe export claim/release/complete state machine. Only an HMAC digest of an opaque delivery reference and its maximum 24-hour expiry are persisted; no export payload or delivery URL is written to Platform tables, logs, or contracts.
- A private OIDC-protected export task handler and local processor require a durable claim, an encrypted-delivery sink, a short-lived delivery result, and atomic completion. Delivery errors release the job for retry and never report completion. The route remains unmounted until a deployment supplies a real encrypted sink.
- Actual deletion removes account-linked export jobs and delivery-reference digests before state becomes `deleted`, invalidating any outstanding export artifact. Local synthetic lifecycle/worker regressions and the clean PostgreSQL proof pass. Object storage, delivery notification, Cloud Run task identity, and staging deletion/export evidence remain external gates.

### Explicit store-provider normalization boundaries — 2026-09-08

- Apple ASSN V2 ingress now has an explicit adapter contract that accepts only a cryptographically validated, normalized App Store delivery: stable delivery ID, purchase root, product ID, and known ledger event kind. It rejects cross-store, incomplete, or unknown facts before the durable ledger boundary.
- Google reconciliation now has an explicit authority contract requiring a Google Play Developer API-verified purchase fact and current active state. A decoded RTDN by itself cannot create or correct an entitlement.
- Existing private store/reconciler handlers accept those typed adapters and continue to fail closed when no real Apple JWS/Google Play authority is configured. Live provider credentials, cryptographic key/certificate verification, API calls, scheduling, and sandbox evidence remain external gates.

### Documentation and local-evidence reconciliation — 2026-09-08

- The Platform repository exists and contains the approved local implementation. The earlier “does not yet exist” wording was an obsolete definition-time statement and has been corrected without changing any ownership, security, retention, or external-release decision.
- The deterministic local gate was re-run against the current tree: unit, vet, race, four command-image builds, and every clean PostgreSQL 16 migration/role proof passed through `0024`. `git diff --check` found no remaining whitespace errors after the baseline-migration correction.
- A link and structured-document audit resolved all 121 in-scope Markdown links and parsed all checked-in JSON/YAML contracts/templates. This is self-review/evidence hygiene only; independent review, consumer integration, provider, staging, and production gates remain open.

### Deployment-template regression guard — 2026-09-08

- Added an in-repository Go contract test that parses all four Cloud Run templates and the Cloud Tasks template on every normal `go test ./...` run. It requires distinct expected service identities, one container and service account per service, no duplicate environment-variable name, an explicit Secret-Manager database-url entry, production mode, and HTTPS private audiences for the two private task services.
- The guard found and drove correction of unquoted private-audience URL scalars in the reconciler and eraser templates. The complete deterministic runner then passed: unit, vet, race, four image builds, and all disposable PostgreSQL 16 proofs through `0024`; `git diff --check` passed. This validates checked-in templates only, not Cloud Run/Cloud Tasks/IAM deployment behavior.
