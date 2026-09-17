# PRF-02 slice 6 — Lobby Status (§6 catalogue module #16) and the minimum §16 Lobby schema

**Status:** `Conditionally complete — implemented and locally verified; independent review unavailable; no register state letter assigned`
**Owner:** **Sukhdev Singh**
**Classification:** L3 (new database objects, a new entitlement check, new creator write paths, a new overlay read path)
**Authority:** `../../FULL-PRODUCT-DEFINITION.md` §6 module #16, §9.1.1, §12.6, §12.7, §16 (in full), §30.3, §33, §34
**Binding owner decisions:** `../../reviews/2026-09-16-prf-02-slice-6-owner-decisions.md` decisions **4** and **5**
**Predecessor scope review:** `../../reviews/2026-09-16-prf-02-slice-5-scope-review.md` (classified #16 `BLOCKED-DECISION`; decisions 4 and 5 are what unblocked it)
**Acceptance record:** `../../tests/TC-PRF-02-slice-6-lobby-status.md`
**Decision record:** `../../reviews/2026-09-16-prf-02-slice-6-lobby-status-decisions.md`
**Parent task:** `PRF-02.md`. Recorded in its own file, with `lobby` in every record name, because
slice 6 runs concurrent agents and a single appended section is what collided in slice 5.

**No register state letter is assigned by this task.** `PRF-02`'s and the `LOB-*` rows' letters are
decided after audit, by the owner, never by an implementer.

---

## What is being built

A complete vertical slice of §6 catalogue module #16, **Lobby Status**, plus the **minimum §16
Lobby schema** needed to render it. Nothing else from §16, and nothing else from Phase 3.

| Layer | Object |
|---|---|
| Schema | `packages/db/migrations/0140_v1_prf02_lobby_status.sql` — **migration number assigned to this task**; no other number is used and nothing is renumbered |
| Entitlement | `app_private.events_pack_entitled(uuid)` — `tier in ('creator','studio')` **or** an active Events Pack grant, built with **no grant path** |
| Creator writes | `app_private.open_lobby_session`, `app_private.update_lobby_session_counts`, `app_private.close_lobby_session` — all owner/admin, none tier-gated |
| Creator read | `app_private.list_channel_lobby_session(uuid)` — any channel member, never tier-gated |
| Overlay read | `app_private.list_overlay_lobby_status(uuid, text)` — three integers, entitlement-gated |
| API | `GET/POST /v1/channels/:channelId/lobby-session`, `PATCH .../lobby-session/:lobbyId`, `POST .../lobby-session/:lobbyId/close`, and `GET /v1/overlay-widgets/:overlayId/lobby-status` |
| Contracts | OpenAPI paths and components, two JSON-Schemas, two fixtures, negative privacy cases in `contracts/validate-fixtures.mjs` |
| RT-12 | `packages/db/explain-plans/lobby-status.explain.md` and a `required-queries.json` entry |
| Canvas | `modules/lobby-status-logic.ts` and `modules/lobby-status-module.ts`, on the ONE existing connection and the ONE existing rAF loop |
| Tests | SQL, API route, pure-logic, renderer and canvas-integration layers |

---

## The owner decisions this slice is bound by

Quoted as constraints. None was decided by this implementer, none is extended, none is relitigated.

1. **PRF-02 may build the minimum §16 Lobby schema needed to render this card.** This is an
   override of §34's Phase 3 placement **for module #16 only** and authorises nothing else from
   Phase 3 (decision 4).
2. **Aggregates only.** §16 itself: the public overlay shows "aggregate status only". No
   per-viewer row on the overlay path, and nothing that correlates one visit to another
   (decision 4).
3. **Entitlement is `tier in ('creator','studio')` OR an active Events Pack grant, built with no
   grant path**, so present behaviour is exactly "included at Creator+" (decision 5).
4. **No price, no billing, no purchase path.** §33's ₹129/mo stays in the authority; this work
   charges nothing (decision 5).
5. **Opted-in initials and avatars are out of scope** — §16 permits them, but they need an opt-in
   mechanism that does not exist in this schema (decision 5's closing paragraph).

---

## Where the line against the full Lobby Engine was drawn

The rule applied, stated once and applied everywhere: **if the card can render without it, it is
out of scope.** §16.1's flow has eight steps; the card renders from three numbers produced by
step 1 and by the outcome of steps 3–4. Everything that exists to make those numbers *fair*
rather than *true* is the Lobby Engine, and is Phase 3.

| §16 feature | In this slice? | Why |
|---|---|---|
| Seats, confirmed seats, queue count | **Yes** | The card is literally "8/16 seats confirmed" plus a queue count (§16 L3002–3003) |
| Opening and closing a session | **Yes** | Without it the three numbers have no lifecycle and no channel scope |
| Ready check (§16.1 step 4) | No | The card renders from `confirmed_seat_count`; how a seat became confirmed is not on the wire |
| Single-use short-lived seat tokens (step 5) | No | Never rendered, and §16 forbids the token reaching the overlay at all |
| Room-code reveal (step 6) | No | §16: "Never … codes or passwords." The schema has no column for one |
| No-show expiry and reserve promotion (step 7) | No | Changes how a number gets its value, never whether the card can paint it |
| Selection policy, locked-and-displayed, redacted audit log (§16.2) | No | A fairness subsystem with its own records; it is the whole of §16.2 |
| Feedback, report options, automatic deletion of temporary lobby data (step 8) | No | End-of-session behaviour; there is no temporary lobby data in this slice to delete |
| Game, region, mode, platform, time, reserve seats, queue policy (step 1) | No | Not painted by the card; queue policy is §16.2's subsystem |
| Opted-in initials and avatars | No | Owner decision 5 — the opt-in mechanism does not exist |
| Eligibility modes, priority, suspensions, templates, cross-creator lobbies (§16.2, §16.4, §16.6) | No | Phase 3 trust/community/collaboration layers |
| Screened Guest Queue (§16.5) | No | §16.6's "high-risk media" band |

---

## Failure behaviour, kill switch, rollback

- **Failure behaviour.** The overlay read answers `lobbyStatus: null` for an unrecognised,
  expired, revoked or foreign token, for a channel with no open lobby, and for a channel without
  the entitlement. The module renders the same nothing for all four; the API route returns a
  retryable 503 when its store is absent rather than a 200 that reads as "no lobby".
- **Per-module error boundary.** The Canvas runtime's existing PRF-14 boundary covers this module
  unchanged: two throws and it is marked `down`, the other ten keep rendering on the same loop.
- **Kill switch.** The module is inert unless the server returns `lobby_status` from
  `GET /v1/overlay-widgets/:overlayId/master-canvas/modules`. A creator turns it off there;
  `0131`'s module cap and the new entitlement both sit in front of it.
- **Rollback.** `0140` is additive — one table, two indexes, six functions, nothing existing
  altered. Undone by a NEW forward migration dropping them, never by editing `0140`. That drop
  does delete lobby rows; it is an operator rollback of the capability, not a downgrade. **No
  production migration without separate explicit approval.**

---

## Boundaries — what this slice did not touch

- No payment, billing, pricing, subscription or purchase surface of any kind.
- No change to `channel_entitlement_versions`, to any entitlement publisher, or to
  `tier_entitlement_dimensions`.
- No change to `0131`'s module catalogue check constraint — `lobby_status` was already one of its
  twenty keys.
- No second overlay session, no second transport, no second rAF loop.
- No third-party code, URL, iframe or stylesheet reaches the Canvas (§9.1.1).
- §17 (Giveaway / Tournament Card) is untouched. §17.2 makes it depend on §16, so it lands after
  this, never beside it.

---

## Referred to Opus / the owner

1. **Whether the Free tier may buy the Events Pack.** Deliberately undecided by the owner, and
   still unreachable: nothing can grant the pack.
2. **How an Events Pack grant is ever written.** Purchase is website-only per the standing
   constraint; the grant path, its shape and its lifecycle are unbuilt and undecided.
3. **Who reports the confirmed-seat and queue numbers in a real lobby.** In this slice the creator
   (or their tooling) does, because the mechanism that would derive them — the waitlist, the ready
   check and the reserve bench — is Phase 3. That is a product question, not a schema one.
4. **Whether `lobby_sessions` should carry §16.1 step 1's descriptors** (game, region, mode,
   platform, reserve seats) once the Lobby Engine proper is built, or whether they belong to a
   separate session-template record.

---

**Nothing in this record is production, provider, store, legal, device, network or release
readiness.** `RT-07` remains Blocked, `GIV-07`'s legal gate is untouched, and no external evidence
row is advanced by this work.
