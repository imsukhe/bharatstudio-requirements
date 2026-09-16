# TC-PRF-02 slice 5 — Stream Mission Card (§6 module #9)

**Task:** [`../active/tasks/PRF-02.md`](../active/tasks/PRF-02.md) ("Slice 5" section)
**Authority:** [`../FULL-PRODUCT-DEFINITION.md`](../FULL-PRODUCT-DEFINITION.md) §6 (module table row 9, owner decisions 2026-09-16), §9.1.1, §12.6, §12.7, §15.4.3, §19.4, §19.5, §30.3, §34
**Scope review:** [`../reviews/2026-09-16-prf-02-slice-5-scope-review.md`](../reviews/2026-09-16-prf-02-slice-5-scope-review.md)
**Decision record:** [`../reviews/2026-09-16-prf-02-slice-5-stream-mission-implementation.md`](../reviews/2026-09-16-prf-02-slice-5-stream-mission-implementation.md)
**Owner:** Sukhdev Singh
**Status:** `Conditionally complete — local verification passed; independent review unavailable`

This record covers only slice 5: §6 module #9, Stream Mission Card, as a
complete vertical slice (schema, creator read/write, overlay read,
contract, EXPLAIN artefact, renderer, tests). It is not, and does not
claim to be, evidence that PRF-02's full register row is done — twelve
catalogue modules remain unbuilt, and §19.0 RT-07 (blocked) is still the
only row that can supply OBS/device/frame-timing/8-hour-memory evidence;
nothing below is that. **PRF-02 remains register letter `A`.**

## Schema and SQL layer — `packages/db/tests/prf02_slice5_stream_mission.sql`

| Case | Control | Expected evidence | Status |
|---|---|---|---|
| S5.1 | Objective bound is exactly 1–120, reusing `0109`'s challenge-title bound | A 120-character objective is accepted; a 121-character objective is rejected (`22023`); an empty objective is rejected (`22023`) | **Passing** |
| S5.2 | Only owner/admin may start a mission | `start_stream_mission` called as an `operator`, `moderator`, `viewer` and as a non-member each raises `42501` | **Passing** |
| S5.3 | Only owner/admin may end a mission | `end_stream_mission` called as a `viewer` raises `P0002` — the not-authorised answer is deliberately indistinguishable from not-found | **Passing** |
| S5.4 | At most one running mission per channel | Starting a second mission while one is running raises `23505`; the partial unique index `stream_missions_channel_running_idx` is the hard guarantee behind it | **Passing** |
| S5.5 | Ending then starting is allowed | After `end_stream_mission`, a new `start_stream_mission` on the same channel succeeds — the index constrains *running* missions only, never the durable history | **Passing** |
| S5.6 | Ending is idempotent-safe, not silently repeatable | Ending an already-ended mission raises `P0002`; ending a mission belonging to another channel raises `P0002` | **Passing** |
| S5.7 | Creator read returns the current mission at every tier | `list_channel_stream_mission` returns the running mission for a `free`-tier channel exactly as for `studio` — storing/reading a durable creator record is never tier-gated (§12.6) | **Passing** |
| S5.8 | Creator read is visible to every channel member, zero rows to a non-member | Owner, admin, operator, moderator and viewer each see the row; a non-member sees zero rows | **Passing** |
| S5.9 | Overlay read is gated by the existing token-fingerprint model | A correct `(overlay_id, token_fingerprint)` pair returns the mission; a wrong fingerprint, a revoked session and an expired session each return zero rows | **Passing** |
| S5.10 | Overlay read is cross-channel isolated | Channel B's overlay session never sees channel A's mission | **Passing** |
| S5.11 | §12.7 bounded — at most the current mission, never a history | With one ended and one running mission on the same channel, the overlay read returns exactly one row, the running one; with only ended missions it returns zero rows | **Passing** |
| S5.12 | The overlay projection carries no identity and no clock-bound field | `list_overlay_stream_mission` returns exactly `mission_id`, `objective`, `started_at` — asserted against `information_schema.parameters` so a future added OUT column fails this test rather than silently widening the projection | **Passing** |
| S5.13 | No duration/timer/expiry column exists anywhere on the table | `information_schema.columns` for `public.stream_missions` contains no column whose name matches `%duration%`, `%timer%`, `%expire%`, `%deadline%` or `ends_at` | **Passing** |
| S5.14 | RLS and grants match the channel-owned-table pattern | `public.stream_missions` has `relrowsecurity` true and no direct privilege granted to `bsa_app`; all four `app_private` functions have `execute` revoked from `public` and granted to `bsa_app` | **Passing** |

## API layer — `apps/api/test/prf02-stream-mission-routes.test.ts`

