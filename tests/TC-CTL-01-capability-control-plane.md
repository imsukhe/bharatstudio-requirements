# TC-CTL-01 — capability control plane, phase 1: acceptance record

**Date:** 2026-09-17
**Owner:** **Sukhdev Singh**
**Task:** `../active/tasks/CTL-01-capability-control-plane.md`
**Decision:** `../reviews/2026-09-17-ctl-phase-1-implementation.md`
**Authority:** `../FULL-PRODUCT-DEFINITION.md` §12.6, §12.6.2, §30, §31 rows CTL-01/CTL-02/CTL-03/CTL-14/CTL-15 · `active/launch/00_LAUNCH_SCOPE_AUTHORITY.md`

Written to accompany implementation, per `governance/AGENTS.md`. The "Commands run" table is
filled in from actual output against a real `postgres:16-alpine` container, and is the single
place this phase's numbers live.

---

## Acceptance criteria

### A. CTL-01 — the registry table: versioned, audited, every write path covered

| ID | Criterion |
|---|---|
| CTL01.1 | `public.capability_registry` exists with `capability_key` (unique, lowercase-shape-checked), `capacity_class`, `description`, `kill_switch`, `rollout_percentage`, `min_tier`, `version`, `updated_at`, `updated_by` |
| CTL01.2 | `version` starts at 1 on insert and increments on every update — via a `BEFORE INSERT OR UPDATE` trigger, not application convention |
| CTL01.3 | **A direct SQL `UPDATE` (bypassing the staff function entirely) still bumps the version** — proves the guarantee is trigger-based, not a property of one call path |
| CTL01.4 | Every insert/update writes a row to `public.capability_registry_audit` (capability_key, version, action, previous_row, new_row, changed_by, changed_at) via an `AFTER INSERT OR UPDATE` trigger — same "any write path" proof as CTL01.3 |
| CTL01.5 | The audit trail is readable by platform staff (`app_private.staff_list_capability_registry_audit`) and by no one else |
| CTL01.6 | Only `app_private.is_platform_admin()` may write a registry row (`app_private.staff_upsert_capability_registry_entry`) — an ordinary channel owner is rejected `42501` |

### B. CTL-02 — resolution order: kill → denylist → rollout → tier → override, exactly that precedence

| ID | Criterion |
|---|---|
| CTL02.1 | `kill_switch = true` resolves a capability `false` for every channel, unconditionally |
| CTL02.2 | **Kill beats an active channel override that would otherwise say `true`** — the strongest proof of "ahead of override," not merely "ahead of the tier default" |
| CTL02.3 | Channel membership in `capability_denylist` resolves `false` for that channel, with kill off |
| CTL02.4 | **Denylist beats an active override**, independently of kill (kill off, denylist on) |
| CTL02.5 | A channel outside its deterministic rollout bucket (`rollout_percentage = 0`) resolves `false` |
| CTL02.6 | **Rollout beats an active override**, independently of kill and denylist (both off, rollout excludes) |
| CTL02.7 | With kill off, denylist lifted and rollout passing, the tier default applies: a channel below `min_tier` resolves `false` with no override present |
| CTL02.8 | **An explicit `capability_overrides` row flips the tier default** — the only stage that can change a `false` tier default to `true` |
| CTL02.9 | `min_tier IS NULL` resolves `true` on every tier, with no override needed |
| CTL02.10 | An unrecognised tier fails closed (`app_private.capability_tier_rank` raises), never silently resolved |

### C. CTL-03 — the resolved blob: one object per channel, versioned, cached, never per-capability

