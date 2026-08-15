# L01 acceptance and test record — contracts and database baseline

**Status:** `Static contract tree complete; database/fixture evidence passing; cross-language and independent review pending`  
**Task:** `../tasks/L01-contracts-and-database-baseline.md`  
**Contract draft:** `/Users/sukhdevsingh/Workspace/Bharat Studio/bharatstudio-alerts/contracts/CONTRACT_BASELINE.md`

These tests are the minimum acceptance record for the v1 baseline. They use synthetic data and an isolated database only.

| ID | Setup/action | Expected result |
|---|---|---|
| L01-01 | Validate OpenAPI, JSON Schemas, fixtures and enums in CI | OpenAPI 3.1 parses, all local `$ref` targets resolve, and no YouTube/Enterprise scope appears; every committed fixture validates with Draft 2020-12 and `uuid`/`date-time`/`uri` format enforcement; no undocumented required field exists | `pnpm contracts:validate`; 11 fixture/schema pairs and 32 OpenAPI paths pass with Ajv 2020 + `ajv-formats` + YAML parser. |
| L01-02 | Submit two concurrent Razorpay deliveries with the same verified `x-razorpay-event-id` | One provider-delivery record, one financial effect, one alert evidence path |
| L01-03 | Submit distinct provider event IDs referencing the same payment/refund entity | Deliveries remain separately traceable; business-entity uniqueness rules do not erase delivery evidence |
| L01-04 | Route one permitted source event to queues A and B; block A and process B | B progresses independently; no global event status blocks B; audit records identify source, binding and queue |
| L01-05 | Apply source-specific priority/style/bracket/rate-limit overrides | Only the intended source/queue delivery changes; unrelated queues retain their frozen configuration |
| L01-06 | Connect overlay to replica B, commit/publish through replica A, disconnect live notification, reconnect with cursor | Live event or durable replay delivers exactly once per delivery policy and in order; missed notification does not lose the event |
| L01-07 | Create clean isolated database from the new baseline | Roles, constraints, append-only tables, per-queue state and RLS context are present; no legacy migration is required |
| L01-08 | Run representative synthetic upgrade path | Upgrade is additive/explicit, reversible or recoverable, and does not rewrite financial evidence |
| L01-09 | Exercise request API, payment service, alert worker, migration/admin and scheduler identities | Each role can perform only its approved operations; scheduler and clients cannot access the database directly |
| L01-10 | Validate the executable v1 contract tree for YouTube/Enterprise fields, scopes and routes | The contract validator fails closed if an excluded capability term is introduced into OpenAPI, schemas, enums or fixtures; planning-document mentions do not affect this scan |
| L01-11 | Validate every runtime JSON Schema against at least one direct fixture | All eleven committed fixture/schema mappings validate; the duplicate-webhook wrapper is validated by its dedicated wrapper schema; format enforcement is active | `pnpm contracts:validate`; Ajv 2020 + `ajv-formats`; alert event, Cloud Tasks command, entitlement result, error envelope, multi-queue, overlay reconnect, overlay SSE, payment webhook, duplicate-webhook wrapper and queue delivery all pass. |
| L01-12 | Validate the D-2 multi-queue scenario fixture | Both permitted deliveries carry explicit source priority and override snapshots; the scenario asserts queue-B progress is independent of queue-A hold/global event state | `contracts/json-schema/multi-queue-delivery.schema.json`, `contracts/fixtures/multi-queue-delivery.json`; TypeScript/Ajv, Go strict-consumer compatibility test, structural review and disposable DB evidence pass locally; React Native/Windows-C# consumer evidence remains pending; macOS Swift evidence is recorded in L01-14 |
| L01-13 | Validate the standalone per-queue delivery fixture and overlay replay projection | A per-queue delivery carries `overrideValues`, and overlay replay exposes the immutable queue/binding/priority/override snapshot for each delivery | `contracts/json-schema/queue-delivery.schema.json`, `contracts/fixtures/queue-delivery.json`, migration `0020`; TypeScript/Ajv, Go strict-consumer compatibility test, JSON parse and disposable DB evidence pass locally; React Native/Windows-C# consumer evidence remains pending; macOS Swift evidence is recorded in L01-14 |
| L01-14 | Decode approved Companion REST response shapes in the macOS Swift consumer | Hand-written Codable transport models decode the approved state, layout and control-session envelopes using exact wire keys; unsupported action names are rejected | `bharatstudio-companion-desktop/macos/Sources/BharatStudioCompanionMacOS/CompanionContract.swift`, `CompanionContractTests.swift`; `swift test` 7/7, pass locally on 2026-08-15. React Native/Windows consumer, independent review and upgrade/rollback evidence remain pending |
| L01-15 | Consume Companion REST response envelopes in the React Native client | Mobile runtime validation accepts only the approved v1 state, queue, layout, action-result and control-session shapes; UUID identifiers, exact known fields, bounded labels/pages, unique slot indexes, malformed dates/counts and unsupported actions fail as bounded request failures before UI use | `bharatstudio-companion-mobile/src/api/CompanionApi.ts`, `src/api/CompanionApi.test.ts`; Jest 23/23, lint and TypeScript checks pass locally on 2026-08-15. Windows/C# consumer, independent review and upgrade/rollback evidence remain pending |
| L01-16 | Consume Companion REST response envelopes in the Web client | Web runtime validation accepts only the approved v1 user, queue, state, layout and action-result shapes; malformed UUID/date/count/slot values, unsupported tiers/actions and duplicate slot indexes fail closed before UI use | `bharatstudio-alerts/apps/web/app/lib/api.ts`; Web TypeScript check and production build pass locally on 2026-08-15. Windows/C# consumer, independent review and upgrade/rollback evidence remain pending |
| L01-17 | Consume Companion REST response envelopes in the Windows C# consumer | The Windows transport boundary accepts only v1 state/layout/control-session/action-result shapes, rejects unknown fields, empty identifiers, invalid counts/slots, duplicate layout slots and unsupported status values before UI use | `bharatstudio-companion-desktop/windows/CompanionContract.cs`; source boundary added 2026-08-15. Windows SDK/.NET build, runtime tests, signing and independent review remain pending |

