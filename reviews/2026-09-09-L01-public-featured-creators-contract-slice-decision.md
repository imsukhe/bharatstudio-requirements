# Decision — L01 public featured-creators contract slice

**State:** Implemented locally; deployment/browser evidence remains open.

The runtime public projection is already intentionally narrow and opt-in. It
may be published as a versioned anonymous contract only with explicit schemas
that reject internal fields. This decision does not expand the route’s data
ownership or authorize wildcard CORS for any other endpoint.

## Evidence reviewed

- 21 executable fixture mappings and the 45-path/52-operation OpenAPI document
  validate cleanly.
- A hostile injected `channelId` is rejected by the public response schema.
- Focused runtime proof passes the narrow data, bounded request/unavailable
  repository, and wildcard-CORS-without-credentials cases (3/3).

During the same public-projection audit, the older `PublicChannel` OpenAPI
schema was corrected to remove stale optional `avatarUrl`. Runtime types, SQL
projection, and the underlying migration all intentionally exclude avatars; the
field was only a misleading documentation capability. Contract validation was
rerun after removal.

Residual deployment/browser evidence remains separate; no production-readiness
claim follows from local contract publication.
