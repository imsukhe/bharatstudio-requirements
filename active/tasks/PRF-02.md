# PRF-02 — Master Canvas as the runtime

**Authority:** [`../../FULL-PRODUCT-DEFINITION.md`](../../FULL-PRODUCT-DEFINITION.md) §6, §19.4, §19.5, §9.1.1, §12.7, §15.4.3, §30.3, §31.18.1 PRF-02, §34, §37.2, §37.11
**Status:** `Conditionally complete — slice 1 (runtime + Supporter Ticker + Community Goal Ladder), slice 2 (Tug-of-War Vote + Boss Fight + RT-12 blind-spot closure), slice 3 (Support Theater ported onto the runtime, sharing the Canvas's own single overlay session, "next up") and slice 4 (Challenge Board — current-only — plus Milestone Celebration) all implemented and locally verified; independent review unavailable; PRF-02's full register row remains open`. See "Slice 2", "Slice 3" and "Slice 4" below for each later slice's own scope, evidence and referrals — neither repeats or restates an earlier slice's material, which stands as originally recorded. **Slice 3 carries its own dated Correction** (a first build gave Support Theater a second overlay session; corrected, per the coordinator's own instruction, to share the Canvas's one session/connection instead) — read Slice 3's "Correction, 2026-09-16" note before its Decisions. **PRF-02 remains register letter `A`** after this slice — seven of twenty catalogue modules is still not a canvas; no state letter is self-assigned (§0's own rule), Opus decides it after audit.

**This slice is the runtime plus exactly two modules (Supporter Ticker,
Community Goal Ladder) — never the full twenty-module catalogue, and never
the canvas designer UI.** PRF-02's register row is **not** closed by this
slice, by this task's own explicit command (§0). §34 places PRF-02 in
Phase 0.5, "the thing every later phase assumes"; the first six modules are
Phase 1 work, not this slice's. Landing the runtime plus two modules is
necessary but not sufficient to change PRF-02's register letter — Opus
decides the letter after auditing, per this task's hard rule that no state
letter may be self-assigned.

| Field | Value |
|---|---|
| **Scope phase** | `v1`; Phase 0.5 runtime remediation (§34), opening into Phase 1. The Master Canvas runtime (single transport, single rAF scheduler, per-module error boundaries, bounded-DOM recycling) plus the server-owned §30.3 module cap, plus renderers for exactly two modules (`supporter_ticker`, `community_goal_ladder`) |
| **Owner** | **Sukhdev Singh** |
| **Tier and gate** | All tiers. The module cap itself is tier-differentiated (Free 2 / Pro 5 / Creator 12 / Studio all, §30.3) but the runtime and both built renderers are available at every tier — a Free channel's two active module slots are exactly filled by the two modules this slice ships. No release claim; "one source replaces twelve" remains unpublishable per RT-09/§19.5 until RT-07 (blocked) closes |
| **Personal-data class** | None new beyond what the existing overlay/widget read paths already carry. The new `master_canvas_modules` table stores only `channel_id`, a fixed-catalogue `module_key`, `enabled`, and timestamps — no viewer, payment or personal-data field. The overlay-facing read (`list_overlay_master_canvas_modules`) returns module keys only, gated by the existing `overlay_sessions` token-fingerprint model — no new identifier ever enters a log or metric label |
| **Provider or legal dependency** | None. Client-side runtime (browser APIs only: `requestAnimationFrame`, SSE `fetch`, `prefers-reduced-motion`) and existing PostgreSQL/Fastify patterns only |
| **Failure behaviour** | See "Failure behaviour, kill switch, rollback" below |
| **Kill switch** | See "Failure behaviour, kill switch, rollback" below |
| **Acceptance test** | `tests/TC-PRF-02-master-canvas-runtime.md` |
| **Evidence location** | `tests/TC-PRF-02-master-canvas-runtime.md`, `packages/db/tests/prf02_master_canvas_module_cap.sql`, `apps/api/test/prf02-master-canvas-routes.test.ts`, `apps/web/app/overlay/canvas/master-canvas-connection.test.ts`, `apps/web/app/overlay/canvas/master-canvas-runtime.test.ts`, `apps/web/app/overlay/canvas/master-canvas-integration.test.ts`, `apps/web/app/overlay/canvas/modules/supporter-ticker-module.test.ts`, `apps/web/app/overlay/canvas/modules/goal-ladder-module.test.ts`, and this task's review record |
| **Rollback** | See "Failure behaviour, kill switch, rollback" below |

## Failure behaviour, kill switch, rollback

**Failure behaviour** (headline: one module failing must never blank the
canvas):

- **A module throws during mount or render.** The runtime's per-module error
  boundary catches it; every other module keeps rendering on the same
  connection and the same frame loop. A module that fails **twice** stays
  down for the session with a creator-visible note (PRF-14) — it is never
  silently retried forever and never taken as a signal to tear down the
  canvas.