## Evidence required for closure

**Executed contract validation — 2026-08-15:** `pnpm contracts:validate` passed for all eleven committed mappings using Ajv Draft 2020-12 plus `ajv-formats`, parsed the OpenAPI 3.1 document with all 32 paths and local `$ref` targets resolved, and scanned executable contract artifacts for excluded YouTube/Enterprise capability terms. The validator checks that each fixture's `$schema` matches the selected schema and runs a negative invalid-UUID case, proving that `uuid`, `date-time` and `uri` formats are enforced. The duplicate-webhook file is validated by its dedicated wrapper schema, which validates both nested delivery objects against the payment delivery schema. The Go worker now strictly consumes the committed Cloud Tasks, multi-queue, per-queue delivery, overlay SSE and payment webhook fixtures, rejects unknown fields, and checks UUID/time/source-routing invariants. This is Go-consumer evidence only; React Native/C#/Swift consumer evidence and independent review remain open.

- CI validation output with commit and tool versions.
- Isolated database migration and rollback/recovery output.
- Redacted RLS/role negative-test output.
- Cross-language fixture results for TypeScript, Go, React Native, C# and Swift consumers.
- Independent review record with all findings dispositioned.

No test is considered passed from a document inspection alone.

The sentence in the historical executed-validation paragraph that lists
React Native, C# and Swift together predates L01-14. Current status is that
macOS Swift contract decoding is evidenced by L01-14; React Native and
Windows/C# consumer evidence, independent review and upgrade/rollback remain
open.

L01-15 adds the React Native runtime-decoding slice. Current cross-language
status is macOS Swift, React Native and the Web client locally evidenced;
Windows/C# consumer evidence, independent review and upgrade/rollback remain
open.

## Fresh local audit evidence — 2026-08-15

The repository contract command was rerun and passed: eleven fixture/schema
mappings, OpenAPI 3.1 with 32 paths and local references, format validation and
the v1 excluded-capability scan. The Go strict-consumer checks and disposable
PostgreSQL L01/L02/L03 harness also remain passing.

This closes only the locally executable contract slice plus the macOS Swift
consumer slice recorded as L01-14. React Native and Windows/C# consumer checks,
independent architecture review, and a data-preserving upgrade/rollback drill
remain open acceptance evidence.
