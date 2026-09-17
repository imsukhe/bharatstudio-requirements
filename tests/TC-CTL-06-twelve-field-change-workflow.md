# TC-CTL-06 — twelve-field change workflow: acceptance record

**Date:** 2026-09-17
**Owner:** **Sukhdev Singh**
**Task:** `../active/tasks/CTL-06-twelve-field-change-workflow.md`
**Decision:** `../reviews/2026-09-17-ctl-twelve-field-workflow-implementation.md`
**Authority:** `../FULL-PRODUCT-DEFINITION.md` §20.1, §20.6/§20.6.1, §31.19 rows CTL-06/CTL-07/
CTL-08/CTL-09

Written to accompany implementation, per `governance/AGENTS.md`. The "Commands run" table is
filled in from actual output against a real `postgres:16-alpine` container (migrations 0149
through 0157, base fix commit `20e0c36` confirmed) and real `tsc`/`tsx --test` runs, and is the
single place this task's numbers live.

---

## Acceptance criteria

### A. All twelve fields carried through propose → approve → apply

| ID | Criterion |
|---|---|
| CTL12.1 | `staff_propose_capability_change` accepts all twelve fields (14 positional arguments: the original 8, plus `kind`, `limits`, `beta`, `marketingVisible`, `marketingLabel`, `marketingBlurb`) |
| CTL12.2 | A change proposing real values for all twelve fields, once approved by two distinct staff, applies all twelve to `capability_registry` — not just the original six |
| CTL12.3 | `staff_get_capability_change`/`staff_list_capability_changes`/`staff_approve_capability_change`/`staff_reject_capability_change`/`staff_kill_capability_now`/`staff_revert_capability_registry_entry`/`capability_change_row` all project the SAME widened 24-column shape (`information_schema.parameters`, exact match) |

### B. Merge semantics — the permanent, documented behaviour for the six new fields

| ID | Criterion |
|---|---|
| CTL12.4 | An ORDINARY six-field-only propose call (the original 8-positional-argument shape, the six new parameters at their SQL default of `NULL`) preserves the capability's current `kind`/`limits`/`beta`/`marketing_visible`/`marketing_label`/`marketing_blurb` untouched on apply |
| CTL12.5 | A caller that DOES supply real values for the six new fields sees them applied exactly as proposed |

### C. CTL-07's three authority rules, unwidened

| ID | Criterion |
|---|---|
| CTL12.6 | Two DISTINCT staff approvals are still required, maker-checker still enforced, even on a change that also carries real values for the six new fields |
| CTL12.7 | A paid→Free `min_tier` move proposed THROUGH THE WIDENED 14-argument call still sets `requiresOwnerSignoff = true`, unaffected by the six new fields also being present in the same call |
| CTL12.8 | A platform admin who is NOT the real owner (`app_private.is_platform_owner()` false) is still rejected (`42501`) attempting an `owner` approval on that change |
| CTL12.9 | The real owner's approval still completes and applies the change — including the six new fields carried in the same proposal |
| CTL12.10 | `staff_kill_capability_now`'s single-admin, no-approval, immediate-effect behaviour is unchanged |

### D. CTL-08 — revert still restores all twelve

| ID | Criterion |
|---|---|
| CTL12.11 | A capability created with a full twelve-field state (version 1), then changed via the governed twelve-field workflow (version 2), then reverted, has ALL TWELVE fields restored to their version-1 values — not just the original six |
| CTL12.12 | The revert's own `capability_change_requests` row (`change_kind = 'revert'`) shows the RESTORED values in `proposed_kind` etc., proving the widened output shape genuinely carries them |

### E. No second path that skips approval

