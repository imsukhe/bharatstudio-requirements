# Decision — L01 public sticker contract slice

**State:** Implemented locally; external payment and deployment evidence remains open.

The public sticker picker is intentionally a minimal projection: `id`, `name`,
and `category`. The selection acknowledgement contains only its schema version,
selection identifier and sticker identifier. Asset metadata, creator controls,
donor data and payment/order fields are excluded at the contract boundary.

The server remains authoritative for paid-order status, channel binding, tier,
and sticker enablement. This protects against a client trying to attach a
non-existent, disabled, or otherwise ineligible sticker.

## Evidence reviewed

- `pnpm contracts:validate`: 20 fixtures, 44 paths, 51 operations; hostile
  `byteSize` and `orderId` response-field injection tests reject as expected.
- `apps/api` focused L22 route test: TypeScript compile plus 10/10 route cases.
- Runtime/OpenAPI inventory: 159 literal operations, 51 covered, 108 explicitly
  queued, no stale documented operation.

## Residual gates

Actual payment-provider/store lifecycle and deployed ingress authorization need
staging/provider evidence. This decision makes no production-readiness claim.
