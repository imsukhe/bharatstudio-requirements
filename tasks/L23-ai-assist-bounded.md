# L23 — AI assist, bounded

**Status:** `TODO — not started`
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
