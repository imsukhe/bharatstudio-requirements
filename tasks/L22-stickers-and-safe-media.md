# L22 — Stickers and safe media

**Status:** `Curated catalogue and viewer selection locally implemented through migration 0110; creator packs, tier pack quotas, and L20 moderation workflow remain open`
**Level:** L2
**Owner:** [OWNER — product/web/trust-safety, unassigned]
**Depends on:** L16 (sticker/reaction is interaction type #3 on the interaction menu), L20 (asset scanning/storage pipeline)
**Blocks:** none recorded
**Test record:** [`../tests/TC-L22-stickers-and-safe-media.md`](../tests/TC-L22-stickers-and-safe-media.md)

## Authority and evidence

Master plan Part 6, "L22 — Stickers and safe media" (lines ~1155–1168); Part 6 L16 interaction-type table (row 3: "Sticker / reaction — approved assets only").

## Objective

Let viewers trigger sticker/reaction visuals using only BharatStudio-approved or creator-approved assets. No arbitrary viewer upload at launch.

## Tasks

1. Sticker catalogue by tier (Free small, Pro larger, Creator full eligible, Studio full).
2. Viewer selection UI, available at every tier.
3. Creator pack: Pro small, Creator limited, Studio larger; none at Free.
4. Moderation: catalogue-level moderation at Free/Pro; scan-plus-attest at Creator; a review workflow at Studio.
5. Viewer upload: explicitly not built in v1 (see boundary below).

## Exact implementation boundary

In scope: catalogue-driven sticker selection and creator packs, gated by the tier table above, reusing L20's asset-scanning/storage pipeline rather than a second one.

Out of scope, permanently for this task's v1 acceptance: viewer-uploaded stickers. The master plan marks viewer upload "No / No / No / v2, controlled" — even Studio's "v2, controlled" is future work, not this task's deliverable.

## Non-negotiable implementation rules

- No arbitrary viewer media upload at launch, at any tier. This mirrors L16's interaction-menu-wide rule.
- Every sticker asset a viewer can trigger is either BharatStudio-approved (catalogue) or creator-approved (creator pack) — never viewer-supplied, in this task's scope.
- Reuse L20's asset-scanning/storage pipeline; do not stand up a second scanning path for sticker assets.

## Definition gate

Per `governance/AGENTS.md`, L2 work stops after definition pending explicit approval. Owner unassigned: [OWNER].

## Acceptance criteria

- A viewer can select and trigger only catalogue or creator-pack stickers; any attempt to submit a viewer-supplied image is rejected before reaching the overlay, proven by test.
- Creator-pack size limits (small/limited/larger by tier) are enforced server-side at the boundary (test the next-item-over-limit case).
- Sticker assets pass through the same scanning/sanitisation path as other L20 assets — proven by test referencing the same pipeline, not a duplicated one.
- Moderation level (catalogue-only vs scan-plus-attest vs review workflow) matches the creator's tier and is enforced server-side.

## Evidence required for closure

Inline prose citation: exact file paths for the sticker-selection UI and creator-pack management; migration filenames for any new sticker-catalogue/creator-pack tables; test-suite pass count for the upload-rejection and tier-boundary cases; explicit reference to the shared L20 pipeline file/module reused (not duplicated). No artifact/screenshot directory.

## Rollback

Sticker catalogue and creator-pack tables are new and additive; disabling this interaction type removes it from the interaction menu without affecting tip/TTS-tip/other L16 interaction types or payment/alert history. No production migration without separate explicit approval.

## 2026-09-08 reconciliation

`packages/db/migrations/0110_v1_l22_sticker_catalogue.sql` implements a
durable BharatStudio-approved catalogue (`sticker_catalogue_entries`), live
tier eligibility, creator enable/disable controls, and a one-catalogue-id
selection attached only to an already-paid tip. Routes are
`apps/api/src/routes/stickers.ts`; creator management is
`apps/web/app/dashboard/stickers/StickerPanel.tsx`. The validator is
`apps/api/src/domain/sticker-import-validation.ts`, deliberately wrapping the
existing template/Lottie structural validation rather than creating a new
asset path.

This satisfies the no-viewer-upload boundary and the curated catalogue
selection slice. It does **not** add creator-supplied packs, the documented
small/limited/larger pack quota, scan-plus-attest, Studio review, or an L20
asset takedown pipeline. The latter must remain open: a creator only toggles
an approved catalogue entry in the present code.

Local evidence at the 2026-09-08 execution: the SQL suite applied **110**
migrations and passed **44/44**, including `l22_sticker_catalogue`; API
`test/l22-sticker-routes` was in the **396/396** suite; dashboard sticker
tests were in the **287/287** web suite and production build. See the associated review record for the
scope/rollback boundary. No staged media scan or independent review is
claimed.

## Regression recheck — 2026-09-09

After the frozen dependency install, the complete local run passed API
**398/398**, web **289/289** with typecheck/production build, and SQL
**44/44** after 110 migrations. Creator-pack quota, scanning/attestation,
Studio review, and takedown controls remain open.
