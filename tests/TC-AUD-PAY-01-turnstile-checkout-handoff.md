# TC-AUD-PAY-01 — Turnstile checkout hand-off acceptance

**Task:** `../active/tasks/AUD-PAY-01-turnstile-checkout-handoff.md`  
**Authority:** `../active/launch/08_AUDIT_REMEDIATION_AUTHORITY.md`  
**Owner:** **Sukhdev Singh**  
**Status:** `Passed locally — external Cloudflare/browser evidence remains pending`

| ID | Acceptance criterion |
|---|---|
| PAY01.1 | Ordinary tip checkout with a configured synthetic site key renders one first-party-integrated challenge container and serializes the callback's opaque token as `turnstileToken` in the existing order request. |
| PAY01.2 | Tip-intent confirmation serializes the same callback token and still sends no mutable amount/name/message field. |
| PAY01.3 | Before a configured challenge yields a token, its expiry callback fires, or its error callback fires, neither journey sends an order request; the donor receives an accessible recovery message. |
| PAY01.4 | Completing an order request clears the in-memory token and requests a new challenge response before another order attempt. No token appears in `sessionStorage`, `localStorage`, a URL, receipt, or rendered text. |
| PAY01.5 | A production-mode missing public site key refuses checkout locally and sends no request. Development/test without a key preserves the existing local path. |
| PAY01.6 | Existing API guard behaviour still rejects an absent token when enabled and permits a valid synthetic guard response without calling the payment boundary on reject. |
| PAY01.7 | Direct-tip OpenAPI documents the existing optional bounded token and `403` outcome; web typecheck, full web tests, production build, API tests, OpenAPI/fixture validation, and documentation consistency all pass. |
| PAY01.8 | Review confirms no secret, payment data, changed provider payload, migration, direct browser-to-provider verification, or unrecorded external claim was introduced. |

## Commands to record after implementation

```text
cd bharatstudio-alerts && pnpm --filter @bharatstudio/alerts-web test
cd bharatstudio-alerts && pnpm --filter @bharatstudio/alerts-web exec tsc -p tsconfig.json --noEmit
cd bharatstudio-alerts && pnpm --filter @bharatstudio/alerts-web build
cd bharatstudio-alerts && pnpm --filter @bharatstudio/alerts-api test
cd bharatstudio-alerts && pnpm contracts:validate
cd bharatstudio-requirements && python3 tools/doc_consistency.py
```

Real Cloudflare/browser/staging evidence is intentionally not represented by these
local checks.

## Reproducible redacted local evidence — 2026-09-18

| Command | Result |
|---|---|
| `cd bharatstudio-alerts/apps/web && pnpm exec tsx --test --experimental-test-module-mocks --import ./app/test-support/dom-env.ts app/tips/turnstile-challenge.test.tsx 'app/tips/[[]handle[]]/turnstile-tip-form.test.tsx' 'app/t/[[]token[]]/turnstile-tipintent-confirm.test.tsx'` | 5/5 focused tests passed: callback-only order creation, immutable tip-intent body, production missing-key fail-closed, in-memory-only token, expiry/reset lifecycle. |
| `cd bharatstudio-alerts && pnpm --filter @bharatstudio/alerts-web test` | 649/649 passed. |
| `cd bharatstudio-alerts && pnpm --filter @bharatstudio/alerts-web exec tsc -p tsconfig.json --noEmit` | Passed with 0 errors. |
| `cd bharatstudio-alerts && pnpm --filter @bharatstudio/alerts-web build` | Passed; 34 routes generated. |
| `cd bharatstudio-alerts && pnpm --filter @bharatstudio/alerts-api test` | 934/934 passed, including the existing required-guard reject/allow regression. |
| `cd bharatstudio-alerts && pnpm contracts:validate` | Passed: 78 fixtures, 151 paths, 178 operations, 3 negative operation cases. |
| `cd bharatstudio-alerts && pnpm harness:check` | Passed. |
| `cd bharatstudio-requirements && python3 tools/traceability.py && python3 tools/doc_consistency.py` | `TRACEABILITY.md` regenerated (783 rows); 17 consistency checks passed with 0 errors/warnings. |

Evidence was recorded against uncommitted working trees based on Alerts `d5cebc6`
and requirements `4294a00`; no secret value, provider credential, donor data, or
external endpoint response was captured.
