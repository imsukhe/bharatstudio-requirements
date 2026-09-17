# TC-PRF-02 slice 6 — Lobby Status (§6 #16) and the minimum §16 Lobby schema: acceptance record

**Date:** 2026-09-16
**Owner:** **Sukhdev Singh**
**Task:** `../active/tasks/PRF-02-slice-6-lobby-status.md`
**Decisions:** `../reviews/2026-09-16-prf-02-slice-6-lobby-status-decisions.md`
**Binding owner decisions:** `../reviews/2026-09-16-prf-02-slice-6-owner-decisions.md` 4 and 5

Written **before** implementation, per `governance/AGENTS.md`. The "Commands run" table is filled
in after the run, from actual output, and is the single place this slice's numbers live.

---

## Acceptance criteria

### A. The minimum schema and the creator write paths (`packages/db/migrations/0140_v1_prf02_lobby_status.sql`)

| ID | Criterion |
|---|---|
| L16.1 | An owner or admin can open a lobby session with a seat count, and it is recorded |
| L16.2 | A non-owner/admin cannot open one — `42501`, nothing inserted |
| L16.3 | A second open session on the same channel is refused (`23505`), never a silent supersede; the partial unique index is the hard guarantee |
| L16.4 | A seat count below 1 is refused (`22023`), nothing inserted |
| L16.5 | An owner or admin can report confirmed seats and queue length on the open session |
| L16.6 | Confirmed seats above the seat count are refused (`22023`) — a lobby cannot confirm more seats than it has |
| L16.7 | A negative confirmed-seat or queue count is refused (`22023`) |
| L16.8 | A non-owner/admin cannot update the counts — `P0002`, indistinguishable from not-found |
| L16.9 | Closing is owner/admin, addressed by lobby id, and idempotent-safe: closing an unknown, already-closed, other-channel or unauthorised lobby is one `P0002` |
| L16.10 | After closing, a new session may be opened — the partial unique index constrains only OPEN sessions |
| L16.11 | The closed session's row is **not deleted** — the durable record survives (§12.6) |

### B. The entitlement — `tier in ('creator','studio')` OR an Events Pack grant with no grant path

| ID | Criterion |
|---|---|
| L16.12 | `app_private.events_pack_entitled` is **true** for `creator` and for `studio` |
| L16.13 | It is **false** for `free` and for `pro` — today's behaviour is exactly "included at Creator+" |
| L16.14 | The pack branch is present in the shipped function definition (asserted against `pg_get_functiondef`, not against a comment) — the mechanism exists |
| L16.15 | **Nothing can make the pack branch true.** No function in `app_private` other than the check itself mentions the grant key, and `app_private.tier_entitlement_dimensions` emits it for no tier — so no entitlement publisher, and no admin override, can write it |
| L16.16 | No price, amount, currency, paise, plan, subscription or billing token appears anywhere in `0140` |

### C. The overlay read — aggregates only, and the prohibitions enforced on the declared type

| ID | Criterion |
|---|---|
| L16.17 | A valid overlay session on an entitled channel with an open lobby returns exactly one row of three integers |
| L16.18 | **The returned column set is exactly `{seat_count, confirmed_seat_count, queue_count}`** — asserted twice: from `pg_get_function_result`, and from a table materialised out of a live call and read back through `information_schema.columns`. Adding ANY column turns this file red by name |
| L16.19 | A bad, foreign, expired or revoked overlay token returns **zero rows** — never another channel's lobby |
| L16.20 | A channel **without** the entitlement returns zero rows even with a perfectly valid token and an open lobby |
| L16.21 | A closed lobby returns zero rows; the read is current state, never a history (§12.7) |
| L16.22 | The shipped definition of the overlay read contains **no** room-code, password, seat-token, player, in-game-name, Discord, viewer, anonymous-identity or session-id token — asserted against `pg_get_functiondef` |
| L16.23 | `public.lobby_sessions` carries **no** per-viewer column of any kind — asserted against `information_schema.columns`, so there is nothing for a future read to start exposing and nothing that can correlate one visit to another |
| L16.24 | `0131`'s module catalogue check constraint is untouched and still names `lobby_status` |

### D. API routes

| ID | Criterion |
|---|---|
| L16.25 | `GET /v1/overlay-widgets/:overlayId/lobby-status` with no bearer token is 401; with a token and no store is a retryable 503 |
| L16.26 | A store answer is narrowed a SECOND time by `projectLobbyStatus` — an identifying field added by a rogue store never reaches the response body |
| L16.27 | A store answer that is internally inconsistent (confirmed above seats, negative, fractional) is dropped to `null` rather than rendered |
| L16.28 | The creator routes are session-authenticated, carry **no tier check in TypeScript**, and map a non-owner/admin to 404 rather than a leaking 403 |
| L16.29 | `additionalProperties: false` on both write bodies rejects a body carrying `roomCode`, `password`, `seatToken`, `playerName`, `discordName` or `viewerId` with a 400 before any store is called |

### E. Contracts

