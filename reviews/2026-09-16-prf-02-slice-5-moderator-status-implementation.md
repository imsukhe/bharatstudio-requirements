# Review — PRF-02 slice 5 implementation (Moderator Status Card, held half only)

**Date:** 2026-09-16
**Owner:** Sukhdev Singh
**Reviewer:** Implementing agent, self-review. **Independent review unavailable** — no second
reviewer ran against this build, and per `governance/AGENTS.md` this slice is therefore left
`Conditionally complete`, not complete.
**Scope authority:** `2026-09-16-prf-02-slice-5-scope-review.md` — a standalone, persisted
scope review, read before any code was written. Its findings are **not** restated here.
**Task record:** `../active/tasks/PRF-02.md` ("Slice 5")
**Acceptance record:** `../tests/TC-PRF-02-slice-5-moderator-status.md`
**Register:** PRF-02 stays `A`. No state letter was self-assigned.

## What was built

§6 module #12's **held half only**, as a complete vertical slice: migration `0136`
(`app_private.list_overlay_moderator_status` plus one partial index), the overlay route
`GET /v1/overlay-widgets/:overlayId/moderator-status`, its OpenAPI/JSON-Schema/fixture and
the negative privacy cases that go with them, the RT-12 manifest entry and a captured
EXPLAIN artefact, and the canvas renderer registered on the one existing connection and the
one existing rAF loop. File list and per-case evidence live in the task and acceptance
records; not repeated here.

## The four owner decisions, and how each is enforced rather than promised

1. **Safe mode is not `alert_queues.is_paused`, and is not built.** Enforced three ways, none
   of which is a comment: migration `0136`'s function text contains no `is_paused` token at
   all, asserted in SQL against `pg_get_functiondef` (case S5.5); the contract's response
   object is `additionalProperties: false` with exactly one data property, so no safe-mode
   field can be added without a schema change that `contracts:validate` would have to accept;
   and the renderer has no element, option or string for one. Safe mode remains undecided and
   its own record is still owed — referred, not written here, because writing it would mean
   deciding what safe mode *is*.
2. **Held alert deliveries, not chat messages.** The count is over
   `event_outbox_deliveries.status = 'held'`. The rendered label is `N held for review`, and
   the renderer's test asserts the rendered text contains none of `message`, `chat`,
   `comment` — the YouTube-confusion risk the scope review named, closed by assertion.
3. **"Never private content" as a property of the query.** `returns table (held_count
   bigint)` — one column. Case S5.4 asserts the returned column set twice over: from
   `pg_get_function_result`, and from a table materialised out of a live call and read back
   through `information_schema.columns`. The route then narrows a second, independent time
   (case S5.11): a deliberately polluted store answer carrying a supporter name, message
   text, amount, delivery id, viewer id and queue id is projected down to
   `{ schemaVersion, heldCount }`. Two narrowings, not one, because a single one is a single
   point of failure.
4. **All tiers, no second gate.** The only gate is `0131`'s existing §30.3 module cap.
   `moderator_status_card` was already one of `0131`'s twenty catalogue keys, so no migration
   touched the catalogue, and no tier check exists anywhere in `0136`, the store, the route or
   the renderer.

## The negative test of the privacy property

Required by the task, and run rather than reasoned about. The method: temporarily widen
`app_private.list_overlay_moderator_status` so it returns a field it must never return, run
the SQL suite, observe the failure, then restore the function and re-run.

**The deliberate break.** Migration `0136`'s signature was changed to
`returns table (held_count bigint, supporter_display_name text)` and a second scalar
subquery added, pulling `alert_events.payload->>'donorDisplayName'` for one of the held
deliveries — i.e. exactly the class of thing §6 forbids on this path: a real supporter's
name, taken from a real held alert, leaving the database over an overlay read.

**Output with the break in place:**

```
  FAIL prf02_slice5_moderator_status
       ERROR:  the overlay moderator-status read must return the held COUNT and nothing else (§6: never private content, enforced as a property of the query). Declared result is "TABLE(held_count bigint, supporter_display_name text)", expected exactly "TABLE(held_count bigint)"
SQL SUITE: pass=62 fail=1
failed: prf02_slice5_moderator_status
```

**Output after restoring the function unchanged:**

```
  PASS prf02_slice5_moderator_status
SQL SUITE: pass=63 fail=0
```

`pnpm explain:check` was re-run after the restore and reported `OK: 18/18 plans current`,
which independently confirms the restored function body is byte-identical to the one the
captured EXPLAIN artefact hashes — the revert was complete, not approximate.

The point of the exercise is that case S5.4 is a *live* assertion, not a comment that happens
to be true today: a future edit that adds a column to this function fails the suite by name,
and names the offending column in the failure message.

## Verification and what it is worth

Commands and counts are in `../tests/TC-PRF-02-slice-5-moderator-status.md`. Every one of
them ran locally — the Node test runner, JSDOM, and a local Dockerised PostgreSQL.

**None of it is production, provider, store, legal, device, network or release readiness, and
none of it may be represented as any of those.** The EXPLAIN artefact is a plan-shape change
detector captured on an unsized local database; it is not evidence that any §19.4 budget is
met, and it says so in its own body. RT-07 stays Blocked. "One source replaces twelve" stays
unmarketable — eight of twenty modules is not a canvas. The privacy property proven here is
about this one read path and nothing wider.

## Things a reader should be sceptical of, stated rather than buried

- **Self-review only.** Nobody independent looked at this. The scope review that authorised
  the slice was independent; the implementation review is not.
- **The zero-case decision is a judgement, not a derivation.** Hiding the card at zero is
  argued in the task record's Decisions and is genuinely arguable the other way — a creator
  cannot distinguish "nothing held" from "the module never mounted". The alternative was a
  permanent zero badge, which is chrome carrying no information for an entire broadcast, and
  a reassuring string this slice has no authority to write. The choice matches every other
  built module's hide-on-nothing behaviour; it is recorded so it can be overturned cheaply.
- **The captured plan shows a sequential scan on `alert_queues`.** Honest at seed size, and
  not fixed by this slice: `alert_queues(channel_id)` has no index today, and adding one
  changes plan shapes for queries this slice does not own. Referred, not silently patched.
- **Concurrency.** Another agent owns migration `0135` in parallel. This slice wrote `0136`
  only, renumbered nothing, and did not read `0135` as authority. A test or migration count
  higher than this slice's own additions reflects that concurrent work, not this slice's.

## Referred to Opus

- **Safe mode needs its own record and decision.** Owner decision 1 says so; this slice did
  not write it. Until it exists, §6 #12's second half stays unbuilt.
- **`alert_queues(channel_id)` index.** A shared-table question that wants a realistic row
  count before anyone answers it.
- **`MASTER_CANVAS_BUILT_MODULE_KEYS` has been stale since slice 3.** Left stale here to match
  slices 3 and 4 rather than diverge silently. Nothing reads it; it should be fixed or
  deleted, and that is a call for whoever owns the constant.
