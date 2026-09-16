# PRF-02 safe mode — implementation review and decision record

**Date:** 2026-09-16
**Owner:** **Sukhdev Singh**
**Task:** `../active/tasks/PRF-02-safe-mode.md`
**Acceptance:** `../tests/TC-PRF-02-safe-mode.md`
**Authority:** `2026-09-16-prf-02-slice-6-owner-decisions.md` decision 3 — **not restated here**
**Reviewer:** the implementing agent. **Independent fresh review was unavailable**, so this is
self-review and the task closes at `Conditionally complete` at best. Nothing below is production,
provider, store, legal, device, network or release readiness.

---

## Decision log

| # | Decision | Status |
|---|---|---|
| 1 | Safe mode is `public.channels.safe_mode_enabled boolean not null default false` — a column on the channel-scoped table, matching `alert_queues.is_paused` / `channels.accepting_tips` / `channels.featured_consent`, not a new table or row | Implemented |
| 2 | `app_private.initial_delivery_status(uuid)` is the single place that decides a new delivery's status; the three functions that insert deliveries call it instead of writing the literal `'ready'` | Implemented |
| 3 | A safe-mode hold reuses the existing `hold_reason = 'moderation'`; the check constraint is untouched and the existing `approve` path releases it unchanged | Implemented |
| 4 | Turning safe mode off releases nothing. Already-held deliveries stay held and are reviewed individually. **No bulk release was built and none is decided** | Implemented |
| 5 | The overlay projection grows by exactly one boolean; slice 5's column-set assertion is extended in place to the new declared type, never deleted | Implemented |
| 6 | Creator read and write are gated by `has_channel_role(channel, ['owner','admin'])` only — never by tier | Implemented |
| 7 | The card shows safe-mode state alongside the held count and is visible when either is true; slice 5's "no all-clear copy" is preserved for the both-quiet case | Implemented |

## The constraint that shaped this most, and how it was kept

The owner decision says safe mode is **never automatic**. The temptation in a moderation feature is
to add "turn it on when X exceeds Y in window Z", and every one of those letters would have been an
invented number. None exists: `initial_delivery_status` reads one boolean off one row and returns
one of two string literals. `set_channel_safe_mode` writes one boolean. There is no timestamp
comparison, no aggregate, no interval and no counter anywhere in either. `packages/db/tests/
prf02_safe_mode.sql` case SM.11 asserts that against the shipped function definitions rather than
against this paragraph.

## Where the status is first assigned, and why the change is there

Three live functions insert into `public.event_outbox_deliveries`, and all three hard-coded
`'ready'`:

- `app_private.create_manual_alert` — latest definition `0019` L86
- `app_private.record_verified_payment_webhook` — latest definition `0028` L247
- `app_private.record_youtube_alert_event` — latest definition `0117` L483

There is no shared helper they all pass through, so "the place where status is first assigned" is
three places. `0138` re-declares all three with the literal replaced by
`app_private.initial_delivery_status(<that function's channel id>)`, and the hold reason by
`app_private.initial_delivery_hold_reason(<that status>)`. The three bodies are otherwise identical
to their current definitions — extracted mechanically from the source migrations rather than
retyped, because one of them is the verified-payment-webhook path and a transcription error there
would be a money bug.

**A trigger was considered and rejected.** `before insert on event_outbox_deliveries` would have
been fifteen lines instead of five hundred, but it would have been a **fourth** place — one that
silently overrode three literals still reading `'ready'`, which is exactly the "second place that
can disagree" the brief forbids. The cost of the honest version is a long migration; the benefit is
that reading any of the three functions tells you the truth.

## Why no dispatcher change was needed

`held` is already excluded from both `app_private.claim_event_delivery` and
`app_private.list_ready_event_deliveries` (`0062` L166, L188 — `status in ('pending','ready',
'failed_retriable')`). So routing a new delivery to `held` is sufficient on its own: the alert is
never leased, never dispatched, never displayed, and `app_private.refresh_event_outbox_status`
(`0015` L28) already treats a held delivery as keeping its outbox `pending`. This was verified by
reading those functions before the migration was written, and is asserted by case SM.5 rather than
assumed.

