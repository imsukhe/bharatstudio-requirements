# Review — PRF-02 slice 3 implementation (Support Theater on the runtime)

**Date:** 2026-09-16
**Task:** `../active/tasks/PRF-02.md` ("Slice 3" section)
**Test record:** `../tests/TC-PRF-02-slice-3-support-theater.md`

This record points at, rather than repeats, two earlier records: the
product/market/creator/streamer scope review that split Support Theater
into its own slice and named the acknowledgement-race and stale-gate risks
(`2026-09-16-prf-02-slice-2-scope-review.md`) and the coordinator's
two-session ruling that this slice first implemented (`../active/tasks/PRF-02.md`'s
"Slice 3" section carried the full text before the correction below). This
file is the honest account of what was actually built, in the order it was
built, including the part that was wrong and had to be corrected — not
edited to read as though the corrected design was always the plan.

## Correction, 2026-09-16 — read this before everything below it

Everything from "What the scope review and the ruling established" through
"The same-session double-mount guard" describes the FIRST build of this
slice, which is now superseded. It is left in place, marked, rather than
deleted, because the coordinator's own instruction for this specific
correction was explicit: *"Update tests/TC-PRF-02-slice-3-support-theater.md
and the review record to state what changed and why, attributing the
original two-session design to my instruction rather than to your
judgement. Do not quietly rewrite it as though the one-connection design
was always the plan — a record that repairs itself stops being evidence."*

**What was wrong.** The first build gave Support Theater its own, second
overlay session and its own dedicated SSE+acknowledgement transport,
built to the coordinator's instruction as literally written ("the Canvas
Support Theater module requires its own overlay session"). The
coordinator then identified that this was a literal reading of an intent
that was narrower: the race the scope review actually found is between
the CANVAS and the SEPARATE STANDALONE PAGE — two different browser
sources, two different sessions, by construction — not between modules
inside one Canvas. Inside one Canvas there is exactly one acknowledging
consumer (Support Theater itself); the other four modules are stateless
snapshot readers that never call `/cursor`. So there was no
acknowledgement race *inside* a Canvas for a second session to defend
against, and building one cost the exact property PRF-02 exists for: one
connection, adding a module adds zero connections. The first build's own
module header even documented this cost plainly — "the Canvas has two
transports" — which in hindsight was the tell that the design was
weakening the invariant it was supposed to preserve, not defending it.

