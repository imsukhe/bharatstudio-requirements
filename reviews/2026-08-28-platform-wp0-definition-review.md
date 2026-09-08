# Platform WP-0 definition review

**Date:** 2026-08-28
**Reviewer:** Codex self-review
**Independent reviewer:** Not performed in this pass
**Decision state:** `Approved for implementation — owner approval recorded 2026-08-28; independent review remains a verification gate`
**Task:** [`../tasks/PLATFORM-WP0-governance-architecture-definition.md`](../tasks/PLATFORM-WP0-governance-architecture-definition.md)
**Acceptance:** [`../tests/TC-PLATFORM-WP0-governance-architecture-definition.md`](../tests/TC-PLATFORM-WP0-governance-architecture-definition.md)

## Scope reviewed

- Canonical governance lifecycle, L3 classification, and definition-to-implementation approval boundary.
- Owner mission's identity, entitlement, store, lifecycle, and availability requirements.
- The permitted Android/iOS product evidence for server-protected value and local/free continuity.
- Alerts' service split, OIDC, least-privilege database, append-only evidence, Cloud Tasks, deployment-template, health/readiness, and redacted-observability conventions.
- Exact Platform ownership, data model, privacy/deletion, migration, test, rollback, deployment, and prerequisite plan.

## Findings and dispositions

| ID | Finding | Severity | Disposition | Owner/follow-up/release gate |
|---|---|---:|---|---|
| P0-R1 | Platform did not exist, so it had no local instructions to read and no repository state to inspect. | Medium | Recorded; creation of `AGENTS.md` and `CLAUDE.md` is the first post-approval Platform action. | Platform owner; before WP-1. |
| P0-R2 | Identity, store, device/installation, session, and entitlement identities could be accidentally conflated by clients or future services. | Critical | Fixed in proposed authority with distinct records, token claims, binding keys, and no-email-merge rule. | Security/API; test in WP-2/WP-4. |
| P0-R3 | A shared database or direct read by Alerts/mobile apps would violate ownership and expand blast radius. | Critical | Fixed: dedicated Platform PostgreSQL/database roles; versioned API/event integration only. | Platform/SRE; verify deployment IAM in WP-5/WP-6. |
| P0-R4 | Refresh-token replay, stale JWKS, and unsafe key rotation could leave compromised access live. | Critical | Fixed in design: family reuse revocation, bounded cache/retry, KMS/HSM keys, overlap/retirement evidence. | Security; adversarial tests in WP-2/WP-6. |
| P0-R5 | Store claims can be replayed or conflict across accounts; deletion can tempt destructive payment history removal. | Critical | Fixed: verified stable provider facts, one active binding, quarantine/manual proof resolution, append-only compensating ledger, and purpose-separated HMAC tombstones. | Payments/security/privacy; sandbox evidence in WP-3/WP-4. |
| P0-R6 | Platform outage could accidentally block the locked free streaming path. | High | Fixed: free path is explicitly account-free and has no Platform call; only protected operations fail closed. | Mobile/platform; outage rehearsal in WP-5/WP-6. |
| P0-R7 | Retention, legal notices, provider configuration, and real store sandbox credentials are external dependencies that cannot be inferred. | High | Deferred as explicit prerequisites; no legal/provider/production claim is made. | Owner/legal/SRE/provider; before relevant staging/production gate. |
| P0-R8 | An independent review is unavailable in this pass. | Process | Recorded; this is self-review only and cannot advance to Verified. | Owner; obtain fresh independent review before implementation closure. |

## Decision

The WP-0 definition is approved for implementation by the owner. It authorizes repository creation and local implementation only; it does not authorize external infrastructure/provider configuration or any staging/production-readiness claim.

## Required owner approval statement

Approve the linked authority, task, and acceptance record together, including: exact scope/non-goals; listed future affected files; the dedicated data model and retention/tombstone choices; security and privacy controls; migration and test plan; rollback and deployment model; and listed external prerequisites. Any change to these items is scope drift and requires an updated decision before implementation.

## WP-1 security self-review — 2026-08-28

| ID | Finding | Severity | Disposition | Evidence / follow-up |
|---|---|---:|---|---|
| P1-R1 | A Platform contract could accidentally become a dependency of free streaming. | High | Fixed: contract test rejects `rtmp`, and the API inventory contains protected identity/entitlement operations only. | `go test ./...`; mobile outage integration remains WP-5/WP-6. |
| P1-R2 | Fixtures can leak token/receipt material into repositories. | High | Fixed: synthetic fixtures are JSON-parsed and rejected when prohibited secret labels appear. | `go test ./...`; add full secret scanning in WP-5 CI. |
| P1-R3 | Baseline migration is unproven against PostgreSQL. | High | Deferred: it is an unapplied clean baseline by design. | Disposable PostgreSQL apply/behavior evidence is required in WP-6. |

