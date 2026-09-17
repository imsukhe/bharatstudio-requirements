# PRF-02 slice 7 — Vertical Stream Layout (§6 #14): implementation record

**Date:** 2026-09-17
**Owner:** **Sukhdev Singh**
**Authority:** `../FULL-PRODUCT-DEFINITION.md` §6 module #14, §9.1.1, §12.7, §30.3, §34 · `CST-08`
**Binding decision:** `2026-09-17-remaining-eight-modules-and-youtube-v1-amendment.md` Part 1 §4
**Task:** `../active/tasks/PRF-02-slice-7-vertical-layout.md`, including its "CORRECTION, 2026-09-17" section
**Acceptance:** `../tests/TC-PRF-02-slice-7-vertical-layout.md`

---

## What this slice is, and why it needed a migration when the task record originally predicted none

The task record's original body predicted "no new module, no migration, no API route and no
contract change" and told the implementer to stop and re-examine if an overlay read appeared
necessary. It did appear necessary — §30.3 places the vertical layout at Pro+, and
`00_LAUNCH_SCOPE_AUTHORITY.md` already forbids a browser-only version of that kind of gate
("Database projections and RLS enforce this boundary; UI hiding alone is insufficient"). An
overlay browser source is the least trusted surface in the product, so the tier decision cannot
live in `apps/web`. Re-examining produced the CORRECTION section the task record now carries, and
this migration (`0147`) is the direct consequence: it did not exist because the original
prediction turned out to be right and something small was later bolted on; it exists because the
prediction was wrong, and the file's own header records that fact rather than silently
overwriting it.

## A layout is not a module — restated as an implementation decision, not just a comment

`vertical_stream_layout` already existed in migration `0131`'s twenty-key catalogue. Reusing it
would have needed **zero migration work** and would have been the wrong shape: §30.3's cap counts
"Master Canvas modules active" (Free 2 / Pro 5 / Creator 12 / Studio all), so a Pro creator with
five slots would have spent one on *being vertical* and kept four for content. The decision taken
here is the one the CORRECTION section names: the vertical layout is a per-channel canvas
**setting**, not a module.

