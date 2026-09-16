# PRF-02 — Safe mode (§6 module #12, the other half)

**Register row:** PRF-02 (state letter unchanged; no state letter is self-assigned — §0's own rule).
**Owner:** **Sukhdev Singh**
**Status:** `Conditionally complete — implemented and locally verified; independent review
unavailable; PRF-02's register row unchanged`.
**Classification:** **L3** — it changes a migration, adds a durable schema column, changes the
initial state of an alert delivery, and changes a published overlay contract.

**Authority:**
- `../../reviews/2026-09-16-prf-02-slice-6-owner-decisions.md`, **decision 3**. That record is the
  whole authorisation for this work and is deliberately **not restated here**.
- `../../FULL-PRODUCT-DEFINITION.md` §6 module #12, §9.1.1, §12.6, §12.7, §19.4, §30.3.
- `../../reviews/2026-09-16-prf-02-slice-5-scope-review.md` (classified #12 `NEEDS-READ-PATH` with
  safe mode deferred behind its Q1 — this task closes that deferral).
- `PRF-02.md`'s "Slice 5 — Moderator Status Card (§6 #12), held half only" section, whose
  "Referred to Opus" note records that safe mode had no record of its own. **This file is that
  record.** `PRF-02.md` is deliberately **not edited** by this task: a concurrent agent owns work
  in it, and every artefact here carries `safe-mode` in its name so the two cannot collide.

**Migration number:** `packages/db/migrations/0138_v1_prf02_safe_mode.sql`, assigned by the
coordinator. `0139` is owned by a concurrent agent and is never written or renumbered here.

---

## What this builds, stated as the boundary rather than as a feature list

Safe mode is a **creator switch**. While it is on, a newly created alert delivery for that channel
is written with `status = 'held'` instead of `status = 'ready'`, so it waits for the creator or a
moderator instead of reaching the overlay. The creator turns it on and turns it off.

**It is never automatic.** No spike detector, no rejection-rate heuristic, no volume threshold, no
time window, no signal of any kind engages or disengages it. There is no number anywhere in this
work that decides when safe mode turns on, because choosing one would be making a product decision
the owner has explicitly not made. If a future change needs such a number, that is a new owner
decision, not a constant to pick in a migration.

**It is not `alert_queues.is_paused`.** That flag is a queue lifecycle state and stays exactly what
it is. Nothing here reads it, renames it, or surfaces it under a safe-mode label. The SQL
acceptance test asserts that against `pg_get_functiondef`, not against a comment.

---

## Decisions this implementer had to make, and the reasoning for each

Each of these is a scoping decision no authority states. They are recorded so they can be argued
with later rather than rediscovered.

### D1 — The state is a column on `public.channels`, not its own row or table

`safe_mode_enabled boolean not null default false` on `public.channels`.

**Why a column, and why that table.** The instruction was to prefer whatever the codebase's
existing moderation state already does, and the codebase is consistent: every durable,
single-valued, always-present, creator-toggled state in this schema is a boolean column on the row
it belongs to — `alert_queues.is_paused` (`0001`), `channels.accepting_tips` (`0001`),
`channels.featured_consent` (`0072`). Safe mode has exactly that shape.

`channels` rather than `alert_queues` because the owner's decision says **per-channel**: a creator
turning safe mode on means "hold everything for this channel", not "hold everything on this one
queue". A per-queue flag would immediately raise a question nobody has answered (what does a
channel-level switch do to a queue whose own flag disagrees?), and `alert_queues` already carries
`is_paused`, which this must never be confused with.

**Why not its own row.** A row-per-channel table would need an absence-means-off convention, a
second write path to create the row, and a join on the **delivery insert path** — the hottest write
in the product. A column on the channel row is one already-reachable field. `stream_missions`
(`0135`) got its own table because a mission is a record with content and a lifecycle; safe mode is
one bit of current state with neither.

**Nothing else is added.** No `safe_mode_enabled_at`, no actor column, no history table. Each would
be a durable field no authority asks for, and "when was it turned on" is not a question any
authority poses. `channels.updated_at` already moves.

### D2 — Status is decided in ONE function, called from the three places that insert a delivery

`app_private.initial_delivery_status(target_channel_id uuid) returns text` is the only thing in the
schema that decides whether a new delivery starts `ready` or `held`.

The literal `'ready'` was hard-coded at **three** live insert sites —
`app_private.create_manual_alert` (`0019`), `app_private.record_verified_payment_webhook` (`0028`)
and `app_private.record_youtube_alert_event` (`0117`). Migration `0138` re-declares those three
functions with that literal replaced by a call to the new function, so there is exactly one place
that decides and three places that ask.

A trigger rewriting the status after the fact was **rejected**: it would be a fourth place, silently
disagreeing with three literals that still read `ready`.

The three re-declared bodies are otherwise **byte-identical** to their current definitions. They
were extracted mechanically from `0019`/`0028`/`0117` rather than retyped, precisely because one of
them is the payment webhook path.

