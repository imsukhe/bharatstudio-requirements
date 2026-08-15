# L01 — Contracts and database baseline

**Status:** `Implemented — local structural verification passing; cross-language and independent review pending`  
**Level:** L3  
**Owner:** Architecture / API / database  
**Depends on:** L00  
**Blocks:** L03–L07
**Test record:** `../tests/L01-contracts-and-database-baseline.md`  
**Contract draft:** `/Users/sukhdevsingh/Workspace/Bharat Studio/bharatstudio-alerts/contracts/CONTRACT_BASELINE.md`

## Objective

Create one v1 contract and data baseline usable by TypeScript, Go, mobile, Windows and macOS without sharing runtime implementation code.

## Scope

- Versioned OpenAPI for Creator API, public tip order, overlay session, entitlement and authenticated internal job endpoints.
- JSON Schemas for payment receipt, alert event, queue state, Cloud Tasks command, SSE overlay event and error envelope.
- JSON Schema for the approved FRD-011 core channel alert configuration and its versioned API response wrapper.
- D-2 multi-queue scenario schema with frozen per-delivery source priority and override values.
- The payment receipt/webhook contract includes the verified provider delivery identity; the alert contract includes source, binding, queue and per-queue delivery identity needed for independent multi-queue progress.
- Cross-language golden fixtures, including the Cloud Tasks delivery command, role/tier/event/error enums and JSON design tokens. Go worker compatibility tests consume the runtime delivery fixtures strictly; mobile/C#/Swift consumer evidence remains a separate gate.
- Reviewed clean v1 PostgreSQL baseline, roles, RLS context, immutable ledger/outbox and an explicit upgrade strategy.

## Tasks

1. Extract exact v1 API/event requirements from pending slices; mark unapproved fields as excluded.
2. Publish `v1` OpenAPI and JSON Schema contracts in Alerts `contracts/`; validate all examples in CI.
3. Define compatibility rules: additive fields allowed, breaking changes require a new version, producer/consumer deprecation window, event schema version required.
4. Create sanitized fixtures for paid tip, duplicate webhook with the same `x-razorpay-event-id`, missing/invalid provider event identity, held/approved/replayed alert, multi-queue source routing, per-source override, refund reversal, overlay reconnect, entitlement lock and helper action acknowledgement.
5. Build the v1 logical data model from approved scope; identify retained tables, removed YouTube/Enterprise tables, immutability and retention responsibilities.
6. Produce a new baseline migration plus a separate documented legacy-upgrade path. Preserve legacy migrations unchanged as evidence only.
7. Define database roles: request API, payment worker, alert worker, migration/admin, and no database role for scheduler/clients.
8. Define uniqueness and state ownership explicitly: provider/account/environment plus Razorpay event ID for webhook delivery deduplication; payment/refund/dispute IDs as separate business keys; per-queue outbox state for multi-queue delivery; no global event status may block an independent queue.

## Acceptance criteria

- TypeScript, Go, C#, Swift and mobile implementers can generate/hand-write types from one stable contract source.
- No v1 contract contains YouTube scopes/events or Enterprise data/roles.
- Payment and alert state transitions are explicit, append-only where required, idempotent and testable.
- The webhook contract names `x-razorpay-event-id` as the delivery deduplication key; timestamps, random IDs and request IDs are not acceptable substitutes.
- Multi-queue source routing has independent per-queue state and verified source/priority and per-source override semantics.
- D-2 scenario and per-queue delivery fixtures include `sourcePriority` and `overrideValues` as explicit accepted-delivery inputs.
- The standalone per-queue delivery schema/fixture also carries `overrideValues`; the overlay projection must expose the immutable delivery snapshot rather than only the shared event payload.
- Contract fixtures declare their `$schema` URI and every direct fixture must validate against its referenced Draft 2020-12 schema; schema metadata is part of the accepted fixture envelope, not an undocumented extra property.
- The repository validator must enforce Draft 2020-12 formats (`uuid`, `date-time`, `uri`) and validate every committed fixture, including the duplicate-webhook scenario wrapper.
- The repository validator must parse OpenAPI 3.1 and resolve every local `$ref`; `pnpm contracts:validate` is the required single command for JSON fixtures and OpenAPI contract validation.
- The repository validator must scan executable v1 contract artifacts (OpenAPI, JSON Schemas, enums and fixtures) and fail if YouTube or Enterprise capability terms/scopes are introduced; planning documents are outside this executable-contract scan.
- RLS context and bypass list are exact and reviewed.
- Baseline/upgrade approach is approved before any database is provisioned.

## Rollback

Contracts and baseline remain draft until approved. No shared/production database migration runs in this task.

## Fresh local audit — 2026-08-15

The executable contract tree, fixture validator, OpenAPI document, Go worker
consumer checks and L01 acceptance record were rechecked. No additional local
contract defect was found.

`pnpm contracts:validate` passes all eleven committed fixture mappings, Draft
2020-12 format enforcement, the excluded-capability scan and the OpenAPI 3.1
document with 32 local `$ref` targets resolved. The disposable PostgreSQL
harness also passes the current L01/L02/L03 database behavior slice.

L01 remains open for React Native and Windows/C# consumer evidence, independent
architecture review, and a data-preserving upgrade/rollback drill. The macOS
Swift consumer slice is now locally evidenced separately: hand-written
Codable models decode the approved state, layout and control-session response
shapes, including the exact `channelId`, `targetId`, `sessionId` and
`clientInstanceId` wire keys; `swift test` passes 7/7. These local consumer
checks still cannot substitute for independent review or the upgrade/rollback
evidence required for L01 closure.

### Windows C# consumer boundary — 2026-08-15

Added `bharatstudio-companion-desktop/windows/CompanionContract.cs` with strict
JSON response models for Companion state, layouts, control sessions and action
results. The decoder rejects unknown fields, invalid UUIDs/counts, duplicate or
out-of-range layout slots, unsupported action/status values and malformed
client-instance bounds before the future Windows UI can consume a response.
This is source-level contract evidence only; Windows SDK/.NET compilation,
runtime tests, signing and independent review remain open.