| ID | Criterion |
|---|---|
| CTL03.1 | `app_private.get_channel_capabilities(channel_id)` returns exactly `resolved, generation, resolved_at` — one jsonb object covering every registered capability, asserted against `information_schema.parameters` |
| CTL03.2 | A second read with nothing changed returns the **identical `resolved_at`** — proof the cache path took no recompute |
| CTL03.3 | A registry write (`staff_upsert_capability_registry_entry`) strictly advances the global generation counter, and the next read recomputes (new `resolved_at`) automatically |
| CTL03.4 | **A channel's own tier changing invalidates its cache even with the generation unchanged** — the cache key is `(generation, tier)`, not generation alone |
| CTL03.5 | `bsa_app` has **no** `SELECT`/`INSERT`/`UPDATE`/`DELETE` grant on any of the five tables this migration creates (`capability_registry`, `capability_registry_audit`, `capability_denylist`, `capability_overrides`, `capability_registry_generation`, `capability_resolutions`) — asserted from the catalogue AND behaviourally (connecting as `bsa_app` and attempting a direct `SELECT` raises `insufficient_privilege`) |
| CTL03.6 | The resolved blob is reachable ONLY through `app_private.get_channel_capabilities` — no function exists that takes a single `capability_key` and returns one flag |
| CTL03.7 | Only channel members (owner/admin/operator/moderator/viewer) can read a channel's blob; a non-member sees zero rows, same posture as every other creator-facing read in this schema |

### D. CTL-14 — the registry structurally cannot gate a durable creator record (§12.6)

| ID | Criterion |
|---|---|
| CTL14.1 | `capability_registry.capacity_class` is a closed `CHECK` whitelist containing only `active_connector, active_widget, ai_usage, media_upload, custom_asset, team_seat, automation_volume, master_canvas_module` — verbatim §12.6.1 rule 3's list, plus the pre-existing `master_canvas_module` concept |
| CTL14.2 | **Behavioural:** each of the nine §12.6.1 durable-record classes (payment, receipt, refund, audit_trail, supporter_relationship, event_history, configuration, layout, moderation_history) attempted as `capacity_class` raises `check_violation`; none is persisted |
| CTL14.3 | **Structural:** the constraint's own `pg_get_constraintdef` is scanned for the nine forbidden tokens (plus `durable`, `record`) and contains none of them — catches a widened whitelist even before an insert is attempted |
| CTL14.4 | The guard fails the way the task requires: dropping the constraint makes CTL14.2's expected-`check_violation` assertions fail (the forbidden insert would then succeed) |

### E. CTL-15 — no per-tier retention field is representable, anywhere in this migration

| ID | Criterion |
|---|---|
| CTL15.1 | `information_schema.columns` is scanned across all six tables this migration creates for `retention`, `retain`, `ttl`, `expir` (any form) — zero matches |
| CTL15.2 | The guard is the absence itself: the test fails the moment a column reintroducing any of those tokens is added to any of the six tables |
| CTL15.3 | `kill_switch`, `rollout_percentage` and `min_tier` gate whether a capability renders; none of them deletes, expires or shortens access to anything a creator already has, and none is retention |

### F. API layer — read-only, one route, phase 1 scope held

| ID | Criterion |
|---|---|
| CTL_API.1 | `GET /v1/channels/:channelId/capabilities` returns the resolved blob for an authenticated member |
| CTL_API.2 | Both "channel not found" and "caller is not a member" map to the identical 404 — no membership-enumeration distinction, same posture `routes/insights.ts` already takes |
| CTL_API.3 | A store failure degrades to a retryable 503, never a crash; an unwired store is 503-safe |
| CTL_API.4 | An invalid `channelId` is rejected 400 at the schema layer before the store is ever called |
| CTL_API.5 | No write route exists in phase 1 — `staff_upsert_capability_registry_entry` has no HTTP surface; CTL-04's admin UI (phase 2, a different repository) is what will call it |
| CTL_API.6 | `registerMasterCanvasRoutes` is untouched — this plane has no overlay-facing surface in phase 1 and takes no position in that registrar's positional argument list |

### G. Scope discipline held