**What changed, concretely (full detail in the corrected sections' own
headers, which this paragraph only summarises):** `master-canvas-
connection.ts` was extended with `subscribeToEvents()` (delivers each
event's parsed payload once, plus a `connected` marker) and
`acknowledge()` (one-attempt `POST .../cursor`, advancing the
connection's own ack-aware reconnect cursor on success) — the ONE shared
connection now serves both the four snapshot modules and Support
Theater. `support-theater-module.ts` was rewritten to use
`connection.subscribeToEvents`/`connection.acknowledge` instead of its
own fetch loop; its `generation`-token lifecycle safety (the module's own
best property) was untouched by this — it lives in the module's state
machine, not in how events arrive. The host page
(`canvas/[overlayId]/page.tsx`) dropped the `stOverlayId`/`stToken` URL
contract entirely and now registers Support Theater with the SAME
`overlayId`/`token`/`connection` as every other module, first in
registration/entitlement order so its event-payload subscription always
attaches before a snapshot module can start the stream without one (see
"The real work: making a shared connection safe for a once-only
consumer", below, for why that ordering — and the connection's own
forced-resync backstop for when it doesn't hold — matters).

**Attribution, stated plainly per the coordinator's instruction:** the
two-session design was built to the coordinator's own instruction, and
the correction is the coordinator's own correction of that instruction,
identified and communicated by the coordinator — not a defect this
implementer found independently or a redesign this implementer judged
better. The engineering work of making the shared connection safe for a
once-only, acknowledging consumer (the dual-cursor tracking, the forced
resync) is this implementer's own, done in response to that correction.

## What the scope review and the FIRST build's ruling established (superseded design — see Correction above)

The scope review named four things the standalone page's runtime contract
could not express: per-item durable acknowledgement, an in-memory ordered
queue, a timed display-then-acknowledge state machine, and audio/TTS
orchestration — and one risk nobody had named yet: "deactivated
mid-acknowledgement" is a state the standalone page never had to handle,
because it was never a module that could be turned off. Opus's ruling,
issued on top of that review, added the binding architectural decision:
Support Theater needs its own overlay session, never the Canvas's shared
one, because acknowledgement is session-bound
(`app_private.current_overlay_session_id()`, migration 0022) and two
consumers of one session racing to acknowledge the same delivery means a
supporter's paid alert displays twice on the real broadcast.

This slice ported the standalone page's logic into
`apps/web/app/overlay/canvas/modules/support-theater-module.ts` as a
`CanvasModuleDefinition` (`activate`/`deactivate`/`render`), built its own
dedicated SSE+acknowledgement transport separate from
`MasterCanvasConnection`, and wired the host page
(`canvas/[overlayId]/page.tsx`) to require a distinct, dedicated second
session before ever registering the module.

## The central engineering decision: one `generation` counter

The task's own brief was explicit that this slice must "build one
invalidation token covering fetch, display timer and acknowledgement
retry together," naming the standalone page's three independent
`cancelled` flags (one per `useEffect`) as "how one of them gets missed."
The module has exactly one `generation` counter, incremented on every
`deactivate()`. Every await point in the acknowledgement retry loop, the
SSE read loop, the Lottie-asset fetch, and the audio fetch re-checks
`generation === myGeneration` before it is allowed to touch shared module
state or the DOM.

**The stale-`active.current` stall is impossible by construction, not
merely tested against — and here is the specific reasoning, not just the
claim.** The standalone page's "one group in flight" gate
(`active = useRef(false)`) is created once for the component's lifetime
and is never reset, which is safe only because an unmounted React
component never runs `activate()` again. This module's `activate()` CAN
be called again on the same returned object — the runtime's own
`reconcile()` (`master-canvas-runtime.ts`, unchanged by this slice)
re-activates a module whenever it regains entitlement or the page becomes
visible again after being hidden. If the pump-in-flight gate (`pumpActive`)
were reset only inside `deactivate()`, any bug in that function, or any
interleaving its author failed to anticipate, could leave it stuck `true`
forever — permanently stalling the pump on the next activation, exactly
the defect class the task's brief named by name. Instead,
`resetForActivation()` unconditionally resets every piece of pump state —
`pumpActive`, `queue`, `pendingCursors`, `currentGroup`, the display
timer, the stream abort controller — at the **top** of `activate()`
itself, before anything else runs. This means even a hypothetically
broken `deactivate()` cannot leave a stale gate behind: the next
`activate()` call clears it regardless. `support-theater-module.test.ts`'s
"deactivate() mid-acknowledgement ... then re-activate ... the pump runs"
test exercises this directly — it deactivates while an acknowledgement
POST is genuinely in flight, lets that response arrive late (proving it is
a no-op under the new generation), then re-activates the identical module
instance and proves a fresh events stream opens and the pump produces a
real render. The property is proven by construction (the reset happens
unconditionally, independent of what came before) and then proven again
by this specific test, rather than resting on either alone.

## Why Support Theater did not share `MasterCanvasConnection` (SUPERSEDED — see Correction above; it now does)

This needed its own explanation because it looks, at first read, like a
regression of PRF-02.1/S2.8's "one transport" invariant. It is not, and
the reasoning is structural rather than a convenience: every other module
in the catalogue built so far is a snapshot re-reader — the shared
connection's only job is telling a module "something may have changed, go
re-GET your own bounded endpoint," and the value it displays is always
disposable. Support Theater's delivery is the opposite: the event itself
IS the once-only payload, and acknowledging it is what prevents the server
from ever replaying it again. Sharing a "just a re-read signal" connection
across a fundamentally once-only, session-bound delivery mechanism would
either break the once-only guarantee (if acknowledgement piggybacked on
the shared connection's session) or silently reintroduce a second,
undocumented transport disguised as compliance with "one connection." So
this slice keeps the "one transport" claim true of the four snapshot
modules' shared connection specifically, and documents Support Theater's
own session stream as a second, deliberate, named exception —
`master-canvas-integration.test.ts`'s new five-modules test asserts both
halves of this in the same test: the shared connection's open-attempt
count and subscriber count are unaffected by Support Theater's
registration, and Support Theater's own stream opens exactly once.

## The same-session double-mount guard: what it caught, and why it was removed (SUPERSEDED — see Correction above)

The task's brief asked for detection "where you can detect a same-session
double-mount cheaply and safely," explicitly warning against building
anything elaborate. The FIRST build's guard was exactly one boolean
expression in the host page: Support Theater activated only when a
distinct `stOverlayId`/`stToken` pair was present in the URL hash and
that `stOverlayId` differed from the Canvas's own primary session. It
prevented a Canvas configured without ever creating a dedicated Support
Theater session from silently reusing the primary session — but that
entire risk category no longer exists once Support Theater shares the
Canvas's one session by design, so the guard (and the URL contract it
was checking) was removed along with the second session, not left behind
as dead code. The gap this guard never covered anyway — a creator pasting
the SAME session's credentials into a *separate* OBS browser source
running the standalone page — is unaffected by the correction either way,
and remains recorded below and in the task record's Referred section.

## The real work: making the shared connection safe for a once-only consumer

This is the part of the correction that mattered, not just relocating a
transport. `master-canvas-connection.ts`'s existing design was "never a
source of state, only a re-read signal" — correct for the four snapshot
modules, insufficient for Support Theater, whose delivery is once-only
and durable rather than disposable. Two problems had to be solved, not
one:

**Reconnect must never race ahead of what Support Theater has
acknowledged.** `get_overlay_events` (migrations 0022/0127, untouched)
replays anything `status in ('ready','displayed')` — eligible until
ACKNOWLEDGED, regardless of what a consumer merely saw on the wire. The
four snapshot modules never acknowledge, so tracking "last cursor seen"
for their reconnects is fine — they only ever treat any event as "go
re-fetch your own snapshot," so a reconnect re-sending something already
seen costs nothing. Support Theater cannot tolerate the opposite
direction: if reconnect ever sent a cursor AHEAD of what it has actually
acknowledged, an unacknowledged, still-undisplayed delivery could be
silently skipped by the server's own `created_at >` filter — a paid alert
that never appears again. The fix is a second cursor
(`ackCursor`, advanced only by a successful `acknowledge()` call) that
reconnect uses instead of the naive one, but ONLY once an event-payload
subscriber exists — snapshot-only Canvases are unaffected and keep the
original behaviour exactly. Proven directly, not just reasoned about:
`master-canvas-connection.test.ts`'s "once an event-payload subscriber
exists, reconnect uses the ack-aware cursor" test asserts the actual
`last-event-id` header sent is `undefined`, not the seen-but-unacked
cursor, and the companion "acknowledge() success advances the reconnect
cursor" test proves the correct cursor IS sent once one has genuinely
been acknowledged.

**A late event-subscriber must not silently miss history.** If the
stream is already running because snapshot modules started it first, and
Support Theater's event subscription attaches afterward, simply handing
it future frames would silently skip anything already unacknowledged
before it joined — the connection does not replay history to a late
subscriber on its own. `subscribeToEvents()` detects exactly this
transition and calls a new `forceReconnect()`, which resets the backoff
to its initial value and aborts the in-flight read so the very next
connect happens immediately, carrying the correct `ackCursor`. This is
proven to actually unstick a real, abort-aware stream (not just proven to
be *called*) in `master-canvas-connection.test.ts`'s own dedicated test,
using a stream stub that rejects its pending read the moment the
connection's AbortSignal fires — every other stub in that file
deliberately does not model this, so a test using one of those would not
have caught a `forceReconnect()` that only aborted without actually
retrying.

**Why this path is a backstop, not the ordinary case, in this
codebase.** `subscribeToEvents`-before-`subscribe` ordering avoids ever
needing `forceReconnect()` during normal operation. The host page
achieves this by listing `support_theater` FIRST in `BUILT_MODULE_KEYS`
and registering it before the other four, so its event-payload
subscription always attaches while the connection is not yet running —
`start()`'s own idempotency guard then means the snapshot modules'
subsequent `subscribe()` calls add nothing. This is checked, not
assumed: `master-canvas-integration.test.ts`'s five-modules test asserts
`getOpenAttemptCount() === 1` with Support Theater entitled FIRST, the
same order the host page uses, and `master-canvas-connection.test.ts`'s
forced-reconnect test proves the mechanism separately, in the ordering
that WOULD require it, so both "the backstop works" and "the backstop is
not silently firing every time" are each proven rather than only one of
them.

## A choice that cost two small duplicated functions, made explicitly

`playChime()` and `safeAudioUrl()` exist in both the standalone page and a
new file, `apps/web/app/overlay/canvas/alert-audio.ts`, rather than being
extracted from the standalone page into one shared file. The alternative
— refactoring the standalone page to import from a shared location — would
have touched the one file every earlier slice's rollback description
promised was untouched, and which remains this product's own named
mid-stream rollback path (§21.3). Fourteen lines of duplication, stated
explicitly in `alert-audio.ts`'s own header as a cost accepted rather than
an oversight, was judged the better trade against modifying the rollback
file for a task whose own scope boundary is "`apps/web/app/overlay/` is
yours exclusively" together with a standing invariant that the standalone
route is never modified by a Canvas task.

## Audit finding, corrected in place before this record was written

Two of the eleven tests in `support-theater-module.test.ts` failed on
first run, and are recorded here rather than smoothed over:

- The "audio stays synchronised" test asserted on DOM text content without
  ever calling `module.render(0)` — `render()` is gated behind a `dirty`
  flag and only the runtime (or an explicit test call) triggers it, so the
  assertion was checking pre-render DOM state. Fixed by adding the missing
  `render(0)` call before the assertion.
- The aggregate-pool test asserted `ack.pendingCount() === 1` for the
  "lead" item before ever firing its display timer (`timers.flushAll()`),
  so no acknowledgement POST had been issued yet. Fixed by flushing the
  timer first. A second issue in the same test used
  `display.maxVisibleItems: 20` in a fixture's `configSnapshot`, which
  `overlay-policy.ts`'s own `normalizeOverlayConfig` (unchanged, §12.7)
  silently clamps to its legal `[1,10]` range — the module's bound was
  correct; the test fixture asked for an out-of-range value and got the
  clamped default (1) instead, which produced too small an aggregate group
  to exercise the overflow path. Fixed by using the actual legal maximum
  (10) against the module's 8-item pool, which does exceed it.

Both were caught by actually running `pnpm --filter @bharatstudio/alerts-web
test` against this worktree before this record was written, not by
inspection — consistent with this task's own instruction not to write
records the way slice 1's implementer wrote code before its review: build,
run, find what is wrong, fix it, and say so, in that order.

## What was not built, and why

- **Moderator Status Card, backlog depth, an ETA figure.** Held
  deliveries never leave the `ready`/`displayed` filter
  (`get_overlay_events`, migrations 0022/0127, both untouched), so no data
  path for a depth number exists, and §12.7 authorises "current and next
  alert state" — not a queue depth. The scope review refused this by name
  and this slice does not re-litigate it.
- **A dashboard flow to generate a second Canvas session's URL — no
  longer applicable after the correction.** The first build's own referral
  here (a dashboard flow to generate/copy a `stOverlayId`/`stToken` URL)
  is void: there is no second session, so there is nothing for a dashboard
  flow to generate. This is not a gap that was closed by better engineering
  — it is a gap that stopped existing when the design it was attached to
  was removed.
- **Any change to the SSE route, the overlay session/auth model,
  `get_overlay_events`, the cursor endpoint, or either acknowledgement
  migration.** None of these needed to change for this slice — the module
  is a client built entirely on the existing, unmodified contract — and
  the task's hard rules forbid changing them without separate authority
  regardless.

## RT-07 and the marketing claim boundary

Unchanged from every earlier slice, restated because it is the rule most
likely to be skimmed past: everything above is local evidence (JSDOM,
Node's test runner, a local Dockerized Postgres, `go test`). None of it is
OBS, Chromium, device, network, or production evidence. §19.0's RT-07
remains Blocked, so no frame-timing, GPU-compositing, 8-hour-memory, or
"one source replaces twelve" claim is supported by this slice, and PRF-02's
register row stays open — fifteen of twenty catalogue modules remain (corrected 2026-09-16: this said *sixteen*, which does not reconcile with the five that are built — caught by the slice-4 scope review, not by any check)
unbuilt after this slice.