- **The single transport drops.** The existing overlay SSE
  reconnect/backoff behaviour (`overlay-transport.ts`'s pattern, reused by
  the runtime's one shared connection) applies canvas-wide: every mounted
  module keeps showing its last-known-good snapshot while the connection
  retries, and a reconnect forces one full snapshot re-read per module —
  never a blank frame, never a duplicate visual delivery.
- **A snapshot is stale** (connection has not delivered a fresher one yet).
  The module keeps rendering the last value it has; nothing is ever shown
  as current when it is known-stale, and nothing is invented when no value
  has arrived yet (renders nothing until the first real snapshot lands).
- **The canvas is over its module cap.** The over-cap module(s) simply are
  never returned by `list_overlay_master_canvas_modules` — the runtime
  never learns they exist, never opens a connection or does any work for
  them (PRF-05, PRF-02.10). Creator-side, `list_channel_master_canvas_modules`
  shows the module, `active: false`, `inactiveReason: 'tier_module_cap'`, so
  the creator can see which modules are active and why one is not (this
  task's §3).

**Kill switch:** the pre-existing individual widget browser sources
(`/overlay/widgets/supporter-ticker/[overlayId]`,
`/overlay/widgets/goal/[overlayId]`, and every other existing widget route)
are **untouched by this task** and remain fully functional. A creator who
wants to stop using the Master Canvas source simply removes it from OBS and
re-adds the individual widget sources they used before — no data migration,
no account state to unwind, because the Canvas reads the same underlying
data (`/v1/overlay-widgets/:overlayId/supporter-ticker`,
`/v1/overlay-goals/:overlayId`) the standalone widgets already read. This is
also §21.3's own "not deprecated" standalone-widget posture — Canvas is the
recommended default, standalone remains a live escape hatch, mid-stream
recovery included.

**Rollback:**

- Web (`apps/web`): delete `apps/web/app/overlay/canvas/` in full (the
  connection, the runtime, `text-rendering.ts`, `modules/`, the
  `[overlayId]/page.tsx` host page, and every `.test.ts` file alongside
  them). No existing widget route is modified by this task — deleting this
  directory returns the web app to exactly its pre-task route set.
- API (`apps/api`): revert `apps/api/src/app.ts` (the `masterCanvasModules`/
  `overlayMasterCanvasModules` dependency fields and the
  `registerMasterCanvasRoutes` call), `apps/api/src/index.ts` (the two store
  constructions), and delete `apps/api/src/domain/master-canvas-store.ts`,
  `apps/api/src/db/master-canvas-sql-store.ts`,
  `apps/api/src/routes/master-canvas.ts`, and
  `apps/api/test/prf02-master-canvas-routes.test.ts`.
- Migration `packages/db/migrations/0131_v1_prf02_master_canvas_modules.sql`
  is rolled back by a **new forward migration** that drops
  `app_private.list_overlay_master_canvas_modules`,
  `app_private.list_channel_master_canvas_modules`,
  `app_private.upsert_master_canvas_module`,
  `app_private.tier_master_canvas_module_cap`, and
  `public.master_canvas_modules` — never by editing or deleting 0131.
  Rolling this migration back **does** delete configured module rows
  (there is no other way to undo a `create table`); this is the one
  circumstance under which "never destroys configuration" (§12.6) is not
  held, and it is an explicit, operator-initiated rollback of the entire
  capability, not a downgrade — the two are different events and only the
  downgrade path is required to preserve rows.
- Delete `packages/db/tests/prf02_master_canvas_module_cap.sql`.

## Boundaries

**In scope, this slice:** the Master Canvas runtime (one shared transport,
one `requestAnimationFrame` scheduler, per-module error boundaries with the
two-failures-stays-down rule, bounded/recycled DOM for the ticker, composite
-only animation, `prefers-reduced-motion` honoured) plus renderers for
exactly **two** modules (`supporter_ticker`, `community_goal_ladder`); the
server-owned §30.3 module cap (Free 2 / Pro 5 / Creator 12 / Studio all),
covering the full 20-module catalogue for cap-counting purposes even though
only two have a renderer yet; the durable, never-deleted-on-downgrade module
configuration record.

**Explicitly out of scope, not touched:** the other eighteen catalogue
modules' renderers; the canvas designer UI in the dashboard (§7); scene
profiles, theme packs, safe-zone editing, aspect-ratio variants, conditional
themes; §15.4.3 customisation levels beyond what these two modules need;
OBS migration/import; RT-07 evidence (blocked, unrelated to this task);
RT-13's per-channel transport cap (Canvas counts as one connection toward
it — nothing here changes that accounting, nothing here implements the cap
itself); anything YouTube; marketing copy; pricing. The SSE route, the
overlay session/auth model, `get_overlay_events`, the dispatch lease, the
TTS path, and `DEFAULT_TTS_PLAYBACK_TIMEOUT_MS` are **not modified** by this
task — the runtime's shared transport is a new client built on the existing,
unmodified `/v1/overlays/:overlayId/events` route and the existing
per-widget snapshot endpoints.

**Owner ruling, 2026-09-16 — Indic script fallback order (§15.4.3) is OUT
of this slice, explicitly, not a deferral left open for later judgment.**
§15.4.3 places per-text-role Indic fallback at customisation level 1; this
slice is the runtime, not the customisation model, so building the
customisation knob itself is out of scope here, the same as every other
§15.4.3 level-1+ capability this task does not touch. Two constraints bind
the two modules this slice ships, stated by the owner and binding on the
implementation: **(1)** neither module's text rendering may hard-code a
single font family in a way that architecturally forecloses a later
per-text-role fallback stack — the render path must accept a font/fallback
value as data, even though this slice supplies only one first-party
default, not a creator-facing choice; **(2)** Indic fallback is **required**
before either module becomes creator-configurable (i.e. before a later
slice exposes §15.4.3 level-1 typography controls for these two modules) —
supporter names and goal titles in this product's market are routinely
Indic script, and a ticker that renders them as tofu is a broken product,
not a missing feature. This is carried forward as a binding precondition on
the *next* slice that touches these modules' typography, not something this
slice implements.

## Owner ruling, 2026-09-16 — resume authorized, with three bindings

The owner reviewed this record, the review record's §1 product/market
research, and the referred items, and ruled:

1. **The StreamElements framing finding is correct and is now recorded
   directly in `FULL-PRODUCT-DEFINITION.md` §6** (the paragraph beginning
   "Competitive accuracy, checked 2026-09-16"), sourced and dated by the
   owner. §6's "pile" framing already scoped to Streamlabs; the correction
   makes that scoping explicit and states the real differentiator (single
   connection **and** single render loop **and** per-module error isolation
   together) as its own, separately-gated (RT-07) sentence. **Nothing in
   this task's architecture changed as a result.** No marketing copy was
   touched by this task, per its own scope boundary.
2. **Indic script fallback order (§15.4.3) is OUT of this slice — owner
   ruling, not a deferral.** See "Owner ruling ... Indic script fallback
   order" under Boundaries, above. Binding on this slice: no module
   hard-codes a single font family (satisfied — see
   `apps/web/app/overlay/canvas/text-rendering.ts`); Indic fallback is
   required before either module becomes creator-configurable (carried
   forward as a precondition on the next slice that adds §15.4.3 typography
   controls to these two modules, not implemented here).
3. **Resume on the original design — the review changed nothing about its
   correctness.** Additionally directed: the runtime's idle-module
   deactivation (PRF-02.6) must be driven by a `visibilitychange` **signal**,
   never by checking `document.hidden` inside the frame-loop callback,
   because (per the MDN/Chrome evidence in the review record) the frame
   loop itself is exactly what stops running while hidden — see
   `master-canvas-runtime.ts`'s header comment and its own
   `PRF-02.6: a page-hidden signal deactivates...` test for the built
   version of this.

## Current implementation status — complete for this slice

**Server-side entitlement half:**
`packages/db/migrations/0131_v1_prf02_master_canvas_modules.sql` (the
module-cap table and four `app_private` functions, covering all 20 §6
catalogue keys),
`packages/db/tests/prf02_master_canvas_module_cap.sql`,
`apps/api/src/domain/master-canvas-store.ts`,
`apps/api/src/db/master-canvas-sql-store.ts`,
`apps/api/src/routes/master-canvas.ts`,
`apps/api/test/prf02-master-canvas-routes.test.ts`, wiring in
`apps/api/src/app.ts`/`apps/api/src/index.ts`, and one curated-suite
addition: `packages/db/tests/run-l03-application-behavior.sh` now also runs
`prf02_master_canvas_module_cap.sql`.

**Client-side runtime:**
`apps/web/app/overlay/canvas/master-canvas-connection.ts` (the one shared
transport — PRF-02.1, PRF-02.10, PRF-02.12),
`apps/web/app/overlay/canvas/master-canvas-runtime.ts` (the one
`requestAnimationFrame` scheduler, per-module error boundary,
visibility-driven idle deactivation — PRF-02.2, .3, .4, .6, .11),
`apps/web/app/overlay/canvas/text-rendering.ts` (the Indic-ready default
font stack, data-driven per this record's owner ruling above),
`apps/web/app/overlay/canvas/modules/supporter-ticker-module.ts` (bounded/
recycled DOM — PRF-02.5),
`apps/web/app/overlay/canvas/modules/goal-ladder-module.ts`
(`transform: scaleX()` progress, never `width` — PRF-02.7, corrects the
pattern the existing standalone goal widget uses),
`apps/web/app/overlay/canvas/[overlayId]/page.tsx` (the host page — the
new OBS browser-source URl `/overlay/canvas/{overlayId}#token=...`), and
their five `.test.ts` files (listed in Evidence location above).

**All checks run — real counts, this worktree, 2026-09-16:**

| Command | Result |
|---|---|
| `pnpm --filter @bharatstudio/alerts-api build` | passed |
| `pnpm --filter @bharatstudio/alerts-api test` | **578 passed, 0 failed** (baseline 566/0; net +12) |
| `pnpm --filter @bharatstudio/alerts-web build` | passed (new route `ƒ /overlay/canvas/[overlayId]` registered) |
| `pnpm --filter @bharatstudio/alerts-web test` | **358 passed, 0 failed** (baseline 332/0; net +26) |
| `pnpm contracts:validate` | passed — 40 fixtures, 68 OpenAPI paths, 75 operation contracts, 3 negative cases (unchanged from baseline; no new route was added to the public contract, matching the existing precedent that creator-facing CRUD routes like `goals.ts`'s are not documented there either) |
| `pnpm explain:check` | **OK: 10/10 plans current** (unchanged — no widget-backing query this task added has an EXPLAIN artifact yet; see Referred, below) |
| `pnpm db:test:all` | **58 files passed, 0 failed** (baseline 57/0; net +1) |
| `pnpm db:test:l03` | **24 file(s) passed** (baseline 23; net +1, the curated-suite addition above), full integration legs (Go `ingress`/`reconcile`/`store`, `overlay-wakeup.integration.ts`, `overlay-cross-replica.integration.ts`, apps/api concurrency suite) all passed |
| `pnpm measurement:test` | passed — 5 Node tests + 4 Python tests (unchanged) |
| `(cd services/alert-worker-go && go build ./... && go test -race ./... && go vet ./...)` | passed, 10 packages, all `ok` |
| `(cd services/payment-webhook-go && go build ./... && go test -race ./... && go vet ./...)` | passed, 10 packages (one `[no test files]`, pre-existing), all `ok` |
| `git diff --check` | clean |
| `python3 tools/doc_consistency.py` (this repository) | **17 checks · 0 errors · 0 warnings** (unchanged) |
| `python3 tools/traceability.py` (this repository) | regenerated `TRACEABILITY.md` (783 rows), clean |

**What this evidence is not** — repeated here because it is the rule most
likely to be skimmed past: every number above is local (JSDOM/Node test
runner, a local Dockerized Postgres, `go test`). None of it is OBS,
Chromium, device, network, or production evidence. §19.0's RT-07 (blocked)
remains the only row that gates any frame-timing, GPU-compositing,
memory-over-8-hours, or "one source replaces twelve" claim.

## Referred to Opus

- **RT-12's `EXPLAIN ANALYZE` registry (`packages/db/explain-plans/`) was
  not extended to this task's two new widget-backing reads**
  (`app_private.list_channel_master_canvas_modules`,
  `app_private.list_overlay_master_canvas_modules`). RT-12 is explicitly
  out of this task's scope (not named in §1's task list), and
  `explain:check` still reports the unchanged baseline (10/10, the
  existing widgets only). Whether these two queries should get plan
  artifacts now or when the remaining 18 modules land is a scope call for
  the lane that owns RT-12/PRF-11, not decided here.

  **Resolved in slice 2, below.** RT-12 was downgraded U → P on
  2026-09-16 (`tests/TC-RT-12-explain-plans.md`) precisely because this
  gap sat unclosed; slice 2's §1(a) closes it — a declared manifest
  (`packages/db/explain-plans/required-queries.json`) plus a build-time
  scan (`scan-required-queries.mjs`) that fails when an overlay-facing
  query is missing from the manifest, and both of this bullet's named
  functions now have captured artifacts. See "Slice 2" below and the
  updated `tests/TC-RT-12-explain-plans.md` for what is closed versus
  narrowed.
- **Standalone-widget parity (§21.3):** the two built modules read the
  SAME existing REST snapshot endpoints
  (`/v1/overlay-widgets/:overlayId/supporter-ticker`,
  `/v1/overlay-goals/:overlayId`) the standalone widget pages already read
  — this task added no new content endpoint, only the module-cap endpoint
  (`/v1/overlay-widgets/:overlayId/master-canvas/modules`). RT-13's
  per-channel live-transport cap (counting Canvas as one connection
  alongside any standalone widgets a creator still runs) is unimplemented
  and was explicitly out of scope for this task; it remains a real gap
  between what §21.3 describes and what is built.

---

## Slice 2 — Tug-of-War Vote, Boss Fight, and RT-12 blind-spot closure

**Status:** `Conditionally complete — implemented and locally verified; independent review unavailable; PRF-02's full register row still not closed`
**Review authority:** `reviews/2026-09-16-prf-02-slice-2-scope-review.md` — product/market/creator/streamer scope review, already performed by a separate review-only agent and confirmed by Opus. This slice's implementation record (`reviews/2026-09-16-prf-02-slice-2-implementation.md`) points at that review rather than repeating it.
**Acceptance test:** `tests/TC-PRF-02-slice-2-vote-boss-fight.md`

This slice adds exactly two more built modules on the SAME slice-1 runtime
— module #3 (Tug-of-War Vote) and module #4 (Boss Fight) — and closes the
RT-12 blind spot slice 1's own record above found and referred onward. It
does **not** touch Support Theater (module #1, split into its own slice by
the scope review's decision, recorded in the review), Reaction Cloud,
Safe Soundboard Alert, Moderator Status Card, or any other catalogue
module. PRF-02's register row is **still not closed** — five of twenty
modules remains not a canvas, and Opus decides the letter after auditing,
per this task's own hard rule.

### Scope, exactly three things

**(a) RT-12's blind spot.** `packages/db/explain-plans/required-queries.json`
is a declared manifest of every `app_private` function that backs an
overlay/widget-facing route (15 entries after this slice). `packages/db/explain-plans/scan-required-queries.mjs`
scans `apps/api/src/db/*.ts` and `apps/api/src/routes/*.ts` for every
`app_private.list_overlay_*` call actually present and fails the build if
one is missing from the manifest — the "make forgetting hard" half the
scope review's decision #2 asked for. `check-plans.mjs` was changed to
iterate the manifest (require an artifact for every declared entry)
instead of a directory listing (which only knew what already had a file).
`pnpm explain:check` now runs the scan then the plan check, still inside
`verify:local` where RT-12's own original closure wired it.

Building the scan honestly (general-purpose, not hand-tuned to the two
named functions) found **three more gaps beyond the two this task named**:
`app_private.list_overlay_lottie_assets` (migration 0077) and
`app_private.list_overlay_widget_config` (migration 0105) both predate
PRF-02 entirely and had no artefact either; the third, this task's own
named `app_private.list_channel_master_canvas_modules`, does not follow
the `list_overlay_*` convention the scan keys on and is in the manifest
only by explicit addition, not because the scan would ever nominate it. A
scan tuned to catch only the two functions already known about would
repeat RT-12's own failure pattern one level up, so all five gaps found —
the two named, the two pre-existing, and the one new function this slice's
own module #3 added (`app_private.list_overlay_tug_of_war_vote`) — are
captured, not only the two originally named. Five new artefacts:
`master-canvas-modules-overlay.explain.md`, `master-canvas-modules-channel.explain.md`,
`lottie-assets.explain.md`, `widget-config.explain.md`,
`tug-of-war-vote.explain.md`. `pnpm explain:check` now reports
`15/15 plans current`. See `tests/TC-RT-12-explain-plans.md`'s update for
the closed-vs-narrowed assessment.

**(b) Module #3 — Tug-of-War Vote.** A new `app_private.list_overlay_tug_of_war_vote`
function (`packages/db/migrations/0132_v1_prf02_slice2_tug_of_war_vote.sql`)
resolves "the" current two-sided (exactly two options), paid,
`is_enabled` `support_vote` definition for a channel — no per-module
config step exists yet (the canvas designer UI is out of scope, same as
slice 1), so this mirrors `list_overlay_goal`'s own "resolve the one that
applies, no id argument" precedent exactly. It reuses the EXISTING
money-derived tally math from migration 0108
(`app_private.paid_support_vote_tally`/`list_overlay_paid_vote_tally`) —
same join, same "sum payments minus processed refunds, live, every
read" rule — adding only the "which definition" resolution in front of
it. `apps/api/src/db/vote-payment-sql-store.ts` gained
`createSqlTugOfWarVoteOverlayStore`, reusing that file's existing
`PaidVoteTally` shape and `toPaidTally` helper rather than building a
parallel store. New overlay route:
`GET /v1/overlay-widgets/:overlayId/tug-of-war-vote` (`apps/api/src/routes/interactions.ts`,
alongside the existing paid-vote overlay route). New web module:
`apps/web/app/overlay/canvas/modules/tug-of-war-vote-module.ts`, with its
pure-function counterpart `tug-of-war-vote-logic.ts` (the transparency
definition and its reasoning live there — see "Decisions" below).

**Transparency definition (this task's own — no market precedent exists,
confirmed by the scope review's product research):** a two-sided paid
vote is transparent when a viewer and a creator can both see the
displayed bar follows from what was actually paid. Concretely: (1) the
bar's fraction and (2) the exact rupee amount on each side are both pure
functions of the CURRENT server response, recomputed on every render —
the module holds no running counter that could diverge from the durable
record; (3) the exact amount is shown, not only a percentage, because a
percentage alone can round away a real divergence; (4) all three surfaces
that can ever show this vote's state — the creator dashboard tally
(`paid_support_vote_tally`, unchanged), the standalone OBS paid-vote
widget (`list_overlay_paid_vote_tally`, unchanged), and this Canvas
module (`list_overlay_tug_of_war_vote`, new) — read from the same
underlying join, so there are three surfaces but never three independent
derivations that could disagree.

**(c) Module #4 — Boss Fight.** `apps/web/app/overlay/canvas/modules/boss-fight-module.ts`
is a skin over the Community Goal Ladder's existing data path — it
imports and calls the exact same `progressPercent`/`formatRupees`/`isOverlayGoal`
functions from `goal-widget-logic.ts` that `goal-ladder-module.ts` calls,
and reuses the SAME `/v1/overlay-goals/:overlayId` fetch function
(`fetchGoalSnapshot`, defined once in `[overlayId]/page.tsx` and passed to
both modules). No table, no event type, no second progress computation —
the only arithmetic this module performs on top of the shared
`progressPercent(goal)` output is `1 - progress/100` (inverted, for a
"remaining boss health" read), which is presentation of the same number,
not a second source of truth for it.

### Binding constraints — proven with all four modules present

`master-canvas-integration.test.ts` gained two tests: "with all four built
modules entitled: still exactly one connection and one rAF chain" (real
ticker, goal ladder, vote, and boss fight modules together — asserts
exactly 1 transport open attempt, 4 connection subscribers, and 1 pending
frame handle on the manual scheduler) and "a throwing tug_of_war_vote
module does not blank the canvas" (the three OTHER real module renderers
proven to keep rendering across both frames a module keyed
`tug_of_war_vote` throws on, and that it goes `down` with the runtime's
`onModuleDown` firing exactly once after the second failure — reusing the
runtime's own generic error-boundary mechanism, already proven in
isolation by slice 1's `master-canvas-runtime.test.ts`, now proven
alongside real production modules rather than only fakes). Both new
modules' own test files (`tug-of-war-vote-module.test.ts`,
`boss-fight-module.test.ts`, 8 tests each) each carry their own
`deactivate() called twice is idempotent and discards a late in-flight
fetch` case, `prefers-reduced-motion disables the transition` case, and a
composite-only assertion (`scaleX` only, `style.width`/`style.height`
never set to express state).

### Evidence location

`tests/TC-PRF-02-slice-2-vote-boss-fight.md`,
`packages/db/tests/prf02_slice2_tug_of_war_vote.sql`,
`apps/api/test/l16b-interactions-paid-vote-and-widgets-routes.test.ts` (seven new
route-level cases for `/v1/overlay-widgets/:overlayId/tug-of-war-vote`, added after
an audit found the route had none — see `tests/TC-PRF-02-slice-2-vote-boss-fight.md`'s
"Update 2026-09-16" section),
`apps/web/app/overlay/canvas/modules/tug-of-war-vote-logic.test.ts`,
`apps/web/app/overlay/canvas/modules/tug-of-war-vote-module.test.ts`,
`apps/web/app/overlay/canvas/modules/boss-fight-module.test.ts`, the two
new cases in `apps/web/app/overlay/canvas/master-canvas-integration.test.ts`,
`packages/db/explain-plans/required-queries.json`,
`packages/db/explain-plans/scan-required-queries.mjs`, the five new
`.explain.md` artefacts named above, and this section.

### Checks run — real counts, this worktree, 2026-09-16 (from `bharatstudio-alerts` unless noted)

| Command | Result |
|---|---|
| `pnpm --filter @bharatstudio/alerts-api build` | passed |
| `pnpm --filter @bharatstudio/alerts-api test` | **585 passed, 0 failed** (slice-1 baseline 578/0; net +7 — **corrected 2026-09-16**: this row originally read "578, unchanged, no new apps/api test file", which was wrong. An audit found the new overlay route had no route-level test even though the codebase's own established pattern (`l16b-interactions-paid-vote-and-widgets-routes.test.ts`) covers its sibling paid-votes route exactly this way — the SQL and web-module tests exercise the layers either side of the route but not its own auth/error behaviour. Seven route-level tests were added mirroring that file's existing pattern; see `tests/TC-PRF-02-slice-2-vote-boss-fight.md`'s "Update 2026-09-16" section for the full account) |
| `pnpm --filter @bharatstudio/alerts-web build` | passed |
| `pnpm --filter @bharatstudio/alerts-web test` | **386 passed, 0 failed** (slice-1 baseline 358/0; net +28: `tug-of-war-vote-logic.test.ts` ×10, `tug-of-war-vote-module.test.ts` ×8, `boss-fight-module.test.ts` ×8, `master-canvas-integration.test.ts` ×2 new) |
| `pnpm contracts:validate` | passed — 40 fixtures, 68 OpenAPI paths, 75 operation contracts, 3 negative cases, unchanged (the new overlay route was not added to `contracts/openapi/v1.yaml`, matching the same precedent slice 1 already recorded — creator-facing/overlay CRUD-shaped routes aren't documented there) |
| `pnpm explain:check` | **`OK: every app_private.list_overlay_* call ... is present in required-queries.json (15 manifest entries)` then `OK: 15/15 plans current`** (was 10/10; net +5) |
| `pnpm db:test:all` | **59 files passed, 0 failed** (slice-1 baseline 58/0; net +1, `prf02_slice2_tug_of_war_vote.sql`) |
| `pnpm db:test:l03` | **25 file(s) passed** (slice-1 baseline 24; net +1), full Go/TS integration legs unchanged and passing |
| `pnpm measurement:test` | passed — 5 Node tests + 4 Python tests, unchanged |
| `(cd services/alert-worker-go && go build ./... && go test -race ./... && go vet ./...)` | passed, 10 packages, all `ok`, untouched by this slice |
| `(cd services/payment-webhook-go && go build ./... && go test -race ./... && go vet ./...)` | passed, 10 packages (one `[no test files]`, pre-existing), all `ok`, untouched by this slice |
| `git diff --check` | clean |
| `python3 tools/doc_consistency.py` (this repository) | see the run recorded at the foot of this record |
| `python3 tools/traceability.py` (this repository) | see the run recorded at the foot of this record |

**What this evidence is not** — same rule as slice 1, restated because it
is the one most likely skimmed past: every number above is local
(JSDOM/Node test runner, a local Dockerized Postgres, `go test`). None of
it is OBS, Chromium, device, network, or production evidence. §19.0's
RT-07 (blocked) remains the only row that gates any frame-timing,
GPU-compositing, memory-over-8-hours, or "one source replaces twelve"
claim — unchanged and untouched by this slice.

### Decisions

- **Support Theater stays out of this slice** — the scope review's own
  decision (`reviews/2026-09-16-prf-02-slice-2-scope-review.md`), not
  re-litigated here.
- **The Tug-of-War Vote's "which vote" resolution has no per-module
  config step**, because the canvas designer UI is out of scope for this
  slice (same as slice 1). Resolving "the" current two-sided paid vote
  the same way the goal ladder resolves "the" goal — no id argument, an
  explicit, stated tiebreak rule (prefer open over closed; among ties,
  the most recent timestamp) — is this slice's own scoping decision, not
  drawn from any authority, and is recorded in full in migration 0132's
  header and in `reviews/2026-09-16-prf-02-slice-2-implementation.md`.
- **Vote transparency's definition** (above) is this slice's own, for the
  reason the scope review recorded: no competitor's official
  documentation describes a real-money paid vote's fairness model at all.
- **The honest RT-12 scan surfaced two gaps beyond this task's own
  brief** (`list_overlay_lottie_assets`, `list_overlay_widget_config`).
  Both are closed here rather than left, because a scan that finds a gap
  and is only partially acted on is not the "make forgetting hard"
  outcome the scope review asked for.

### Referred to Opus

- Whether `interaction_definitions` would benefit from a partial index on
  `(channel_id, interaction_type, is_enabled)` once a channel accumulates
  many closed/expired votes — `tug-of-war-vote.explain.md` shows a
  `Seq Scan on interaction_definitions` in the `active_definition`
  resolution, honest at this seed size, not evidence of production-size
  behaviour. No number is invented; this is left for a slice where a
  realistic row count is actually measurable.
- RT-12's blind spot is **narrowed, not fully closed** — see
  `tests/TC-RT-12-explain-plans.md`'s update for exactly what would still
  slip past the new manifest-and-scan mechanism.

---
## Slice 3 — Support Theater ported onto the runtime, its own overlay session, "next up"

**Status:** `Conditionally complete — implemented and locally verified; independent review unavailable; PRF-02's full register row still not closed`
**Review authority:** `reviews/2026-09-16-prf-02-slice-2-scope-review.md` — the product/market/creator/streamer scope review that split Support Theater into its own slice, already performed by a separate review-only agent and confirmed by Opus. This slice's implementation record (`reviews/2026-09-16-prf-02-slice-3-implementation.md`) points at that review rather than repeating it, and additionally carries a dated **Correction** section — read that before this task record's own "Decisions" below, because it changes what those decisions say.

### Correction, 2026-09-16 — read this first

This slice was first built and verified with Support Theater given its
own, second overlay session (a `stOverlayId`/`stToken` URL hash pair) and
its own dedicated SSE+acknowledgement transport, separate from the
Canvas's shared `MasterCanvasConnection`. That followed the coordinator's
own instruction as literally written ("the Canvas Support Theater module
requires its own overlay session"). The coordinator then corrected that
instruction: the intent was narrower — the CANVAS must not share a
session with the STANDALONE page, not that Support Theater needed a
session distinct from the rest of its OWN Canvas. Inside one Canvas there
is exactly one acknowledging consumer (Support Theater); the other four
modules are stateless snapshot readers that never call `/cursor`, so
there is no acknowledgement race *inside* a Canvas to defend against, and
giving Support Theater a second session cost the property PRF-02 exists
for — one connection, adding a module adds zero connections — for a risk
that lived at a different boundary (between the Canvas and the separate
standalone page, which already has its own session by construction).

This is recorded as a correction, not silently rewritten, per the
coordinator's own explicit instruction: **the two-session design and its
evidence below have been replaced, in place, by the corrected one-
connection design** — this task record now describes only the corrected
design, and the full account of what was built first, what was wrong
with it, and how it was fixed lives in
`reviews/2026-09-16-prf-02-slice-3-implementation.md`'s own "Correction"
section, attributed there to the coordinator rather than to this
implementer's judgement. Everything below this note describes the
CORRECTED design only.

| Field | Value |
|---|---|
| **Scope phase** | `v1`; Phase 0.5/opening Phase 1, same as slices 1–2. Renderer for the fifth catalogue module (`support_theater`) plus its acknowledgement/queue/display-timer/audio orchestration, ported to the runtime shape — no new capability |
| **Owner** | **Sukhdev Singh** |
| **Tier and gate** | Same server-owned §30.3 module cap as every other built module (Free 2 / Pro 5 / Creator 12 / Studio all) — `support_theater` was already in migration 0131's 20-key catalogue check constraint (slice 1), so no migration change was needed |
| **Personal-data class** | Unchanged from the existing standalone page this module ports: operational/personal (supporter display name, message, amount) already carried by `get_overlay_events`'s existing payload — no new field, no new identifier, no new log/metric label |
| **Provider or legal dependency** | None. Reuses the existing `/v1/overlays/:overlayId/events` and `/v1/overlays/:overlayId/cursor` routes byte-for-byte unchanged, through the Canvas's own single, already-existing overlay session — no second session, no new capability |
| **Failure behaviour** | See "Failure behaviour, kill switch, rollback" below |
| **Kill switch** | See "Failure behaviour, kill switch, rollback" below |
| **Acceptance test** | `tests/TC-PRF-02-slice-3-support-theater.md` |
| **Evidence location** | `tests/TC-PRF-02-slice-3-support-theater.md`, `apps/web/app/overlay/canvas/modules/support-theater-module.ts`, `apps/web/app/overlay/canvas/modules/support-theater-module.test.ts`, `apps/web/app/overlay/canvas/alert-audio.ts`, `apps/web/app/overlay/canvas/master-canvas-connection.ts` (extended: `subscribeToEvents`/`acknowledge`, ack-aware reconnect cursor, forced resync), `apps/web/app/overlay/canvas/master-canvas-connection.test.ts` (+5), `apps/web/app/overlay/canvas/[overlayId]/page.tsx` (wiring), `apps/web/app/overlay/canvas/master-canvas-integration.test.ts` (the five-modules test), `apps/web/app/overlay/canvas/text-rendering.ts` (the additive `message` role), and this section |
| **Rollback** | See "Failure behaviour, kill switch, rollback" below |

### Failure behaviour, kill switch, rollback

**Failure behaviour:**

- **The module throws twice.** The runtime's existing generic per-module
  error boundary (unchanged, proven in slices 1–2) marks it `down` after
  the second failure; the other four modules keep rendering.
- **The shared connection drops.** It reconnects with backoff, exactly as
  it already did for the four snapshot modules. Once Support Theater's
  event-payload subscription exists, reconnect resumes from the
  **acknowledged** cursor, never the merely-seen one, so an unacknowledged
  delivery can never be silently skipped by the server's own
  `created_at >` filter (`get_overlay_events`, unchanged) — see
  `master-canvas-connection.ts`'s own header for the full reasoning.
- **An acknowledgement fails.** Retried with backoff (500ms → 5s,
  unchanged from the standalone page's own values, now issued through the
  connection's `acknowledge()` method rather than a private fetch); the
  item is neither dropped nor shown a second time by this consumer.
- **TTS/audio fails or times out.** Falls through to the chime, exactly
  as RT-03 and the standalone page already specify — `DEFAULT_TTS_PLAYBACK_TIMEOUT_MS`
  (`tts-runtime.ts`) is untouched by this slice.
- **`deactivate()` at any point** — mid-acknowledgement, mid-display-timer,
  mid-audio-playback — is safe and idempotent: one `generation` counter
  gates every fetch, the display timer, and the acknowledgement retry loop
  together (this task's own binding instruction, §1 "Build one
  invalidation token..."). This property was unaffected by the transport
  correction — it lives entirely in the module's own state machine, not in
  how events arrive. See "Decisions" below for why the stale-`active.current`
  stall is impossible **by construction**, not only tested against.

**Kill switch:** identical in kind to slices 1–2's — the pre-existing
standalone page (`/overlay/[overlayId]/page.tsx`) is **untouched by this
slice** (this slice added one new file, `canvas/alert-audio.ts`, rather
than editing the standalone page, specifically so that invariant stays
literally true — see Decisions) and remains fully functional. A creator
who wants out of Canvas Support Theater removes the Canvas source from
OBS and keeps their existing standalone alert source — no data migration,
because both consumers read the same underlying
`event_outbox_deliveries`/`alert_events` tables through the same,
unmodified routes, each through its own session (the Canvas's one session,
the standalone page's own separate one — the real boundary the original
scope review's race lives at).

**Rollback:**

- Delete `apps/web/app/overlay/canvas/modules/support-theater-module.ts`,
  `apps/web/app/overlay/canvas/modules/support-theater-module.test.ts`,
  and `apps/web/app/overlay/canvas/alert-audio.ts`.
- Revert `apps/web/app/overlay/canvas/[overlayId]/page.tsx` (the
  `supportTheaterContainerRef`, the module registration block, and the
  note/CSS additions), `apps/web/app/overlay/canvas/master-canvas-connection.ts`
  (the `subscribeToEvents`/`acknowledge` extension, the dual-cursor
  tracking, `forceReconnect`), and `apps/web/app/overlay/canvas/text-rendering.ts`
  (the additive `message` role) to their slice-2 state.
- Revert the new tests in `apps/web/app/overlay/canvas/master-canvas-connection.test.ts`
  and `apps/web/app/overlay/canvas/master-canvas-integration.test.ts`.
- No migration, no new table, no new route — nothing to roll back
  server-side. This slice added zero database or API surface.

### Boundaries

**In scope, this slice:** Support Theater (§6 #1) as a fifth built
module — queue selection/aggregation, per-item durable acknowledgement
with retry, the timed display-then-acknowledge state machine, TTS/chime
audio orchestration, best-effort Lottie enrichment — all ported from the
standalone page onto `activate()`/`deactivate()`/`render()`, all gated by
one invalidation token; the "next up" field (§12.7); extending the shared
`MasterCanvasConnection` with an event-payload subscription and an
`acknowledge()` method, so Support Theater can join the ONE connection
the other four modules already use rather than needing a second one.

**Explicitly out of scope, not touched:** every other unbuilt catalogue
module (Reaction Cloud, Safe Soundboard Alert, Moderator Status Card, and
the rest); the canvas designer UI in the dashboard; §15.4.3 customisation
controls for this module; RT-07 evidence (blocked, unrelated); the SSE
route, the overlay session/auth model, `get_overlay_events`, the cursor
endpoint or its semantics, migrations `0022`/`0127`'s acknowledgement
behaviour — **none of these were changed**; `DEFAULT_TTS_PLAYBACK_TIMEOUT_MS`
(`tts-runtime.ts`) — untouched; the standalone page
(`apps/web/app/overlay/[overlayId]/page.tsx`) — untouched, per §21.3 and
this task's own instruction not to remove or deprecate it.

### Decisions

- **One Canvas, one session, one connection — Support Theater included.**
  Corrected per the coordinator's own instruction (see "Correction,
  2026-09-16" above): the session-sharing race the original scope review
  found is between the Canvas and the SEPARATE standalone page, not
  between modules inside one Canvas. Support Theater now acknowledges
  through the Canvas's own single session, using the SAME `overlayId`/
  `token`/`connection` the other four modules already share.
- **The shared connection was extended, not duplicated.** `master-canvas-
  connection.ts` gained `subscribeToEvents()` (delivers each event's
  parsed payload once, plus a `{type:'connected'}` marker on every
  (re)connect) and `acknowledge()` (one-attempt POST `.../cursor`,
  advancing the connection's own ack-aware reconnect cursor on success).
  Snapshot-only modules are unaffected: `subscribe()` is unchanged, and a
  data frame's JSON body is only ever parsed when at least one
  event-payload subscriber exists — a module that never calls
  `subscribeToEvents` pays nothing extra.
- **Reconnect correctness needed a second, ack-aware cursor.**
  `get_overlay_events` (migrations 0022/0127, unchanged) replays
  `status in ('ready','displayed')` — replay-eligible until acknowledged,
  regardless of whether a consumer merely saw an item on the wire. The
  four snapshot modules never acknowledge, so "last cursor seen"
  (`rawCursor`) is fine for them. Support Theater cannot tolerate a
  reconnect cursor racing ahead of what it has actually acknowledged — an
  unacknowledged delivery could be silently skipped by the server's
  `created_at >` filter. So once any event-payload subscriber exists,
  reconnect uses `ackCursor` (advanced only by a successful
  `acknowledge()`) instead. Proven directly:
  `master-canvas-connection.test.ts`'s "once an event-payload subscriber
  exists, reconnect uses the ack-aware cursor" test.
- **A late event-subscriber forces one immediate, deliberate reconnect.**
  If the stream is already running for snapshot-only reasons and Support
  Theater's event subscription joins afterward, the connection would
  otherwise only hand it FUTURE frames, silently missing anything already
  unacknowledged. `subscribeToEvents()` detects exactly this transition
  and calls `forceReconnect()` (backoff bypassed, reset to the initial
  delay) so the fresh connect's `last-event-id` triggers a correct
  replay. In THIS codebase, `BUILT_MODULE_KEYS` lists `support_theater`
  FIRST and the host page registers/entitles it first, specifically so
  this path is the correctness backstop, not the ordinary case — proven
  directly in `master-canvas-connection.test.ts`'s "a late event-payload
  subscriber... forces an IMMEDIATE reconnect" test, and proven NOT to
  fire spuriously in the ordinary five-modules-together case by
  `master-canvas-integration.test.ts`'s `getOpenAttemptCount() === 1`
  assertion.
- **One invalidation token, not three flags — unaffected by the
  transport correction.** The standalone page effectively had three
  independent cancellation mechanisms because each was a separate
  `useEffect`. This module has exactly one `generation` counter gating the
  acknowledgement retry loop, the display timer, the Lottie fetch, and the
  audio fetch together, per this task's own binding instruction. This
  property lives entirely in the module's own state and did not need to
  change when the transport did.
- **The stale-`active.current` stall is impossible by construction, not
  merely tested against.** The standalone page's "one group in flight"
  gate (`active = useRef(false)`) is created once and never reset — safe
  there only because an unmounted component never runs again. This
  module's `activate()` can be called again on the SAME returned object
  (the runtime's own `reconcile()`, unchanged). `resetForActivation()`
  unconditionally resets every piece of pump state at the **top** of
  `activate()` itself, not only relying on a prior `deactivate()` having
  done so. `support-theater-module.test.ts`'s "deactivate() mid-
  acknowledgement ... then re-activate ... the pump runs" test proves this
  directly.
- **A canvas-scoped duplicate of two small audio helpers, not a
  cross-cutting refactor of the rollback file.** `playChime`/`safeAudioUrl`
  are duplicated into `apps/web/app/overlay/canvas/alert-audio.ts` rather
  than extracted from the standalone page, so the standalone page — this
  product's named mid-stream rollback path — stays untouched by this
  task. Stated explicitly in `alert-audio.ts`'s own header as a cost
  accepted rather than an oversight.
- **"Next up" is bounded to exactly one item, proven not asserted.** The
  module reads only `queue[0]`; nothing in its render path can reach
  `queue[1]` or a depth/count.
- **Bounded aggregate DOM, correcting the standalone page's own pattern.**
  A fixed, recycled 8-line pool (`DEFAULT_THEATER_AGGREGATE_POOL_SIZE`,
  an engineering default, same class of value as the ticker's own
  `DEFAULT_TICKER_ROW_POOL_SIZE`) with a "+N more" summary for anything
  beyond it.
- **Indic script fallback.** Unchanged posture from slices 1–2: font
  family stays data (`defaultCanvasTextStyles()`, extended with one
  additive `message` role). Porting the alert surface makes Indic
  fallback **more clearly mandatory**, not less, before this module
  becomes creator-configurable — carried forward as the same binding
  precondition slices 1–2 already recorded, now extended to this module.
- **Moderator Status Card, backlog depth, ETA stay OUT**, per the scope
  review and Opus's ruling — not re-litigated here.
- **A same-session mismatch with the standalone page is not detected,
  and that is stated rather than guessed at.** The original design's
  "same-session double-mount" guard was built to protect against a risk
  that, corrected, no longer applies to the Canvas's own session at all —
  the real, remaining risk (a creator pasting the Canvas's session into a
  *separate* standalone-page browser source, or vice versa) is not
  observable from this page's own JavaScript, which has no visibility
  into a different browser source's configuration. Per this task's
  instruction not to build elaborate detection where cheap detection
  is not available, no client-side heuristic is built for it — see
  Referred, below.

### Evidence location

`tests/TC-PRF-02-slice-3-support-theater.md`,
`apps/web/app/overlay/canvas/modules/support-theater-module.ts`,
`apps/web/app/overlay/canvas/modules/support-theater-module.test.ts` (10
cases), `apps/web/app/overlay/canvas/alert-audio.ts`,
`apps/web/app/overlay/canvas/master-canvas-connection.ts` (extended),
`apps/web/app/overlay/canvas/master-canvas-connection.test.ts` (+5 cases),
`apps/web/app/overlay/canvas/[overlayId]/page.tsx`,
`apps/web/app/overlay/canvas/text-rendering.ts`,
`apps/web/app/overlay/canvas/master-canvas-integration.test.ts` (one
corrected five-modules case), and this section.

### Checks run — real counts, this worktree, 2026-09-16 (from `bharatstudio-alerts` unless noted)

| Command | Result |
|---|---|
| `pnpm --filter @bharatstudio/alerts-api build` | passed, untouched by this slice |
| `pnpm --filter @bharatstudio/alerts-api test` | **585 passed, 0 failed** (slice-2 baseline 585/0; unchanged — this slice added no `apps/api` code) |
| `pnpm --filter @bharatstudio/alerts-web build` | passed; `/overlay/canvas/[overlayId]` route unchanged in the route table |
| `pnpm --filter @bharatstudio/alerts-web test` | **402 passed, 0 failed** (slice-2 baseline 386/0; net +16: `support-theater-module.test.ts` ×10, `master-canvas-connection.test.ts` ×5 new, `master-canvas-integration.test.ts` ×1 corrected) |
| `pnpm contracts:validate` | passed — 40 fixtures, 68 OpenAPI paths, 75 operation contracts, 3 negative cases, unchanged (no new/changed route) |
| `pnpm explain:check` | **OK: every app_private call ... present (16 manifest entries, 6 exemptions)** then **OK: 16/16 plans current** — unchanged from the count already present when this slice's correction pass began (another agent's concurrent work in `packages/db/explain-plans/`, not this slice's; per this task's own instruction, a higher count from that agent is not a failure). This slice added no widget-backing query |
| `pnpm db:test:all` | **59 files passed, 0 failed** — unchanged from slice 2 (this slice added no migration and no SQL test file) |
| `pnpm db:test:l03` | **25 file(s) passed** — unchanged from slice 2, full Go/TS integration legs passed |
| `pnpm measurement:test` | passed — 5 Node tests + 4 Python tests, unchanged |
| `(cd services/alert-worker-go && go build ./... && go test -race ./... && go vet ./...)` | passed, 10 packages, all `ok`, untouched by this slice |
| `(cd services/payment-webhook-go && go build ./... && go test -race ./... && go vet ./...)` | passed, 10 packages (one `[no test files]`, pre-existing), all `ok`, untouched by this slice |
| `git diff --check` | clean |
| `python3 tools/doc_consistency.py` (this repository) | see the run recorded at the foot of this record |
| `python3 tools/traceability.py` (this repository) | see the run recorded at the foot of this record |

**What this evidence is not** — same rule as slices 1–2, restated because
it is the one most likely skimmed past: every number above is local
(JSDOM/Node test runner, a local Dockerized Postgres, `go test`). None of
it is OBS, Chromium, device, network, or production evidence. §19.0's
RT-07 (blocked) remains the only row that gates any frame-timing,
GPU-compositing, memory-over-8-hours, or "one source replaces twelve"
claim — unchanged and untouched by this slice.

### Referred to Opus

- **A same-session mismatch between the Canvas and the standalone page
  cannot be detected client-side**, and this task's own hard rules
  forbid building a server-side signal for it (an L3 API/data change)
  without separate authority. If this is worth closing, it needs its own
  scope call — not decided here. (The original slice's dashboard-URL
  referral, "no flow exists to generate a second session's URL," no
  longer applies: there is no second session to generate a URL for.)

---

## Slice 4 — Challenge Board (current-only) and Milestone Celebration

**Status:** `Conditionally complete — implemented and locally verified; independent review unavailable; PRF-02's full register row still not closed`
**Review authority:** the product/market/creator/streamer scope review for this slice was performed by a separate review-only agent and confirmed by Opus, exactly as slices 2/3's own review gate required — but unlike slice 2's (`reviews/2026-09-16-prf-02-slice-2-scope-review.md`), that review was not itself persisted as a standalone file in `reviews/`; its findings and Opus's resulting decisions were instead carried directly into this task's own command text (the exact `app_private.list_overlay_challenge` `limit 1` finding, the false→true edge definition for Milestone Celebration, and the three decisions below). This slice's implementation record (`reviews/2026-09-16-prf-02-slice-4-implementation.md`) points at that command text as the scope authority, per this task's own instruction not to repeat it, and separately notes the missing standalone file as a gap against the slice 2/3 precedent rather than silently matching the pattern by inventing a citation to a file that does not exist.

### Opus's three decisions, carried forward from the scope review

1. **Challenge Board (§6 #8) ships current-only, not "current / next / completed."** `app_private.list_overlay_challenge` (migration `0109_v1_l17_paid_challenges.sql`, lines ~344–368) returns exactly the single most-recently-updated public challenge for the channel, `limit 1` — there is no "next" (no priority/queue column exists on `public.challenges`, only `created_at`/`updated_at`) and no "completed" list to read. Building either is new query work with no defined ordering for "next," and is explicitly deferred, not built, not stubbed.
2. **The "next"/"completed" ordering question is open, not decided.** No product decision exists for what "next" would even mean (creation order? creator-set priority? a queue column that does not exist yet). This slice does not answer it — a follow-up slice needs its own product decision before "next"/"completed" can be built.
3. **Milestone Celebration (§6 #13) does NOT fire on a challenge reaching target this slice.** #8 is current-only and exposes no client-observable "just crossed the target" edge distinct from the ambiguity `isRisingEdge` exists to resolve for goal/vote (a freshly-read `targetReached: true` could already have been true the first time it was ever observed) — wiring a third trigger here would either invent an edge signal challenge-board-module.ts does not have, or couple #13 to a surface (challenge board) that is not built for it. Milestone Celebration stays on exactly the two transitions this task's own command named: `goal.reached` and the paid vote's `resolved`. Revisit when #8 grows past current-only.

| Field | Value |
|---|---|
| **Scope phase** | `v1`; Phase 0.5/opening Phase 1, same as slices 1–3. Renderers for the sixth and seventh catalogue modules (`challenge_board`, `milestone_celebration`) — no new capability, no new endpoint, no new query, no new event |
| **Owner** | **Sukhdev Singh** |
| **Tier and gate** | Same server-owned §30.3 module cap as every other built module (Free 2 / Pro 5 / Creator 12 / Studio all) — both `challenge_board` and `milestone_celebration` were already in migration `0131`'s 20-key catalogue check constraint (slice 1), so no migration change was needed for either |
| **Personal-data class** | Unchanged from the existing endpoints this slice reads. Challenge Board reads `/v1/overlay-challenges/:overlayId` (unchanged, pre-existing L17 route) — operational/personal at most (challenge title, amounts; no viewer-identifying field). Milestone Celebration reads only the pre-existing goal (`/v1/overlay-goals/:overlayId`) and vote (`/v1/overlay-widgets/:overlayId/tug-of-war-vote`) snapshots already fetched by other modules — no new field, no new identifier, no new log/metric label introduced by either module |
| **Provider or legal dependency** | None. Both modules are pure client-side renderers over existing, unmodified REST snapshot endpoints, driven by the existing shared `MasterCanvasConnection`'s plain re-read signal (`subscribe()`) — never its event-payload/acknowledgement path (`subscribeToEvents()`/`acknowledge()`), which stays Support Theater's alone. Reaching for that path here would repeat the exact transport mistake slice 3's Correction warns against: a second, wrongly-scoped connection concern grafted onto a module with no acknowledgement semantics of its own |
| **Failure behaviour** | See "Failure behaviour, kill switch, rollback" below |
| **Kill switch** | See "Failure behaviour, kill switch, rollback" below |
| **Acceptance test** | `tests/TC-PRF-02-slice-4-challenge-milestone.md` |
| **Evidence location** | `tests/TC-PRF-02-slice-4-challenge-milestone.md`, `apps/web/app/overlay/canvas/modules/challenge-board-module.ts`, `apps/web/app/overlay/canvas/modules/challenge-board-module.test.ts`, `apps/web/app/overlay/canvas/modules/challenge-failure-copy-parity.test.ts`, `apps/web/app/overlay/canvas/modules/milestone-celebration-logic.ts`, `apps/web/app/overlay/canvas/modules/milestone-celebration-logic.test.ts`, `apps/web/app/overlay/canvas/modules/milestone-celebration-module.ts`, `apps/web/app/overlay/canvas/modules/milestone-celebration-module.test.ts`, `apps/web/app/overlay/canvas/[overlayId]/page.tsx` (wiring), `apps/web/app/overlay/canvas/master-canvas-integration.test.ts` (the seven-modules test), and this section |
| **Rollback** | See "Failure behaviour, kill switch, rollback" below |

### Failure behaviour, kill switch, rollback

**Failure behaviour:**

- **Either module throws twice.** The runtime's existing generic per-module error boundary (unchanged, proven in slices 1–3) marks it `down` after the second failure; every other module — including the other of this pair — keeps rendering on the same loop.
- **The shared connection drops.** It reconnects with backoff exactly as it already does for every snapshot-only module; both new modules are plain `subscribe()` consumers, so a reconnect simply triggers one fresh re-read for each, same as the goal ladder/boss fight/vote modules already do.
- **A Challenge Board snapshot is stale or absent.** The module keeps rendering the last value it has (or nothing, if it has never received one) — never invented, never a broken/zero-progress bar shown as current.
- **A Milestone Celebration fetch fails.** `.catch(() => null)` on both the goal and vote fetch legs — a failed read simply does not update `lastGoalReached`/`lastVoteResolved` for that cycle, and no celebration fires from a fetch that never completed. The next successful re-read resumes edge detection from wherever it last successfully observed each field — no state is corrupted by a transient failure.
- **`deactivate()` on either module, at any point** — mid-fetch, mid-visible-celebration-window — is safe and idempotent: both modules gate every in-flight fetch behind a monotonically-incremented token (`fetchToken`) exactly like every other snapshot module in this Canvas, and Milestone Celebration additionally clears its own hide-timer and hides both its DOM elements immediately on `deactivate()`, proven directly by `milestone-celebration-module.test.ts`'s "deactivate() hides an in-progress celebration immediately and is idempotent" case.
- **The `master-canvas-modules/modules` entitlement endpoint never returns either key.** Exactly PRF-02.10's existing rule (slices 1–3, unchanged): a module the server does not return is never activated — never subscribed, never fetched, never rendered.

**Kill switch:** identical in kind to every prior slice's. Challenge Board's kill switch is the pre-existing standalone widget (`apps/web/app/overlay/widgets/challenge/[overlayId]/page.tsx`), untouched by this slice and still fully functional — a creator who wants out of the Canvas simply removes this Canvas source from OBS and keeps or re-adds the standalone challenge widget source, no data migration, because both read the exact same `/v1/overlay-challenges/:overlayId` endpoint. Milestone Celebration has no standalone equivalent (§6 names it only as a Canvas module) — its kill switch is the server-owned module cap/entitlement toggle (`app_private.upsert_master_canvas_module`, unchanged from slice 1): disabling the `milestone_celebration` row removes it from `list_overlay_master_canvas_modules`'s response, and the runtime never activates it, same as any other module falling outside the tier cap.

**Rollback:**

- Delete `apps/web/app/overlay/canvas/modules/challenge-board-module.ts`, `challenge-board-module.test.ts`, `challenge-failure-copy-parity.test.ts`, `milestone-celebration-logic.ts`, `milestone-celebration-logic.test.ts`, `milestone-celebration-module.ts`, and `milestone-celebration-module.test.ts`.
- Revert `apps/web/app/overlay/canvas/[overlayId]/page.tsx` (the `challengeContainerRef`/`milestoneContainerRef` refs, the `fetchChallengeSnapshot` function, the two module-registration blocks, the two `BUILT_MODULE_KEYS` entries, and the CSS/DOM additions) and `apps/web/app/overlay/canvas/master-canvas-integration.test.ts` (the seven-modules test) to their slice-3 state.
- No migration, no new route, no new database function — nothing to roll back server-side. Both `challenge_board` and `milestone_celebration` were already present in migration `0131`'s catalogue check constraint before this slice; this slice adds no schema of any kind.

### Boundaries

**In scope, this slice:** Challenge Board (§6 #8), narrowed to current-only, as the sixth built module — reading the existing `/v1/overlay-challenges/:overlayId` snapshot exactly as the standalone widget does, rendering exactly the single challenge that endpoint returns; Milestone Celebration (§6 #13) as the seventh built module — one reusable animation (plus its reduced-motion static alternative) fired on the false→true edge of `goal.reached` and of the paid vote's `resolved`, sourced from the SAME snapshot-fetcher functions already passed to the goal/vote modules; a cross-package test (`challenge-failure-copy-parity.test.ts`) that closes a pre-existing, previously-unchecked gap — the API's and the web widget's `CHALLENGE_FAILURE_COPY` copies had never been automatically verified byte-identical before this slice, only commented as such in both files.

**Explicitly out of scope, not touched:** "next"/"completed" ordering for Challenge Board (Opus's decision 1–2 above); Milestone Celebration firing on a challenge (Opus's decision 3); every other unbuilt catalogue module (Reaction Cloud, Safe Soundboard Alert, Stream Mission Card, QR Smart Card, Sponsor Card, Moderator Status Card, and the rest); the canvas designer UI in the dashboard; §15.4.3 customisation controls for either new module; RT-07 evidence (blocked, unrelated); the SSE route, the overlay session/auth model, `get_overlay_events`, the cursor endpoint, migrations `0022`/`0109`/`0127` — **none of these were changed**; the standalone challenge widget (`apps/web/app/overlay/widgets/challenge/[overlayId]/page.tsx`) — untouched, per §21.3 and every prior slice's own instruction not to remove or deprecate a standalone route; `apps/api/src/observability/`, `apps/api/src/routes/metrics.ts`, and anything OPS — untouched, per this task's own explicit boundary (a separate agent's concurrent work); `active/traceability/register-map.tsv` and `semantic-mapping-audit.md` — untouched, reconciled by Opus.

### Decisions

- **`CHALLENGE_FAILURE_COPY` is imported, never re-declared, in the Canvas module.** `challenge-board-module.ts` imports the constant from `../../widgets/challenge/challenge-widget-logic.ts` — the same web-side copy the standalone widget itself renders — rather than declaring a third copy. This follows the task's own preference ("prefer importing the existing constant over re-declaring it") and means there is structurally no THIRD string that could drift; there remains exactly the pre-existing two (API, web widget), now covered by an automated identity check for the first time (see below).
- **No override slot exists for the protected copy, and this is proven at the call site, not only by the type signature.** `ChallengeBoardModuleOptions` has no field of any kind for supplying alternate failure/refund copy. `challenge-board-module.test.ts`'s "the protected copy cannot be overridden" case passes an unrelated extra option (`failureCopyOverride`, a string promising a guaranteed refund) that the module's type does not declare and the module never reads, and asserts the rendered copy is still exactly `CHALLENGE_FAILURE_COPY` — proving the absence of an override path operationally, not merely by inspection of the type.
- **The pre-existing two-copy situation (API, web widget) gets its first automated identity check.** `challenge-failure-copy-parity.test.ts` reads `apps/api/src/domain/challenge-store.ts`'s source text directly via `fileURLToPath(new URL(..., import.meta.url))` (apps/web and apps/api share no import boundary for internal modules) and asserts the extracted string is byte-identical to the web-side constant — mirroring the existing cross-package parity pattern already in this codebase (`accept-terms/terms-content.test.ts`'s migration-hash check). Before this slice, the "byte-identical" claim in both files' own header comments was asserted only by comment, never verified by a test.
- **The honest register is enforced by construction, not merely by the copy's wording.** `CHALLENGE_FAILURE_COPY` itself uses "refund"/"escrowed"/"holds no funds" only as denials, never as a promise (`challenge-failure-copy-parity.test.ts`'s "the protected copy names no false refund promise" case asserts this pattern directly against the string). Separately, `challenge-board-module.test.ts` asserts that on a succeeded challenge no refund-adjacent word appears anywhere in the rendered output, and that on a failed/cancelled challenge the ONLY refund-adjacent text present, anywhere in the rendered card, is the sanctioned copy itself — proven by stripping the copy out of the rendered text and asserting the remainder contains no such word.
- **Milestone Celebration's edge-tracking state (`lastGoalReached`/`lastVoteResolved`) lives for the module object's lifetime, not reset by `activate()`/`deactivate()`.** This is a deliberate choice, not an oversight: resetting it on every re-activation (an OBS scene toggling hidden/visible) would make `undefined` the starting point again on every toggle, which would either miss a genuine transition that happened while the module was inactive, or — the more dangerous failure — treat an already-true value observed for the first time right after reactivation as fresh, which is exactly the spurious-refire failure mode this task's own §5 instruction forbids ("not... on a reconnect that re-delivers the same already-true snapshot"). Preserving the state across activation cycles avoids both.
- **The rising-edge rule starts at `undefined`, never at `false`.** `milestone-celebration-logic.ts`'s `isRisingEdge(previous, next)` fires only when `previous === false && next === true` — an unseen value (`undefined`) transitioning straight to `true` is deliberately NOT an edge. This single rule is what satisfies both halves of this task's own §5 requirement at once: it fires on a genuine false→true transition, and it does not fire on a reconnect (or a fresh activation) that redelivers an already-true snapshot the module had never previously seen become true.
- **One reusable animation, two DOM elements, never one implementation per trigger.** Both `goal.reached` and the vote's `resolved` calling `fire(label)` is the only difference between the two triggers — there is exactly one render path, one pair of elements (`milestone-celebration-animated`, `milestone-celebration-badge`), reused regardless of which field fired. Boss Fight rides the same goal object Community Goal Ladder reads, so a goal's edge is already one celebration shared by both surfaces, not two.
- **The reduced-motion alternative is a distinct element with no transition, not the same animation played faster.** `milestone-celebration-badge` is a separate DOM node from `milestone-celebration-animated`, toggled with no CSS `transition` property set at all — its opacity flips from 0 to 1 (and back) as a genuinely instantaneous state change, carried by its own colour/border/text, not by motion at any speed. `milestone-celebration-module.test.ts`'s "prefers-reduced-motion: a distinct static badge becomes visible, the animated burst never does" case asserts both that the badge becomes visible AND that it carries no transition, specifically to rule out "the same animation, just shorter" as a passing implementation.
- **Milestone Celebration reuses the host page's existing `fetchGoalSnapshot`/`fetchTugOfWarVoteSnapshot` functions by reference — no second source of truth.** Passed exactly as Boss Fight already reuses `fetchGoalSnapshot` verbatim (slice 2's own precedent) rather than duplicating either fetch function or endpoint. This does mean the goal endpoint is now independently called by three modules (Goal Ladder, Boss Fight, Milestone Celebration) and the vote endpoint by two (Tug-of-War Vote, Milestone Celebration) — an accepted, precedented cost (Boss Fight already duplicated the goal fetch in slice 2), not a new query or endpoint.
- **Challenge Board is current-only, proven structurally, not merely by not building "next."** The module's `fetchSnapshot` type returns a single `OverlayChallenge | null`, matching `/v1/overlay-challenges/:overlayId`'s own shape exactly — there is no array, no list, no second field anywhere in the module for a "next" or "completed" entry to occupy. `challenge-board-module.test.ts`'s own header case name states this directly ("no next/completed field exists anywhere in this module").
- **Composite-only (PRF-03), same technique as every prior slice's modules.** Challenge Board corrects the standalone widget's own `.challenge-widget-fill { transition: width 400ms ease }` pattern exactly as `goal-ladder-module.ts` and `boss-fight-module.ts` already did for the goal endpoint — `transform: scaleX()` on a fixed-size track. Milestone Celebration's burst uses `opacity`/`transform: scale()` exclusively; the badge uses `opacity` only. `node .github/scripts/canvas-static-check.mjs` scans both new files' `render()` bodies and reports zero PRF-03 violations.
- **Indic script fallback.** Unchanged posture from slices 1–3: both new modules read their font families from `defaultCanvasTextStyles()` (`text-rendering.ts`, unmodified), never a hard-coded family. Neither module renders new free-text fields beyond what §15.4.3's binding precondition (owner ruling, slices 1–3, recorded above under "Boundaries") already covers — Challenge Board's title is creator-authored text of the same kind Goal Ladder's title already is, so this slice's addition does not change the urgency already recorded: Indic fallback remains required before either module becomes creator-configurable, not before it merely renders (which it already does, via the shared default stack).
- **Not wired to Support Theater's acknowledgement stream, and not wired to a challenge target.** Both are stated explicitly here because this task's own command named them as the two mistakes to avoid: Milestone Celebration uses `connection.subscribe()`, never `connection.subscribeToEvents()`/`acknowledge()` (see "Provider or legal dependency" above), and it fetches no challenge data of any kind — `MilestoneCelebrationModuleOptions` has no field for a challenge snapshot fetcher, proven at compile time by `milestone-celebration-module.test.ts`'s "does not fire on a challenge reaching target" case (a type-level check that fails to compile if such a field is ever added).
- **No register state letter changed.** PRF-02 stays `A` — seven of twenty modules is still not a canvas, per this task's own explicit instruction.

### Evidence location

`tests/TC-PRF-02-slice-4-challenge-milestone.md`,
`apps/web/app/overlay/canvas/modules/challenge-board-module.ts`,
`apps/web/app/overlay/canvas/modules/challenge-board-module.test.ts` (10
cases), `apps/web/app/overlay/canvas/modules/challenge-failure-copy-parity.test.ts`
(2 cases), `apps/web/app/overlay/canvas/modules/milestone-celebration-logic.ts`,
`apps/web/app/overlay/canvas/modules/milestone-celebration-logic.test.ts`
(6 cases), `apps/web/app/overlay/canvas/modules/milestone-celebration-module.ts`,
`apps/web/app/overlay/canvas/modules/milestone-celebration-module.test.ts`
(11 cases), `apps/web/app/overlay/canvas/[overlayId]/page.tsx` (wiring),
`apps/web/app/overlay/canvas/master-canvas-integration.test.ts` (one new
seven-modules case), and this section.

### Checks run — real counts, this worktree, 2026-09-16 (from `bharatstudio-alerts` unless noted)

| Command | Result |
|---|---|
| `pnpm --filter @bharatstudio/alerts-api build` | passed, untouched by this slice |
| `pnpm --filter @bharatstudio/alerts-api test` | **585 passed, 0 failed** (slice-3 baseline 585/0; unchanged — this slice added no `apps/api` code) |
| `pnpm --filter @bharatstudio/alerts-web build` | passed; `/overlay/canvas/[overlayId]` route unchanged in the route table (same dynamic route, new modules registered inside it) |
| `pnpm --filter @bharatstudio/alerts-web test` | **431 passed, 0 failed** (slice-3 baseline 402/0; net +29: `challenge-board-module.test.ts` ×10, `challenge-failure-copy-parity.test.ts` ×2, `milestone-celebration-logic.test.ts` ×6, `milestone-celebration-module.test.ts` ×11, `master-canvas-integration.test.ts` ×1 new) |
| `pnpm contracts:validate` | passed — 40 fixtures, 68 OpenAPI paths, 75 operation contracts, 3 negative cases, unchanged (no new/changed route — both modules read pre-existing endpoints) |
| `pnpm explain:check` | **OK: 16/16 plans current** — unchanged from the slice-3 baseline; both `app_private.list_overlay_challenge` (pre-existing, L17) and `app_private.list_overlay_goal`/`list_overlay_tug_of_war_vote` (already covered by slices 1–2) already carried manifest entries and artifacts before this slice — no new widget-backing query was added |
| `pnpm db:test:all` | **61 files passed, 0 failed** — slice-3 baseline was 59/0; the +2 is another agent's concurrent OPS work (`ops08_activation_state.sql`, `ops11_revenue_kpis.sql`), not this slice's — per this task's own instruction, a higher number from concurrent work is not a failure. This slice added no SQL file |
| `pnpm db:test:l03` | **25 file(s) passed** — unchanged from slice 3 (this slice added no migration and no SQL test file); full Go/TS integration legs passed |
| `pnpm measurement:test` | passed — 5 Node tests + 4 Python tests, unchanged |
| `(cd services/alert-worker-go && go build ./... && go test -race ./... && go vet ./...)` | passed, 10 packages, all `ok`, untouched by this slice |
| `(cd services/payment-webhook-go && go build ./... && go test -race ./... && go vet ./...)` | passed, 10 packages (one `[no test files]`, pre-existing), all `ok`, untouched by this slice |
| `node .github/scripts/canvas-static-check.mjs` | passed — 16 canvas source files scanned (up from 14 at slice 3, both new module files included), zero PRF-03 violations; PRF-04 ceiling unset, reported for visibility only (`challenge-board-module.ts`: 6 static `createElement()` sites; `milestone-celebration-module.ts`: 4) |
| `git diff --check` | clean |
| `python3 tools/doc_consistency.py` (this repository) | **17 checks · 0 errors · 0 warnings** (unchanged) |
| `python3 tools/traceability.py` (this repository) | regenerated `TRACEABILITY.md`, clean |

**What this evidence is not** — same rule as slices 1–3, restated because it
is the one most likely skimmed past: every number above is local
(JSDOM/Node test runner, a local Dockerized Postgres, `go test`). None of
it is OBS, Chromium, device, network, or production evidence. §19.0's
RT-07 (blocked) remains the only row that gates any frame-timing,
GPU-compositing, memory-over-8-hours, or "one source replaces twelve"
claim — unchanged and untouched by this slice.

### Referred to Opus

- **No standalone scope-review file was produced for this slice**, unlike slices 2/3's own `reviews/2026-09-16-prf-02-slice-2-scope-review.md`. The review's findings reached this implementation only through the coordinator's own command text. This is recorded as a gap against the established pattern, not silently matched by fabricating a citation to a file that was never written — whether a standalone record should be back-filled is a documentation-process call for whoever owns that pattern, not decided here.
- **"Next"/"completed" ordering for Challenge Board remains genuinely undefined.** Opus's decision 2 above states the gap; closing it needs a product decision (creation order? a creator-set priority field? a queue column that does not exist yet on `public.challenges`?) before any schema or query work can start. Not decided here, and not guessed at.
- **The `master-canvas-integration.test.ts` seven-modules test reuses `async () => null` fetchers for Challenge Board and both of Milestone Celebration's snapshot fetchers**, matching the existing four/five-module tests' own convention of exercising the connection/runtime wiring rather than each module's full internal logic (which the modules' own dedicated test files already cover in depth). Named here only so the test's scope is not overstated.
