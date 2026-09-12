# TC-L02 — Account-control input and history bounds

**Status:** `Pass — full local verifier subsequently green`  
**Task:** [`../tasks/L02-account-controls-input-and-history-bounds.md`](../tasks/L02-account-controls-input-and-history-bounds.md)

| ID | Action | Expected result |
| --- | --- | --- |
| L02-AC-01 | Submit empty and whitespace-only closure reasons through HTTP and SQL | Both reject; valid non-blank reason still succeeds. **Pass:** API 2/2; new disposable SQL proof. |
| L02-AC-02 | Seed 257+ own privacy requests and another user's record | Exactly newest 256 own rows, deterministically ordered; foreign row absent. **Pass:** SQL suite 45/45. |
| L02-AC-03 | Run focused API/SQL/full regression checks | Contract, deployment, SQL, role, load/fault, API/web, builds, Go race/vet and all images now pass via `pnpm verify:local`; L10 removed the redundant frontend dependency. |
