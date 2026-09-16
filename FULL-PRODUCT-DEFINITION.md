# BharatStudio — Full Product Definition

**Version 1.1 · 2026-09-14**

| | |
|---|---|
| **Status** | `Proposed — product authority for direction and content. NOT a release authority.` |
| **Owner** | Project owner |
| **Authorises** | What the product is, what each capability means, which tier and phase it belongs to, and what must never be built |
| **Does not authorise** | Any public claim, any release, any payment-routing work, or any spend of build time on a post-v1 slice |
| **Superseded by, on any conflict** | `active/launch/00_LAUNCH_SCOPE_AUTHORITY.md` · `active/launch/01_MASTER_RELEASE_AUTHORITY.md` · `active/launch/05_SUPPORT_AND_EXTERNAL_EVIDENCE_REGISTER.md` |
| **Supersedes** | Master plan Part 7, **on product content and capability status only** — not on release scope |

This is the whole product in one file: what exists, what is broken, what is missing,
what we are building, and what we deliberately will not build. Nothing is deferred out
of this document. Items that cannot be built today appear in §32 with the exact
condition that unblocks them, not as silent omissions.

**"Nothing is deferred" is a statement about the document, not about v1.** Everything
described here is written down so it is not lost. Almost none of it is in v1. §1.9 is
the phase boundary and it is binding; a capability's presence in this file is never
permission to build it now.

---

## 0. How to read this

Three vocabularies are used throughout and they mean different things.

| Term | Meaning |
|---|---|
| **USABLE** | A person can trigger it and see the result |
| **UNREACHABLE** | Code exists, is tested, is committed — and no human can reach it |
| **ABSENT** | Not built |
| **BLOCKED** | Cannot be built until a named external condition is met |

**UNREACHABLE is the category that matters.** Every prior status review asked "does
this code exist?" and answered yes. 496 + 324 + 97 passing tests coexist with a
product where a creator cannot connect YouTube, cannot start hype mode, cannot send a
sticker, and whose entire supporter-history feature returns empty on every read. Tests
seed their own data and call functions directly; they never traverse the path a user
takes. **A green suite is not evidence of a working product.**

---

## 1. The thesis

**BharatStudio is a Creator Command Center, not a mobile remote for OBS.**

> Before, during, and after a stream, BharatStudio is the one app a creator opens.
> YouTube, OBS, payments, overlays, moderation, sponsors, and supporter engagement are
> controlled from one place.

It does not replace YouTube's protected checkout, YouTube Studio, or the local OBS
process. It is the **safe control plane that coordinates them**.

### Scope — decided 2026-09-13

**In scope, and nothing else:** BharatStudio **Alerts** · the **creator dashboard** ·
the **overlay / Master Canvas** · the **Live Support Hub** (donation page) ·
**Companion** for **iOS and Android only**.

**Out of scope for this document and this roadmap:** Mirror (`stream-mac`,
`stream-windows`) · Stream (`stream-ios`, `stream-android`) · desktop Companion as a
product surface · any other BharatStudio product. Those repos continue to exist; they
are not planned, prioritised or reported here.

Consequences, recorded so nobody re-derives them later:

- The Companion action catalogue's **mirror** and **stream** groups (5 of 17 actions)
  are out of product scope. Leave the enum values — removing them is a migration for
  no benefit — but build no UI, and do not count them as gaps.
- A **desktop helper may still exist as a mechanism** where OBS control genuinely
  requires a local process. It is plumbing for the mobile app, not a surface we design,
  document or ship features to.
- Cross-product identity (Platform), store entitlements and licence keys leave this
  roadmap entirely.

Three properties define the product and none of them are negotiable:

1. **One source, one app, one deck.** One Master Canvas browser source replaces the
   pile of Streamlabs/StreamElements sources. One phone app runs the stream.
   *Aspiration, not present tense: Master Canvas is not built (PRF-02) and today each
   widget is a separate source. Not publishable until it ships and RT-01..RT-07 close.*
2. **Everything agrees on what happened.** UPI tips, YouTube events, overlay state and
   moderation decisions reconcile to one truth.
3. **Failure is legible and partial.** If YouTube chat dies, tips and overlay keep
   working, and the creator is told exactly which part failed.

### 1.9 Release phasing — binding, and stricter than this document

The launch authority is narrower than this document and it wins. Recorded here so
nobody reads a section of this file as a licence to start.

**v1 — the only thing anybody may build toward a release.** Frozen to
`00_LAUNCH_SCOPE_AUTHORITY.md`: Alerts tip page · creator dashboard · overlay and
Master Canvas · durable queues, moderation and history · Companion (iOS/Android and
the web console) · **creator-direct Razorpay only**. Nothing else is a launch feature
and nothing else may be described as one.

**Explicitly not v1**, restated from the launch authority so it cannot be lost:
YouTube data/live ingestion, Super Chat, memberships and catch-up summaries · every
Enterprise capability · client-owned entitlement decisions · public desktop APIs ·
client-facing gRPC · **in-app checkout in Companion** (see §5.6.1).

**Phase labels used throughout this document.** Every row in the §31 register carries one
**as a column**, added 2026-09-14 — `tools/assign_phases.py` records the rules each value
was derived from, and `tools/doc_consistency.py` fails the build on a missing or invalid
phase, or on an R or N row scheduled in a §34 build phase. Before that column existed the
build/research boundary was unenforceable, because §1.9 described labels the register did
not carry.

| Label | Meaning |
|---|---|
| **v1** | In the frozen launch scope above |
| **P2** | Post-v1, product-ready, needs only build time |
| **P3** | Post-v1, needs a product or pricing decision first |
| **·G** (suffix) | **Release-gated.** Implementation proceeds now; **release** waits on named external evidence. This is the normal state for most of v1 — Razorpay is a provider dependency, the store declarations are a store dependency, the tax position needs a CA. Build it, do not launch it, and never claim the evidence exists |
| **R** | **Research only.** No implementation, no schema, no UI, no marketing, at all. Needs written external evidence before it can become P2/P3 |
| **N** | Never |

**G and R are different states and conflating them breaks v1.** An earlier version of
this table said any provider or legal dependency becomes phase R, which would have made
the Razorpay path itself unbuildable. The test: *can we build this correctly today and
decide later whether to turn it on?* If yes it is **·G**, carried as a suffix on its scope phase — `v1·G`, `P2·G`. If building it at all requires
someone outside to say yes first — because it would mean holding a credential we are not
permitted to hold, distributing goods we cannot yet account for, or shipping a surface a
provider has not approved — it is **R**.

Currently **R**: delegated payment routes (§25) · third-party package marketplace
(§9.7) · StreamElements event bridge · Enterprise (§24).
Currently **·G**: creator-direct Razorpay · app-store submission · anything touching the
tax, privacy or terms rows in `05_SUPPORT_AND_EXTERNAL_EVIDENCE_REGISTER.md`.

**Post-v1 slices, in labelled order.** YouTube depth (P2) · AI credits and top-ups (P2)
· interop: Canvas Packages, asset import and the migration wizard (P2, §9) ·
BharatStudio Bot (P2, §36, and additionally blocked on the chat-write scope) · Lobby
Engine and tournaments (P3) · Social Relay (P3) · packs and creator jobs (P3) ·
outbound bridges (P3, §9.6) · payment Compatibility Routing (**R**) · third-party
package marketplace (**R**, §9.7) · StreamElements event bridge (**R**) · Enterprise
(**R**, and additionally blocked on §32).

**The evidence rule, which this document does not get to relax.** A local test, a
passing suite, a document review, or a section of this file is never launch evidence.
Only the dated external evidence named in `05_SUPPORT_AND_EXTERNAL_EVIDENCE_REGISTER.md`
— provider, tax, privacy, legal, app-store, staging, security, migration, outage and
operational — moves a row out of `Open`. All four critical external filings were
**unfiled as of 2026-09-07**.

### What would make a serious creator switch

1. "Import my OBS setup safely; nothing breaks."
2. "One source, one app, one phone control deck."
3. "My UPI tips, YouTube events, overlays, and moderation agree on what happened."
4. "I can go live without opening five tabs."
5. "If YouTube or chat fails, my stream and payment flow still work."
6. "I can enter Clutch Mode instantly and not lose queued support."
7. "I can prove sponsor exposure and reconcile earnings later."
8. "I can leave BharatStudio with my layouts, events, receipts, and exports."

Point 8 is a feature, not a concession. Portability is why a cautious creator tries us.

---

## 2. Current reality — the reachability truth

### 2.1 The root cause: one missing write

`0084:109` adds `payments.viewer_identity_id` as nullable with no backfill. The only
`payments` INSERT — `record_verified_payment_webhook` (`0007`) — **does not list the
column**. Nothing anywhere sets it. It is NULL on every row ever written.

Readers filter `viewer_identity_id is not null` (`0105:981`, `0108:401`), so they
return empty rather than erroring:

| Downstream | State |
|---|---|
| `creator_supporter_relations` (`0084:94`) | never populated — no writer at all |
| Streaks, badges (`0107`) | always zero |
| Reputation score and verdict (`0120`) | always `clear` |
| Supporter history | `get_channel_supporter_history` has no route either |

**The entire viewer-history product is correct, tested, and permanently blank.**
Fixing this one write is the highest-leverage change in the codebase.

### 2.2 Unreachable — built, tested, committed, reachable by nobody

**Connectors — the whole YouTube feature cannot be switched on**

| Gap | Missing piece |
|---|---|
| YouTube OAuth connect | no page calls `POST /v1/channels/:id/connectors/youtube/connect` |
| YouTube disconnect | no page calls the DELETE route |
| Revoked-auth prompt | poller never sets `status='revoked'` on `invalid_grant`; nothing surfaces it |

`/dashboard/sources` is contribution-source toggles only. Poller, quota budget,
`streamList`, Super Chat, `!tip` and bot ack are all real, tested — and unreachable.

**Engagement — the interaction layer has no viewer surface.** `TipForm.tsx` sends an
amount, a name and a message. Nothing else.

| Gap | Missing piece |
|---|---|
| Interaction menu (viewer picker) | component does not exist |
| Support votes (free) | no creator UI calls `createVoteOption`; no viewer UI casts |
| Paid support votes | TipForm never sends `interactionDefinitionId`/`voteOptionKey` |
| Mega alert, priority question | no payment path can tag an interaction definition |
| **Sticker / GIF selection** | TipForm has zero sticker code — `stickers.ts:124` comments claim a tip-page picker that does not exist |
| Hype mode | `startHypeMode` defined in the API client, **zero callers** — can never start |
| Widget privacy scope | no UI calls `update_widget_config`; stuck `private` forever |
| Staff creator-pack review (`0122`) | API-only, no admin page |
| Template catalogue | GET route exists, no frontend calls it |
| Challenge source-inclusion | route exists; `ChallengesPanel` never wires it |

**Payments and ops**

| Gap | Missing piece |
|---|---|
| **All six cron schedules** | `bharatstudio-crons/schedules/v1.json` `"enabled": false` on every entry, including `outbox-recovery` (the delivery pump) |
| Payment account activation | `activate_creator_payment_account` zero non-test callers; accounts stay `pending` (`0060:111-112`) |
| Manual-review quarantine | `resolve_reconciliation_manual_review` zero callers — fills, never drains |
| Featured-creator curation | read function only; nothing sets the flag |
| Provider capability snapshot | written every check, read by nothing |
| Preferred UPI app memory | server allowlist only; browser half absent |
| Razorpay partner OAuth | `app.ts:268` passes `undefined` — route 503s everywhere |

**Viewer identity**

Platform-identity claim route (no caller) · badges/streaks route (no caller) · receipt
minting `POST /v1/public/receipts` (no caller, so `/r/[token]` is dead and anonymous
tips have no claim path) · `record_reputation_signal` (zero non-test callers — no
chargeback hook, no velocity or moderation-strike producer) · reputation display (no
UI) · anonymous browser identity (zero inserts).

**Companion — the mobile app's controls are not connected**

`CompanionShell` declares `onAction`, `onRunFullTest`, `onMuteTts`, `onCancelTts`,
`onModerate`. `App.tsx:143-165` passes **none of them**. Every OBS action, the
run-full-test button, mute/cancel TTS and approve/reject **render and do nothing**.
Props are optional so TypeScript is silent; tests inject their own handlers so 97/97
passes. Moderator seat management has zero callers on any surface despite `0104`
enforcing the limits.

### 2.3 Falsely marked DONE in the old plan

Custom sound upload (zero `sound` hits repo-wide) · built-in themes (zero `theme`
hits) · 72-hour replay buffer (replay is cursor-based, no time bound).

**Corrected on further reading:** Part 7's "Action/layout page-size entitlement
(8/16/32/64)" is a *mislabel*, not a fabrication. L07 specifies layout **slot**
allocations of 8/16/32/64 per tier and **page sizes** of 4/8/16. Both numbers are
real; the register attached the slot ladder to the wrong noun. An earlier review of
mine called the row false — it is wrong about the label only.

### 2.4 What genuinely works — protect this

Tip page and payment capture end to end · webhook verification, dedup, and a single
atomic transaction (delivery + payments + intent + alert_events + outbox) ·
multi-account attribution guard · payments ledger and CSV export · refund tracking
with derive-don't-store proven in two independent read paths · alert queues,
bindings, modes, quiet hours, rate controls · SSE overlay with cursor replay and
cross-replica fan-out · overlay token design (fragment-only, sha256 stored,
per-overlay lookup, revoke/rotate) · moderation approve/hold/suppress/replay with
audit and a correct lease-and-CAS that makes the suspected suppress race impossible
(`0004:29-42`, `0030:40`) · TTS synthesis, cache, quota metering, amount ladder,
chime and browser fallbacks · support goals · overlay widget reads · Super Chat →
goals aggregation (`0117:433`) · creator-published challenges with honest on-stream
failure disclosure · sticker catalogue and creator packs (creator side) · AI assist
with audit · admin DLQ console · entitlement management · email outbox · viewer
accounts, login, password reset, DPDP deletion, opt-in profiles and search.

**The architecture is sound. Almost everything broken is a connection nobody made.**

---

## 3. Foundation repairs — P0, before any new feature

These are not features. They are the difference between a demo and a product.

| ID | Repair | Why first |
|---|---|---|
| F01 | Write `payments.viewer_identity_id` in the capture path | Unlocks supporter relations, streaks, badges, reputation, history in one change |
| F02 | Backfill strategy for existing NULL rows | Decide: leave historical NULL, or match by receipt/provider identity |
| F03 | Populate `creator_supporter_relations` on capture | Second half of F01 |
| F04 | Mint receipts from the tip confirmation page | Makes `/r/[token]` live and gives anonymous tips a claim path |
| F05 | TTS content safety (see §12.2) | Only item with real-world harm potential |
| F06 | YouTube connect / disconnect / reconnect UI | **Moved to Phase 4, 2026-09-14.** It makes a built subsystem reachable, but YouTube is excluded from v1 by the launch authority and building its connect surface in Phase 0 is scope drift. It stays a recorded defect, fixed when YouTube work starts |
| F07 | Set `status='revoked'` on `invalid_grant` + surface it | **Moved to Phase 4** with F06, for the same reason — it is YouTube connector behaviour |
| F08 | Wire mobile Companion handlers in `App.tsx` | Every control currently inert |
| F09 | TipForm as the interaction surface | Unblocks stickers, paid votes, mega alert, priority question together |
| F10 | Enable cron schedules (needs L06 IAM/staging evidence) | Reconciliation and delivery pump do not run |
| F11 | Call `activate_creator_payment_account` | Accounts never leave `pending` |
| F12 | Admin UI for reconciliation quarantine | Queue fills, never drains |
| F13 | Wire Razorpay partner OAuth config in `app.ts`/`index.ts` | Route 503s everywhere |
| F14 | Hype mode Start control | `startHypeMode` has zero callers |
| F15 | Widget privacy-scope control | All widgets stuck `private` |
| F16 | Featured-creator curation writer | List can never change |
| F17 | Staff creator-pack review admin page | Studio uploads unreviewable |
| F18 | Moderator seat management UI | Enforced in DB, unmanageable in product |
| F19 | Template catalogue frontend | GET route with no caller |
| F20 | Challenge source-inclusion in `ChallengesPanel` | Route exists, unwired |
| F21 | Activation instrumentation (payout + OBS + first alert) | The core funnel question is unanswerable |
| F22 | Reachability CI checks (see §17) | Stops this class recurring |

**F22 is the one that prevents repetition:** flag exported API-client functions with
zero callers, SQL functions granted to an app role with no application caller,
declared-but-never-passed React handler props, and add one real end-to-end smoke path
per surface.

---

## 4. Platform reality checks

Verified constraints. Design against these, not against optimism.

| Idea | Verdict | Constraint |
|---|---|---|
| **Like goals** | Viable | `videos.list` costs 1 quota unit. Live polling cadence must be measured against real quota before shipping, not assumed. |
| **Member reconciliation** | Viable | `members.list` needs the sensitive membership scope, creator authorization and access eligibility; supports `updates` mode; 2 units per call. **Never treat chat events as financial or member truth** — reconcile against the API. |
| **Assisted gifting** | Reminder/deep-link only | YouTube's flow requires the user to open a live stream, choose gifting, select quantity and complete the transaction. **BharatStudio must never automate a membership purchase or card confirmation.** |
| **One-tap go live** | Guarded workflow only | Create/bind broadcast → verify YouTube sees ingest as `active` → transition to `testing` → `live`. Transitioning because OBS says "connected" produces bad streams. |
| **Google Sheets export** | Batch/delta only | Per-minute quotas; needs retry and backoff. Never one request per tip. |
| **Chat write / moderation** | Supported, gated | Needs scoped OAuth, rate limiting, audit trail, and a clear fallback when YouTube rejects or disables chat operations. |
| **BYOK / InnerTube** | Ruled out | Verified ToS violations; InnerTube additionally has no contract, unverifiable financial provenance, and a client-POST fraud vector. |

### 4.1 YouTube quota is ours, not the creator's — corrected 2026-09-14

A working assumption surfaced that each creator brings their own YouTube API quota. **They
do not, and the design must not depend on it.**

- **Quota is allocated per Google Cloud project**, not per authorising user. Every creator
  who connects spends **our** project's daily allowance. A creator's OAuth grant conveys
  permission to act on their data; it conveys no quota.
- The default allowance for a new project is **10,000 units per day, shared across every
  creator on it**. It does not scale with signups.
- There is no supported way to attribute usage to a creator's own allowance. Per-creator
  projects are not a workable structure, and creator-supplied keys / InnerTube are already
  **ruled out** in the table above as ToS violations.

Why that matters concretely: a poll costing a handful of units, run every few seconds for
a four-hour stream, consumes a large share of a 10,000-unit day **for one creator**.
Several creators live at once exhausts it outright, and the failure is not graceful —
calls start returning quota errors and the connector goes dark mid-stream.

So three things follow, none of them optional:

1. **A quota increase must be granted before YouTube ships at any scale.** It is an
   application with an audit, and it is a lead-time item even though YouTube itself is
   Phase 4.
2. **Every per-call unit cost in this document needs the §27.2 treatment** — a dated
   official source, because these figures change and ours are currently unverified.
   `L15` records that the poller's switch to `streamList` has **never been measured
   against a real Google project**, which is exactly the gap.
3. **Polling cadence is a quota budget, not a latency preference.** Cadence, creator
   count and the daily allowance are one equation, and the connector needs a measured
   per-creator cost, a project-wide budget, and a defined degradation path when the
   budget is spent — reduce cadence, then pause, always with a creator-visible reason,
   never a silent stop.

### 4.2 One fetch, many surfaces — the rule that makes the quota affordable

**Quota is consumed per API call, never per person looking at the result.** That single
fact decides the architecture, and it is worth more than any clever sourcing trick:

> **No surface ever calls YouTube. The server fetches once per channel and fans the
> result out over the existing channel-keyed SSE path (RT-02).**

Overlay, dashboard, Companion and the tip page all read the same fanned-out value. Twelve
widgets showing the like count cost what one costs. A creator with the dashboard open and
the overlay live costs what one costs. This is the same rule as §12.7 — surfaces receive
projections, they do not fetch — applied to an external provider instead of our database.

#### 4.2.1 What each surface may use

| Need | Overlay (OBS browser source) | Dashboard | Quota |
|---|---|---|---|
| Tips, alerts, goals, supporters, moderation — everything BharatStudio-native | Our SSE | Our API | **None** |
| Viewer count, like count | Fanned out from the server's single poll | Same fanned-out value | 1 unit per poll **per channel**, not per surface |
| Playback and presence ("are we live", player state) | **IFrame Player API** — client-side, official, free | Same | **None** |
| A creator reading their own live chat | Not on the overlay — chat display belongs in the dashboard and Companion | **YouTube's official live-chat embed** | **None** |
| Chat as *data* — commands, `!tip`, bot replies, moderation actions | Never | Server-side ingestion only | **The expensive one.** Phase 4, gated on the quota grant |
| Super Chat, memberships, gifting | Never | Server-side API, reconciled | Metered, and never taken from a chat display |
| Stream health — bitrate, dropped frames, scene, sources | Desktop helper / OBS WebSocket | Same | **None — this never touches Google at all** |
| Broadcast lifecycle — title, thumbnail, go live, end | — | Server-side API, per action | Per action, not polling |

Two things fall out of that table and both are worth stating plainly:

- **A large part of "is my stream healthy" never involves YouTube.** Bitrate, dropped
  frames, scene state and source visibility come from the local helper. We should not
  spend a single unit discovering something OBS already knows.
- **Displaying chat and ingesting chat are different products.** A creator who wants to
  *see* chat while operating gets the official embed for free. Ingestion is only needed
  for commands, the bot and moderation — and that is the one place the cost is real.

#### 4.2.2 Cadence is a budget

Poll **only while live**. Back off when nothing changes. Tier the cadence by creator size
rather than giving everyone the fastest setting. Define the degradation path before the
ceiling is reached: slow down, then pause, always with a creator-visible reason, never a
silent stop.

Worked example, with the figures marked as needing §27.2 sources: `videos.list` at a
documented 1 unit, polled every 60 seconds across a four-hour stream, is **240 units per
creator-stream** — roughly 40 creator-streams inside the free 10,000/day allowance before
any increase. Most quota anxiety comes from assuming a 5-second cadence nobody asked for.

### 4.3 `liveChatMessages.streamList` and the quota-increase track

**The structural claim is sound and the numbers are not ours yet.** `streamList` is
documented as a streaming variant of the chat-list call: instead of asking repeatedly
whether new messages exist, the client holds a long-lived connection and messages arrive
as they appear. Fewer calls for the same coverage. Our poller already uses it — L15
records the switch — and L15 also records that **its wire framing and its real quota cost
have never been measured against a live Google project**.

So the honest position: `streamList` is very likely the right mechanism and is why chat
ingestion may be affordable at all, and **we cannot yet say how many concurrent creators
it supports before the 10,000 ceiling**. Neither the optimistic nor the pessimistic answer
is currently evidence.

#### 4.3.1 The measurement, which is also the quota application

These are one piece of work, not two, and it runs **in parallel with the build**:

1. **Instrument quota consumption from the first call.** A per-call, per-endpoint,
   per-channel counter, exported as a histogram like every other budgeted path (RT-06).
   Without this we will be applying for an increase with a guess, which is the weakest
   possible application.
2. **Measure `streamList` against a real project** on one real multi-hour stream: units
   consumed per hour, per channel, per message volume, and how the cost behaves during a
   chat burst.
3. **Derive the ceiling honestly** — concurrent creators supported at the free allowance,
   and at each increase tier we might request.
4. **Then apply**, with measured numbers, the described use case, the scopes, and a
   working product to demonstrate. A quota audit asks for the app, not the plan.

**Sequenced deliberately:** the owner decision of 2026-09-14 files external gates after
the build works, and this fits it — but the *instrumentation* is not an external gate and
ships with the connector, or the application arrives with nothing behind it. Steps 1 and 2
are engineering work in Phase 4; steps 3 and 4 are the filing.

### 4.4 Demand-driven fetching — nothing is polled because it exists

§4.2 removed per-surface calls. This removes calls nobody is waiting for. Together they
are what makes the free allowance workable, and neither needs a single line of the
scraping approach.

> **A YouTube call happens only while a human is looking at something that needs it.**

#### 4.4.1 Subscription with reference counting

Every surface that needs a YouTube-derived value **subscribes** to a
`(channel, datum)` pair rather than triggering a fetch. Datums are things like
`broadcast_state`, `viewer_count`, `like_count`, `chat_stream`.

- The server polls a datum **only while its reference count is above zero**.
- Ten widgets wanting `like_count` on one channel is **one subscription, refcount 10**.
- A hidden module, an inactive OBS scene, a closed dashboard tab or a backgrounded
  Companion **unsubscribes**. `document.visibilityState` drives it; a background tab
  drops to a slow cadence rather than holding the fast one.
- **Hysteresis before unsubscribing** — a grace window of roughly a minute — so a
  creator flicking between scenes does not thrash the subscription.
- A creator whose overlay shows no YouTube-derived widget costs **zero YouTube quota**,
  all day, even while live.

**This is the same registry as RT-02.** The channel-keyed subscriber map being built for
the SSE fanout is the map that drives upstream demand. One registry, not two — a
subscriber count that already exists for delivery becomes the input that decides whether
to fetch at all.

#### 4.4.2 Batch across channels, and across fields

Two multipliers, and the first is the largest single lever in this section:

- **Many channels per call.** `videos.list` accepts a batch of video IDs in one request.
  One global poller collects every channel with an active subscription, chunks them, and
  issues one call per chunk instead of one per channel.
- **Many fields per call.** Ask for the parts needed together — live details and
  statistics in the same request — rather than two calls for one screen.

Worked arithmetic, with the per-call figures flagged for §27.2 sourcing: at a documented
1 unit per `videos.list` and a batch of 50 IDs, **200 concurrently live channels cost
4 units per tick**. At a 60-second cadence that is 240 units per hour, well inside the
free 10,000-unit day even at continuous full load.

The naive design — one call per channel per tick — costs 200 units per tick and exhausts
the same allowance in under an hour. **Same data, same freshness, fifty-fold difference.**

#### 4.4.3 Lazy behind an explicit action, especially on the tip page

The tip page server-renders creator identity, presets and the payment form and **nothing
else** (§12.7). Everything live is click-to-load:

| Control | What happens on click | Quota |
|---|---|---|
| **Watch live** | Mounts the IFrame player | **None** |
| **Open live chat** | Mounts YouTube's official chat embed | **None** |
| A live-state badge, if the creator enables one | Subscribes to `broadcast_state` while the page has a visitor, unsubscribes after an idle timeout | Shared across every visitor to that page |

So a tip page with a thousand visitors costs the same as one with a single visitor, and a
tip page with no visitors costs nothing. **Traffic never multiplies quota** — only
distinct channels and distinct datums do.

#### 4.4.4 Chat is subscribed by feature, not by liveness

Chat ingestion is a long-lived connection per channel and cannot be batched, which makes
it the one genuinely expensive datum. So it is **not** subscribed merely because a stream
is live:

- Subscribed when a chat-dependent feature is actually in use — the bot is enabled,
  commands are configured, a moderator has the queue open, or `!tip` is switched on.
- Unsubscribed the moment none of those is true.
- A creator who uses BharatStudio purely for tips and overlays **never opens a chat
  connection at all**.

#### 4.4.5 The budget manager

One component owns the daily allowance and behaves like a scheduler, not a counter:

- **Priority by datum.** `broadcast_state` outranks `viewer_count`, which outranks
  `like_count`. Under pressure, the cheap truthful signal survives and the decorative one
  degrades.
- **Global degradation, not per-creator starvation.** When the budget tightens, every
  cadence slows together. We never silently stop serving one creator so another keeps a
  fast counter.
- **Visible degradation.** A slowed or paused datum says so in the dashboard and on the
  affected widget. Never a stale number presented as live (§12.7).
- **Spend accounting** feeds the same histograms as CON-37, so the quota application in
  §4.3 is written from measured behaviour.
- **Negative caching.** A channel that is not live is checked on the cheap datum only,
  rarely, and its expensive datums are not polled at all.
- **Never a cold-start stall.** A new subscriber receives the last known value with its
  age immediately, then live updates. A render never waits on an upstream call.

#### 4.4.6 The anti-patterns, named

No client-side calls to YouTube · no per-widget or per-surface fetching · no polling while
a channel is offline · no fetch on page load "just in case" · no prefetch on hover · no
fixed global timer that runs whether or not anyone is watching · no per-visitor
subscription on a public page.

**Standing rule:** the YouTube connector is *locally proven only*. Real OAuth
verification, quota grant, chat-write approval and staged live-stream evidence must
land before anything here is called production-ready.

---

## 5. Companion — the creator cockpit

### 5.1 Pre-stream: "Prepare Stream"

One large button that validates everything and reports plainly.

**Validates:** YouTube channel connected, token healthy, correct channel selected ·
broadcast title, thumbnail, category, description, playlist, privacy, DVR, delay ·
OBS/desktop helper connected and correct scene collection loaded · Master Canvas
overlay heartbeat healthy · microphone, audio tracks, replay buffer, recording,
source visibility · QR/tip page live, payment account active, donor receipt settings
valid · sponsor campaign, goals, challenges, moderation profile loaded · YouTube chat
and BharatStudio event bridge healthy.

**Reports:**

```text
Ready to go live
✓ YouTube ingest detected
✓ Master Overlay connected
✓ Tips and QR enabled
✓ Chat moderation active
! Sponsor asset expires in 3 days
```

**Actions:** Start OBS · Start testing · Go live · Start local recording · Send test
alert · Share stream/tip link · Abort safely.

Irreversible actions — ending a broadcast, changing a live privacy setting — require
explicit confirmation.

### 5.2 During stream: "Live Deck"

Usable one-handed in two seconds.

```text
LIVE • 01:42:18 • YouTube healthy • Overlay healthy • ₹8,420 • 1,204 viewers
```

- **Panic / Clutch Mode** — mute TTS, hide QR, suppress loud media, **retain all
  financial events** and show them later. Nothing is lost, only deferred.
- **Alert modes** — full / visual-only / queue / pause
- **Scene presets** — Gameplay, Just Chatting, BRB, Sponsor, Vertical, Ending
- **Master Canvas modules** — chat, ticker, goals, QR, music metadata, challenge,
  hype, sponsor card
- **Test alert** and **test overlay**
- **Goal controls** — increase target, start timer, mark complete, trigger celebration
- **Quick note / stream marker** — "great clutch", "sponsor mention", "clip this",
  "technical issue"
- **OBS control** via desktop helper — scene switch, source toggle, mute, replay
  buffer, recording, transition

**Degraded-mode strip** — the single most important element on the screen:

```text
YouTube chat delayed — BharatStudio tips and overlay remain live.
```

A creator must never have to guess whether the problem is YouTube, OBS, payment,
overlay or their own network.

### 5.3 Moderation and safety

Where Companion beats generic overlay products.

- Swipe actions: approve, hide, visual-only, timeout request, ban request, pin safe
  message
- Role-based moderation: creator, trusted moderator, producer, sponsor operator
- **Indic transliteration-aware TTS safety** for Hinglish and regional-language abuse
- Separate decisions for: public visual · TTS · stored payment/receipt · moderator
  review. One message can be paid, visible, and unspoken.
- **No-accidental-doxxing detector**: phone numbers, UPI IDs, email, addresses,
  card-like numbers, unsafe URLs
- Slow-mode / raid-mode / high-toxicity profile toggles
- Policy presets: family-friendly, gaming, mature audience, sponsor-safe

### 5.4 Community and monetization controls

- Embedded live chat · unified supporter ticker · dynamic QR/tip CTA · curated
  meme/media queue · metadata-only "now playing" card · goals, challenges, paid
  votes, boss battles, hype meter
- Retention mechanics: like goal, tip goal, member goal, chat goal, watch-time goal ·
  community boss fight with carefully configured contribution rules · daily/weekly
  stream streaks · creator challenge cards ("15 kills", "finish the mission") ·
  viewer prediction/vote widget **with no gambling-like economic mechanic**
- **Milestone queue** — when a goal lands, automatically *prepare* the thank-you,
  sponsor reveal, giveaway reminder or scene transition. Prepare, not fire.
- VIP recognition from opted-in supporter history, **never public spend amount by
  default**

### 5.5 Post-stream: "Wrap Stream"

The "I'm exhausted" workflow. One button.

- Confirm OBS has stopped and the YouTube broadcast is really complete
- Preserve overlay/event/payment audit records
- Generate a private stream summary
- Suggest VOD title cleanup, description blocks, chapters from markers, playlist
- **Prepare, not auto-post**, supporter thank-you comments for creator approval
- Sponsor exposure log with timestamps and caveats
- Export a finance delta to Google Sheets/CSV
- Schedule a follow-up clip/replay-buffer review
- Report missed alerts, queued items, failures and reconciliation tasks

Top supporter names are never auto-published without visibility consent.

### 5.6 Shipping the app — the part a product spec usually forgets

Everything above describes what Companion does. This section describes what it takes to
put it on two stores and keep it there. It was absent from version 1.0 of this
document, and every row below is a real blocker for a mobile release, not a polish
item.

Two constraints from `00_LAUNCH_SCOPE_AUTHORITY.md` are already binding and are not
reopened here: **React Native for both platforms**, and **floors of iOS 15.1 and
Android API 26**.

#### 5.6.1 Buying happens on the website. Never in the app.

**Decided 2026-09-14. There is no purchase of any kind inside Companion, on either
platform.** No subscription, no tier upgrade, no top-up, no AI credits, no pack, no
add-on. This matches the launch authority's exclusion of in-app checkout and it is a
product decision, not only a compliance one.

Why it is the right call and not merely the safe one:

- A store's commission on digital goods would take 15–30% of a ₹199 subscription and of
  every ₹99 credit top-up. The §10 credit model computes a **25%-floor margin** before
  issuing units. Store commission does not fit inside that; it would force either a
  higher price on mobile than on web, or a smaller unit bundle on mobile for the same
  rupees. Both are worse products and both are confusing.
- Two purchase paths means two receipt systems, two refund policies, two entitlement
  sources of truth and two support scripts. The entitlement model in §15 is
  server-owned by design; a store-owned purchase punches a hole in it.
- Nothing a creator buys is consumed only on mobile. The tier drives the overlay, the
  tip page and the dashboard. The natural place to buy it is where it is configured.

What that means concretely in the app:

| Situation | Behaviour |
|---|---|
| A locked control | Shows as locked with the unlocking tier named (§15.3), exactly like the web. No price, no purchase button |
| Credits exhausted mid-stream | A plain statement of the state and what still works. Never a purchase prompt |
| Free creator viewing a Creator-tier control | Sees it, sees the tier that unlocks it, and cannot buy it here |
| Subscription lapsed (§26) | Grace and paused notices appear in Companion as specified — as **notices**, never as a payment wall, and never on stream |
| Any screen anywhere | No price, no currency amount for a BharatStudio product, no "upgrade" call to action, no link out to a purchase page from an iOS build |

The link-out question is deliberately settled the conservative way: **iOS builds contain
no link, button or instruction directing a creator to a purchase surface.** Anti-steering
rules have changed repeatedly by jurisdiction and a rejected build during launch week
costs far more than the conversion this would earn. A creator who wants to upgrade uses
the dashboard, and they are already in it — that is where they set up everything else.
Android builds follow the same rule for a single reason: one codebase, one behaviour,
no platform-conditional monetisation logic to get wrong.

Revisit only if store review evidence shows link-outs are safely permitted in India for
this category, and then as a deliberate change with its own decision row.

#### 5.6.2 Languages — the app speaks the creator's language

This is a product for Indian creators and an English-only cockpit is a poor one. Three
different things are involved and version 1.0 of this document conflated them.

| Layer | What it is | State |
|---|---|---|
| **App UI language** | Every label, button, error, notification and empty state in Companion | **Missing entirely — this section adds it** |
| **TTS voice language** | What the alert reads aloud to viewers | Partly present; Indic voices are a §11 credit class |
| **Safety language coverage** | Abuse and doxxing detection across Hinglish and Indic scripts | Specified in §5.3, unbuilt |

**Launch set, v1:** English and **Hindi**, both complete. Hindi is not a partial
translation with English fallbacks scattered through it — a half-translated interface
reads as broken, and creators will judge the whole product by it.

**Wave two, P2, in this order:** Marathi · Bengali · Telugu · Tamil · Kannada.
**Wave three, P3:** Gujarati · Malayalam · Punjabi · Odia · Assamese.
Order follows creator-base share, and each wave is a capability-registry row so a
language can be published or pulled without a release.

**Deliberately not now: Urdu and any RTL language.** The layout system is not
direction-aware and retrofitting RTL onto every screen is a large piece of work.
Half-done RTL is worse than no RTL, so it is a labelled P3 with its own layout track,
not a translation task.

Engineering rules that make this survivable rather than a permanent tax:

- **No user-visible string literal in a component, ever.** A CI check fails the build on
  one. This is cheap on day one and near-impossible to retrofit at screen forty.
- **ICU MessageFormat**, so plurals and gender work. Hindi plural rules are not English
  plural rules, and no amount of string concatenation fixes that.
- **Never concatenate translated fragments.** `"You have " + n + " alerts"` cannot be
  translated correctly into an SOV language. One message, one placeholder set.
- **`Intl` for every number, currency, date, duration and relative time.** Rupee
  grouping is 2,2,3 (`₹1,23,456`), not 3,3,3. Getting this wrong on a money screen is
  the single most visible possible localisation bug in this product.
- **Locale is a device default with an in-app override**, persisted per install and sent
  on every API call. A creator on an English phone who wants a Hindi cockpit gets one.
- **Server-generated strings are localised server-side** from the request locale — push
  notification bodies, validation errors, health messages, degraded-mode text. A
  translated app in front of an English API is not a translated product.
- **Push notification bodies are localised at send time** from the stored device locale,
  not at registration time.
- **Pseudo-locale build** in CI (`Ħēĺĺō [[[wörld]]]`) catches hardcoded strings and
  layout that breaks on expansion before a translator ever sees it.
- **Layout survives +40% text expansion.** Hindi and Tamil run longer than English.
  Every button, tab label and status chip is tested at expansion, not just at English
  width.
- **Fonts.** Devanagari and the other Indic scripts must render with correct conjuncts
  and matras on both platforms; bundle the faces rather than trusting the device set,
  and check vertical metrics — clipped matras are the classic failure.
- **Translation is reviewed by a native speaker who streams.** Machine translation of
  "Clutch Mode", "queue", "overlay" and "Super Chat" produces text that is technically
  correct and reads as absurd to the audience. Product vocabulary gets a glossary that
  is fixed once and reused.
- **A missing translation falls back to English and is reported**, never rendered as a
  key. The fallback rate per locale is a monitored number.

#### 5.6.3 Push notifications — the delivery path, not just the six types

§30.4 tiers notification types and CMP-24 lists six. Neither says how a notification
arrives. It arrives over **APNs** on iOS and **FCM** on Android, and that carries its
own set of decisions.

- **Token lifecycle.** Register on permission grant; re-register on every app launch,
  on token rotation, and after a restore to a new device. Delete the token on sign-out
  and on session revoke (CMP-26). Prune tokens APNs or FCM reports as invalid, on the
  feedback response, rather than accumulating dead devices forever.
- **Priority classes.** Only two things justify a high-priority, waking delivery: a
  **stream-health failure while live**, and a **payment or delivery failure**. Tips,
  goals, milestones and social events are normal priority and are allowed to be
  batched by the OS. A product that wakes a creator's phone for every ₹20 tip gets its
  notifications disabled inside a week, and then the alerts that matter never arrive.
- **iOS reality.** Normal-priority notifications may be delayed or coalesced by the
  system; background app refresh is not a schedule. The Live Deck's freshness must never
  depend on a background delivery having happened — it reconciles on foreground, always.
- **Android reality.** Notification channels per type, so a creator can silence tips and
  keep health alerts, and so the OS gives us per-channel controls for free. Doze and
  app-standby will delay normal-priority messages; the same foreground reconciliation
  applies.
- **Permission prompt timing.** Never on first launch. The prompt appears at the moment
  it is meaningful — the creator has just finished Prepare Stream, or has just enabled a
  notification type — with one sentence saying what will be sent. A denied permission is
  a supported state the app works in, not an error screen, and is re-requestable from
  settings with a deep link into the OS settings page.
- **Payload rule, already binding (CMP-32).** A notification payload never carries tip
  amounts, donor identity, message content or payment detail. It carries a type and an
  identifier; the app fetches the content after unlock. This survives a locked-screen
  preview being visible to whoever is standing next to the creator.
- **Delivery is best-effort and is stated as such.** Nothing about correctness may depend
  on a push arriving. Push is an accelerator over a state the app can always re-derive.
- **Quiet hours** per creator, with the two high-priority classes able to override, and
  an explicit "everything, always" option for creators who want it.

#### 5.6.4 Authentication and device security

- **Sign in with Apple is mandatory on iOS** if Google Sign-In ships in the app, which
  it does — that is the v1 authentication method. This is an App Store review
  requirement, and discovering it during submission week is a self-inflicted delay. It
  is a real backend change too: a second identity provider, an account-linking rule for
  a creator who has used both, and Apple's private-relay email addresses handled as
  first-class addresses rather than rejected by a validator.
- **Biometric app lock**, optional and default off. Face ID / Touch ID / Android
  BiometricPrompt gates re-entry to a foregrounded app. This is a cockpit showing
  revenue on a device that gets handed around; the control belongs to the creator.
- **Session expiry is visible and graceful.** An expired session shows a re-auth sheet
  that returns the creator to exactly where they were, never a silent logout mid-stream.
  The control-session lease (CMP-01) and the auth session are separate things and their
  failure messages must say which one ended.
- **Secure storage is already specified** — `WHEN_UNLOCKED_THIS_DEVICE_ONLY`, no
  plaintext fallback (CMP-33) — and it holds for the auth token and the paired-device
  secret alike.
- **Screenshot and screen-recording awareness.** The Live Deck shows revenue. A creator
  screen-sharing their phone should not leak supporter identities; a single "hide
  sensitive values" toggle, honoured across the app, is enough and is far simpler than
  per-field masking.
- **Sign-out clears everything** — token, cached state, push registration, biometric
  enrolment — and revokes the control lease server-side rather than letting it expire.

#### 5.6.5 Navigation, information architecture and deep links

Version 1.0 described screens with no structure connecting them.

**Five tabs, fixed, no more.** More than five in a bottom bar makes each one
unreachable one-handed.

| Tab | Contents |
|---|---|
| **Live** | The Live Deck (§5.2) — the default tab whenever a stream is live |
| **Prepare** | Prepare Stream and Wrap Stream (§5.1, §5.5); becomes Wrap after a stream ends |
| **Queue** | Current and next items, per-item replay and skip, moderation actions (§5.3) |
| **Money** | Recent tips, payment and refund status, goals — everything with a rupee in it, in one place, behind the sensitive-values toggle |
| **More** | Sessions and devices, notification preferences, language, help, account |

- The **degraded-mode strip** (§5.2) is not a tab. It is persistent across every tab
  whenever any signal is unhealthy, because the whole point is that it cannot be missed.
- **Deep links resolve to a screen with state, not to the home tab.** Every notification
  taps through to the thing it is about: an alert item, a payment, a goal, a lobby, a
  health failure. A cold-start deep link waits for auth and then lands correctly rather
  than dropping the destination.
- **Universal Links and App Links** — a `bharatstudio.in` link opens the app when it is
  installed and the website when it is not. That requires the association files hosted
  and verified on the domain, which is an infrastructure task with a lead time and
  belongs on the launch checklist, not the app backlog.
- **Back behaviour is predictable**, Android hardware back included, and scroll position
  and filters survive a tab switch.
- **No modal traps.** Every sheet has a visible dismiss, and a sheet with unsaved
  changes confirms before discarding.

#### 5.6.6 First run — the claim in §30.4 has to be true

§30.4 says Companion on Free is "the cockpit that makes a first stream succeed". Nothing
in version 1.0 described a first run, so the claim was unsupported.

1. **Sign in.** Google or Apple. Nothing else on the screen.
2. **Pair or connect.** Device-code pairing (CMP-06) presented in plain language with a
   scannable code, and a stated alternative if the camera is denied.
3. **One guided run of Prepare Stream**, on the creator's real setup, with each failed
   check explaining what to do rather than showing a red cross. This is the moment the
   product proves itself.
4. **Permissions, in order and in context** — notifications after the first successful
   check, camera only at the moment a code is scanned. Never a wall of prompts at
   launch.
5. **A first test alert**, fired from the phone, visible on the overlay. The single most
   convincing thing this app can do in its first two minutes.

**Every empty state is written, not defaulted.** No stream yet · no tips yet · no queue
items · no devices paired · notifications denied · offline · subscription paused. Each
says what would fill it and what the creator can do next. Empty states are where a Free
creator spends their first week.

#### 5.6.7 Devices, layout and accessibility

- **Floors: iOS 15.1, Android API 26**, from the launch authority. Below the floor, the
  app refuses to install rather than half-working.
- **The reference device is a mid-range Android on 4G** (§19.8), not a flagship on
  Wi-Fi. Performance budgets are measured there or they are not measured.
- **Phone portrait is the designed orientation.** Landscape must remain usable — a
  creator with the phone on a stand beside the monitor is a normal setup — and must not
  hide the degraded-mode strip or the panic control.
- **Tablets get the phone layout scaled with a maximum content width**, not a bespoke
  two-pane design. A bad tablet layout is worse than an honest scaled one, and the
  audience is small.
- **Dynamic Type and Android font scaling are honoured up to the largest accessibility
  sizes**, with no truncation of a control label and no control falling below its
  minimum touch size. Tested at the largest size, not assumed.
- **Minimum touch target 44pt / 48dp**, with spacing, on every control on the Live Deck.
  This is a one-handed panel operated in a hurry.
- **Screen reader labels on every control**, including the icon-only ones, in the
  selected language. The panic control is reachable and announced.
- **Reduced-motion honoured**; no critical state communicated only by animation.
- **Colour is never the only signal** for health state — a shape or a word accompanies
  every colour, on every one of the six signals.
- **Dark mode is the default** and light mode is complete. A creator in a dark room at
  1 a.m. is the normal case.
- **Safe areas** — notch, Dynamic Island, gesture bar. No control under the home
  indicator, no health strip under the notch.

#### 5.6.8 Release, versioning and updates

- **Channels.** Internal → TestFlight / Play internal test → staged production rollout
  starting at 10%, with a halt on a crash-rate regression.
- **Version scheme.** Semantic app version plus a monotonic build number, and every
  build recorded against the commit and the API contract version it was built for.
- **The API is versioned and the app is not assumed current.** Some creators will run a
  six-month-old build. Every endpoint the app calls is either backward compatible or
  behind a version negotiation, and breaking an old build is a deliberate, dated act.
- **Forced upgrade exists and is used sparingly.** The server can mark a build below a
  floor as unsupported; the app then shows a blocking screen with a store link and a
  plain reason. Reserved for security fixes and protocol breaks — never for feature
  pushes.
- **Soft upgrade prompt** for everything else: dismissible, and never during a live
  stream.
- **Over-the-air JavaScript updates: permitted, narrowly.** Allowed for a JS-only fix
  within the same native binary; every OTA bundle is versioned, signed, staged the same
  way a store release is, and instantly rollback-able. Never used to add a feature, to
  change anything monetisation-related, or to alter behaviour a store reviewed. Native
  changes always go through the store.
- **A rollback plan for each release**: the previous binary stays available on internal
  channels, and any migration the app performs on local state is reversible or additive.

#### 5.6.9 Store compliance — the review-risk list, written before submission

Each of these has rejected apps in this category before.

| Risk | Position |
|---|---|
| **Digital purchases outside the store** | Not applicable — no purchase, no price, no link-out from iOS (§5.6.1) |
| **Sign in with Apple** | Implemented alongside Google Sign-In (§5.6.4) |
| **Account deletion in-app** | **This is the open one.** Both stores require an in-app route to delete an account for apps that create one, while §33.1 blocks the deletion policy on legal. These must be reconciled **before submission**, not during review. The likely landing point is an in-app request route with a stated, lawful retention policy — and that wording is legal's, not ours |
| **Permission purpose strings** | Written per permission, specific, in every shipped language. Generic strings are a routine rejection |
| **Data-safety and privacy-nutrition declarations** | Filled from the actual data map, matching the published policy exactly. A mismatch between the declaration and the policy is a rejection and, worse, a credibility problem |
| **Payments and creator earnings content** | The app shows a creator their own earnings. It never processes a payment, never handles a card, never shows a supporter's payment instrument |
| **User-generated content** | The app can display supporter messages, so the store's UGC expectations apply: report, block, moderate. §5.3 provides the mechanics; the store needs them documented |
| **Background execution** | No background audio keepalive, no misdeclared background mode. Background use is push plus foreground reconciliation |
| **Name collision** | "BharatStudio Companion" in full, always, in the store title, subtitle and screenshots (CMP-31) |
| **Age rating and content descriptors** | Set from the moderation reality, honestly |
| **Accounts and demo access** | A reviewer needs a working demo account with seeded data reaching a live-looking Live Deck. Preparing this is a task, not an afterthought |

#### 5.6.10 Connectivity, offline and battery

- **Offline is a first-class state, not an error.** The app shows the last known state
  with its age, plainly, and never presents stale numbers as live ones.
- **The offline queue-of-intent (CMP-27)** holds actions taken while disconnected, shows
  them as pending, and reconciles with explicit success or failure per action on
  reconnect. An action that cannot be safely replayed is refused offline rather than
  queued — anything irreversible, and anything financial.
- **Reconnection is exponential with jitter**, and a reconnect always reconciles state
  rather than assuming the stream of events was continuous.
- **Battery.** A three-hour stream with the app open must not be the reason the phone
  dies. No polling loop, no permanent socket held across backgrounding, no animation
  running while backgrounded.
- **Data usage** stays modest on a metered connection — no image or media prefetch on
  cellular beyond what is on screen.

#### 5.6.11 Operations — what tells us the app is working

- **Crash and error reporting** from day one, with release-tagged builds, symbol upload
  in CI, and a crash-free-sessions target that gates a staged rollout. Reports are
  scrubbed of tip amounts, supporter identity and message content before they leave the
  device.
- **Product analytics that respect the privacy position** in §12.3: event names and
  coarse counts, no identifiers in labels, consent handled the same way as the web
  surfaces, and an opt-out that actually stops collection.
- **The measured budgets are the ones in §19.4** — under 2s to interactive cold start,
  under 300ms perceived action round trip — recorded per release on the reference
  device, not asserted.
- **End-to-end tests on both platforms** covering the paths that matter: sign in, pair,
  Prepare Stream, fire a test alert, enter Clutch Mode, act on a queue item, go offline
  and reconcile. A screen-level unit test proves nothing here, for exactly the reason
  §2 exists.
- **CI builds both platforms on every merge** and produces an installable artifact.
  Discovering that iOS has not compiled in three weeks, during submission week, is the
  Windows Companion failure (§32) repeating on a platform that matters.
- **A release checklist that includes the store artefacts** — screenshots in every
  shipped language, localised descriptions, the demo account, the declarations — because
  those, not the code, are what usually delays a submission.

---

## 6. Master Canvas and the module catalogue

One browser source replaces the pile. Streamlabs' own pattern — alerts, chat, ticker,
media, custom widgets and themes each added as a separate browser source — is exactly
the clutter we remove.

**Competitive accuracy, checked 2026-09-16 and recorded before the claim can be made.**
"One source replaces twelve" is true against **Streamlabs**, which is genuinely per-widget:
one Widget URL becomes one browser source, repeated per widget. It is **not** a
differentiator against **StreamElements**, whose Overlay Editor already composes alerts,
widgets, goals and chat into a single browser source
(`docs.streamelements.com/overlays`, accessed 2026-09-16). Anyone writing that sentence for
publication must name Streamlabs or re-verify StreamElements first.

What is **not** matched by either, on their public documentation: a single connection **and**
a single render loop **and** per-module error isolation together. That is the correctness
claim, and it is a different sentence from the source-count one — it needs RT-07 evidence
before it may be made at all (RT-09).

**Every module below is a module of the one canvas, never a new OBS source, and never
a parallel state system.** Goals, votes, leaderboards, hype, challenges and stickers
are extended through these modules rather than duplicated.

| # | Module | Notes |
|---|---|---|
| 1 | **Support Theater** | Current verified alert, queue state, moderator decision |
| 2 | **Community Goal Ladder** | Milestone tiers and progress |
| 3 | **Tug-of-War Vote** | Two-sided transparent result bar |
| 4 | **Boss Fight** | A visual skin over an ordinary support goal — not a new mechanic |
| 5 | **Reaction Cloud** | Sampled and rate-limited, non-identifying. *Owner decisions 2026-09-16: reactions are sends of entries from the existing curated **sticker catalogue** (first-party plus staff-reviewed creator packs, migration `0110`) — no new asset pipeline, no new rights question. Rate limiting reuses the built per-channel `rateLimitPerMinute` mechanism (creator-configurable 1–1000, one-minute window, migrations `0032`/`0063`); the display ceiling ships **configured but unset**. Sampling is server-side — the client is never sent the full stream and told to drop some (§12.7). "Non-identifying" must be a property of the query: counts and catalogue entry ids, never a viewer identifier.* |
| 6 | **Safe Soundboard Alert** | Approved clips only, with cooldown and queue |
| 7 | **Supporter Ticker** | Latest supporter, goal, creator-selected copy |
| 8 | **Challenge Board** | Current / next / completed, with no false refund promise |
| 9 | **Stream Mission Card** | Creator-defined objective and timer. *Owner decision 2026-09-16: built in PRF-02 slice 5, overriding §34's Phase 3 placement for this module only. Objective text reuses the already-decided challenge-title bound (1–120 characters, migration `0109`); the mission is session-bounded, not clock-bounded — no duration number is invented.* **Built in PRF-02 slice 5.** Schema, creator read/write paths, the overlay read `app_private.list_overlay_stream_mission` (migration `0135`) and the canvas renderer. The no-invented-duration rule is visible in the schema itself: the table carries no duration, timer, expiry, deadline or ends-at column of any kind, so a mission can only end because the creator ended it or the overlay session did. Objective text is bounded 1–120 characters, the same `char_length` bound migration `0109` already decided for challenge titles — reused, not chosen again.* |
| 10 | **QR Smart Card** | Visibility tied to scene, gameplay safe zones, or Clutch Mode |
| 11 | **Sponsor Card** | Scheduled placement with an exposure event log |
| 12 | **Moderator Status Card** | Held count and moderation state — never private content. *Owner decision 2026-09-16 (second): **safe mode is a creator switch that holds every alert for review** — while on, incoming alerts route to `held` rather than `ready`. It is never automatic and is never triggered by a spike, a rejection rate or any other signal; a creator turns it on and off. Anything automatic is a separate, unmade decision.* *Owner decision 2026-09-16 (first): "safe mode" is **not** `alert_queues.is_paused`. Safe mode is a separate moderation control that does not exist in the schema, so this module ships its held half only and safe mode needs its own record and decision before it can appear here. The held figure is held **alert deliveries** (`event_outbox_deliveries.status = 'held'`), not chat messages — §6's original "messages held" wording predates the schema and is corrected to it.* **Built in PRF-02 slice 5, held half only.** The overlay read is `app_private.list_overlay_moderator_status` (migration `0136`), gated by the existing `overlay_sessions` token-fingerprint model. §6's "never private content" is a property of the query, not of the renderer: the function's return type is a single `held_count bigint` column and nothing else — no supporter name, message text, amount, delivery id, queue id or viewer identifier can leave the database on this path, and the returned column set is asserted in `packages/db/tests/prf02_slice5_moderator_status.sql`. The function reads no queue lifecycle column at all (`alert_queues.is_paused` is never referenced), so no surface resembling safe mode exists on it. Safe mode remains unbuilt and still needs its own record and decision. |
| 13 | **Milestone Celebration** | One reusable animation fired by verified state transitions |
| 14 | **Vertical Stream Layout** | Narrow chat, compact goal, QR, reactions for mobile scenes |
| 15 | **Stream Health Widget** | Creator-only view of YouTube, payment, alert and OBS health |
| 16 | **Lobby Status** | Aggregate seats and queue only (§16). *Owner decision 2026-09-16: PRF-02 may build the **minimum §16 Lobby schema** needed to render this card, overriding §34's Phase 3 placement for this module only. Aggregates only — no per-viewer row, and nothing that correlates one visit to another.* |
| 17 | **Giveaway / Tournament Card** | Entry state, draw status, bracket (§17). *Owner decision 2026-09-16: PRF-02 may build the **minimum §17 schema**, overriding §34's Phase 3 placement for this module only — but with **no chance-based draw mechanic at all**. `GIV-07` gates chance-based formats on legal review, which has not happened; entry state and bracket are buildable, the draw is not, and it must not be approximated by a creator-records-the-winner surface nobody decided.* |
| 18 | **Now Playing** | Metadata only, never audio |
| 19 | **Chat** | Embedded live chat |
| 20 | **Media / Meme Queue** | Curated, approved assets only |

Canvas requirements: safe zones · scene profiles · theme packs · per-module placement
and z-order · vertical and mobile layout variants · preview with sample data · one
heartbeat the Live Deck can read · **graceful per-module degradation — one module
failing must never blank the canvas**.

---

## 7. Dashboard — setup and business, not live pressure

Companion is for live operation. The dashboard owns the deeper work.

- Canvas designer, layouts, safe zones, scene profiles, theme packs
- OBS migration/import report and one-click rollback
- YouTube connection, scopes, quota use, stream presets, templates
- Goal/challenge builder
- Moderator roles, policies, audit log, blocked phrases
- Media library, rights confirmation, scanning, quotas, cooldowns
- Sponsor campaign manager and exposure schedule
- Supporter/receipt ledger and refunds
- Google Sheets/Drive export setup
- Integrations: OBS helper, Streamer.bot, SAMMI, Mix It Up, Streamlabs and
  StreamElements compatibility relays
- Post-stream performance review

### 7.1 The screen inventory — what exists, and what was missing

The list above named the dashboard's *jobs*. It never named its **screens**, and the
register had no dashboard section at all — which is how an audit surface guaranteed by
§12.6 ended up with nothing rendering it. A job with no screen is how the §2 failure
begins.

| Screen | What a creator does there |
|---|---|
| **Home / Today** | Today's support, goal progress, stream state, queue depth, six health signals, anything needing attention. Pinnable cards |
| **Activity Log** | Every audited action by anyone — creator, moderator, operator, platform staff, system (§7.5) |
| **Money → Payments** | The ledger. Row → payment detail with its full timeline |
| **Money → Receipts** | Every receipt, its token link, its delivery state |
| **Money → Refunds** | Refund state and its effect on every derived number |
| **Money → Statements** | Monthly statement, exports, reconciliation view *(Finance pack)* |
| **Supporters** | Search, filter, and a profile per supporter (§7.4) |
| **Alerts → Queues** | Queue list, per-queue settings, bindings, priority |
| **Alerts → History** | Every alert event, its delivery timeline, replay and skip, and **why one did not fire** |
| **Canvas** | Designer, scene profiles, modules, safe zones, adversarial preview, browser-source URLs and token rotation |
| **Tip page** | Editor, live preview, campaign pages, QR download, short links, share-card preview |
| **Moderation** | Live queue, blocked terms per language, policies, appeals, seats and roles, shift handover |
| **Sounds & Media** | Library, upload, quota, scan state, rights attestation, takedown status, and **where each asset is used** |
| **Integrations** | Connectors, OBS helper, bridges, packages, migration report, webhooks |
| **AI** | Credit balance, usage by feature, spend caps, and a log of every AI action with its reason and confidence |
| **Health & Diagnostics** | Six signals with heartbeat ages, run-full-test with a per-hop report, incident notices, status history |
| **Insights** | Per-stream recap, comparisons, funnels — never live-pressure numbers |
| **Settings** | Account · security (sessions, devices, 2FA) · team · notifications · language · billing · **data and privacy** (export, deactivate) · brand kit |
| **Bot** *(P2)* · **Social** *(P3)* · **Community** *(P3)* | Their own areas, out of v1 |

### 7.2 The detail-view contract — every noun has one, and they all look the same

**Decided 2026-09-14.** A creator should never hit a dead row. Every object has a detail
view, and every detail view has the same five parts in the same order:

1. **Summary** — what this is, its state, the two or three numbers that matter.
2. **Timeline** — what happened to it, in order, with timestamps and the trace ID.
3. **Relations** — what it connects to, each a link: a payment's supporter, receipt,
   alert event and refund; an asset's modules; a module's data source.
4. **Actions** — what can be done now; irreversible ones confirmed, reversible ones
   undoable.
5. **Audit** — who changed this, when and why, filtered from the same log as §7.5.

The nouns: payment · receipt · refund · alert event · queue · supporter · moderator ·
asset · module · scene profile · connector · package · campaign page · AI job ·
notification · lobby · giveaway. One layout, learned once.

### 7.3 One click, from anywhere

| Affordance | Behaviour |
|---|---|
| **Copy** | Tip link, short link, overlay URL, QR image, receipt link — one click, with a toast |
| **"Why this number?"** | Any derived figure — goal total, leaderboard rank, badge, streak — opens an explain panel showing the computation and the rows behind it. **Possible only because §19.6 derives rather than stores**; a stored counter could not explain itself |
| **"Why didn't this fire?"** | Any alert that did not appear opens a per-hop diagnosis — payment verified? event created? queued? delivered? rendered? acknowledged? — naming the failing hop rather than saying "unknown" |
| **Trace** | Every payment and alert row exposes its trace ID and a timeline built from it |
| **Send a test** | A test alert from any screen, not only from settings |
| **Show me on stream** | Preview any module on the real overlay for a few seconds, then auto-revert |
| **Replay** | Re-run any alert event, subject to the existing moderation rules |
| **Undo** | Every reversible action gets an undo toast with a real window, rather than a confirmation dialog beforehand |
| **Open in Companion** | Deep-link the same object to the phone (`CMP-61`) |
| **Export this view** | The current filter set, as a background job, never by rendering rows (§12.7) |
| **Pin to Home** | Any card |
| **Report a problem** | Attaches a redacted context bundle — §7.6 |

### 7.4 Two screens worth specifying properly

**Supporter profile.** Support history, streak, badges, first and most recent support,
messages shown and hidden, consent state, creator-private notes, and the controls that
matter: mute from TTS, block stickers, block entirely, report. **Amounts follow §12.3** —
never a public lifetime total, and visibility consent governs anything shown on stream.

**Command palette and global search.** One shortcut opens a palette that searches
supporters, payments, receipts, assets, modules and actions, and runs any action it
finds. For a creator with a thousand payments, search *is* the navigation.

### 7.5 Activity Log — the surface §12.6 already required

§12.6 makes moderation history a durable record that must be **viewable, searchable and
exportable at every tier**. Until 2026-09-14 the audit *records* existed — `ALQ-10`,
`ADM-02`, `ADM-08`, `CTL-01`, `AUD-08`, `LOB-08`, `BOT-14` — and **nothing rendered
them**. The §2 pattern, forming before any new code was written.

One chronological view over every audited action, not one log per feature.

- **Filters:** actor (me · a named moderator · operator · platform staff · system),
  action type, time range, affected object.
- **Each entry:** who, what, when, the target, the reason where one was required, the
  before-and-after where a setting changed, and a link to the object.
- **Platform-staff actions appear here too.** A `global_kill` or a retier affecting this
  channel is visible to the creator afterwards; §20.6.1 already requires telling them
  within the hour, and this is where they look later.
- **Role-scoped reading**, enforced by projections and RLS rather than hidden UI:
  operators and moderators see operational entries without financial amounts.
- **Free at every tier, uncapped** — it is a durable record (§12.6). Only the *team*
  dimension is tierable: multi-moderator filtering, saved views, scheduled export.
- Cursor-paginated, virtualised past 50 rows, exported as a background job.

**Companion gets a different thing, deliberately.** Not this screen — a short,
session-scoped **Recent Actions** list on the Live Deck: the last few actions anyone took
on this channel right now, each with one-tap undo where reversible. Mid-stream the
question is *"did my mod just ban someone, and why"*, not *"show me last Tuesday"*.

### 7.6 Support handoff bundle

One click produces a redacted diagnostic bundle — trace IDs, health signals, recent
errors, entitlement state, build versions — with **no tip amounts, no supporter
identities and no message content** (§12.4). It attaches to a support conversation, so a
creator never has to describe a failure they could not see.

### 7.7 States, not just screens

Every screen ships its **empty**, **loading**, **error** and **denied** states, authored
rather than defaulted:

- **Empty** says what would fill it and what to do next.
- **Loading** is a skeleton in the final layout's shape, never a spinner over a blank page.
- **Error** names the hop that failed and the action that retries it.
- **Denied** names the tier that unlocks it, or the role that lacks permission — never a
  dead control, never a silent hide (§15.3).

---


## 8. The Live Support Hub

The donation page is not a payment form. It is where a viewer watches, participates,
supports, and **immediately sees the outcome**.

> "Watch the stream, join the moment, support in three taps, and see your
> contribution land live."

An embedded YouTube player is viable through the official IFrame API, with correct
`origin` handling and real responsive testing. The player stays YouTube-owned; we never
proxy, re-host or overlay their playback.

### 8.1 The interaction set

| Feature | Viewer value | Overlay counterpart | Safety boundary |
|---|---|---|---|
| Sticky live player + support tray | Watch while paying | Optional "Support live now" CTA | Player stays YouTube-owned |
| Quick UPI amount pills | Faster conversion | Goal / ticker update after verified payment | Never trust client success alone |
| Live supporter wall | Shared momentum | Recent-supporter ticker | Names only with opt-in |
| Reactions | Feeling present without spending | Reaction cloud / stadium wave | Rate-limited, no identity exposure |
| Community support goal | One visible shared target | Goal bar / boss-health | Clear non-refundable wording |
| Pick-a-side vote | Fans influence what happens next | Tug-of-war / poll | Transparent rules, no chance mechanics |
| Approved sticker / sound pick | Personality before checkout | Sticker / media alert | Catalogue or creator-approved assets only |
| Safe message preview | Prevents embarrassing TTS | Alert-card preview | Policy re-runs server-side regardless |
| Milestone unlocks | Immediate community reward | Celebration, scene change, challenge card | A creator promise, never a financial contract |
| Post-payment live confirmation | Proof it counted | Queued → shown state | Only after verified provider state |

**The verification rule, absolute:** Checkout may give fast client feedback, but a
payment becomes a supporter event **only after server-side webhook verification**.
Razorpay itself distinguishes immediate Checkout feedback from webhook truth, and our
ledger already enforces this. The page may say "confirming"; it may never say "paid".

### 8.2 Changes to the proposed mechanics

Kept as proposed: sticky player and mobile-first tray · amount presets, UPI intent,
short optional message · live community goal · previewable approved sounds and
stickers · on-page activity and reactions · creator-configured challenge board ·
realtime verified→queued→shown state · recent supporters, streaks and badges with
consent.

UPI Intent works on mobile web, Android and iOS and returns the user to the app or
site, but must be device-tested; desktop falls back to QR.

Changed, and why:

- **Crowd bounty → an ordinary support goal.** A multi-party refundable contract is
  unbuildable: no rail supports refund initiation, and N refunds each able to fail is
  precisely the shape already cut from the plan.
- **Tip-to-vote → fixed, visible rules.** Contribution amount, vote weight, close
  time, and final result all published before the vote opens. No concealed weighting.
- **Spin-the-dare wheel → a creator-approved challenge deck.** A paid random-chance
  mechanic is a regulatory and trust problem. Use deterministic turn order or explicit
  creator selection instead.
- **VIP lounge counter → aggregate presence only.** Never reveal top-supporter
  identity or spend without explicit opt-in.
- **Sound jukebox → catalogue and creator-pack only.** No viewer uploads, no arbitrary
  URLs, no executable media. This matches the standing L22 safe-media boundary.

### 8.2.1 QR and UPI — the flows, precisely

Added 2026-09-15. The pieces were scattered across five sections and three of the rules
that matter most were assumptions rather than text.

#### 8.2.1.1 Three kinds of QR, and they are not interchangeable

| Kind | Encodes | Used on | Lifetime |
|---|---|---|---|
| **Channel QR** | The creator's **tip-page short link**. Never a payment, never an amount | The **overlay**, print, business cards, a stream's ending screen, anywhere the creator shares it | Stable for the life of the channel. Rotates only if the creator rotates the link |
| **Order QR** | One specific payment order, produced by the provider at checkout | The **tip page**, on desktop, inside the checkout step | Short-lived, expires with the order |
| **Campaign QR** | A campaign page's link (§15.4.4) | A campaign or event page, a poster, a sponsor asset | Lives with the campaign page |

> **The overlay QR is always a Channel QR.** An Order QR on stream would expire while
> people are still scanning it, bind every viewer to one stranger's order, and break the
> moment the page reloads. This was previously an unstated assumption; it is now a rule
> (`QR-02`).

#### 8.2.1.2 Amounts, expiry and refresh

- **A Channel QR never embeds an amount.** The supporter chooses on the page. This is the
  same reason a bare `!tip` replies with the link and no amount (§33.1).
- **A Campaign QR may carry a suggested amount as a page parameter**, which the page
  pre-fills and the supporter can change. It is a suggestion in the URL, never a fixed
  sum in the QR payload.
- **An Order QR carries the exact amount** and expires with its order. The tip page shows
  its remaining validity and offers one regeneration, rather than silently refreshing
  underneath someone mid-scan.
- **Rotating the channel short link invalidates every Channel QR in circulation**, which
  is a destructive act on printed material. It requires confirmation naming that
  consequence, and it is audited (§7.5).

#### 8.2.1.3 The device paths

| Device | Path |
|---|---|
| **Mobile web** | **UPI Intent** — the app chooser opens, the supporter pays in their UPI app, and the return path brings them back to the confirmation screen |
| **Desktop** | **Order QR** in the checkout step, scanned from the phone, with the page polling its own order state — never the provider's |
| **Tablet** | Treated as mobile when a UPI app is installed, desktop otherwise; the page offers both rather than guessing |
| **JavaScript degraded** | A link and a QR still work (§19.9). The payment path never depends on the client |

**The UPI-intent return path is the fragile part and needs real devices**, not an
assumption: Android and iOS differ, several UPI apps differ from each other, and a
supporter who does not come back cleanly must still land on a page that tells them the
truth about their payment. `QR-07` owns that, with device-lab coverage (`ENV-05`).

**Preferred-app memory** is half-built today — the server allowlist exists, the browser
half does not (§2). It stores *which app a supporter chose*, never a credential, never an
account identifier (§12.1), and it is per-device.

#### 8.2.1.4 Verification is not negotiable

- The page **never** treats a return from a UPI app as success. Only the HMAC-verified
  webhook confirms (`PAY-02`).
- The page shows the honest intermediate state — *waiting for confirmation* — with a
  bounded wait, and then a recovery screen with the receipt link so the supporter can
  check later without an account.
- **No "mark as paid", no generic QR fallback, no screenshot-based confirmation.** Ever
  (`RTE-14`).
- The receipt link is the supporter's only artefact, so it must work with no login, from
  any device, at any later time (`VID-04`).

#### 8.2.1.5 What we record

Per attempt: which path was offered (intent / QR / link), which was taken, which app was
chosen where the OS reports it, whether the return path completed, time from intent to
webhook, and the failure class when it fails. **No account identifiers, no VPAs, no
banking data** — §12.1 and §12.4 both apply, and the PII detector treats a UPI ID as PII
(`SAF-12`).

That data exists for one reason: conversion on the tip page is the product's economics,
and today nothing measures where a supporter falls out.

### 8.3 The "support without paying" lane

Not every interaction should demand money. This lane makes the page useful to viewers
who cannot pay, and removes the guilt that suppresses the ones who can.

Free reactions with anti-spam cooldown · join a community goal · follow/share reminder
· one free vote plus an optional, transparent paid boost · submit a creator-approved
challenge proposal · a "cheer card" with no TTS or alert unless approved · join
notifications for opted-in supporters · poll participation · daily check-in and
streak, **never redeemable for cash**.

### 8.4 Trust and conversion

UPI app chooser with plain "secure checkout" language · a creator-configurable "where
does my support go?" explainer · receipt access without an account · payment-retry
recovery screen · QR on desktop, UPI Intent on mobile · guest checkout by default ·
Indian language support · low-bandwidth / no-player mode · accessibility (reduced
motion, no autoplay sound, screen-reader labels).

Status states shown to the viewer, and these exact five:

```text
Payment pending
Payment verified
Alert queued
Shown on stream
Message held for moderation
```

### 8.5 Community

Current stream mission card · milestone ladder (₹500 / ₹1,000 / ₹2,500) · **goal
source labels** showing whether UPI tips, Super Chats and memberships are included or
excluded · thank-you wall with visibility controls · opt-in badges, never public spend
figures · team/squad goals with creator-defined attribution · a live "what changed"
feed (goal advanced, poll moved, challenge completed) · creator next-action card
("next game is decided in 3 minutes").

### 8.6 Creator growth

Shareable mini-card for WhatsApp and Instagram · referral link with fraud-safe
attribution · campaign links ("BGMI night", "birthday stream", "sponsor stream") ·
first-time supporter welcome copy · return-supporter streak acknowledgement ·
event-specific layouts (gaming, music, community goal, podcast, tournament) ·
post-stream supporter recap and receipt export.

### 8.7 Hub build order

1. Mobile support tray, verified payment state, receipts, QR/UPI flows
2. Supporter ticker, goals, reactions, consented supporter wall
3. Approved sticker/sound picker and safe message/TTS preview
4. Community goal ladder, transparent vote widget, mission card
5. Embedded YouTube player and a bounded public activity feed
6. Sponsor widget, squad goals, referral and campaign links
7. Advanced challenge flows — only after refund/provider capability evidence exists

---

## 9. Migration and interop — the feature that wins switchers

Creators switch only if we help before demanding replacement.

| Mode | What happens |
|---|---|
| **Observe** | Import OBS layout, watch events; nothing changes on stream |
| **Bridge** | BharatStudio becomes payment/event truth but forwards signed events to existing Streamlabs/StreamElements/custom tooling |
| **Replace** | One Master Canvas replaces old browser sources; old sources hidden, retained, reversible |

Bridge supports: signed outbound webhooks · local desktop bridge · OBS WebSocket
actions · Streamer.bot / SAMMI / Mix It Up templates · generic browser-compatible
relay widget · MIDI / hotkey / Stream Deck trigger mappings.

**Never** scrape Streamlabs or StreamElements sessions, copy their secrets, or call
undocumented provider endpoints. Use user-installed compatibility widgets and explicit
local configuration only.

### 9.1 The Interop layer — three separate capabilities, deliberately not one

Expanded 2026-09-14. Creators want other people's alert designs, other people's
automations, and a way to switch without a disruptive weekend. Those are three
different problems with three different risk profiles, and merging them into one
"integrations" feature is how a product ends up executing strangers' JavaScript inside
OBS.

| Capability | Purpose | Safe approach |
|---|---|---|
| **Style packages** | More alert designs and widget looks | Import or re-author assets into a signed BharatStudio package format |
| **Migration tools** | Make switching from an existing setup easy | Inspect, map, preview, import — with approval and reversal |
| **Event bridges** | Keep using existing automation during the switch | Emit selected BharatStudio events outbound to chosen tools |

#### 9.1.1 The rule that makes all three safe

> **BharatStudio never embeds an arbitrary third-party browser-source URL, HTML,
> JavaScript, CSS or iframe inside the Master Canvas. Ever.**

This is the same boundary as PRF-13 ("no third-party scripts in the overlay"), stated
from the interop side because this is where the pressure to break it will come from.
An external script inside the Canvas would put someone else's code in charge of OBS
performance, viewer data, reliability, our visual branding and our security — and it
would sit above the protected watermark layer (§30.6) and outside the bounded-data
rule (§12.7). There is no tier, no attestation and no "advanced mode" that makes it
acceptable.

What we do instead is everything below.

### 9.2 BharatStudio Canvas Packages — the format that makes a look portable

A **signed, versioned, declarative** template format. A package contains:

- layout and slot definitions
- theme tokens (colour, type scale, spacing, radii)
- animations chosen from an **allowed set**, not authored as code
- fonts, images, video, audio and Lottie assets, all bundled
- configurable fields the creator fills in (name, colour, threshold, sound)

#### 9.2.1 The signer model — decided 2026-09-14

"Signed and versioned" is not a security property without saying who signs. For now:

- **BharatStudio holds the only signing key.** First-party packages are signed by us.
- **A creator's private package is bound to their account and validated, not signed.**
  It never leaves that account, so there is no third party for a signature to protect.
- **Key handling:** the signing key lives in KMS with no human read path; rotation is
  scheduled and a package records the key ID it was signed with, so rotation does not
  invalidate history; a revocation list is checked at import **and again at render**.
- **Canonical serialisation is specified before the first package is signed** — a
  signature over a non-canonical form is a signature over nothing.
- **Provenance travels with the package:** author, source, version, licence statement,
  and the import or authoring event that produced it.
- **Licence and takedown** follow §18.3 — a package's bundled assets are assets, with
  the same attestation, quarantine and takedown route.
- **Renderer sandboxing** does not depend on the signature. The renderer treats every
  package as untrusted data regardless of who signed it, because a valid signature on a
  malformed package must still fail safely.

Creator signing keys, a revocation infrastructure and a third-party trust model arrive
**with the marketplace**, which is phase R (§9.7). Building them now would be
infrastructure for a thing we have decided not to ship yet.

A package contains **no JavaScript, no network fetches, no external font or asset URLs,
no CSS that executes, and no template expressions that can reach the runtime**. It is
data the Canvas renders, not a program the Canvas runs. Every package is signed,
version-pinned, and declares the minimum Canvas runtime it needs, so an old package
keeps rendering when the runtime moves.

**This is also the answer to the template-catalogue problem** that has been open since
§33.2 item 1. The 359 unwritten packages were unwritten because each one was bespoke
work. With a declarative format the shape of the work changes: author a small,
genuinely good first-party set, and let asset import cover the long tail. That is a
different and far more tractable problem than authoring 359 of anything.

### 9.3 Asset imports — creators bring the look they already own

Support importing assets a creator **owns or has licensed**: exports from Canva, Figma,
LottieFiles, Photoshop, and purchased packs of the OWN3D / Nerd or Die kind. Accept
SVG, PNG, WebP, audio, video and Lottie.

Every import goes through the pipeline that already exists in §19.1 and is gated by
§18.3: validate → scan → normalise and transcode → store content-addressed and
tenant-scoped → serve from CDN → render through our own engine.

Two consequences that must not be lost:

- **An imported asset is a creator upload.** It carries the same rights attestation,
  the same quarantine, the same provenance record and the same takedown route as any
  other upload. Importing from a design tool does not launder the rights question, and
  a purchased pack's licence is between the creator and the seller.
- **We never present one creator's imported asset to another creator** (§18.2), and
  imported assets are tenant-scoped in storage (§19.1). An import is not a
  contribution to a shared library.

The creator gets the look; we keep the runtime fast, safe and ours.

### 9.4 Migration wizard — "bring my setup"

1. **Inventory.** Read an OBS scene collection or a supported exported configuration
   and list what is there.
2. **Map.** Translate sounds, images, durations, thresholds, queue behaviour and text
   settings into BharatStudio equivalents.
3. **Preview and diff.** Side by side, before anything changes, with every unmapped
   item named rather than silently dropped.
4. **Publish on approval only.** Nothing goes live until the creator says so.
5. **Reversible.** The original sources are untouched and stay in the scene, disabled
   rather than deleted, so the creator can go back in one action.

An honest "could not import" list is worth more than a high import percentage. A
mapping we are unsure of is shown as unsure.

### 9.5 Bridges — outbound only, and outside the critical path

```text
Verified payment / event
  → durable BharatStudio event + overlay release
  → Master Canvas renders immediately
  → optional connector outbox
       → Streamlabs / Streamer.bot / SAMMI / Mix It Up
```

**A bridge failure must never delay, cancel, duplicate or alter a BharatStudio alert.**
This is the same architecture as RT-03 and RT-04: the critical path completes first and
the optional work happens afterwards, in its own outbox.

Every bridge destination gets: its own queue · retries with backoff · a dead-letter
record · a per-destination kill switch · an idempotency key · and a redacted delivery
log. A destination that fails repeatedly is disabled with a creator-visible notice, not
retried forever.

### 9.6 Per-integration assessment — including where I disagree with the proposal

| Integration | Position | Phase |
|---|---|---|
| **Streamlabs outbound alert bridge** | Build, but **do not position it as parity** — see below | P3 |
| **Streamer.bot local adapter** | Build, in the Companion desktop helper, `localhost` only, explicit pairing, creator-chosen allow-list of actions | P3 |
| **SAMMI local adapter** | Same shape as Streamer.bot | P3 |
| **Mix It Up local adapter** | Same shape, lower priority — smallest overlap with our audience | P3 |
| **StreamElements** | Configuration **migration** only. An event bridge waits on a confirmed API/partner position | **R** |

**Where I would change the proposal: Streamlabs cannot be a general alert bridge.**
Their documented guidance is roughly **two alerts per user per minute**. A creator
taking forty tips during a raid cannot bridge them, and a bridge that silently drops
thirty-eight of them is worse than no bridge — the creator will believe the tips did
not arrive. So the bridge ships as:

- **Selected event types only**, defaulting to low-frequency ones — goal reached,
  milestone, session start, sponsor moment — and **not** every tip.
- **Rate-limited and coalesced** by us, below the documented limit, with the coalescing
  stated in the UI: *"bridged alerts are summarised; your BharatStudio overlay shows
  every one."*
- **Labelled a transition tool** in the product, with the Replace step as the
  destination. It is a bridge in the literal sense: something you walk across once.

**Local adapters are helper mechanisms, not a product surface.** §14 keeps desktop
Companion out of scope as a product; these adapters live in the same local helper that
already exists for OBS control. Rules: `localhost` only, never a publicly reachable
port · the creator pairs explicitly and picks the permitted actions from a list · we
never accept an arbitrary command, from us or from anyone else (the same rule as
CMP-05, which already rejects `obs_*` sent directly).

**StreamElements stays research-only.** Migration of a creator's own exported
configuration is fine. An event bridge is not, until there is a confirmed API position
or partner contract — and under no circumstances do we scrape a dashboard, import a
browser-source secret, or execute copied widget code.

### 9.7 The marketplace — the part I would slow down

A reviewed template marketplace with creator publishing is the most attractive item on
this list and the one with the most hidden product in it. It is not a feature; it is a
second business:

- **Payouts to package authors**, which means a second money flow, a second settlement
  problem, a second refund policy and a second tax position — on top of the one that is
  still gated on the CA row in `05_SUPPORT_AND_EXTERNAL_EVIDENCE_REGISTER.md`.
- **GST on digital goods** sold by third parties through our storefront.
- **Content review at scale**, plus takedown, disputes, impersonation and repeat
  infringement — the §18.3 gate again, but now for assets we distribute rather than
  host privately.
- **Curation liability**: a "verified" badge is a claim we have to be able to defend.

So the sequencing is: **first-party curated packages only**, free, authored by us, with
private creator packages that never leave the creator's account. Third-party paid
publishing is **phase R** and reopens only when the payout, tax and review positions
exist. Nothing else in the interop layer depends on it.

### 9.8 Tier placement

| Tier | Interop |
|---|---|
| **Free** | First-party native templates and basic customisation |
| **Pro** | First-party packages, asset import within the storage quota |
| **Creator** | Migration wizard · private imported style packages · outbound bridges |
| **Studio** | Multi-destination bridges · team-managed style libraries · reusable brand kits · approval workflow before a package goes live |

Consistent with §33.1: connect, import and bridge are Creator-tier and above, and
nothing here touches the never-charged-for set. **Importing is a paid capability;
exporting your own work never is** (§12.6).

### 9.9 Build order for the interop layer

1. Define and validate the declarative Canvas Package format — everything else depends
   on it, and it is also the template-catalogue answer.
2. Asset import, transcoding, validation and preview, on the §18.3 gate.
3. OBS/setup migration inventory and configuration mapping.
4. Streamlabs bridge (selected events, rate-limited) plus the Companion-helper adapters
   for Streamer.bot, SAMMI and Mix It Up.
5. First-party curated package library and private creator packages.
6. *(Phase R)* Third-party marketplace publishing, once payouts, tax and review exist.

---

## 10. Monetization

### 10.1 The revenue model, stated plainly

BharatStudio takes **0% of tips**. That promise is the positioning and must not be
diluted. Revenue comes from three clean lines that never touch a creator's tip:

1. **Subscription tiers** — Free / Pro ₹199 / Creator ₹399 / Studio ₹599
2. **Top-ups** — the creator buys capacity from us; we are the merchant of record
3. **AI credits** — metered feature value (§11)

**There is no commission anywhere, and no provider pricing is ever shown in a
BharatStudio price.** A top-up is not someone else's money passing through and it is
not a percentage of anything.

The one deliberate exception is the **public tip-fee comparison calculator** (§12.5),
which is a comparison tool, not a price. The two rules are not in conflict and the
boundary is stated once, in §12.5.1.
The creator buys a **bundle of BharatStudio units at a flat price**:

```text
₹99  →  X characters of BharatStudio AI voice
₹99  →  Y BharatStudio AI credits
```

That is the entire customer-facing model. The creator never sees a provider name, a
provider price, a per-token rate, or a "BharatStudio fee". They see a rupee price and
a quantity of our units.

**Never say "tokens" to a customer.** A token is a provider-metered commodity; naming
it makes an implicit promise about a rate we do not control and complicates consumer
disclosure. The customer-facing units are **AI voice characters** and **AI credits**,
both defined by us, both re-priceable without breaking a promise. "Token" may appear in
internal cost models and nowhere else.

**Internally** we compute the bundle so that a margin of **25% or more** is retained
before the remainder is issued as units. **Decided 2026-09-13: 25% is a floor, not a
flat rate** — the actual figure is set per credit class, because premium vision work
costs many times a TTS call and one global percentage would over-charge the cheap
features and under-charge the expensive ones. The margin is a private input to the
conversion, never a line item, never disclosed, and never described as a commission —
because it is not one. Nothing is being taken from the creator's earnings.

Rules that keep this honest and safe:

- The quantity shown at purchase is what the creator gets. If provider cost moves, we
  change the bundle size **for future purchases**, never retroactively for units
  already sold.
- Units already purchased do not shrink, expire silently, or revalue.
- Consumption is metered in **our** units in the ledger, so a provider change never
  rewrites history.
- We never publish a per-unit provider cost, even in support conversations.
- Gateway fees on the purchase are our cost of doing business, never surfaced.

**Commission on creator earnings is, and stays, zero.** That is the positioning and
the top-up model must never blur it.

### 10.2 Top-up menu

**Two consumables, and nothing else** (§28.1.1). Anything that raises a standing limit
is a pack, not a top-up, and appears in §28 only.

| Top-up | Unit | Notes |
|---|---|---|
| **TTS characters** | packs of characters | Quota already metered (`0081`), so the ledger half exists |
| **AI credits** | micro / standard / premium (§11) | Largest long-run margin; paid tiers only |

**Moved to packs on 2026-09-14**, because each raises a standing limit rather than being
spent: asset storage · extra connectors · extra moderator seats · extra sticker and
media pack slots · priority alert-queue burst capacity · sponsor campaign slots ·
vertical and multi-canvas outputs. **Season Pass issuance** leaves both menus — it is
the creator's own monetisation product (§10.4), billed on its own terms.

**Never sold as a top-up (§12.6):** event retention, history depth, record search,
export, receipt access, audit access, or anything else that is a durable creator
record. An earlier draft of this menu listed "Event retention +30/+90/+365 days"; it is
deleted, and retention is now uniform for every tier.

Rules for every top-up: purchased balance is **additive to the tier allowance, never
a substitute** · clear disclosure of any expiry, and prefer no expiry on paid balances
· a spend cap and a confirmation step before large purchases · an append-only ledger
(grant, reserve, settle, release, refund, expiry) · admin cannot alter a balance
without an audited compensating entry.

### 10.3 Ingest and reward existing YouTube members

Free for us, high value to the creator.

Detect via the Members API (§4) that a donor is already a channel member. When a
member tips through BharatStudio, their alert card gets a **golden-diamond border, an
exclusive sound, and an AI voice upgrade**. The creator honours existing YouTube
loyalty on stream and we build no subscription engine.

Requires: member scope and eligibility, reconciliation against the API rather than
chat, and the identity link from §3 F01.

### 10.4 Stream Season Passes — one-time, no mandate

Instead of recurring auto-debit (blocked: no rail supports recurring), sell
**time-boxed passes**: ₹99 for a 30-day "Summer Gaming Pass" or "Tournament Pass".

- Paid by ordinary one-time UPI — **zero mandate failure**
- Grants VIP status, priority queue, highlighted chat for 30 days
- Expires naturally; the viewer simply buys another if they want to

This is the single best answer to the memberships blocker. It gives creators recurring
*revenue behaviour* without recurring *payment infrastructure*. Model it as periods
with explicit start/end, never a boolean.

### 10.5 Private custom room access — superseded by the Lobby Engine

**Decided 2026-09-13: dropped as a paid mechanic.** The original idea was a qualifying
tip (say ₹50) returning the room ID and password on the receipt screen — a real pain
point, since BGMI, Free Fire, Valorant and GTA RP creators currently type passwords
into Instagram DMs and Discord.

It is superseded by the Lobby Engine (§16), which solves the same problem better and
without selling a seat: private single-use seat tokens, codes revealed only after a
ready check, no code ever on stream, reserve promotion on no-show, and an auditable
selection policy shown before anyone joins.

**A seat is never bought.** Creators who want to reward supporters use the
*verified member priority* or *attendance priority* eligibility modes. That keeps one
eligibility model, one audit trail, and no fairness argument in chat.

### 10.6 Priority Question / AMA queue ("Super Questions")

A ₹100 tip to ask a question is common, and in fast gameplay the creator reads it and
forgets. Tag the tip as a **Priority Question**; it stays pinned in an "Unanswered"
tab in Companion; the creator answers during a lull and taps **Mark Answered**, which
triggers a green check on stream. The definition types already exist (`0105`); the
missing half is the viewer trigger (§2.2) and the Companion tab.

### 10.7 VIP Discord / WhatsApp role sync

Link a donor's Discord account and assign a **VIP Supporter** role when lifetime
support crosses a creator-set threshold (e.g. ₹500). WhatsApp community equivalent
where the API permits.

Needs: explicit viewer opt-in and OAuth · thresholds derived live from
`payments − refunds` (never a stored counter) · automatic role removal on refund
reversal · clear disclosure that spend drives a role.

### 10.8 Additional monetization worth building

- **Tip-to-unlock media** — a meme, sound or sticker plays only above an amount, from
  the approved catalogue with cooldowns
- **Team / squad goals** — supporters pick a side; both totals shown; no wagering
- **Sponsor-matched goals** — "Sponsor doubles the next ₹5,000"; needs the exposure
  log for proof
- **Clip bounties** — a viewer funds a clip request; creator marks delivered
- **Charity mode** — a stream or goal flagged charitable, with a distinct receipt
  template and a public total. High trust value in India; needs legal review.
- **Creator-to-creator raids with a carry-over goal** — the raiding channel's goal
  progress is displayed for a set window on the receiving stream
- **Merch / external link cards** on the tip page, no payment integration required
- **Scheduled "support windows"** — double-XP style periods where badges accrue
  faster (recognition only, never payment odds)

### 10.9 Integrations with tools creators already pay for

| Integration | Direction | Value |
|---|---|---|
| OBS (WebSocket, via desktop helper) | control | Core |
| **Elgato Stream Deck plugin** | control | Highest-leverage single integration — most serious creators own one |
| Streamer.bot / SAMMI / Mix It Up | events out + templates | Keeps power users |
| Streamlabs / StreamElements relay | events out | Migration bridge (§9) |
| Discord | role sync, webhooks | §10.7 |
| WhatsApp community | notify | India-specific |
| Google Sheets / Drive | batch export | Finance and sponsor reporting |
| Google Calendar | schedule | Stream planning, pass expiry |
| Notion | export | Creator ops |
| Canva / Figma | thumbnail handoff manifest | §11 |
| VTube Studio | scene/model triggers | VTuber segment |
| Spotify / music apps | **metadata only** | Now-playing card; never audio |
| MIDI / hotkeys | control | Producer setups |
| Tally / Zoho Books | finance export | Indian accounting reality |
| Razorpay | payments | Core |

Rule: every integration is either **user-installed and explicitly configured** or an
**official API with scoped OAuth**. No scraping, no undocumented endpoints, no
credential copying.

---

## 11. AI — sold as Bharat AI Credits

### 11.1 The framing

Creators buy **predictable feature credits**, never model tokens.

```text
AI Credits: 1,240 remaining
• 1 title pack: 8 credits
• 1 thumbnail concept: 25 credits
• 1 hour of live moderation: 30 credits
• 1 post-stream highlights pack: 60 credits
```

Internally we meter input, output, vision and runtime cost. Externally the unit is a
feature. **Never offer "unlimited AI"** — provider cost, abuse and high-volume chat
make it commercially dangerous.

### 11.2 The existing boundary, and why it is not enough

L23's assist seam (`0121`) is deliberately narrow, deterministic, provider-free, and
now wired but nav-less. It sends no donor text, payment data or viewer identity to any
model, and the shipping generator makes no network call at all.

That is a good foundation and **it is not a licence to widen the same endpoint**. Real
AI moderation reads donor messages, which is a different data classification. It needs
its own reviewed privacy and security path: explicit consent, a documented retention
rule, a named provider, a DPA, and a separate audit trail.

### 11.3 Live safety and moderation — highest retention value

- Hinglish / Romanized Indic toxicity detection
- Hindi, Tamil, Telugu, Punjabi, Marathi, Bengali and English transliteration-aware
  moderation
- **TTS-safe rewrite** — turn a borderline message into a sanitized spoken version or
  visual-only
- PII detection: phone, UPI ID, email, address, card-like strings, unsafe links
- Spam / repetition / raid detection
- **Clutch Mode AI** — detect unusual chat intensity, recommend muting TTS or going
  visual-only
- Moderator copilot — summarize chat, surface likely harmful messages
- Sponsor-safe mode — flag profanity, sensitive politics, adult content, brand
  exclusions

The pipeline, which preserves the money boundary:

```text
Tip received → payment remains immutable
             → rules + AI safety classify message
             → allow / visual-only / queue / moderator review
             → creator can override
```

**If AI credits run out, fall back to deterministic rules and visual-only safe
handling. A payment must never disappear because an AI provider is unavailable.**

### 11.4 Growth and post-stream packaging

- **Channel style profile** — language, Hinglish tone, title structure, emoji usage,
  game and category patterns
- Title, description, tag, pinned-comment and playlist suggestions
- **Thumbnail concept generator** — real game frame, creator-owned face cutout, native
  SVG/HTML typography, editable layers, **no AI-rendered text**
- **Editor handoff pack** — title ideas, frame timestamp, safe crop, face pose
  recommendation, visual hierarchy, PSD/Figma-ready export manifest
- VOD moment finder from chat velocity, event spikes, stream markers, manual tags
- Short-form clip recommendations with captions, hook text, aspect presets
- Multilingual title/description translation with creator review
- Post-stream recap: what worked, goal results, peak moments, likely clips, open
  technical issues

AI recommends; the creator approves. Same suggestion-and-audit shape as L23.

### 11.5 Companion AI Copilot — a producer in the pocket

One-tap prompts: "What is breaking?" · "Summarize chat in 10 seconds." · "Show only
messages needing moderation." · "Suggest a title change for the game I just switched
to." · "Write a sponsor mention in my tone." · "Give me three challenge ideas." ·
"What goal should I set based on today's support pace?" · "Prepare an end-stream
thank-you, but do not post it." · "Explain why my overlay/chat/tips are delayed." ·
"Turn this stream marker into a clip brief."

The assistant receives a **minimized, permissioned context bundle** — never
unrestricted chat history, payment records, private donor data or arbitrary creator
files.

### 11.6 Credit and tier design

| Tier | Included AI value | Credit behaviour |
|---|---|---|
| Free | Deterministic safety rules, limited title/copy suggestions, no vision | Small monthly trial allowance |
| Pro | AI copy, translation, light moderation, basic recap | Monthly credits + recharge packs |
| Creator | Real-time moderation, Channel DNA, thumbnail concepts, clip recommendations | Larger monthly pool |
| Studio | Shared team pool, producer/moderator roles, advanced vision, sponsor workflow, priority jobs | Pooled credits, cost controls, scheduled audit exports (a one-off export is free on every tier, §12.6.3) |

Three credit classes: **micro** (classification, translation, titles) · **standard**
(long summaries, content packs, thumbnail concepts) · **premium** (vision analysis,
frame selection, clip planning, batch analysis).

### 11.7 Billing flow

```text
Creator requests AI action
        ↓
Validate tier, role, consent, data classification, rate limit
        ↓
Estimate maximum credits and reserve them durably
        ↓
Run deterministic policy / model job
        ↓
Record model/version/usage class/result status
        ↓
Settle actual credit cost; release unused reservation
        ↓
Show suggestion or safe fallback
```

Rules: idempotency key prevents double charge on retry · provider timeout or failure
costs **zero** credits · duplicate request returns the original result · append-only
ledger (grant, reserve, settle, release, refund, expiry) · creator sees feature usage
and remaining credits, never raw provider tokens · admin cannot alter balances without
an audited compensating entry · disclose recharge expiry, and prefer none · cap daily
spend and confirm before expensive batch jobs.

### 11.8 What AI must never do

Generate "guaranteed viral" or CTR promises · automatically purchase or gift YouTube
memberships · make payout, refund, TDS/GST, tax or fraud decisions · auto-publish
supporter names or amounts · upload creator face assets, raw VODs or donor messages to
an external model without explicit consent and a documented retention rule · use
scraped channel data as model context · silently refund, permanently ban, change
payouts, or alter live configuration.

### 11.9 First AI build order

1. Safety rules + AI-assisted moderation queue
2. TTS-safe rewrite and PII protection
3. Title / description / translation assistant
4. Post-stream recap and moment recommendations
5. Companion live-producer summaries
6. Credit ledger, tier entitlements, recharge packs, spend caps
7. Thumbnail concept canvas from real frames and creator-owned assets

### 11.10 Voice routing — spend premium TTS only where it is worth it

Today every eligible alert goes to Sarvam (TTS-01) until the quota runs out, then falls
back to browser voice (TTS-04). That means a ₹20 "gg" and a ₹2,000 message with a
Tamil name cost the creator the same characters, and the quota is gone by the middle of
a good stream on the message that mattered least.

**Decided 2026-09-14: a creator-owned routing rule set, default off.**

#### 11.10.1 What decides the route

Deterministic, inspectable rules the creator sets in the dashboard. No model sits in
the live path.

| Rule | Sends to premium when | Why it is the right signal |
|---|---|---|
| **Amount** | The tip is at or above a creator-set bracket | The strongest signal, and it already exists — the amount ladder (TTS-03) governs TTS eligibility, so this extends a concept creators understand |
| **Length** | The message is under a creator-set character count | A 400-character message is being skimmed, not savoured. Short messages are where voice quality is actually heard |
| **Language / script** | The message contains Devanagari or another Indic script, or code-mixed Hinglish | This is the one thing browser voice genuinely cannot do. An English sentence on a browser voice is fine; a Hindi sentence is not |
| **Named supporter** | The supporter is a repeat or VIP supporter (opted-in relationship data) | Recognising a regular is worth more than a stranger's fifth tip of the night |
| **Event class** | Goal completion, milestone, sponsor moment | Moments the creator has decided matter |

Rules combine as **any-match sends premium**, with an explicit creator-set override
list. Script detection is a Unicode range check, not a classifier — cheap, offline,
deterministic and explainable.

**Deliberately not built: an AI classifier deciding whether a message "deserves" a good
voice.** It would cost credits to save credits, add latency to a live path, and produce
behaviour no support agent could explain when a creator asks why one tip sounded
different. Revisit only with measured evidence that the rules route badly.

#### 11.10.2 Defaults and control

- **Default off.** A new or existing creator's behaviour never changes without them
  choosing it. Turning it on is a two-tap preset ("Save credits: premium above ₹100 and
  for Indic messages"), then fully editable — the §15.2 customisation model.
- **The setting lives in the dashboard**, with a preview: "under last week's traffic
  this would have used about 38% of your characters".
- **Companion shows the active mode** on the Live Deck and can switch it mid-stream,
  including a one-tap "premium everything for the next 10 minutes" for a big moment.
- **A quota-saving nudge, never an automatic change**: at ~70% consumption (TTS-07) the
  dashboard may *suggest* enabling routing. It never enables it.

#### 11.10.3 Rules that keep it honest

- **Routing never changes whether an alert fires, is displayed, is acknowledged, or is
  recorded.** It changes one thing: which voice speaks. Correctness is untouched
  (§30.1).
- **Safety runs before routing, identically for both voices.** The §12.2 content suite
  and the Indic transliteration checks are not a premium feature and are not skipped on
  the browser path.
- **The chosen route and the reason are recorded** on the alert, visible in history and
  in the quota view. "Why did this one sound different" must always have an answer.
- **Provider failure still falls back** to browser voice and then to a chime (TTS-04),
  independent of routing.
- **Routing is a cost control, never a paywall.** It is available on every tier that has
  premium voice at all, is never itself sold, and is never used to make a lower tier
  sound deliberately worse than its quota already implies.
- **Never routes to premium to burn quota faster.** Any change we make to the default
  preset that increases premium usage is a pricing change and follows §20.4.

### 11.11 Quota exhaustion — continuity, never extra consumption

**Decided 2026-09-14.** When premium characters run out, synthesis falls to browser voice
**immediately**, with a notice in Companion and on the dashboard (TTS-17). No dead alert,
no silence, no delay — and **no grace buffer**.

A proposal for a 5% grace allowance was rejected, and the reason is recorded so it cannot
return:

- It is an **ungranted spend with no entry type** in the append-only credit ledger
  (§10.2), which lists grant, reserve, settle, release, refund and expiry. "Grace" is
  none of those.
- It **silently redefines the cap**. If the effective limit is 63,000, the limit is
  63,000, and the next conversation asks for another 5%.
- It solves a problem TTS-04 already solved. The guarantee the creator needs is
  *continuity*, not extra premium consumption.

The ladder stays **20K / 40K / 60K**. Rollover and a better Studio top-up rate are both
deferred and both blocked on the same open item — what a rupee of credit actually buys
(§33.2) — because units whose value is not fixed cannot be rolled over or discounted.

### 11.12 Safety classification cost — the ladder, and the cache

Running a model over every message is the most expensive design available and close to
the least accurate. Chat is enormously repetitive; abuse vocabulary is finite and slow to
change; and most of what arrives is `gg`, an emoji and a copypasta. The architecture
should exploit all three.

**The target: AI touches the residual band only — the small fraction that the
deterministic layers genuinely cannot decide — and its verdicts become deterministic
rules so the residual shrinks over time.**

#### 11.12.1 Decide as cheaply as possible, escalate rarely

The §12.2.3 ladder is a cost design as much as a safety one. L0–L2 run in microseconds on
our own CPU with no provider call. L3 is our compute. **Only L4 is metered**, and a
message reaches it only when the layers below abstain.

Two consequences worth stating plainly:

- **Each language's coverage is a cost curve.** English and Hindi corpora will be strong
  early, so their residual band is small. A low-resource language starts with a large
  residual and gets cheaper as its corpus fills.
- **Every AI verdict is an opportunity to never pay again.** A novel term the model
  catches is reviewed and promoted into the L1 corpus, after which it costs nothing
  forever. **The model's real job is to grow the list, not to judge every message.**

#### 11.12.2 The verdict cache

The product already content-caches TTS audio by SHA-256 (`TTS-01`). Safety verdicts use
the same shape:

```text
key   = HMAC(server_secret, normalised_text ‖ language ‖ policy_version)
value = verdict · confidence · deciding layer · matched rule
```

- **Normalised text, not raw**, so `fuuuck`, `f.u.c.k` and `ｆｕｃｋ` share one entry.
- **`policy_version` in the key** means a corpus or model change invalidates naturally —
  no purge, no stale verdict surviving a policy change.
- **Cross-channel by design.** A classification of a string is not channel-specific, and
  a shared cache is what makes the hit rate high. **Creator-specific rules are applied
  after the cache**, never baked into it.
- **HMAC with a server-side secret, not a bare hash.** A global store keyed on plain
  message hashes would be reversible by dictionary attack; keyed hashing removes that.
- **PII-flagged messages are never cached**, at all. If L0 detects a phone number, UPI
  ID, email or card-like string, the verdict is computed and discarded.
- **The cache stores verdicts, never message text.**

#### 11.12.3 Sub-message caching, which is where the leverage is

Whole-message caching helps with copypasta. **Term-level caching helps with everything
else.** Once a token or n-gram has a verdict, every future message containing it is
decided at L1 — so a single AI call on one novel slur immunises every later message that
uses it, in any spelling that folds to the same phonetic key.

This is why the corpus is the asset and the model is the tool.

#### 11.12.4 The other cost controls

| Control | Effect |
|---|---|
| **Batch the residual** | Classify the residual band in one call per short window rather than one call per message. Chat bursts batch naturally |
| **Signal-based escalation** | Escalate on signal — first-time author, unusually long, mixed script, contains a link, high amount — not on arrival order |
| **Spoken versus scrolling** | A message that will be **spoken to the audience** gets the full ladder. A message that only scrolls past in chat can stop at L3 unless it carries signal. The harm surfaces differ, and this is not tiering safety — every surface still runs L0–L3 |
| **Distillation** | Periodically retrain L3 on accumulated L4 verdicts. Cost decays monthly rather than scaling with traffic |
| **Negative caching** | Common benign phrases are cached as safe, which is most of chat |
| **Compiled per-channel matcher** | Global corpus plus creator terms compiled into one automaton per channel, rebuilt on change, held in memory |
| **Budgets** | Per-channel and global daily AI budgets, with the §4.4.5 degradation shape: slow, then stop escalating — **never stop running L0–L3** |

#### 11.12.5 The rules this optimisation may not break

- **Cost is never a reason to skip safety.** If the budget is spent, the deterministic
  layers still run and TTS still fails closed (§12.2.6). Degradation is visible to the
  creator.
- **A cache hit is not a weaker decision.** It is the same verdict, from the same policy
  version.
- **Nothing here is tierable.** The cheap path exists to make safety affordable for every
  creator including Free, not to give paid creators a better one.
- **AI moderation stays recommend-or-soft-action** (§11.8), cache or no cache.

#### 11.12.6 What gets measured

Cache hit rate overall and per language · residual rate reaching L4 · **cost per thousand
messages** · terms promoted into the corpus per week · false-negative reports from
creators · L3-versus-L4 agreement. All as histograms (`RT-06`), because a hit rate is a
distribution, not an average.

**Why this matters commercially:** AI moderation is a Creator-tier capability, not a
metered credit line — so its provider cost comes out of the tier margin, not the
creator's balance. Every point of cache hit rate is margin, and the §10.1 25% floor
depends on it.

### 10.10 Refunds — the whole flow, and what it costs us to get wrong

A refund is the only event that runs *backwards* through every derived number in the
product, so it is the best test of whether the architecture actually holds.

#### 10.10.1 Who can initiate one, and why that is the hard part

Razorpay supports refunds through its API — full and partial, with a normal and an
instant speed, and its own webhook events. **The provider is not the obstacle; our money
model is.**

In the creator-direct design the payment settles to the **creator's** account. The funds
are not ours, so the authority to reverse them is not ours either. Three ways out:

| Route | Verdict |
|---|---|
| **Creator refunds in the Razorpay dashboard; we reconcile from the webhook** | **Works today, zero new permission.** This is what ships first |
| **We initiate on the creator's behalf via partner OAuth with a refund scope on the linked account** | **The target.** Depends on `PAY-13` (partner OAuth config, currently unreachable) and on the Technology Partner approval that is already a v1 release gate |
| **We hold the creator's API keys and call as them** | **Never.** This is the §25.5 consumer-credential prohibition wearing different clothes |

So the register's "no rail reports `supportsRefunds: true`" is accurate about our
*abstraction* and misleading about the *provider*. Corrected here: **Razorpay supports
refunds; we do not yet hold the delegated authority to trigger one**, and that authority
arrives with the partner approval rather than with a code change.

**Every per-field and per-behaviour claim about the provider in this section carries the
§27.2 requirement** — a dated official source before it becomes a planning number. The
shape below is designed to survive being wrong about a field name; it must not be built
against memory.

#### 10.10.2 The data we must store, per refund

Reconciliation is impossible later if any of this is missing at the time:

| Field | Why |
|---|---|
| Our `refund_id`, and our **idempotency key** for the initiation attempt | So a retry never double-refunds |
| Provider `refund_id`, `payment_id`, `order_id` | The join back to the money |
| `amount_paise`, `currency` | Partial refunds mean the payment's amount is not the refund's amount |
| `status` and every transition, with timestamps | The state machine below |
| `speed_requested` and `speed_processed` | A requested instant refund can be processed as normal; the creator will ask why |
| `reason_code` (our taxonomy) and `reason_text` | Support, disputes and the Activity Log |
| `initiated_by` — creator, admin, provider-side, or system | Owner/admin only; operator and moderator never (§ role scoping) |
| `initiated_where` — our product or the provider dashboard | Out-of-band refunds must be recognised, not treated as anomalies |
| Provider event ID of each webhook | Dedup, exactly as payments already do |
| `arn` / acquirer reference, once available | The number a supporter's bank will ask for |
| Expected and actual credit timing | "When will I see it" is the only question a supporter asks |
| `failure_code` and `failure_reason` | A failed refund is a state, not an absence |
| Balance context at initiation | A refund against an already-settled payment can overdraw; see below |
| Link to the alert event, receipt and supporter identity | Every derived number and the receipt must reflect it |

#### 10.10.3 The state machine

```text
requested → accepted_by_provider → processing → processed
                     │                  │
                     │                  └→ failed → (retry | manual)
                     └→ rejected
processed → (reversed_by_bank)        ← rare, but it exists
```

Every transition is webhook-driven, idempotent on the provider event ID, and written to
the ledger as an append-only row. **We never infer a state from elapsed time.**

#### 10.10.4 What a refund must touch, and what it must not

**Recomputes automatically, because we derive rather than store (§19.6):** goal progress ·
leaderboards · badges · streaks · supporter reputation · season-pass eligibility · any
widget total. **This is the payoff of that decision** — there is no counter to decrement,
no badge to revoke, no leaderboard to rebuild, and a refund needs no special handling in
any of them.

**Updates:** the receipt, which already reflects live refund state (`VID-04`) · the
Activity Log (§7.5) · the payment's detail view timeline (§7.2) · the creator's payout
reconciliation view.

**Does not touch:**

- **The alert that already played.** It happened; the audience saw it. We do not rewrite
  the past on stream. The record shows the reversal; the stream does not.
- **TTS already spoken.** Same reason.
- **The stored message and its moderation history.** Durable records (§12.6).
- **The supporter's ability to support again.** A refund is not a punishment.

#### 10.10.5 The edge cases that decide whether this is real

| Case | Behaviour |
|---|---|
| **Partial refund, then another** | Track cumulative refunded amount; refuse to exceed the payment. Derived numbers use `paid − Σ refunds`, which already works |
| **Refund after settlement** | The creator's balance may be insufficient. The provider's behaviour governs; we surface it as a distinct, explained state rather than a generic failure |
| **Refund of a Compatibility-Routing signal** | **Impossible, and must fail loudly.** A routed signal is not a verified payment (§25.3). There is no money for us to reverse and no receipt to amend |
| **Refund before the webhook for the original payment** | Queue it; refunds are ordered behind their payment, never applied to a payment we have not yet recorded |
| **Duplicate refund webhooks** | One refund row, exactly as `PAY-02` handles payments |
| **Refund during a live stream** | No on-stream change of any kind. The creator sees it in Companion; the audience does not |
| **Chargeback or dispute** | **A separate state machine, not a refund.** Different timeline, evidence pack, provider-driven, and it can arrive months later |
| **Repeated refunds by one supporter** | A private risk signal on the creator's view (§12.11). Never an automatic block, never cross-creator |
| **Tax treatment** | Unresolved and gated on the CA review. **No refund copy may state a tax consequence** until then |

#### 10.10.6 What the creator and the supporter each see

- **Creator:** a refund action on the payment detail view (once delegated authority
  exists), a reason field that is required, an undo window before submission rather than
  a confirmation dialog, live status afterwards, and the effect on their goals shown
  immediately.
- **Supporter:** an honest status and an expected credit window, reachable from their
  receipt link with no login (`/r/[token]`), because the receipt token is the only thing
  an anonymous supporter has.
- **Neither sees** a silent change. A refund that fails is visible to both.

---

## 12. Hard boundaries — the rules that never bend

These are collected from every authority document. A feature that violates one of
these is not shipped, regardless of revenue.

### 12.1 Money

- `PlatformBilling` and `CreatorPaymentConnections` are separate modules and **must
  never share a table**
- The schema must never contain `creator_balance`, `withdrawable_amount`,
  `bharatstudio_held_funds`, or `payout_request` — verified absent across all migrations
- **No personal-UPI mode. No Android notification scraper. Ever.** Client-side UPI
  "success" is not proof of settlement
- BharatStudio holds no escrow and is never in the settlement path
- BharatStudio **cannot issue a refund** — only reconcile a status the provider
  reports. Any future feature must gate on `connectionCapabilities().supportsRefunds`,
  never assume it
- TipIntent tokens are opaque — never encode amount, name or message in a query
  parameter (fraudulent-alert risk)
- Never store banking credentials, even for a "preferred UPI app" preference. This
  explicitly governed Compatibility Routing (§25) until the 2026-09-13 owner decision.
  **Amended:** a delegated *business* credential may be held under conditions C1–C7
  (legal sign-off, provider terms verified, no sanctioned alternative, explicit consent,
  KMS/HSM envelope encryption, instant revocation, blast-radius controls). A *consumer*
  account password remains outside this exception
- No automatic multi-rail payment routing. Provider-neutral yes; automatic routing no
- Payment dedup must never derive from time or browser input — `X-Razorpay-Event-Id`
  with DB uniqueness across provider/environment/account/event
- Enterprise 85/15 is enterprise↔creator via Route at capture; BharatStudio takes 0%
  and is never the parent Route account holder
- Paytm: no "Connect Paytm" button until all eight written conditions are confirmed
- **Correctness is never a premium feature.** Payment verification, immutable records,
  webhook dedupe, reconciliation, refund tracking, queue durability, retry/replay,
  security, privacy, audit, accessibility, downgrade preservation and legal
  disclosures are on every tier including Free

### 12.2 Content safety — one pipeline, every surface

Current state: `provider.ts:28-29` strips C0/DEL control characters and bounds to 500
characters. **That is the entire filter.** Everything below is required before public
launch (`TTS-06`, P0) and is the single highest-harm gap in the register.

#### 12.2.1 One corpus, one pipeline, every surface

**Decided 2026-09-14.** There is exactly one safety pipeline and exactly one term corpus.
Tip messages, TTS input, chat (`BOT-06`), Super Chat when it lands in Phase 4, supporter display
names, sticker captions, lobby names and bot replies all pass through it. Two lists means
a term blocked in speech and permitted in chat, and neither list ever fully maintained.

```text
message
  → L0 normalise        → L1 exact match  → L2 fuzzy / phonetic
  → L3 local classifier → L4 AI (residual only)
  → decision: allow · mask · hold · block   (per surface, not global)
```

#### 12.2.2 L0 — normalisation, where most evasion dies

Evasion is cheap; normalisation is cheaper. Before any matching:

- **Unicode NFKC**, then strip zero-width (`U+200B-D`, `U+FEFF`), RTL/LTR overrides
  (`U+202A-E`, `U+2066-9`) and combining-mark floods ("Zalgo").
- **Homoglyph folding** — Cyrillic `а`, Greek `ο`, fullwidth forms and mathematical
  alphanumerics fold to their Latin equivalents.
- **Leet and separator folding** — `f_u_c_k`, `f.u.c.k`, `ph`→`f`, `0`→`o`, `1`→`i`,
  `@`→`a`, `$`→`s`.
- **Repeated-character collapse** — `fuuuuck` → `fuck`, with the original preserved for
  display.
- **Script detection and transliteration**: Devanagari, Bengali, Tamil, Telugu, Kannada,
  Malayalam, Gujarati, Gurmukhi, Odia. A Hindi slur written in Devanagari, in Latin
  transliteration, or code-mixed within an English sentence is **the same term**, and is
  matched by a phonetic key rather than by spelling.
- **The original text is never destroyed.** Normalisation produces a parallel form for
  matching; display, receipts and audit keep what the supporter actually typed.

#### 12.2.3 L1 to L4 — decide as cheaply as possible

| Layer | What it does | Cost |
|---|---|---|
| **L1 exact** | Aho–Corasick over the compiled corpus — global terms plus this creator's own list — on the normalised form. Whole-word and substring rules are separate, because `assist` must not match a substring slur | Microseconds, no provider |
| **L2 fuzzy and phonetic** | Bounded edit distance for typo-obfuscation, and a **phonetic key per script** (Soundex-class for Latin, a syllable-based key for Indic) so `bhosdi`/`भोसडी`/`bhosadi` collapse to one key | Microseconds, no provider |
| **L3 local classifier** | A small model running on our own CPU for context the lists miss — threats, sexual harassment, scam patterns, coordinated raids | Our compute, no provider |
| **L4 AI** | **The residual band only** — genuinely ambiguous, novel, or in a language where L1–L3 coverage is thin. See §11.12 for how this stays affordable | Metered |

#### 12.2.4 Decisions are per surface, not one verdict

One message can be **paid, displayed, unspoken and held for review** at the same time.
Each decision is independent and separately audited:

| Decision | Question |
|---|---|
| **Payment** | Never affected by content. A message is never a reason to reject money |
| **Public display** | Shown, masked, or withheld |
| **TTS** | Spoken, spoken after rewrite, or silent |
| **Stored record** | Always stored in full — it is a durable record (§12.6) |
| **Moderator review** | Queued for a human or not |

#### 12.2.5 Everything else required before launch

- URL removal or neutralisation, with an allow/deny domain list per creator
- **SSML-injection guard** — a message can never become synthesis instructions
- Blocked terms and blocked users, creator-configurable, per language
- Minimum amount for TTS
- **Moderator approval before TTS as a decision distinct from alert display**
- **PII detection** — phone, UPI ID, email, address, card-like strings — and the
  no-accidental-doxxing rule from §5.3
- Rate, flood, repeated-text and emoji-flood controls
- Slow mode, raid mode and a high-toxicity profile
- Policy presets: family-friendly · gaming · mature audience · sponsor-safe

#### 12.2.6 Failure behaviour — closed for speech, open for money

- **Safety unavailable → TTS does not speak.** Silence is a recoverable disappointment;
  a slur read aloud to an audience is not.
- **Payment and receipt are never blocked by a safety failure.** The money path does not
  depend on the classifier.
- **Display falls back to masked**, not to raw.
- The creator sees the degraded state in Companion and on the dashboard; the audience
  never does.
- Safety runs **identically before both voice routes** (§11.10.3). The browser-voice path
  is not a cheaper path with weaker checks.

#### 12.2.7 Untiered, auditable, appealable

- **No part of this pipeline is tierable** (§30.1). A Free creator's chat is not a less
  safe place, and no pack, tier or add-on may sell better safety.
- Every automated action records the original text, the normalised form, the layer that
  decided, the matched rule or model score, the confidence, the **policy version**, and
  the actor if a human was involved — visible in the Activity Log (§7.5).
- **AI recommends or soft-actions; it never bans** (§11.8). Permanent bans and any
  payment decision need explicit creator or moderator policy.
- A supporter-visible appeal path exists for a block, and a reversal is itself audited.

**Audio never blocks the picture, and its delay is bounded.** *Amended by owner decision
2026-09-16; the earlier absolute — "never waits for synthesis" — was replaced because it
bought latency at the cost of desync, and desync is what a creator actually sees.* A TTS
failure, quota exhaustion or safety rejection changes only whether a voice speaks. The
visual alert is released, displayed, acknowledged and recorded regardless.

What is bounded rather than forbidden is the wait: an alert may be held for **one**
synthesis attempt, already capped by the 2.5-second provider timeout, so that picture and
voice are released together. There is no unbounded wait, no retry-driven wait and no
second timeout. §19.0 RT-03 carries the full rule, including which failures may be
retried — and a timeout may not be, because a timeout is ambiguous about whether audio was
produced and billed.

Safety runs **before** synthesis and identically on both voice routes (§11.10.3). The
browser-voice path is not a cheaper path with weaker checks.

### 12.3 Privacy and viewer rights

- **Tipping must never require login, at any level, ever.** If a viewer-account outage
  ever blocks anonymous tipping, that is a P0
- Never claim history from a typed display name — only from OAuth-verified platform
  identity
- A creator must never see cross-creator viewer spend
- Public viewer profiles are opt-in and off by default; exact lifetime spend is
  private by default and never published
- **Deletion is BLOCKED on legal — not decided.** Corrected 2026-09-14: an earlier
  version of this bullet recorded archival deletion as decided on 2026-09-13, which
  contradicted §33.1 and §32 and is exactly the kind of stale text §35.1 rule 7 forbids.
  - The **engineering preference**, which is a preference and not a policy: no hard
    delete for a viewer or a creator; identifying fields (email, display name, contact)
    move out of the live columns into an archive so history and audit stay intact; a
    returning person is treated as new and never re-linked.
  - **It may not ship and may not be promised.** No deletion flow, and no
    account-deletion statement in product, terms or marketing, until the privacy/legal
    row in `05_SUPPORT_AND_EXTERNAL_EVIDENCE_REGISTER.md` is approved.
  - Three things are unresolved: DPDP erasure duties, statutory retention for payment
    records, and whether the archived identity may be plaintext at all — an email kept
    in an archive column is still personal data retained after an erasure request, so
    the defensible form is probably an irreversible hash, which still satisfies "keep
    the history, treat returners as new".
  - Both app stores require an in-app deletion route (CMP-78). That conflict is
    resolved **before submission**, not during review.
  - What ships meanwhile is **deactivation**, with a plainly worded statement of what is
    retained and why.
- Historical claiming must be idempotent, with repeat-claim and contested-claim tested
- Badges are explicitly non-financial and opt-in: *Supporter since 2026*, *3-month
  member*, *12-month member*, *Challenge Champion*, *10 Challenges Completed*, *Stream
  Streak ×5*, *Founding Supporter*, *Top 10 Supporter*
- Top supporter names are never auto-published without visibility consent

### 12.4 Diagnostics

- A trace ID is a bounded diagnostic value only — never an authorization credential,
  payment identifier substitute, request payload, or Prometheus label
- Canonical form `razorpay:<x-razorpay-event-id>`; never accepted from a client header
  as source of truth
- Propagation chain: verified webhook → `alert_events.trace_id` → outbox deliveries →
  Cloud Tasks `command.traceId` → worker evidence → overlay replay traceId
- Charset ASCII letters/digits/`-`/`_`/`.`/`:`, max 128 chars
- Prometheus labels must never contain trace, event, order, payment, account, donor,
  queue or user IDs
- Malformed correlation metadata fails or retries at the owning boundary — never
  replaced with `Date.now()`, a random value, or a client-supplied value

### 12.5 Naming and copy

- Avoid: "UPI donation alerts", "Cheap Streamlabs for India", "Razorpay alerts", "OBS
  alerts with Hindi TTS", "Super Chat alternative"
- 0% commission is a trust statement, not the headline differentiator
- Gateway-fee rule: state our 0% clearly, state the provider sets its own fees, never
  advertise "0% forever" as a property of the payment rail. Calculator handling is
  specified in §12.5.1
- No competitor names in rendered HTML
- One brand, one domain (`bharatstudio.in`), four product areas differentiated by a
  per-route accent token — Alerts gold, Stream broadcast red-magenta, Mirror cool
  cyan/steel, Companion inheriting Alerts gold while bundled. Everything else
  (typeface, spacing, card-bezel system, nav, footer, legal) is shared: four accents
  off one system reads as a family, four design languages reads as four weak brands
- Do not buy separate domains; 301 any defensive domains into sections

#### 12.5.1 The fee-display boundary — one rule, stated once

| Surface | Provider fees | Why |
|---|---|---|
| Pricing page, checkout, top-up menu, credit purchase, receipts, in-product copy | **Never shown** | These are BharatStudio prices. A provider fee is not part of one, and showing it invites the reader to treat our price as a pass-through |
| The public **tip-fee comparison calculator** | **Shown, on both sides, or the calculator does not ship** | A comparison that hides the rail's fee on one side is a misleading claim, which is worse than not comparing |

Rules that make the calculator safe to publish:

- **Which fees.** Only the provider's published standard rate for the exact instrument
  compared (UPI, card, netbanking), plus GST on that fee where it applies. Never a
  negotiated rate, never an estimate, never a competitor's rate we inferred.
- **Currency of the data.** Every figure carries the provider's published rate, the
  source URL and the date it was read, rendered on the page.
- **Owner.** Marketing owns the page; the payments owner signs off the figures. It is a
  content review, dated in the marketing snapshot (§20.4).
- **Staleness.** Rates older than **90 days** fail the marketing snapshot build. The
  calculator then renders in a degraded state — the comparison hidden, our 0% statement
  and a "rates being re-verified" note kept — rather than showing a stale number.
- **Never** implies a rail's fee will not change, and never presents another product's
  pricing as current unless it too carries a source and a date.

### 12.6 Durable creator records — never a tier, never a top-up

**Decided 2026-09-14. This is a hard boundary and it outranks every tier table, pack,
top-up and pricing decision in this document.** Where any other section disagrees, this
section wins and the other section is a defect.

#### 12.6.1 The five rules

1. **Never tier-gate storing, viewing, searching, fetching or exporting a durable
   creator record.** Durable records are: payments · receipts · refunds · the audit
   trail · supporter relationships · event history · configurations · layouts ·
   moderation history. Every one of these, in full, at every tier including Free, with
   no row cap, no date-range cap, no search restriction and no charge.
2. **Never charge to restore access to data we already accepted.** Not after a
   downgrade, not after a lapse, not after a payment failure, not ever. Data the
   creator gave us or earned through us is theirs at every price including ₹0.
3. **Tiering may limit only new active capacity** — active connectors, active widgets,
   AI usage, new media uploads, custom assets, team seats, automation volume. Capacity
   is what costs us money to run. History is not capacity.
4. **Over-quota assets after a downgrade become read-only or inactive, and stay
   viewable and exportable.** Deletion follows the published retention and deletion
   policy alone. A tier lapse is never a deletion trigger.
5. **"Event retention" is never sold.** Retention is a trust, privacy and legal
   position, not an upsell. Selling more of it says our default is deliberately short
   so we can charge to fix it, which is both a bad product and a bad answer under DPDP.

#### 12.6.2 Retention is uniform across every tier

**Decided 2026-09-14: one published retention policy, identical for Free and Studio.**
Per-tier retention windows are removed. A Free creator's payment history, audit trail
and moderation history are kept exactly as long as a Studio creator's.

**Uniform across tiers does not mean one number for every kind of data.** Retention is a
**schedule by data class**, published with effective dates, and every class applies
identically to Free and Studio:

| Data class | Schedule set by |
|---|---|
| Payment, receipt, refund and audit records | Statutory retention — the longest, and not ours to shorten |
| Supporter relationships and event history | The privacy/legal gate |
| Moderation history and its evidence | The privacy/legal gate, balanced against appeal windows |
| Configurations, layouts, presets | Retained while the account exists |
| Raw chat logs and other high-volume, low-value streams | The shortest class, and a product decision about what we ingest and index at all |

**The tier is never an input to any row of that schedule.** A class may have a shorter
window than another class; a creator may never have a shorter window than another
creator. Each window is a legal or product number, not a pricing one, and is published
with an effective date.

Consequences, so nobody re-derives them:

- The **Event retention top-up is deleted** from §10.2.
- Any per-tier history or retention limit anywhere in the register is a defect
  (CON-17 corrected accordingly).
- The **Storage Pack sells space for new uploads only.** It never buys back access to
  anything historical, and running out of storage never hides, truncates or deletes a
  record.
- Chat-log volume is managed by what we choose to **ingest and index**, uniformly, for
  everybody — never by charging one creator to keep what another keeps free.

#### 12.6.3 The one distinction: the data, versus doing work with it

Owning the data is free. Us doing continuous work on the creator's behalf is a service.

| Always free, every tier | Tierable |
|---|---|
| Download or fetch **all** of it, any time, in an open format, unrestricted | **Scheduled or automated delivery** into Google Sheets, Tally, a webhook or another tool — that is an active connector with a running cost |
| Search, filter and page the full history in product | Advanced *derived* analytics products built on top of the history |
| A one-off export at any scale | Automation volume and frequency |

The test: if the creator asks for their own records, that is free at any tier and any
size. If we run something on a schedule for them, that is a service and may be priced.
**A creator on Free is never told their history is unavailable — only, at most, that we
will not push it somewhere on a timer for them.**

### 12.7 Bounded data — no surface fetches more than it can safely display

**Decided 2026-09-14, and it is a hard boundary, not a guideline.**

> **No surface may fetch, render, subscribe to, or retain more live data than it can
> display safely.**

The browser, OBS and the phone receive **small, purpose-built projections**. They never
receive raw history. Every server response to a live surface is already aggregated,
capped and projected to the fields that surface actually paints.

This does not narrow §12.6 in any way. Durable records stay complete, searchable and
exportable — the rule is about **what a live surface pulls into memory in one go**, not
about what a creator can reach. Deep history is paginated, searched, or exported
asynchronously as a background job. It is never dumped into a dashboard or an overlay.

| Surface | What it may hold |
|---|---|
| **Dashboard** | A compact summary first. Each tab lazy-loads. Cursor pagination only. Lists over 50 rows virtualised. Search debounced. **Exports run as background jobs**, never by rendering thousands of rows |
| **Tip page** | Server-renders creator identity, presets and the payment form — nothing else. Player, reactions, wall, stickers and social embeds load after first paint and only if enabled |
| **Overlay** | One Master Canvas connection · a bounded event queue · current and next alert state · compact widget snapshots. **Never** all tips, supporter history, chat, or full goal transactions |
| **Widgets** | The server returns already-aggregated capped results — top 10 supporters, latest 5 tips, one goal number — never hundreds of rows for the client to reduce |
| **Media** | Pre-processed, CDN-ready assets. No database binary reads, no browser-side resizing, no arbitrary remote URLs, no unbounded Lottie or audio work in the browser |
| **Companion** | Push-driven, virtualised above ~50 rows, no continuous value held in React state (§19.8) |

Backend obligations that make it enforceable rather than aspirational:

- Strict cursor and payload limits on **every** endpoint, with field projections rather
  than `select *`.
- Query timeouts, so a pathological read fails fast instead of holding a connection.
- Every widget-backing query proven with `EXPLAIN ANALYZE`, checked in, and re-checked
  when the query changes. A sequential scan on `payments` behind a widget is a
  production incident waiting for a popular creator.
- Derived-cache invalidation driven by the event (§19.6), never by polling.
- **Backpressure before a read can harm payment traffic.** The payment path has priority
  over every widget, dashboard and analytics read, and that priority is enforced, not
  assumed.

**Of the two violations named here, one is closed and one is not.** Idle overlays polling
every two seconds (RT-01) was corrected on 2026-09-15 — a connected idle overlay now issues
zero store reads. **Standalone widgets still each open their own live transport** (§21.3):
`apps/web/app/overlay/widgets/shared/overlay-transport.ts` states in its own comment that it
holds "one long-lived connection per widget instance", so twelve widgets remain twelve
connections. Collapsing that is PRF-02, in progress. Until it lands the experience may not be
described as smooth, and §19.4's marketing ban stands regardless because RT-07 is Blocked.

### 12.8 One message, end to end — the story

Machinery is easier to check against a narrative than against a spec. This is one real
message, from typing to appeal.

**A supporter tips ₹500 and types a message containing a slur written as `f.u.c.k`, plus
a Hindi insult in Devanagari, plus their phone number.**

1. **The money is never in question.** The payment is captured, verified, recorded and
   receipted. Nothing about the text can reject it (§12.2.4). This is the rule everything
   else hangs from.
2. **L0 normalises.** `f.u.c.k` loses its separators; the Devanagari term is transliterated
   and reduced to its phonetic key; the phone number is detected as PII. The original text
   is untouched and stored exactly as typed.
3. **L1 matches**, twice: an English T1 term and a Hindi T1 term, both on the phonetic key
   rather than the spelling. **No provider call.** Microseconds.
4. **The verdict is not cached**, because L0 flagged PII (`SAF-21`). Computed, used,
   discarded.
5. **Four independent decisions** (§12.2.4): payment — recorded. Display — masked. TTS —
   silent. Record — stored in full. Review — queued, because ₹500 is above the creator's
   review threshold.
6. **The overlay shows** the alert with a masked message. The creator's audience never
   sees the slur or the phone number.
7. **Companion buzzes** the creator: a ₹500 tip, held for review, with the reason. One tap
   shows the original, because the creator is allowed to see what was actually said about
   them.
8. **The Activity Log records** the automated action: original, normalised form, the layer
   that decided, both matched rules, the policy version, and that no human was involved
   (`SAF-18`).
9. **The creator sets a rule**: auto-timeout on a T1 match. The next such message from the
   same supporter triggers it — and the timeout carries an **evidence snapshot** (§12.10),
   so three weeks later the creator can still see exactly why.
10. **The supporter appeals** from their receipt link. The appeal, the reviewer and the
    outcome are all audited, and a reversal is as visible as the block was (`SAF-19`).
11. **Nothing here was tiered.** A Free creator's message travelled the identical path,
    with the identical latency (`SAF-17`).

**Where AI appears in this story: nowhere.** Both terms were already in the corpus. AI
only enters when the corpus does not know a term yet — and then its verdict becomes a
corpus entry, so it never pays for that term again (§11.12.3).

### 12.9 The corpus — seeding, growth and governance

#### 12.9.1 Seed small and precise, not large and noisy

**Do not import a public profanity list wholesale.** They are noisy, they cause the
Scunthorpe problem, and several include words that are ordinary in Indic languages. A
public list is a source of **candidates**, each reviewed before it ships.

| | |
|---|---|
| **Launch set** | English and Hindi/Hinglish only — roughly 300–800 unambiguous terms each |
| **Wave two** | Marathi · Bengali · Telugu · Tamil · Kannada, matching the §5.6.2 language waves |
| **Per-term record** | surface form · language · script · phonetic key · severity tier · whole-word or substring · source · added-by · reviewed-by · date · policy version |
| **T1** | Always blocked, never spoken — slurs, sexual violence, threats |
| **T2** | Masked in display, never spoken |
| **T3** | Context-dependent — a signal to L3/L4, never a hard rule |
| **Owner** | One native speaker per language **who actually streams**. Machine-translated abuse lists are worse than none |
| **Allowlist** | Legitimate words containing a banned substring, maintained alongside — this is the fix for `assist`, `Sussex`, `classic` |

#### 12.9.2 The growth flywheel

```text
message the corpus cannot decide
  → offline batch classification (§11.12.1)
  → candidate term with context and frequency
  → native-speaker review: accept · reject · mark T3
  → corpus entry, new policy_version
  → every future message with that term decides at L1, free, forever
```

**Near-miss telemetry is how we catch the next spelling.** Anything at edit-distance one
or two from a banned term that did *not* match is logged as a candidate. That is how
`phuck` gets added before it spreads, rather than after.

#### 12.9.3 Governance

Corpus changes are versioned, audited and reversible — the same shape as the capability
registry (§20). A term addition names its reviewer. A removal names its reason. The
`policy_version` bump invalidates cached verdicts automatically (§11.12.2), so there is no
purge step and no stale verdict outliving its rule.

### 12.10 Evidence and retention for moderation actions

The rule that makes short retention compatible with long accountability:

> **Snapshot the evidence at action time. Do not retain the firehose.**

| What | Retention |
|---|---|
| **Action record** — the timeout, ban, hold, mask or block | Long. Moderation history is a durable record (§12.6) |
| **Evidence snapshot attached to it** — original text, normalised form, matched rule, layer, confidence, policy version, actor, and **±N surrounding messages** | Lives with the action record |
| **Raw chat never acted on** | The shortest retention class (§12.6.2) — enough for appeals and context, then gone |
| **Appeal record** | With the action, including the outcome and reviewer |

So a creator asked "why was this person timed out three weeks ago" has a complete answer,
and we are not storing every message anyone ever typed to get it.

### 12.11 Flags and cross-creator signals — share signals, never verdicts

| Scope | Position |
|---|---|
| **A creator's own flag and block list** | Fully supported. Their channel, their data |
| **A global shared blacklist** | **Never.** §16.3 already prohibits a permanent blacklist keyed on Google or UPI identity |
| **A cross-creator risk *signal*** | Defensible only as a hint: *this identity has been actioned by several creators recently*. Decaying, never naming which creators, never auto-actioning, keyed only on OAuth-verified platform identity and **never on payment identity**. Gated on DPDP review — phase G |

The distinction that keeps it safe: a risk signal **orders a moderation queue**; it never
bans anyone anywhere they have not been. Nobody arrives pre-punished.

### 12.12 Supporter reputation — derived, private where it is negative

Computed live, never stored as a score — `0120` already raises rather than storing one,
and §19.6 governs.

- **Inputs:** payments minus refunds · tenure · consistency · actioned events · appeal
  outcomes.
- **Positive signals may be visible** — badges, *supporter since* — subject to visibility
  consent. **Negative signals are private to that one creator.** Never a public lifetime
  total (§12.3).
- **Used for:** auto-approving trusted supporters, TTS eligibility hints, queue priority,
  lobby attendance priority, and the named-supporter rule in voice routing (§11.10).
- **Guardrails:** it decays, it is appealable, it is never shared as a negative across
  creators, it is never permanent, and it is **never purchasable** — no tier, pack or
  top-up may raise it.

---

## 13. Portability — "I can leave with my data"

A stated switching reason (§1, "what would make a serious creator switch"), so it is a feature with an owner, not a compliance
afterthought.

- Export layouts, scene profiles and Master Canvas configuration
- Export events, receipts and the payment ledger (CSV and Sheets)
- Export supporter relationships subject to viewer consent
- Export moderation audit and sponsor exposure logs
- One-click rollback of the OBS migration (restore hidden sources)
- Downgrade never deletes accepted payments, refunds or audit history, and **never
  narrows search, filtering or export** either. Corrected 2026-09-14: this bullet
  previously said downgrade "narrows the dashboard search window", which directly
  violates §12.6. Durable records stay fully reachable at every tier including Free
- On downgrade, excess queues pause newest-first and are never deleted; stored assets
  over the new quota become read-only, never deleted
- Grandfathered price held 12 months from subscription start, with a 30-day renewal
  grace

---

## 14. Out of scope

Recorded so it is not rediscovered as a "gap" in six weeks.

| Product | Repos | Status here |
|---|---|---|
| **Mirror** | `stream-mac`, `stream-windows` | Out of scope. Screen mirroring from phone to desktop. |
| **Stream** | `stream-ios`, `stream-android` | Out of scope. Mobile live-streaming apps. |
| **Desktop Companion** | `companion-desktop` | Not a product surface. May persist as a local **mechanism** only — OBS control, and the Streamer.bot / SAMMI / Mix It Up adapters in §9.6. `localhost` only, explicit pairing, creator-chosen action allow-list, never a public port, never an arbitrary command. |
| **Platform** | `bharatstudio-platform` | Out of scope. Cross-product identity and store entitlements. |

The Companion catalogue's `mirror_*` (3) and `stream_*` (2) actions stay in the enum
and stay permanently inactive — `0093` already hard-codes their activation false
because those products emit no liveness signal. That is now the correct end state, not
a gap.

The **`is_platform_admin`** concept and the admin console remain in scope: they are
BharatStudio staff operations for Alerts, unrelated to the Platform service.

One naming item survives the cut: **"Companion" collides with Bitfocus Companion**, an
established Stream Deck / OBS controller.

**Decided 2026-09-13: keep the name.** The collision is accepted as a known store-search
and SEO risk. It is a real risk — the collision sits directly in our category, which is
the worst case for discovery — and the mitigation is brand-led rather than nominal:
always ship as "BharatStudio Companion", never bare "Companion", in store titles,
subtitles and keywords. Revisit only if store search data shows it costing installs.

---

## 15. Customisation and tier gating — the universal model

**Every feature and every widget is optional, configurable, and tier-gated.** A
creator decides what exists on their stream and page; the tier decides what they are
allowed to reach for. This is one mechanism applied everywhere, not per-feature
improvisation.

### 15.1 Four independent switches per capability

| Switch | Owner | Question |
|---|---|---|
| **Entitled** | Tier / top-up | May this creator use it at all? |
| **Enabled** | Creator | Do they want it? |
| **Configured** | Creator | How does it look and behave? |
| **Active** | Runtime | Is its dependency live right now? |

All four must be true for anything to appear. This is the existing two-layer
entitlement/activation gate extended with the creator's own on/off and configuration —
the same shape L24 already proved, applied universally.

### 15.2 What "customisable to the max" means concretely

Per widget or module: show/hide · position, size, z-order, anchor to one of the 9 safe
zones · theme, colours, fonts, corner radius, opacity · animation in/out, duration,
easing, or none · sound on/off and which sound · data window (stream / daily / monthly
/ open) · which contribution sources count (UPI tips, Super Chats, memberships —
independently) · privacy scope · thresholds that change appearance · empty-state copy
· language.

Per alert: per-amount-bracket styling, sound, duration, TTS eligibility and character
limit · per-source styling (a Super Chat may look different from a UPI tip) · per-queue
routing and mode.

Per page: layout preset by event type · which lanes appear (free lane, community lane,
growth lane) · copy overrides · which modules the viewer sees.

### 15.3 Gating rules

- A locked capability is **shown, labelled, and explains which tier unlocks it** —
  never silently hidden and never a dead control. This is the existing disabled-slot
  rule generalised.
- Downgrade never deletes configuration. Over-limit items become read-only or paused,
  exactly as queues and assets already do, and reactivate on upgrade.
- A creator's configuration survives our defaults changing.
- **No switch may ever gate a durable creator record (§12.6).** Storing, viewing,
  searching, fetching and exporting payments, receipts, refunds, audit trail, supporter
  relationships, event history, configurations, layouts and moderation history are
  outside the four-switch model entirely — there is no entitlement row to turn them
  off, and the capability registry rejects an attempt to create one. Only *new active
  capacity* is gateable.
- Over-quota assets after a downgrade go read-only or inactive and stay viewable and
  exportable. Deletion follows the published retention policy alone; a tier lapse is
  never a deletion trigger.
- Preset bundles ("Gaming night", "Charity goal", "Podcast", "Tournament") are one-tap
  starting points, then fully editable — presets must never be a separate,
  less-configurable path.

### 15.4 Customisation by tier — three levels, six surfaces

Added 2026-09-14. §15.2 says how deep customisation goes; it never said **who gets which
depth**, and it only covered the overlay and the tip page. The dashboard, the moderator
view, Companion and transactional mail had no customisation model at all.

#### 15.4.1 Three levels, and what each is for

| Level | Name | What it is | Tier |
|---|---|---|---|
| **0** | Presets | Choose from first-party designs, change nothing structural | **Free** |
| **1** | Safe presentation | Colour, layout, typography, sound, motion | **Pro** |
| **2** | Advanced creator control | Conditional rules, per-scene variants, multilingual copy | **Creator** |
| **3** | Brand and team | Brand kits, team approvals, multi-surface templates | **Studio** |

Levels are cumulative. Each is a capability-registry row, so a level can be retiered
without a release.

#### 15.4.2 The protected string class — enforced, not reviewed

**A creator may never override payment, legal, security, consent or error text.** This is
the same kind of rule as the protected watermark layer (§30.6.1): the customisation
system does not expose these strings at all, so there is nothing for a reviewer to catch
later.

| Protected | Why |
|---|---|
| Payment amounts, currency statements, "this is not refundable", fee and settlement wording | Consumer protection. A creator rewriting payment copy is a misrepresentation we carry |
| The read-aloud consent checkbox and every consent prompt | DPDP. Consent that has been reworded is not the consent that was reviewed |
| Refund policy, terms links, privacy notices, issuer identity (§30.6.4) | Legal documents are ours to word |
| Security and account messages | A rewritten security notice is a phishing template |
| Error text on a payment, auth or delivery failure | The supporter must be told what actually happened |

Everything outside that set is fair game — headings, labels, thank-yous, empty states,
preset names, module copy — per language.

#### 15.4.3 Overlay and Master Canvas

| Capability | 0 | 1 | 2 | 3 |
|---|---|---|---|---|
| First-party presets · premium first-party set at level 3 | yes | yes | yes | yes |
| Colour from our palette · free colour choice at level 1 | palette | free | free | free |
| Fonts from our set · **uploaded fonts** at level 3 | — | our set | our set | **uploaded** |
| Position, size, anchor to the 9 safe zones | — | yes | yes | yes |
| Show/hide, z-order, opacity, corner radius | — | yes | yes | yes |
| Animation in/out, duration, easing, or none | — | yes | yes | yes |
| **Reduced-motion variant** of every animation | — | yes | yes | yes |
| **Performance mode** — strips blur and shadow for a weaker encoding PC | — | yes | yes | yes |
| Per-widget sound, fade in/out, loudness target | — | yes | yes | yes |
| Amount rendering: ₹1,000 / ₹1K / bracket name only / hidden | — | yes | yes | yes |
| Name rendering: platform name / creator alias / anonymous, mask style, max length | — | yes | yes | yes |
| Message rendering: line clamp, emoji and sticker scale, censoring style | — | yes | yes | yes |
| **Indic script fallback order** per text role | — | yes | yes | yes |
| A font per role — name, amount, message — with its own size, weight, tracking | — | — | yes | yes |
| Per-bracket and per-source styling | — | — | yes | yes |
| Burst behaviour: stack, replace or queue when two land together | — | — | yes | yes |
| Do-not-interrupt windows tied to a scene | — | — | yes | yes |
| **Per-scene-profile placement and theming** | — | — | yes | yes |
| **Per-aspect-ratio variants** (16:9, 9:16, 4:3) of one canvas | — | — | yes | yes |
| *Owner decision 2026-09-16 — the vertical layout itself is **Pro**, per §30.3's tier table, which binds. This row covers something different and narrower: maintaining **three** aspect-ratio variants of one canvas as a customisation system. A Pro creator gets a vertical layout; keeping 16:9, 9:16 and 4:3 variants of the same canvas side by side stays Creator. §6 module #14 is the Pro thing, CST-08 is this row.* | | | | |
| **Conditional themes**: festival date ranges (Diwali, Holi, Eid), time of day | — | — | yes | yes |
| **Sponsor-safe mode** — swap to a neutral theme for a segment, swap back | — | — | yes | yes |
| Overlay theme follows the OBS scene automatically | — | — | yes | yes |
| Multilingual overlay copy and number formatting | — | — | yes | yes |
| **Brand kit** — palette, type, logo saved once and applied across every surface | — | — | — | **yes** |
| **Multi-surface templates** and package authoring with approval | — | — | — | **yes** |
| Layer groups, lock, snap, guides, alignment, solo-preview | — | — | — | yes |
| **Adversarial preview** — long Tamil name, 500-char message, emoji flood, before it happens live | — | yes | yes | yes |

#### 15.4.4 Tip page

| Capability | 0 | 1 | 2 | 3 |
|---|---|---|---|---|
| Name, avatar, amount presets, one accent colour | yes | yes | yes | yes |
| Cover image, background colour, avatar shape, tagline, social row order | — | yes | yes | yes |
| Module show/hide and lane order (free, community, growth) | — | yes | yes | yes |
| **Labelled amount presets** — "Chai ₹49", "Fuel ₹199" — with min, max and default | — | yes | yes | yes |
| Custom amount on/off, quick-pay chips | — | yes | yes | yes |
| Copy overrides on non-protected strings (§15.4.2) | — | yes | yes | yes |
| Privacy display: names, initials or nothing · hide amounts · anonymous default | — | yes | yes | yes |
| FAQ block, "where support goes" text, trust row | — | yes | yes | yes |
| Message settings: char limit, required or optional, read-aloud opt-in | — | — | yes | yes |
| Which sticker and sound packs are offered | — | — | yes | yes |
| Event layout presets, campaign and referral pages | — | — | yes | yes |
| Multilingual copy sets, language selector or auto-by-browser | — | — | yes | yes |
| Low-bandwidth default, player off, high-contrast variant | — | yes | yes | yes |
| **Full theme including background media, brand kit applied** | — | — | — | **yes** |
| **Multiple campaign pages per account**, each with its own theme, goal, copy and countdown, scheduled open and close | — | — | — | **yes** |
| Per-page OG image, title and description for sharing | — | — | yes | yes |

#### 15.4.5 Dashboard

| Capability | 0 | 1 | 2 | 3 |
|---|---|---|---|---|
| Dark / light / system | yes | yes | yes | yes |
| Accent colour | — | yes | yes | yes |
| Density comfortable or compact, default landing tab | — | yes | yes | yes |
| Pin and reorder home cards | — | — | yes | yes |
| **Named saved views** with filters and sort, for payments, moderation and supporters | — | — | yes | yes |
| Saved export column sets | — | — | yes | yes |
| Notification choices, digest cadence, quiet hours | — | yes | yes | yes |
| Timezone, week start, fiscal month, number format | — | yes | yes | yes |
| Keyboard shortcut map | — | — | yes | yes |
| **Logo and brand accent across the dashboard, per-role default views** | — | — | — | **yes** |

**No background images at any tier.** The dashboard is where people read numbers; a
background image breaks the contrast floor in §37.7 and buys nothing. Logo and accent
give the same ownership feeling without the harm.

#### 15.4.6 Moderator and operator view — preference versus policy

The distinction matters, and neither existed before. A **preference** belongs to the
person; a **policy** belongs to the channel and a moderator cannot customise their way
out of it.

| Per-moderator preference | 2 | 3 |
|---|---|---|
| Queue-first or chat-first layout, column choice, message density | yes | yes |
| Which quick actions appear and in what order | yes | yes |
| Notification and sound preferences | yes | yes |

| Channel-enforced policy | 2 | 3 |
|---|---|---|
| Blocked terms per language, including transliterated variants | yes | yes |
| Link domain allow and deny lists | yes | yes |
| Auto-hold rules and escalation targets | yes | yes |
| Canned responses per language | yes | yes |
| Shift handover notes, audit filters | yes | yes |
| **Team-managed policy libraries, approval workflows, per-moderator view layouts set centrally** | — | **yes** |

**Permission classes themselves are never customisable.** Owner, admin, operator,
moderator and viewer are fixed by the launch authority, and §24 places RBAC beyond
owner/moderator in Enterprise, which is blocked. Studio gets presets, libraries and
layouts inside those classes and never a new class.

#### 15.4.7 Companion

| Capability | 0 | 1 | 2 | 3 |
|---|---|---|---|---|
| Live Deck slot layout, within the tier's slot and page-size allocation (§30.4) | yes | yes | yes | yes |
| Which stats sit on the top strip | — | yes | yes | yes |
| Which health signals are shown | — | yes | yes | yes |
| One-hand mode, left or right | yes | yes | yes | yes |
| Colour-blind palette, haptics on/off | yes | yes | yes | yes |
| Language override, independent of device language | yes | yes | yes | yes |
| Notification types and quiet hours | tier-limited | yes | yes | yes |
| Saved deck presets per stream type | — | — | yes | yes |
| **Team decks — a layout pushed to every operator** | — | — | — | **yes** |

Accessibility settings are level 0 on purpose. One-hand mode, colour-blind palettes and
language are not premium features.

#### 15.4.8 Receipts and transactional mail

| Capability | 0 | 1 | 2 | 3 |
|---|---|---|---|---|
| Creator name and avatar on the receipt | yes | yes | yes | yes |
| Creator logo and accent | — | yes | yes | yes |
| Custom thank-you copy, per language | — | — | yes | yes |
| Reply-to address | — | — | yes | yes |
| **Brand kit applied, custom follow-up link block** | — | — | — | **yes** |

All of it sits inside §30.6.4: the creator's brand goes on it, our issuer identity stays
as a legal line, and every protected string in §15.4.2 is untouchable.

#### 15.4.9 Rules that apply to all of it

- **Every row above is a capability-registry entry** (§20), retierable without a release.
  These are starting positions, to be tuned on real usage.
- **Customisation never reaches a durable record** (§12.6) and never changes correctness
  behaviour (§30.1).
- **No customisation may increase what a live surface loads** (§12.7). A theme is data the
  renderer already holds; it is never a reason to fetch more.
- **The protected string class is enforced by the customisation system**, not by review.
- Every customisation row carries its §31.0 metadata and the §37.11 suites for its area —
  a theme that fails contrast or breaks at +40% text expansion is a defect, not a taste
  question.

---

## 16. Lobby Engine — a Game Session Manager

Positioned as trustworthy queues and private access, **not** a paid lobby engine.

> "Run community games from one Companion screen — fair queues, private codes, no
> leaked rooms, no Discord chaos."

### 16.1 Core flow

1. Creator opens a session: game, region, mode, platform, time, seats, reserve seats,
   queue policy.
2. Viewer joins with their BharatStudio account and in-game name.
3. They enter a **public waitlist** — the room code is never on stream.
4. Creator runs a **ready check**.
5. Selected players receive a **single-use, short-lived private seat token**.
6. The room code is revealed **only after they confirm readiness**.
7. No-shows lose the seat; reserves are promoted automatically.
8. Session ends with feedback, report options, and automatic deletion of temporary
   lobby data.

The public overlay shows **aggregate status only**: "8/16 seats confirmed", queue
count, next round, and opted-in initials or avatars. Never player identifiers, never
Discord names, never codes or passwords.

### 16.2 Eligibility — creator-selectable, and not "tip ₹X to enter"

Starting from paid entry creates fairness problems and, depending on selection rules,
can resemble paid access or a chance-based scheme.

| Mode | Good use |
|---|---|
| Open FIFO queue | Community games, early adoption |
| Creator / mod pick | Competitive or trusted lobbies |
| Verified member priority | A clear membership benefit |
| Attendance priority | Rewards regular participation, not spending |
| Invite-only | Scrims, collaborators, sponsors |
| Free transparent draw | Only with published rules, cooldowns and legal review |

The selection policy is **locked and displayed before anyone joins**, with a redacted
audit log: join time, selection method, promotion, no-show expiry, moderator override
and reason. Per-stream caps, per-user limits and cooldowns apply throughout.

**Corrected 2026-09-14.** An earlier draft of this section let a qualifying tip return
a room code on the receipt. That contradicted §10.5 and the decision register, and it
recreated exactly the pay-to-access mechanic the Lobby Engine exists to remove. It is
**deleted, not narrowed**. No payment, of any size, at any tier, ever returns a seat, a
code, a password or a place in a queue. A creator who wants to reward supporters uses
*verified member priority* or *attendance priority*, which are eligibility inputs and
never a purchase. One eligibility model, one audit trail, no fairness argument in chat.

### 16.3 Explicitly not built

- **Paid roulette.** Random selection tied to payment is a regulatory, trust and
  support burden.
- **Cashback, wagering, "loser pays" bounties, peer-to-peer prize pools.** Replace
  with creator-funded prizes, cosmetic recognition, community milestones and
  non-cash achievements.
- **Permanent blacklist keyed on Google or UPI identity.** Payment identity is never a
  punishment key. Use account-level, evidence-backed, **time-bound** lobby suspensions
  with an appeal path and human review.
- **Paid WebRTC hotline.** Real-time calling needs TURN infrastructure, consent,
  moderation, recording disclosure, abuse response and age safety.
- **Viewer image or file uploads.** Our scanning is a documented no-op; this is not
  buildable safely today. If ever built: allowlisted types, content validation,
  generated filenames, size limits, isolation, malware scanning and human approval
  before display.

A safe first "roast my setup": text or a YouTube URL, manually approved by the
creator, with no automatic fetching and no overlay playback.

### 16.4 What makes it genuinely better

**Ready check plus reserve bench** is the highest-value feature — it removes dead
airtime, which is the actual pain. Then: no-show automation with configurable grace and
one-tap skip · session templates (BGMI TDM, Free Fire customs, Valorant 5-stack, GTA RP
recruitment) · language, region, platform and accessibility filters (mic optional,
beginner-friendly, family-safe) · voluntary skill bands and friend-group locking, never
hidden ratings · creator squads where co-hosts run the queue with attributed actions ·
lobby reputation from attendance and respectful play, **no public shaming** ·
post-match "would you queue with them again?" with private reporting · **clip consent**
before featuring a player's gameplay or voice · cross-creator combined queues with each
side keeping its own moderation boundary · sponsor activations with no purchase
requirement and transparent terms · recurring community nights with reminders,
check-in windows and analytics.

### 16.5 Screened Guest Queue — instead of paid calls

Viewer submits a short text or voice note · creator selects one · creator may invite
them to an **audio-only, time-boxed** guest slot · identity stays inside BharatStudio
with no phone number exposure · explicit consent, one-tap eject, report, session
expiry. A true live guest-call feature comes only after media relay, moderation,
incident and privacy controls exist.

### 16.6 Lobby delivery order

1. **MVP** — free queue, private seat delivery, countdown, ready checks, reserve
   seats, code expiry, Companion controls, safe public overlay
2. **Trust** — roles, audit log, no-show controls, reports, suspension and appeal,
   account/device abuse limits
3. **Community** — member priority, attendance rewards, filters, templates, recurring
   events, post-session feedback
4. **Collaboration** — cross-creator lobbies, creator-funded prizes, sponsor
   activations, tournament brackets
5. **High-risk media** — screened guest calls and approved submissions, only after
   real scanning, moderation, legal and infrastructure evidence

---

## 17. Giveaways and tournaments

Both are creator-hosted, both are tier-gated, and both are **non-cash by default**.

### 17.1 Giveaways

Creator defines: prize (described, creator-supplied, never held by us), entry method,
entry window, and draw method — all published before entry opens.

Entry methods, creator-selectable: free entry · follow/subscribe check where the API
permits · attendance-based · supporter-status-based (opt-in) · **never a paid-only
entry**. If a creator wants supporters weighted, the weighting is published up front
and a free entry route must remain.

Draw: deterministic and auditable. Server-side seeded draw with the seed and entrant
count recorded, a redacted audit log, and a result the creator cannot silently
override — an override is possible but is logged and labelled as an override.

**Decided 2026-09-13: free-entry and skill-based formats only.** No chance-based
giveaway ships until counsel signs off, and supporter-weighted odds are not built. This
removes the lottery question entirely rather than managing it.

Boundaries: **BharatStudio never holds, escrows, ships or guarantees a prize.** The
creator is the promoter and is responsible for eligibility, taxes and delivery; our
terms must say this plainly. No random-chance mechanic may be gated behind payment.
Skill-based and free-entry formats are strongly preferred, and anything resembling a
lottery needs legal review before it ships in India.

Overlay: entry count, time remaining, winner announcement with consent, and a
claim flow that never exposes an address on stream.

### 17.2 Tournaments

Built on the Lobby Engine rather than beside it. Bracket types (single elimination,
double elimination, round robin, points table) · seeding by attendance, creator pick,
or random with a published seed · check-in windows · match scheduling and reminders ·
score reporting by creator or a designated operator with a dispute note · standings
overlay module · participant clip consent · sponsor slot with an exposure log.

Prizes follow the giveaway rules: creator-funded, creator-delivered, never held by us,
never a peer-to-peer pool.

---

## 18. Custom audio and creator-supplied media

Creators get real flexibility here, with liability placed where it belongs.

### 18.1 What a creator may supply, by tier

Custom alert sounds · custom widget and module sounds · milestone and celebration
stings · soundboard clips triggerable by supporters · per-bracket and per-source sound
selection · a music bed for BRB and countdown scenes. Counts, total storage and clip
length are tier-gated, using the asset quota ladder (Free none / Pro 100MB /
Creator 250MB / Studio 1GB) that is specified and not yet enforced (MED-13).

### 18.2 The liability position

**The creator is solely responsible for the rights to any audio or media they upload,
and our terms must say so explicitly.** Practically that means:

- An upload requires a positive attestation of rights — a checkbox with a recorded
  timestamp, not buried terms.
- We keep an audit record of who uploaded what and when.
- We honour takedown requests and can disable an asset immediately.
- Uploaded audio is still subject to structural validation, size and duration caps,
  and the asset scan pipeline (stage 2 remains a no-op — MED-14).
- Viewer-supplied media stays out of scope. Creator-supplied only.
- We never claim an upload is licensed or cleared, and never present a creator's
  upload to other creators.

This deliberately does not extend to a shared or discoverable music library — that
would make us a distributor and the attestation would no longer be sufficient cover.

### 18.3 The upload gate — attestation is not a safety control

A structural validator plus a creator checkbox does not address malware, copyright
complaints, impersonation, or what happens after a complaint arrives. **Creator media
upload stays disabled in public product until every row below is defined, built and
rehearsed.** It is a single capability-registry row (MED-15) and it stays off.

| Control | Requirement before the flag opens |
|---|---|
| **Malware** | Stage 2 scanning actually running, not the current no-op (MED-14). Unscanned bytes are never served, not even to the uploader |
| **Quarantine** | New uploads land in quarantine and are unreachable by any overlay, alert or public URL until scan and moderation state both clear. Failure state is quarantined, never "allow" |
| **Provenance** | Per asset: uploader identity, timestamp, source IP, client, original filename, hash, attestation text and version accepted, and every state transition — immutable |
| **Takedown workflow** | A named intake route, a target response time, one-action disable that takes effect at the CDN within minutes, a counter-notice path, and a retained evidence record of the complaint and the disposition |
| **Repeat infringement** | A recorded policy: what happens on a second and third substantiated complaint against the same creator, up to upload suspension. Written before the first complaint, not after |
| **Impersonation and voice** | Explicit prohibition of uploads imitating a real person's voice or a brand, in terms and in the attestation, with the same takedown route |
| **Serving limits** | Signed short-lived URLs only; no public bucket path; no asset served cross-channel |
| **Rehearsal** | One end-to-end drill — complaint in, asset disabled, evidence recorded, creator notified — before the flag opens for anyone |

Until that gate closes, custom audio remains an internal capability behind the registry
flag, usable by a named pilot cohort at most, and it is not marketed.

---

## 19. Architecture — stack, storage, flows and performance

### 19.0 Runtime remediation — four P0 paths, from the 2026-09-14 architecture audit

**Local correctness is green. Production performance is unproven, and four shipped
paths will not hold under load.** These are corrections to running code, not new
features, and they outrank every feature in §34 Phase 1. Until all four close, **no
"lag-free", "fast", "smooth" or "one source replaces twelve" claim may appear anywhere**
— marketing site, store listing, pricing page or investor material (§20.4 enforces it
through the snapshot).

**Progress, 2026-09-16.** RT-01 and RT-02 are **corrected in code and verified locally**
(`active/tasks/RT-01.md`, `active/tasks/RT-02.md`). RT-03, RT-04 and RT-05 are untouched,
so the claim ban above stands in full — and it would stand anyway, because RT-07 is the
row that turns any performance sentence into something sayable, and RT-07 is blocked on a
staging environment that does not exist yet. **A passing local suite is not a load
result.** Nothing here may be cited as performance evidence (§35.1 rule 6).

#### RT-01 · Idle overlays poll the database every two seconds

`apps/api/src/routes/overlay.ts:18` — the SSE route runs a 25-second stream window with
a 2-second replay poll. At the Cloud Run cap of 800 concurrent API requests that is
roughly **400 replay queries per second while nothing is happening**, before a single
tip, dashboard read or webhook.

**Fix:** delete the idle poll. An idle overlay issues **zero** database queries. The
connection is held open with a heartbeat; state moves only when an event for that
channel arrives. Polling returns only as a **jittered slow fallback after a
disconnect**, never as the steady state.

**Corrected 2026-09-15, locally verified.** The idle loop no longer touches the store: a
wait that times out with the listener connected continues without a query. Jittered
polling is entered only from listener failure or disconnect. Evidence:
`tests/TC-RT-01-overlay-idle-replay.md`.

#### RT-02 · One event wakes every overlay on the instance

`apps/api/src/db/overlay-wakeup.ts:29` — `LISTEN/NOTIFY` resolves *all* waiters and each
one then replays from the database. A tip to Channel A causes replays for Channels
B through Z. That is a thundering herd, and it gets worse exactly when the product is
busiest.

**Fix:** **channel-keyed fanout.** The notification carries the channel; only that
channel's subscribers wake; each replays once and the result is shared across that
channel's sessions rather than fetched per session. Per-instance subscriber and
admission limits are explicit, and a rejected admission is a clear, retryable state, not
a silent hang.

**Corrected 2026-09-16, locally verified.** The waiter registry is keyed by channel, so a
notification for one channel cannot wake another's sessions; replay is single-flighted per
`channel + cursor + limit`; and every session re-validates **its own** token on every wake,
so a shared read never carries another session's authorization. One consequence was not
obvious and needed a migration: `app_private.get_overlay_events` used to build
`ttsAudioUrl` from the *calling* session's overlay id, so a shared row would have handed
one session a URL pointing at another's. Migration `0127` returns the resolved artifact id
as its own column and the URL is composed per session. The admission ceilings ship
**unset** — no authority states a number, and one is not inferable from the 2,000-overlay
design target; the value waits on ENV-08, which is blocked. Evidence:
`tests/TC-RT-02-overlay-channel-fanout.md`.

#### RT-03 · TTS delays the visual alert

`services/alert-worker-go/internal/handler/cloud_tasks.go:137` calls TTS enrichment
*before* releasing the delivery, with a 2.5-second HTTP timeout
(`internal/tts/client.go:42`). A slow provider therefore delays the picture. That
directly contradicts §12.2's rule that audio failure never delays the visual.

**Fix, decided by the owner 2026-09-16: checks, then synthesis, then one release.**
An alert is released only once every moderation and safety check has passed **and** its
audio is either ready or definitively not coming. Picture and voice go out together, in
one event. There is no second audio event and no late join.

*This supersedes the two-phase release decided 2026-09-14, and the intermediate
"synthesise during the display queue wait" refinement of 2026-09-16. Both are void.* The
reasoning that replaced them is recorded below, because it inverts this row's original
premise and that must not be rediscovered as a surprise.

**Why the original objection did not survive contact with the code.** Two-phase release
was chosen to stop a slow provider delaying the picture. But each delivery is its own
Cloud Task and they run concurrently, so a slow synthesis delays **only its own alert** —
it never stalls the alerts behind it. The head-of-line blocking that justified splitting
the release does not exist. What splitting the release does buy is a voice that starts
partway through an alert, or misses it entirely, which is the defect a creator actually
notices.

**The ordering risk is real but not a loss.** `app_private.get_overlay_events` declares
`target_after_created_at` and `target_after_delivery_id` and **never uses them**; the real
cursor is acknowledgement, and an acknowledged delivery drops out of the projection. So a
late-released alert still appears — ordered by `created_at`, not by arrival. Nothing is
dropped. The dead parameters are recorded as a separate cleanup, not fixed here.

**The rules, all binding:**

- **Checks first, always.** Moderation, safety, quota and the §11.10 routing decision all
  complete before synthesis begins — never after, and never in parallel with it.
- **One synthesis attempt's worth of delay, at most.** The hold is capped by the
  provider timeout that already exists in `internal/tts/client.go`. No new timeout, no
  cumulative retry budget, no configurable wait.
- **Retry only an unambiguous failure.** Connection refused, DNS, TLS, a 5xx before any
  body, or a 429 carrying retry-after: nothing was synthesised and nothing was billed, and
  these fail in milliseconds rather than seconds, so retrying them costs no visible delay.
- **Never retry a timeout.** A timeout is ambiguous — the provider may have synthesised
  and billed the characters while the response was lost. Retrying spends a creator's
  premium characters a second time on audio nobody will hear. This is the rule that keeps
  the hold bounded without inventing a number.
- **Never retry a terminal refusal.** Quota exhaustion falls to browser voice immediately
  (§11.11, no grace buffer). Safety rejection, an unsupported voice or language, and a
  malformed request all fail identically on a second attempt.
- **A failed synthesis must not consume premium characters.** Not an assumption — an
  acceptance test. Retries multiply any charge-on-failure defect that already exists.
- **Failure releases immediately, without audio.** The chime fallback covers it. A
  creator never loses an alert because a voice could not be produced.
- **The overlay orders its display queue by the alert's creation time, not arrival time**,
  so an alert delayed by slow synthesis slots back into payment order rather than
  appearing after one paid later. Since alerts display for seconds, a late arrival
  usually lands while the other is still queued.

**What this row now means.** Not "never delay the visual" — that was the 2026-09-14
reading. It now means **bound the delay to one attempt and never desync**.

**Built 2026-09-16, locally verified.** The worker classifies every enrichment outcome
(`EnrichSuccess` / `EnrichTimeoutAmbiguous` / `EnrichTerminal`), retries only unambiguous
failures and — structurally, not by convention — can never retry a timeout:
`classifyTransportError` never returns the retryable class for one, so the retry branch is
unreachable from the ambiguous case. Every failure class still reaches `Store.Release`
unconditionally. The overlay orders its display queue by `createdAt`. Evidence:
`tests/TC-RT-03-checks-synthesis-release.md`.

**Correction, 2026-09-16 — the quota release was not what its own comments claimed.**
Migration `0128` closed the live defect (a failed synthesis permanently consumed premium
characters) but left two properties enforced by nothing but a caller-side comment, and
both could **manufacture quota a creator never reserved**:

- **Release was not idempotent.** The `greatest(...,0)` floor stops a negative counter and
  nothing more; a second release against a month holding other usage subtracts twice.
- **Release credited the current month, not the month charged.** A billing-month rollover
  between reserve and release left the old month charged and the new month credited.

The acceptance test asserted the first property and passed, because it only ever released
a month whose counter had already reached zero — the one arrangement where the floor hides
the missing property. Migration `0134` makes reservations durable rows: the meter records
what it charged and to which month, release consumes that reservation exactly once against
that month, and the non-idempotent signature is dropped rather than left callable. Both
defects were reintroduced one at a time and the rewritten test failed on each. Evidence:
`tests/TC-RT-03-checks-synthesis-release.md`, `active/tasks/RT-03.md`.

This is local arithmetic verification only. It is not provider, invoice or settlement
evidence, and it makes no claim about what any TTS provider has actually billed.

#### RT-04 · Payment acknowledgement waits on a worker-pump scan

`services/payment-webhook-go/internal/ingress/handler.go:109` — after committing payment
truth, the webhook waits on a worker-pump HTTP call with a five-second timeout
(`worker_pump.go:15`). A burst turns an **already-safe payment** into a provider retry
purely because dispatch was slow. And a failed enqueue has no enabled periodic sweeper
to recover it (`bharatstudio-crons` ships every schedule `"enabled": false`).

**Corrected 2026-09-16, locally verified.** The commit is the truth and the 2xx follows it
unconditionally; dispatch became a fire-and-forget post-commit wake-up that cannot influence
the status code. Every pre-commit guarantee is unchanged — HMAC over the raw body, event-id
dedup, append-only evidence — and **a commit failure still returns 503 and is still retried**.
The recovery path is real: `bharatstudio-crons`'s `outbox-recovery` schedule is enabled
(RT-08), so a missed wake-up is re-scanned on the next tick rather than lost. The honest cost:
for a *missed* wake-up, dispatch latency for that one delivery becomes the schedule interval.
Evidence: `tests/TC-RT-04-webhook-commit-and-leased-dispatcher.md`.

**Fix:** the webhook does exactly one thing — **one atomic durable commit, then an
immediate 2xx**. Dispatch is a **post-commit wakeup only**, fire-and-forget, and never
part of the acknowledgement. An **independently scheduled, leased outbox dispatcher**
owns enqueueing, so a missed wakeup is recovered on the next tick rather than lost.
That dispatcher is the reason the cron schedules must be enabled (F-track) — without it
this fix has no recovery path.

#### RT-05 · The pump is uncoordinated

`packages/db/migrations/0063_...sql:101` — every webhook may scan up to 100 ready
deliveries, so concurrent webhooks scan and enqueue the same backlog repeatedly.
Deterministic Cloud Task names protect correctness but not latency, and not the pressure
we put on our own API and on the provider.

**Fix:** the leased dispatcher from RT-04 is the only scanner. Webhooks never scan.
Leases make concurrent dispatchers safe and bounded.

**Corrected 2026-09-16, locally verified.** Migration `0129` adds a single-row dispatch lease:
`acquire` is one atomic `UPDATE` with its guard inside the statement, so concurrent runs
serialise on the control row and the loser's predicate re-evaluates false. It deliberately
does **not** reuse `event_outbox_deliveries.lease_token` — that field means "this delivery is
claimed for processing" and is set at Cloud-Task-fire time, so borrowing it as a *scan* lease
would block the real claim for the lease TTL on every normal delivery, trading a dispatch bug
for a latency bug. No new number: the 60s TTL is the `outbox-recovery` schedule's own
`timeoutSeconds`. Evidence: `tests/TC-RT-05-dispatcher-is-the-only-scanner.md`.

#### The target shape, stated once

```text
Payment webhook
  → one atomic durable commit
  → immediate provider 2xx
  → post-commit wakeup only (fire-and-forget)
  → independently scheduled, leased outbox dispatcher
  → Cloud Task
  → moderation, safety, quota and voice routing
  → ONE synthesis attempt (retried only on an unambiguous failure, never on a timeout)
  → release picture and voice together, or release without voice

Committed event
  → channel-keyed fanout
  → only that channel's active overlay sessions wake
  → one Master Canvas SSE connection per channel session
  → one bounded snapshot / state update
  → zero idle database polling
```

#### RT-06 · We cannot currently measure the budgets we promise

`apps/api/src/observability/metrics.ts:42` and the Go services expose **totals and
duration sums, not histograms**. That yields averages. §19.4 promises p99s, and an
average cannot falsify a p99 claim. Reconciliation snapshots are process-local and the
reconciler schedule is unwired (`apps/api/src/routes/metrics.ts:48`).

**Fix:** histogram metrics with explicit buckets on every path that carries a budget,
aggregated across instances, plus a real p95/p99 read-out. **A budget without a
histogram is not a budget**, and PRF-01 cannot pass CI without this.

**Built 2026-09-16, and partially — the instrument exists, two things do not.** Histograms
with §19.4's budget numbers as exact bucket boundaries, a bucket-derived p95/p99 read-out
with its error bound stated, an additive merge, and a durable cross-instance reconciliation
snapshot (migration `0130`) are in place and locally verified. What is **not** closed:
cross-instance aggregation is proven only as the additive property, never against a real
scrape — that needs a deployed environment; and the reconciler still has no schedule.

**Correction, 2026-09-16 — this row named the wrong reconciler.** The sentence above said
"the reconciler schedule is unwired". `payment-reconciliation` in `bharatstudio-crons` is a
real, implemented schedule, but it targets `payment-webhook-go`'s Razorpay provider-status
recovery — a different thing. The **L09 reliability reconciler** at apps/api's
`/internal/metrics/reconcile`, which is what this row's defect is actually about, has **no
schedule pointing at it at all**. Nothing was "unwired"; a schedule was never written.
**Closed 2026-09-16 by [`active/tasks/OPS-RECON-01.md`](./active/tasks/OPS-RECON-01.md):**
the owner decided the reconciler gets its own schedule in its own task, and
`reliability-reconciliation` now targets it — cadence `*/5`, borrowed from
`payment-reconciliation`'s existing cadence rather than newly chosen, because no authority
states one for this job. Whether `payment-reconciliation` should be enabled on its own
separate merits remains open and does not belong to this row.

Only the buckets derive from stated budgets. §19.4 names exactly two duration numbers —
p99 < 200ms for reads and < 500ms for the tip-order path — and both are placed as exact
boundaries so CI can check a boundary bucket's own cumulative count, which is an exact
fact, rather than an interpolated quantile. Two paths §19.4 gives no duration number to
(the webhook acknowledgement and the dispatcher pump) are measured on a **borrowed
measurement grid**, and each metric's help text says so in those words. A borrowed grid is
not a budget, and no CI check may treat it as one.

#### RT-07 · No browser, OBS or device evidence exists

The web suite is JSDOM. There is no Chromium-in-OBS harness, no low-end Android run, no
3G profile, no 8-hour soak, no frame or memory profiler in any repo. **Every number in
§19.4 is currently an assertion.**

**Fix, and this is the release gate:** a real end-to-end browser harness; a staged test
at the concurrency target below; and an **8-hour OBS soak** proving flat memory and node
count. Local suites and the SQL harness (20 synthetic tips, concurrency 5, p95 31ms) are
SQL-correctness evidence only — that harness runs no HTTP, no Razorpay, no Cloud Tasks,
no real SSE, no Cloud Run, no OBS and no sized database, and it may never be cited as
performance evidence (§35.1 rule 6).

#### The concurrency target

**Decided 2026-09-14: design and size for 2,000 concurrent live overlays.** That number
governs the connection model, the per-instance subscriber limits, the database
connection budget and the Cloud Run caps, and it is the concurrency the staged test must
actually reach. It is deliberately above a first-year expectation: a shared, channel-keyed
subscriber registry is cheap to design in now and a rebuild later, and the failure we are
avoiding is a successful launch weekend taking the product down.

### 19.1 The stack, and what is already decided

| Layer | Choice | Status |
|---|---|---|
| Creator dashboard, Support Hub, marketing | Next.js (App Router), React, TypeScript | In place |
| API | Fastify + TypeScript, versioned OpenAPI 3.1, REST + JSON | In place |
| Payment ingress | Go service, HMAC raw-body verification | In place |
| Alert dispatch | Go worker, Cloud Tasks, durable outbox | In place |
| Connector polling | Go poller (`cmd/youtube-poller`) | In place |
| Database | PostgreSQL 16, RLS, SECURITY DEFINER as the sole write path | In place |
| Realtime to overlay | SSE with cursor + explicit ack | In place |
| Wake-up signalling | Postgres LISTEN/NOTIFY, **best-effort only** | In place |
| Scheduling | Cloud Scheduler → private OIDC endpoints | Defined, disabled |
| Hosting | Cloud Run, per-service identity | Defined |
| Edge | Cloudflare, checked-in `_headers` CSP | In place |
| Mobile Companion | React Native 0.87, New Architecture, Hermes | In place |

**Decisions still open, and my recommendations:**

| Question | Recommendation | Why |
|---|---|---|
| Overlay framework | **No framework.** Vanilla TS + a tiny module registry | React's reconciler is the wrong tool for a 60fps canvas inside OBS. Modules are pure render functions over one state store |
| Overlay animation | CSS transitions + Web Animations API; Lottie only for creator art | Compositor-driven, no JS per frame |
| Overlay audio | Web Audio API with a normalisation gain stage | Loudness normalisation (§23.1) is impossible with bare `<audio>` |
| Dashboard state | TanStack Query + a versioned `if-match` write path | Matches the optimistic-concurrency model already in the API |
| Overlay ↔ server | Keep SSE. Do **not** move to WebSockets | One direction, replayable, proxy-friendly, already correct |
| Cache | Postgres-backed derived cache first; Redis only when measured | Avoids a new dependency and a new failure mode before there is evidence |
| Object storage | **Google Cloud Storage + Cloudflare CDN** | See 19.0.1 |

#### 19.1.1 Where custom audio and GIF libraries live — this must change

Lottie and branding are currently stored as **`bytea` in Postgres**. That was a
reasonable call for a handful of small vector files. **It does not extend to audio and
GIF libraries** and must not be copied forward:

- Every read pulls binary through the connection pool, competing with payment traffic.
- Backups and replication bloat with media.
- No range requests, no CDN, no browser caching.
- A Studio creator at 1GB × N creators makes the primary database a media server.

**Target design:**

```text
Upload  → API validates type, size, duration, dimensions
        → asset scan pipeline (stage 1 structural; stage 2 malware, MED-14)
        → normalise: audio loudness + transcode to a single codec,
                     GIF → MP4/WebM, images pre-scaled to the sizes we serve
        → store bytes in GCS at a TENANT-SCOPED content-addressed key
                     (channel_id + sha256), encrypted per tenant
        → Postgres row: id, channel, kind, sha256, bytes, duration,
                        moderation state, rights attestation, audit
        → serve via CDN with a short-lived signed URL
```

**Corrected 2026-09-14: deduplication is tenant-scoped by default, not global.** The
earlier design deduplicated the same bytes across all creators. That is cheaper and it
is unsafe:

- **Existence leak.** A global key lets one creator's upload reveal that another
  creator already holds the identical asset — a probe with a known file returns a hit.
- **Coupled takedowns.** One rights complaint against shared bytes removes the asset
  from every creator storing it, including creators with a valid licence.
- **Ambiguous attribution.** Rights attestations differ per creator, so a single stored
  object has several conflicting rights claims attached to it and no way to say whose
  applies.

The rule:

| Class | Addressing | Dedup |
|---|---|---|
| Creator upload (default) | `channel_id` + sha256, tenant-scoped encryption key | Within one channel only |
| BharatStudio-owned assets (stock stings, default sounds, template media) | Global content address | Global — we own the rights and the takedown path |
| Explicitly licensed shared library | Global, only under a written licence recorded against the asset | Global |

Storage cost of per-tenant duplication is small next to a cross-tenant rights or
disclosure incident, and this is not reversible after the fact. Postgres keeps metadata,
moderation state and the rights attestation; it never keeps the bytes.

**Storage design resolved 2026-09-14.** The master release authority approved Postgres
`bytea` for uploaded Lottie; this section moves media to GCS. Two approved designs is one
too many. **Owner decision: GCS/CDN is the design, and
`active/launch/01_MASTER_RELEASE_AUTHORITY.md` is amended** rather than contradicted from
here.

| Rule | Detail |
|---|---|
| **Migration** | Existing `bytea` rows keep working and keep serving. All *new* media writes to GCS. Backfill is opportunistic and never blocks a release |
| **Serving** | GCS behind the CDN with short-lived signed URLs. A `bytea` row serves from the API until it is backfilled. No public bucket path in either case |
| **Retention** | Media follows the uniform retention policy (§12.6.2), not the storage tier it happens to live in. Moving bytes between stores never changes what is kept |
| **Rollback** | Until backfill completes, the `bytea` path stays functional, so a GCS or CDN failure degrades to the old path rather than losing an asset. The switch is a per-channel flag, revertible in one action |
| **Done when** | Zero new writes to `bytea`, the backfill queue is empty, and one asset has been served from both paths in the same session to prove the fallback |

### 19.2 The flows that matter

**Tip → alert (the critical path).**

```text
Support Hub → POST tip order (idempotency key)
            → provider order created, scoped to the creator's connected account
            → viewer pays in Razorpay Checkout / UPI intent / QR
            → Hub shows "confirming", never "paid"
            → Razorpay webhook → Go ingress → HMAC + event-id dedup
            → ONE transaction: delivery + payments + intent + alert_events + outbox
            → best-effort NOTIFY → worker pump → queue selection → moderation gate
            → Interaction Rules Engine evaluates (§23.2)
            → TTS synthesis if eligible → SSE push → overlay renders → ack
            → Hub status advances verified → queued → shown
```

**Capability resolution (every render, every surface).**

```text
control plane (kill → denylist → rollout → min_tier → override)
  → creator enabled → creator config → runtime activation → render
```

Resolved server-side, cached per channel with a version, invalidated on control-plane
change. The client never decides entitlement — it only renders what it is told, which
is the existing L24 rule generalised.

**Creator media upload.** As 19.0.1, plus: manual activation before an asset can be
triggered, and immediate disable propagating to the overlay within one SSE cycle.

**Co-stream room.** Both creators authorise → room record with short-lived grants →
public page renders two IFrame players + our modules → Companion controls layout,
audio side and safe layout → revoke kills the grant and the page falls back to a
single-creator or ended state.

### 19.3 Grilling the architecture — the four real risks

**Risk 1: the control plane becomes a new source of outages.** Making tiers editable
at runtime means a bad admin edit can disable a feature for everyone. Mitigations are
in §20.6, and the non-negotiable one is that Layer 1 correctness dimensions are not
editable there.

**Risk 2: derived aggregates do not scale.** Already covered (§19.3 below), and the
answer is a cache invalidated by the outbox event, never a stored counter.

**Risk 3: the capability registry becomes an N+1 disaster.** Sixty capabilities ×
per-channel resolution on every request is a trap. Resolve once per channel into a
compact bitmap-plus-limits blob, version it, cache it, and invalidate on control-plane
or subscription change. Never query per capability.

**Risk 4: media serving pulled into the API.** If signed URLs are not in place before
audio ships, the API becomes a file server and the frame budget dies. GCS + CDN is a
prerequisite for AUD-01, not a follow-up.

---


The overlay runs inside OBS while the machine is encoding a game. Every millisecond we
spend is a frame the creator loses. "Lightweight" is therefore a correctness
requirement, not a nice-to-have, and the honest constraint is that **we are adding
work to a machine that is already saturated**.

### 19.4 Budgets — measured, not asserted

| Surface | Budget |
|---|---|
| Overlay browser source | < 5% of one CPU core idle · < 15% during an alert · zero sustained GC churn · no frame over 16ms |
| Overlay memory | < 150MB steady, no growth over an 8-hour stream |
| Companion cold start | < 2s to interactive on a mid-range Android |
| Companion action round trip | < 300ms perceived, optimistic UI with rollback |
| Live Deck refresh | Push-driven; no polling loop faster than 10s as a fallback |
| Support Hub first contentful paint | < 1.5s on 4G, < 3s on 3G |
| Support Hub JS | < 150KB gzipped before the optional player |
| API p99 | < 200ms for reads, < 500ms for the tip-order path |
| Idle overlay database load | **Zero queries.** An overlay with nothing happening touches the database not at all (RT-01) |
| Visual alert release | Never waits on TTS, media or any enrichment (RT-03) |
| Payment webhook acknowledgement | 2xx after the durable commit, never after a dispatch call (RT-04) |
| Concurrency the design is sized for | **2,000 concurrent live overlays**, and that is the concurrency the staged test must reach |

These go in CI as budgets that fail the build, not in a document as aspirations.

**A budget with no histogram is not a budget (RT-06).** Every path above needs bucketed
histogram metrics aggregated across instances before its number means anything; totals
and duration sums yield averages, and an average cannot falsify a p99. PRF-01 does not
pass until this exists.

**And no budget is met until it is measured where it runs (RT-07):** Chromium inside
OBS, a low-end Android, a 3G profile, and an 8-hour soak showing flat memory and a flat
node count. JSDOM tests and the local SQL harness are not evidence of any number in this
table.

### 19.5 Overlay — the architecture that keeps it cheap

**One source, one connection, one loop.** The Master Canvas collapses N browser sources
into one; the win is only real if it also collapses N connections and N render loops.
One SSE connection, one `requestAnimationFrame` scheduler, modules as pure render
functions driven by a single state store.

**Master Canvas is not built yet (PRF-02, absent), so the claim is not yet true.** Today
each widget route is an independent OBS browser source opening its own transport. Until
Canvas is the runtime, **"one source replaces twelve" may not be marketed** (§20.4).

The connection model, corrected 2026-09-14 (RT-01, RT-02):

- **Channel-keyed subscribers.** A notification carries its channel; only that channel's
  sessions wake. No cross-channel wake, ever.
- **Deduplicated per-channel replay.** One replay per channel per event, shared across
  that channel's sessions — not one query per session.
- **Heartbeats** carry connection health; they are not a data path.
- **Zero idle polling.** Jittered slow polling exists only as a post-disconnect
  fallback.
- **Explicit per-instance subscriber and admission limits**, with a clear retryable
  rejection rather than a silent hang.

Rules that keep it fast:

- **Composite-only animation.** `transform` and `opacity` exclusively. Never animate
  width, height, top, left, or anything that triggers layout. Each animated element
  gets its own layer deliberately, not accidentally.
- **No layout thrash.** Batch reads then writes. Never read `offsetHeight` inside a
  loop that also writes.
- **Bounded DOM.** A hard cap on nodes per module and on total canvas nodes. A ticker
  recycles its rows; it does not append forever. An 8-hour stream must end with the
  same node count it started with.
- **Idle modules cost nothing.** A hidden or inactive module unsubscribes and stops
  rendering — it is not merely `display:none` with a live timer behind it.
- **Sampling, not streaming, for high-frequency data.** Reactions and chat are sampled
  and rate-limited server-side before they reach the canvas. The Reaction Cloud shows a
  representative sample, never every event.
- **Burst coalescing.** The reconnect-replays-an-hour-of-alerts problem (ALQ-16) is a
  performance bug as much as a UX one. Replay collapses into a summary plus a bounded
  catch-up sequence.
- **Assets budgeted.** Lottie complexity capped, sound files length- and size-capped,
  images pre-scaled server-side. A creator cannot upload a 4K PNG and have us scale it
  in the browser every frame.
- **No third-party scripts in the overlay. Ever.** No analytics, no font CDN, no tag
  manager. The CSP already restricts this; keep it.
- **Degrade per module.** One module throwing must not blank the canvas — error
  boundaries per module, and a module that fails twice stays down for the session with
  a creator-visible note.
- **The Free watermark is a protected top layer** rendered after every module, outside
  the module system and outside the error boundaries. A module crash must never take the
  attribution with it. Specified in §30.6.

### 19.6 The derive-don't-store tension, and how to resolve it

Goal progress, streaks, badges, leaderboards and reputation are all computed live from
`payments − refunds`. That is architecturally right — it is why refunds need no special
handling anywhere — but a windowed aggregate per widget read does not scale to a
popular stream with eight widgets and a reconnecting overlay.

**Resolve it with a read-through cache, never a stored counter.**

- Cache the computed value keyed by `(channel, widget, window)` with a short TTL.
- **Invalidate on the event, don't poll for it.** A verified payment, refund or
  external contribution already fires an outbox event; that same event invalidates the
  cache. The SSE "re-read" signal we already use fits this exactly.
- The cache is a derived artefact with no authority. If it is cold, empty or wrong, the
  query is the truth and recomputing is always safe.
- Never introduce a `progress` column. `0102` deliberately has none, and `0120` raises
  rather than storing a reputation score. Those decisions stand.
- Materialised views are acceptable for expensive historical reads (supporter history,
  post-stream analytics) where staleness is tolerable and visible.

### 19.7 Server and realtime

- The overlay listener needs its **own direct connection** (`DATABASE_URL_DIRECT`);
  pooled `LISTEN/NOTIFY` is best-effort signalling only and never the correctness path.
  Durable cursor replay remains authoritative (ALQ-04).
- **The notify payload carries the channel, and fanout is keyed on it** (RT-02). Waking
  every waiter and letting each one query is the current behaviour and it is a defect.
- SSE fan-out is per-overlay, not per-widget. Adding a widget must not add a connection.
- **Dispatch is never inside a request the provider is waiting on** (RT-04). One atomic
  commit, immediate 2xx, post-commit wakeup, and a separately scheduled leased dispatcher
  that owns enqueueing and recovers anything the wakeup missed.
- **Only the dispatcher scans for ready deliveries** (RT-05). Request handlers never
  scan a backlog.
- **The visual path waits for at most one synthesis attempt** (RT-03, owner decision
  2026-09-16). Picture and voice are released together; a terminal or ambiguous failure
  releases the picture without audio rather than retrying.

### 19.8 Companion (mobile)

- Push-driven, not polling. The Live Deck updates from events; a slow timer exists only
  as a fallback.
- Optimistic UI with explicit rollback on failure, so a one-tap control feels instant
  on a bad connection.
- Virtualise every list over ~50 rows.
- No re-render storms: continuous values (progress, timers) must not be React state
  that re-renders a tree every tick.
- Respect background execution limits; reconnect cleanly rather than holding sockets.
- The app must remain usable one-handed on a mid-range Android on 4G — that is the real
  device, not a flagship on Wi-Fi.

### 19.9 Support Hub

- Server-render the page; the YouTube player is lazy and optional.
- The player is the heaviest thing on the page — it must never block first paint, and a
  low-bandwidth mode omits it entirely.
- Realtime goal and ticker updates arrive over one connection, shared by all modules.
- Reactions are optimistic locally and sampled server-side.
- The payment path stays functional with JavaScript degraded — a QR and a link always
  work.

### 19.10 How we stay ahead of competitors on this

**This claim is currently unpublishable (RT-09).** Master Canvas is absent, idle
overlays poll every two seconds, and no OBS measurement exists. Everything below is what
the claim becomes once Phase 0.5 closes and the benchmark is real.

The competitive claim is not "more widgets". It is **one source instead of twelve**,
which is a measurable CPU and memory win on the creator's encoding machine, and the
reason a creator with a mid-range PC can run our full feature set and not theirs.
That claim must be backed by a published, reproducible benchmark: our full canvas
versus an equivalent stack of separate browser sources, measured on a mid-range
machine, re-run in CI.

If that benchmark ever stops favouring us, the architecture has drifted and the
feature set is not worth what it costs the creator.

---

## 20. The control plane — flags, tiers and limits as data

**Requirement: every feature and every widget has a master switch in the admin panel,
and staff can move any capability between tiers, change any limit, or kill any feature
at any time — with the marketing site following automatically.**

This is the single biggest architectural change in this document, because today the
opposite is true.

### 20.1 What has to change

| Today | Required |
|---|---|
| Tier values live in `app_private.tier_entitlement_dimensions` (a migration) and in `entitlement-policy.ts` (TypeScript constants) | One authoritative, admin-editable store |
| Changing a limit means a migration and a deploy | Changing a limit is an audited admin action |
| Marketing pricing copy is hand-written and hand-synced | Marketing reads the same source |
| Eight closed entitlement dimensions | An open registry of capabilities, each with its own gate |
| No kill switch | Every capability independently disableable, globally or per channel |

The closed eight-dimension set was a deliberate decision and it was right for
correctness-critical queue behaviour. It does not extend to sixty widgets and
features. The resolution is two layers, not one.

### 20.2 Two layers, deliberately separate

**Layer 1 — correctness entitlements (unchanged).** The eight dimensions that govern
queue behaviour, TTS eligibility and character limits stay exactly where they are:
enforced in SQL and in `entitlement-policy.ts`, changed by migration, reviewed. These
affect payment and delivery correctness and must not be editable from a web form at
2am.

**Layer 2 — the capability registry (new).** Everything else — every widget, module,
Hub feature, lobby mode, AI feature, giveaway type, audio capability — is a row:

```
capability_id            stable slug, e.g. "widget.wins_this_season"
kind                     widget | module | feature | hub_lane | lobby_mode | ai_feature
min_tier                 free | pro | creator | studio | enterprise | disabled
limits                   jsonb, e.g. {"max_instances": 3, "max_duration_ms": 8000}
global_kill              boolean
rollout                  {percent, allowlist_channel_ids, denylist_channel_ids}
beta                     boolean
marketing_visible        boolean
marketing_label          text
marketing_blurb          text
effective_from           timestamptz
created_by / reason      audit
```

Every change is an append-only version with an actor and a reason, exactly like the
existing entitlement override audit. Nothing is edited in place.

### 20.3 Resolution order at runtime

```text
global_kill            → off for everyone, immediately
denylist               → off for this channel
allowlist / rollout %  → on for this channel regardless of tier
min_tier vs tier       → entitled or not
per-channel override   → staff grant, audited, time-boxed
creator enabled flag   → does the creator want it
creator configuration  → how it behaves
runtime activation     → is its dependency live
```

The last three are the creator's four-switch model from §15; the first five are the
control plane. **A capability is visible to a creator only if the resolution says
entitled; a locked one is shown with the tier that unlocks it** — never hidden, never
a dead control.

### 20.4 How the marketing site follows automatically

The marketing site stops hand-writing feature and pricing tables. It reads a published
snapshot:

- The API exposes `GET /v1/public/capability-matrix` — capability id, marketing label,
  blurb, and the minimum tier, filtered to `marketing_visible = true`.
- Marketing builds render from that snapshot at build time, and revalidate on a
  webhook when the matrix version changes. Static output stays static; it just stops
  being hand-maintained.
- A capability with `marketing_visible = false` (internal, beta, killed) never appears
  publicly. This is how we stop advertising things that do not exist — the exact
  failure behind the current watermark and custom-sound claims.
- Prices remain a separate, deliberately manual, legally-reviewed decision. The matrix
  controls **what is in which tier**, not what a tier costs.
- **Performance claims are gated the same way (RT-09).** "Lag-free", "fast", "smooth",
  "instant" and "one source replaces twelve" are treated as capability claims with a
  `marketing_visible` flag that stays **false** until RT-01 to RT-07 close and the
  published benchmark exists. A performance adjective is a claim about measured
  behaviour, and we have no measurement yet.

**This inverts the current bug class.** Today the site can claim a feature the code
does not have. After this, the site cannot render a capability the control plane does
not publish.

### 20.5 Full site behind flags

Every marketing page, section and CTA gets a flag in the same registry
(`kind = marketing_section`), so an unlaunched product area, a pricing experiment or a
legally-unreviewed claim can be switched off without a deploy. The existing rule that
no Enterprise tier or contact-sales CTA may appear until L10 is amended becomes a flag
default rather than a code review.

### 20.6 Safety rails on the admin panel

Because this panel can now break production:

- Correctness dimensions are **not** exposed here. Attempting to gate a Layer 1
  dimension through Layer 2 is rejected.
- Lowering a limit never destroys creator data — the same read-only/pause behaviour as
  a tier downgrade.
- Every change previews an impact count: "affects 214 channels, 3 currently live".
- Changes affecting live channels are staged by default with an effective time.
- Two-person approval for every capability change, and owner sign-off for moving a paid
  capability into Free.
- **`global_kill` is the one exception, and it is an emergency path with its own
  rules** — see §20.6.1. It is not a second, looser way to make ordinary changes.
- A capability can be reverted to its previous version in one action.
- All of it is behind platform-admin auth with MFA (ADM-07) — this panel is now a much
  higher-value target than a DLQ viewer.

#### 20.6.1 The emergency kill path

Requiring two people to stop an actively harmful capability is how a five-minute
incident becomes a fifty-minute one. Requiring nobody is how an admin silently removes
a paid feature. The resolution is a **single-actor action with a hard expiry and a
mandatory second look**, not a second standing rule.

| Rule | Value |
|---|---|
| Who may fire it | Any platform admin, alone, with MFA already satisfied |
| What it does | The capability is off for everyone immediately; **creator settings, data and history are retained untouched** |
| Reason required | A free-text reason at the moment of firing. The action is refused without one |
| Maximum duration | **24 hours.** At expiry it auto-reverts to its previous state unless a second admin has ratified it |
| Ratification | A second platform admin must ratify within **4 hours**; an unratified kill still runs to its 24-hour expiry but is escalated to the owner at the 4-hour mark |
| Extension | Only by the two-person path, with a stated new expiry. There is no indefinite kill |
| Logging | Immutable, append-only: actor, timestamp, capability, reason, affected channel count, live-channel count, ratifier, expiry, revert. Not editable by any admin, including the one who fired it |
| Notification | Affected creators are told the same hour, in Companion and by email, per §25.6.1 — and are never billed for a capability that is off |
| Post-incident review | Mandatory within **72 hours**, written, attached to the log entry. A kill with no review blocks further kills by that actor until it is filed |

`global_kill` may never be used to perform a tier change, a limit change, or a pricing
change. Those are ordinary changes and take the ordinary path.

---

## 21. More widgets, and where their data comes from

### 21.1 Stat widgets — the honest data question first

"Wins this season" needs a source, and **we cannot read game state**. Anything that
claims to is either a game integration we do not have or scraping we will not do. So
every stat widget declares its source explicitly:

| Source | How | Reliability |
|---|---|---|
| **Companion tap** | Creator taps +1 Win / +1 Loss on the Live Deck | Honest, instant, always available |
| **Lobby / tournament result** | Auto-filled when the match ran through our Lobby Engine (§16) | Automatic, only for our sessions |
| **Manual correction** | Creator edits the running total in the dashboard | Always available, audited |

That is the whole set for v1. It is also a genuine advantage: a creator tapping a
button on their phone is more reliable than a fragile game-memory reader, and it works
for every game including ones nobody integrates with.

### 21.2 New widget modules

| Module | Data source |
|---|---|
| **Wins This Season** | Companion tap / lobby result |
| **Session Record (W–L–D)** | Same, scoped to this stream |
| **Win Streak** | Derived from the record |
| **Personal Best / Record** | Creator-set, celebrated when beaten |
| **Rank / Tier Progress** | Creator-entered current rank and target |
| **Season Objective Tracker** | Creator-defined objective with progress |
| **Head-to-Head** | Two creators or two squads, for co-streams (§22) |
| **Match Countdown** | Next scheduled lobby or tournament match |
| **Tournament Standings** | Bracket state (§17) |
| **Squad Roster Card** | Lobby seats, opted-in names only |
| **Hours Streamed** | Session and weekly totals from our own session records |
| **Milestone Ticker** | Subscriber, member or viewer milestones via the YouTube API |
| **Top Clip of Stream** | Creator-marked stream marker |
| **Stream Recap Card** | End-of-stream stats, for the outro scene |
| **Scoreboard** | Manual two-side score with a centre event rail |

All of them are modules of the one canvas (§6), all carry the four switches (§15), and
all are rows in the capability registry (§20) so staff can retier them at will.

### 21.3 Standalone widget URLs — kept, capped, second-class

**Decided 2026-09-14.** Standalone widget browser sources stay supported. Creators built
working scenes around them and breaking those setups punishes people who did nothing
wrong. But they are the second violation of §12.7 — each one opens its own live
transport — so they are bounded rather than free.

| Rule | Detail |
|---|---|
| **Live-transport budget** | A **per-channel cap on concurrent live transports**, counted across Master Canvas and every standalone widget together. Canvas counts as one no matter how many modules it holds |
| **Over the cap** | Additional standalone widgets fall back to a slow, jittered snapshot poll instead of a live transport, and say so plainly in the dashboard. Nothing silently stops updating |
| **Product direction** | Canvas is the default and the recommended path everywhere — the editor, the docs, the onboarding. Standalone is an escape hatch, never the thing we teach |
| **Transport parity** | A standalone widget uses the same channel-keyed subscriber path as Canvas. No second delivery mechanism (ENG-06 already rejects that) |
| **Free-tier attribution** | A standalone widget carries the watermark **only if it is the channel's only active overlay source**; otherwise Canvas owns it and duplicating it would be worse (§30.6) |
| **Not deprecated** | There is no removal date. If we ever want one, it is a decision row with a migration, not a quiet break |

---

## 22. Creator Co-Stream Room

Two creators, one BharatStudio page, two official YouTube embeds.

**The boundary that makes this buildable: we embed, we never ingest.** BharatStudio
puts two authorised YouTube players on a shared page and composes everything *around*
them. Ingesting, mixing and rebroadcasting two live feeds would mean relay and encoding
infrastructure, rights handling and latency control, and it is outside this product.

### 22.1 Flow

1. Creator A opens a room: title, category, time, layout, audience rules.
2. Creator B **explicitly accepts** — a request alone attaches nothing.
3. Both select their live broadcast.
4. BharatStudio creates a public viewer page at `/live/collab/<id>`, a private
   Companion control room, and an OBS scene preset.
5. At start, both broadcasts appear together.
6. Either creator can end the session, pause their card, or revoke access instantly.

No viewer can attach a stream. Viewer participation and creator co-stream permission
are separate systems.

### 22.2 Layout modes

Horizontal 50/50 (duos, podcasts, debates) · Vertical 50/50 (mobile co-streams) ·
Active speaker (interviews) · Gameplay + facecam · Squad grid (3–4 approved creators) ·
Battle view (two sides, centre score rail) · Host + guest (70/30) · **Switch Window**.

**Switch Window replaces "random switching":** creators pick a range (45–90s) and we
choose the next change within it. Both see the countdown; either can pause or override.
Dynamic without feeling arbitrary or unfair.

### 22.3 What makes it better than two browser tabs

**One audio source at a time — never both by default**, with viewer-controlled
switching and volume · shared event rail (kills, rounds, votes, goals, milestones) ·
supporter alerts visually assigned to the correct side · shared timer, scorecard, match
state, next-round prompt · chat tabs per creator plus optional community chat · clear
attribution ("Watching Creator A on YouTube") · follow/subscribe for both ·
mobile-first vertical with swipe-to-focus · optional captions and translation ·
session metadata recording collaborators, times, layout and sponsor placements.

### 22.4 Companion control room

Invite / accept / revoke · confirm each broadcast is live · choose layout and switch
window · select primary audio · pause one side, show BRB or a disconnected card ·
one-tap **safe layout** if a stream ends or becomes unsuitable · shared moderation
notes and operator roles · preview before going public · OBS scene-template export.

For OBS, we generate a **collaboration overlay scene** — branded frames, team cards,
score, timers, alerts, live state. The creator keeps controlling their real media
sources; the embedded player is never their production feed.

### 22.5 Money — the rule that must not bend

A tip to Creator A stays Creator A's transaction, receipt, ledger entry and alert. A
tip to Creator B stays Creator B's. **Never silently split a supporter's payment.**

A joint goal may show combined progress, but each contribution's destination is shown
clearly. Any real revenue split needs an explicit agreement, a separate payout ledger,
refund rules and tax treatment — not a 50/50 toggle. That is the Enterprise problem
(§24) and it is blocked for the same reasons.

**Amended 2026-09-14: "shared goal" money language does not ship until it is fully
defined.** A supporter reading "support the shared goal" reasonably believes the money
is shared. If it settles to one creator, that is a misleading payment presentation, and
a beneficiary line in small type at the bottom of a receipt does not cure it.

What ships first is the safe half: a **contribution selector** with two honest options —
*Support Creator A* · *Support Creator B*. Combined progress may still be **displayed**
as a joint target, because a progress bar is not a payment destination.

A third "shared goal" option may be added only when all of the following exist:

- the single declared beneficiary is named **before checkout, on the checkout screen
  itself, and on the receipt** — not only in a tooltip or the terms;
- the refund policy states who refunds and from where;
- the tax responsibility of the receiving creator is stated and reviewed;
- a creator-to-creator agreement is recorded in product by both parties before the
  option can be enabled for a session;
- the wording is reviewed by the same legal gate as the payment surfaces.

Absent those, the word "shared" is not used next to money anywhere in the product.

### 22.6 Add-ons and safety

Creator Battle Mode with transparent scoring and no paid random outcomes · Squad Night ·
Guest Pass for an emerging creator · Raid Hand-off · collaborative non-monetary
challenge votes · sponsor mode with an auditable exposure timeline · clip handoff with
both creators' approval · cross-community lobby via §16.

Safety: mutual approval, re-authentication, **short-lived collaboration grants** ·
instant revoke either side · no permanent channel linking · no merged private chats or
supporter data without consent · per-creator moderation boundaries · the public page
tolerates one feed ending, being region-blocked, or lagging · **we never promise
frame-perfect sync** — two independent YouTube broadcasts have different delay and the
UI must say so rather than look broken.

---

## 23. Sound Moments and the Interaction Rules Engine

Benchmarked against StreamTipz, which ships a soundboard, alert media, TTS voices,
goal/top-supporter/recent-tip widgets and provider routing. The gap worth attacking is
not "more toggles" — it is turning dozens of disconnected settings into one auditable
system.

### 23.1 Sound Moments

A supporter picks a creator-approved **moment** while tipping: sound, animation,
sticker, TTS style, optional on-screen effect. The creator controls every allowed
combination.

```text
₹49   GG sound + small chat bubble
₹99   Hindi meme sound + supporter name
₹199  animated sticker + premium TTS voice
₹499  creator-approved mega alert scene effect
```

Controls: creator-curated catalogue, no arbitrary supporter uploads · one sound per tip
· strict duration and **loudness normalisation** · per-sound, per-viewer and
stream-wide cooldowns · one-tap Companion mute, skip, pause, emergency safe mode ·
themed packs (family-safe, gaming, roast, Hindi, Punjabi, Tamil, festival) · creator
uploads only after type validation, scanning, size and duration limits, copyright
acknowledgement and manual activation (§18).

**Never execute a remote audio or GIF URL in the overlay.** Everything is validated and
served from our own storage. Convenient remote URLs are how overlays become an abuse,
reliability and copyright problem.

### 23.2 The Interaction Rules Engine

Instead of sixty settings, a creator writes rules:

```text
Tips above ₹99          → supporter may choose one safe sound
Tips ₹199+              → TTS enabled
Mode = ranked match     → suppress all audio, show a small ticker only
Mode = BRB              → queue alerts, replay afterwards
Overlay offline         → hold everything, nothing is lost
```

Supports thresholds · stream-mode rules · member and subscriber perks · cooldowns ·
daily caps · event priority · creator-approval-required · **never interrupt gameplay**
mode · automatic fallback when the overlay is offline.

This is the feature that turns the product from a widget collection into an operating
system, and it composes with everything else: Sound Moments, TTS eligibility, Clutch
Mode, queue modes and the capability registry are all inputs to the same evaluation.

### 23.3 Goal lifecycle — what happens when a goal completes

Added 2026-09-15. The product had goals, a milestone queue and a rules engine, and
nothing that said **what actually happens at 100%**. This is that section, and it is the
same trigger→action engine as §23.2 rather than a second one.

#### 23.3.1 Completion must be latched, not recomputed

**This is the design point everything else depends on.** Goal progress is *derived* from
`payments − refunds` (§19.6), which means progress can go **down**. If "complete" were a
recomputed boolean, a refund would un-complete a goal and the next tip would fire the
celebration a second time.

So completion is a **recorded event with a latch**:

- The first read that crosses the target writes a `goal_completed` event, **once**,
  idempotently, with the contribution that crossed it and the derived total at that
  moment.
- Actions fire from that event, never from the boolean.
- **A later refund does not un-complete the goal.** It is recorded against it, the
  progress display shows the true derived figure, and the completion stands — because it
  happened, and the audience saw it (the same rule as §10.10.4: we do not rewrite the
  past on stream).
- A creator may **manually reopen** a goal. That is an explicit, audited action with a
  reason, not an automatic consequence of arithmetic.

#### 23.3.2 Triggers — everything that can fire a rule

| Class | Triggers |
|---|---|
| **Goal** | Reached 100% · a creator-defined threshold (percentage **or** absolute) · first contribution · the contribution that completed it ("the closer") · biggest single contribution · stretch beyond 100% at defined steps · goal stalled for N minutes · goal expired unmet · ladder step complete · **all** goals complete · **any** goal complete |
| **Session** | Session total crossing a figure · Nth supporter of the stream · new top supporter · first-time supporter · returning supporter (reputation, §12.12) |
| **Platform** *(P2, Phase 4)* | Super Chat received · membership · gifted memberships · like-count milestone · viewer-count milestone |
| **Community** *(P3)* | Challenge complete · lobby filled · tournament result · giveaway drawn |
| **Operational** | Stream start · stream end · scene change · Clutch Mode entered or left · sponsor segment start or end |

Every trigger carries the same controls: enabled · threshold · **once per stream / every
time / at most N per stream** · cooldown · minimum contribution · quiet window · and which
contribution sources count (UPI tip, Super Chat, membership, manual adjustment —
independently, per §15.2).

#### 23.3.3 Actions — the full catalogue

**On the overlay:** celebration animation · confetti or particle burst · full-screen
takeover for a bounded duration · banner or lower third · ticker message · progress-bar
flourish · module swap · **theme swap** (festival, sponsor-safe, celebration) · winner or
closer card · a "goal smashed" scene preset.

**Audio:** a Sound Moment · a music sting · a TTS announcement — **through the §12.2
pipeline like any other text** · duck other audio for the duration.

**Goal lifecycle:** mark complete · **auto-advance to the next goal in the ladder** ·
**auto-create the next goal** by a rule — `+₹X`, `×N`, next value from a template list, or
the same target again · **roll the overflow into the next goal** or discard it · convert to
a stretch goal · extend the deadline · pause · archive · reset for the next stream.

**To the creator:** Companion push · a Live Deck banner · a suggested next action · a
**stream marker** so the moment is findable in the Wrap Stream summary (§5.5).

**To supporters:** a thank-you card naming the closer *with visibility consent* · a badge
grant (§12.12 rules apply) · a note appended to receipts issued during the goal.

**Outbound** *(P2/P3, approve-then-send by default per §27.1):* a rate-limited YouTube
chat announcement · a Discord webhook post · Telegram · WhatsApp opt-in reminder · a
social post with a generated card.

**OBS, through the local helper:** scene switch · source toggle · save the replay buffer ·
trigger an approved Streamer.bot or SAMMI action (§9.6).

**Sponsor:** reveal a sponsor card · log the exposure with a timestamp for the
proof-of-delivery report.

#### 23.3.4 What YouTube can and cannot do — Phase 4, and narrower than people expect

| Wanted | Reality |
|---|---|
| Post a chat announcement | **Possible**, needs the chat-write scope (unfiled, §32), and is rate-limited and coalesced by us (§36.6) |
| Pin the announcement | Possible within the same scope |
| Update the broadcast title or description — "GOAL SMASHED" | Possible, and **heavily rate-limited**; treat as once per stream, not per milestone |
| Create a poll | Possible where authorised |
| Trigger a membership gift, a Super Chat, or any purchase | **Never.** §4 is explicit: BharatStudio must never automate a membership purchase or card confirmation |
| Change anything about someone else's account | Never |

**Everything above is Phase 4**, and none of it may be marketed before the scope exists.
The BharatStudio-side actions in §23.3.3 are available without any of it — which is the
point of not building the celebration on top of YouTube.

#### 23.3.5 Sequencing, conditions and the safety interlocks

Actions are an **ordered list with delays**, not a set. A creator composes:

```text
goal reached 100%
  → 0.0s  duck audio · play sting
  → 0.2s  confetti · full-screen takeover (4s)
  → 4.2s  banner: "{goal_name} complete — thank you {closer}!"
  → 5.0s  auto-create next goal: +₹2000, roll overflow in
  → 6.0s  prepare Discord post  (approve-then-send)
  → 6.0s  stream marker "goal 1 complete"
```

**Conditions** on any rule: only while live · only in named scenes · **not** while Clutch
Mode is active · not during a sponsor segment · only above a tier · only if the overlay is
connected · only outside quiet hours.

**Interlocks that are not creator-configurable:**

- **Clutch Mode suppresses everything loud or full-screen**, and the deferred actions are
  shown afterwards rather than lost (§5.2).
- **Never interrupt an alert mid-play.** Celebrations queue behind the current alert.
- **Never-interrupt-gameplay mode** (`RUL-02`) holds full-screen actions until a safe
  moment.
- **Any text that will be spoken or displayed goes through §12.2**, including generated
  announcement copy.
- **Rate limits are ours to enforce**, not the platform's to reject.
- **Prepare, not fire, is the default for anything outbound or public** (§5.4) — the
  creator releases it. Low-risk local actions (a sound, a banner) may auto-fire.

#### 23.3.6 Templates, preview and configurability

Text templates carry variables — `{goal_name}` `{target}` `{raised}` `{remaining}`
`{percent}` `{closer}` `{top_supporter}` `{supporter_count}` `{session_total}` `{next_goal}`
— and every string is per-language (§15.4).

**Every action is configurable to the §15.2 depth**: which sound, which animation, its
duration and easing, its position within the safe zones, colour, size, and whether it
exists at all. **Preview fires the whole sequence** on the overlay in a test mode that is
visually marked and auto-reverts, so a creator sees the composition before an audience
does.

**Starting points, not cages:** presets — *Quiet* (banner and marker only), *Standard*
(sting, confetti, banner, auto-advance), *Hype* (takeover, theme swap, outbound posts
prepared) — each fully editable afterwards, per §15.3.

#### 23.3.7 Refunds, overflow and the accounting

- **Overflow** — the amount above the target — is either rolled into the next goal or
  discarded, creator's choice, recorded either way.
- **A refund after completion** reduces the derived total and is visible on the goal's
  detail view, but does not reverse the completion event, the celebration, or a rolled-over
  overflow that has already been credited to the next goal.
- **The goal's detail view** follows the §7.2 contract: summary, timeline of every
  contribution and every rule that fired, relations to the contributions and the next goal,
  actions, and the audit of any manual reopen.
- **"Why this number?"** (§7.3) explains a goal total from its contributions, including
  refunds — which is only possible because the total is derived.

### 23.4 Overlay URLs are bearer credentials

The competitor review's sharpest lesson. Our current design is already good — token in
the URL fragment, only a SHA-256 hash stored, per-overlay lookup, rotate and revoke —
but it is missing expiry.

Required: **short-lived signed capabilities** with explicit renewal, session and device
binding where practical, scheduled rotation, immediate revocation, and a standing rule
that overlay URLs never appear in screenshots, support tickets, logs or error messages.
A creator screenshotting their OBS setup for a support request must not hand over a
permanent credential.

### 23.5 Other things worth taking from the benchmark

Test/sandbox mode that never reaches viewers · shadow mode beside an existing provider
· a global emergency-disable button · transparent-background source · portrait and
landscape layouts · scene profiles (gameplay, Just Chatting, BRB, lobby, results,
sponsor) · Indic TTS pronunciation dictionaries · multi-goal campaigns with scheduled
rollover · captions for TTS and reduced-motion overlay mode · a creator policy panel
(no abusive audio, no adult sounds, no political content, family-safe defaults).

---

## 24. Enterprise

Governance-blocked in v1, and included here so the scope is not lost.

### 24.1 Capability set

Multi-channel allocations · SSO · RBAC beyond owner/moderator · shared brand kits ·
licensed design packs · campaigns · cross-channel analytics · API and outbound webhooks
· finance and audit exports · SLA and named support.

### 24.2 The money shape

The 85/15 split is **enterprise ↔ creator** via Razorpay Route, executed at capture.
BharatStudio takes 0% and **is never the parent Route account holder** — the enterprise
holds the parent, creators are linked accounts. If Razorpay says a BharatStudio-owned
parent is the only supported shape, that reopens the product decision; it is not
accepted silently.

### 24.3 The rule that governs every split

The payment-account binding and allocation-policy version stored at order creation is
**permanent**. A later policy change never retroactively alters an old tip's split, and
refunds read the stored snapshot, never current config. This is the same
immutable-snapshot discipline the alert path already uses.

### 24.4 Work sequence

EN-00 approve the commercial and legal model · EN-01 org, roles, allocations · EN-02
immutable snapshot schema · EN-03 creator-direct / enterprise-retained / Route adapters
· EN-04 pre-order snapshot resolver · EN-05 visibility and finance-control APIs · EN-06
transfers, refunds, reconciliation · EN-07 scheduler handlers · EN-08 dashboard views ·
EN-09 pilot rollout.

### 24.5 Reopening gate

Written evidence required on: Route linked-account onboarding, KYC, transfer, reversal,
refund, dispute and settlement · merchant-of-record and funds-flow model · TDS, GST,
KYC, AML, FCRA, consumer and privacy obligations · seats, invitations, auto-allocation,
roles, reporting, billing and support model · immutable effective-dated snapshots ·
finance access, step-up auth, audit and refund authority.

Until then: **no Enterprise tier, role, UI, allocation, fund movement, marketing CTA or
contact-sales flow anywhere.** In the new control plane this is a flag default, not a
convention.

---

## 25. Payment routing — Direct and Compatibility

Razorpay Direct is the recommended, verified rail. **Compatibility Routing** is an
honest second lane for creators who cannot use it yet — with a trust boundary drawn
hard enough that a provider changing behaviour overnight cannot damage us.

### 25.1 The two lanes

**Direct Integration — recommended.** Razorpay today; Paytm Business, PhonePe Business,
Google Pay Business and HDFC move here as official integrations land. Direct
BharatStudio checkout, HMAC-verified webhook confirmation, full alerts, TTS, Sound
Moments, receipts, goals, leaderboard, and refund reconciliation where the rail
supports it.

**Compatibility Routing — Beta, best-effort.** The creator configures their own
provider identity. BharatStudio still owns the whole experience: the single supporter
tip page, the payment attempt UI, the Sound Moment / TTS / overlay event, the activity
dock, Companion control, goals and supporter interaction. Only the *payment
confirmation signal* comes from whatever the provider exposes.

### 25.2 How it is presented — never as a direct integration

```text
Compatibility Routing — Beta
Uses available provider routing signals to trigger BharatStudio events.
Alerts can be delayed, duplicated, missed, or stop working if the
provider changes its behaviour.
Recommended for creators who cannot yet use Razorpay.
```

The creator **accepts this on enabling the route**. It does not live in Terms.

**These routes are labelled Beta and explicitly not recommended.** The card says so, the
dashboard says so, and the acceptance step says so. A creator must finish enabling one
knowing it can be withdrawn at any time — by us, or by the provider, without notice.

**What the Terms must state, in the creator's own acceptance flow and not buried:**

- The provider's terms bind the creator as the account holder. If those terms prohibit
  credential sharing or automated access, using this route may put the creator in breach
  and **the provider may suspend or terminate their merchant account**. BharatStudio
  cannot restore it.
- *(Removed 2026-09-14.)* A generic clause here previously told creators they could
  authorise BharatStudio to hold a provider PIN or password. It is deleted. **No generic
  credential language exists anywhere in the product.** A consent flow that mentions a
  credential may only ever appear inside a **named, provider-approved route**, describing
  that route's specific delegated sub-user and its specific secret — and no such route
  has passed its four gates, so no such flow may be built or shown today (§25.5, §1.9
  phase R).
- Detection is best-effort. Alerts may be delayed, duplicated, missed or stop entirely,
  and a routed signal is **not** a verified payment or a receipt.
- The route may be removed at any time, by us or by the provider, with the notification
  sequence in §25.6.1 where circumstances allow it.
- Razorpay Direct is the recommended, verified alternative and is always available.

Responsibility for the provider relationship sits with the creator. **Our own
obligations do not transfer with it** — breach notification, secure handling under
C1–C7, and honest labelling remain ours regardless of what the creator accepted.

Live health state, shown on the dashboard and in Companion:

| State | Meaning |
|---|---|
| **Active** | Recent routing signals arriving normally |
| **Degraded** | Delayed or inconsistent signals |
| **Paused** | Route disabled — provider change or reliability failure |
| **Direct available** | An official integration now exists; migrate |

### 25.3 The internal state boundary — the part that protects us

A routed signal is **never** a verified payment. Internally:

```text
routed_signal_received  →  alert_queued  →  alert_delivered
```

`verified_payment` is reserved for a rail with a cryptographically verified provider
confirmation. A routed signal is promoted to `verified_payment` only if an official
direct integration later confirms it.

**Works in routing mode:** tip-triggered alerts · creator-approved sounds and Sound
Moments · TTS · stickers and visual effects · supporter message cards · goals, ticker,
recent supporters · Companion event queue · Master Canvas · activity dock · outbound
Streamer.bot and OBS bridge events.

**Must stay unavailable in routing mode:** official payment receipts · automatic
refunds · entitlement unlocks · prize distribution · membership or paid access ·
payout splitting · tax reports · irreversible supporter badges · financial dispute
decisions.

That boundary means a provider silently changing its behaviour costs us delayed alerts,
never a wrong receipt or a false financial record.

### 25.4 The kill switch, built on day one

1. Mark the route **degraded**.
2. Stop accepting new payment attempts through it once confidence falls below threshold.
3. Let already-started attempts settle or expire safely.
4. Disable automatic alert triggering the moment duplicate or false signals appear.
5. Tell the creator: *"This provider's compatibility route is temporarily unavailable.
   Switch to Razorpay Direct or another active route."*
6. **Keep their settings. Pause the route** rather than silently producing wrong alerts.

**No generic QR fallback. No "mark as paid". No fake confirmation.** Ever.

### 25.5 Per-provider assessment — and where I stop

Competitor research shows the incumbent's actual flows. The product *structure* is
worth copying. The credential handling is not.

| Route | Their pattern | Our position |
|---|---|---|
| **Paytm Business** | Legal name, Business VPA, 21-char Merchant ID, optional QR upload to extract the VPA | **Safest to pursue.** Merchant identity only, no credentials. Build first — *once the signal mechanism is known* (§25.6) |
| **Google Pay Business** | Fields locked; activation done manually by their support | **Assisted activation.** Acceptable: no credential, manual gate, low volume |
| **PhonePe Business** | Creator creates a delegated **Supervisor** user on a spare number, logs in once to activate, then hands us the number — and must never log in again | **Gated.** See below |
| **HDFC SmartHub Vyapaar** | Creator creates a **Cashier** user, sets a **4-digit mPIN**, and hands us the number and mPIN | **Gated.** See below |
| **Amazon Pay** | Creator enters their Amazon **mobile/email and account password** | **Never build.** Non-negotiable, and not reopened by C1–C7 — see the note below the table |

**Amazon Pay is outside the consent decision entirely.** C1–C7 apply to *delegated
sub-user* routes — a Supervisor or Cashier account the creator creates for this purpose
and can revoke without losing their own access. Amazon Pay is a **consumer account
password**. Different category, different failure mode, permanently excluded. Any later
document that shows it as pending or buildable is stale and this line wins.

**Owner decision 2026-09-13, amended 2026-09-14: the delegated-sub-user routes proceed
on a consent basis, and remain phase label R (research only) until written provider
permission, counsel sign-off, a security design review and a provider sandbox route all
exist.** Consent is one of four gates, not the gate. No schema, no UI and no marketing
for these routes before all four close.
The creator gives explicit, specific, unbundled consent to share delegated-account data,
and the T&C place responsibility for that sharing with them.

**What that consent does and does not settle** — recorded so the risk is carried
knowingly rather than assumed away:

*Settled by consent.* The privacy and data-sharing dimension. With a DPDP-compliant
purpose statement, unbundled consent, and a stated retention rule, collecting and
processing the delegated-account data is defensible.

*Not settled by consent, because the creator is not the party whose permission is
missing:*

1. **The provider's terms bind the account holder.** If PhonePe or HDFC prohibit
   credential sharing or automated portal access, the creator's agreement with us does
   not make it permitted — it puts the *creator* in breach and makes us the inducing
   party. The realistic failure is not litigation against BharatStudio; it is the
   provider terminating a creator's merchant account mid-stream. Our indemnity does not
   give them their account back, and it is our product they will blame.
2. **An mPIN is a payment authentication credential.** A contract between us and a
   creator does not override Indian payment regulation, nor our own breach-notification
   duties if it leaks.
3. **Four digits × thousands of creators** is a low-entropy secret set of very high
   value. That is a security problem independent of who agreed to what.

**Therefore these routes proceed only when all of the following hold:**

| # | Condition |
|---|---|
| C1 | **Legal sign-off**, specifically covering delegated-credential handling — folded into the existing unfiled legal gate, not a separate opinion |
| C2 | The provider's terms read directly and recorded, with a dated note on whether delegated access is permitted. If clearly prohibited, we do not build it — consent does not cure a third-party prohibition |
| C3 | No sanctioned alternative exists (merchant webhook, reporting API, partner programme) that reaches the same signal without a credential. If one exists, we build that instead |
| C4 | Consent is explicit, specific, unbundled, revocable in one action, and re-confirmed whenever the scope changes. Never a pre-ticked box, never inside general Terms |
| C5 | The secret is held under **KMS/HSM envelope encryption**, never in plaintext at rest or in logs, with per-access audit and no human read path |
| C6 | A creator can revoke instantly, and revocation deletes the secret rather than disabling a flag |
| C7 | Blast-radius controls: per-route kill switch (§25.4), anomaly detection on access patterns, and a rehearsed incident procedure specific to credential compromise |

**C1–C7 do not apply to Amazon Pay and never did.** They govern *scoped delegated
business users* — a PhonePe Supervisor or an HDFC Cashier the creator creates for this
purpose and can revoke without losing their own access. Amazon's flow takes the
creator's **primary consumer account password**, which also reaches their shopping
account, saved cards, addresses and order history. That is a different category of
credential with a different failure mode, and no condition in this list reaches it.

**Amazon Pay is never built.** See the note under the §25.5 table and the decision row
in §33.1. The paragraph that previously stood here said "build under C1–C7, behind an
admin switch"; it was wrong, it contradicted the table two screens above it, and it has
been deleted rather than annotated, per §35.1 rule 7.

### 25.6 Every route has an admin master switch

**Every payment route** — Razorpay Direct included, not only the compatibility ones —
is a capability-registry row (§20) with its own switch, so any route can be enabled,
disabled, restricted to a tier, rolled out to a percentage, or killed outright without
a deploy. One uniform mechanism, no special cases. This is what makes a high-risk route acceptable to attempt:
**we can withdraw it in one action.**

| Control | Effect |
|---|---|
| `global_kill` | Route disappears for everyone immediately; existing settings retained |
| `min_tier` | Which tier may use it |
| `rollout` | Percentage or allowlist, for a cautious first cohort |
| `beta` | Forces the Beta labelling and the acceptance step |
| `sunset_date` | Starts the notification sequence below |

#### 25.6.1 Notifying creators when a route is added or removed

**Adding a route:** a dashboard notice and a Companion card. No action needed, nothing
changes for anyone already set up.

**Planned removal** (we withdraw it, or a Direct integration supersedes it):

1. **T-30 days** — the route is marked *Sunsetting* with the date, in the dashboard, in
   Companion, and by email. The card explains why and names the recommended
   alternative.
2. **T-14 days** — reminder, and the route stops accepting *new* creators.
3. **T-7 days** — daily reminder to affected creators only.
4. **On the date** — the route moves to **Paused**. Settings, mappings and history are
   retained under the §26 lifecycle. Nothing is deleted.
5. **T+90 days** — held credentials are revoked and deleted, after a final notice.

**Emergency removal** (provider blocks us, or signals become unreliable):

1. Route pauses immediately; in-flight attempts settle or expire safely.
2. The creator is told **the same hour**, in Companion and by email, that it is
   provider-side and not their fault.
3. The dashboard shows the migration path to Razorpay Direct.
4. Settings are retained exactly as in a planned removal.
5. If the cause is a credential compromise, C7's incident procedure runs and credentials
   are revoked before notification, not after.

**A creator on a paid tier whose only route is withdrawn is never billed for a
capability we removed** — the next invoice is credited automatically.

### 25.7 Per-provider assessment — and where I stop

Competitor research shows the incumbent's actual flows. The product *structure* is
worth copying. The credential handling is not.

| Route | Their pattern | Our position |
|---|---|---|
| **Paytm Business** | Legal name, Business VPA, 21-char Merchant ID, optional QR upload to extract the VPA | **Safest to pursue.** Merchant identity only, no credentials. Build first — *once the signal mechanism is known* (§25.6) |
| **Google Pay Business** | Fields locked; activation done manually by their support | **Assisted activation.** Acceptable: no credential, manual gate, low volume |
| **PhonePe Business** | Creator creates a delegated **Supervisor** user on a spare number, logs in once to activate, then hands us the number — and must never log in again | **Gated.** See below |
| **HDFC SmartHub Vyapaar** | Creator creates a **Cashier** user, sets a **4-digit mPIN**, and hands us the number and mPIN | **Gated.** See below |
| **Amazon Pay** | Creator enters their Amazon **mobile/email and account password** | **Never build.** Non-negotiable |

**Amazon: never.** Collecting a consumer account password is credential harvesting
regardless of intent. It cannot be made safe with encryption, it violates the
provider's terms, and one breach would end the company. No experimental gate, no
opt-in, no exception.

**PhonePe and HDFC: gated on three answers, not scheduled.** As described, these
require us to hold a delegated login — and in HDFC's case a **4-digit mPIN**, which is
a payment credential — and to operate a provider's business portal as that user. That
collides directly with our own standing rule (§12.1: *never store banking credentials*)
and with the reasoning that ruled out BYOK and InnerTube. Before any design work:

1. **Does the provider permit it?** A written answer, or the relevant terms read
   directly. Delegated-user credential sharing and automated portal access are commonly
   prohibited. If prohibited, we do not build it, exactly as with BYOK.
2. **Is there a sanctioned alternative?** A merchant webhook, a reporting API, or a
   partner programme reaching the same signal without holding a credential.
3. **If permitted, can the secret be avoided?** Store nothing reusable, or nothing at
   all. An mPIN in our database is an unacceptable design even encrypted.

If all three resolve favourably, these ship as compatibility routes with the §25.2
labelling. If not, they do not ship, and the honest creator message is "use Razorpay
Direct" rather than a route we cannot operate safely.

### 25.8 The engineering point everyone skips

**None of the competitor's cards reveal how the payment event is actually detected.**
Merchant ID plus VPA does not, by itself, tell anyone that a payment happened. The card
UI is the easy half; the *signal* is the product.

So no compatibility route enters the build queue without a documented, permitted
detection mechanism — webhook, reporting API, or sanctioned callback — named and
verified. Building the card first and discovering the signal later is how we end up
with the delegated-credential pattern by default.

**What we build now, provider-agnostically:** the routing abstraction, the health-state
machine, the honest labelling, the `routed_signal_received` state class, the capability
restrictions of §25.3, and the kill switch. That framework is valuable on its own and
lets any verified route slot in later.

---

## 26. Subscription lifecycle — paid integrations that fail gracefully

Connect, import and compatibility features are paid. **A lapsed subscription must never
turn a creator's live stream into a broken screen or a payment wall on camera.**

### 26.1 Never charged for

Viewing receipts · exporting their own data · recovering their account · disconnecting
an integration · basic security controls (sessions, revoke, password, 2FA). Charging
for any of these makes leaving hostile, and §13 makes portability a feature.

Extended 2026-09-14 by §12.6, which governs: **every durable creator record** —
payments, receipts, refunds, audit trail, supporter relationships, event history,
configurations, layouts and moderation history — remains stored, viewable, searchable,
fetchable and exportable in every state below, including Expired, at no charge. A lapse
pauses what costs money to run. It never withdraws access to what we already accepted.

### 26.2 The five states

| State | Duration | Behaviour |
|---|---|---|
| **Active** | — | Everything works |
| **Grace** | 14 days | Everything still works. Clear notices in Companion and dashboard, never on stream |
| **Paused** | — | Paid connectors stop processing new third-party events. Imported setups and configuration become **read-only** |
| **Retained** | 90 days | The window in which **encrypted third-party connector secrets** are still held so a renewal reconnects without re-authorising. Configuration, mappings, templates and every durable record are **not** on this clock — they persist under the uniform retention policy (§12.6.2) and stay viewable and exportable throughout |
| **Expired** | after notice | **Only the provider credentials and connector secrets are revoked and destroyed** — a security necessity, since we must not hold a third-party secret for an account that has stopped paying us to use it. Everything else stays: configuration, layouts, mappings, templates, and every durable record, still viewable and exportable. Reconnecting restores the setup |

Advance notices precede every transition, and the destruction of provider secrets at
Expired is announced more than once. **Corrected 2026-09-14:** an earlier version of
this table deleted paid-only *configuration* at Expired. That contradicted §12.6 —
configuration is a durable record — and only the third-party secrets are destroyed.

### 26.3 What the creator sees after grace

- **Existing OBS URLs keep working.** They must never become a payment wall and must
  never advertise BharatStudio on stream. A billing problem is not the audience's
  business.
- The Master Overlay falls back to a **quiet safe state**: transparent, or basic native
  alert behaviour, with no premium module output. No error text, no watermark change
  mid-stream.
- External synchronisation, outbound automations, multi-channel routing, premium packs
  and bridge commands pause.
- **Kept regardless:** account access, receipts, verified payment history, audit
  history, exports, security controls.
- Native and free behaviour stays independent of subscription status *and* of Platform
  availability.
- **Nothing is silently deleted** — not scenes, alert settings, media, or imported
  mappings.
- On renewal, configuration restores without reconnecting everything, unless the
  provider token itself expired or was revoked.

### 26.4 Desktop bridge resilience

Where a local helper exists, it caches a **signed entitlement valid for 24 hours**. A
billing hiccup or a connectivity outage must not break a live stream. The cache is
short enough to bound abuse and long enough to cover any realistic outage.

### 26.5 Why this is a competitive feature, not just courtesy

Creators have been burned by tools that break mid-stream. A documented, generous,
non-punitive lapse policy is a reason to switch — and it costs us little, because the
expensive parts (connector processing, outbound automation, AI) are exactly what pauses.
Storage and configuration are cheap to retain for 90 days.

---

## 27. Social Relay

**One creator event becomes an approved, platform-specific action — never the same
message blasted everywhere.** That distinction is the entire product. Blasting gets
creators muted, rate-limited and banned, and the blame lands on the tool that did it.

### 27.1 What relays, and what never does

**Relayable events:** go-live and scheduled-live reminder · title or category changed ·
collaboration or squad announcement · new clip/reel/short ready for review · milestone
or goal completed · lobby or session opening · post-stream recap · supporter thank-you
**only where that supporter explicitly opted in**.

**Never auto-relayed:** every tip · every follower · every alert · anything to every
network at once. High-frequency events stay on the overlay and in Companion, which is
where they belong.

Every relay is **approve-then-send by default**. A creator may enable auto-send per
event type per destination, and that is a deliberate choice, not the default.

### 27.2 Platform map — what we can promise, and what we cannot

**Every cell in this table is an undocumented assertion until it carries evidence, and
platform capabilities change without notice.** Before any row below becomes a product
promise — in the UI, in marketing, or in a register row moving past `A` — it must carry
six things, dated and checked in:

| Field | Requirement |
|---|---|
| **Source** | The official provider document, with its URL and the date it was read |
| **OAuth scope** | The exact scope required, and whether it needs provider review |
| **Rate limit or quota** | The published number, its unit, and what we do at the ceiling |
| **Privacy data flow** | What personal data crosses, on what basis, retained how long |
| **Failure mode** | What the creator sees when the platform says no |
| **Owner** | One named person who re-verifies it on a schedule |

A row that has gone **stale past 180 days fails the marketing snapshot build** (§20.4),
the same way a stale gateway fee does. The table below is our current reading, not
verified fact, and the Kick, Instagram and WhatsApp rows in particular are the ones most
likely to be wrong by the time they are built.

| Platform | What we build | What we must never promise |
|---|---|---|
| **YouTube** | Schedule/manage live, title, description, privacy, thumbnails, tags · live chat in Companion · rate-limited chat announcements · polls · pinned rules/lobby/tip link at controlled moments · Super Chat, membership, gifting and moderation events · post-stream wrap with timestamps | **Community posts and DMs** — no supported API route |
| **Instagram** | Publish approved Reels and feed posts · clip-to-Reel drafts · Stories for eligible Business accounts · comment and mention inbox · "Live now" link card | **Personal accounts** (Professional only) · **unsolicited DMs** · group-DM alerts |
| **Twitch** | EventSub: follows, subs, gifts, raids, cheers, chat, redemptions · Channel Point redemptions mapped to safe BharatStudio interactions · polls, predictions, moderation queue, clips, multi-chat · OBS bridge triggers | Transferring platform money · paid chance mechanics |
| **Kick** | OAuth 2.1 connection · read stream/channel state · send chat · listen to chat, follows, subs · rewards and overlay integration · moderation where scoped | Anything outside currently granted scopes |
| **Discord** | One-way channel alerts via webhook · rich embeds with thumbnail, countdown, link button · bot commands `/live` `/queue` `/goal` `/tip-page` `/schedule` · role-gated lobby registration · supporter opt-in roles | **Bulk unsolicited DMs** |
| **WhatsApp** | Opt-in "notify me when live" · approved live and event reminder templates · verified payment status and receipts · user-initiated support inbox · click-to-chat community links | **Automatic group posting** · unsolicited messaging · relaying a supporter's tip message |
| **Snapchat** | Turn a stream moment into a vertical Snap/Story/Spotlight-ready asset with caption, sticker, link and topic prefilled — **creator taps the final share** | Background posting to ordinary accounts |
| **Telegram** | Optional bot channel alerts, polls, commands, community queue | Replacing our own identity and moderation layer |

### 27.3 The rate-limit discipline

Every destination gets a **per-channel queue with a cooldown**, never a send-per-event
rule.

- **YouTube** rejects excessive chat sends — announcements are queued and cooled down,
  and a pinned message is a scheduled moment, not a reflex.
- **Discord** returns dynamic rate-limit headers; we **obey the returned headers**
  rather than hard-coding a number. The general bot ceiling is 50 requests/second and
  we stay far below it.
- **WhatsApp** allows free-form replies only inside the 24-hour window after the user
  writes. Outside it, only approved templates, only with opt-in, and those cost money —
  so template sends are metered and shown to the creator as a cost.
- **Instagram** conversations must be user-initiated. Use click-to-message,
  comment-keyword opt-in, or a "remind me" flow — never a tip-triggered DM.

A destination that returns a limit error backs off and surfaces a **Degraded** state,
the same health model as payment routing (§25.2).

### 27.4 Uploads and verification

We can prepare and upload a Short or VOD, but **uploads from an unverified API project
may be forced private until Google audits it**. That is disclosed in-product before a
creator relies on it, and it joins the unfiled external gate list alongside OAuth
verification and quota.

### 27.5 Lapse behaviour

On lapse: retain read-only connection configuration · stop new automatic sends after
grace · keep manual share links working · and **never send a "your subscription
expired" message to the creator's audience**. The audience is not party to the billing
relationship.

---

## 28. Add-on packs

Tiers sell a **capability class**. Packs sell **capacity and scope**. Keeping that line
clean is what stops the pricing page becoming unreadable and stops packs cannibalising
upgrades.

### 28.1 The rules

1. A pack **never** grants a correctness capability (§30.1 of the tier matrix), and
   never touches a durable creator record (§12.6). *Corrected 2026-09-14 — this rule
   previously cited §27.1, which is Social Relay.*
2. A pack is **never the only way** to get something — it deepens a capability the
   creator's tier already has, or adds capacity to it.
3. Every pack is a capability-registry row (§20), so staff can retier, reprice or kill
   it without a deploy.
4. Packs stack additively with tier allowances and never replace them.
5. A lapsed pack follows the §26 lifecycle: paused, retained 90 days, nothing deleted.

#### 28.1.1 Top-up or pack — the line, decided 2026-09-14

The two menus overlapped: extra seats, connectors, media slots and outputs appeared in
both, with no settled commercial model behind either. One rule now decides which menu an
item belongs to, and **nothing appears in both**.

| | Top-up | Pack |
|---|---|---|
| **What it is** | A prepaid balance you spend once | A monthly subscription that raises a standing limit |
| **Billing** | One-time purchase, additive to the tier allowance | Recurring, additive to the tier allowance |
| **Runs out by** | Being consumed | Being cancelled |
| **Examples** | AI credits · TTS characters | Seats · connectors · storage · channels · outputs · sticker and media slots · sponsor campaign slots |

Consequences, applied in §10.2:

- **Top-ups shrink to the two genuine consumables**: AI credits and TTS characters.
- Everything else that was in the top-up menu — asset storage, extra connectors, extra
  moderator seats, sticker and media pack slots, sponsor campaign slots, vertical and
  multi-canvas outputs, priority queue burst capacity — **moves to packs**, because each
  one raises a standing limit rather than being spent.
- A creator who wants ₹99 of AI credits once never has to start a subscription to get
  it. That is the whole reason top-ups survive as a category.
- Season Pass issuance is neither: it is a creator's own monetisation product (§10.4),
  billed on its own terms, and it leaves both menus.

### 28.2 The packs

| Pack | What it adds | For |
|---|---|---|
| **AI Credits** | Consumable units, three classes (§11) | **Paid tiers only**; the only pure consumable |
| **Socials Pack** | +3 connected accounts · auto-send per event type · post scheduling · multilingual variants · social calendar | A Creator-tier streamer who promotes seriously but does not need Studio's team features |
| **Events Pack** | Full tournament brackets · lobby templates · recurring community nights · advanced giveaway formats | Creators who run community nights but stream alone |
| **Team Seats** | +2 moderator or operator seats, +1 concurrent control session | A growing creator with helpers, not yet a studio |
| **Storage Pack** | +500MB for **new** uploads, +50 sound uploads. Never buys back access to anything historical (§12.6.2) | Heavy Sound Moments users |
| **Sponsor Pack** | Sponsor manager · scheduled placements · exposure log · proof-of-delivery report | A creator who just landed their first sponsor |
| **Multi-Channel Pack** | +1 channel or brand under one account | Creators running a second persona or a clips channel |
| **Finance Pack** | Monthly statement · GST-ready export · TDS reference notes · payout-vs-bank reconciliation view | See §29.2 — this is the one I would build first |

**Deliberately not a pack:** anything in §30.1 correctness, **any durable creator
record under §12.6** (payments, receipts, refunds, audit trail, supporter
relationships, event history, configurations, layouts, moderation history, their search
and their export), retention or history depth, account recovery, security controls, or
Companion itself. Corrected 2026-09-14 — this list previously cited §27.1, which is
Social Relay, not the correctness list.

### 28.3 Pack pricing — proposed, GST-inclusive at 18%

**Status: proposed 2026-09-14, not approved.** No pack ships in v1 (§1.9 — packs are a
P3 slice), so this is the price sheet for the first pack release, not a launch price.

| Pack | Price | Eligibility | What the creator gets | What is still missing — the actual gate |
|---|---|---|---|---|
| **AI Credits** | ₹49 / ₹149 / ₹399 top-ups | Paid tiers | Extra prepaid usage for AI writing, translation, summaries, moderation assistance and premium TTS | A **measured provider cost model**, per-action credit pricing, spend caps, abuse controls and a quality evaluation. Without the cost model we cannot price a unit; without spend caps one runaway loop bills a creator for a month |
| **Storage Pack** | ₹49/mo, +500MB of new-upload space and +50 sound uploads | Pro+ | Room for more custom audio and media | The **asset quota pipeline is specified and not enforced** (MED-13, AUD-10), and the media lifecycle — quarantine, scan, provenance, takedown — is the §18.3 gate, still open |
| **Socials Pack** | ₹129/mo | Creator+ | +3 connected accounts, scheduled posts, event-triggered posting, multilingual variants, social calendar | **Social Relay itself** (P3), plus each platform's approved API and permissions. No unofficial posting routes, ever |
| **Multi-Channel Pack** | ₹199/mo per added channel or brand | Creator+ | A second channel or brand under one account | **Strong tenant and channel separation** — RLS boundaries, role scoping across channels, billing allocation, connector routing, and per-channel audit. This is the largest hidden item on the list |
| **Events Pack** | ₹129/mo | Creator+ | Full brackets, lobby templates, recurring community nights, advanced giveaway formats | The **Lobby and tournament engine** (§16, §17) and the fair-giveaway safeguards. Free-entry and skill-based only stands (§33.1) |
| **Team Seats** | ₹129/mo | Creator+ | +2 moderator or operator seats, +1 concurrent control session | Seat **management** — invitations, scoped permissions, audit, session control (F18). The enforcement exists in `0104`; the management UI does not |
| **Sponsor Pack** | ₹149/mo | Creator+ | Sponsor campaign workspace, scheduled placements, exposure timeline, proof-of-delivery report | The sponsor manager, the campaign workflow, and **correctness of the evidence report** — a proof-of-delivery document that is wrong is worse than no report, because a creator will send it to a sponsor |
| **Finance Pack** | ₹79/mo | Creator+ | Monthly statement, GST-ready export, TDS reference notes, payout-vs-bank reconciliation | Provider evidence **plus CA/tax/legal review**. It must not make an unsupported tax claim, and today we cannot make any |

#### 28.3.0 Why these are gated, and whether the gate is worth keeping

The question is fair: every one of these would upsell, so why hold them? The answer
differs per pack, and only two of the eight are being held for a reason we could
choose to drop.

**Held because selling it would be a false promise.** Sponsor and Finance. A
proof-of-delivery report a creator forwards to a sponsor, and a GST-ready export a
creator hands to their CA, are documents that leave our product and get relied on by a
third party. Shipping either before it is correct does not lose us a sale later — it
costs us the creator, because they find out in front of someone whose opinion of them
matters. Finance additionally cannot make a tax claim of any kind until the CA row in
`05_SUPPORT_AND_EXTERNAL_EVIDENCE_REGISTER.md` closes.

**Held because the feature does not exist yet.** Events and Socials. A pack is a
capacity and scope multiplier on a real capability (§28.1); there is nothing to
multiply. The gate lifts the day the engine ships, and no extra decision is needed.

**Held because the enforcement is missing, not the feature.** Storage and Team Seats.
Both are the closest to sellable — the quota ladder is specified, seat enforcement is
already in `0104` — and both would sell a limit we cannot currently apply. Selling
"+500MB" when no quota is enforced means the creator paid for something they already
had, which is the worst version of an upsell.

**Held because the price has no basis.** AI Credits. We can build it; we cannot yet
say what ₹49 buys, and publishing a number we then have to cut is far more damaging
than launching a month later (§33.2 item 5).

**Held because of an architectural dependency people underestimate.** Multi-Channel —
see below.

#### 28.3.1 Practicality check on the four "first visible" packs

The proposed initial set is AI Credits, Storage, Socials and Multi-Channel, on the
grounds that each maps to a sentence a creator would say. That reasoning is right, and
two of the four have dependencies that make them the *last* of the eight to be ready,
not the first.

| Pack | Realistic readiness |
|---|---|
| **Storage** | **Nearest.** Needs MED-13/AUD-10 enforcement and the §18.3 gate — both already P0/P1 work we are doing anyway |
| **AI Credits** | **Near, once metered.** The ledger half exists (`0081`); what is missing is a measured cost model, which is a fortnight of real usage data, not an engineering project |
| **Socials** | **Blocked on a P3 slice.** Social Relay is Phase 7. The pack cannot precede the feature by definition |
| **Multi-Channel** | **The largest item on the list, disguised as a pack.** Tenant separation, cross-channel role boundaries, billing allocation, connector routing and per-channel audit are Enterprise-shaped problems (§24). Selling a second channel on top of weak separation risks one brand's data appearing under another — the single worst bug this product could ship |

**Amended 2026-09-14: the pack system launches with the packs that are ready, not with
a fixed set of four.** The four named above remain the *target* initial set, and the
order they actually arrive in is **Storage → AI Credits → Socials → Multi-Channel**.
Holding the pack system closed until the slowest of the four is ready would delay two
sellable packs behind an Enterprise-shaped dependency for no benefit.

**Multi-Channel does not ship until tenant separation has an isolation test suite that
passes** — see §37.6. That is not a gate we relax for revenue.

#### 28.3.2 The boundary that applies to every pack

Restated because it is the one that would be easiest to erode under upsell pressure:

- **A pack never limits access to existing payments, receipts, refunds, supporter
  history, layouts, configurations, audit records, search or export** (§12.6). None of
  those is capacity.
- **Storage restricts new uploads only.** Running out blocks the next upload and
  nothing else. Nothing already uploaded is hidden, truncated, degraded or deleted.
- **A lapsed pack pauses future added capacity and retains everything.** Over-quota
  assets go read-only and stay viewable and exportable; configuration and data are kept
  (§26, §12.6.1 rule 4). A lapse is never a deletion trigger.
- **A pack never grants correctness** (§30.1) and is never the only route to a
  capability (§28.1).

Each hidden pack is a capability-registry row (§20), so it becomes visible without a
release the moment its gate closes.

#### 28.3.3 Where I changed your numbers, and why

Two changes to the proposed menu, both to make its own stated logic actually hold.

**Socials, Events and Team Seats: ₹99 → ₹129.** The rule "Creator plus two or more
packs should push a customer toward Studio at ₹599" fails at ₹99 — Creator ₹399 plus
two ₹99 packs is **₹597**, which sits *below* Studio while delivering less. That is
exactly the trap the rule exists to avoid, and a customer who finds it is right to feel
misled when they later discover Studio was cheaper and larger. At ₹129 the cheapest two
feature packs (Finance ₹79 + Socials ₹129) reach **₹607**, and every other pair is
higher, so the ladder works as intended.

The single-pack rule is unaffected: Creator plus one pack lands between ₹448 and ₹598,
all below Studio.

**Multi-Channel stays at ₹199, and the ₹1 gap is deliberate.** Creator ₹399 + ₹199 =
**₹598** against Studio at **₹599**. That reads like an accident and it is not: a
customer comparing them pays one rupee less for one extra channel and none of Studio's
seats, approvals, tournaments or pooled AI. It is the sharpest possible steer toward
Studio and it costs us nothing. **Do not "fix" it later** without re-reading this
paragraph.

#### 28.3.4 The pricing rules behind the sheet

- **Creator + one focused pack stays below Studio.** A creator with one real need is
  not pushed into a tier they do not need.
- **Creator + two feature packs exceeds Studio.** Two needs means Studio, and the
  arithmetic must say so rather than the sales copy.
- **Storage and AI Credits are capacity, not feature packs**, and are excluded from
  that second rule. Buying space or credits is not a signal that someone needs a
  bigger tier.
- **Multi-channel is deliberately expensive.** Multiple brands are operationally
  costly, and Studio should be the obvious answer.
- **AI is prepaid and consumption-based.** We do not promise a fixed number of model
  tokens, or a fixed number of anything, until real provider cost, retry behaviour and
  the §10.1 margin floor are measured. The three top-up sizes are approved; **what a
  rupee buys is not**, and stays open (§33.2) until the cost model is measured.
- **A pack never grants correctness, never grants access to a durable record, and is
  never the only route to a capability** (§12.6, §30.1).
- **Storage never restricts historical records** — only future creator media uploads.
  Running out of space blocks the next upload and nothing else.
- Every price here is **GST-inclusive at 18%**, matching how the tiers are quoted.
- A pack, like a tier, may be **withdrawn only through the §25.6.1 notification
  sequence**, and a creator is never billed for a capability we removed.

### 28.4 Why packs beat more tiers

A fifth tier forces a creator to buy nine things to get one. Packs let a Creator-tier
streamer who runs tournaments buy exactly that, and they give us a much better signal:
**pack attach rates tell us what the next tier should contain**, using real money rather
than a survey.

---

## 29. Day-to-day creator jobs we could solve

Beyond the stream itself. Ordered by how often the pain recurs.

### 29.1 Scheduling and consistency

A **content calendar** holding stream schedule, planned socials, sponsor commitments and
lobby nights in one place — with a public schedule page carrying "notify me" that feeds
the WhatsApp and Discord opt-ins we already have. Plus a consistency view: streak,
hours, rest days. Creators burn out on an invisible treadmill and a rest day shown as a
deliberate choice rather than a broken streak is a genuinely kind piece of design.

### 29.2 Finance and compliance — the biggest unserved need in India

Nobody serves this well, it recurs monthly, and we already hold the ledger.

Monthly earnings statement · **GST-ready export** · TDS reference notes · payout-versus-
bank reconciliation · per-sponsor income breakdown · year-end summary for a CA.

**The hard boundary: we export data, we never give tax advice.** Every artefact is
labelled as a record for the creator's accountant, never as a filing or a
recommendation. This needs the same legal review as the rest of the money surface, and
it is the single feature most likely to make a serious Indian creator switch — because
it is the job they currently do in a spreadsheet at midnight.

### 29.3 Sponsors

A deliverable tracker: what was promised, when it is due, what proof exists. Paired with
the exposure log the Sponsor Card already produces, that turns "did I do the sponsor
read" into an auditable record a creator can invoice against.

### 29.4 Content operations

Clip request queue from the audience · a clip-to-social pipeline that ends in a draft,
never an auto-post · title and thumbnail performance tracking against our own stream
records · an editor handoff pack (§11.4) · a shareable gear and setup profile, which
answers the most-asked chat question automatically.

### 29.5 Relationships

A lightweight collab record — who, when, which format, how it performed — so a creator
can see which collaborations actually grew them. Community FAQ auto-answers in chat for
the questions asked every single stream.

### 29.6 What I would not build

- **Editor payouts or revenue splitting with staff.** It is money movement, needs
  escrow or Route, and drags us into being a payroll product.
- **A full CRM.** Creators will not maintain it.
- **Cross-posting to every network on a schedule.** That is the spam pattern §27 exists
  to prevent, wearing a calendar as a disguise.
- **Analytics competing with YouTube Studio.** Report on what *we* uniquely see —
  support, goals, sponsor exposure, lobby attendance — not on generic view counts.

---

## 30. Tier matrix

**This is the seed for the capability registry (§20), not a hard-coded ladder.** Once
the control plane exists, staff move any row at any time. What matters is that the
initial division is principled rather than arbitrary.

The principle, one line per tier:

| Tier | What it is |
|---|---|
| **Free** | Everything correctness-critical, plus a real working alert. Never crippled, always watermarked |
| **Pro ₹199** | Personality — voice, sounds, look, more alerts on screen |
| **Creator ₹399** | Community mechanics — goals, votes, lobbies, co-streams, connectors |
| **Studio ₹599** | **Brand and scale** — brand kits and multi-surface templates, multi-channel, team seats and approval workflows, events and tournaments, pooled AI, priority support |
| **Enterprise** | Governance-blocked (§24) |

### 30.1 Correctness — identical on every tier, forever

Payment verification · immutable records · webhook dedup · reconciliation · refund
tracking · queue durability and no-drop · retry and replay · security · privacy · audit
· accessibility · downgrade preservation · legal disclosures · receipts · anonymous
tipping with no login.

**And every durable creator record (§12.6), which is not a tier row at all.** Stated
here because a matrix invites someone to add a column to it:

| Always, every tier, no cap, no charge | Free | Pro | Creator | Studio |
|---|---|---|---|---|
| Payment, receipt and refund records — full history | yes | yes | yes | yes |
| Audit trail — full history | yes | yes | yes | yes |
| Supporter relationships and event history | yes | yes | yes | yes |
| Moderation history | yes | yes | yes | yes |
| Configurations and layouts, including over-quota ones | yes | yes | yes | yes |
| Search, filter and page all of the above | yes | yes | yes | yes |
| One-off export of all of the above, any size, open format | yes | yes | yes | yes |
| Retention window | **identical for everyone** | | | |

What remains tierable is **new active capacity only**: active connectors, active
widgets, AI usage, new media uploads, custom assets, team seats and automation volume.
The rows further down this matrix are all of that kind, and any row that is not is a
defect against §12.6.

### 30.2 The existing ladder (already enforced in code)

| Dimension | Free | Pro | Creator | Studio |
|---|---|---|---|---|
| Queues | 1 | 2 | 3 | 5 |
| Queue modes | fifo | +stacked, pills, aggregated | +priority | same as Creator |
| Visible items | 3 | 5 | 8 | 12 |
| Char limit | 100 | 150 | 300 | 500 |
| Display ms | 6,000 | 8,000 | 12,000 | 20,000 |
| Quiet mode | — | yes | yes | yes |
| Approval required | — | — | yes | yes |
| Premium TTS | — | 20K chars | 40K | 60K |
| Moderator seats | 0 | 0 | 2 | 5 |
| Connectors | 0 | 1 | 2 | 3 |
| Interaction types | 3 | 6 | 8 | 8 |
| Widget types | 1 | 3 | 7 | 7 |
| Sticker packs | — | 10 | 25 | 50 |
| Asset storage | — | 100MB | 250MB | 1GB |
| Companion slots | 8 | 16 | 32 | 64 |
| Companion page size | 4 | 8 | 16 | 16 |
| Control sessions (concurrent) | 1 | 1 | 2 | 4 |
| Read-only sessions | 2 | 3 | 5 | 8 |
| Event bindings | 3 | 5 | 10 | **50** |
| Saved presets | 1 | 2 | 4 | **20** |
| Pending visuals | 20 | 50 | 150 | 500 |
| Overlay watermark — one protected mark, fixed corner (§30.6) | yes | — | — | — |
| Tip-page attribution line (§30.6) | yes | — | — | — |
| Lottie / branding upload | — | — | — | yes |

**Event bindings and saved presets raised for Studio, 2026-09-14** (20 → 50 and 8 → 20).
These are stored configuration counts, not live payloads, so neither touches §12.7 or the
connection model. **Read-only sessions stay at 8** — those are concurrent transports and
interact with the RT-02 per-instance subscriber limits, so they wait for load evidence.

**Pending visuals stay 20 / 50 / 150 / 500, and 500 itself needs verification.** A
proposal to raise Studio to 2,000 was **rejected 2026-09-14**: a live surface may not
hold 2,000 items (§12.7). Server-side retention is a separate matter and depth is reached
by pagination and export, never by shipping it to the browser. Open question: whether the
existing 500 is what the overlay holds or what the server retains — if the former, the
current ladder is already over the bounded-data line and must be cut, not raised.

**Queue count: 1 / 2 / 3 / 5.** Two authorities disagreed — the launch authority carried
the now-superseded 1/3/5/10 while the migration, the remediation authority and this document carried
1/2/3/5. **Resolved 2026-09-14 by owner decision: 1/2/3/5 stands, and
`active/launch/00_LAUNCH_SCOPE_AUTHORITY.md` is amended** rather than overruled from
here. It matches what is enforced today, so there is no migration, no billing change and
no creator impact. Raising a limit later is painless; lowering one breaks creators.

### 30.3 Proposed placement for everything new

| Capability | Free | Pro | Creator | Studio |
|---|---|---|---|---|
| **Master Canvas modules active** | 2 | 5 | 12 | all |
| Support Theater, goal bar, ticker | yes | yes | yes | yes |
| Stat widgets (wins, streak, record) | — | 2 | all | all |
| Scoreboard, head-to-head | — | — | yes | yes |
| Tournament standings | — | — | — | yes |
| Vertical layout | — | yes | yes | yes |
| Scene profiles | 1 | 3 | 6 | unlimited |
| **Support Hub** | | | | |
| Amount presets, message, receipts | yes | yes | yes | yes |
| Free reactions, supporter wall | yes | yes | yes | yes |
| Approved sticker picker | — | yes | yes | yes |
| Sound Moments (catalogue) | — | yes | yes | yes |
| Goal ladder + milestones | — | yes | yes | yes |
| Pick-a-side vote | — | — | yes | yes |
| Embedded YouTube player | — | yes | yes | yes |
| Event layout presets | — | — | yes | yes |
| Campaign + referral links | — | — | yes | yes |
| "Where support goes" explainer | yes | yes | yes | yes |
| **Sound and media** | | | | |
| Browser TTS | yes | yes | yes | yes |
| Voice routing controls (§11.10) — a cost control, never sold | yes | yes | yes | yes |
| Creator sound uploads | — | 5 | 25 | 100 |
| Themed sound packs | — | 1 | 5 | all |
| Mega alert scene effects | — | — | — | yes |
| Loudness normalisation | yes | yes | yes | yes |
| **Interaction Rules Engine** | | | | |
| Amount thresholds | — | yes | yes | yes |
| Stream-mode rules (ranked, BRB) | — | — | yes | yes |
| Cooldowns and daily caps | — | — | yes | yes |
| Approval-required rules | — | — | — | yes |
| Never-interrupt-gameplay mode | — | yes | yes | yes |
| **Community** | | | | |
| Lobby Engine (queue, ready check, seats) | — | — | yes | yes |
| Lobby templates and filters | — | — | — | yes |
| Cross-creator lobbies | — | — | — | yes |
| Co-Stream Room (2 creators) | — | — | **yes** | yes |
| Squad grid (3–4 creators) | — | — | — | yes |
| Giveaways (free entry) | — | yes | yes | yes |
| Giveaways (scheduled, free entry) | — | — | yes | yes |
| Tournaments — single elim, up to 8 | — | — | yes | yes |
| Tournaments — double elim, round robin, seeding, sponsor slots | — | — | — | yes |
| **AI credits** (allowance) | trial | monthly | larger monthly | pooled team |
| AI credit **top-ups** (§28.3) | — | yes | yes | yes |
| AI moderation (live) | — | — | yes | yes |
| Thumbnail / Channel DNA | — | — | yes | yes |
| **Integrations and import** | | | | |
| BharatStudio tip page + native alert | yes | yes | yes | yes |
| Razorpay Direct | yes | yes | yes | yes |
| Compatibility Routing (a verified route) | — | — | yes | yes |
| OBS scene / template import | — | — | yes | yes |
| Streamlabs / StreamElements migration + bridge | — | — | yes | yes |
| YouTube connection + advanced live controls | — | — | yes | yes |
| Outbound events (Streamer.bot, SAMMI, Mix It Up, OBS WS) | — | — | yes | yes |
| First-party Canvas Packages | yes | yes | yes | yes |
| Asset import into a package (within the storage quota) | — | yes | yes | yes |
| Migration wizard, private imported packages, outbound bridges | — | — | yes | yes |
| Multi-destination bridges, team style libraries, brand kits, package approval | — | — | — | yes |
| Bot — commands, aliases, cooldowns, role permissions | yes | yes | yes | yes |
| Bot — scheduled messages, deterministic moderation controls | — | yes | yes | yes |
| Bot — import wizard, overlay/Companion actions, multilingual aliases | — | — | yes | yes |
| Bot — multi-channel, moderator approval, team command libraries | — | — | — | yes |
| Multiple channels, brands, collaborators, advanced routing | — | — | — | yes |
| Sponsor reports, multi-creator controls | — | — | — | yes |
| Custom domains | — | — | — | add-on, **hidden until the domain service is proven** (verification, TLS issuance and renewal, DNS support load, abuse handling, rollback) |
| API / outbound webhooks | — | — | — | add-on |
| **Never charged for** (§12.6 durable records in full, receipts, one-off exports, account recovery, disconnecting an integration, security controls) | yes | yes | yes | yes |
| **Social Relay** | | | | |
| Profile links, share cards, manual copy/open | yes | yes | yes | yes |
| Connected social/live accounts | — | 1 | 2 | 6 |
| Discord webhook alerts | — | yes | yes | yes |
| YouTube / Twitch / Kick chat tools | — | — | yes | yes |
| Instagram publishing (Professional accounts) | — | — | yes | yes |
| WhatsApp opt-in reminders (approved templates) | — | — | yes | yes |
| Automations per event type | — | 1 | 1 | unlimited |
| Auto-send (vs approve-then-send) | — | — | yes | yes |
| Post scheduling + social calendar | — | — | — | yes |
| Multilingual variants | — | — | — | yes |
| Team approval before a social post | — | — | — | yes |
| Snapchat hand-off composer | — | yes | yes | yes |
| **Ops** | | | | |
| Sponsor manager + exposure log | — | — | — | yes |
| Finance exports — **scheduled push** into Sheets or Tally (a one-off export of the same data is free on every tier, §12.6.3) | — | — | yes | yes |
| Post-stream analytics | basic | yes | yes | yes |
| Priority support | — | — | — | yes |
| White-glove migration — capped pilot (§30.7) | — | — | — | yes |

### 30.4 Companion controls by tier

Companion is available on **every** tier including Free — it is the cockpit that makes a
first stream succeed — but what it can *do* is tiered.

| Control | Free | Pro | Creator | Studio |
|---|---|---|---|---|
| View state, health signals | basic | full | full | full |
| Concurrent control sessions | 1 | 1 | 2 | 4 |
| Pause / resume queue | yes | yes | yes | yes |
| Send test alert | yes | yes | yes | yes |
| Recent tips, payment status | — | yes | yes | yes |
| Mute / cancel TTS | — | yes | yes | yes |
| Approve / reject moderation | — | — | yes | yes |
| OBS control (scenes, sources, record) | — | — | yes | yes |
| Scene presets, goal controls, markers | — | — | yes | yes |
| Clutch Mode | **yes** | yes | yes | yes |
| Prepare Stream / Wrap Stream | — | yes | yes | yes |
| Lobby operator console | — | — | yes | yes |
| Co-stream control room | — | — | yes | yes |
| Multi-operator, producer roles | — | — | — | yes |
| Push notification types | 2 | all | all | all |

**Clutch Mode is on Free, corrected 2026-09-14.** An earlier draft of this table
withheld it below Pro while CMP-17 listed it P0 with no tier caveat. Clutch Mode is a
safety control — one tap that mutes TTS, hides the QR and suppresses loud media while
retaining every financial event. §30.5 says nothing correctness-related or safety-
related moves up a tier, and a Free creator being unable to silence their own stream
would violate that. It is the single panic control, not the granular TTS controls above
it, which stay tiered.

#### 30.4.1 Why the grant is separate even while bundled

Buying an Alerts tier issues a **distinct Companion membership record**, not an implied
permission. That costs nothing today and it is what makes unbundling later a pricing
change rather than a rebuild.

The mechanism already exists: migration `0100` made Companion its own entitlement with
a `source_key → grant` table read **live** on every call, explicitly supporting
`source_key = 'standalone'` for a Companion-only channel. So the required work is to
issue a grant row on subscription — not to design the separation.

The one genuine blocker to actually selling it standalone remains **implicit channel
provisioning** (CMP-12): a Companion-only signup has no channel, and nothing creates
one. Until that exists, standalone is a config flag with no viable signup path.

### 30.5 Rules that keep the matrix honest

- **Nothing correctness-related ever moves up a tier.** §25.1 is immutable.
- **Free must be genuinely usable**, not a demo. A Free creator takes real money, gets
  a real alert, real TTS via browser voice, and a real receipt. **The price is exactly
  two marks — one small logo in a fixed Master Canvas corner and one quiet line on the
  tip page (§30.6) — and nothing else.**
- Every locked row is **visible with its unlocking tier** (§15.3), never hidden.
- A capability moved down a tier takes effect immediately; **moved up, it grandfathers
  existing users** rather than breaking them — matching the existing moderator-seat
  behaviour.
- Any change to this matrix that affects a published marketing claim requires the
  marketing snapshot to rebuild (§20.4) before it is announced.

### 30.6 Branding and attribution — one watermark, one place

**Decided 2026-09-14. The tier distinction is exactly this and nothing more:**

| Tier | Branding |
|---|---|
| **Free** | One small BharatStudio logo in a fixed corner of the stream overlay, plus one quiet attribution line on the tip page |
| **Any paid tier** | **Zero BharatStudio marketing attribution anywhere.** No logo, no watermark, no "powered by", no end-card, no spoken mention, no QR badge, no tip-page attribution, no promotional line in any email. The one carve-out is legal and transactional issuer identity — §30.6.4, defined narrowly |

#### 30.6.1 How the overlay watermark behaves

- **Rendered once per Master Canvas**, in a fixed safe corner. **Not** repeated on every
  alert, widget, ticker, sound or module — one mark, one place.
- **Visible only while the Free tier is active.**
- **Never spoken by TTS, and never interrupts or delays an alert.**
- **A protected top-layer element**: rendered after every module, above all widgets,
  images, GIFs, themes, alerts and creator-uploaded assets. It is not a configurable
  widget and there is no switch that disables it.
- **The corner is a reserved safe zone.** The Canvas editor refuses module placement
  over it — the constraint lives in the editor, so a creator cannot accidentally cover
  it and cannot deliberately cover it from inside our product.
- **Outside the module error boundaries**, so a crashing module cannot take the
  attribution down with it (§19.5).
- **On a standalone widget, only when that widget is the channel's only active overlay
  source.** Otherwise Canvas owns the mark and a second copy would just look broken.

#### 30.6.2 What we do not do

We cannot stop a creator adding an image source above our browser source in OBS,
cropping it, or hiding it. OBS is their software on their machine, and trying to defeat
that would be brittle, invasive and hostile — a product that spies on a creator's local
scene graph is a product people rightly refuse to install.

So the position is stated plainly and honestly:

- **Technically prevent hiding inside our Canvas.** That part is ours and we enforce it.
- **Never attempt detection of external OBS layers, scene inspection, or any
  covering-check telemetry.** Not now, not as a "compliance feature" later.
- **State it in the Free terms**: attribution must remain visible while BharatStudio
  Free overlays are in use. It is a term of the free tier, enforced the way terms are.
- **Paid tiers remove it completely**, which is the actual answer to anyone who does not
  want it.

#### 30.6.3 Lapse behaviour — branding never appears mid-stream

- A paid creator stays **completely unbranded through the entire grace period** (§26.2).
- **Branding is never injected into a live stream** after a payment problem. Not on
  grace, not on pause, not ever. The audience is not told about a billing issue by a
  logo appearing on screen.
- Once **paused**, premium modules stop. Only on the **next clean overlay reload** may
  the Free fallback render the single watermark, and only if native alerts are still
  enabled.
- This is the same rule as LIF-06 and §26.3, stated from the branding side.

#### 30.6.4 Marketing attribution versus legal issuer identity

**Decided 2026-09-14.** "Zero branding" governs **marketing attribution**. It does not
and cannot remove the identity of the party that actually issued a document or sent a
security message — a receipt with no issuer is a weak document, and a security email
that does not say who sent it trains creators to ignore exactly the mail they must not
ignore.

The carve-out is a **closed list**. Nothing is added to it without a decision row.

| Surface | Paid tier | What is permitted |
|---|---|---|
| Overlay, tip page, widgets, alerts, QR, end-cards, TTS | Nothing, ever | — |
| **Payment receipt and refund notice** | Issuer identity | Legal entity name, GSTIN where required, support contact, and the statement of who processed what. No logo lockup, no tagline, no link to our marketing site |
| **Security and account mail** (sign-in, device added, session revoked, password, 2FA) | Sender identity | The sending entity named in the from-line and body so the mail is verifiable. No promotional content of any kind |
| **Privacy notices, terms changes, legal documents** | Full identity | These are our documents; they say so |
| **Billing and subscription mail to the creator** | Full identity | This is our commercial relationship with them, not their audience's |
| **Anything reaching a supporter** | Creator's brand only | A supporter's receipt carries our issuer identity because law and dispute handling require it, and carries **nothing else** of ours |

Two rules keep the carve-out from drifting into marketing:

- **A carve-out surface may state who we are. It may never suggest what else we sell.**
  No product name-drops, no feature mentions, no "create your own tip page" footer.
- **Any addition to the table above is a decision row in §33.1**, not a copy change.

### 30.7 White-glove migration — a defined service, not a promise

**Decided 2026-09-14: a capped Studio pilot.** Creators do not switch because migrating
is frightening, and a human doing it once is the most direct answer we have.

| Term | Value |
|---|---|
| **Scope** | One migration per account, a capped number of hours, booked not open-ended |
| **Supported setups** | A named list — OBS scene collections and the supported exported configurations. Anything else is declined up front, in writing |
| **Turnaround** | A stated working-day target from booking |
| **On failure** | An honest written "could not import" list plus the wizard's own diff. No implication that a failed import affects billing either way |
| **Escalation** | A named owner and a route when a setup is unusual or a creator disputes the result |
| **Instrumentation** | **Every session logs what the migration wizard could not do, feeding INT-08 and INT-09** |

That last row is the point. Without it, white-glove becomes how migrations succeed and we
have masked a failing wizard with labour. It is a pilot precisely so we can read that log
and decide whether the service or the wizard is the real product.

**It is an acquisition benefit, not a retention one.** It fires once, at onboarding, and
gives a creator nothing at their second invoice. It must never be counted as closing
Studio's ongoing value gap.

### 30.8 Reserved capacity, never priority

**Recorded 2026-09-14 so the idea cannot return in the wrong shape.**

- **Additive — may eventually be sold.** Reserved burst capacity, where we provision extra
  headroom so a Studio channel's spike is absorbed without touching anyone else's service.
- **Zero-sum — may never be sold.** Priority processing, where a paid tier goes first. In a
  saturated system that means another tier's *accepted* alert arrives later, which §30.1
  and the launch authority's no-drop rule forbid.

Even the additive form waits for load evidence at the §37.5 target and a demonstrated
no-drop guarantee for **every** tier including Free. And the phrase **"raid-night
guarantee" is not usable** — a guarantee is a measured claim, and it implies priority.

---

## 31. Master task register — nothing deferred

Status key: **U** usable · **X** unreachable · **P** partial · **A** absent · **B** blocked ·
**N** never build.
Priority: **P0** launch-blocking · **P1** launch-shaping · **P2** post-launch · **P3** later ·
**R** research only (§1.9).

### 31.0 What a row must carry before it can be built

The two-column state/priority form below is a **summary index**, not a specification.
No row may be picked up by a build lane until its entry in `active/` carries all ten
fields. A row missing any of them is not ready, and "we will work it out while
building" is how the unreachable-code problem in §2 happened.

| Field | Meaning |
|---|---|
| **Scope phase** | **v1 · P2 · P3 · R · N** per §1.9, with the suffix **·G** when the row is release-gated (build now, release waits on named external evidence). Carried as a **column in the §31 register itself**, not only in the `active/` record, so the build/research boundary is machine-checkable. A row without a phase fails the build |
| **Owner** | One named person, not a team |
| **Tier and gate** | Which tier, which capability-registry row, which of the four switches (§15.1) apply |
| **Personal-data class** | None / operational / personal / payment / sensitive — and the retention rule that follows from it |
| **Provider or legal dependency** | The named external gate, or explicitly "none". A row naming one is **G — release-gated: build now, release waits** (§1.9), unless building it *at all* would require the external party's permission first, in which case it is **R**. *Corrected 2026-09-14 — this field previously said any provider or legal dependency inherits phase R, which would have made the Razorpay path, the store declarations, the tax position and the privacy work research-only and therefore unbuildable.* |
| **Failure behaviour** | What a creator and a supporter see when it fails. Never "it will not fail" |
| **Kill switch** | The registry row that turns it off, and what a creator keeps when it is off |
| **Acceptance test** | The **user path** a person traverses, not a unit test. Per §35.1, a test that seeds its own data proves nothing about reachability. **§37.2 is the full definition of done, and §37.11 says which suites this row's area requires** |
| **Evidence location** | Where the dated evidence lives. Local test output is never evidence |
| **Rollback** | How it is undone after it has been live, including any data written |

### 31.1 Foundation repairs
See §3 for full detail. F01–F22, all **P0** except F16/F19/F20 (P1) and F22 (P0, cheap).

### 31.2 Payments and money

| ID | Item | Phase | State | Pri |
|---|---|:-:|:-:|:-:|
| PAY-01 | Tip order → checkout → webhook → ledger → alert (atomic) | v1 | U | — |
| PAY-02 | HMAC raw-body verification, `x-razorpay-event-id` dedup, case-insensitive | v1·G | U | — |
| PAY-03 | ₹10 floor + per-channel minimum, enforced at API and DB trigger | v1 | U | — |
| PAY-04 | 15-minute intent expiry; Razorpay checkout `timeout: 900` | v1·G | U | — |
| PAY-05 | Idempotency key contract, 16–128 chars `A-Za-z0-9._:-` | v1 | U | — |
| PAY-06 | `alertConsent=false` skips alert/outbox, keeps ledger entry | v1 | U | — |
| PAY-07 | Reconciliation policy: paid→recovery item, expired→expire, mismatch→quarantine | v1 | U | — |
| PAY-08 | Refunds/disputes as append-only compensating evidence | v1·G | U | — |
| PAY-09 | `__channel_default__` reserved binding; exact provider binding wins | v1·G | U | — |
| PAY-10 | Donor-safe status projection (UUID, amount, INR, state, updated) | v1 | U | — |
| PAY-11 | Payments ledger + CSV export (explicitly not a CA tax report) — **untiered and uncapped**, §12.6 | v1·G | U | — |
| PAY-12 | Provider capability snapshots; features gate on capability, not name | v1·G | P | P1 |
| PAY-13 | Razorpay partner OAuth | v1·G | X | P0 |
| PAY-14 | Payment account activation | v1 | X | P0 |
| PAY-15 | Reconciliation sweep + refund sweep actually running | v1 | X | P0 |
| PAY-16 | Manual-review quarantine resolution UI | v1 | X | P0 |
| PAY-17 | Dynamic **Order QR** on the tip page — server side exists, the surface half does not (§8.2.1) | v1 | P | **P0** |
| QR-01 | **Three QR kinds** implemented distinctly: Channel QR (tip-page short link), Order QR (one payment, expiring), Campaign QR (campaign page) | v1 | A | **P0** |
| QR-02 | **The overlay QR is always a Channel QR** — an Order QR on stream would expire mid-scan, bind every viewer to one stranger's order, and break on reload | v1 | A | **P0** |
| QR-03 | A Channel QR never embeds an amount; a Campaign QR may carry a suggested amount as a page parameter the supporter can change; an Order QR carries the exact amount | v1 | A | **P0** |
| QR-04 | Order QR shows remaining validity and offers one explicit regeneration — never a silent refresh mid-scan | v1 | A | P1 |
| QR-05 | Rotating the channel short link invalidates every Channel QR in circulation: confirmation naming that consequence, and audited | v1 | A | P1 |
| QR-06 | Device routing — mobile UPI Intent, desktop Order QR, tablet offers both rather than guessing | v1 | P | **P0** |
| QR-07 | **UPI-intent return path proven on real devices** across Android, iOS and several UPI apps; a supporter who does not return cleanly still lands on a page that tells them the truth (`ENV-05`) | v1 | A | **P0** |
| QR-08 | Preferred-app memory: the **browser half** (server allowlist exists). Stores which app was chosen, never a credential or account identifier, per device | v1 | P | P1 |
| QR-09 | A return from a UPI app is **never** success — only the HMAC-verified webhook confirms (`PAY-02`) | v1 | U | — |
| QR-10 | Honest waiting state with a bounded wait, then a recovery screen carrying the receipt link | v1 | P | **P0** |
| QR-11 | Receipt link works with no login, from any device, at any later time (`VID-04`) | v1 | U | — |
| QR-12 | QR download and copy from the tip-page editor and the §7.3 copy affordances, at print resolution | v1 | A | P1 |
| QR-13 | Per-attempt funnel record: path offered, path taken, app chosen where the OS reports it, return completed, intent-to-webhook time, failure class. **No account identifiers, no VPAs, no banking data** | v1 | A | P1 |
| QR-14 | Payment path functional with JavaScript degraded — a link and a QR always work (§19.9) | v1 | P | **P0** |
| QR-15 | No "mark as paid", no generic QR fallback, no screenshot-based confirmation | v1 | N | — |
| PAY-18 | Preferred UPI app memory (browser half) | v1 | X | P2 |
| PAY-19 | Direct UPI intent `upi://pay?pa&pn&tr&am&cu` | v1 | A | P2 |
| PAY-20 | Payout/settlement status visible to creator | v1 | A | P1 |
| PAY-21 | Payment failure classification surfaced to creator | v1 | A | P2 |
| PAY-22 | Subscriptions: annual = 10 months charged / 12 served | v1 | U | — |
| PAY-23 | Past-due 30-day grace preserves price; rejoin at current pricing | v1 | U | — |
| PAY-24 | Downgrade pauses newest queues, never deletes; `paused_reason` distinguishes cause | v1 | U | — |
| PAY-25 | Referral credit = service-time (30-day reward, 14-day hold, 5/30-day cap, 12 banked, same-subnet fraud signal) | v1 | U | — |
| PAY-26 | Top-up purchase, ledger and balances (§10.2) | v1 | A | P1 |
| PAY-27 | Season Passes (§10.4) | v1 | A | P1 |
| PAY-30 | Paid room-code unlocking | N | N | — |
| PAY-28 | Paytm / Cashfree / PhonePe | v1 | B | — |
| PAY-29 | Recurring memberships | v1 | B | — |

### 31.3 Alerts, queues, overlay

| ID | Item | Phase | State | Pri |
|---|---|:-:|:-:|:-:|
| ALQ-01 | Durable queues, outbox, per-queue deliveries, sequence numbers | v1 | U | — |
| ALQ-02 | SSE with `Last-Event-Id`, cursor replay, explicit ack | v1 | U | — |
| ALQ-03 | Cross-replica fan-out via LISTEN/NOTIFY | v1 | U | — |
| ALQ-04 | Overlay listener needs its own `DATABASE_URL_DIRECT` — pooled LISTEN/NOTIFY is best-effort only, never the correctness path (durable cursor replay is) | v1 | P | P0 |
| ALQ-05 | Queue modes FIFO + priority-with-aging (server); stacked/pills/aggregated (presentation only) | v1 | U | — |
| ALQ-06 | Quiet hours, rate controls (delay-only, never drop) | v1 | U | — |
| ALQ-07 | No-drop guarantee on every tier | v1 | U | — |
| ALQ-08 | Multi-queue bindings, immutable per-delivery source/priority snapshot | v1 | U | — |
| ALQ-09 | `allow_duplicates` consent required per binding for duplicate delivery | v1 | U | — |
| ALQ-10 | Moderation approve/hold/suppress/replay + admin replay/discard, audited | v1 | U | — |
| ALQ-11 | Role-scoped financial reads (owner/admin amounts; operator/moderator content; viewer status) | v1 | U | — |
| ALQ-12 | Overlay token in fragment only; per-overlay hash lookup; revoke/rotate | v1 | U | — |
| ALQ-13 | 9 safe anchors, scale/width, reduced motion | v1 | U | — |
| ALQ-14 | Long-message/multiline contract: truncation, continuation, no clipping | v1 | U | — |
| ALQ-15 | Per-item skip action | v1 | A | P2 |
| ALQ-16 | Reconnect burst coalescing after a long gap | v1 | A | P1 |
| ALQ-17 | Time-bounded replay window (the "72-hour buffer" that never existed) | v1 | A | P2 |
| ALQ-18 | Master Canvas single browser source with modules (§6) | v1 | A | P0 |
| ALQ-19 | Vertical / second-output canvas | v1 | A | P2 |

### 31.4 TTS

| ID | Item | Phase | State | Pri |
|---|---|:-:|:-:|:-:|
| TTS-01 | Sarvam synthesis, 13 locales, SHA-256 content cache, 2MB/60s caps | v1 | U | — |
| TTS-02 | Quota metering, hard stop, quotas 20K/40K/60K by tier | v1·G | U | — |
| TTS-03 | Amount-tiered character ladder; `maxCharLimit` shared with Alert Studio (never two limits) | v1 | U | — |
| TTS-04 | Chime fallback on provider failure; browser voice on tier/quota | v1·G | U | — |
| TTS-05 | 1.5s playback cap, never blocks visual display or acknowledgement | v1 | U | — |
| TTS-06 | **Content safety suite (§12.2)** | v1 | A | **P0** |
| TTS-07 | Quota bar visible from ~70% consumption | v1·G | A | P1 |
| TTS-08 | Upgrade prompt on exhaustion | v1 | A | P1 |
| TTS-09 | Mute / cancel in-flight from dashboard (companion API exists) | v1 | P | P1 |
| TTS-10 | TTS character top-ups | v1 | A | P1 |
| TTS-11 | Voice routing rule set: amount, length, script, supporter, event class (§11.10) | v1 | A | P1 |
| TTS-12 | Unicode-range script detection in the live path — no model, no network call | v1 | A | P1 |
| TTS-13 | Dashboard control with a "what this would have cost last week" preview | v1 | A | P1 |
| TTS-14 | Companion mode display and mid-stream switch, plus timed "premium everything" | v1 | A | P2 |
| TTS-15 | Route and reason recorded per alert and shown in history and the quota view | v1·G | A | P1 |
| TTS-16 | Safety suite runs identically before both routes — never skipped on browser voice | v1 | A | **P0 with TTS-06** |
| TTS-17 | Companion and dashboard notice at the moment of fallback; no grace buffer exists and none may be added (§11.11) | v1 | A | P1 |

### 31.5 Viewer identity, history, trust

| ID | Item | Phase | State | Pri |
|---|---|:-:|:-:|:-:|
| VID-01 | **`payments.viewer_identity_id` writer** | v1 | A | **P0** |
| VID-02 | `creator_supporter_relations` writer | v1 | A | **P0** |
| VID-03 | Receipt minting from the confirmation page | v1 | X | **P0** |
| VID-04 | Opaque receipt token, SHA-256 fingerprint, reflects live refunds | v1 | U | — |
| VID-05 | Anonymous / platform / account identity levels; tipping never requires login | v1 | P | P0 |
| VID-06 | First-claim-wins idempotent platform claiming, contested handled, audited | v1 | X | P1 |
| VID-07 | Badges (8 named, opt-in, non-financial), streaks | v1 | X | P1 |
| VID-08 | Opt-in searchable profiles, viewer profile and search pages | v1 | U | — |
| VID-09 | Dashboard bounded to newest 100 relations, deterministic tie-break | v1 | U | — |
| VID-10 | Sessions capped at newest 100; password reset 30-min single-use, enumeration-safe | v1 | U | — |
| VID-11 | DPDP erased-vs-retained split — **the logic exists in code; no deletion flow ships or is promised** (§33.1, §32). Deactivation is what ships. State is B, not U: a capability nobody may reach is not usable | v1·G | B | — |
| VID-21 | Archival deletion: no hard deletes, identity fields moved aside, returner treated as new. **Engineering preference, not approved policy** — blocked on the privacy/legal gate (§32) | v1·G | B | P1 |
| VID-22 | Irreversible hashing of archived identity (legal-gated) | v1·G | A | P1 |
| VID-12 | DPDP data export | v1·G | A | P1 |
| VID-13 | Reputation: verdict-only (3 keys), score never stored, 180-day window | v1·G | X | P1 |
| VID-14 | Reputation write path (chargeback, velocity, moderation strike producers) | v1 | A | P1 |
| VID-15 | Creator-facing reputation display | v1 | A | P1 |
| VID-16 | Flag / report a supporter | v1 | A | P1 |
| VID-17 | Block a supporter | v1 | A | P1 |
| VID-18 | Anonymous non-platform tip claim path | v1 | A | P1 |
| VID-19 | YouTube identity attribution carried onto payments | P2 | A | P0 |
| VID-20 | YouTube handle-vs-channel-ID trust model and namespaces (§12.3 identity rules) | P2 | A | P1 |

### 31.6 Engagement — interactions, widgets, goals, challenges

| ID | Item | Phase | State | Pri |
|---|---|:-:|:-:|:-:|
| ENG-01 | 8 interaction types (tip, TTS tip, sticker, mega alert, priority question, support vote, community goal, hype mode), tier counts 3/6/8/8 | v1 | P | P0 |
| ENG-02 | 7 widget types, tier counts 1/3/7/7 | v1 | P | P1 |
| ENG-03 | Support goals, progress computed live, clamped ≥0, windows stream/daily/monthly/open | v1 | U | — |
| ENG-04 | Recent tips, top supporters, ticker, mega-tip banner widgets | v1 | U | — |
| ENG-05 | Leaderboard returns rank + coarse tier bucket only, never exact amount, single channel | v1 | U | — |
| ENG-06 | Widgets reuse the overlay fragment-token/SSE path — a second delivery mechanism is a rejected design | v1 | U | — |
| ENG-07 | Paid votes bind one confirmed payment to one option; tally money-derived with refund effect | v1 | P | P1 |
| ENG-08 | Vote options capped at 16, serialized in the creating procedure | v1 | U | — |
| ENG-09 | **Viewer interaction menu** | v1 | A | **P0** |
| ENG-10 | Support-vote creator UI (create options) | v1 | A | P0 |
| ENG-11 | Support-vote viewer UI (cast) | v1 | A | P0 |
| ENG-12 | Mega alert + priority question viewer trigger | v1 | A | P0 |
| ENG-13 | Hype mode start control | v1 | X | P1 |
| ENG-14 | Widget privacy-scope control | v1·G | X | P1 |
| ENG-15 | Widget preview / sample data for all widget types | v1 | P | P2 |
| ENG-16 | External contribution aggregation (Super Chat → goals), INR-only, include/exclude per source, no multipliers. The aggregation mechanism is source-agnostic and usable; the **Super Chat source itself is Phase 4** with the rest of YouTube | P2 | U | — |
| ENG-17 | Contribution-source toggles wired into Challenges panel | v1 | X | P1 |
| ENG-18 | Priority Question "Unanswered" tab + Mark Answered (§10.6) | v1 | A | P1 |
| ENG-19 | Community boss battle | v1 | A | P2 |
| ENG-20 | Team / squad goals | v1 | A | P2 |
| ENG-21 | Milestone queue (prepare thank-you / sponsor reveal / transition) | v1 | A | P1 |
| ENG-22 | Stream streaks (daily/weekly) | v1 | A | P2 |
| ENG-23 | Like goal, member goal, chat goal, watch-time goal | v1 | A | P1 |
| ENG-24 | Prediction widget, no gambling mechanic | v1 | A | P2 |
| CHL-01 | Creator-published challenge, state machine, live progress, OBS widget | v1 | U | — |
| CHL-02 | Locked refund copy: "Refund automatically initiated through the creator's connected payment provider" | v1·G | U | — |
| CHL-03 | Viewer-proposed challenges (plan calls this the better default) | v1 | A | P1 |
| CHL-04 | Completion evidence submission | v1·G | A | P1 |
| CHL-05 | Dispute record | v1 | A | P1 |
| CHL-06 | Public standalone challenge board page | v1 | A | P2 |
| CHL-07 | `!challenge` chat command | v1 | A | P2 |
| CHL-08 | Refundable multi-contributor challenges | v1 | B | — |

### 31.7 Stickers, media, Alert Studio

| ID | Item | Phase | State | Pri |
|---|---|:-:|:-:|:-:|
| MED-01 | Curated catalogue exposing only id/name/category; selection re-validated server-side | v1 | U | — |
| MED-02 | Creator packs, tier quotas 10/25/50 (implementation choice, needs sign-off) | v1·G | U | — |
| MED-03 | Moderation ladder: Pro structural scan, Creator +attestation, Studio `pending_review` | v1 | U | — |
| MED-04 | Staff review gate on `is_platform_admin` | v1 | P | P1 |
| MED-05 | Staff review admin UI | v1 | X | P1 |
| MED-06 | **Viewer sticker / GIF picker on the tip page** | v1 | X | **P0** |
| MED-07 | No route ever accepts viewer-supplied media bytes — catalogue IDs only | v1 | U | — |
| MED-08 | Template import rejects inline script / non-schema content outright | v1 | U | — |
| MED-09 | Template catalogue frontend | v1 | X | P1 |
| MED-10 | 359 of 600 runtime packages missing; individual authoring required, no mass-copy | v1 | A | P1 |
| MED-11 | Raw-HTML template shape forbidden at every tier | v1 | U | — |
| MED-12 | `render_bytes` capped at 2,000,000 | v1 | U | — |
| MED-13 | Asset storage quotas Free none / Pro 100MB / Creator 250MB / Studio 1GB | v1·G | A | P1 |
| MED-14 | Malware scan stage 2 | v1 | A | P1 |
| MED-15 | Custom sound upload — **stays off until the whole §18.3 gate closes** | v1 | A | P2 |
| MED-22 | Quarantine on upload; unscanned bytes never served, failure state is quarantined | v1 | A | P2 |
| MED-23 | Immutable provenance record per asset (uploader, time, IP, client, filename, hash, attestation version, every transition) | v1 | A | P2 |
| MED-24 | Takedown workflow: intake route, response target, one-action CDN disable, counter-notice, retained evidence | v1·G | A | P2 |
| MED-25 | Repeat-infringement policy written before the first complaint, up to upload suspension | v1 | A | P2 |
| MED-26 | Impersonation and voice-imitation prohibition in terms and attestation, same takedown route | v1·G | A | P2 |
| MED-27 | One rehearsed end-to-end takedown drill before the flag opens for anyone | v1 | A | P2 |
| MED-16 | Built-in themes / theme packs | v1 | A | P2 |
| MED-17 | Per-event styling beyond `displayStyle` brackets | v1 | P | P2 |
| MED-18 | Drag/resize/layer tools (numeric config exists) | v1 | P | P2 |
| MED-19 | Media and sound libraries | v1 | A | P2 |
| MED-20 | Curated meme/media queue module | v1 | A | P2 |
| MED-21 | Lottie + custom branding upload, Studio-tier, live gate. **`bytea` storage is legacy** — new writes go to GCS per §19.1; the `bytea` path stays as the rollback route until backfill completes | v1 | U | — |

### 31.8 Companion

| ID | Item | Phase | State | Pri |
|---|---|:-:|:-:|:-:|
| CMP-01 | Control-session lease; Free exactly one active lease | v1 | U | — |
| CMP-02 | Companion state / layout read and patch | v1 | U | — |
| CMP-03 | Layout slots 8/16/32/64 by tier; page sizes 4/8/16 | v1 | U | — |
| CMP-04 | 17-action catalogue, 4 groups, two-layer gate (entitlement AND activation) | v1 | U | — |
| CMP-05 | Server rejects `obs_*` sent directly, bypassing the client picker | v1 | U | — |
| CMP-06 | Device-code pairing | v1 | U | — |
| CMP-07 | **Mobile handler wiring in `App.tsx`** | v1 | X | **P0** |
| CMP-08 | macOS OBS control | v1 | U | — |
| CMP-09 | Windows OBS control | v1 | B | — |
| CMP-10 | Mirror actions (start/stop/screenshot) | v1 | B | — |
| CMP-11 | Stream actions (go live / end) | v1 | B | — |
| CMP-12 | Implicit channel provisioning for Companion-only signup | v1 | A | P1 |
| CMP-36 | Issue a distinct Companion grant row on Alerts subscription (`0100` mechanism) | v1 | A | P1 |
| CMP-37 | Companion available on Free with tier-limited controls (§30.4) | v1 | P | P1 |
| CMP-13 | Stream health panel (all six signals, heartbeat ages) | v1 | P | P0 |
| CMP-14 | Prepare Stream / go-live checklist (§5.1) | v1 | A | P0 |
| CMP-15 | Run full test with per-hop report | v1 | P | P0 |
| CMP-16 | Live Deck top strip + degraded-mode strip (§5.2) | v1 | A | P0 |
| CMP-17 | Panic / Clutch Mode | v1 | A | P0 |
| CMP-18 | Current and next queue item, live | v1 | A | P1 |
| CMP-19 | Per-item replay / skip | v1 | A | P1 |
| CMP-20 | Scene presets | v1 | A | P1 |
| CMP-21 | Goal controls from Companion | v1 | A | P1 |
| CMP-22 | Quick note / stream markers | v1 | A | P1 |
| CMP-23 | Recent tips, payment status, refund status in Companion (API exists, no web caller) | v1 | P | P1 |
| CMP-24 | Six monetisation push notification types | v1 | A | P1 |
| CMP-25 | Per-notification-type preferences (3 coarse toggles today) | v1 | P | P1 |
| CMP-26 | Session/device list with revoke | v1 | U | — |
| CMP-27 | Offline queue-of-intent | v1 | A | P2 |
| CMP-28 | Helper diagnostics (port, OBS version, ws auth state) | v1 | A | P2 |
| CMP-29 | Disabled-slot explanations naming the failing layer | v1 | P | P1 |
| CMP-30 | Wrap Stream post-stream workflow (§5.5) | v1 | A | P1 |
| CMP-31 | Companion rename before any standalone store listing | v1·G | A | P1 |
| CMP-32 | Notification payloads never carry tip/donor/payment content | v1 | U | — |
| CMP-33 | Mobile secure storage `WHEN_UNLOCKED_THIS_DEVICE_ONLY`, no plaintext fallback | v1 | U | — |
| CMP-34 | Push tokens stored as fingerprint + ciphertext, raw never returned | v1·G | U | — |
| CMP-35 | Desktop READMEs claim no pairing endpoint exists — stale since `0082`; update them | v1 | A | P2 |

#### 31.8.1 Shipping the app (§5.6) — absent from version 1.0 of this register

| ID | Item | Phase | State | Pri |
|---|---|:-:|:-:|:-:|
| CMP-38 | **No purchase surface of any kind in either build** — no price, no upgrade CTA, no iOS link-out; enforced by a CI string/route check, not by review | v1 | A | **P0** |
| CMP-39 | Localisation framework: zero hardcoded user-visible strings (CI-enforced), ICU MessageFormat, no fragment concatenation | v1 | A | **P0** |
| CMP-40 | Hindi as a complete UI language at launch, native-speaker reviewed against a fixed product glossary | v1 | A | **P0** |
| CMP-41 | `Intl` for every number, currency, date and duration — Indian 2,2,3 rupee grouping | v1 | A | **P0** |
| CMP-42 | Locale as device default with in-app override, persisted and sent on every API call | v1 | A | P1 |
| CMP-43 | Server-side localisation of API errors, health text and push bodies from request/device locale | v1 | A | P1 |
| CMP-44 | Pseudo-locale CI build and +40% text-expansion layout tests | v1 | A | P1 |
| CMP-45 | Bundled Indic fonts with conjunct/matra rendering verified on both platforms | v1 | A | P1 |
| CMP-46 | Wave-two languages behind registry rows: Marathi, Bengali, Telugu, Tamil, Kannada | v1 | A | P2 |
| CMP-47 | Wave-three languages: Gujarati, Malayalam, Punjabi, Odia, Assamese | v1 | A | P3 |
| CMP-48 | RTL/Urdu — separate layout track, not a translation task | v1 | A | P3 |
| CMP-49 | APNs + FCM token lifecycle: register, rotate, restore, revoke on sign-out, prune on feedback | v1·G | A | **P0** |
| CMP-50 | Two priority classes only (live health failure, payment/delivery failure); everything else normal priority | v1 | A | P1 |
| CMP-51 | Android notification channels per type | v1 | A | P1 |
| CMP-52 | Contextual permission prompt (never at launch); denied-permission is a supported state with a settings deep link | v1 | A | P1 |
| CMP-53 | Foreground reconciliation — no correctness depends on a push arriving | v1 | A | **P0** |
| CMP-54 | Quiet hours with high-priority override | v1 | A | P2 |
| CMP-55 | **Sign in with Apple** alongside Google Sign-In, with account linking and private-relay addresses handled | v1·G | A | **P0** |
| CMP-56 | Optional biometric app lock | v1 | A | P1 |
| CMP-57 | Session-expiry re-auth sheet returning to the same screen; distinct messaging from control-lease expiry | v1 | A | P1 |
| CMP-58 | "Hide sensitive values" toggle honoured app-wide | v1 | A | P1 |
| CMP-59 | Sign-out clears token, cache, push registration, biometric enrolment and revokes the lease server-side | v1 | A | P1 |
| CMP-60 | Five-tab IA (Live / Prepare / Queue / Money / More) with the degraded strip persistent across all tabs | v1 | A | **P0** |
| CMP-61 | Deep links resolve to a stateful screen, cold start included | v1 | A | P1 |
| CMP-62 | Universal Links + App Links with association files hosted and verified on `bharatstudio.in` | v1 | A | P1 |
| CMP-63 | First-run flow: sign in → pair → guided Prepare Stream → contextual permissions → first test alert | v1 | A | **P0** |
| CMP-64 | Every empty state authored (no stream, no tips, no queue, no devices, notifications denied, offline, paused) | v1 | A | P1 |
| CMP-94 | **Recent Actions on the Live Deck** — session-scoped list of the last actions taken by anyone on this channel, one-tap undo where reversible (§7.5) | v1 | A | P1 |
| CMP-95 | Object detail on tap follows the §7.2 contract — queue item, tip, supporter, health signal | v1 | A | P1 |
| CMP-96 | "Why didn't this fire?" from the Companion queue, same per-hop diagnosis as DSH-17 | v1 | A | P2 |
| CMP-65 | Enforce iOS 15.1 / Android API 26 floors at install | v1 | A | P1 |
| CMP-66 | Landscape usable; degraded strip and panic control never hidden | v1 | A | P1 |
| CMP-67 | Tablet = scaled phone layout with max content width | v1 | A | P2 |
| CMP-68 | Dynamic Type / font scaling to largest sizes with no truncation or sub-minimum targets | v1 | A | P1 |
| CMP-69 | Screen-reader labels on every control in the selected language | v1 | A | P1 |
| CMP-70 | Colour never the only health signal; reduced-motion honoured | v1 | A | P1 |
| CMP-71 | Dark default, complete light mode, full safe-area handling | v1 | A | P1 |
| CMP-72 | Release channels: internal → TestFlight/Play internal → staged rollout with crash-rate halt | v1 | A | **P0** |
| CMP-73 | App-version + build-number scheme recorded against commit and API contract version | v1 | A | P1 |
| CMP-74 | API back-compatibility for old builds; breaking an old build is a dated, deliberate act | v1 | A | **P0** |
| CMP-75 | Server-driven forced-upgrade floor (security/protocol only) plus dismissible soft prompt, never mid-stream | v1 | A | P1 |
| CMP-76 | OTA JS-bundle policy: signed, versioned, staged, rollback-able; never features, monetisation or reviewed behaviour | v1 | A | P1 |
| CMP-77 | Per-release rollback plan; local-state migrations additive or reversible | v1 | A | P1 |
| CMP-78 | **Reconcile in-app account deletion (store requirement) with the blocked deletion policy — before submission** | v1·G | B | **P0** |
| CMP-79 | Permission purpose strings, specific, in every shipped language | v1 | A | **P0** |
| CMP-80 | Data-safety / privacy-nutrition declarations matching the published policy exactly | v1·G | A | **P0** |
| CMP-81 | UGC obligations documented for review: report, block, moderate | v1 | A | P1 |
| CMP-82 | Reviewer demo account with seeded data reaching a live-looking Live Deck | v1 | A | **P0** |
| CMP-83 | Age rating and content descriptors set from moderation reality | v1 | A | P1 |
| CMP-84 | Offline as a first-class state showing last-known values with their age | v1 | A | P1 |
| CMP-85 | Offline queue reconciliation per action; irreversible and financial actions refused offline, never queued | v1 | A | P1 |
| CMP-86 | Exponential reconnect with jitter, always reconciling rather than assuming continuity | v1 | A | P1 |
| CMP-87 | Battery and metered-data discipline over a three-hour stream | v1 | A | P2 |
| CMP-88 | Crash reporting with release tagging, CI symbol upload, crash-free-sessions gate; payloads scrubbed of money, identity and message content | v1 | A | **P0** |
| CMP-89 | Privacy-respecting product analytics with working opt-out | v1·G | A | P1 |
| CMP-90 | §19.4 budgets measured per release on the reference mid-range Android | v1 | A | P1 |
| CMP-91 | End-to-end tests both platforms: sign in, pair, prepare, test alert, Clutch, queue action, offline reconcile | v1 | A | **P0** |
| CMP-92 | CI builds both platforms every merge, producing installable artifacts | v1 | A | **P0** |
| CMP-93 | Store release checklist: localised screenshots and descriptions, demo account, declarations | v1·G | A | P1 |

### 31.9 Connectors and chat

| ID | Item | Phase | State | Pri |
|---|---|:-:|:-:|:-:|
| CON-01 | YouTube OAuth token storage, refresh, encryption | P2·G | U | — |
| CON-02 | **Connect / disconnect UI** | P2 | X | **P0** |
| CON-03 | **Revoked-auth detection + creator prompt** | P2 | A | **P0** |
| CON-04 | Live status discovery, `streamList` polling, 3-failure fallback with reset | P2 | U | — |
| CON-05 | Quota budget, fair share, day-exhaust on 403 | P2·G | U | — |
| CON-06 | Super Chat / Super Sticker / member / milestone / gifted normalisation | P2 | U | — |
| CON-07 | `!tip`, `!tip 100`, `!tip 100 message` → opaque short link | P2 | U | — |
| CON-22 | Bare `!tip` replies with the short link and no amount; viewer chooses on the page | P2 | A | P1 |
| CON-08 | Bot chat acknowledgement (flag default off) | P2 | B | — |
| CON-09 | Connector entitlement counts 0/1/2/3 | P2 | U | — |
| CON-10 | Connector count / limit shown in UI | P2 | A | P1 |
| CON-11 | Ingest-failure admin surface UI | P2 | X | P1 |
| CON-12 | Financial truth never derived from a platform event — webhook only | P2 | U | — |
| CON-13 | Member reconciliation via `members.list` (never chat as truth) | P2 | A | P1 |
| CON-14 | Like goals via `videos.list` (cadence measured, not assumed) | P2 | A | P1 |
| CON-15 | Controlled broadcast lifecycle: create/bind → verify ingest `active` → testing → live | P2 | A | P1 |
| CON-16 | Assisted gifting as reminder/deep link only | P2 | A | P2 |
| CON-17 | Chat display and filtering — tierable. **Retention is not** (§12.6.2): what we ingest and index is a uniform product decision, identical on every tier | P2 | A | P1 |
| CON-18 | Twitch EventSub | P2 | B | — |
| CON-19 | Kick | P2 | B | — |
| CON-20 | Optional YouTube `/live` support page | P2 | A | P3 |
| CON-21 | YouTube identity/trust model and namespaces (§12.3 identity rules) | P2 | A | P1 |
| CON-31 | **One fetch, many surfaces** — no surface calls YouTube; the server polls once per channel and fans out over the channel-keyed SSE (§4.2) | P2 | A | **P0 rule for Phase 4** |
| CON-32 | IFrame Player API for overlay and dashboard presence and playback — client-side, official, zero quota | P2·G | A | P2 |
| CON-33 | Official YouTube live-chat **embed** for the creator to read chat in the dashboard and Companion — zero quota, display only, never a data source | P2·G | A | P2 |
| CON-34 | Stream health from the desktop helper / OBS WebSocket, never from a YouTube call | P2 | A | P1 |
| CON-35 | Cadence as a budget: poll only while live, back off when idle, tier by creator size, defined degradation (slow → pause, always with a visible reason) | P2 | A | P1 |
| CON-36 | **Per-call, per-endpoint, per-channel quota instrumentation**, exported as a histogram (RT-06). Ships with the connector — the quota application is worthless without it | P2·G | A | **P0 for Phase 4** |
| CON-37 | Measure `streamList` against a real Google project: units per hour, per channel, per message volume, and behaviour during a chat burst | P2·G | A | **P0 for Phase 4** |
| CON-38 | Derive the supported concurrent-creator ceiling at the free allowance and at each increase tier, then file the quota application with measured numbers | P2·G | A | P2 |
| CON-40 | **Subscription registry with reference counting** — a datum is polled only while refcount > 0; reuses the RT-02 channel-keyed subscriber map rather than a second registry | P2 | A | **P0 for Phase 4** |
| CON-41 | Visibility-driven subscribe and unsubscribe: hidden module, inactive scene, background tab, backgrounded Companion | P2 | A | P1 |
| CON-42 | Unsubscribe hysteresis (~60s grace) so scene flicking does not thrash subscriptions | P2 | A | P1 |
| CON-43 | **Cross-channel batching** — one global poller, chunked IDs, one call per chunk instead of one per channel | P2 | A | **P0 for Phase 4** |
| CON-44 | Field batching — request the parts needed together in one call, never two calls for one screen | P2 | A | P1 |
| CON-45 | Tip page: live player and chat are click-to-load embeds; a live badge subscribes only while the page has a visitor and drops after idle | P2 | A | P1 |
| CON-46 | Chat ingestion subscribed **by feature in use**, never by liveness; a tips-and-overlay creator opens no chat connection | P2 | A | **P0 for Phase 4** |
| CON-47 | Budget manager: per-datum priority, global degradation rather than per-creator starvation, visible slowdown, negative caching for offline channels | P2 | A | **P0 for Phase 4** |
| CON-48 | Cold subscriber gets last-known value with its age immediately; a render never waits on an upstream call | P2 | A | P1 |
| CON-49 | Anti-pattern enforcement (§4.4.6) — no client calls, no per-surface fetch, no offline polling, no fixed global timer, no per-visitor subscription | P2 | A | P1 |
| CON-39 | Page scraping and InnerTube — **never build.** ToS-prohibited automated access, no contract, no stability, unverifiable financial provenance, and it moves the consequence onto the creator's channel (§4) | N | N | — |

### 31.10 Entitlements, billing, admin, ops

| ID | Item | Phase | State | Pri |
|---|---|:-:|:-:|:-:|
| ENT-01 | Eight entitlement dimensions, closed set, all enforced | v1 | U | — |
| ENT-02 | Moderator seats 0/0/2/5, new grants only, existing grandfathered | v1 | U | — |
| ENT-03 | Moderator seat management UI | v1 | X | P1 |
| ENT-04 | Internal ceilings: pending visuals 20/50/150/500 (500 pending §12.7 verification) · bindings 3/5/10/**50** · presets 1/2/4/**20** · read-only sessions 2/3/5/8 (held pending load evidence) · control sessions 1/1/2/4. *Updated 2026-09-14 to match §30.2.* | v1·G | P | P1 |
| ENT-05 | Grandfathering 12 months + 30-day renewal grace | v1 | U | — |
| ENT-06 | Referral engine with fraud signal | v1 | U | — |
| ENT-07 | Billing panel, upgrade/downgrade/reactivate/payment-method | v1 | U | — |
| ENT-08 | Top-up entitlement additivity, ledger, spend caps | v1 | A | P1 |
| ENT-09 | AI credit ledger, classes, reservations (§11.7) | v1 | A | P1 |
| ADM-01 | Admin console separate from creator dashboard, consumes platform-admin API only | v1 | U | — |
| ADM-02 | DLQ inspection, controlled replay/discard, audited, reason required | v1 | U | — |
| ADM-03 | Entitlement + channel-capacity management | v1 | U | — |
| ADM-04 | DB-backed billing plan catalogue with append-only history | v1 | P | P2 |
| ADM-05 | Reconciliation quarantine review UI | v1 | X | P0 |
| ADM-06 | Featured-creator curation writer | v1 | X | P1 |
| ADM-07 | Admin OIDC + MFA, durable admin registry (vs allowlist) | v1 | A | P0 |
| ADM-08 | Redaction by default; destructive ops need confirmation + reason + audit ref | v1 | U | — |
| ADM-09 | Admin console responsive at 320px/iPad/desktop, keyboard nav | v1 | U | — |
| OPS-01 | Six schedules defined with owner, OIDC, retry/DLQ, idempotency, monitoring, rollback | v1 | U | — |
| OPS-02 | **Schedules actually enabled** | v1 | X | **P0** |
| OPS-03 | Idempotency key `schedule:<id>:<window>`; receipt ≠ business completion | v1 | U | — |
| OPS-04 | Archive schedules stay disabled pending legal approval | v1·G | B | — |
| OPS-05 | Email outbox with Resend; invoice, subscription, DPDP export, overlay-expiry mails | v1·G | U | — |
| OPS-06 | Runbooks per critical alert | v1 | U | — |
| OPS-07 | On-call rotation | v1 | A | P0 |
| OPS-08 | Activation instrumentation (payout + OBS + first alert) | v1 | A | P0 |
| OPS-09 | Reliability metrics: captured-without-LiveEvent, duplicate LiveEvent, lost delivery, replay success, webhook lag, refund failures, TTS failures | v1 | P | P0 |
| OPS-10 | Creator activation funnel and viewer funnel instrumentation | v1 | A | P0 |
| OPS-11 | Revenue KPIs: tips/viewer-hour, average tip, repeat-supporter rate, TTS-driven tips, threshold uplift, goal-driven tips, `!tip` conversion, challenge and vote revenue | v1 | A | P0 |
| OPS-12 | Trace-ID discipline (§12.4) | v1 | U | — |
| OPS-13 | Metrics require service identity; no IDs in labels or paths | v1 | U | — |
| OPS-14 | Deployment manifest is `not-deployable` until placeholders resolved | v1 | B | — |
| OPS-15 | Static build publishes checked-in `_headers` CSP/framing/referrer/permissions | v1 | U | — |

**OPS-11 deserves emphasis.** These are the numbers that decide whether the business
works, they must be instrumented from the first cohort, and they **cannot be
reconstructed later**. Shipping without them means never knowing whether BharatStudio
raised a creator's income.

### 31.11 Marketing, legal, support

| ID | Item | Phase | State | Pri |
|---|---|:-:|:-:|:-:|
| MKT-01 | Product-per-page IA (/alerts, /mirror, /stream) with 301s | v1 | U | — |
| MKT-02 | Commission calculator with provider fees shown on both sides | v1·G | U | — |
| MKT-03 | No competitor names in rendered HTML | v1 | U | — |
| MKT-04 | No Enterprise tier, CTA or contact-sales flow until L10 amended | v1 | U | — |
| MKT-05 | Watermark claim vs reality — the pricing page says tip page + overlay, and only the overlay has one. §30.6 settles it as correct: build the tip-page line rather than weaken the claim | v1 | A | P1 |
| MKT-06 | `/features` frames Alerts and Companion as co-equal; Companion is bundled | v1 | A | P2 |
| MKT-07 | Legal sign-off: pricing/feature claims, DPDP deletion, plaintext reset URL in email | v1·G | B | — |
| MKT-08 | Support surface and staffing | v1 | A | P0 |
| MKT-09 | Public copy matches versioned decisions with dated history | v1 | U | — |

### 31.12 AI

All **A** (absent) except the L23 seam. AI-01 safety rules + moderation queue ·
AI-02 TTS-safe rewrite and PII protection · AI-03 title/description/translation ·
AI-04 post-stream recap and moments · AI-05 Companion live-producer summaries ·
AI-06 credit ledger, tiers, recharge, spend caps · AI-07 thumbnail concept canvas ·
AI-08 Channel DNA style profile · AI-09 editor handoff pack · AI-10 clip
recommendations · AI-11 moderator copilot · AI-12 Clutch Mode intensity detection ·
AI-13 sponsor-safe scanning. Priority P1 for AI-01/02/06, P2 for the rest.
L23 assist (`0121`) is **P** — built and wired, but nav-less and provider-free.

### 31.13 Live Support Hub

| ID | Item | Phase | State | Pri |
|---|---|:-:|:-:|:-:|
| HUB-01 | Mobile support tray, verified payment state, receipts, QR/UPI | v1 | P | P0 |
| HUB-02 | Amount presets | v1 | A | P0 |
| HUB-03 | Five explicit status states (pending → verified → queued → shown → held) | v1 | A | P0 |
| HUB-04 | Safe message preview before checkout | v1 | A | P0 |
| HUB-05 | Approved sticker / sound picker | v1 | X | P0 |
| HUB-06 | Live supporter wall with opt-in names | v1 | A | P1 |
| HUB-07 | Free reactions, rate-limited and sampled | v1 | A | P1 |
| HUB-08 | Community goal ladder with milestone tiers | v1 | P | P1 |
| HUB-09 | Goal source labels. The tips label is v1; **Super Chat and membership labels are Phase 4** and must not render a source that cannot yet exist | P2 | A | P1 |
| HUB-10 | Pick-a-side vote with published rules and close time | v1 | A | P1 |
| HUB-11 | Stream mission card | v1 | A | P1 |
| HUB-12 | Live "what changed" feed | v1 | A | P2 |
| HUB-13 | Embedded YouTube player (IFrame Player API — no data scopes, no quota, §4.2). **Phased P2 conservatively**: the launch authority excludes YouTube capabilities and §34 says no YouTube surface before Phase 4; whether a no-API embed is inside that exclusion is open (§33.2) | P2 | A | P2 |
| HUB-14 | Free lane: one free vote, check-in streak, challenge proposal, cheer card | v1 | A | P1 |
| HUB-15 | "Where does my support go?" creator explainer | v1 | A | P1 |
| HUB-16 | Payment-retry recovery screen | v1 | A | P1 |
| HUB-17 | Low-bandwidth / no-player mode | v1 | A | P1 |
| HUB-18 | Indian language support | v1 | P | P1 |
| HUB-19 | Accessibility: reduced motion, no autoplay sound, SR labels | v1 | P | P0 |
| HUB-20 | Shareable mini-card, campaign links, referral attribution | v1 | A | P2 |
| HUB-21 | Event-specific layout presets | v1 | A | P2 |
| HUB-22 | Post-stream supporter recap and receipt export | v1 | A | P2 |
| HUB-23 | Milestone unlocks framed as a creator promise, never a contract | v1 | A | P1 |

### 31.13.1 Dashboard screens and affordances (§7)

*The register had no dashboard section before 2026-09-14, which is why §7's guaranteed
surfaces had no rows.*

| ID | Item | Phase | State | Pri |
|---|---|:-:|:-:|:-:|
| DSH-10 | **Screen inventory built as named screens** (§7.1), not jobs | v1 | A | **P0** |
| DSH-11 | **Detail-view contract** (§7.2): Summary · Timeline · Relations · Actions · Audit, in that order, for every noun | v1 | A | **P0** |
| DSH-12 | **Activity Log** (§7.5): one chronological view over every audited action, filterable by actor, type, range and object | v1 | A | **P0** |
| DSH-13 | Platform-staff actions affecting this channel visible to the creator in the Activity Log | v1 | A | P1 |
| DSH-14 | Activity Log role-scoping by projection and RLS — operational entries without financial amounts | v1 | A | **P0** |
| DSH-15 | Activity Log free and uncapped at every tier (§12.6); only team filtering, saved views and scheduled export are tierable | v1 | A | **P0** |
| DSH-16 | **"Why this number?"** explain panel on every derived figure, showing the computation and its rows | v1 | A | P1 |
| DSH-17 | **"Why didn't this fire?"** per-hop alert diagnosis naming the failing hop, never "unknown" | v1 | A | **P0** |
| DSH-18 | Trace ID and timeline on every payment and alert row | v1 | A | P1 |
| DSH-19 | Copy affordances: tip link, short link, overlay URL, QR image, receipt link | v1 | A | P1 |
| DSH-20 | Send a test alert from any screen | v1 | A | P1 |
| DSH-21 | **Show me on stream** — brief real-overlay preview with auto-revert | v1 | A | P2 |
| DSH-22 | Undo toast with a real window on every reversible action | v1 | A | P1 |
| DSH-23 | Export-this-view as a background job, never by rendering rows (§12.7) | v1 | A | P1 |
| DSH-24 | Pin any card to Home | v1 | A | P2 |
| DSH-25 | **Supporter profile** (§7.4): history, streak, badges, shown/hidden messages, consent state, private notes, mute-TTS, block stickers, block, report | v1 | A | **P0** |
| DSH-26 | Supporter amounts follow §12.3 — no public lifetime total; visibility consent governs anything on stream | v1 | A | **P0** |
| DSH-27 | **Command palette and global search** across supporters, payments, receipts, assets, modules and actions | v1 | A | P1 |
| DSH-28 | **Support handoff bundle** — redacted diagnostics, no amounts, identities or message content (§12.4) | v1 | A | P1 |
| DSH-29 | Asset detail shows **where each asset is used** | v1 | A | P2 |
| DSH-30 | Empty, loading, error and denied states authored for every screen (§7.7) | v1 | A | **P0** |
| DSH-31 | Denied states name the unlocking tier or the missing role — never a dead control, never a silent hide (§15.3) | v1 | A | **P0** |

### 31.13.2 Safety pipeline (§12.2, §11.12)

| ID | Item | Phase | State | Pri |
|---|---|:-:|:-:|:-:|
| SAF-01 | **One corpus, one pipeline, every surface** — tips, TTS, chat, display names, sticker captions, lobby names, bot replies, and Super Chat when it lands in Phase 4 | v1 | A | **P0** |
| SAF-02 | L0 normalisation: NFKC, zero-width and RTL-override stripping, combining-mark flood, homoglyph folding, leet and separator folding, repeated-character collapse | v1 | A | **P0** |
| SAF-03 | Script detection and **phonetic keys per Indic script**, so a slur in Devanagari, Latin transliteration or code-mixed text is one term | v1 | A | **P0** |
| SAF-04 | Original text never destroyed — normalisation produces a parallel matching form | v1 | A | **P0** |
| SAF-05 | L1 Aho–Corasick over the compiled corpus, global plus per-creator, whole-word and substring rules kept separate | v1 | A | **P0** |
| SAF-06 | L2 bounded edit distance plus phonetic match for obfuscation | v1 | A | P1 |
| SAF-07 | L3 local classifier on our own compute for threats, harassment, scam patterns, raid coordination | v1 | A | P1 |
| SAF-08 | L4 AI on the **residual band only** | v1 | A | P1 |
| SAF-09 | **Per-surface decisions** — payment, display, TTS, stored record, moderator review are independent and separately audited | v1 | A | **P0** |
| SAF-10 | URL neutralisation with per-creator allow and deny domains | v1 | A | **P0** |
| SAF-11 | SSML-injection guard — a message can never become synthesis instructions | v1 | A | **P0** |
| SAF-12 | PII detection: phone, UPI ID, email, address, card-like strings, plus the no-accidental-doxxing rule | v1 | A | **P0** |
| SAF-13 | Rate, flood, repeated-text and emoji-flood controls; slow, raid and high-toxicity modes | v1 | A | P1 |
| SAF-14 | Policy presets: family-friendly, gaming, mature audience, sponsor-safe | v1 | A | P1 |
| SAF-15 | **Fails closed for speech, open for money** — safety unavailable means TTS is silent; payment and receipt are never blocked | v1 | A | **P0** |
| SAF-16 | Degraded state visible to the creator, never to the audience | v1 | A | P1 |
| SAF-17 | **Untiered** (§30.1) — no pack, tier or add-on may sell better safety | v1 | A | **P0** |
| SAF-18 | Audit per action: original, normalised, deciding layer, matched rule or score, confidence, **policy version**, human actor — surfaced in the Activity Log | v1 | A | **P0** |
| SAF-19 | Supporter-visible appeal path for a block; reversals audited | v1 | A | P1 |
| SAF-20 | **Verdict cache** keyed `HMAC(secret, normalised ‖ language ‖ policy_version)`, storing verdicts and never text | v1 | A | P1 |
| SAF-21 | PII-flagged messages are **never cached** | v1 | A | **P0** |
| SAF-22 | Cross-channel cache with creator-specific rules applied **after** the lookup | v1 | A | P1 |
| SAF-23 | **Term-level caching** — an AI verdict on a novel term is promoted into the L1 corpus after review, so it costs nothing again | v1 | A | P1 |
| SAF-24 | Residual batching within a short window; signal-based escalation (new author, length, mixed script, link, amount) | v1 | A | P2 |
| SAF-25 | Spoken messages get the full ladder; scrolling chat may stop at L3 absent signal — every surface still runs L0–L3 | v1 | A | P2 |
| SAF-26 | Periodic distillation of L3 from accumulated L4 verdicts | v1 | A | P3 |
| SAF-27 | Negative caching of common benign phrases | v1 | A | P2 |
| SAF-28 | Compiled per-channel matcher rebuilt on change, held in memory | v1 | A | P1 |
| SAF-29 | Per-channel and global AI budgets that stop escalation, **never L0–L3** | v1 | A | P1 |
| SAF-31 | **Seed corpus**: English + Hindi/Hinglish, 300–800 reviewed terms each, tiered T1/T2/T3. Public lists are candidates only, never shipped unreviewed | v1 | A | **P0** |
| SAF-32 | Per-term record: surface · language · script · phonetic key · severity · whole-word or substring · source · added-by · reviewed-by · date · policy version | v1 | A | **P0** |
| SAF-33 | **Allowlist of legitimate words containing a banned substring** — the Scunthorpe fix | v1 | A | **P0** |
| SAF-34 | Named native-speaker owner per language, who streams | v1 | A | P1 |
| SAF-35 | Wave-two corpora matching the §5.6.2 language waves | v1 | A | P2 |
| SAF-36 | **Growth flywheel**: offline classification → candidate → native-speaker review → corpus entry → new policy version | v1 | A | P1 |
| SAF-37 | **Near-miss telemetry** — unmatched text within edit-distance 1–2 of a banned term logged as a candidate | v1 | A | P1 |
| SAF-38 | Corpus changes versioned, audited, reversible; additions name their reviewer, removals name their reason | v1 | A | P1 |
| SAF-39 | **AI is not in the live path for chat** — deterministic online, AI offline and batched; an exhausted budget degrades discovery, never protection | v1 | A | **P0** |
| SAF-40 | Unicode TR39 confusables mapping, vowel-elision keys, skeleton form, Double Metaphone for Latin and a syllable key for Indic | v1 | A | **P0** |
| SAF-41 | **Evidence snapshot at action time**: original, normalised, rule, layer, confidence, policy version, actor, ±N surrounding messages | v1 | A | **P0** |
| SAF-42 | Raw unactioned chat on the shortest retention class; action records and their snapshots on the long one | v1 | A | **P0** |
| SAF-43 | Appeal record stored with the action, including outcome and reviewer | v1 | A | P1 |
| SAF-44 | Creator-scoped flag and block lists | v1 | A | P1 |
| SAF-45 | **No global shared blacklist, ever** (§16.3) | v1 | N | — |
| SAF-46 | Cross-creator risk **signal** only: decaying, unattributed, never auto-actioning, OAuth identity only, never payment identity | v1·G | A | P2 |
| REP-01 | Supporter reputation **derived, never stored as a score** (§19.6) | v1 | A | P1 |
| REP-02 | Inputs: payments minus refunds · tenure · consistency · actioned events · appeal outcomes | v1 | A | P1 |
| REP-03 | Negative signals private to that creator; positive signals subject to visibility consent; never a public lifetime total | v1 | A | **P0** |
| REP-04 | Consumers: auto-approve trusted supporters · TTS eligibility hints · queue priority · lobby attendance priority · voice-routing named supporter | v1 | A | P2 |
| REP-05 | Decays, appealable, never cross-creator negative, never permanent, **never purchasable** | v1 | A | **P0** |
| REF-01 | Reconcile provider-initiated refunds from the webhook, idempotent on the provider event ID — **ships first, needs no new permission** | v1 | P | **P0** |
| REF-02 | **In-product refund initiation via partner OAuth with a refund scope** on the linked account | v1·G | A | P1 |
| REF-03 | Never hold creator API keys to refund as them (§25.5) | v1 | N | — |
| REF-04 | Full refund record per §10.10.2 — our id and idempotency key, provider ids, amount, status transitions, speeds requested and processed, reason code and text, initiator, origin, event ids, ARN, timing, failure code, balance context, links to alert, receipt and supporter | v1 | A | **P0** |
| REF-05 | State machine: requested → accepted → processing → processed, with rejected, failed and bank-reversed branches; webhook-driven, never time-inferred | v1 | A | **P0** |
| REF-06 | Cumulative partial-refund tracking; never exceed the payment | v1 | A | **P0** |
| REF-07 | Derived numbers recompute with no special handling — the §19.6 payoff | v1 | U | — |
| REF-08 | Receipt reflects live refund state (`VID-04`) | v1 | U | — |
| REF-09 | Refund appears in the Activity Log and the payment detail timeline | v1 | A | P1 |
| REF-10 | **No on-stream change** — the alert and the TTS that already played are not rewritten | v1 | A | **P0** |
| REF-11 | Refund of a Compatibility-Routing signal is impossible and **fails loudly** (§25.3) | v1 | A | P1 |
| REF-12 | Refund ordered behind its payment; never applied to an unrecorded payment | v1 | A | **P0** |
| REF-13 | **Chargebacks and disputes are a separate state machine**, provider-driven, with an evidence pack | v1·G | A | P1 |
| REF-14 | Repeated-refund risk signal, private to that creator, never automatic, never cross-creator | v1 | A | P2 |
| REF-15 | Owner and admin may refund; operator and moderator never | v1 | A | **P0** |
| REF-16 | Reason required, undo window before submission rather than a confirmation dialog | v1 | A | P1 |
| REF-17 | Supporter sees status and expected credit window from the receipt link, with no login | v1 | A | P1 |
| REF-18 | **No refund copy states a tax consequence** until the CA review closes | v1·G | A | **P0** |
| REF-19 | Insufficient-balance and post-settlement refunds surfaced as an explained state, not a generic failure | v1·G | A | P1 |
| REF-20 | Every provider field and behaviour in §10.10 carries a dated source per §27.2 before it is built against | v1·G | A | **P0** |
| SAF-30 | Metrics as histograms: cache hit rate overall and per language, residual rate, **cost per thousand messages**, terms promoted per week, creator-reported false negatives, L3-vs-L4 agreement | v1 | A | P1 |

### 31.14 Customisation and gating

| ID | Item | Phase | State | Pri |
|---|---|:-:|:-:|:-:|
| CUS-01 | Four-switch model (entitled / enabled / configured / active) applied universally | v1 | P | P0 |
| CUS-02 | Per-widget full config surface (§15.2) | v1 | A | P0 |
| CUS-03 | Locked capabilities shown with the unlocking tier, never hidden or dead | v1 | P | P1 |
| CUS-04 | Downgrade preserves configuration; over-limit items read-only | v1 | P | P1 |
| CUS-05 | Preset bundles that are fully editable afterwards | v1 | A | P2 |
| CUS-06 | Per-source alert styling. UPI-tip styling is v1; a **Super Chat style is Phase 4**, since there is no such source in v1 | P2 | A | P1 |

### 31.15 Lobby Engine

| ID | Item | Phase | State | Pri |
|---|---|:-:|:-:|:-:|
| LOB-01 | Session create: game, region, mode, platform, time, seats, reserves, policy | P3 | A | P1 |
| LOB-02 | Public waitlist; code never on stream | P3 | A | P1 |
| LOB-03 | Ready check | P3 | A | P1 |
| LOB-04 | Single-use, short-lived private seat token | P3 | A | P1 |
| LOB-05 | Code revealed only after readiness confirmed | P3 | A | P1 |
| LOB-06 | No-show expiry and automatic reserve promotion | P3 | A | P1 |
| LOB-07 | Six eligibility modes, policy locked and displayed before joining | P3 | A | P1 |
| LOB-08 | Redacted audit log incl. moderator override reason | P3 | A | P1 |
| LOB-09 | Aggregate-only public overlay module | P3 | A | P1 |
| LOB-10 | Companion operator console | P3 | A | P1 |
| LOB-11 | Automatic deletion of temporary lobby data | P3 | A | P1 |
| LOB-12 | Time-bound suspensions with appeal; never keyed on payment identity | P3 | A | P1 |
| LOB-13 | Session templates | P3 | A | P2 |
| LOB-14 | Language / region / platform / accessibility filters | P3 | A | P2 |
| LOB-15 | Voluntary skill bands, friend-group locking | P3 | A | P2 |
| LOB-16 | Creator squads with attributed operator actions | P3 | A | P2 |
| LOB-17 | Lobby reputation, no public shaming | P3 | A | P2 |
| LOB-18 | Post-match pulse with private reporting | P3 | A | P2 |
| LOB-19 | Clip consent before featuring a player | P3 | A | P1 |
| LOB-20 | Cross-creator combined queues | P3 | A | P3 |
| LOB-21 | Recurring community nights with reminders | P3 | A | P2 |
| LOB-22 | Screened Guest Queue (audio-only, time-boxed) | P3 | A | P3 |
| LOB-23 | Paid roulette, wagering, prize pools, paid WebRTC, viewer uploads | N | N | — |

### 31.16 Giveaways and tournaments

| ID | Item | Phase | State | Pri |
|---|---|:-:|:-:|:-:|
| GIV-01 | Creator-defined prize, entry method, window, draw method, published up front | P3 | A | P1 |
| GIV-02 | Free entry route always available; no paid-only entry | P3 | A | P1 |
| GIV-03 | Deterministic seeded draw, seed and entrant count recorded | P3 | A | P1 |
| GIV-04 | Override possible but logged and labelled | P3 | A | P1 |
| GIV-05 | Terms: creator is promoter, responsible for eligibility, tax and delivery | P3·G | A | P1 |
| GIV-06 | Overlay: entry count, timer, consented winner, no address on stream | P3 | A | P1 |
| GIV-07 | Legal review before any chance-based format ships in India | P3·G | A | P1 |
| TRN-01 | Single-elimination brackets up to 8 (Creator) | P3 | A | P2 |
| TRN-01b | Double elimination, round robin, points, seeding, sponsor slots (Studio) | P3 | A | P2 |
| TRN-02 | Seeding by attendance, creator pick, or published-seed random | P3 | A | P2 |
| TRN-03 | Check-in windows, scheduling, reminders | P3 | A | P2 |
| TRN-04 | Score reporting with dispute note | P3 | A | P2 |
| TRN-05 | Standings overlay module | P3 | A | P2 |
| TRN-06 | Sponsor slot with exposure log | P3 | A | P2 |

### 31.17 Custom audio and creator media

| ID | Item | Phase | State | Pri |
|---|---|:-:|:-:|:-:|
| AUD-01 | Custom alert sounds, tier-gated | v1 | A | P1 |
| AUD-02 | Widget / module / milestone sounds | v1 | A | P1 |
| AUD-03 | Supporter-triggerable soundboard, cooldown and queue | v1 | A | P1 |
| AUD-04 | Per-bracket and per-source sound selection | v1 | A | P1 |
| AUD-05 | BRB / countdown music bed | v1 | A | P2 |
| AUD-06 | Rights attestation checkbox with recorded timestamp | v1 | A | P1 |
| AUD-07 | Terms text placing copyright liability on the creator | v1·G | A | P1 |
| AUD-08 | Upload audit record, immediate disable, takedown handling | v1 | A | P1 |
| AUD-09 | Duration, size and format caps; scan pipeline applied | v1 | A | P1 |
| AUD-10 | Asset storage quota enforcement (MED-13 dependency) | v1·G | A | P1 |
| AUD-11 | Shared or discoverable music library | N | N | — |

### 31.18 Performance

#### 31.18.0 Runtime remediation (§19.0) — corrections to shipped code, ahead of Phase 1

| ID | Item | Phase | State | Pri |
|---|---|:-:|:-:|:-:|
| RT-01 | Delete the 2s idle replay poll; an idle overlay issues **zero** queries; jittered polling only as a post-disconnect fallback | v1 | U | **P0** |
| RT-02 | Channel-keyed fanout: only the affected channel's sessions wake; per-channel deduplicated replay; explicit per-instance subscriber and admission limits. **P, not U**: fanout and deduplicated replay are done and locally verified; the admission **ceiling values** ship unset because no authority states one, and they wait on ENV-08 | v1 | P | **P0** |
| RT-03 | Checks, then synthesis, then **one** release: picture and voice go out together. Hold capped at one attempt by the existing provider timeout; retry only unambiguous failures, **never a timeout** (ambiguous — may already be billed); terminal failure releases without audio; overlay orders its display queue by alert creation time. *Supersedes the 2026-09-14 two-phase release* (owner decision 2026-09-16) | v1 | U | **P0** |
| RT-04 | Webhook does one atomic commit then 2xx; post-commit wakeup is fire-and-forget; an independently scheduled **leased outbox dispatcher** owns enqueueing and recovery | v1 | U | **P0** |
| RT-05 | Only the dispatcher scans ready deliveries; request handlers never scan a backlog | v1 | U | **P0** |
| RT-06 | Histogram metrics with explicit buckets, aggregated across instances, on every budgeted path — a budget without a histogram is not a budget. **P, not U**: histograms, bucket-derived p95/p99 and the durable reconciliation snapshot exist; cross-instance aggregation is proven only as the additive property, and the L09 reconciler still has no schedule | v1 | P | **P0** |
| RT-07 | Real evidence: Chromium-in-OBS harness · low-end Android · 3G profile · staged test at **2,000 concurrent overlays** · **8-hour OBS soak** with flat memory and node count | v1·G | A | **P0** |
| RT-08 | Enable the cron schedules the dispatcher depends on (`bharatstudio-crons` ships every schedule `"enabled": false`). **P, not U**: `outbox-recovery` — the only schedule the dispatcher depends on — is enabled; the reconciliation and maintenance schedules stay disabled under their own rows. Enabling a flag in the repository is **not** deploying it | v1 | P | **P0** |
| RT-09 | No "lag-free / fast / smooth / one source replaces twelve" claim publishable until RT-01..RT-07 close — enforced through the marketing snapshot (§20.4) | v1 | A | **P0** |
| RT-10 | Backpressure: payment traffic has enforced priority over widget, dashboard and analytics reads. **P, not U**: the mechanism and its fail-safe classification are built and tested, and hold *by construction* (only GETs are ever classified, so no write can be shed); the pool and admission **values ship unset** because no authority states one — they wait on ENV-08 | v1 | P | **P0** |
| RT-11 | Query timeouts on every read path; a pathological query fails fast rather than holding a connection. **P, not U**: the mechanism is built, excludes every durable-path statement by construction, and rejects at startup any configured timeout below §19.4's 200ms read budget; the **value ships unset** pending ENV-08 | v1 | P | P1 |
| RT-12 | `EXPLAIN ANALYZE` proof checked in for every widget-backing query, re-checked when the query changes — wired into `verify:local`. The plans are **plan-shape change detectors captured on an unsized local database**, never evidence a §19.4 budget is met at production scale; each artefact says so in its own body. **Downgraded U→P on 2026-09-16**: the checker is artefact-driven, so it proves existing plans are current but is structurally blind to a widget-backing query that never got one — PRF-02 added two and it still reported 10/10 green | v1 | P | **P0** |
| RT-13 | Per-channel live-transport cap counted across Canvas and standalone widgets; over-cap widgets degrade to slow snapshot polling with a visible notice (§21.3) | v1 | A | P1 |

#### 31.18.1 Overlay and read-path performance

| ID | Item | Phase | State | Pri |
|---|---|:-:|:-:|:-:|
| PRF-01 | CI-enforced budgets (§19.4) — **cannot pass until RT-06 exists**; averages cannot falsify a p99 | v1 | A | P0 |
| PRF-02 | Master Canvas as the runtime: single connection, single rAF loop, modules as pure renderers. **Absent — so "one source replaces twelve" is unmarketable until it lands** | v1 | A | P0 |
| PRF-03 | Composite-only animation; no layout-triggering properties | v1 | P | P0 |
| PRF-04 | Bounded DOM with recycling; flat node count over 8 hours | v1 | A | P0 |
| PRF-05 | Idle modules fully unsubscribed | v1 | A | P0 |
| PRF-06 | Server-side sampling and rate limiting for reactions and chat | v1 | A | P0 |
| PRF-07 | Burst coalescing on long-gap replay | v1 | A | P1 |
| PRF-08 | Read-through cache for derived aggregates, invalidated by event, never a stored counter | v1·G | A | P0 |
| PRF-09 | `DATABASE_URL_DIRECT` for the overlay listener | v1 | P | P0 |
| PRF-10 | Universal cursor pagination with bounded pages | v1 | P | P1 |
| PRF-11 | Index coverage for every widget-backing query | v1 | P | P0 |
| PRF-12 | Asset budgets: Lottie complexity, audio length, server-side image pre-scaling | v1 | A | P1 |
| PRF-13 | No third-party scripts in the overlay | v1 | U | — |
| PRF-14 | Per-module error boundaries; twice-failed module stays down with a note | v1 | A | P1 |
| PRF-15 | Companion: optimistic UI, virtualised lists, no re-render storms | v1 | P | P1 |
| PRF-16 | Published one-source-vs-many benchmark, re-run in CI | v1 | A | P1 |
| PRF-17 | Bounded-data rule (§12.7) enforced per surface: dashboard summary-first and virtualised, tip page first-paint-only, overlay bounded queue, widgets server-aggregated and capped | v1 | A | **P0** |
| PRF-18 | Exports run as background jobs, never by rendering rows into a page | v1 | A | P1 |
| PRF-19 | Field projections and strict payload caps on every endpoint — no `select *` behind a live surface | v1 | A | P1 |
| WMK-01 | Watermark as a protected top layer rendered after every module, outside the module system and its error boundaries | v1 | A | **P0** |
| WMK-02 | Reserved safe-zone corner the Canvas editor refuses to place modules over | v1 | A | **P0** |
| WMK-03 | Watermark on a standalone widget only when it is the channel's only active overlay source | v1 | A | P1 |
| WMK-04 | Tip-page attribution line on Free only (MKT-05) | v1 | A | P1 |
| WMK-05 | Zero **marketing attribution** on every paid tier, everywhere — overlay, tip page, end-cards, QR, TTS, and every promotional line in mail. The **narrow legal and transactional issuer-identity carve-out in §30.6.4** is the one exception and is not branding. *Corrected 2026-09-14 — this row previously said zero branding on receipts and emails, contradicting §30.6.4.* | v1·G | A | **P0** |
| WMK-06 | Branding never injected mid-stream on lapse; Free fallback mark appears only on the next clean overlay reload after pause | v1 | A | **P0** |
| WMK-07 | No external-layer detection, scene inspection or covering-check telemetry — ever | N | N | — |

### 31.19 Control plane and admin

| ID | Item | Phase | State | Pri |
|---|---|:-:|:-:|:-:|
| CTL-01 | Capability registry table with versioned, audited rows | v1 | A | **P0** |
| CTL-02 | Resolution order engine (kill → denylist → rollout → tier → override) | v1 | A | **P0** |
| CTL-03 | Per-channel resolved blob, versioned and cached; never per-capability queries | v1 | A | P0 |
| CTL-04 | Admin UI: master switch, retier, edit limits, kill | v1 | A | P0 |
| CTL-05 | Impact preview ("affects 214 channels, 3 live") | v1 | A | P1 |
| CTL-06 | Staged effective-time changes | v1 | A | P1 |
| CTL-07 | Two-staff approval on every change; **owner sign-off for paid→Free moves**; single-admin `global_kill` for incidents | v1 | A | P1 |
| CTL-08 | One-action revert to previous version | v1 | A | P1 |
| ENV-01 | Cloud Run at the production configuration in a non-production project — same concurrency cap, instance settings, one region | v1 | A | **P0** |
| ENV-02 | Database seeded to §37.4 size (500 channels · 2M payments · 5M alert events · 200k identities) with production index definitions | v1 | A | **P0** |
| ENV-03 | Razorpay sandbox wired end to end in that environment | v1·G | A | **P0** |
| ENV-04 | OBS harness: pinned OBS on a mid-range Windows machine, plus headless Chromium for CI trend-tracking | v1 | A | **P0** |
| ENV-05 | Device lab: one named mid-range Android and one iPhone at the supported floors | v1 | A | **P0** |
| ENV-06 | Network shaping for the 4G and 3G profiles in §37.4 | v1 | A | P1 |
| ENV-07 | Pass/fail artefact pipeline emitting the §37.4 JSON document per run | v1 | A | **P0** |
| ENV-08 | Exit: one full §37.5 target-concurrency run completes and emits a valid artefact, before any Phase 0.5 row claims an exit number | v1 | A | **P0** |
| ENV-09 | **Owner for the environment lane — Sukhdev Singh** | v1 | A | **P0** |
| CTL-09 | Layer 1 correctness dimensions rejected from this panel | v1 | A | P0 |
| CTL-14 | **Registry rejects any capability whose subject is a durable creator record (§12.6)** — no row may be created that gates storing, viewing, searching, fetching or exporting one. Enforced in the registry, not by review | v1 | A | **P0** |
| CTL-15 | Retention is a single platform-wide value, not a per-tier limit; the schema offers no per-tier retention field to set | v1 | A | **P0** |
| CTL-10 | `GET /v1/public/capability-matrix` published snapshot | v1 | A | P0 |
| CTL-11 | Marketing build reads the snapshot; webhook revalidation | v1 | A | P0 |
| CTL-12 | Marketing sections behind flags (`kind = marketing_section`) | v1 | A | P1 |
| CTL-13 | Admin MFA + durable admin registry (ADM-07 dependency) | v1 | A | P0 |

### 31.20 New widgets

| ID | Item | Phase | State | Pri |
|---|---|:-:|:-:|:-:|
| WID-01 | Companion tap source (+1 win / +1 loss) | v1 | A | P1 |
| WID-02 | Lobby/tournament auto-fill of results | v1 | A | P2 |
| WID-03 | Wins This Season, Session Record, Win Streak | v1 | A | P1 |
| WID-04 | Personal Best, Rank Progress, Season Objective | v1 | A | P2 |
| WID-05 | Head-to-Head, Scoreboard | v1 | A | P2 |
| WID-06 | Match Countdown, Tournament Standings, Squad Roster | v1 | A | P2 |
| WID-07 | Hours Streamed, Milestone Ticker, Top Clip, Recap Card | v1 | A | P2 |

### 31.21 Co-Stream Room

| ID | Item | Phase | State | Pri |
|---|---|:-:|:-:|:-:|
| COS-01 | Room create, explicit mutual accept, short-lived grants | P3 | A | P1 |
| COS-02 | Public `/live/collab/<id>` page with two IFrame players | P3 | A | P1 |
| COS-03 | Eight layout modes | P3 | A | P1 |
| COS-04 | Switch Window with published range, countdown, override | P3 | A | P2 |
| COS-05 | One audio source at a time, viewer-switchable | P3 | A | P1 |
| COS-06 | Shared event rail, timer, scorecard | P3 | A | P1 |
| COS-07 | Side-assigned supporter alerts | P3 | A | P1 |
| COS-08 | Chat tabs per creator | P3 | A | P2 |
| COS-09 | Companion control room incl. one-tap safe layout | P3 | A | P1 |
| COS-10 | OBS collaboration overlay scene export | P3 | A | P2 |
| COS-11 | Contribution selector (A / B / shared goal) | P3 | A | P1 |
| COS-12 | Instant revoke; page degrades to single or ended state | P3 | A | P1 |
| COS-13 | Explicit "feeds are not frame-synced" UI treatment | P3 | A | P1 |
| COS-14 | Clip handoff consent | P3 | A | P2 |
| COS-15 | Silent payment splitting | N | N | — |

### 31.22 Sound Moments and Rules Engine

| ID | Item | Phase | State | Pri |
|---|---|:-:|:-:|:-:|
| SND-01 | Moment = sound + animation + sticker + TTS style + effect, creator-curated | v1 | A | P1 |
| SND-02 | Amount-tiered moment catalogue | v1 | A | P1 |
| SND-03 | Loudness normalisation and duration caps | v1 | A | P1 |
| SND-04 | Per-sound, per-viewer, stream-wide cooldowns | v1 | A | P1 |
| SND-05 | Themed packs incl. Indic and festival | v1 | A | P2 |
| SND-06 | Companion mute / skip / pause / emergency safe mode | v1 | P | P1 |
| SND-07 | No remote URL execution in the overlay | v1 | A | P0 |
| RUL-01 | Rules engine: thresholds, modes, cooldowns, caps, priority, approval | v1 | A | P1 |
| RUL-02 | Never-interrupt-gameplay mode | v1 | A | P1 |
| RUL-03 | Overlay-offline hold-and-replay | v1 | P | P1 |
| GOA-01 | **Completion latch** — `goal_completed` written once, idempotently, with the closing contribution and the derived total. Actions fire from the event, never from a recomputed boolean | v1 | A | **P0** |
| GOA-02 | A refund never un-completes a goal; it is recorded against it and the progress display shows the true derived figure | v1 | A | **P0** |
| GOA-03 | Manual reopen is explicit, audited and reason-required — never an automatic consequence of arithmetic | v1 | A | P1 |
| GOA-04 | Goal triggers: 100% · percentage and absolute thresholds · first contribution · the closer · biggest single · stretch steps · stalled N minutes · expired unmet · ladder step · all/any goals complete | v1 | A | P1 |
| GOA-05 | Session triggers: session total · Nth supporter · new top supporter · first-time · returning supporter | v1 | A | P2 |
| GOA-06 | Platform triggers — Super Chat, membership, gifting, like and viewer milestones | P2 | A | P2 |
| GOA-07 | Community triggers — challenge, lobby, tournament, giveaway | P3 | A | P3 |
| GOA-08 | Operational triggers — stream start/end, scene change, Clutch enter/leave, sponsor segment | v1 | A | P2 |
| GOA-09 | Per-trigger controls: enabled · threshold · once-per-stream / every time / max N · cooldown · minimum contribution · quiet window · which contribution sources count | v1 | A | P1 |
| GOA-10 | Overlay actions: celebration, confetti, bounded takeover, banner, ticker, progress flourish, module swap, theme swap, closer card, scene preset | v1 | A | P1 |
| GOA-11 | Audio actions: Sound Moment, sting, TTS announcement **through the §12.2 pipeline**, audio duck | v1 | A | P1 |
| GOA-12 | Goal-lifecycle actions: complete · **auto-advance the ladder** · **auto-create next** (`+₹X`, `×N`, template, repeat) · **roll overflow in or discard** · convert to stretch · extend · pause · archive · reset | v1 | A | P1 |
| GOA-13 | Creator actions: Companion push · Live Deck banner · suggested next action · **stream marker** into the Wrap Stream summary | v1 | A | P1 |
| GOA-14 | Supporter actions: thank-you card naming the closer **with visibility consent** · badge grant · receipt note | v1 | A | P2 |
| GOA-15 | Outbound actions, **approve-then-send by default**: YouTube chat announcement, Discord, Telegram, WhatsApp opt-in, social card | P2 | A | P2 |
| GOA-16 | OBS actions via the local helper: scene switch, source toggle, replay-buffer save, approved Streamer.bot or SAMMI action | v1 | A | P2 |
| GOA-17 | Sponsor actions: reveal card, log exposure with timestamp for proof-of-delivery | v1 | A | P3 |
| GOA-18 | **Ordered action sequences with per-step delays**, not a set | v1 | A | P1 |
| GOA-19 | Conditions: only live · named scenes · not in Clutch · not during a sponsor segment · tier · overlay connected · outside quiet hours | v1 | A | P1 |
| GOA-20 | **Interlocks, not creator-configurable**: Clutch suppresses loud and full-screen and defers rather than drops · never interrupt an alert mid-play · never-interrupt-gameplay holds takeovers · all text through §12.2 · our rate limits, not the platform's rejection | v1 | A | **P0** |
| GOA-21 | Prepare-not-fire default for anything outbound or public (§5.4); low-risk local actions may auto-fire | v1 | A | **P0** |
| GOA-22 | Text templates with `{goal_name}` `{target}` `{raised}` `{remaining}` `{percent}` `{closer}` `{top_supporter}` `{supporter_count}` `{session_total}` `{next_goal}`, per language | v1 | A | P1 |
| GOA-23 | Every action configurable to §15.2 depth — sound, animation, duration, easing, safe-zone position, colour, size, or absent | v1 | A | P1 |
| GOA-24 | **Sequence preview** fires the whole composition on the overlay in a marked test mode that auto-reverts | v1 | A | P1 |
| GOA-25 | Presets — Quiet · Standard · Hype — each fully editable afterwards (§15.3) | v1 | A | P2 |
| GOA-26 | Overflow rolled into the next goal or discarded, creator's choice, recorded either way | v1 | A | P1 |
| GOA-27 | Goal detail view follows the §7.2 contract, with a timeline of every contribution and every rule that fired | v1 | A | P1 |
| GOA-28 | **"Why this number?"** explains a goal total from its contributions including refunds (§7.3) | v1 | A | P1 |
| GOA-29 | YouTube goal actions are Phase 4 and narrower than expected: announce, pin, one title update per stream, poll. **Never a purchase or a gift** (§4) | P2 | A | P2 |
| SEC-01 | Short-lived signed overlay capabilities with renewal | v1 | A | **P0** |
| SEC-02 | Session/device binding where practical | v1 | A | P1 |
| SEC-03 | Scheduled rotation; never in screenshots, logs or tickets | v1 | P | P1 |
| MIG-01 | Shadow mode with a migration report (delivered, missed, latency, unsupported) | v1 | A | P1 |
| MIG-02 | Test/sandbox mode that never reaches viewers | v1 | A | P1 |
| MIG-03 | Global emergency-disable button | v1 | A | P0 |

### 31.23 Enterprise

All **B** (blocked) pending §24.5. EN-00 commercial/legal model · EN-01 org, roles,
allocations · EN-02 immutable snapshot schema · EN-03 settlement adapters · EN-04
pre-order snapshot resolver · EN-05 finance-control APIs · EN-06 transfers, refunds,
reconciliation · EN-07 scheduler handlers · EN-08 dashboard views · EN-09 pilot.
Plus SSO, RBAC, shared brand kits, licensed packs, campaigns, cross-channel analytics,
outbound webhooks, finance/audit exports, SLA support.

### 31.24 Payment routing

| ID | Item | Phase | State | Pri |
|---|---|:-:|:-:|:-:|
| RTE-01 | Routing abstraction: a route is a signal source, not a rail | R | A | P1 |
| RTE-02 | Health-state machine (active / degraded / paused / direct available) | R | A | P1 |
| RTE-03 | `routed_signal_received → alert_queued → alert_delivered` state class, distinct from `verified_payment` | R | A | P1 |
| RTE-04 | Capability restrictions in routing mode (§25.3) enforced server-side | R | A | P1 |
| RTE-05 | Per-provider kill switch with confidence threshold | R | A | P1 |
| RTE-06 | Explicit in-product acceptance of the Beta terms on enabling a route | R | A | P1 |
| RTE-07 | Duplicate/false-signal detection disabling auto-alerts | R | A | P1 |
| RTE-08 | Migration prompt when a Direct integration becomes available | R | A | P2 |
| RTE-09 | Paytm Business route — **Gated on §25.6 signal mechanism** | R | B | P2 |
| RTE-10 | Google Pay Business route (assisted activation) — **Gated on §25.6** | R | B | P3 |
| RTE-11 | PhonePe Supervisor route — **Consent-gated on C1–C7** | R | B | P2 |
| RTE-12 | HDFC Cashier route — **Consent-gated on C1–C7** | R | B | P2 |
| RTE-13 | Amazon Pay consumer-credential route | N | N | — |
| RTE-14 | Generic QR fallback / "mark as paid" | N | N | — |
| RTE-15 | Consent flow: explicit, unbundled, revocable, re-confirmed on scope change | R | A | P2 |
| RTE-16 | KMS/HSM envelope encryption for any delegated secret, no human read path | R | A | P2 |
| RTE-17 | Credential-compromise incident procedure, rehearsed | R | A | P2 |

### 31.25 Subscription lifecycle

| ID | Item | Phase | State | Pri |
|---|---|:-:|:-:|:-:|
| LIF-01 | Five-state lifecycle (active / grace 14d / paused / retained 90d / expired) | v1 | A | P1 |
| LIF-02 | Grace-period notices in dashboard and Companion, never on stream | v1 | A | P1 |
| LIF-03 | Paused: connectors stop, configuration read-only, nothing deleted | v1 | A | P1 |
| LIF-04 | Retained 90d applies to **encrypted connector secrets only**; configuration, mappings, templates and durable records persist under the uniform retention policy (§12.6.2) and stay exportable | v1 | A | P1 |
| LIF-05 | Expired: credential revocation and paid-only secret deletion, after repeated notice | v1 | A | P1 |
| LIF-06 | Overlay quiet safe state — no payment wall, no on-stream branding change | v1 | A | **P1** |
| LIF-07 | Never-charged-for list enforced (receipts, exports, recovery, disconnect, security) — and the full §12.6 durable-record set in every lifecycle state including Expired | v1 | A | P1 |
| LIF-08 | Renewal restores configuration without reconnecting, unless the token expired | v1·G | A | P1 |
| LIF-09 | Desktop bridge caches a signed entitlement for 24h | v1 | A | P2 |
| LIF-10 | Free and native behaviour independent of subscription and Platform status | v1 | P | P0 |

### 31.26 Social Relay

| ID | Item | Phase | State | Pri |
|---|---|:-:|:-:|:-:|
| SOC-01 | Event model: 8 relayable event types, approve-then-send default | P3 | A | P2 |
| SOC-02 | Per-destination queue with cooldown; never send-per-event | P3 | A | P2 |
| SOC-03 | Obey returned rate-limit headers (Discord) rather than hard-coded limits | P3 | A | P2 |
| SOC-04 | Health states per destination, mirroring §25.2 | P3 | A | P2 |
| SOC-05 | Discord webhook + rich embeds + bot commands | P3 | A | P2 |
| SOC-06 | YouTube: broadcast metadata, chat announcements, polls, pinned moments | P3 | A | P2 |
| SOC-07 | YouTube post-stream wrap with timestamps | P3 | A | P2 |
| SOC-08 | Instagram: Reels/feed publish, clip-to-Reel draft, comment inbox | P3 | A | P3 |
| SOC-09 | WhatsApp: opt-in, approved templates, 24h window respected, template cost shown | P3 | A | P3 |
| SOC-10 | Twitch EventSub + Channel Point mapping | P3 | A | P3 |
| SOC-11 | Kick OAuth 2.1 connector within granted scopes | P3·G | A | P3 |
| SOC-12 | Snapchat Creative Kit hand-off, creator taps final share | P3 | A | P3 |
| SOC-13 | Telegram bot channel alerts | P3 | A | P3 |
| SOC-14 | Upload-forced-private disclosure until Google audits the project | P3·G | A | P2 |
| SOC-15 | Lapse: manual share kept, auto-send stopped, no message to the audience | P3 | A | P2 |
| SOC-16 | Auto-posting every tip/follower/alert anywhere | N | N | — |
| SOC-17 | YouTube Community posts, IG personal accounts, unsolicited DMs, WhatsApp groups, Snapchat background posting | N | N | — |

### 31.27 Packs and creator-ops

| ID | Item | Phase | State | Pri |
|---|---|:-:|:-:|:-:|
| PCK-01 | Pack as a capability-registry row, additive, lifecycle-aware | P3 | A | P2 |
| PCK-02 | AI Credits pack — ₹49/₹149/₹399, paid tiers only. Ships once the **measured** cost model exists; the ledger half is in `0081` | P3 | A | P1 |
| PCK-03 | Socials Pack — ₹129/mo, Creator+. Target initial set, but cannot precede Social Relay (Phase 7) | P3 | A | P2 |
| PCK-04 | Events Pack — ₹129/mo, Creator+. Hidden until lobby/tournament features exist | P3 | A | P2 |
| PCK-05 | Team Seats pack — ₹129/mo, Creator+. Hidden until seat management ships (F18) | P3 | A | P2 |
| PCK-06 | Storage Pack — ₹49/mo for +500MB of **new-upload** space, Pro+. Never affects historical records. **Nearest to ready**; needs MED-13/AUD-10 enforcement first | P3 | A | P2 |
| PCK-07 | Sponsor Pack — ₹149/mo, Creator+. Hidden until the sponsor manager exists | P3 | A | P2 |
| PCK-08 | Multi-Channel Pack — ₹199/mo per added channel, Creator+. Target initial set, but **last of the four to be ready**: blocked on the tenant-isolation suite (§37.6). The ₹598-vs-₹599 comparison with Studio is deliberate (§28.3.3) | P3 | A | P3 |
| PCK-09 | **Finance Pack** — statement, GST-ready export, TDS notes, payout reconciliation. Hidden until the CA/tax evidence row closes; sells the *prepared statement*, never access to the underlying records | P3·G | A | **P1** |
| PCK-10 | Pack attach-rate reporting to inform future tier composition | P3 | A | P3 |
| PCK-11 | Hidden packs exist as registry rows so they become visible without a release | P3 | A | P2 |
| PCK-12 | No pack, top-up or tier may sell retention, history depth, record search or export — enforced by CTL-14 | P3 | A | **P0** |
| PCK-13 | Pack system launches with whatever is ready — arrival order Storage → AI Credits → Socials → Multi-Channel — not held for a fixed set of four | P3 | A | P2 |
| PCK-14 | A lapsed pack pauses added capacity only; over-quota assets go read-only and stay viewable and exportable | P3·G | A | P2 |
| PCK-15 | Multi-Channel Pack blocked until the §37.6 tenant-isolation suite passes | P3 | A | P3 |
| JOB-01 | Content calendar + public schedule page with notify-me | P3 | A | P2 |
| JOB-02 | Consistency view: streak, hours, rest days framed kindly | P3 | A | P3 |
| JOB-03 | Sponsor deliverable tracker with proof | P3 | A | P2 |
| JOB-04 | Clip request queue | P3 | A | P3 |
| JOB-05 | Clip-to-social pipeline ending in a draft, never auto-post | P3 | A | P3 |
| JOB-06 | Title/thumbnail performance against our own stream records | P3 | A | P3 |
| JOB-07 | Shareable gear/setup profile | P3 | A | P3 |
| JOB-08 | Collab record | P3 | A | P3 |
| JOB-09 | Community FAQ auto-answers in chat | P3 | A | P3 |
| JOB-10 | Editor payouts / staff revenue splitting | N | N | — |
| JOB-11 | Full CRM · scheduled cross-posting to all networks · analytics competing with YouTube Studio | N | N | — |

### 31.28 Interop, packages and bridges (§9)

| ID | Item | Phase | State | Pri |
|---|---|:-:|:-:|:-:|
| INT-01 | **Declarative Canvas Package format** — signed, versioned, runtime-pinned; no JS, no network fetch, no external font or asset URL, no executing CSS, no runtime-reaching expressions | P2 | A | P2 |
| INT-02 | Package validator and signature verification at import and at render | P2·G | A | P2 |
| INT-03 | Allowed-animation set — animations are chosen, never authored as code | P2 | A | P2 |
| INT-04 | First-party curated package library authored by us | P2 | A | P2 |
| INT-05 | Private creator packages, tenant-scoped, never shown to another creator | P2 | A | P2 |
| INT-06 | Asset import (SVG, PNG, WebP, audio, video, Lottie) on the §18.3 gate: attestation, quarantine, scan, provenance, takedown | P2 | A | P2 |
| INT-07 | Transcode, normalise and pre-scale on import; content-addressed tenant-scoped storage (§19.1) | P2 | A | P2 |
| INT-08 | Migration wizard: inventory → map → side-by-side preview and diff → publish on approval → reversible | P2 | A | P2 |
| INT-09 | Unmapped items named explicitly; an uncertain mapping shown as uncertain | P2 | A | P2 |
| INT-10 | Connector outbox per destination: queue, backoff, dead-letter, kill switch, idempotency key, redacted delivery log | P2 | A | P2 |
| INT-11 | A bridge failure never delays, cancels, duplicates or alters a BharatStudio alert | P2 | A | **P0 rule, P2 build** |
| INT-12 | Streamlabs bridge — **selected low-frequency event types only**, rate-limited and coalesced below the documented ~2/min guidance, labelled a transition tool | P2 | A | P3 |
| INT-13 | Streamer.bot local adapter in the Companion helper: `localhost` only, explicit pairing, creator-chosen action allow-list | P2 | A | P3 |
| INT-14 | SAMMI local adapter, same shape | P2 | A | P3 |
| INT-15 | Mix It Up local adapter, same shape | P2 | A | P3 |
| INT-16 | StreamElements configuration migration only | P2 | A | P3 |
| INT-17 | StreamElements event bridge — **gate:** confirmed API/partner position | R | B | — |
| INT-18 | Third-party paid marketplace publishing — **gate:** author payouts, GST on third-party digital goods, content review at scale, takedown and dispute handling, defensible "verified" badge | R | B | — |
| INT-19 | Never embed a third-party browser-source URL, HTML, JS, CSS or iframe in the Canvas — enforced by the package validator, not by review | P2 | A | **P0** |
| INT-20 | Never scrape a competitor dashboard, import a browser-source secret, or execute copied widget code | N | N | — |

### 31.29 Customisation depth by tier (§15.4)

*IDs use the **CST-** prefix. §31.14 already owns **CUS-** for the gating model (four switches, locked-capability display, downgrade preservation); these are a different concern and must not share a namespace.*

| ID | Item | Phase | State | Pri |
|---|---|:-:|:-:|:-:|
| CST-01 | Three-level model (0 presets / 1 safe presentation / 2 advanced / 3 brand and team) as registry rows, retierable without a release | P2 | A | P1 |
| CST-02 | **Protected string class enforced by the customisation system** — payment, legal, consent, security and error text are never exposed for override | P2·G | A | **P0** |
| CST-03 | Overlay level 1: free colour, our fonts, position and anchor, show/hide, z-order, opacity, radius, animation, reduced-motion variant, performance mode | P2 | A | P1 |
| CST-04 | Amount / name / message rendering controls incl. hidden amounts and bracket-name-only | P2 | A | P1 |
| CST-05 | **Indic script fallback order per text role** | P2 | A | P1 |
| CST-06 | Overlay level 2: font per role, per-bracket and per-source styling, burst behaviour, do-not-interrupt windows | P2 | A | P2 |
| CST-07 | Per-scene-profile placement and theming; overlay theme follows the OBS scene | P2 | A | P2 |
| CST-08 | Per-aspect-ratio variants (16:9 / 9:16 / 4:3) of one canvas | P2 | A | P2 |
| CST-09 | **Conditional themes** — festival date ranges, time of day | P2 | A | P2 |
| CST-10 | **Sponsor-safe mode** — swap to a neutral theme for a segment and back | P2 | A | P2 |
| CST-11 | **Adversarial preview** — long Indic name, 500-char message, emoji flood | P2 | A | P1 |
| CST-12 | **Brand kit** — palette, type, logo saved once, applied across every surface | P2 | A | P3 |
| CST-13 | Multi-surface templates and package authoring with team approval | P2 | A | P3 |
| CST-14 | Tip page level 1: cover image, avatar shape, tagline, lane order, labelled amount presets, privacy display | P2·G | A | P1 |
| CST-15 | Tip page level 2: message settings, pack selection, event layouts, campaign and referral pages, multilingual copy sets | P2 | A | P2 |
| CST-16 | Tip page level 3: full theme with background media, multiple campaign pages with own goal, copy, countdown and schedule | P2 | A | P3 |
| CST-17 | Per-page OG image, title and description | P2 | A | P2 |
| CST-18 | Dashboard: theme, accent, density, landing tab, notification and locale preferences | P2 | A | P1 |
| CST-19 | Dashboard: pinned cards, **named saved views**, saved export column sets, shortcut map | P2 | A | P2 |
| CST-20 | Dashboard: logo and brand accent, per-role default views. **No background images at any tier** | P2 | A | P3 |
| CST-21 | Moderator **preferences** — layout, columns, density, quick-action order | P2 | A | P2 |
| CST-22 | Moderator **policies** — blocked terms per language, link allow/deny, auto-hold, escalation, canned responses, handover notes | P2·G | A | P2 |
| CST-23 | Team-managed policy libraries, approval workflows, centrally set moderator layouts | P2 | A | P3 |
| CST-24 | **Permission classes are never customisable** — presets and libraries only inside owner/admin/operator/moderator/viewer | P2 | A | **P0 rule** |
| CST-25 | Companion: top-strip stats, health signals shown, saved deck presets | P2 | A | P2 |
| CST-26 | Companion accessibility at level 0 — one-hand mode, colour-blind palette, haptics, language override | P2 | A | P1 |
| CST-27 | Companion team decks pushed to every operator | P2 | A | P3 |
| CST-28 | Receipts and transactional mail: creator logo, accent, thank-you copy per language, reply-to, brand kit — inside §30.6.4 | P2 | A | P2 |
| CST-29 | No customisation increases what a live surface loads (§12.7); themes are data the renderer already holds | P2 | A | **P0 rule** |
| CST-30 | Every theme passes contrast and +40% text-expansion checks (§37.7) — a failing theme is a defect, not a taste question | P2 | A | P1 |

### 31.30 BharatStudio Bot (§36)

| ID | Item | Phase | State | Pri |
|---|---|:-:|:-:|:-:|
| BOT-01 | Command engine: names, aliases, cooldowns, role permissions | P2 | A | P2 |
| BOT-02 | Scheduled and timed messages | P2 | A | P2 |
| BOT-03 | Six-area UI and no more (Commands, Moderation, Automations, Languages, Connected channels, Import) | P2 | A | P2 |
| BOT-04 | Deterministic multilingual aliases with Unicode and transliteration matching | P2 | A | P2 |
| BOT-05 | Localised replies per channel or per the viewer's command language | P2 | A | P2 |
| BOT-06 | Blocked-term lists by language including transliterated variants — **one corpus shared with §12.2 TTS safety, never a second list** | P2 | A | **P0 with TTS-06** |
| BOT-07 | Deterministic spam, flood, repeated-text, emoji and link controls | P2 | A | P2 |
| BOT-08 | Import wizard for simple commands from creator-supplied exports; honest "cannot import" table | P2 | A | P2 |
| BOT-09 | Never import scripts, raw JS, shell commands, arbitrary HTTP calls or third-party credentials | N | N | — |
| BOT-10 | Automation recipes from a narrow allow-list of actions | P2 | A | P3 |
| BOT-11 | One event action at first release: command → overlay or Companion action | P2 | A | P2 |
| BOT-12 | Rate-limited and coalesced writes; degrade to silence with a visible notice, never a delayed backlog dump | P2 | A | P2 |
| BOT-13 | AI layer on §11 credits: translate, summarise, suggest, classify — **recommend or soft-action only** | P2 | A | P3 |
| BOT-14 | AI audit record: original text, action, reason, confidence, policy version, appeal and reversal path | P2 | A | P3 |
| BOT-15 | Moderation correctness untiered (§30.1); a Free creator's chat is not less safe | P2 | A | P2 |
| BOT-16 | Bot UI languages follow the §5.6.2 waves; no separate language set | P2 | A | P2 |
| BOT-17 | Blocked on the Google chat-write scope (`CON-08`, §32) and on YouTube being post-v1 | P2·G | B | — |

### 31.31 Storage and media platform

| ID | Item | Phase | State | Pri |
|---|---|:-:|:-:|:-:|
| STO-01 | GCS + CDN with content-addressed keys and signed URLs | v1 | A | **P0 for audio** |
| STO-02 | Postgres holds metadata, moderation state and attestation only | v1 | A | P0 |
| STO-03 | Normalisation pipeline (audio loudness, GIF→MP4/WebM, image pre-scale) | v1 | A | P1 |
| STO-04 | Tenant-scoped dedup (`channel_id` + sha256); global dedup only for BharatStudio-owned or explicitly licensed assets (§19.1) | v1 | A | P2 |
| STO-05 | Keep existing Lottie bytea working; new media to GCS; opportunistic backfill | v1 | A | P1 |

---

## 32. Blocked — with the exact unblocking condition

| Item | Unblocked by |
|---|---|
| Recurring memberships | A rail reporting `supportsRecurringPayments: true`. **Interim answer: Season Passes (§10.4)** |
| **In-product** refund initiation, refundable challenges | **Delegated authority, not provider capability.** Razorpay supports refunds; our creator-direct model means the funds sit in the creator's account, so initiation needs partner OAuth with a refund scope on the linked account (`REF-02`), which arrives with the Technology Partner approval. *Corrected 2026-09-14 — this row previously read "no rail supports refunds", which was true of our abstraction and misleading about the provider.* Reconciling a creator-initiated refund (`REF-01`) is **not** blocked and ships first |
| Enterprise workspace | Five written Razorpay Route answers (parent/linked structure, third-party split rights, direct settlement, per-account flexibility, suspended-account behaviour) + counsel/CA advice |
| Paytm | All eight written conditions confirmed |
| Cashfree, PhonePe | Partner confirmation |
| Windows Companion | A Windows build agent; target has never compiled |
| Mirror and Stream Companion actions | Those products emitting a liveness signal (`0093` hard-codes activation false) |
| Bot chat acknowledgement, and **BharatStudio Bot as a whole** (§36) | Google chat-write scope approval, plus YouTube depth landing at all — the bot has no platform without it |
| Third-party paid package marketplace (§9.7) | Author payout flow · GST position for third-party digital goods sold through us · content review at scale with takedown and dispute handling · a "verified" badge we can defend. Four separate positions, none of which exist |
| StreamElements event bridge | A confirmed API position or partner contract. Configuration migration is unaffected and may proceed |
| Template catalogue (359 packages) | Individual authoring + design/native-language review. Mass-copy explicitly forbidden |
| Archive schedules | Approved eligibility, integrity and retention/legal decision |
| Platform KMS/HSM signing | Provisioned KMS/HSM |
| Deployment | Resolved `REQUIRED_*` placeholders, IAM/OIDC, staging recovery, capacity, observability, rollback rehearsal |
| Account deletion policy and any deletion flow or promise | Approved DPDP erasure position reconciling statutory payment-record retention, the archived-identity plaintext-vs-hashed question, and the store requirement for an in-app deletion route (CMP-78) |
| Creator media upload in public product | Every row of the §18.3 gate built and one end-to-end takedown drill rehearsed |
| "Shared goal" money language in Co-Stream | Named beneficiary before checkout and on the receipt, refund policy, tax review, recorded creator agreement, legal review of the wording (§22.5) |
| Delegated payment routes (PhonePe Supervisor, HDFC Cashier, Paytm, Google Pay Business) | Four gates, all open: written provider permission · counsel sign-off · security design review · a provider sandbox route. Phase **R** until then |
| **v1 release** (Alerts + Companion) | Razorpay Technology Partner approval for the **creator-direct** flow · legal sign-off (terms, privacy, DPDP, refunds) · CA/tax conclusion · store declarations · public host, SSL and support mailbox. **Google OAuth verification** belongs here too, because Google Sign-In is v1 authentication — but only the sign-in consent screen, not YouTube data scopes |
| **YouTube capability only, post-v1** | YouTube data scopes · **quota grant** · chat-write scope. *Corrected 2026-09-14: these were previously grouped under "everything production", which would have delayed the Alerts and Companion launch behind Phase 4 work. The external register has always scoped them correctly* |
| **Enterprise only, post-v1** | Razorpay **Route** enquiry — the five written answers in the Enterprise row above. Not a v1 gate |
| Non-production measurement environment | **Not blocked** — see `07_BUILD_BOOTSTRAP_AUTHORITY.md` §3. The "Deployment" row above is about production; a production-shaped staging environment needs none of it, and conflating them is what made the Phase 0.5 exit criteria unreachable |

---

## 33. Decisions taken, and decisions still open

### 33.1 Decided 2026-09-13

| Decision | Outcome |
|---|---|
| **Studio price** | **₹599** GST-inclusive. `active/launch/00_LAUNCH_SCOPE_AUTHORITY.md` wins; ₹499 and ₹799 are superseded everywhere. The margin work behind the 20K/40K/60K TTS ladder assumed ₹599. |
| **Queue-count ladder** | **1 / 2 / 3 / 5.** The conservative reading, matching what is enforced. Raising a limit later is painless; lowering one breaks creators. |
| **Control plane sequencing** | **Phase 0, before feature work.** Seed the registry with the capabilities that exist today rather than retrofitting it onto sixty hard-coded gates. Marketing stops being able to over-claim immediately. |
| **Giveaways** | **Free-entry and skill-based only.** No chance-based format ships until counsel signs off. The creator is always the promoter; we never hold a prize. |
| **Room codes** | **The Lobby Engine governs seats. Paid room-code unlocking is dropped.** One eligibility model, no fairness problem. Creators reward supporters through priority modes, never by selling a seat. |
| **Co-Stream Room tier** | **Creator ₹399.** Squad grid (3–4 creators) stays Studio-only as the premium step. |
| **Companion name** | **Kept.** The Bitfocus Companion collision is accepted as a known store-search and SEO risk rather than paid for with a rename. Revisit only if store search proves it costly. |
| **Template catalogue** | **Still pending** — deliberately left open, not decided by default. |
| **Paid integrations** | Connect, import, bridge, YouTube and compatibility routing are **Creator-tier and above**. Sponsor reports and multi-creator controls are Studio. **Multi-channel is a Studio capability, and the Multi-Channel Pack is the Creator-tier route to buying a single additional channel** — the pack sells scope on a capability Studio includes, which is exactly what §28.1 says a pack is for. Corrected 2026-09-14; an earlier version of this row listed multi-channel as Studio-only while §28.3 sold it from Creator. Receipts, exports, account recovery, disconnecting an integration and security controls are **never** paid. |
| **Lapse behaviour** | Five states: active → grace 14d → paused → retained 90d → expired. The overlay falls back to a quiet safe state; existing OBS URLs never become a payment wall or change branding on stream; nothing is deleted silently. |
| **Delegated-credential routes** | **Proceed on a consent basis**, subject to legal sign-off. PhonePe Supervisor and HDFC Cashier are consent-gated on conditions C1–C7 in §25.5. Consent settles the privacy dimension; it does not settle the provider's own terms, payment regulation, or the security of holding the secret — those are carried knowingly. |
| **Amazon Pay routing** | **Never build. Corrected 2026-09-14.** The earlier "build under C1–C7" row contradicted §25.5, which prohibits it non-negotiably, and it was wrong. The Amazon Pay pattern requires the creator's **consumer account password** — not a delegated sub-user, not a merchant identifier. Consent does not cure holding a consumer credential: it does not bind Amazon, it does not satisfy the provider's own terms, and it converts a breach into an account takeover of the creator's shopping and payment identity. No admin switch, no beta label and no attestation makes it acceptable. The route is removed from the register (RTE-13) rather than left pending. |
| **Route switches** | **Every** payment route, Razorpay Direct included, is an independently switchable capability-registry row. Adding or removing one follows the §25.6.1 notification sequence, and a creator is never billed for a capability we withdrew. |
| **Top-up margin** | **25% is a floor, tuned per credit class**, not a flat rate. |
| **Account deletion** | **BLOCKED on legal, not decided.** The engineering preference is archival, never destructive: no hard deletes, identity fields moved aside, a returning person treated as new. That is a preference, not an approved policy, and it may not be shipped or promised. DPDP erasure duties, statutory retention for payment records, and the plaintext-vs-hashed question for archived identity are all unresolved (§32). Until the privacy/legal row in `05_SUPPORT_AND_EXTERNAL_EVIDENCE_REGISTER.md` is approved: **no account-deletion promise appears in product, terms or marketing**, and no deletion flow ships. What ships in the meantime is deactivation with a plainly worded statement of what is retained and why. |
| **Bare `!tip`** | Replies with the creator's short link and no amount; the viewer picks on the page. |
| **Sound uploads** | Free none · Pro 5 · Creator 25 · Studio 100. Excluding Free keeps copyright and scanning exposure on identifiable, billable accounts. |
| **Control sessions** | Free 1 · Pro 1 · Creator 2 · Studio 4 concurrent, matching the recorded internal ceilings. |
| **Control-plane authority** | Any platform admin proposes; a second approves. **Moving a paid capability into Free needs owner sign-off** — that is a revenue decision, not an ops one. `global_kill` is a single-admin **emergency** action governed by §20.6.1: reason required, 24-hour hard expiry, second-admin ratification within 4 hours, immutable log, mandatory 72-hour post-incident review. It may never be used to make an ordinary change. |
| **Tournaments** | Creator gets single elimination up to 8 players. Studio gets double elimination, round robin, seeding and sponsor slots. |
| **Lobby default** | **Open FIFO queue** for new creators. Member priority and creator pick are deliberate opt-ins, so the product does not read as pay-to-play by default. |
| **Sticker packs** | **Confirmed 10 / 25 / 50.** Already built and shipped in `0119`; changing it would cost a migration and a marketing correction for no evidenced benefit. |
| **Social Relay** | One event becomes an approved, platform-specific action. Approve-then-send is the default; auto-send is Creator+ and opt-in. Never auto-post tips, followers or alerts anywhere. |
| **Packs** | Tiers sell a capability class, packs sell capacity and scope. A pack never grants correctness and is never the only route to a capability. |
| **Queue-count ladder, settled** | **1 / 2 / 3 / 5**, and `00_LAUNCH_SCOPE_AUTHORITY.md` is **amended** to say so. This document does not get to overrule a launch authority; the authority carries the change itself, dated, the way the Studio ₹599 amendment did. Matches what the migration enforces, so no migration, no billing change, no creator impact. |
| **Media storage, settled** | **GCS/CDN, and `01_MASTER_RELEASE_AUTHORITY.md` is amended.** Postgres holds metadata only. Existing `bytea` rows keep serving and stay as the rollback path until backfill completes; new writes go to GCS; backfill never blocks a release. Migration, serving, retention and rollback rules are in §19.1. |
| **Marketing attribution vs issuer identity** | Paid tiers get **zero marketing attribution**. Legal and transactional **issuer identity** is a narrow, closed carve-out (§30.6.4): receipts, refund notices, security and account mail, privacy and terms documents, and billing mail to the creator. A carve-out surface may say who we are and may never suggest what else we sell. Additions to that list are decision rows, not copy changes. |
| **YouTube out of Phase 0** | **F06 and F07 move to Phase 4.** The connect / disconnect / reconnect UI makes a built subsystem reachable, but YouTube is excluded from v1 and building its connect surface in Phase 0 is scope drift against the launch authority. It stays a recorded defect until YouTube work starts. |
| **Phase G vs phase R** | Two states, not one. **G — release-gated**: build now, release waits on external evidence (Razorpay, store declarations, tax, privacy). **R — research only**: no implementation of any kind until a named gate closes (delegated payment routes, marketplace, StreamElements bridge, Enterprise). The earlier "any provider or legal dependency becomes R" rule would have made the Razorpay path itself unbuildable. |
| **Canvas Package signing** | **BharatStudio holds the only signing key.** First-party packages are signed by us; a creator's private package is bound to their account and validated rather than signed. KMS-held key with no human read path, scheduled rotation with key IDs recorded per package, a revocation list checked at import *and* at render, canonical serialisation specified before the first signature, provenance travelling with the package, and a renderer that treats every package as untrusted data regardless of signature. Creator keys and a third-party trust model arrive with the marketplace, which is phase R. |
| **Top-up vs pack** | **One-time consumable is a top-up; recurring capacity or scope is a pack**, and nothing appears in both menus. Top-ups shrink to AI credits and TTS characters. Storage, connectors, seats, sticker and media slots, queue burst capacity, sponsor slots and extra outputs all move to packs. Season Pass issuance leaves both — it is the creator's own product. |
| **Document repair sequencing** | **Fix every contradiction in the single file first; split into six documents second** (§35.5). Splitting a document that still contradicts itself copies the conflicts into six files. The split proceeds once the §35.3 CI checks pass clean. |
| **Studio positioning** | Line becomes **"Brand and scale"**. Copy change; no capability moves. |
| **Customisation by tier** | **§15.4, three levels**: 0 presets (Free) · 1 safe presentation (Pro) · 2 advanced creator control (Creator) · 3 brand and team (Studio), across six surfaces — overlay, tip page, dashboard, moderator view, Companion, receipts. **Customisation depth, not relocated features, is how Studio earns its price**, because it takes nothing from Creator and costs almost nothing to run. Accessibility settings sit at level 0 on purpose. |
| **Protected strings** | A creator may **never** override payment, legal, security, consent or error text. "Every string overridable" was proposed and **rejected** — it is a consumer-protection and DPDP exposure. Enforced by the customisation system, not by review (CST-02). |
| **Dashboard backgrounds** | **Never, at any tier.** Logo and accent only. A background image breaks the §37.7 contrast floor on the surface where people read numbers. |
| **Studio ceilings** | Event bindings 20 → **50**, saved presets 8 → **20** — stored configuration, no bounded-data or connection impact. **Read-only sessions stay 8** pending load evidence. **Pending visuals stay 500**, and whether even that is a client-held figure needs checking against §12.7. |
| **TTS exhaustion** | Ladder held at 20K/40K/60K. **No grace buffer, and none may be added** — it is an ungranted spend with no ledger entry type and it silently redefines the cap. Immediate browser-voice fallback with a Companion and dashboard notice (§11.11, TTS-17). |
| **White-glove migration** | Capped Studio pilot with defined scope, supported setups, turnaround, failure handling and escalation — **instrumented to feed the migration wizard** (§30.7). It is an acquisition benefit that fires once and must never be counted as closing Studio's ongoing gap. |
| **Reserved capacity, never priority** | Additive reserved burst capacity may eventually be sold; **zero-sum priority processing may not**, because it delays another tier's accepted alert (§30.8). Even the additive form waits for load evidence, and **"raid-night guarantee" is not usable language**. |
| **Custom domains** | Add-on **hidden until the domain service is proven** — verification, TLS issuance and renewal, DNS support load, abuse handling, rollback. An unproven service is not sellable as an add-on any more than it is includable in a tier. API and outbound webhooks split into their own add-on so they are not blocked by it. |
| **Studio pack bundling** | **Rejected as proposed.** "Studio includes ₹357 of packs" double-counted: the sponsor manager, exposure log, sponsor reports and multi-creator controls are **already Studio-only** in the matrix, and scheduled finance push is already Creator+. Those packs largely exist to sell Studio-shaped capabilities *to Creator*. Bundling them would also advertise Sponsor and Finance, which are hidden precisely because their features and legal evidence are incomplete. The **₹357 figure may never appear in marketing.** Replaced by the open item in §33.2. |
| **Pack gating** | Each of the eight packs is held for a stated reason, not out of caution (§28.3.0). Sponsor and Finance are held because selling them early produces a **document a creator forwards to a sponsor or a CA** — being wrong there costs the creator, not just us. Events and Socials are held because the feature does not exist and a pack multiplies a real capability. Storage and Team Seats are held because the **enforcement** is missing, and selling a limit we cannot apply means charging for something the creator already had. AI Credits is held because the price has no measured basis. |
| **Pack launch sequencing** | **The pack system launches with whatever is ready, not with a fixed four.** Arrival order **Storage → AI Credits → Socials → Multi-Channel**. Socials cannot precede Social Relay; **Multi-Channel is the largest item on the list disguised as a pack** — tenant separation, cross-channel roles, billing allocation, connector routing and per-channel audit — and it does not ship until the tenant-isolation suite (§37.6) passes. Holding two sellable packs behind that dependency would be a choice with no benefit. |
| **Testing and evidence** | **§37 is binding on every register row.** Done means: use cases, unit and contract tests, a reachability assertion, at least one real-browser or real-device E2E scenario, failure-path coverage, a measured performance number where the row is on a budgeted path, dated artefacts, and rollback proof. Merge gates and release gates are separated (§37.9), and §37.10 lists what is never evidence — including the local SQL harness, JSDOM tests, averages standing in for p99s, and any staging run we performed ourselves where a provider or counsel must speak. |
| **Interop layer** | **Three separate capabilities, never merged** (§9.1): style packages, migration tools, event bridges. The boundary that makes all three safe: **BharatStudio never embeds a third-party browser-source URL, HTML, JavaScript, CSS or iframe in the Master Canvas** — no tier, no attestation and no advanced mode changes that (INT-19). |
| **Canvas Packages** | A **signed, versioned, declarative** format: layout, theme tokens, an allowed animation set, bundled assets, configurable fields. No JS, no network fetch, no external font or asset URL, no executing CSS. This is also the answer to the template-catalogue problem — author a small first-party set well and let asset import cover the long tail. |
| **Asset imports** | Creators bring assets they own from Canva, Figma, LottieFiles, Photoshop or purchased packs. **An imported asset is a creator upload**: same §18.3 gate, same attestation, quarantine, provenance and takedown, tenant-scoped, never shown to another creator. |
| **Streamlabs bridge** | **Build, but never position it as parity.** Their guidance is roughly two alerts per user per minute, so a general tip bridge would silently drop most of a raid and make a creator believe the tips never arrived. It ships as **selected low-frequency events only**, rate-limited and coalesced by us, with the summarising stated in the UI, labelled a transition tool. |
| **Local adapters** | Streamer.bot, SAMMI and Mix It Up live in the Companion desktop **helper** — a mechanism, not a product surface (§14). `localhost` only, never a public port, explicit pairing, creator-chosen action allow-list, never an arbitrary command. |
| **StreamElements** | Configuration migration only. An event bridge is **phase R** until a confirmed API or partner position exists. Never scrape a dashboard, import a browser-source secret, or execute copied widget code. |
| **Package marketplace** | **Slowed deliberately.** First-party curated packages and private creator packages only. Third-party **paid** publishing is phase R: it is a second money flow with author payouts, GST on third-party digital goods, content review at scale, takedowns, disputes, and a "verified" badge we would have to defend. Nothing else in the interop layer depends on it. |
| **BharatStudio Bot** | **An automation product, not another dashboard** (§36). Six areas and no more. First release is six things done well: commands with aliases/cooldowns/roles, scheduled messages, English/Hindi/Hinglish, deterministic spam and link controls, a simple import wizard, and one event action. Multilingual is **deterministic first** — transliteration-matched aliases and per-language blocked terms — with AI as an optional, quota'd layer that **recommends or soft-actions and never bans**. The blocked-term corpus is **one list shared with §12.2 TTS safety**, never a second. Never imports scripts, raw JS, shell commands or third-party credentials. P2 at the earliest, blocked on the Google chat-write scope and on YouTube being post-v1. |
| **Bootstrap exemption** | **Steps −1 and 0 are exempt from the §31.0 ten-field precondition**, narrowly and by name, under `07_BUILD_BOOTSTRAP_AUTHORITY.md` §1 — they are the steps that produce those records, so requiring one first was a deadlock, not a standard. The exemption covers no capability row and sets no precedent, and each exempt step carries its own ten-field record written *as* the step. |
| **The environment is its own lane** | **A non-production measurement environment is not blocked; production deployment is** (bootstrap authority §3). Conflating them made the Phase 0.5 exit criteria unreachable. Step 0.25 provisions Cloud Run at production configuration, a database seeded to §37.4 size, provider sandboxes, the OBS harness, the device lab, network shaping and the pass/fail artefact pipeline — **before** any Phase 0.5 row claims an exit number. Owner: Sukhdev Singh. |
| **Freeze checkpoint** | Before any schema freeze, public copy freeze or store submission, five areas are reviewed against current assumptions with a written go/no-go each: payment boundary · deletion and retention · mobile purchase boundary · tax representation · consent wording. **A freeze without this review is not approved.** This is what makes "file external gates after the build" a managed risk rather than an unbounded one. |
| **External filings sequencing** | **Owner decision 2026-09-14: none of the external gates blocks development, and all are filed after the build works.** Razorpay Technology Partner approval, legal counsel, the CA/tax review and Google OAuth verification are **release gates, not build gates** (§1.9 phase **G**), and the owner has chosen to file them once the decided scope is built and working, accepting that minor changes may follow from their feedback. Two obligations follow and are not optional: (a) **build to best practice as if each review had already happened** — DPDP-shaped data handling, GST-inclusive pricing arithmetic, terms and refund wording drafted to be reviewable rather than rewritten; and (b) **make no claim that depends on a filing that has not happened** — no "Razorpay partner", no tax representation beyond the GST-inclusive arithmetic already published, no verified-OAuth claim. The launch date moves with the filing cycle, not with the code. |
| **Client-side scraping and InnerTube** | **Never build** (CON-39). "Just fetching" is accurate for one request and inaccurate for a scheduled client: the ToS prohibits automated access outside the API, and the API's quota *is* the permitted path. Moving the traffic to the creator's browser and IP does not change what the terms permit — it moves the consequence onto **their** channel, for our product's benefit. The valuable data (chat, Super Chat, members) is not reachable by public fetching at all; it needs InnerTube, which requires impersonating the official client. And what *is* publicly reachable — viewer count, likes — costs 1 unit, so the trade is bad before ethics enter it. **The permitted client-side path is the IFrame Player API and the official chat embed** (CON-32, CON-33), which are free and cover presence, playback and chat *display*. |
| **Demand-driven fetching** | **A YouTube call happens only while a human is looking at something that needs it** (§4.4). Reference-counted subscriptions per `(channel, datum)`, driven by the same RT-02 subscriber map; visibility-based unsubscribe with hysteresis; cross-channel and cross-field batching; tip-page live player and chat behind an explicit click, as zero-quota embeds; chat ingestion subscribed **by feature in use**, never by liveness; and a budget manager that degrades globally and visibly rather than starving one creator. A creator with no YouTube-derived widget costs zero quota all day. Traffic never multiplies quota — only distinct channels and datums do. |
| **Surface data sources** | **One fetch, many surfaces** (§4.2, CON-31): no surface ever calls YouTube; the server fetches once per channel and fans out over the channel-keyed SSE. Twelve widgets cost what one costs. Stream health comes from the local helper and never touches Google. Chat *display* is the official embed at zero quota; chat *ingestion* is the only genuinely expensive item and is Phase 4, gated on the quota grant. |
| **YouTube quota** | **Quota is per Google Cloud project, not per creator** (§4.1). A creator's OAuth grant conveys permission, never allowance; every connected creator spends our 10,000-unit default day. A quota increase is required before YouTube ships at any scale, per-call unit costs need dated sources, and polling cadence is a quota budget with a defined degradation path. Filed in Phase 4 with measured usage, per the sequencing decision above. |
| **Runtime remediation** | **Corrected 2026-09-15/16, locally verified** (§19.0): the 2s idle poll (RT-01, `U`), the wake-everyone fanout (RT-02, `P` — ceilings unset), TTS delaying the visual (RT-03, `U`), the webhook waiting on a pump scan (RT-04, `U`), uncoordinated scanning (RT-05, `U`), missing histograms (RT-06, `P` — cross-instance aggregation unproven), and the disabled dispatcher schedule (RT-08, `P`). **RT-07 remains Blocked** — no browser, OBS, device or load evidence exists — so **no speed or "one source replaces twelve" claim is publishable**, and that is unchanged by every fix above. Master Canvas (PRF-02) is also still absent, which independently blocks the "one source" claim. |
| **Alert audio** | **Checks, then synthesis, then one release.** Picture and voice go out together, after every moderation and safety check. The hold is capped at one synthesis attempt by the provider timeout that already exists; an unambiguous failure may be retried, a timeout never may, because a timeout does not tell us whether the characters were already billed. Terminal failure releases the picture without audio and the chime covers it. *Owner decision 2026-09-16, superseding the two-phase release.* |
| **Concurrency target** | **2,000 concurrent live overlays.** Deliberately above a first-year expectation, because a shared channel-keyed subscriber registry is cheap now and a rebuild later, and the failure being avoided is a successful launch weekend taking the product down. |
| **Bounded data** | **No surface may fetch, render, subscribe to or retain more live data than it can display safely** (§12.7). Live surfaces receive small purpose-built projections, never raw history. Deep history stays durable and exportable under §12.6 but is paginated, searched, or exported as a background job — never dumped into a dashboard or an overlay. |
| **Standalone widget URLs** | **Kept, capped, second-class** (§21.3). A per-channel live-transport cap counts Canvas and standalone widgets together; over-cap widgets degrade to slow snapshot polling with a visible notice. No deprecation date, no silent break. |
| **Branding** | **Free: one small protected logo in a fixed Master Canvas corner, plus one quiet tip-page line. Every paid tier: zero branding anywhere** — no logo, watermark, "powered by", end-card, spoken mention, QR badge, tip-page attribution, receipt or email line. The mark is rendered once per Canvas, never per alert or per widget, never spoken, never delaying an alert, above every module and outside their error boundaries, in an editor-reserved safe zone. On a standalone widget only when it is the channel's only overlay source. |
| **Branding enforcement** | **Prevent hiding inside our Canvas; never attempt to detect external OBS layers.** No scene inspection, no covering-check telemetry, now or later. Free terms require attribution to remain visible; paid tiers remove it entirely. Branding is **never injected mid-stream** after a payment problem — the Free mark can appear only on the next clean overlay reload after pause. |
| **Durable creator records** | **Never tier-gated, never sold, never withdrawn.** Storing, viewing, searching, fetching and exporting payments, receipts, refunds, audit trail, supporter relationships, event history, configurations, layouts and moderation history is free at every tier including Free, with no row, date or search cap. Restoring access to data we already accepted is never charged for. Tiering limits **new active capacity only** — active connectors, active widgets, AI usage, new media uploads, custom assets, team seats, automation volume. Over-quota assets go read-only and stay viewable and exportable; deletion follows the published retention policy alone, never a tier lapse. §12.6 outranks every tier table and pricing decision in this document. |
| **Retention** | **One uniform published policy for every tier**, Free to Studio. Per-tier retention windows are removed and the "Event retention" top-up is deleted. Retention is a trust, privacy and legal position, not an upsell. The window itself is a legal number and stays open (§33.2). |
| **Export vs. automation** | Owning the data is free; us doing scheduled work with it is a service. A one-off export of everything, any size, open format, is free at every tier. **Scheduled delivery** into Sheets, Tally or a webhook is an active connector and stays Creator+. |
| **Voice routing** | **Creator-owned deterministic rules, default off.** Amount, message length, Indic script (Unicode range check, no model), supporter relationship and event class decide browser voice versus Sarvam. No AI classifier in the live path — it would cost credits to save credits and be unexplainable. Safety runs identically before both routes; the chosen route and its reason are recorded per alert. Routing is a cost control, never sold and never a paywall. |
| **Pack prices** | **Proposed 2026-09-14, GST-inclusive:** AI Credits ₹49/₹149/₹399 · Storage ₹49 · Socials ₹129 · Events ₹129 · Team Seats ₹129 · Sponsor ₹149 · Finance ₹79 · Multi-Channel ₹199. The three ₹99 packs were raised to ₹129 so that Creator plus two feature packs actually exceeds Studio — at ₹99 it did not (₹597 against ₹599). Multi-Channel stays ₹199 and the resulting ₹598-vs-₹599 comparison is a deliberate steer, not an accident. |
| **Pack launch set** | **The pack system launches with whatever is ready — there is no fixed set of four.** Arrival order **Storage → AI Credits → Socials → Multi-Channel** (§28.3.3, PCK-13): Socials cannot precede Social Relay, and Multi-Channel is blocked on the §37.6 tenant-isolation suite. Events, Team Seats, Sponsor and Finance stay hidden registry rows until their underlying features are real and, for Finance, until the CA/tax evidence row closes. No pack ships in v1 at all — packs are a P3 slice (§1.9). *Corrected 2026-09-14: this row previously promised "four visible at first", contradicting §28.3.* |
| **AI credit top-ups** | **Paid tiers only.** Free keeps its trial allowance; prepaid balances sit on accounts with an existing payment relationship. |
| **Companion packaging** | **Bundled now, unbundlable later — and modelled that way from the start.** Buying any Alerts tier *automatically grants a separate Companion membership record* rather than Companion being implied by the Alerts tier. Free gets Companion too, with controls limited per tier. |

### 33.2 Still open

**Needs data or legal input, not a snap judgement**

1. **Template catalogue** — **answered in principle 2026-09-14 by §9.2, still open on
   scope.** The declarative Canvas Package format changes the problem: instead of
   authoring 359 bespoke packages, author a small first-party set well and let asset
   import (§9.3) cover the long tail. The HTML prohibition is now permanent rather than
   pending — §9.1.1 makes it a boundary, not a trade-off. What remains open is only how
   many first-party packages ship and whether the 241 that render are migrated into the
   new format or retired. Nothing in Phases 0–7 depends on the answer.
2. **The retention window itself** — one number, uniform for every tier (§12.6.2),
   reconciling DPDP with statutory retention for payment records. A legal number, not a
   pricing one, and it blocks nothing else in Phase 0.
3. Legal sign-off on pricing and feature claims, DPDP deletion, and the plaintext reset
   URL in the email outbox.
4. Whether any chance-based giveaway format ever ships (currently: no).

**Pricing and packaging**

5. **What a rupee of AI credit actually buys**, per credit class. The ₹49 / ₹149 / ₹399
   top-up *sizes* are proposed (§28.3); the *quantity* behind them is not, and must not
   be published until real provider cost, retry rates and the §10.1 margin floor are
   measured. Nothing else waits on this.
6. Whether any pack should later become Studio-only rather than purchasable from
   Creator. Answered "no" for the first release; revisit on attach-rate data.

**Product behaviour**

7. Whether the voice-routing default preset (§11.10.2) should ever ship enabled for new
   accounts. Currently off for everyone; changing it is a pricing change and follows
   §20.4.

**Governance**

8. **In-app account deletion vs. the blocked deletion policy** (CMP-78). Both stores
   require a route; legal has not approved one. Needs a decision before submission, not
   during review.
9. **Studio allowances instead of pack bundling** — define concrete numbers rather than
    bundling packs: moderator and operator seats, sponsor campaign slots, scheduled
    finance-export capacity, approval workflows, pooled AI capacity. **Each exposed only
    after its own feature and evidence gate closes**, so none of it is an advance promise.
10. **Pro moderator path** — one limited **non-financial** seat, or a tightly scoped
    moderator add-on purchasable from Pro. Never exposes payment amounts or financial
    records. Requires role projection, RLS, audit and the §37.6 tenant-isolation suite to
    pass first — the same dependency as the Multi-Channel Pack, so one piece of work
    unlocks two revenue items. Probably the strongest single pricing improvement
    available.
11. **A5 split rather than move** — basic campaign and referral links, and basic
    Thumbnail / Channel DNA, stay at Creator; Studio takes multi-campaign management,
    approvals, analytics, batch generation and team review. Moving entry-level
    capabilities upward makes Creator feel artificially crippled. Deferred until usage
    data shows which half people actually want.
12. **Compatibility Routing tier placement** — it is phase R and tier placement cannot
    loosen that gate. Recorded only so the reasoning is not re-derived: its audience is
    creators who *cannot* use Razorpay, so Creator ₹399 may be the wrong home if it ever
    ships. Decide when the four gates close, not before.
13. **Is a no-API YouTube embed inside the v1 exclusion?** `HUB-13` is the IFrame Player
    API — no data scopes, no OAuth, no quota (§4.2) — but the launch authority excludes
    "YouTube channel/data ingestion" and §34 says no YouTube surface before Phase 4. It is
    currently phased **P2, conservatively**. Reversing it to `v1` would need the launch
    authority amended to say the exclusion covers data and scopes, not embeds.
14. **Owners for Step 0, Step 0.25 and every external-evidence row.** Three of these are
    named gaps rather than open questions — the work cannot start without a person
    attached, and the evidence register currently lists roles, not people.
15. Whether iOS link-outs to a purchase surface are safely permitted in India for this
   category — currently answered conservatively as no (§5.6.1) and revisited only on
   evidence.


---

## 34. Build order

Scope is Alerts, dashboard, overlay, Support Hub and mobile Companion. Nothing else.

**Phases 0–2 are v1. Phases 3 onward are not, and none of them may be started, staffed
or announced while a v1 row is open.** The phase labels in §1.9 govern; this ordering
is how the labelled work is sequenced, not a licence to run it in parallel with the
launch.

**The mobile shipping track (§5.6) runs alongside Phases 0–2, not after them.**
Localisation, the five-tab IA, Sign in with Apple, push infrastructure, both-platform
CI and the store artefacts have lead times measured in weeks and several are external.
Starting them at the end is how a mobile launch slips by a month. CMP-39, CMP-49,
CMP-55, CMP-60, CMP-92 and the store-declaration rows begin in Phase 0.

**Phase 0 — make what exists real, and make it controllable.** F01–F22, PRF-01, plus
the control plane (CTL-01 to CTL-04, CTL-09 to CTL-11) and short-lived overlay
capabilities (SEC-01). The control plane comes first because every later phase adds
capabilities that need a switch, and retrofitting a registry onto sixty hard-coded
gates is far worse than seeding it with eight. Nothing new ships until the
product stops being a set of disconnected parts. The identity writer, receipts, TTS
safety, mobile handler wiring, TipForm as the interaction surface,
schedules on, account activation, quarantine UI, the reachability CI checks, and the
performance budgets that will police everything after.

### 34.0 The executable sequence

Everything below runs in this order. Steps −1 and 0 are governance work and are the only
ones exempt from the §31.0 ten-field precondition, under
[`active/launch/07_BUILD_BOOTSTRAP_AUTHORITY.md`](./active/launch/07_BUILD_BOOTSTRAP_AUTHORITY.md)
§1 — they are the steps that *produce* those records, so requiring one first was a
deadlock.

```text
Step −1  Approve and link the external-evidence register        (governance)
Step  0  Register ↔ L-track semantic mapping; JIT active records (governance)
Step  0.25  Provision the production-shaped NON-production
            measurement environment                            (infrastructure)
Phase 0 + 0.5  Foundation and runtime remediation,
               with measured exit criteria
Phase 1–2      Surfaces, then E2E / load / OBS / device rehearsal
Then           External filings · staging evidence · release decision
```

**Step −1 existed because the register that governs external evidence had not yet
governed.** On 2026-09-15 the owner approved it, the master release authority linked it,
and Sukhdev Singh became accountable for every row. The register is now effective as an
operational evidence authority, while its provider, legal, tax, store and production
rows remain open release gates. It still cannot self-approve external evidence.

**Step 0.25 resolves a circularity.** Phase 0.5 blocks Phase 1 and needs OBS and load
evidence; §37.4 requires a production-shaped environment to produce it; §32 lists
deployment as blocked. The resolution is that **a non-production environment is not
blocked — production deployment is**, and the environment is its own scheduled lane with
its own owner rather than a by-product of Phase 0.5. Deliverables and exit criteria are
in the bootstrap authority §3. **Its owner is Sukhdev Singh.**

**A freeze checkpoint sits before anything irreversible.** Filing external gates after the
build is an accepted schedule risk; it is only safe with a review before any schema
freeze, public copy freeze or store submission, covering the payment boundary, deletion
and retention, the mobile purchase boundary, tax representation and consent wording.
Bootstrap authority §4 carries the checklist and requires a written go/no-go per area.

**Step 0 — join the two ID systems, before any lane starts.** This repository already
holds task, test and review records, keyed on the **L-track** system;
the §31 register is keyed on area prefixes, and almost nothing references both
(`TRACEABILITY.md`). So the first task is a **mapping**: register ID → the existing
L-track record that already covers it, and a new `active/` record with the ten §31.0
fields created just in time before implementation only where none does. Two consequences, both load-bearing:

- **Prior evidence is selectively creditable.** The semantic map conditionally credits
  only the `mapped-existing` rows to reviewed task/test/review trios. The remaining
  rows stay `new-record-required`; see [`TRACEABILITY.md`](./TRACEABILITY.md) for the
  generated live counts. They need a real ten-field active record created
  just in time before their lane starts. Neither category is capability-completion
  evidence.
- **The semantic mapping is conditionally closed; capability implementation remains open.**
  Rows marked `new-record-required` are not schedulable until their ten-field
  active task/test/review records are created just in time before implementation;
  no all-rows stub set is created in advance. This is governance evidence only and
  makes no capability-completion or release-readiness claim.

The two checks that are **Blocked** in §35.3 — missing row metadata and reading the phase
from the `active/` record rather than only the register column — become implementable as
part of this, and should land with it rather than after it.

Step 0 has a task record with all ten fields:
[`active/tasks/STEP-0-register-mapping.md`](./active/tasks/STEP-0-register-mapping.md).
**Its owner is Sukhdev Singh**, and the mapping is being validated as a separate
fail-closed artifact. It is deliberately *not* scoped to fill ten fields for every row
before a lane takes them — that would be documentation theatre. Rows are recorded when a
lane takes them; the mapping exists so taking one is cheap.

**Phase 0.5 — runtime remediation, and it blocks Phase 1.** RT-01 to RT-13. These are
corrections to code that already runs in front of real payments, and every one of them
gets worse with more traffic and more surfaces on top. RT-06 and RT-07 come with them
rather than after, because a fix with no histogram and no OBS soak is a fix we cannot
show worked. Master Canvas (PRF-02) lands here too — it is the thing every later phase
assumes and the reason the connection model is worth fixing once.

**Phase 1 — the surfaces people touch.** Live Support Hub steps 1–3 (tray, verified
state, receipts, ticker, goals, reactions, sticker and sound picker, message preview) ·
Companion Live Deck with health and degraded states · Clutch Mode · Master Canvas with
the first six modules · the four-switch customisation model.

**Phase 2 — the cockpit completes.** Prepare Stream checklist · Wrap Stream · scene
presets · goal controls · markers · per-item queue control · the six monetisation
notification types.

**Phase 3 — community mechanics.** Lobby MVP and trust layer · goal ladder ·
transparent votes · mission card · milestone queue · Sound Moments and the Interaction
Rules Engine · custom audio with attestation, on GCS (STO-01 first) · stat widgets with
the Companion tap source.

*Everything from here is post-v1 (§1.9).*

**Phase 4 — YouTube depth (P2, excluded from v1 by the launch authority).** Opens with
**F06 and F07**, moved here from Phase 0 on 2026-09-14: the connect / disconnect /
reconnect UI and revoked-auth surfacing. No YouTube surface is built before this phase,
including the connect step, and no YouTube capability may be marketed until it lands.
Also· Member reconciliation · like goals · controlled broadcast
lifecycle · chat moderation · the identity and trust model.

**Phase 5 — monetisation depth (P2).** Season Passes · Priority
Questions · member perks · top-ups and the credit ledger · Discord role sync.

**Phase 6 — safety and AI (P2).** Indic safety · AI moderation queue · TTS-safe rewrite ·
copilot · recap and clips.

**Phase 6.5 — creator ops (P3).** Finance Pack (the highest-value unserved job) · content
calendar and public schedule page · sponsor deliverable tracker · the pack framework
itself.

**Phase 6.75 — interop (P2).** Canvas Package format and validator · asset import on
the §18.3 gate · migration wizard · first-party curated package library · private
creator packages. The format comes first because it is also the template-catalogue
answer, and because every later interop item renders through it.

**Phase 7 — events, collaboration and social (P3).** Social Relay starting with Discord,
then YouTube, then Instagram and WhatsApp opt-in · Co-Stream Room · giveaways · tournaments ·
sponsor manager and exposure logs · finance exports · post-stream analytics ·
portability.

**Decided:** the control plane is Phase 0, not a later retrofit.

**Phase 7.5 — bot and bridges (P2/P3).** BharatStudio Bot's six-item first release
(§36.5), then the Streamlabs bridge and the Companion-helper adapters for Streamer.bot,
SAMMI and Mix It Up. The bot cannot start before YouTube depth (Phase 4) and the
chat-write scope; the bridges cannot start before the connector outbox (INT-10).

**Research-only track, phase R, unscheduled and unstaffed.** Third-party package
marketplace publishing (INT-18) · StreamElements event bridge (INT-17) · Payment
Compatibility Routing (§25) — no schema, no UI, no marketing until its four gates close. Enterprise
(§24) proceeds only when its reopening gate closes. Nothing in Phases 0–7 depends on
either.

**Phase 5's "room-password delivery" line is void** — superseded by the Lobby Engine
and by the §16.2 correction. No payment returns a code.

Two things are not phases:

- **Instrumentation** (OPS-08 to OPS-11) ships with Phase 0 or the first cohort's data
  is lost permanently.
- **Performance budgets** (PRF-01) land before Phase 1, because retrofitting a frame
  budget onto twenty modules is far harder than holding it from the first one.

---

## 35. Maintaining this document

**What this file is.** The authority on *product content* — what each capability is,
what it means, which tier and phase it belongs to, and what must never be built. Master
plan Part 7 is superseded on that, and should not be consulted for status.

**What it is not.** A release authority. On scope, dates, gates and evidence,
`active/launch/00_LAUNCH_SCOPE_AUTHORITY.md` and
`active/launch/01_MASTER_RELEASE_AUTHORITY.md` win, always, without needing to be
re-argued. If this document and one of those disagree, this document is wrong and gets
corrected — not the other way round.

### 35.1 Rules for keeping it true, learned from how Part 7 went wrong:

1. A status may only be changed by someone who **traced the user path**, not by
   someone who found the code.
2. Every row's state uses the §0 vocabulary. "Done" is not a permitted value.
3. Reconciliation runs **after** a batch closes, never inside it — a lane running
   alongside build lanes records the tree as it was at dispatch.
4. When a claim here turns out to be wrong, correct it in place and say what was wrong.
   Four rows in Part 7 asserted things that were never true; nobody caught it for
   eleven days because the register was never re-derived from code.
5. Test counts are never cited as evidence of completeness.
6. **No local artefact is ever promoted to launch evidence.** A passing suite, a staging
   run we ran ourselves, a review of this document, or a section of this document, is
   never the thing that closes an evidence row in
   `05_SUPPORT_AND_EXTERNAL_EVIDENCE_REGISTER.md`. Those rows close on dated external
   evidence with a named reviewer and a disposition — provider, counsel, store, or a
   third party — and self-review is not a substitute.
7. **One outcome per decision.** A decision lives in §33.1 and nowhere else. When a
   decision changes, the superseded text is **deleted** from the body of the document
   and the change is recorded as a dated correction in the §33.1 row. Version 1.0
   carried three live outcomes for Amazon Pay, two for paid room codes and two for
   weighted giveaways, because superseded text was left standing next to its
   replacement. Leaving the old wording "for the record" is how that happened; the
   record belongs in the decision row.
8. **Every proposed tier-ladder or pricing change states which boundaries it was checked
   against** — §12.6 durable records, §12.7 bounded data, §30.1 correctness, and the
   launch authority's no-drop rule. Four lines on every proposal. Three proposals in a row
   violated rules already written in this document (a TTS grace buffer against the ledger
   invariant, Studio-only widgets against §37.11, 2,000 pending visuals against §12.7);
   that is a missing gate, not three slips.
9. **A capability's presence here is never permission to build it.** Phase label first
   (§1.9), then the ten fields in §31.0, then a lane.

### 35.2 Corrections applied 2026-09-14

| What was wrong | Correction |
|---|---|
| Document presented itself as an authority superseding the launch scope | Restated as `Proposed`, product-content authority only; launch authority wins on conflict (header, §1.9, §35) |
| Amazon Pay was simultaneously "never", "pending" and "build under C1–C7" | **Never build.** RTE-13 set to N; §33.1 row rewritten; §25.5 explains why consent does not reach a consumer credential |
| Paid room-code access dropped in §10.5 and retained in §16.2 | §16.2 clause deleted, not narrowed. No payment returns a seat or a code |
| Tier matrix advertised weighted giveaways against a free-entry-only decision | Row changed to "Giveaways (scheduled, free entry)" |
| `global_kill` governed by two conflicting rules | §20.6.1 defines the emergency path: reason, 24h expiry, 4h ratification, immutable log, 72h review |
| Account deletion presented as decided | Moved to §32 blocked; no flow and no promise until legal approves. Store requirement tracked as CMP-78 |
| "No provider pricing is ever shown" contradicted the calculator requirement | §12.5.1 states the boundary once, with fee scope, sourcing, owner, 90-day staleness rule |
| Customer-facing "AI tokens" contradicted the units model | Renamed to AI credits; "token" is internal-only vocabulary |
| Global cross-creator content-addressed dedup | Tenant-scoped by default; global only for owned or licensed assets (§19.1, STO-04) |
| Media upload gated only by attestation and a no-op scanner | §18.3 upload gate; capability stays off until every row is built and one takedown drill is rehearsed |
| "Support the shared goal" with money settling to one creator | Option withheld until beneficiary disclosure, refunds, tax, agreement and legal wording exist (§22.5) |
| CMP-37 cross-referenced §27.4 (Social Relay) | Corrected to §30.4 |
| Clutch Mode withheld from Free while CMP-17 listed it P0 | Available on Free — it is a safety control (§30.4) |
| Register rows had no phase, owner, data class, failure behaviour, kill switch, acceptance test, evidence location or rollback | §31.0 makes all ten mandatory before a row is schedulable |
| **`CUS-01`–`CUS-06` were defined twice** — once for the gating model, once for the new customisation-depth block | The depth block is renumbered **`CST-01`–`CST-30`**; one prefix, one owner, and `tools/doc_consistency.py` now fails the build on any duplicate ID |
| **`01_MASTER_RELEASE_AUTHORITY.md` still carried the superseded 1/3/5/10 ladder and the superseded `bytea` decision** below their own amendments | Both blocks now carry an explicit SUPERSEDED banner; the queue table shows the old and approved columns side by side; the checker fails if either marker disappears |
| **L15 said "YouTube ships in v1" throughout its body** after only its opening was corrected | Rewritten end to end as Phase 4 / post-v1, including the scope, deliverables and `CON-01`–`CON-07` phase note |
| **`ENT-04` carried the old Studio ceilings** (bindings 20, presets 8) | Updated to 50 and 20, with the held rows named |
| **`WMK-05` said zero branding on receipts and emails**, contradicting the §30.6.4 issuer-identity carve-out | Rewritten as zero *marketing attribution*, with the carve-out named |
| **The pack-launch decision row previously promised "four visible at first"** against §28.3's "whatever is ready" | Row rewritten to the arrival order, with the correction dated |
| **§28.3.1 and §28.3.2 were each used twice** | Renumbered to 28.3.3 and 28.3.4; the checker fails on any duplicate section number |
| **§33.2 skipped item 9** | Renumbered; the checker fails on any ordered-list gap |
| **Nine CI checks were claimed but nothing executable existed** | `tools/doc_consistency.py` and `.github/workflows/doc-consistency.yml` — implemented, running, and it found 20 further defects on its first run, all now fixed |
| **§35.4 gave a traceability schema with no populated rows** | `TRACEABILITY.md`, generated by `tools/traceability.py`, regenerated in CI and stale-checked. Counts live only in that file |
| **"One uniform retention window" conflated tiers with data classes** | §12.6.2 is now a **schedule by data class** — payment and audit on statutory retention, chat logs shortest — with the tier never an input to any row |
| **Register state cells carried gates instead of state letters** (`**Never**`, `**Consent-gated on C1–C7**`, `**R**`) | Normalised to U/X/P/A/B/N with the gate moved into the item text; enforced by the checker |
| **§35.3 presented a specification as running controls** — eleven checks claimed, nine narrow ones implemented, several not implementable at all | Every check row now carries its real status: Running, Partial, Warn or Blocked with the named prerequisite. The overstated blanket claim is gone |
| **`tools/traceability.py` hard-coded zero acceptance, review and evidence** and asserted "no build work has started", while the repository holds 62 task records, 62 test records and 72 reviews it never looked at | Rewritten to scan `tasks/`, `tests/`, `reviews/`, `done/` and `active/` and report only what it finds. The real finding — two ID systems that do not meet — replaces the false zero |
| **§35.4 restated a register count in prose** that the generator had already moved past | Counts live only in `TRACEABILITY.md`; a checker rule now fails the build on any count hard-coded near the words "requirement", "register" or "rows" |
| **§31.0 still said any provider or legal dependency inherits phase R**, after §1.9 split G from R | Corrected — a provider or legal dependency is **G** unless building it at all needs the external party's permission first |
| **§34 Step 0 was "generate stubs"**, which would have produced 633 empty files and buried the existing corpus | Step 0 is now semantic mapping first; capability records are created just in time only when a lane takes a row |
| **§1.9 required a phase label on every register row; the register had no phase column**, so §35.3's phase check was Blocked and the build/research boundary was unenforceable | A **Phase column** added to all register rows by `tools/assign_phases.py` from printed rules, and the phase check is now **Running** — invalid phases fail, and an R or N row named in a §34 build phase fails |
| **§31.0's scope-phase field omitted the G state** that §1.9 had just defined | Field rewritten to `v1 · P2 · P3 · R · N` with the `·G` release-gated suffix, and it names the register column as the machine-checkable home |
| **The traceability generator looked for evidence only in `done/`**, while §35.4 names `active/launch/05_SUPPORT_AND_EXTERNAL_EVIDENCE_REGISTER.md` as the authority — so a closed provider or legal row would still have read as empty | The generator now scans `active/launch/` as an evidence corpus and reports it as its own column |
| **§35.3 carried a duplicate, malformed "Stale external claim" row** with no status cell, inside the table that promises every row states its status | Duplicate removed, and a **Table shape** check added — every row in a table must match that table's column count. It immediately found five more malformed rows elsewhere |
| **The phase classifier was prefix-only, so it phased every `VID-` and `HUB-` row `v1`** — including YouTube identity attribution, YouTube namespaces and the embedded player | Content rules now run **before** prefix defaults in `tools/assign_phases.py`, and a **Scope semantics** check enforces the same rule independently. Five rows were mis-phased; the audit found two, the check found three more (`ENG-16` Super Chat aggregation, `HUB-09` Super Chat goal labels, `CUS-06` Super Chat styling) |
| **`VID-11` reported a DPDP deletion capability as usable** while §33.1 blocks deletion and §32 lists it as unblocked-by-legal-only | State corrected to **B**, with the row stating that the split logic exists in code, no flow ships or is promised, and deactivation is what ships. `VID-21` archival deletion corrected the same way — an engineering preference is not an approved policy |
| **`HUB-13`, a no-API YouTube embed, was phased `v1`** | Phased **P2 conservatively** and raised as §33.2 item 13: whether the launch authority's exclusion covers embeds or only data and scopes is a question for the authority, not for this document to assume |
| **The v1-scope scan checked only Phase 0** while §1.9 makes Phases 0–2 v1 | Widened |
| **§34 Step 0 was mandatory "before any lane starts" and had no authority, owner, record or acceptance** — the plan's own first gate was unstartable under its own rules | `active/launch/07_BUILD_BOOTSTRAP_AUTHORITY.md` defines a narrow bootstrap exemption for Steps −1 and 0, and `active/tasks/STEP-0-register-mapping.md` carries all ten fields. Owner assigned to Sukhdev Singh; remaining lifecycle-record work is explicit |
| **Performance validation was circular** — Phase 0.5 needed OBS and load evidence, §37.4 needed a production-shaped environment, §32 listed deployment as blocked | Resolved by distinguishing **non-production measurement from production deployment**. Step 0.25 is a scheduled infrastructure lane with named deliverables and an exit criterion |
| **§32 grouped YouTube OAuth, YouTube quota and the Razorpay Route enquiry under "everything production"** — which would have held the Alerts and Companion launch behind Phase 4 and Enterprise work | Split into three rows: v1 release gates, YouTube-capability-only gates, and Enterprise-only gates. The external register had always scoped them correctly |
| **The plan relied on an evidence register that declares itself not effective** until approved and linked from the master release authority | **Step −1** added: approve it, link it from `01`, and give each row a named owner rather than a role name |
| **"File external gates after the build" had no checkpoint** before irreversible schema or copy freeze | Freeze checkpoint added, with five named areas and a required written go/no-go |
| **§12.6 guaranteed moderation history be viewable and searchable, and nothing rendered it** — audit records existed (`ALQ-10`, `ADM-02`, `ADM-08`, `CTL-01`, `AUD-08`, `LOB-08`, `BOT-14`) with no surface. The §2 pattern forming before new code | §7.5 Activity Log, `DSH-12`…`DSH-15`, Companion Recent Actions (`CMP-94`), E2E `DSH-E6`…`DSH-E8` |
| **§7 listed the dashboard's jobs and never its screens, and the register had no dashboard section at all** | §7.1 screen inventory · §7.2 detail-view contract · §7.3 one-click affordances · §7.4 supporter profile and command palette · §7.6 support handoff bundle · §7.7 authored states. New register section §31.13.1, `DSH-10`…`DSH-31` |
| **§12.2 was a nine-bullet list** for the highest-harm gap in the register, with no pipeline, no evasion handling, no failure behaviour and no per-surface decision model | §12.2.1–12.2.7: one corpus and one pipeline across every surface, L0 normalisation against homoglyph/leet/zero-width/Zalgo evasion, phonetic keys per Indic script, independent per-surface decisions, fail-closed-for-speech, untiered, auditable, appealable. `SAF-01`…`SAF-19` |
| **Nothing addressed what AI safety classification would cost** | §11.12: the ladder decides cheaply and escalates rarely; an HMAC-keyed verdict cache with `policy_version` in the key; **term-level caching so an AI verdict becomes a permanent deterministic rule**; batching, signal-based escalation, distillation, budgets that never stop L0–L3. `SAF-20`…`SAF-30`, E2E `SAF-E1`…`SAF-E10` |
| **The corpus had no seeding plan, no schema, no growth model and no governance** | §12.9: seed small and precise, per-term record, T1/T2/T3, allowlist for the Scunthorpe problem, named native-speaker owners, the discovery flywheel and near-miss telemetry. `SAF-31`…`SAF-40` |
| **Nothing said how long moderation evidence is kept** | §12.10: **snapshot the evidence at action time**, keep the action record long, keep raw unactioned chat on the shortest class. `SAF-41`…`SAF-43` |
| **Cross-creator flagging was undefined**, next to a §16.3 rule prohibiting a global blacklist | §12.11: share **signals, never verdicts** — decaying, unattributed, never auto-actioning, OAuth identity only. `SAF-44`…`SAF-46` |
| **Supporter reputation was referenced and never specified** | §12.12: derived not stored, negatives private, decaying, appealable, never purchasable. `REP-01`…`REP-05` |
| **§32 read as "no rail supports refunds"**, which was true of our abstraction and misleading about the provider | §10.10: Razorpay supports refunds; **we lack the delegated authority**, which arrives with the partner approval. Reconcile-from-webhook ships first, in-product initiation follows. Full data model, state machine, nine edge cases, and both parties' views. `REF-01`…`REF-20`, E2E `REF-E1`…`REF-E10` |
| **The product had goals, a milestone queue and a rules engine, and nothing saying what happens at 100%** | §23.3: the completion latch, the full trigger and action catalogues, YouTube's real and narrow options, ordered sequences with delays, non-configurable safety interlocks, templates and preview, and the overflow and refund accounting. `GOA-01`…`GOA-29`, E2E `GOA-E1`…`GOA-E10` |
| **Completion would have been a recomputed boolean over a derived total** — so a refund would have un-completed a goal and the next tip would have re-fired the celebration | `GOA-01` latches `goal_completed` as a recorded event; actions fire from the event, never the boolean |
| **QR and UPI flows were scattered across five sections, and three load-bearing rules were assumptions rather than text** — which QR the overlay shows, whether a QR may embed an amount, and what happens when the channel link rotates | §8.2.1: three distinct QR kinds, **the overlay QR is always a Channel QR**, amount rules per kind, expiry and regeneration, device routing, the intent return path, verification, and the funnel record. `QR-01`…`QR-15`, E2E `QR-E1`…`QR-E10` |
| A TTS grace buffer was proposed, contradicting the append-only ledger and TTS-04 | Rejected; §11.11 states no buffer exists and none may be added |
| Studio-only widgets were costed at zero the day after §37.11 required per-widget runtime, performance, accessibility and OBS verification | Deferred until each widget's package passes |
| 2,000 pending visuals was proposed against §12.7 | Rejected; the existing 500 is now itself flagged for verification |
| "Studio includes ₹357 of packs" double-counted capabilities already Studio-only, and would have advertised two hidden packs | Rejected; replaced by concrete gated allowances (§33.2 item 9) |
| "Every string overridable" would have exposed payment, legal, consent, security and error text | §15.4.2 protected string class, enforced by the system |
| No boundary check existed on tier or pricing proposals | §35.1 rule 8 |
| **Amazon Pay carried three live outcomes** — "never build" in the §25.5 table, "build under C1–C7" in the conditions section, and "never build" again in §33.1 | The §25.5 conditions paragraph is **deleted**, not annotated. C1–C7 are stated to cover delegated sub-users only and never to reach a consumer credential |
| **Account deletion was decided in §12.3 and blocked in §33.1** | §12.3 rewritten: the archival approach is an engineering *preference*, deletion is blocked on legal, nothing ships or is promised, deactivation ships meanwhile, and CMP-78 carries the store conflict |
| **Phase 0 contained YouTube connect work** while the launch authority excludes YouTube from v1 | F06 and F07 moved to Phase 4; the Phase 0 prose no longer lists a YouTube surface |
| **Two authorities carried different queue ladders** | 1/2/3/5 stands and the launch authority is **amended**, rather than being declared superseded from inside this document |
| **Two approved storage designs** for uploaded Lottie | GCS/CDN is the design, the release authority is **amended**, and §19.1 now carries migration, serving, retention, rollback and done-when rules |
| **"Zero branding anywhere" removed issuer identity** from receipts and security mail | §30.6.4 defines a narrow closed carve-out for legal and transactional identity, with two rules preventing drift into marketing |
| **§25.2 carried generic credential language** telling creators they could authorise us to hold a PIN or password | Deleted. A credential consent flow may exist only inside a named, provider-approved route, and none has passed its gates |
| **Portability said downgrade "narrows the dashboard search window"** | Deleted — it directly violated §12.6. Search, filter and export are unrestricted at every tier |
| **"Any provider or legal dependency becomes phase R"** would have made the Razorpay path unbuildable | Split into **G** (release-gated, build now) and **R** (research only), with the current membership of each listed |
| **Top-ups and packs overlapped** with no commercial model | §28.1.1 draws the line; §10.2 shrinks to two consumables; seven items move to packs |
| **Canvas Packages were "signed" with no signer model** | §9.2.1: BharatStudio-only signing, KMS key with no human read path, rotation with recorded key IDs, revocation checked at import and render, canonical serialisation, provenance, and sandboxing independent of signature |
| **Platform-map capabilities were undocumented assertions** | §27.2 requires source URL and read date, OAuth scope, published rate limit, privacy data flow, failure mode and a named owner per row, with a 180-day staleness build failure |
| **Performance targets were not reproducible** | §37.4 fixes the reference environment: topology, seeded database size, skewed channel-size profile, asset mix, network profiles, named devices, OBS as the pass/fail environment, a JSON pass/fail artefact, and "worst of three runs is the result" |
| **Nothing prevented the next contradiction** | §35.3 adds nine CI checks on this document — duplicate decision outcomes, stale superseded wording, orphan corrections, missing row metadata, post-v1 references in v1 sections, phase-label integrity, cross-reference validity, authority conflict, and stale external claims |
| §33.1 listed multi-channel as Studio-only while §28.3 sold a Multi-Channel Pack from Creator | Multi-channel is a Studio **capability**; the pack is the Creator-tier route to one additional channel — which is what §28.1 says a pack does |
| Four packs were named as the first release with no readiness check | §28.3.1: Socials cannot precede Social Relay and Multi-Channel needs tenant isolation; the system launches with what is ready, in a stated order (PCK-13) |
| The document specified no tests, evidence or performance numbers per task | §37: the ladder and what each level cannot prove, a definition of done, 56 named E2E scenarios across eight surfaces, a measured performance table, load/soak/chaos profiles, security/isolation/accessibility/localisation suites, evidence artefacts, merge-versus-release gates, and what is never evidence |
| §9 described interop in six lines with no format, no boundary and no bridge architecture | §9.1–9.9: three separated capabilities, the no-embedded-third-party-code boundary, the Canvas Package format, asset imports on the §18.3 gate, the migration wizard, the outbound-only bridge path, per-integration positions, tier placement and build order (INT-01 to INT-20) |
| No chat-bot product existed anywhere in the document | §36 BharatStudio Bot: six areas, deterministic multilingual first, AI recommends and never bans, one shared safety corpus with §12.2, a deliberately small first release, and an explicit statement of what blocks it (BOT-01 to BOT-17) |
| The template catalogue had been open since v1.0 with no path | §9.2 answers it in principle — a declarative format plus imports replaces authoring 359 bespoke packages; the HTML prohibition becomes permanent rather than pending |
| Architecture claimed "one source, one connection, one loop" while overlays polled every 2s and one event woke every stream | §19.0 RT-01 to RT-13, a new Phase 0.5 that blocks Phase 1, and a publishable-claims freeze until they close |
| TTS enrichment ran before the visual was released, with no failure classification, no retry policy and no ordering guarantee | Kept before release **deliberately** so picture and voice stay synced, but bounded: one attempt, retry only unambiguous failures, never a timeout, release without audio on terminal failure (RT-03, owner decision 2026-09-16) |
| Payment webhook acknowledged only after a worker-pump call with no recovery sweeper | One commit, immediate 2xx, fire-and-forget wakeup, leased dispatcher that owns enqueueing and recovery (RT-04, RT-05, RT-08) |
| §19.4 promised p99s the metrics cannot compute | Histograms mandatory; PRF-01 cannot pass without RT-06; §19.4 gains idle-load, visual-release, ack and concurrency rows |
| §19.5 asserted the Canvas benefit as present tense | Marked absent, and the "one source replaces twelve" claim blocked until PRF-02 ships |
| No rule bounded what a live surface may load | §12.7 bounded data, with a per-surface table and the backend obligations that make it enforceable (PRF-17 to PRF-19) |
| Standalone widgets each opened their own transport with no limit | §21.3 keeps them, capped by a per-channel live-transport budget, degrading to snapshot polling over the cap (RT-13) |
| Branding was one undefined "watermark" row in the tier matrix | §30.6: one protected Canvas mark plus a Free tip-page line; zero branding on every paid tier; no mid-stream injection; explicitly no external-layer detection (WMK-01 to WMK-07) |
| Durable creator records were tier-gated and retention was sold as a top-up | §12.6 makes records untiered and unsellable at every tier; retention is uniform; the top-up row is deleted; CTL-14/CTL-15 enforce it in the registry rather than by review |
| §26.2 deleted paid-only configuration at Expired | Only third-party secrets are destroyed; configuration, layouts, mappings and every durable record persist and stay exportable |
| The "Retained 90 days" state read as a history clock | It is the connector-secret window only; durable records are not on that clock |
| CON-17 tiered chat retention | Display and filtering stay tierable; retention does not |
| §28.2 cited "§27.1 correctness" (Social Relay) | Corrected to §30.1, and extended with the §12.6 record set |
| Premium TTS was spent uniformly until the quota ran out | §11.10 voice routing: deterministic creator rules, default off, no classifier in the live path, route and reason recorded (TTS-11 to TTS-16) |
| Packs had no prices | §28.3 price sheet; three ₹99 packs raised to ₹129 so Creator + two feature packs actually exceeds Studio (₹597 did not); four-pack first release, four hidden until their features are real |
| Companion had no shipping plan: no purchase position, no languages, no push infrastructure, no auth requirements, no IA, no first run, no device matrix, no release process, no store compliance, no ops | §5.6 and 56 new register rows (CMP-38 to CMP-93) |

### 35.3 CI checks on this document itself

**Implementation status, stated per check rather than as a blanket claim.**
`tools/doc_consistency.py` runs in `.github/workflows/doc-consistency.yml` on every push
and pull request, exits non-zero on any error, and the workflow regenerates the §35.4
index and fails if it is stale. Run it locally with `python3 tools/doc_consistency.py`.

**But the table below is a specification, and only part of it is executable today.**
An earlier version of this section presented the whole list as running controls, which
overstated what exists — the same failure this document keeps recording about itself.
Every row now carries its real status:

| Status | Meaning |
|---|---|
| **Running** | Implemented, fails the build |
| **Partial** | Implemented as a narrower or curated rule than the description; catches the known cases, not the general one |
| **Warn** | Implemented, reports, does not fail the build |
| **Blocked** | Cannot be implemented until data that does not yet exist is created. The prerequisite is named |

The structural failure this file keeps producing is that a correction is recorded in
§33.1 while the stale text survives in the body — which is how Amazon Pay carried three
live outcomes, deletion carried two, and the pack launch set carried two. §35.1 rule 7
already forbids it; a rule nobody can enforce is a wish. These checks run in CI and fail
the build:

| Check | Fails when | Status |
|---|---|---|
| **Duplicate requirement IDs** | One ID is defined in two register tables | **Running** |
| **Duplicate section numbers** | One `§n.n` heading number is used twice | **Running** |
| **Cross-reference validity** | A `§n.n` reference points at a heading that does not exist | **Running.** *Subject* matching — that the cited section is about what the citation claims — is **not** implemented and would need a semantic check |
| **Register row shape** | A row lacks four cells, carries a state outside U/X/P/A/B/N, or has an empty priority. A gate belongs in the item text, never the state column | **Running** |
| **Ordered-list gaps** | A numbered list skips a number — the signal that a log entry was deleted rather than superseded | **Running** |
| **Authority conflict** | This document states a value differing from `active/launch/*`, or an authority carries a superseded value with no marker within 15 lines | **Running**, for the two known values (queue ladder, `bytea`). A general value-diff across documents is not implemented |
| **Stale superseded wording** | A decision appears as a live instruction after its §33.1 row says blocked, never or proposed | **Partial.** A curated rule list covers Amazon Pay, the pack launch set, the queue ladder, deletion, branding, the ₹357 figure and the raid-night phrase. It is not a general duplicate-outcome detector — that needs every decidable statement to carry a decision key, which does not exist yet |
| **Post-v1 references in v1 sections** | A **Phase 0, 0.5, 1 or 2** entry references a post-v1 capability | **Partial.** Keyword list. *Corrected 2026-09-14 — it previously scanned Phase 0 only, while §1.9 makes Phases 0–2 v1* |
| **Scope semantics** | A row whose text names a YouTube capability (YouTube, Super Chat, chat-write, live chat, `streamList`) carries a `v1` phase · a deletion capability is marked usable while §33.1 blocks deletion | **Running.** This is the check that phase *syntax* validation cannot do: a prefix classifier cannot see that a `VID-`, `ENG-`, `HUB-` or `CUS-` row is really YouTube work. It found five such rows on its first run, three of which no reviewer had spotted |
| **Orphan corrections** | A correction is logged while its superseded text survives in the body | **Warn.** Heuristic — it compares inline correction markers against §35.2 rows and cannot locate the surviving text |
| **Missing row metadata** | A taken register row lacks any of the ten §31.0 fields in its `active/` record | **Running.** `new-record-required` rows remain JIT with `-` targets; taken rows fail closed until their active record is complete |
| **Phase-label integrity** | A row has no phase label, carries one outside the values defined in §1.9, or a row labelled R or N is scheduled in a §34 build phase | **Running.** The register gained a Phase column on 2026-09-14; `tools/assign_phases.py` records how each value was derived |
| **Stale external claim** | A platform-map row (§27.2) or gateway-fee figure (§12.5.1) is older than its freshness window | **Blocked.** No row carries a source date yet — the §27.2 requirement was added after that table was written |
| **Table shape** | A row in any table has a different column count from the rest of that table — which is how a malformed duplicate row survived in this very table | **Running** |

### 35.4 Traceability — one index, six columns

Every requirement is followable end to end, in one place, or the evidence rules in §37
cannot be audited:

```text
requirement → task → acceptance record → review → evidence → release gate
```

| Column | Content |
|---|---|
| **Requirement** | The §-reference and the register ID |
| **Task** | The file in `active/` carrying the ten §31.0 fields |
| **Acceptance record** | The named E2E scenarios from §37.3 and the reachability assertion |
| **Review** | Who traced the user path, and when — §35.1 rule 1 |
| **Evidence** | The dated artefacts from §37.8, or the external row in `05_SUPPORT_AND_EXTERNAL_EVIDENCE_REGISTER.md` |
| **Release gate** | Which gate in §37.9 this blocks, or "none" |

A row with a gap in any column is not done, whatever its state letter says. The index is
generated from the register and the task files, not hand-maintained — a hand-maintained
index drifts exactly the way Part 7 did.

**It exists and is generated:** [`TRACEABILITY.md`](./TRACEABILITY.md), produced by
`tools/traceability.py` and regenerated in CI, which fails if it is stale. **Counts live
in that file and are deliberately not restated here**, because a number copied into prose
goes stale the moment the register changes — which it already did once.

**Historical finding before the 2026-09-15 Step 0 map — superseded.** What it found,
and it is not what an earlier version of this section asserted. That
version said the index showed zero acceptance records, zero reviews and zero evidence
"because no build work has started". Both halves were wrong. This repository contains
Existing task, test and review records come from substantial prior work; the generator
now scans all of those corpora and reports their actual coverage.

The real finding is sharper: **two ID systems that do not meet.** The existing corpus is
keyed on the **L-track** system (`L01`…`L32`, plus `WP-`, `FORM-`, `FRD-` work-package
identifiers). The §31 register is keyed on **area prefixes** (`PAY-`, `CMP-`, `RT-`…).
The semantic map now joins the reviewed trios for its mapped-existing rows; the
remaining rows stay new-record-required until their JIT records exist. Local evidence
remains subject to self-review and does not satisfy external or release gates.

**Step 0 semantic mapping is conditionally closed; capability implementation lifecycle remains open** —
register ID → the
L-track record that already covers it, and a new `active/` record only where none does.
Rows marked `new-record-required` remain unschedulable until a lane creates and verifies
their ten-field records.

### 35.5 Splitting this file — agreed, and deliberately sequenced after the fixes

At 5,400-plus lines this document mixes frozen authority, roadmap, decision log,
registry, evidence rules and test plan, and those layers are hard to review together.
The agreed target is six documents plus the §35.4 index:

1. Frozen v1 authority
2. Post-v1 product backlog
3. Decision log
4. Capability and tier registry
5. External evidence register (already exists in `active/launch/`)
6. Test and performance plan

**Decided 2026-09-14: fix every contradiction first, split second.** Splitting a
document that still contains conflicting statements copies the conflicts into six files
and makes them harder to find, not easier. The split happens once §35.3 passes clean on
the single file.

---

## 36. BharatStudio Bot

Added 2026-09-14. **Phase P2, and gated** — see §36.8. This section exists so the shape
is decided before anyone starts, not because it is next.

### 36.1 What it is, and what it must not become

An **automation product, not another dashboard**. The failure mode for every chat bot
is the same: it grows into an unreadable node-graph builder that three power users love
and everyone else abandons. We are building the opposite — a small set of things
creators actually type into chat, done well, in their language.

```text
Chat platform events
  → connected-channel adapter
  → BharatStudio command / moderation engine
  → actions: reply · overlay · loyalty · poll · Discord · Companion · webhook
```

The creator sees six areas and no more:

**Commands · Moderation · Automations · Languages · Connected channels · Import from
existing bot**

### 36.2 Command import — guided, honest, best-effort

Creators can import or paste **their own exported** command sets from Nightbot,
StreamElements, Streamlabs Cloudbot, Streamer.bot, Mix It Up and SAMMI. Export files
the creator supplies, never a scrape and never their credentials.

Mappable fields: command name and aliases · response text · cooldown and user-level
restriction · enabled platforms · basic variables (`{user}`, `{amount}`, `{count}`) ·
trigger phrases · simple timed messages.

The result is shown as a plain table, and the honest rows matter more than the imported
ones:

```text
Old command      BharatStudio result
!discord         Imported
!rules           Imported
!songrequest     Needs a music-provider connection
Custom script    Cannot import safely — recreate as an Automation
```

**Never imported, under any circumstance:** arbitrary scripts, raw JavaScript, shell
commands, HTTP calls to arbitrary URLs, or any third-party credential. Those become an
explicit manual **Automation recipe** built from a narrow allow-list of actions — the
same principle as CMP-05 and §9.6: we never execute a command shape we did not define.

### 36.3 What the bot is for

- **Info commands** — `!tip`, `!support`, `!membership`, `!discord`, `!rules`,
  `!socials`
- **Live mechanics** — goals, polls, predictions, giveaways, viewer queues, "play with
  me" lobbies (§16, §17)
- **Acknowledgement** — tip acknowledgement and donor thank-yous, subject to the
  visibility consent rules in §12.3
- **Outbound** — "stream is live", "goal reached", "new video" to Discord, Telegram, and
  WhatsApp Community where permitted. This is the Social Relay path (§27), not a second
  one
- **Chat-controlled overlays** — `!vote`, `!join`, `!rank`, `!challenge`
- **Moderation** — warnings, timeout and ban *requests*, blocked terms, link filtering,
  spam and flood detection
- **Creator workflow** — a command that opens a Companion action, switches a scene
  through an approved local adapter, or triggers a selected Streamer.bot / SAMMI action
  (§9.6)
- **Commerce** — sponsor codes, affiliate links, ticket links, merch announcements
- **Post-stream** — chat highlights, an FAQ list, moderator actions, poll results, into
  the Wrap Stream summary (§5.5)

### 36.4 Multilingual chat — deterministic first, AI second

This is the part with the most value for an Indian audience and the most temptation to
do badly. **The default is not "AI translates everything".**

Deterministic layer, built first:

- Command aliases in English, Hindi, Hinglish and creator-selected languages
- **Unicode and transliteration matching** — `!rules`, `!niyam`, `!niyem`, `!नियम` all
  reach the same command
- Localised bot replies, per channel or per the language the viewer used
- **Profanity and blocked-term lists by language, including transliterated variants** —
  this is the same corpus as the §5.3 TTS safety work, and it must be one list, not two
- Canned moderation responses in the creator's preferred language
- Language-aware rate limits, emoji flooding, repeated-text detection and link controls

Optional AI layer, on explicit quotas from the §11 credit model:

- Translate a selected message for the creator or a moderator
- Summarise fast chat in the creator's language
- Suggest a polite multilingual reply
- Classify likely spam, harassment or scam attempts
- Translate a creator's announcement into chosen community languages

**AI recommends or soft-actions. It does not ban.** Permanent bans, any payment
decision and any public reply need explicit creator or moderator policy — this is
§11.8 applied to chat. Every AI action records the original text, the action, the
reason, the confidence, the policy version, and an appeal and reversal path.

The bot's UI language set follows the Companion waves in §5.6.2. It does not get its
own, and it does not ship ahead of them.

### 36.5 The first release is deliberately small

1. Connected YouTube chat, once provider access exists
2. Native commands, aliases, cooldowns, role permissions, scheduled messages
3. English / Hindi / Hinglish localisation
4. Deterministic spam and link controls
5. The import wizard, for simple commands only
6. **One** event action: command → BharatStudio overlay or Companion action

Everything else — advanced automations, multi-platform chat unification, AI moderation,
third-party bot bridges — comes later. A creator with six working commands in Hinglish
is better served than one facing an empty automation canvas.

### 36.6 Rate limits are a design input, not an afterthought

Writing to YouTube chat costs quota and is rate-limited, and the product must be
designed around that rather than discovering it in production: announcements are
rate-limited and coalesced by us (§27 already specifies this for relays), a command
storm produces one reply and not two hundred, and the bot degrades to silence with a
creator-visible notice rather than queueing a backlog it will dump minutes later. The
measured ceiling replaces every assumed number before this ships.

### 36.7 Tier placement

| Tier | Bot |
|---|---|
| **Free** | Commands, aliases, cooldowns, role permissions — a real working bot, with the §30.6 attribution unchanged |
| **Pro** | Scheduled messages, more commands, deterministic moderation controls |
| **Creator** | Import wizard · overlay and Companion actions from commands · multilingual alias sets · outbound announcements |
| **Studio** | Multi-channel, moderator roles and approval, team-managed command libraries |

Moderation **correctness** — blocked terms, link filtering, the safety corpus — is not
tiered. It sits with §30.1 for the same reason TTS safety does: a Free creator's chat
is not a less safe place.

### 36.8 What blocks it

- **YouTube chat write needs the Google chat-write scope**, which is unfiled (§32,
  `CON-08`). Without it there is no bot on the only platform we support.
- **YouTube ingestion is excluded from v1** by the launch authority (§1.9). The bot is
  therefore **P2 at the earliest**, and cannot be marketed before it exists.
- The safety corpus it depends on is the §12.2 work, which is P0 and unbuilt.

Nothing in Phases 0 to 2 depends on the bot, and it may not be used as a reason to
start YouTube work early.

---

## 37. Testing, evidence and performance gates

Added 2026-09-14. **This section is binding on every register row in §31.** A row
without the evidence named here is not done, whatever its code looks like.

### 37.0 Why this section exists

496 + 324 + 97 passing tests coexist with a product where a creator cannot connect
YouTube, cannot start hype mode, cannot send a sticker, and whose entire supporter
history returns empty on every read (§2). Every one of those tests passed because it
seeded its own data and called the function directly. **The suite was measuring the
code, not the product.**

So the rule that governs everything below: **a test that constructs the state it
verifies proves the function works. Only a test that traverses the path a person takes
proves the product works.** Both are needed. Only the second one closes a row.

### 37.1 The ladder — what each level proves, and what it cannot

| Level | Proves | Cannot prove | Blocks |
|---|---|---|---|
| **Unit** | A function's logic and its edge cases | That anything calls it | Merge |
| **Contract** | Request and response shapes match the OpenAPI spec both ways | That the endpoint is reachable from a UI | Merge |
| **Integration** | Two real components agree — API and a real Postgres, worker and a real queue | That a human can trigger the sequence | Merge |
| **Reachability** | An exported client function has a caller · a SQL function granted to the app role has an application caller · a declared React handler prop is actually passed | Correct behaviour | Merge (this is F22, and it is the check that would have caught §2) |
| **E2E** | A person completes the journey in a real browser or on a real device | Behaviour under load | Release |
| **Load** | The system holds at the target concurrency | Behaviour over hours | Release |
| **Soak** | No leak, no drift, no unbounded growth over a full stream | Behaviour when a dependency fails | Release |
| **Chaos** | Correct degradation when something breaks | Anything about real providers | Release |
| **External evidence** | The provider, the CA, the store or counsel said so, in writing, on a date | — | Release, and only this closes an evidence row |

### 37.2 Definition of done, per register row

§31.0 already requires ten fields before a row is schedulable. A row is **done** when
all of the following exist and are linked from its entry in `active/`:

1. **Use cases** — the named journeys this row serves, in the creator's or supporter's
   words, including the unhappy ones.
2. **Unit and contract tests** for the logic and the shapes.
3. **A reachability assertion** — the specific thing a human clicks, and the test that
   fails if the wiring is removed.
4. **At least one E2E scenario** from §37.3, run in a real browser or on a real device.
5. **Failure-path coverage** — what the creator and the supporter see when it breaks,
   tested, not described.
6. **A performance number** where the row sits on a budgeted path (§37.4), measured on
   the reference environment.
7. **Evidence artefacts** stored per §37.8, dated, with the commit they were produced
   from.
8. **Rollback proof** — the row was turned off, and the product behaved as the row's
   kill-switch field says it should.

A row that cannot state its use cases is not ready to build. A row that cannot state
its failure behaviour is not ready to ship.

### 37.3 End-to-end suites, by surface

Each scenario below is a named test. "Real" means a real browser (Chromium, and inside
OBS where the surface is an overlay), a real device for mobile, a real Postgres, and
provider sandboxes where a provider is involved.

#### 37.3.1 Payments and alerts — the path that must never break

| # | Scenario | Passes when |
|---|---|---|
| PAY-E1 | Anonymous supporter opens the tip page, pays ₹100 by UPI in the Razorpay sandbox | Payment recorded · receipt reachable at its token URL · alert visible on the overlay · Companion shows the tip |
| PAY-E2 | The same webhook is delivered three times | Exactly one payment, one alert, one receipt |
| PAY-E3 | Webhook arrives with an invalid HMAC | Rejected, logged, no payment, no alert |
| PAY-E4 | The worker is down when the payment commits | Payment safe, alert delivered after the worker returns, no provider retry caused by us |
| PAY-E5 | A refund is processed | Every derived view — goal, leaderboard, badges, supporter history — reflects it on the next read, with no counter to correct |
| PAY-E6 | 200 tips to one channel in 60 seconds | Every one recorded · none dropped · alerts coalesce per the approved rule · no alert lost to a display limit |
| PAY-E7 | Supporter pays, closes the tab immediately | Receipt still reachable, alert still fires |
| PAY-E8 | `viewer_identity_id` is written on capture (F01) | Supporter history is non-empty for a real payment made through the UI — the exact failure in §2 |

#### 37.3.2 Overlay and Master Canvas

| # | Scenario | Passes when |
|---|---|---|
| OVL-E1 | Overlay loads in OBS as a browser source and stays connected for 8 hours | Flat memory, flat node count, no frame over 16ms during alerts |
| OVL-E2 | Overlay idles for 10 minutes with no events | **Zero database queries** for that session (RT-01) |
| OVL-E3 | A tip lands on Channel A while Channel B is also live on the same instance | Only Channel A's sessions wake; Channel B issues no query (RT-02) |
| OVL-E4 | Network drops for 90 seconds mid-stream | Reconnect, cursor replay, no duplicate alert, no lost alert, consistent within 2 seconds |
| OVL-E5 | Reconnect after a 1-hour gap | Burst coalesced into a summary plus a bounded catch-up, not an hour of alerts fired at once |
| OVL-E6 | TTS provider returns 500 for every request | Visual alert appears on time; a chime or silence follows; nothing delayed (RT-03) |
| OVL-E7 | TTS returns after the alert's display window closed | Audio dropped, never played over the following alert |
| OVL-E8 | A single module throws on render | Canvas keeps rendering, module shows its error state, second failure keeps it down for the session, **watermark still visible** (WMK-01) |
| OVL-E9 | Free-tier overlay | Exactly one watermark, in the reserved corner, above every module; the editor refuses to place a module over it |
| OVL-E10 | Paid-tier overlay | Zero BharatStudio branding anywhere in the rendered output |
| OVL-E11 | Subscription lapses to paused mid-stream | No visual change on stream; on the next clean reload, the Free fallback renders (WMK-06) |
| OVL-E12 | Twelve widgets as separate sources versus one Canvas | The published benchmark reproduces, on the reference machine (PRF-16) |

#### 37.3.3 Tip page and Live Support Hub

| # | Scenario | Passes when |
|---|---|---|
| HUB-E1 | Cold load on a throttled 3G profile | First contentful paint under 3s, payment form usable before any optional module loads |
| HUB-E2 | JavaScript disabled | QR and payment link still work |
| HUB-E3 | Player, reactions, wall and stickers all enabled | None of them loads before first paint (§12.7) |
| HUB-E4 | Supporter sends a message containing a phone number and a UPI ID | PII detected, not spoken, not displayed per policy, payment unaffected |
| HUB-E5 | Supporter with a screen reader completes a tip | Every control labelled, focus order correct, no keyboard trap |

#### 37.3.4 Dashboard

| # | Scenario | Passes when |
|---|---|---|
| DSH-E1 | Creator with 50,000 payments opens the dashboard | Summary renders within budget; no query returns more than its page; nothing unbounded is fetched (§12.7) |
| DSH-E2 | Search across that history | Cursor-paginated, debounced, indexed — `EXPLAIN ANALYZE` proof attached (RT-12) |
| DSH-E3 | Export of the full history | Runs as a background job, completes, downloads, and never renders rows into the page (PRF-18) |
| DSH-E4 | Free-tier creator does all of the above | Identical result — no cap, no date limit, no charge (§12.6) |
| DSH-E5 | Connector revoked upstream | The creator is told, with a reconnect action that works (CON-03) |
| DSH-E6 | A moderator hides a message, then the creator opens the Activity Log | The action appears with actor, target, reason and timestamp, and the affected object is reachable from it |
| DSH-E7 | An operator opens the Activity Log | Operational entries visible, financial amounts absent — verified against the projection, not the rendered page |
| DSH-E8 | A platform admin fires `global_kill` on a capability this channel uses | It appears in the creator's Activity Log, and the §20.6.1 notice was sent the same hour |
| DSH-E9 | A tip arrives but no alert appears | "Why didn't this fire?" names the failing hop, and Companion gives the same answer |
| DSH-E10 | A goal total looks wrong after a refund | "Why this number?" shows the computation and the rows, and the refund is among them |
| DSH-E11 | Every screen with no data yet | Each renders an authored empty state naming what would fill it — no blank panels, no bare spinners |
| DSH-E12 | A Free creator opens an Activity Log with 50,000 entries | Full history, searchable, exportable, no cap, no charge (§12.6) |

#### 37.3.5 Companion

| # | Scenario | Passes when |
|---|---|---|
| CMP-E1 | Sign in → pair → guided Prepare Stream → first test alert | Completes on a real mid-range Android and a real iPhone; the test alert appears on the overlay |
| CMP-E2 | Every Live Deck control | Each one performs a server-side action — the §2 failure was controls that render and do nothing |
| CMP-E3 | Clutch Mode on a Free account | Works; TTS muted, QR hidden, financial events retained and shown afterwards |
| CMP-E4 | Airplane mode, three actions, then reconnect | Each action reconciles with an explicit result; irreversible and financial actions were refused rather than queued |
| CMP-E5 | Notification permission denied | App fully usable, state re-derived on foreground, settings deep link works |
| CMP-E6 | Device language set to Hindi | Every string localised, no key rendered, rupee grouped 2,2,3, layout intact at +40% expansion |
| CMP-E7 | Session expires while the Live Deck is open | Re-auth sheet returns to the same screen; no silent logout |
| CMP-E8 | Search the store build for a price or purchase CTA | None found, on either platform (CMP-38) |

#### 37.3.6 Interop and packages

| # | Scenario | Passes when |
|---|---|---|
| INT-E1 | Import a package containing a `<script>`, an external font URL and a remote image | All three rejected by the validator with a specific reason (INT-19) |
| INT-E2 | Import a valid signed package | Renders identically to its preview; runtime version pin honoured |
| INT-E3 | Tamper with a signed package's bytes | Rejected at import and again at render |
| INT-E4 | Import a 4K PNG and a 40MB WAV | Transcoded and pre-scaled server-side; the browser never resizes |
| INT-E5 | Migration wizard on a real OBS scene collection | Inventory correct, unmapped items named, nothing published without approval, original scene untouched, one-action revert |
| INT-E6 | Streamlabs bridge during a 200-tip burst | BharatStudio alerts all delivered on time; bridge output coalesced below the documented limit; a bridge failure changes nothing upstream (INT-11) |
| INT-E7 | Bridge destination returns 500 for ten minutes | Dead-lettered, destination disabled with a creator-visible notice, no retry storm |

#### 37.3.7 Bot

| # | Scenario | Passes when |
|---|---|---|
| BOT-E1 | `!rules`, `!niyam`, `!niyem` and `!नियम` | All four reach the same command |
| BOT-E2 | 500 chat messages in 10 seconds including 50 command invocations | One reply per cooldown window, rate limits respected, no backlog dumped later (BOT-12) |
| BOT-E3 | Import a command set containing a script | Imported commands land; the script is reported as "cannot import safely", never executed (BOT-09) |
| BOT-E4 | A blocked term in transliterated Hinglish | Caught by the same corpus that catches it in TTS (BOT-06) |
| BOT-E5 | AI classifies a message as harassment | Recommendation surfaced, no automatic ban, full audit record written (BOT-13, BOT-14) |

#### 37.3.8 Lifecycle, entitlement and the control plane

| # | Scenario | Passes when |
|---|---|---|
| LIF-E1 | Subscription lapses through all five states | Nothing deleted · overlay never becomes a payment wall · notices in dashboard and Companion, never on stream |
| LIF-E2 | Renewal after Expired | Configuration restores; only provider credentials need reconnecting |
| LIF-E3 | Downgrade with over-quota assets | Assets read-only, still viewable, still exportable (§12.6.1 rule 4) |
| LIF-E4 | Admin retiers a capability | Takes effect per the resolution order; impact preview matched reality; revert works in one action |
| LIF-E5 | `global_kill` fired | Capability off immediately, log immutable, expires at 24h without ratification, affected creators notified, not billed (§20.6.1) |
| LIF-E6 | Attempt to create a registry row gating a durable record | Rejected by the registry (CTL-14) |

#### 37.3.9 Safety pipeline

| # | Scenario | Passes when |
|---|---|---|
| SAF-E1 | The same slur in Devanagari, Latin transliteration, code-mixed, with repeated characters, with zero-width joiners, and in homoglyphs | All six resolve to one term and one verdict |
| SAF-E2 | A message containing a phone number | Detected, not spoken, handled per policy — **and no cache entry is written** |
| SAF-E3 | A ₹5,000 tip with a borderline message | Payment recorded, receipt issued, alert displayed per policy, TTS decision independent of all three |
| SAF-E4 | The AI layer is unavailable for ten minutes | L0–L3 still run · TTS fails closed · payments unaffected · the creator sees the degraded state and the audience does not |
| SAF-E5 | The AI budget is exhausted mid-stream | Escalation stops, deterministic layers continue, degradation is visible |
| SAF-E6 | A novel slur is caught by L4, reviewed, and promoted | The next message containing it is decided at L1 with no provider call |
| SAF-E7 | The corpus is updated | Every affected cache entry is invalidated by the `policy_version` key change, with no purge step |
| SAF-E8 | A copypasta raid — 500 identical messages in 30 seconds | One classification, 499 cache hits, and the measured cost reflects it |
| SAF-E9 | A Free creator and a Studio creator send identical borderline messages | Identical verdicts, identical layers, identical latency (SAF-17) |
| SAF-E10 | An automated block is appealed | The appeal path works, the reversal is audited, and both appear in the Activity Log |
| SAF-E11 | The §12.8 story, run end to end | Every one of its eleven steps happens as written, on a Free account |
| SAF-E12 | A term is added to the corpus | `policy_version` bumps, affected cache entries stop matching, and the reviewer is recorded |
| SAF-E13 | A near-miss one character from a banned term | Logged as a candidate, not blocked |
| SAF-E14 | A creator asks why a supporter was timed out three weeks ago | The evidence snapshot answers it in full, after raw chat for that day has expired |

#### 37.3.10 QR and UPI

| # | Scenario | Passes when |
|---|---|---|
| QR-E1 | Scan the overlay QR from three phones at once, mid-stream, then reload the overlay | All three reach the tip page; the QR is unchanged; no order is bound to it |
| QR-E2 | Desktop checkout, Order QR scanned after its expiry | An honest expired state with one regeneration, not a silent swap |
| QR-E3 | Mobile web, UPI Intent, pay, return | Confirmation screen reached; the **webhook**, not the return, marks it verified |
| QR-E4 | Mobile web, UPI Intent, pay, **do not return** — kill the browser | The payment still completes; the receipt link resolves later with correct status |
| QR-E5 | Across the device lab: Android and iOS, several UPI apps | The return path works or degrades to a truthful waiting state on every one |
| QR-E6 | JavaScript disabled entirely | Link and QR still work; a payment completes end to end |
| QR-E7 | Creator rotates the channel short link | Confirmation names the printed-material consequence; old Channel QRs stop resolving; the action is in the Activity Log |
| QR-E8 | Campaign QR with a suggested amount | The page pre-fills it and the supporter can change it |
| QR-E9 | A supporter's UPI ID appears in a message | Treated as PII (`SAF-12`) — never spoken, never cached |
| QR-E10 | Funnel data after 100 attempts | Path, outcome and timing recorded; **no VPA, account identifier or banking data anywhere in it** |

#### 37.3.11 Goal lifecycle

| # | Scenario | Passes when |
|---|---|---|
| GOA-E1 | A tip completes a goal, then is refunded, then another tip arrives | The celebration fired **once**; the refund is recorded and visible; the second tip does not re-fire it |
| GOA-E2 | A goal completes while Clutch Mode is active | Nothing loud or full-screen plays; the deferred actions are shown to the creator afterwards, not dropped |
| GOA-E3 | A goal completes while an alert is playing | The celebration queues behind it and never interrupts |
| GOA-E4 | Auto-create next goal with overflow roll-in | The next goal exists with the correct target and starting amount, and the overflow is recorded once |
| GOA-E5 | A sequence with delays is previewed | The whole composition plays on the overlay in a marked test mode and auto-reverts |
| GOA-E6 | An outbound action is configured | It is **prepared**, not sent, until the creator releases it |
| GOA-E7 | A generated announcement contains a blocked term | The §12.2 pipeline catches it before it is spoken or posted |
| GOA-E8 | Threshold rules at 25/50/75% with "once per stream" | Each fires exactly once, and re-crossing after a refund does not re-fire |
| GOA-E9 | A creator manually reopens a completed goal | Audited with a reason and visible in the Activity Log |
| GOA-E10 | "Why this number?" on a goal total after two refunds | Shows the contributions, both refunds, and the arithmetic |

#### 37.3.12 Refunds

| # | Scenario | Passes when |
|---|---|---|
| REF-E1 | Creator refunds in the Razorpay dashboard | Webhook reconciles, ledger records it, every derived number reflects it on next read, receipt updates, Activity Log shows it |
| REF-E2 | Two partial refunds totalling the payment, then a third attempt | The third is refused; cumulative tracking is correct |
| REF-E3 | Duplicate refund webhooks | One refund row |
| REF-E4 | A refund webhook arrives before its payment webhook | Queued and applied in order, never to an unrecorded payment |
| REF-E5 | A refund lands mid-stream | Nothing changes on stream; Companion shows it; the audience sees nothing |
| REF-E6 | A refunded tip had contributed to a goal and earned a badge | Both recompute with no counter to fix and no badge to revoke |
| REF-E7 | A refund fails at the provider | A visible failed state with its reason, for both creator and supporter — never a silent disappearance |
| REF-E8 | Refund attempted on a Compatibility-Routing signal | Refused loudly, with the reason that a routed signal is not a verified payment |
| REF-E9 | An operator attempts a refund | Refused by projection and RLS, not by a hidden button |
| REF-E10 | An anonymous supporter opens their receipt link after a refund | Live status and expected credit window, no login |

### 37.4 Performance numbers — the table that gets measured

**The reference environment, specified concretely.** A performance number measured
somewhere undefined is not reproducible, so this is fixed and versioned; changing any row
invalidates prior results and is a decision, not a tuning step.

| Dimension | Fixed value |
|---|---|
| **Deployment topology** | Cloud Run at the production configuration, the production concurrency cap, minimum instances as configured for production, one region |
| **Database** | The production instance class, with a seeded dataset of **500 channels · 2,000,000 payments · 5,000,000 alert events · 200,000 supporter identities**, and production index definitions |
| **Load profile** | Defined per profile in §37.5. Channel size is skewed, not uniform: **80% small (under 50 concurrent viewers), 15% mid, 5% large** — a uniform profile hides the thundering-herd behaviour that RT-02 is about |
| **Asset mix per overlay** | 6 active modules · 1 Lottie under the complexity cap · 3 pre-scaled images · 2 sounds under the length cap · 1 web font. This is a realistic canvas, not an empty one |
| **Network** | Overlay and dashboard on 50Mbit wired. Tip page measured on **4G (9Mbit, 170ms RTT)** and **3G (1.6Mbit, 300ms RTT)** profiles. Companion on 4G with 5% loss |
| **Overlay client** | A mid-range Windows PC running the pinned OBS version, plus the same page in headless Chromium for CI trend-tracking. **OBS is the pass/fail environment; headless is a trend signal only** |
| **Mobile client** | A named mid-range Android device and a named iPhone at the supported floors, both on battery, not plugged in |
| **Measurement** | p50/p95/p99 from bucketed histograms (RT-06), aggregated across instances. **Never an average** |
| **Duration** | 30 minutes steady state after a 5-minute warm-up, discarding the warm-up |
| **Pass/fail artefact** | A single JSON document per run: profile ID, environment version, commit SHA, start and end timestamps, every §37.4 row with its measured p50/p95/p99, pass or fail per row, and the raw histogram export attached. A run without this document did not happen |
| **Repeatability** | Three runs. **The worst run is the result**, not the median — the budget is a promise about a bad day |

| Path | p95 | p99 | Hard limit |
|---|---|---|---|
| Webhook acknowledgement after durable commit | 150ms | 300ms | Never waits on dispatch (RT-04) |
| Commit → dispatcher pickup | 500ms | 1.5s | Recovered by the next tick if missed |
| Verified payment → alert painted on overlay | **2.0s** | **3.5s** | Never blocked by TTS (RT-03) |
| TTS phase-two audio arrival after visual | 1.5s | 2.5s | Dropped, not played late |
| API read | 150ms | **200ms** | — |
| Tip-order path | 350ms | **500ms** | — |
| Any query on a live path | 50ms | 100ms | No sequential scan on `payments` (RT-12) |
| Overlay reconnect to consistent state | 1.5s | 2.0s | No duplicate, no loss |
| Bot reply after a command | 1.0s | 1.5s | Within the platform rate limit |
| Companion cold start to interactive | — | **2.0s** | Mid-range Android |
| Companion action round trip, perceived | **300ms** | — | Optimistic with rollback |
| Support Hub first contentful paint | 1.5s on 4G | 3.0s on 3G | JS under 150KB gzipped before the optional player |

| Resource | Limit |
|---|---|
| Idle overlay database queries | **Zero per session per minute** (RT-01) |
| Overlay CPU | < 5% of one core idle · < 15% during an alert · no frame over 16ms |
| Overlay memory | < 150MB steady · **±5% over 8 hours**, no upward trend |
| Overlay DOM nodes | Flat over 8 hours; a ticker recycles rows |
| Database CPU at target load | < 40%, leaving headroom for a burst |
| Database connections | Within the documented budget, the overlay listener's direct connection counted |
| Companion crash-free sessions | > 99.5% per release, gating the staged rollout |
| Layout shift on the tip page | CLS < 0.1 |

### 37.5 Load, soak and chaos profiles

| Profile | Shape | Must hold |
|---|---|---|
| **Target concurrency** | 2,000 concurrent live overlay sessions across ≥200 channels, 30 minutes | Every number in §37.4; database CPU under 40%; zero idle queries |
| **Raid burst** | 200 tips to one channel in 60 seconds, other channels idle | No drop, no cross-channel wake, alerts coalesce per rule, other channels unaffected |
| **Steady mixed** | 50 tips/second across all channels, 10 minutes | Queue depth returns to zero; no dead-letter growth |
| **8-hour OBS soak** | One overlay in OBS, periodic alerts, 8 hours | Flat memory and node count; no reconnect storm; watermark still rendered at hour 8 |
| **24-hour backend soak** | Continuous low traffic | No connection leak, no unbounded table, no metric drift |
| **Chaos: TTS down** | Provider returns 500 for 10 minutes | Visual alerts unaffected; audio degrades to chime then silence |
| **Chaos: dispatcher down** | Dispatcher stopped for 5 minutes | Payments still committed and acknowledged; backlog drains on restart with no duplicates |
| **Chaos: `LISTEN/NOTIFY` down** | Direct listener killed | Cursor replay keeps the overlay correct; latency degrades visibly, correctness does not |
| **Chaos: database failover** | Primary fails over | No accepted payment lost; alerts resume; the creator is told what degraded |
| **Chaos: Cloud Tasks throttled** | Dispatch rate limited | Alerts arrive late, never lost, never duplicated |
| **Chaos: duplicate webhook storm** | The same event 100 times | One payment, one alert, one receipt |

### 37.6 Security, privacy and tenant isolation

| Suite | Must prove |
|---|---|
| **Tenant isolation** | No query, view, cache, export, asset URL, metric label or log line can return one channel's data under another channel's context. **This suite gates the Multi-Channel Pack** (§28.3.3) and every cross-channel feature |
| **Role boundaries** | Operator and moderator cannot read financial amounts; viewer sees delivery metadata only; enforced by projections and RLS, not by hiding UI |
| **Payment-secret handling** | No provider secret in a log, metric, trace, error message or crash report; KMS envelope paths have no human read route |
| **PII in telemetry** | No trace, event, order, payment, account, donor, queue or user ID in a Prometheus label; crash reports scrubbed of amounts, identity and message content |
| **Notification payloads** | No tip amount, donor identity or message content in any push payload (CMP-32) |
| **Asset serving** | Signed short-lived URLs only; no public bucket path; no cross-channel asset reachable |
| **Package validator** | The INT-E1/E3 cases, plus a fuzz corpus of malformed and adversarial packages |
| **Overlay token** | Fragment-only, never logged, revocable, short-lived (SEC-01) |
| **Durable-record access** | A Free account can reach, search and export everything a Studio account can (§12.6) — tested, not assumed |

### 37.7 Accessibility and localisation

| Suite | Must prove |
|---|---|
| **Contrast and focus** | 4.5:1 on body text, visible focus on every interactive element, on web and mobile |
| **Screen reader** | Tip page and Companion completable end to end, every icon-only control labelled, in the selected language |
| **Dynamic Type** | Largest accessibility sizes with no truncated control label and no target below 44pt/48dp |
| **Reduced motion** | Honoured everywhere; no state communicated only by animation |
| **Colour independence** | All six health signals distinguishable without colour |
| **Pseudo-locale** | No hardcoded user-visible string anywhere in Companion (CMP-39) |
| **Expansion** | Every screen intact at +40% text length |
| **Indic rendering** | Devanagari and each shipped script render with correct conjuncts and matras, no clipping, on both platforms |
| **Number and currency** | Indian 2,2,3 grouping everywhere a rupee appears (CMP-41) |

### 37.8 Evidence artefacts — what is produced and where it lives

Every suite above produces an artefact. An artefact without a date and a commit is not
evidence.

| Artefact | Produced by | Stored |
|---|---|---|
| Test run with pass/fail per scenario | CI | Build record, linked from the register row |
| Reachability report | The F22 checks | Build record; a regression fails the merge |
| `EXPLAIN ANALYZE` output per live query | Checked in beside the query | The repository, re-verified when the query changes |
| Histogram export at p50/p95/p99 per budgeted path | Load run | Attached to the release record |
| Soak trace: memory, node count, connection count over 8 hours | Soak run | Attached to the release record |
| Chaos run log: what was broken, what degraded, what held | Chaos run | Attached to the release record |
| Benchmark: one Canvas versus twelve sources | Benchmark run | Published, and re-run in CI (PRF-16) |
| Rollback proof | Manual, once per row | The register row |
| Provider, CA, counsel and store evidence | The external party | `05_SUPPORT_AND_EXTERNAL_EVIDENCE_REGISTER.md` — **and nothing else may be recorded there** |

### 37.9 What blocks a merge, and what blocks a release

**Merge-blocking:** unit · contract · integration · reachability (F22) · lint and type
checks · the CI performance budgets that can be measured in CI · the pseudo-locale and
hardcoded-string checks · the no-purchase-surface check (CMP-38) · the registry
rejection checks (CTL-14, CTL-15).

**Release-blocking:** every E2E suite in §37.3 for the surfaces in the release · the
load, soak and chaos profiles in §37.5 · the security and isolation suites in §37.6 ·
the accessibility and localisation suites in §37.7 · the §37.4 numbers measured on the
reference environment · and every applicable external evidence row.

**A conditional exception to any release gate needs an owner, an expiry and a
rollback** — the same rule the master release authority already applies.

### 37.10 What is never evidence

- A passing local suite, of any size.
- A test that seeds its own data, for any claim about reachability.
- The local SQL harness (20 synthetic tips, concurrency 5, p95 31ms). It runs no HTTP,
  no Razorpay, no Cloud Tasks, no real SSE, no Cloud Run, no OBS and no sized database.
- A JSDOM test, for any claim about a browser, OBS, or a device.
- An average, for any p95 or p99 claim.
- A review of this document, or any section of it.
- A staging run we performed ourselves, for any row that requires a provider, counsel,
  a CA or a store to say something.

### 37.11 Which suites apply to which register area

| Register area | Required beyond unit and contract |
|---|---|
| PAY, VID, ALQ | PAY-E1..E8 · raid burst · duplicate-webhook chaos · dispatcher-down chaos · isolation suite |
| ENG, PRF, RT, WMK | OVL-E1..E12 · target concurrency · 8-hour soak · benchmark |
| HUB | HUB-E1..E5 · 3G profile · accessibility suite |
| DSH, ADM, CTL | DSH-E1..E5 · LIF-E4..E6 · isolation and role-boundary suites |
| CMP | CMP-E1..E8 on both platforms · localisation suite · crash-free gate |
| TTS | OVL-E6, OVL-E7 · TTS-down chaos · safety corpus tests on both routes |
| INT | INT-E1..E7 · package fuzz corpus |
| BOT | BOT-E1..E5 · rate-limit compliance · shared-corpus test with TTS |
| LIF, PCK | LIF-E1..E3 · DSH-E4 · durable-record access suite |
| REF | REF-E1..E10 · duplicate-webhook and dispatcher-down chaos · isolation |
| QR, PAY | QR-E1..E10 · device-lab coverage · degraded-JS path |
| GOA, RUL | GOA-E1..E10 · OVL suites for the celebration path · §12.2 corpus test on generated text |
| STO, MED | INT-E4 · asset-serving suite · one rehearsed takedown drill (§18.3) |
| CUS (gating model) | DSH-E1..E5 · role-boundary suite |
| CST (customisation depth) | OVL-E1..E12 · HUB-E1..E5 · accessibility and localisation suites · +40% expansion |
| SAF, REP | SAF-E1..E14 · REP guardrail tests · the shared-corpus test with TTS and the bot · cost-per-thousand-messages measured, not asserted |
| DSH | DSH-E1..E12 · isolation and role-boundary suites |
| SOC, RTE, Enterprise | Not scheduled — phase R or blocked. No suite required until a gate closes |
