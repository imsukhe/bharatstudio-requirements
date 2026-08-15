# L02 acceptance and test record — security, RLS and archive integrity

**Status:** `Conditionally complete — isolated PostgreSQL 16 verification passed; independent review pending`  
**Task:** `../tasks/L02-security-rls-and-archive-proof.md`  
**Migration draft:** `/Users/sukhdevsingh/Workspace/Bharat Studio/bharatstudio-alerts/packages/db/migrations/0002_v1_security_rls_archive.sql`  
**Archive transfer migrations:** historical `/Users/sukhdevsingh/Workspace/Bharat Studio/bharatstudio-alerts/packages/db/migrations/0024_v1_l02_archive_transfer.sql`; effective retention correction `/Users/sukhdevsingh/Workspace/Bharat Studio/bharatstudio-alerts/packages/db/migrations/0047_v1_l02_soft_archive_only.sql`

All tests use synthetic identities and an isolated PostgreSQL database. No production or shared database may be used.

| ID | Setup/action | Expected result |
|---|---|---|
| L02-01 | Connect as `bsa_app` with no transaction context | Private tenant tables return zero rows and writes fail closed |
| L02-02 | Set a verified user/channel context inside a transaction and query channel A | Only channel A rows visible; commit clears context before connection reuse |
| L02-03 | Attempt channel B read/write using channel A context | Read returns no B rows; write is rejected; no cross-tenant side effect occurs |
| L02-04 | Attempt to set context from an untrusted browser/header value | Route rejects it; context is derived only from server-verified membership/overlay session data |
| L02-05 | Connect as payment and alert-worker identities through their private handlers | Each service can access only its documented global/append-only work; public routes cannot reach either identity |
| L02-06 | Omit the payment/worker role secret or alter the connected role | Service startup fails closed; no fallback to `bsa_app` occurs |
| L02-07 | Inspect all `SECURITY DEFINER` helpers | Fixed safe `search_path`, explicit owner, `PUBLIC` execute revoked, only named service roles granted; the remediation harness mechanically audits every current `app_private` helper |
| L02-08 | Submit unauthenticated, invalid-HMAC and replayed webhook requests | No business mutation; response follows retry/quarantine policy; secrets and raw payloads are not logged |
| L02-09 | Exercise CORS, CSP, SSRF, rate-limit, overlay-token rotation and revocation cases | Only approved origins/targets pass; revoked/expired tokens fail; no internal metadata is exposed |
| L02-10 | Copy a synthetic event to `archive_records`, verify digest/completeness, then soft-archive the source in one transaction | Destination is complete before the source is hidden; the source row remains internally present and marked; restore clears the marker |
| L02-11 | Attempt UPDATE/DELETE on archive and financial evidence as app/worker roles | Operation is denied; only the approved soft-archive path can mark eligible operational evidence |
| L02-12 | Soft-close a channel/user and exercise every private/public read path | Access is revoked while payment evidence remains traceable and no hard-delete occurs |
| L02-13 | Call the public-channel projection as `bsa_app` for active, closed and unknown handles | Only the minimised active projection is returned; closed/unknown handles return no row; private channel columns remain inaccessible |
| L02-14 | Invoke the approved operational archive transfer and restore path as `bsa_alert_worker`; attempt PUBLIC execution | Only whitelisted operational source tables can be marked; archive digest and row identity are verified before soft archival; source rows remain retained and normal reads hide them; restore clears the marker; repeated transfer is idempotent; PUBLIC cannot execute either function | `0024_v1_l02_archive_transfer.sql` is historical; `0047_v1_l02_soft_archive_only.sql` is effective; `l03_application_behavior.sql`; `pnpm db:test:l03`; pass |

## Closure evidence

- Isolated PostgreSQL version/plan and migration command recorded.
- Role attributes, grants, policy definitions and negative tests captured without secrets.
- Transaction-context leak test across pooled connection reuse.
- Archive copy/digest/restore/failure-injection output.
- Fresh independent security review with all P0/P1 findings dispositioned.

Document inspection alone cannot close an L02 test.

## 2026-08-14 isolated verification evidence

Executed against a fresh disposable `postgres:16-alpine` container after the F1–F3 fixes:

- Role prerequisite, baseline migration and security migration executed successfully.
- The four initial runtime/migration roles, 17 RLS-enabled tables and 20 policies were present. Migration `0024` additionally provisions the separate `bsa_archive_owner` NOLOGIN function-owner role; it is not a runtime client identity.
- Reused-connection transaction test: user A saw only A's payment; after commit, user B on the same connection saw only B's payment.
- Cross-tenant update test: user A's update against channel B affected zero rows.
- Archive test: `bsa_alert_worker` invoked the corrected `0047` soft-archive path for a synthetic `audit_events` row; destination digest/identity was verified, the source row remained present with an archive marker and was hidden from normal reads, restore cleared the marker, repeat archival succeeded, and PUBLIC execution was denied. Direct source/archive DELETE remains denied to both runtime and archive-owner roles.
- Ten concurrent identical webhook inserts produced exactly one row under the provider/environment/account/event uniqueness constraint.
- Public projection test: `bsa_app` received only the approved active-channel fields; closed and unknown handles returned no row.
- Remediation assertion: `l02_security_remediations.sql` passed, confirming the role prerequisite, `bsa_app` NOBYPASSRLS, private-role bypass scope and append-only `archive_records` grants. The same run also mechanically audited every current `app_private` `SECURITY DEFINER` helper: each has a fixed `search_path` and `PUBLIC` no longer retains `EXECUTE`.
- Current fixture tree includes the direct `queue-delivery`, `overlay-sse-event`, `alert-event`, `entitlement-result`, `error-envelope` and `payment-webhook-delivery` fixtures, plus the dedicated `overlay-reconnect-case` and multi-queue scenario shapes.

This closes the isolated database portion conditionally. It does not replace the independent security review or the application-level tests listed above.

## 2026-08-15 rerun

The disposable PostgreSQL harness was rerun after the L03–L05 evidence
reconciliation. It returned `L02_SECURITY_REMEDIATIONS=PASS` and
`L03_APPLICATION_BEHAVIOR=PASS`, with the same RLS, archive, webhook-dedup,
multi-queue, overlay-wakeup and Companion-session checks passing. No external
database, provider credential or production role was used.

## Fresh local audit evidence — 2026-08-15

No additional local failure was found when the effective migrations, role
prerequisite, security assertions, archive tests and L02 closure criteria were
checked together. The status remains conditional rather than `Verified`:
independent review, deployed role/secret/IAM evidence, application/deployment
negative tests and data-preserving rollback/restore rehearsal are still
required.
