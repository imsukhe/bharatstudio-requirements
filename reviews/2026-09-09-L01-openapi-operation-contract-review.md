# L01 OpenAPI operation-contract review

**Decision state:** `Implemented and locally verified; surface-expansion decision remains open`
**Level:** L3
**Date:** 2026-09-09
**Reviewer:** Self-review; independent review unavailable.
**Authority:** `tasks/L01-contracts-and-database-baseline.md`

## Finding

**P1 — fixed.** The executable OpenAPI check only parsed YAML and resolved
local references. It could accept a document that exposed a duplicate client
operation name, lacked a path parameter declaration, or claimed a successful
response without any schema. The published channel PATCH schema also contained
the stale `avatarUrl` field rather than the runtime's `featuredConsent` and
validated `handle`; the maintenance request/202 response were likewise stale.

## Disposition

`bharatstudio-alerts/contracts/validate-openapi.mjs` now validates operation
identity, tags, path parameters, request-body schemas and all non-204 success
response schemas in addition to the existing OpenAPI/ref checks.
`contracts/test-openapi-validator.mjs` executes three deterministic negative
mutations in a temporary directory. The contract now matches the live channel
PATCH and maintenance route shapes for its approved v1 scope.

This did not publish or infer contracts for runtime routes that the current v1
authority has not yet accepted. In particular, v1's explicit YouTube exclusion
remains enforced by the existing capability scan.

`contracts/runtime-route-inventory.mjs` provides a deterministic route-to-
contract report. At this review it found 159 literal Fastify operations, 42
covered by the approved OpenAPI, 117 outside it, and no stale documented
operation. Those 117 operations remain an explicit completion queue; the
inventory is deliberately a report rather than a false green coverage gate
until each route is either brought into approved versioned documentation or
removed under a separately approved scope decision.

## Reproducible redacted evidence

- `cd bharatstudio-alerts && pnpm contracts:validate` — **11** JSON
  fixture/schema mappings, **35** paths, **42** operation contracts and **3**
  negative mutation cases pass.
- `cd bharatstudio-alerts && pnpm contracts:route-inventory` — **159** runtime
  operations, **42** documented, **117** outside the published surface, and
  **0** stale operations.
- `git diff --check` passed in Alerts and central requirements.

## Risk, rollback, and open gates

The change is contract/test-only; no database or external provider state was
changed. Reverting the validator would restore an incomplete-contract release
blind spot; a consumer compatibility issue should be addressed with an
additive versioned schema instead. Complete coverage of newly added runtime
routes, independent review, cross-client evidence, deployed provider/device
evidence and upgrade/rollback rehearsal remain open. No production-readiness
claim is made.
