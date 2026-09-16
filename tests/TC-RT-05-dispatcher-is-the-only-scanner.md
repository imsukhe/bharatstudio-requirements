# TC-RT-05 — the dispatcher is the only scanner

**Task:** `../active/tasks/RT-05.md`
**Owner:** Sukhdev Singh
**Status:** `Conditionally complete — local verification passed; no load evidence claimed`

| Case | Control | Expected evidence |
|---|---|---|
| RT-05.1 | Mutual exclusion | Two concurrent dispatch runs: one acquires the lease and scans, the other returns `skipped` without scanning or enqueueing. |
| RT-05.2 | No duplicate enqueue | The same ready delivery is never enqueued twice by concurrent runs. |
| RT-05.3 | Crash recovery | A run that dies before releasing its lease is superseded once the lease expires; the backlog is picked up, not stranded. |
| RT-05.4 | No handler scans | No request handler lists ready deliveries; the scan exists only behind the leased pump. |
| RT-05.5 | Lease isolation | The dispatch lease does not touch `event_outbox_deliveries.lease_token`/`lease_until`, so a normal per-delivery claim is never blocked by a scan lease. |

**Commands:** shared with RT-04 — see `TC-RT-04-webhook-commit-and-leased-dispatcher.md` for the exact commands, counts and the independent Opus verification.

## Recorded local evidence — 2026-09-16

The implementation, the checks and the audit are the same change as RT-04 and are recorded
once, in that record, rather than restated here. The evidence specific to this row:

- `packages/db/migrations/0129_v1_rt04_rt05_outbox_dispatch_lease.sql` —
  `acquire_outbox_dispatch_lease` is a single atomic `UPDATE` whose guard
  (`lease_until is null or lease_until <= current_timestamp`) lives inside the statement, so
  two concurrent acquires serialise on the one control row and the loser's predicate
  re-evaluates false. `release_outbox_dispatch_lease` matches on `lease_token`, so a run
  whose lease already expired and was reacquired cannot release the new holder's.
- `packages/db/tests/rt04_outbox_dispatch_lease.sql` — SQL-level proof, in
  `pnpm db:test:all` (**56 passed, 0 failed**) and in the curated `pnpm db:test:l03` run.
- `services/alert-worker-go/internal/tasks/pump_lease_test.go` — acquire/skip/release
  behaviour under `go test -race`, **10 packages `ok`**, `go vet` clean.

**Not claimed:** any measurement of the duplicate-scan pressure this removes. The lease
eliminates the duplicate scan by construction; how much load it was costing is a load
property and ENV-08 and RT-07 are Blocked. Local runs are never performance evidence
(§35.1 rule 6).
