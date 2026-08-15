# L06 — Scheduler boundary and private maintenance handlers

**Status:** `Local scheduler/maintenance slices passing — private handlers, IAM, deployed recovery and staging proof pending`
**Level:** L3  
**Owner:** Infra / SRE / Alerts  
**Depends on:** L04, L05  
**Blocks:** payment recovery, archival and release readiness

## Objective

Keep `bharatstudio-crons` scheduler-only while moving every scheduled mutation behind private, idempotent Alerts handlers.

## v1 scheduled responsibilities

- payment-status reconciliation and captured-payment-without-alert recovery;
- refund/dispute reconciliation;
- event lease/dispatch recovery only where Cloud Tasks/outbox design requires it;
- overlay expiry reminders and token maintenance;
- archival maintenance and audit log archival;
- subscription grace cancellation/price-protection scheduling when their calendar date becomes relevant.

## Tasks

1. For each schedule, define owner, target endpoint, OIDC service account, schedule, input schema, idempotency key, timeout, retry/backoff, dead-letter/alert and disable/rollback action.
2. Implement private Alerts endpoints that perform each mutation transactionally; validate OIDC audience/identity and reject public access.
3. Create schedule definitions and smoke tests in `bharatstudio-crons`; no SQL, provider credentials or business mutation code there.
4. Create infrastructure/IAM in `bharatstudio-infra` with least privilege and environment isolation.
5. Keep scheduler targets bound to the canonical deployment service ID (`alerts-api`, `payment-webhook`, or `alert-worker`) as well as the human/runtime service name; both are required before enablement.
6. Define the authenticated request contract for every target: JSON `POST`, concrete UTC window and stable `schedule:<id>:<window>` idempotency key.
5. Prove duplicate schedule firing, delayed execution, target timeout, partial provider outage, and manual replay are safe.
6. Document operations dashboard, missed-run alert, backlog alert, run audit and recovery playbook.

## Current implementation evidence — 2026-08-15

- Added scheduler-only `bharatstudio-crons/contracts/schedule-contract.json` with private Alerts target, UTC schedule, OIDC identity/audience, timeout, retry/dead-letter, idempotency and rollback requirements.
- Added disabled `bharatstudio-crons/schedules/v1.json` definitions for payment reconciliation, refund reconciliation, outbox recovery, overlay-session maintenance, event archival and audit archival. The template contains no SQL, provider credentials or database connection field. Payment reconciliation targets the payment service's private status/recovery route; outbox recovery targets the private `bharatstudio-alert-worker/internal/v1/tasks/pump` endpoint directly; other maintenance schedules target the Alerts API.
- Added `bharatstudio-crons/tests/schedule-contract.test.mjs`; `npm test` passes with all schedules disabled and private target checks.
- Added the Alerts API private maintenance route shell for all six schedule paths. It requires a Google OIDC service identity, strict job/idempotency input and an injected transactional store; without the store it returns retryable `503`, so a schedule cannot create a false success. Added Google ID-token verification and production/staging audience configuration requirements.
- Added migration `0011_v1_l06_maintenance_runs.sql` and `createSqlMaintenanceStore`. The private boundary records each scheduler run through `app_private.accept_maintenance_run`; the `(job, idempotency_key)` constraint prevents a second row, unfinished runs remain retryable, and only a completed run returns `already_completed`. No direct table grant is given to the app role. The disposable PostgreSQL harness proves the first run is accepted and the duplicate is not inserted twice.
- Implemented the first concrete API maintenance mutation in `0016_v1_l06_overlay_session_maintenance.sql`. `overlay-sessions` accepts the run and soft-revokes expired sessions in one database transaction, then marks the run completed; duplicate execution is a no-op. The API SQL store now rejects payment/refund/outbox/archive jobs because those mutations belong to their payment/worker/archive owners and are not allowed to become ledger-only false successes.
- Added the L02 archive-transfer primitive in Alerts migration `0024_v1_l02_archive_transfer.sql`, then corrected it with `0047_v1_l02_soft_archive_only.sql` so eligible operational source rows are retained and marked rather than physically deleted. This is only a database capability; it is not yet a scheduled archive handler. Event/audit archive schedules remain disabled until an owner-specific private handler, retention eligibility rule, OIDC binding, failure/replay proof and legal/retention approval exist.
- Corrected ownership: the scheduler no longer routes payment/refund reconciliation through the API ledger shell or outbox recovery through the API's ledger-only `outbox-recover` route. Payment and refund reconciliation run in the payment service, which owns the provider client and compensating recovery mutations; outbox recovery invokes the worker pump, which can list ready rows and create stable Cloud Tasks tasks. The worker never acknowledges a row merely because a schedule fired. The schedule contract and crons test assert the distinct services and audiences. OIDC binding, deployed audiences and staging proof remain open.
- Tightened the scheduler contract so every schedule must declare a five-field UTC schedule, bounded timeout, monitoring signal, dead-letter signal, retry policy, idempotency key and rollback action. The disabled v1 fixtures now provide those fields and the crons test rejects an incomplete schedule shape; `npm test` passes.
- Added `bharatstudio-crons/docs/SCHEDULER_OPERATIONS.md`, mapping every disabled v1 schedule to outcome, failure, dead-letter, freshness/backlog, disable/replay and rollback handling. The runbook explicitly keeps durable business state owned by the target service, forbids scheduler credentials/direct database work, and lists the evidence required before enablement. The contract test verifies that every schedule has its declared monitoring/dead-letter signals covered; live monitoring and rehearsal remain open.
- Added an explicit `implementationStatus` to every scheduler definition. Payment/refund reconciliation, outbox recovery and overlay-session maintenance are marked `implemented` but remain disabled until deployment evidence exists; event/audit archival are marked `planned` and are mechanically required to remain disabled. This prevents a syntactically valid schedule from being mistaken for a live handler and blocks accidental activation of the unsupported archive targets.
- Narrowed the Alerts API maintenance route to its currently implemented owner, `overlay-sessions`. Payment/refund jobs and outbox recovery are rejected before the API store is called because they belong to the private Go payment and alert-worker services; archive jobs remain disabled until their retention and handler contracts are approved. This prevents an unsupported scheduler target from returning a false success.
- Re-ran the full local regression slice after the ownership correction: the Alerts API suite (current run 54/54), production build, contract validation, disposable PostgreSQL L02/L03 harness, payment/worker Go tests plus vet/race checks, scheduler contract, mobile checks and macOS check all passed. The database harness included duplicate maintenance-run calls, overlay-session expiry and retry, cross-service job rejection, multi-queue independent delivery projection and durable Companion test-alert creation. Earlier historical counts in this document remain historical.

