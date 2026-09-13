# L16 — Interaction menu, goals and widgets

**Status:** `Locally implemented and self-audited through migration 0119 — paid support-vote binding, external-contribution aggregation into goals/challenges/hype, and all widget reads (now SSE-invalidation-signalled, REST-snapshot-sourced) are composed in the API runtime and have reproducible API/web/SQL evidence; independent review and deployed browser/OBS evidence remain open`
**Level:** L2
**Owner:** [OWNER — product/API/web, unassigned]
**Depends on:** L14 (supporter identity on leaderboards); L20 (visual layer for widgets)
**Blocks:** L17 (`!challenge` surfaces on the interaction menu; community challenges are handled as support goals here, not as refundable contracts)
**Test record:** [`../tests/TC-L16-interaction-menu-goals-and-widgets.md`](../tests/TC-L16-interaction-menu-goals-and-widgets.md)

## Authority and evidence

Master plan Part 6, "L16 — Interaction menu, goals and widgets" (lines ~854–917); Part 7 §7.6 (widgets/engagement feature register — all rows TODO, all owned by L16).

## Objective

Turn a tip amount into a chosen interaction, and put the stream's support state on screen.

## Tasks

1. `interaction_definitions` per channel — amount, label, queue binding, TTS rule, moderation rule, visual.
2. `support_goals` — target, current, window, reset policy, public/private.
3. `widget_configs` — type, placement, style, data source, privacy scope.
4. Widget browser sources sharing the existing overlay session/cursor/replay machinery. Do not build a second delivery path.
5. Support votes: option set, per-option tally, resolution.
6. Hype mode: time-boxed meter, decay, threshold visual.
7. Leaderboard windows: stream / weekly / monthly, applying the L14 privacy rules (no exact lifetime spend published by default).

## Exact implementation boundary

In scope: the nine interaction types listed in the master plan's interaction-menu table (tip, TTS tip, sticker/reaction [assets via L22], mega alert, priority question, support vote, community support goal, hype mode) except paid challenge, which is L17. Widget tiers per the master plan's table (main alert, support goal, recent tips, top supporters, supporter ticker, public leaderboard, mega-tip banner) gated by plan as specified there.

Out of scope: paid challenges (hard creator obligation) — owned entirely by L17; any new overlay delivery mechanism outside the existing SSE/outbox/replay machinery from L03/L05.

## Non-negotiable implementation rules

- No arbitrary viewer media upload in any interaction type at launch.
- Widgets must reuse the existing overlay session/cursor/replay machinery (L03/L05) — a second delivery path is a rejected design.
- Leaderboard/top-supporter widgets must apply L14's privacy rule: no exact lifetime spend published by default, and never any cross-creator amount.
- A "soft" creator obligation (priority question, support vote, community goal, hype mode) must never be represented in the schema as a refundable/hard obligation — that state machine belongs solely to L17.

## Definition gate

Per `governance/AGENTS.md`, this L2 work still requires scope/acceptance/affected-files/data-impact/test-plan/rollback approval before implementation. Owner is unassigned: record as [OWNER].

## Acceptance criteria

- Each of the eight non-challenge interaction types (tip, TTS tip, sticker, mega alert, priority question, support vote, community goal, hype mode) is definable per channel via `interaction_definitions` and testably bound to a queue.
- A support goal's `current` value updates only from confirmed payment events, never from a platform (Super Chat/Cheer) event alone, consistent with L15's "financial truth from the payment provider only" rule.
- Widget browser sources render through the existing overlay session/cursor/replay path; test proves no second SSE/delivery mechanism was introduced.
- A leaderboard widget response is proven by test to withhold exact lifetime spend when the channel's privacy setting is default (private), and to exclude any other channel's data.
- Hype mode's time-boxed meter decays and resolves deterministically under test (start, threshold, decay, end).

## Evidence required for closure

Inline prose citation: exact migration filenames for `interaction_definitions`, `support_goals`, `widget_configs`; exact file paths for the widget browser-source integration proving reuse of the existing overlay path; test-suite pass counts for goal-update-from-payment-only, leaderboard privacy withholding, and hype-mode lifecycle. No artifact/screenshot directory is created for this evidence.

## Rollback

All three new tables are additive; none touches existing `alert_events`/`payments`/queue tables beyond read-only joins. Disabling L16 (feature-flagging the interaction menu) must not affect existing tip/TTS-tip flows, which predate this task and are DONE per L03. No production migration without separate explicit approval.

## Implementation slice — 2026-09-07 reconciliation

