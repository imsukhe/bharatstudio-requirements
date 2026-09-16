# PRF-02 — Master Canvas as the runtime

**Authority:** [`../../FULL-PRODUCT-DEFINITION.md`](../../FULL-PRODUCT-DEFINITION.md) §6, §19.4, §19.5, §9.1.1, §12.7, §15.4.3, §30.3, §31.18.1 PRF-02, §34, §37.2, §37.11
**Status:** `Conditionally complete — this slice (runtime + Supporter Ticker + Community Goal Ladder) implemented and locally verified; independent review unavailable; PRF-02's full register row remains open`

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
