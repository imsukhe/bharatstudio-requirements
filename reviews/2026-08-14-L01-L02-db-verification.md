# Review record — L01/L02 database-layer verification

**Reviewer/agent:** Claude (Opus 5), this session
**Scope:** Everything in L01/L02's pending lists that can be tested against
the committed SQL artifacts alone, in an isolated database, without
application code (Go payment service, Go alert worker, TypeScript Creator
API, mobile/desktop clients) that does not yet exist.
**Environment:** Fresh `postgres:16-alpine` container, isolated from both
the legacy repo's DB (port 5433) and any other running database. Torn down
at the end of this session.
**Method:** Real `psql` execution against the committed migration files,
with output captured, not inferred. Every claim below has a command and its
actual output behind it.

**This record does not itself change L01/L02's status.** It provides
evidence for the owner/reviewer to weigh. Several items below are findings,
not passes.

**Current disposition note — 2026-08-15:** The original F1/F2/F3 findings
below are historical evidence. Their remediations are recorded and rerun in
the follow-up section: role prerequisites now exist, archive grants are
executable and tested, and the fixture/schema coverage is corrected. The
remaining status is conditional because independent review, deployment
hardening and application/staging evidence are still open.

**Contract follow-up — 2026-08-15:** `pnpm contracts:validate` now parses the
OpenAPI 3.1 document, verifies all 29 paths and resolves every local `$ref`,
in addition to validating the ten JSON fixture/schema mappings with format
enforcement. Cross-language consumer and independent-review evidence remain
open.

---

## Verified — real evidence, no findings

| # | Item | Evidence |
|---|---|---|
| 1 | `0001_v1_baseline.sql` runs clean in isolation | 17/17 objects created, zero errors |
| 2 | Schema drop + full re-apply from empty state | 17 objects recreated, zero errors — the schema is reproducible, not just runnable once |
| 3 | Cross-tenant `SELECT` isolation | User A (`bsa_app`, `app.user_id` set) reads own channel (1 row), Channel B (0 rows), own payment (1 row), **Channel B's payment (0 rows — financial data)** |
| 4 | Cross-tenant `UPDATE` isolation | `UPDATE channels SET display_name='HACKED'` against Channel B as User A → `UPDATE 0`. Confirmed as superuser the row is genuinely unmodified, not silently permitted |
| 5 | Transaction-scoped context clears on a **reused connection** | Same session: User A's `set_config(..., true)` inside a transaction is invisible after `COMMIT`; a second transaction on the *same connection* for User B sees only User B's data; context clears again after. This is the actual pool-safety claim, tested, not assumed |
| 6 | `SECURITY DEFINER` hardening | All 4 functions: fixed `search_path`, explicit owner, `PUBLIC` execute = false, confirmed via `pg_proc`/`has_function_privilege` |
| 7 | Duplicate webhook dedup under **real concurrency** | 10 simultaneous `INSERT ... ON CONFLICT DO NOTHING` for the same `(provider, environment, connected_account_ref, provider_event_id)` → exactly 1 row persisted |
| 8 | Independent multi-queue delivery | One event routed to two queues as two separate `event_outbox_deliveries` rows; advancing Queue 1 to `displayed` left Queue 2 at `pending`; a duplicate `(outbox_id, queue_id)` row was rejected by the unique constraint |
| 9 | Worker-only tables are structurally unreachable by `bsa_app` | `SELECT` against `event_outbox` as `bsa_app` → `permission denied` (no table grant exists, stronger than an RLS 0-row filter) |
| 10 | FK cascade safety | `payments.channel_id` → `channels.id` is `NO ACTION`, not `CASCADE` — a channel cannot be deleted out from under payment evidence |

---

## Findings — real gaps, with evidence

