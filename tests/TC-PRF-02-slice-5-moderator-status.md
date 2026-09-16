# TC-PRF-02 slice 5 — Moderator Status Card (§6 #12), held half only

**Task:** `../active/tasks/PRF-02.md` ("Slice 5" section)
**Authority:** `../FULL-PRODUCT-DEFINITION.md` §6 (module #12, owner decisions 2026-09-16), §9.1.1, §12.7, §19.4, §19.5, §30.3
**Scope review:** `../reviews/2026-09-16-prf-02-slice-5-scope-review.md`
**Implementation review:** `../reviews/2026-09-16-prf-02-slice-5-moderator-status-implementation.md`
**Owner:** Sukhdev Singh
**Status:** `Conditionally complete — local verification passed; independent review unavailable`

This record covers only slice 5: §6 module #12's **held half**, as the
eighth built renderer on the runtime slices 1–4 already proved, plus the
one overlay read path it needed. It is not, and does not claim to be,
evidence that PRF-02's full register row is done — twelve catalogue
modules remain unbuilt, safe mode (the other half of #12) is unbuilt and
undecided, and §19.0 RT-07 (Blocked) is still the only row that can
supply OBS/device/frame-timing/8-hour-memory evidence. **PRF-02 remains
register letter `A`;** no state letter is self-assigned.

## The property that matters most, and how it is proven

§6's "never private content" is proven as a **property of the query**,
not of the renderer. `app_private.list_overlay_moderator_status`
(migration `0136`) declares `returns table (held_count bigint)` — one
column. Case **S5.4** asserts the *actual returned column set* two
independent ways: from the catalogue
(`pg_catalog.pg_get_function_result`), and from a table materialised out
of a real call to the function, read back through
`information_schema.columns`. Either assertion fails the moment a second
column is added, whatever it is called. The negative test recorded in the
implementation review confirms this by adding a forbidden column and
observing the suite go red before restoring it.

| Case | Control | Expected evidence | Status | Where |
|---|---|---|---|---|
| S5.1 | Held deliveries are counted, scoped to the channel | A channel with held deliveries reads back exactly that many; deliveries in every other status (`pending`, `ready`, `displayed`, `acknowledged`, `failed_retriable`, `quarantined`, `suppressed`, `refunded_after_display`) are never counted | **Passing** | `prf02_slice5_moderator_status.sql` |
| S5.2 | The zero case is a real row reading zero | A valid overlay session for a channel with nothing held returns **one** row whose `held_count` is `0` — never zero rows, so the client can tell "nothing held" from "not authorised" | **Passing** | `prf02_slice5_moderator_status.sql` |
| S5.3 | A bad/foreign/expired/revoked token returns zero rows | A wrong fingerprint, another channel's session, an expired session and a revoked session each return **zero rows** — never an error, never a row, never another channel's count | **Passing** | `prf02_slice5_moderator_status.sql` |
| S5.4 | **Privacy by construction: the returned column set is exactly `{held_count}`** | `pg_get_function_result` reads exactly `TABLE(held_count bigint)`, and a table materialised from a live call has exactly one column named `held_count` — asserted from the catalogue *and* from real output, so neither a signature edit nor a select-list edit can slip past | **Passing** | `prf02_slice5_moderator_status.sql` |
| S5.5 | **No safe-mode surface exists on this path** | The function's own source text (`pg_get_functiondef`) contains no `is_paused`, no `safe_mode`, and no `closed_at` — the owner's decision 1 proven against the shipped definition, not against a comment | **Passing** | `prf02_slice5_moderator_status.sql` |
| S5.6 | Queue lifecycle does not change the count | Held deliveries on a paused queue and on a closed queue are still counted; pausing or closing a queue changes the count by zero — a delivery state, not a queue state | **Passing** | `prf02_slice5_moderator_status.sql` |
| S5.7 | Route: no bearer token is 401, never 200 | `GET /v1/overlay-widgets/:overlayId/moderator-status` with no `Authorization`, and with a malformed one, answers `401 overlay_unauthorized` with a `traceId` | **Passing** | `prf02-slice5-moderator-status-routes.test.ts` |
| S5.8 | Route: the exact token is forwarded to the store, unmodified | The store receives byte-for-byte the token the header carried; the response body is the store's own answer | **Passing** | `prf02-slice5-moderator-status-routes.test.ts` |
| S5.9 | Route: an unrecognised token yields `null`, never another session's count | A store recognising exactly one token returns `null` for every other; the route surfaces `{ moderatorStatus: null }`, `200` | **Passing** | `prf02-slice5-moderator-status-routes.test.ts` |
| S5.10 | Route: unwired or throwing store is a retryable 503, never 500/401, and leaks nothing | `503 master_canvas_store_unavailable`, `retryable: true`; the thrown error's message text appears nowhere in the response | **Passing** | `prf02-slice5-moderator-status-routes.test.ts` |
| S5.11 | **Route: the projection strips anything the store hands up beyond the count** | A deliberately polluted store answer (supporter name, message text, amount, delivery id, viewer id, queue id) is projected down to `{ schemaVersion, heldCount }` and nothing else — the route is a second, independent narrowing, not a pass-through that trusts the store | **Passing** | `prf02-slice5-moderator-status-routes.test.ts` |
| S5.12 | Route: a non-integer or negative count never reaches the client | A store answering a negative, fractional or non-numeric count yields `moderatorStatus: null` rather than a rendered nonsense figure | **Passing** | `prf02-slice5-moderator-status-routes.test.ts` |
| S5.13 | Guard: `isModeratorStatus` accepts only the exact shape | Exactly the declared keys, `schemaVersion: 'v1'`, a non-negative safe integer count; every extra key, missing key, wrong type, negative and fractional value is rejected | **Passing** | `moderator-status-logic.test.ts` |
| S5.14 | Copy: the label names held **deliveries**, never chat messages | `formatHeldLabel` renders `1 held for review` / `4 held for review`; the rendered text contains none of `message`, `chat`, `comment` | **Passing** | `moderator-status-logic.test.ts`, `moderator-status-module.test.ts` |
| S5.15 | **Renderer: the zero case hides the card and writes no copy** | `heldCount: 0` leaves the container at `opacity: 0` with empty text — no "all clear", no tick, no celebratory string of any kind | **Passing** | `moderator-status-module.test.ts` |
| S5.16 | Renderer: a non-zero count shows the card | `heldCount: 3` sets `opacity: 1` and renders `3 held for review` | **Passing** | `moderator-status-module.test.ts` |
| S5.17 | Renderer: falling back to zero re-hides the card | A count going `3 → 0` returns the container to `opacity: 0` and clears the text — the card does not latch on | **Passing** | `moderator-status-module.test.ts` |
| S5.18 | Renderer: `null`/malformed snapshot renders nothing visible | `fetchSnapshot` resolving `null`, throwing, or resolving a payload failing the guard leaves the card hidden and never throws out of `render()` | **Passing** | `moderator-status-module.test.ts` |
| S5.19 | **Renderer: composite-only (PRF-03)** | `render()` writes only `opacity`/`transform`; `width`/`height`/`top`/`left` stay unset — asserted in the module's own test and by the repository's static scanner | **Passing** | `moderator-status-module.test.ts`, `node .github/scripts/canvas-static-check.mjs` |
| S5.20 | Renderer: no third-party code, no network of its own (§9.1.1) | The module's options carry no URL, HTML, script or iframe field; it performs no `fetch` of its own — every read goes through the host page's injected `fetchSnapshot` | **Passing** | `moderator-status-module.test.ts` |
| S5.21 | Renderer: `deactivate()` unsubscribes and discards a late in-flight fetch, idempotently | A fetch resolving after `deactivate()` never renders; a second `deactivate()` does not throw | **Passing** | `moderator-status-module.test.ts` |
| S5.22 | Renderer: bounded DOM | The module creates its elements once; repeated snapshots/renders leave the node count unchanged | **Passing** | `moderator-status-module.test.ts` |
| S5.23 | **Canvas integration: eight modules, still exactly one connection and one rAF chain** | With all eight built modules entitled together the shared `MasterCanvasConnection` opens exactly one transport with eight subscribers, and the manual scheduler holds exactly one pending frame handle | **Passing** | `master-canvas-integration.test.ts` |
| S5.24 | Canvas integration: un-entitled costs nothing | `moderator_status_card` never marked entitled is never subscribed, never fetched, never rendered (PRF-02.10) | **Passing** | `master-canvas-integration.test.ts` |
| S5.25 | Contract: the response schema admits the count and nothing else | The fixture validates; adding `supporterName`, `message`, `amountPaise`, `deliveryId` or `viewerIdentityId` to it is rejected by the compiled schema — the same negative-case pattern the goal/challenge/vote fixtures already carry | **Passing** | `contracts/validate-fixtures.mjs` |
| S5.26 | Contract: no safe-mode field exists anywhere in the contract | Neither the JSON-Schema nor the OpenAPI component declares a `safeMode`/`isPaused`/`paused` property, and `additionalProperties: false` means one cannot be sent | **Passing** | `contracts/validate-fixtures.mjs`, `contracts/validate-openapi.mjs` |
| S5.27 | RT-12: the new read is in the manifest and its plan artefact is current | `pnpm explain:check` passes with the new entry; rules 1, 2 and 3 of the scan all independently cover the call site | **Passing** | `packages/db/explain-plans/required-queries.json`, `moderator-status.explain.md` |

## Commands run — real output, 2026-09-16, from `bharatstudio-alerts`

See the implementation review
(`../reviews/2026-09-16-prf-02-slice-5-moderator-status-implementation.md`) for the
negative test's own two outputs, which are recorded there rather than
here because they are evidence about a deliberately broken intermediate
state, not about the shipped one.

| Command | Exact result line |
|---|---|
| `pnpm db:test:all` | `SQL SUITE: pass=63 fail=0` — includes `PASS prf02_slice5_moderator_status` |
| `pnpm --filter @bharatstudio/alerts-api test` | `pass 617` · `fail 0` (617 tests) |
| `pnpm --filter @bharatstudio/alerts-web test` | `pass 472` · `fail 0` (472 tests) |
| `pnpm --filter @bharatstudio/alerts-api build` | `tsc -p tsconfig.json` — exit 0, no diagnostics |
| `pnpm contracts:validate` | `Validated 42 fixtures …` · `Validated OpenAPI 3.1 document with 74 paths, 82 operation contracts, and all local $ref targets.` · `Validated 3 negative OpenAPI operation-contract cases.` |
| `pnpm explain:check` | `OK: every app_private call found by rule 1 … rule 2 … and rule 3 (composition-root derived-read scan, 11 wired declaration(s) resolved and scanned) is present in required-queries.json (18 manifest entries, 9 exemptions)` · `OK: 18/18 plans current` |
| `node .github/scripts/canvas-static-check.mjs` | `PRF-03/PRF-04 canvas static check: all checks passed against current code.` — `moderator-status-module.ts: 3 static call site(s)`, `moderator-status-logic.ts: 0`; PRF-04 ceiling still unset, reported for visibility only |

**These totals are not this slice's additions alone, and saying so
matters.** A second agent was building §6 module #9 (Stream Mission Card,
migration `0135`) in the same checkout concurrently. This slice
contributed: one SQL test file, ten API route cases, nine renderer-logic
cases, fourteen renderer cases and three canvas-integration cases; one
OpenAPI path and one operation; one fixture; one manifest entry and one
plan artefact. Any remainder above those is the other agent's work, not
this one's.

## What this evidence is not

Every command above runs locally — the Node test runner, JSDOM, and a
local Dockerised PostgreSQL. **None of it is production, provider, store,
legal, device, network or release readiness evidence, and nothing here may
be represented as any of those.** In particular:

- No §19.4 budget is measured or met by anything in this record. The
  EXPLAIN artefact is a plan-shape change detector on an unsized local
  database and says so in its own body. RT-07 remains Blocked and is the
  only row that can supply OBS, Chromium, device, network or 8-hour-soak
  evidence.
- "One source replaces twelve" stays unmarketable (§19.5, §20.4, RT-09).
  Eight of twenty modules is not a canvas.
- The privacy property proven here is about **this read path**. It is not
  a claim about the product's overall privacy posture, nor about any
  other surface's projections.
- Safe mode — the other half of §6 #12 — is **not built**, not stubbed,
  and not decided. Nothing in this record should be read as covering it.
