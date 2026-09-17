# TC-PRF-02 slice 6 — Giveaway / Tournament Card (§6 #17) and the minimum §17 schema: acceptance record

**Date:** 2026-09-17
**Owner:** **Sukhdev Singh**
**Task:** `../active/tasks/PRF-02-slice-6-giveaway-tournament.md`
**Decisions:** `../reviews/2026-09-17-prf-02-slice-6-giveaway-tournament-decisions.md`
**Binding owner decisions:** `../reviews/2026-09-16-prf-02-slice-6-owner-decisions.md` 4 and 5
**Builds on:** `TC-PRF-02-slice-6-lobby-status.md` and migration `0140`

Written **before** implementation, per `governance/AGENTS.md`. The "Commands run" table is filled
in after the run, from actual output, and is the single place this slice's numbers live.

---

## Acceptance criteria

### A. The giveaway half — entry state, and no entry path at all

| ID | Criterion |
|---|---|
| G17.1 | An owner or admin can open a giveaway with a creator-supplied entry-window close instant, and it is recorded |
| G17.2 | A non-owner/admin cannot open one — `42501`, nothing inserted |
| G17.3 | A second open giveaway on the same channel is refused (`23505`), never a silent supersede; the partial unique index is the hard guarantee |
| G17.4 | A close instant at or before the open instant is refused (`22023`) — a window that closes before it opens is not a window |
| G17.5 | An owner or admin can report the entry count on the open giveaway; a negative count is refused (`22023`) |
| G17.6 | A non-owner/admin cannot report it — `P0002`, indistinguishable from not-found |
| G17.7 | Closing is owner/admin, addressed by giveaway id, and one indistinguishable `P0002` for unknown, already-closed, other-channel or unauthorised |
| G17.8 | The closed giveaway's row is **not deleted** — the durable record survives (§12.6) |

### B. The tournament half — built ON `0140`'s lobby, never beside it

| ID | Criterion |
|---|---|
| G17.9 | `public.tournaments` carries a `not null` foreign key to `public.lobby_sessions(id)` (§17.2: "built on the Lobby Engine rather than beside it") |
| G17.10 | **`tournaments` carries no seat, queue, confirmed-seat, field-size, capacity or participant column at all** — the bracket's field size IS the referenced lobby's `seat_count`, asserted against `information_schema.columns` |
| G17.11 | An owner or admin can start a tournament on an OPEN lobby of their own channel whose `seat_count` is 2, 4 or 8 |
| G17.12 | A lobby whose `seat_count` is not 2, 4 or 8 is refused (`22023`) — single elimination without byes needs a power of two, and §30.3 caps the field at 8 |
| G17.13 | A lobby belonging to another channel, or an already-closed lobby, is refused (`P0002`) |
| G17.14 | A non-owner/admin cannot start one — `42501` |
| G17.15 | A second running tournament on the same channel is refused (`23505`) |
| G17.16 | Progress can be reported: `current_round` within `1 .. log2(seat_count)`, and `completed_matches_in_round` within `0 .. seat_count >> current_round` — both derived from the referenced lobby, both refused (`22023`) outside those bounds |
| G17.17 | Concluding is owner/admin, addressed by tournament id, one indistinguishable `P0002`, and deletes nothing |

### C. No chance mechanic, no prize custody, no paid entry — asserted structurally

| ID | Criterion |
|---|---|
| G17.18 | **No shipped `app_private` function of `0142` contains a randomness or chance-selection primitive** — `random(`, `setseed`, `tablesample`, `shuffle`, `lottery`, `raffle`, `random_bytes`, `weight`, `odds`. `gen_random_uuid()` is permitted and is the only `random`-containing token in the file. This is the structural guard the no-chance property rests on |
| G17.19 | **No table created by `0142` carries a draw, seed, winner, odds, weight, chance or override column**, asserted against `information_schema.columns` |
| G17.20 | **No table created by `0142` carries a prize, escrow, custody, shipping, delivery, fulfilment, address or claim column**, asserted against `information_schema.columns`. BharatStudio never holds, escrows, ships or guarantees a prize (§17.1) |
| G17.21 | No price, amount, currency, paise, plan, subscription, billing or payment token appears in any function `0142` ships — a paid-only entry is impossible because no entry path exists at all |
| G17.22 | `0142` does not mention the Events Pack grant key, so `0140`'s own "nothing can grant the pack" assertion stays true after this migration lands |

