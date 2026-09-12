# L01 — Overlay widget configuration and tip-read availability

**Status:** `Locally verified; external deployment evidence pending`  
**Level:** L3  
**Parent authority:** `L01-contracts-and-database-baseline.md`; `L16-interaction-menu-goals-and-widgets.md`  
**Test record:** [`../tests/TC-L01-overlay-widget-config-and-tip-read-availability.md`](../tests/TC-L01-overlay-widget-config-and-tip-read-availability.md)  
**Review:** [`../reviews/2026-09-09-L01-overlay-widget-config-and-tip-read-availability-decision.md`](../reviews/2026-09-09-L01-overlay-widget-config-and-tip-read-availability-decision.md)

## Scope

Harden the remaining existing bearer-token overlay reads: widget config,
recent tips, top supporters, supporter ticker, and mega-tip banner. Missing or
malformed bearer must remain 401. An absent SQL/store dependency or a query
failure must be a redacted retryable 503, never a misleading authorization
failure or raw exception. Widget config receives an explicit top-level
projection; its approved creator-authored `placement`, `style`, and
`dataSource` documents remain opaque here.

## Boundaries and acceptance

No widget semantics, SQL query, database schema, payment/tip data, privacy
rules, token model, deployment, or browser layout changes. Focused route tests
must cover all 401/503/success branches and prove top-level sensitive fields
cannot escape. Full local verifier, clean-diff audit, and central evidence are
required. Contract publication for the free-form configuration document remains
a separate authority decision.

## Local evidence — 2026-09-09

- All five bearer-token routes now classify missing bearer as 401 and an absent
  or failed dependency as redacted retryable 503. SQL failures are logged
  safely and do not enter a response body.
- Widget config uses an explicit top-level projection
  (`widgetConfigId`, `widgetType`, `placement`, `style`, `dataSource`),
  stripping injected account/channel/payment/provider/refund fields; its
  creator-authored nested documents remain intentionally opaque.
- API TypeScript, all 293 API/web tests, contract validation, and
  `pnpm verify:local` exit **0** passed after the change. The latter includes
  116 migrations, 46 SQL proofs, deployment/load/fault/build, Go race/vet, and
  image checks. No production/staging/provider/device claim is made.
