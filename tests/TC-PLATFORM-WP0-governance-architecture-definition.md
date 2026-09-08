# TC-PLATFORM-WP0 — Governance, architecture, and approval acceptance record

**Task:** [`../tasks/PLATFORM-WP0-governance-architecture-definition.md`](../tasks/PLATFORM-WP0-governance-architecture-definition.md)
**Status:** `Approved — document gate passed; owner approval recorded 2026-08-28`
**Owning repository:** `bharatstudio-requirements`
**Test data:** No personal, payment, provider, or production data. This package is documentation-only.

| ID | Setup/action | Expected result | Failure/retry and evidence | Cleanup/rollback |
|---|---|---|---|---|
| WP0-01 | Read canonical governance, workspace, requirements instructions, and current authority before changes. | L3 classification and explicit approval boundary are recorded. | Missing/conflicting instruction blocks the task; evidence is the linked records. | Supersede/archive only; no runtime state. |
| WP0-02 | Compare ownership against owner mission and Alerts deployment model. | Platform owns global identity/store truth only; no Alerts/Android/iOS modification or direct DB coupling appears. | Any cross-boundary table/client dependency is rejected before code. | Remove/replace proposed boundary in a new approved authority. |
| WP0-03 | Inspect identity and entitlement design. | Immutable UUIDv7 user ID; no email merge; explicit reauth linking; rotating refresh reuse detection; JWKS/key rotation are specified. | Any missing security control blocks WP-1. Evidence is the authority's exact-security section. | Amend before approval. |
| WP0-04 | Inspect data/privacy/deletion design. | Purpose/minimisation/access/retention/erasure/audit rules and keyed-HMAC tombstones are defined; raw secrets/receipts are excluded from logs. | Unjustified personal-data retention or raw identifier tombstone blocks approval. | Amend before approval. |
| WP0-05 | Inspect store-entitlement design. | Verified provider facts, append-only ledger, conflict quarantine/manual resolution, refund/revoke/void reconciliation, and no client entitlement authority are defined. | Any automatic account merge, timestamp dedup key, or destructive ledger edit blocks approval. | Amend before approval. |
| WP0-06 | Inspect availability and protected-authorisation behavior. | Free streaming has no Platform dependency; protected packs/capabilities fail closed, are short-lived/scoped, and use revocation. | Any mandatory Platform call in a free-stream start blocks approval. | Amend before approval. |
| WP0-07 | Inspect migration/deployment/rollback plan. | Dedicated database, forward-only disposable-first migrations, least-privilege Cloud Run/OIDC pattern, key overlap, immutable image rollback, and no provider provisioning are specified. | Missing rollback or a shared production migration blocks approval. | Amend before approval. |
| WP0-08 | Inspect planned evidence gates. | WP-1–WP-6 include contract, token replay, key rotation, deletion, store sandbox, conflict, refund/revoke, outage, migration, staging, hostile audit, and rollback evidence. | Production-readiness language without those artifacts is rejected. | Keep status proposed until evidence exists. |
| WP0-09 | Owner reviews the authority, task, test, and review records as one decision. | Explicit approval covers scope, acceptance, affected files, data/security/privacy impact, migration/test/rollback, deployment, and prerequisites. | Owner approved the complete program in the 2026-08-28 interactive instruction. | Proceed to WP-1. |

## Future executable evidence gates

WP-1 generates and validates OpenAPI/event fixtures, including malformed/unknown-version negatives. WP-2 proves authentication, token rotation/reuse detection, revocation, JWKS and key overlap/retirement. WP-3 proves deactivation, export, deletion, tombstone and outbox propagation. WP-4 proves Apple/Google sandbox purchase, restore, notification replay/reorder, conflict, refund/revoke/void, reconciliation, and corrective ledger events. WP-5 proves pack/capability authorization, token leakage negatives, rate limits, health/readiness, alerting, and free-stream outage isolation. WP-6 runs disposable clean/upgrade migrations, staged deployments, provider rehearsals, replay/rollback drills, and hostile independent review with redacted reproducible evidence.

### WP-1 local evidence — 2026-08-28

`go test ./...` passed for contract fixture/version checks. This is deterministic local evidence only; no live contract consumer, database migration, provider, staging, or independent review occurred.

### WP-2 through WP-6 local evidence — 2026-08-28

