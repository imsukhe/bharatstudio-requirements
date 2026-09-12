# L01 — Viewer dashboard contract slice

**Status:** `Implemented and locally verified; external gates remain open`  
**Level:** L3  
**Parent authority:** `L01-contracts-and-database-baseline.md`; `L14-viewer-identity-and-supporter-history.md`  
**Test record:** [`../tests/TC-L01-viewer-dashboard-contract-slice.md`](../tests/TC-L01-viewer-dashboard-contract-slice.md)  
**Review/decision:** [`../reviews/2026-09-09-L01-viewer-dashboard-contract-slice-decision.md`](../reviews/2026-09-09-L01-viewer-dashboard-contract-slice-decision.md)

## Scope

Publish and verify the existing `GET /v1/viewer/dashboard` contract only. It is
an authenticated viewer-account history read, not a creator route. The route
already uses the separate viewer bearer-token namespace and the database read
is bounded to 100 newest relations by migration `0114`.

Add the versioned OpenAPI operation, strict response schema and redacted
fixture; add positive and hostile fixture checks; and enhance the focused API
test to prove unauthenticated rejection, response bounds, and the approved
projection. Do not change the data model, financial calculations, UI, identity
providers, or public surface.

## Security, data, rollback and prerequisites

The contract may contain the viewer's own per-channel support totals but must
not contain a viewer account ID, email, session credential, provider identity,
payment/order identifier, donor message, or another viewer's data. Collection
maximum is 100. A contract rollback must be coordinated with clients; no
database rollback is needed because this slice adds no schema or migration.
Local prerequisites are checked-in Node dependencies and disposable PostgreSQL
for the already-existing bound proof. Provider, staging, production, device,
and legal evidence are external gates.

## Acceptance

- The route is documented with `viewerBearerAuth`, its actual 100-item bound,
  200 projection, and 401/503 failure envelopes.
- The schema/fixture enforce all scalar types, member-state enum, dates and
  strict additional-properties rules.
- Hostile injected account/payment/provider identity fields are rejected.
- Focused API, contract validation, role-separated SQL, and root verifier pass
  with reproducible redacted evidence.

## Local evidence — 2026-09-09

OpenAPI now contains `getViewerDashboard` behind `viewerBearerAuth`, a strict
`ViewerDashboardResponse`, and a 100-item collection cap. The matching JSON
schema and redacted fixture enforce types, date formats, non-negative decimal
strings, and the member-state enum. The validator rejects injected account and
payment identifiers. The API test now asserts the exact narrow row projection
and confirms those identifiers are absent.

`pnpm verify:local` passed after this change: **27** fixtures, **54** paths,
**61** OpenAPI operations, 3 OpenAPI negatives; isolated SQL **44/44**;
role-separated SQL **19/19**; API **402/402**; web **289/289**; app builds,
Go race/vet, L09 load/fault, deployment negatives, and declared image builds.
The inventory is 159 runtime operations, 61 documented, 98 queued, 0 stale.
This is local evidence only; provider/staging/device/production/legal gates
remain unclaimed.
