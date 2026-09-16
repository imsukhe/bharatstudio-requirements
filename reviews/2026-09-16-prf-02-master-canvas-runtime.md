# PRF-02 — Master Canvas runtime: decision record

**Task:** `../active/tasks/PRF-02.md`
**Reviewer:** Sukhdev Singh (owner self-review; independent reviewer unavailable)
**Scope:** Build the Master Canvas runtime (one shared transport, one
`requestAnimationFrame` scheduler, per-module error boundaries, bounded/
recycled DOM) and exactly two module renderers (Supporter Ticker, Community
Goal Ladder), plus the server-owned §30.3 module cap. This record's §1 was
written **after** the server-side half of the implementation had already
been started, on an explicit mid-task instruction from the orchestrator to
pause, write records, and complete this review before any further code —
see "When this review was actually done," below. That is stated plainly
because governance/AGENTS.md and this task's own §35.1 rule 4 require
correcting a process gap in place rather than presenting the work as if the
order had been followed from the start.

## 0. When this review was actually done, stated honestly

**This review was not performed before code was written.** The server-side
entitlement half of PRF-02 (migration `0131`, the domain/store/route files,
and their tests) was implemented first, verified locally (build/test/SQL
suite all green), and only then did the orchestrator interrupt with an
explicit instruction to stop, write the three `active/`/`tests/`/`reviews/`
records, and complete this product/market/competitor review before writing
any client-side runtime code. That is a real process-ordering fault against
this task's own §6 ("before any code"), not a hypothetical one, and it is
recorded here rather than smoothed over. No client-side runtime code exists
yet as a result — see `active/tasks/PRF-02.md`'s "Current implementation
status" section for the exact file list of what does and does not exist.
The upside of the ordering fault: nothing below required the already-
written server-side code to be reworked, because the module-cap and durable
-configuration design was already following stated authorities (§30.3,
§12.6) rather than shaped by the review's findings.

## 1. Product/market/creator review (§6 of the operator's command)

Bounded, official-documentation-only research, sources and access dates
below (all accessed 2026-09-16). This is evidence for a runtime-architecture
decision and a marketing-claim gate, not a pricing or legal recommendation.

### OBS Studio — browser sources

