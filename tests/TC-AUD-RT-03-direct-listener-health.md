# TC-AUD-RT-03 — Direct listener loss acceptance

**Task:** `../active/tasks/AUD-RT-03-direct-listener-health.md`  
**Authority:** `../active/launch/08_AUDIT_REMEDIATION_AUTHORITY.md`  
**Owner:** **Sukhdev Singh**  
**Status:** `Passed locally — managed/deployed evidence pending`

| ID | Acceptance criterion |
|---|---|
| RT03.1 | A direct listener that had registered successfully becomes unhealthy when its actual connection closes, not only if initial registration rejects. |
| RT03.2 | Every in-flight waiter rejects with `overlay_listener_unavailable`; the SSE route uses its pre-existing bounded durable-replay fallback rather than treating that wait as a healthy timeout. |
| RT03.3 | One close produces one failure/reconnect sequence; stale callbacks cannot disconnect a new listener, and explicit shutdown schedules no reconnect. |
| RT03.4 | Health becomes connected only after a successful replacement `LISTEN`; a notification on the replacement listener still reaches only the matching channel. |
| RT03.5 | No schema/API/browser/polling/provider/permission/personal-data surface or user-controlled channel name is added. |
| RT03.6 | Focused unit/integration tests, full suites/builds/contracts/harness, hostile source/diff audit, traceability and document consistency pass. |

## Executed local evidence — 2026-09-18

```text
cd bharatstudio-alerts && pnpm --filter @bharatstudio/alerts-api test
cd bharatstudio-alerts && packages/db/tests/run-l03-application-behavior.sh
cd bharatstudio-alerts && pnpm db:test:all
cd bharatstudio-alerts && pnpm --filter @bharatstudio/alerts-api build && pnpm --filter @bharatstudio/alerts-web build
cd bharatstudio-alerts && pnpm --filter @bharatstudio/alerts-web test
cd bharatstudio-alerts && pnpm contracts:validate && pnpm harness:check && git diff --check
cd bharatstudio-requirements && python3 tools/traceability.py && python3 tools/doc_consistency.py
```

Managed PostgreSQL/network-loss and deployed browser/OBS evidence remains external.

Results: focused wake-up state-machine 11/11; API 935/935; web 658/658; SQL
87/87; API/Web builds; contracts (78 fixtures, 151 paths, 178 operations, 3
negative cases); harness; and disposable PostgreSQL behavior harness all passed.
The direct-listener integration locates the fixed-name non-personal listener backend,
terminates it with `pg_terminate_backend`, proves an in-flight waiter rejects and
health becomes false, waits for one replacement registration, then proves matching
notification delivery. Existing API route tests cover the catch-to-bounded-fallback
branch; no browser/OBS claim is made.
