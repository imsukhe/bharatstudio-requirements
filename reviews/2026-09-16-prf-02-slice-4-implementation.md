# Review — PRF-02 slice 4 implementation (Challenge Board current-only, Milestone Celebration)

**Date:** 2026-09-16
**Reviewer:** Implementing agent, self-review (independent review unavailable).
**Scope authority:** the product/market/creator/streamer scope review for this slice was
performed by a separate review-only agent and confirmed by Opus — the same two-step gate
slices 2/3 used. **Unlike slice 2's own `2026-09-16-prf-02-slice-2-scope-review.md`, that
review was not itself persisted as a standalone file in `reviews/`.** Its findings (the
`app_private.list_overlay_challenge` `limit 1` finding, the false→true edge definition, and
the three decisions below) were instead carried directly into this task's own command text.
This record points at that command text as the scope authority, per this task's own
instruction not to repeat the review, and states the missing standalone file as a fact rather
than papering over it with a fabricated citation. Whether a standalone record should be
back-filled for this slice, matching the slice 2/3 pattern, is not this implementer's call —
recorded in "Referred to Opus," below.

## What was built

Exactly what the command's scope named: module #8 (Challenge Board), narrowed to
current-only, and module #13 (Milestone Celebration), on the slice-1/2/3 runtime. Full file
list and evidence in `active/tasks/PRF-02.md`'s "Slice 4" section and
`tests/TC-PRF-02-slice-4-challenge-milestone.md` — not repeated here.

## Opus's three decisions, and how the build honours each

1. **Challenge Board ships current-only.** Verified directly against the data path before
   writing any module code: `app_private.list_overlay_challenge`
   (`packages/db/migrations/0109_v1_l17_paid_challenges.sql`, lines 344–368) selects one row
   via `order by c.updated_at desc limit 1` — there is no ambiguity here, no column this
   implementer had to infer. The module's `fetchSnapshot` type is `() => Promise<OverlayChallenge | null>`,
   a single value, matching the endpoint's own shape exactly; there is no array, list, or
   second field anywhere in the module for a "next"/"completed" entry to occupy.
2. **"Next"/"completed" stays an open product question, not answered here.** No ordering rule
   is invented, guessed at, or stubbed. `public.challenges` carries only `created_at`/
   `updated_at` — no priority/queue column — so even "oldest configured wins" (the tiebreak
   `master_canvas_modules` itself uses for a genuinely unstated question) is not obviously the
   right answer for "next," and this record does not pick one.
3. **Milestone Celebration does not fire on a challenge.** `MilestoneCelebrationModuleOptions`
   has no field for a challenge snapshot fetcher — checked at compile time by
   `milestone-celebration-module.test.ts`'s type-level assertion, not only documented in
   prose. The module fires on exactly two fields: `OverlayGoal.reached` and
   `TugOfWarVoteTally.resolved`, both already present in snapshots the Canvas already fetches
   for other modules.

## The rising-edge rule, and why `undefined` matters as much as `false`

This task's own §5 states two requirements that look like they could conflict: fire on a
genuine false→true transition, but never on "a reconnect that re-delivers the same
already-true snapshot." The naive implementation — track the previous boolean, fire when it
differs and the new value is `true` — gets this wrong on the very first observation: if a
module's first-ever fetch already returns `reached: true` (a fresh activation on an
already-completed goal, or a reconnect before any `false` was ever seen), a previous value
initialised to `false` would treat that as a false→true edge and celebrate something that
already happened before this viewer was watching.

`isRisingEdge(previous, next)` in `milestone-celebration-logic.ts` is `previous === false &&
next === true` — nothing else. The previous-value slots (`lastGoalReached`/
`lastVoteResolved`) start at `undefined`, not `false`, so `undefined -> true` is explicitly
not an edge. This single rule resolves both halves of the requirement with one function,
tested directly and exhaustively across all four boolean transitions plus both `undefined`
starting cases (`milestone-celebration-logic.test.ts`, six cases) before the module that uses
it was even written.

**Why the edge-tracking state is never reset by `activate()`/`deactivate()`:** an OBS scene
toggling a module's visibility must not re-arm `undefined` as the starting point on every
toggle — doing so would risk exactly the failure mode above on every single scene switch, not
just on first load. The state lives for the module object's lifetime, a deliberate choice
recorded in the module's own header and in `active/tasks/PRF-02.md`'s Slice 4 "Decisions".

## The protected string, and what "cannot be overridden" actually means here

`CHALLENGE_FAILURE_COPY` is imported, not re-declared, in `challenge-board-module.ts` — from
`../../widgets/challenge/challenge-widget-logic.ts`, the same constant the standalone widget
itself renders. This was a deliberate choice against the task's own fallback instruction ("if
the Canvas needs its own copy for layering reasons, add a test asserting all copies are
identical") — no third copy was needed, so none was created, which is the strongest form of
"cannot diverge" available: there is nothing to diverge.

"Cannot be overridden" is proven three ways, not asserted once:

1. **No field exists.** `ChallengeBoardModuleOptions` has no option for alternate copy.
2. **Proven at the call site.** `challenge-board-module.test.ts`'s "the protected copy cannot
   be overridden" case constructs the module with an extra, undeclared option
   (`failureCopyOverride`, a fabricated guaranteed-refund string) and asserts the rendered
   text is still exactly `CHALLENGE_FAILURE_COPY` — proving the module never reads such a
   field, not merely that the type does not declare one.
3. **No refund-adjacent word appears anywhere else in the rendered card.** Two tests strip the
   sanctioned copy out of the full rendered text and assert the remainder contains no
   refund/reversal/escrow/funds-held word — on both a succeeded challenge (where the copy
   never appears at all) and a failed/cancelled one (where it is the only place such language
   is permitted to appear).

**The pre-existing two-copy situation got its first automated check.** Before this slice, the
API's (`challenge-store.ts`) and the web widget's (`challenge-widget-logic.ts`) copies were
asserted byte-identical only by a comment in each file — nothing verified it. Because apps/web
and apps/api share no import boundary for internal source, `challenge-failure-copy-parity.test.ts`
reads the API file's source text directly via `fileURLToPath(new URL(..., import.meta.url))`,
mirroring the exact cross-package pattern this codebase already uses
(`apps/web/app/accept-terms/terms-content.test.ts`'s migration-hash check), and asserts the
extracted string matches verbatim. **Is the reduced-motion alternative genuinely
perceivable, not merely a shorter animation?** Yes, by construction: `milestone-celebration-
badge` is a separate DOM element from `milestone-celebration-animated`, never given a CSS
`transition`, so its opacity change is instantaneous rather than eased — what changes under
reduced motion is which element renders and how its own colour/border/text look, never the
duration of the same animation. `milestone-celebration-module.test.ts` asserts both that the
badge becomes visible AND that it has no `transition` set, specifically to rule out "the same
burst, just faster" as a passing implementation.

## What this record is not

Not a repeat of the scope review's product/market/competitive research — recorded only in this
task's own command text, per the gap named above. Not evidence of any §19.4 performance
budget — nothing in this slice touches frame timing or memory; the seven-module integration
test proves connection/loop-count logic only, on JSDOM.

## Independent review

Unavailable — self-review only, stated plainly per §35.1 rule 6: a self-review never closes an
evidence row, and none is claimed closed here. This record and its evidence are `Conditionally
complete`, pending Opus's audit, exactly as `active/tasks/PRF-02.md`'s status line for this
slice states. **PRF-02 remains register letter `A`** — this implementer does not self-assign a
state letter, per this task's own hard rule.