- `gofmt -w cmd internal tests`, `go test ./... -count=1`, `go vet ./...`, and `go build ./cmd/platform-api` passed.
- `docker build --file Dockerfile --tag bharatstudio-platform:local .` passed; the image is local-only and production bootstrap intentionally fails closed until KMS/HSM/database adapters are configured.
- A disposable `postgres:16-alpine` container applied the full clean baseline successfully using `psql -v ON_ERROR_STOP=1`; it created 24 tables and was removed immediately after.
- The deterministic integration test covers sign-in/no-email-merge, refresh reuse detection, purchase conflict, protected pack one-time redemption, capability scope, deletion, revocation, and tombstone retention.
- Open gates: real Apple/Google provider and store sandbox flows, RTDN/ASSN delivery/reorder, deployment IAM/secrets/KMS, migration upgrade rehearsal, free-stream mobile outage proof, rollback deployment proof, legal retention evidence, and an independent hostile audit.

### Audit-remediation evidence — 2026-08-28

- Regression suite includes deleted-account reactivation denial, active-session access-token verification, issuer/audience/nonce-bound OIDC verification, passkey registration/origin enforcement, expiry-aware store authorization, duplicate purchase idempotency, retryable notification quarantine, signed grant replay denial, and lifecycle capability revocation.
- Migrations `0001` and `0002` applied in order to disposable PostgreSQL 16. The erasure procedure removed synthetic profile/provider records and marked the user deleted.

### Follow-up authorization-boundary remediation — 2026-08-28

- Corrected protected-pack delivery so `/v1/packs/{packId}/authorize` returns only a five-minute opaque grant. The signed artifact URL is minted only by the authenticated `/v1/packs/grants/redeem` operation after atomic one-time consumption; cross-subject and replay redemption tests pass.
- Corrected broadcast-capability binding so the handler derives the session and device exclusively from the verified bearer-token session. It no longer accepts caller-selected session/device identifiers; session verification now requires the exact session/subject/device tuple.
- `gofmt`, `go test -race ./... -count=1`, `go vet ./...`, and `docker build --file Dockerfile --tag bharatstudio-platform:local-remediation .` passed. This is local evidence only. Durable repository wiring, distributed revocation, store/provider integrations, and staging evidence remain open gates.

### Repair-and-reaudit loop — 2026-08-28

- `0003_audit_outbox_executor.sql` replaces direct API-table writes with a subject-checked security-definer append boundary. A clean PostgreSQL 16 run as `bsp_platform_api` successfully appended exactly one synthetic audit/outbox pair; the prior direct-table permission denial is no longer relied on.
- `0004_erasure_operational_cleanup.sql` deletes identity-linked challenges and entitlement projections, nulls the capability-revocation subject, and tombstones active purchase bindings before the account becomes deleted. A clean PostgreSQL 16 run proved the deleted state with zero synthetic challenge/snapshot records and zero linked capability revocations.
- Logout now revokes the verified current session and its refresh family; refresh-family identifiers cannot be rebound to a different subject/session; error responses include a correlated UUID trace ID. `go test -race ./... -count=1`, `go vet ./...`, and the local container build passed.

### Deployment-command remediation — 2026-08-28

- Added distinct `platform-store-ingress`, `platform-reconciler`, and `platform-eraser` commands with a database-backed health/readiness bootstrap. The deployment templates now provide a role-scoped database secret for each private worker.
- Dockerfile command selection was tested by building all four synthetic local images: `platform-api`, `platform-store-ingress`, `platform-reconciler`, and `platform-eraser`. `go test ./... -count=1` and `go vet ./...` also passed. Worker task handlers and API durable-service wiring remain in progress and are not claimed by this evidence.

### Runtime persistence precondition — 2026-08-28

- Corrected generated session/token IDs to RFC 4122 v4 UUID format. The prior formatter produced values PostgreSQL UUID columns could not accept. The new auth regression test and `go vet ./...` pass.

### Durable-session implementation in progress — 2026-08-28

- Added PostgreSQL session create/list/active/revoke repository operations and forward migration `0005` granting only transaction-subject-scoped session writes to the API role. A clean PostgreSQL 16 run as `bsp_platform_api` proved synthetic insert, revoke, and read operations under RLS.
- This evidence covers the repository boundary and policy only. API runtime wiring and durable refresh/identity/store/lifecycle state remain in progress.

### Durable refresh and contract work — 2026-08-28

