# Review — PRF-02 slice 2 scope, before any code

**Date:** 2026-09-16
**Reviewer:** Review-only agent (no worktree changes), then orchestrator decision.
**Process:** This is step 3 of the operator's loop run as a **separate review-only pass**,
with scope confirmed before implementation. Slice 1 was run as a single pass and the
implementing agent wrote code before both its review and its records; that is why the gate
now exists.

## What the review changed

**Support Theater (§6 #1) is split into its own slice.** The proposed scope had it riding
alongside Tug-of-War Vote and Boss Fight. The review's argument, which the orchestrator
accepts: those two are low-blast-radius — Boss Fight is explicitly "a visual skin over an
ordinary support goal" (§6) and the paid-vote infrastructure already exists — whereas
Support Theater is **a rewrite of a 418-line imperative SSE/queue/acknowledgement component**
(`apps/web/app/overlay/[overlayId]/page.tsx`) into the runtime's pure
`activate`/`deactivate`/`render` shape. That is adapter work, not registration, and a
regression in it is **payment-visible**, not cosmetic. Reviewing it with the same attention
budget as a goal-bar skin, in one pass, is how a payment-path regression ships.

**A risk nobody had named.** Support Theater's acknowledgement-retry loop must become
idempotently `deactivate()`-able. "Deactivated mid-acknowledgement" is a state the existing
standalone page has never had to handle, because it was never a module that could be turned
off. That needs explicit test coverage in the slice that ports it.

## Findings recorded, not built

**The kill switch depends on something nothing enforces.** PRF-02's rollback is "leave the
standalone widget sources wired and remove the Canvas source" — stronger than anything a
competitor documents, since no vendor documents a live mid-stream rollback at all
(obsproject.com/kb/scene-collections, accessed 2026-09-16, covers import but says nothing
about doing it live). But it holds **only while a creator has not deleted their old
sources**, and nothing in the product currently discourages deleting them. Recorded as a
gap against the migration story; not this slice's to fix.

**A paid vote's transparency has no market precedent to copy.** Twitch Predictions
(dev.twitch.tv/docs/api/predictions/, accessed 2026-09-16) is the only official
"transparent result" mechanic found — results post to chat on resolution, and an unresolved
prediction auto-refunds after 24 hours — but it is **free and points-only**. No official
documentation from Streamlabs, StreamElements, Twitch or YouTube describes a **real-money**
paid vote's fairness model. §6's "two-sided **transparent** result bar" is therefore a
self-imposed bar with nothing to benchmark against, and what "transparent" must mean for
money is ours to define rather than copy.

**Moderation is already closed server-side, and nothing shows it.** `get_overlay_events`
filters `delivery.status in ('ready','displayed')`, so a held delivery never reaches an
overlay — the safety gate is correct. But no surface shows a creator queue depth or "X held".
That is the Moderator Status Card (§6 #12), out of this slice, and the review was right to
refuse to smuggle it in.

## Orchestrator decisions

**1. Support Theater → its own slice (slice 3).** Taken by the orchestrator, not referred:
both readings build the same modules and only the batching differs, so it is an engineering
risk call inside an approved authority rather than a product, pricing, legal, provider or
scope decision. Stated here so the owner can overrule it cheaply.

**2. RT-12's declared set is a manifest *and* a route scan.** The review proposed
`packages/db/explain-plans/required-queries.json` plus a scan of route files for the
`app_private` functions an overlay/widget-facing route actually calls. Both, not either: a
manifest alone fails the same way the directory listing does — it only knows what someone
remembered to add. The scan is what makes forgetting hard.

## Honesty of the review's own sources

The review recorded that Streamlabs' and StreamElements' support articles returned **HTTP
403** to automated fetch, so those two claims are search-engine synthesis rather than a
primary read, and it said so rather than presenting them as sourced. It also recorded two
genuine documentation gaps — no competitor documents a paid vote's transparency model, and
none documents a live mid-stream rollback — as gaps in the market rather than in its own
work. Both are the right call.