### D3 — The hold reason is the existing `'moderation'`, not a new one

`event_outbox_deliveries.hold_reason` is constrained to `('moderation', 'operator')` (`0062`). A
safe-mode hold is a delivery **awaiting a moderator's decision**, which is what `'moderation'`
already means — and it is what makes the existing release path work unchanged:
`app_private.apply_moderation_action(..., 'approve')` releases held deliveries whose
`hold_reason = 'moderation'` (`0062` L117–L120). Adding a `'safe_mode'` reason would have required
widening that check constraint **and** teaching the approve path about it — duplicating the held
path instead of reusing it. The constraint is untouched.

### D4 — Turning safe mode OFF releases nothing. Already-held alerts stay held

**This is the answer, and it is deliberate.** Switching safe mode off changes the routing of
**newly created** deliveries only. Every delivery already sitting at `held` stays `held` and is
reviewed one at a time through the existing `app_private.apply_moderation_action` path (`approve`
to release it, `suppress` to drop it) — the same path a manually held delivery has always used.

No bulk release is built, because no bulk release has been decided. Auto-releasing a backlog on
toggle-off would mean a creator flipping a switch causes an unknown number of unreviewed alerts to
fire onto a live broadcast at once — a moderation product behaviour with real on-stream
consequences that nobody has asked for, and one that is not reversible once the alerts have played.

This is asserted rather than promised: `packages/db/tests/prf02_safe_mode.sql` turns safe mode on,
creates deliveries, turns it off, and asserts (a) the already-held ones are still `held` with their
`hold_reason` intact, (b) the next new delivery is `ready`, and (c) the existing `approve` action
still releases a safe-mode-held delivery.

### D5 — The overlay projection grows by exactly one boolean, and the slice-5 assertion is updated, never deleted

`app_private.list_overlay_moderator_status` now returns
`table (held_count bigint, safe_mode boolean)`. PostgreSQL cannot change a function's OUT columns
with `create or replace`, so `0138` drops and re-creates it — the same mechanic `0127` already used
for `get_overlay_events`.

Slice 5's assertion that the projection is "the held count and nothing else" is **extended in
place** in `packages/db/tests/prf02_slice5_moderator_status.sql`: case S5.4 now asserts the exact
string `TABLE(held_count bigint, safe_mode boolean)`, and case S5.5 now asserts that the shipped
definition still never references `is_paused` or `closed_at` while positively requiring that it
reads `safe_mode_enabled`. Neither case is deleted or weakened; both still fail by name the moment
a third column appears.

§6's "never private content" stays a property of the query: a boolean is not a supporter, a message
or an amount, and the column-set assertion still refuses anything that is.

### D6 — Creator read and write are never tier-gated

§12.6: storing, viewing and changing a durable creator record is available at every tier. Safe mode
is a moderation control, not a rendering feature. The §30.3 module cap (`0131`) governs only whether
the Canvas **renders** the Moderator Status Card; it has nothing to say about whether a creator may
turn safe mode on. There is no tier check anywhere in the new routes, the new store or the new SQL
functions.

The only gate is the existing role gate:
`app_private.has_channel_role(channel, ['owner','admin'])`, the same one
`app_private.skip_payout_onboarding` (`0079`) uses. A non-owner/admin gets the codebase's existing
indistinguishable answer (`404 not_found`), never a `403` that confirms the channel exists.

### D7 — The card shows safe mode alongside the count, and safe mode alone is enough to show it

Slice 5's card hid itself at `heldCount === 0`. It now shows whenever **either** something is held
**or** safe mode is on, because "safe mode is on" is itself the thing a creator needs to see
mid-stream — it is the reason nothing is reaching the overlay. Hiding it would leave a creator
staring at a silent overlay with no indication why.

Slice 5's deliberate absence of all-clear copy is preserved exactly: with safe mode off and nothing
held, the card renders nothing at all — no "All clear", no tick.

### D8 — The creator routes live in their own file

`apps/api/src/routes/safe-mode.ts`, registered beside the others in `app.ts`. Safe mode is a
moderation control, not a canvas module; `routes/master-canvas.ts` already takes six positional
dependencies, and `routes/interactions.ts` fifteen. The overlay read stays where slice 5 put it.

---

## Data impact

| | |
|---|---|
| **New table** | None |
| **New column** | One: `public.channels.safe_mode_enabled boolean not null default false`. Additive and defaulted, so every existing row reads `false` — today's behaviour exactly |
| **Changed constraint** | None. `event_outbox_deliveries_hold_reason_check` and the delivery `status` check are both untouched |
| **Personal-data class** | **None new.** The switch is channel state. The overlay projection is one integer and one boolean; no supporter, message, amount, delivery id, event id, queue id or viewer identifier exists on that path |
| **Append-only / payment semantics** | Preserved. No payment row, refund row, outbox row or delivery row is deleted or rewritten. A safe-mode hold changes a **new** delivery's initial status; it never drops a delivery, never fails a payment, and never removes money state. `held` is already a first-class state of the existing machine (`0001` L134) and is already excluded from `claim_event_delivery` / `list_ready_event_deliveries` (`0062`), so no dispatcher change was needed |
| **Provider / legal dependency** | None |

