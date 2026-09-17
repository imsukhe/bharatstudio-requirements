# The remaining eight §6 modules, three standing questions, and a v1 scope amendment

**Date:** 2026-09-17
**Owner:** Sukhdev Singh
**Status:** `Approved` (owner decisions), except where a row below says `Blocked`
**Authority:** `FULL-PRODUCT-DEFINITION.md` §4.2, §4.2.1, §6, §9.1.1, §12.6.2, §12.7, §12.10, §19.6, §30.3, §34 · `active/launch/00_LAUNCH_SCOPE_AUTHORITY.md` · `active/launch/01_MASTER_RELEASE_AUTHORITY.md` · `active/launch/05_SUPPORT_AND_EXTERNAL_EVIDENCE_REGISTER.md` · `active/launch/06_BACKEND_GAP_REMEDIATION_AUTHORITY.md` · `AUD-11`, `CMP-17`, `CST-08`, `GIV-07`, `MED-20`
**Predecessors:** `reviews/2026-09-16-prf-02-slice-6-owner-decisions.md` · `reviews/2026-09-16-prf-02-slice-5-scope-review.md`

The slice-5 scope review classified thirteen remaining §6 modules and found **zero**
buildable, because every one sat behind an owner decision or an absent subsystem. Slice 6
cleared five. This record clears the remaining eight, answers the three questions that had
been carried forward, and records one amendment to a launch authority.

Every decision below names its **reuse anchor** — the already-decided value or already-built
mechanism it rests on. Where a number would be needed, it comes from something already
decided or from the creator. Nothing here invents a limit, a price, a provider behaviour, a
legal wording or a retention window.

---

## Part 1 — The eight modules

### 1. Safe Soundboard (§6 #6): two sources, and no review before a creator's own clip plays

**Decision.** Sound comes from **both** a first-party clip set we author **and** creator
uploads. A creator's own uploaded clip plays without any review step.

**Reasoning recorded, because this is the part that will be questioned later.** A creator
uploading to their own soundboard is publishing their own content onto their own stream,
which is exactly what every other creator-authored asset in this product already does. A
review gate would need a reviewer, and naming a queue nobody staffs is worse than having no
gate at all — it converts an honest "we do not review this" into an implied promise that we
do.

**Reuse anchor.** The creator-pack upload and asset-storage path built for the sticker
catalogue (`sticker_catalogue_entries`, migration `0110`) and the media storage rules in
§19.1 (GCS/CDN, Postgres holds metadata only). Retention follows the uniform policy
(§12.6.2), not the storage tier — §19.1 already states this.

**What this does NOT authorise.** No takedown flow, no reporting surface, and no automated
content scanning — none of those were decided, and none may be implied in UI copy. Copy must
not claim clips are "safe", "approved", "checked" or "reviewed". The module's name is
historical; it describes the *playback* being safe for a broadcast, not the *content* being
vetted.

**Still open, and not blocking the build.** The duration and file-size caps have no decided
value and no honest reuse anchor — there is no existing audio-duration limit anywhere in the
register. They ship **configured but unset**, which for an upload path means the upload
control is inert until a cap exists. First-party clips are unaffected and play from day one.

---

### 2. QR Smart Card (§6 #10): standalone, one destination, one toggle

**Decision.** The creator sets one destination and one label. The card shows or hides on a
single toggle. No scene profiles, no Clutch Mode dependency.

**What this closes.** The slice-5 review classified #10 `BLOCKED-DECISION` on `CMP-17`
(Clutch Mode, absent) and on a scene-profile system that does not exist. Neither is needed
for a card that has exactly one state and one destination.

**Forward compatibility, deliberately.** A single-destination card can later gain scene
awareness by being *selected by* a scene profile. Nothing built here has to be unwound when
`CMP-17` lands, because the module holds no scene concept to conflict with one.

**What this does NOT authorise.** No destination allow-list, no link shortening, no scan
counting, and no claim about how many people scanned anything.

---

### 3. Sponsor Card (§6 #11): it renders, and it counts nothing

**Decision.** The card displays the sponsor. Nothing is counted, nothing is stored, and no
number is ever shown to anyone.

