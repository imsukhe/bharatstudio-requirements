# L02 — Security, RLS and archive-integrity proof

**Status:** `Conditionally complete — isolated verification and mechanical remediation checks passed; independent review and application/security evidence pending`  
**Level:** L3  
**Owner:** Security / database  
**Depends on:** L01  
**Blocks:** production database provisioning and L10
**Security migration draft:** `/Users/sukhdevsingh/Workspace/Bharat Studio/bharatstudio-alerts/packages/db/migrations/0002_v1_security_rls_archive.sql`  
**Archive transfer migrations:** historical `/Users/sukhdevsingh/Workspace/Bharat Studio/bharatstudio-alerts/packages/db/migrations/0024_v1_l02_archive_transfer.sql`; effective retention correction `/Users/sukhdevsingh/Workspace/Bharat Studio/bharatstudio-alerts/packages/db/migrations/0047_v1_l02_soft_archive_only.sql`  
**Role prerequisite:** `/Users/sukhdevsingh/Workspace/Bharat Studio/bharatstudio-alerts/packages/db/roles/0001_v1_service_roles.sql`  
**Test record:** `../tests/L02-security-rls-and-archive-proof.md`

## Objective

Close the known launch-security residuals before production roles or data are created.

## Tasks

1. Use service-specific roles in the new topology: `bsa_app` is `NOBYPASSRLS`; the private Go payment and alert-worker identities have only the bypass scope their handlers require; migration/admin is separate; scheduler and clients have no database credentials. Do not copy the legacy broad `bsa_worker` scope.
2. Use transaction-scoped tenant context for pool-safe RLS; prove one tenant cannot read/write another tenant's records through every v1 route.
3. Ensure SECURITY DEFINER functions have fixed safe search paths, explicit owners and `REVOKE EXECUTE FROM PUBLIC`; grant only the service roles that need each helper. Document every privileged function, including the minimised active-channel public projection.
4. Prove archival conditions with tests: atomic copy/soft-mark relocation, destination completeness, source visibility rules, access audit, restore path, and no physical source/archive deletion.
5. Port/redesign least-privilege roles and secret access for TS API, Go payment service, Go alert worker, migration tooling and scheduler.
6. Add security regression tests for unauthenticated/webhook paths, SSRF/CORS/CSP/rate limits, secret redaction, overlay token rotation and soft account closure.

## Acceptance criteria

- No request path bypasses tenant isolation accidentally.
- Scheduler and companion clients have no direct database access.
- Archive transfer is evidenced, tested and auditable.
- Privileged functions and roles are least-privilege reviewed.
- Missing worker/payment credentials fail closed; no silent fallback from a service-specific role to the request role is allowed.
- No `SECURITY DEFINER` helper is callable by `PUBLIC`, and every helper has a fixed search path and negative-test coverage.
- Critical/high findings are fixed or explicitly blocked with owner and release gate.

## Rollback

Use isolated test/staging database only. Every role/policy migration has a tested rollback/recovery procedure before production use.

## Remediation follow-up — 2026-08-14

- F1 is closed for the isolated contract: `packages/db/roles/0001_v1_service_roles.sql` is the explicit role prerequisite and the L03 harness applies it before `0002`. It provisions no passwords; login/secret/IAM configuration remains deployment-owned.
- F2 is closed at the SQL-grant layer: `0002_v1_security_rls_archive.sql` revokes all archive access from `bsa_app` and `bsa_payment`, grants only `SELECT, INSERT` to `bsa_alert_worker`, enables RLS and defines worker-only policies. `packages/db/tests/l02_security_remediations.sql` asserts these exact grants and role attributes.
- The remediation harness now also audits every current `app_private` `SECURITY DEFINER` helper, not only the original L02 functions: each must carry a fixed `search_path` setting and `PUBLIC` must not retain `EXECUTE`. This protects later L03/L04/L05 migrations from reintroducing the same privilege-hardening gap.
- F3 is closed in the current contract tree: `queue-delivery.schema.json` declares `sourcePriority`, `overlay-reconnect-case.schema.json` validates the reconnect scenario, and the direct fixtures cover the six runtime schemas plus the separate multi-queue scenario. A cross-language validator still remains an L01/L07 evidence task.
- Archive transfer is now implemented as a narrow SQL primitive in `0024_v1_l02_archive_transfer.sql`, corrected by `0047_v1_l02_soft_archive_only.sql` to retain source rows. Only `audit_events` and `event_processing_attempts` are eligible; payment, refund, webhook and alert evidence are not eligible for this operational archive path. A separate `bsa_archive_owner` NOLOGIN role owns the `SECURITY DEFINER` functions and may mark source rows but cannot physically delete source or archive rows; only `bsa_alert_worker` can execute the functions. Normal `bsa_app` reads exclude marked rows, while restore clears the marker. The disposable harness verifies digest/completeness, soft archival, restore, repeat archival and PUBLIC-execute denial.
- Reran the disposable PostgreSQL proof on 2026-08-15: `L02_SECURITY_REMEDIATIONS=PASS` and `L03_APPLICATION_BEHAVIOR=PASS`, including RLS tenant isolation, archive soft-mark/restore, duplicate webhook concurrency, queue-independent delivery, overlay wake-up and Companion session boundaries. This remains isolated/local evidence; independent security review and deployment role/secret evidence remain open.

## Fresh local audit — 2026-08-15

The effective role prerequisite, security/RLS migrations, archive soft-mark
correction, current helper hardening assertions and L02 acceptance record were
rechecked after the L03–L10 local regression pass. No additional locally
verifiable L02 defect was found.

`L02_SECURITY_REMEDIATIONS=PASS` and `L03_APPLICATION_BEHAVIOR=PASS` remain
repeatable in the disposable PostgreSQL harness, including tenant isolation,
transaction-scoped context clearing, SECURITY DEFINER hardening, append-only
archive/restore, duplicate webhook concurrency, per-queue delivery and
Companion/session guards.

L02 remains conditional/open for independent security/application review,
production role/secret/IAM provisioning evidence, application-level negative
tests in the deployed topology, and a data-preserving rollback/restore drill.
No archival schedule is enabled by this audit.

## Deep-audit remediation — 2026-08-16

The role bootstrap was rechecked against the effective soft-archive migration
and exposed one real least-privilege mismatch: `bsa_archive_owner` was being
created with `BYPASSRLS`, while migration `0047` documents that the
`SECURITY DEFINER` owner must be `NOLOGIN` and `NOBYPASSRLS`. This is fixed by
changing `packages/db/roles/0001_v1_service_roles.sql` and adding forward
migration `0058_v1_l02_archive_owner_rls_hardening.sql`, which normalizes
existing installations and fails if the prerequisite role is missing.
`packages/db/tests/l02_security_remediations.sql` now asserts `NOLOGIN`,
`NOSUPERUSER` and `NOBYPASSRLS`. The disposable PostgreSQL harness passes after
the change.

This closes the local role-attribute mismatch only. Production role
provisioning, secret/IAM evidence, independent security review and rollback
rehearsal remain required before L02 can become `Verified`.