- Migrations `0006` and `0007` add atomic opaque-refresh issuance/rotation/reuse detection and durable session/subject revocation. Clean PostgreSQL 16 evidence proved `ok` on rotation, `reuse` on replay, and `invalid` after session revocation.
- The auth service supports the durable refresh backend, and `/v1/sessions/refresh` rotates it before minting an access token. The purchase-verification contract handler accepts server-verifier output only and covers verified/unverified deterministic cases.
- Access-token activity checks now receive signed claims and validate the `sid`/`sub` relationship. `go test -race ./... -count=1` and `go vet ./...` passed.

### Durable identity and store claim work — 2026-08-28

- `0008_identity_executor.sql` adds RLS-safe security-definer create, link, keyed pre-auth lookup, lifecycle transition, and unlink operations. Clean PostgreSQL evidence created, linked, and resolved synthetic identity material under the API role.
- `0009_store_claim_executor.sql` adds a deployment-owned product catalogue and atomic purchase-root binding/transaction/idempotency/ledger/snapshot claim. Clean PostgreSQL evidence returned `ok` and entitlement version `1` for a synthetic verified purchase.

### Durable API session and entitlement wiring — 2026-08-28

- With `PLATFORM_DATABASE_URL`, the API now constructs PostgreSQL-backed session and refresh authorities and a PostgreSQL-backed entitlement manager. Access-token `sid`/`sub` validation, session listing/revocation, refresh revocation, purchase claims, entitlement reads, pack authorization, and capability entitlement-version reads no longer consult process maps.
- Durable session mutations run with transaction-scoped `app.subject` RLS context and report database failure to HTTP callers instead of returning a successful logout/list response. A regression uses a deliberately failing backend to prove there is no in-process fallback.
- Forward migration `0010_entitlement_snapshot_executor.sql` grants only a subject-checked security-definer entitlement projection; the API role still lacks direct snapshot-table access. A fresh disposable PostgreSQL 16 run applied migrations `0001`–`0010` under `ON_ERROR_STOP=1`.
- `gofmt`, `go test -race ./...`, `go vet ./...`, and `git diff --check` passed. This is local synthetic evidence only. Durable identity/lifecycle/notification worker integration, real provider adapters, KMS, and staging evidence remain open.

### Durable provider-identity runtime wiring — 2026-08-28

- Database-configured runtime now uses an atomic provider-subject sign-in routine protected by an advisory lock on the keyed digest. It creates one immutable user/account and provider link, or returns the already linked account; email remains absent from the model and merge logic.
- Provider subject persistence requires a 32-byte AES-GCM key (base64 configuration) and a distinct lookup HMAC key. The in-code protector regression proves ciphertext is not the raw subject and digest length is 32 bytes. Unlinking is a subject-scoped durable function that refuses the final active recovery method.
- Fresh PostgreSQL 16 applied `0001`–`0011` successfully; `go test -race ./...` and `go vet ./...` passed. This does not claim a real OIDC callback, passkey ceremony, KMS key holder, lifecycle worker, or staging evidence.

### Durable lifecycle and erasure task evidence — 2026-08-28

- Forward migration `0012_durable_lifecycle_and_erasure.sql` provides subject-checked atomic deactivation/reactivation/export/deletion request routines. Deactivation/deletion revokes sessions and refresh families while writing audit/outbox facts; deletion requests are durable jobs.
- The private eraser command now exposes only strict `POST /tasks/deletions/{uuid}` task handling in addition to probes. It calls an eraser-role executor that atomically claims the job, copies the keyed provider digest into a versioned tombstone, erases identity material, and marks completion. Cloud Run IAM remains the deployment authentication control.
- Reproducible synthetic PostgreSQL evidence is `bharatstudio-platform/tests/sql/durable_lifecycle.sql`: API-role sign-in/deactivate/reactivate/delete-request followed by eraser-role completion yielded `deleted`, one retained provider tombstone, and zero sessions. `go test -race ./...` and `go vet ./...` passed. Real task OIDC/IAM, backup restoration, export delivery, and staging deletion rehearsal remain open.

### Durable verified store-notification ingestion — 2026-08-28

