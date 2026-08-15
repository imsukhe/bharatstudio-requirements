# L06 acceptance and test record — scheduler boundary

**Status:** `Local scheduler/maintenance slices passing — private handlers, IAM and staging evidence remain open`  
**Task:** [`../tasks/L06-scheduler-boundary.md`](../tasks/L06-scheduler-boundary.md)  
**Repository:** `/Users/sukhdevsingh/Workspace/Bharat Studio/bharatstudio-crons`

| ID | Setup/action | Expected result | Evidence |
|---|---|---|---|
| L06-01 | Load the v1 schedule document | Every schedule has owner, private target, five-field UTC cadence, bounded timeout, retry/dead-letter, idempotency, monitoring and rollback fields | `npm test`; pass |
| L06-02 | Inspect scheduler definitions for credentials or direct mutation fields | No database DSN, secret, SQL/business mutation or public endpoint is present | `tests/schedule-contract.test.mjs`; pass |
| L06-03 | Attempt to treat a disabled template as deployable | Test and README keep every schedule disabled until endpoint/IAM/staging gates are recorded | `schedules/v1.json`; pass |
| L06-04 | Call a maintenance path without OIDC, with OIDC but no transactional store, and with a verified store | Public/unauthorized calls fail; unconfigured handlers return retryable 503; verified idempotent jobs reach only the injected store | `apps/api/test/app.test.ts`; current API suite 54/54 and build pass |
| L06-05 | Submit the same unfinished private maintenance job twice to the database boundary | Both attempts refer to one ledger row; the unfinished run remains retryable rather than being mislabeled completed. A genuinely completed run returns `already_completed` | `0011_v1_l06_maintenance_runs.sql`, `0016_v1_l06_overlay_session_maintenance.sql`, `l03_application_behavior.sql`; `pnpm db:test:l03`; pass |
| L06-06 | Load the scheduler contract with payment-reconciliation and outbox-recovery schedules | Payment reconciliation targets only the private payment-service route; outbox recovery targets only the private Alert Worker pump; remaining schedules stay on the Alerts maintenance boundary; no schedule contains credentials or direct SQL | `bharatstudio-crons/contracts/schedule-contract.json`, `schedules/v1.json`, `tests/schedule-contract.test.mjs`; `npm test`; pass |
| L06-07 | Run `overlay-sessions` maintenance, repeat the same run, and submit an API-owned payment/archive job to the SQL maintenance store | Expired overlay sessions are soft-revoked and the run becomes `completed` in one transaction; repeat execution is `already_completed`; jobs owned by another service fail before ledger acceptance | `packages/db/migrations/0016_v1_l06_overlay_session_maintenance.sql`, `packages/db/tests/l03_application_behavior.sql`, `apps/api/src/db/maintenance-store.ts`; `pnpm db:test:l03`, API typecheck; pass |
| L06-08 | Invoke the Alerts maintenance HTTP route with `outbox-recover` using a verified service identity | The route rejects the cross-service job before calling the API store, so an unsupported target cannot return a false 202 | `apps/api/src/routes/maintenance.ts`, `apps/api/test/app.test.ts`; API test suite; pass |
| L06-09 | Inspect scheduler operations contract and map every disabled schedule to monitoring, backlog/freshness, dead-letter, disable, replay and rollback rules | Every schedule has an owner-specific operational path; failures remain retryable/actionable; no rule authorizes deleting, acknowledging or rewriting durable business evidence; no scheduler credential or direct database operation is introduced | `bharatstudio-crons/docs/SCHEDULER_OPERATIONS.md`, `tests/schedule-contract.test.mjs`; `npm test`; local pass; deployed monitoring and rehearsal evidence pending |
| L06-10 | Load the schedule catalogue with the runtime route ownership map | Every schedule declares `implementationStatus`; planned event/audit archive targets are disabled and cannot be treated as available routes; implemented payment/refund/worker/overlay targets remain disabled until deployment evidence | `bharatstudio-crons/contracts/schedule-contract.json`, `schedules/v1.json`, `docs/SCHEDULER_OPERATIONS.md`, `tests/schedule-contract.test.mjs`; local pass |
| L06-11 | Compare scheduler target identity with the deployment service boundary | Every schedule declares the canonical `serviceId` used by `bharatstudio-infra`; payment/refund map to `payment-webhook`, outbox recovery maps to `alert-worker`, and Alerts maintenance maps to `alerts-api`; an unrecognised or mismatched ID fails the scheduler contract | `bharatstudio-crons/contracts/schedule-contract.json`, `schedules/v1.json`, `bharatstudio-infra/deployment/v1/manifest.template.json`, `tests/schedule-contract.test.mjs`; local pass |
| L06-12 | Materialise the scheduler HTTP request from a schedule entry | Every target is a JSON `POST` with a concrete-window body and stable `schedule:<id>:<window>` idempotency key; missing method/body/identity data fails the schedule contract | `bharatstudio-crons/contracts/schedule-contract.json`, `schedules/v1.json`, `docs/SCHEDULER_OPERATIONS.md`, `tests/schedule-contract.test.mjs`; local pass |

### Local rerun evidence — 2026-08-15

`pnpm db:test:l03` passed the L02/L03 disposable PostgreSQL harness, including
the L06 maintenance idempotency and overlay-session expiry paths. The same
regression batch passed the Alerts API (54/54 tests/build), Go payment and worker
tests/vet/race, cron contract, mobile tests/lint/typecheck and macOS Swift
tests. These checks do not satisfy deployed OIDC, Cloud Scheduler, IAM,
provider-recovery or staging fault-injection gates.

The v1 infrastructure contract also passes 8/8 and confirms that Scheduler is
disabled, private-OIDC-only and has no direct database credentials. Live Cloud
Scheduler/IAM/target and recovery evidence remains open.

The scheduler operations contract now maps all six v1 schedules to required
outcome, failure, dead-letter, freshness/backlog and disable/replay signals,
with owner-specific recovery and evidence requirements. It remains a
deployment/runbook contract: no schedule was enabled and no live monitoring or
recovery rehearsal is claimed.

### Fresh local audit evidence — 2026-08-15

The checked-in scheduler contract, six disabled schedule definitions, API
maintenance route/store, L06 SQL migrations, operations runbook and
`bharatstudio-infra/deployment/v1/manifest.template.json` were reviewed
together. No additional local failure was found. The local acceptance slice is
therefore unchanged: scheduler ownership and fail-closed routing pass, while
deployed identity/IAM, live monitoring, target availability, provider recovery
and staging fault-injection evidence remain outstanding.

The same continuation rerun passed the scheduler contract (`npm test`, 2/2),
the payment service (`go test ./...`, race and vet) and the alert worker (same
three checks). The payment service's private payment/refund reconciliation
handlers are therefore locally implemented and exercised; they are not listed
as missing implementation below. This remains local evidence only and does
not prove Cloud Scheduler delivery, deployed OIDC/IAM, provider behavior,
monitoring or staging recovery.

## Not yet satisfied

- Transactional implementations behind the event/audit archive private handlers and their OIDC audience/service-account bindings. Payment and refund reconciliation are implemented in the Go payment service and the overlay-session mutation is implemented in the Alerts API; the database now has a whitelisted operational archive transfer/restore primitive, but no archive schedule may call it until the handler owns eligibility and retention policy.
- Cloud Scheduler deployment/IAM evidence and environment-specific values.
- Duplicate firing, delayed target, outage, missed-run, replay and dead-letter staging proof.
- Operations dashboard, alerting and manual recovery runbook.
- Live worker-pump OIDC binding, scheduler delivery, crash-after-persistence recovery and staging proof.
