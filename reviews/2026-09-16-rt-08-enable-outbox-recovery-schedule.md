# Review — RT-08

**Task:** `../active/tasks/RT-08.md`
**Date:** 2026-09-16
**Reviewer:** Orchestrator self-review. **Independent review unavailable** — not claimed.

## Disposition

RT-08 closed as part of the RT-04 change. The design reasoning, the market review, the
decisions and the independent Opus verification are recorded once in
[`2026-09-16-rt-04-webhook-commit-and-leased-dispatcher.md`](./2026-09-16-rt-04-webhook-commit-and-leased-dispatcher.md)
rather than duplicated, because duplicating a review is how two records drift apart and
then disagree.

This record exists because §31.0 requires each register row to carry its own task, test and
review record. It adds the row-specific disposition and nothing else.

## Row-specific notes

See `../tests/TC-RT-08-enable-outbox-recovery-schedule.md` for this row's own evidence and for what is explicitly **not**
claimed by it.

## Follow-up

The wake-up coalescing finding recorded in
`../tests/TC-RT-04-webhook-commit-and-leased-dispatcher.md` is open and deliberately not
performed: it needs new concurrency in the payment path, and the threshold at which it
matters is a load property that ENV-08 and RT-07 would measure. Both are Blocked.
