# L01 — Overlay interaction state contract slice

**Status:** `Locally verified; external deployment evidence pending`  
**Level:** L3  
**Parent authority:** `L01-contracts-and-database-baseline.md`; `L16-interaction-menu-goals-and-widgets.md`  
**Test record:** [`../tests/TC-L01-overlay-interaction-state-contract-slice.md`](../tests/TC-L01-overlay-interaction-state-contract-slice.md)  
**Review:** [`../reviews/2026-09-09-L01-overlay-interaction-state-contract-slice-decision.md`](../reviews/2026-09-09-L01-overlay-interaction-state-contract-slice-decision.md)

## Scope

Publish strict v1 contracts and named server projections for these existing
overlay-token reads:

- vote tally, hype state, leaderboard, and paid-vote tally under
  `/v1/overlay-widgets/{overlayId}/…`.

The routes must distinguish no/invalid token (401) from missing dependency
(retryable 503), and return only typed rendering state. They must exclude
account/channel/payment/provider/token/refund/instrument/internal definition
fields. Free-form widget configuration and the four SQL-projected tip widgets
are intentionally excluded to keep this slice semantically exact.

## Boundaries and acceptance

No database query, vote accounting, money calculation, entitlement, widget
configuration, token model, provider, migration, or deployment behavior is
changed. Exact OpenAPI/schema/fixture projections, hostile store responses,
focused routes, browser guards, full local verifier and central evidence are
required. Production/OBS/browser-device/staging/provider evidence remains out
of scope.

## Local evidence — 2026-09-09

- Implemented named projections and retryable dependency/runtime failures for
  vote, hype, leaderboard, and paid-vote overlay reads. Missing bearer remains
  401; absent or failed stores return redacted retryable 503s.
- Published four OpenAPI operations, four strict JSON schemas, four golden
  fixtures, and hostile-field/negative-value/timestamp proof cases. Contract
  validation: **38 fixtures, 64 paths, 71 operations, 3 negative cases**.
- Focused hostile-store route tests and the complete API/web suite pass:
  **293/293**. `pnpm verify:local` exit **0** covers deployment checks, 46
  isolated SQL proofs, role proofs, load/fault checks, builds, Go race/vet, and
  three image builds.
- `git diff --check` is clean in Alerts and central requirements. Route
  inventory: **0 stale** OpenAPI operations; **88** runtime operations remain
  outside the published surface for later authority slices.
