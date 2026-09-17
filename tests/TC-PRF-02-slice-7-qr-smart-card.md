# TC-PRF-02 slice 7 — QR Smart Card (§6 #10): acceptance record

**Date:** 2026-09-17
**Owner:** **Sukhdev Singh**
**Task:** `../active/tasks/PRF-02-slice-7-qr-smart-card.md`
**Decision:** `../reviews/2026-09-17-prf-02-slice-7-qr-smart-card-implementation.md`
**Binding owner decision:** `../reviews/2026-09-17-remaining-eight-modules-and-youtube-v1-amendment.md` Part 1 §2

Written **before** implementation, per `governance/AGENTS.md`. The "Commands run" table is filled
in after the run, from actual output, and is the single place this slice's numbers live.

---

## Acceptance criteria

### A. The schema and creator write path (`packages/db/migrations/0144_v1_prf02_slice7_qr_smart_card.sql`)

| ID | Criterion |
|---|---|
| QR10.1 | An owner or admin can set a destination and a label, upserting one row per channel (`channel_id` is the primary key) |
| QR10.2 | A non-owner/admin cannot write it — `42501`, nothing changed |
| QR10.3 | A destination or label outside 1–120 characters (empty, 121 chars, or null) is refused (`22023`) — the bound reused from migration `0109` line 67 |
| QR10.4 | Calling the upsert twice updates destination/label on the same row, never creates a second row |
| QR10.5 | The upsert **never touches `is_enabled`** — a card toggled on stays on across a destination/label update |
| QR10.6 | A newly created card defaults `is_enabled` to false |
| QR10.7 | `set_qr_smart_card_enabled` toggles the flag in both directions, and never touches destination/label |
| QR10.8 | `set_qr_smart_card_enabled` on a channel that has never upserted a card raises not-found (`P0002`) — never an implicit create |
| QR10.9 | `set_qr_smart_card_enabled` by a non-owner/admin raises the identical not-found (`P0002`) — not a distinguishable forbidden |

### B. No scene concept, no counter — structural proofs

| ID | Criterion |
|---|---|
| QR10.10 | No column named `%scene%`, `%visibility_rule%` or `%safe_zone%` exists on `public.qr_smart_cards` — asserted against `information_schema.columns`, not just claimed in a comment |
| QR10.11 | No column named `%scan%`, `%view_count%`, `%impression%`, `%exposure%` or `%count%` exists on `public.qr_smart_cards` — same assertion method |
| QR10.12 | `qr_smart_card` is already one of migration `0131`'s twenty catalogue keys; this migration adds no key and alters no constraint |
| QR10.13 | No function in this migration reads a tier or calls an entitlement function — storing, viewing and changing a durable creator record is never tier-gated (§12.6) |

### C. The overlay read — two fields, `is_enabled`-gated, never a second toggle field

| ID | Criterion |
|---|---|
| QR10.14 | A valid overlay session on a channel with `is_enabled = true` returns exactly one row of `{destination, label}` |
| QR10.15 | **The returned column set is exactly those two fields** — asserted against `information_schema.parameters` for the function's declared `OUT` columns |
| QR10.16 | `is_enabled = false` returns zero rows even with a perfectly valid token — the toggle IS the read, no separate `enabled` column is returned |
| QR10.17 | A channel that has never configured a card returns zero rows, identical to a disabled one |
| QR10.18 | A bad, foreign, expired or revoked overlay token returns zero rows |
| QR10.19 | Disabling a card makes the overlay read return zero rows on the very next call, while the creator read still shows the (disabled) card — the row is never deleted (§12.6) |

### D. API routes

| ID | Criterion |
|---|---|
| QR10.20 | `GET /v1/overlay-widgets/:overlayId/qr-smart-card` with no bearer token is 401; with a token and no store is a retryable 503 |
| QR10.21 | A store answer is narrowed a SECOND time by `projectOverlayQrSmartCard` in the route layer — a scan count, an `isEnabled` flag, a card id or a scene id handed up by a rogue store never reaches the response body |
| QR10.22 | `GET /v1/channels/:channelId/qr-smart-card` (creator session) returns the full card or `null` |
| QR10.23 | `PUT /v1/channels/:channelId/qr-smart-card` (creator session) upserts and returns the card; a non-owner/admin channel is 404 (never a leaking 403) |
| QR10.24 | The upsert body schema's `additionalProperties: false` rejects a body carrying `scanCount`, `allowedDestinations`, `shortLink` or `sceneId` with a 400 before the store is ever called |
| QR10.25 | `PUT /v1/channels/:channelId/qr-smart-card/enabled` (creator session) toggles and returns the card; a non-boolean/missing `enabled` is a 400 (using `enum: [true, false]`, not a bare `type: boolean`, to avoid the AJV type-coercion divergence `routes/safe-mode.ts` already guards against); a channel with no card is 404 |

