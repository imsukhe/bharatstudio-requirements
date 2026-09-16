# TC-OPS-RECON-01 — the reliability reconciler has a schedule

**Task:** `../active/tasks/OPS-RECON-01.md`
**Owner:** Sukhdev Singh
**Status:** `Conditionally complete — repository definition only; explicitly not a deployment`

| Case | Control | Expected evidence |
|---|---|---|
| OPS-RECON-01.1 | The schedule exists and is on | `reliability-reconciliation` is present and `enabled: true`. |
| OPS-RECON-01.2 | It targets the right endpoint | `alerts-api`, `POST /internal/metrics/reconcile`, `alerts-api.` audience. |
| OPS-RECON-01.3 | Nothing else was switched on | Exactly two schedules are enabled, asserted as a set rather than spot-checked. |
| OPS-RECON-01.4 | Planned stays off | Both `planned` schedules remain disabled. |
| OPS-RECON-01.5 | The endpoint accepts the scheduler body | `{ idempotencyKey, window }` reaches the handler. |
| OPS-RECON-01.6 | Unknown-field behaviour is documented | An unknown field is **stripped by Fastify, not rejected** — asserted so the schema is not misread. |
| OPS-RECON-01.7 | The operations contract covers it | Ops doc carries its section, monitoring signal and dead-letter rows. |

**Commands:** `node --test tests/*.test.mjs` in `bharatstudio-crons`; `pnpm --filter @bharatstudio/alerts-api build` and `test` in `bharatstudio-alerts`.

## Recorded local evidence — 2026-09-16

- `bharatstudio-crons` `node --test tests/*.test.mjs` — **2 passed, 0 failed**. The contract
  test now asserts the enabled set (`outbox-recovery`, `reliability-reconciliation`) rather
  than a single id, so switching a third on silently becomes a failure, not a review miss.
  It also pins this schedule's service, serviceId, path and audience.
- Verified by reading every flag: enabled are `outbox-recovery` and
  `reliability-reconciliation`; `payment-reconciliation`, `refund-reconciliation`,
  `overlay-session-maintenance`, `event-archive-maintenance` and `audit-archive-maintenance`
  remain `false`. Both `planned` schedules are still disabled.
- `pnpm --filter @bharatstudio/alerts-api build` — passed.
- `pnpm --filter @bharatstudio/alerts-api test` — **566 passed, 0 failed** (baseline 564).
- The repository boundary held: no database credential, no SQL, no business logic, no public
  endpoint. A schedule entry, a test assertion and an operations section.

### A wrong claim, caught by its own test

The orchestrator recorded a latent defect — that the endpoint's `additionalProperties: false`
with only `idempotencyKey` meant a house-pattern schedule would be **rejected 400 on every
run**. Writing the test to prove it returned **503, not 400**: Fastify configures AJV with
`removeAdditional: true`, so an unknown field is **stripped**, not rejected, and `window`
would have vanished silently before the handler ran. The schedule would have worked.

The claim was corrected in the route comment, in the test name and in the task record rather
than quietly dropped. Declaring `window` explicitly still stands as the right change — a
schema that silently discards what a caller sends cannot be read as a contract — but it is a
clarity fix, not a bug fix, and it is recorded as one.

**What this is not.** **Enabling a schedule in a repository is not deploying it.** Nothing
here is evidence that a Cloud Scheduler job exists, that its OIDC service account
authenticates, or that the endpoint is reachable. That is deployment evidence and stays
gated with everything else in §32.
