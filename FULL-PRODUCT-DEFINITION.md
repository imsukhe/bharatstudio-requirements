# BharatStudio — Full Product Definition

**Version 1.0 · 2026-09-13 · supersedes master plan Part 7 as the authority on state**

This is the whole product in one file: what exists, what is broken, what is missing,
what we are building, and what we deliberately will not build. Nothing is deferred out
of this document. Items that cannot be built today appear in §16 with the exact
condition that unblocks them, not as silent omissions.

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
2. **Everything agrees on what happened.** UPI tips, YouTube events, overlay state and
   moderation decisions reconcile to one truth.
3. **Failure is legible and partial.** If YouTube chat dies, tips and overlay keep
   working, and the creator is told exactly which part failed.

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
| F06 | YouTube connect / disconnect / reconnect UI | Makes an entire built subsystem reachable |
| F07 | Set `status='revoked'` on `invalid_grant` + surface it | Stops silent permanent failure |
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

---

## 6. Master Canvas and the module catalogue

One browser source replaces the pile. Streamlabs' own pattern — alerts, chat, ticker,
media, custom widgets and themes each added as a separate browser source — is exactly
the clutter we remove.

**Every module below is a module of the one canvas, never a new OBS source, and never
a parallel state system.** Goals, votes, leaderboards, hype, challenges and stickers
are extended through these modules rather than duplicated.

| # | Module | Notes |
|---|---|---|
| 1 | **Support Theater** | Current verified alert, queue state, moderator decision |
| 2 | **Community Goal Ladder** | Milestone tiers and progress |
| 3 | **Tug-of-War Vote** | Two-sided transparent result bar |
| 4 | **Boss Fight** | A visual skin over an ordinary support goal — not a new mechanic |
| 5 | **Reaction Cloud** | Sampled and rate-limited, non-identifying |
| 6 | **Safe Soundboard Alert** | Approved clips only, with cooldown and queue |
| 7 | **Supporter Ticker** | Latest supporter, goal, creator-selected copy |
| 8 | **Challenge Board** | Current / next / completed, with no false refund promise |
| 9 | **Stream Mission Card** | Creator-defined objective and timer |
| 10 | **QR Smart Card** | Visibility tied to scene, gameplay safe zones, or Clutch Mode |
| 11 | **Sponsor Card** | Scheduled placement with an exposure event log |
| 12 | **Moderator Status Card** | "Messages held", "safe mode on" — never private content |
| 13 | **Milestone Celebration** | One reusable animation fired by verified state transitions |
| 14 | **Vertical Stream Layout** | Narrow chat, compact goal, QR, reactions for mobile scenes |
| 15 | **Stream Health Widget** | Creator-only view of YouTube, payment, alert and OBS health |
| 16 | **Lobby Status** | Aggregate seats and queue only (§16) |
| 17 | **Giveaway / Tournament Card** | Entry state, draw status, bracket (§17) |
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

---

## 10. Monetization

### 10.1 The revenue model, stated plainly

BharatStudio takes **0% of tips**. That promise is the positioning and must not be
diluted. Revenue comes from three clean lines that never touch a creator's tip:

1. **Subscription tiers** — Free / Pro ₹199 / Creator ₹399 / Studio ₹499
2. **Top-ups** — the creator buys capacity from us; we are the merchant of record
3. **AI credits** — metered feature value (§11)

**There is no commission anywhere, and no provider pricing is ever shown.** A top-up
is not someone else's money passing through and it is not a percentage of anything.
The creator buys a **bundle of BharatStudio units at a flat price**:

```text
₹99  →  X characters of BharatStudio AI voice
₹99  →  Y BharatStudio AI tokens
```

That is the entire customer-facing model. The creator never sees a provider name, a
provider price, a per-token rate, or a "BharatStudio fee". They see a rupee price and
a quantity of our units.

**Internally** we compute the bundle so that a margin of **25% or more** is retained
before the remainder is issued as units. The margin is a private input to the
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

| Top-up | Unit | Notes |
|---|---|---|
| **TTS characters** | packs of characters | The obvious first one — quota already metered (`0081`), so the ledger half exists |
| **AI credits** | micro / standard / premium (§11) | Largest long-run margin |
| **Asset storage** | GB | Needs the storage quota that is currently absent |
| **Event retention** | +30 / +90 / +365 days | Retention windows already exist per tier |
| **Extra connectors** | +1 platform | Entitlement counts already enforced (`0086:118`) |
| **Extra moderator seats** | +1 seat | Enforced by `0104`; needs the management UI (F18) |
| **Extra sticker/media pack slots** | +N | Tier quotas 10/25/50 already implemented |
| **Priority alert-queue capacity** | burst allowance | For tournament and raid days |
| **Sponsor campaign slots** | +N concurrent | Once the sponsor manager ships |
| **Season Pass issuance** | per pass sold, or bundled | See 10.4 |
| **Vertical/multi-canvas outputs** | +1 output | For creators streaming to two aspect ratios |

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

### 10.5 Private custom room / match password delivery

Large in India — BGMI, Free Fire, Valorant, GTA RP creators run daily custom matches.

A viewer who sends a qualifying tip (e.g. ₹50) receives the **room ID and password on
their post-payment receipt screen**. It replaces the creator typing passwords into
Instagram DMs and Discord.

Needs: creator sets the qualifying amount and the secret per session · secret is
revealed only after verified capture · rotation and revoke · rate limiting and
an abuse guard · secret never in a URL, never in an alert, never in a log.

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
| Studio | Shared team pool, producer/moderator roles, advanced vision, sponsor workflow, priority jobs | Pooled credits, cost controls, audit exports |

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
- Never store banking credentials, even for a "preferred UPI app" preference
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

### 12.2 Content and TTS safety

Current state: `provider.ts:28-29` strips C0/DEL control characters and bounds to 500
chars. That is the entire filter. Required before public launch:

- Profanity and slur filtering, Hinglish and Romanized Indic included
- URL removal or neutralisation
- Unicode normalisation, RTL-override and zero-width stripping
- Repeated-character suppression
- SSML-injection guard
- Blocked terms and blocked users, creator-configurable
- Minimum amount for TTS
- Moderator approval before TTS as a distinct decision from alert display
- PII detection (phone, UPI ID, email, address, card-like strings)

### 12.3 Privacy and viewer rights

- **Tipping must never require login, at any level, ever.** If a viewer-account outage
  ever blocks anonymous tipping, that is a P0
- Never claim history from a typed display name — only from OAuth-verified platform
  identity
- A creator must never see cross-creator viewer spend
- Public viewer profiles are opt-in and off by default; exact lifetime spend is
  private by default and never published
- Deleting a viewer account removes profile and linkage but preserves the immutable
  payment and audit record
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
- Gateway-fee rule: state our 0% clearly, state the provider sets its own fees, show
  provider fees on both sides of any calculator, never advertise "0% forever" as a
  property of the payment rail
- No competitor names in rendered HTML
- One brand, one domain (`bharatstudio.in`), four product areas differentiated by a
  per-route accent token — Alerts gold, Stream broadcast red-magenta, Mirror cool
  cyan/steel, Companion inheriting Alerts gold while bundled. Everything else
  (typeface, spacing, card-bezel system, nav, footer, legal) is shared: four accents
  off one system reads as a family, four design languages reads as four weak brands
