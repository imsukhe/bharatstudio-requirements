# PRF-02 slice 6 — Giveaway / Tournament Card (§6 catalogue module #17) and the minimum §17 schema

**Status:** `Conditionally complete — implemented and locally verified; independent review unavailable; no register state letter assigned`
**Owner:** **Sukhdev Singh**
**Classification:** L3 (new database objects, new creator write paths, a new overlay read path, a legal-adjacent boundary)
**Authority:** `../../FULL-PRODUCT-DEFINITION.md` §6 module #17, §9.1.1, §12.6, §12.7, §16, §17 (in full — §17.1 and §17.2), §30.3, §34, `GIV-07`
**Binding owner decisions:** `../../reviews/2026-09-16-prf-02-slice-6-owner-decisions.md` decisions **4** and **5**
**Predecessor this builds ON TOP OF:** `PRF-02-slice-6-lobby-status.md` and `packages/db/migrations/0140_v1_prf02_lobby_status.sql` — §17.2 says tournaments are "built on the Lobby Engine rather than beside it", so module #17 depends on module #16 and could not be built in parallel with it
**Acceptance record:** `../../tests/TC-PRF-02-slice-6-giveaway-tournament.md`
**Decision record:** `../../reviews/2026-09-17-prf-02-slice-6-giveaway-tournament-decisions.md`
**Parent task:** `PRF-02.md`. Recorded in its own file, with `giveaway` in every record name, because
slice 6 runs concurrent agents and a single appended section is what collided in slice 5.

**No register state letter is assigned by this task.** `PRF-02`'s, the `GIV-*` and the `TRN-*` rows'
letters are decided after audit, by the owner, never by an implementer. **`GIV-07` stays `Blocked`
and nothing in this slice closes, narrows or touches it.**

---

## What is being built

A complete vertical slice of §6 catalogue module #17, **Giveaway / Tournament Card**, plus the
**minimum §17 schema** needed to render it. Nothing else from §17, and nothing else from Phase 3.

| Layer | Object |
|---|---|
| Schema | `packages/db/migrations/0142_v1_prf02_giveaway_tournament.sql` — **migration number assigned to this task**; `0141` is held concurrently by another agent, is never written here, and nothing is renumbered |
| Entitlement | `app_private.events_pack_entitled(uuid)` — **reused unchanged from `0140`**, called and never reimplemented |
| Creator writes | `app_private.open_giveaway`, `update_giveaway_entry_count`, `close_giveaway`, `start_tournament`, `set_tournament_progress`, `conclude_tournament` — all owner/admin, none tier-gated |
| Creator reads | `app_private.list_channel_giveaway(uuid)`, `app_private.list_channel_tournament(uuid)` — any channel member, never tier-gated |
| Overlay read | `app_private.list_overlay_giveaway_tournament(uuid, text)` — six aggregate columns, entitlement-gated |
| API | `GET/POST /v1/channels/:channelId/giveaway`, `PATCH .../giveaway/:giveawayId`, `POST .../giveaway/:giveawayId/close`, `GET/POST /v1/channels/:channelId/tournament`, `PATCH .../tournament/:tournamentId`, `POST .../tournament/:tournamentId/conclude`, and `GET /v1/overlay-widgets/:overlayId/giveaway-tournament` |
| Contracts | OpenAPI paths and components, three JSON-Schemas, three fixtures, negative privacy / no-chance / no-prize-custody cases in `contracts/validate-fixtures.mjs` |
| RT-12 | `packages/db/explain-plans/giveaway-tournament.explain.md` and a `required-queries.json` entry |
| Canvas | `modules/giveaway-tournament-logic.ts` and `modules/giveaway-tournament-module.ts`, on the ONE existing connection and the ONE existing rAF loop |
| Tests | SQL, API route, pure-logic, renderer and canvas-integration layers |

---

## The prohibitions this slice is bound by

Quoted as constraints. None was decided by this implementer, none is extended, none is relitigated.

1. **No chance-based draw mechanic of any kind.** No random selection, no seeded draw, no shuffle,
   no weighted odds, no `random()`, no lottery. §17.1 decided this on **2026-09-13** — before and
   independently of `GIV-07` — restricting giveaways to "free-entry and skill-based formats only"
   and stating that supporter-weighted odds are not built. `GIV-07` additionally gates chance-based
   formats on a legal review that has not happened.