## What turning safe mode off does — stated plainly because it is the question most likely to be got wrong

**Nothing happens to alerts already held.** They stay `held`, they keep `hold_reason = 'moderation'`,
their `state_version` does not move, and they are reviewed one at a time through
`app_private.apply_moderation_action`. Only the routing of *new* deliveries changes.

That is a real answer, not a gap. A bulk release would fire an unknown number of unreviewed alerts
onto a live broadcast the instant a creator flips a switch — irreversible once played, and a
moderation product behaviour nobody has decided. Case SM.6 proves the holds survive the toggle and
that the next new delivery is `ready`; case SM.7 proves the existing per-event approve path still
releases one.

## Privacy and bounded data

- The overlay projection is **one integer and one boolean**. §6's "never private content" stays a
  property of the query: nothing that identifies a supporter, a message or an amount can leave the
  database on this path without changing the function's declared `returns table` signature, which
  case S5.4 asserts by exact string.
- §12.7: two scalars. The card cannot fetch more than it can display because there is nothing more
  to fetch.
- §9.1.1: the renderer's options remain plain values and function references. No URL, HTML, CSS or
  script field was added.
- No new personal-data class. The switch is channel state, written by an owner/admin.

## Residual risk, stated rather than smoothed over

1. **`0138` is a long migration** because it re-emits three existing function bodies. The risk is a
   silent transcription difference. Mitigated by extracting the bodies mechanically and by a
   post-extraction diff showing the only textual changes are the status/hold-reason expressions and
   one added local declaration per function — but it is still the largest thing to check in review.
2. **`alert_queues(channel_id)` still has no index.** Unchanged from slice 5, still an open question
   for whoever can measure a realistic per-channel queue count, still not patched speculatively.
3. **`MASTER_CANVAS_BUILT_MODULE_KEYS`** in `apps/api/src/domain/master-canvas-store.ts` is still
   stale, as slice 5 recorded. Not touched here either; it remains a documentation drift someone
   should decide about.
4. **No dashboard UI** exists for the switch. The creator routes are the API surface; the canvas
   designer/dashboard is out of PRF-02's scope, as it was for every prior slice.

## A defect this work found in itself, and fixed

**`enabled: null` silently turned safe mode OFF in the first version of the creator route.** With
the API's normal `type: 'boolean'` declaration and Fastify's default AJV `coerceTypes`, `null` was
MEASURED to coerce to `false` and answer `200` — an uninitialised form field or a cleared client
state would have released a channel's held alert flow onto a live broadcast with nobody asking, and
that is not recoverable by retrying once the alerts have played.

The route now declares the two allowed **values** (`enum: [true, false]`) rather than a type, which
removes AJV coercion entirely: `null`, `"true"`, `1` and `"on"` are all 400. This is **stricter than
every other boolean field in this API**, and that deviation is deliberate, recorded in the route's
own header and in the OpenAPI description, and carries a real cost — a client sending `"true"` now
gets a 400 where another route would accept it. For a switch that decides whether a channel's alerts
reach a live broadcast, that is the right trade. It was found by writing the case and running it,
not by reading the code.

## Verification

Recorded in `../tests/TC-PRF-02-safe-mode.md`'s "Commands run" table, which is the single place this
work's numbers live so the two records cannot drift apart. Summary: `SQL SUITE: pass=64 fail=0`;
API `628/628`; web `482/482`; API build clean; contracts, `explain:check` (`OK: 18/18 plans
current`) and `harness:check` all green.

## Negative tests

Two, both against throwaway databases with the repository never modified, both reproduced in full in
`../tests/TC-PRF-02-safe-mode.md`:

1. **The never-automatic guard.** `initial_delivery_status` was given the exact forbidden change —
   safe mode engaging on a spike, threshold 10, one-minute window. `prf02_safe_mode.sql` failed by
   name on case SM.11; with the shipped definition restored it passes.
2. **Slice 5's column-set assertion, to prove extending it did not weaken it.** A third column
   (`channel_id uuid`) on the overlay projection made `prf02_slice5_moderator_status.sql` fail on
   case S5.4 with the new expected type printed; restored, it passes.

## Register

**No state letter is self-assigned.** PRF-02's register row is unchanged by this record.