- Do not buy separate domains; 301 any defensive domains into sections

---

## 13. Portability — "I can leave with my data"

A stated switching reason (§1.8), so it is a feature with an owner, not a compliance
afterthought.

- Export layouts, scene profiles and Master Canvas configuration
- Export events, receipts and the payment ledger (CSV and Sheets)
- Export supporter relationships subject to viewer consent
- Export moderation audit and sponsor exposure logs
- One-click rollback of the OBS migration (restore hidden sources)
- Downgrade never deletes accepted payments, refunds or audit history — it only
  narrows the dashboard search window
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
| **Desktop Companion** | `companion-desktop` | Not a product surface. May persist as a local OBS mechanism only. |
| **Platform** | `bharatstudio-platform` | Out of scope. Cross-product identity and store entitlements. |

The Companion catalogue's `mirror_*` (3) and `stream_*` (2) actions stay in the enum
and stay permanently inactive — `0093` already hard-codes their activation false
because those products emit no liveness signal. That is now the correct end state, not
a gap.

The **`is_platform_admin`** concept and the admin console remain in scope: they are
BharatStudio staff operations for Alerts, unrelated to the Platform service.

One naming item survives the cut: **"Companion" collides with Bitfocus Companion**, an
established Stream Deck / OBS controller. Since Companion now ships only as a mobile
app under our own brand, this is a store-listing and SEO concern rather than a
blocker — but it should be settled before the first App Store or Play submission.

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
- Preset bundles ("Gaming night", "Charity goal", "Podcast", "Tournament") are one-tap
  starting points, then fully editable — presets must never be a separate,
  less-configurable path.

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

The paid tip-for-room-code idea from §10.5 survives only in its narrow form — a
creator-set qualifying tip that returns a code on the receipt — and even there the
lobby's own eligibility policy governs seats. The two must not be conflated.

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

---

## 19. Architecture — stack, storage, flows and performance

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
        → store bytes in GCS at a content-addressed key (sha256)
        → Postgres row: id, channel, kind, sha256, bytes, duration,
                        moderation state, rights attestation, audit
        → serve via CDN with a short-lived signed URL
```

Content addressing gives free deduplication — the same meme sound uploaded by 500
creators is stored once. Postgres keeps metadata, moderation state and the rights
attestation; it never keeps the bytes.

Migration: keep existing Lottie `bytea` rows working, write all *new* media to GCS,
backfill opportunistically. Do not block on the backfill.

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

These go in CI as budgets that fail the build, not in a document as aspirations.

### 19.5 Overlay — the architecture that keeps it cheap

**One source, one connection, one loop.** The Master Canvas already collapses N browser
sources into one; the win is only real if it also collapses N connections and N render
loops. One SSE connection, one `requestAnimationFrame` scheduler, modules as pure
render functions driven by a single state store.

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
- SSE fan-out is per-overlay, not per-widget. Adding a widget must not add a connection.
- Every list endpoint is cursor-paginated with a bounded page size — no offset
  pagination, no unbounded reads. Several are already capped at 100; make it universal.
- Index every query behind a widget. A widget read that sequential-scans `payments` is a
  production incident waiting for a popular creator.
- Rate-limit and debounce at the edge: reactions, votes and chat commands are shaped
  before they reach application logic.
- Keep the alert path's atomic transaction narrow. It is correct today; new features
  must not be added inside that transaction.

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
- Two-person approval for `global_kill` and for moving a paid capability into Free.
- A capability can be reverted to its previous version in one action.
- All of it is behind platform-admin auth with MFA (ADM-07) — this panel is now a much
  higher-value target than a DLQ viewer.

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

v1 ships a **contribution selector**: *Support Creator A · Support Creator B · Support
the shared goal* — where the shared goal is a visual target and money settles to one
declared beneficiary.

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

### 23.3 Overlay URLs are bearer credentials

The competitor review's sharpest lesson. Our current design is already good — token in
the URL fragment, only a SHA-256 hash stored, per-overlay lookup, rotate and revoke —
but it is missing expiry.

Required: **short-lived signed capabilities** with explicit renewal, session and device
binding where practical, scheduled rotation, immediate revocation, and a standing rule
that overlay URLs never appear in screenshots, support tickets, logs or error messages.
A creator screenshotting their OBS setup for a support request must not hand over a
permanent credential.

### 23.4 Other things worth taking from the benchmark

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

## 25. Tier matrix

**This is the seed for the capability registry (§20), not a hard-coded ladder.** Once
the control plane exists, staff move any row at any time. What matters is that the
initial division is principled rather than arbitrary.

The principle, one line per tier:

| Tier | What it is |
|---|---|
| **Free** | Everything correctness-critical, plus a real working alert. Never crippled, always watermarked |
| **Pro ₹199** | Personality — voice, sounds, look, more alerts on screen |
| **Creator ₹399** | Community mechanics — goals, votes, lobbies, co-streams, connectors |
| **Studio ₹499/₹599** | Team and events — seats, approval, tournaments, pooled AI, priority |
| **Enterprise** | Governance-blocked (§24) |

### 25.1 Correctness — identical on every tier, forever

Payment verification · immutable records · webhook dedup · reconciliation · refund
tracking · queue durability and no-drop · retry and replay · security · privacy · audit
· accessibility · downgrade preservation · legal disclosures · receipts · anonymous
tipping with no login.

### 25.2 The existing ladder (already enforced in code)

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
| Control sessions | 1 | 1 | 2 | 4 |
| Read-only sessions | 2 | 3 | 5 | 8 |
| Event bindings | 3 | 5 | 10 | 20 |
| Saved presets | 1 | 2 | 4 | 8 |
| Pending visuals | 20 | 50 | 150 | 500 |
| Watermark | yes | — | — | — |
| Lottie / branding upload | — | — | — | yes |

**Queue count is disputed** — 1/2/3/5 in one source, 1/3/5/10 in another (open
decision 2). The table above uses the conservative reading.

### 25.3 Proposed placement for everything new

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
| Co-Stream Room (2 creators) | — | — | yes | yes |
| Squad grid (3–4 creators) | — | — | — | yes |
| Giveaways (free entry) | — | yes | yes | yes |
| Giveaways (weighted, scheduled) | — | — | yes | yes |
| Tournaments and brackets | — | — | — | yes |
| **AI credits** | trial | monthly | larger monthly | pooled team |
| AI moderation (live) | — | — | yes | yes |
| Thumbnail / Channel DNA | — | — | yes | yes |
| **Ops** | | | | |
| Sponsor manager + exposure log | — | — | — | yes |
| Finance exports (Sheets, Tally) | — | — | yes | yes |
| Post-stream analytics | basic | yes | yes | yes |
| Priority support | — | — | — | yes |

### 25.4 Rules that keep the matrix honest

- **Nothing correctness-related ever moves up a tier.** §25.1 is immutable.
- **Free must be genuinely usable**, not a demo. A Free creator takes real money, gets
  a real alert, real TTS via browser voice, and a real receipt. The watermark is the
  price.
- Every locked row is **visible with its unlocking tier** (§15.3), never hidden.
- A capability moved down a tier takes effect immediately; **moved up, it grandfathers
  existing users** rather than breaking them — matching the existing moderator-seat
  behaviour.
- Any change to this matrix that affects a published marketing claim requires the
  marketing snapshot to rebuild (§20.4) before it is announced.

---

## 26. Master task register — nothing deferred

Status key: **U** usable · **X** unreachable · **P** partial · **A** absent · **B** blocked.
Priority: **P0** launch-blocking · **P1** launch-shaping · **P2** post-launch · **P3** later.

### 26.1 Foundation repairs
See §3 for full detail. F01–F22, all **P0** except F16/F19/F20 (P1) and F22 (P0, cheap).

### 26.2 Payments and money

| ID | Item | State | Pri |
|---|---|---|---|
| PAY-01 | Tip order → checkout → webhook → ledger → alert (atomic) | U | — |
| PAY-02 | HMAC raw-body verification, `x-razorpay-event-id` dedup, case-insensitive | U | — |
| PAY-03 | ₹10 floor + per-channel minimum, enforced at API and DB trigger | U | — |
| PAY-04 | 15-minute intent expiry; Razorpay checkout `timeout: 900` | U | — |
| PAY-05 | Idempotency key contract, 16–128 chars `A-Za-z0-9._:-` | U | — |
| PAY-06 | `alertConsent=false` skips alert/outbox, keeps ledger entry | U | — |
| PAY-07 | Reconciliation policy: paid→recovery item, expired→expire, mismatch→quarantine | U | — |
| PAY-08 | Refunds/disputes as append-only compensating evidence | U | — |
| PAY-09 | `__channel_default__` reserved binding; exact provider binding wins | U | — |
| PAY-10 | Donor-safe status projection (UUID, amount, INR, state, updated) | U | — |
| PAY-11 | Payments ledger + CSV export (explicitly not a CA tax report) | U | — |
| PAY-12 | Provider capability snapshots; features gate on capability, not name | P | P1 |
| PAY-13 | Razorpay partner OAuth | X | P0 |
| PAY-14 | Payment account activation | X | P0 |
| PAY-15 | Reconciliation sweep + refund sweep actually running | X | P0 |
| PAY-16 | Manual-review quarantine resolution UI | X | P0 |
| PAY-17 | Dynamic UPI QR on the tip page (server side exists) | P | P1 |
| PAY-18 | Preferred UPI app memory (browser half) | X | P2 |
| PAY-19 | Direct UPI intent `upi://pay?pa&pn&tr&am&cu` | A | P2 |
| PAY-20 | Payout/settlement status visible to creator | A | P1 |
| PAY-21 | Payment failure classification surfaced to creator | A | P2 |
| PAY-22 | Subscriptions: annual = 10 months charged / 12 served | U | — |
| PAY-23 | Past-due 30-day grace preserves price; rejoin at current pricing | U | — |
| PAY-24 | Downgrade pauses newest queues, never deletes; `paused_reason` distinguishes cause | U | — |
| PAY-25 | Referral credit = service-time (30-day reward, 14-day hold, 5/30-day cap, 12 banked, same-subnet fraud signal) | U | — |
| PAY-26 | Top-up purchase, ledger and balances (§10.2) | A | P1 |
| PAY-27 | Season Passes (§10.4) | A | P1 |
| PAY-28 | Paytm / Cashfree / PhonePe | B | — |
| PAY-29 | Recurring memberships | B | — |

