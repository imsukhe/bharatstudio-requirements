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

## 6. Master Canvas

One browser source replaces the pile. Streamlabs' own pattern — alerts, chat, ticker,
media, custom widgets and themes each added as a separate browser source — is exactly
the clutter we remove.

Modules: alerts · chat · supporter ticker · goals · challenges · hype meter · QR/tip
CTA · sponsor card · now-playing metadata · media/meme queue · boss battle · vote and
prediction · milestone celebration · countdown/BRB/ending cards.

Requirements: safe zones · scene profiles · theme packs · per-module placement and
z-order · vertical/mobile layout variants · preview with sample data · a single
heartbeat the Live Deck can read · graceful degradation per module (one module
failing must not blank the canvas).

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

## 8. Supporter page — conversion infrastructure

Not a payment form.

- Fast UPI-first flow with a clearly branded creator page
- **Preset amounts** plus custom amount
- Optional short, moderated message
- **Optional approved meme / sticker / GIF selection** — the catalogue and creator
  packs already exist server-side and have no picker (§2.2)
- Anonymous / visible-name choice
- Consent choice for on-stream alert and public recognition
- Receipt immediately after verified payment
- **"Your message is queued"** status — never a false claim that it already displayed
- QR deep link and browser fallback
- Live goal context: "₹420 remaining to unlock the creator challenge"
- Supporter streak, badge or thank-you **only with explicit identity/visibility consent**
- Accessibility; Hindi and English now, regional languages later
- Fair, transparent giveaway/challenge terms where a creator uses them

**Hard boundary:** never ship a UPI "cashback membership grant" as a growth hack. It
is a regulated financial workflow needing payout/KYC, fraud, age, tax,
consumer-protection, dispute and anti-abuse design — not an overlay widget.

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

**On the "we take 1-5% on each top-up" question: no — that framing is wrong and worse
for us.** A top-up is not someone else's money passing through. The creator pays
BharatStudio directly for a service we supply. Our margin is `price − provider cost`,
which on TTS is far more than 5%, and on AI is whatever we set it to. Taking a
"commission" on our own sale would be a strange way to describe revenue and would
invite the question of whether we also take a cut of tips. Keep the line absolute:
**commission on creator earnings is zero; we sell capacity and software.**

Gateway fees on the top-up purchase itself (2–3%) are our cost of doing business, the
same as they are for the creator on tips. Per the locked copy rule, we never present
gateway fees as a BharatStudio charge.

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

## 14. Cross-product architecture

Four products, one brand, one account.

| Product | What it is | Relationship |
|---|---|---|
| **Alerts** | The tipping, overlay, moderation and engagement product | The core; everything else orbits it |
| **Companion** | Web/iOS/Android/desktop control plane | Bundled with Alerts today; **cannot be sold standalone until implicit channel provisioning exists** (§16) |
| **Stream** | Android/iOS live streaming (separate master plans) | Source of "go live" and stream controls in Companion |
| **Mirror** | Screen mirroring, sold on its own licence key | Source of mirror controls in Companion |

**BharatStudio Platform** is the shared service that makes "one account" true:
cross-product identity (`bharatstudio_user_id`), Apple/Google/passkey auth, OAuth/OIDC
with refresh rotation, App Store and Play purchase verification, entitlement-gated pack
authorization, signed broadcast capabilities. Store catalogue ₹9/day, ₹19/week,
₹49/month, ₹139/3-month, ₹249/6-month, ₹499/year — **store price is authoritative and
the client never computes or enforces price**.

Platform explicitly does **not** own RTMP, media, capture, encoding, relay or broadcast
transport; nor Razorpay/UPI/tips/donor data/Alerts queues/overlays; nor Alerts creator
config; nor direct DB access into any product. Free local streaming stays account-free
and works even when Platform is down.

Purchase binding: a verified purchase root binds to exactly one account. A conflicting
claim returns a non-enumerating `purchase_account_conflict` and **never auto-merges or
transfers**.

### 14.1 Naming problem that blocks a store listing

"Companion" collides with **Bitfocus Companion**, the established Stream Deck / OBS
controller. It must be renamed before any standalone store listing. There is also an
internal collision: Stream's `CompanionApp` (local TCP 27190) is a different Companion
from the L07 product, and `companion-desktop/windows-mirror-test/` is filed under
Companion but belongs to Mirror.

### 14.2 YouTube identity and trust (phase-2 design, worth pulling forward)

A designed-but-unbuilt feature set that directly serves creator trust:

- The **YouTube channel ID is the immutable ownership key; the handle is a changeable
  alias and must never be treated as identity**
- URL namespaces: `/u/<slug>` ordinary · `/@<youtube-handle>` verified only ·
  `/channel/<stable-id>` permanent
