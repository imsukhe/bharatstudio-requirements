# PRF-02 slice 6 — Giveaway / Tournament (§6 #17): the decisions this implementation took, and what each rests on

**Date:** 2026-09-17
**Owner:** **Sukhdev Singh**
**Task:** `../active/tasks/PRF-02-slice-6-giveaway-tournament.md`
**Acceptance:** `../tests/TC-PRF-02-slice-6-giveaway-tournament.md`
**Binding owner decisions:** `2026-09-16-prf-02-slice-6-owner-decisions.md` decisions 4 and 5
**Builds on:** `2026-09-16-prf-02-slice-6-lobby-status-decisions.md` and migration `0140`
**Reviewer:** self-review only. **No independent review occurred**, and none is claimed.

Every decision below is recorded with the thing it rests on, because the standing constraint is
that no numeric limit, provider behaviour, legal wording or pricing may be invented.

---

## 1. The minimum schema is two tables, and neither carries a participant

**Decision.** `public.giveaways` carries `entry_count`, `entry_opens_at` and `entry_closes_at` plus
a lifecycle. `public.tournaments` carries `current_round` and `completed_matches_in_round` plus a
lifecycle and a **reference to a `public.lobby_sessions` row**. There is no entrant table, no
participant table, no match table, no team table and no per-viewer row anywhere in `0142`.

**Why this is the minimum rather than a shortcut.** §17.1's overlay sentence is "entry count, time
remaining, winner announcement with consent, and a claim flow". Two of those four are buildable
(see §5 below for why the other two are not), and rendering them needs exactly one integer and one
instant. §17.2's overlay contribution is the "standings overlay module" (`TRN-05`); rendering
bracket progress needs exactly one round number and one completed-match count.

**Why storing counts is the stronger privacy position, not the weaker one.** With no entrant or
participant column existing anywhere in this migration, "the overlay read can never return a
participant identifier" holds **by construction** rather than by projection discipline — there is
nothing for a future read to start returning, and nothing two visits could be joined on. This is
the identical argument `0140` made for `lobby_sessions`, and it is asserted the same way, against
`information_schema.columns`.

**The cost, stated rather than glossed.** The entry count and the bracket progress are as accurate
as whoever reports them, and in this slice that is the creator, because no entry path and no match
record exists. Deriving them would mean building the entry subsystem and the match subsystem, which
is the whole of §17. Referred as a product question, not patched with an invented derivation.

---

## 2. Single elimination, and why it is the *only* bracket type that could ship

**Decision.** Single elimination. Not double elimination, not round robin, not a points table.

**Three independent reasons, each sufficient on its own.**

1. **§30.3 and `TRN-01`/`TRN-01b` place them at different tiers.** `Tournaments — single elim, up
   to 8` is `— | — | yes | yes` (Creator+). `Tournaments — double elim, round robin, seeding,
   sponsor slots` is `— | — | — | yes` (Studio only). The entitlement owner decision 5 authorises
   is `tier in ('creator','studio')` **or** a pack grant — one gate, not two. Shipping a
   Studio-only format behind a Creator+ gate would be implementing a tier nobody decided.
2. **A points table is not a bracket, it is a standings table keyed on participants.** It cannot be
   rendered at all without participant labels (see §6).
3. **Round robin and double elimination have no single "current round" that is arithmetic.** In
   single elimination the entire bracket shape is determined by the field size: round *r* has
   `field / 2^r` matches, and there are `log2(field)` rounds. Nothing has to be stored, chosen or
   invented. Double elimination has a losers' bracket whose length depends on a seeding convention,
   and round robin's schedule depends on a pairing algorithm — both are choices, and choices are
   what this slice is forbidden to make.

**Not one numeric bound in `0142` was chosen by its author.**

