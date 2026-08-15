# Launch task register

Work packages use dependency-based sequencing. Individual implementation tasks may be parallelised after their dependency/task documents are `Approved`, their contracts are stable, and their changes do not overlap. Final launch remains sequential at L10; implementation does not need to wait for unrelated packages.

1. `L00-legacy-freeze-and-inventory.md`
2. `L01-contracts-and-database-baseline.md`
3. `L02-security-rls-and-archive-proof.md`
4. `L03-alerts-web-and-creator-api.md`
5. `L04-go-payment-boundary.md`
6. `L05-go-alert-worker-and-cloud-tasks.md`
7. `L06-scheduler-boundary.md`
8. `L07-companion-web-mobile-desktop.md`
9. `L08-marketing-support-legal.md`
10. `L09-observability-load-failure.md`
11. `L10-release-readiness-and-rollout.md`

Every task must point to one pending requirement slice, one acceptance record, one review/decision record, exact affected files, a rollback method, and evidence status.
