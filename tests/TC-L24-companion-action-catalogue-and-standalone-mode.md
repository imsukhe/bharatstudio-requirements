# TC-L24 — Companion action catalogue and standalone mode acceptance

**Status:** `Code built and locally test-suite-green for the server-side/macOS scope; several acceptance cases below still lack a re-run pass count in this reconciliation; L24-06/L24-07 (regression, no-row-rewrite) confirmed by direct reading; native OBS handshake against a real OBS install and any Windows evidence remain unmet — see per-row notes`
**Task:** [`../tasks/L24-companion-action-catalogue-and-standalone-mode.md`](../tasks/L24-companion-action-catalogue-and-standalone-mode.md)
**Authority:** `bharatstudio-alerts/docs/BharatStudio-MASTER-PLAN.md` Part 6 (L24), Part 7 §7.11 items 23–28
**Repository:**
- `/Users/sukhdevsingh/Workspace/Bharat Studio/bharatstudio-alerts` (API/entitlement/Companion state)
- `/Users/sukhdevsingh/Workspace/Bharat Studio/bharatstudio-companion-mobile` (catalogue UI)
- `/Users/sukhdevsingh/Workspace/Bharat Studio/bharatstudio-companion-desktop` (native OBS control, macOS/Windows)
**Data:** Synthetic channel/entitlement/activation fixtures only. No real OBS instance or production Companion account is required to close L24-01 through L24-05; native OBS WebSocket evidence against a real OBS install is a separate device-evidence gate, consistent with L07's own test record conventions.

## Preconditions

1. L07's pairing, secure storage and control-session lease are already built and their existing test suite is green (baseline to protect against regression).
2. Migration `0041` (three-action allowlist) and `0042` (layout slot validation) exist and are understood before extension.
3. Disposable PostgreSQL test harness available for the allowlist/target-type-discriminator migrations.

## Acceptance cases

