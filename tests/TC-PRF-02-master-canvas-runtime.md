# TC-PRF-02 — Master Canvas runtime (plus two modules)

**Task:** `../active/tasks/PRF-02.md`
**Owner:** Sukhdev Singh
**Status:** `Conditionally complete — local verification passed; independent review unavailable`

This record covers only this slice: the runtime plus the Supporter Ticker
and Community Goal Ladder modules. It is not, and does not claim to be,
evidence that PRF-02's full register row is done — the other eighteen
catalogue modules are future slices, and §19.0 RT-07 (blocked) is the only
row that can ever supply OBS/device/frame-timing/8-hour-memory evidence —
nothing below is that.

| Case | Control | Expected evidence | Status | Where |
|---|---|---|---|---|
| PRF-02.1 | Single transport | A canvas with both modules opens exactly one transport connection; adding a module adds zero | **Passing** | `master-canvas-connection.test.ts` ("two subscribers share exactly one connection attempt"); `master-canvas-integration.test.ts` ("a canvas with both built modules entitled opens exactly one connection") |
| PRF-02.2 | Single rAF loop | One `requestAnimationFrame` loop drives every module; no module schedules its own frame | **Passing** | `master-canvas-runtime.test.ts` ("one shared frame loop drives every active module") — asserts exactly one `requestFrame` handle pending regardless of module count |
| PRF-02.3 | Per-module error boundary | A module that throws does not blank the canvas; the others keep rendering | **Passing** | `master-canvas-runtime.test.ts` ("a module that throws during render does not blank the canvas") — the good module renders on the SAME frame the bad one throws |
| PRF-02.4 | Fail-twice-stays-down | A module that fails twice stays down with a visible note (PRF-14), never retried a third time | **Passing** | `master-canvas-runtime.test.ts` ("a module that fails twice stays down...") — asserts exactly 2 render attempts ever, the down callback fires exactly once, and the host page renders a note (`[overlayId]/page.tsx`'s `downModules` state, wired to `onModuleDown`) |
| PRF-02.5 | Bounded/recycled DOM | Ticker node count is bounded and returns to baseline over many events, not two | **Passing** | `supporter-ticker-module.test.ts` ("the ticker row pool is created once...") — drives 80 distinct events, asserts flat node count (`DEFAULT_TICKER_ROW_POOL_SIZE`) after every one |
| PRF-02.6 | Idle/inactive unsubscribe, driven by a signal not by rAF cadence | A hidden or inactive module unsubscribes and does no work — zero render calls, zero subscription | **Passing** | `master-canvas-runtime.test.ts` (two cases: un-entitled module gets zero activate/render calls; a `visibilitychange` signal deactivates synchronously with zero frames ticked in between); `master-canvas-integration.test.ts` ("going hidden tears down every module's connection subscription") |
| PRF-02.7 | Composite-only animation, `prefers-reduced-motion` | Animations use only `transform`/`opacity`, asserted against actual computed styles; reduced motion honoured | **Passing** | `supporter-ticker-module.test.ts` ("animation touches only transform/opacity", "prefers-reduced-motion disables the transition outright"); `goal-ladder-module.test.ts` ("progress is expressed as a transform (scaleX), never as width", "prefers-reduced-motion disables the fill transition") |
| PRF-02.8 | Server-owned module cap | The cap is enforced server-side at Free 2 / Pro 5 / Creator 12 / Studio all, at every tier, by creation order | **Passing** | `packages/db/tests/prf02_master_canvas_module_cap.sql` |
| PRF-02.9 | Durable, never-deleted config | Over-cap modules inactive but viewable/exportable; a downgrade destroys no row; a disable frees the next-oldest module's slot live | **Passing** | same SQL test file; also `apps/api/test/prf02-master-canvas-routes.test.ts` (a `forbidden`/`invalid` upsert outcome never mutates, correct HTTP status) |
| PRF-02.10 | Bounded data (§12.7) | The canvas holds only the bounded set; a module cannot request more than it can display safely | **Passing** | SQL test (`list_overlay_master_canvas_modules` returns `module_key` only — no config, no reason, no disabled/over-cap module); `master-canvas-connection.test.ts` ("the connection retains no event history"); `master-canvas-integration.test.ts` ("a module the server never marks active is never subscribed, never fetched, never rendered") |
| PRF-02.11 | No third party (§9.1.1, PRF-13) | No external browser-source URL, script, iframe or style can enter the canvas, and it is not configurable | **Passing** | `master-canvas-runtime.test.ts` ("a module definition has no field capable of carrying a third-party URL/HTML/script/iframe") — structural: `CanvasModuleDefinition` is exactly `{key, activate, deactivate, render}`, no slot for a URL/HTML/script to occupy even in principle |
| PRF-02.12 | Reconnect without loss/duplication/staleness-as-current | A dropped transport recovers without losing or duplicating an event, and no module shows a stale value as current | **Passing** | `master-canvas-connection.test.ts` ("a dropped stream reconnects and forces a fresh notify") — a reconnect always triggers a fresh notify to every subscriber, never silently resumes as if nothing happened; `supporter-ticker-module.test.ts`/`goal-ladder-module.test.ts` ("deactivate ... discards a late in-flight fetch") — a response that resolves after teardown is never applied as current |
| PRF-02.SQL | Migration 0131 | Cap enforcement at all four tiers by creation order; durable rows across a downgrade; owner/admin-only upsert; creator-facing list readable by every member role, zero rows for a non-member; overlay-facing read gated by token fingerprint; unrecognised tier fails closed | **Passing** | `packages/db/tests/prf02_master_canvas_module_cap.sql` |

**Commands run (this worktree, 2026-09-16):**
`pnpm --filter @bharatstudio/alerts-api build` · `pnpm --filter @bharatstudio/alerts-api test` ·
`pnpm --filter @bharatstudio/alerts-web build` · `pnpm --filter @bharatstudio/alerts-web test` ·
`pnpm contracts:validate` · `pnpm explain:check` · `pnpm db:test:all` · `pnpm db:test:l03` ·
`pnpm measurement:test` · `(cd services/alert-worker-go && go build ./... && go test -race ./... && go vet ./...)` ·
`(cd services/payment-webhook-go && go build ./... && go test -race ./... && go vet ./...)` ·
`git diff --check` — all from `bharatstudio-alerts`.
`python3 tools/doc_consistency.py` · `python3 tools/traceability.py` — from `bharatstudio-requirements`.

## Recorded local evidence — 2026-09-16

- `pnpm --filter @bharatstudio/alerts-api build` — passed.
- `pnpm --filter @bharatstudio/alerts-api test` — **578 passed, 0 failed** (this session's own pre-task baseline: 566/0, matching Opus's stated baseline exactly; net +12: `prf02-master-canvas-routes.test.ts`).
- `pnpm --filter @bharatstudio/alerts-web build` — passed; new route `ƒ /overlay/canvas/[overlayId]` registered alongside every pre-existing route, unchanged.
- `pnpm --filter @bharatstudio/alerts-web test` — **358 passed, 0 failed** (baseline 332/0; net +26: `master-canvas-connection.test.ts` ×6, `master-canvas-runtime.test.ts` ×6, `master-canvas-integration.test.ts` ×3, `supporter-ticker-module.test.ts` ×5, `goal-ladder-module.test.ts` ×6).
- `pnpm contracts:validate` — passed: 40 fixtures + the v1 template catalogue, OpenAPI 3.1 document (68 paths, 75 operation contracts), 3 negative cases — unchanged from baseline. The creator-facing `master-canvas.ts` routes were **not** added to `contracts/openapi/v1.yaml`, matching this codebase's own existing precedent (checked, not assumed): neither `goals.ts`'s nor `challenges.ts`'s creator-facing CRUD routes are documented there either — only overlay/browser-source-facing reads are, and this task added no new overlay content route (the two content endpoints the runtime reads, `/v1/overlay-widgets/:overlayId/supporter-ticker` and `/v1/overlay-goals/:overlayId`, already existed and are unchanged).
- `pnpm explain:check` — **OK: 10/10 plans current**, unchanged. This task's two new widget-backing reads do not yet have an RT-12 plan artifact — RT-12 is not in this task's scope; see the task record's Referred section.
- `pnpm db:test:all` (`sh packages/db/tests/run-sql-suite.sh`) — **58 files passed, 0 failed** (baseline 57/0; net +1, `prf02_master_canvas_module_cap.sql`).
- `pnpm db:test:l03` (`sh packages/db/tests/run-l03-application-behavior.sh`, full mode) — **24 file(s) passed** (baseline 23; net +1 — `prf02_master_canvas_module_cap.sql` was added to the curated list), followed by the Go integration legs (`payment-webhook-go/internal/ingress`, `payment-webhook-go/internal/reconcile`, `alert-worker-go/internal/store`), `integration/overlay-wakeup.integration.ts`, `integration/overlay-cross-replica.integration.ts` (both pre-existing, unrelated to this task, passed unchanged), and the apps/api concurrency integration suite (2 tests) — exit 0 end to end.
- `pnpm measurement:test` — passed: 5 Node tests + 4 Python tests, unchanged (unaffected by this task).
- `(cd services/alert-worker-go && go build ./... && go test -race ./... && go vet ./...)` — passed, 10 packages, all `ok` (cached where unchanged), `go vet` clean. Untouched by this task.
- `(cd services/payment-webhook-go && go build ./... && go test -race ./... && go vet ./...)` — passed, 10 packages (`internal/auth` `[no test files]`, pre-existing), all `ok`, `go vet` clean. Untouched by this task.
- `git diff --check` — clean, no whitespace errors.
- `python3 tools/doc_consistency.py` — **17 checks · 0 errors · 0 warnings**, unchanged.
- `python3 tools/traceability.py` — regenerated `TRACEABILITY.md` (783 rows: task 2 · acceptance 23 · review 24 · active 43), no error.

**External blocker:** none. Docker was available locally (`postgres:16-alpine`), so `db:test:all` and `db:test:l03` ran to completion.

**Rollback proof:** not separately rehearsed as a live drill in this session. The rollback path is stated in the task record's Rollback field (delete the listed web/api files; revert the two wiring files; roll back migration 0131 with a new forward migration, never by editing/deleting it — and that specific rollback path does delete configured module rows, an explicit, named exception to §12.6 stated in the task record, not a silent one).

## What this evidence is not

Every command above ran locally: JSDOM/Node's test runner, a local
Dockerized Postgres, `go test`. Per §35.1 rule 6 and this task's §10, none
of it is OBS, Chromium, device, network, or production evidence, and none
of it may be cited as a frame-timing, GPU-compositing, 8-hour-memory, or
"one source replaces twelve" claim. §19.0's RT-07 (blocked) remains the
only row that can supply that evidence.

## Independent Opus verification — 2026-09-16

Files read directly; checks re-run rather than the report accepted.

- `pnpm --filter @bharatstudio/alerts-api test` — **578 passed, 0 failed** (baseline 566).
- `pnpm --filter @bharatstudio/alerts-web test` — **358 passed, 0 failed** (baseline 332).
- `pnpm --filter @bharatstudio/alerts-web build` — succeeded.
- `pnpm db:test:all` — **58 passed, 0 failed** (baseline 57). `git diff --check` clean.
- `python3 tools/doc_consistency.py` — 17 checks, 0 errors, 0 warnings.

**The visibility handling is right, including the part that is easy to get wrong.**
`requestAnimationFrame` does not fire in a backgrounded or hidden context, so a module that
checked `document.hidden` *inside* its rAF callback could never notice it had gone hidden —
the callback stops being called. Deactivation is driven by the `visibilitychange` event and
is independent of whether the frame loop is running. An OBS source that is not on the
current scene is exactly that state, and on a real stream it is the common case rather than
an edge case.

**The module cap is server-owned and derives rather than stores.** Migration `0131` computes
`active`/`inactive_reason` live from current tier and creation-order rank on every read,
mirroring how `support_goal_reached()` computes rather than stores. There is **no delete
path in the file at all**, so a downgrade cannot destroy configuration — an over-cap module
stays viewable, editable and exportable, which is the standing rule that durable creator
records are never tier-gated, enforced in schema rather than asserted in prose. Creation
order is the downgrade tiebreak because no authority states a module priority field, which
is the right refusal to invent one.

### Finding — RT-12's checker is blind to a query that never got a plan

This slice added `app_private.list_channel_master_canvas_modules` and
`app_private.list_overlay_master_canvas_modules`. Neither has an EXPLAIN artefact, and
`pnpm explain:check` still reports **10/10 plans current**. RT-12 has been downgraded
**U → P** and the detail is recorded in `TC-RT-12-explain-plans.md`. Fixing it is folded into
the next PRF-02 slice rather than left, because every ported module adds widget-backing
queries and the gap recurs once per slice otherwise.

### The process fault on this task, recorded rather than smoothed over

The implementing agent wrote the server-side half **before** performing the §6 review and
**before** creating these records, contrary to §8 of its own command and to the operator's
step 5. It was paused mid-task, reported the fault honestly when asked directly, and the
review then produced a commercially material finding (§6's StreamElements note). The
orchestrator's command carried the review and the records-first rule but no enforced pause
between review and build; that gate is now part of the process for Phase 1.

**What this evidence is not.** **The web suite is JSDOM.** It proves the *logic* — one
transport, one rAF loop, bounded and recycled nodes, per-module isolation, visibility-driven
idling. It proves **nothing** about frame timing, GPU compositing, memory across an 8-hour
stream, or behaviour inside OBS. RT-07 is Blocked, so **"one source replaces twelve" remains
unpublishable**, and §6 now additionally records that the source-count claim does not
differentiate against StreamElements at all.