### 26.3 Alerts, queues, overlay

| ID | Item | State | Pri |
|---|---|---|---|
| ALQ-01 | Durable queues, outbox, per-queue deliveries, sequence numbers | U | — |
| ALQ-02 | SSE with `Last-Event-Id`, cursor replay, explicit ack | U | — |
| ALQ-03 | Cross-replica fan-out via LISTEN/NOTIFY | U | — |
| ALQ-04 | Overlay listener needs its own `DATABASE_URL_DIRECT` — pooled LISTEN/NOTIFY is best-effort only, never the correctness path (durable cursor replay is) | P | P0 |
| ALQ-05 | Queue modes FIFO + priority-with-aging (server); stacked/pills/aggregated (presentation only) | U | — |
| ALQ-06 | Quiet hours, rate controls (delay-only, never drop) | U | — |
| ALQ-07 | No-drop guarantee on every tier | U | — |
| ALQ-08 | Multi-queue bindings, immutable per-delivery source/priority snapshot | U | — |
| ALQ-09 | `allow_duplicates` consent required per binding for duplicate delivery | U | — |
| ALQ-10 | Moderation approve/hold/suppress/replay + admin replay/discard, audited | U | — |
| ALQ-11 | Role-scoped financial reads (owner/admin amounts; operator/moderator content; viewer status) | U | — |
| ALQ-12 | Overlay token in fragment only; per-overlay hash lookup; revoke/rotate | U | — |
| ALQ-13 | 9 safe anchors, scale/width, reduced motion | U | — |
| ALQ-14 | Long-message/multiline contract: truncation, continuation, no clipping | U | — |
| ALQ-15 | Per-item skip action | A | P2 |
| ALQ-16 | Reconnect burst coalescing after a long gap | A | P1 |
| ALQ-17 | Time-bounded replay window (the "72-hour buffer" that never existed) | A | P2 |
| ALQ-18 | Master Canvas single browser source with modules (§6) | A | P0 |
| ALQ-19 | Vertical / second-output canvas | A | P2 |

### 26.4 TTS

| ID | Item | State | Pri |
|---|---|---|---|
| TTS-01 | Sarvam synthesis, 13 locales, SHA-256 content cache, 2MB/60s caps | U | — |
| TTS-02 | Quota metering, hard stop, quotas 20K/40K/60K by tier | U | — |
| TTS-03 | Amount-tiered character ladder; `maxCharLimit` shared with Alert Studio (never two limits) | U | — |
| TTS-04 | Chime fallback on provider failure; browser voice on tier/quota | U | — |
| TTS-05 | 1.5s playback cap, never blocks visual display or acknowledgement | U | — |
| TTS-06 | **Content safety suite (§12.2)** | A | **P0** |
| TTS-07 | Quota bar visible from ~70% consumption | A | P1 |
| TTS-08 | Upgrade prompt on exhaustion | A | P1 |
| TTS-09 | Mute / cancel in-flight from dashboard (companion API exists) | P | P1 |
| TTS-10 | TTS character top-ups | A | P1 |

### 26.5 Viewer identity, history, trust

