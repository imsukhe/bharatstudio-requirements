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