| ID | Criterion |
|---|---|
| CTL_SCOPE.1 | The seven existing hand-rolled gates (`events_pack_entitled`, `soundboard_module_entitled`, `soundboard_tier_rank`, `vertical_canvas_layout_entitled`, `canvas_layout_tier_rank`, `sticker_tier_rank`, `template_tier_rank`) are untouched — zero diff against base `7d8682f`, and every test file covering them still passes |
| CTL_SCOPE.2 | `apps/web/app/overlay/canvas/` is untouched; `getSubscriberCount()` remains 16 |
| CTL_SCOPE.3 | No admin UI, change-management workflow or public capability matrix is built — data-layer primitives only (`staff_upsert_capability_registry_entry`, `staff_list_capability_registry_audit`) that a phase-2 admin surface will call |

---

## Commands run

| Command | Result |
|---|---|
| Base fix (`git reset --hard 7d8682f`) | Applied; worktree confirmed at `7d8682f Close the arbitrary-origin hole the hostile review found in the Media Queue` |
| Full SQL suite (`sh packages/db/tests/run-sql-suite.sh`, 73 files incl. this phase's own `ctl_capability_registry.sql`), real `postgres:16-alpine` container | pass=73 fail=0 (baseline 72/0) |
| `apps/api` route/unit suite (`tsx --test`; package `@bharatstudio/alerts-api`) | tests 779, pass 779, fail 0 (baseline 775/0; +4, all new: `apps/api/test/capability-routes.test.ts`) |
| `apps/web` suite (`tsx --test`; package `@bharatstudio/alerts-web`) | tests 644, pass 644, fail 0 (baseline 644/0, unchanged — no web files touched) |
| `apps/api` TypeScript typecheck (`tsc -p tsconfig.json --noEmit`, separate from the test runner) | 0 errors |
| `apps/web` TypeScript typecheck (`tsc --noEmit -p tsconfig.json`) | 0 errors |
| `node contracts/validate-fixtures.mjs` | Validated 64 fixtures plus the v1 template catalogue contract (baseline 63) |
| `node contracts/validate-openapi.mjs` | Validated OpenAPI 3.1 document with 105 paths, 122 operation contracts (baseline 104/121) |
| `node contracts/test-openapi-validator.mjs` | Validated 3 negative OpenAPI operation-contract cases |
| `node packages/db/explain-plans/scan-required-queries.mjs` | OK, 27 manifest entries, 9 exemptions (baseline 26 entries) |
| `node packages/db/explain-plans/check-plans.mjs` | OK: 27/27 plans current (baseline 26/26) |
| `pnpm harness:check` (`node .github/scripts/api-test-harness-check.mjs`) | all checks passed; 38 files reference `createTestFastify` (`capability-routes.test.ts` uses `buildApp`, itself built on the shared AJV options module, not a bare `Fastify()` — the harness check's own rule 2 scans for exactly that construction and found none in this file) |

**Not run:** `go test`/`go vet` on the three Go services, `pnpm build`, Docker image builds, and
`scripts/load/*` self-tests — none of this phase's files touch Go services or change build output
shape.

**`pnpm test`'s `measurement:test` sub-step is blocked in this sandboxed execution environment,
confirmed pre-existing and unrelated to this phase**, the same class of finding
`TC-PRF-02-slice-7-vertical-layout.md` already recorded for the same sub-step (a different exact
symptom this time): `scripts/measurement/run_local_measurement.py` reads
`../bharatstudio-infra/deployment/v1/measurement-manifest.template.json` relative to a sibling
`bharatstudio-infra` checkout under `.claude/worktrees/`, which does not exist in this session's
worktree layout (`ls .claude/worktrees/` shows only the two `bharatstudio-alerts` agent
worktrees, no `bharatstudio-infra`) — a `FileNotFoundError`, not the docker-availability mismatch
the precedent hit. `scripts/measurement/` has no diff against base commit `7d8682f`, and the
failure reproduces identically running the script directly, outside `pnpm test`. Flagged here
rather than silently worked around; `apps/api` and `apps/web` — the two sub-steps `pnpm test`
actually exercises that this phase could affect — both pass in full, as recorded above.