| ID | Criterion |
|---|---|
| L16.30 | The published overlay response schema **refuses** every one of: `roomCode`, `password`, `seatToken`, `playerId`, `playerName`, `inGameName`, `discordName`, `viewerId`, `anonymousIdentityId`, `sessionId`, `overlaySessionId`, `ipAddress`, `initials`, `avatarUrl`, `participants` |
| L16.31 | An empty (`null`) lobby status is a VALID answer — it is what a quiet channel, an unentitled channel and an unrecognised token all return |
| L16.32 | `confirmedSeatCount` above `seatCount` is refused by the contract, and `seatCount` below 1 is refused |
| L16.33 | `pnpm contracts:validate` passes with the new fixtures and paths |

### F. Canvas — one connection, one loop, composite-only

| ID | Criterion |
|---|---|
| L16.34 | With **eleven** modules registered and entitled there is still exactly ONE transport connection, ELEVEN subscribers on it, and ONE pending frame on the one rAF scheduler |
| L16.35 | PRF-02.10: an un-entitled `lobby_status` never subscribes, never fetches its snapshot and never builds its DOM |
| L16.36 | PRF-14: a Lobby Status module that throws twice goes `down` while its neighbours keep rendering on the same loop |
| L16.37 | The renderer paints "N/M seats confirmed" and the queue count, and paints **no** identifier of any kind; its guard rejects a payload carrying an unexpected key |
| L16.38 | `node .github/scripts/canvas-static-check.mjs` passes — `render()` writes only `transform` and `opacity` |

### G. RT-12

| ID | Criterion |
|---|---|
| L16.39 | `packages/db/explain-plans/lobby-status.explain.md` exists, with a `query_hash` matching `0140`'s current function body |
| L16.40 | `packages/db/explain-plans/required-queries.json` carries the entry, and `pnpm explain:check` passes |

---

## The negative test, run deliberately

**L16.18 is the criterion this slice exists to make un-bypassable**, so it is proven by breaking it
rather than by assertion:

1. Edit `0140` so `app_private.list_overlay_lobby_status` returns a player identifier alongside the
   three counts.
2. Run `pnpm db:test:all`. `prf02_slice6_lobby_status` must **FAIL**, by name, on the declared
   result type — not on data, and not on a downstream renderer check.
3. Restore `0140`. Re-run. It must pass.

Both outputs are recorded here, from the actual runs.

**Broken** -- `list_overlay_lobby_status` changed to
`returns table (seat_count integer, confirmed_seat_count integer, queue_count integer, created_by_player_id uuid)`
with `lobby.created_by_user_id` added to the select list:

```
  FAIL prf02_slice6_lobby_status
       ERROR:  the overlay lobby read must return aggregate counts and nothing else (§16: aggregate
       status only -- never player identifiers, never Discord names, never codes or passwords).
       Declared result is "TABLE(seat_count integer, confirmed_seat_count integer, queue_count
       integer, created_by_player_id uuid)", expected exactly "TABLE(seat_count integer,
       confirmed_seat_count integer, queue_count integer)"
SQL SUITE: pass=65 fail=1
failed: prf02_slice6_lobby_status
```

It failed on the **declared result type**, before any data was read -- which is exactly the
property being claimed. **Restored**, and re-run:

```
  PASS prf02_slice6_lobby_status
SQL SUITE: pass=66 fail=0
```

---

## Commands run

Run on this worktree, 2026-09-16. Exact result lines, not summaries.

| Command | Result |
|---|---|
| `pnpm db:test:all` | `SQL SUITE: pass=66 fail=0` (`PASS prf02_slice6_lobby_status`) |
| `pnpm --filter @bharatstudio/alerts-api test` | `tests 668 / pass 668 / fail 0` |
| `pnpm --filter @bharatstudio/alerts-web test` | `tests 537 / pass 537 / fail 0` |
| `pnpm --filter @bharatstudio/alerts-api build` | `tsc -p tsconfig.json` -- clean, no output |
| `pnpm contracts:validate` | `Validated 47 fixtures ...` - `Validated OpenAPI 3.1 document with 81 paths, 91 operation contracts, and all local $ref targets.` - `Validated 3 negative OpenAPI operation-contract cases.` |
| `pnpm explain:check` | `OK: every app_private call found by rule 1 ... rule 2 ... rule 3 ... is present in required-queries.json (20 manifest entries, 9 exemptions)` - `OK: 20/20 plans current` |
| `pnpm harness:check` | `API test harness check: all checks passed against current code.` |
| `node .github/scripts/canvas-static-check.mjs` | `PRF-03/PRF-04 canvas static check: all checks passed against current code.` |

Counts moved by this slice: fixtures 45 -> 47, OpenAPI paths 77 -> 81, operations 86 -> 91,
RT-12 manifest entries 19 -> 20, SQL suite files 65 -> 66.

---

## What this record is not

An acceptance record for §16, for the Lobby Engine, or for module #17. It covers module #16's card
and the minimum schema behind it, and nothing else. It is **not** production, provider, store,
legal, device, network or release readiness: the EXPLAIN artefact is a plan-shape change detector
captured against a minimally-seeded local database, `RT-07` remains Blocked, and no §37.4
production-scale evidence exists for any query in this slice.