**Reasoning recorded, because the cheaper option was rejected for a specific reason.** An
"internal only, not billable" counter was considered and declined. Any number we render will
eventually be screenshotted into a sponsorship negotiation, and at that moment a label saying
it is not an auditable metric protects nobody. The two definitions this module was blocked on
— what counts as an exposure, and who may rely on the log — both stop existing once nothing
is counted.

**What this closes.** #11 was `BLOCKED-DECISION` and legal-adjacent. It is now buildable with
zero legal surface.

**What this does NOT authorise.** No exposure log, no impression metric, no duration
accounting, and no sponsor-facing reporting of any kind. Building one later is a new decision
requiring legal review, not an extension of this one.

---

### 4. Vertical Stream Layout (§6 #14): one fixed variant now

**Decision.** Ship a single fixed 9:16 arrangement with no variant selection.

**Risk accepted, and stated.** `CST-08` (the layout-variant system, Phase 2) may later define
variants in a shape this fixed layout does not fit, in which case this becomes a special case
to unwind. The owner accepted that trade in exchange for having vertical output in v1.

**Reuse anchor.** The Master Canvas runtime's existing module contract — one transport, one
rAF loop, `transform`/`opacity` only. A fixed layout is a pure renderer like the other twelve
and introduces no new runtime concept.

**Tier.** Pro (§30.3 binding, decided 2026-09-16).

---

### 5. Stream Health Widget (§6 #15): it leaves the canvas

**Decision.** Health is built as a **dashboard panel**, not a canvas module, and is **dropped
from the §6 catalogue**.

**Reasoning.** The module was specified as creator-only, but the Master Canvas is a broadcast
surface — everything on it is visible to every viewer, so "creator-only" cannot be enforced
there by any means. Rather than weaken the widget until it is safe to broadcast, it moves to
the surface where authentication is real.

**This agrees with an authority that already said so.** §4.2.1 records stream health as
coming from the desktop helper / OBS WebSocket at **zero quota** and notes that "a large part
of 'is my stream healthy' never involves YouTube". Nothing in that row ever placed health on
the overlay.

**Consequence.** The §6 catalogue is now **nineteen** modules, not twenty. The Master Canvas
target moves from twelve-of-twenty to twelve-of-nineteen without a line of code changing.

---

### 6. Now Playing (§6 #18): `AUD-11` stands

**Decision.** The existing `AUD-11` decision — never build — stands. The row is closed as
`Never`.

**No new record was needed and none is created.** The authority already says this; this entry
exists only so the §6 row stops being carried as an open question.

**What this does NOT authorise.** Not even a creator-typed "now playing" text field. That was
offered and declined. Anything in this space is a new decision that must overturn `AUD-11`
explicitly and name a metadata source.

---

### 7. Chat (§6 #19): it was never a canvas module, and the authority already said so

**Finding, corrected here.** This module had been carried as `BLOCKED-EXTERNAL` on the
grounds that the zero-quota path is the official embed and §9.1.1 forbids it. That reading was
too broad. **§9.1.1 scopes strictly to "inside the Master Canvas."** §4.2.1 already decides
the whole question:

| Need | Overlay | Dashboard | Quota |
|---|---|---|---|
| A creator reading their own live chat | **Not on the overlay** — chat display belongs in the dashboard and Companion | YouTube's official live-chat embed | **None** |
| Chat as *data* — commands, `!tip`, bot replies, moderation actions | **Never** | Server-side ingestion only | The expensive one |

§4.2.2 likewise permits the official chat embed on the **tip page** at zero quota
("Open live chat | Mounts YouTube's official chat embed | None").

**Decision.** #19 is closed as **not a canvas module**. Chat display lives in the dashboard,
the Companion and the tip page, via the official embed, at zero quota, exactly as already
written. Chat *ingestion* is governed by Part 3 below.

---

### 8. Media / Meme Queue (§6 #20): creator-only, and `MED-20` says so

**Decision.** The creator queues their own media. Viewers cannot submit. `MED-20` is written
to record exactly this.

**Reasoning.** Viewer submission would make us a host of viewer-supplied media at broadcast
volume, carrying the same rights, storage and takedown posture as the soundboard uploads but
at far higher volume and with no relationship to the person submitting. Creator-only has none
of that.

