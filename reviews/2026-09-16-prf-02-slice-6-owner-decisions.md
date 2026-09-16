# PRF-02 slice 6 — four owner decisions, and exactly what each one authorises

**Date:** 2026-09-16
**Owner:** Sukhdev Singh
**Authority:** `FULL-PRODUCT-DEFINITION.md` §6, §16, §17, §19.5, §30.3, §34, HUB-07, GIV-07
**Predecessor:** `reviews/2026-09-16-prf-02-slice-5-scope-review.md`, which classified all thirteen
remaining modules and named the exact blockers these decisions answer.

Each decision below is recorded with its **reuse anchor** — the already-decided value or
already-built mechanism it rests on — because the standing constraint is that no numeric limit,
provider behaviour, legal wording or pricing may be invented. Where a number is needed, it comes
from something already decided or from the creator, never from me.

---

## 1. Reaction Cloud (§6 #5): reactions are the existing sticker catalogue

**Decision.** A viewer's reactions are drawn from the curated sticker catalogue that already
exists — first-party entries plus staff-reviewed creator packs.

**Reuse anchor.** `sticker_catalogue_entries` (migration `0110`), the public sticker read path,
creator packs and the staff review queue are all built, tested and moderated today. No new asset
pipeline, no new rights question, no new moderation surface.

**What this closes.** The slice-5 review classified #5 `BLOCKED-DECISION` because nothing named
"reaction" exists anywhere in the schema. It does not need to: a reaction is a send of an
already-approved catalogue entry. HUB-07 ("Free reactions, rate-limited and sampled", `v1`, `A`)
is the register row this serves.

**What it does NOT authorise.** No new sticker may be added to the catalogue as part of this
work, no upload path, and no change to how packs are reviewed.

---

## 2. Reaction limits (§19.5): reuse the built rate-limit mechanism; the creator owns the number

**Decision.** Rate limiting reuses the per-channel mechanism already built and enforced in SQL.
The canvas's display ceiling ships **configured but unset**.

**Reuse anchors.**
- `rateLimitPerMinute` — creator-configurable, bounded 1–1000, in the channel config schema
  (`apps/api/src/domain/channel-config-schema.ts`) and enforced against a **one-minute window**
  in `packages/db/migrations/0032` and `0063`. The window and the bounds are already decided;
  the number inside them is the creator's.
- The **"configured but unset"** pattern already used for six other values: build the mechanism,
  read the value from config, and let unset mean today's behaviour — never a guessed default.

**Why this satisfies §19.5 without inventing anything.** §19.5 requires reactions to be "sampled
and rate-limited server-side before they reach the canvas" and that the cloud show "a
representative sample, never every event". The rate limit is the creator's existing per-minute
figure. The sample ceiling is a configured value that, left unset, imposes no ceiling beyond
§12.7's existing bounded-data rules — so shipping it unset changes nothing and shipping it set
changes exactly one thing.

**Hard constraint carried from §19.5 and §12.7.** The canvas must never fetch, render, subscribe
to or retain more reactions than it can display safely. Sampling happens **server-side**; the
client is never sent the full stream and then told to drop some.

**Non-identifying is a property of the query.** §6 #5 says "non-identifying". As with the
Moderator Status Card, that must be enforced by what the read returns — counts and catalogue
entry ids, never a viewer identifier — not by what the renderer chooses to draw.

---

## 3. Safe mode (§6 #12): a creator switch that holds every alert for review

**Decision.** Safe mode is an explicit per-channel moderation state the creator turns on. While
it is on, incoming alerts are routed to `held` rather than `ready`, for the creator or a
moderator to review.

**Reuse anchor.** The held path already exists end to end: `event_outbox_deliveries.status =
'held'` (migration `0001`), and the Moderator Status Card built in slice 5 already counts it.

**What this closes.** The owner previously decided safe mode is **not** `alert_queues.is_paused`,
so slice 5 shipped the held half only. This gives safe mode its own meaning and makes §6 #12
completable.

**Explicitly not this.** Safe mode is not automatic and is not triggered by any signal — no
spike detection, no rejection-rate heuristic. A creator turns it on and turns it off. Anything
automatic is a separate decision that has not been made.

---

## 4. Phase 3 subsystems (§6 #16, #17): PRF-02 may build the minimum schema for both

