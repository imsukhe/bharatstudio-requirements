# TC-L23 — AI assist, bounded acceptance

**Status:** `TODO — not started, no evidence exists yet`
**Task:** [`../tasks/L23-ai-assist-bounded.md`](../tasks/L23-ai-assist-bounded.md)
**Authority:** `bharatstudio-alerts/docs/BharatStudio-MASTER-PLAN.md` Part 6 (L23)
**Repository:** `/Users/sukhdevsingh/Workspace/Bharat Studio/bharatstudio-alerts`
**Data:** Synthetic configuration/challenge/moderation fixtures only. No real payment or refund is invoked by any AI-assist code path in this suite — that is precisely what is being proven absent.

## Preconditions

1. Each of the five assist surfaces (configuration suggestions, challenge copy, translation/localisation, style proposals, moderation assistance) has, at minimum, a defined suggestion-object contract to test against.

## Acceptance cases

| ID | Setup and action | Expected result | Failure/retry and evidence |
|---|---|---|---|
| L23-01 | Invoke each of the five AI-assist surfaces and inspect the returned object | Each returns a suggestion object with no direct write path to `payments`, `refunds`, or `challenges` status tables | Not run — TODO |
| L23-02 | Attempt to call a payment-capture, refund, payment-destination-change, or challenge-complete action directly from the AI-assist code path | Fails by design — no such direct path exists | Not run — TODO |
| L23-03 | Apply an AI suggestion (e.g., a style proposal) to a live surface | A separate, auditable human-confirmation event is recorded (who confirmed, when, what was suggested vs. applied) before the change takes effect | Not run — TODO |
| L23-04 | Search any marketing copy or in-product messaging for AI positioned as the primary launch message | AI is not the launch message anywhere in scope | Not run — TODO |

## Closure rules

Closes only when every row has a real pass/fail result with inline evidence (file paths for each of the five surfaces and their suggestion/confirm split, negative-test pass count for L23-02) replacing "Not run — TODO." No artifact/screenshot directory exists or may be created.

## Cleanup and rollback

All fixtures are synthetic and run without touching any production financial table. No cleanup beyond standard test-run teardown is required, since no AI-assist code path may write to payments/refunds/challenges by this suite's own acceptance criteria.
