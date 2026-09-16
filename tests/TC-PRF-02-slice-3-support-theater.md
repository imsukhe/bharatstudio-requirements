# TC-PRF-02 slice 3 — Support Theater on the runtime, sharing the Canvas's one session, "next up"

**Task:** `../active/tasks/PRF-02.md` ("Slice 3" section)
**Owner:** Sukhdev Singh
**Status:** `Conditionally complete — local verification passed; independent review unavailable`

## Correction, 2026-09-16 — read this first

This record originally covered a first build of slice 3 in which Support
Theater opened its own, second overlay session and its own dedicated
SSE+acknowledgement transport, separate from the Canvas's shared
`MasterCanvasConnection`. That design followed the coordinator's own
instruction ("the Canvas Support Theater module requires its own overlay
session") as literally written. The coordinator then corrected that
instruction: the actual intent was narrower — the CANVAS must not share a
session with the STANDALONE page, not that Support Theater needed a
session distinct from the rest of its own Canvas. Inside one Canvas there
is exactly one acknowledging consumer (Support Theater); the other four
modules never call `/cursor`, so there was no session-sharing race
*inside* a Canvas to defend against, and the second session cost the
"one connection, adding a module adds zero connections" property PRF-02
exists for.

**This record has been rewritten in place to test the corrected,
one-connection design, per the coordinator's own explicit instruction —
not silently, and not because this implementer judged the original
design wrong on its own.** The original test cases S3.12 (five modules,
one transport) and S3.13 (the second-session misconfiguration guard) are
replaced below: S3.12 now asserts ONE connection for all five modules,
and S3.13 (the second-session guard) is removed entirely — there is no
second session to guard, and the guard's old form no longer applies. Five
new cases (S3.14–S3.18) cover the mechanics the correction actually
required: the shared connection's event-payload subscription, its
ack-aware reconnect cursor, and its forced-resync backstop. The full
account of what was built first, what was wrong, and how it was found and
fixed lives in `reviews/2026-09-16-prf-02-slice-3-implementation.md`'s own
"Correction" section.

This record covers only slice 3: Support Theater (§6 #1) ported onto the
slice-1/2 runtime, sharing the Canvas's single overlay session, plus the
"next up" field. It is not, and does not claim to be, evidence that
PRF-02's full register row is done — sixteen catalogue modules remain
unbuilt, and §19.0 RT-07 (blocked) is still the only row that can supply
OBS/device/frame-timing/8-hour-memory evidence — nothing below is that.

| Case | Control | Expected evidence | Status | Where |
|---|---|---|---|---|
| S3.1 | Basic port correctness | A delivered alert renders name/amount/message; the watermark kicker follows the server-computed `watermark` field, unchanged | **Passing** | `support-theater-module.test.ts` ("a delivered alert renders name/amount/message...") |
| S3.2 | §12.7 "current and next alert state", bounded not asserted | "Next up" shows exactly the immediately-queued item and nothing deeper — a third queued item's name never appears anywhere in the rendered output | **Passing** | same test ("...next-up shows only the immediate next item, never deeper (§12.7)") — three items queued, only the second's name asserted present, the third's absence asserted directly |
| S3.3 | `deactivate()` mid-acknowledgement is safe, and the stale-`active.current` stall is impossible **by construction** | Deactivating while an acknowledgement call is in flight causes no exception; a late-arriving stale response is a no-op (never repaints); re-activating the SAME module instance afterward causes the pump to run again (a fresh event-payload subscription attaches, the item displays) | **Passing** | `support-theater-module.test.ts` ("deactivate() mid-acknowledgement is safe ... and re-activating the SAME instance runs the pump again — the stale active.current defect, made impossible by construction") — proves the specific defect class named in this task's brief, not a generic smoke test |
| S3.4 | `deactivate()` mid-display-timer is safe and idempotent | Two consecutive `deactivate()` calls neither throw; the display timer is actually cleared (not merely orphaned) — flushing every remaining scheduled callback triggers zero further acknowledgement calls | **Passing** | `support-theater-module.test.ts` ("deactivate() mid-display-timer is safe and idempotent...") |
| S3.5 | `deactivate()` mid-audio-playback is safe and idempotent | An in-flight `play()` is `pause()`d exactly once on `deactivate()`; a second `deactivate()` call does not throw | **Passing** | `support-theater-module.test.ts` ("deactivate() mid-audio-playback is safe and idempotent...") |
| S3.6 | A failed acknowledgement requeues and retries; never dropped, never double-shown | A transient (non-400/401) ack failure is retried with backoff; exactly two acknowledgement attempts are made for the one item — a retry, never a duplicate delivery to the same consumer | **Passing** | `support-theater-module.test.ts` ("a failed acknowledgement retries with backoff and eventually succeeds...") |
| S3.7 | Cross-reconnect dedup survives the port | An item already pending/displayed is not redisplayed or re-queued after the SHARED connection reconnects and replays it again — the module's own cross-lifetime `pendingCursors` set is what prevents the duplicate | **Passing** | `support-theater-module.test.ts` ("cross-reconnect dedup survives the port...") — the shared connection's own reconnect is simulated via `emitConnected()` + re-`emitData()` of the same item |
| S3.8 | RT-03: audio stays synchronised to the displayed item | A late-resolving audio fetch for a group that is no longer current (the pump has already advanced to the next item) never starts playback — `createAudio` is asserted called zero times for the stale group | **Passing** | `support-theater-module.test.ts` ("audio stays synchronised to the displayed item...") |
| S3.9 | Bounded DOM for an aggregated group | An aggregated group's per-supporter lines are drawn from a fixed, recycled pool (`DEFAULT_THEATER_AGGREGATE_POOL_SIZE`); supporters beyond the pool are summarised ("+N more"), never silently dropped from the count and never each given their own appended element | **Passing** | `support-theater-module.test.ts` ("an aggregated group is drawn from a fixed, recycled pool...") |
| S3.10 | `prefers-reduced-motion`; composite-only | Reduced motion disables the module's opacity transition; `width`/`height`/`top`/`left` are never written to express any state | **Passing** | `support-theater-module.test.ts` ("prefers-reduced-motion disables the opacity transition...") |
| S3.11 | Malformed data degrades gracefully | A malformed/unrecognisable event payload is ignored (never thrown); the next, well-formed item still displays normally | **Passing** | `support-theater-module.test.ts` ("a throwing/malformed event payload is ignored...") |
| S3.12 | **Corrected** — five modules registered: still exactly ONE shared transport and one rAF loop | With Support Theater registered alongside the four slice-1/2 modules, the shared `MasterCanvasConnection` opens exactly one connection and has exactly FIVE subscribers (Support Theater included, not a second, separate transport) | **Passing** | `master-canvas-integration.test.ts` ("with all five built modules registered (Support Theater included): still exactly one connection and one rAF chain — PRF-02.1 restored to cover all five, not four") |
| S3.13 | *(removed)* | The second-session misconfiguration guard this case originally covered no longer exists — there is no second session to misconfigure. See "Correction" above | — | — |
| S3.14 | The shared connection's event-payload subscription | `subscribeToEvents()` delivers a `{type:'connected'}` marker on (re)connect and each event frame's parsed payload exactly once — no duplication, no history retained | **Passing** | `master-canvas-connection.test.ts` ("subscribeToEvents receives a connected marker on (re)connect and each event frame's parsed payload exactly once") |
| S3.15 | Snapshot-only subscribers pay nothing extra | With no event-payload subscriber, a malformed data frame still delivers the plain re-read signal without disruption (payload parsing is gated behind an event-listener check, never attempted for signal-only consumers) | **Passing** | `master-canvas-connection.test.ts` ("a plain subscribe() listener pays nothing extra...") |
| S3.16 | Reconnect correctness: ack-aware cursor, never the merely-seen one | Once an event-payload subscriber exists, a reconnect never sends `last-event-id` for a cursor that was seen but not yet acknowledged — sending it would let the server skip re-sending an undisplayed delivery | **Passing** | `master-canvas-connection.test.ts` ("once an event-payload subscriber exists, reconnect uses the ack-aware cursor...") |
| S3.17 | `acknowledge()` advances the reconnect cursor | A successful `acknowledge()` call causes the NEXT reconnect to resume `last-event-id` from exactly that cursor | **Passing** | `master-canvas-connection.test.ts` ("acknowledge() success advances the reconnect cursor...") |
| S3.18 | Forced resync for a late event-subscriber | An event-payload subscriber joining a stream already running for snapshot-only reasons forces one immediate reconnect (backoff bypassed), receiving its own `connected` marker — the real work the correction required, per the coordinator's own instruction, proven directly rather than only end-to-end | **Passing** | `master-canvas-connection.test.ts` ("a late event-payload subscriber joining an already-running signal-only stream forces an IMMEDIATE reconnect...") |

**Commands run (this worktree, 2026-09-16, from `bharatstudio-alerts`):**
`pnpm --filter @bharatstudio/alerts-api build` · `pnpm --filter @bharatstudio/alerts-api test` ·
`pnpm --filter @bharatstudio/alerts-web build` · `pnpm --filter @bharatstudio/alerts-web test` ·
`pnpm contracts:validate` · `pnpm explain:check` · `pnpm db:test:all` · `pnpm db:test:l03` ·
`pnpm measurement:test` · `(cd services/alert-worker-go && go build ./... && go test -race ./... && go vet ./...)` ·
`(cd services/payment-webhook-go && go build ./... && go test -race ./... && go vet ./...)` ·
`git diff --check` — real counts recorded in `active/tasks/PRF-02.md`'s "Slice 3" section, not
repeated here.
`python3 tools/doc_consistency.py` · `python3 tools/traceability.py` — from `bharatstudio-requirements`.

## What this evidence is not

Every command above ran locally (JSDOM/Node test runner, a local
Dockerized Postgres, `go test`). None of it is OBS, Chromium, device,
network, or production evidence — §19.0's RT-07 (blocked) remains the
only row that can supply that. The JSDOM web suite proves the module's
and the connection's *logic*: the invalidation-token lifecycle, dedup,
bounded rendering, the runtime's own generic error-boundary/idempotent-
deactivate behaviour, and now the shared connection's dual-cursor
reconnect correctness — reproduced with this real production module
rather than only fakes. It proves nothing about frame timing, GPU
compositing, or behaviour inside OBS.

**The "no double-ack from the standalone page" claim is bounded, and
this is unchanged by the correction.** The Canvas and the standalone page
are separate browser sources with separate sessions by construction — the
real boundary the original scope review's race lives at — but nothing in
this Canvas's own JavaScript can detect a creator error that configures
BOTH sources with the SAME session's credentials. That gap is named in
the task record's "Referred to Opus" section, not hidden here, and is
unaffected by whether Support Theater shares its Canvas's session (the
corrected design) or has its own (the original one) — it was never a gap
the second session closed either.

## Independent Opus verification, after the correction — 2026-09-16

- `pnpm --filter @bharatstudio/alerts-web test` — **402 passed, 0 failed** (386 at slice 2;
  +11 for the module, +5 more for the ack-aware cursor and forced-resync mechanics).
- `pnpm --filter @bharatstudio/alerts-api test` — 585/0. `pnpm db:test:all` — 59/0.
  `pnpm explain:check` — 16/16. `pnpm contracts:validate` — clean. Web build clean.
  `node .github/scripts/canvas-static-check.mjs` — passes over the canvas with five modules.
  `git diff --check` clean.
- `stOverlayId` / `stToken` are gone from the URL contract. The only remaining mention is the
  dated correction comment in the host page, which attributes the original design to the
  coordinator's instruction rather than to the implementer.

**The dual cursor is correct where it matters.** `resumeCursor = eventListeners.size > 0 ?
ackCursor : rawCursor`. Once an event-payload subscriber exists, reconnect resumes from the
last **acknowledged** cursor rather than the last cursor merely *seen on the wire* — so a
delivery that arrived, was displayed, and was not yet acknowledged is replayed rather than
skipped. Resuming from `rawCursor` with Support Theater attached would silently drop a paid
alert on every reconnect, which is the worst failure this module can have.

**`resetForActivation()` survived the rework**, and it is the strongest thing in this slice.
Every pump-state field is reset unconditionally at the top of **every** `activate()`,
independent of what a prior `deactivate()` did — so the stale `active.current` stall is
**impossible by construction**, not merely tested against. That defect would have silently
stopped alerts after any routine visibility toggle or module re-enable.

### The correction, and whose error it was

The first implementation gave Support Theater a **second overlay session and a second
transport**, breaking PRF-02's central invariant — "one source, one connection, one loop",
"adding a module adds zero connections" — for the most important module on the canvas.

**That was the coordinator's instruction, not the implementer's judgement.** The instruction
read "the Canvas Support Theater module requires its own overlay session"; the intent was that
the **Canvas** must not share a session with the **standalone page**. It was implemented
faithfully as written.

The literal reading does not survive scrutiny: inside one Canvas there is exactly **one**
acknowledging consumer, because the other four modules are stateless snapshot readers that
never call `/cursor`. So a single Canvas on a single session has no acknowledgement race to
defend against, and the second session bought nothing while costing the invariant and
forcing a creator to hand-create a session and paste two tokens into one URL.

The tell was visible in the implementer's own output and was missed on first reading: the
module header had narrowed the one-transport proof to *"the four snapshot modules"*. **An
invariant being re-scoped rather than held is the signal that something is wrong with the
instruction, not with the invariant.**

The superseded sections are marked SUPERSEDED and left in place rather than deleted. A record
that quietly repairs itself stops being evidence.

### A fragility recorded rather than left implicit

Support Theater is registered **first**, so it attaches as an event subscriber before any
snapshot module can open the stream without it — keeping `forceReconnect()` a backstop rather
than the ordinary path. Both orders are tested, so a reorder degrades to an immediate resync
instead of data loss. It is still an ordering dependency, and it is named here so a future
reorder is a considered change rather than an accident.

**What this evidence is not.** JSDOM proves module logic — one transport across five modules,
one rAF loop, cursor semantics, lifecycle safety — and **nothing** about frame timing, GPU
compositing, memory across an 8-hour stream, or behaviour inside OBS. RT-07 is Blocked.
**PRF-02 remains `A`**: five of twenty modules is not a canvas.
