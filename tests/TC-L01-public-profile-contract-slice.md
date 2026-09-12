# TC-L01 — Public profile contract slice

**Status:** `Pass — local contract and privacy-route evidence`  
**Task:** `../tasks/L01-public-profile-contract-slice.md`

| ID | Action | Expected result |
|---|---|---|
| L01-PP-01 | Validate public search and lookup operations | Typed query/path and typed public projection responses |
| L01-PP-02 | Validate public profile fixture and hostile extra-field mutation | Only display name and slug are accepted; account identifiers and financial fields are rejected |
| L01-PP-03 | Run L14 focused route tests and inventory | Default-private route behavior stays proven; two runtime operations become covered |

## Evidence — 2026-09-09

L01-PP-01 through L01-PP-03 passed: `pnpm contracts:validate` reports 17
fixtures/41 paths/48 operations and rejects a financial field added to the
public profile fixture. `cd apps/api && npx tsc --noEmit && npx tsx --test
test/l14-viewer-profile-routes.test.ts` passed 7/7. Provider/OAuth, deployment,
real-user data, and independent review remain external gates.