### D. The overlay read — aggregates only, enforced on the declared result type

| ID | Criterion |
|---|---|
| G17.23 | **The returned column set is exactly `{entry_count, entry_closes_at, tournament_current_round, tournament_total_rounds, tournament_completed_matches_in_round, tournament_matches_in_round}`** — asserted twice: from `pg_get_function_result`, and from a table materialised out of a live call and read back through `information_schema.columns`. Adding ANY column turns this file red by name. **This is the privacy property the first negative test breaks and restores** |
| G17.24 | The read contains no participant, player, in-game, Discord, viewer, anonymous, winner, initials, avatar, supporter, address or contact token at all |
| G17.25 | A valid overlay session on an entitled channel with an open giveaway and a running tournament returns exactly one row; the tournament columns derive `total_rounds` and `matches_in_round` from the referenced lobby's `seat_count` |
| G17.26 | A giveaway with no tournament returns one row with the four tournament columns null, and vice versa |
| G17.27 | A bad, foreign, expired or revoked overlay token returns **zero rows** |
| G17.28 | A channel **without** the entitlement returns zero rows even with a perfectly valid token — the tier gate is on the module, via `0140`'s `app_private.events_pack_entitled`, reused and not reimplemented |
| G17.29 | A closed giveaway and a concluded tournament both return zero rows — current state, never a history (§12.7). **There is no terminal or winner state to render** |
| G17.30 | The creator's own reads (`list_channel_giveaway`, `list_channel_tournament`) and every write path call **no** tier function (§12.6), and leak nothing to a non-member |
| G17.31 | `0142` is additive: `giveaway_tournament_card` was already one of `0131`'s twenty catalogue keys and that check constraint is not altered |

### E. API, contracts and canvas

| ID | Criterion |
|---|---|
| G17.32 | Creator routes are session-authenticated, 404 (never 403) for a non-member, 503 when the store is absent — never a 200 asserting "nothing is running" when nothing has checked |
| G17.33 | The overlay route returns 200 with nulls for an unrecognised token, 401 only for a MISSING bearer token, and narrows a second, independent time in front of the store |
| G17.34 | `contracts/validate-fixtures.mjs` refuses every prohibited field on both the overlay and creator response schemas: winner, drawnAt, seed, odds, weight, prize, prizeValue, escrow, shippingAddress, claimUrl, entryFeePaise, participants, playerName, discordName, viewerId |
| G17.35 | The canvas module is registered on the ONE existing connection and the ONE existing rAF loop — no second session, no second transport, no timer of its own — and `node .github/scripts/canvas-static-check.mjs` passes |
| G17.36 | `render()` writes only `transform` and `opacity` (PRF-03); the DOM is bounded and created once (§19.5) |

---

## The two required negative tests

Each is applied, its failure observed, and the file restored **byte-identical** (verified by
`git diff --stat` returning empty for that path).

| # | Property | Mutation | Expected |
|---|---|---|---|
| 1 | **Privacy** — the overlay read returns aggregate state only | Added `entrant_user_id uuid` to `app_private.list_overlay_giveaway_tournament`'s `returns table (...)` and `giveaway.created_by_user_id` to its select list | FAILED, by name, on the DECLARED RESULT TYPE — before any data is read |
| 2 | **No chance mechanic** | Added `if random() < 0.5 then new_id := gen_random_uuid(); end if;` to `app_private.open_giveaway` | FAILED, by name, on G17.18's structural randomness assertion |

**Negative test 1 — the four outputs.**

1. Mutation applied to `packages/db/migrations/0142_v1_prf02_giveaway_tournament.sql`.
2. Test result: `RESULT: prf02_slice6_giveaway_tournament FAILED (exit 3)`
3. The failure, verbatim:

```
ERROR:  the overlay giveaway/tournament read must return aggregate state and nothing else (§17: entry count, time remaining, bracket state -- never a participant identifier, an in-game name, a Discord name, a viewer id, an anonymous identity, a session id, an address or a contact detail). Declared result is "TABLE(entry_count integer, entry_closes_at timestamp with time zone, tournament_current_round integer, tournament_total_rounds integer, tournament_completed_matches_in_round integer, tournament_matches_in_round integer, entrant_user_id uuid)"
```

4. Restored byte-identical: `sha256 a07191ab6adcb40883a8977858c2731be65a02548628156ff7e1d3658359e750`, the
   pre-mutation hash.

**Negative test 2 — the four outputs.**

1. Mutation applied to the same file.
2. Test result: `RESULT: prf02_slice6_giveaway_tournament FAILED (exit 3)`
3. The failure, verbatim:

```
ERROR:  app_private.open_giveaway contains a "random(" token -- NO chance-based mechanic of any kind may ship (FULL-PRODUCT-DEFINITION.md §17.1, decided 2026-09-13; GIV-07 is Blocked)
```

4. Restored byte-identical: `sha256 a07191ab6adcb40883a8977858c2731be65a02548628156ff7e1d3658359e750`.

**G17.18's assertion was WRITTEN for this slice**, because no existing test caught a randomness
primitive. It scans every shipped `app_private` function definition from `pg_get_functiondef` for
`random(`, `random_bytes`, `setseed`, `tablesample`, `shuffle`, `lottery`, `raffle`, `sortition`,
`odds`, `weighted` and `weight`, and fails by function name. `gen_random_uuid()` is permitted and
is not matched — the banned token is `random(` and the permitted call spells `random_uuid(` — and a
second assertion checks that `open_giveaway` really does mint its id with it, so the exemption
guards something that exists rather than being a loophole.

---

## Commands run

Filled in from actual output after the run.

| Command | Exact result line |
|---|---|
| `pnpm db:test:all` | `SQL SUITE: pass=67 fail=0` (was 66 before this slice; `PASS prf02_slice6_giveaway_tournament`) |
| `pnpm --filter @bharatstudio/alerts-api test` | `ℹ tests 687` · `ℹ pass 687` · `ℹ fail 0` (was 668) |
| `pnpm --filter @bharatstudio/alerts-web test` | `ℹ tests 560` · `ℹ pass 560` · `ℹ fail 0` (was 537) |
| `pnpm --filter @bharatstudio/alerts-api build` | `tsc -p tsconfig.json` — exit 0, no diagnostics |
| `pnpm contracts:validate` | `Validated 50 fixtures plus the v1 template catalogue contract with Draft 2020-12, format enforcement and v1 capability exclusion (including invalid-UUID rejection).` · `Validated OpenAPI 3.1 document with 88 paths, 100 operation contracts, and all local $ref targets.` · `Validated 3 negative OpenAPI operation-contract cases.` |
| `pnpm explain:check` | `OK: every app_private call found by rule 1 (convention scan), rule 2 (overlay-store-file scan) and rule 3 (composition-root derived-read scan, 14 wired declaration(s) resolved and scanned) is present in required-queries.json (21 manifest entries, 9 exemptions)` · `OK: 21/21 plans current` |
| `pnpm harness:check` | `API test harness check: all checks passed against current code.` |
| `node .github/scripts/canvas-static-check.mjs` | `PRF-03/PRF-04 canvas static check: all checks passed against current code.` |

**Before the manifest entry was added, `pnpm explain:check` failed by name**, which is the
evidence that RT-12's scan actually covers this slice rather than happening to pass:

```
RT-12 required-queries scan: 1 overlay-facing app_private call(s) missing from packages/db/explain-plans/required-queries.json:
  - app_private.list_overlay_giveaway_tournament called at apps/api/src/db/giveaway-tournament-overlay-store.ts:99 has no manifest entry (rule1-convention)
```

---

## What this record is not

**Local verification only.** Nothing here is production, provider, store, legal, device, network or
release readiness. `RT-07` remains `Blocked`. The EXPLAIN artefact is a plan-shape change detector
captured against a minimally-seeded local database and is **not** §37.4 production-scale evidence.
**`GIV-07` stays `Blocked` and nothing in this slice may be described as closing it.**