| ID | Item | State | Pri |
|---|---|---|---|
| VID-01 | **`payments.viewer_identity_id` writer** | A | **P0** |
| VID-02 | `creator_supporter_relations` writer | A | **P0** |
| VID-03 | Receipt minting from the confirmation page | X | **P0** |
| VID-04 | Opaque receipt token, SHA-256 fingerprint, reflects live refunds | U | — |
| VID-05 | Anonymous / platform / account identity levels; tipping never requires login | P | P0 |
| VID-06 | First-claim-wins idempotent platform claiming, contested handled, audited | X | P1 |
| VID-07 | Badges (8 named, opt-in, non-financial), streaks | X | P1 |
| VID-08 | Opt-in searchable profiles, viewer profile and search pages | U | — |
| VID-09 | Dashboard bounded to newest 100 relations, deterministic tie-break | U | — |
| VID-10 | Sessions capped at newest 100; password reset 30-min single-use, enumeration-safe | U | — |
| VID-11 | DPDP deletion (erased-vs-retained split) | U | — |
| VID-12 | DPDP data export | A | P1 |
| VID-13 | Reputation: verdict-only (3 keys), score never stored, 180-day window | X | P1 |
| VID-14 | Reputation write path (chargeback, velocity, moderation strike producers) | A | P1 |
| VID-15 | Creator-facing reputation display | A | P1 |
| VID-16 | Flag / report a supporter | A | P1 |
| VID-17 | Block a supporter | A | P1 |
| VID-18 | Anonymous non-platform tip claim path | A | P1 |
| VID-19 | YouTube identity attribution carried onto payments | A | P0 |
| VID-20 | YouTube handle-vs-channel-ID trust model and namespaces (§14.2) | A | P1 |

### 26.6 Engagement — interactions, widgets, goals, challenges

| ID | Item | State | Pri |
|---|---|---|---|
| ENG-01 | 8 interaction types (tip, TTS tip, sticker, mega alert, priority question, support vote, community goal, hype mode), tier counts 3/6/8/8 | P | P0 |
| ENG-02 | 7 widget types, tier counts 1/3/7/7 | P | P1 |
| ENG-03 | Support goals, progress computed live, clamped ≥0, windows stream/daily/monthly/open | U | — |
| ENG-04 | Recent tips, top supporters, ticker, mega-tip banner widgets | U | — |
| ENG-05 | Leaderboard returns rank + coarse tier bucket only, never exact amount, single channel | U | — |
| ENG-06 | Widgets reuse the overlay fragment-token/SSE path — a second delivery mechanism is a rejected design | U | — |
| ENG-07 | Paid votes bind one confirmed payment to one option; tally money-derived with refund effect | P | P1 |
| ENG-08 | Vote options capped at 16, serialized in the creating procedure | U | — |
| ENG-09 | **Viewer interaction menu** | A | **P0** |
| ENG-10 | Support-vote creator UI (create options) | A | P0 |
| ENG-11 | Support-vote viewer UI (cast) | A | P0 |
| ENG-12 | Mega alert + priority question viewer trigger | A | P0 |
| ENG-13 | Hype mode start control | X | P1 |
| ENG-14 | Widget privacy-scope control | X | P1 |
| ENG-15 | Widget preview / sample data for all widget types | P | P2 |
| ENG-16 | External contribution aggregation (Super Chat → goals), INR-only, include/exclude per source, no multipliers | U | — |
| ENG-17 | Contribution-source toggles wired into Challenges panel | X | P1 |
| ENG-18 | Priority Question "Unanswered" tab + Mark Answered (§10.6) | A | P1 |
| ENG-19 | Community boss battle | A | P2 |
| ENG-20 | Team / squad goals | A | P2 |
| ENG-21 | Milestone queue (prepare thank-you / sponsor reveal / transition) | A | P1 |
| ENG-22 | Stream streaks (daily/weekly) | A | P2 |
| ENG-23 | Like goal, member goal, chat goal, watch-time goal | A | P1 |
| ENG-24 | Prediction widget, no gambling mechanic | A | P2 |
| CHL-01 | Creator-published challenge, state machine, live progress, OBS widget | U | — |
| CHL-02 | Locked refund copy: "Refund automatically initiated through the creator's connected payment provider" | U | — |
| CHL-03 | Viewer-proposed challenges (plan calls this the better default) | A | P1 |
| CHL-04 | Completion evidence submission | A | P1 |
| CHL-05 | Dispute record | A | P1 |
| CHL-06 | Public standalone challenge board page | A | P2 |
| CHL-07 | `!challenge` chat command | A | P2 |
| CHL-08 | Refundable multi-contributor challenges | B | — |

### 26.7 Stickers, media, Alert Studio

| ID | Item | State | Pri |
|---|---|---|---|
| MED-01 | Curated catalogue exposing only id/name/category; selection re-validated server-side | U | — |
| MED-02 | Creator packs, tier quotas 10/25/50 (implementation choice, needs sign-off) | U | — |
| MED-03 | Moderation ladder: Pro structural scan, Creator +attestation, Studio `pending_review` | U | — |
| MED-04 | Staff review gate on `is_platform_admin` | P | P1 |
| MED-05 | Staff review admin UI | X | P1 |
| MED-06 | **Viewer sticker / GIF picker on the tip page** | X | **P0** |
| MED-07 | No route ever accepts viewer-supplied media bytes — catalogue IDs only | U | — |
| MED-08 | Template import rejects inline script / non-schema content outright | U | — |
| MED-09 | Template catalogue frontend | X | P1 |
| MED-10 | 359 of 600 runtime packages missing; individual authoring required, no mass-copy | A | P1 |
| MED-11 | Raw-HTML template shape forbidden at every tier | U | — |
| MED-12 | `render_bytes` capped at 2,000,000 | U | — |
| MED-13 | Asset storage quotas Free none / Pro 100MB / Creator 250MB / Studio 1GB | A | P1 |
| MED-14 | Malware scan stage 2 | A | P1 |
| MED-15 | Custom sound upload | A | P2 |
| MED-16 | Built-in themes / theme packs | A | P2 |
| MED-17 | Per-event styling beyond `displayStyle` brackets | P | P2 |
| MED-18 | Drag/resize/layer tools (numeric config exists) | P | P2 |
| MED-19 | Media and sound libraries | A | P2 |
| MED-20 | Curated meme/media queue module | A | P2 |
| MED-21 | Lottie + custom branding upload, Studio-tier, live gate, bytea storage | U | — |

### 26.8 Companion

