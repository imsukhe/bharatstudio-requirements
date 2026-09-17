# PRF-02 slice 7 — Vertical Stream Layout (§6 module #14)

**Status:** `Defined — implementation pending a quiet tree`
**Owner:** Sukhdev Singh
**Date:** 2026-09-17
**Authority:** `../../FULL-PRODUCT-DEFINITION.md` §6 module #14, §9.1.1, §12.7, §30.3, §34 · `CST-08`
**Decision record:** `../../reviews/2026-09-17-remaining-eight-modules-and-youtube-v1-amendment.md` Part 1 §4

## Scope

One **fixed 9:16 arrangement** of already-built canvas modules. No variant selection, no
variant system, no aspect-ratio switcher.

**Tier: Pro**, per §30.3's tier table, which binds. Note the deliberate distinction already
recorded at §30.3: the *vertical layout* is Pro; maintaining **three** aspect-ratio variants
of one canvas side by side is `CST-08`, which is Creator and Phase 2. This task is the first
thing, never the second.

## A contradiction this task inherits, and how it resolves

§6 row #14 describes the layout's contents as **"Narrow chat, compact goal, QR, reactions
for mobile scenes."**

**There is no chat module.** Owner decision 2026-09-17 closed §6 #19 as *not a canvas
module*: §4.2.1 places chat display in the dashboard and Companion via YouTube's official
embed, and §9.1.1 forbids that embed inside the Master Canvas. A vertical layout cannot
arrange a module that does not exist on the surface it arranges.

**Resolution.** The vertical layout contains **compact goal, QR and reactions**. It contains
no chat, and no placeholder, empty slot or reserved region standing in for chat — a reserved
gap is a promise that something will fill it, and nothing will. §6's "narrow chat" wording
predates the #19 decision and is superseded by it.

This is recorded rather than silently dropped because a future reader comparing the built
layout against §6's row will otherwise count three of four elements and file a defect.

## CORRECTION, 2026-09-17 — this task's own stop-condition fired, and the answer changed

The section below predicted "no new module, no migration, no API route and no contract
change", and told the implementer to stop and re-examine if an overlay read appeared
necessary. It appeared necessary. Re-examining produced a different answer, recorded here
rather than contradicted silently.

**1. A layout is not a module, so it must not be a module key.** `vertical_stream_layout`
already exists in migration `0131`'s `master_canvas_modules` key catalogue, written when §6
had twenty modules. Reusing it would need no migration at all — and would be wrong. §30.3's
cap counts **"Master Canvas modules active"** (2 / 5 / 12 / all), so a Pro creator with five
slots would spend one on *being vertical* and keep four for content. A layout arranges the
others; it is not one of them.

**2. The Pro gate needs server-side truth.** §30.3 places the vertical layout at Pro+. A gate
enforced only in the browser is UI hiding, which `00_LAUNCH_SCOPE_AUTHORITY.md` already
rejects for the channel-read boundary in as many words: *"Database projections and RLS enforce
this boundary; UI hiding alone is insufficient."* An overlay browser source is the least
trusted surface in the product; a tier decision cannot live there.

**Therefore a migration IS required**, contrary to the prediction below. It reuses
`app_private.current_channel_tier` (migration `0086`, generic and pre-existing) rather than
inventing a tier lookup, and follows the entitlement shape `0143`'s
`app_private.soundboard_module_entitled` already established for the same Pro+ tier — the
check is called from **inside** the overlay read, so an unentitled channel's valid token
simply receives the horizontal layout.

**3. A second defect found while re-examining, and fixed in the same migration.** `0131`'s
check constraint still admits four keys no module implements: `now_playing`, `chat`,
`stream_health_widget` and `vertical_stream_layout`. Today's owner decisions made the first
three **permanently** dead — `AUD-11` stands, chat was never a canvas module, and health
moved to the dashboard — and the fourth is this task's layout, which is not a module. Left
alone, a creator can enable `now_playing`, consume a §30.3 cap slot, and render nothing
forever. That is configuration reachable to no effect, and it is closed here because today's
decisions are what created it.

## What it may contain

Only modules already registered on the runtime. This slice builds **no new module, no
migration, no API route and no contract change** — it is an arrangement of existing
renderers. If it appears to need a new overlay read, that is a signal the scope has drifted;
stop and re-examine.

## Constraints

- Pure renderer on the existing contract: ONE transport, ONE rAF loop, per-module error
  boundary, idempotent `deactivate()`, `transform`/`opacity` only.