Reconciled against `bharatstudio-alerts` as read on 2026-09-07; local build/test evidence only. Verified: `interaction_definitions` and `widget_configs` do not exist anywhere in `packages/db/migrations` or `apps/` — a repo-wide search found no such table or route. Only `support_goals` (task item 2) shipped; the correction to the map handed into this reconciliation is recorded below.

**Built and locally test-proven:**
- `packages/db/migrations/0102_v1_l16_support_goals.sql`: `support_goals` table. Progress is never stored — the migration's own header states `app_private.support_goal_progress_paise()` computes it live on every read as a windowed sum over `payments` (captured/refunded/partially_refunded) minus `refunds` rows with status `processed` for those same payments, clamped at zero as a defensive floor only. This satisfies the "goal's `current` updates only from confirmed payment events" acceptance criterion by construction — there is no write path a platform event could reach.
- Four goal windows (`stream`, `daily`, `monthly`, `open`) with daily/monthly computed live from `current_timestamp`, needing no reset job.
- `apps/web/app/overlay/widgets/goal/[overlayId]/page.tsx` plus `goal-widget-logic.ts`/`goal-widget-page.test.tsx` reuse the existing overlay fragment-token auth — the same session/cursor machinery from L03/L05, not a second delivery path. API-side store/routes at `apps/api/src/db/goal-overlay-store.ts`, `apps/api/src/db/goal-store.ts`, `apps/api/src/domain/goal-store.ts`, `apps/api/src/routes/goals.ts`.
- Cross-creator/security boundary for goal-adjacent supporter data is covered by the same `packages/db/tests/l16_security_boundary.sql` cited under L14, run as the actual `bsa_app` role.

**Not built — do not record as done:** `interaction_definitions` (so none of the eight non-challenge interaction types — tip, TTS tip, sticker/reaction, mega alert, priority question, support vote, community goal, hype mode — are definable per channel as this task requires; only the community-support-goal type has a working slice via `support_goals`); `widget_configs` (so the widget-tier gating by plan, and any widget beyond the goal widget — main alert, recent tips, top supporters, supporter ticker, public leaderboard, mega-tip banner — is unbuilt); support votes and hype mode (no code found for either); leaderboard windows and their L14 privacy-withholding behavior (no leaderboard route/table found). This task's acceptance criteria for "each of the eight… interaction types," the leaderboard privacy-withholding test, and the hype-mode lifecycle test are unmet, not merely untested.

**Correction to the map handed into this task:** the map described L16 by citing only migration 0102 and the goal widget path, without asserting interaction_definitions/widget_configs — that framing is accurate and is preserved here; this reconciliation adds the explicit confirmation that the other seven interaction types and both missing tables are absent, since the task file's original TODO status did not distinguish "not started" from "partially started."

## Batch 8 amendment — 2026-09-07 (post-reconciliation)

The entry above is now stale as of the same day it was written: batch 8 shipped `packages/db/migrations/0105_v1_l16_interaction_definitions_and_widgets.sql` after the reconciliation pass above landed. Verified by reading 0105 and the calling code.

**Now built and locally test-proven:**
- `interaction_definitions` (all eight types: `tip`, `tts_tip`, `sticker`, `mega_alert`, `priority_question`, `support_vote`, `community_goal`, `hype_mode`), per-channel, bound to a queue, with tier-limited counts (`app_private.tier_interaction_definition_limit`, 3/6/8/8 free/pro/creator/studio) and role-gated CRUD (`app_private.create_interaction_definition`/`update_interaction_definition`/`close_interaction_definition`, owner/admin only).
- `widget_configs` (all seven widget types listed in the task, including `main_alert`, `recent_tips`, `top_supporters`, `supporter_ticker`, `public_leaderboard`, `mega_tip_banner`), tier-limited (`tier_widget_count_limit`, 1/3/7/7) and privacy-scoped (`private`/`public`).
- `interaction_vote_options` / `interaction_vote_records`: support votes with a one-vote-per-`voter_fingerprint`-per-poll tally, resolved via `close_interaction_definition`.
- `hype_mode_activations`: a time-boxed activation window; the meter is computed live (`app_private.hype_mode_state`, same decayed-live-sum shape as `support_goal_progress_paise`) over real captured payments minus processed refunds, never stored.
- A leaderboard function (0105, "LEADERBOARD PRIVACY" section) that returns rank + a coarse tier bucket only, always scoped to one `channel_id`, computed read-only from `payments`/`refunds`.
- API routes: `apps/api/src/routes/interactions.ts`-equivalent surface (verified as `l16-interactions-routes.test.ts`, `l16-goals-routes.test.ts` — 28 test cases total) plus dashboard/overlay UI: `apps/web/app/dashboard/interactions/` (panel), and overlay pages at `apps/web/app/overlay/widgets/{vote,leaderboard,hype,goal}/[overlayId]/page.tsx` — each reusing the existing overlay fragment-token/SSE machinery, no second delivery path.
- SQL suite `packages/db/tests/l16-interaction-widgets.sql` covers role gating, vote tally/resolution, hype-mode lifecycle (start/threshold/decay/end) fed by real payments, and leaderboard privacy (no exact amounts, no cross-channel data); `l16_security_boundary.sql` (shared with L14) covers the cross-creator isolation boundary, run as the actual `bsa_app` role.