| Case | Control | Expected evidence | Status |
|---|---|---|---|
| S5.15 | Creator read route | `GET /v1/channels/:channelId/stream-mission` returns the store's mission; a channel with none returns `{ mission: null }`, never a fabricated one | **Passing** |
| S5.16 | Creator read without a session | `401`, and the store is never called | **Passing** |
| S5.17 | Creator read without a configured store | `503` with `stream_mission_store_unavailable`, never a `200` with an empty body masquerading as "no mission" | **Passing** |
| S5.18 | Start route, happy path | `POST /v1/channels/:channelId/stream-mission` with a valid objective returns `201` and the created mission, and passes `(userId, channelId, objective)` to the store unchanged | **Passing** |
| S5.19 | Objective bound enforced at the schema layer | A 121-character objective is rejected `400` **before the store is ever called**; a 120-character objective is accepted; an empty objective is rejected `400` | **Passing** |
| S5.20 | No clock-bound field is accepted on the wire | A body carrying `durationSeconds`/`endsAt` alongside a valid objective is rejected `400` by `additionalProperties: false`, before the store is called | **Passing** |
| S5.21 | Conflict mapping | A store `conflict` outcome (a mission already running) becomes `409` with `stream_mission_already_running`, never a `500` and never a silent supersede | **Passing** |
| S5.22 | Forbidden mapping | A store `forbidden` outcome becomes `404 not_found`, never a leaking `403` | **Passing** |
| S5.23 | End route | `POST /v1/channels/:channelId/stream-mission/:missionId/end` returns `204`; a `not_found` outcome returns `404`; a thrown store error returns a retryable `503` | **Passing** |
| S5.24 | Overlay read route auth | `GET /v1/overlay-widgets/:overlayId/stream-mission` without a bearer token is `401`; with one it passes the raw token to the store | **Passing** |
| S5.25 | Overlay read route degradation | A thrown store error is a retryable `503`, never a `500`; a missing store is a `503`, never a `200` with `mission: null` masquerading as "no mission" | **Passing** |
| S5.26 | Overlay response shape | The `200` body is exactly `{ schemaVersion, mission }` where mission is `{ schemaVersion, missionId, objective, startedAt }` or `null` — no identity field, no end-shaped field | **Passing** |

## Contract layer — `pnpm contracts:validate`

| Case | Control | Expected evidence | Status |
|---|---|---|---|
| S5.27 | The overlay fixture validates against its schema | `contracts/fixtures/overlay-stream-mission-response.json` validates against `contracts/json-schema/overlay-stream-mission-response.schema.json` (Draft 2020-12, format enforcement on) | **Passing** |
| S5.28 | A clock-bound field cannot enter the contract | Adding `endsAt`, `durationSeconds` or `expiresAt` to the fixture is **rejected** by the schema — three separate negative cases in `contracts/validate-fixtures.mjs`, so the owner's session-bounded decision is checked by the build on every run, not merely promised in a document | **Passing** |
| S5.29 | Viewer/payment identity cannot enter the contract | Adding `viewerAccountId` or `paymentId` to the fixture's mission object is rejected | **Passing** |
| S5.30 | An over-long objective cannot enter the contract | A 121-character objective is rejected by the schema's `maxLength: 120` | **Passing** |
| S5.31 | The four new OpenAPI operations are contract-valid | `validate-openapi.mjs` accepts the four paths with unique `operationId`s, tags, required path parameters with schemas, required request bodies where present, and a described, schema-bearing 2xx for each | **Passing** |

## EXPLAIN / RT-12 layer — `pnpm explain:check`

| Case | Control | Expected evidence | Status |
|---|---|---|---|
| S5.32 | The new overlay read is in the manifest with a current artefact | `required-queries.json` carries `app_private.list_overlay_stream_mission` → `stream-mission.explain.md`; `check-plans.mjs` re-extracts the function body from `0135` and matches the recorded `query_hash` | **Passing** |
| S5.33 | Rule 1 (convention scan) passes on substance | The `app_private.list_overlay_stream_mission(` call in `apps/api/src/db/stream-mission-overlay-store.ts` is found by the `list_overlay_*` convention scan and is manifested | **Passing** |
| S5.34 | Rule 2 (overlay-store-file scan) passes on substance | The store filename contains "overlay", so every `app_private` call inside it is scanned; the one call present is manifested, with no exemption added | **Passing** |
| S5.35 | Rule 3 (composition-root derived-read scan) passes on substance | `apps/api/src/index.ts` constructs `createSqlStreamMissionOverlayStore(derivedReadSql!)`, so rule 3 resolves that factory through index.ts's own import, brace-matches its body and scans it; the one `app_private` call inside is manifested | **Passing** |