## WP-2 security self-review — 2026-08-28

| ID | Finding | Severity | Disposition | Evidence / follow-up |
|---|---|---:|---|---|
| P2-R1 | A rotated refresh token could otherwise remain replayable. | Critical | Fixed: reusing it revokes the entire family and all its derived tokens. | `TestRefreshReuseRevokesFamily`. |
| P2-R2 | Key rotation can cause a verification outage or accept a retired key. | Critical | Fixed: explicit publish/activate/retire states, overlap verification and retired-key rejection. | `TestAccessTokenAndKeyRotation`; KMS/JWKS-cache rehearsal remains WP-6. |
| P2-R3 | Email/provider matching could merge unrelated accounts. | Critical | Fixed: provider subject is the only identity key; linking is explicit/recent-auth and conflicts fail closed. | `TestNeverMergesEmailEquivalentProviders`. |
| P2-R4 | Passkey cryptography cannot be safely hand-waved. | Critical | Deferred behind a mandatory verifier interface; challenge/replay/counter policy is local-tested, while production WebAuthn parser/origin/attestation integration requires WP-6 evidence. | No live passkey claim. |

## WP-3/WP-4 security self-review — 2026-08-28

| ID | Finding | Severity | Disposition | Evidence / follow-up |
|---|---|---:|---|---|
| P34-R1 | Deactivation/deletion without token revocation leaves a compromised client active. | Critical | Fixed: subject-wide session and refresh-family revocation emits audited revocation events before deletion completes. | `TestDeactivateExportAndActualDeletion`. |
| P34-R2 | Erasure could retain raw provider identifiers, or erase justified anti-replay records. | High | Fixed locally: provider maps/passkeys are erased; only keyed HMAC tombstones persist. | Local lifecycle test; DB retention/crypto-erasure proof remains WP-6. |
| P34-R3 | Store receipts can bind a purchase to the wrong account. | Critical | Fixed: stable verified purchase-root binding accepts one subject only; conflicts neither merge nor disclose owner. | `TestClaimConflictAndCompensatingRevocation`. |
| P34-R4 | Delayed/malformed store notifications could corrupt entitlement truth. | Critical | Fixed locally: verified delivery-ID deduplication and quarantine precede projection; corrections append a fact. | Local tests; provider notification/order/reconciliation rehearsal remains required. |

## WP-5/WP-6 security self-review — 2026-08-28

| ID | Finding | Severity | Disposition | Evidence / follow-up |
|---|---|---:|---|---|
| P56-R1 | A protected-pack URL/capability could be replayed or used by another account/service. | Critical | Fixed locally: one-time 5-minute grants and signed 15-minute audience/session/device-bound capabilities with negative tests. | `TestProtectedGrantAndCapabilityAreScopedAndShort`; real object service/revocation cache test remains staging work. |
| P56-R2 | Health endpoints can falsely declare a production runtime ready. | High | Fixed: local production bootstrap fails closed pending KMS/HSM and DB adapters; `/readyz` accepts a dependency predicate. | HTTP unit test and local build; wire real probes in staging. |
| P56-R3 | Baseline SQL can fail only when applied. | High | Fixed for clean migration: applied to disposable PostgreSQL 16 under `ON_ERROR_STOP=1`. | 24 tables created; clean migration evidence only. |
| P56-R4 | Local tests cannot establish provider, staging, deployment, outage, rollback, or hostile-audit readiness. | Critical | Open / blocking verification gate. | No production-readiness claim; execute only after prerequisites are supplied. |

## Security-audit remediation review — 2026-08-28

| ID | Original finding | Disposition | Evidence |
|---|---|---|---|
| AR-1 | Deleted accounts could reactivate. | Fixed: state transition validates current state before mutation; regression added. | `TestDeletedAccountCannotReactivate`. |
| AR-2 | Expired products and duplicate transactions could grant access. | Fixed: expiry-aware authorization and transaction idempotency. | Store/package regression tests. |
| AR-3 | WebAuthn RP/origin/registration verification was not enforceable. | Fixed at service boundary: verifier result must carry exact RP/origin, user verification and public key registration evidence. | Passkey regression test; live WebAuthn ceremony remains external evidence. |
| AR-4 | Store notification verification was caller-controlled. | Fixed: public ingestion requires a notification-verifier adapter; malformed/unbound input quarantines retryably. | Store regression tests. |
| AR-5 | Capability revocation and pack authorization were insufficiently scoped. | Fixed: signer-issued five-minute URL grants and session/version/subject capability revocation checks; lifecycle invokes revocation. | Pack + integration regression tests. |
| AR-6 | No RLS/erasure database enforcement existed. | Fixed in migration `0002`; disposable PostgreSQL proof completed. | Migration run and SQL erasure result. |
| AR-7 | Runtime contract/persistence gaps. | Partially fixed: authenticated handler and PostgreSQL repository boundaries added. Full provider/KMS/database adapter wiring remains an open staging/implementation gate and must not be represented as complete. | Fails closed in production bootstrap. |