**What this does NOT authorise.** No submission endpoint, no approval queue, no viewer-facing
surface of any kind. Adding one is a new decision, not an extension.

---

## Part 2 — The three standing questions

### 9. Reaction-send retention: the shortest class, which means we do not retain sends

**Decision.** Reaction sends are classified into the §12.6.2 schedule under **"Raw chat logs
and other high-volume, low-value streams"** — the shortest class. They are **not retained
individually**. What persists is the aggregate count and the rate-limit window, which expires
on its own.

**How this follows from the policy rather than from a number I chose.** §12.6.2 makes
retention a schedule **by data class**, uniform across tiers, where each window "is a legal or
product number, not a pricing one". The window for the shortest class is set by the
privacy/legal gate, which is **Open** in `05_SUPPORT_AND_EXTERNAL_EVIDENCE_REGISTER.md`. So
the class is decided and the number is not available. §12.6.2 then names the lever for exactly
this situation: high-volume low-value streams are managed by **"what we choose to ingest and
index at all"**, uniformly, for everybody. Not writing a per-send row is that lever applied.

**Reuse anchors.** §19.6 derive-don't-store (aggregates computed, never counted into a
column); §12.10's rule that we "snapshot the evidence at action time, do not retain the
firehose"; the existing `reaction_sender_rate_limits` window (migration `0141`), which already
expires without a retention policy of its own.

**Why this is also the safe direction.** With the channel-wide cap removed (2026-09-16), write
volume scales with audience size. Not writing the row removes that scaling entirely. Retaining
less is always reversible; retaining more requires the gate that is still open.

**Cost, stated.** We lose the ability to investigate an individual abuse incident after the
fact. The per-sender rate limit remains the live defence. The known residual stands: a
cookie-discarding client evades sender keying, which is inherent to cookie keying and was
recorded when `0141` landed.

---

### 10. §30.3 tournaments: standings follow tournaments

**Decision.** The Studio-only classification of "Tournament standings" is a **defect**.
Standings are available wherever tournaments are — **Creator+**.

**Reasoning.** §30.3 carried both "Tournament standings — Studio" and "Tournaments — single
elim, up to 8 — Creator+". Both cannot hold. A bracket whose standings cannot be shown is not
a feature, and the alternative readings both reduce something already offered.

**What this does NOT authorise.** No change to the bracket size (single elimination, up to 8),
and no change to `GIV-07`, which still blocks chance-based formats pending legal review.

---

### 11. Events Pack: any tier may buy it, Free included

**Decision.** The Events Pack may be purchased by any tier, including Free. The entitlement
built in migration `0140` (`app_private.events_pack_entitled`) may now be granted.

**Consistency checks recorded.** Buying happens on the website, never in the app — the
standing rule holds and nothing here changes it. The pack grants **live surfaces only**; it
never gates storing, viewing, searching, fetching or exporting a creator's own durable records
(§12.6, CTL-14, PCK-12), and it never charges to restore access to previously accepted data.

**What this does NOT authorise.** No price. The pack's price is a pricing decision that
belongs in a launch authority, not here, and the grant mechanism works without one.

---

## Part 3 — Amendment: YouTube moves into v1

**Decision.** `00_LAUNCH_SCOPE_AUTHORITY.md` is amended to admit YouTube chat ingestion,
Super Chat / Super Sticker ingestion, and channel / live-stream lookup into **v1**.

**Scope of the amendment, stated precisely because it was not enumerated in the instruction.**
The v1 exclusion line reads "YouTube channel/data ingestion, live polling, SuperChat/membership
views and catch-up summaries." The owner's instruction named chat ingest, Super Chat / Super
Sticker ingest, and channel and live-stream lookup. It did **not** name membership views or
catch-up summaries, and those **remain excluded from v1**. This is a deliberate narrow reading:
widening later is a safe change, and the record is here so the owner can correct it in one
line if the intent was broader.

**Consequence, stated plainly and not softened.** v1 now depends on two external approvals
that are **Unfiled** in `05_SUPPORT_AND_EXTERNAL_EVIDENCE_REGISTER.md`:

| Prerequisite | Register status |
|---|---|
| Google OAuth app verification — the YouTube read scopes **and** the high-sensitivity chat-write scope | Unfiled |
| YouTube Data API quota sufficiency for projected concurrent live-chat polling | Unfiled |

