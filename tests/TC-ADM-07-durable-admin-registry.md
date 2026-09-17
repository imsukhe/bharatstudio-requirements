# TC-ADM-07 — a durable admin registry, and ONE admin identity: acceptance record

**Date:** 2026-09-17
**Owner:** **Sukhdev Singh**
**Task:** `../active/tasks/ADM-07-durable-admin-registry.md`
**Decision:** `../reviews/2026-09-17-adm-07-implementation.md`
**Authority:** `../FULL-PRODUCT-DEFINITION.md` §20.6/§20.6.1 · register rows ADM-07, CTL-13

Written to accompany implementation, per `governance/AGENTS.md`. The "Commands run" table is filled
in from actual output against a real `postgres:16-alpine` container and real `tsc`/`node --test`/
`vitest` runs, and is the single place this task's numbers live.

---

## Acceptance criteria

### A. Job 1 — the durable registry (migration `0156`)

| ID | Criterion |
|---|---|
| REG.1 | `app_private.staff_set_platform_admin` requires the caller to be `is_platform_admin()` — a non-admin caller is rejected (`insufficient_privilege`) |
| REG.2 | Self-conferral is rejected in BOTH directions — an admin targeting themselves with `true` (self-reconfirmation) and with `false` (self-revocation) both fail `insufficient_privilege` |
| REG.3 | A missing or empty reason is rejected (`22023`) |
| REG.4 | A non-existent target user is rejected (`22023`) |
| REG.5 | A real grant sets `app_users.is_platform_admin = true`, records exactly one `platform_admin_audit` row with the correct `previous_value`/`new_value`/`changed_by`/`reason`, and `app_private.staff_list_platform_admins` surfaces the granted user with that audit row's metadata |
| REG.6 | `platform_admin_audit` is append-only — a direct `UPDATE`/`DELETE` by the SAME session that wrote the row is rejected (`feature_not_supported`) |
| REG.7 | Every new table (`platform_admin_audit`) is revoked from `public` AND `bsa_app`; every new function is revoked from `public`, granted to `bsa_app` |
| REG.8 | A non-admin cannot call `staff_list_platform_admins` either |

### B. "0149-0155 still authorise" — proven, not assumed

| ID | Criterion |
|---|---|
| AUTH.1 | A user granted admin ONLY through `staff_set_platform_admin` (never seeded `is_platform_admin=true` directly) successfully calls one representative `is_platform_admin()`-gated function from each of migrations `0149`, `0151`, `0152`, `0153`, and each of `0155`'s three jobs (`staff_set_platform_owner`, `staff_list_kill_events`, `staff_set_capability_registry_entry`'s new-capability path) |
| AUTH.2 | After that same user is revoked through `staff_set_platform_admin`, EVERY one of those same calls now fails `insufficient_privilege` |
| AUTH.3 | Migrations `0150` and `0154` have no `is_platform_admin()`-gated function to test — both are entirely channel-scoped — named explicitly rather than silently skipped |

### C. Bootstrap, named and proven

| ID | Criterion |
|---|---|
| BOOT.1 | With the registry driven to zero admins system-wide (direct SQL, the same access level required to run the migration itself — legitimate test setup, not an application-reachable path), a non-admin calling `staff_set_platform_admin` targeting THEMSELVES is rejected `insufficient_privilege` — no special-cased empty-registry branch exists |
| BOOT.2 | The same non-admin calling `staff_set_platform_admin` targeting SOMEONE ELSE, with the registry still at zero, is also rejected `insufficient_privilege` — an empty registry does not create a privilege escalation for any actor, self-targeting or not |

### D. Owner unchanged (smoke check; full proof remains `ctl_emergency_kill_and_owner.sql`)

| ID | Criterion |
|---|---|
| OWN.1 | `app_users_platform_owner_singleton_idx` still rejects a second `is_platform_owner=true` row after migration `0156` |
| OWN.2 | `app_private.staff_set_platform_owner` remains callable and functions identically (used directly as one of the AUTH.1 representative calls) |

### E. Job 2 — the console (route layer; `packages/db/tests/adm_admin_registry.sql` covers the SQL layer)

| ID | Criterion |
|---|---|
| API.1 | `PUT /v1/admin/platform-admins/:userId` and `GET /v1/admin/platform-admins` are reachable only by a platform admin (403 for a non-admin, 401 unauthenticated) |
| API.2 | `GET /v1/admin/whoami` is reachable only by a platform admin (403/401), returns `{schemaVersion, userId, isPlatformAdmin: true}` on success, and has no field for a caller to branch on instead of the status code |
| API.3 | An unwired store degrades to 503 (`platform_admin_unavailable`), never a crash, on all three routes |
| API.4 | Request-schema validation rejects a missing `reason` and an undeclared body field (400) |
| API.5 | `PlatformAdminError` reasons (`target_not_found`, `self_conferral_forbidden`, `invalid_input`) map to the documented HTTP status (404/403/400) |
| API.6 | An unexpected store failure degrades to a clean, retryable 503, never a crash |

### F. Job 2 — the admin console repository (uncommitted; reviewed, not proven by this repository's own test suite)

