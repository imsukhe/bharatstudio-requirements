# L01 — Payment ledger failure classification

**Status:** `Locally verified; external deployment evidence remains open`
**Level:** L3
**Parent authority:** `L01-contracts-and-database-baseline.md`; `L04-go-payment-boundary.md`
**Test record:** [`../tests/TC-L01-payment-ledger-failure-classification.md`](../tests/TC-L01-payment-ledger-failure-classification.md)
**Review:** [`../reviews/2026-09-12-L01-payment-ledger-failure-classification-decision.md`](../reviews/2026-09-12-L01-payment-ledger-failure-classification-decision.md)

## Scope and acceptance

Keep malformed payment-ledger cursors as a bounded 400, but map a durable
ledger failure to a redacted retryable 503. Add deterministic tests proving
the distinction and run full local verification. Do not change payment data,
authorization, or provider behavior.

## Reproducible local evidence — 2026-09-12

- Added the explicit `PaymentLedgerInvalidCursorError` boundary. Only the SQL
  cursor codec emits it; the route maps that typed condition to `bad_cursor`.
- All other ledger-store failures now use safe logging and return the existing
  redacted `payment_ledger_unavailable` retryable 503 envelope.
- Focused route tests passed 4/4, proving malformed-cursor 400 and injected
  secret-shaped database-outage 503 behavior; API TypeScript build passed.
- `pnpm verify:local` passed across contracts, deployment, 116 migrations, 46
  SQL proofs, load/fault checks, API/web, builds, Go race/vet, and images.

This record is local-only evidence; provider and deployed operational proof
remain separate readiness gates.
