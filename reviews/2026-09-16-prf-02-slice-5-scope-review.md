# Review — PRF-02 slice 5 scope, before any code

**Date:** 2026-09-16
**Owner:** Sukhdev Singh
**Reviewer:** Review-only agent (no worktree changes; no file under `bharatstudio-alerts/`,
`bharatstudio-crons/` or any migration was created or modified by this review).
**Authority:** `../FULL-PRODUCT-DEFINITION.md` §6, §9.1.1, §12.7, §15.4.3, §19.4, §19.5,
§30.3, §31, §32, §33, §34 · `../active/tasks/PRF-02.md` ·
`2026-09-16-prf-02-slice-4-scope-review.md` · `2026-09-16-prf-02-master-canvas-runtime.md`

Seven of the twenty §6 modules are built (#1, #2, #3, #4, #7, #8 current-only, #13).
This review audits the remaining thirteen against the repository before anything is
scoped, because slice 4 recorded the standing lesson and this audit exists to apply it:
**read the data path before believing the catalogue.**

---

## The finding that should change how slice 5 is scoped

**Not one of the thirteen is READY.** Every module in the §6 catalogue whose data is
already reachable over the Canvas's single overlay session has already been built. The
complete overlay-session-reachable read surface in this repository is fourteen
`app_private` functions and the routes over them:

| Function | Migration | Route |
|---|---|---|
| `list_overlay_lottie_assets` | `0077` L171 | `/v1/overlay-lottie/:overlayId` (`overlay-lottie.ts:23`) |
| `list_overlay_goal` | `0102` L365 | `/v1/overlay-goals/:overlayId` (`goals.ts:182`) |
| `list_overlay_vote_tally` | `0105` L567 | `/v1/overlay-widgets/:overlayId/votes/:definitionId` (`interactions.ts:533`) |
| `list_overlay_hype_mode` | `0105` L769 | `.../hype/:definitionId` (`interactions.ts:550`) |
| `list_overlay_widget_config` | `0105` L926 | `.../config/:widgetType` (`interactions.ts:516`) |
| `list_overlay_leaderboard` | `0105` L1021 | `.../leaderboard` (`interactions.ts:567`) |
| `list_overlay_paid_vote_tally` | `0108` L244 | `.../paid-votes/:definitionId` (`interactions.ts:590`) |
| `list_overlay_recent_tips` | `0108` L320 | `.../recent-tips` (`interactions.ts:629`) |
| `list_overlay_top_supporters` | `0108` L351 | `.../top-supporters` (`interactions.ts:650`) |
| `list_overlay_supporter_ticker` | `0108` L380 | `.../supporter-ticker` (`interactions.ts:671`) |
| `list_overlay_mega_tip_banner` | `0108` L416 | `.../mega-tip-banner` (`interactions.ts:692`) |
| `list_overlay_challenge` | `0109` L344 | `/v1/overlay-challenges/:overlayId` (`challenges.ts:179`) |
| `list_overlay_master_canvas_modules` | `0131` L179 | `.../master-canvas/modules` (`master-canvas.ts:94`) |
| `list_overlay_tug_of_war_vote` | `0132` L56 | `.../tug-of-war-vote` (`interactions.ts:612`) |

Plus `get_overlay_events` (SSE, `overlay.ts:74`), `ack_overlay_cursor`
(`overlay.ts:257`) and `get_overlay_tts_audio` (`overlay-audio.ts:12`). Nothing else in
the schema is addressable by an overlay session token.

**Consequence for planning:** the cheap half of §6 is finished. Every remaining module
costs at least a new `app_private` read function plus a new route, and eleven of the
thirteen cost more than that. Any plan that assumes slice 5 is "two more renderers" is
wrong before it starts.

**Second finding, from the enum rather than the prose.** `0131`'s `module_key` check
constraint (L40–L48) already names all twenty modules, so the §30.3 module cap counts
them today. That is a cap, not an implementation — the catalogue string
`'reaction_cloud'` existing in a check constraint is the *only* occurrence of the word
"reaction" anywhere in `packages/db/migrations/`, `apps/api/src/`, `apps/web/app/` or
`services/`. The same is true of `sponsor`, `lobby`, `giveaway`, `tournament`,
`now_playing` and `soundboard`. Seven of the thirteen have literally no data anywhere in
the product except their own name in a cap.

---

## PART A — data-path audit of the thirteen remaining modules

| # | Module | Classification | Reason |
|:-:|---|---|---|
| 5 | Reaction Cloud | BLOCKED-DECISION | No reaction data exists; `HUB-07` absent; §19.5 mandates server-side sampling and rate-limiting but states no numbers |
| 6 | Safe Soundboard Alert | BLOCKED-EXTERNAL | No audio catalogue exists at all; creator audio is held shut by the §18.3 gate (`MED-15`), whose scanner is still a no-op (`MED-14`) |
| 9 | Stream Mission Card | NEEDS-SCHEMA | Nothing exists, but the record is purely internal — creator text plus a deadline, no money, no viewer data |
| 10 | QR Smart Card | BLOCKED-DECISION | Its visibility rule names Clutch Mode (`CMP-17`), which is absent from the repository, and scene profiles, which do not exist |
| 11 | Sponsor Card | BLOCKED-DECISION | No sponsor schema anywhere; an exposure log is evidence a third party relies on, and §33.1 holds the Sponsor pack for exactly that reason |
| 12 | Moderator Status Card | NEEDS-READ-PATH | Held count and queue-paused state are both durable and channel-scoped today; no overlay session can read them |
| 14 | Vertical Stream Layout | BLOCKED-DECISION | §30.3 places "Vertical layout" at Pro; §15.4.3 places per-aspect-ratio variants at customisation level 2 (Creator). The two disagree |
| 15 | Stream Health Widget | BLOCKED-DECISION | "Creator-only" has no meaning on a surface composited into the broadcast; YouTube health is post-v1; the reliability snapshot is a platform-wide singleton |
| 16 | Lobby Status | BLOCKED-DECISION | The entire §16 Lobby Engine (`LOB-01`–`LOB-23`) is absent and is Phase 3; this card is a view of a subsystem nobody has built |
| 17 | Giveaway / Tournament Card | BLOCKED-DECISION | `GIV-*`/`TRN-*` are absent and Phase 3; `GIV-07` additionally gates any chance-based format on legal review |
| 18 | Now Playing | BLOCKED-EXTERNAL | No music-metadata source exists anywhere, and `AUD-11` marks a shared/discoverable music library "never build" |
| 19 | Chat | BLOCKED-EXTERNAL | The zero-quota path is the official embed (`CON-33`), which §9.1.1 forbids inside the Canvas; first-party ingestion is Phase 4 behind the YouTube quota grant |
| 20 | Media / Meme Queue | BLOCKED-DECISION | `MED-20` absent; the only catalogue that exists is Lottie JSON, and "curated" has no defined source |

### #5 Reaction Cloud

**Would render:** a sampled, non-identifying cloud of viewer reactions.
**Schema:** none. The string `reaction_cloud` in `0131` L42 is the only match for
"reaction" in the schema, API, web app or services.
**Read path:** none, and nothing to read.
**Outside code:** the reaction *set* is a product decision; the sampling window and
per-viewer rate limit are numeric limits this review may not invent, and §19.5's
"sampled and rate-limited server-side before they reach the canvas" states the
obligation without a number. Upstream, the capture surface is `HUB-07` ("Free
reactions, rate-limited and sampled", state `A`) on the Support Hub — a different
register row on a different surface, not Canvas work.
**Classification: BLOCKED-DECISION.**

### #6 Safe Soundboard Alert

**Would render:** an approved audio clip triggered by a supporter, with cooldown and
queue.
**Schema:** no audio asset table exists. `sticker_catalogue_entries`
(`0110` L66) is the only creator-facing asset catalogue, and it constrains
`mime_type text not null check (mime_type = 'application/json')` (`0110` L73) — Lottie
JSON, never audio. The one audio path that exists is TTS artifacts
(`get_overlay_tts_audio`, `overlay-audio.ts:12`), which is synthesised speech, not a
clip library.
**Read path:** none.
**Outside code:** `AUD-03` is state `A`. Creator-supplied audio is held shut by §18.3,
whose own table requires stage-2 malware scanning actually running (`MED-14`, still a
no-op), quarantine, immutable provenance, a takedown workflow with a named intake route,
a written repeat-infringement policy and one rehearsed end-to-end takedown drill
(`MED-27`) before the flag opens for anyone. A first-party clip library instead would
need clips somebody holds the rights to — an acquisition, not a build.
**Classification: BLOCKED-EXTERNAL** (the §18.3 gate, and rights to any first-party
catalogue).

### #9 Stream Mission Card

**Would render:** a creator-defined objective and a timer (§6 L1019). §8.5 describes it
in the Hub as the "Current stream mission card"; `HUB-11` is state `A`, phase v1.
**Schema:** none. Grep for "mission" across the schema and API returns only
`permission`/`admission` false positives.
**Read path:** none.
**Outside code:** nothing external. No money, no provider, no legal wording, no viewer
identity, no new personal-data class — the record is creator text plus a deadline,
written by the creator and read by their own overlay. §30.3 needs no new tier row
because the module already counts against "Master Canvas modules active" through
`0131`'s enum.
**The one thing that is not free:** §34 places the mission card in **Phase 3**
("community mechanics … transparent votes · mission card · milestone queue"), while
PRF-02 sits in Phase 0.5 opening into Phase 1. Building it now is a sequencing choice,
not a technical one.
**Classification: NEEDS-SCHEMA**, with a phase question attached (Q2).

### #10 QR Smart Card

**Would render:** a QR pointing at the creator's tip page, shown or hidden by scene,
safe zone or Clutch Mode.
**Schema, partially:** `tip_intents` (`0097` L13) and channel handles (`0087`, `0090`)
exist, and `/v1/public/channels/:handle` (`public.ts:107`) resolves a public channel —
but by handle, unauthenticated, and no overlay-session read returns the channel's own
public URL. `payment_order_qr_codes` (`0123` L18) is a per-payment-order provider QR,
bound to one intent; it is not a standing tip-page QR and must not be repurposed as one.
**Outside code:** the visibility rule §6 states is the blocker, not the QR. Clutch Mode
is `CMP-17`, state `A`, and the string "clutch" appears nowhere in
`packages/db/migrations/`, `apps/api/src/` or `apps/web/app/`. Scene profiles do not
exist. Slice 4 already refused this module for the same reasons; nothing has changed.
**Classification: BLOCKED-DECISION** (which existing state gates visibility, given
Clutch Mode is absent).

### #11 Sponsor Card

**Would render:** a scheduled sponsor placement plus an exposure event log.
**Schema:** none — `sponsor_card` in `0131` L43 is the only occurrence outside a
YouTube event translation unrelated to this module.
**Outside code:** the exposure log is the problem, not the card. §29 describes it as the
artefact that answers "did I do the sponsor read", and §33.1 holds the Sponsor pack
precisely because selling it early "produces a **document a creator forwards to a
sponsor or a CA** — being wrong there costs the creator, not just us." An exposure count
a creator invoices against is a measurement claim, and there is no authority stating what
counts as an exposure, how it is proven, or who may rely on it. §30.3 puts sponsor
reports in Studio only.
**Classification: BLOCKED-DECISION.**

### #12 Moderator Status Card

**Would render:** §6 L1022 — "Messages held", "safe mode on" — **never private content.**
**Schema, and this is the one module whose data is already durable:**

- **Held count:** `event_outbox_deliveries.status` includes `'held'`
  (`0001` L134), and the row carries `queue_id` → `alert_queues.channel_id`
  (`0001` L53–L55). Moderation itself is `ALQ-10`, state `U` — built and verified —
  through `alert_moderation_actions` with `action in ('approve','hold','suppress','replay')`
  (`0003` L52–L60) and `app_private.apply_moderation_action` (`0062` L88).
- **Queue paused:** `alert_queues.is_paused` (`0001` L57), already enforced across the
  dispatch guards (`0023` L56, L102, L155).
- **Precedent for the projection:** `get_companion_state` already computes exactly this
  shape for the creator — `pending_alerts integer` over outbox statuses
  (`0003` L238–L257, re-declared `0093` L116–L141).

**Read path: does not exist.** `get_companion_state` is reached by a creator/companion
session, never an overlay session. A new `app_private.list_overlay_moderator_status`
joining `overlay_sessions` → `alert_queues` → `event_outbox_deliveries` on the same
`token_fingerprint` / `revoked_at` / `expires_at` pattern every other `list_overlay_*`
function uses (`0105` L926–L943 is the canonical shape) is the whole server-side cost.
**Bounded-data posture (§12.7):** the projection is two integers and one boolean. No
message text, no viewer reference, no amount — which is also what makes §6's "never
private content" satisfiable by construction rather than by review.
**Outside code:** one gap. **"Safe mode on" is not a state this product has.** There is
no `safe_mode` column, flag or route anywhere in the schema or the API. §23.1 uses the
phrase for a Companion control ("one-tap Companion mute, skip, pause, emergency safe
mode") that is not built. `alert_queues.is_paused` is a *different* thing — a paused
queue, not a safety posture — and rendering one under the other's label would be
inventing a product rule inside a UI port, which is the exact fault slice 4 refused.
**Classification: NEEDS-READ-PATH**, with "safe mode" deferred behind Q1.

### #14 Vertical Stream Layout

**Would render:** "Narrow chat, compact goal, QR, reactions for mobile scenes" (§6 L1024)
— three of whose four named contents are themselves unbuilt and blocked (#19, #10, #5).
**Schema:** none. `master_canvas_modules` (`0131` L37) stores `channel_id`, `module_key`,
`enabled` and timestamps — no placement, no z-order, no aspect ratio. `widget_configs`
(`0105` L165) has `placement jsonb` but its `widget_type` check constraint
(`0105` L168–L171) is a closed list of seven legacy widget types that does not include
any Canvas module.
**Outside code — and this is a contradiction in the authority, not a gap in the code:**
§30.3 lists "Vertical layout | — | yes | yes | yes", i.e. **Pro and above**. §15.4.3
lists "**Per-aspect-ratio variants** (16:9, 9:16, 4:3) of one canvas | — | — | yes |
yes", i.e. customisation level 2, which §33.1 maps to **Creator**. A vertical variant of
one canvas is a per-aspect-ratio variant of one canvas. One of those two rows is wrong
and this review may not pick. Separately, `ALQ-19` ("Vertical / second-output canvas")
is state `A`, P2, and the placement/aspect configuration is the canvas designer, which
`PRF-02.md`'s own Boundaries section puts explicitly out of scope.
**Classification: BLOCKED-DECISION.**

### #15 Stream Health Widget

**Would render:** "Creator-only view of YouTube, payment, alert and OBS health"
(§6 L1025).
**Schema, piece by piece:**

- **OBS health exists, narrowly.** `0093` adds `obs_status_reported_at` to
  `companion_control_sessions` and its own header states the honesty position: it is a
  heartbeat treated as stale after 45 seconds, not a fact, and `mirror_reachable` /
  `stream_paired` are "modelled as always false" because those products report no
  liveness. `CON-34` confirms the source: stream health comes from the desktop helper,
  never a YouTube call. This is also the only lawful source — §6's own constraint and
  this review's brief both forbid anything resembling detection of external OBS layers.
- **YouTube health exists but is out of reach.** `youtube_channel_connections`
  (`0086` L79) and `get_youtube_connections` (`0086` L359) are creator-auth reads, and
  §32 keeps every YouTube capability post-v1 behind data scopes, a quota grant and chat
  scope.
- **Payment/alert health does not exist per channel.**
  `reliability_reconciliation_snapshot` (`0130` L34) is a **singleton** — `id smallint
  primary key default 1` with a `check (id = 1)` constraint (`0130` L44) — a
  platform-wide operations figure with no channel dimension at all. It cannot back a
  per-creator widget, and surfacing it to a creator would be showing them someone else's
  numbers.

**Outside code:** "creator-only" is undefined on a surface whose entire purpose is to be
composited into a broadcast. The Canvas has no non-broadcast rendering mode; placing the
module off the visible frame is a creator's manual act, not an enforceable property, and
promising "creator-only" for something we cannot keep off stream is a claim the product
cannot hold.
**Classification: BLOCKED-DECISION** (with a YouTube component that is separately
BLOCKED-EXTERNAL per §32).

### #16 Lobby Status

**Would render:** aggregate seats and queue only (§6 L1026, §16).
**Schema:** none — `lobby_status` in `0131` L47 is the only occurrence of "lobby" in the
schema or API.
**Outside code:** `LOB-01`–`LOB-23` are all state `A`, phase **P3**. `LOB-09` is
literally "Aggregate-only public overlay module" — this module is a register row of its
own, downstream of a seat/queue/eligibility/audit subsystem nobody has built. §33.1 has
settled the product questions (open FIFO default, seats governed by the Lobby Engine,
paid room-code unlocking dropped), so the blocker is not ambiguity — it is that
delivering the card means delivering §16.
**Classification: BLOCKED-DECISION** (whether PRF-02 may build §16 itself).

### #17 Giveaway / Tournament Card

**Would render:** entry state, draw status, bracket (§6 L1027, §17).
**Schema:** none.
**Outside code:** `GIV-01`–`GIV-07` and `TRN-01`–`TRN-06` are state `A`, phase **P3**.
`GIV-06` is the overlay row itself ("entry count, timer, consented winner, no address on
stream"), downstream of a deterministic seeded draw with recorded seed and entrant count
(`GIV-03`) and creator-promoter terms (`GIV-05`, phase `P3·G`). `GIV-07` holds any
chance-based format behind legal review in India, and §33.1 has already decided
free-entry and skill-based only, with the creator always the promoter and BharatStudio
never holding a prize. As with #16, the product decisions exist; the subsystem does not.
**Classification: BLOCKED-DECISION** (whether PRF-02 may build §17 itself).

### #18 Now Playing

**Would render:** track metadata, never audio (§6 L1028).
**Schema:** none, and no candidate source anywhere — no music integration, no player
state, no scrobble path, nothing in `services/`.
**Outside code:** a metadata provider that does not exist, under terms nobody has read.
§31.17 `AUD-11` marks "Shared or discoverable music library" as **`N | N`** — never
build — and §18.2 explains the posture it comes from: a library would make us a
distributor and the creator's rights attestation would stop being sufficient cover.
Slice 4 already refused this module for having no data source anywhere; that is
confirmed, not merely repeated.
**Classification: BLOCKED-EXTERNAL.**

### #19 Chat

**Would render:** embedded live chat (§6 L1029).
**Schema:** no chat message store exists. The YouTube work that does exist
(`0086`, `0091`, `0094`, `0099`) is connection, delivery and ingest-failure
bookkeeping, not chat content.
**The boundary that decides this module, stated plainly:** §33.1 records that "the
permitted client-side path is the IFrame Player API and the official chat embed"
(`CON-32`, `CON-33`), and `CON-33` adds "display only, never a data source." §9.1.1
forbids BharatStudio embedding any third-party browser-source URL, HTML, JavaScript, CSS
**or iframe** inside the Master Canvas — "Ever… There is no tier, no attestation and no
'advanced mode' that makes it acceptable." **So the one cheap chat path in the product is
the one path the Canvas may never use.** The remaining option is first-party ingestion,
which `CON-46` puts in Phase 4 and §32 gates on YouTube data scopes plus a quota grant,
and which would introduce viewer chat content as a personal-data class the overlay does
not carry today.
**Classification: BLOCKED-EXTERNAL.**

### #20 Media / Meme Queue

**Would render:** curated, approved assets only (§6 L1030).
**Schema:** `MED-20` ("Curated meme/media queue module") is state `A`. The only asset
catalogue that exists is `sticker_catalogue_entries` (`0110` L66), Lottie JSON only, with
creator packs (`0119` L57), staff review (`0122`) and a tip-attachment path
(`0119` L349) — a sticker attached to a tip, which is not a queue and has no
overlay-session read.
**Outside code:** "curated" has no defined source. First-party curation is an asset
acquisition; creator-supplied media is the §18.3 gate again (`MED-15` off, `MED-14` a
no-op). Queue semantics — who may enqueue, at what price, with what cooldown, and who
approves — are unstated, and every one of those is a numeric or product decision.
**Classification: BLOCKED-DECISION.**

---

## PART B — product, market, creator and streamer review

Official documentation only, every URL and access date recorded, fetch failures recorded
as failures rather than filled in with search synthesis. Where a finding came from a
search engine's summary of an official page rather than a direct fetch of that page, it
is labelled **search-derived** and is not treated as a verified primary quote. Nothing
below is a pricing, numeric-limit, provider-behaviour or legal-wording proposal.

### Sources actually reached

| Source | URL | Accessed | Result |
|---|---|---|---|
| StreamElements — Overlays docs | `https://docs.streamelements.com/overlays` | 2026-09-16 | Fetched |
| StreamElements — homepage | `https://streamelements.com/` | 2026-09-16 | Fetched |
| Streamlabs — Ultra | `https://streamlabs.com/ultra` | 2026-09-16 | Fetched |
| Streamlabs — pricing | `https://streamlabs.com/pricing` | 2026-09-16 | **Returned no content** |
| Streamlabs — Media Share support article | `https://support.streamlabs.com/hc/en-us/articles/360038335291-Media-Share` | 2026-09-16 | **HTTP 403** to automated fetch |
| OBS Project — vertical canvas kb | `https://obsproject.com/kb/vertical-canvas` | 2026-09-16 | **HTTP 404 — no such page** |
| OBS Project — 31.0 release notes | `https://obsproject.com/blog/obs-studio-31-0-release-notes` | 2026-09-16 | Search-derived only |
| OBS Forums — Aitum Vertical (third-party plugin) | `https://obsproject.com/forum/resources/aitum-vertical.1715/` | 2026-09-16 | Search-derived only |
| YouTube Help — Moderate live chat | `https://support.google.com/youtube/answer/9826490` | 2026-09-16 | Search-derived only |
| Twitch Help — Polls | `https://help.twitch.tv/s/article/polls` | 2026-09-16 | **HTTP 503** |
| Kick Help Centre — streamer articles | `https://help.kick.com/en/collections/3901863-for-streamers` | 2026-09-16 | Search-derived only |

**Discord, Instagram and WhatsApp were not fetched, and that is a scoping judgement
stated rather than an omission.** None of the thirteen modules reads from them: Discord
appears in §30.3 only as "Discord webhook alerts", and Instagram and WhatsApp only as
Social Relay destinations (§27, §31.26). No Canvas module in scope has a data path
through any of the three, so their documentation could not change a classification in
Part A.

### What the sources say, and what it means for the thirteen

**StreamElements Overlays** (`docs.streamelements.com/overlays`, accessed 2026-09-16)
names, of the modules in scope, exactly two: a **"Chat Overlay"** described as *"Show
your stream chat on your overlay"*, and **KappaGen**, *"Show chat emotes on stream"*.
Alongside these it lists AlertBox, a "Custom Widget" described as fully custom-coded, and
"labels, goals, and session widgets". The page names **no** soundboard, now-playing,
sponsor, stream-health, giveaway/tournament, QR or vertical/portrait overlay widget.

Two things follow, and they cut in opposite directions:

1. **KappaGen is the closest competitor analogue to #5 Reaction Cloud that exists in
   official documentation**, and it is sourced from *chat emotes* — i.e. from an ingested
   chat stream. Our #5 is specified from a different source entirely (Support Hub
   reactions, `HUB-07`), which is a genuinely better privacy position (§6: "non-identifying")
   but is also why it cannot be cheap: we do not get the source for free the way a
   chat-ingesting competitor does.
2. **StreamElements' "Custom Widget" is fully custom-coded**, which is precisely the
   capability §9.1.1 forbids us to offer inside the Canvas. That asymmetry is real and
   permanent, and it is worth stating internally so nobody proposes closing it: a
   creator-authored JavaScript widget is a feature we have decided not to have. §9.2's
   declarative Canvas Packages are the answer we chose instead, and the honest framing is
   "a different trade", not "parity".

**Streamlabs Ultra** (`streamlabs.com/ultra`, accessed 2026-09-16) states **"Starting at
$15.75/mo"** and lists, among others, *"Full access to thousands of stream overlays and
widget themes including Reactive Overlays"*, *"Custom named Cloudbot"*, *"Up to 10 stream
automations"*, *"1,000 Sidekick interactions/month"*, *"10GB Cloud Storage"* and *"Collab
Cam for up to 11 guests or cameras"*. **A correction worth recording:** a search summary
during this review reported Streamlabs Ultra at "$27/month or $189/year". That figure was
**not** on the page when fetched and is recorded here as unverified, not adopted. The
primary-source figure is the "Starting at $15.75/mo" above, and `streamlabs.com/pricing`
returned no content at all, so this review does not claim to have established Streamlabs'
full price ladder.

**StreamElements' homepage** (accessed 2026-09-16) displays no paid tier at all and
positions alerts and widgets as **"100% FREE forever"**, naming overlays, chatbot,
alerts, tipping, merchandise and *sponsorship offers*. Two consequences:

- **Tier-benefit framing.** Against a competitor whose overlay widgets are free and whose
  revenue comes from elsewhere, tier value cannot be "you get modules". §33.1 already
  reached this conclusion independently — "**customisation depth, not relocated
  features, is how Studio earns its price**" — and the §30.3 module cap (2/5/12/all) is
  the one place slice 5 touches it. Nothing in this review proposes changing that cap.
- **Sponsorship.** StreamElements offers sponsorship *matching* as a marketplace, not a
  sponsor-exposure-log widget. That is a different business, and it does not tell us
  what our §6 #11 exposure log should record — which is exactly the decision Part A
  leaves open (Q11).

**OBS and vertical output (#14).** There is **no** official OBS kb page at
`obsproject.com/kb/vertical-canvas` (HTTP 404, accessed 2026-09-16). Search over
`obsproject.com` and `github.com` surfaced the OBS Studio 31.0 release notes and the
third-party **Aitum Vertical** plugin (`obsproject.com/forum/resources/aitum-vertical.1715/`,
`github.com/Aitum/obs-vertical-canvas`) — i.e. **vertical canvas in OBS is, on the
evidence reachable today, a third-party plugin rather than a documented native feature.**
This is recorded as search-derived; the release notes themselves were not fetched and no
claim is made about what OBS 31 or 32 does or does not ship natively. The relevance is
that #14's switcher story is not "OBS already does this and we must match it", and
nothing here establishes a performance budget for a second canvas either — §19.4's
numbers remain unmeasured and RT-07 remains Blocked.

**YouTube live-chat moderation (#12 and #19).** YouTube Help's "Moderate live chat"
(`support.google.com/youtube/answer/9826490`, accessed 2026-09-16, **search-derived**)
describes creator-set moderation of None / Basic / Strict, with held messages shown in
the chat feed for the creator to show or hide, and — the detail that matters — *if the
creator takes no action the messages remain hidden from viewers*. Two readings for us:

- **The "held" concept is familiar to creators**, which is in #12's favour: a card
  reading "3 held" needs no teaching.
- **It is a different "held" from ours.** YouTube holds *chat messages*; our
  `event_outbox_deliveries.status = 'held'` holds *paid alert deliveries* awaiting a
  moderator. Labelling ours "messages held" risks a creator reading it as their YouTube
  chat backlog, which we do not have and (per #19) cannot have before Phase 4. The label
  is a copy decision the implementer must not settle alone.

**Twitch** (`help.twitch.tv/s/article/polls`) returned **HTTP 503** on 2026-09-16. No
Twitch finding is recorded, and none is inferred. The master-canvas runtime review
recorded the same class of failure for Zendesk-hosted support pages; this is that pattern
continuing, not a new obstacle.

**Kick** (help centre, accessed 2026-09-16, **search-derived**): Kick's own streamer
guidance describes alerts as *powered through services like Streamlabs or
StreamElements*, and its browser-based "Web Go Live" offers scenes and widgets. The
switcher-friction reading: **Kick creators are already in the per-widget browser-source
pattern §6 targets**, because Kick points them at exactly the two products that produce
it. That supports §6's framing for Kick as it does for Streamlabs — and, per the
master-canvas review and §6's own competitive-accuracy note, still not against
StreamElements' Overlay Editor. `RT-09` continues to block publishing any of this.

### Evaluation against the criteria set for this review

| Criterion | Finding for the thirteen |
|---|---|
| **Switcher friction** | Lowered only where a switcher's current setup is per-widget (Streamlabs, and Kick via Streamlabs/StreamElements). Unchanged for StreamElements. None of the thirteen changes this; #12 and #9 add capability a switcher does not currently have rather than removing setup steps |
| **Creator value** | #12 is the only one of the thirteen that answers a question a creator asks mid-stream ("is anything stuck?") using data we already hold. #9 answers a question they currently answer by typing into a scene text source |
| **Tier benefits** | Unchanged and should stay unchanged. The §30.3 cap already counts all twenty modules (`0131` L40–L48); no module in the thirteen needs a new tier row, and §12.6's "never tier-gate storing, viewing, searching, fetching or exporting durable creator records" means a mission or a module configuration is stored at every tier even when the cap prevents rendering it |
| **Latency** | Unmeasured, and unmeasurable by this task. §19.4's budgets need RT-07 (Blocked) evidence in real OBS on real hardware. Nothing in this review is offered toward any number in that table |
| **Moderation** | #12 is a moderation-*status* surface and must stay counts-only; §6's "never private content" and `ALQ-11`'s role-scoped reads both point the same way, and the projection proposed in Part A carries no message text, viewer reference or amount |
| **Monetization** | None of the thirteen introduces a money path. #11, #17 and #20 would, which is part of why all three are blocked |
| **Accessibility** | The runtime's `prefers-reduced-motion` handling and slice 4's ruling that a reduced-motion alternative must be *perceivable*, not merely shortened, bind any new renderer. A count that changes without animation is already compliant; a mission timer is the case that needs care |
| **Localisation** | §15.4.3's per-text-role **Indic script fallback order** remains unimplemented product-wide and is explicitly out of PRF-02 per the owner's 2026-09-16 ruling. Both recommended modules render creator-authored text (a mission objective) or short labels, so the same constraint the owner placed on slices 1–4 applies: the render path takes the font/fallback value as data and hard-codes no single family. This is a carried gap, not a closed one |
| **Reliability** | The one shared connection and the two-failures-stays-down error boundary already cover a new module. Nothing in #12 or #9 requires a second connection, a second session, or an acknowledgement path — both are snapshot modules using `subscribe()`, never `subscribeToEvents()` |

---

## PART C — recommended slice 5 scope

### Recommended

**1. #12 Moderator Status Card — held count and queue-paused state only.**
It is the only module of the thirteen whose data is already durable, already
channel-scoped and already verified (`ALQ-10`, state `U`); the entire server-side cost is
one `list_overlay_moderator_status` function following the `0105` L926 pattern and one
route beside the existing `/v1/overlay-widgets/:overlayId/*` family. The projection is
two integers and a boolean, which satisfies §12.7 by construction and makes §6's "never
private content" a property of the query rather than a rule a reviewer has to enforce.

**2. #9 Stream Mission Card — conditional on Q2 only.**
It is the only module of the thirteen that needs schema yet needs no owner product,
pricing, legal or provider decision: a creator-authored objective and a deadline, written
and read by the same channel, with no money, no viewer identity and no new personal-data
class. **It carries exactly one open question** — §34 places the mission card in Phase 3
— and that question is a yes/no the owner can close in one line. **If the answer is no,
slice 5 is #12 alone**, and this review recommends shipping one complete module over
padding the slice.

**No third module is recommended, and that is the honest answer rather than a gap in the
audit.** Eleven of the thirteen have an owner decision, an absent subsystem or an
external gate in front of them, and the brief's own standard — "no owner decision
outstanding" — excludes every one. A third pick would have to be manufactured by guessing
one of the fifteen questions below, which is the failure slice 4 was written to prevent.

**One adjacent option the coordinator may prefer over #9**, offered as a note rather than
a pick because it is not one of the thirteen: **#8 Challenge Board's "completed" lane.**
Slice 4 deferred "next" *and* "completed" together on an ordering question, but that
question is only genuinely open for "next" — there is no priority or queue column, so
"next" has no defined meaning. "Completed" has an obvious ordering (most recently
completed first) available from existing columns. Whether reopening a shipped module
beats starting a new one is a scope judgement for the coordinator, not a finding.

### Checked against the standing constraints

| Constraint | #12 | #9 |
|---|---|---|
| Never tier-gate storing/viewing/searching/fetching/exporting durable creator records (§12.6) | Reads existing records; stores nothing new | The mission record is stored, editable and exportable at **every** tier; only rendering counts against the §30.3 module cap, exactly as `0131` already treats the other nineteen |
| §12.7 bounded data | Two integers, one boolean | One row: title, objective, optional deadline |
| §9.1.1 no third-party code on the overlay | None; first-party render of our own data | None |
| No spyware-like detection of external OBS layers | Reads only our own queue state; this constraint is part of why #15 is rejected, not a risk here | Not applicable |
| Local verification is never production/provider/store/legal/device/network/release readiness | Any evidence produced is local only; RT-07 stays Blocked and §19.4's numbers stay unclaimed | Same |

### Rejected, and why

| Module | Rejected because |
|---|---|
| #5 Reaction Cloud | The reaction set and the sampling/rate-limit numbers are owner decisions (§19.5 states the obligation without a number), and the capture surface is `HUB-07` on the Support Hub — a different register row, not Canvas work |
| #6 Safe Soundboard Alert | No audio catalogue exists (`0110` L73 constrains the only catalogue to `application/json`), and creator audio is behind §18.3 with `MED-14` still a no-op and `MED-27`'s takedown drill unrehearsed |
| #10 QR Smart Card | Clutch Mode (`CMP-17`) is absent from the repository and scene profiles do not exist, so §6's visibility rule cannot be implemented as written. Same refusal as slice 4, re-verified |
| #11 Sponsor Card | The exposure log is a measurement a creator would invoice against, with no authority defining what counts as an exposure; §33.1 holds the Sponsor pack for this reason |
| #14 Vertical Stream Layout | §30.3 and §15.4.3 disagree on its tier, the placement/aspect schema does not exist, and the canvas designer is explicitly out of PRF-02's scope |
| #15 Stream Health Widget | "Creator-only" is unenforceable on a broadcast-composited surface; the reliability snapshot is a platform singleton (`0130` L34, L44) with no channel dimension; YouTube health is post-v1 |
| #16 Lobby Status | Delivering the card means delivering §16 (`LOB-01`–`LOB-23`, all state `A`, Phase 3) |
| #17 Giveaway / Tournament Card | Delivering the card means delivering §17 (`GIV-*`/`TRN-*`, Phase 3), and `GIV-07` gates chance-based formats on legal review |
| #18 Now Playing | No metadata source exists anywhere and `AUD-11` marks a music library "never build". Slice 4's refusal confirmed |
| #19 Chat | The only zero-quota path (`CON-33`, the official embed) is the one §9.1.1 forbids inside the Canvas; ingestion is Phase 4 behind the quota grant and introduces a personal-data class the overlay does not carry |
| #20 Media / Meme Queue | "Curated" has no defined source, the only catalogue is Lottie JSON, and queue semantics (who enqueues, at what price, with what cooldown) are all unstated |

### Owner questions — each is a single question, none may be answered by the implementer

1. Does "safe mode on" in §6 module #12 mean the existing `alert_queues.is_paused`
   state, or a separate control that does not exist in the schema today?
2. May PRF-02 slice 5 build §6 module #9 Stream Mission Card now, given §34 places the
   mission card in Phase 3?
3. What are the maximum objective-text length and the maximum mission duration for §6
   module #9?
4. Should §6 module #12's held-count label read "messages held" as §6 writes it, given
   that the underlying state is held *alert deliveries* and not chat messages?
5. Which reactions may a viewer send for §6 module #5, and what are the server-side
   sampling window and per-viewer rate limit §19.5 requires?
6. For §6 module #6, is the soundboard catalogue first-party audio whose rights
   BharatStudio holds, or creator-uploaded audio behind the §18.3 gate?
7. For §6 module #10, which existing state gates QR visibility, given Clutch Mode
   (`CMP-17`) is absent from the repository and scene profiles do not exist?
8. For §6 module #11, what event counts as a sponsor exposure, and who may rely on the
   exposure log as evidence?
9. Is Vertical Stream Layout available from Pro (per §30.3's "Vertical layout" row) or
   from Creator (per §15.4.3's per-aspect-ratio variants at customisation level 2)?
10. For §6 module #15, how is "creator-only" enforced on a surface that is composited
    into the broadcast?
11. Which per-channel payment and alert health figures may §6 module #15 display, given
    `reliability_reconciliation_snapshot` is a platform-wide singleton?
12. May PRF-02 build the §16 Lobby Engine schema itself, or does module #16 wait for the
    Phase 3 Lobby task?
13. May PRF-02 build the §17 giveaway and tournament schema itself, or does module #17
    wait for the Phase 3 task?
14. For §6 module #19, is the Canvas chat module first-party-rendered ingested chat
    (Phase 4, quota-gated), given §9.1.1 forbids the official embed inside the Canvas?
15. For §6 module #20, does "curated, approved assets" mean a first-party catalogue, or
    creator uploads behind the §18.3 gate?

---

## Scope this review did not cover

- **No code was written, and no file under `bharatstudio-alerts/`,
  `bharatstudio-crons/` or any migration was created or modified.** This record is the
  only file written.
- **No performance, latency or budget claim is made.** §19.4's numbers need RT-07
  evidence in real OBS on real hardware; RT-07 is Blocked and nothing here is offered
  toward it.
- **No independent review occurred.** This is a single review-only pass; the owner's own
  disposition is still required, and PRF-02's register letter remains Opus's to assign
  per that task's own rule.
- **Twitch was not evaluated** — its polls documentation returned HTTP 503 and no
  substitute source was accepted. **Streamlabs' full price ladder was not established** —
  `streamlabs.com/pricing` returned no content. **Streamlabs Media Share** — the closest
  competitor analogue to §6 module #20 — **was not read**, its support article returning
  HTTP 403 to automated fetch. These are gaps, not findings.
