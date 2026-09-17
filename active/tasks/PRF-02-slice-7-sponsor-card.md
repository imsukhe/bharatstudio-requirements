# PRF-02 slice 7 — Sponsor Card (§6 catalogue module #11)

**Status:** `Conditionally complete — implemented and locally verified; independent review unavailable; no register state letter assigned`
**Owner:** **Sukhdev Singh**
**Classification:** L3 (new database objects, a new creator write path, a new overlay read path, a legal-adjacent boundary the owner just closed)
**Authority:** `../../FULL-PRODUCT-DEFINITION.md` §6 module #11, §9.1.1, §12.6, §12.7, §19.1, §30.3, §34
**Binding owner decision:** `../../reviews/2026-09-17-remaining-eight-modules-and-youtube-v1-amendment.md` Part 1 §3
**Acceptance record:** `../../tests/TC-PRF-02-slice-7-sponsor-card.md`
**Decision record:** `../../reviews/2026-09-17-prf-02-slice-7-sponsor-card-implementation.md`
**Parent task:** `PRF-02.md`. Recorded in its own file, with `sponsor-card` in every record name, per
the slice-5/slice-6 convention for concurrent-agent slices — three other agents are building
migrations `0143`, `0144` and `0146` at the same time.

**No register state letter is assigned by this task.** States are decided after audit, by the
owner, never by an implementer.

---

## What is being built

A complete vertical slice of §6 catalogue module #11, **Sponsor Card**. The card renders the
sponsor and counts nothing.

| Layer | Object |
|---|---|
| Schema | `packages/db/migrations/0145_v1_prf02_sponsor_card.sql` — **migration number assigned to this task**; `0143`, `0144` and `0146` are held concurrently by other agents, never written here, nothing is renumbered |
| Creator writes | `app_private.upsert_sponsor_card` — owner/admin only, not tier-gated |
| Creator reads | `app_private.list_channel_sponsor_card(uuid)` — any channel member, never tier-gated |
| Overlay read | `app_private.list_overlay_sponsor_card(uuid, text)` — three fields, schedule- and enabled-gated |
| API | `GET/PUT /v1/channels/:channelId/sponsor-card` and `GET /v1/overlay-widgets/:overlayId/sponsor-card` |
| Contracts | OpenAPI paths and components, two JSON Schemas, two fixtures, negative no-counter/no-third-party cases in `contracts/validate-fixtures.mjs` |
| RT-12 | `packages/db/explain-plans/sponsor-card.explain.md` and a `required-queries.json` entry |
| Canvas | `modules/sponsor-card-logic.ts` and `modules/sponsor-card-module.ts`, on the ONE existing connection and the ONE existing rAF loop |
| Tests | SQL (including a structural no-counter proof), API route, pure-logic and renderer layers |

---

## The prohibitions this slice is bound by

Quoted as constraints from the 2026-09-17 decision. None was decided by this implementer, none is
extended, none is relitigated.

1. **The card renders the sponsor and counts nothing.** Nothing is counted, nothing is stored about
   display, and no number about display is ever shown to anyone.
2. **The exposure event log named in §6's original row is DROPPED.** That phrase is superseded.
3. **Not even an internal-only, not-billable counter.** Considered and declined: any number
   rendered will eventually be screenshotted into a sponsorship negotiation, and a label saying it
   is not auditable protects nobody.
4. **Not authorised at all:** exposure log, impression metric, duration accounting, display counter
   of any kind, sponsor-facing reporting. Building one later is a new decision requiring legal
   review, not an extension of this one.
5. **No column, API field, event, log line or UI element may count, time or accumulate anything**
   about the card being displayed — not even "last shown at".
6. **"Scheduled placement" survives.** A schedule is an instruction about the future ("show this
   sponsor between two instants"), never a record of the past ("it was shown").
7. **§9.1.1**: no third-party code, URL, iframe, script or stylesheet may reach the Master Canvas;
   the module definition has no field capable of carrying one. A sponsor logo is an asset (§19.1:
   GCS/CDN for bytes, Postgres holds metadata only), never a remote URL the canvas fetches from a
   third party.

---

## Where the line was drawn, and the one blocker this slice reports rather than works around

| Sponsor Card element | In / out | Why |
|---|:-:|---|
| Sponsor name | **in** | The whole point of the card |
| Enable/disable toggle | **in** | Owner decision: "one show/hide toggle", matching module #10's shape |
| Scheduled placement window (absolute start/end instants) | **in** | Explicitly authorised — "an instruction about the future" |
| Sponsor logo, as content-addressed asset METADATA (`channel_id` + sha256, mime type, byte size) | **in, schema-complete** | §19.1's target design row shape, reused verbatim as a formula, not a new invented format |
| Actual logo BYTES stored in / served from GCS+CDN | **BLOCKED — reported, not built** | No GCS/CDN client, bucket, credential or signed-URL code exists anywhere in this repository (grep proof in the decision record). Building one is standing up new infra, which is out of this slice's ownership boundary — the identical judgement call `apps/api/src/domain/asset-scan-pipeline.ts` already makes in this codebase for malware scanning. The metadata columns and validation ship now; wiring them to real bytes needs that infra decision first |
| Exposure log, impression count, duration accounting, sponsor-facing report | **out, never** | The whole point of the 2026-09-17 decision |
| Recurring daily local-time schedule ("every day 7–9pm") | **out** | Needs a creator-timezone concept; none is decided anywhere in this repository (grepped). Ships as an absolute UTC `timestamptz` window instead, which needs no timezone concept |
| A second, module-specific tier gate | **out** | `sponsor_card` is already one of migration `0131`'s twenty catalogue keys; the §30.3 module-count cap already governs rendering. No tier row for this module exists anywhere in §30.3's placement table, so none is invented here |

---

## Verification run and reported by this implementer

SQL suite, `pnpm --filter @bharatstudio/api test`, `pnpm --filter @bharatstudio/web test`, the
TypeScript compiler (typecheck, separate from the test runner), and `pnpm harness:check`. Exact
counts are in the decision record, not restated here.