| # | Severity | Finding | Evidence | Disposition |
|---|---|---|---|---|
| F1 | **High** | `0002_v1_security_rls_archive.sql` cannot run standalone in an isolated database. 18 `CREATE POLICY ... TO bsa_app` statements fail with `role "bsa_app" does not exist` | First run: 18 errors at lines 149–236. Only succeeded after I hand-created `bsa_app`/`bsa_payment`/`bsa_alert_worker`/`bsa_migrator` myself, matching the role contract documented in the file's own header comment | **No role-provisioning SQL exists anywhere in the repository tree** (searched for `create role`, `*role*.sql`, `*provision*.sql` — zero hits). L02 task 5 ("port/redesign least-privilege roles") has no artifact yet. This is not a defect in `0002`'s design — its header is explicit that role creation is deployment's job — but it means L02's own pending item "run the security migration in isolated PostgreSQL" cannot currently be executed by a third party without first writing a script this repo doesn't have. **Owner action:** add a `0000_roles.sql` (or equivalent) before this is called runnable |
| F2 | **High** | Archive-transfer hardening is **prose, not SQL** | `archive_records` table: zero grants exist for `bsa_app`, `bsa_payment`, or `bsa_alert_worker` — checked directly against `information_schema.table_privileges`. The file's own comment at line 258 says *"Deployment must explicitly revoke UPDATE/DELETE from request and worker roles, grant insert/select only to the approved archival handler"* — but unlike the `SECURITY DEFINER` functions three sections earlier (where the equivalent hardening **is** real `REVOKE` statements, not a comment), this one was never turned into executable SQL | The file treats two structurally identical hardening requirements inconsistently. L02 task 4 ("prove archival conditions with tests") cannot be attempted yet — there is no grant model to test against, only a description of one |
| F3 | **Medium** | 2 of 3 committed fixtures **fail schema validation**; 4 of 6 schemas have **zero fixture coverage** | Mechanically validated with `jsonschema` (Draft 2020-12), not read by eye:<br>• `payment-webhook-duplicate.json` → valid against `payment-webhook-delivery.schema.json` (both items) — **the one fixture that passes**<br>• `multi-queue-delivery.json` → **fails** against `queue-delivery.schema.json`: both delivery items carry `sourcePriority`, a field the schema does not declare, and `additionalProperties: false` rejects it<br>• `overlay-reconnect.json` → matches **none** of the 6 schemas; no schema for an "overlay reconnect scenario" exists — this isn't a fixable fixture typo, a new schema needs to exist<br>• `alert-event`, `entitlement-result`, `error-envelope`, and `overlay-sse-event` schemas have no fixture exercising them at all | L01's own acceptance criterion requires named delivery-identity fields be present and correct; the fixture testing exactly that — `sourcePriority`, the field `L-31`/`L-32` depend on — is the one that fails. Fix candidates: either add `sourcePriority` to `queue-delivery.schema.json`, or move it to a separate test-scenario wrapper schema that doesn't constrain the production delivery shape. Either way, `L01` task 4's "cross-language golden fixtures" cannot be called done while 2 of 3 fail their own schemas |
| F4 | **Note, not a defect** | "Rollback tested" in this record means *drop-and-recreate-from-empty*, proven reproducible. **No down-migration or data-preserving revert script exists.** | Confirmed by inspection — only `0001_v1_baseline.sql` and `0002_v1_security_rls_archive.sql` exist; no `..._down.sql` or equivalent | If "rollback" in L01's pending list is meant to cover reverting a *later* migration while preserving earlier data (the real production scenario), that is untested and has no artifact yet. What's proven here is narrower: the schema is not one-way-runnable garbage — it is genuinely reproducible from nothing |

---

## Not testable yet — no application code exists

These require the Go payment service, Go alert worker, TypeScript Creator
API, or mobile/desktop clients — none of which have been written. Listed so
they are not silently skipped, per this repo's own review-record
convention.

- SSE reconnect/replay across replicas (needs a running overlay/SSE server)
- Cross-language fixture checks for TS/Go/React Native/C#/Swift (needs
  codegen tooling wired to consume the JSON Schemas — none configured yet)
- Service credentials failing closed with no silent fallback (an
  application startup behaviour, not a database property)
- Untrusted client headers cannot set tenant context (this is enforced by
  the *application* choosing to call `set_config` from a verified session,
  not by the database — the database imposes no barrier against a
  misbehaving caller with a valid `bsa_app` connection; this is worth
  stating precisely rather than as a pass)
