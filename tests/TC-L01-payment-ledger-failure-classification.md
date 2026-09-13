# TC-L01 — Payment ledger failure classification

**Status:** `Pass — local evidence recorded 2026-09-12`
**Task:** [`../tasks/L01-payment-ledger-failure-classification.md`](../tasks/L01-payment-ledger-failure-classification.md)

| ID | Action | Expected result |
| --- | --- | --- |
| L01-PLF-01 | Submit invalid cursor | Bounded 400 `bad_cursor`. |
| L01-PLF-02 | Reject durable-ledger read | Redacted retryable 503, not 400. |
| L01-PLF-03 | Run deterministic verifier | No local regression. |

## Evidence

- Focused route suite: 4/4 pass, including typed invalid-cursor and redacted
  datastore-outage cases.
- API TypeScript build and `pnpm verify:local`: pass.
