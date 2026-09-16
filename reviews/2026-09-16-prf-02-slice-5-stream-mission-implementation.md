# Review — PRF-02 slice 5 implementation (Stream Mission Card, §6 module #9)

**Date:** 2026-09-16
**Owner:** Sukhdev Singh
**Reviewer:** Implementing agent, self-review (independent review unavailable — governance/AGENTS.md's "if independent review is unavailable, say so, self-review, and leave the task `Conditionally complete`" applies, and is applied).
**Scope authority:** [`2026-09-16-prf-02-slice-5-scope-review.md`](2026-09-16-prf-02-slice-5-scope-review.md) (the persisted standalone scope review that authorises this work) and [`../FULL-PRODUCT-DEFINITION.md`](../FULL-PRODUCT-DEFINITION.md) §6's module table row 9, carrying the owner's four decisions dated 2026-09-16. Neither is restated here, per this task's own instruction.
**Task record:** [`../active/tasks/PRF-02.md`](../active/tasks/PRF-02.md), "Slice 5" section.
**Acceptance record:** [`../tests/TC-PRF-02-slice-5-stream-mission.md`](../tests/TC-PRF-02-slice-5-stream-mission.md).
**Register state:** unchanged. PRF-02 stays `A`. No state letter is self-assigned.

## Disposition

`Conditionally complete.` The vertical slice is built and locally verified
at every layer the task named (SQL, API route, contract, EXPLAIN, renderer,
canvas integration). Independent review did not occur. Nothing here is
production, provider, store, legal, device, network or release readiness,
and no such claim is made anywhere in this slice's records.

## What was built

Module #9 as a complete vertical slice, in this order (schema first,
because the scope review's standing lesson is *read the data path before
believing the catalogue*, and #9's data path did not exist):

1. `packages/db/migrations/0135_v1_prf02_slice5_stream_mission.sql` — `public.stream_missions` plus four `app_private` functions (`start_stream_mission`, `end_stream_mission`, `list_channel_stream_mission`, `list_overlay_stream_mission`).
2. `apps/api` — one domain module, two SQL stores (creator and overlay, deliberately split), one routes file, one test file, and the two composition-root wirings.
3. `contracts` — one JSON-Schema, one fixture, four OpenAPI operations, three new negative cases in the fixture validator.
4. `packages/db/explain-plans` — one captured EXPLAIN artefact and one manifest entry.
5. `apps/web` — the eighth canvas module renderer, its test file, the host-page wiring, and the eight-modules canvas integration case.

Full file list and evidence paths are in the task record's "Slice 5"
section; they are not repeated here.

## How each owner decision is honoured, checked rather than asserted

1. **Phase override is single-module.** Nothing outside module #9 was added. The other twelve unbuilt catalogue modules have no renderer, no schema, no route and no entitlement change in this slice. `0131`'s catalogue constraint was not edited — `stream_mission_card` was already one of its twenty keys.
2. **1–120 characters, reusing `0109`'s bound.** The number appears in four places and is the same in all four, each traceable to `0109` line 67 rather than to a fresh judgement: the table check constraint, `start_stream_mission`'s re-validation, the route's JSON schema `maxLength`, and the contract schema's `maxLength`. There is exactly one creator-authored text column; no `title`, no `description`, no second field of any kind.
3. **Session-bounded, not clock-bounded — and this is enforced, not promised.** Three independent checks make it a property of the build:
   - `packages/db/tests/prf02_slice5_stream_mission.sql` queries `information_schema.columns` and fails if `public.stream_missions` ever grows a column matching `%duration%`, `%timer%`, `%expire%`, `%deadline%` or `ends_at`.
   - The same file queries `information_schema.parameters` and fails if `list_overlay_stream_mission`'s OUT columns are ever anything but `mission_id`, `objective`, `started_at` — so a widened projection is a failing test, not a silent change.
   - `contracts/validate-fixtures.mjs` asserts the schema **rejects** `endsAt`, `durationSeconds` and `expiresAt` on the overlay fixture.

   "Until the overlay session ends" needed no new mechanism: `list_overlay_stream_mission` is gated by `overlay_sessions.revoked_at is null and expires_at > current_timestamp`, the same pre-existing clause every other `list_overlay_*` function carries. No duration constant was needed anywhere, so none was chosen and none is reported as blocked.
4. **All tiers, one gate.** `list_channel_stream_mission`, `start_stream_mission` and `end_stream_mission` read no tier and call no cap function. The SQL test proves a `free`-tier channel can start, read and end a mission exactly as a `studio` one can. Only rendering passes through `0131`'s existing cap.

## The judgement calls this slice had to make, and why each went the way it did

These are decisions the authority does not state. Each is recorded so a
reviewer can disagree with the reasoning rather than only with the result.

- **Two running missions are impossible, enforced by a partial unique index** (`stream_missions_channel_running_idx on (channel_id) where ended_at is null`) rather than by the overlay read's `limit 1` alone. §12.7 says "at most the current mission, never a history" — that is an answered question, so it is enforced in the schema, not tie-broken in a query. `limit 1` is still present, matching `list_overlay_challenge`'s shape, but it never has to choose.
- **Starting a second mission is a `409`, not a silent supersede.** Auto-ending the running mission would invent a lifecycle rule no authority states and would destroy a creator's running mission on a mis-click. `start_stream_mission` raises `23505` with a readable message before the insert; the route returns `409 stream_mission_already_running`. Ending and starting remain two explicit acts.
- **`end_stream_mission` is addressed, not ambient** — it takes the mission id as well as the channel id, so a stale dashboard tab cannot end a mission started after that tab loaded. The read that precedes it already returns the id, so this costs nothing.
- **The elapsed reading counts up and is derived, never stored.** §6's row names a temporal element and the owner's decision removes the timer; a card with no sense of "since when" is a worse product than one with an elapsed reading, and an elapsed reading derived on the frame loop from a server-sent `startedAt` is not a duration, an expiry or a countdown. It never reaches an end, nothing expires on it, and the card's visibility is decided solely by whether the server still returns a row. `StreamMissionModuleOptions` has no field for an end time, checked at compile time by the module's own test, so a future edit cannot quietly reintroduce one through the options bag.
- **The elapsed reading writes to the DOM once per whole second.** `render()` is still called every frame, as the runtime requires, and no-ops until the whole-second value changes — the "cheap to call every frame, no-op quickly when nothing changed" contract `CanvasModuleDefinition.render` already states.
- **Reduced motion suppresses the entrance transition, not the reading.** Slice 4's ruling is that a reduced-motion alternative must be *perceivable*, not merely shortened. The elapsed reading is information, so it keeps updating; the card's `translateY` entrance is motion, so it becomes `none`.
- **The overlay projection omits `created_by_user_id`, `ended_at`, `created_at`, `updated_at`.** §12.7: the overlay gets what it paints. A running mission's `ended_at` is `null` by definition, so returning it would carry no information while putting an end-shaped field into a contract that must not have one.
- **The store is split in two, and the split is what makes `scan-required-queries.mjs` pass on substance.** Rule 3 is new, so the scan was read before the files were named rather than after:
  - `apps/api/src/db/stream-mission-overlay-store.ts` — the filename contains "overlay", so **rule 2** scans every `app_private` call inside it; and `apps/api/src/index.ts` constructs it with `derivedReadSql`, so **rule 3** independently resolves it through index.ts's own import statement, brace-matches the exported factory's body, and scans that. The single call inside, `app_private.list_overlay_stream_mission`, is in `required-queries.json`'s manifest with a captured artefact. **Rule 1** also finds it by the `list_overlay_*` convention. All three rules cover it; none is dodged, and **no exemption entry was added by this slice.**
  - `apps/api/src/db/stream-mission-store.ts` — the creator surface, wired to the main `sql` pool exactly as `goals`, `challenges` and `masterCanvasModules` already are. It is a creator write/read path, not a derived read, so it is outside all three rules by the same structural reasoning the existing creator stores rely on. Putting it on `derivedReadSql` to "be safe" would have been wrong twice over: it would have run creator writes on RT-10/RT-11's read-only-shaped pool, and it would have forced three pro-forma exemptions — and pro-forma exemptions are how an exemption list stops being read.

## Honest limits of this slice

- **No independent review.** Self-review only. Recorded here and in the task record's status line rather than implied away.
- **No mission history surface.** The table is durable and a mission's row survives ending, so §12.6's "storing, viewing, searching, fetching, exporting a durable creator record is never tier-gated" is satisfied structurally — but no *history* read, list or export endpoint is built by this slice, and none is claimed. A creator can read the current mission and nothing else through the API this slice adds.
- **No standalone browser-source route.** §6 names module #9 as a Canvas module only. The kill switch is therefore the entitlement toggle, not a fallback widget — a weaker kill switch than Challenge Board's or Goal Ladder's, and stated as such rather than glossed.
- **The EXPLAIN artefact is a plan-shape change detector, captured against a minimally-seeded local database.** It is not §19.4 evidence and not §37.4 production-scale evidence. The `stream_missions` lookup resolves through the partial unique index at this seed size; whether that holds at scale is not demonstrated here and is not asserted.
- **Indic script fallback (§15.4.3) remains open, and this module raises its urgency.** The objective is free creator-authored text that will routinely be Indic script in this market. The renderer takes every font family from `defaultCanvasTextStyles()` and hard-codes none, so the architecture does not foreclose the fix — but the fix itself is not in this slice, and the binding precondition (Indic fallback required before these modules become creator-configurable) now covers module #9 too.
- **Every result below is local.** Dockerised PostgreSQL 16, the Node test runner, JSDOM. No OBS, no Chromium, no device, no network, no provider, no store, no legal review, no release.

## Checks run — exact result lines, this worktree, 2026-09-16

Recorded verbatim below, after the build was complete.

| Command | Exact result line |
|---|---|
| `pnpm db:test:all` | `SQL SUITE: pass=63 fail=0` — includes the new `PASS prf02_slice5_stream_mission`. The count is 63 rather than slice 4's 61 because two other agents' concurrent files (`prf02_slice5_moderator_status`, and this slice's own) are present in the same tree; a higher number from concurrent work is not a failure |
| `pnpm --filter @bharatstudio/alerts-api test` | `ℹ tests 617` · `ℹ pass 617` · `ℹ fail 0` (slice-4 baseline 585/0; this slice adds 17 cases in `prf02-stream-mission-routes.test.ts`, the remainder is another agent's concurrent work in the same tree) |
| `pnpm --filter @bharatstudio/alerts-web test` | `ℹ tests 472` · `ℹ pass 472` · `ℹ fail 0` (slice-4 baseline 431/0; this slice adds 13 cases in `stream-mission-module.test.ts` plus 2 in `master-canvas-integration.test.ts`, the remainder is another agent's concurrent work) |
| `pnpm --filter @bharatstudio/alerts-api build` | `> tsc -p tsconfig.json` — exit 0, no diagnostics |
| `pnpm contracts:validate` | `Validated 42 fixtures plus the v1 template catalogue contract with Draft 2020-12, format enforcement and v1 capability exclusion (including invalid-UUID rejection).` · `Validated OpenAPI 3.1 document with 74 paths, 82 operation contracts, and all local $ref targets.` · `Validated 3 negative OpenAPI operation-contract cases.` (slice-4 baseline 40 fixtures / 68 paths / 75 operations; this slice adds 1 fixture and 4 operations across 3 paths, the remainder is concurrent work) |
| `pnpm explain:check` | `OK: every app_private call found by rule 1 (convention scan), rule 2 (overlay-store-file scan) and rule 3 (composition-root derived-read scan, 11 wired declaration(s) resolved and scanned) is present in required-queries.json (18 manifest entries, 9 exemptions)` · `OK: 18/18 plans current` (slice-4 baseline 16/16; this slice adds `app_private.list_overlay_stream_mission` → `stream-mission.explain.md`, and adds **no** exemption) |

**Not run, and therefore not claimed:** `pnpm db:test:l03`, `pnpm measurement:test`, the Go
suites, `pnpm --filter @bharatstudio/alerts-web build`, the load/fault self-tests and the Docker
image builds. This slice's command named six commands; those six were run and are reported above.
Nothing is asserted about the ones that were not.

**One real defect this verification found, in this slice's own test harness rather than in the
build.** The first run of `prf02-stream-mission-routes.test.ts` failed its "no clock-bound field on
the wire" case with `actual: 201, expected: 400`. Cause: the test built its app with a bare
`Fastify()`, and Fastify's DEFAULT ajv options silently **strip** a property that
`additionalProperties: false` forbids instead of rejecting the request — so the harness was testing
a different server than the one this codebase ships. `apps/api/src/app.ts:205` sets
`ajv: { customOptions: { removeAdditional: false } }`, which is what turns that strip into a 400.
The harness now mirrors that option, with the reason written at the call site. The production
behaviour was correct throughout; what was wrong was a test that would have passed for the wrong
reason. Recorded rather than quietly fixed, because the pre-existing
`prf02-master-canvas-routes.test.ts` uses a bare `Fastify()` too — its own cases do not depend on
the difference, but the pattern is one a future test could inherit unknowingly.

## Negative test

**Guard broken:** the new 1–120 objective bound at the route's JSON-Schema layer —
`apps/api/src/routes/stream-mission.ts`'s `startBody.properties.objective.maxLength`, changed from
`STREAM_MISSION_OBJECTIVE_MAX_LENGTH` (120, migration `0109` line 67's bound, reused per the owner's
decision) to a hand-typed `500`. This is the guard that makes acceptance case S5.19 real: without
it, an over-long objective reaches the store and is caught only by the database.

**With the guard removed** (`pnpm --filter @bharatstudio/alerts-api test`):

```
✖ POST accepts a 120-character objective and rejects a 121-character one at the schema layer, before the store is ever called (6.904667ms)
ℹ tests 617
ℹ pass 616
ℹ fail 1
✖ failing tests:
✖ POST accepts a 120-character objective and rejects a 121-character one at the schema layer, before the store is ever called (6.904667ms)
  AssertionError [ERR_ASSERTION]: Expected values to be strictly equal:
    actual: 201,
    expected: 400,
```

**With the guard restored** (same command, no other change):

```
ℹ tests 617
ℹ pass 617
ℹ fail 0
```

The guard is restored in the working tree; `grep -n "maxLength"
apps/api/src/routes/stream-mission.ts` reads
`36:      maxLength: STREAM_MISSION_OBJECTIVE_MAX_LENGTH,`. A guard that has never been observed
failing is not a verified guard — this one has now been observed failing and passing, on the same
command, with only the guard changed between the two runs.

## Referred to Opus

- **The register letter.** PRF-02 stays `A`; eight of twenty is still not a canvas. Opus decides the letter after audit — not self-assigned here.
- **Mission history.** Whether a creator-facing list of past missions (and an export surface for them) belongs in a later slice, and what §12.7 bound it should carry, is a product decision, not an implementation one. The data is already durable; only the surface is absent.
- **Whether `stream_mission_card`'s kill switch being entitlement-only is acceptable**, given every other Canvas module except Milestone Celebration has a standalone widget fallback. Building a standalone `/overlay/widgets/stream-mission/...` route was outside this slice's scope and is not obviously wanted; naming the asymmetry is this record's job, deciding it is not.