| Constraint | Where it comes from |
|---|---|
| field size in `{2, 4, 8}` | §30.3's `up to 8` gives the ceiling; power-of-two is the arithmetic of single elimination **without byes**, and byes are part of seeding (`TRN-02`), which is not built |
| `current_round between 1 and 3` | `log2(8) = 3`. The ceiling is §30.3's `8`, not a preference |
| `completed_matches_in_round between 0 and 4` | `8 / 2 = 4` is the largest a round can be at field size 8. Same source |
| the exact per-tournament bound `completed_matches_in_round <= field >> current_round` | Arithmetic of the format, enforced in `set_tournament_progress` because it depends on the referenced lobby row and a table check constraint cannot reach another row |
| `entry_closes_at > entry_opens_at` | Arithmetic: a window that closes before it opens is not a window |
| `concluded_at >= started_at`, `closed_at >= opened_at` | The same shape `0135` uses for `ended_at >= started_at` and `0140` for `closed_at >= opened_at` |
| one open giveaway and one running tournament per channel | §12.7's bounded read as a database guarantee — the same partial unique index `0140` and `0135` already use |

**There is no duration, countdown, timer or deadline column.** `entry_closes_at` is an instant the
**creator supplies**, because §17.1 names the entry window as something the creator defines and
publishes before entry opens. That is the difference from `0140`, which refused a lobby duration:
there, §16 named no such value and choosing one would have been inventing a number; here the
authority names the value and the creator provides it.

---

## 3. The tournament references `0140`'s lobby; it does not duplicate it

**Decision.** `tournaments.lobby_session_id` is a `not null` foreign key to
`public.lobby_sessions(id)` from migration `0140`, and **the bracket's field size is the referenced
lobby's `seat_count`**. There is no field-size, seat-count, confirmed-seat-count, queue-count,
queue-policy, ready-check or participant column on `tournaments` at all.

**Why the field size is not stored.** §17.2 says tournaments are "built on the Lobby Engine rather
than beside it". The strongest reading of that is not "point at a lobby and then keep your own copy
of its size" — it is that the lobby row **is** where the session's size lives, and the tournament
adds only what the lobby does not have: where the bracket has got to. So `start_tournament` reads
`lobby_sessions.seat_count`, refuses a lobby whose seat count is not 2, 4 or 8, and stores nothing;
the overlay read derives `total_rounds` and `matches_in_round` from that same column at read time.
Deleting the duplicate removes the entire class of drift where a tournament says 8 and its lobby
says 16.

**The cost, stated.** A creator running an 8-team bracket on a 16-seat squad lobby cannot start a
tournament, because teams do not exist in this schema — only seats do. That is a refusal with a
readable error, not a wrong render, and the alternative (a team concept) is a product surface
nobody decided.

**What is deliberately not inherited.** `start_tournament` requires the lobby to be **open** at the
moment the tournament starts, but the tournament does not end when the lobby is closed: the lobby
row stays durable (§12.6) and the overlay read joins it by id rather than by `closed_at`, so
closing the lobby does not silently blank a running bracket.

---

## 4. There is no randomness primitive anywhere, and that is asserted structurally

**Decision.** `0142` contains no `random()`, no `setseed`, no `tablesample`, no shuffle, no weighted
selection, no odds, no seed column, no draw column and no winner column. `gen_random_uuid()` is used
for primary keys, exactly as `0140` uses it, and is the **only** token in the file containing the
substring `random`.

**Why this is asserted rather than asserted-in-prose.** §17.1's decision of **2026-09-13** —
which predates and is independent of `GIV-07` — restricts giveaways to "free-entry and skill-based
formats only" and states that supporter-weighted odds are not built. `GIV-07` separately gates
chance-based formats on legal review that has not happened. A rule that lives only in a comment is
a rule a future edit can remove without anything turning red, so
`packages/db/tests/prf02_slice6_giveaway_tournament.sql` scans every shipped `app_private` function
definition for a randomness or selection primitive and fails by name on any of them. That is the
same structural shape `0140`'s "nothing can grant the Events Pack" assertion already uses.

**`GIV-07` is untouched.** Nothing in this slice closes it, narrows it, or may be described as
progress against it. It stays `Blocked`.

**Paid entry is impossible by construction, not by policy.** There is no entry path in this slice at
all — `entry_count` is a number the creator reports — so there is nothing for a payment to gate. The
SQL test additionally asserts that no price, amount, currency, paise, plan, subscription or billing
token appears in any of `0142`'s functions.

---

## 5. The card cannot show a winner in this slice, and that is the correct conclusion

Owner decision 4 anticipated this and said so: if the card cannot show a winner, that is the answer,
and it must not be approximated by a creator-records-the-winner surface.

**Three separate blocks, any one of which is enough.**