### E. Canvas module — the first-party QR encoder and the renderer

| ID | Criterion |
|---|---|
| QR10.26 | The encoder produces a square grid sized `17 + 4*version` for every version boundary from 1 through 10 |
| QR10.27 | The encoder places correct finder patterns, an alternating timing pattern, and the always-dark module, for a range of inputs |
| QR10.28 | The encoder is deterministic for identical input and produces a different matrix for a different destination |
| QR10.29 | The encoder handles a single-character destination and a multi-byte-UTF-8 destination (emoji, accented Latin) without error |
| QR10.30 | The encoder returns `null` (never throws) once a destination's UTF-8 byte length exceeds version 10's own capacity at EC level M (213 bytes) |
| QR10.31 | The SVG path builder emits exactly one subpath per dark module, applies the quiet-zone offset correctly, and returns `''` for an empty/all-light matrix |
| QR10.32 | The module renders nothing until a real, non-null snapshot lands; it hides again (and clears the label/path) the moment a later snapshot goes back to null — it does not latch on |
| QR10.33 | The module creates exactly one card container, one `<svg>`, one `<path>` and one label element, regardless of the QR code's version/size (§19.5 bounded DOM) |
| QR10.34 | The module rebuilds the SVG path only when the destination/label actually changes, not on every snapshot |
| QR10.35 | **§9.1.1 structural proof, at the rendered-DOM level:** no `<a>`, `<iframe>` or `<script>` element exists anywhere in the module's output, and the destination string never appears as an `href` or `src` attribute on any rendered element |
| QR10.36 | **External verification, recorded but not re-run by the unit suite:** every supported version (1–10), the boundary lengths between them, a 1-character and a 120-character destination, and a Unicode destination were round-tripped through `zbar` (a real, independent, spec-compliant decoder) during development and decoded back byte-for-byte to the original string |

---

## Commands run

| Command | Result |
|---|---|
| Full SQL suite (`sh packages/db/tests/run-sql-suite.sh`, all 68 files incl. this slice's own) | pass=68 fail=0 |
| `apps/api` route/unit suite (`tsx --test 'test/**/*.test.ts'`; package is named `@bharatstudio/alerts-api` in this checkout, not `@bharatstudio/api`) | tests 712, pass 712, fail 0 (20 of which are this slice's own route tests) |
| `apps/web` suite (`tsx --test ... 'app/**/*.test.ts' 'app/**/*.test.tsx'`; package is named `@bharatstudio/alerts-web`, not `@bharatstudio/web`) | tests 583, pass 583, fail 0 (23 of which are this slice's own encoder/renderer tests) |
| `apps/api` TypeScript typecheck (`tsc -p tsconfig.json --noEmit`, separate from the test runner) | 0 errors |
| `apps/web` TypeScript typecheck (`tsc -p tsconfig.json`, `noEmit: true` already in tsconfig) | 0 errors |
| `node contracts/validate-fixtures.mjs` | Validated 52 fixtures plus the v1 template catalogue contract |
| `node contracts/validate-openapi.mjs` | Validated OpenAPI 3.1 document with 91 paths, 104 operation contracts |
| `node contracts/test-openapi-validator.mjs` | Validated 3 negative OpenAPI operation-contract cases |
| `node packages/db/explain-plans/scan-required-queries.mjs` | OK, 22 manifest entries, 9 exemptions |
| `node packages/db/explain-plans/check-plans.mjs` | OK: 22/22 plans current |
| `pnpm harness:check` (`node .github/scripts/api-test-harness-check.mjs`) | all checks passed |
| External encoder verification (`zbarimg`, installed via Homebrew for verification only) against 16+ generated QR images spanning versions 1–10 plus edge cases | every image decoded to the exact original input string |

Not run: `go test`/`go vet` on the three Go services, `pnpm build`, and Docker image builds — none of
this slice's files touch Go services or change build output shape, and the full `verify:local` chain
(which also runs load/fault self-tests) was judged out of proportion to a schema-and-two-endpoints
slice. Flagged here rather than silently skipped.