**Still open, recorded plainly, not resolved:**
- **Support votes are NOT money-gated.** 0105's own header states this explicitly: the only path that creates a real Razorpay order (`apps/api/src/routes/public.ts`'s tip-order route) is out of this migration's ownership boundary and has no field to tag an order with a vote `option_key`. Votes today are a free per-voter tally (`voter_fingerprint` dedupe), not a paid interaction. Making votes paid needs `routes/public.ts` (and the order-creation client) to accept an interaction tag on the tip-order body — out of L16's boundary as shipped.
- **4 of 7 widget types have config storage and entitlement gating but no OBS-facing overlay page.** `apps/web/app/overlay/widgets/` contains only `goal`, `vote`, `leaderboard`, `hype`. `recent_tips`, `top_supporters`, `supporter_ticker`, `mega_tip_banner` exist as valid `widget_configs.widget_type` values with tier gating but render nothing on stream.
- **The leaderboard has no amount field in any configuration**, not just the default-private case. 0105's header explains why: L14 (migration 0084) never built the opt-in public-profile column its own task file promised ("Public profiles are opt-in, default-off... NOT built"). With no opt-in switch to check anywhere, and touching 0084 out of bounds, the only safe behavior is to never expose an exact amount from any leaderboard function, under any configuration — there is no public mode to fall into by mistake.
- **The two new per-tier caps (`tier_interaction_definition_limit`, `tier_widget_count_limit`) are the implementing lane's own defaults**, computed live the same way `tier_goal_count_limit` (0102) is, but unconfirmed by product — not a merged ninth entitlement dimension, and not signed off outside this migration's own header comment.

Evidence: `packages/db/migrations/0105_v1_l16_interaction_definitions_and_widgets.sql`; `apps/api/src/routes/public.ts` (grep confirms no interaction/vote-option field on the tip-order body); `apps/web/app/overlay/widgets/` directory listing (four subdirectories only: `goal`, `vote`, `leaderboard`, `hype`); `apps/api/test/l16-interactions-routes.test.ts` and `l16-goals-routes.test.ts` (28 cases); `packages/db/tests/l16-interaction-widgets.sql`. Nothing here has been proven in a deployed environment.

## Completion addendum — 2026-09-08

The Batch 8 remaining gaps are now closed by the already-present, additive
`packages/db/migrations/0108_v1_l16_paid_votes_and_missing_widgets.sql` plus
the browser sources completed on 2026-09-08.

**Implemented locally:**

- Paid support votes bind a confirmed payment to exactly one configured vote
  option. `0108` supplies the payment tag, money-derived tally, refund effect,
  and the authenticated overlay reads. The public tip-order boundary carries
  the optional interaction-definition and vote-option tag; malformed or
  untagged checkout remains a normal tip flow.
- The missing route pages now exist at
  `apps/web/app/overlay/widgets/recent-tips/[overlayId]/page.tsx`,
  `apps/web/app/overlay/widgets/top-supporters/[overlayId]/page.tsx`,
  `apps/web/app/overlay/widgets/supporter-ticker/[overlayId]/page.tsx`, and
  `apps/web/app/overlay/widgets/mega-tip-banner/[overlayId]/page.tsx`.
  They share `widgets/shared/WidgetPoller.tsx`, use the established fragment
  bearer token and existing overlay-session-scoped API reads, and add no SSE,
  persistence, provider, or payment path.
- `l16-widget-data.ts` admits only the narrow, normalised response shapes.
  Empty/malformed/unavailable values render transparently. Recent tips and the
  mega banner show only consented display data. Top supporters and the ticker
  do not accept or render a monetary field; they show only the pseudonymous
  values returned by the existing SQL projection.

**Reproducible redacted local evidence:**

- `cd apps/api && npm test && npm run build` — **396/396** tests pass and
  TypeScript build passes. This includes
  `test/l16b-interactions-paid-vote-and-widgets-routes.test.ts`, covering
  authentication, missing-store fail-closed behaviour, empty/full responses,
  and the no-amount projections.
