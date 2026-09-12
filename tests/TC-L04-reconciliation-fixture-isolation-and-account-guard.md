# TC-L04 — Reconciliation fixture isolation and account-context guard

**Status:** `Pass — local executable evidence`
**Task:** [`../tasks/L04-reconciliation-fixture-isolation-and-account-guard.md`](../tasks/L04-reconciliation-fixture-isolation-and-account-guard.md)

| Case | Acceptance | Evidence |
| --- | --- | --- |
| Isolated L04 fixture | A reconciliation account does not collide with the main payment-flow account slot. | `l04_reconciliation_quarantine.sql` owns a dedicated synthetic channel; full disposable suite passes. |
| Attributed candidate | A requested refund linked to `test` payment evidence with a valid linked account is returned to the real Go SQL adapter. | `pnpm db:test:l03`; `TestSQLStoreListsAccountScopedCandidatesAgainstPostgres` passes. |
| Missing account | A requested refund linked to payment evidence with no account context cannot become an automated provider candidate. | `l04_reconciliation_quarantine.sql` negative assertion passes through migration `0111`. |
| Malformed account | Unsafe header characters cannot enter a candidate/provider call, even when the database value is nonempty. | `l04_reconciliation_quarantine.sql` asserts exclusion of `acct_l04/unsafe`; SQL grammar matches provider validation. |
| Regression matrix | Migration, SQL-role, service-adapter, overlay and race checks all remain compatible. | `pnpm db:test:l03`; payment `go test -race ./... && go vet ./...`; both pass on 2026-09-09. |

No provider API, staging database, or production data was accessed. Those are
not represented by these synthetic local results.
