# Decision and review — L01 public donor contract completion slice

**Date:** 2026-09-09  
**State:** `Implemented and locally verified; independent review open`  
**Authority:** L01 contract baseline; L14 receipts; L15 TipIntent short links

## Decision

The existing public receipt and TipIntent browser flows are contract-bearing
interfaces and must not remain undocumented merely because their tokens are
opaque. They are added to the published v1 OpenAPI surface with explicit
state/privacy variants. The connector-secret TipIntent creation operation stays
outside public OpenAPI until its private service contract receives a separate
scope decision.

## Review boundaries

This decision publishes no new capability and changes no runtime behavior,
database schema, data retention, authentication, provider integration or
deployment topology. It requires redacted fixtures and API regression evidence.
Provider sandbox, Turnstile, Google OAuth, real receipt data, staging and
independent review remain external gates.

## Implementation review

The published OpenAPI has four new `PublicDonor` operations with typed path
parameters, idempotency header, request bodies and success responses. Ready and
closed TipIntent responses are separate closed schemas so used/expired states
cannot carry amount/name/message. The contract fixture harness validates both
redacted positive states and hostile disclosure/tampering mutations. No runtime
route, schema migration, credential or data-retention behavior changed.
