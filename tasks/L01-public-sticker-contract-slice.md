# L01 — Public sticker contract slice

**Status:** `Implemented locally — fixture, route, and hostile-field evidence recorded`  
**Level:** L3  
**Authority:** L01 baseline and L22 curated-sticker scope

The public picker exposes only id/name/category. Attachment accepts only order
and sticker UUIDs and is server-side revalidated for channel, paid state, tier
and enablement. No asset byte data, creator settings, donor identity or payment
detail is public.

## Local completion evidence — 2026-09-09

- `pnpm contracts:validate` passed with 20 fixture/schema mappings, 44 OpenAPI
  paths, 51 operation contracts and three structural negative cases.
- `apps/api`: `npx tsc --noEmit && npx tsx --test test/l22-stickers-routes.test.ts`
  passed 10/10, including public projection, valid selection, unavailable or
  disabled sticker rejection and malformed-body rejection.
- The picker fixture contains only the public `id`, `name`, and `category`
  projection. The validator proves an injected internal `byteSize` field is
  rejected. The selection response fixture contains no payment order detail;
  the validator proves an injected `orderId` is rejected.

Store/order payment status, channel ownership, entitlement tier and sticker
enablement remain server-side checks. Provider sandbox and deployed ingress
evidence are external gates; this local slice does not claim either.
