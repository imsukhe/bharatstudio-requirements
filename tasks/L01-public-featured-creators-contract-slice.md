# L01 — Public featured-creators contract slice

**Status:** `Implemented locally — executable evidence recorded`
**Level:** L3
**Authority:** L01 contract baseline; L03 featured-creator public projection

Publish only the existing anonymous read route
`GET /v1/public/featured`. The wire projection is limited to `handle`,
`displayName`, `acceptingTips`, and `locale`, within a schema-versioned envelope.
The bounded optional `limit` query is 1–100 (default 60).

No channel ID, consent flag, tier, financial, account, contact, configuration,
or identity data is public. The route remains read-only and credential-free;
wildcard CORS is intentionally scoped to this anonymous projection only.

## Local completion evidence — 2026-09-09

- `pnpm contracts:validate` passed 21 fixtures, 45 OpenAPI paths, 52 operation
  contracts and three structural-negative cases.
- The fixture contract rejects injected `channelId`, proving the anonymous list
  cannot silently grow an internal identifier field.
- `apps/api`: `npx tsc --noEmit && npx tsx --test --test-name-pattern='featured-creator listing' test/app.test.ts`
  passed 3/3: narrow projection, request bounds/unavailable-store failure, and
  the no-credentials wildcard-CORS exception.
- Route inventory is 159 literal runtime operations, 52 covered, 107 explicitly
  outside the published surface, and 0 stale operations.

This slice does not add marketing, account or provider behavior. Deployed
browser/CDN behavior remains a separate external gate.