- **Official OBS Project docs**, [Browser Source](https://obsproject.com/kb/browser-source) — confirms Browser Source is "based on Chrome Embedded Framework" (CEF) and that CEF flags (e.g. `--enable-gpu`) can be passed via the OBS Studio shortcut. **The page states nothing about hardware-acceleration cost, GPU/CPU budget, or any guidance on how many browser sources a scene should carry.** Recorded as a genuine documentation gap, not inferred — matching RT-02's own review's honesty about OBS's own docs being sparse on delivery-mechanics detail.
- **Official OBS Project docs**, [Stream Layout Tutorial 2: Alerts & Chat Box](https://obsproject.com/kb/stream-tutorial-2-alerts) — OBS's own tutorial for adding alerts/chat notes that StreamElements-style tools "allow you to combine multiple types of widgets (alerts, chat box, etc.) into a single overlay," but does not itself mandate one browser source over several — it describes the mechanics of adding a browser source, not a performance policy.
- No official OBS Project page describing a numeric limit on browser-source count, or per-source CPU/GPU accounting, was reachable. This mirrors RT-02's own finding for OBS reconnect semantics: community sources (forum threads, third-party guides) discuss hardware-acceleration toggles, but the authoritative kb does not quantify cost. Treated as an honest gap, not filled with community evidence, per this task's "official documentation only" instruction.

### Chromium/CEF and `requestAnimationFrame` in a background or occluded source

- **MDN**, [`Window: requestAnimationFrame()`](https://developer.mozilla.org/en-US/docs/Web/API/Window/requestAnimationFrame) — *"`requestAnimationFrame()` calls are paused in most browsers when running in background tabs or hidden `<iframe>`s, in order to improve performance and battery life."*
- **Chrome for Developers blog**, [Background tabs in Chrome 57](https://developer.chrome.com/blog/background_tabs) — *"Chrome does not call `requestAnimationFrame()` when a page is in the background."* Since Chrome 11, background timers are batched to run "no more than once per second"; Chrome 57 added budget-based throttling — a page is time-budget-limited "after 10 seconds in the background," the budget regenerates "at a rate of 0.01 seconds per second," and a timer task runs "only when the time budget is non-negative." Pages playing audible audio, or holding a WebSocket/WebRTC connection, are exempt from this throttling. The post's own recommendation: chunk background work to 50ms or less and use the Page Visibility API to suspend unnecessary work when hidden.
- **Relevance to this task:** an OBS Browser Source is a CEF-hosted page, not a Chrome tab, and it is typically the *active/visible* source on the current program scene — so the "background tab" throttling case is not the normal operating condition for a canvas the creator is actively streaming. But it **is** the exact condition for a module living on a scene that is not currently the program scene (a creator with several OBS scenes, only one on air) — which is precisely why PRF-05 ("idle modules cost nothing") cannot be satisfied by CSS `display:none` alone: a hidden-but-still-mounted module could still be time-budget-throttled rather than fully stopped, and worse, a canvas relying on `requestAnimationFrame` firing to do its unsubscribe bookkeeping could have that bookkeeping itself throttled to once-per-second-or-worse on an inactive scene. This is exactly why this task's design does the unsubscribe explicitly, on a visibility/activity signal, rather than depending on the rAF loop's own cadence to notice and react — the loop being throttled is precisely when correctness matters most, not a convenience it can lean on.

### Streamlabs and StreamElements — how many browser sources do they ask a creator to add?

**This is the commercial core, so it is stated plainly rather than
summarised past the finding.**

- **StreamElements**, official docs, [`docs.streamelements.com/overlays`](https://docs.streamelements.com/overlays) — *"Overlays are the visuals layered on top of your stream — alerts, labels, goals, chat — composed in the StreamElements Overlay Editor and rendered in your broadcast software via **a single browser source**."* StreamElements's own support article, [Overlays: The Complete Guide](https://support.streamelements.com/hc/en-us/articles/10474479981074-Overlays-The-Complete-Guide-Gallery-OBS-Setup-Widgets-Alerts-Data) (fetch blocked by the site's bot protection — 403 to automated fetch, recorded honestly as RT-02's review recorded the same failure mode for other Zendesk-hosted support pages), and OBS's own tutorial (above) corroborate the same "one overlay, one browser source, multiple widgets composed inside it" model.
- **Streamlabs**, official support article, [Setting up Your Streamlabs Alerts](https://support.streamlabs.com/hc/en-us/articles/52499995174299-Setting-up-Your-Streamlabs-Alerts) — instructs the creator to **"Copy the Widget URL... and paste it as a Browser Source in your streaming program"** per widget, and separately covers using "multiple Alert Box themes by copying and pasting each theme's respective Alert Box widget URL" — i.e. **one widget, one Widget URL, one browser source**, repeated per widget type (Alert Box, Chat Box, Goal, etc.), unless the creator also uses the separate Streamlabs Desktop/OBS plugin (which manages its own set of sources internally rather than eliminating them).

**Finding that should be surfaced, not buried in the paragraph above:
StreamElements already ships a one-browser-source consolidation model today**,
via its Overlay Editor compositing multiple widget types into one overlay
asset. §6/§19.5's "one source replaces twelve" framing describes Streamlabs's
per-widget pattern accurately, but describing it as if it were true of "the
pile" generically overstates it against StreamElements specifically — a
serious competitor already does the consolidation this task is building.
**This does not invalidate PRF-02** (Master Canvas is still a real,
necessary architecture fix — see §12.7/§19.5's independent correctness
arguments: one connection, one render loop, per-module error isolation,
none of which StreamElements's marketing claims to prove server-side or
client-side, and none of which is about the OBS-source count alone). But
the *marketing* framing "one source replaces twelve" needs to be checked
against "twelve, replacing Streamlabs's per-widget pattern specifically,"
not asserted as true of every competitor — **and RT-09 already blocks
publishing any such claim until RT-07 closes**, so no marketing copy is at
risk today. Flagged under §4 below for Opus, not acted on unilaterally
(copy/marketing changes are explicitly out of this task's scope).

### Accessibility, localisation, low-end hardware, and mid-stream failure

- **`prefers-reduced-motion`** is a standard CSS media feature (already a
  stated requirement at customisation level 1 in §15.4.3, "Reduced-motion
  variant of every animation"); this task's runtime honours it structurally
  (module render functions consult it before choosing an animated vs.
  static transform/opacity transition), not as an opt-in per module. No
  external research was needed here beyond confirming the feature's
  existence and behaviour, which MDN documents as a standard, widely-
  supported CSS media query — not re-cited separately since it is
  uncontested web-platform behaviour, unlike the rAF-throttling numbers
  above which needed a primary source.
- **Indic script fallback per text role** (§15.4.3) is out of this slice's
  two modules' actual text surface (a ticker shows a viewer handle and tier
  label; the goal bar shows a title and two formatted amounts) — both
  already render whatever UTF-8 string the server sends, with no font-
  fallback-chain control added by this task. Recorded as an explicit gap:
  this slice does not implement §15.4.3's Indic-fallback-order customisation
  knob; it inherits the same system-font stack `overlay-transport.ts`'s
  existing widgets already use. Not a regression (no widget in this
  codebase implements it today), but also not closed by this task.
- **What a creator does when one module misbehaves mid-stream:** PRF-02.4's
  fail-twice-stays-down behaviour, paired with a visible note, is the
  in-canvas answer; the kill switch (existing individual widget browser
  sources, untouched by this task) is the out-of-canvas answer for a
  creator who wants to abandon the Canvas mid-stream entirely rather than
  wait out one failed module. Both are stated in the task record's
  "Failure behaviour, kill switch, rollback" section.
- **Low-end hardware:** unmeasured by this task, and unmeasurable by it —
  §19.4/RT-07 (blocked) are the only rows that can produce that evidence
  (real OBS, real low-end device, real 8-hour soak). Nothing in this
  record, and nothing this task produces, is offered as evidence toward
  those numbers.

**Evaluation against the operator's specific criteria:**

| Criterion | Finding |
|---|---|
| Switcher friction | Lowered for a Streamlabs-pattern switcher (per-widget browser sources → one); roughly neutral for a StreamElements-pattern switcher, who already has one-source consolidation, though not this task's specific correctness properties (single connection *and* single render loop *and* per-module isolation, all three at once, is not something either competitor's public docs claim) |
| Creator-visible latency | Unmeasured by this task (RT-07 gated); architecturally, one shared connection removes N-connection contention the current per-widget-page pattern (`overlay-transport.ts`, "one long-lived connection per widget instance") has today |
| Alert-loss risk on reconnect | Unchanged in kind from the existing per-widget snapshot-on-connect design (`overlay-transport.ts`), applied to a shared connection — see PRF-02.12 |
| Accessibility | `prefers-reduced-motion` honoured structurally; Indic-fallback-order not implemented by this slice (gap, stated above) |
| Localisation | No new localisation surface added or removed; inherits existing widget text rendering |
| Reliability on low-end hardware | Unmeasured, unmeasurable by this task; RT-07 remains the gate |

**Referred to Opus:** see §4 below.

## 2. Design decisions this command did not settle

1. **The module catalogue is 20 keys wide in the database from day one**,
   even though only two have a client renderer in this slice. This makes
   the §30.3 cap real for every future module rather than something
   retrofitted when module #3 ships — the alternative (a 2-key catalogue,
   widened later) would have made an early cap check meaningless (a
   Free-tier creator could never exceed a 2-module catalogue) and would
   have required a schema change later just to make the cap mean anything.
2. **Module priority/order uses creation-time ordering**, not an invented
   position/rank column — mirrors RT-02/RT-03's "configured but unset"
   posture applied to an ordering concept rather than a numeric limit: no
   authority states a module priority field, so the one timestamp that
   already exists or on every row is the tiebreak, not a new column with no
   stated meaning.
3. **A module's `enabled` toggle and its tier-cap `active` state are two
   independent, both computed-live concepts**, distinguished by
   `inactiveReason` (`'disabled'` vs `'tier_module_cap'`). This is what
   lets disabling a module free its cap slot for the next-oldest enabled
   module, live, on the very next read — proven in
   `packages/db/tests/prf02_master_canvas_module_cap.sql`.
4. **The creator-facing list/toggle routes are not in `contracts/openapi/
   v1.yaml`**, matching this codebase's own existing precedent: neither
   `POST /v1/channels/:channelId/goals` nor any of `challenges.ts`'s
   creator-facing CRUD routes are documented there either — only overlay/
   browser-source-facing reads are. Checked, not assumed, by grepping the
   existing spec before deciding.

## 3. What exists as of this record

Both halves are now implemented and locally verified — see
`active/tasks/PRF-02.md`'s "Current implementation status" section for the
complete file list and the full real-count check results (api 578/0, web
358/0, SQL suite 58/0, db:test:l03 24 files, contracts/explain/measurement/
both Go services all at their unchanged baselines, `git diff --check`
clean, requirements-repo doc checks 17/0/0).

## 4. Owner rulings on the items referred above, and their disposition

All three items referred in the version of this record written before the
client-side runtime resumed were addressed directly by the owner rather
than left open:

1. **StreamElements framing** — verified and recorded by the owner
   directly in `FULL-PRODUCT-DEFINITION.md` §6 (the "Competitive accuracy,
   checked 2026-09-16" paragraph, sourced and dated), rather than deferred
   to a future marketing gate as a note. §6's Streamlabs-specific "pile"
   framing was already correct; the addition makes the StreamElements
   exception explicit and names the real, still-RT-07-gated differentiator
   (single connection **and** single render loop **and** per-module error
   isolation together) as its own sentence. Confirmed in this worktree —
   the paragraph is present at `FULL-PRODUCT-DEFINITION.md` lines 992-999.
   **No architecture change followed**, and this task touched no marketing
   copy, consistent with its scope boundary throughout.
2. **Indic script fallback order** — ruled explicitly **out of this slice**
   by the owner (not left as an open scope question), with two binding
   constraints on the implementation: no module may hard-code a single font
   family (satisfied — see `text-rendering.ts` and both modules' use of it,
   below), and Indic fallback must be required before either module becomes
   creator-configurable (recorded as a binding precondition in the task
   record, for the next slice that adds typography controls, not
   implemented here).
3. **Resume authorized** on the original design, with one addition made
   binding rather than left implicit: PRF-02.6's idle-deactivation must be
   driven by a `visibilitychange` **signal**, never by checking
   `document.hidden` inside the frame-loop callback — because the frame
   loop is exactly what MDN/Chrome's own documentation says stops firing
   while hidden, so a check living inside it would never get to run at the
   moment it matters. Built exactly this way — see
   `master-canvas-runtime.ts`'s header comment and its dedicated test
   ("a page-hidden signal deactivates every active module... driven by the
   visibility event, not by rAF cadence").

No item remains referred and unresolved from this review.

## 5. Independent review

**Unavailable.** This is self-review by the implementing owner. No second
reviewer inspected the worktree, the diff, or the evidence in this record.
Per `governance/AGENTS.md`, this leaves the task `Conditionally complete`,
never `Verified`, and no release or launch claim follows from it.

**Disposition:** `Conditionally complete — local evidence; independent review unavailable`
**Owner:** Sukhdev Singh
**Follow-up/release gate:** an independent reviewer must inspect the actual
worktree diff against this record before any state change beyond
`Conditionally complete`. No external (staging, OBS, device, network,
provider) evidence is claimed; RT-07's separate gates are untouched by
this task, and PRF-02's full register row (all twenty catalogue modules,
plus RT-07 evidence before "one source replaces twelve" is publishable) is
**not** closed by this slice.
**Decision lifecycle:** `Approved → Implemented → Verified` (conditionally
complete pending independent review)

## Register state

**Not changed by this record.** Per this task's hard rule, no register
state letter is self-assigned here — PRF-02 remains whatever letter it
carried before this task, pending Opus's audit after the full slice
(including the client-side runtime) is complete.