| ID | Item | State | Pri |
|---|---|---|---|
| CMP-01 | Control-session lease; Free exactly one active lease | U | — |
| CMP-02 | Companion state / layout read and patch | U | — |
| CMP-03 | Layout slots 8/16/32/64 by tier; page sizes 4/8/16 | U | — |
| CMP-04 | 17-action catalogue, 4 groups, two-layer gate (entitlement AND activation) | U | — |
| CMP-05 | Server rejects `obs_*` sent directly, bypassing the client picker | U | — |
| CMP-06 | Device-code pairing | U | — |
| CMP-07 | **Mobile handler wiring in `App.tsx`** | X | **P0** |
| CMP-08 | macOS OBS control | U | — |
| CMP-09 | Windows OBS control | B | — |
| CMP-10 | Mirror actions (start/stop/screenshot) | B | — |
| CMP-11 | Stream actions (go live / end) | B | — |
| CMP-12 | Implicit channel provisioning for Companion-only signup | A | P1 |
| CMP-13 | Stream health panel (all six signals, heartbeat ages) | P | P0 |
| CMP-14 | Prepare Stream / go-live checklist (§5.1) | A | P0 |
| CMP-15 | Run full test with per-hop report | P | P0 |
| CMP-16 | Live Deck top strip + degraded-mode strip (§5.2) | A | P0 |
| CMP-17 | Panic / Clutch Mode | A | P0 |
| CMP-18 | Current and next queue item, live | A | P1 |
| CMP-19 | Per-item replay / skip | A | P1 |
| CMP-20 | Scene presets | A | P1 |
| CMP-21 | Goal controls from Companion | A | P1 |
| CMP-22 | Quick note / stream markers | A | P1 |
| CMP-23 | Recent tips, payment status, refund status in Companion (API exists, no web caller) | P | P1 |
| CMP-24 | Six monetisation push notification types | A | P1 |
| CMP-25 | Per-notification-type preferences (3 coarse toggles today) | P | P1 |
| CMP-26 | Session/device list with revoke | U | — |
| CMP-27 | Offline queue-of-intent | A | P2 |
| CMP-28 | Helper diagnostics (port, OBS version, ws auth state) | A | P2 |
| CMP-29 | Disabled-slot explanations naming the failing layer | P | P1 |
| CMP-30 | Wrap Stream post-stream workflow (§5.5) | A | P1 |
| CMP-31 | Companion rename before any standalone store listing | A | P1 |
| CMP-32 | Notification payloads never carry tip/donor/payment content | U | — |
| CMP-33 | Mobile secure storage `WHEN_UNLOCKED_THIS_DEVICE_ONLY`, no plaintext fallback | U | — |
| CMP-34 | Push tokens stored as fingerprint + ciphertext, raw never returned | U | — |
| CMP-35 | Desktop READMEs claim no pairing endpoint exists — stale since `0082`; update them | A | P2 |

### 26.9 Connectors and chat

| ID | Item | State | Pri |
|---|---|---|---|
| CON-01 | YouTube OAuth token storage, refresh, encryption | U | — |
| CON-02 | **Connect / disconnect UI** | X | **P0** |
| CON-03 | **Revoked-auth detection + creator prompt** | A | **P0** |
| CON-04 | Live status discovery, `streamList` polling, 3-failure fallback with reset | U | — |
| CON-05 | Quota budget, fair share, day-exhaust on 403 | U | — |
| CON-06 | Super Chat / Super Sticker / member / milestone / gifted normalisation | U | — |
| CON-07 | `!tip`, `!tip 100`, `!tip 100 message` → opaque short link | U | — |
| CON-08 | Bot chat acknowledgement (flag default off) | B | — |
| CON-09 | Connector entitlement counts 0/1/2/3 | U | — |
| CON-10 | Connector count / limit shown in UI | A | P1 |
| CON-11 | Ingest-failure admin surface UI | X | P1 |
| CON-12 | Financial truth never derived from a platform event — webhook only | U | — |
| CON-13 | Member reconciliation via `members.list` (never chat as truth) | A | P1 |
| CON-14 | Like goals via `videos.list` (cadence measured, not assumed) | A | P1 |
| CON-15 | Controlled broadcast lifecycle: create/bind → verify ingest `active` → testing → live | A | P1 |
| CON-16 | Assisted gifting as reminder/deep link only | A | P2 |
| CON-17 | Chat display, retention, filtering (tiered) | A | P1 |
| CON-18 | Twitch EventSub | B | — |
| CON-19 | Kick | B | — |
| CON-20 | Optional YouTube `/live` support page | A | P3 |
| CON-21 | YouTube identity/trust model and namespaces (§14.2) | A | P1 |

### 26.10 Entitlements, billing, admin, ops

| ID | Item | State | Pri |
|---|---|---|---|
| ENT-01 | Eight entitlement dimensions, closed set, all enforced | U | — |
| ENT-02 | Moderator seats 0/0/2/5, new grants only, existing grandfathered | U | — |
| ENT-03 | Moderator seat management UI | X | P1 |
| ENT-04 | Internal ceilings: pending visuals 20/50/150/500 · bindings 3/5/10/20 · presets 1/2/4/8 · read-only sessions 2/3/5/8 · control sessions 1/1/2/4 | P | P1 |
| ENT-05 | Grandfathering 12 months + 30-day renewal grace | U | — |
| ENT-06 | Referral engine with fraud signal | U | — |
| ENT-07 | Billing panel, upgrade/downgrade/reactivate/payment-method | U | — |
| ENT-08 | Top-up entitlement additivity, ledger, spend caps | A | P1 |
| ENT-09 | AI credit ledger, classes, reservations (§11.7) | A | P1 |
| ADM-01 | Admin console separate from creator dashboard, consumes platform-admin API only | U | — |
| ADM-02 | DLQ inspection, controlled replay/discard, audited, reason required | U | — |
| ADM-03 | Entitlement + channel-capacity management | U | — |
| ADM-04 | DB-backed billing plan catalogue with append-only history | P | P2 |
| ADM-05 | Reconciliation quarantine review UI | X | P0 |
| ADM-06 | Featured-creator curation writer | X | P1 |
| ADM-07 | Admin OIDC + MFA, durable admin registry (vs allowlist) | A | P0 |
| ADM-08 | Redaction by default; destructive ops need confirmation + reason + audit ref | U | — |
| ADM-09 | Admin console responsive at 320px/iPad/desktop, keyboard nav | U | — |
| OPS-01 | Six schedules defined with owner, OIDC, retry/DLQ, idempotency, monitoring, rollback | U | — |
| OPS-02 | **Schedules actually enabled** | X | **P0** |
| OPS-03 | Idempotency key `schedule:<id>:<window>`; receipt ≠ business completion | U | — |
| OPS-04 | Archive schedules stay disabled pending legal approval | B | — |
| OPS-05 | Email outbox with Resend; invoice, subscription, DPDP export, overlay-expiry mails | U | — |
| OPS-06 | Runbooks per critical alert | U | — |
| OPS-07 | On-call rotation | A | P0 |
| OPS-08 | Activation instrumentation (payout + OBS + first alert) | A | P0 |
| OPS-09 | Reliability metrics: captured-without-LiveEvent, duplicate LiveEvent, lost delivery, replay success, webhook lag, refund failures, TTS failures | P | P0 |
| OPS-10 | Creator activation funnel and viewer funnel instrumentation | A | P0 |
| OPS-11 | Revenue KPIs: tips/viewer-hour, average tip, repeat-supporter rate, TTS-driven tips, threshold uplift, goal-driven tips, `!tip` conversion, challenge and vote revenue | A | P0 |
| OPS-12 | Trace-ID discipline (§12.4) | U | — |
| OPS-13 | Metrics require service identity; no IDs in labels or paths | U | — |
| OPS-14 | Deployment manifest is `not-deployable` until placeholders resolved | B | — |
| OPS-15 | Static build publishes checked-in `_headers` CSP/framing/referrer/permissions | U | — |

**OPS-11 deserves emphasis.** These are the numbers that decide whether the business
works, they must be instrumented from the first cohort, and they **cannot be
reconstructed later**. Shipping without them means never knowing whether BharatStudio
raised a creator's income.

