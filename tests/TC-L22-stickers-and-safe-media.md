# TC-L22 — Stickers and safe media acceptance

**Status:** `Curated-catalogue AND creator-pack acceptance have local evidence through migration 0119, including tier quotas and the tiered moderation ladder; Studio human-review route and stage-2 malware scanning remain open`
**Task:** [`../tasks/L22-stickers-and-safe-media.md`](../tasks/L22-stickers-and-safe-media.md)
**Authority:** `bharatstudio-alerts/docs/BharatStudio-MASTER-PLAN.md` Part 6 (L22)
**Repository:** `/Users/sukhdevsingh/Workspace/Bharat Studio/bharatstudio-alerts`
**Data:** Synthetic sticker-catalogue and creator-pack fixtures only.

## Preconditions

1. L20's asset-scanning/storage pipeline is available or stubbed for reuse.
2. Disposable PostgreSQL test harness available for sticker-catalogue/creator-pack tables.

## Acceptance cases

| ID | Setup and action | Expected result | Failure/retry and evidence |
|---|---|---|---|
| L22-01 | Attempt to submit a viewer-supplied image as a sticker trigger | Rejected before reaching the overlay, at every tier | **Pass for the implemented catalogue boundary.** No route, schema, or table accepts viewer bytes; `routes/stickers.ts` accepts only an order and approved catalogue ID, and focused API tests reject malformed/unknown/disabled selections. |
| L22-02 | Select and trigger a catalogue sticker as a viewer | Renders through the existing overlay delivery path | **Pass, local selection evidence.** `0110` validates an eligible enabled catalogue ID after a paid tip, and API tests cover attached/unavailable states. Overlay delivery integration remains an L16 boundary and is not claimed by this row. |
| L22-03 | Add creator-pack stickers up to and one past a tier's limit (small/limited/larger) | The over-limit addition is rejected server-side | Not run — TODO |
| L22-04 | Upload a creator-pack sticker asset through the shared pipeline | Same scanning/sanitisation path as other L20 assets is used, verified by code reference, not a duplicated path | Not run — TODO |
| L22-05 | Compare moderation level applied on Free/Pro (catalogue-only) vs. Creator (scan+attest) vs. Studio (review workflow) | Each tier enforces its documented moderation level server-side | Not run — TODO |

## Closure rules

Closes only when every row has a real pass/fail result with inline evidence (file paths, migration filenames, test-suite pass counts, and explicit reference to the shared L20 pipeline module) replacing "Not run — TODO." No artifact/screenshot directory exists or may be created.

## Cleanup and rollback

All fixtures run against the disposable harness, torn down after the run. Sticker/creator-pack tables are new and additive; no production database or asset store is touched by this suite.

## 2026-09-08 reconciliation

| ID | Result |
|---|---|
| L22-01 | **Pass for the implemented catalogue boundary.** There is no route/schema/table accepting viewer bytes; `sticker-import-validation` rejects unsafe catalogue manifests and `routes/stickers.ts` accepts only `orderId` plus `stickerId`. API tests cover malformed/unknown/disabled selections. |
| L22-02 | **Pass, local selection evidence.** `0110` validates the selected id against the channel's current tier/enabled catalogue set after the tip order is paid; API tests cover attach and unavailable states. Overlay rendering of a selection remains a separate L16 interaction integration, not claimed here. |
| L22-03–L22-05 | **Open.** No creator-pack upload table/path, quota, scan-plus-attest, or Studio review workflow exists. A curated catalogue is not evidence for those acceptance rows. |

Reproducible local results at the 2026-09-08 execution:
`sh packages/db/tests/run-sql-suite.sh` applied **110** migrations and
reported **44/44** proofs including `l22_sticker_catalogue`; the API suite was
**396/396**; the web suite was **287/287** and its production build passed. No asset-store, staging, or
independent trust-and-safety evidence is asserted.

**Regression recheck — 2026-09-09:** full dependency-installed API and web
verification passed **398/398** and **289/289** respectively; the disposable
SQL suite remains **44/44** after 110 migrations. Creator-pack and L20 rows
remain open.

## Batch 10 addendum — 2026-09-13

`apps/api/test/l22b-asset-scan-pipeline.test.ts`, `l22b-sticker-creator-pack-routes.test.ts`, `apps/web/.../l22b-creator-pack-panel.test.tsx`, and `packages/db/tests/l22b_creator_sticker_packs.sql` all pass locally as part of API 465/465, web 312/312, SQL 49/49 (120 migrations), re-run 2026-09-13. See `../tasks/L22-stickers-and-safe-media.md` batch 10 section for the pack-quota, moderation-ladder and open-Studio-route detail.

## QA remediation case — 2026-09-14

| ID | Setup and action | Expected result |
| --- | --- | --- |
| L22-06 | Reject then approve the same Studio creator-pack sticker within one transaction | The later approval is deterministically the newest audit row via a monotonic write order; random UUID ordering and timestamp ties cannot reverse it. |

**L22-06 local result: Pass.** `packages/db/tests/l22c_staff_creator_pack_review.sql` now performs both decisions in one transaction and reads `review_order` from migration `0125`; `pnpm verify:local` applied 125 migrations and passed all 52 isolated SQL proofs on 2026-09-14. No operational media-scan/staging conclusion is implied.
