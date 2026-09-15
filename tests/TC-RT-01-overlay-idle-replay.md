# TC-RT-01 — overlay idle replay

**Task:** `../active/tasks/RT-01.md`  
**Owner:** Sukhdev Singh  
**Status:** `Conditionally complete — local verification passed; external release evidence not applicable`

| Case | Control | Expected evidence |
|---|---|---|
| RT-01.1 | Initial replay | Existing cursor/token replay is emitted before waiting. |
| RT-01.2 | Logical idle window | Fake clock advances 10 minutes; connected idle path performs zero DB replay calls. |
| RT-01.3 | Valid wake | One valid notification causes one bounded replay; malformed notification does not release a waiter. |
| RT-01.4 | Listener failure/disconnect | Injected deterministic jittered bounded fallback is used only after failure; reconnect cancels fallback. |
| RT-01.5 | Abort/failure | Abort clears timers/waiters; replay failure closes without acknowledgement or event loss. |

**Commands:** `pnpm --filter @bharatstudio/alerts-api build`; `pnpm --filter @bharatstudio/alerts-api test`; `pnpm measurement:test`  
**Security audit:** bearer/CORS/cursor validation and cross-session token isolation remain covered by existing API tests; no new data boundary.  
**External evidence:** none claimed; staging/OBS/device evidence remains outside this task.

## Recorded local evidence — 2026-09-15

- `pnpm --filter @bharatstudio/alerts-api build` — passed.
- `pnpm --filter @bharatstudio/alerts-api test` — 511 passed, 0 failed.
- Overlay characterization: connected idle timeout produced exactly one replay call (initial replay only); two disconnected fallback cycles replayed the late event exactly once with fixed RNG/bounded jitter, then reconnect stopped replay polling.
- Fake-clock characterization advanced logical time by 10 minutes during a connected wait and still observed only the initial replay; `OverlayWakeup.waitForNotification` and mandatory health state distinguish timeout from listener failure.
- `pnpm --filter @bharatstudio/alerts-api test` also covered token isolation, cursor validation, CORS and bounded stream close. No provider or staging evidence claimed.
- Rollback: revert `apps/api/src/routes/overlay.ts`, `apps/api/src/db/overlay-wakeup.ts`, `apps/api/src/domain/overlay-wakeup.ts`, and the characterization test; no migration changed.
- `test/overlay-wakeup.test.ts` — 6 passed, including listener rejection of the current waiter, disconnected health, reconnect, malformed notification and abort cleanup.
- API seam coverage records exactly `[750, 750]` ms fallback sleeps with RNG `.25`, recovers the second event once, performs no replay after reconnect idle, and stops before replay when the fallback sleep aborts.
- `test/abortable-sleep.test.ts` directly aborts a pending 60-second sleep, verifies prompt resolution and no retained abort handler. A real loopback HTTP SSE request destroys its socket during fallback, proving the passed signal aborts and store replay remains exactly one; a separate injected sleep-error case retains `replay-unavailable` behavior.