- Historical handles are permanently reserved and never auto-released on disconnect,
  deletion or inactivity
- A conflicting later claimant is frozen for manual review, never auto-transferred
- Sync states: `verified_current`, `handle_changed`, `sync_pending`, `stale`,
  `frozen_for_review`
- Donor-facing verification badge on the tip page
- OAuth with PKCE and state, `mine=true`, multi-channel selection, identity preview;
  disconnect does not release aliases
- No token or email exposure; rate limits; redaction in logs

This is the answer to impersonation, which is the main trust risk on a page that
accepts money on a creator's behalf.

---

## 15. Master task register — nothing deferred

Status key: **U** usable · **X** unreachable · **P** partial · **A** absent · **B** blocked.
Priority: **P0** launch-blocking · **P1** launch-shaping · **P2** post-launch · **P3** later.

### 15.1 Foundation repairs
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

### 15.4 TTS

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

### 15.5 Viewer identity, history, trust

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

### 15.6 Engagement — interactions, widgets, goals, challenges

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

### 15.7 Stickers, media, Alert Studio

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

### 15.8 Companion

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

### 15.9 Connectors and chat

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

### 15.10 Entitlements, billing, admin, ops

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

### 15.11 Marketing, legal, support

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

### 15.12 AI

All **A** (absent) except the L23 seam. AI-01 safety rules + moderation queue ·
AI-02 TTS-safe rewrite and PII protection · AI-03 title/description/translation ·
AI-04 post-stream recap and moments · AI-05 Companion live-producer summaries ·
AI-06 credit ledger, tiers, recharge, spend caps · AI-07 thumbnail concept canvas ·
AI-08 Channel DNA style profile · AI-09 editor handoff pack · AI-10 clip
recommendations · AI-11 moderator copilot · AI-12 Clutch Mode intensity detection ·
AI-13 sponsor-safe scanning. Priority P1 for AI-01/02/06, P2 for the rest.
L23 assist (`0121`) is **P** — built and wired, but nav-less and provider-free.

### 15.13 Cross-product

| ID | Item | State | Pri |
|---|---|---|---|
| XP-01 | Platform service: cross-product identity, auth, store verification, entitlement projections | P | P1 |
| XP-02 | Four isolated Platform services with distinct service accounts and DB roles | P | P1 |
| XP-03 | KMS/HSM ES256 signing — build fails closed until it exists | B | — |
| XP-04 | Purchase binds to exactly one account; conflict returns non-enumerating error, never merges | U | — |
| XP-05 | Free streaming never gated on Platform availability | U | — |
| XP-06 | Stream (iOS/Android) live streaming apps | P | — |
| XP-07 | Mirror (mac/Windows) screen mirroring, sold on its own licence key | P | — |
| XP-08 | Mirror ↔ Companion session handshake (`MirrorSessionService` unimplemented) | A | P2 |
| XP-09 | Companion ↔ Stream go-live control (blocked on liveness signal) | B | — |
| XP-10 | `REPOSITORY-STRUCTURE.md` is stale — omits admin, platform, stream-*, Mirror | A | P3 |
| XP-11 | Stream Deck plugin (§10.9) | A | P1 |
| XP-12 | Bridge/relay integrations (§9) | A | P1 |

---

## 16. Blocked — with the exact unblocking condition

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

## 17. Open decisions the owner must make

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

---

## 18. Build order

**Phase 0 — make what exists real.** F01–F22. Nothing new ships before the product
stops being a set of disconnected parts. Roughly: the identity writer, receipts, TTS
safety, YouTube connect UI, mobile wiring, TipForm interactions, schedules on, account
activation, quarantine UI, and the reachability CI checks.

**Phase 1 — the cockpit.** Companion Live Deck with health and degraded states ·
Master Canvas · Prepare Stream checklist · Wrap Stream · Clutch Mode.

**Phase 2 — migration.** OBS Migration Assistant · Observe/Bridge/Replace · Stream
Deck plugin · compatibility relays.

**Phase 3 — YouTube depth.** Preflight, controlled broadcast lifecycle, chat
moderation, member reconciliation, like goals, identity/trust model.

**Phase 4 — monetisation depth.** Season Passes · room-password delivery · Priority
Questions · Discord/WhatsApp sync · member perks · top-ups.

**Phase 5 — safety and AI.** Indic safety · AI moderation queue · TTS-safe rewrite ·
credit ledger · copilot.

**Phase 6 — business.** Sponsor manager and exposure logs · finance exports ·
post-stream analytics · portability.

Instrumentation (OPS-08 through OPS-11) is not a phase. It ships with Phase 0 or the
first cohort's data is lost permanently.

---

## 19. Maintaining this document

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
