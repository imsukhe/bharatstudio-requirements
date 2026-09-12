# TC-L14 — Public viewer privacy and bounded-read hardening

**Status:** `Pass — local disposable and application evidence`  
**Task:** [`../tasks/L14-public-viewer-privacy-and-bounds-hardening.md`](../tasks/L14-public-viewer-privacy-and-bounds-hardening.md)

| ID | Action | Expected result |
| --- | --- | --- |
| L14-PB-01 | Search and fetch an opted-in public profile | Only `displayName` and `profileSlug` are returned; no durable viewer identifier or financial field appears. |
| L14-PB-02 | Inject `viewerAccountId` into the public-profile fixture | Strict JSON-schema validation fails. |
| L14-PB-03 | Seed 101+ dashboard relations for one viewer and query as that viewer and another viewer | Own query returns exactly 100 newest deterministic rows; another viewer receives none. |
| L14-PB-04 | Run the isolated SQL suite and root verifier | Every SQL proof, including `l14-receipts-claims-badges-profiles`, executes; root command remains fail-fast and exits zero. |

## Evidence — 2026-09-09

L14-PB-01 passed: focused API route proof **7/7** verifies both public search
and lookup return exactly display name and slug; its response has no
`viewerAccountId`. L14-PB-02 passed: `pnpm contracts:validate` rejects both an
injected financial field and an injected immutable account identifier under
strict additional-properties rules; the documented search maximum is now 25.
L14-PB-03 passed in `l14_viewer_identity.sql`: after 101 relations, own
dashboard reads return exactly the newest 100 and exclude the deliberate
oldest relation; other-viewer reads remain empty. L14-PB-04 passed:
`pnpm db:test:all` reports **44/44** and `pnpm verify:local` passes with the
isolated SQL suite before role-separated integrations.

All data was synthetic/disposable. Provider, staging, production, device and
independent-review evidence remains out of scope and unclaimed.
