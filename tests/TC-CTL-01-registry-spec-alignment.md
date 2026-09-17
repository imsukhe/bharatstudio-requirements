# TC-CTL-01 — registry spec alignment: acceptance record

**Date:** 2026-09-17
**Owner:** **Sukhdev Singh**
**Task:** `../active/tasks/CTL-01-capability-control-plane.md`, its "CORRECTION, 2026-09-17" section
**Decision:** `../reviews/2026-09-17-ctl-registry-spec-alignment-implementation.md`
**Authority:** `../FULL-PRODUCT-DEFINITION.md` §20 (§20.1-§20.6 in full), §12.6/§12.6.1/§12.6.2, §31
**Predecessor:** `../reviews/2026-09-17-ctl-phase-1-implementation.md` (migration 0149, built against
the wrong section) and migration 0152 (change management)

Written to accompany implementation, per `governance/AGENTS.md`. The "Commands run" table is
filled in from actual output against a real `postgres:16-alpine` container, and is the single
place this slice's numbers live.

---

## Acceptance criteria

### A. Gap 1 — §20.2's declared field set

| ID | Criterion |
|---|---|
| SPEC1.1 | `public.capability_registry` gains `kind` (nullable, `CHECK` enum `widget \| module \| feature \| hub_lane \| lobby_mode \| ai_feature`), `limits` (`jsonb`, `NOT NULL DEFAULT '{}'`), `beta` (`boolean`, default `false`), `marketing_visible` (`boolean`, default `false`), `marketing_label`, `marketing_blurb` (both text, nullable) |
| SPEC1.2 | `capacity_class` (CTL-14's own column) is untouched — a different check constraint, a different concept, both kept, documented explicitly in the migration header so the two are never collapsed |
| SPEC1.3 | `kind = 'marketing_section'` is rejected — §20.2's own enum does not contain it; not invented here (see BLOCKER below) |
| SPEC1.4 | `marketing_visible = true` with `marketing_label` or `marketing_blurb` null is rejected (`check_violation`) |
| SPEC1.5 | Every new field round-trips exactly through `app_private.staff_set_capability_registry_entry` → `staff_get_capability_registry_entry` |
| SPEC1.6 | `limits` defaults to `{}` when not supplied — no numeric limit value is invented anywhere in this slice |
| SPEC1.7 | `app_private.staff_upsert_capability_registry_entry` (0149's original 6-field write function) is BYTE-FOR-BYTE unmodified — same exact 6-argument signature, same exact 8-column output, still passes 0149's own `has_function_privilege` literal-signature probe and exact-output-column assertion (`packages/db/tests/ctl_capability_registry.sql`) |
| SPEC1.8 | An update through the ORIGINAL function leaves `kind`/`limits`/`beta`/`marketing_visible`/`marketing_label`/`marketing_blurb` untouched (its own `SET` clause never mentions them — plain SQL semantics, not new code) |
| SPEC1.9 | `effective_from` is NOT added — 0152's `capability_change_requests.effective_at` already covers staged effective-time (CTL-06); adding a second mechanism would duplicate it |

### B. Gap 2 — §20.3's resolution order, the missing allowlist stage

| ID | Criterion |
|---|---|
| SPEC2.1 | `public.capability_allowlist` exists, same shape as `capability_denylist` (composite PK, cascade on capability delete, references a real channel), revoked from public AND `bsa_app` |
| SPEC2.2 | **Allowlist beats tier**: a channel below a capability's `min_tier` (the lower-precedence rule, left unchanged) resolves `true` once allowlisted — the higher-precedence rule deciding |
| SPEC2.3 | Allowlist beats rollout-exclusion (`rollout_percentage = 0`) — an explicit per-channel grant bypasses the percentage bucket the same way it bypasses tier |
| SPEC2.4 | Allowlist does NOT beat denylist — both active on the same channel/capability, denylist (higher precedence, §20.3 step 2) still decides |
| SPEC2.5 | Allowlist does NOT beat kill — kill (absolute, step 1) still decides |
| SPEC2.6 | `app_private.resolve_channel_capabilities`'s external signature (`(uuid) → resolved, generation, resolved_at`) is UNCHANGED — a body-only `CREATE OR REPLACE`, re-verified against 0149's own exact-output-column assertion |
| SPEC2.7 | The last three §20.3 steps (creator enabled flag, creator configuration, runtime activation) are explicitly judged NOT part of this resolver — recorded in the migration header, not silently omitted |

### C. CTL-14 and CTL-15, re-proven over the widened schema

| ID | Criterion |
|---|---|
| CTL14.W1 | The same nine §12.6.1 forbidden `capacity_class` values are rejected via the NEW write function too (`staff_set_capability_registry_entry`), not just the original one |
| CTL14.W2 | `capability_registry_capacity_class_check`'s own definition, re-scanned, still contains none of the nine forbidden tokens |
| CTL14.W3 | `kind`'s own new check constraint is independently scanned for the same nine tokens — a second taxonomy must not become a second way to smuggle a durable-record concept in |
| CTL15.W1 | `information_schema.columns` re-scanned for `retention\|retain\|ttl\|expir` across ALL nine tables now in play (0149's original six, `capability_allowlist`, and `capability_change_requests`/`capability_change_approvals` from 0152) — zero matches |

### D. 0152 (change management) still works

| ID | Criterion |
|---|---|
| CM.1 | `capability_change_requests` gains six nullable `proposed_*` columns (kind/limits/beta/marketing_visible/marketing_label/marketing_blurb) — no default, so a pre-existing/old-path row has them `NULL` |
| CM.2 | An ordinary propose → two-staff-approve → apply cycle run ENTIRELY through 0152's own unmodified functions (`staff_propose_capability_change`, `staff_approve_capability_change`) still reaches `status = applied` and still takes effect for the fields it knows about (`min_tier`) |
| CM.3 | The SAME cycle PRESERVES the six new fields it never mentions — proof that the original write function's `ON CONFLICT DO UPDATE` never touching those columns is sufficient, no code change needed there |
| CM.4 | `staff_kill_capability_now` (unmodified) preserves the six new fields the same way |
| CM.5 | `staff_revert_capability_registry_entry` (the ONE 0152 function this slice touches, body-only `CREATE OR REPLACE`, external signature unchanged) now restores kind/limits/beta/marketing_visible/marketing_label/marketing_blurb from the immediately-previous version's audit snapshot, not just the original five fields |
| CM.6 | The revert's own `capability_change_requests` row also records the restored `proposed_kind`/`proposed_beta` etc. |
| CM.7 | `staff_get_capability_change`/`staff_list_capability_changes`'s exact-output-column assertion (`packages/db/tests/ctl_change_management.sql`) still passes, unmodified — because neither function, nor `capability_change_row`, was touched |

### E. New staff surface: readable and settable, without a new per-capability consumer query path

| ID | Criterion |
|---|---|
| SURF.1 | `staff_get_capability_registry_entry(text)` and `staff_list_capability_registry_entries()` are staff-only (`is_platform_admin`), revoked from public, granted to `bsa_app` |
| SURF.2 | `staff_set_capability_registry_entry` requires the COMPLETE desired state every call (all 12 fields) — the same idiom 0149's own write function already established |
| SURF.3 | Non-staff is rejected `insufficient_privilege` on all three new functions |
| SURF.4 | CTL-03's posture is unaffected: `bsa_app` still has zero table-level grant on `capability_registry` or any support table (including the new `capability_allowlist`); these are staff/admin introspection functions, the same category as 0149's own `staff_list_capability_registry_audit`, not a new consumer/runtime per-capability query path |

### F. API layer

| ID | Criterion |
|---|---|
| API.1 | `GET /v1/admin/capability-registry/entries`, `GET .../entries/{capabilityKey}`, `PUT .../entries/{capabilityKey}` — platform-admin gated, same posture as `/v1/admin/capability-registry/changes` |
| API.2 | `PUT` requires the complete body (`additionalProperties: false`, every field `required`) — an undeclared field or a missing field is 400 |
| API.3 | `kind: marketing_section` is rejected 400 at the schema layer too |
| API.4 | A `CapabilityRegistryAdminError` maps to 400; an unwired store degrades to a safe 503; a not-found `GET` is 404 |
| API.5 | `/v1/channels/:channelId/capabilities` (the CTL-03 consumer resolved blob) is UNCHANGED — still exactly `schemaVersion, generation, resolvedAt, capabilities` |

---

## Commands run

| Command | Result |
|---|---|
| Base fix (`git reset --hard eac0150`) | Applied; worktree confirmed at `eac0150 SAF phase 1: a moderation pipeline where there was none` |
| Full SQL suite (`sh packages/db/tests/run-sql-suite.sh`, 77 files incl. this slice's own `ctl_registry_spec_alignment.sql`), real `postgres:16-alpine` container | pass=77 fail=0 (baseline 76/0; +1, all new) |
| `apps/api` route/unit suite (`tsx --test`; package `@bharatstudio/alerts-api`) | tests 822, pass 822, fail 0 (baseline 815/0; +7, all new: `apps/api/test/capability-registry-admin-routes.test.ts`) |
| `apps/web` suite (`tsx --test`; package `@bharatstudio/alerts-web`) | tests 644, pass 644, fail 0 (baseline 644/0, unchanged — no web files touched) |
| `apps/api` TypeScript typecheck (`tsc -p tsconfig.json --noEmit`, separate from the test runner) | 0 errors |
| `apps/web` TypeScript typecheck (`tsc -p tsconfig.json --noEmit`) | 0 errors (unaffected, no web files touched) |
| `node contracts/validate-fixtures.mjs` | Validated 68 fixtures plus the v1 template catalogue contract (unchanged — no new fixture file added) |
| `node contracts/validate-openapi.mjs` | Validated OpenAPI 3.1 document with 117 paths, 137 operation contracts (baseline 115/134; +2 paths / +3 operations: `GET /entries`, `GET /entries/{capabilityKey}`, `PUT /entries/{capabilityKey}`) |
| `node contracts/test-openapi-validator.mjs` | Validated 3 negative OpenAPI operation-contract cases |
| `node packages/db/explain-plans/scan-required-queries.mjs` | OK, 29 manifest entries, 11 exemptions (unchanged — no new derivedReadSql-backed function added) |
| `node packages/db/explain-plans/check-plans.mjs` | OK: 29/29 plans current (unchanged — `get_channel_capabilities`'s own hashed body untouched; `resolve_channel_capabilities`'s widened body is not independently hash-checked, per `capability-resolution.explain.md`'s own documented scope, but is described in a new dated section appended to that artifact) |
| `pnpm harness:check` (`node .github/scripts/api-test-harness-check.mjs`) | all checks passed; 39 files reference `createTestFastify` (the new route test uses `buildApp`, same pattern `capability-change-management-routes.test.ts` already established, itself built on the shared AJV options module, not a bare `Fastify()`) |

**`measurement:test`** (`node --test scripts/measurement/run_local_measurement.test.mjs`) fails in
this sandboxed execution environment (`full mode is blocked without external harness` assertion,
`1 !== 2`) — confirmed pre-existing and environmental, not a regression: `scripts/measurement/` has
no diff against base commit `eac0150`, and this slice touches no file the measurement harness reads.
Reported per this task's own instruction to report rather than chase.

**Not run:** `go test`/`go vet` on the three Go services, `pnpm build`, Docker image builds —
none of this slice's files touch Go services or change build output shape.
