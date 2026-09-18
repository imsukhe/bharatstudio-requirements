# TC-AUD-SB-01 — Safe Soundboard replay/wake-up acceptance

**Task:** `../active/tasks/AUD-SB-01-soundboard-replay-and-wakeup.md`  
**Authority:** `../active/launch/08_AUDIT_REMEDIATION_AUTHORITY.md`  
**Owner:** **Sukhdev Singh**  
**Status:** `Passed locally — external deployment/browser evidence pending`

| ID | Acceptance criterion |
|---|---|
| SB01.1 | Receiving the same latest `playId` after deactivate/reactivate never creates or plays a second audio instance. |
| SB01.2 | A different later `playId` after reactivation stops/replaces audio and displays the new caption; normal same-poll de-duplication remains intact. |
| SB01.3 | A valid committed creator trigger emits exactly the existing channel-scoped overlay wake-up from inside the durable trigger transaction; no rejected/rolled-back trigger emits it. |
| SB01.4 | The migration preserves security-definer role checks, `bsa_app` execute grant, exact-one-source validation, no new data/output surface, and overlay fallback correctness. |
| SB01.5 | No polling, new browser connection, direct client notification, extra overlay session, clip bytes, supporter/viewer identity, CDN/provider configuration, or public wake-up route is introduced. |
| SB01.6 | Focused module/API/SQL/migration checks, full web/API suites, typecheck/build, contracts/harness, diff/source hostile review, traceability, and doc consistency pass. |

## Executed local evidence — 2026-09-18

```text
cd bharatstudio-alerts/apps/web && pnpm exec tsx --test --import ./app/test-support/dom-env.ts app/overlay/canvas/modules/safe-soundboard-module.test.ts
cd bharatstudio-alerts && pnpm --filter @bharatstudio/alerts-api test
cd bharatstudio-alerts && pnpm db:test:all
cd bharatstudio-alerts && packages/db/tests/run-l03-application-behavior.sh
cd bharatstudio-alerts && pnpm --filter @bharatstudio/alerts-web test
cd bharatstudio-alerts && pnpm --filter @bharatstudio/alerts-api build && pnpm --filter @bharatstudio/alerts-web build
cd bharatstudio-alerts && pnpm contracts:validate && pnpm harness:check
cd bharatstudio-requirements && python3 tools/traceability.py && python3 tools/doc_consistency.py
```

Results: focused module 10/10; API 934/934; SQL 87/87; web 658/658; API/Web
builds; contracts (78 fixtures, 151 paths, 178 operations, 3 negative cases);
harness; and the disposable PostgreSQL behavior harness all passed. The latter uses
two direct PostgreSQL listeners and exercises a committed real Soundboard trigger,
durable-row check and rejected-trigger no-wake case.

Real deployed browser/OBS/CDN/autoplay evidence is intentionally external. This
record does not claim it.