## Failure behaviour, kill switch, rollback

**Failure behaviour**
- **`initial_delivery_status` finds no channel row:** it returns `'ready'`. Failing open on the
  *routing* decision is correct — the alternative is a payment webhook that cannot create a
  delivery at all. It is `stable` and reads one primary-key row.
- **The creator store is unwired or throws:** the route answers `503`
  `safe_mode_store_unavailable`, `retryable: true`. Never a `500`, never a `401`.
- **The overlay read is unwired or throws:** unchanged from slice 5 — `503`
  `master_canvas_store_unavailable`, `retryable: true`.
- **An invalid / expired / revoked / foreign overlay token:** zero rows, so
  `moderatorStatus: null`. Unchanged from slice 5, and still distinguishable from a real
  `heldCount: 0, safeMode: false`.
- **The module throws twice:** the runtime's existing per-module error boundary marks it `down`;
  every other module keeps rendering.

**Kill switch.** Two, at different layers: the creator's own switch (off stops new holds
immediately), and the server-owned module toggle
(`app_private.upsert_master_canvas_module`) which removes the card from the Canvas without touching
the moderation behaviour.

**Rollback.**
- Delete `apps/api/src/domain/safe-mode-store.ts`, `apps/api/src/db/safe-mode-store.ts`,
  `apps/api/src/routes/safe-mode.ts`, `apps/api/test/prf02-safe-mode-routes.test.ts`,
  `packages/db/tests/prf02_safe_mode.sql`,
  `contracts/json-schema/channel-safe-mode-response.schema.json`,
  `contracts/fixtures/channel-safe-mode-response.json`.
- Revert the additive hunks in `apps/api/src/app.ts`, `apps/api/src/index.ts`,
  `apps/api/src/routes/master-canvas.ts`, `apps/api/src/domain/moderator-status-store.ts`,
  `apps/api/src/db/moderator-status-overlay-store.ts`,
  `apps/api/test/prf02-slice5-moderator-status-routes.test.ts`,
  `apps/web/app/overlay/canvas/modules/moderator-status-logic.ts`,
  `apps/web/app/overlay/canvas/modules/moderator-status-module.ts`,
  `apps/web/app/overlay/canvas/modules/moderator-status-logic.test.ts`,
  `apps/web/app/overlay/canvas/modules/moderator-status-module.test.ts`,
  `apps/web/app/overlay/canvas/[overlayId]/page.tsx`,
  `apps/web/app/overlay/canvas/master-canvas-integration.test.ts`,
  `contracts/openapi/v1.yaml`, `contracts/validate-fixtures.mjs`,
  `packages/db/explain-plans/required-queries.json`,
  `packages/db/explain-plans/moderator-status.explain.md`, and the two extended cases in
  `packages/db/tests/prf02_slice5_moderator_status.sql`.
- Migration `0138` reverses by re-applying `0019`, `0028`, `0117` and `0136`'s function bodies and
  then `alter table public.channels drop column safe_mode_enabled;`. The column is additive and
  defaulted, so dropping it restores the previous behaviour exactly. **No production migration
  without separate explicit approval.**

## Acceptance

`../../tests/TC-PRF-02-safe-mode.md` holds the cases and the real command output.

## Review

`../../reviews/2026-09-16-prf-02-safe-mode-implementation.md`. Independent fresh review is
**unavailable**; this is self-review, so this task closes at `Conditionally complete` at best.

## Outcome

Implemented and locally verified. The numbers live in one place only —
`../../tests/TC-PRF-02-safe-mode.md`'s "Commands run" table — so the two records cannot drift apart.
Summary: `SQL SUITE: pass=64 fail=0`; API `628/628`; web `482/482`; API build clean; contracts,
`explain:check` (`OK: 18/18 plans current`) and `harness:check` all green. Two negative tests, both
reproduced there in full.

**One defect was found in this work by this work and fixed**: `enabled: null` on the creator write
was measured to coerce to `false` under the API's shared validator configuration, silently turning
safe mode OFF. The route now declares the two allowed values rather than a type. Recorded in
`../../reviews/2026-09-16-prf-02-safe-mode-implementation.md`.

**Not built, and named rather than left implicit:** no dashboard UI for the switch (the canvas
designer/dashboard is outside PRF-02's scope, as for every prior slice); no bulk release on
toggle-off (undecided, see D4); no index on `alert_queues(channel_id)` (unchanged open question from
slice 5). Nothing here is production,
provider, store, legal, device, network or release readiness; local verification is local
verification. RT-07 stays Blocked and §19.4's budgets stay unclaimed. **No register state letter is
self-assigned.**
