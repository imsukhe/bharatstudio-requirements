# L14 — Public viewer privacy and bounded-read hardening

**Status:** `Implemented and locally verified; external gates remain open`  
**Level:** L3  
**Parent authority:** `L14-viewer-identity-and-supporter-history.md`; `L01-contracts-and-database-baseline.md`  
**Test record:** [`../tests/TC-L14-public-viewer-privacy-and-bounds-hardening.md`](../tests/TC-L14-public-viewer-privacy-and-bounds-hardening.md)  
**Review/decision:** [`../reviews/2026-09-09-L14-public-viewer-privacy-and-bounds-hardening-decision.md`](../reviews/2026-09-09-L14-public-viewer-privacy-and-bounds-hardening-decision.md)

## Scope

The continuing owner-directed local QA loop found three related, locally
reproducible gaps in the viewer surface:

1. The public profile search and lookup projection returns the immutable
   `viewer_account_id` despite the public UI needing only display name and slug.
2. The authenticated private dashboard has no SQL result bound.
3. The root local verifier does not execute the independent L14
   receipt/claim/badge/profile SQL proof, so a regression in that proof can be
   missed by the advertised one-command check.

Implement only the following: forward migrations to minimise the public SQL
projection and bound dashboard reads; matching API/domain/OpenAPI/fixture/test
updates; and root-harness inclusion of the isolated all-SQL runner. Do not add
identity providers, expose new data, alter payment semantics, or change the
existing default-private visibility model.

## Data, security, migration and rollback

The public contract is narrowed: `viewerAccountId` is removed, while
`displayName` and `profileSlug` remain. This prevents public correlation via a
durable internal identifier. Dashboard output remains authenticated and is
bounded to the newest 100 channel relations, ordered deterministically by
`last_supported_at DESC, channel_id DESC`.

Use additive forward migrations only (planned `0113` for public projection and
`0114` for dashboard bounding); never rewrite `0107` or `0085`. A deployed
rollback must be a new forward migration restoring the prior function shape
only after clients no longer rely on the narrowed contract. Local rollback is
discarding the disposable database. No production database is touched here.

## Service boundary and prerequisites

Only Alerts API calls the `app_private` functions under the application role.
Public callers receive the typed route response, never database access. The
work requires local Docker/PostgreSQL, the checked-in Node/Go dependencies, and
the existing contract validator; no provider, OAuth, device, staging, or
production credential is required.

## Acceptance and test plan

- Public SQL functions, API domain/store, route tests, OpenAPI, JSON schema,
  and fixtures contain no `viewerAccountId`.
- Hostile contract validation rejects an injected `viewerAccountId`; public
  search is documented with its actual maximum of 25 items.
- A disposable SQL proof creates more than 100 dashboard relations and proves
  exact deterministic truncation and viewer isolation.
- `pnpm verify:local` runs the isolated full SQL suite as well as the existing
  role-separated integration harness, remains fail-fast, and completes cleanly.
- Focused API tests, TypeScript checks, contract validation, both SQL runners,
  and the root verifier are recorded with redacted reproducible commands.

External provider, staging, production migration, independent security review,
and legal/retention evidence remain explicit gates and are not implied by a
local pass.

## Local execution evidence — 2026-09-09

Implemented forward migrations
`0113_v1_l14_public_profile_projection_minimization.sql` and
`0114_v1_l14_viewer_dashboard_bound.sql`. The former recreates only the two
public API-boundary functions with `display_name`/`profile_slug`; the latter
caps the authenticated dashboard at 100 with a deterministic tie-break.
`apps/api/src/domain/viewer-profile-store.ts`, its SQL adapter, public route
test, OpenAPI, JSON schema, fixture, and hostile fixture validator were
updated together. `package.json` now provides `db:test:all` and includes it in
`verify:local` before the role-separated integration harness.

Reproducible redacted local evidence:

- `pnpm contracts:validate && cd apps/api && npx tsc --noEmit && npx tsx --test test/l14-viewer-profile-routes.test.ts` — pass: 26 fixtures, 53 paths, 60 operations, three OpenAPI negatives, API typecheck, focused **7/7**.
- `DB_SQL_TESTS_ONLY=1 pnpm db:test:l03` — pass: migrations through **0114** and **19/19** role-separated SQL proofs, including the 101-relation dashboard bound/isolation test.
- `pnpm db:test:all` — pass: fresh PostgreSQL, **114** migrations and **44/44** isolated SQL proofs, including `l14-receipts-claims-badges-profiles`.
- `pnpm verify:local` — pass: the preceding checks plus deployment negatives,
  L09 load/fault self-tests, API **402/402**, web **289/289**, API/web builds,
  Go race/vet checks, and all three declared image builds.

No real provider, device, staging, production migration, legal conclusion, or
independent security-review result is claimed by this local evidence.
