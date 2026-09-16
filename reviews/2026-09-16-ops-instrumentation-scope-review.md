# Review — OPS-08 / OPS-10 / OPS-11 scope, before any code

**Date:** 2026-09-16
**Reviewer:** Review-only agent (no worktree changes), then orchestrator decisions.
**Recorded retrospectively.** See "A process defect" at the end — this is the second slice
where the implementer was told to read a completed scope review that existed only as agent
output and had never been written to a file.

## The tension the review was pointed at

Instrumentation means collecting data about creators and viewers, and this product's posture
is that it does not surveil people. §12.3 and these three rows pull against each other, and
the pull is sharpest in two places:

**The viewer funnel.** A supporter can tip anonymously, with no account. So the line between
"how many people who opened a tip page completed one" and following a person around is the
whole design, not a detail.

**Repeat-supporter rate.** It requires knowing two payments came from the same human — which
needs an identity, a retention rule, and an answer for the supporter who never made an account.

## What the market check found

None of Streamlabs, StreamElements, Twitch or YouTube discloses, in any creator-facing
surface, what it retains about an **anonymous one-time supporter**, or gives that supporter
any control panel. Sources with access dates are listed in the implementation review record.
StreamElements' own privacy policy describes collecting name, contact details, account
credentials, payment card data and transaction history for account holders, and separately
running third-party behavioural analytics sitewide.

That absence is the differentiator §12.3 sets up, and nobody is currently doing better.

The closest published analogue to a tips-per-viewer-hour KPI is YouTube Analytics' RPM —
post-share revenue per 1,000 views, blending ads, memberships and Super Chat.

## Orchestrator decisions

**1. Revenue numbers do not go into Prometheus.** They live in a durable, creator-reachable
record. This follows from authority rather than taste: §12.6 requires durable creator records
to be viewable, searchable and exportable and never tier-gated; §7 gives them dashboard
screens; and `metrics.ts`'s own header forbids identifiers in labels, which several of these
KPIs would need. A business KPI scraped into an ops endpoint lands where the creator cannot
reach it and no retention policy governs it.

**2. The 30-day anonymous-identity TTL is the privacy boundary, not an obstacle.**
Repeat-supporter rate must not outlive it.

**3. Nothing may correlate an anonymous tip-page visit to a return visit** by fingerprint, IP,
or any identifier that is not already the bounded, TTL'd `anonymous_browser_identities` token.

**4. The attribution KPIs are not built.** TTS-driven tips, threshold uplift and goal-driven
tips each require attributing a tip to a *cause* — "did the goal bar move this person?" —
which is new derived logic rather than a read, and needs its own decision record.

## A concern the review raised that turned out to be sound

The review flagged that `creator_supporter_relations.lifetime_amount_paise` might be a stored
counter no refund updates, which would put OPS-11's averages out of step with
`payments − refunds`.

**Checked, and it holds.** Migration `0124` *recomputes* the value as net of processed refunds
on every relevant payment change rather than incrementing, and `0014`'s refund sync updates
`payments.status`, which is exactly what fires that trigger. It also survives the awkward
case: a second refund on an already-`refunded` payment still executes the `UPDATE`, so the
trigger fires even though the status value does not change. Recorded because it is
non-obvious and will otherwise be re-raised.

## A process defect, mine

The implementing agent was told to read "the completed scope review" and could not find it —
it searched `reviews/`, `pending/` and the alerts tree before writing any code, then flagged
the absence rather than fabricating a pointer. The same thing happened on PRF-02 slice 4.

**Cause:** review-agent findings were passed to implementers inside the command text and never
written to a file, so a record that the command asserted existed did not.

**Correction:** a review agent's findings are written to `reviews/` **before** the
implementation agent is dispatched, and the command points at the file rather than restating
it. Both missing records are now written retrospectively and labelled retrospective rather
than backfilled to look original.

## A contradiction in the dispatching command, also mine

The command's top-line scope named OPS-08 and OPS-11 and listed records for only those two,
while a later subsection used imperative "build" language for OPS-10. The implementer resolved
it conservatively — did not build OPS-10, applied its two privacy rules to OPS-11's
repeat-supporter rate where they were needed anyway, and reported the ambiguity. That is the
right resolution of an ambiguous instruction: take the narrower reading and say so.

**OPS-10's standing after this slice:** its *creator* activation funnel is effectively
satisfied by OPS-08, which derives the same payout → overlay → first-alert milestones. Only
the **viewer aggregate open-versus-completion counter** remains, and it is a follow-up slice
under decisions 2 and 3 above.
