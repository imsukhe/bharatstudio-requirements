# CTL-13 — MFA enforcement and durable admin registry

**Status:** `Conditionally complete locally; external release gates remain`

| Field | Value |
|---|---|
| **Scope phase** | `v1`; Phase 0 capability-control-plane foundation. Decide and implement MFA enforcement for the standalone platform-admin console while retaining the database durable admin registry as the authorization source of truth. |
| **Owner** | Sukhdev Singh |
| **Tier and gate** | Internal platform-admin only. Section 20.6 requires MFA before CTL-04/05 mutation UI is reachable; ADM-07 bootstrap remains deployment-only and cannot become a standing bypass. |
| **Personal-data class** | Depends on the approved MFA method. No method may persist an authenticator secret, recovery code, device identifier, or identity-provider token without an explicit approved data/retention/recovery design. |
| **Provider or legal dependency** | Owner selected application-managed passkeys. Owner approved a five-minute ceremony challenge, fifteen-minute privileged-session elevation, and audited two-person lost-passkey recovery on 2026-09-18. Production RP ID/origin allowlist remains a configured-unset release gate; no provider is contacted. |
| **Failure behaviour** | Fail closed: absent, unverifiable, expired or insufficient MFA assurance denies all platform-admin routes and shows a recovery-safe message without identity enumeration. Local development bootstrap remains development-only. |
| **Kill switch** | Disable the admin console deployment/route through existing deployment controls; no MFA change may weaken the database `is_platform_admin` gate or make `staff_bootstrap_platform_admin()` API reachable. |
| **Acceptance test** | `tests/TC-CTL-13-admin-mfa.md` |
| **Evidence location** | `reviews/2026-09-18-ctl-admin-control-plane-decision.md`; concrete test/evidence paths follow the owner decision. |
| **Rollback** | Roll back only to a previously approved and verified MFA posture. Never fall back to production bootstrap-secret or email allowlist authentication. Database admin registry and audit history remain unchanged. |

## Selected posture and retained external gates

The owner selected **application-managed passkeys**. The implementation stores only public
credential material and bounded operational metadata, requires user verification and monotonic
counter checks, and fails closed when WebAuthn configuration or verified assertion state is absent.

The owner approved these policy values on 2026-09-18: a ceremony challenge lasts **five minutes**;
a verified privileged-admin session lasts **fifteen minutes**; and there are **no recovery codes or
self-service credential resets**. A locked-out platform admin may create a recovery request only
for their own account. Before it can complete, two *distinct*, currently passkey-verified platform
admins must approve it: the singleton designated platform owner and one non-owner platform admin.
Approval may not be self-approval, requests expire after 24 hours, and completion atomically
revokes every active passkey and session for the target. The target must authenticate again and
enrol a new passkey. Recovery retains only request/actor/target/timestamps and append-only audit
state; it stores no recovery secret, credential response, identity-provider token or free-form
reason. This is an app-managed safety process, not an identity-provider account-recovery claim.

No production RP ID/origin or production provider claim is inferred. Those values remain
configured-unset deployment/release gates in the decision record.

## 2026-09-18 local implementation evidence

- Forward-only migration `0165_v1_ctl_admin_passkeys.sql` persists public credential material,
  SHA-256 challenge hashes, challenge/session/user binding, expiry/one-time consumption, counters and
  `user_sessions.admin_mfa_verified_at`, plus append-only redacted registration/assertion audit
  records; it stores no private key, password, recovery secret, provider token or attestation blob.
- The API requires user verification, configured RP ID/origins and SQL finalization that atomically
  consumes a matching challenge before counter/session elevation. Capability mutation routes return
  `428 admin_mfa_required` without recent MFA; unavailable configuration/store returns 503.
- `bharatstudio-admin` has a same-origin server proxy and `/mfa` user flow. `/admin/*` requires
  verified MFA; browser code never receives the API bearer token.
- The final full local Alerts verification pipeline passed after a fresh 166-migration database: 89
  isolated SQL proofs, contract/explain/harness/deployment/load/fault/API/web/measurement checks,
  Go race/vet checks and three command-image builds. The admin console typecheck, 4-test unit suite
  (including BFF allowlist denial), and
  production build passed. A final UI audit corrected stale login copy that claimed MFA was absent,
  corrected success/error announcement semantics on the passkey screen, and preserves the BFF's
  narrow route allowlist. `git diff --check` and requirements traceability/doc consistency also
  pass after the evidence update.

## 2026-09-18 recovery-policy implementation evidence

- Forward-only migration `0166_v1_ctl_admin_passkey_recovery.sql` implements the approved policy:
  self-targeted request only, durable 24-hour expiry, one designated-owner approval plus one
  distinct non-owner platform-admin approval, recent fifteen-minute MFA assertion at each approval,
  append-only minimised audit, and one transaction that revokes every active target passkey and
  session on completion. Direct table access is revoked from `bsa_app` and `public`.
- API recovery request is role-gated; pending-list and approval routes are recent-MFA-gated. The
  admin console exposes the locked-out user request at `/mfa` and the controlled approval queue at
  `/admin/security` through the existing narrow same-origin BFF allowlist. The browser never
  receives the upstream bearer token.
- Reproducible local commands and results: `pnpm --dir apps/api exec tsc --noEmit`; `pnpm --dir
  apps/api exec tsx --test test/admin-passkeys-routes.test.ts test/app.test.ts`; `pnpm
  contracts:validate`; and `sh packages/db/tests/run-sql-suite.sh 0166` all passed. The final fresh
  SQL suite reported 166 migrations and `pass=89 fail=0`; the focused route suite proved role-only
  request plus MFA-gated list/approval; Admin `pnpm typecheck && pnpm test && pnpm build` passed
  with the new security route and BFF allowlist tests. A final `pnpm verify:local` also passed after
  the migration/contract/UI additions. An initial SQL proof caught a recovery
  finalisation control-flow bug before acceptance; migration `0166` was corrected and the fresh
  suite passed afterward.

## Conditional-completion boundary

This is a local, self-reviewed completion only. It does not establish production passkey readiness.
Open release gates are: approved production RP ID/origin; real browser/device WebAuthn ceremony
evidence; deployed migration and forward-rollback rehearsal; external security review; and
independent fresh review.
