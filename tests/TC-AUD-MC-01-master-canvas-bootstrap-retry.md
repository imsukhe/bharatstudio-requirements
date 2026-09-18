# TC-AUD-MC-01 — Master Canvas bootstrap retry acceptance

**Task:** `../active/tasks/AUD-MC-01-master-canvas-bootstrap-retry.md`  
**Authority:** `../active/launch/08_AUDIT_REMEDIATION_AUTHORITY.md`  
**Owner:** **Sukhdev Singh**  
**Status:** `Passed locally — independent review and external browser/OBS evidence remain pending`

| ID | Acceptance criterion |
|---|---|
| MC01.1 | Initial module/layout reads are attempted, and a transient failure does not permanently blank modules or lock the default layout. |
| MC01.2 | A successful later connection on the existing shared transport triggers one bounded reconciliation that applies only parsed server truth. |
| MC01.3 | A failed modules read cannot enable a module; a failed layout read preserves last-known-good/default horizontal state; one read's failure does not suppress the other successful value. |
| MC01.4 | Reconnect/lifecycle bursts during a read coalesce to at most one additional read pair. Disposal prevents late state mutation and removes the lifecycle subscription. |
| MC01.5 | The lifecycle subscriber creates no second SSE fetch, no event-payload subscriber/parser, no polling interval, no new endpoint, and no bearer-token persistence. |
| MC01.6 | Focused and full web/API tests, typecheck/build, contract/harness, source/diff review, traceability regeneration, and doc consistency pass. |

## Commands to record after implementation

```text
cd bharatstudio-alerts/apps/web && pnpm exec tsx --test --import ./app/test-support/dom-env.ts app/overlay/canvas/*.test.ts
cd bharatstudio-alerts && pnpm --filter @bharatstudio/alerts-web test
cd bharatstudio-alerts && pnpm --filter @bharatstudio/alerts-web exec tsc -p tsconfig.json --noEmit
cd bharatstudio-alerts && pnpm --filter @bharatstudio/alerts-web build
cd bharatstudio-alerts && pnpm --filter @bharatstudio/alerts-api test
cd bharatstudio-alerts && pnpm contracts:validate && pnpm harness:check
cd bharatstudio-requirements && python3 tools/traceability.py && python3 tools/doc_consistency.py
```

Browser/OBS/network-shaping evidence remains an external release gate.

## Reproducible redacted local evidence — 2026-09-18

| Command | Result |
|---|---|
| `cd bharatstudio-alerts/apps/web && pnpm exec tsx --test --import ./app/test-support/dom-env.ts app/overlay/canvas/canvas-bootstrap-reconciler.test.ts app/overlay/canvas/canvas-bootstrap-recovery.test.ts app/overlay/canvas/master-canvas-connection.test.ts app/overlay/canvas/master-canvas-integration.test.ts` | 39/39 passed: independent failure recovery, bounded coalescing, synchronous failure resilience, late-result disposal, visible-only lifecycle subscription, one transport, and existing Canvas module/rAF invariants. |
| `cd bharatstudio-alerts && pnpm --filter @bharatstudio/alerts-web test` | 657/657 passed. |
| `cd bharatstudio-alerts && pnpm --filter @bharatstudio/alerts-web exec tsc -p tsconfig.json --noEmit` | Passed with 0 errors. |
| `cd bharatstudio-alerts && pnpm --filter @bharatstudio/alerts-web build` | Passed; existing route generation completed. |
| `cd bharatstudio-alerts && pnpm --filter @bharatstudio/alerts-api test` | 934/934 passed. |
| `cd bharatstudio-alerts && pnpm contracts:validate && pnpm harness:check` | Passed: 78 fixtures, 151 paths, 178 operation contracts, 3 negative contract cases; API harness check passed. |
| `cd bharatstudio-alerts && git diff --check` | Passed. |
| `cd bharatstudio-requirements && python3 tools/traceability.py && python3 tools/doc_consistency.py` | `TRACEABILITY.md` regenerated (783 rows); 17 consistency checks passed with 0 errors/warnings. |

Evidence is from uncommitted local worktrees based on Alerts `d5cebc6` and requirements
`4294a00`; it contains no bearer token, creator/viewer data, deployment configuration,
or external endpoint result.
