# L06 scheduler-boundary review

**Date:** 2026-08-14  
**Reviewer:** Codex self-review  
**Independent reviewer:** Not performed in this pass  
**Decision state:** `Implementation slice complete; L06 remains open`  
**Task:** [`../tasks/L06-scheduler-boundary.md`](../tasks/L06-scheduler-boundary.md)  
**Acceptance:** [`../tests/TC-L06-scheduler-boundary.md`](../tests/TC-L06-scheduler-boundary.md)

## Findings and dispositions

| ID | Finding | Severity | Disposition | Owner/follow-up |
|---|---|---:|---|---|
| L06-R1 | Scheduler repository could accidentally become a second mutation service | High | Fixed in contract/readme: scheduler-only, no credentials, no public endpoint, private Alerts target only | Infra/SRE; enforce in CI |
| L06-R2 | A schedule without idempotency/retry/dead-letter/rollback metadata is not deployable safely | High | Fixed in schema and all v1 templates | Infra/SRE; deploy review |
| L06-R3 | Enabling schedules before private endpoints/IAM/staging evidence could create unowned mutations | High | Fixed: all templates are disabled and marked staging-template | Owner; enable only at L06 gate |
| L06-R4 | Independent review is unavailable in this pass | Process | Recorded; L06 remains conditional/open | Owner; fresh review before Verified |
| L06-R5 | Schedule targets had no corresponding API boundary and could not be proven private | High | Fixed locally: six exact maintenance paths require Google OIDC identity and strict idempotency input; no store means retryable 503. Transactional handlers and deployment IAM remain open | API/Payments/Alerts/SRE; implement stores and staging |
| L06-R6 | A verified private request could still be delivered twice by the scheduler without a durable run identity, and an unfinished run could be mislabeled completed on retry | High | Fixed locally: `maintenance_runs` uses a unique `(job, idempotency_key)` boundary; unfinished calls remain retryable without a second row, while only completed calls return `already_completed` | API/DB; wire each job's transactional mutation and retain duplicate-delivery regression |
| L06-R7 | Outbox recovery targeted the API ledger shell, which could record a run without re-enqueuing a ready delivery | Critical | Fixed locally: the disabled schedule now targets the private Alert Worker pump, the only boundary that lists ready rows and creates stable Cloud Tasks names. The API ledger route is no longer used for outbox recovery | Alerts/Worker/SRE; prove worker OIDC invocation, scheduler retry and crash-after-persistence recovery in staging |
| L06-R8 | Payment reconciliation targeted the API ledger shell, which has no provider client and could not perform status/recovery work | High | Fixed locally: the disabled schedule now targets the payment service's private reconciliation handler; provider fetch and recovery mutation remain inside the payment boundary | Payment/SRE; prove payment-service OIDC invocation, provider test mode, retry and staging recovery |
| L06-R9 | The generic API SQL maintenance store could accept an unimplemented job and create a false-success ledger row | Critical | Fixed for the API boundary: `overlay-sessions` now accepts and soft-revokes expired sessions transactionally through `0016`; payment/refund/outbox/archive requests fail closed before ledger acceptance because their owning services must execute those mutations | API/Payments/Worker/SRE; add owner-specific handlers and staging proof |
| L06-R10 | The schedule contract did not require cadence, timeout or a named monitoring signal, so an incomplete schedule could pass structural review even though governance requires those controls | High | Fixed: the JSON contract now requires a five-field UTC cadence, bounded timeout and monitoring signal; all disabled v1 fixtures provide them and the crons test asserts the fields | Infra/SRE; retain schema validation in deployment CI |
| L06-R11 | A schedule could have structural metadata but no executable operations/recovery contract for missed runs, backlog, dead letters or safe replay | High | Fixed locally: `bharatstudio-crons/docs/SCHEDULER_OPERATIONS.md` maps all six schedules to outcome/failure/dead-letter/freshness signals, owner-specific recovery, disable ordering, replay evidence and data-protection rules; the scheduler test verifies every declared signal is covered | Infra/SRE; connect signals to deployed monitoring and rehearse before enablement |

## Decision

The scheduler-only contract, disabled templates, OIDC-protected handler shell and transactional overlay-session slice are acceptable implementation slices. No schedule is approved for enablement until owner-specific job stores, IAM, monitoring and staging recovery evidence exist.

## Fresh local audit — 2026-08-15

The current `bharatstudio-crons` contract and schedule templates were checked
against the Alerts API maintenance route/store, the L06 SQL migrations, the
operations runbook and the infrastructure deployment template. The audit found
no new locally verifiable correctness gap. The ownership split remains:

- Go payment service: payment and refund reconciliation;
- Go Alert Worker: outbox recovery/pump;
- Alerts API: overlay-session expiry only;
- archive schedules: disabled until an approved handler, eligibility rule,
  retention/legal decision and restore/integrity evidence exist.

This is not independent review and is not a release sign-off. L06 remains open
for deployed OIDC/IAM and private-ingress proof, monitoring and alert wiring,
duplicate/timeout/provider-outage/dead-letter/manual-replay staging tests,
owner-specific reconciliation/archive implementations, and an explicit enable
decision for each schedule.
