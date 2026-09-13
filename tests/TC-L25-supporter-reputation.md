# TC-L25 — Supporter reputation acceptance

**Status:** `Pass — locally reproducible 2026-09-13; not proven in a deployed environment`
**Task:** [`../tasks/L25-supporter-reputation.md`](../tasks/L25-supporter-reputation.md)
**Authority:** No prior master-plan section; created fresh per this reconciliation. Built in `bharatstudio-alerts` migration `0120_v1_l02b_reputation_signals_and_score.sql`.
**Repository:** `/Users/sukhdevsingh/Workspace/Bharat Studio/bharatstudio-alerts`
**Data:** Synthetic viewer/payment/refund/Super-Chat fixtures only. No production database or real supporter data is used.

| ID | Action | Expected result |
| --- | --- | --- |
| L25-01 | Attempt `app_private.record_reputation_signal` with `signal_type = 'refund'` for any source | Rejected with `errcode 22023`; no row inserted. **Pass:** `packages/db/tests/l02b-reputation-signals.sql`. |
| L25-02 | Raw-insert a `chargeback` row with `source = 'youtube_superchat'`, bypassing the function | Rejected by table CHECK (`signal_type <> 'chargeback' or source = 'bharatstudio_tip'`). **Pass:** same SQL suite file. |
| L25-03 | Query `information_schema.columns` for any column matching `%score%` across the schema | Zero rows. **Pass:** asserted directly in `l02b-reputation-signals.sql`. |
| L25-04 | Insert a `bharatstudio_tip` refund, read the live score, flip the refund to `reversed`, read again, flip back | Score changes on each read with zero writes to any reputation table — refund contribution is fully derived, never stored. **Pass:** same SQL suite file. |
| L25-05 | Call the creator-facing reputation route for a real supporter | Response has exactly three keys, no signal/source/channel column. **Pass:** `apps/api/test/reputation-routes.test.ts`. |
| L25-06 | Feed the route a store returning extra/unexpected fields | Rejected by `additionalProperties: false`. **Pass:** same test file. |
| L25-07 | Request viewer account deletion for a viewer with reputation signal history | Erasure record's `retained` array contains an entry naming `reputation_signal_events`. **Pass:** `packages/db/tests/l02b-reputation-signals.sql` line ~240-246 calls `app_private.request_viewer_account_deletion` directly and asserts the retained-array entry exists. The `legalDispositionOpen: true` flag inside that entry's text was confirmed by reading the migration, not by a separate assertion on the flag's boolean value — a narrower gap than initially assumed, corrected here after checking the actual test rather than trusting a first read. |

## Local evidence — 2026-09-13

- `apps/api`: `npm test` (via `tsx --test`) — **465/465** passing, including `test/reputation-routes.test.ts` (146 lines, new in this batch).
- `packages/db`: `sh packages/db/tests/run-sql-suite.sh` — **49/49** passing across **120** migrations, including `l02b-reputation-signals.sql` (257 lines, new in this batch).
- `apps/web`: **312/312** passing (unaffected by this migration; re-run for the full batch-10 reconciliation, not because this task touches web).
- All three Go services (`youtube-poller-go`, `alert-worker-go`, `payment-webhook-go`): `go test ./...` clean, unaffected by this migration.

## Gaps, recorded not resolved

- No independent review of this feature exists yet.
- No deployed-environment evidence exists for any row above.
- The retention-vs-DPDP legal question is unresolved; see the task file's retention-decision section. No legal conclusion is asserted here.
