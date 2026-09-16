# Review — PRF-02 slice 2 implementation

**Date:** 2026-09-16
**Reviewer:** Implementing agent, self-review (independent review unavailable).
**Scope authority:** [`2026-09-16-prf-02-slice-2-scope-review.md`](2026-09-16-prf-02-slice-2-scope-review.md) —
that record is the product/market/creator/streamer scope decision for this slice, already
performed by a separate review-only agent and confirmed by Opus. **This record points at it
rather than repeating it.** What follows is the implementation record: what was built, the
transparency definition this task's §1(b) required, and what was found and corrected while
building.

## What was built

Exactly what the scope review's own approved scope named: module #3 (Tug-of-War Vote) and
module #4 (Boss Fight) on the slice-1 runtime, plus the RT-12 blind-spot closure the slice-1
implementation record referred onward. Full file list and evidence in
`active/tasks/PRF-02.md`'s "Slice 2" section and `tests/TC-PRF-02-slice-2-vote-boss-fight.md`
— not repeated here.

## The vote transparency definition, and why it is ours to write

The scope review recorded the finding precisely: Twitch Predictions is the only official
"transparent result" mechanic documented by any competitor, and it is free and points-only.
No official Streamlabs, StreamElements, Twitch or YouTube documentation describes a
real-money paid vote's fairness model. There was nothing to copy, so this task defined one
and is recording the definition and the reasoning here, not only in code comments, per this
task's own §1(b) instruction.

**Definition:** a two-sided paid vote's result bar is transparent when a viewer and a creator
can both see that the displayed state follows from what was actually paid — a bar that could
be made to show something other than the recorded totals is not transparent, no matter how
polished its animation.

**What this requires, concretely, and why each piece:**

1. **Derive, never store.** The bar's fraction and each side's exact amount are pure
   functions of the current fetched tally — `optionPaidFraction`/`totalPaidAmountPaise` in
   `tug-of-war-vote-logic.ts` take the tally as an argument and return a value; nothing in the
   module persists a running total across renders. This is §19.6's derive-don't-store rule and
   §12.7's bounded-data rule applied to this specific surface, not a new principle — but it is
   worth stating explicitly here because "transparent" is exactly the property that a hidden
   client-side counter would quietly violate: two viewers reloading at different times could
   see two different bars if either module cached a value instead of re-deriving it every
   time, and neither viewer would have any way to know.
2. **Show the amount, not only the percentage.** A percentage alone can visually round away a
   real difference (₹49 vs ₹51 both round to roughly 50/50). The exact rupee figure for each
   side is rendered alongside the bar (`tug-of-war-vote-module.ts`'s `leftText`/`rightText`),
   because the amount is the thing that was actually paid — the percentage is a derived
   convenience, not the fact being asserted.
3. **One join, three surfaces, never three derivations.** The creator's own dashboard tally
   (`app_private.paid_support_vote_tally`, migration 0108, unmodified), the standalone OBS
   paid-vote widget (`app_private.list_overlay_paid_vote_tally`, migration 0108, unmodified),
   and this Canvas module (`app_private.list_overlay_tug_of_war_vote`, migration 0132, new)
   all resolve to the same underlying `vote_payment_tags` → `payment_order_intents` →
   `payments`/`refunds` join. A creator checking their own dashboard against what the overlay
   shows is checking the SAME computation from two entry points, not two independent
   implementations that could quietly drift apart. This is the concrete meaning of "a viewer
   and a creator can both see the result follows from the record" — they are, literally,
   reading the same query.
4. **A resolved vote stays visible with the winner named.** Twitch Predictions posts the
   result to chat on resolution rather than making it disappear; this task's own analogous
   choice is that `list_overlay_tug_of_war_vote` continues to return the closed vote's row
   (with `resolved: true` and the correct `resolved_option_key`) rather than reverting to "no
   vote configured" the instant it closes — a result that vanishes the moment it is decided is
   not more transparent than one that stays visible, and hiding the outcome would remove
   exactly the information transparency exists to preserve.

**What this definition deliberately does not claim:** it does not claim the bar is provably
tamper-proof against a compromised server, does not claim any UI-level cryptographic proof,
and does not claim parity with any specific competitor mechanic (there being none to claim
parity with). It is a statement about where the displayed value comes from and how many
independent computations exist that could disagree — the failure mode this task's own
language flags ("a bar that can be made to show something other than the recorded totals is
not transparent") is a divergent client-side counter, and the design above makes that
specific failure structurally impossible rather than merely discouraged.

## The RT-12 scan finding two more gaps, and why both are closed here

Recorded in full in `active/tasks/PRF-02.md`'s "Slice 2" section and in the manifest file's
own top-level comment (`packages/db/explain-plans/required-queries.json`). Summary: building
a general-purpose scan (rather than one hand-tuned to the two functions this task's own
command named) found `app_private.list_overlay_lottie_assets` and
`app_private.list_overlay_widget_config` — both predating PRF-02 by several migrations — with
no EXPLAIN artefact either. Capturing artefacts for only the two named functions while the
scan's own honest output showed four missing would have shipped a still-red check, or would
have meant hand-tuning the scan to hide what it found — either one repeats the exact failure
pattern this task exists to close. Both are captured; `pnpm explain:check` reports
`15/15 plans current`.

## What this record is not

Not a repeat of the scope review's product/market/competitive research — that stands as
written in `2026-09-16-prf-02-slice-2-scope-review.md`. Not evidence of any §19.4 performance
budget — the five new EXPLAIN artefacts are, like the original ten, plan-shape change
detectors captured on an unsized local database, and each artefact's own body says so.

## Independent review

Unavailable — self-review only, stated plainly per §35.1 rule 6: a self-review never closes
an evidence row, and none is claimed closed here. This record and its evidence are
`Conditionally complete`, pending Opus's audit, exactly as `active/tasks/PRF-02.md`'s status
line for this slice states.
