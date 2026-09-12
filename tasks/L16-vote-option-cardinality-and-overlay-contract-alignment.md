# L16 — Vote-option cardinality and overlay contract alignment

**Status:** `Locally verified; external deployment evidence pending`  
**Level:** L3  
**Parent authority:** `L16-interaction-menu-goals-and-widgets.md`  
**Test record:** [`../tests/TC-L16-vote-option-cardinality-and-overlay-contract-alignment.md`](../tests/TC-L16-vote-option-cardinality-and-overlay-contract-alignment.md)  
**Review:** [`../reviews/2026-09-09-L16-vote-option-cardinality-and-overlay-contract-alignment-decision.md`](../reviews/2026-09-09-L16-vote-option-cardinality-and-overlay-contract-alignment-decision.md)

## Scope

Align the existing support-vote creation procedure with the published v1
overlay contract and browser bound: no interaction definition can create more
than 16 options. The procedure must serialize concurrent creation attempts on
the same definition, so a race cannot bypass the limit.

## Boundaries and acceptance

One forward-only PostgreSQL migration may replace only
`app_private.create_vote_option`; it must retain authorization, ownership,
input, and existing-outcome behavior. Prove 16 accepted options, a sequential
17th rejection, and concurrent/transactional serialization with a
role-separated SQL test. Re-run API/browser/contract/full local verification
and record redacted reproducible evidence. No payment, tally, entitlement,
provider, deployment, or production behavior is changed.

## Local evidence — 2026-09-09

- Added forward-only migration `0116_v1_l16_vote_option_cardinality.sql`.
  `app_private.create_vote_option` locks its support-vote definition with
  `FOR UPDATE`, counts under that lock, then rejects an attempted 17th option
  before insert.
- Added `l16_vote_option_cardinality.sql`: proves sixteen accepted options,
  the seventeenth rejected with no persisted extra row, and retains the
  parent-row lock in the procedure definition as a regression proof.
- `pnpm verify:local` exit **0** after the migration: 116 migrations, **46/46
  isolated SQL tests**, 293/293 API/web, contract/deployment/load/fault/build,
  Go race/vet, and image stages all green. No external/staging deployment claim
  is made.