The schedule files are not enabled and do not claim endpoint, IAM, provider or staging readiness.

## Deployment-boundary evidence — 2026-08-15

The infrastructure contract links Scheduler to the scheduler-only repository,
requires private OIDC invocation, forbids scheduler database credentials and
keeps scheduling disabled until deployment evidence exists. The contract
validator passes 8/8 in `bharatstudio-infra`; this does not prove Cloud
Scheduler IAM, target deployment or fault-injection recovery.

## Fresh local audit — 2026-08-15

The scheduler-only contract and current maintenance boundary were re-read
against the checked-in cron definitions, API route, SQL store, migrations,
operations runbook and infrastructure manifest.

Confirmed locally:

- all six v1 schedule templates remain disabled;
- the cron repository contains no database credential, SQL, provider secret or
  business mutation implementation;
- payment and refund reconciliation target the private Go payment service;
- outbox recovery targets the private Alert Worker pump;
- the Alerts API accepts only its implemented `overlay-sessions` maintenance
  job and rejects cross-service/archive jobs before ledger acceptance;
- the overlay-session run is transactionally idempotent and soft-revokes
  expired sessions without deleting payment, alert or session evidence;
- schedule definitions require OIDC metadata, UTC cadence, bounded timeout,
  retry/dead-letter, monitoring, idempotency and rollback fields;
- each schedule declares whether its target is `implemented` or `planned`, and
  planned archive schedules are tested as disabled;
- the infrastructure template keeps Scheduler disabled, private-OIDC-only and
  forbidden from holding direct database credentials.

No additional locally verifiable L06 defect was found in this audit. L06 is not
release-verified: the remaining work is deployed OIDC/IAM proof, owner-specific
archive handlers, monitoring wiring, duplicate/timeout/outage/
dead-letter/manual-replay staging rehearsal, and production enablement approval.
Do not enable an unimplemented schedule merely because its template validates.

The payment and refund reconciliation handlers are now the owner-specific
private Go routes named by the scheduler contract and are covered by their
local unit/race/vet and disposable database integration checks. Their remaining
L06 work is deployment configuration and provider/staging evidence, not a new
handler implementation. Event/audit archive handlers remain unimplemented and
must stay disabled until retention eligibility, restricted access, replay and
legal approval are evidenced.

## Acceptance criteria

- No scheduler identity can access the database directly.
- No maintenance endpoint is public.
- Every scheduled action is idempotent, auditable, monitored and manually disableable.
- Reconciliation and archival paths pass staging recovery tests.
- A duplicate delivery for the same job/idempotency key returns the existing run and cannot create a second maintenance-run ledger row.
- A crash after payment persistence but before the immediate pump call is recoverable by the scheduled worker pump; repeated scans remain safe because durable ready rows and stable task names are authoritative.

## Rollback

Disable the schedule before disabling the endpoint. Preserve work item/audit state and use an approved manual recovery invocation; never rerun SQL by hand against production.

If the worker pump is unavailable, leave ready deliveries durable and page the Alerts/SRE owner; do not mark them completed through the API maintenance ledger.

## Automatic continuation verification — 2026-08-15

`bharatstudio-crons` `npm test` passed 2/2. The disabled schedule catalogue,
required OIDC/UTC/timeout/retry/dead-letter/idempotency/monitoring/rollback
fields and operations coverage checks remain green. No schedule was enabled.

`bharatstudio-infra` `npm test` passed 8/8. The deployment template continues
to enforce disabled task/scheduler state, private worker ingress, event-ID
deduplication metadata, pooled-listener prohibition, private observability and
required pre-deploy gates.

This does not close deployed Scheduler IAM, target readiness, live monitoring,
provider recovery, archive ownership/legal approval or staging rehearsal.
