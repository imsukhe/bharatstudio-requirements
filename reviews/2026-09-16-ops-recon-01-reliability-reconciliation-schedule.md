# Review — OPS-RECON-01

**Task:** `../active/tasks/OPS-RECON-01.md`
**Date:** 2026-09-16
**Reviewer:** Orchestrator self-review. **Independent review unavailable** — not claimed.

## Decision

The owner decided on 2026-09-16 that the L09 reliability reconciler should get its own
schedule in its own task, rather than reopening RT-06 to carry scheduling work. That keeps
RT-06's `P` honest — its remaining open item, cross-instance aggregation, genuinely needs a
deployed environment — and gives the reconciler an owner.

## What was checked before scheduling anything at it

The endpoint was read first. It verifies service identity, takes the same idempotency-key
shape as `/internal/maintenance/:job`, fails closed with a retryable 503 when the database
is absent rather than reporting zeros, and replaces one snapshot row rather than appending —
so repeated runs converge. A schedule pointing at an endpoint that was not safe to call
repeatedly would have been worse than no schedule.

Its own comment claimed it "writes nothing durable", which RT-06 had made untrue. Corrected.

## The cadence

`*/5`, borrowed from `payment-reconciliation` — the closest reconciliation analogue already
approved in the catalogue. No authority states a cadence for this job. Borrowing an approved
value beats inventing one, and the record says which value was borrowed and from where so a
later reader can challenge it.

## A claim I got wrong

I recorded, and told the owner, that the endpoint's body schema would have **rejected** the
standard scheduler body with a 400 — "scheduled, and never once successful". The test written
to prove it returned 503: Fastify runs AJV with `removeAdditional: true`, so
`additionalProperties: false` **strips** an unknown field instead of rejecting it. The
schedule would have worked without any route change.

The correction is recorded in the route comment, the test name, the task record and the
acceptance record. The route change stands on a weaker but still real justification — a
schema that silently discards a field it was sent cannot be read as a contract, and the next
reader cannot distinguish "ignored deliberately" from "forgotten".

## Disposition

`Conditionally complete`. The schedule is defined, enabled and covered by the contract test
and the operations contract. **Enabling a flag is not a deployment**, and no evidence is
claimed that this job has ever run.
