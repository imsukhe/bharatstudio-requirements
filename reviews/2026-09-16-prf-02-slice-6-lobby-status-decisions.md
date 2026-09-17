# PRF-02 slice 6 — Lobby Status (§6 #16): the decisions this implementation took, and what each rests on

**Date:** 2026-09-16
**Owner:** **Sukhdev Singh**
**Task:** `../active/tasks/PRF-02-slice-6-lobby-status.md`
**Acceptance:** `../tests/TC-PRF-02-slice-6-lobby-status.md`
**Binding owner decisions:** `2026-09-16-prf-02-slice-6-owner-decisions.md` decisions 4 and 5
**Reviewer:** self-review only. **No independent review occurred**, and none is claimed.

Every decision below is recorded with the thing it rests on, because the standing constraint is
that no numeric limit, provider behaviour, legal wording or pricing may be invented.

---

## 1. The minimum schema is three integers on one session row, and no viewer table at all

**Decision.** `public.lobby_sessions` carries `seat_count`, `confirmed_seat_count` and
`queue_count` as columns on the session, written by the creator. There is no waitlist table, no
participant table and no per-viewer row anywhere in this migration.

**Why this is the minimum rather than a shortcut.** §16 L3002–3003 says the public overlay shows
"aggregate status only: '8/16 seats confirmed', queue count". Rendering that needs exactly three
numbers and a lifecycle to scope them to. A per-viewer waitlist would be the *source* of two of
those numbers, but it is also the whole of §16.2 — selection policy, locked-and-displayed,
promotion, no-show expiry, the redacted audit log — which owner decision 4 does not authorise.

**Why storing counts is the stronger privacy position, not the weaker one.** Owner decision 4
forbids "a per-viewer row on the overlay path, and nothing that correlates one visit to another".
With no viewer column existing anywhere in this schema, that is true by construction rather than
by projection discipline: there is nothing for a future read to start returning, and nothing two
visits could be joined on. `L16.23` asserts that against `information_schema.columns`.

**The cost, stated rather than glossed.** The numbers are as accurate as whoever reports them. In
this slice that is the creator or their tooling, because the mechanism that would derive them does
not exist yet. That is referred as a product question, not patched with an invented derivation.

---

## 2. Not one numeric bound in `0140` was chosen by its author

| Constraint | Where it comes from |
|---|---|
| `seat_count >= 1` | Arithmetic, not a policy: a lobby with zero seats cannot render "0/0 seats confirmed" as a status. **No upper bound is set** — §16 states no maximum seat count and this file will not invent one |
| `confirmed_seat_count >= 0`, `queue_count >= 0` | A count cannot be negative |
| `confirmed_seat_count <= seat_count` | The arithmetic of "8/16": a lobby cannot confirm more seats than it has |
| `closed_at >= opened_at` | The same shape `0135` already uses for `ended_at >= started_at` |
| One open lobby per channel | §12.7's bounded read as a database guarantee — the same partial unique index `stream_missions_channel_running_idx` (`0135`) already uses, for the same reason |
| `maximum: 2147483647` on the API's `seatCount` | PostgreSQL `integer`'s own range, so an out-of-range value is a 400 rather than a 500. A storage bound, not a product bound, and it is named as such in the route |

**There is no duration, timer, expiry, deadline, countdown or scheduled-end column of any kind**,
and there must never be one added quietly — §16.1's "time" descriptor is part of step 1's session
setup, which is out of scope here, and choosing a lobby duration would be inventing a number.

---

## 3. The entitlement: `tier in ('creator','studio')` OR a pack grant nothing can grant

**Decision.** `app_private.events_pack_entitled(channel)` is

```
app_private.current_channel_tier(channel) in ('creator', 'studio')
  or  (the channel's latest entitlement values -> 'eventsPack' ->> 'active') = 'true'
```

**Why the pack side reads `channel_entitlement_versions.values` and not a new grants table.** A
grants table would itself be a grant path: it would need a shape, a lifecycle and an expiry, all
of which are undecided, and any of them would be a product surface nobody asked for. Reading a key
out of the entitlement store that already exists adds nothing and decides nothing.

