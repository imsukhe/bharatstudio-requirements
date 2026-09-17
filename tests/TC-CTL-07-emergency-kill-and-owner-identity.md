# TC-CTL-07 — emergency kill in full, and real platform-owner identity: acceptance record

**Date:** 2026-09-17
**Owner:** **Sukhdev Singh**
**Task:** `../active/tasks/CTL-07-emergency-kill-and-owner-identity.md`
**Decision:** `../reviews/2026-09-17-ctl-emergency-kill-implementation.md`
**Authority:** `../FULL-PRODUCT-DEFINITION.md` §20.6/§20.6.1 · register row CTL-07 ·
`reviews/2026-09-17-platform-owner-identity-decision.md`

Written to accompany implementation, per `governance/AGENTS.md`. The "Commands run" table is filled
in from actual output against a real `postgres:16-alpine` container and a real `tsc`/`tsx --test`
run, and is the single place this task's numbers live.

---

## Acceptance criteria

### A. Job 1 — real platform owner identity

| ID | Criterion |
|---|---|
| OWN.1 | `app_users.is_platform_owner` exists, defaults `false` |
| OWN.2 | `app_users_platform_owner_singleton_idx` rejects a second `true` row (`unique_violation`), proven via a direct `UPDATE` attempt |
| OWN.3 | `app_private.staff_approve_capability_change('owner')` requires `is_platform_owner()` in addition to `is_platform_admin()` — an admin who is not owner is rejected (`insufficient_privilege`), an owner who is not admin is rejected at the SAME top-of-body gate, and an admin who IS the real owner succeeds |
| OWN.4 | `app_private.staff_set_platform_owner` rejects self-conferral (`actor = target_user_id`, 403) |
| OWN.5 | `app_private.staff_set_platform_owner` requires a non-empty reason (22023) |
| OWN.6 | Every ownership change is recorded in `platform_owner_audit` (previous value, new value, changed_by, reason) |
| OWN.7 | `platform_owner_audit` is append-only — a direct `UPDATE`/`DELETE` by the same session that wrote it is rejected (`feature_not_supported`) |
| OWN.8 | A non-admin caller is rejected from `staff_set_platform_owner` |

### B. Job 2 — §20.6.1's emergency kill path, one row at a time

| ID | Criterion |
|---|---|
| KILL.1 | `staff_fire_global_kill`: one admin, alone, immediate `kill_switch=true`, mandatory reason (22023 without one), clean rejection on a non-existent capability |
| KILL.2 | `expires_at` is always exactly `fired_at + 24 hours` — a direct `INSERT` violating that is rejected (`check_violation`), proving the ceiling is structural, not a default an admin could override |
| KILL.3 | Ratification: a second, DISTINCT admin succeeds; the firer attempting to ratify their own kill is rejected (`insufficient_privilege`); a second ratification attempt is rejected (`unique_violation`) |
| KILL.4 | Escalation: an unratified kill past the 4-hour mark reads `escalatedToOwner=true`; ratifying clears it — both read-time derived, proven via a back-dated direct `INSERT` (no real 4-hour wait) |
| KILL.5 | Extension: must move the effective expiry forward (22023 otherwise); capped at the request's own time + 24 hours (`check_violation` otherwise); the proposer cannot also approve (`insufficient_privilege`); a SECOND, distinct admin approving moves the effective expiry to the stated value; a second approval on the same request is rejected (`unique_violation`); proposing on an already-expired kill event is rejected (22023) |
| KILL.6 | **Auto-revert is correct at READ TIME, with no sweeper.** A kill event back-dated 25 hours (already past expiry), read via ONLY a plain `staff_get_kill_event` call — no apply/sweep call anywhere in the test — reports `reverted=true` AND `capability_registry`'s live row already matches the exact pre-kill snapshot (kill_switch, min_tier, capacity_class, kind, limits, beta, rollout_percentage all restored) |
| KILL.7 | The log is immutable: a direct `UPDATE`/`DELETE` on `capability_kill_events` (by the SAME session that fired it) is rejected (`feature_not_supported`); same for `capability_kill_reviews` |
| KILL.8 | **Review blocks the next kill, enforced.** A kill fired with no review on file blocks that actor's NEXT `staff_fire_global_kill` call (409/`object_not_in_prerequisite_state`); filing the review unblocks it |
| KILL.9 | **Never a tier/limit/pricing change — structural.** `information_schema.parameters` scan proves none of `staff_fire_global_kill`/`staff_ratify_kill_event`/`staff_propose_kill_extension`/`staff_approve_kill_extension`/`staff_file_kill_review` accepts a `min_tier`/`limits`/`rollout_percentage`/`capacity_class`/`tier`/`pric*`-named parameter |
| KILL.10 | Every function above rejects a non-`is_platform_admin()` caller |

### C. Job 3 — the single-admin bypass, closed

| ID | Criterion |
|---|---|
| BYP.1 | `staff_set_capability_registry_entry` on a NEW `capabilityKey` succeeds (single-admin create remains legitimate) |
| BYP.2 | `staff_set_capability_registry_entry` on an EXISTING `capabilityKey` is rejected (`insufficient_privilege`) and leaves the row untouched |
| BYP.3 | **Revert still works after the restructure.** `staff_revert_capability_registry_entry` (now calling the internal unchecked helper) restores the immediately-prior version's values (description, min_tier, kind, beta) and produces exactly ONE new forward `capability_registry_audit` row — the two prior rows are untouched |
| BYP.4 | `app_private.set_capability_registry_entry_unchecked` is revoked from `public` AND is NOT granted to `bsa_app` at all |

