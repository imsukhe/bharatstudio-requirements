# TC-AUD-OVL-01 — standalone overlay API-origin audio acceptance

**Task:** `../active/tasks/AUD-OVL-01-standalone-overlay-api-origin.md`  
**Authority:** `../active/launch/08_AUDIT_REMEDIATION_AUTHORITY.md`  
**Owner:** **Sukhdev Singh**  
**Status:** `Passed locally — independent review and external browser/OBS evidence remain pending`

| ID | Acceptance criterion |
|---|---|
| OVL01.1 | Given web origin `https://overlay.example` and configured API origin `https://api.example`, an API-emitted relative artifact path resolves only to `https://api.example/v1/overlay-audio/...`. |
| OVL01.2 | A canonical API-origin artifact URL remains allowed; external, web-origin, malformed, credential-bearing, non-artifact, and invalid-origin values return no URL and cannot be fetched. |
| OVL01.3 | Both Canvas and standalone overlay use the same pure allowlist boundary; their future behaviour cannot drift through duplicated origin logic. |
| OVL01.4 | Existing bearer-token fetch behaviour, audio/chime/browser-TTS fallback order, API artifact routes, event payload shape, migrations, and TTS entitlement policy are unchanged. |
| OVL01.5 | Focused URL tests, full applicable web/API suites, web typecheck/build, diff/static review, traceability regeneration, and documentation consistency pass. |

## Commands to record after implementation

```text
cd bharatstudio-alerts && pnpm --filter @bharatstudio/alerts-web test
cd bharatstudio-alerts && pnpm --filter @bharatstudio/alerts-web exec tsc -p tsconfig.json --noEmit
cd bharatstudio-alerts && pnpm --filter @bharatstudio/alerts-web build
cd bharatstudio-alerts && pnpm --filter @bharatstudio/alerts-api test
cd bharatstudio-requirements && python3 tools/traceability.py && python3 tools/doc_consistency.py
```

Real browser/OBS cross-origin evidence is intentionally excluded from local acceptance
and remains a release gate.

## Reproducible redacted local evidence — 2026-09-18

| Command | Result |
|---|---|
| `cd bharatstudio-alerts/apps/web && pnpm exec tsx --test --import ./app/test-support/dom-env.ts app/overlay/alert-audio-url.test.ts app/overlay/canvas/modules/support-theater-module.test.ts` | 14/14 passed: configured API-origin resolution, hostile URL rejection, and Canvas lifecycle/audio replay protections. The jsdom preload is required by the existing Canvas suite. |
| `cd bharatstudio-alerts && pnpm --filter @bharatstudio/alerts-web test` | 651/651 passed. |
| `cd bharatstudio-alerts && pnpm --filter @bharatstudio/alerts-web exec tsc -p tsconfig.json --noEmit` | Passed with 0 errors. |
| `cd bharatstudio-alerts && pnpm --filter @bharatstudio/alerts-web build` | Passed; existing route generation completed. |
| `cd bharatstudio-alerts && pnpm --filter @bharatstudio/alerts-api test` | 934/934 passed. |
| `cd bharatstudio-alerts && pnpm contracts:validate && pnpm harness:check` | Passed: 78 fixtures, 151 paths, 178 operation contracts, 3 negative contract cases; API harness check passed. |
| `cd bharatstudio-alerts && git diff --check` | Passed. |
| `cd bharatstudio-requirements && python3 tools/traceability.py && python3 tools/doc_consistency.py` | `TRACEABILITY.md` regenerated (783 rows); 17 consistency checks passed with 0 errors/warnings. |

Evidence is from uncommitted local worktrees based on Alerts `d5cebc6` and requirements
`4294a00`. No bearer token, audio content, donor data, credential, or external endpoint
response was recorded.