## Renderer and canvas layer — `apps/web/.../stream-mission-module.test.ts`, `master-canvas-integration.test.ts`

| Case | Control | Expected evidence | Status |
|---|---|---|---|
| S5.36 | The objective renders from the single fetched snapshot | The objective text and the elapsed reading render from one `StreamMission` snapshot; the container becomes visible only after a real snapshot lands | **Passing** |
| S5.37 | Nothing is shown before the first real snapshot | With no snapshot yet delivered, the container's opacity stays `0` and no text is painted — a mission is never invented | **Passing** |
| S5.38 | No mission configured hides the card | `fetchSnapshot` resolving `null` hides the card; a mission that ends mid-stream hides it on the next re-read, with no timer involved | **Passing** |
| S5.39 | The elapsed reading counts **up** from `startedAt` and never toward an end | Advancing the injected clock increases the reading monotonically; the module exposes no end time, and `StreamMissionModuleOptions` has no field of any kind for one — a compile-time check that fails to build if such a field is ever added | **Passing** |
| S5.40 | The elapsed reading updates once per whole second, not once per frame | Repeated `render()` calls within the same whole second write to the DOM exactly once | **Passing** |
| S5.41 | Composite-only (PRF-03) | Only `opacity` and `transform` are ever written; `width`, `height`, `top` and `left` stay unset — verified in the test and by `node .github/scripts/canvas-static-check.mjs` | **Passing** |
| S5.42 | Reduced motion is a perceivable alternative, not a faster animation | Under `prefers-reduced-motion` the entrance transition is `none` while the objective and the elapsed reading still render and still update — information is never suppressed as if it were motion | **Passing** |
| S5.43 | Malformed payloads degrade, never throw | A payload failing the module's own `isStreamMission` guard is ignored; the last good mission keeps rendering | **Passing** |
| S5.44 | `deactivate()` hygiene | `deactivate()` unsubscribes, discards a late in-flight fetch via the monotonic fetch token, and is idempotent | **Passing** |
| S5.45 | Fonts are data, never hard-coded (§15.4.3 precondition) | Every font family on every element comes from `defaultCanvasTextStyles()`; no family string is inlined in the module | **Passing** |
| S5.46 | Eight modules: still exactly one connection and one rAF chain | With all eight built modules registered and entitled, the shared `MasterCanvasConnection` opens exactly one transport connection with eight subscribers and the manual frame scheduler holds exactly one pending frame handle | **Passing** |
| S5.47 | Never a second overlay session or transport | The module's options carry no `overlayId`/`token`/`apiOrigin` of their own — it receives only the shared `connection` and a `fetchSnapshot` closure from the host page, so it structurally cannot open a session | **Passing** |
| S5.48 | No third-party code (§9.1.1) | The module imports only first-party modules (`master-canvas-runtime`, `master-canvas-connection`, `text-rendering`) — no CDN URL, no script tag, no iframe, no external stylesheet anywhere in the file | **Passing** |

## Negative test of a new guard, performed and restored

Case S5.19's guard (the 120-character objective bound at the route's JSON
schema layer) was deliberately broken and re-run to prove the test fails
when the guard is absent, then restored. Both outputs are recorded in
[`../reviews/2026-09-16-prf-02-slice-5-stream-mission-implementation.md`](../reviews/2026-09-16-prf-02-slice-5-stream-mission-implementation.md)
under "Negative test". A guard that has never been observed failing is not
a verified guard.

## Commands run — this worktree, 2026-09-16, from `bharatstudio-alerts`

`pnpm db:test:all` · `pnpm --filter @bharatstudio/alerts-api test` ·
`pnpm --filter @bharatstudio/alerts-web test` ·
`pnpm --filter @bharatstudio/alerts-api build` · `pnpm contracts:validate` ·
`pnpm explain:check`

Exact result lines are recorded in `../active/tasks/PRF-02.md`'s "Slice 5"
section and in the implementation review. They are not duplicated here.

## What this evidence is not

Same rule as slices 1–4, restated because it is the one most likely
skimmed past: every result is **local** — a Dockerised PostgreSQL 16, the
Node test runner, JSDOM. None of it is OBS, Chromium, a real device, a
real network, a provider, a store, a legal review or a release. The
EXPLAIN artefact is a plan-**shape** change detector captured against a
minimally-seeded database; it is not evidence that any §19.4 performance
budget is met at §37.4's production-scale dataset. §19.0's RT-07 (blocked)
remains the only row that can gate a frame-timing, GPU-compositing,
memory-over-8-hours or "one source replaces twelve" claim, and this slice
neither closes nor touches it.
