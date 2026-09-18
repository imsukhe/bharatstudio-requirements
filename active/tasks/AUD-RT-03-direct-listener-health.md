# AUD-RT-03 — Direct PostgreSQL listener health after registration loss

**Status:** `Conditionally complete — locally verified`  
**Owner:** **Sukhdev Singh**  
**Authority:** `../launch/08_AUDIT_REMEDIATION_AUTHORITY.md` (AUD-RT-03)  
**Acceptance record:** `../../tests/TC-AUD-RT-03-direct-listener-health.md`  
**Review record:** `../../reviews/2026-09-18-aud-rt-03-direct-listener-health.md`

## Scope

Replace the opaque `postgres.js` convenience `listen()` use for the direct overlay
wake-up path with a dedicated one-connection listener adapter whose close callback
is visible to the wake-up state machine. A connection that closes after successful
`LISTEN` must immediately become unhealthy, reject outstanding waits so the existing
overlay route takes its bounded durable-replay fallback, and reconnect with the
existing bounded exponential backoff. Only successful re-registration may return the
health state to connected.

The adapter must retain one canonical, hard-coded PostgreSQL notification channel,
use a fixed non-user-controlled listener application name solely to identify the
disposable integration connection, and end the latest listener on shutdown. The
generic test seam keeps its adapter interface and gains an optional close callback;
existing callers that do not provide it remain valid.

## Data, security, failure behaviour and boundaries

- No schema/migration, API/OpenAPI event, browser payload, subscriber identity,
  overlay token, payment state, provider action, or new database permission is
  introduced.
- The listener consumes the existing opaque `{ channelId, eventId }` notification
  only. Its channel name is internal constant, never request/config input. It makes
  no durable write and never changes durable replay correctness.
- On direct socket loss, `health().connected` is false and current waits reject with
  `overlay_listener_unavailable`; the existing route then applies its bounded jitter
  fallback and reads the authoritative store. It must not silently wait the full
  listener interval as though healthy.
- One failed connection can signal failure only once. Stale close/reject/register
  callbacks from an older attempt must not change a newer connection's health or
  schedule duplicate reconnects. Explicit shutdown is not a failure/reconnect.
- Service boundary remains API instance → direct PostgreSQL `LISTEN/NOTIFY`; workers
  and browsers neither own nor can invoke listener lifecycle.

## Rollback and deployment

This is source-only. Rollback is a normal source revert to the prior direct adapter;
there is no applied migration, data conversion, flag, credential or provider action
to undo. Deployment requires a normal API rollout/restart so each instance creates
its one listener. No deployment is authorised by this task.

## Required verification

- Unit tests simulate a post-registration close and prove false health, rejection of
  all channel waiters, exactly-one backoff/reconnect, stale-callback immunity and
  clean shutdown.
- A disposable PostgreSQL integration terminates the real dedicated listener backend
  after registration, observes the fallback-signalling rejection, then observes only
  successful re-registration restore health and deliver a later notification.
- Existing routing tests prove the fallback remains bounded and durable replay is
  still the correctness path. Run full API/web/SQL suites, application behavior
  harness, builds, contract/harness, source/diff hostile review, traceability and
  document consistency.

## External evidence gate

Local termination verifies only a disposable PostgreSQL listener. A real managed
PostgreSQL/network-loss and browser/OBS replay-latency rehearsal remains external;
this task cannot claim staging, provider, deployment or production evidence.

## Reproducible redacted evidence — 2026-09-18

Working-tree baseline: Alerts `d5cebc6`; this corrective slice remains uncommitted.

- Reworked `apps/api/src/db/overlay-wakeup.ts`: the generic wake-up state machine
  now has an optional post-registration close callback and attempt-generation guard.
  The direct adapter owns exactly one explicit, canonical-channel PostgreSQL listener
  with idle/lifetime disabled, a fixed non-personal application name and shutdown
  cleanup. A close immediately fails waiters and schedules one bounded reconnect;
  only the replacement registration restores `connected`.
- `postgres` 3.4.9 declares the connection `onclose` option. Its installed runtime
  notification hook is constrained to this one adapter because the package type
  declaration omits it; the real PostgreSQL termination test below pins that runtime
  contract rather than trusting mocks.
- Added a focused post-registration-close/stale-callback/shutdown regression in
  `apps/api/test/overlay-wakeup.test.ts` and a real backend-termination rehearsal in
  `integration/overlay-wakeup.integration.ts`. The latter kills the exact dedicated
  backend by fixed application name, checks wait rejection/false health, waits for
  replacement registration and verifies later matching notification delivery.
- Existing `apps/api/src/routes/metrics.ts` already exports the listener health gauge;
  no telemetry/data-schema change was required. Existing overlay-route tests retain
  the bounded fallback upon `overlay_listener_unavailable`.

| Command | Result |
|---|---|
| `cd bharatstudio-alerts/apps/api && pnpm exec tsx --test test/overlay-wakeup.test.ts` | 11/11 passed, including post-registration close, stale callbacks and shutdown |
| `cd bharatstudio-alerts && packages/db/tests/run-l03-application-behavior.sh` | 25 SQL behavior files and all Go/TypeScript integrations passed; the real direct listener termination/recovery rehearsal passed inside `test:overlay-wakeup:integration` |
| `cd bharatstudio-alerts && pnpm db:test:all` | SQL suite: 87 passed, 0 failed |
| `cd bharatstudio-alerts && pnpm --filter @bharatstudio/alerts-api test` | 935 passed, 0 failed |
| `cd bharatstudio-alerts && pnpm --filter @bharatstudio/alerts-web test` | 658 passed, 0 failed |
| `cd bharatstudio-alerts && pnpm --filter @bharatstudio/alerts-api build && pnpm --filter @bharatstudio/alerts-web build` | API TypeScript build and web production build (34 routes) passed |
| `cd bharatstudio-alerts && pnpm contracts:validate && pnpm harness:check && git diff --check` | 78 fixtures, 151 paths/178 operations, 3 negative cases, harness and whitespace check passed |

This is self-reviewed local evidence only. It does not establish managed database,
network-loss, browser/OBS, deployment, staging, provider or production readiness.