| ID | Criterion |
|---|---|
| CONSOLE.1 | `auth.ts` no longer gates `signIn` on `PLATFORM_ADMIN_EMAILS`; any Google account may complete sign-in |
| CONSOLE.2 | `auth.ts`'s `jwt` callback exchanges the Google `id_token` for a real BharatStudio access token via `POST /v1/auth/google/exchange` and carries it on the JWT (falls through safely — no token stored — if the API is unreachable or the exchange fails) |
| CONSOLE.3 | `admin-api.ts`'s `authToken()` forwards that real access token as the bearer (dev-bootstrap escape hatches unchanged); `hasAdminSession()` calls `GET /v1/admin/whoami` and returns its real result, not an env comparison |
| CONSOLE.4 | `src/lib/admin-policy.ts` and its test are deleted; nothing else in the repository imports them (checked by grep before deletion) |
| CONSOLE.5 | The admin repository's own `tsc --noEmit` and `vitest run` both pass after every change |
| CONSOLE.6 | Login-page copy, the bootstrap-login error message, and the README no longer claim or imply MFA is enforced |

### G. Scope discipline held

| ID | Criterion |
|---|---|
| SCOPE.1 | Migrations `0149`-`0155` and every prior `SAF-*`/`GOA-*`/`CTL-*` record are byte-for-byte untouched |
| SCOPE.2 | `apps/web/app/overlay/canvas/` untouched; `getSubscriberCount()` remains 16 |
| SCOPE.3 | No admin UI (`CTL-04/05/13`), public capability matrix (`CTL-10/11/12`), or widened `0152` change workflow was built |
| SCOPE.4 | No MFA provider, enrolment flow, or recovery-code count was invented — see the task's own "MFA: what is missing, precisely" |
| SCOPE.5 | Migrations `0157`/`0158` (two concurrent agents' own lanes) were never globbed or read for their own content; fixture range `...7000-...70ff` was the only one used, and no shared file was rewritten non-additively |

---

## Commands run

| Command | Result |
|---|---|
| Base fix (`git reset --hard 20e0c36`) | Applied; worktree confirmed at `20e0c36 §20.6.1's emergency kill path, a real owner identity, and the bypass closed` |
| Full SQL suite (`sh packages/db/tests/run-sql-suite.sh`, real `postgres:16-alpine` container, incl. this task's own `adm_admin_registry.sql`) | pass=80 fail=0 (baseline 79/0; +1 new file) |
| `apps/api` route/unit suite (`node --test`; package `@bharatstudio/alerts-api`) | tests 872, pass 872, fail 0 (baseline 865/0; +7, new: `apps/api/test/platform-admin-routes.test.ts`) |
| `apps/web` suite (`node --test`) | tests 644, pass 644, fail 0 (baseline 644/0, unchanged — no web files touched) |
| `apps/api` TypeScript typecheck (`tsc -p tsconfig.json`, run separately) | 0 errors |
| `apps/web` TypeScript typecheck (`tsc -p tsconfig.json`, run separately) | 0 errors |
| `node contracts/validate-fixtures.mjs` | Validated 70 fixtures plus the v1 template catalogue contract (unchanged — no new fixture files required; this surface follows the same precedent `platform-owner`/`emergency-kills` set — staff/governance endpoints in this contract do not carry dedicated fixtures) |
| `node contracts/validate-openapi.mjs` | Validated OpenAPI 3.1 document with 130 paths, 151 operation contracts (baseline 127/148; +3 paths / +3 operations — `setPlatformAdmin`, `listPlatformAdmins`, `getAdminWhoami`) |
| `node contracts/test-openapi-validator.mjs` | Validated 3 negative OpenAPI operation-contract cases (unchanged) |
| `node packages/db/explain-plans/scan-required-queries.mjs` | OK, 32 manifest entries, 13 exemptions (baseline 31; +1: `app_private.staff_list_platform_admins`, not caught by any of the three scan rules — manifested per this task's own instruction, same posture as `staff_list_kill_events` in `CTL-07`) |
| `node packages/db/explain-plans/check-plans.mjs` | OK: 32/32 plans current (baseline 31/31) — `admin-registry-list.explain.md` captured against a real, freshly migrated `postgres:16-alpine` container (all 156 migrations through `0156` applied cleanly), both the wrapped `Function Scan` and the unwrapped listing query's real `EXPLAIN (ANALYZE, BUFFERS)` output |
| `pnpm harness:check` (`node .github/scripts/api-test-harness-check.mjs`) | all checks passed; the new route-test file reaches Fastify only through `buildApp`, never a bare `Fastify()` |
| `pnpm db:test:l03` (`sh packages/db/tests/run-l03-application-behavior.sh` plus its Go/integration steps) | exit 0, all sub-steps passed |
| `pnpm measurement:test` | FAILED (`1 !== 2` in `run_local_measurement.test.mjs`'s "full mode is blocked without external harness" case) — reproduced the documented environmental failure, not chased, per this task's own dispatch instructions |
| `bharatstudio-admin`: `npx tsc --noEmit` | 0 errors |
| `bharatstudio-admin`: `npx vitest run --config vitest.config.ts` | 1 file, 2 tests, 2 passed, 0 failed (unchanged from before this task's changes — `src/lib/admin-policy.test.ts`, the only file that referenced the deleted `admin-policy.ts`, was deleted alongside it, so its removal is not a test-count regression) |

**Not run:** `go test`/`go vet` on the three Go services individually (covered indirectly inside
`pnpm db:test:l03`'s own run, which passed), `pnpm build` (web), Docker image builds, and
`scripts/load/*` self-tests, `playwright test` in `bharatstudio-admin` — none of this task's files
touch Go services, change web build output shape, or touch any Playwright-covered page beyond the
login copy (a text change, not a flow change).

**A note on the fixture range and concurrency.** This task used only UUIDs in `...7000`-`...70ff`
(pre-assigned) and created exactly one new file under `packages/db/migrations/` (`0156`) and one
under `packages/db/tests/` (`adm_admin_registry.sql`), both additive. `packages/db/migrations/` was
never globbed to discover neighbours; `0157`/`0158` (two other agents' own lanes) were not read.