- `0013_durable_store_notification_ingress.sql` creates a store-role-only verified notification executor. It deduplicates by provider delivery ID, quarantines unbound purchases, appends immutable refund/revoke/etc. ledger facts, and recalculates the versioned entitlement projection in the same transaction.
- Reproducible synthetic evidence is `bharatstudio-platform/tests/sql/durable_store_notification.sql`: an API-role claim followed by a store-role verified refund returned `processed`, changed snapshot version from `1` to `2`, cleared active products, and retained one grant plus one refund ledger fact.
- Raw deliveries still require concrete Apple ASSN/Google RTDN cryptographic adapters and provider credentials before the worker route may be mounted. Those provider/sandbox gates remain open; no unsigned ingress is accepted.

### Durable protected-pack grant evidence — 2026-08-28

- `0014_durable_pack_grants.sql` persists only HMAC digests of five-minute grants. Authorization checks the account-scoped, non-expired entitlement projection and pack catalogue; redemption atomically marks the grant consumed before returning an artifact reference for the URL-signer boundary.
- Reproducible synthetic proof is `bharatstudio-platform/tests/sql/durable_pack_grant.sql`: configured product claim, catalogue/artifact authorization, and redemption returned only `synthetic://artifact` inside the protected backend and left exactly one consumed grant. The API never stores the raw grant.
- A real KMS/object-storage signed-URL signer, deployment catalogue seed, and staging replay/revocation test remain external operational gates.

### Durable passkey state and contract evidence — 2026-08-28

- `0015_durable_passkeys.sql` persists passkey challenge and credential digests, consumes challenges atomically, binds assertions to the challenge account/RP, and advances the sign counter only when non-regressing. The raw credential ID never reaches persistence.
- `bharatstudio-platform/tests/sql/durable_passkey.sql` proved registration then assertion for a synthetic account: the returned account matched the challenge binding, credential count advanced `2`→`3`, and two challenges were consumed. The durable-service test proves no local challenge/credential map is written.
- `/v1/auth/passkeys/options` and `/v1/auth/passkeys/verify` now accept only adapter outputs; verify cannot choose the account from request bytes. A concrete WebAuthn parser/attestation adapter, RP/origin deployment values, device support, and staging ceremony evidence remain external prerequisites.

### Native Apple/Google OIDC challenge evidence — 2026-08-28

- `0016_durable_oidc_challenges.sql` persists only keyed state/nonce digests and atomically consumes both values. `NativeOIDC` uses that boundary before validating a signed ID token; its callback test proves successful nonce-bound sign-in and rejects callback replay.
- The configured runtime now accepts optional Google/Apple client IDs, uses only explicit HTTPS JWKS endpoints, and fails configuration when the challenge HMAC is shorter than 32 bytes. The JWKS resolver has a bounded five-minute cache and refreshes on unknown key ID.
- Local evidence covers synthetic RS256 signature/JWKS-bound verifier behavior and database challenge consumption. Real Google/Apple client registration, live device callback, key rotation, provider sandbox, and staging remain external evidence gates.

### Durable reconciliation correction evidence — 2026-08-28

- `0017_durable_reconciliation.sql` adds a reconciler-role executor that resolves the account from the locked purchase-root binding, appends either `correction` or `revoke`, and increments the snapshot version. It never accepts a task-supplied BharatStudio user ID.
- `bharatstudio-platform/tests/sql/durable_reconciliation.sql` proved API claim followed by reconciler correction: the role returned `corrected`, entitlement version moved `1`→`2`, active products cleared, and both grant/revoke ledger facts remained. The private handler regression proves it HMAC-digests only an adapter-verified purchase root.
- Provider API reconciliation credentials/query implementation, periodic scheduling, Cloud Run task IAM, and live sandbox correction evidence remain external gates.

### Fresh reauthentication and account recovery evidence — 2026-08-28

- `0018_durable_reauth_and_unlink_guard.sql` applies final-recovery-method protection to identity-ID unlink operations as well as subject-digest unlink. Configured runtime treats an active session created within five minutes by a provider/passkey ceremony as fresh reauthentication for sensitive session-bound operations.
- The reactivation handler also supports a verifier-bound reauthentication callback without an existing active account session, avoiding the deactivation/reactivation deadlock. Its regression proves a deactivated account returns active only after adapter verification; it cannot use client-selected account input.
- Live reauth UX/device tests, provider session assurance policy, and staged deletion/link/unlink checks remain external gates.

### Local hostile/runtime regression sweep — 2026-08-28

- `go test -race ./...` and `go vet ./...` passed after migrations `0001`–`0018`; the published versioned HTTP-route regression confirms every public OpenAPI operation has a handler rather than falling through to 404. Private store ingress intentionally remains non-discoverable without private authorization.
- All four local distroless command images built successfully: API, eraser, store-ingress, and reconciler. These are build artifacts only, not deployment or provider/staging evidence.

