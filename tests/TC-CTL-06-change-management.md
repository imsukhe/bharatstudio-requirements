# TC-CTL-06 — change management, phase 2 Lane A: acceptance record

**Date:** 2026-09-17
**Owner:** **Sukhdev Singh**
**Task:** `../active/tasks/CTL-06-change-management.md`
**Decision:** `../reviews/2026-09-17-ctl-change-management-implementation.md`
**Authority:** `../FULL-PRODUCT-DEFINITION.md` §31.19 rows CTL-06/CTL-07/CTL-08/CTL-09 ·
`active/launch/00_LAUNCH_SCOPE_AUTHORITY.md`

Written to accompany implementation, per `governance/AGENTS.md`. The "Commands run" table is
filled in from actual output against a real `postgres:16-alpine` container and a real `tsc`/`tsx
--test` run, and is the single place this task's numbers live.

---

## Acceptance criteria

### A. CTL-06 — staged effective-time changes, read-time correctness

| ID | Criterion |
|---|---|
| CTL06.1 | `capability_change_requests.effective_at` accepts a future timestamp; a change proposed with one stays `status = 'approved'` (never `'applied'`) and `public.capability_registry` is untouched until that moment passes |
| CTL06.2 | A change whose `effective_at` has ALREADY passed is applied on the very next PLAIN READ through this plane (`staff_get_capability_change` or `staff_list_capability_changes`) — no explicit "apply"/"sweep" call anywhere, proving read-time correctness without a scheduler |
| CTL06.3 | Re-reading an already-applied change is idempotent — `public.capability_registry.version` does not drift on a repeat read |
| CTL06.4 | Omitting `effectiveAt` at propose time defaults to "now" — an ordinary, unstaged change still goes through the full CTL-07 gate and applies itself the instant that gate closes |

### B. CTL-07 — three separate authority rules

| ID | Criterion |
|---|---|
| CTL07.1 | Two DISTINCT `staff` approvals are required before `approved`; one approval alone is not enough |
| CTL07.2 | The same approver cannot approve the same change twice (`UNIQUE(change_request_id, approver_id)`, `unique_violation`) |
| CTL07.3 | **The proposer of a change may never approve their own change** (maker-checker) |
| CTL07.4 | `requiresOwnerSignoff` is `true` only for an EXISTING capability's paid (`pro`/`creator`/`studio`) → `null`/`free` `min_tier` move; `false` for a brand-new capability's own initial tier and for every non-tier-lowering change |
| CTL07.5 | When `requiresOwnerSignoff` is true, two `staff` approvals ALONE are not enough — `approved` additionally requires `>=1` approval of kind `owner` |
| CTL07.6 | An `owner` approval is rejected on a change that does not require one |
| CTL07.7 | `app_private.staff_kill_capability_now`: ONE platform admin, zero approval rows, immediate effect on `capability_registry.kill_switch` |
| CTL07.8 | Killing a capability that does not exist is a clean rejection, not a crash |
| CTL07.9 | Every function above rejects a non-`is_platform_admin()` caller with `insufficient_privilege` |

### C. CTL-08 — one-action revert, append-only

| ID | Criterion |
|---|---|
| CTL08.1 | `app_private.staff_revert_capability_registry_entry` is a single call, immediately applied, by ONE platform admin |
| CTL08.2 | It restores the values of the capability's immediately-PRIOR version (read from `capability_registry_audit`) |
| CTL08.3 | It produces a NEW forward version (via 0149's own `staff_upsert_capability_registry_entry`, hence 0149's own version/audit triggers) — never a mutation or deletion of any existing `capability_registry_audit` row, proven by byte-for-byte comparison of the untouched audit rows before and after |
| CTL08.4 | A capability at version 1 (no previous version) is rejected, not silently no-op'd |
| CTL08.5 | A capability that does not exist at all is rejected |
| CTL08.6 | The revert is recorded as its own `capability_change_requests` row (`change_kind = 'revert'`) naming the exact `capability_registry_audit` row it restored (`reverts_audit_id`) |

### D. CTL-09 — Layer 1 correctness dimensions structurally unrepresentable

| ID | Criterion |
|---|---|
| CTL09.1 | `capability_change_requests.proposed_capacity_class` is a closed `CHECK` whitelist, IDENTICAL to `capability_registry.capacity_class`'s (CTL-14) — the eight active-capacity concepts, nothing else |
| CTL09.2 | **Behavioural:** each of the nine §12.6.1 durable-record classes attempted as `proposed_capacity_class` (via `staff_propose_capability_change`) raises `check_violation`; none is persisted |
| CTL09.3 | **Structural:** the constraint's own `pg_get_constraintdef` is scanned for the nine forbidden tokens (plus `durable`, `record`) and contains none — the guard that fails when removed (dropping the constraint makes CTL09.2's expected-`check_violation` assertions fail because the forbidden propose call would then succeed) |

