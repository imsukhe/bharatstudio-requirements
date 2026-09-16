# Review — PRF-02 slice 4 scope, before any code

**Date:** 2026-09-16
**Reviewer:** Review-only agent (no worktree changes), then orchestrator decisions.
**Recorded retrospectively** — the findings reached the implementer inside the coordinator's
command text rather than as a file. The implementing agent flagged that absence rather than
writing around it, which is why this record exists. Slices 2 and 3 have standalone scope
reviews and this one should have too.

## The finding that changed the slice

**§6's catalogue oversells #8 Challenge Board.** It reads "Current / next / completed", but
`app_private.list_overlay_challenge` (migration `0109`, ~344–368) returns exactly **one**
challenge — the most recently updated, `limit 1`. A multi-item board is new query work, and
**"next" has no defined ordering at all**: no priority or queue column exists, only
`created_at` and `updated_at`.

**Decision: ship current-only.** It matches the existing contract and needs no new endpoint.
"Next" and "completed" are deferred pending a product decision on what ordering means — that
is a real question, not a deferral of work, and guessing it would have invented a product
rule inside a UI port.

This is the second module whose one-line catalogue entry misdescribed its cost (Boss Fight
was cheaper than it looked; Challenge Board is dearer). Worth carrying into the remaining
thirteen: **read the data path before believing the catalogue.**

## What made #13 genuinely cheap

Milestone Celebration fires on the **false→true edges** of `goal.reached` and the vote
tally's `resolved` — both already present in polled snapshots the canvas receives. No new
endpoint, no new query, no new event.

## The market check that mattered

The honest register for a failed challenge came from a primary source: YouTube's Super Chat
Goals states that when a goal is not met, the revenue is the creator's and they should start
a new goal (support.google.com/youtube/answer/15685577, accessed 2026-09-16) — no refund, no
punitive framing. Twitch's and Streamlabs' non-refund positions could not be verified against
live primary text (a load failure and a missing clause respectively), and the review said so
rather than presenting search synthesis as sourced.

## Orchestrator decisions

1. **#8 current-only.** Above.
2. **Milestone Celebration does not fire on a challenge target this slice.** #8 exposes no
   target-reached edge, so wiring them would either invent one or couple #13 to a surface
   that is not built.
3. **The reduced-motion alternative must be perceivable**, not a shortened animation. A
   celebration a reduced-motion viewer cannot perceive is not accessible, only quieter.
4. **`CHALLENGE_FAILURE_COPY` stays §15.4.2 protected-class** and non-overridable in the
   Canvas port. A creator able to edit it could promise a refund the product cannot deliver,
   for money it never held.

## Refused

Building "next" without a product decision on ordering · any celebration trigger that is not
an already-verified boolean from a polled snapshot · wiring #13 into Support Theater's
once-only acknowledgement stream, which is the wrong shape and repeats slice 3's transport
correction · #10 QR Smart Card (needs Clutch Mode `CMP-17`, absent; a QR library, absent; and
scene-profile visibility, outside PRF-02) · #18 Now Playing (no data source exists anywhere).
