# Decision — L01 overlay asset contracts

**State:** `Accepted for local verification; deployment evidence remains open`

Browser-consumed overlay assets require versioned API contracts. This approves
contract publication only; runtime behavior remains unchanged.

## Review outcome — 2026-09-12

Reviewed the OpenAPI contract against the mounted runtime routes and their
tests. The previously unpublished Lottie-list, Lottie-artifact, and
audio-artifact operations now match the route paths, bearer boundary, UUID
parameters, success media types, 401/404/503 outcomes, and private no-store
artifact behavior. The published surface has zero stale operations.

The fixture uses an intentionally narrow public projection. Negative proofs
reject channel identity leakage and an unsupported display style. Runtime tests
also cover malformed bearer input and both asset cache-control headers.

Accepted on local evidence: 39 contract fixtures, 418 API tests, and the full
`verify:local` deterministic suite. This review does not substitute for a
deployed browser, CDN, or provider/device staging rehearsal.