2. **No creator-records-the-winner surface**, which owner decision 4 names explicitly as an
   invented product surface nobody decided.
3. **BharatStudio never holds, escrows, ships or guarantees a prize** (§17.1). No prize custody, no
   escrow, no fulfilment state, no delivery language anywhere in schema, contract, copy or renderer.
4. **Never a paid-only entry**, and no random-chance mechanic gated behind payment (§17.1).
5. **Winner announcement requires consent** (§17.1), and a claim flow must never expose an address
   on stream. No consent mechanism exists in this schema and building one is out of scope.
6. **Entitlement is `tier in ('creator','studio')` OR an Events Pack grant nothing can set**
   (decision 5) — the existing `0140` function, called rather than rewritten.
7. **The tier gate is on the MODULE only** (§12.6). Storing, viewing, searching, fetching and
   exporting a durable creator record is never tier-gated.

---

## Where the line against the full §17 subsystem was drawn

The same rule slice 6's Lobby Status record applied: **if the card can render without it, it is out
of scope.** Applied to every §17 feature:

| §17 feature | In / out | Why |
|---|:-:|---|
| Entry count | **in** | §17.1's overlay list names it first |
| Entry window / time remaining | **in** | §17.1's overlay list names it; the instant is creator-supplied, not invented |
| Bracket progress (round, matches complete) | **in** | §17.2's "standings overlay module" (`TRN-05`), in the only form that needs no participant label |
| Draw, seed, entrant-count-for-a-draw, override log | out | §17.1's 2026-09-13 decision and `GIV-07`. `GIV-03` and `GIV-04` are not built |
| Winner, winner announcement, claim flow | out | Requires consent (§17.1) and a participant identity; neither exists. See the decision record |
| Prize description, prize state, delivery | out | Not rendered by the card, and any stored prize state is a step toward the custody language §17.1 forbids |
| Entry method (`GIV-01`), follow/subscribe check, supporter status | out | There is no entry path at all in this slice; a stored method with nothing enforcing it is decoration |
| Bracket tree with named slots | out | Inherently needs participant labels. **Reported as a tension, not solved by inventing a display-name concept** |
| Seeding (`TRN-02`), check-in windows and reminders (`TRN-03`) | out | Seeding by "published-seed random" is a chance mechanic; check-in is the Lobby Engine's ready check, which `0140` deliberately did not build |
| Score reporting with a dispute note (`TRN-04`) | out | A dispute note is free text on a match row; matches do not exist as rows here |
| Sponsor slot with an exposure log (`TRN-06`) | out | Slice 5's scope review left #11 blocked precisely because "what counts as an exposure" is undecided and legal-adjacent |
| Double elimination, round robin, points table | out | §30.3 and `TRN-01b` place all three at **Studio**; this slice's entitlement is Creator+ and does not carry a second, finer tier gate |

---

## Verification

Every command and its exact result line is recorded in the acceptance record
`../../tests/TC-PRF-02-slice-6-giveaway-tournament.md`, together with the two required negative
tests (the privacy property and the no-chance property) and the byte-identical restoration of each.

**Local verification only.** Nothing here is production, provider, store, legal, device, network or
release readiness. `RT-07` remains `Blocked`; the EXPLAIN artefact is a plan-shape change detector
captured against a minimally-seeded local database and is **not** §37.4 production-scale evidence.

---

## Referred to the owner

- **The `Tournament standings` row of §30.3 says `— | — | — | yes` (Studio only)**, while owner
  decision 5 makes the §16/§17 entitlement `tier in ('creator','studio')` or a pack grant. This
  slice implements decision 5 (the later and explicit instruction) and ships only the
  single-elimination-up-to-8 form that §30.3's own `Tournaments — single elim, up to 8` row places
  at **Creator+**, so the two rows agree for what actually ships. Whether a Creator-tier channel may
  render tournament *standings* in a richer form is the owner's to settle, not an implementer's.
- **The card cannot show a winner in this slice, and the decision record says why.** If the product
  wants one, someone has to author the consent mechanism §17.1 requires. That is a product decision.
- **The entry count and the bracket progress are as accurate as whoever reports them** — the creator,
  because no entry path and no match record exists. This is the identical cost `0140` recorded for
  its seat and queue counts, and it is referred rather than patched with an invented derivation.
