# L16/L17 — Overlay widget response-integrity hardening

**Status:** `Locally implemented and verified`  
**Level:** L3  
**Parent authority:** `L16-interaction-menu-goals-and-widgets.md`; `L17-paid-challenges.md`; `L01-contracts-and-database-baseline.md`  
**Test record:** [`../tests/TC-L16-overlay-widget-response-integrity.md`](../tests/TC-L16-overlay-widget-response-integrity.md)  
**Review:** [`../reviews/2026-09-09-L16-overlay-widget-response-integrity-decision.md`](../reviews/2026-09-09-L16-overlay-widget-response-integrity-decision.md)

## Scope

Harden existing browser-overlay response guards for goal, challenge,
leaderboard, hype and vote widgets, plus the shared polling envelope. Guards
must require exact keys, supported enums, finite/non-negative numeric values,
bounded strings/arrays and valid timestamps before render. The shared poller
must accept only `{ schemaVersion: 'v1', <expectedField> }`; a successful HTTP
response with an unknown/malformed envelope is unavailable rather than trusted.

No overlay token design, data source, authorization, database, payment,
challenge, goal, broadcast transport, deployment, or public contract change is
authorized. This is a browser response-integrity and render-safety change only.

## Acceptance

- Hostile extra identity/payment/provider/credential fields and malformed
  primitive values are rejected by every affected guard.
- Valid existing widget payloads continue to render; malformed response keeps
  the safe blank state and does not throw.
- Focused widget tests, full web/API suites and full verifier are recorded;
  external image/staging/device evidence remains explicit.

## Local evidence — 2026-09-09

- Added one shared exact-record/bounded primitive helper and applied it to
  goal, challenge, leaderboard, hype and vote remote response guards. The
  shared widget poller now requires exactly `schemaVersion` plus its expected
  field before parsing.
- New hostile integrity tests prove rejection of account/payment/provider/
  credential expansions, unsupported enums, non-finite/negative numeric
  values, malformed dates and contradictory field types. Focused overlay
  suite passed 48/48; `pnpm test` passed API/web 293/293; web production build
  passed; `pnpm contracts:validate` passed 32 fixtures, 58 paths and 65
  operations.
- `git diff --check` passed. The complete local verifier including images
  subsequently passed after L10 hardening; no device/OBS, staging, deployment
  or production assertion is made.
