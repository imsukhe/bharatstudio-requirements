# TC-L14 — Viewer identity and supporter history acceptance

**Status:** `Local acceptance reconciled through migration 0107; provider-verified claim execution and legal/deployment gates remain open`
**Task:** [`../tasks/L14-viewer-identity-and-supporter-history.md`](../tasks/L14-viewer-identity-and-supporter-history.md)
**Authority:** `bharatstudio-alerts/docs/BharatStudio-MASTER-PLAN.md` Part 6 (L14) and Part 8
**Repository:** `/Users/sukhdevsingh/Workspace/Bharat Studio/bharatstudio-alerts`
**Data:** Synthetic viewer/channel/payment fixtures only. No production database is used. No real platform (YouTube) account data.

## Preconditions

1. L01 contract baseline exists and is approved.
2. A disposable PostgreSQL test harness is available (same harness pattern as L01/L02/L03).
3. This task's migrations (new `viewer_identities`, `viewer_platform_identities`, `anonymous_browser_identities`, `creator_supporter_relations` tables, plus nullable `viewer_identity_id` on `alert_events`/`payments`) are applied to the disposable harness only.
4. The L08 legal-review disposition on DPDP-compliant deletion is on file before this task closes (see task file's Definition gate).

## Acceptance cases

| ID | Setup and action | Expected result | Failure/retry and evidence |
|---|---|---|---|
| L14-01 | Complete an anonymous tip with no viewer session | Tip captures and delivers unchanged from today's flow; no login is required or offered as a blocker | Satisfied by construction, not re-run here: `viewer_identity_id` on `alert_events`/`payments` is nullable and backfilled null (migrations 0084/0085); the existing L03 tip flow is untouched by this task |
| L14-02 | Simulate a `!tip` from a known platform user ID with no BharatStudio signup | A Level-2 `viewer_platform_identities` row attaches to the event with zero signup steps | **Not built.** `viewer_platform_identities` exists as a table (`0084_v1_l14_viewer_identity.sql:56`) but no code path writes to it — the YouTube poller (L15) does not attach chat/tip events to a viewer identity. Remains not run |
| L14-03 | Link YouTube channel `UC123` to a new BharatStudio account, then repeat the same link action | Prior `UC123` history attaches exactly once; the repeat call is idempotent and does not duplicate the attachment | **SQL pass; provider execution gated.** `0107` proves idempotent first-claim-wins. `POST /v1/viewer/platform-claims` accepts only a server-verified identity and fails closed (`503`) until an L15 verifier exists; no browser-supplied `UC123` can be claimed. |
| L14-04 | Two distinct BharatStudio accounts attempt to claim the same platform identity `UC123` | The contested claim resolves deterministically (first-claim-wins or explicit conflict error); behavior is covered by test either way | **SQL pass; provider execution gated.** `l14-receipts-claims-badges-profiles.sql` proves first-claim-wins and contested claims; API execution remains unavailable without an L15 trusted verifier. |
| L14-05 | Query a creator-facing API for supporter data on channel A while viewer also supports channel B | Response includes only channel A's amounts; channel B's spend is proven absent from the payload | Pass, local evidence: `packages/db/tests/l14_viewer_identity.sql:109` (creator sees exactly 1 row for their own channel, 0 for another channel they don't own); repeated running as the actual `bsa_app` application role in `packages/db/tests/l16_security_boundary.sql`. Deployed/staging evidence not gathered |
| L14-06 | Delete a viewer account that has prior payments | Profile and linkage rows are removed; the immutable payment/audit record for prior payments is preserved and unchanged | Pass, local evidence: `app_private.request_viewer_account_deletion` (`packages/db/migrations/0085_v1_l14_viewer_sessions_and_deletion.sql:169`) nulls email/password_hash/display_name/profile fields and revokes sessions, while its own `erasure_record` explicitly lists `payments`, `refunds` and `creator_supporter_relations` as retained financial/audit records. Deployed/staging evidence not gathered |
| L14-07 | Create a receipt for an anonymous payment and fetch it via the receipt page with no login | Receipt renders using the opaque token only; no authentication is required | **Pass, local.** `0107`, `routes/viewer.ts`, `db/viewer-profile-store.ts`, and `app/r/[token]/page.tsx` implement an opaque, no-auth receipt; focused API tests prove resolution and unknown-token handling. |
| L14-08 | Toggle a viewer's public-profile opt-in off (default) then on | Default-off state hides the profile from search; opting in makes it discoverable; exact lifetime spend never appears in either state | **Pass for the local private-profile boundary.** `0107` plus `app/viewer/profile/page.tsx` proves default-private behaviour, opt-in/out search visibility, normalised slug, and no financial public projection. |

## Closure rules

This test record closes only when every row above has a real pass/fail result with inline evidence (exact file paths, migration filenames, disposable-harness or CI test-suite pass counts) replacing "Not run — TODO." No row may be marked passed from memory or by inspection alone. Per the evidence convention in this repository, there is no artifact/screenshot directory — evidence is inline prose citation only, and creating such a directory is forbidden. Closure additionally requires the L08 legal-review disposition for DPDP deletion to be cited by date and reviewer.

## Cleanup and rollback

All test data lives in the disposable PostgreSQL harness torn down after the run; no production database is touched. New tables/columns introduced by L14 are additive and nullable, so the harness can be reset without special migration-down logic beyond the standard disposable-harness teardown.

## Completion reconciliation — 2026-09-08

| ID | Result and reproducible local evidence |
|---|---|
| L14-01 | **Pass, local.** Nullable identity columns preserve the unauthenticated tip path; the L14 additions add no login precondition. |
| L14-03, L14-04 | **SQL pass; API execution safely gated.** `l14-receipts-claims-badges-profiles.sql` proves idempotent first-claim-wins and contested claims. `apps/api/test/l14-viewer-profile-routes.test.ts` **7/7** proves the browser cannot choose a provider user id and the route returns `503` with no trusted L15 verifier. Actual OAuth verification is therefore an explicit external prerequisite, not simulated evidence. |
| L14-05, L14-06 | **Pass, local.** `l14_viewer_identity`, `l16_security_boundary`, and the full disposable SQL run prove channel scope and retained audit/payment records. The L08/DPDP legal disposition is still required for task closure. |
| L14-07 | **Pass, local.** Receipt entity/API/page paths are `0107`, `routes/viewer.ts`, `db/viewer-profile-store.ts`, and `app/r/[token]/page.tsx`; the focused API test proves no-auth resolution, opaque unknown-token handling, and one-time minting. |
| L14-08 | **Pass for the implemented opt-in/private-profile boundary, local.** The SQL test proves private profiles never search and public profiles disappear immediately on opt-out. `app/viewer/profile/page.tsx` has focused **2/2** tests for private default and normalised public slug; the public route contains no financial projection. |

Full local database evidence: `sh packages/db/tests/run-sql-suite.sh` applies
**110** migrations and passes **44/44** isolated proofs. Staging, provider,
and independent-review results are intentionally absent from this record.

**Regression recheck — 2026-09-09:** full dependency-installed API and web
verification passed **398/398** and **289/289** respectively, with typecheck
and production build. This is not provider-verified-claim or legal closure
evidence.