### E. API layer — platform-staff-only, same posture as the DLQ admin routes

| ID | Criterion |
|---|---|
| CTL_API.1 | Every route (`POST/GET /v1/admin/capability-registry/changes`, `GET .../changes/{id}`, `POST .../changes/{id}/approve`, `POST .../changes/{id}/reject`, `POST .../{capabilityKey}/kill`, `POST .../{capabilityKey}/revert`) requires `requirePlatformAdmin` — 401 unauthenticated, 403 non-admin |
| CTL_API.2 | Every route fails closed 503 with no configured store, never a crash |
| CTL_API.3 | `CapabilityChangeManagementError` reasons map to the documented HTTP status (404 not_found/capability_not_found, 409 not_open/duplicate_approval, 403 self_approval_forbidden, 400 owner_signoff_not_required/no_previous_version/invalid_input) |
| CTL_API.4 | `proposeChange`'s request schema rejects an undeclared body field and a `capacityClass` outside the CTL-09 whitelist at 400, before the store is ever called |
| CTL_API.5 | `GET .../changes/{id}` returns the change plus its recorded `approvals` array; 404 when not found |

### F. Scope discipline held

| ID | Criterion |
|---|---|
| CTL_SCOPE.1 | Migration `0149`, `0150` and every `SAF-*`/`GOA-*` record are byte-for-byte untouched |
| CTL_SCOPE.2 | The seven existing hand-rolled gates are untouched |
| CTL_SCOPE.3 | `apps/web/app/overlay/canvas/` untouched; `getSubscriberCount()` remains 16 |
| CTL_SCOPE.4 | No admin UI (CTL-04/05/13) or public capability matrix (CTL-10/11/12) was built |

---

## Commands run

| Command | Result |
|---|---|
| Base fix (`git reset --hard 849bb02`) | Applied; worktree confirmed at `849bb02 GOA-01/02/03: a refund could un-complete a goal, and now cannot` |
| Full SQL suite (`sh packages/db/tests/run-sql-suite.sh`, real `postgres:16-alpine` container, incl. this task's own `ctl_change_management.sql`) | pass=75 fail=0 (baseline 74/0; +1 new file) |
| `apps/api` route/unit suite (`tsx --test`; package `@bharatstudio/alerts-api`) | tests 797, pass 797, fail 0 (baseline 790/0; +7, all new: `apps/api/test/capability-change-management-routes.test.ts`) |
| `apps/web` suite (`tsx --test`; package `@bharatstudio/alerts-web`) | tests 644, pass 644, fail 0 (baseline 644/0, unchanged — no web files touched) |
| `apps/api` TypeScript typecheck (`pnpm --filter @bharatstudio/alerts-api build`, i.e. `tsc -p tsconfig.json`, run separately from the test runner) | 0 errors |
| `node contracts/validate-fixtures.mjs` | Validated 66 fixtures plus the v1 template catalogue contract (baseline 65; +1: `capability-change-detail-response.json`) |
| `node contracts/validate-openapi.mjs` | Validated OpenAPI 3.1 document with 113 paths, 131 operation contracts (baseline 107/124; +6 paths / +7 operations — 6 new path keys, 7 operations because `/changes` carries both POST and GET) |
| `node contracts/test-openapi-validator.mjs` | Validated 3 negative OpenAPI operation-contract cases (unchanged) |
| `node packages/db/explain-plans/scan-required-queries.mjs` | OK, 28 manifest entries, 9 exemptions (baseline 27 entries; +1: `app_private.staff_list_capability_changes`, not caught by any of the three scan rules — manifested per this task's own instruction, same posture as phase 1's `get_channel_capabilities`) |
| `node packages/db/explain-plans/check-plans.mjs` | OK: 28/28 plans current (baseline 27/27) |
| `pnpm harness:check` (`node .github/scripts/api-test-harness-check.mjs`) | all checks passed; `capability-change-management-routes.test.ts` reaches Fastify only through `buildApp` (built on the shared AJV options module), never a bare `Fastify()` |

**Not run:** `go test`/`go vet` on the three Go services, `pnpm build` (web), Docker image builds,
and `scripts/load/*` self-tests — none of this task's files touch Go services or change web build
output shape. `pnpm test`'s `measurement:test` sub-step was not separately re-verified here; it is
recorded as environmental (fails in agent sandboxes, passes on `main`) per this task's own
dispatch instructions and the identical finding `TC-CTL-01-capability-control-plane.md` already
recorded for phase 1 under the same base commit lineage.
