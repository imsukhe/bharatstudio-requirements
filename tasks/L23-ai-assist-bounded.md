# L23 — AI assist, bounded

**Status:** `Built and locally test-green through migration 0121 — all five surfaces suggest-only behind an explicit human confirmation, provider seam carries no donor/message/payment data, full audit trail; wired into app.ts/index.ts; not proven in a deployed environment and no model provider is integrated (the shipping generator is rule-based and makes no network call)`
**Level:** L2
**Owner:** [OWNER — product/API, unassigned]
**Depends on:** none recorded
**Blocks:** none recorded
**Test record:** [`../tests/TC-L23-ai-assist-bounded.md`](../tests/TC-L23-ai-assist-bounded.md)

## Authority and evidence

Master plan Part 6, "L23 — AI assist, bounded" (lines ~1169–1178): "AI is not the launch message... AI must never autonomously: capture money, refund, change payment destinations, mark a challenge complete, or create a financial obligation without explicit human confirmation."

## Objective

Add bounded AI assistance to configuration and content-adjacent surfaces, with a hard, testable boundary against any autonomous financial or state-changing action.

## Tasks

1. Configuration suggestions (e.g., alert-style, queue-mode recommendations).
2. Challenge copy suggestions (drafting text for a proposed challenge — never submitting or approving it).
3. Translation/localisation assistance.
4. Style proposals for Alert Studio (L20) content — proposals only, never auto-applied without confirmation.
5. Moderation assistance (surfacing a suggested moderation action for a human moderator to confirm — never auto-executing it).

## Exact implementation boundary

In scope: the five assist surfaces above, all producing a suggestion that requires explicit human confirmation before any effect.

Out of scope, permanently, with no future-phase exception recorded in this task: AI autonomously capturing money, issuing a refund, changing a payment destination, marking a challenge complete, or otherwise creating a financial obligation. Any of these five actions must always originate from an explicit human action, never from an AI-assist code path, at any tier, in any phase.

## Non-negotiable implementation rules

- AI is never the launch message — this task does not authorize AI-forward marketing claims.
- AI must never autonomously: capture money, refund, change payment destinations, mark a challenge complete, or create a financial obligation without explicit human confirmation. This is an absolute rule with no per-tier exception.
- Every AI-assist surface produces a proposal/suggestion object distinct from the state-changing command; the human-confirmation step must be a separate, auditable action.

## Definition gate

Per `governance/AGENTS.md`, L2 work stops after definition pending explicit approval. Owner unassigned: [OWNER].

## Acceptance criteria

- For each of the five assist surfaces, the AI-produced output is a suggestion object with no direct write path to `payments`, `refunds`, `challenges` status, or any other financially-consequential table — proven by test (the suggestion path and the confirm-and-apply path are architecturally and testably separate).
- Attempting to invoke a financial action (capture, refund, destination change, challenge-complete) directly from the AI-assist code path fails by design, proven by a negative test.
- Every AI suggestion applied to a live surface (alert style, challenge copy, translation, moderation action) is preceded by a human-confirmation event that is itself recorded (who confirmed, when, what was suggested vs. applied).

## Evidence required for closure

Inline prose citation: exact file paths for each of the five assist surfaces and their suggestion/confirm split; test-suite pass count for the negative test proving no direct financial write path exists from the AI-assist code. No artifact/screenshot directory.

## Rollback

AI-assist surfaces are additive suggestion layers over existing configuration/content/moderation UI; disabling any of them reverts to the pre-existing manual flow with no data-model change to payments, refunds, or challenge state. No production migration without separate explicit approval.

## Build record — 2026-09-13

Built in `bharatstudio-alerts` commit `dac8fc4` (`feat(0121): L23 bounded AI assist — suggestions that cannot act`), migration `0121_v1_l23_ai_assist_bounded.sql`.

This record said `TODO — not started` after the work had already landed and been committed. That is the same class of failure as the L22 staleness corrected in this batch: the building lane did not update its own task file, and reconciliation had already run. Recorded rather than silently fixed.

**The bound is structural, not conventional.** `decide_assist_suggestion` is the only function that can move a suggestion out of `pending`, and it writes solely to `assist_suggestions` / `assist_confirmations`. Accepting a suggestion records a decision; it never applies anything to the live config, challenge, alert-style or moderation tables. A human applies it afterwards through the product's existing endpoints. Proven by a direct `select count(*) from public.challenges` assertion after an accept, and by `apps/api/test/l23-assist-routes.test.ts:88`.

**Permanently out of scope at every tier, no exception:** AI capturing money, refunding, changing a payment destination, marking a challenge complete, or creating any financial obligation. Neither new table references `payments`, `refunds` or `challenges`.

**The provider seam** carries `surface`, `tier`, and a flat `signal` object of strings/numbers/booleans only (`apps/api/src/domain/assist-provider.ts:36`). Never donor or viewer names, message text, payment or payout data, or session/device identifiers. `createLocalAssistProvider` is rule-based, makes no network call, and reads only its own request argument, so it cannot leak what it never receives. Asserted at `apps/api/test/l23-assist-routes.test.ts:180` on both the exact key set and the absence of donor/message/payment-shaped strings.

**Audit trail** reconstructs what was suggested, on what basis, who requested it, who decided, when, and what was actually applied — `applied_payload` stays distinct from `suggested_payload` when a human edits at accept time, and is null on rejection. The deciding user's role is snapshotted so a later role change cannot rewrite history.

**Evidence:** 13 SQL checks in `packages/db/tests/l23-ai-assist-bounded.sql`; 13 API route tests; 6 web page tests. Full-tree re-run 2026-09-13: SQL suite 51/51 on real Postgres 16, `apps/api` 496/496 tsc 0, `apps/web` 324/324 tsc 0.

**Open, not resolved:** no model provider is integrated — wiring one is a deliberate future swap of the `AssistSuggestionProvider` implementation, and the privacy claims above hold for the local generator only and must be re-proven against any real provider. Suggestion generation is manual (a creator picks a surface); there is no scheduled trigger. The dashboard page is not linked from any nav. Nothing is proven in a deployed environment.
