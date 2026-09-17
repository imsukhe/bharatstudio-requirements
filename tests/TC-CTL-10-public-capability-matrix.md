# TC-CTL-10 — the public capability matrix: acceptance record

**Date:** 2026-09-17
**Owner:** **Sukhdev Singh**
**Task:** `../active/tasks/CTL-10-public-capability-matrix.md`
**Decision:** `../reviews/2026-09-17-ctl-public-matrix-implementation.md`
**Authority:** `../FULL-PRODUCT-DEFINITION.md` §20.2, §20.4, §20.5, §31 register rows `CTL-10`,
`CTL-11`, `CTL-12`
**Predecessor:** `../reviews/2026-09-17-ctl-registry-spec-alignment-implementation.md` (migration
0153), `../reviews/2026-09-17-ctl-twelve-field-workflow-implementation.md` (migration 0157)

Written to accompany implementation, per `governance/AGENTS.md`. The "Commands run" table is
filled in from actual output against a real `postgres:16-alpine` container and a real `pnpm`
toolchain in this worktree.

---

## Acceptance criteria

### A. CTL-10 — the public read

| ID | Criterion |
|---|---|
| PUB1.1 | `GET /v1/public/capability-matrix` requires no authentication of any kind (no bearer token, no session cookie) |
| PUB1.2 | `app_private.get_public_capability_matrix()` returns exactly seven columns — `capability_id, marketing_label, marketing_blurb, min_tier, is_marketing_section, snapshot_version, published_at` — asserted against `information_schema.parameters`, never `capacity_class`, `limits`, `rollout_percentage`, `kill_switch`, `beta`, `version`, or any audit/channel column |
| PUB1.3 | A capability with `marketing_visible = false` is entirely ABSENT from the response, not merely nulled out |
| PUB1.4 | A capability with `kill_switch = true` is entirely ABSENT even when `marketing_visible = true` (§20.3's "off for everyone, immediately", applied to the marketing surface at publish time) |
| PUB1.5 | Before any snapshot has ever been published, the response is an empty array, never an error |
| PUB1.6 | `bsa_app` has no `SELECT`/`INSERT`/`UPDATE`/`DELETE` grant on `capability_matrix_snapshots` — the function is the only reachable path (CTL-03 posture extended) |
| PUB1.7 | The function itself is revoked from `public`, granted to `bsa_app` — the same posture every other capability-plane function uses; there is no separate "truly public" Postgres role, since an unauthenticated HTTP caller is still served through the API's own `bsa_app` connection |

### B. CTL-10/CTL-11 — a published snapshot, not a live query

| ID | Criterion |
|---|---|
| SNAP1.1 | `capability_matrix_snapshots` rejects `UPDATE` and `DELETE` structurally, for any role (`app_private.reject_table_mutation`, migration 0155's trigger, reused) |
| SNAP1.2 | `app_private.staff_publish_capability_matrix_snapshot` computes a new row from exactly the capabilities where `marketing_visible AND NOT kill_switch`, with a strictly-increasing `version` |
| SNAP1.3 | A registry change made after a publish is invisible on the public read until the NEXT publish (frozen snapshot, not live) |
| SNAP1.4 | Every entry in one response carries the same `snapshotVersion`/`publishedAt`, so a caller can identify which published version it is looking at without a second field |
| SNAP1.5 | `app_private.staff_list_capability_matrix_snapshots` (staff-only) lists every publish, newest first — an internal accountability trail |

### C. CTL-12 — marketing sections, their own field

| ID | Criterion |
|---|---|
| SEC1.1 | `capability_registry.kind`'s own enum does NOT contain `marketing_section` — re-proven after this migration, not merely left alone |
| SEC1.2 | `is_marketing_section` (new boolean column) is the field CTL-12 uses instead |
| SEC1.3 | `capability_registry_row_shape_check` rejects `is_marketing_section = true` with a non-null `capacity_class`, and rejects `is_marketing_section = false` with a null `capacity_class` — probed by a direct `INSERT`, not only through the write functions |
| SEC1.4 | `app_private.staff_create_marketing_section` creates only NEW rows; refuses an existing `capability_key`, whether it names a real capability or an existing marketing section |
| SEC1.5 | `app_private.staff_set_capability_marketing_section` refuses (42501) any row where `is_marketing_section` is false — structurally cannot touch a real capability's governed fields, so it is not a path around migration 0157's two-person workflow |
| SEC1.6 | A marketing-section row is absent from `app_private.resolve_channel_capabilities`'s resolved blob for every channel; an ordinary capability in the same registry still appears |
| SEC1.7 | CTL-14 (capacity_class closed whitelist) re-proven over the relaxed-to-nullable column: the same nine forbidden classes are still rejected on an ordinary (non-section) row |
| SEC1.8 | CTL-15 (no retention/TTL/expiry column) re-proven over this migration's new table and column |

### D. Route layer (`bharatstudio-alerts` `apps/api`)

| ID | Criterion |
|---|---|
| RT1.1 | `GET /v1/public/capability-matrix` has no `preHandler` auth gate; degrades to 503 (never a crash) with no store configured |
| RT1.2 | `POST /v1/admin/capability-matrix/publish` and `GET /v1/admin/capability-matrix/snapshots` require `requirePlatformAdmin` — 401 unauthenticated, 403 non-admin |
| RT1.3 | A webhook failure (thrown error, non-2xx, or no URL configured) never fails the publish response — `webhookAttempted`/`webhookDelivered` are diagnostic fields only |
| RT1.4 | The publish request body requires a non-empty `reason`; an undeclared field is rejected (400) |

### E. Contracts

| ID | Criterion |
|---|---|
| CT1.1 | `contracts/openapi/v1.yaml` declares both routes with `additionalProperties: false` schemas at every level |
| CT1.2 | `contracts/json-schema/public-capability-matrix.schema.json` + fixture prove, by negative test in `validate-fixtures.mjs`, that `capacityClass`/`limits`/`killSwitch`/`rolloutPercentage` are all REJECTED if present on a public matrix entry |

### F. `bharatstudio-marketing` (CTL-11, separate repository, uncommitted)

| ID | Criterion |
|---|---|
| MKT1.1 | `scripts/fetch-capability-matrix.mjs` runs before `next build`; falls back to an empty matrix (never fails the build) when `ALERTS_API_BASE_URL` is unset, unreachable, or returns a malformed body |
| MKT1.2 | No in-repo inbound webhook receiver exists or was added — this repository is a `next export` static site with no server, structurally incapable of one; the real revalidation trigger is documented as a Cloudflare Pages Deploy Hook |
| MKT1.3 | No existing marketing copy (pricing/features pages) was rewired or blanked — the matrix has zero real published rows today |

---

## Commands run (real numbers, this worktree, 2026-09-17)

| Command | Result |
|---|---|
| `sh packages/db/tests/run-sql-suite.sh` | `SQL SUITE: pass=83 fail=0` (baseline 82/0 + `ctl_public_capability_matrix.sql`) |
| `pnpm --filter @bharatstudio/alerts-api test` | `tests 904 pass 904 fail 0` (baseline 891/0 + 13 new route tests) |
| `pnpm --filter @bharatstudio/alerts-web test` | `tests 644 pass 644 fail 0` (unchanged — this task touches no web code) |
| `pnpm --filter @bharatstudio/alerts-api exec tsc -p tsconfig.json --noEmit` | 0 errors |
| `node contracts/validate-fixtures.mjs` | `Validated 78 fixtures plus the v1 template catalogue contract` |
| `node contracts/validate-openapi.mjs` | `Validated OpenAPI 3.1 document with 138 paths, 162 operation contracts` |
| `node contracts/test-openapi-validator.mjs` | `Validated 3 negative OpenAPI operation-contract cases` |
| `node packages/db/explain-plans/scan-required-queries.mjs` | `OK` (33 manifest entries, 13 exemptions) |
| `node packages/db/explain-plans/check-plans.mjs` | `OK: 33/33 plans current` (baseline 32/32 + `public-capability-matrix.explain.md`) |
| `node .github/scripts/api-test-harness-check.mjs` | `all checks passed` |
| `cd bharatstudio-marketing && npm run build` | clean — 32 routes generated, CSP regenerated |
| `cd bharatstudio-marketing && npm run test` | `tests 8 pass 8 fail 0` (unchanged) |

## Disposition

**Conditionally complete.** Self-reviewed only — no independent reviewer was available in this
session. All acceptance criteria above are proven by the SQL test (`packages/db/tests/
ctl_public_capability_matrix.sql`), the route tests (`apps/api/test/public-capability-matrix-
routes.test.ts`, `apps/api/test/capability-matrix-admin-routes.test.ts`), the contracts negative
tests, and the explain-plan artifact. Remaining, explicitly out of scope: adopting the matrix on
live marketing pages (no real published rows exist yet), and a two-person governance workflow for
marketing-section rows (reported as bounded follow-up in migration 0160's own header).
