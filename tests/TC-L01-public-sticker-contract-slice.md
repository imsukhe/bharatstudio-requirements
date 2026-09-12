# TC-L01 — Public sticker contract slice

**Status:** `Pass — local executable evidence`

## Acceptance

1. The anonymous picker publishes only the minimal sticker projection.
2. Attaching a sticker accepts only sticker/order identifiers and returns no
   payment or donor information.
3. Internal sticker metadata and payment-order fields are rejected by the
   independently executable wire-schema validation.
4. Route tests cover both the valid path and malformed, unavailable, disabled,
   unauthenticated, and unwired-store boundaries.

## Executed evidence — 2026-09-09

- `pnpm contracts:validate` — pass: 20 fixtures, 44 paths, 51 operations, and
  three negative OpenAPI cases. The two new hostile mutations inject `byteSize`
  into a public sticker list and `orderId` into a selection response; both fail
  schema validation as required.
- `apps/api`: `npx tsc --noEmit && npx tsx --test test/l22-stickers-routes.test.ts`
  — pass, 10/10.
- `pnpm contracts:route-inventory` — 159 literal runtime operations, 51 covered
  by approved OpenAPI, 108 still outside the published surface, 0 stale.

Residual evidence is limited to real payment/provider sandbox and deployed
ingress rehearsal. It is not inferred from local mocks.