| ID | Setup and action | Expected result | Failure/retry and evidence |
|---|---|---|---|
| L24-01 | Provision a Companion-only signup with no payment account connected | Zero Alerts actions appear in the catalogue; OBS grid is present and its slots reflect activation state (paired vs. not) | Code path exists (`companion.ts` entitlement resolution + `companion_grant_policies`/0100 channel-scoped entitlement); not run against a real provisioned signup in this reconciliation — OPEN |
| L24-02 | Provision a Free Alerts account with no OBS helper paired | Queue controls (`pause_queue`/`resume_queue`) are enabled; OBS actions are disabled until a helper is paired | Code path exists (0093's `helper_paired`/`obs_connected` signals feed the activation layer); not run against a real provisioned account — OPEN |
| L24-03 | Send an `obs_set_scene` action directly to the API (bypassing the client picker) for a channel not entitled to OBS actions | Rejected server-side — the client filter is proven to not be the actual authority | Server-side entitlement check confirmed present in `apps/api/src/routes/companion.ts` (`resolveEntitledGroups`, Layer 1); included in `apps/api` 285/285 last-known suite count, not individually re-run/re-cited in this pass — OPEN pending an isolated pass count |
| L24-04 | Send an `obs_set_scene` action for an entitled but not-yet-activated (helper unpaired) channel | Rejected server-side by the activation layer, distinct from the entitlement layer | Activation-layer check confirmed present (companion.ts, distinct from Layer 1); same evidence caveat as L24-03 — OPEN pending an isolated pass count |
| L24-05 | Submit a layout patch assigning a queue-shaped target to an `obs_*` action | Rejected — the correct shape is enforced per action type | PASS, with a recorded mechanism deviation. Enforcement is in SQL inside `app_private.update_companion_layout` (`packages/db/migrations/0089_v1_l24_companion_action_catalogue.sql:320-348`), not a `target_type` column with a per-type CHECK as the task's wording implied. The layout table has no direct write grant, so the definer function is the only write path; `apps/api/src/routes/companion.ts:196` merely translates the raised exception into `companion_layout_target_shape_invalid`. An earlier draft of this row wrongly called this application-layer-only — corrected 2026-09-07. |
| L24-06 | Apply the `0041` allowlist-extension and `0042` target-type migrations to a harness pre-populated with historical `companion_commands` rows using the original three actions | No historical row is rewritten or deleted; migrations apply `NOT VALID` as documented | MET: `0089_v1_l24_companion_action_catalogue.sql` drops and re-adds `companion_commands_v1_action_check` (same constraint name as `0041`) with `NOT VALID`; no `DELETE` or destructive `UPDATE` against `companion_commands` rows in 0089, 0093, or 0100 (confirmed by direct reading). No target-type migration exists (see L24-05) |
| L24-07 | Re-run L07's existing acceptance suite (pairing, secure storage, lease, "no arbitrary command execution") after this task's changes | All previously-passing L07 criteria still pass, unchanged | Not independently re-run in this reconciliation; last-known counts cited in the task file (`apps/api` 285/285 etc.) are asserted, not re-executed here — OPEN pending an actual re-run and dated record |
| L24-08 | Inspect a disabled action slot in the catalogue UI (web and mobile) | UI states which layer failed (not entitled vs. not activated) rather than a silent grey-out | Not independently inspected in this reconciliation (web/mobile UI code not read) — OPEN |
| L24-09 | Provision a Companion-only signup and inspect the channel created for it | An implicit channel exists with no payment account connected and no tip page published; no second, non-channel scope is introduced | Data-model support confirmed (`companion_grant_policies`/0100 keys off the existing channel-as-entitlement-unit model, no new scope table found); not run against a real provisioned signup — OPEN |

## Additional evidence outside the original acceptance table

The five-way allowlist mirror (`bharatstudio-alerts/scripts/companion-action-catalogue-drift-check.mjs`) was run directly during this reconciliation and passed: 17 actions across 5 sources (0089 SQL, `apps/api/companion.ts`, macOS `CompanionPolicy.swift`, Windows `CompanionPolicy.cs`, mobile `CompanionApi.ts`), "No drift," exit 0. This is real, dated (2026-09-07) evidence, distinct from the last-known whole-suite pass counts cited elsewhere, which were not re-executed.

## Closure rules

Closes only when every row has a real pass/fail result with inline evidence (exact migration filenames for the `0041`/`0042` extensions, exact file paths for entitlement tier-matrix, Companion state endpoint, implicit-channel provisioning, native OBS control in both `bharatstudio-companion-desktop` platforms, and catalogue UI in web/mobile; test-suite pass counts including the direct-API bypass test) replacing "Not run — TODO." L24-07's evidence must cite L07's own test files/pass counts (e.g., `swift test` count, mobile Jest count, API test count) to prove no regression. No artifact/screenshot directory exists or may be created. **Not yet closed**: L24-01, L24-02, L24-03, L24-04, L24-07, L24-08, L24-09 remain open pending an isolated, dated test re-run (this reconciliation verified code presence and the drift check directly, not per-case pass counts); L24-05 is only partially met and records a real deviation from the task's original migration-based plan; L24-06 is fully met by direct reading.

## Batch 8 amendment — 2026-09-07 (post-reconciliation)

No L24-owned migration or code shipped in batch 8 (`packages/db/migrations` still shows only 0089/0093/0100 for L24; repo total is now 106 migrations, all from other lanes). Every row above stands unchanged.

## Authorization regression evidence — 2026-09-09

`cd apps/api && npx tsc --noEmit && npx tsx --test
test/companion-entitlement-grant-policy.test.ts` passed **6/6**. The added
case supplies a permissive live policy but an explicit empty override and then
a malformed override; each direct `/v1/channels/:channelId/companion/actions`
request returns `403 companion_action_group_not_entitled`. This confirms the
API treats override presence as authoritative and fails closed before action
activation or execution. `sh packages/db/tests/run-sql-suite.sh` also passed
**44/44** after 110 migrations. This focused evidence does not close the
native, Windows, deployed-OBS, or other explicitly open acceptance rows.

**Full-test gate correction — 2026-09-09:** the full-test endpoint now applies
the alerts entitlement and overlay activation gate before creating its
synthetic alert. Focused Companion authorization tests passed **18/18** and
the full API suite passed **399/399** with a TypeScript build. This closes a
route-level bypass found in self-review; it does not close native or deployed
acceptance gates.

**Full-test entitlement regression — 2026-09-09:** a policy with an explicitly
unentitled alerts group now receives `403 companion_action_group_not_entitled`
before a store fake that would accept `send_test_alert` can write anything. The
inactive-overlay case remains a pre-write
`409 companion_action_not_active`. `npx tsc --noEmit && npx tsx --test
test/l07-companion-feature-store.test.ts` passed **13/13**; the full API suite
and build passed **400/400**. These supersede the prior 18/18 and 399/399
counts and remain local evidence only.

## Cleanup and rollback

All fixtures run against the disposable PostgreSQL harness, torn down after the run. Both migrations are additive/`NOT VALID`; no production `companion_commands` or layout row is touched by this suite. Native OBS device-evidence (real OBS WebSocket handshake) remains a separate release-gate item, not required to close this definition-level test record, consistent with how L07's own test record (`TC-L07`) treats device/native evidence as a distinct pending gate from local/contract evidence.
