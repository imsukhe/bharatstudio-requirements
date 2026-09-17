# PRF-02 slice 7 — QR Smart Card (§6 #10): implementation record

**Date:** 2026-09-17
**Owner:** **Sukhdev Singh**
**Authority:** `../FULL-PRODUCT-DEFINITION.md` §6 module #10, §9.1.1, §12.6, §12.7, §19.5, §30.3
**Binding decision:** `2026-09-17-remaining-eight-modules-and-youtube-v1-amendment.md` Part 1 §2
**Task:** `../active/tasks/PRF-02-slice-7-qr-smart-card.md`
**Acceptance:** `../tests/TC-PRF-02-slice-7-qr-smart-card.md`

---

## What this slice is

The QR Smart Card is the smallest of the remaining eight modules by creator-facing surface: one
destination, one label, one toggle. It closes the slice-5 scope review's `BLOCKED-DECISION`
classification, which had module #10 waiting on `CMP-17` (Clutch Mode) and a scene-profile system
— neither of which exists anywhere in this repository. The 2026-09-17 decision is that neither is
needed for a card with exactly one state, and that the module should be built to hold **no scene
concept at all**, so that a future `CMP-17` (a card selected by a scene profile) has nothing to
conflict with.

## Reuse anchors, named as the task requires

| Value / shape | Reused from |
|---|---|
| Destination and label bound, 1–120 characters each | `packages/db/migrations/0109_v1_l17_paid_challenges.sql:67`, `check (char_length(title) between 1 and 120)` — the same bound `0135` (`objective`) and `0145` (`sponsor_card` name, concurrently built) already reuse |
| Owner/admin role check, `has_channel_role` | Used identically throughout — `0109`, `0131`, `0135`, `0140`, `0142`, `0145` |
| "Not-found and not-authorised are the same answer" (`P0002`) | `0135`'s `end_stream_mission`, reused verbatim for `set_qr_smart_card_enabled` |
| "One row per channel, upsert, single toggle" shape | The same shape `0138`'s safe-mode switch and `0145`'s (concurrently built) Sponsor Card use — a single-purpose creator config, not a session lifecycle like the Stream Mission or Giveaway/Tournament cards |
| No second tier gate; `qr_smart_card` is already a module key | `packages/db/migrations/0131_v1_prf02_master_canvas_modules.sql:43` — `'qr_smart_card'` is already in the twenty-key catalogue check constraint. §30.3's placement table has no row naming QR Smart Card specifically, so none is invented here |
| `enum: [true, false]` for a boolean toggle body, not `type: boolean` | `apps/api/src/routes/safe-mode.ts`'s own `setBody` — a measured fix for this API's shared AJV configuration coercing types (a bare `type: boolean` accepts `"true"`/`"false"` strings). Found by writing the negative test, not by reading: the first version of this slice's own `enabledBody` schema used a bare `type: boolean` and a test asserting `{enabled: "true"}` is rejected failed with 200 until this was applied |

## §9.1.1's tension, and how this slice resolves it

The creator's destination IS a URL — that is the entire point of the card — and §9.1.1 forbids any
third-party code, URL, iframe, script or stylesheet from reaching the Master Canvas. The
resolution: the destination is DATA the client renders as a QR code image, never a link the canvas
fetches, navigates to or embeds — the same relationship a printed QR code on a poster has to a
phone camera. This is enforced three independent ways:

1. **Schema:** `destination` is an ordinary bounded `text` column with no `href`/`src`/`iframe`-shaped
   name or format anywhere in migration `0144`.
2. **Runtime type:** `CanvasModuleDefinition` (the shared module contract every canvas module
   implements) has no field for a URL/HTML/script/iframe at all —
   `master-canvas-runtime.test.ts`'s existing structural assertion covers this generically for
   every module, this one included.
3. **Rendered-DOM proof, specific to this module:**
   `qr-smart-card-module.test.ts` asserts directly against the module's own rendered output that
   no `<a>`, `<iframe>` or `<script>` element exists, and that the destination string never
   appears as an `href` or `src` attribute anywhere in the DOM it produces — only inside the SVG
   path's geometric `d` attribute, which is drawn ink, not a navigable reference.

## The first-party QR encoder: why it had to be written, and how it was verified