| ID | Criterion |
|---|---|
| CTL12.13 | `app_private.set_capability_registry_entry_unchecked` (the internal helper `apply_due_capability_change` now calls) remains revoked from `public` and NOT granted to `bsa_app` — unreachable directly by the running API, exactly as migration `0155` shipped it |
| CTL12.14 | `staff_set_capability_registry_entry` (the single-admin route's own function) still rejects a call targeting an EXISTING capability after this migration — the bypass migration `0155` closed stays closed |

### F. Guards re-asserted over the widened surface

| ID | Criterion |
|---|---|
| CTL12.15 | CTL-09: every one of the nine §12.6.1 forbidden `capacity_class` values is still rejected on the widened 14-argument propose call (behavioural), and both `capability_registry.capacity_class`'s and `capability_change_requests.proposed_capacity_class`'s own `pg_get_constraintdef` contain none of the nine forbidden tokens (structural, both definitions) |
| CTL12.16 | CTL-14: the registry's own whitelist, unaffected by this migration (no column added to `capability_registry`), still rejects a forbidden class on the direct single-admin write path too |
| CTL12.17 | CTL-15: no retention/TTL/expiry-shaped column exists on `capability_registry`, `capability_change_requests`, or `capability_change_approvals` |
| CTL12.18 | CTL-03: `bsa_app` still has zero table-level grant (SELECT/INSERT/UPDATE) on any of the three tables above |
| CTL12.19 | CTL-06 read-time correctness: a change carrying twelve-field content, staged with an already-past `effective_at`, is applied by the very next plain read (no explicit apply/sweep call), and a repeat read does not re-apply it (`capability_registry.version` stable) |

### G. API layer

| ID | Criterion |
|---|---|
| CTL12.20 | `POST /v1/admin/capability-registry/changes` accepts and forwards `kind`/`limits`/`beta`/`marketingVisible`/`marketingLabel`/`marketingBlurb`, all optional |
| CTL12.21 | An invalid `kind` value is rejected at 400 by the request schema, before the store is ever called |
| CTL12.22 | Omitting all six leaves them `undefined` at the store boundary — never coerced to a real value (`false`/`{}`/`null`) that would defeat merge semantics |

### H. Scope discipline held

| ID | Criterion |
|---|---|
| CTL_SCOPE.1 | `apps/web/app/overlay/canvas/` untouched; `getSubscriberCount()` remains 16 |
| CTL_SCOPE.2 | No `ADM-07` (platform-admin definition), `CTL-04/05/13`, or `CTL-10/11/12` work was done |
| CTL_SCOPE.3 | No numeric `limits` value, price, provider behaviour, legal wording, or retention window was invented anywhere |
| CTL_SCOPE.4 | Migrations `0149`–`0155` are byte-for-byte untouched; every change to their SQL shapes lives in the new migration `0157` |

---

## Commands run

| Command | Result |
|---|---|
| Base fix (`git reset --hard 20e0c36`) | Applied; worktree confirmed at `20e0c36 §20.6.1's emergency kill path, a real owner identity, and the bypass closed` |
| Full SQL suite (`sh packages/db/tests/run-sql-suite.sh`, real `postgres:16-alpine` container, 156 migrations incl. `0157`, 80 test files incl. this task's new `ctl_change_management_twelve_fields.sql`) | pass=80 fail=0 (baseline 79/0; +1 new file) |
| `apps/api` route/unit suite (`tsx --test`; package `@bharatstudio/alerts-api`) | tests 866, pass 866, fail 0 (baseline 865/0; +1 new: propose-forwards-twelve-fields test in `capability-change-management-routes.test.ts`) |
| `apps/web` suite (`tsx --test`) | tests 644, pass 644, fail 0 (baseline 644/0, unchanged — no web files touched) |
| `apps/api` TypeScript typecheck (`tsc -p tsconfig.json --noEmit`, run separately) | 0 errors |
| `apps/web` TypeScript typecheck (`tsc --noEmit -p tsconfig.json`, run separately) | 0 errors |
| `node contracts/validate-fixtures.mjs` | Validated 70 fixtures plus the v1 template catalogue contract (unchanged count — this task edited one existing fixture, `capability-change-detail-response.json`, added none) |
| `node contracts/validate-openapi.mjs` | Validated OpenAPI 3.1 document with 127 paths, 148 operation contracts (unchanged from baseline — this task widened existing schemas, added no new path or operation) |
| `node contracts/test-openapi-validator.mjs` | Validated 3 negative OpenAPI operation-contract cases (unchanged) |
| `node packages/db/explain-plans/scan-required-queries.mjs` | OK, 31 manifest entries, 13 exemptions (unchanged — no new `app_private` call site added) |
| `node packages/db/explain-plans/check-plans.mjs` | OK: 31/31 plans current — `capability-change-management-list.explain.md` re-anchored to migration `0157` (where `staff_list_capability_changes` now actually lives, DROP+CREATE having moved it out of `0152`) and genuinely re-captured (real `EXPLAIN ANALYZE`, real `postgres:16-alpine` container, all 156 migrations applied), not merely re-pointed |
| `pnpm harness:check` (`node .github/scripts/api-test-harness-check.mjs`) | all checks passed; every capability-change-management test reaches Fastify only through `createTestFastify`, never a bare `Fastify()` |

**Not run:** `go test`/`go vet` on the three Go services, `pnpm build` (web/API bundling), Docker
image builds, and `scripts/load/*` self-tests — none of this task's files touch Go services or
change build output shape. `pnpm test`'s `measurement:test` sub-step was not separately
re-verified here; it is recorded as environmental (fails in agent sandboxes, passes on `main`) per
this task's own dispatch instructions and the identical finding `TC-CTL-01-capability-control-
plane.md` and `TC-CTL-06-change-management.md` already recorded under the same base-commit
lineage.