**The one reason nothing can currently make it true.** `channel_entitlement_versions.values` is
never caller-supplied. Every writer in the schema builds it server-side: the publishers
(`0048`, `0070`, `0080`) write `app_private.tier_entitlement_dimensions(tier)` verbatim, and the
admin override (`0074`) writes that value merged with exactly two literal keys, `queueCount` and
`adminOverrideReason`. `tier_entitlement_dimensions` emits no `eventsPack` key for any tier. So no
publisher, no admin, and no API caller can produce one — asserted in `L16.15` against every
`app_private` function definition, not against this paragraph.

**This is the configured-but-unset discipline, applied to an entitlement.** The six existing
instances (`overlayMaxInstanceSubscribers`, `overlayMaxChannelSubscribers`,
`derivedReadMaxConcurrent`, `derivedReadPoolMax`, `derivedReadStatementTimeoutMs`,
`reactionCloudSampleMax`) build the mechanism, read the value, and let absent mean today's
behaviour rather than a guess. Here the mechanism is the `or`, the value is the grant, and absent
means exactly "included at Creator+" — which is precisely what §30.3's row says today.

**No price is implemented.** §33's ₹129/mo stays in the authority. `L16.16` asserts that no price,
amount, currency, paise, plan, subscription or billing token appears in `0140` at all.

---

## 4. The prohibitions are enforced on the declared result type, exactly as `0136` and `0139` do

`app_private.list_overlay_lobby_status` declares

```sql
returns table (seat_count integer, confirmed_seat_count integer, queue_count integer)
```

and `packages/db/tests/prf02_slice6_lobby_status.sql` asserts that set twice — from
`pg_get_function_result`, and from a table materialised out of a live call and read back through
`information_schema.columns`. A room code, a password, a seat token, a player identifier, an
in-game name, a Discord name, a viewer id, an anonymous identity or a session id cannot be added
without changing the declared signature, which turns that file red by name.

It is not merely withheld, either: **none of those things exists in this schema**. There is no
column to expose, in `lobby_sessions` or anywhere else `0140` creates.

**Why the lobby id is not returned.** It would carry no information the card paints, and "a
session id" is on the prohibited list. Three numbers is the whole projection.

---

## 5. The tier gate is on the module, never on the creator's own record

`app_private.open_lobby_session`, `update_lobby_session_counts`, `close_lobby_session` and
`list_channel_lobby_session` read **no tier and call no entitlement function**. The role gate
(`app_private.has_channel_role`) is the only gate on them, and it lives in SQL — the same place
`0135`'s mission functions and `0079`'s payout-onboarding setting put theirs.

`app_private.events_pack_entitled` is called from exactly one place: the OVERLAY read. A Pro
creator can open a lobby, report seats, close it and read it back at any time; what they do not
get is the Canvas module painting it on a broadcast. That is §30.3's row implemented literally,
and it is the direction §12.6 requires.

---

## 6. Where the line against the full Lobby Engine falls, restated as a rule

**If the card can render without it, it is out of scope.** The task record's table applies that to
every §16 feature. The three that are easiest to talk oneself into, and why each was refused:

- **The ready check.** It is §16.4's own "highest-value feature", which is exactly why it is not a
  side effect of a card slice. The card reads `confirmed_seat_count`; how a seat became confirmed
  never reaches the overlay.
- **Seat tokens and the room-code reveal.** §16 forbids both on the overlay in the same sentence.
  Building the storage "for later" would create the column the prohibition exists to prevent.
- **Automatic deletion of temporary lobby data (§16.1 step 8).** There is no temporary lobby data
  in this slice — no tokens, no codes, no per-viewer rows — so a deletion job would be a retention
  policy for an empty set, and retention policy is not this slice's to decide.

---

## 7. What this record is not

A product decision record; the product decisions are the owner's, in
`2026-09-16-prf-02-slice-6-owner-decisions.md`. Nothing here is production, provider, store,
legal, device, network or release readiness. `RT-07` remains Blocked. The EXPLAIN artefact is a
plan-shape change detector captured against a minimally-seeded local database and is **not**
§37.4 production-scale evidence. `GIV-07`'s legal gate is untouched and module #17 is not started.
