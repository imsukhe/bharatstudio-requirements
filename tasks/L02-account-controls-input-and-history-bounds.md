# L02 — Account-control input and history bounds

**Status:** `Locally implemented and verified`  
**Level:** L3  
**Parent authority:** `L02-security-rls-and-archive-proof.md`; `L01-contracts-and-database-baseline.md`  
**Test record:** [`../tests/TC-L02-account-controls-input-and-history-bounds.md`](../tests/TC-L02-account-controls-input-and-history-bounds.md)  
**Review:** [`../reviews/2026-09-09-L02-account-controls-input-and-history-bounds-decision.md`](../reviews/2026-09-09-L02-account-controls-input-and-history-bounds-decision.md)

## Scope

Correct two locally reproducible account-control boundary gaps:

1. a required creator account-closure reason currently accepts the empty string;
2. `app_private.list_privacy_requests` returns an unbounded history although the
   browser client only accepts 256 items.

Add a forward-only migration and matching route validation. The private SQL
function must retain its caller-is-current-user predicate and `bsa_app` grant,
order deterministically newest-first, and expose at most 256 rows. An account
closure reason must be non-blank after trim and at most 500 characters at both
HTTP and database boundaries.

## Security, privacy, data, deployment, and rollback

No identity, payment, provider, session, account lifecycle, retention, public
profile, or external deployment behavior is expanded. The migration only
tightens an existing input validation condition and adds a read cap; it neither
deletes nor alters privacy-request rows. Existing callers continue to receive
their own newest data. Rollback is a controlled replacement of the private
function and removal of the HTTP minimum, but it would reintroduce validation/
amplification defects and is not automatic. Apply with the ordinary ordered
database migration release; no provider or environment prerequisite exists.

## Acceptance

- Blank/whitespace closure reason is rejected at HTTP and SQL boundaries;
  normal non-blank reason still closes/revokes as before.
- A synthetic history above 256 returns exactly the newest 256, never another
  user's request; direct SQL caller-scope proof remains intact.
- API focused tests, affected SQL proof, contracts/builds, and full local
  verifier pass. Evidence is redacted/synthetic and does not claim deployment,
  staging, production, legal, or device verification.

## Local evidence — 2026-09-09

- Migration `0115_v1_l02_account_controls_input_and_history_bounds.sql`
  preserves the current-user predicate and app grant, orders privacy requests
  newest-first with a 256-row cap, and rejects blank-after-trim closure
  reasons. The HTTP route rejects the same empty/whitespace inputs before the
  database boundary.
- Focused API proof passed: `test/account-routes.test.ts`, 2/2.
- Disposable SQL suite passed: 45/45 files. The new proof seeds 257 synthetic
  requests plus another user's row; it proves exactly 256 newest own rows,
  excludes the oldest/foreign rows, rejects whitespace closure, and accepts a
  non-blank closure.
- `pnpm contracts:validate` and API TypeScript build passed.
- `pnpm verify:local` completed all contract, deployment, SQL, role, load,
  fault, API/web (291 tests), build, and Go race/vet stages. Its API image
  stage then failed twice before source evaluation because BuildKit could not
  fetch `docker/dockerfile:1` from the external registry:
  `DeadlineExceeded: context deadline exceeded`. A direct retry of the same
  declared image build failed at the same registry step. This is recorded as
  an external image-registry gate, not a green image proof or product defect.

The root verifier was subsequently rerun successfully after L10 removed the
redundant Dockerfile frontend fetch. No deployment, staging, production,
provider, legal, or device conclusion is claimed.
