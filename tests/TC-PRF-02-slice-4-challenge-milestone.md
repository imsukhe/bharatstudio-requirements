# TC-PRF-02 slice 4 — Challenge Board (current-only) and Milestone Celebration

**Task:** `../active/tasks/PRF-02.md` ("Slice 4" section)
**Owner:** Sukhdev Singh
**Status:** `Conditionally complete — local verification passed; independent review unavailable`

This record covers only slice 4: Challenge Board (§6 #8), narrowed to
current-only, and Milestone Celebration (§6 #13) as the sixth and seventh
built modules on the runtime slices 1–3 already proved. It is not, and
does not claim to be, evidence that PRF-02's full register row is done —
thirteen catalogue modules remain unbuilt, and §19.0 RT-07 (blocked) is
still the only row that can supply OBS/device/frame-timing/8-hour-memory
evidence — nothing below is that. **PRF-02 remains register letter `A`.**

| Case | Control | Expected evidence | Status | Where |
|---|---|---|---|---|
| S4.1 | Current-only Challenge Board renders correctly | Title, state label and formatted progress amounts render from the single fetched `OverlayChallenge` snapshot | **Passing** | `challenge-board-module.test.ts` ("current-only: title, state and progress render from the single fetched snapshot — no next/completed field exists anywhere in this module") |
| S4.2 | Composite-only progress (PRF-03) | Progress is expressed as `transform: scaleX()` on a fixed-size track, never `width` — corrects the standalone widget's own `width`-transition pattern | **Passing** | `challenge-board-module.test.ts` ("progress is expressed as a transform (scaleX), never as width...") |
| S4.3 | A draft challenge is never shown on stream | A `draft`-state challenge renders nothing visible, matching the standalone widget's own `isWidgetVisible` rule | **Passing** | `challenge-board-module.test.ts` ("a draft challenge renders nothing visible...") |
| S4.4 | No challenge configured degrades gracefully | `fetchSnapshot` resolving `null` renders nothing visible, never a broken/zero-progress bar | **Passing** | `challenge-board-module.test.ts` ("no challenge configured renders nothing visible") |
| S4.5 | §15.4.2 — no false refund promise, succeeded state | A `succeeded` challenge shows a plain "Succeeded!" state label; no refund/reversal/escrow/funds-held word appears anywhere in the rendered output | **Passing** | `challenge-board-module.test.ts` ("a succeeded challenge shows a plain state label and NO refund-adjacent language anywhere") |
| S4.6 | §15.4.2 — the protected copy on failure/cancellation | A `failed`/`cancelled` challenge renders `CHALLENGE_FAILURE_COPY` verbatim, and stripping that exact string from the rendered output leaves no other refund/reversal/escrow/funds-held word anywhere | **Passing** | `challenge-board-module.test.ts` (parameterised "a failed/cancelled challenge shows CHALLENGE_FAILURE_COPY verbatim, and it is the ONLY refund-adjacent text present (§15.4.2)") |
| S4.7 | §15.4.2 — the copy cannot be overridden | Passing an option the module's type does not declare (a fabricated "guaranteed refund" override) never changes the rendered copy — proven operationally, at the call site, not only by the type signature | **Passing** | `challenge-board-module.test.ts` ("the protected copy cannot be overridden — no option field exists for it...") |
| S4.8 | Cross-package copy parity, previously unchecked | The API's (`challenge-store.ts`) and the web widget's (`challenge-widget-logic.ts`) `CHALLENGE_FAILURE_COPY` are byte-identical — verified by reading the API file's source text directly (no shared import boundary between the two packages), not merely asserted by a comment as before this slice | **Passing** | `challenge-failure-copy-parity.test.ts` ("CHALLENGE_FAILURE_COPY is byte-identical between the API...and the web widget...") |
| S4.9 | The copy itself never promises a refund | `CHALLENGE_FAILURE_COPY` only ever denies holding funds/issuing a refund ("cannot issue a refund", "holds no funds"); it never contains a future-tense refund promise or a guarantee | **Passing** | `challenge-failure-copy-parity.test.ts` ("the protected copy names no false refund promise...") |
| S4.10 | Deactivate/reduced-motion hygiene, Challenge Board | `deactivate()` unsubscribes and discards a late in-flight fetch; `prefers-reduced-motion` disables the fill transition | **Passing** | `challenge-board-module.test.ts` ("deactivate unsubscribes and discards a late in-flight fetch", "prefers-reduced-motion disables the fill transition") |
| S4.11 | Milestone fires on the false→true edge of `goal.reached` | A goal snapshot transitioning `reached: false` → `reached: true` fires the celebration and renders the animated burst with the goal-reached label | **Passing** | `milestone-celebration-module.test.ts` ("fires on the false -> true edge of goal.reached, and renders the animated burst (motion allowed)") |
| S4.12 | Milestone fires on the false→true edge of the vote's `resolved` | A vote-tally snapshot transitioning `resolved: false` → `resolved: true` fires the SAME celebration path with the vote-resolved label | **Passing** | `milestone-celebration-module.test.ts` ("fires on the false -> true edge of the vote tally's resolved") |
| S4.13 | Fires on the edge only — not repeatedly while true | Once fired, further re-reads that still report `reached: true` do not refire the celebration | **Passing** | `milestone-celebration-module.test.ts` ("does NOT fire repeatedly while goal.reached stays true across multiple re-reads") |
| S4.14 | Does not fire on a reconnect/first-observation that redelivers an already-true snapshot | A module whose very first-ever observed value is already `true` (never having seen a `false`) does not celebrate | **Passing** | `milestone-celebration-module.test.ts` ("does NOT fire when the FIRST-ever observed snapshot is already true...") |
| S4.15 | `isRisingEdge` pure-function correctness, all four transitions plus both `undefined` starting cases | `undefined→true` is not an edge; `false→true` is; `true→true`, `false→false`, `true→false`, `undefined→false` are not | **Passing** | `milestone-celebration-logic.test.ts` (six cases) |
| S4.16 | Reduced motion — a genuinely static, perceivable alternative | Under `prefers-reduced-motion`, a distinct badge element becomes visible (opacity 1) with the correct label; the animated burst element never becomes visible; the badge carries no CSS `transition` at all — an instantaneous state change, not a shorter animation | **Passing** | `milestone-celebration-module.test.ts` ("prefers-reduced-motion: a distinct static badge becomes visible, the animated burst never does — not merely a shorter animation") |
| S4.17 | Composite-only (PRF-03), Milestone Celebration | Only `opacity`/`transform` are ever written on either element — `width`/`height`/`top`/`left` stay unset | **Passing** | `milestone-celebration-module.test.ts` ("composite-only: only opacity/transform are ever written on either element") |
| S4.18 | The celebration clears itself | After its visible window elapses, the celebration hides itself without further input | **Passing** | `milestone-celebration-module.test.ts` ("the celebration clears itself after its visible window...") |
| S4.19 | `deactivate()` hygiene, Milestone Celebration | Deactivating mid-celebration hides both elements immediately; a second `deactivate()` call does not throw (idempotent) | **Passing** | `milestone-celebration-module.test.ts` ("deactivate() hides an in-progress celebration immediately and is idempotent") |
| S4.20 | Not wired to a challenge (Opus's decision (c)) | `MilestoneCelebrationModuleOptions` has no field of any kind for a challenge snapshot fetcher — a compile-time check that fails to build if one is ever added | **Passing** | `milestone-celebration-module.test.ts` ("does not fire on a challenge reaching target — this module has no challenge fetcher of any kind") |
| S4.21 | Malformed data degrades gracefully, Milestone Celebration | A malformed goal/vote payload (fails the shared `isOverlayGoal`/`isTugOfWarVoteTally` guards) is ignored — never thrown, never treated as a rising edge | **Passing** | `milestone-celebration-module.test.ts` ("a malformed goal/vote payload is ignored, never thrown, and never treated as a rising edge") |
| S4.22 | Seven modules registered: exactly one transport, one rAF loop | With all seven built modules (Support Theater, Supporter Ticker, Community Goal Ladder, Tug-of-War Vote, Boss Fight, Challenge Board, Milestone Celebration) entitled together, the shared `MasterCanvasConnection` opens exactly one connection with seven subscribers, and the manual frame scheduler holds exactly one pending frame handle | **Passing** | `master-canvas-integration.test.ts` ("with all seven modules registered (Challenge Board + Milestone Celebration included): still exactly one connection and one rAF chain") |
| S4.23 | PRF-03 static discipline, both new files | `render()` in both new modules writes only `opacity`/`transform` — verified by the same static scanner every prior slice's modules pass | **Passing** | `node .github/scripts/canvas-static-check.mjs` — 16 canvas source files scanned, zero violations |

**Commands run (this worktree, 2026-09-16, from `bharatstudio-alerts`):**
`pnpm --filter @bharatstudio/alerts-api build` · `pnpm --filter @bharatstudio/alerts-api test` ·
`pnpm --filter @bharatstudio/alerts-web build` · `pnpm --filter @bharatstudio/alerts-web test` ·
`pnpm contracts:validate` · `pnpm explain:check` · `pnpm db:test:all` · `pnpm db:test:l03` ·
`pnpm measurement:test` · `(cd services/alert-worker-go && go build ./... && go test -race ./... && go vet ./...)` ·
`(cd services/payment-webhook-go && go build ./... && go test -race ./... && go vet ./...)` ·
`node .github/scripts/canvas-static-check.mjs` · `git diff --check` — real counts recorded in
`active/tasks/PRF-02.md`'s "Slice 4" section, not repeated here.
`python3 tools/doc_consistency.py` · `python3 tools/traceability.py` — from `bharatstudio-requirements`.

## What this evidence is not

Every command above ran locally (JSDOM/Node test runner, a local
Dockerized Postgres, `go test`). None of it is OBS, Chromium, device,
network, or production evidence — §19.0's RT-07 (blocked) remains the
only row that can supply that. The JSDOM web suite proves both new
modules' *logic*: current-only rendering, the protected-copy honesty
rules, the rising-edge detection rule, the reduced-motion static
alternative, lifecycle safety, and the runtime's own generic
error-boundary/idempotent-deactivate behaviour — reproduced with real
production modules alongside the five already built, not only in
isolation. It proves nothing about frame timing, GPU compositing, or
behaviour inside OBS.

**Two scope narrowings are recorded here, not silently absorbed:**
"current / next / completed" (§6) is current-only this slice, and
Milestone Celebration does not fire on a challenge. Both are Opus's own
decisions, carried in `active/tasks/PRF-02.md`'s Slice 4 section — this
record does not restate the reasoning, only confirms the built behaviour
matches the decision (S4.1, S4.20).

**PRF-02 remains `A`**: seven of twenty modules is not a canvas.

## Independent Opus verification — 2026-09-16

- `pnpm --filter @bharatstudio/alerts-web test` — **431 passed, 0 failed** (baseline 402).
- `pnpm --filter @bharatstudio/alerts-api test` — 590/0 (585 baseline; +5 is the concurrent
  instrumentation agent's work, not this slice's).
- `node .github/scripts/canvas-static-check.mjs` — passes across 16 files, zero PRF-03
  violations, now covering seven modules.
- `python3 tools/doc_consistency.py` — 17 checks, 0 errors, 0 warnings.

### The refund-copy guard was negative-tested, because a comment is not a check

`CHALLENGE_FAILURE_COPY`'s "byte-identical in two places" claim had been **only a comment**.
The two copies live in different packages with no shared import, so they could have diverged
silently — and the string is the one the product's honesty rests on: *"BharatStudio holds no
funds and cannot issue a refund."*

The new `challenge-failure-copy-parity.test.ts` reads the API file's source text directly
across the package boundary and asserts byte equality. **Opus verified it by breaking it:**
changing the API copy to "BharatStudio will refund you shortly" failed exactly **1 test**;
restored, 431/0, and `git status` confirms the file is clean. It also carries a useful failure
message for the case where the declaration's *shape* changes rather than its text.

Non-overridability is proven operationally rather than asserted: the Canvas module imports
the existing constant instead of declaring a third copy, its options type has no override
field, and a test passes a fabricated "guaranteed refund" option and asserts the rendered copy
is unchanged.

### Two implementation choices worth keeping

**`isRisingEdge` starts `previous` as `undefined`, not `false`.** That single rule satisfies
both requirements at once — it fires on a genuine false→true edge, and it does **not** fire on
a reconnect that re-delivers an already-true snapshot. Initialising to `false` would have
celebrated every reconnect of an already-completed goal.

**The reduced-motion alternative is a separate badge element with no CSS `transition` at all** —
an instantaneous state change with distinct colour, border and text. Not the burst animation
replayed faster, which would have been the easy and useless answer.

### Recorded rather than smoothed over

The implementer noted that no standalone scope-review file existed for this slice, unlike
slices 2 and 3 — the findings had arrived only inside the coordinator's command. It flagged
the gap instead of writing around it. `reviews/2026-09-16-prf-02-slice-4-scope-review.md` now
records those findings retrospectively, labelled as retrospective.

**What this evidence is not.** JSDOM proves logic — seven modules on one transport, one rAF
loop, edge semantics, copy parity — and **nothing** about frame timing, GPU compositing,
8-hour memory or OBS. RT-07 is Blocked. **PRF-02 remains `A`**: seven of twenty modules is not
a canvas, and §6's Challenge Board is not fully shipped — only its current-challenge half.