## Follow-up self-review — 2026-08-28

| ID | Finding | Severity | Disposition | Evidence / follow-up |
|---|---|---:|---|---|
| FU-1 | A pre-signed pack URL was returned before the one-time grant was redeemed. | Critical | Fixed locally: authorization now returns only the opaque grant; redemption atomically consumes it before signing. | Pack regression plus `go test -race ./...`; object-storage integration remains an external gate. |
| FU-2 | A caller could nominate arbitrary session/device IDs while minting a capability. | High | Fixed locally: the handler derives both fields from the verified access-token session, and capability validation accepts only an exact session/subject/device binding. | Session-binding regression plus `go test -race ./...`. |
| FU-3 | The prior audit labelled production bootstrap refusal as a deployment crash. | Process | Corrected: deployment files are explicitly substitution templates and local bootstrap intentionally fails closed without real KMS/HSM/database adapters. The unimplemented durable adapter wiring remains the actual release blocker. | Do not deploy templates unchanged; prove actual adapters in WP-6. |

## Repair-and-reaudit self-review — 2026-08-28

| ID | Finding | Severity | Disposition | Evidence / follow-up |
|---|---|---:|---|---|
| RR-1 | API role had no viable audit/outbox append path under RLS permissions. | Critical | Fixed locally with a subject-bound security-definer function; direct table writes remain denied. | Clean PostgreSQL 16 run as `bsp_platform_api` wrote one synthetic audit/outbox pair. |
| RR-2 | Logout left refresh families usable; a family ID could be rebound by an internal caller. | Critical | Fixed locally: current-session logout revokes its family and family/session/subject association is immutable. | HTTP/auth regressions in race suite. |
| RR-3 | Database erasure left challenge/snapshot/capability subject links. | High | Fixed locally in forward migration `0004`; the binding is tombstoned and capability subject is nulled. | Clean PostgreSQL 16 erasure run. |

