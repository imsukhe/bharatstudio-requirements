# L01 — Referral read recovery boundary

**Status:** `Locally verified; external deployment evidence remains open`
**Level:** L3
**Parent authority:** `L01-contracts-and-database-baseline.md`; `L03-alerts-web-and-creator-api.md`
**Test record:** [`../tests/TC-L01-referral-read-recovery-boundary.md`](../tests/TC-L01-referral-read-recovery-boundary.md)
**Review:** [`../reviews/2026-09-12-L01-referral-read-recovery-boundary-decision.md`](../reviews/2026-09-12-L01-referral-read-recovery-boundary-decision.md)

## Scope and acceptance

Ensure authenticated referral overview and history reads map durable-store
rejections to the established redacted retryable 503 envelope. Preserve
authentication, database-enforced role projection, referral data, and
deployment behavior. Add deterministic outage/redaction proof and run the
full local verifier.

## Reproducible local evidence — 2026-09-12

- Referral overview and history now catch store rejections, use safe logging,
  and return `referral_store_unavailable` as a retryable 503.
- Deterministic tests inject secret-shaped datastore failure text for both
  reads and prove 503, `retryable: true`, and no response leakage.
- Focused API test passed 5/5 and the API TypeScript build passed.
- `pnpm verify:local` passed across contract/deployment, 116 migrations, 46
  SQL proofs, load/fault, API/web, build, Go race/vet, and image-build stages.

Only local evidence is recorded; staging and operational deployment checks
remain separate gates.