**Decision.** PRF-02 may build the minimum §16 Lobby and §17 Giveaway/Tournament schemas needed
to render modules #16 and #17, as it did for #9's mission record.

**Bounds that come with it.**
- **§16 Lobby Status is aggregates only** — seats and queue counts. §16 already says so. No
  per-viewer row, and nothing that correlates one visit to another.
- **§17 ships with no chance-based draw mechanic at all.** `GIV-07` gates chance-based formats on
  legal review, which has not happened. Entry state and bracket are buildable; the draw itself is
  not, and must not be approximated by "the creator records who won" — that invents a product
  surface nobody decided.

**This is the second and third deliberate override of §34's phase placement**, after #9. It is
scoped to these two modules' minimum schemas and authorises nothing else from Phase 3.

---

---

## 5. Events Pack entitlement (§16, §17) — decided 2026-09-16, after a contradiction surfaced

**The contradiction, found by reading §30.3 and §33 against the schema before dispatching any
work.** §30.3's tier table lists the Lobby Engine as included at Creator+ (`— | — | yes | yes`),
while §33's pricing lists an **Events Pack at ₹129/mo for Creator+** bundling "the Lobby and
tournament engine (§16, §17)". Those cannot both be true. And **no add-on or pack entitlement
exists anywhere in the schema** — the only mechanism is the four-tier
`channel_entitlement_versions` ladder. Neither §16/§17 tables nor any pack concept is present.

**Owner decision.** Both, and they are not in conflict once stated properly: **included at
Creator+, and additionally purchasable as a pack, because a Pro creator may well want to buy it.**

**What that means for the build, and why it needs nothing invented:**

- The entitlement check for §16/§17 is `tier in ('creator', 'studio')` **or** an active Events
  Pack grant.
- The pack-grant side is built as a check with **no grant path yet**. Nothing can currently make
  it true, so today's behaviour is exactly "included at Creator+" — the established
  **configured-but-unset** discipline, applied to an entitlement instead of a number. The
  mechanism exists, the value is absent, and absent means today's behaviour rather than a guess.
- **No price is implemented.** §33's ₹129/mo is the authority's existing figure and stays there;
  this work charges nothing, prices nothing and touches no billing surface.
- Purchasing, when it is built, is **website-only** per the standing constraint — never in-app.

**Left undecided, deliberately, because it was not asked and must not be assumed:** whether the
Free tier may also buy the pack. It does not block anything — nothing can grant the pack yet, so
the question is not yet reachable.

**A dependency the catalogue line hides.** §17.2 says tournaments are "built on the Lobby Engine
rather than beside it". So module #17 **depends on** module #16 and they cannot be built in
parallel; #16 lands first and #17 builds on it. Two further constraints come from §17 itself, not
from GIV-07 alone: §17.1's decision of 2026-09-13 already restricts giveaways to "free-entry and
skill-based formats only", and states plainly that **BharatStudio never holds, escrows, ships or
guarantees a prize**. §16's overlay is aggregate-only and must never show a room code, a
password, a player identifier or a Discord name; opted-in initials and avatars need an opt-in
mechanism that does not exist, so they are out of scope too.

## What remains blocked after these four

Unchanged: #6 Safe Soundboard (no audio catalogue; `sticker_catalogue_entries` is constrained to
`application/json`, and creator audio sits behind §18.3), #10 QR Smart Card (Clutch Mode `CMP-17`
absent, scene profiles do not exist), #11 Sponsor Card (what counts as an exposure, and who may
rely on the log, is legal-adjacent and undecided), #14 Vertical Stream Layout (tier resolved, but
the layout-variant system itself is CST-08, Phase 2), #15 Stream Health Widget ("creator-only" is
unenforceable on a surface composited into the broadcast), #18 Now Playing (no metadata source;
`AUD-11` marks a music library "never build"), #19 Chat (the zero-quota path is the official
embed, which §9.1.1 forbids inside the canvas), #20 Media/Meme Queue (`MED-20` absent).

Also still open: whether the replay endpoint should keep silently accepting `Last-Event-ID`,
reject it, or state in the contract that it is accepted and deliberately not a resume point.

## What this record is not

A set of product decisions and their reuse anchors. No implementation has been verified against
it yet, and nothing here is production, provider, store, legal, device, network or release
readiness. `GIV-07`'s legal gate is untouched and RT-07 remains Blocked.
