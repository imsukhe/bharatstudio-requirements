# TC-RT-08 — the outbox-recovery schedule is enabled

**Task:** `../active/tasks/RT-08.md`
**Owner:** Sukhdev Singh
**Status:** `Conditionally complete — repository definition only; explicitly not a deployment`

| Case | Control | Expected evidence |
|---|---|---|
| RT-08.1 | The dependency is on | `outbox-recovery.enabled` is `true` in `bharatstudio-crons/schedules/v1.json`. |
| RT-08.2 | Nothing else changed | The other five schedules remain `enabled: false`. |
| RT-08.3 | Contract still holds | The enabled schedule still validates against `contracts/schedule-contract.json`. |
| RT-08.4 | Planned stays off | `event-archive-maintenance` and `audit-archive-maintenance` are still `implementationStatus: "planned"` and are not enabled. |
| RT-08.5 | Operator procedure | `docs/SCHEDULER_OPERATIONS.md` states how to turn the dispatcher off and what happens to accepted events while it is off. |

**Commands:** `node --test tests/*.test.mjs` in `bharatstudio-crons`; the rest are shared with RT-04.

## Recorded local evidence — 2026-09-16

- `bharatstudio-crons/schedules/v1.json` — verified by reading every schedule's flag:
  `outbox-recovery` → `true`; `payment-reconciliation`, `refund-reconciliation`,
  `overlay-session-maintenance`, `event-archive-maintenance`, `audit-archive-maintenance`
  → all still `false`.
- `tests/schedule-contract.test.mjs` now asserts that `outbox-recovery` is the **only**
  enabled schedule, so switching another one on silently becomes a test failure rather than
  a review miss.
- The repository boundary was respected: no database credential, no SQL, no business logic
  and no public endpoint were added. Only a flag, a test assertion and an operations
  section changed.

**What this is not.** **Enabling a flag in a repository is not deploying a schedule.**
Nothing here is evidence that a Cloud Scheduler job exists, that its OIDC service account
authenticates, or that the endpoint is reachable. That is deployment evidence and remains
gated with everything else in §32. No production, provider, staging or release readiness is
claimed.