- `cd apps/web && npm test && npx tsc --noEmit && npm run build` —
  **287/287** tests pass, TypeScript passes, and the production Next build
  lists all four dynamic L16 widget routes. The local shape-guard test is
  `app/overlay/widgets/l16-widget-data.test.ts`.
- `sh packages/db/tests/run-sql-suite.sh` — a fresh PostgreSQL 16 container
  applies **110 migrations** and runs **44/44** isolated SQL proofs. The
  `l16b_paid_votes_and_widgets` proof covers payment/refund-derived votes,
  overlay-session scoping, recent/mega consented data, and the amount-free
  top-supporter/ticker projections.
- `git diff --check` passes. Source review found and fixed a stale API test
  expectation (`401`, not `503`, for an unauthenticated paid-vote tally) and
  an L17 test timing race before this record was updated.

**Remaining non-local gate:** no deployed browser/OBS session, staging
rollout, or independent security review has been performed. The additive
rollback is to remove the four browser sources and disable the existing L16
feature configuration; no alert, payment, queue, or overlay history needs
rewriting.

## Runtime-composition correction — 2026-09-09

A fresh self-audit found that the routes and SQL adapters added by `0108` had
previously been test-injected but omitted from the application composition
root. The failure was material: paid-vote tally requests would return
`503 interaction_store_unavailable`; protected paid-vote and the four new
widget reads would return `401 overlay_unauthorized`; and checkout would not
persist the bounded vote tag.

`apps/api/src/app.ts` now declares and passes `votePaymentTags`, `paidVotes`,
`paidVoteOverlay`, and the scoped SQL read client. `apps/api/src/index.ts`
constructs all three durable SQL adapters from `vote-payment-sql-store.ts`.
`apps/api/test/l16-runtime-composition.test.ts` builds the actual Fastify app
and proves checkout tagging, authenticated tally, paid overlay tally, and
all four widget routes rather than relying only on direct route mocks.

The correction is additive and retains the stated rollback: disabling the
L16 feature configuration or removing the additive browser sources leaves
existing payments, alerts, queues, and overlay history unchanged. It does
not satisfy the separate staging/browser/OBS or independent-review gates.

## Batch 10 reconciliation — 2026-09-13

Verified against `bharatstudio-alerts` commits `5a29868` (0117 external-contribution aggregation) and `7517a93` (overlay SSE-invalidation refactor), read directly.

- Migration `0117_v1_l16c_external_contribution_aggregation.sql` adds `external_contributions` in a shape deliberately incompatible with `payments` so it cannot be joined into reconciliation by accident (verified: no shared key/FK to `payments`). Goal/challenge/hype progress functions (`apps/api/src/db/contribution-sql-store.ts`, `apps/api/src/routes/challenges.ts`, `goals.ts`, `interactions.ts`) compute `greatest(coalesce(payment_net,0) + coalesce(external_net,0), 0)` at read time — confirmed in the migration SQL (lines 577, 638) — never a synthetic `payments` row. Progress is never stored; a reversal reduces it on the next read with no un-award step, matching the existing refund-handling discipline.
- `apps/api/src/domain/contribution-source-types.ts` confirms include/exclude only, default include, and explicitly no percentage/multiplier field or column anywhere — verified by grep, zero hits for `percentage`/`multiplier` in the contribution domain/store files.
- Only INR Super Chats become contributions; no FX rate exists in this code. Confirmed: `contributionSourceTypes` is `['payment', 'youtube_superchat']` only.
- Paid vote tallies and the leaderboard are confirmed NOT unioned with external contributions — no `external_contribution`/`superchat` reference found in the vote-tally or leaderboard read paths. `viewer_platform_identities` (migration `0084_v1_l14_viewer_identity.sql`) does exist, contrary to a claim in an earlier draft of this feature's own migration header, which the migration text itself corrects; it is populated only on claim, so attribution stays sparse by design, not by omission.
- `7517a93`: nine overlay widgets (challenge, goal, hype, leaderboard, vote) now share `apps/web/app/overlay/widgets/shared/overlay-transport.ts` and `WidgetPoller.tsx`. Confirmed by reading the transport file: the SSE stream is used only to trigger a debounced re-read of the existing REST snapshot endpoint; it never carries state itself. The pre-existing interval poll continues running until the stream connects, and resumes if it drops — confirmed in `WidgetPoller.tsx`.
- Local re-run 2026-09-13: `apps/api` 465/465 (`npm test` via `tsx --test`), `apps/web` 312/312, SQL suite 49/49 across 120 migrations, all three Go services `go test ./...` clean. These are local-only figures; no staging/OBS/browser-source or independent-review evidence is added by this reconciliation.
