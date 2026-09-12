# TC-L01 — Public featured-creators contract slice

**Status:** `Pass — local executable evidence`
**Task:** [`../tasks/L01-public-featured-creators-contract-slice.md`](../tasks/L01-public-featured-creators-contract-slice.md)

| Case | Expected result |
| --- | --- |
| Valid anonymous listing | The versioned envelope exposes only the approved four creator fields. |
| Bounded request | `limit` is a typed integer from 1 through 100; the runtime default remains 60. |
| Privacy mutation | Schema validation rejects injected channel/account/financial/consent fields. |
| Availability and CORS | Missing repository fails closed; this one anonymous route permits `*` CORS without credentials. |

## Executed evidence — 2026-09-09

- `pnpm contracts:validate` — pass: 21 fixtures, 45 paths, 52 operations and
  three negative OpenAPI cases. A `channelId` privacy mutation is rejected by
  the featured-creators schema.
- `apps/api`: focused featured-listing suite — pass, 3/3.
- `pnpm contracts:route-inventory` — 159 literal operations, 52 covered, 107
  pending, 0 stale.

The wildcard CORS behavior remains limited to this credential-free anonymous
route; no deployed-browser or CDN evidence is inferred from the local proof.
