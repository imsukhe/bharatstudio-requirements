# L17 — Paid challenges

**Status:** `Local non-refundable challenge alternative implemented through migration 0109; original refundable paid-challenge requirements remain blocked by absent provider refund capability and require a new product/provider decision`
**Level:** L3
**Owner:** [OWNER — API/payments/product, unassigned]
**Depends on:** L15 (`!challenge` command), L19 (payment-provider capability introspection for the refund-capability gate)
**Blocks:** none recorded
**Test record:** [`../tests/TC-L17-paid-challenges.md`](../tests/TC-L17-paid-challenges.md)

## Authority and evidence

Master plan Part 6, "L17 — Paid challenges" (lines ~918–979); Part 7 §7.7 (all rows TODO, owned by L17); Part 4 §4.8 state-machine sketch, "Challenge (TODO — L17). Kept strictly separate from payment state."

## Objective

Let a viewer pay for a conditional creator action, with an explicit refund path and no escrow.

## Tasks

1. `challenges`, `challenge_proposals`, `challenge_payment_links`, `challenge_status_events`, `challenge_disputes`.
2. Challenge state machine per Part 4 §4.8, stored strictly separately from payment state.
3. Capability gate: challenges are invisible unless `PaymentProviderConnection.capabilities.refunds` is true.
4. Creator/moderator approval flow for viewer-proposed challenges (the default flow: viewer proposes → creator/moderator approves → payment link activates → viewer pays → FUNDED).
5. Completion submission and creator confirmation.
6. Failure → refund initiation → refund status surfaced to both parties.
7. Dispute record.
8. Public challenge board page + OBS widget (IN PROGRESS / NEXT / COMPLETED states).
9. `!challenge` chat command (depends on L15).

## Exact implementation boundary

In scope: viewer-proposed challenge flow (the master plan's stated default, because it avoids refunding unwanted creator-published challenges); the refund-capability gate; the state machine and its five tables.

Out of scope, explicitly: multi-contributor refundable challenges — the master plan directs these be modeled as L16 support goals instead ("a failure means N individual refund operations, each of which can fail independently... v2+"). Creator-published challenges are not the default and are not required by this task's acceptance criteria; if built, they must not bypass the refund-capability gate.

## Non-negotiable implementation rules

- Challenges are never tips: a tip carries no creator obligation, a challenge does. The two must never share a state machine.
- Enable challenges **only** on a provider connection whose capability snapshot proves verified payment **and** a refund API **and** refund status. This is a hard capability gate, not a manual toggle.
- The refund is invoked on the **creator's** merchant account. BharatStudio holds no escrow.
- Product-facing copy must say, verbatim: "Refund automatically initiated through the creator's connected payment provider." Never promise unconditional or instant refunds — the payment may already have settled, the refund may be pending or fail, and the provider may require merchant balance for it to succeed.
- Community/multi-contributor challenges are modeled as support goals (L16), never as refundable multi-party contracts, in this task's scope.

## Definition gate

Per `governance/AGENTS.md`, L3 work stops after definition pending explicit scope/acceptance/data-impact/test-plan/rollback approval. Owner unassigned: [OWNER]. The refund-capability gate depends on L19 delivering `provider_capability_snapshots` first — sequencing, not a design decision, is open pending L19's schedule.

## Acceptance criteria

- A challenge cannot be created, proposed, or paid for on a channel whose connected payment provider capability snapshot does not report `refunds: true`; proven by test.
- The viewer-proposed flow transitions proposal → approved → payment-link-active → FUNDED and is covered by a state-machine test for each transition, including rejection at the approval step.
- A failed/unconfirmed challenge triggers refund initiation against the creator's merchant account, and refund status (initiated/pending/failed/completed) is surfaced to both creator and viewer — proven by test, including the failure case.
- The refund product copy used anywhere in the UI matches the locked sentence verbatim: "Refund automatically initiated through the creator's connected payment provider."
- The public challenge board renders IN PROGRESS / NEXT / COMPLETED correctly from `challenge_status_events`, and an OBS widget consumes the same state without a second delivery path.
- A dispute record can be opened against a FUNDED or refund-failed challenge and is retained even after resolution (append-only).

## Evidence required for closure

Inline prose citation: exact migration filenames for the five new tables; exact file path for the state machine implementation and its unit-test file with pass count; exact test proving the refund-capability gate rejects a non-capable provider; exact test proving refund-status surfacing on a simulated refund failure. No artifact/screenshot directory.

## Rollback

All five tables are new and additive; disabling L17 removes challenge-only surfaces without touching `payments`, `refunds`, or `alert_events`. Challenge state events are append-only (`challenge_status_events`) so no historical row is rewritten by a later migration. No production migration or live refund test runs without separate explicit approval and synthetic/sandbox provider credentials only, per `governance/AGENTS.md`'s "use synthetic data unless consented otherwise."

## Superseded historical reconciliation — 2026-09-07

This was a point-in-time repository search on 2026-09-07. It is retained for
traceability but is superseded by the 2026-09-08 alternative-slice
reconciliation below; it is not current delivery status.

## 2026-09-08 reconciliation — do not treat as original-task closure

`packages/db/migrations/0109_v1_l17_paid_challenges.sql` and its API/web
callers now exist, but they intentionally implement a different safe product
slice: a creator-set, **non-refundable** challenge target. It has
`challenges` and append-only `challenge_status_events`, live progress from
confirmed payment/refund records, role/tier gating, dashboard management at
`apps/web/app/dashboard/challenges/`, and an existing-overlay-session widget
at `apps/web/app/overlay/widgets/challenge/[overlayId]/page.tsx`.

This does **not** implement the original task's `challenge_proposals`,
`challenge_payment_links`, `challenge_disputes`, verified refund-capability
snapshot, merchant refund initiation/status, viewer-proposal flow, or
`!challenge` connector. `0109` is explicit that no configured provider can
perform those actions. The locked refund copy is therefore inapplicable and
must not be claimed as present. The alternative's failure copy says a
contribution is a tip and that only the creator can refund through their own
provider dashboard.

Local evidence at the 2026-09-08 execution: `packages/db/tests/l17-paid-challenges.sql` is part of the
PostgreSQL **110-migration, 44/44** isolated proof run; API
`test/l17-challenges-routes.test.ts` was in the **396/396** API suite; web
`app/dashboard/challenges/l17-challenges-page.test.tsx` and challenge overlay
sources are in the **287/287** web suite and production build. The dashboard
test timing race found by the whole-web run was corrected before recording.
The alternative is approved only within
`reviews/2026-09-08-L17-nonrefundable-challenge-decision.md`; a future
refundable challenge requires a new explicit authority slice after real L19
provider/sandbox evidence.

## Regression recheck — 2026-09-09

The dependency-installed full local recheck passed API **398/398**, web
**289/289** with typecheck/production build, and disposable SQL **44/44**
after 110 migrations. This refreshes only the approved non-refundable
alternative's evidence; it does not satisfy original refundable-L17 criteria.
