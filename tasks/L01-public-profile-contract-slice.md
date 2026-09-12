# L01 — Public profile contract slice

**Status:** `Implemented and locally verified; remaining contract queue active`  
**Level:** L3  
**Parent authority:** `L01-contracts-and-database-baseline.md`; `L14-viewer-identity-and-supporter-history.md`  
**Test record:** [`../tests/TC-L01-public-profile-contract-slice.md`](../tests/TC-L01-public-profile-contract-slice.md)  
**Review/decision:** [`../reviews/2026-09-09-L01-public-profile-contract-slice-decision.md`](../reviews/2026-09-09-L01-public-profile-contract-slice-decision.md)

## Scope and invariant

Publish typed v1 contracts for `GET /v1/public/viewer-profiles` and
`GET /v1/public/viewer-profiles/{slug}` only. Profiles are default-private;
financial history, badges, email, session data, immutable account identifiers,
and visibility controls are excluded. The initially published account-ID
projection was superseded by
`L14-public-viewer-privacy-and-bounds-hardening.md` on 2026-09-09. Rollback is
forward migration/contract coordination; runtime data is unchanged.

## Local evidence — 2026-09-09

`pnpm contracts:validate` passed with 17 fixtures, 41 paths, 48 operations and
three structural OpenAPI negatives. The public profile fixture accepts only the
minimal projection and the validator rejects an injected
`netLifetimeAmountPaise` field. Focused L14 route evidence passed 7/7. Runtime
inventory is 159 literal operations, 48 covered, 111 pending and 0 stale.
