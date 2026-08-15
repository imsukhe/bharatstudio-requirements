# Migration gap review — pooler, Razorpay identity, and D-2 routing

**Date:** 2026-08-14  
**Reviewer:** Codex self-review  
**Independent reviewer:** Not performed in this pass  
**Scope:** Current BharatStudio migration plan, launch authority, L01/L04/L05/L07/L08/L09 and task register

| Finding | Severity | Evidence | Disposition | Follow-up |
|---|---|---|---|---|
| Pooler/direct endpoint and cross-replica SSE transport were not explicit | P0 | Legacy `INFRASTRUCTURE_ROADMAP.md` and `OVERLAY_FANOUT.md`; current migration plan retained SSE without a concrete transport test | Fixed in requirements; v1 direct listener decision recorded; implementation pending | L01, L05, L09; verify before L10 |
| Razorpay deduplication did not name `x-razorpay-event-id` | P0 | Legacy webhook derived an event key with `Date.now()`; official Razorpay webhook guidance names the header | Fixed in requirements and Go verifier/SQL uniqueness path | L04; provider sandbox proof before L10 |
| Approved D-2 multi-queue routing and L-31/L-32 were absent from new authority | P0 | Legacy `MASTER-RELEASE-AUTHORITY.md` D-2; P11 queue plan | Fixed in authority and pending slice; implementation/proof pending | L01, L05, L09; bindings UI blocked until verified |
| Mobile framework/OS floor and release setup were not resolved before L07 | P0 | L07 required a decision before app code; desktop was locked but mobile was not | React Native selected; owner-approved floors are iOS 15.1+/Android API 26+; release accounts/signing remain open | L07; provision accounts and complete store review before submission |
| Legal/provider work was structurally delayed until Companion completion | P0 | L08 depended on L03/L04/L07 and deferred review | L08 split into early applications/review plus final implementation sign-off | L08; Razorpay/provider and legal evidence before L10 |
| Package rule made the build unnecessarily serial | P1 | Migration §6 and task register required previous package completion | Replaced with dependency-based waves; acceptance and final L10 gate remain mandatory | All tasks; recheck overlapping file ownership |

## Review result

The current requirements now carry the three decisions without copying the legacy repository wholesale. The documents remain planning-stage; no implementation, migration, provider configuration or production approval is implied.

## L00 freeze/inventory review

**Reviewer:** Codex self-review  
**Scope:** Legacy repository metadata and redacted secret-scan output  
**Result:** `Conditionally complete — owner confirmation required before L01`

- Commit `6679bf6bd8348b87ef76cb59877f285130abb648`, branch `master`, and clean working-tree state were recorded.
- 582 tracked files and top-level inventories were recorded in `LEGACY_EVIDENCE_REGISTER.md`.
- No secrets were printed or copied. The two redacted content-pattern matches—the archived `TASKS.md` and `pnpm-lock.yaml`—remain in the legacy snapshot and are explicitly excluded from migration; no manual clearing is required for the new v1 baseline.
- No tag was created because L00 explicitly requires owner confirmation before creating an immutable tag/archive reference.

## L01 definition review

**Reviewer:** Codex self-review  
**Scope:** v1 cross-language contract inventory, fixture/test matrix and logical database ownership  
**Result:** `Conditionally complete — static validation passed; independent review and isolated integration tests pending`

- Draft contract baseline is recorded in Alerts `contracts/CONTRACT_BASELINE.md`.
- Acceptance/test cases are recorded in `tests/L01-contracts-and-database-baseline.md`.
- OpenAPI YAML and all JSON artifacts parse successfully; the SQL draft was statically inspected and no database was provisioned or migrated.
- The contract and logical schema remain unapproved for production until isolated migration tests, RLS/security review and the required independent review are complete.

## L02 definition review

**Reviewer:** Codex self-review  
**Scope:** Service roles, transaction-scoped RLS context, SECURITY DEFINER hardening, archive-transfer boundary and negative-test matrix  
**Result:** `Conditionally complete — static review passed; isolated database and independent security review pending`

- Draft security migration contains 17 RLS-enabled tables, 20 explicit policies, five `SECURITY DEFINER` helpers and fixed `search_path` clauses.
- `PUBLIC` execution is explicitly revoked for privileged helpers; production grants remain deployment-controlled and must be least privilege.
- No hard-delete, role-creation, credential, provider URL or database execution was performed.
- `psql` was unavailable in this environment, so SQL execution and PostgreSQL-version validation remain pending.
- Legacy broad worker-bypass scope was not copied; the new draft uses service-specific private identities and no scheduler/client database credentials.

## L02 test-report follow-up

**Source:** Fresh isolated PostgreSQL 16 test report supplied by the user  
**Disposition:** Findings accepted; mechanical fixes applied; re-run pending

| Finding | Disposition |
|---|---|
| F1 — security migration referenced `bsa_app` without a role prerequisite | Fixed by adding `packages/db/roles/0001_v1_service_roles.sql` and linking it from L02. The role script contains no credentials. |
| F2 — archive permissions existed only as comments | Fixed with explicit `REVOKE ALL`, `GRANT SELECT, INSERT` to the private alert worker, RLS enablement and no update/delete policy. |
| F3 — source priority and fixture/schema coverage mismatch | Fixed by adding `sourcePriority` to the queue schema, completing direct queue fixtures, adding an overlay reconnect scenario schema, and adding direct fixtures for all six runtime schemas. |

The supplied PostgreSQL evidence was followed by corrected isolated PostgreSQL 16 reruns on 2026-08-14. The reruns passed migration execution, transaction-scoped tenant isolation on a reused connection, cross-tenant update denial, append-only archive permissions, ten-concurrent-identical-event deduplication, and the minimised active-channel public projection (closed/unknown handles returned no row). L02 is therefore `Conditionally complete`; an independent security review is still pending. SSE reconnect, cross-language code generation, credential fail-closed and header-trust tests remain application-level work.
