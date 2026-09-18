# TC-CTL-13 — platform-admin MFA acceptance plan

**Task:** `../active/tasks/CTL-13.md`  
**Status:** `Conditionally complete locally; external/device/release evidence pending`

The selected passkey plan must prove enrollment/bootstrap, user-verified assertion, challenge
single-use, origin/RP ID validation, signature/counter enforcement, session expiry/re-authentication,
durable platform-admin authorization, local-development isolation, audit redaction, approved
five-minute challenge and fifteen-minute elevation bounds, and denial of every privileged
control-plane route when assertion state is absent or invalid. It must also prove that a recovery
request is self-targeted, expires, cannot self-approve, requires two distinct current MFA approvers
including the owner, revokes every old passkey/session atomically, and stores no recovery secret or
free-form reason. Production RP/origin values and real-device evidence remain external release gates
and cannot be claimed from local mocks.

## Local proof executed 2026-09-18

1. A fresh PostgreSQL container applied every role and migration through `0165`, loaded synthetic
   fixtures, then ran `packages/db/tests/ctl_admin_passkeys.sql`: `CTL_ADMIN_PASSKEYS=PASS`.
   This proves direct-table privilege lockdown, non-admin denial, hash-only challenge state, challenge
   single-use, session isolation, counter progression and redacted append-only audit events.
2. `pnpm --filter @bharatstudio/alerts-api exec tsx --test test/admin-passkeys-routes.test.ts`
   passed 3/3: configuration absence fails closed, options are session-bound and do not serialize a
   bearer token, and malformed ceremony responses cannot finalize durable state.
3. Every operational `/v1/admin/*` route is now passkey-gated. Only the identity-only `whoami` and
   MFA ceremony bootstrap routes retain the platform-admin-only gate. Focused privileged-route tests
   cover explicit `428 admin_mfa_required` denial, including creator-pack review operations.
4. `pnpm verify:local` passed on the final working tree: contract/fixture validation (158 paths,
   185 operations), explain/harness/deployment checks, 89 isolated SQL proofs, load/fault checks,
   Alerts API/web/measurement suites, API/web builds, Go race/vet tests, and all three command-image
   builds. `bharatstudio-admin` `pnpm typecheck && pnpm test && pnpm build` also
   passed (4 unit tests, including a strict BFF allowlist test).

The first full SQL-suite attempt exposed a PostgreSQL invalid-regex defect in the new migration;
it was corrected with `char_length` plus a character-class check and the final full pipeline passed.
This acceptance record remains conditional because local synthetic checks cannot prove the external
release gates stated above.

## Recovery-policy proof executed 2026-09-18

1. `sh packages/db/tests/run-sql-suite.sh 0166` applied 166 migrations to a fresh template and ran
   89 isolated SQL proofs, all passing. `ctl_admin_passkey_recovery.sql` proves function-only table
   access, self-approval denial, no revocation after just the owner approval, completion only after
   a distinct staff approval, append-only four-event audit and atomic revocation of every target
   credential/session.
2. `pnpm --dir apps/api exec tsx --test test/admin-passkeys-routes.test.ts test/app.test.ts` passed:
   request is available only to the durable platform-admin role; list/approve reject a role-authorised
   session without current MFA; configured recovery responses are BFF-safe; and production config
   fixes the approved 300-second ceremony/900-second elevation values while requiring a canonical
   matching RP/origin pair.
3. `bharatstudio-admin` `pnpm typecheck && pnpm test && pnpm build` passed after adding the
   self-request and protected approval-queue surfaces. Its allowlist proof accepts only the exact
   recovery endpoints and a canonical UUID approval path, rejecting traversal and arbitrary token
   relay paths.
