# TC-PRF-02 slice 2 — Tug-of-War Vote, Boss Fight, RT-12 closure

**Task:** `../active/tasks/PRF-02.md` ("Slice 2" section)
**Owner:** Sukhdev Singh
**Status:** `Conditionally complete — local verification passed; independent review unavailable`

This record covers only slice 2: modules #3 (Tug-of-War Vote) and #4
(Boss Fight) on the slice-1 runtime, plus RT-12's blind-spot closure. It
is not, and does not claim to be, evidence that PRF-02's full register row
is done — sixteen catalogue modules remain unbuilt, and §19.0 RT-07
(blocked) is still the only row that can supply OBS/device/frame-timing/
8-hour-memory evidence — nothing below is that.

| Case | Control | Expected evidence | Status | Where |
|---|---|---|---|---|
| S2.1 | Vote derives from the durable record, never a held counter | The bar fraction and both sides' exact rupee amounts are pure functions of the fetched tally, recomputed every render; no field in the module persists a running total across fetches | **Passing** | `tug-of-war-vote-module.test.ts` ("the bar fraction is derived from the fetched tally amounts, never a held counter"); `tug-of-war-vote-logic.test.ts` (`totalPaidAmountPaise`/`optionPaidFraction` are pure functions, tested directly) |
| S2.2 | A vote's displayed totals match what was actually paid | Money-derived tally correctness including a live refund reducing the total on the very next read, no event to miss | **Passing** | `packages/db/tests/prf02_slice2_tug_of_war_vote.sql` ("THE MONEY-DERIVED TALLY TEST", "THE REFUND TEST") |
| S2.3 | Both a supporter and a creator can see the result follows from the record | The creator dashboard tally (`paid_support_vote_tally`), the standalone OBS widget (`list_overlay_paid_vote_tally`) and this Canvas module (`list_overlay_tug_of_war_vote`) all read the same underlying join — three surfaces, one derivation | **Passing** | `packages/db/migrations/0132_v1_prf02_slice2_tug_of_war_vote.sql`'s header (states the shared-derivation design); `tug-of-war-vote-module.test.ts` ("each side shows its exact rupee amount... the transparency requirement") |
| S2.4 | §6 "two-sided" is structural, not assumed | A tally with one or three options is rejected by the client-side guard; the SQL function itself only ever resolves a definition with exactly two `interaction_vote_options` rows | **Passing** | `tug-of-war-vote-logic.test.ts` (two rejection cases); SQL test's eligibility section (a three-option paid poll is seeded and proven never selected) |
| S2.5 | A resolved vote stays visible with the winner named, never vanishes | After `close_interaction_definition`, the tally still returns rows with `resolved: true` and the correct `resolved_option_key`, derived from the same tally row | **Passing** | SQL test ("RESOLUTION TIEBREAK" section); `tug-of-war-vote-module.test.ts` ("a resolved vote shows the winner...") |
| S2.6 | Boss Fight is a skin, not a new mechanic | The module imports and calls the SAME `progressPercent`/`formatRupees`/`isOverlayGoal` functions the goal ladder calls, reads the SAME `/v1/overlay-goals` fetch function, and performs no computation beyond `1 - progressPercent(goal)/100` | **Passing** | `boss-fight-module.test.ts` ("boss health is 1 - the SAME shared progressPercent(goal), never a second progress computation" — asserts against the literal imported function's own output); `[overlayId]/page.tsx` (both modules constructed with the identical `fetchGoalSnapshot` reference) |
| S2.7 | No new table, no new event type for Boss Fight | `packages/db/migrations/` has no new migration touching goals; `boss-fight-module.ts` defines no new type beyond `OverlayGoal`, imported not redeclared | **Passing** | Structural — `git diff` scoped to this slice shows one new migration (0132, vote-only) and zero goal-table changes |
| S2.8 | Four modules registered: still exactly one transport and one rAF loop | Ticker, goal ladder, vote, and boss fight all entitled — exactly one connection open attempt, one pending frame handle | **Passing** | `master-canvas-integration.test.ts` ("with all four built modules entitled: still exactly one connection and one rAF chain") |
| S2.9 | A throwing vote module does not blank the canvas | The three other real modules (ticker, goal ladder, boss fight) keep rendering across both frames a `tug_of_war_vote`-keyed module throws on; it goes `down` after exactly two failures with the runtime's `onModuleDown` firing once | **Passing** | `master-canvas-integration.test.ts` ("a throwing tug_of_war_vote module does not blank the canvas...") |
| S2.10 | `deactivate()` mid-update is safe and idempotent for both new modules | Calling `deactivate()` twice is a no-op the second time; a fetch that resolves after deactivation is discarded, never rendered | **Passing** | `tug-of-war-vote-module.test.ts` and `boss-fight-module.test.ts` (each: "deactivate unsubscribes and discards a late in-flight fetch, and is idempotent") |
| S2.11 | Both new modules honour `prefers-reduced-motion`, composite-only animation | `transition: none` when reduced motion is preferred; only `transform`/`opacity` ever written, `style.width`/`style.height` never set | **Passing** | Both modules' own test files ("prefers-reduced-motion disables..."; width/height assertions in the boss-fight transform test) |
| RT12.S2.1 | A widget-backing function absent from the manifest fails the check | Removing an entry from `required-queries.json`, then running `pnpm explain:check`, fails with the offending function named; restoring the entry passes again | **Passing** — exercised directly: `app_private.list_overlay_tug_of_war_vote`'s manifest entry was removed, `pnpm explain:check` exited 1 with `RT-12 required-queries scan: 1 overlay-facing app_private call(s) missing... app_private.list_overlay_tug_of_war_vote called at apps/api/src/db/vote-payment-sql-store.ts:132 has no manifest entry`, the entry was restored, and `pnpm explain:check` exited 0 (`15/15 plans current`) again. Not (yet) wrapped as a standalone automated Node test file — see "Referred", below |
| RT12.S2.2 | `explain:check` passes with the new artefacts present | `pnpm explain:check` reports every manifest entry current | **Passing** | `pnpm explain:check` → `OK: every app_private.list_overlay_* call ... is present in required-queries.json (15 manifest entries)` then `OK: 15/15 plans current` |

**Commands run (this worktree, 2026-09-16, from `bharatstudio-alerts`):**
`pnpm --filter @bharatstudio/alerts-api build` · `pnpm --filter @bharatstudio/alerts-api test` ·
`pnpm --filter @bharatstudio/alerts-web build` · `pnpm --filter @bharatstudio/alerts-web test` ·
`pnpm contracts:validate` · `pnpm explain:check` · `pnpm db:test:all` · `pnpm db:test:l03` ·
`pnpm measurement:test` · `(cd services/alert-worker-go && go build ./... && go test -race ./... && go vet ./...)` ·
`(cd services/payment-webhook-go && go build ./... && go test -race ./... && go vet ./...)` ·
`git diff --check` — real counts recorded in `active/tasks/PRF-02.md`'s "Slice 2" section, not
repeated here.
`python3 tools/doc_consistency.py` · `python3 tools/traceability.py` — from `bharatstudio-requirements`.

## What this evidence is not

Every command above ran locally. None of it is OBS, Chromium, device,
network, or production evidence — §19.0's RT-07 (blocked) remains the
only row that can supply that. The JSDOM web suite proves the *logic*:
derivation from a fetched snapshot, structural two-sidedness, composite-
only styling, and the runtime's own generic error-boundary/idempotent-
deactivate behaviour reproduced with real production modules instead of
only fakes. It proves nothing about frame timing, GPU compositing, or
behaviour inside OBS.

## Update 2026-09-16 — route-level test coverage found missing in audit, closed

The coordinator's audit found a real gap this record's original evidence table did not have:
`/v1/overlay-widgets/:overlayId/tug-of-war-vote` had no route-level test, even though
`apps/api/test/l16b-interactions-paid-vote-and-widgets-routes.test.ts` is this codebase's own
established pattern for overlay-widget route coverage (it already covers the sibling
`/v1/overlay-widgets/:overlayId/paid-votes/:definitionId` route in exactly this shape). The
SQL test (S2.2) and the web module tests (S2.1, S2.3) prove the layers either side of the
route — the query's correctness and the client's rendering — but neither can reach the
route's own auth and error behaviour: bearer-token rejection, a malformed header, an unwired
store, a store that throws, or whether the route forwards a token to the store unmodified
rather than substituting or conflating it. **This gap existed in the evidence this record
originally presented as complete; it is recorded here as a finding closed, not edited out of
the earlier rows to look as though it was never missing.**

Seven new tests added to `apps/api/test/l16b-interactions-paid-vote-and-widgets-routes.test.ts`,
mirroring the file's own existing paid-votes block:

| Case | Control | Expected evidence | Status |
|---|---|---|---|
| S2.12 | Missing bearer token rejected | 401, `overlay_unauthorized`, a `traceId` present | **Passing** |
| S2.13 | Malformed authorization header rejected, never a 500 | `Basic ...`, `Bearer` alone, and `Bearer   ` (whitespace only) all → 401 `overlay_unauthorized` | **Passing** |
| S2.14 | A valid token's tally is returned, and the exact token is forwarded to the store unmodified | 200, `tally` deep-equals the store's response, `seenToken` matches the request's bearer value exactly | **Passing** |
| S2.15 | A token the store does not recognize (wrong session/channel) never surfaces another session's data | A store that only recognizes one token returns `null` for every other — the route returns `tally: null`, 200, for the foreign token and the real tally only for the recognized one | **Passing** |
| S2.16 | Unwired or failing store fails closed, never 401 or 500; sensitive fields stripped | No store → 503 `interaction_store_unavailable`, `retryable: true`; a store returning a polluted object with extra fields (`accountId`, `providerSecret`, `paymentId`, etc.) → those fields never reach the response; a throwing store → 503, error message text never leaked | **Passing** |
| S2.17 | The transparency property, asserted at the route boundary | A deliberately distinct (not shared-fixture) tally — asymmetric amounts, one side zero, resolved with a named winner — passes through the route with every amount, `resolved`, and `resolvedOptionKey` field intact and unmodified | **Passing** |
| S2.18 | No active vote for the channel is a normal empty state, not an error | Store returns `null` → route returns `{ tally: null }`, 200 | **Passing** |

**Re-run counts (this worktree, 2026-09-16, from `bharatstudio-alerts`):**

| Command | Result |
|---|---|
| `pnpm --filter @bharatstudio/alerts-api build` | passed |
| `pnpm --filter @bharatstudio/alerts-api test` | **585 passed, 0 failed** (this record's earlier count: 578/0 — unchanged from slice-1 baseline; net +7, exactly the seven cases above) |
| `pnpm contracts:validate` | passed — 40 fixtures, 68 OpenAPI paths, 75 operation contracts, 3 negative cases, unchanged (no change to any HTTP contract shape, only new test coverage) |
| `git diff --check` | clean |

## RT-12: closed or narrowed

**Narrowed, not fully closed.** The manifest-and-scan mechanism makes
forgetting a *declared* function's artefact impossible (the scan fails
the build), and closes the specific gap PRF-02 slice 1 found (two
functions with no artefact, invisible to a directory-listing-driven
check) plus two more pre-existing gaps the honest scan surfaced while
being built. What it does **not** catch, stated plainly per this task's
own instruction:

- **A widget-backing function that does not follow the `list_overlay_*`
  naming convention.** The scan is a regex over that convention, not a
  real call-graph analysis. `list_channel_master_canvas_modules` is
  exactly this case — it is in the manifest only because this task named
  it explicitly, not because the scan would ever nominate a
  differently-named function. A future overlay-facing read that does not
  follow the convention would ship invisible to this scan, exactly the
  way the original two PRF-02 functions shipped invisible to the
  directory-listing check.
- **A call reached only through indirection the regex cannot see** (built
  as a string at runtime, re-exported under an alias, etc.). Every call
  site in this codebase today is a literal `app_private.fn_name(` inside
  a tagged SQL template, so this is a theoretical gap, not an observed
  one — but it is a gap, not a false statement of completeness.
- **Whether a found function genuinely needs production-scale
  performance attention** is still a human judgement made once per
  artefact, at capture time — the scan is deliberately over-inclusive
  (every `list_overlay_*` call is treated as in-scope) rather than
  under-inclusive, so a false positive here costs one more artefact to
  capture, never a missed one.

Full detail in `packages/db/explain-plans/scan-required-queries.mjs`'s own
header comment, which states this same list in the code itself.

## Independent Opus verification — 2026-09-16

Checks re-run against the worktree, and the RT-12 scan negative-tested rather than trusted.

- `pnpm --filter @bharatstudio/alerts-api test` — **585 passed, 0 failed** (578 before the fix).
- `pnpm --filter @bharatstudio/alerts-web test` — **386 passed, 0 failed** (baseline 358).
- `pnpm --filter @bharatstudio/alerts-web build` — succeeded. `pnpm db:test:all` — **59/0**.
- `pnpm explain:check` — scan OK, **15/15 plans current** (10/10 before this slice).
- `pnpm contracts:validate` — clean. Both Go services: build clean, **10 packages `ok`** each
  under `-race`, vet clean. `git diff --check` clean.
- `python3 tools/doc_consistency.py` — 17 checks, 0 errors, 0 warnings.
- Cache sweep: nothing a commit would pick up — the only matches were inside ignored
  `node_modules`.

### The RT-12 scan was negative-tested, not taken on trust

A check that reports green is worth nothing until it has been seen to fail. Removing
`app_private.list_overlay_goal` from `required-queries.json` produced:

> `app_private.list_overlay_goal called at apps/api/src/db/goal-overlay-store.ts:21 has no
> manifest entry -- add it to required-queries.json and capture an EXPLAIN artefact before
> this can pass`

Entry restored; 15/15 passes again. The failure names the call site, which is what makes it
actionable rather than merely red.

### Building the scan general-purpose found gaps nobody had asked about

It was scoped to two known-missing plans. Built against the convention rather than tuned to
those two, it also found **`list_overlay_lottie_assets`** and **`list_overlay_widget_config`**
(migrations 0077 and 0105), invisible since they shipped. A check written to satisfy only the
defects already known would have reported green over both indefinitely. The manifest went
from 10 entries to 15.

### RT-12 stays P, and the implementer's own example is why

The scan keys on the codebase's `list_overlay_*` naming convention by regex, not on real
call-graph analysis, so a widget-backing function that breaks the convention still ships
invisible. The proof offered is the sharp one: **`list_channel_master_canvas_modules` is in
the manifest only because this task named it** — the scan would never have found it. Narrowed,
not closed, and recorded as such rather than claimed.

### The audit finding, and how it was recorded

`/v1/overlay-widgets/:overlayId/tug-of-war-vote` shipped with no route-level test. The
implementer flagged it rather than omitting it silently, but the justification did not hold:
`l16b-interactions-paid-vote-and-widgets-routes.test.ts` already exists, so sibling
overlay-widget routes do get this coverage, and the SQL and web-module tests sit either side
of the route without reaching its auth. Seven tests were added, including that a token the
store does not recognise returns `null` rather than another session's tally, and the
transparency property asserted at the route boundary with a non-shared fixture.

The earlier evidence was **not** edited to look as though the gap never existed — it is
recorded as found in audit and closed, and `active/tasks/PRF-02.md`'s claim that no
`apps/api` test was added was corrected in place with a note saying it was wrong.

**What this evidence is not.** The web suite is JSDOM: it proves logic — one transport, one
rAF loop, derivation from the durable record, bounded nodes — and **nothing** about frame
timing, GPU compositing, 8-hour memory or OBS. RT-07 is Blocked. **PRF-02 remains `A`**:
five of twenty modules is not a canvas, and "one source replaces twelve" stays unpublishable
and additionally does not differentiate against StreamElements (§6).