### 26.11 Marketing, legal, support

| ID | Item | State | Pri |
|---|---|---|---|
| MKT-01 | Product-per-page IA (/alerts, /mirror, /stream) with 301s | U | — |
| MKT-02 | Commission calculator with provider fees shown on both sides | U | — |
| MKT-03 | No competitor names in rendered HTML | U | — |
| MKT-04 | No Enterprise tier, CTA or contact-sales flow until L10 amended | U | — |
| MKT-05 | Watermark claim vs reality — pricing page says tip page + alert; only the alert has one | A | P1 |
| MKT-06 | `/features` frames Alerts and Companion as co-equal; Companion is bundled | A | P2 |
| MKT-07 | Legal sign-off: pricing/feature claims, DPDP deletion, plaintext reset URL in email | B | — |
| MKT-08 | Support surface and staffing | A | P0 |
| MKT-09 | Public copy matches versioned decisions with dated history | U | — |

### 26.12 AI

All **A** (absent) except the L23 seam. AI-01 safety rules + moderation queue ·
AI-02 TTS-safe rewrite and PII protection · AI-03 title/description/translation ·
AI-04 post-stream recap and moments · AI-05 Companion live-producer summaries ·
AI-06 credit ledger, tiers, recharge, spend caps · AI-07 thumbnail concept canvas ·
AI-08 Channel DNA style profile · AI-09 editor handoff pack · AI-10 clip
recommendations · AI-11 moderator copilot · AI-12 Clutch Mode intensity detection ·
AI-13 sponsor-safe scanning. Priority P1 for AI-01/02/06, P2 for the rest.
L23 assist (`0121`) is **P** — built and wired, but nav-less and provider-free.

### 26.13 Live Support Hub

| ID | Item | State | Pri |
|---|---|---|---|
| HUB-01 | Mobile support tray, verified payment state, receipts, QR/UPI | P | P0 |
| HUB-02 | Amount presets | A | P0 |
| HUB-03 | Five explicit status states (pending → verified → queued → shown → held) | A | P0 |
| HUB-04 | Safe message preview before checkout | A | P0 |
| HUB-05 | Approved sticker / sound picker | X | P0 |
| HUB-06 | Live supporter wall with opt-in names | A | P1 |
| HUB-07 | Free reactions, rate-limited and sampled | A | P1 |
| HUB-08 | Community goal ladder with milestone tiers | P | P1 |
| HUB-09 | Goal source labels (tips / Super Chats / memberships in or out) | A | P1 |
| HUB-10 | Pick-a-side vote with published rules and close time | A | P1 |
| HUB-11 | Stream mission card | A | P1 |
| HUB-12 | Live "what changed" feed | A | P2 |
| HUB-13 | Embedded YouTube player, correct `origin`, responsive | A | P2 |
| HUB-14 | Free lane: one free vote, check-in streak, challenge proposal, cheer card | A | P1 |
| HUB-15 | "Where does my support go?" creator explainer | A | P1 |
| HUB-16 | Payment-retry recovery screen | A | P1 |
| HUB-17 | Low-bandwidth / no-player mode | A | P1 |
| HUB-18 | Indian language support | P | P1 |
| HUB-19 | Accessibility: reduced motion, no autoplay sound, SR labels | P | P0 |
| HUB-20 | Shareable mini-card, campaign links, referral attribution | A | P2 |
| HUB-21 | Event-specific layout presets | A | P2 |
| HUB-22 | Post-stream supporter recap and receipt export | A | P2 |
| HUB-23 | Milestone unlocks framed as a creator promise, never a contract | A | P1 |

### 26.14 Customisation and gating

| ID | Item | State | Pri |
|---|---|---|---|
| CUS-01 | Four-switch model (entitled / enabled / configured / active) applied universally | P | P0 |
| CUS-02 | Per-widget full config surface (§15.2) | A | P0 |
| CUS-03 | Locked capabilities shown with the unlocking tier, never hidden or dead | P | P1 |
| CUS-04 | Downgrade preserves configuration; over-limit items read-only | P | P1 |
| CUS-05 | Preset bundles that are fully editable afterwards | A | P2 |
| CUS-06 | Per-source alert styling (Super Chat distinct from UPI tip) | A | P1 |

### 26.15 Lobby Engine

| ID | Item | State | Pri |
|---|---|---|---|
| LOB-01 | Session create: game, region, mode, platform, time, seats, reserves, policy | A | P1 |
| LOB-02 | Public waitlist; code never on stream | A | P1 |
| LOB-03 | Ready check | A | P1 |
| LOB-04 | Single-use, short-lived private seat token | A | P1 |
| LOB-05 | Code revealed only after readiness confirmed | A | P1 |
| LOB-06 | No-show expiry and automatic reserve promotion | A | P1 |
| LOB-07 | Six eligibility modes, policy locked and displayed before joining | A | P1 |
| LOB-08 | Redacted audit log incl. moderator override reason | A | P1 |
| LOB-09 | Aggregate-only public overlay module | A | P1 |
| LOB-10 | Companion operator console | A | P1 |
| LOB-11 | Automatic deletion of temporary lobby data | A | P1 |
| LOB-12 | Time-bound suspensions with appeal; never keyed on payment identity | A | P1 |
| LOB-13 | Session templates | A | P2 |
| LOB-14 | Language / region / platform / accessibility filters | A | P2 |
| LOB-15 | Voluntary skill bands, friend-group locking | A | P2 |
| LOB-16 | Creator squads with attributed operator actions | A | P2 |
| LOB-17 | Lobby reputation, no public shaming | A | P2 |
| LOB-18 | Post-match pulse with private reporting | A | P2 |
| LOB-19 | Clip consent before featuring a player | A | P1 |
| LOB-20 | Cross-creator combined queues | A | P3 |
| LOB-21 | Recurring community nights with reminders | A | P2 |
| LOB-22 | Screened Guest Queue (audio-only, time-boxed) | A | P3 |
| LOB-23 | Paid roulette, wagering, prize pools, paid WebRTC, viewer uploads | **Never** | — |

### 26.16 Giveaways and tournaments

| ID | Item | State | Pri |
|---|---|---|---|
| GIV-01 | Creator-defined prize, entry method, window, draw method, published up front | A | P1 |
| GIV-02 | Free entry route always available; no paid-only entry | A | P1 |
| GIV-03 | Deterministic seeded draw, seed and entrant count recorded | A | P1 |
| GIV-04 | Override possible but logged and labelled | A | P1 |
| GIV-05 | Terms: creator is promoter, responsible for eligibility, tax and delivery | A | P1 |
| GIV-06 | Overlay: entry count, timer, consented winner, no address on stream | A | P1 |
| GIV-07 | Legal review before any chance-based format ships in India | A | P1 |
| TRN-01 | Brackets (single, double, round robin, points) on the Lobby Engine | A | P2 |
| TRN-02 | Seeding by attendance, creator pick, or published-seed random | A | P2 |
| TRN-03 | Check-in windows, scheduling, reminders | A | P2 |
| TRN-04 | Score reporting with dispute note | A | P2 |
| TRN-05 | Standings overlay module | A | P2 |
| TRN-06 | Sponsor slot with exposure log | A | P2 |

