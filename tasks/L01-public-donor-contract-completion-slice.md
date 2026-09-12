# L01 — Public donor contract completion slice

**Status:** `Implemented and locally verified; remaining contract queue active`  
**Level:** L3  
**Parent authority:** [`L01-contracts-and-database-baseline.md`](L01-contracts-and-database-baseline.md)  
**Test record:** [`../tests/TC-L01-public-donor-contract-completion-slice.md`](../tests/TC-L01-public-donor-contract-completion-slice.md)  
**Review/decision:** [`../reviews/2026-09-09-L01-public-donor-contract-slice-decision.md`](../reviews/2026-09-09-L01-public-donor-contract-slice-decision.md)

## Scope

Publish typed v1 OpenAPI contracts for the unauthenticated, donor-facing
receipt and TipIntent flows already implemented by Alerts:

- `POST`/`GET /v1/public/receipts`;
- `GET /v1/public/tip-intents/{token}`; and
- `POST /v1/public/tip-intents/{token}/orders`.

The internal TipIntent creation route is deliberately excluded: it is a
connector-secret service boundary, not a browser/public API. Viewer identity,
YouTube OAuth and provider verification are also excluded from this small
contract slice.

## Security and privacy invariants

- Tokens are opaque and bounded; no OpenAPI example or fixture may contain a
  real token or payment identifier.
- A ready TipIntent may return its intended amount/name/message; used, expired
  and unknown states must not expose any of those fields.
- Receipts are no-auth by design but remain token-scoped; unknown tokens return
  the standard bounded error envelope.
- Confirming a TipIntent takes only an idempotency header and optional
  Turnstile token; client-supplied amount, donor identity or message are not
  accepted.
- A payment-provider order is represented only by the existing bounded order
  response; provider credentials/instrument data are never part of this API.

## Acceptance and rollback

`pnpm contracts:validate` must validate all new operations and redacted positive
and negative fixtures. Existing API route tests must still prove token state,
single-use and no client-controlled amount. The route inventory must show the
four operations as covered and no stale operation. Rollback is a source-only
revert of the OpenAPI/fixture addition; runtime behavior and stored data are
unchanged.

## Local evidence — 2026-09-09

`pnpm contracts:validate` passed with 16 direct fixtures, 39 OpenAPI paths, 46
operation contracts and the existing three structural negative cases. Its new
fixture negatives reject amount disclosure on used/expired TipIntents and a
client-supplied amount in the confirmation request. Focused API TypeScript and
route tests passed 15/15 for receipt opacity/idempotency and TipIntent
secret/opacity/state/single-use/tamper/rate-limit/fail-closed behavior.
`pnpm contracts:route-inventory` reported 159 runtime operations, 46 covered,
113 pending and 0 stale. This completed slice reduces the pending queue by four
operations; it does not imply the remaining 113 are approved or documented.