**No first-party QR encoder existed anywhere in this repository.** Grepped:
`grep -ril "qrcode\|qr-code\|'qr'" --include=package.json .` (no matches for a QR dependency) and
`find . -iname "*qr*"` (the only hits are migration `0123`'s Razorpay dynamic-QR table — a
**provider-hosted image URL**, `qr_image_url`, which is exactly the remote-image-on-the-canvas
shape §9.1.1 forbids, and therefore not reusable here). A third-party library or a remote QR-image
service were both closed off by the task's own instruction; the only remaining option was to write
the encoder.

**What was written:** `apps/web/app/overlay/canvas/modules/qr-smart-card-logic.ts` implements
ISO/IEC 18004's QR Code encoding algorithm from scratch — byte-mode data encoding, Reed-Solomon
error correction over GF(256) (EC level M — an engineering choice for scan reliability, not a
product decision needing a reuse anchor, the same category as choosing a hash algorithm's block
size), finder/alignment/timing pattern placement, all eight standard mask patterns evaluated by the
standard four-rule penalty score, and BCH-encoded format/version information. It supports versions
1 through 10, covering byte-mode payloads up to 213 bytes — comfortably above the 120-character
destination bound even accounting for multi-byte UTF-8 (see `MAX_DESTINATION_BYTES`'s own doc
comment for the documented, non-throwing fallback on the rare input that still doesn't fit).

**Verification, because a QR encoder can look right and be wrong.** QR encoding has several places
a bit-order mistake produces a matrix that is the right size, has right-looking finder patterns,
and still decodes to garbage or nothing — format-info and version-info bit ordering in particular
are not safely derivable by inspection. `zbar` (the real, independent, spec-compliant decoder
`zbarimg` ships with; installed via Homebrew for this verification only, never added as a project
dependency) was used to round-trip every supported version (1–10), the boundary byte-lengths
between them, a 1-character destination, a 120-character destination, and a destination containing
emoji and accented Latin (multi-byte UTF-8) — sixteen-plus generated images, each decoded back to
the exact original string.

**This caught two real, independently-confirmed bugs before any of this code shipped:**

1. **Format-info bit order.** The first implementation read format-info bit `i` as the value's bit
   `i` (LSB-first). Cross-checked against Python's `qrcode` library (versions 1–6, where that
   library is itself correct) by comparing full matrices cell-by-cell: every function/finder/
   timing/data cell matched exactly, and only the format-info strip differed, at exactly the bits
   whose positions the standard's coordinate list orders MSB-first. Fixed to `bit(i) =
   (value >> (14 - i)) & 1`; the cross-check then matched exactly and `zbar` decoded the result.
2. **Version-info bit order (versions 7+).** The naive fix-by-analogy (apply the same MSB-first
   reversal to version info) produced images `zbar` could not decode. Python's `qrcode` library
   turned out to be **independently broken for version 7+** (its own output for a 107-byte
   destination also failed to decode under `zbar` — confirmed by decoding the reference library's
   own generated image, not assumed), so it could not be used as a cross-check for this half.
   Resolved instead by brute-forcing the four possible (bit-order × row/column-major) placement
   conventions against `zbar` directly and keeping the one that decoded correctly: direct
   (LSB-first) bit order with row-major placement — the opposite convention from format info. This
   asymmetry is real, not a copy-paste error: the two information blocks use different bit orders
   in the actual ISO/IEC 18004 figures, and only an external decoder could settle which was which
   with confidence.

Both bugs are recorded here rather than only in a commit message because they are the concrete
answer to "why does this file's header insist on external verification rather than trusting
self-consistency" — a plausible-looking, well-structured, internally-consistent matrix was wrong
twice during this slice's own development.

## No-scene, no-counter proof, stated plainly

`packages/db/tests/prf02_slice7_qr_smart_card.sql` cases QR10.10/QR10.11 scan
`information_schema.columns` for `public.qr_smart_cards` against `%scene%`, `%visibility_rule%`,
`%safe_zone%`, `%scan%`, `%view_count%`, `%impression%`, `%exposure%` and `%count%` — none may
match. This is a standing test a future edit cannot get past by only touching a comment.

## Verification

See `../tests/TC-PRF-02-slice-7-qr-smart-card.md`'s "Commands run" table for the actual numbers
from this run.
