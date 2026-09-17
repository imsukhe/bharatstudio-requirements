# TC-PRF-02 slice 7 — Vertical Stream Layout (§6 #14): acceptance record

**Date:** 2026-09-17
**Owner:** **Sukhdev Singh**
**Task:** `../active/tasks/PRF-02-slice-7-vertical-layout.md` (including its "CORRECTION, 2026-09-17" section)
**Decision:** `../reviews/2026-09-17-prf-02-slice-7-vertical-layout-implementation.md`
**Binding owner decision:** `../reviews/2026-09-17-remaining-eight-modules-and-youtube-v1-amendment.md` Part 1 §4

Written to accompany implementation, per `governance/AGENTS.md`. The "Commands run" table is filled
in from actual output, and is the single place this slice's numbers live.

---

## Acceptance criteria

### A. A layout is not a module — no cap slot, no catalogue key

| ID | Criterion |
|---|---|
| VL14.1 | `public.master_canvas_modules.module_key` no longer accepts `'vertical_stream_layout'`, `'now_playing'`, `'chat'` or `'stream_health_widget'` — the tightened check constraint rejects all four |
| VL14.2 | Configuring a channel's canvas layout (`app_private.set_channel_canvas_layout`) creates no `master_canvas_modules` row — verified directly by row count before and after |
| VL14.3 | `apps/api/src/domain/master-canvas-store.ts`'s `MASTER_CANVAS_MODULE_KEYS` carries exactly sixteen keys, none of them the four retired ones |
| VL14.4 | `apps/web/.../master-canvas-integration.test.ts`'s all-sixteen-modules subscriber-count assertion (`getSubscriberCount() === 16`) is unaffected — the layout is never registered via `runtime.registerModule()` |
| VL14.5 | Migration 0147 deletes any pre-existing dead-key rows before tightening the constraint, and logs the exact count and (channel_id, module_key) pairs via `RAISE NOTICE` — never silent |

### B. Storing is never tier-gated; the Pro+ render gate lives only in the overlay read