### Restart-stable JWT and JWKS hardening — 2026-09-08

- Executed `go test ./...`, `go vet ./...`, and `go test -race ./...` in the Platform repository after adding the configuration-backed JWT key ring and JWKS use filter; all passed.
- `TestKeySetFromJSONKeepsPublishedKeyAcrossRotation` proves a configured active key mints/verifies tokens while a public-only published key remains in JWKS. `TestKeySetFromJSONRejectsInvalidKeyRings` rejects missing signing material and multiple active keys. `TestHTTPJWKSResolverAcceptsOnlySigningKeys` uses a local TLS JWKS server to reject `use: enc` and resolve `use: sig`.
- No production or provider evidence is implied. KMS/HSM, deployed secret rotation, provider JWKS rotation, staging deployment, rollback, and independent hostile review remain required.

### Current-tree reproducibility rerun — 2026-09-08

- Rebuilt all four command-selected local images from the current tree: `api-0018-jwks` (`sha256:0381779f…`), `eraser-0018-jwks` (`sha256:39023d44…`), `store-ingress-0018-jwks` (`sha256:cdf0b0a5…`), and `reconciler-0018-jwks` (`sha256:81c8a104…`).
- In a disposable PostgreSQL 16 container, six independently initialized databases each applied migrations `0001`–`0018` with `ON_ERROR_STOP=1`, then passed their synthetic role-separated proof: lifecycle, store notification, pack grant, passkey, OIDC, and reconciliation.
- This rerun is local, synthetic, and redacted. It is not provider/store sandbox, deployment, migration-upgrade, outage, rollback, or production evidence.

### Durable protected-operation revocation — 2026-09-08

- Executed `go test ./...`, `go vet ./...`, and `go test -race ./...` after migration `0019`; all passed.
- A fresh disposable PostgreSQL 16 database applied migrations `0001`–`0019` under `ON_ERROR_STOP=1`, then `durable_capability_revocation.sql` proved that API-role deactivation recorded a subject cutoff and revoked one outstanding pack grant atomically.
- The proof uses synthetic IDs and storage references only. It does not prove downstream consumer cache invalidation, deployed event propagation, provider flow, or staging/production behavior.
- After `0020_erase_capability_subject_revocations.sql`, the clean lifecycle/eraser proof reports `deleted`, one provider tombstone, zero sessions, and zero retained account-linked capability cutoffs. `go test ./...` and `go vet ./...` pass.

### Contract fixture hardening — 2026-09-08

- `TestEntitlementEventFixtureHasRequiredV1EnvelopeAndNegativeIsRejected` validates every required v1 envelope field for the positive entitlement event and rejects the synthetic `2.0` version fixture. `TestOpenAPIIsVersionedAndHasNoFreeStreamingPath` now requires reusable public response schemas.
- `go test ./internal/contracts`, full `go test ./...`, and `go vet ./...` passed. No consumer/provider/staging claim is made.

### Private worker OIDC enforcement — 2026-09-08

- `TestOIDCVerifierValidatesServiceTokenAudience` signs synthetic RS256 service tokens and proves exact audience validation; the wrong audience is rejected. `TestEraserTaskHandlerRejectsUnauthorizedPrivateCaller` proves no deletion processing occurs when authorization fails.
- Focused identity/worker tests and `go vet ./...` pass. Cloud Run/Tasks OIDC configuration and staging evidence remain open.

### Discoverable WebAuthn assertion wiring — 2026-09-08

- `TestDurableDiscoverablePasskeyCannotChooseAccount` proves the durable backend returns the credential-selected account, not caller input. The library adapter requires HTTPS origin/RP configuration and verifies challenge, origin, user verification, and signature before the counter mutation executor.
- Clean PostgreSQL `0001`–`0022`, `go test ./...`, `go vet ./...`, and `go test -race ./...` passed using synthetic data only.

### WebAuthn registration/link ceremony evidence — 2026-09-08