### D. CTL-15 vs kill-event expiry, and existing guards

| ID | Criterion |
|---|---|
| GUARD.1 | No column across this migration's six new tables matches `retention`/`retain`/`ttl` |
| GUARD.2 | The ONLY columns matching `expir` across those six tables are `capability_kill_events.expires_at` and `capability_kill_extension_requests.new_expires_at` — both kill-event deadlines, named and reasoned about explicitly in the migration header, not data-retention fields |
| GUARD.3 | Every new table (six total) is revoked from `public` AND `bsa_app`; every new staff function is revoked from `public`, granted to `bsa_app` (except the deliberately-unreachable internal helper, GUARD.4) |
| GUARD.4 | CTL-14 (capacity_class whitelist) and 0151's allow-only checks are unaffected — this migration touches neither |

### E. Scope discipline held

| ID | Criterion |
|---|---|
| SCOPE.1 | Migrations `0149`, `0150`, `0151` and every prior `SAF-*`/`GOA-*` record are byte-for-byte untouched |
| SCOPE.2 | `apps/web/app/overlay/canvas/` untouched; `getSubscriberCount()` remains 16 |
| SCOPE.3 | No admin UI (CTL-04/05/13) or public capability matrix (CTL-10/11/12) was built |
| SCOPE.4 | No notification or billing mechanism was invented — see the task's own "what was not built" section |

---

## Commands run

| Command | Result |
|---|---|
| Base fix (`git reset --hard 8a69410`) | Applied; worktree confirmed at `8a69410 CTL registry brought to §20.2's actual field set — and a bypass found while merging` |
| Full SQL suite (`sh packages/db/tests/run-sql-suite.sh`, real `postgres:16-alpine` container, incl. this task's own `ctl_emergency_kill_and_owner.sql`) | pass=79 fail=0 (baseline 78/0; +1 new file) |
| `apps/api` route/unit suite (`tsx --test`; package `@bharatstudio/alerts-api`) | tests 865, pass 865, fail 0 (baseline 852/0; +13, new: `apps/api/test/platform-owner-routes.test.ts`, `apps/api/test/capability-kill-events-routes.test.ts`, plus one new case each in `capability-change-management-routes.test.ts` and `capability-registry-admin-routes.test.ts`) |
| `apps/web` suite (`tsx --test`) | tests 644, pass 644, fail 0 (baseline 644/0, unchanged — no web files touched) |
| `apps/api` TypeScript typecheck (`tsc -p tsconfig.json`, run separately) | 0 errors |
| `node contracts/validate-fixtures.mjs` | Validated 70 fixtures plus the v1 template catalogue contract (unchanged — no new fixture files required) |
| `node contracts/validate-openapi.mjs` | Validated OpenAPI 3.1 document with 127 paths, 148 operation contracts (measured baseline at this checkout, pre-change: 119/140; +8 paths / +8 operations — `setPlatformOwner`, `fireEmergencyKill`, `listEmergencyKills`, `getEmergencyKill`, `ratifyEmergencyKill`, `proposeEmergencyKillExtension`, `approveEmergencyKillExtension`, `fileEmergencyKillReview`) |
| `node contracts/test-openapi-validator.mjs` | Validated 3 negative OpenAPI operation-contract cases (unchanged) |
| `node packages/db/explain-plans/scan-required-queries.mjs` | OK, 31 manifest entries, 13 exemptions (baseline 30 entries; +1: `app_private.staff_list_kill_events`, not caught by any of the three scan rules — manifested per this task's own instruction, same posture as `staff_list_capability_changes` in `CTL-06-change-management.md`) |
| `node packages/db/explain-plans/check-plans.mjs` | OK: 31/31 plans current (baseline 30/30) |
| `pnpm harness:check` (`node .github/scripts/api-test-harness-check.mjs`) | all checks passed; both new route-test files reach Fastify only through `buildApp` (built on the shared AJV options module, the same posture `capability-registry-admin-routes.test.ts` and `capability-change-management-routes.test.ts` already use), never a bare `Fastify()` |

**A discrepancy, reported rather than silently reconciled:** this task's own dispatch instructions
stated a baseline of "contracts 117 paths/137 operations." A fresh `node contracts/validate-openapi.mjs`
run against the base commit (`8a69410`), BEFORE this task's own OpenAPI edits, measured 119
paths/140 operations instead. The delta this task's own edits produced (+8/+8) is exact either way;
the pre-existing baseline number in the dispatch instructions does not match what this checkout's
own tooling reports at that commit, and is recorded here rather than silently overwritten.

**Not run:** `go test`/`go vet` on the three Go services, `pnpm build` (web), Docker image builds,
and `scripts/load/*` self-tests — none of this task's files touch Go services or change web build
output shape. `pnpm test`'s `measurement:test` sub-step was not separately re-verified here; it is
recorded as environmental (fails in agent sandboxes, passes on `main`) per this task's own dispatch
instructions and the identical finding `TC-CTL-06-change-management.md` already recorded under the
same base-commit lineage.
