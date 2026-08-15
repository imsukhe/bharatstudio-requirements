# Deep production-readiness audit — 2026-08-16

**Scope:** second-pass audit of the active BharatStudio v1 repositories after
the previous implementation/regression pass. This is remediation evidence,
not a production approval.

**Repositories inspected:** Alerts, Requirements, Companion Mobile, Companion
Desktop, Infrastructure, Marketing and Crons. The audit followed the central
governance rules and checked code, migrations, tests, deployment contracts and
task evidence rather than relying on status prose.

## Findings fixed in this pass

| ID | Severity | Finding | Disposition and evidence |
|---|---|---|---|
| AUD-2026-08-16-01 | High | `bsa_archive_owner` was created with `BYPASSRLS`, contradicting the effective `0047` soft-archive contract that describes a `NOLOGIN`, `NOBYPASSRLS` SECURITY DEFINER owner. | Fixed in `bharatstudio-alerts/packages/db/roles/0001_v1_service_roles.sql`; `0058_v1_l02_archive_owner_rls_hardening.sql` normalizes existing installations; L02 test now asserts `NOLOGIN`, `NOSUPERUSER` and `NOBYPASSRLS`. Disposable PostgreSQL L02/L03 harness passes. |
| AUD-2026-08-16-02 | Medium | The public tip page collapsed missing creator, creator-closed and API outage into the same “Tips are currently closed” state. | Fixed with `apps/web/app/tips/[handle]/public-channel-loader.ts`. Valid, 404, 503, missing-origin, network and malformed/expanded response tests pass. |
| AUD-2026-08-16-03 | Low | Normal authenticated API routes accepted only exact-case `Bearer`, unlike the overlay parser and the HTTP authentication scheme. | Fixed in `apps/api/src/auth/pre-handler.ts` with case-insensitive parsing; API regression test passes. |
| AUD-2026-08-16-04 | Medium | The Alerts static surface had no checked-in browser security-header artifact, while the L03 provider/CSP gate was still open. | Added `apps/web/public/_headers` with CSP, frame, referrer, permissions and content-type protections; added a Web contract test and Infrastructure manifest/test requirement. Deployment must publish and retrieve the file before production. |

## Deep-path audit results

### Identity, tenant isolation and secrets

- No new cross-tenant read/write path was found in the local route/store and
  migration review.
- Transaction-scoped tenant context, cross-tenant denial, role-scoped
  financial reads, overlay-session scope and helper privilege checks pass in
  the disposable PostgreSQL harness.
- Payment and worker service-specific credentials remain fail-closed in local
  configuration. The production secret-manager, service-account and OIDC
  negative tests are still deployment gates.
- Browser access tokens remain session-scoped `sessionStorage` values by the
  current approved web design. The new CSP reduces script-injection exposure,
  but authenticated browser/XSS, CSP enforcement and deployed header retrieval
  still require staging evidence; this audit does not claim token theft risk is
  eliminated.

### Payments, idempotency and reconciliation

- The payment boundary uses raw-body HMAC validation and
  `X-Razorpay-Event-Id` as the durable deduplication identity; no new timestamp
  or randomness-derived dedup key was found.
- Local concurrent duplicate, idempotency-mismatch, provider-response-boundary
  and ledger/outbox tests pass.
- Razorpay Technology Partner approval, real sandbox checkout/webhook/refund,
  connected-account behavior, reconciliation, credentials/IAM and staging
  recovery remain open. No local test can substitute for those provider gates.

### Queue, worker and overlay no-drop path

- Per-queue delivery state, durable replay, cursor acknowledgement, reconnect
  suffix replay, notification outage fallback, cross-replica local replay and
  multi-queue source/priority snapshots were rechecked. No new local
  accepted-event loss path was found.
- Presentation limits, TTS failure and capacity pressure do not acknowledge or
  delete durable rows in the tested path.
- Live Cloud Tasks retry/dead-letter, worker crash, queue backlog, 1,000-row
  partial retry, cross-replica deployed SSE, OBS browser-source behavior and
  capacity proof remain launch gates.

### Companion and public surfaces

- Web Companion responses are bounded and privacy-minimised; notification
  preferences/device routes are authenticated and token ciphertext is not
  returned to the client.
- Mobile foreground notification handling is privacy-safe. Native background
  OS notification display, real-device/provider behavior and store evidence
  remain L07 work; the audit did not mark the validation-only adapter as full
  background delivery.
- Desktop native pairing, secure credential storage, OBS WebSocket control,
  signing/notarisation and real Windows/macOS OBS validation remain open; no
  local shell/raw-secret boundary regression was found in the inspected
  contract.
- TTS is currently an optional browser side effect with chime fallback. A
  production provider/audio route and real TTS validation are not present in
  this pass and remain an explicit L03/L05/provider gate rather than an implied
  working feature.

## Evidence executed in this pass

- Alerts API: `pnpm test` — **63/63 pass**.
- Alerts Web: `pnpm test` — **39/39 pass**; `pnpm build` — pass.
- Database: `pnpm db:test:l03` — `L02_SECURITY_REMEDIATIONS=PASS` and
  `L03_APPLICATION_BEHAVIOR=PASS`.
- Contracts: `pnpm contracts:validate` — 11 fixtures and the v1 OpenAPI
  document with 35 paths pass.
- Infrastructure contract: `npm test` must pass after the manifest header
  requirement is applied.

## Residual production blockers

This pass does not change the release verdict. Production remains blocked on:

1. Razorpay/provider approval and real provider sandbox/live evidence.
2. Neon region/compute/connection budget and Cloud Run min/max/concurrency
   decisions with deployed capacity proof.
3. Secret Manager, IAM/OIDC, Cloud Tasks retry/DLQ, direct database listener,
   cross-replica SSE, backup/restore and rollback rehearsal.
4. Authenticated browser/accessibility/localisation/long-text/reduced-motion,
   OBS and deployed CSP/header verification.
5. Native mobile background/provider/device/store evidence.
6. Windows SDK/signing and macOS OBS/pairing/signing/notarisation evidence.
7. TTS/provider behavior, support/legal/privacy/compliance approval and fresh
   independent review.

**Verdict:** local implementation is stronger after this pass, with the
confirmed role, public-state, auth-scheme and static-header defects fixed. The
system is not yet production-ready because the remaining blockers are real
external/deployment/integration evidence requirements, not because this audit
found a new silent data-loss or tenant-isolation defect.
