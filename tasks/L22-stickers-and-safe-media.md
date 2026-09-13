# L22 — Stickers and safe media

**Status:** `Curated catalogue, viewer selection AND creator packs locally implemented through migration 0119, with tier pack quotas (Pro 10 / Creator 25 / Studio 50, an implementation choice not a plan citation) and a tiered moderation ladder (structural scan / attestation / pending_review-until-reviewed); the Studio human-review step is routed and staff-gated through migration 0122 (see the batch 11 correction below); malware scanning (stage 2 of the shared asset-scan pipeline) remains a documented no-op pending an infra decision`
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

## Batch 10 reconciliation — 2026-09-13

Verified against `bharatstudio-alerts` commit `30ff3bf` (`feat(0119): creator sticker packs and a shared asset-scan entry point`), read directly.

- Migration `0119_v1_l22b_creator_sticker_packs.sql` adds creator-supplied packs in wholly separate tables from the BharatStudio-approved catalogue — confirmed by reading the migration; neither listing function reads the other's table.
- Pack size limits confirmed: `app_private.creator_pack_tier_limit` (migration lines 105-121) returns 10 (pro) / 25 (creator) / 50 (studio). This task's own file says only "Pro small, Creator limited, Studio larger" with no numbers — the 10/25/50 ladder is a documented implementation choice by the building agent, not a citation from this task, and is flagged here for product sign-off, matching the commit's own framing.
- Moderation ladder confirmed tier-scoped: Pro gets the structural scan only; Creator additionally requires attestation; Studio uploads are inserted as `pending_review` (migration line 66 CHECK constraint; line 194 sets `pending_review` for `current_tier = 'studio'`) and are invisible to every listing function until reviewed.
- `apps/api/src/domain/asset-scan-pipeline.ts` confirmed as the shared entry point: both the sticker-pack path and this batch's stage-1 structural check delegate to the single existing structural walker rather than a second implementation. Stage 2 (malware/AV scanning) is confirmed a documented no-op in the same file — no AV vendor exists in this codebase, and the file records the migration trap for whoever implements stage 2 (L20's template-import validator calls the structural validator directly, bypassing the shared pipeline; harmless only while stage 2 does nothing).
- Studio review workflow: confirmed a DB primitive exists (an approve/reject function moving a pack sticker out of `pending_review`) but no route calls it — no platform-staff role exists anywhere in this codebase to gate one, confirmed by repo-wide search for `platform-staff`/`platform_staff` finding only this migration's own commentary, no actual role.
- The only endpoint accepting asset bytes is owner/admin-gated; both public sticker-listing routes resolve an id server-side and never accept bytes — confirmed by reading `apps/api/src/routes/stickers.ts`.
- Local re-run 2026-09-13: `apps/api` 465/465 (including `l22b-asset-scan-pipeline.test.ts` and `l22b-sticker-creator-pack-routes.test.ts`), `apps/web` 312/312 (including `l22b-creator-pack-panel.test.tsx`), SQL suite 49/49 across 120 migrations (including `l22b_creator_sticker_packs`).

No staged media scan, independent review, or malware-scanning evidence is claimed by this reconciliation. Stage 2 remaining a no-op is recorded as open, not resolved.

## Batch 11 correction — 2026-09-13

**The batch 10 reconciliation entry above is wrong on one point and is corrected here, not deleted.**

Line 97 of that entry records the Studio review workflow as having "a DB primitive but no route — no platform-staff role exists anywhere in this codebase to gate one, confirmed by repo-wide search for `platform-staff`/`platform_staff`". That claim failed twice over:

1. **It was already false when written.** `app_private.is_platform_admin()` has existed since migration `0073` — a real, account-scoped staff predicate independent of any channel role. The reconciliation searched for the literal strings `platform-staff` and `platform_staff` and so never saw it. A search that only proves the absence of a chosen spelling was reported as proving the absence of the concept.
2. **It went stale inside its own batch.** The route was being built concurrently by a sibling lane in the same batch, so the record described a gap that was closing as it was written.

**What is actually true as of migration `0122_v1_l22c_staff_creator_pack_review.sql`:**

- Four functions in `app_private` — `staff_list_pending_creator_pack_stickers`, `staff_get_creator_pack_sticker_for_review`, `staff_review_creator_pack_sticker`, `staff_list_creator_pack_review_audit` — each gate on the pre-existing `app_private.is_platform_admin()` rather than on a newly invented parallel role. Reusing the existing predicate is the correct call: a second staff concept would have been a second thing to keep in sync.
- `public.staff_creator_pack_review_audit` records who reviewed what, when, and why.
- Routes exist in `apps/api/src/routes/admin.ts` (lines ~196–265), wired through `dependencies.staffCreatorPackReview`.
- The boundary is explicit in the migration's own header comment: a channel owner or channel admin holds no `is_platform_admin` row and is refused exactly like any other non-staff caller. No channel-level action can flip it.

**Process consequence:** governance reconciliation must run *after* a batch closes, never inside it. A reconciliation lane running alongside build lanes records the tree as it was at dispatch, not as it is at commit. This correction exists because that ordering was wrong for batch 10.

**Verification, 2026-09-13, full tree quiet:** SQL suite 51/51 across all migrations through `0123` (real Postgres 16, `ON_ERROR_STOP=1`, so every migration through 0123 is proven to apply); `apps/api` 496/496 with `tsc` clean; `apps/web` 324/324 with `tsc` clean; companion macOS 34/34; companion mobile 97/97; marketing 8/8; all three Go services build and test clean; companion action-catalogue drift check reports no drift across all five mirrors.

Stage 2 malware scanning remains a documented no-op. That part of the batch 10 entry stands unchanged.