- `TestWebAuthnRegistrationOptionsRequireUserVerificationAndOpaqueSubject` proves options require user verification and use the immutable Platform subject only as an opaque WebAuthn handle.
- `TestCeremonyRegistrationVerifierAcceptsVerifiedSyntheticNoneAttestation` verifies a deterministic synthetic standards-shaped registration and rejects a mismatched challenge; no user/device/provider material is used.
- `TestDurableRegistrationChallengeIsBoundToAuthenticatedSubject` proves the exact library challenge is stored with the authenticated account in the durable backend, and refuses an unbound challenge.
- `TestPasskeyRegistrationRequiresCurrentSessionRecentAuthAndBindsSubject` proves anonymous registration is denied, server-derived subject binding is used, and invalid registration input cannot select an account.
- `./tests/run-local-verification.sh` passed after the change: `go test ./...`, `go vet ./...`, `go test -race ./...`, four Docker command image builds, and clean PostgreSQL 16 migration/proof runs. This remains local synthetic evidence, not device or staging proof.

### OpenAPI structural validation — 2026-09-08

- `TestOpenAPIParsesAndAllReferencesResolve` loads the checked-in `/v1` contract with an OpenAPI 3.1 parser and fails on unresolved references, invalid schemas, or missing path parameters. It exposed and corrected the previously undocumented `provider`, `sessionId`, `identityId`, `store`, and `packId` parameters.
- The registration routes now declare bearer security, concrete completion/status schemas, shared error responses, and all references are validated locally. This is contract-structure evidence only; it does not claim consumer or provider compatibility.
- `TestWebAuthnRegistrationFixturesMatchTheirVersionedSchemas` validates a synthetic positive registration-status fixture against its published schema and rejects a completion fixture missing its required challenge. Fixtures contain no credentials, tokens, receipts, or provider assertions.
- The same contract test validates the public purchase-conflict error fixture against the shared `Error` schema and rejects a missing-`traceId` negative fixture.

### Durable export-delivery evidence — 2026-09-08

- `TestExportProcessorCompletesOnlyAfterShortLivedDelivery` proves the processor claims first, persists only a 32-byte delivery-reference HMAC, and completes only after an expiring delivery result.
- `TestExportProcessorReleasesOnDeliveryFailure` proves a sink failure releases the durable claim and writes no delivery reference; `TestExportHandlerIsPrivateAndDoesNotAcceptAccountInput` proves private task authorization and job-ID-only processing.
- Clean PostgreSQL migration/proof execution through `0024` passes via `tests/run-local-verification.sh`; `durable_lifecycle.sql` creates an export job before deletion and proves zero export-job rows remain after actual deletion. This is synthetic-only local evidence.

### Explicit store-provider boundary evidence — 2026-09-08

- `TestAppleNotificationAdapterRequiresNormalizedVerifiedFact` accepts only a complete App Store fact from the JWS validator contract and rejects cross-store or unknown event inputs.
- `TestGoogleReconciliationAdapterRequiresGoogleAPIFact` accepts only a complete Google Play authority result and rejects a failed Developer API verification. The tests use synthetic facts only; neither invokes Apple nor Google.

### Documentation, template, and evidence reconciliation — 2026-09-08

- Corrected the obsolete definition-time claim that the Platform repository did not exist and reconciled WP-0’s original service-directory sketch with the bounded Go command/package layout that was actually implemented. The change preserves the original decision-time context and does not broaden scope beyond the Platform repository.
- Corrected the sole whitespace defect found by `git diff --check` in migration `0001`.
- The complete local gate passed after the changes: `tests/run-local-verification.sh` ran unit tests, vet, race tests, four command-image builds, and every clean PostgreSQL 16 proof through migration `0024`. A separate YAML parser accepted all five deployment templates, including the corrected quoted private-audience URLs for eraser and reconciler. `git diff --check` then passed.
- This is reproducible local self-review evidence. It does not establish deployment validity against Cloud Run, Google IAM, Secret Manager, KMS, Apple, Google Play, or any staging environment.

### Deployment-template regression guard — 2026-09-08

- `TestDeploymentTemplatesParseAndPreserveServiceBoundaries` parses the four Cloud Run manifests under the normal Go test suite and requires their distinct names, service accounts, single image container, required database-secret entry, production mode, no duplicate environment names, and HTTPS private audiences for eraser/reconciler.
- `TestCloudTasksTemplateParses` parses the task queue template and requires exactly the reconciliation and erasure queues. The focused package test and vet passed, followed by the complete `tests/run-local-verification.sh` gate and `git diff --check`.
- The tests deliberately do not claim that placeholder values can be deployed, or substitute for Cloud Run/Cloud Tasks/IAM/staging evidence.