### 26.17 Custom audio and creator media

| ID | Item | State | Pri |
|---|---|---|---|
| AUD-01 | Custom alert sounds, tier-gated | A | P1 |
| AUD-02 | Widget / module / milestone sounds | A | P1 |
| AUD-03 | Supporter-triggerable soundboard, cooldown and queue | A | P1 |
| AUD-04 | Per-bracket and per-source sound selection | A | P1 |
| AUD-05 | BRB / countdown music bed | A | P2 |
| AUD-06 | Rights attestation checkbox with recorded timestamp | A | P1 |
| AUD-07 | Terms text placing copyright liability on the creator | A | P1 |
| AUD-08 | Upload audit record, immediate disable, takedown handling | A | P1 |
| AUD-09 | Duration, size and format caps; scan pipeline applied | A | P1 |
| AUD-10 | Asset storage quota enforcement (MED-13 dependency) | A | P1 |
| AUD-11 | Shared or discoverable music library | **Never** | — |

### 26.18 Performance

| ID | Item | State | Pri |
|---|---|---|---|
| PRF-01 | CI-enforced budgets (§19.1) | A | P0 |
| PRF-02 | Single connection, single rAF loop, modules as pure renderers | A | P0 |
| PRF-03 | Composite-only animation; no layout-triggering properties | P | P0 |
| PRF-04 | Bounded DOM with recycling; flat node count over 8 hours | A | P0 |
| PRF-05 | Idle modules fully unsubscribed | A | P0 |
| PRF-06 | Server-side sampling and rate limiting for reactions and chat | A | P0 |
| PRF-07 | Burst coalescing on long-gap replay | A | P1 |
| PRF-08 | Read-through cache for derived aggregates, invalidated by event, never a stored counter | A | P0 |
| PRF-09 | `DATABASE_URL_DIRECT` for the overlay listener | P | P0 |
| PRF-10 | Universal cursor pagination with bounded pages | P | P1 |
| PRF-11 | Index coverage for every widget-backing query | P | P0 |
| PRF-12 | Asset budgets: Lottie complexity, audio length, server-side image pre-scaling | A | P1 |
| PRF-13 | No third-party scripts in the overlay | U | — |
| PRF-14 | Per-module error boundaries; twice-failed module stays down with a note | A | P1 |
| PRF-15 | Companion: optimistic UI, virtualised lists, no re-render storms | P | P1 |
| PRF-16 | Published one-source-vs-many benchmark, re-run in CI | A | P1 |

### 26.19 Control plane and admin

| ID | Item | State | Pri |
|---|---|---|---|
| CTL-01 | Capability registry table with versioned, audited rows | A | **P0** |
| CTL-02 | Resolution order engine (kill → denylist → rollout → tier → override) | A | **P0** |
| CTL-03 | Per-channel resolved blob, versioned and cached; never per-capability queries | A | P0 |
| CTL-04 | Admin UI: master switch, retier, edit limits, kill | A | P0 |
| CTL-05 | Impact preview ("affects 214 channels, 3 live") | A | P1 |
| CTL-06 | Staged effective-time changes | A | P1 |
| CTL-07 | Two-person approval for global kill and paid→Free moves | A | P1 |
| CTL-08 | One-action revert to previous version | A | P1 |
| CTL-09 | Layer 1 correctness dimensions rejected from this panel | A | P0 |
| CTL-10 | `GET /v1/public/capability-matrix` published snapshot | A | P0 |
| CTL-11 | Marketing build reads the snapshot; webhook revalidation | A | P0 |
| CTL-12 | Marketing sections behind flags (`kind = marketing_section`) | A | P1 |
| CTL-13 | Admin MFA + durable admin registry (ADM-07 dependency) | A | P0 |

### 26.20 New widgets

| ID | Item | State | Pri |
|---|---|---|---|
| WID-01 | Companion tap source (+1 win / +1 loss) | A | P1 |
| WID-02 | Lobby/tournament auto-fill of results | A | P2 |
| WID-03 | Wins This Season, Session Record, Win Streak | A | P1 |
| WID-04 | Personal Best, Rank Progress, Season Objective | A | P2 |
| WID-05 | Head-to-Head, Scoreboard | A | P2 |
| WID-06 | Match Countdown, Tournament Standings, Squad Roster | A | P2 |
| WID-07 | Hours Streamed, Milestone Ticker, Top Clip, Recap Card | A | P2 |

### 26.21 Co-Stream Room

| ID | Item | State | Pri |
|---|---|---|---|
| COS-01 | Room create, explicit mutual accept, short-lived grants | A | P1 |
| COS-02 | Public `/live/collab/<id>` page with two IFrame players | A | P1 |
| COS-03 | Eight layout modes | A | P1 |
| COS-04 | Switch Window with published range, countdown, override | A | P2 |
| COS-05 | One audio source at a time, viewer-switchable | A | P1 |
| COS-06 | Shared event rail, timer, scorecard | A | P1 |
| COS-07 | Side-assigned supporter alerts | A | P1 |
| COS-08 | Chat tabs per creator | A | P2 |
| COS-09 | Companion control room incl. one-tap safe layout | A | P1 |
| COS-10 | OBS collaboration overlay scene export | A | P2 |
| COS-11 | Contribution selector (A / B / shared goal) | A | P1 |
| COS-12 | Instant revoke; page degrades to single or ended state | A | P1 |
| COS-13 | Explicit "feeds are not frame-synced" UI treatment | A | P1 |
| COS-14 | Clip handoff consent | A | P2 |
| COS-15 | Silent payment splitting | **Never** | — |

### 26.22 Sound Moments and Rules Engine

| ID | Item | State | Pri |
|---|---|---|---|
| SND-01 | Moment = sound + animation + sticker + TTS style + effect, creator-curated | A | P1 |
| SND-02 | Amount-tiered moment catalogue | A | P1 |
| SND-03 | Loudness normalisation and duration caps | A | P1 |
| SND-04 | Per-sound, per-viewer, stream-wide cooldowns | A | P1 |
| SND-05 | Themed packs incl. Indic and festival | A | P2 |
| SND-06 | Companion mute / skip / pause / emergency safe mode | P | P1 |
| SND-07 | No remote URL execution in the overlay | A | P0 |
| RUL-01 | Rules engine: thresholds, modes, cooldowns, caps, priority, approval | A | P1 |
| RUL-02 | Never-interrupt-gameplay mode | A | P1 |
| RUL-03 | Overlay-offline hold-and-replay | P | P1 |
| SEC-01 | Short-lived signed overlay capabilities with renewal | A | **P0** |
| SEC-02 | Session/device binding where practical | A | P1 |
| SEC-03 | Scheduled rotation; never in screenshots, logs or tickets | P | P1 |
| MIG-01 | Shadow mode with a migration report (delivered, missed, latency, unsupported) | A | P1 |
| MIG-02 | Test/sandbox mode that never reaches viewers | A | P1 |
| MIG-03 | Global emergency-disable button | A | P0 |

### 26.23 Enterprise

