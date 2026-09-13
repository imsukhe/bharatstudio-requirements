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

### 20.2 What "customisable to the max" means concretely

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

### 20.3 Gating rules

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

## 19. Performance architecture — no lag, anywhere

The overlay runs inside OBS while the machine is encoding a game. Every millisecond we
spend is a frame the creator loses. "Lightweight" is therefore a correctness
requirement, not a nice-to-have, and the honest constraint is that **we are adding
work to a machine that is already saturated**.

### 19.1 Budgets — measured, not asserted

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

### 19.2 Overlay — the architecture that keeps it cheap

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

### 19.3 The derive-don't-store tension, and how to resolve it

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

### 20.4 Server and realtime

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

### 20.5 Companion (mobile)

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

### 20.6 Support Hub

- Server-render the page; the YouTube player is lazy and optional.
- The player is the heaviest thing on the page — it must never block first paint, and a
  low-bandwidth mode omits it entirely.
- Realtime goal and ticker updates arrive over one connection, shared by all modules.
- Reactions are optimistic locally and sampled server-side.
- The payment path stays functional with JavaScript degraded — a QR and a link always
  work.

### 20.7 How we stay ahead of competitors on this

The competitive claim is not "more widgets". It is **one source instead of twelve**,
which is a measurable CPU and memory win on the creator's encoding machine, and the
reason a creator with a mid-range PC can run our full feature set and not theirs.
That claim must be backed by a published, reproducible benchmark: our full canvas
versus an equivalent stack of separate browser sources, measured on a mid-range
machine, re-run in CI.

If that benchmark ever stops favouring us, the architecture has drifted and the
feature set is not worth what it costs the creator.

---

## 20. Master task register — nothing deferred

Status key: **U** usable · **X** unreachable · **P** partial · **A** absent · **B** blocked.
Priority: **P0** launch-blocking · **P1** launch-shaping · **P2** post-launch · **P3** later.

### 20.1 Foundation repairs
See §3 for full detail. F01–F22, all **P0** except F16/F19/F20 (P1) and F22 (P0, cheap).

### 15.2 Payments and money

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

### 15.3 Alerts, queues, overlay

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

### 19.4 TTS

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

### 19.5 Viewer identity, history, trust

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

### 19.6 Engagement — interactions, widgets, goals, challenges

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

### 19.7 Stickers, media, Alert Studio

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

### 20.8 Companion

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

### 20.9 Connectors and chat

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

### 20.10 Entitlements, billing, admin, ops

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

### 20.11 Marketing, legal, support

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

### 20.12 AI

All **A** (absent) except the L23 seam. AI-01 safety rules + moderation queue ·
AI-02 TTS-safe rewrite and PII protection · AI-03 title/description/translation ·
AI-04 post-stream recap and moments · AI-05 Companion live-producer summaries ·
AI-06 credit ledger, tiers, recharge, spend caps · AI-07 thumbnail concept canvas ·
AI-08 Channel DNA style profile · AI-09 editor handoff pack · AI-10 clip
recommendations · AI-11 moderator copilot · AI-12 Clutch Mode intensity detection ·
AI-13 sponsor-safe scanning. Priority P1 for AI-01/02/06, P2 for the rest.
L23 assist (`0121`) is **P** — built and wired, but nav-less and provider-free.

### 20.13 Live Support Hub

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

### 20.14 Customisation and gating

| ID | Item | State | Pri |
|---|---|---|---|
| CUS-01 | Four-switch model (entitled / enabled / configured / active) applied universally | P | P0 |
| CUS-02 | Per-widget full config surface (§15.2) | A | P0 |
| CUS-03 | Locked capabilities shown with the unlocking tier, never hidden or dead | P | P1 |
| CUS-04 | Downgrade preserves configuration; over-limit items read-only | P | P1 |
| CUS-05 | Preset bundles that are fully editable afterwards | A | P2 |
| CUS-06 | Per-source alert styling (Super Chat distinct from UPI tip) | A | P1 |

### 20.15 Lobby Engine

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

### 20.16 Giveaways and tournaments

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

### 20.17 Custom audio and creator media

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

### 20.18 Performance

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

## 21. Blocked — with the exact unblocking condition

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

## 22. Open decisions the owner must make

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

---

## 23. Build order

Scope is Alerts, dashboard, overlay, Support Hub and mobile Companion. Nothing else.

**Phase 0 — make what exists real.** F01–F22 plus PRF-01. Nothing new ships until the
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
transparent votes · mission card · milestone queue · custom audio with attestation.

**Phase 4 — YouTube depth.** Member reconciliation · like goals · controlled broadcast
lifecycle · chat moderation · the identity and trust model.

**Phase 5 — monetisation depth.** Season Passes · room-password delivery · Priority
Questions · member perks · top-ups and the credit ledger · Discord role sync.

**Phase 6 — safety and AI.** Indic safety · AI moderation queue · TTS-safe rewrite ·
copilot · recap and clips.

**Phase 7 — events and business.** Giveaways · tournaments · sponsor manager and
exposure logs · finance exports · post-stream analytics · portability.

Two things are not phases:

- **Instrumentation** (OPS-08 to OPS-11) ships with Phase 0 or the first cohort's data
  is lost permanently.
- **Performance budgets** (PRF-01) land before Phase 1, because retrofitting a frame
  budget onto twenty modules is far harder than holding it from the first one.

---

## 24. Maintaining this document

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