1. **Consent does not exist.** §17.1 permits a winner announcement *with consent*. No consent
   mechanism exists anywhere in this schema, and building one is explicitly out of scope. §16's
   ruling that opted-in initials and avatars need an opt-in mechanism that does not exist is the
   same ruling in a different costume.
2. **A winner is a participant identifier.** The overlay read's declared result type is aggregate
   columns only, and no participant identity exists in `0142` to name. Displaying one would require
   inventing a display-name concept, which the scope forbids in terms.
3. **There is no mechanism that could produce one.** The draw is not built (§17.1's 2026-09-13
   decision plus `GIV-07`), and "the creator types who won" is the invented surface decision 4 names
   outright.

**Consequently the tournament card has no terminal state either.** When a creator concludes a
tournament, the overlay read returns nothing for it — the same nothing a channel with no tournament
returns. There is deliberately no "Final complete" or "Champion decided" copy, because a terminal
label on a bracket is a winner announcement with the name left out, and it invites the obvious next
edit.

---

## 6. The bracket TENSION, reported rather than solved

**The tension, stated plainly.** A bracket *tree* — the thing most people picture when they read
"bracket" — is a diagram of who plays whom. It is meaningless without participant labels. §16
already ruled that opted-in initials and avatars need an opt-in mechanism that does not exist, and
the same ruling binds here.

**So the bracket tree is not built, and no display-name concept was invented to make it buildable.**

**What ships instead, and why it is not a consolation prize.** Bracket **progress**: the current
round, the total number of rounds, how many matches in the current round are complete, and how many
there are. "Round 2 of 3 · 2 of 4 matches complete" is a true, complete and useful statement of
where a tournament has got to, it is what a viewer joining mid-stream actually needs, and it
requires no participant label at all. §17.2's own overlay contribution is a "standings overlay
module"; this is the part of it that can be aggregate-only.

**What this costs.** The card cannot show who is still in. That is a real reduction in what §17.2
describes, it is stated here rather than hidden, and closing it needs a product decision about
participant consent that nobody has made.

---

## 7. The entitlement is `0140`'s function, called and not rewritten

`app_private.events_pack_entitled(uuid)` is called from **exactly one place** in this slice: the
overlay read. It is not reimplemented, not copied and not modified — `0142` does not contain the
pack grant key at all, which keeps `0140`'s own "nothing can grant the Events Pack" assertion (which
scans every `app_private` function except the check itself) true after this migration lands.

`open_giveaway`, `update_giveaway_entry_count`, `close_giveaway`, `start_tournament`,
`set_tournament_progress`, `conclude_tournament`, `list_channel_giveaway` and
`list_channel_tournament` read **no tier and call no entitlement function** (§12.6). Their only gate
is `app_private.has_channel_role`, in SQL, the same gate `0135`, `0140` and `0131` use. A Pro
creator may open a giveaway, report entries, start and advance a tournament and read all of it back;
what they do not get is the Canvas module painting it on a broadcast.

**No price is implemented.** §33's Rs 129/mo stays in the authority. Purchase, when it is built, is
website-only per the standing constraint, and it is not built here.

---

## 8. A contradiction in the authority, surfaced rather than silently resolved

§30.3 contains **two rows that disagree about tournaments**:

- `Tournament standings` (in the Master Canvas module block) — `— | — | — | yes`, i.e. **Studio**.
- `Tournaments — single elim, up to 8` (in the Community block) — `— | — | yes | yes`, i.e.
  **Creator+**.

Owner decision 5 settles the §16/§17 entitlement as `tier in ('creator','studio')` or a pack grant,
which matches the second row. This slice implements that, and ships **only** the single-elimination
up-to-8 form — so for what actually ships, the two rows do not conflict. The broader question of
whether a richer standings surface is Creator+ or Studio is left to the owner and is recorded in the
task record's "Referred to the owner" section rather than decided here.

---

## 9. What this record is not

A product decision record; the product decisions are the owner's, in
`2026-09-16-prf-02-slice-6-owner-decisions.md`. Nothing here is production, provider, store, legal,
device, network or release readiness. `RT-07` remains `Blocked`. The EXPLAIN artefact is a
plan-shape change detector captured against a minimally-seeded local database and is **not** §37.4
production-scale evidence. **`GIV-07`'s legal gate is untouched and stays `Blocked`.**