| RR-4 | Deployment templates referenced three binaries that did not exist. | Critical | Partially fixed: separate worker commands and container targets now build and require their own database connection. Durable task handlers remain open. | Four local Docker command-target builds passed. |
| RR-5 | Session/token identifiers could not be written into PostgreSQL UUID columns. | Critical | Fixed locally: RFC 4122 v4 formatting replaces the malformed formatter. | `TestGeneratedSessionAndTokenIDsAreUUIDs`. |
| RR-6 | Refresh rotation/revocation was process-local and could race under replicas. | Critical | Partially fixed: atomic PostgreSQL procedures issue, rotate, detect reuse, and revoke durable families. Runtime identity/session/ledger wiring remains open. | Clean PostgreSQL 16 rotation/replay/revocation proof. |
| RR-7 | Provider identity and purchase binding operations were process-local. | Critical | Partially fixed: identity and atomic store-claim PostgreSQL executors were added with RLS-safe clean-database evidence. Service/runtime integration remains open. | Clean PostgreSQL 16 synthetic identity and claim proof. |
| RR-8 | Configured API runtime still read session and entitlement truth from process memory. | Critical | Partially fixed: configured runtime now uses fail-closed PostgreSQL session/refresh and entitlement backends; the subject-bound snapshot path is protected by a forward-only executor. Identity, lifecycle, notifications, and workers remain open. | Race suite, vet, diff check, and clean PostgreSQL 16 migrations `0001`–`0010`. |
| RR-9 | Configured identity sign-in had no durable provider-subject ownership path. | Critical | Partially fixed: configured runtime has AES-GCM/HMAC protected provider material, atomic keyed-digest provider sign-in, durable state reads/transitions, and durable final-method guard. Concrete OIDC/passkey adapters and durable lifecycle completion remain open. | Identity protector regression; clean PostgreSQL 16 migrations `0001`–`0011`; race suite and vet. |
| RR-10 | Account lifecycle and deletion jobs remained process-local; eraser image had no durable task behavior. | Critical | Partially fixed: atomic PostgreSQL lifecycle/job/outbox executors and a strict eraser task handler now exist. A clean role-separated synthetic database flow proved actual deletion, retained keyed tombstone, and session removal. Export delivery, task IAM/OIDC proof, backup restore, and staging remain open. | `tests/sql/durable_lifecycle.sql`, clean PostgreSQL 16 output, worker regression, race suite, vet. |
| RR-11 | Store notification state and refund/revocation projection were process-local. | Critical | Partially fixed: verified notifications now have a store-role atomic persistence/ledger/snapshot function with delivery idempotency and quarantine. Concrete Apple/Google verification/reconciliation adapters and actual ingress mount remain open. | `tests/sql/durable_store_notification.sql`, clean PostgreSQL 16 role proof, store/worker tests. |
| RR-12 | Protected-pack grants were process-local and could not survive replica/restart boundaries. | Critical | Partially fixed: opaque-grant HMAC digests, entitlement/catalogue authorization, and atomic redemption are now durable. KMS/object storage signer and distributed capability-revocation evidence remain open. | `tests/sql/durable_pack_grant.sql`, clean PostgreSQL 16 proof, existing pack regressions. |
| RR-13 | Passkey challenge/credential/counter state was process-local and passkey routes were absent. | Critical | Partially fixed: durable challenge/credential/replay/counter procedures and verifier-only versioned routes now exist. Concrete WebAuthn ceremony parsing/attestation and RP/origin staging configuration remain open. | `tests/sql/durable_passkey.sql`, durable-service regression, HTTP route regression. |
| RR-14 | Apple/Google callback state/nonce was not durable and the verifier had no network JWKS adapter. | Critical | Partially fixed: state/nonce digests are durable and one-time; configured native OIDC uses HTTPS-only JWKS lookup before identity/session issuance. Live provider registration, redirect/device flows, and key-rotation sandbox evidence remain open. | `tests/sql/durable_oidc.sql`, native OIDC replay regression, configuration validation. |
| RR-15 | Reconciliation could only modify an in-memory projection and did not have a reconciler role boundary. | Critical | Partially fixed: locked purchase-root reconciliation appends a durable correction/revocation under a distinct DB role. Provider-query/scheduling adapters and live reconciliation evidence remain open. | `tests/sql/durable_reconciliation.sql`, role proof, strict worker-handler regression. |
| RR-16 | Deactivated accounts could not complete a fresh reauthentication to reactivate, and ID-based unlink lacked final-method guard. | Critical | Partially fixed: verifier-bound reactivation callback exists and durable ID unlink now refuses final recovery method. Live provider/device reauth policy validation remains open. | Reactivation HTTP regression, migration `0018`, race suite. |
| RR-17 | Published API inventory could still diverge from HTTP routing after incremental work. | High | Fixed locally: regression invokes every public OpenAPI operation and rejects route fall-through. Private ingress is deliberately hidden without private authorization. | `TestPublishedVersionedRoutesDoNotFallThroughToNotFound`; full race/vet and four command-image builds. |
| RR-18 | Database-configured API instances still generated an ephemeral signing key on every restart, breaking durable JWKS overlap. | Critical | Fixed locally: database configuration now requires a validated versioned P-256 key ring with one active private key and optional public-only published overlap keys; malformed/multi-active rings fail at bootstrap. | `TestKeySetFromJSONKeepsPublishedKeyAcrossRotation`, `TestKeySetFromJSONRejectsInvalidKeyRings`, full test/race/vet run on 2026-09-08. KMS/HSM-backed production signing and deployed rotation proof remain open. |
| RR-19 | HTTP JWKS lookup could use an RSA key explicitly designated for encryption. | High | Fixed locally: resolver permits only absent `use` or `sig`; `enc` keys are ignored. | TLS-backed `TestHTTPJWKSResolverAcceptsOnlySigningKeys`; live provider JWKS/key-rotation evidence remains open. |
| RR-20 | Prior SQL/image evidence could have become stale after runtime hardening. | Process | Re-run against the current tree completed. | Four command images rebuilt locally and six clean PostgreSQL 16 migration-plus-role proofs passed on 2026-09-08. No staging/provider/production claim follows. |
| RR-21 | Configured capability revocation still depended on a process-local subject map, so a restart could accept an old protected capability. | Critical | Fixed locally: lifecycle deactivation/deletion now atomically records a durable subject cutoff and revokes outstanding pack grants; configured verification denies capabilities issued at or before it. | `TestDurableCapabilityRevocationDoesNotUseProcessMap`; clean `0001`–`0019` PostgreSQL proof. Downstream event/cache propagation remains a staging gate. |
| RR-22 | The new cutoff initially retained a direct account reference after deletion. | High | Fixed before package closure with forward migration `0020`; erasure deletes the cutoff after it has served its pre-deletion revocation purpose. | Clean lifecycle/eraser PostgreSQL proof reports zero retained capability-subject revocation rows; synthetic `go test ./...` and vet pass. |
| RR-23 | Versioned contracts had little machine-checked response shape or negative-version evidence. | High | Fixed locally with reusable OpenAPI schemas and a negative event-version fixture. | Focused contracts, full tests, and vet pass; independent consumer compatibility remains open. |
| RR-24 | The eraser route relied only on perimeter deployment IAM and had no in-process cryptographic caller verification. | Critical | Fixed locally: Google RS256 service-token issuer/audience/signature verification is mandatory at the private route. | Synthetic signed-token/audience and unauthorized-handler regressions; deployed IAM/Cloud Tasks/staging proof remains open. |
| RR-25 | Passkey login could not safely be discoverable because durable challenges required an account before credential verification. | Critical | Partially fixed locally: unbound discoverable challenges, HMAC credential lookup, standards-library assertion verification, and atomic credential-selected completion now exist. | Clean migrations/tests/race pass. Registration/link ceremony and live device evidence remain open. |
| RR-26 | Passkey registration/link had durable state but no standards-library ceremony or authenticated HTTP completion, leaving credential enrollment incomplete. | Critical | Fixed locally: authenticated recent-session options, library verification with required UV/RP/origin/challenge checks, keyed durable credential storage, and account-bound atomic challenge consumption are wired. | Deterministic synthetic `none`-attestation, HTTP account-binding regressions, and full local runner pass. Real RP/device/staging and independent hostile-audit evidence remain open. |
| RR-27 | The OpenAPI file could be syntactically valid-looking while containing unresolved references or missing required path parameters. | High | Fixed locally: OpenAPI 3.1 parsing/validation is now a contract test, and every parameterized path declares its required parameter. | `TestOpenAPIParsesAndAllReferencesResolve`; consumer compatibility remains an external integration gate. |
| RR-28 | Contract fixtures were parsed as JSON but were not proven to satisfy the corresponding request/response schemas. | High | Fixed locally for WebAuthn registration: positive status fixture is schema-valid and a missing-challenge completion fixture is rejected by the published schema. | `TestWebAuthnRegistrationFixturesMatchTheirVersionedSchemas`; expand equivalent fixture pairs as each consumer contract is generated. |
| RR-29 | Export requests had durable creation but no safe delivery state machine; deletion could leave an account-linked export artifact reference. | Critical | Fixed locally: role-scoped claim/release/complete, keyed opaque delivery references, private handler, retry release, and deletion-time export-job erasure are implemented. | Lifecycle/worker regressions and clean PostgreSQL proof through `0024`; real encrypted storage/delivery and staging remain open. |
| RR-30 | Store adapters accepted a generic verifier interface without making Apple ASSN versus Google authoritative reconciliation requirements explicit. | Critical | Fixed locally: typed Apple validated-notification and Google Developer-API reconciliation authority adapters normalize and reject invalid/cross-store facts before durable worker handlers. | Focused synthetic regressions; real Apple JWS/Google API credentials and sandbox evidence remain open. |
| RR-31 | A shared public error fixture was not checked against its reusable OpenAPI schema. | Medium | Fixed locally: positive conflict and negative missing-trace fixtures are validated against `Error`. | `TestWebAuthnRegistrationFixturesMatchTheirVersionedSchemas`; consumer integration remains pending. |
| RR-32 | WP-0 definition-time wording described a repository that now exists and an implementation layout that changed from the original service-directory sketch; two private Cloud Run template URLs were also invalid YAML plain scalars. | Medium | Fixed locally: the authority and task retain their historical context while naming the actual bounded Go layout; eraser/reconciler audiences are quoted valid YAML scalars. | Complete local runner plus all-five-template YAML parse and `git diff --check` passed on 2026-09-08; no scope, security, retention, or release decision changed. |
| RR-33 | Deployment-template syntax and minimum service-boundary invariants were not part of the deterministic normal Go test path, allowing invalid YAML to escape until manual audit. | High | Fixed locally: Go contract tests parse all deployment templates and enforce the checked-in private-service boundaries. | Focused test/vet and the complete runner through PostgreSQL `0024` passed on 2026-09-08; Cloud Run schema/IAM/runtime validation remains external. |
