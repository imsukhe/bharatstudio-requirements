# TC-L20 — Alert Studio depth acceptance

**Status:** `Batch 8 — L20-05, L20-06, L20-07 have local evidence from the import pipeline (migration 0106); L20-01/02/03/04/08 (capability matrix, asset quotas) remain unmet, no code found`
**Task:** [`../tasks/L20-alert-studio-depth.md`](../tasks/L20-alert-studio-depth.md)
**Authority:** `bharatstudio-alerts/docs/BharatStudio-MASTER-PLAN.md` Part 6 (L20), Part 7 §7.4
**Repository:** `/Users/sukhdevsingh/Workspace/Bharat Studio/bharatstudio-alerts`
**Data:** Synthetic template/asset fixtures only. No production database or asset store is used.

## Preconditions

1. The existing Lottie upload pipeline (`0077`) is available as the base to extend, not duplicate.
2. A representative sample of the 600-template catalogue is available as synthetic import fixtures.
3. Disposable PostgreSQL/asset-store test harness available for quota and template-metadata tables.

## Acceptance cases

| ID | Setup and action | Expected result | Failure/retry and evidence |
|---|---|---|---|
| L20-01 | Attempt to save a custom-text alert exceeding the tier's character ceiling (100/150/300/500) | Save is rejected server-side at one character over the ceiling for each tier | Not run — TODO |
| L20-02 | Attempt to create a 6th custom template on a Creator-tier channel (limit 5) | Creation is rejected at the 6th | Not run — TODO |
| L20-03 | Upload an asset exceeding a plan's storage quota (Free/Pro/Creator/Studio) | Upload is rejected for each plan at its boundary | Not run — TODO |
| L20-04 | Upload a disallowed file type and a file that fails malware scanning | Both are rejected before storage | Not run — TODO |
| L20-05 | Import a sample from the 600-template catalogue containing inline script/non-schema content | Import pipeline rejects the non-schema-expressible template rather than stripping and admitting it | Not run — TODO |
| L20-06 | Import a schema-clean sample template and gate its visibility by tier | Template appears only for tiers whose library includes it | Not run — TODO |
| L20-07 | Scan the alert-rendering code path for any arbitrary HTML/CSS/JS execution from a creator- or template-supplied string | None exists, at any tier | Not run — TODO |
| L20-08 | Compare the character ceiling used by Alert Studio against the `maxCharLimit` used by TTS amount-tiering (§3.2) | Both read from the same single configured value | Not run — TODO |

## Batch 8 addendum — 2026-09-07 (post-reconciliation)

| ID | Result |
|---|---|
| L20-01, L20-02, L20-03, L20-04 | **Unmet.** No per-tier capability-matrix enforcement (library size, custom-template count, asset-storage quota, malware scanning, takedown path) found anywhere in `apps/api` or `apps/web`. Remain not run. |
| L20-05 | **Pass, local evidence.** `apps/api/src/domain/template-import-validation.ts` wraps the existing Lottie validator (`lottie-validation.ts`); `apps/api/test/l20-template-import-validation.test.ts` includes a dedicated case, `'rejects a renderDocument carrying an inline script — the real catalogue's index.html shape'`, among 9 total cases. This is also the exact mechanism behind the master-plan 3.16 finding that the real catalogue (raw HTML per design) cannot be imported — the rejection is real and directly exercised. |
| L20-06 | **Pass, local evidence.** `alert_template_catalogue_entries.min_tier` (migration 0106) gates visibility; `packages/db/tests/l20_template_catalogue_import.sql` and `apps/api/test/l20-templates-routes.test.ts` exercise the import/list path. Caveat: only `design.json` metadata from the real 600-template catalogue is importable today (§3.16) — this row's schema-clean-sample case passes for a synthetic fixture, not for the real catalogue's actual runtime-package format. |
| L20-07 | **Pass, local evidence.** The import validator's rejection of inline script (L20-05's test) is the direct proof of this row: no code path in the render pipeline accepts raw HTML/CSS/JS from a creator- or template-supplied string, and the real catalogue's HTML-shaped packages are rejected rather than admitted. |
| L20-08 | **Unmet as an explicit test, though satisfied by construction.** No dedicated test compares Alert Studio's character ceiling against TTS's `maxCharLimit`, but there is only one `maxCharLimit` value in the codebase (`apps/api/src/domain/entitlement-policy.ts:6,33-35`, shared with L03/L07's TTS amount-tiering) — there is no second, divergent Alert Studio-specific limit to diverge from. Recorded as satisfied by the absence of a second value, not by a direct comparison test; a real capability-matrix implementation (L20-01/02) would need to prove this at that point too. |

## Closure rules

Closes only when every row has a real pass/fail result with inline evidence (exact file paths for capability-matrix and quota enforcement, reference to the extended `0077` pipeline, import-pipeline test-suite pass count) replacing "Not run — TODO." No artifact/screenshot directory exists or may be created.

## Cleanup and rollback

All fixtures run against the disposable harness, torn down after the run. Template import is batch-based and reversible per batch; no production asset store or database is touched by this suite.