- Webhook, CORS, CSP, SSRF, rate-limit, overlay-token security (application
  middleware, doesn't exist)
- Soft-close/account-revocation as a full flow (the schema supports it —
  `closed_at` is nullable, no destructive trigger exists — but the actual
  revocation handler and its ordering guarantees are application code)

## Not mine to certify

- Database region/plan approval — already decided elsewhere (Neon Launch,
  Singapore `ap-southeast-1`) and is an owner decision, not a database test
- Exact REST paths/fields/error codes — a specification decision against
  `contracts/openapi/v1.yaml`, not something a database test resolves
- Independent architecture review (L01) / independent security review (L02)
  — by definition cannot be this same session; a second, separate reviewer
  context is required per this repo's own `AGENTS.md`/`CLAUDE.md` rule

---

## Recommended status

**Neither L01 nor L02 should move to `Verified` from this record alone.**

What changes:
- The **structural/DB-layer half** of both lists now has real, reproducible
  evidence — 10 items — rather than "statically reviewed."
- **F1 and F2 are High-severity gaps** that block calling either migration
  file deployment-ready as committed: one has no role-provisioning artifact
  to run against, the other has hardening described but not implemented.
- **F3 blocks the fixture-validation item outright** — it does not pass
  today, mechanically confirmed.
- The applic­ation-layer half of both lists remains genuinely untested,
  because the application does not exist yet — this is expected at this
  stage, not itself a finding.

**Suggested next action:** F1 and F2 are small, mechanical fixes (a roles
script; turning the archive-grant comment into `REVOKE`/`GRANT`
statements) and should be closed before anyone treats `0002` as
deployment-ready. F3 needs an owner decision on which fixture/schema is
wrong. None of the three block continued planning work; all three block
calling L01/L02 `Verified`.

## Remediation follow-up — 2026-08-14

The three findings above were rechecked against the current tree after the
original review:

- F1 is remediated for isolated execution by
  `packages/db/roles/0001_v1_service_roles.sql`; the L03 harness applies it
  before `0002` and `l02_security_remediations.sql` asserts the role
  attributes. It intentionally creates no passwords or production IAM.
- F2 is remediated in `0002_v1_security_rls_archive.sql` with explicit
  `REVOKE`/`GRANT` statements and worker-only RLS policies; the same SQL
  assertion confirms append-only worker access.
- F3 is remediated in the current contract tree: `sourcePriority` is declared
  by `queue-delivery.schema.json`, `overlay-reconnect-case.schema.json` is
  present, and direct fixtures exist for each runtime schema. A real
  cross-language validator and independent L01/L02 review are still open.

This follow-up supersedes the three findings' *current* disposition, but does
not erase the original evidence or move either lane to `Verified`.

The fixture/schema claim was subsequently executed: the repository validator
now validates all ten committed fixtures with Ajv Draft 2020-12 and
`ajv-formats`, including `uuid`, `date-time` and `uri` enforcement and the
duplicate-webhook wrapper schema. Cross-language consumers and independent
review remain open.

## Application-layer follow-up — 2026-08-15

- The TypeScript Creator API now has local authentication, public projection,
  payment-boundary, maintenance, queue/configuration, overlay-session and
  metrics/readiness tests. The Go payment and alert-worker services have
  local authorization, persistence, task, replay, release/acknowledgement and
  readiness tests. These are local evidence, not deployment or independent
  review evidence.
- Overlay SSE reconnect and cursor acknowledgement are covered by local
  adapter tests and the disposable PostgreSQL harness. Cross-replica
  notification outage, direct-endpoint deployment and browser/OBS staging
  evidence remain open.
- Credential fail-closed behavior and header-only overlay token transport are
  covered locally. Production IAM, secret provisioning, provider sandbox and
  cross-language client consumption remain open.
- Mobile/desktop application code, app-store signing, legal/privacy review,
  and the creator configuration schema/preview matrix are not yet implemented
  or verified.

## Archive-transfer follow-up — 2026-08-15

The earlier archive evidence proved only direct append-only insertion. That
was insufficient for L02-10's archive-integrity requirement. Historical
`0024_v1_l02_archive_transfer.sql` introduced the narrowly
whitelisted transfer and restore function for `audit_events` and
`event_processing_attempts`; effective migration
`0047_v1_l02_soft_archive_only.sql` supersedes its physical-delete step.
The effective path copies and verifies the record, marks the source with
`archived_at`/`archived_by`, hides it from normal `bsa_app` reads, and retains
the source and archive rows internally. It uses a separate
`bsa_archive_owner` NOLOGIN role so the runtime worker does not receive
direct archive mutation privileges; only `bsa_alert_worker` can execute the
functions. The disposable PostgreSQL harness proves source-row locking,
digest/completeness verification before soft archival, restore, repeat
archival, no physical source/archive deletion privileges, and no `PUBLIC`
execution of either function.

The original `0024` SQL is retained as migration history and must never be
executed as an isolated current-state archive implementation; deployment
must apply `0047` before enabling any archival operation.

This closes the local archive-transfer proof slice. It does not authorize
production archival schedules, does not apply to payment/refund/webhook or
alert evidence, and does not replace independent security review, deployment
IAM review, staging failure injection or a data-preserving rollback drill.