- §9.1.1: no third-party code, URL, iframe, script or stylesheet; no module-definition field
  capable of carrying one.
- §12.7: the overlay receives projections and never fetches freely. A narrower viewport must
  not cause any module to fetch more, subscribe more, or retain more than it already does.
  **No surface may fetch, render, subscribe to, or retain more live data than it can display
  safely** — and a vertical layout displays *less*, so it must never ask for more.
- §30.3's active-module cap counts modules, not layouts. A layout is not a module and must
  not consume a cap slot.
- No invented dimension, breakpoint or ratio beyond the fixed 9:16 the decision names.

## Risk accepted by the owner, restated

`CST-08` may later define variants in a shape this fixed layout does not fit, making it a
special case to unwind. The owner took that trade knowingly to have vertical output in v1.
Recorded here so the eventual unwind is understood as a known cost, not a surprise.

## Sequencing

Implementation waits for a quiet tree. Four concurrent lanes (`0143`–`0146`) are editing
`apps/web/app/overlay/canvas/[overlayId]/page.tsx`, which this task must also edit. Any
measurement taken while those lanes are active is void, and any commit taken now risks
sweeping their in-progress files.

## Implementation note, 2026-09-17

Implemented. `packages/db/migrations/0147_v1_prf02_vertical_layout.sql`: a `public.channels.canvas_layout`
column (`horizontal` default / `vertical`, mirroring `0138`'s `safe_mode_enabled` shape — one bit
of state, no new table), `app_private.set_channel_canvas_layout`/`get_channel_canvas_layout`
(creator, owner/admin write, all-member read, never tier-gated to store), and
`app_private.list_overlay_canvas_layout` (overlay read, evaluating the Pro+ gate
`app_private.vertical_canvas_layout_entitled` — reusing `app_private.current_channel_tier`,
0086:139 — INSIDE the query, so a sub-Pro channel's valid token gets `layout: 'horizontal'`, never
an error). The same migration retires the four dead `master_canvas_modules` catalogue keys
(`now_playing`, `chat`, `stream_health_widget`, `vertical_stream_layout`) this task's CORRECTION
section named, deleting any existing rows (logged via `RAISE NOTICE`, none existed) and tightening
the check constraint to the remaining sixteen.

API: `apps/api/src/domain/canvas-layout-store.ts` (types + `projectOverlayCanvasLayout`),
`apps/api/src/db/canvas-layout-store.ts` / `canvas-layout-overlay-store.ts` (SQL, main pool /
derivedReadSql split), `apps/api/src/routes/canvas-layout.ts` (creator GET/PUT), and the overlay
GET wired into `apps/api/src/routes/master-canvas.ts` as `registerMasterCanvasRoutes`'s 14th
positional dependency. `MASTER_CANVAS_MODULE_KEYS` (master-canvas-store.ts) now lists sixteen keys.

Web: `apps/web/app/overlay/canvas/modules/canvas-layout-logic.ts`
(`CANVAS_LAYOUT_ARRANGED_MODULE_KEYS` = exactly `community_goal_ladder`, `qr_smart_card`,
`reaction_cloud` — never chat) wired into `[overlayId]/page.tsx` as one additional fetch, outside
`runtime.registerModule()` entirely (§12.7: no new subscriber, `getSubscriberCount()` stays 16).
CSS `.master-canvas-root--vertical` hides every module except the three arranged ones and stacks
them into one fixed 9:16 column; the goal ladder gets a compact CSS variant only, never a second
renderer.

Contracts: `/v1/channels/{channelId}/canvas-layout` (GET/PUT, creator) and
`/v1/overlay-widgets/{overlayId}/canvas-layout` (GET, overlay) added to `contracts/openapi/v1.yaml`
with their schemas and fixtures — the OpenAPI `moduleKey` enum instruction did not apply (no such
enum exists in the contract; see the implementation record's "Blocker recorded" section).

Governance: `../tests/TC-PRF-02-slice-7-vertical-layout.md`,
`../reviews/2026-09-17-prf-02-slice-7-vertical-layout-implementation.md`.

Verification (this run): sql 72/0 · api 775/0 · web 643/0 · typecheck 0/0 (api, web, run
separately from the test runner) · contracts 63 fixtures/104 paths/121 operations · explain 26/26 ·
harness pass. One pre-existing, unrelated environmental failure noted and excluded:
`scripts/measurement/run_local_measurement.test.mjs` (Docker-availability assumption mismatch in
this sandbox; no diff against base commit `8643e87`).