**Shape chosen: a column on `public.channels`, not a new table.** The task instructions left the
shape open ("your call"). `channels.canvas_layout` mirrors `channels.safe_mode_enabled`
(migration `0138`) exactly — that migration's own header reasons through this precise question
("one bit of current state, no content, no lifecycle, no history... A row-per-channel table would
have needed an absence-means-off convention, a second write path to create the row") and the
vertical layout has the identical shape: one small enum, always present, no history any authority
asks for. A new table was considered and rejected for the same reason `0138` rejected one.

## Reuse anchors, named as the task requires

| Value / shape | Reused from |
|---|---|
| `app_private.current_channel_tier` | `packages/db/migrations/0086_v1_l15_youtube_connectors.sql:139` — generic, pre-existing, not invented for this slice |
| The Pro+ entitlement shape (`*_tier_rank` helper + `*_entitled` wrapper, called FROM INSIDE the overlay read) | `packages/db/migrations/0143_v1_prf02_safe_soundboard.sql`'s `soundboard_tier_rank`/`soundboard_module_entitled` — `canvas_layout_tier_rank`/`vertical_canvas_layout_entitled` are a new, identically-shaped pair rather than a shared helper, matching how every existing `*_tier_rank` function in this schema is already scoped one-per-feature (there is no precedent for a shared one) |
| "One bit of current state, a column not a table" | `packages/db/migrations/0138_v1_prf02_safe_mode.sql`'s `channels.safe_mode_enabled` and its own `set_channel_safe_mode`/`get_channel_safe_mode` pair — `set_channel_canvas_layout`/`get_channel_canvas_layout` mirror their structure (role check, validate, update, return the new value) |
| Owner/admin role check, `has_channel_role` | Used identically throughout — `0109`, `0131`, `0135`, `0138`, `0140`, `0142`, `0143`, `0144`, `0145` |
| Creator-facing read role set (owner/admin/operator/moderator/viewer) | `list_channel_qr_smart_card` (`0144`), `list_channel_master_canvas_modules` (`0131`) |
| "A valid overlay session ALWAYS answers a row" contrasted with "zero rows means the session is invalid" | The overlay-session token-fingerprint/revoked/expired gate every prior slice's overlay read already uses (`0135`, `0138`, `0140`, `0142`, `0143`, `0144`, `0145`, `0146`) — reused for the SESSION half only; the entitlement half is new to this slice because no prior overlay read had a "always answers, but the answer's VALUE depends on entitlement" shape (every prior Pro+-gated read, e.g. `list_overlay_soundboard_play`, answers zero rows for an unentitled channel, not a substituted value) |
| `registerMasterCanvasRoutes` positional-append pattern | Every slice 6/7 overlay dependency already follows it (`overlayReactionCloud` through `overlayQrSmartCard`) — `overlayCanvasLayout` is appended at position 14, after `overlayQrSmartCard` at 13, per the task's own instruction |

## Four dead keys retired, and why this migration is where that happens

`0131`'s check constraint admitted `'now_playing'`, `'chat'`, `'stream_health_widget'` and
`'vertical_stream_layout'` — none has a renderer, and none ever will under today's decisions:
`AUD-11` keeps `now_playing` permanently unbuilt, the 2026-09-17 §19 decision closed chat as never
a canvas module, stream health moved to the dashboard, and section 1 above is this task's own
determination that vertical layout is not a module at all. Left alone, a creator could enable
`now_playing`, spend a §30.3 cap slot on it, and render nothing forever — configuration reachable
to no effect. Closing this here, in the same migration that makes the fourth key's status
official, keeps the "why now" traceable: today's decisions created this specific defect, so
today's migration closes it, rather than opening a separate, unrelated migration whose only
justification would be "found while working on something else."

Migration `0147` deletes any existing rows carrying the four keys **before** tightening the
constraint, and does so loudly: a `RAISE NOTICE` reports the exact row count and every
`(channel_id, module_key)` pair removed, so a schema that genuinely had rows to clean up would
show it in migration output rather than losing them silently. In every environment this migration
is meant to run against today (fresh schemas, the SQL test suite's per-file template databases),
that count is zero — verified by running the full 72-file suite against the migrated schema.

## The sub-Pro proof, and why it is the one required negative test

The task named one negative test explicitly: proving a sub-Pro channel gets horizontal. This is
structurally different from every other Pro+-gated overlay read in this codebase (soundboard,
lobby status, giveaway/tournament) — those all answer **zero rows** for an unentitled channel,
because "nothing to show" is a valid answer for a module. A layout has no such state: the Canvas
always needs *some* arrangement to paint, so `list_overlay_canvas_layout` cannot fall back to
"nothing" the way a module read can. The function's own `case` expression resolves this: entitled
+ configured vertical → `'vertical'`; anything else (including a perfectly valid session on an
unentitled channel that configured vertical) → `'horizontal'`.
`packages/db/tests/prf02_slice7_vertical_layout.sql` section 6 sets up exactly that state — a
Free-tier channel with `canvas_layout = 'vertical'` and a valid overlay token — and asserts the
returned value is `'horizontal'`, then (section 7) upgrades the same channel to Pro and re-asserts
the SAME token now answers `'vertical'`, proving the branch is live-evaluated per read rather than
cached at configuration time.

## No chat, no gap — where this is enforced

The owner's 2026-09-17 §19 decision that chat is never a canvas module is not re-litigated here;
it is inherited as already settled. What this slice adds is the affirmative proof that the
*vertical arrangement specifically* carries no trace of it:
`CANVAS_LAYOUT_ARRANGED_MODULE_KEYS` (`apps/web/app/overlay/canvas/modules/canvas-layout-logic.ts`)
is exactly three keys — `community_goal_ladder`, `qr_smart_card`, `reaction_cloud` — and
`canvas-layout-logic.test.ts` asserts both its length (3) and that it never contains `'chat'`. The
CSS rule set added to `[overlayId]/page.tsx` hides every module except those three when the root
carries the `--vertical` modifier class; there is no fourth rule reserving screen space for
anything, and no commented-out placeholder — the task's own instruction that "a reserved gap is a
promise that something will never arrive" is treated as a constraint on the CSS itself, not only
on the data model.

## §12.7 — no new fetch, subscription or retained state added to any existing module

The vertical layout is wired into `[overlayId]/page.tsx` as exactly one additional `fetch` call,
structurally identical to (and placed alongside) the existing entitlement-list fetch, and
deliberately OUTSIDE `runtime.registerModule()` — it is never subscribed to the shared connection
and never counted by `getSubscriberCount()`. `master-canvas-integration.test.ts`'s existing
all-sixteen-modules assertion is unmodified and still passes, which is the standing proof that
this slice added no seventeenth subscriber. Every module the vertical arrangement reuses (compact
goal, QR Smart Card, Reaction Cloud) keeps its existing fetch function unchanged — "compact" is a
CSS-only modifier on the goal ladder's existing rendered output, never a second renderer or a
second read of goal data.

## Verification

See `../tests/TC-PRF-02-slice-7-vertical-layout.md`'s "Commands run" table for the actual numbers
from this run, including the one pre-existing, unrelated environmental test failure it names and
excludes (`scripts/measurement/run_local_measurement.test.mjs`, reproduced identically with none of
this slice's files present).

## Blocker recorded rather than worked around

`bharatstudio-requirements/active/tasks/PRF-02-slice-7-vertical-layout.md` instructs updating
"the OpenAPI `moduleKey` enum" as part of the dead-key retirement's follow-through. No such enum
exists anywhere in `contracts/openapi/v1.yaml`: `apps/api/src/routes/master-canvas.ts`'s module
list/toggle endpoints build their `moduleKey` enum inline from the `MASTER_CANVAS_MODULE_KEYS`
TypeScript constant (`master-canvas.ts:49`, `enum: [...MASTER_CANVAS_MODULE_KEYS]`) and are not,
and have never been, part of the OpenAPI contract — `master-canvas.ts`'s own header states this
plainly ("this is deliberately NOT the canvas designer UI... neither is in
contracts/openapi/v1.yaml"). That TypeScript constant is updated (now sixteen keys); there was no
separate YAML enum to update to match it. This is not a gap this slice introduced — grepping the
pre-existing contract for `moduleKey` or any of the twenty original catalogue key strings returns
zero matches before this slice's changes as well.