All **B** (blocked) pending §24.5. EN-00 commercial/legal model · EN-01 org, roles,
allocations · EN-02 immutable snapshot schema · EN-03 settlement adapters · EN-04
pre-order snapshot resolver · EN-05 finance-control APIs · EN-06 transfers, refunds,
reconciliation · EN-07 scheduler handlers · EN-08 dashboard views · EN-09 pilot.
Plus SSO, RBAC, shared brand kits, licensed packs, campaigns, cross-channel analytics,
outbound webhooks, finance/audit exports, SLA support.

### 26.24 Storage and media platform

| ID | Item | State | Pri |
|---|---|---|---|
| STO-01 | GCS + CDN with content-addressed keys and signed URLs | A | **P0 for audio** |
| STO-02 | Postgres holds metadata, moderation state and attestation only | A | P0 |
| STO-03 | Normalisation pipeline (audio loudness, GIF→MP4/WebM, image pre-scale) | A | P1 |
| STO-04 | Deduplication by sha256 across creators | A | P2 |
| STO-05 | Keep existing Lottie bytea working; new media to GCS; opportunistic backfill | A | P1 |

---

## 27. Blocked — with the exact unblocking condition

| Item | Unblocked by |
|---|---|
| Recurring memberships | A rail reporting `supportsRecurringPayments: true`. **Interim answer: Season Passes (§10.4)** |
| Refund initiation, refundable challenges | A rail reporting `supportsRefunds: true`. No rail does today |
| Enterprise workspace | Five written Razorpay Route answers (parent/linked structure, third-party split rights, direct settlement, per-account flexibility, suspended-account behaviour) + counsel/CA advice |
| Paytm | All eight written conditions confirmed |
| Cashfree, PhonePe | Partner confirmation |
| Windows Companion | A Windows build agent; target has never compiled |
| Mirror and Stream Companion actions | Those products emitting a liveness signal (`0093` hard-codes activation false) |
| Bot chat acknowledgement | Google chat-write scope approval |
| Template catalogue (359 packages) | Individual authoring + design/native-language review. Mass-copy explicitly forbidden |
| Archive schedules | Approved eligibility, integrity and retention/legal decision |
| Platform KMS/HSM signing | Provisioned KMS/HSM |
| Deployment | Resolved `REQUIRED_*` placeholders, IAM/OIDC, staging recovery, capacity, observability, rollback rehearsal |
| Everything production | Google OAuth verification · YouTube quota · legal sign-off · Razorpay Route enquiry — **all four still unfiled** |

---

## 28. Open decisions the owner must make

1. **Studio price: ₹499 or ₹599?** `active/launch/00_LAUNCH_SCOPE_AUTHORITY.md` says
   ₹599 GST-inclusive superseding ₹499/₹799; task files carry both. One must win.
2. **Queue count ladder** — sources disagree: 1/2/3/5 versus Free 1 / Pro 3 /
   Creator 5 / Studio 10. Reconcile before any pricing page change.
3. Companion rename before a standalone store listing.
4. Companion bundled-vs-standalone pricing (must remain configurable either way).
5. Mirror and Stream pricing numbers.
6. Sticker pack limits 10/25/50 — implementation choice, needs sign-off.
7. Bare `!tip` with no amount — behaviour undefined.
8. Template catalogue: author 359 packages, cut the catalogue, or relax the HTML
   prohibition (the plan's author recommends against relaxing, even sandboxed).
9. Reputation retention vs DPDP — decided by default, recorded as open.
10. Top-up pricing and margins per §10.2.
11. AI credit prices per feature and per class.
12. Paid-tier Companion control-session concurrency (Free is exactly one; paid undecided).
13. **Credit bundle sizing** — the rupee price and unit count per bundle, and the
    internal margin floor (25% is the stated minimum, not a decision).
14. **Giveaway legal position in India** — which formats are safe without a licence,
    and whether any chance-based format ships at all.
15. Whether tournaments are a Studio-only capability or available lower.
16. Custom-audio tier ladder — which tiers get sounds, how many, and clip length caps.
17. Lobby: default eligibility mode shipped to new creators.
18. Whether the tip-for-room-code flow (§10.5) coexists with the Lobby Engine or is
    replaced by it — they overlap and currently both exist on paper.
19. **Queue-count ladder** must be settled before the capability matrix is seeded —
    1/2/3/5 or 1/3/5/10.
20. Whether the Co-Stream Room is Creator-tier or Studio-only.
21. Whether creator sound-upload counts (5 / 25 / 100) and the Free tier's exclusion
    from uploads are right.
22. Who may operate the control plane, and whether moving a paid capability into Free
    needs owner approval rather than two-staff approval.

---

## 29. Build order

Scope is Alerts, dashboard, overlay, Support Hub and mobile Companion. Nothing else.

**Phase 0 — make what exists real, and make it controllable.** F01–F22, PRF-01, plus
the control plane (CTL-01 to CTL-04, CTL-09 to CTL-11) and short-lived overlay
capabilities (SEC-01). The control plane comes first because every later phase adds
capabilities that need a switch, and retrofitting a registry onto sixty hard-coded
gates is far worse than seeding it with eight. Nothing new ships until the
product stops being a set of disconnected parts. The identity writer, receipts, TTS
safety, YouTube connect UI, mobile handler wiring, TipForm as the interaction surface,
schedules on, account activation, quarantine UI, the reachability CI checks, and the
performance budgets that will police everything after.

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

**Phase 4 — YouTube depth.** Member reconciliation · like goals · controlled broadcast
lifecycle · chat moderation · the identity and trust model.

**Phase 5 — monetisation depth.** Season Passes · room-password delivery · Priority
Questions · member perks · top-ups and the credit ledger · Discord role sync.

**Phase 6 — safety and AI.** Indic safety · AI moderation queue · TTS-safe rewrite ·
copilot · recap and clips.

**Phase 7 — events and collaboration.** Co-Stream Room · giveaways · tournaments ·
sponsor manager and exposure logs · finance exports · post-stream analytics ·
portability.

**Blocked track, unscheduled.** Enterprise (§24) proceeds only when its reopening gate
closes. Nothing in Phases 0–7 depends on it.

Two things are not phases:

- **Instrumentation** (OPS-08 to OPS-11) ships with Phase 0 or the first cohort's data
  is lost permanently.
- **Performance budgets** (PRF-01) land before Phase 1, because retrofitting a frame
  budget onto twenty modules is far harder than holding it from the first one.

---

## 30. Maintaining this document

This file is the product authority. Master plan Part 7 is superseded and should not be
consulted for status.

Rules for keeping it true, learned from how Part 7 went wrong:

1. A status may only be changed by someone who **traced the user path**, not by
   someone who found the code.
2. Every row's state uses the §0 vocabulary. "Done" is not a permitted value.
3. Reconciliation runs **after** a batch closes, never inside it — a lane running
   alongside build lanes records the tree as it was at dispatch.
4. When a claim here turns out to be wrong, correct it in place and say what was wrong.
   Four rows in Part 7 asserted things that were never true; nobody caught it for
   eleven days because the register was never re-derived from code.
5. Test counts are never cited as evidence of completeness.
