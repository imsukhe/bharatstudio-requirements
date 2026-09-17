# PRF-02 slice 7 — QR Smart Card (§6 catalogue module #10)

**Status:** `Conditionally complete — implemented and locally verified; independent review unavailable; no register state letter assigned`
**Owner:** **Sukhdev Singh**
**Classification:** L3 (a new database object, a new creator write path, a new overlay read path, a first-party encoder written from scratch to satisfy §9.1.1)
**Authority:** `../../FULL-PRODUCT-DEFINITION.md` §6 module #10, §9.1.1, §12.6, §12.7, §19.5, §30.3
**Binding owner decision:** `../../reviews/2026-09-17-remaining-eight-modules-and-youtube-v1-amendment.md` Part 1 §2
**Acceptance record:** `../../tests/TC-PRF-02-slice-7-qr-smart-card.md`
**Decision record:** `../../reviews/2026-09-17-prf-02-slice-7-qr-smart-card-implementation.md`
**Parent task:** `PRF-02.md`. Recorded in its own file, with `qr-smart-card` in every record name, per
the slice-5/slice-6 convention for concurrent-agent slices — three other agents are building
migrations `0143`, `0145` and `0146` at the same time.

**No register state letter is assigned by this task.** States are decided after audit, by the
owner, never by an implementer.

---

## What is being built

A complete vertical slice of §6 catalogue module #10, **QR Smart Card**. This closes the slice-5
scope review's `BLOCKED-DECISION` classification: module #10 had been blocked on `CMP-17` (Clutch
Mode) and a scene-profile system, neither of which exists in this repository, and the 2026-09-17
decision is that neither is needed for a card with exactly one state and one destination.

| Layer | Object |
|---|---|
| Schema | `packages/db/migrations/0144_v1_prf02_slice7_qr_smart_card.sql` — **migration number assigned to this task**; `0143`, `0145` and `0146` are held concurrently by other agents, never written here, nothing is renumbered |
| Creator writes | `app_private.upsert_qr_smart_card` (destination/label) and `app_private.set_qr_smart_card_enabled` (the single toggle) — owner/admin only, not tier-gated, two independent writes for two independent decisions |
| Creator reads | `app_private.list_channel_qr_smart_card(uuid)` — any channel member, never tier-gated |
| Overlay read | `app_private.list_overlay_qr_smart_card(uuid, text)` — two fields, gated by the card's own `is_enabled` (the toggle IS the read) |
| API | `GET/PUT /v1/channels/:channelId/qr-smart-card`, `PUT /v1/channels/:channelId/qr-smart-card/enabled`, and the overlay read wired into `apps/api/src/routes/master-canvas.ts` alongside every other module's overlay endpoint |
| Contracts | OpenAPI paths and components, two JSON Schemas, two fixtures |
| RT-12 | `packages/db/explain-plans/qr-smart-card.explain.md` and a `required-queries.json` entry, captured against a real seeded Postgres 16 database |
| Canvas | `modules/qr-smart-card-logic.ts` (pure helpers **and** the first-party QR encoder) and `modules/qr-smart-card-module.ts` (the renderer), on the ONE existing connection and the ONE existing rAF loop |
| Tests | SQL (including two structural no-scene/no-counter proofs), API route, pure-logic (encoder) and renderer layers |

---

## The prohibitions this slice is bound by

Quoted as constraints from the 2026-09-17 decision. None was decided by this implementer, none is
extended, none is relitigated.

1. **The creator sets one destination and one label. The card shows or hides on a single toggle.
   That is the entire feature.**
2. **No scene profiles and no `CMP-17` Clutch Mode dependency.** Neither exists in this repository.
   Neither is built, neither is stubbed, and no column anticipates either.
3. **Forward-compatible on purpose:** a single-destination card later gains scene awareness by
   being *selected by* a scene profile, so the module holds no scene concept at all — nothing a
   future `CMP-17` could conflict with.
4. **Not authorised:** a destination allow-list, link shortening, scan counting, and any claim
   about how many people scanned anything. No scan, view, impression or exposure counter anywhere
   — not in schema, not in the API, not in the UI.
5. **§9.1.1**: no third-party code, URL, iframe, script or stylesheet may reach the Master Canvas.
   The creator's destination IS a URL, and the resolution is that it is data rendered as a QR code
   image, never something the canvas fetches, navigates to or embeds.
6. **Generate the QR code first-party.** No third-party QR library, no remote QR-image service — a
   remote image URL on the canvas would itself violate §9.1.1.

---

## Where the line was drawn

| QR Smart Card element | In / out | Why |
|---|:-:|---|
| Destination (1–120 chars) | **in** | The whole point of the card |
| Label (1–120 chars) | **in** | Owner decision: "one destination and one label" |
| Enable/disable toggle | **in** | Owner decision: "shows or hides on a single toggle" — a card-specific state, separate from the generic §30.3 module-activation cap every module already has |
| First-party QR encoder (byte mode, EC level M, versions 1–10) | **in, built from scratch** | No first-party encoder existed in this repository; a third-party library or remote image service would violate §9.1.1 |
| Destination allow-list / validation beyond length | **out** | Not authorised. The destination is bounded text, reusing the same 1–120 bound every other short creator-authored field in this schema already uses — no URL-format check is invented |
| Link shortening | **out** | Not authorised |
| Scan/view/impression/exposure counter | **out, never** | Explicitly not authorised — "no claim about how many people scanned anything" |
| Scene profile / `CMP-17` dependency | **out, structurally impossible** | Neither exists; no column, no field, no concept |
| A second, module-specific tier gate | **out** | `qr_smart_card` is already one of migration `0131`'s twenty catalogue keys; the §30.3 module-count cap already governs rendering |

**No blocker.** Unlike Sponsor Card (module #11, blocked on missing GCS/CDN infrastructure for a
logo asset), this slice needed no infrastructure this repository does not already have: the QR
encoder is pure arithmetic (Reed-Solomon over GF(256), BCH format/version info, standard mask
penalty scoring) and needed nothing beyond what TypeScript already provides.

---

## Verification run and reported by this implementer

Full SQL suite, `pnpm --filter @bharatstudio/alerts-api test`, `pnpm --filter @bharatstudio/alerts-web test`,
the TypeScript compiler for both packages (typecheck, separate from the test runner), `pnpm harness:check`,
and the contracts/explain-plan checks. Exact counts are in the decision record, not restated here.

**One verification step beyond what any prior slice needed:** because this slice ships a
from-scratch QR encoder, every version it supports (1 through 10), the boundary lengths between
them, a single-character destination, a 120-character destination, and a destination containing
multi-byte UTF-8 text were round-tripped through `zbar` — a real, independent, spec-compliant QR
decoder (`zbarimg`, installed via Homebrew for this verification only, not a project dependency) —
during development, and each decoded back to the exact original string. This caught two real bugs
(format-info and version-info bit-order mistakes that produced plausible-looking but
non-decodable matrices) that a self-consistency check alone would not have found. See the decision
record for the full account.