| ID | Criterion |
|---|---|
| VL14.6 | A Free-tier channel can call `set_channel_canvas_layout` with `'vertical'` and have it recorded — no exception, no tier check in the write path |
| VL14.7 | `app_private.list_overlay_canvas_layout` evaluates `app_private.vertical_canvas_layout_entitled` (Pro+, reusing `app_private.current_channel_tier`, migration 0086 line 139) **inside** the query |
| VL14.8 | **The sub-Pro proof:** a Free-tier channel configured `'vertical'` receives a valid overlay token answer of `layout = 'horizontal'` — never an error, never zero rows for that reason |
| VL14.9 | Upgrading the same channel to Pro flips the overlay projection to `'vertical'` live, with no second write to `canvas_layout` |
| VL14.10 | An explicit `'horizontal'` choice on a Pro-entitled channel is honoured (entitlement never overrides the creator's own choice) |
| VL14.11 | Only owner/admin may write (`42501` for operator/moderator/viewer/non-member); every member role can read; a non-member sees zero rows |
| VL14.12 | An unrecognised layout value (not `'horizontal'`/`'vertical'`, including `null`) is rejected `22023` — checked *after* the authorization check, so a non-owner/admin's malformed request still answers `42501` |
| VL14.13 | An unrecognised tier fails closed (`app_private.canvas_layout_tier_rank` raises), never silently resolved |

### C. Overlay session gating — the one place a valid session still answers nothing

| ID | Criterion |
|---|---|
| VL14.14 | A **valid** overlay session **always** returns exactly one row — there is no "nothing to paint" state for a layout, unlike every other module read in this schema |
| VL14.15 | A wrong token fingerprint, an expired session, and a revoked session each return **zero rows** — the one state `canvasLayout: null` still represents at the route layer |
| VL14.16 | Cross-channel isolation: another channel's overlay session never sees this channel's configured layout |
| VL14.17 | **The returned column set is exactly `layout`** — asserted against `information_schema.parameters` for `list_overlay_canvas_layout`'s declared `OUT` columns; `get_channel_canvas_layout`'s is exactly `layout,vertical_entitled` |

### D. API routes

| ID | Criterion |
|---|---|
| VL14.18 | `GET /v1/overlay-widgets/:overlayId/canvas-layout` with no bearer token is 401; with a token and no store is a retryable 503 |
| VL14.19 | A store answer is narrowed a SECOND time by `projectOverlayCanvasLayout` in the route layer — a channel id, a variant id or an unrecognised layout value handed up by a rogue store never reaches the response body |
| VL14.20 | `GET /v1/channels/:channelId/canvas-layout` (creator session) returns the full projection (`layout`, `verticalEntitled`) or `null` |
| VL14.21 | `PUT /v1/channels/:channelId/canvas-layout` (creator session) sets and returns the layout; a non-owner/admin channel is 404 (never a leaking 403) |
| VL14.22 | The request body schema accepts only `{"layout": "horizontal"}` / `{"layout": "vertical"}` — `additionalProperties: false` and `enum` (not a bare `type: string`) reject any variant id, aspect ratio, scene id, or unrecognised value with a 400 before the store is ever called |
| VL14.23 | `registerMasterCanvasRoutes`'s positional dependency list is extended (position 14, after `overlayQrSmartCard` at position 13) without breaking any existing positional call site |

### E. The client arrangement — compact goal, QR, reactions; no chat, no gap

| ID | Criterion |
|---|---|
| VL14.24 | `CANVAS_LAYOUT_ARRANGED_MODULE_KEYS` is exactly three keys — `community_goal_ladder`, `qr_smart_card`, `reaction_cloud` — and never includes `chat` or a fourth placeholder entry |
| VL14.25 | `canvasRootClassName('horizontal')` returns the unmodified base class; `canvasRootClassName('vertical')` adds exactly one modifier class |
| VL14.26 | The page reads the layout from exactly ONE new endpoint call, outside `runtime.registerModule()` entirely — no new module fetch, subscription or retained state is added to satisfy §12.7 |
| VL14.27 | A failed or missing layout read leaves the page at its `'horizontal'` default — never guessed as vertical |

---

## Commands run

| Command | Result |
|---|---|
| Full SQL suite (`sh packages/db/tests/run-sql-suite.sh`, all 72 files incl. this slice's own two: `prf02_slice7_vertical_layout.sql`, and `prf02_master_canvas_module_cap.sql` updated in place) | pass=72 fail=0 |
| `apps/api` route/unit suite (`tsx --test`; package `@bharatstudio/alerts-api`) | tests 775, pass 775, fail 0 |
| `apps/web` suite (`tsx --test`; package `@bharatstudio/alerts-web`) | tests 643, pass 643, fail 0 |
| `apps/api` TypeScript typecheck (`tsc -p tsconfig.json --noEmit`, separate from the test runner) | 0 errors |
| `apps/web` TypeScript typecheck (`tsc --noEmit -p tsconfig.json`) | 0 errors |
| `node contracts/validate-fixtures.mjs` | Validated 63 fixtures plus the v1 template catalogue contract |
| `node contracts/validate-openapi.mjs` | Validated OpenAPI 3.1 document with 104 paths, 121 operation contracts |
| `node contracts/test-openapi-validator.mjs` | Validated 3 negative OpenAPI operation-contract cases |
| `node packages/db/explain-plans/scan-required-queries.mjs` | OK, 26 manifest entries, 9 exemptions |
| `node packages/db/explain-plans/check-plans.mjs` | OK: 26/26 plans current |
| `pnpm harness:check` (`node .github/scripts/api-test-harness-check.mjs`) | all checks passed |

Not run: `go test`/`go vet` on the three Go services, `pnpm build`, Docker image builds, and
`scripts/load/*` self-tests — none of this slice's files touch Go services or change build output
shape. `pnpm test`'s `measurement:test` sub-step (`scripts/measurement/run_local_measurement.test.mjs`)
fails in this sandboxed execution environment because Docker IS available here (the test's own second
case expects "blocked without external harness" / exit code 2 and gets 1) — confirmed pre-existing and
unrelated to this slice: `scripts/measurement/` has no diff against base commit `8643e87`, and the
failure reproduces identically with none of this slice's files present. Flagged here rather than
silently worked around.
