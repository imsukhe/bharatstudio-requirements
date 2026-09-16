# OPS-RECON-01 — the L09 reliability reconciler gets a schedule

**Authority:** [`../../FULL-PRODUCT-DEFINITION.md`](../../FULL-PRODUCT-DEFINITION.md) §19.0 RT-06, and the owner decision of 2026-09-16 that this be its own task rather than an extension of RT-06
**Status:** `Conditionally complete — schedule defined and enabled in the repository; this is not a deployment; independent review unavailable`

| Field | Value |
|---|---|
| **Scope phase** | `v1`; Phase 0.5 runtime remediation; scheduler definition plus the one route-schema correction it required |
| **Owner** | **Sukhdev Singh** |
| **Tier and gate** | All tiers; no release claim. `bharatstudio-crons` stays scheduler-only — no database credential, no SQL, no business logic, no public endpoint |
| **Personal-data class** | None. The reconciler computes aggregate counts; the gauges carry no identifier, and `renderPrometheus` is already asserted never to emit one |
| **Provider or legal dependency** | Google Cloud Scheduler and the OIDC service account named in the schedule. Neither is exercised here — this edits a definition file |
| **Failure behaviour** | A missed or failing run costs **freshness only**. The gauges go stale; no payment, alert, delivery or overlay record depends on this job, and the last snapshot written stays readable. The endpoint already fails closed with a retryable 503 rather than reporting zeros |
| **Kill switch** | Set `reliability-reconciliation.enabled` back to `false` in `bharatstudio-crons/schedules/v1.json`. Documented in `docs/SCHEDULER_OPERATIONS.md` |
| **Acceptance test** | `tests/TC-OPS-RECON-01-reliability-reconciliation-schedule.md` |
| **Evidence location** | `tests/TC-OPS-RECON-01-reliability-reconciliation-schedule.md`, `reviews/2026-09-16-ops-recon-01-reliability-reconciliation-schedule.md` |
| **Rollback** | Set the flag to `false`, or remove the schedule entry; revert the contract-test and operations-doc changes and the `apps/api/src/routes/metrics.ts` body-schema change |

## Why this exists

RT-06 left one thread open: the L09 reliability reconciler at
`POST /internal/metrics/reconcile` had **no schedule pointing at it at all**, so its gauges
only moved when something called it by hand. `payment-reconciliation` is a different
reconciler — Razorpay provider-status recovery in `payment-webhook-go` — and stays disabled
under its own row.

## Cadence is borrowed, not chosen

`*/5` is `payment-reconciliation`'s existing cadence, the closest reconciliation analogue
already approved in the catalogue. No authority states a cadence for this job, so an
existing value was reused rather than a new number invented. It is safe to change: the job
is idempotent and nothing depends on its interval.

## The route change it required, and a correction

Every schedule in the catalogue sends `{ idempotencyKey, window }`, and
`/internal/metrics/reconcile` declared only `idempotencyKey`. `window` is now declared
explicitly.

**The orchestrator initially recorded this as a latent defect — "a schedule written in the
house pattern would have 400'd on every run" — and that was wrong.** Fastify configures AJV
with `removeAdditional: true`, so `additionalProperties: false` **strips** an unknown field
rather than rejecting it; `window` would simply have vanished before the handler ran. The
error was caught by the test written to prove the claim, and the test now documents the real
behaviour instead. Declaring `window` is still right — a schema that silently drops what a
caller sends is a contract that lies about itself — but it is a clarity fix, not a bug fix.

## Boundaries

**Out of scope:** enabling any other schedule; deployment, IAM or OIDC configuration; the
reconciler's own query logic; RT-06's cross-instance aggregation, which remains open and
needs a deployed environment.