Neither can be filed, accelerated or predicted from here. v1's ship date is now partly
Google's. Both move from Phase-4 gates to **v1 launch blockers** in `L10`. The standing rule
at §4.4.6 is unchanged and still binding: **the YouTube connector is locally proven only**, and
nothing built under this amendment may be represented as provider-ready, quota-verified or
production-ready.

### 3a. The broker boundary — new, and not previously written anywhere

**Decision.** The creator's Google refresh and access tokens **never leave the server**. No
client — web dashboard, Android Companion, iPad, Moderator Console, tip page — ever receives a
Google credential. The backend issues its own narrow, short-lived BharatStudio token instead,
carrying only what that client is permitted to do:

```
{ "channelId": "…", "role": "moderator", "canReadChat": true, "canModerate": false, "expiresAt": "…" }
```

**Why this needed recording.** §4.2 already says no *surface* ever calls YouTube, and that the
server fetches once and fans the result out. It does not say that no surface may *hold the
credential*. That is the security half of the same rule, and it was missing. A Google token
represents the creator's entire Google account; it is not a safe session token for a moderator
or a viewer. Keeping it server-side preserves central revocation, audit, quota control and
scope enforcement — all four of which are lost the moment a token is copied to a device.

**Relationship to Google Sign-In.** Sign-in stays exactly as the authority has it —
authentication only, requesting no YouTube scopes. Connecting YouTube is a **separate,
deliberate OAuth grant** the creator makes, not a widening of the sign-in scope. The amendment
below preserves that split rather than deleting the line.

### 3b. No impersonation — new, and not previously written anywhere

**Decision.** BharatStudio never posts to YouTube chat using the creator's token on a viewer's
behalf. A viewer who posts must authorise their own Google account. The creator's credential
may not be used to make anyone else appear to speak as the creator.

**Scope for v1.** No viewer-posting path ships. The tip page gets the embedded player, the
read-only public chat projection and tipping. Posting is done by opening YouTube. A viewer
OAuth flow is a later, separate decision.

### 3c. What every surface may receive

**Decision.** One server-side ingestion per channel, fanned out as a **projection per surface**,
each carrying only what that surface is permitted to see — the §12.7 rule applied to an external
provider, which is what §4.2 already says.

| Surface | Receives | Never receives |
|---|---|---|
| Creator dashboard, Companion, Moderator Console | Full authenticated chat and control feed, scoped by role | Any Google token |
| Public tip page (`/tips/{publicCode}`) | Live status, embedded player, public chat messages, live indicator, tip activity | Google tokens · moderator fields · private author data · payment/provider detail · internal queue events |
| Master Canvas | Nothing from chat. Unchanged | Everything above |

**Role scoping is not new** and must reuse what exists: the v1 channel read permissions in
`00_LAUNCH_SCOPE_AUTHORITY.md` already define owner/admin, operator/moderator and viewer
boundaries, enforced by database projections and RLS, with the explicit rule that **UI hiding
alone is insufficient**.

---

## What is buildable now, and what is not

| # | Module / item | State | Blocker if any |
|---|---|---|---|
| 6 | Safe Soundboard | Buildable — first-party clips | Upload caps unset; upload control inert until a cap exists |
| 10 | QR Smart Card | Buildable | — |
| 11 | Sponsor Card | Buildable | — |
| 14 | Vertical Stream Layout | Buildable | — |
| 15 | Stream Health | Buildable as dashboard panel | Dropped from §6 |
| 18 | Now Playing | Closed `Never` | — |
| 19 | Chat (canvas) | Closed — not a canvas module | — |
| 20 | Media / Meme Queue | Buildable | `MED-20` to be written first |
| 9 | Reaction retention | Decided — no per-send row | — |
| 10 | §30.3 standings | Decided — Creator+ | — |
| 11 | Events Pack | Decided — any tier | Price undecided, not needed for the grant |
| — | YouTube ingestion (v1) | **Blocked-external** | Google OAuth verification · quota grant. Both Unfiled |

**No register letter is assigned by this record.** States are decided after audit, against the
worktree, not from a decision.
