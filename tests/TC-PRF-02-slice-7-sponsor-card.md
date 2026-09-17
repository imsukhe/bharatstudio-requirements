# TC-PRF-02 slice 7 — Sponsor Card (§6 #11): acceptance record

**Date:** 2026-09-17
**Owner:** **Sukhdev Singh**
**Task:** `../active/tasks/PRF-02-slice-7-sponsor-card.md`
**Decision:** `../reviews/2026-09-17-prf-02-slice-7-sponsor-card-implementation.md`
**Binding owner decision:** `../reviews/2026-09-17-remaining-eight-modules-and-youtube-v1-amendment.md` Part 1 §3

Written **before** implementation, per `governance/AGENTS.md`. The "Commands run" table is filled
in after the run, from actual output, and is the single place this slice's numbers live.

---

## Acceptance criteria

### A. The schema and creator write path (`packages/db/migrations/0145_v1_prf02_sponsor_card.sql`)

| ID | Criterion |
|---|---|
| SP11.1 | An owner or admin can set a sponsor name, enable/disable the card, and (optionally) a schedule window — recorded as one row per channel |
| SP11.2 | A non-owner/admin cannot write it — `42501`, nothing changed |
| SP11.3 | A sponsor name outside 1–120 characters is refused (`22023`) — the bound reused from migration `0109` line 67 |
| SP11.4 | Calling the write function twice **upserts** the same row (one card per channel), never creates a second row |
| SP11.5 | A schedule with only one of the two instants set is refused (`22023`) — both or neither |
| SP11.6 | A schedule whose end is not after its start is refused (`22023`) |
| SP11.7 | Logo metadata (content sha256, mime type, byte size) may be set to all-null or all-non-null only; a partial set is refused (`22023`) |
| SP11.8 | A malformed sha256 (not 64 lowercase hex characters) is refused (`22023`) |
| SP11.9 | The logo storage key is **generated**, never independently writable, and equals `channel_id || '/' || logo_content_sha256` — proof that the tenant-scoped content-addressed shape (§19.1) holds by construction |

### B. No tier gate beyond the existing module cap

| ID | Criterion |
|---|---|
| SP11.10 | `sponsor_card` is already one of migration `0131`'s twenty catalogue keys; this migration adds no key and alters no constraint |
| SP11.11 | No function in this migration reads a tier or calls an entitlement function — storing, viewing and changing a durable creator record is never tier-gated (§12.6) |

### C. The overlay read — three fields, enabled- and schedule-gated, and the no-counter proof

| ID | Criterion |
|---|---|
| SP11.12 | A valid overlay session on a channel with `enabled = true` and no schedule returns exactly one row of `{sponsor_name, logo_mime_type, logo_storage_key}` |
| SP11.13 | **The returned column set is exactly those three fields** — asserted from `pg_get_function_result` AND from a table materialised out of a live call, read back through `information_schema.columns` |
| SP11.14 | `enabled = false` returns zero rows even with a perfectly valid token |
| SP11.15 | Outside the schedule window, a card with a schedule set returns zero rows; inside the window it returns one row |
| SP11.16 | A card with no schedule set (both instants null) always returns a row while enabled, regardless of time |
| SP11.17 | A bad, foreign, expired or revoked overlay token returns zero rows |
| SP11.18 | **Structural proof no counter exists.** Every function this migration ships is scanned (`pg_get_functiondef`) for `count`, `impression`, `exposure`, `views`, `shown_at`, `displayed_at`, `duration` — none may appear. `public.sponsor_cards`' own columns are scanned via `information_schema.columns` for the same tokens plus `%last_shown%`/`%last_display%` — none may exist. This is the test a future edit cannot get past by only touching a comment |
| SP11.19 | No column on `public.sponsor_cards` is a `bytea` — asserted against `information_schema.columns` (`udt_name <> 'bytea'` for every column), proving the logo is metadata-only per §19.1 |

### D. API routes

| ID | Criterion |
|---|---|
| SP11.20 | `GET /v1/overlay-widgets/:overlayId/sponsor-card` with no bearer token is 401; with a token and no store is a retryable 503 |
| SP11.21 | A store answer is narrowed a SECOND time by `projectOverlaySponsorCard` in the route layer — a field the projection does not declare never reaches the response body even if a rogue store handed it up |
| SP11.22 | `GET /v1/channels/:channelId/sponsor-card` (creator session) returns the full row or `null` |
| SP11.23 | `PUT /v1/channels/:channelId/sponsor-card` (creator session) upserts and returns the row; a non-owner/admin channel is 404 (never a leaking 403) |
| SP11.24 | The request body schema's `additionalProperties: false` rejects any field named `impression`, `exposure`, `count`, `views`, `shownAt` or `displayedAt` with a 400 before the store is ever called |

### E. Canvas module

| ID | Criterion |
|---|---|
| SP11.25 | The module renders nothing until a real, non-null snapshot lands |
| SP11.26 | The module's option/state types carry no field for a URL, script, iframe or stylesheet (§9.1.1) — checked at compile time |
| SP11.27 | The module never calls any counting, timing or accumulation function — grepped in the test file itself |

---

## Commands run

| Command | Result |
|---|---|
| Full SQL suite (`sh packages/db/tests/run-sql-suite.sh`, all 68 files incl. this slice's own) | pass=68 fail=0 |
| `apps/api` route/unit suite (`tsx --test 'test/**/*.test.ts'`, real command; package is named `@bharatstudio/alerts-api` in this checkout, not `@bharatstudio/api`) | tests 707, pass 707, fail 0 (15 of which are this slice's own route tests) |
| `apps/web` suite (`tsx --test ... 'app/**/*.test.ts' 'app/**/*.test.tsx'`; package is named `@bharatstudio/alerts-web`, not `@bharatstudio/web`) | tests 578, pass 578, fail 0 (18 of which are this slice's own canvas-module tests) |
| `apps/api` TypeScript typecheck (`tsc -p tsconfig.json --noEmit`, separate from the test runner) | 0 errors |
| `apps/web` TypeScript typecheck (`tsc -p tsconfig.json`, `noEmit: true` already in tsconfig) | 0 errors |
| `node contracts/validate-fixtures.mjs` | Validated 52 fixtures plus the v1 template catalogue contract |
| `node contracts/validate-openapi.mjs` | Validated OpenAPI 3.1 document with 90 paths, 103 operation contracts |
| `node contracts/test-openapi-validator.mjs` | Validated 3 negative OpenAPI operation-contract cases |
| `node packages/db/explain-plans/scan-required-queries.mjs` | OK, 22 manifest entries, 9 exemptions |
| `node packages/db/explain-plans/check-plans.mjs` | OK: 22/22 plans current |
| `pnpm harness:check` (`node .github/scripts/api-test-harness-check.mjs`) | all checks passed |

Not run: `go test`/`go vet` on the three Go services, `pnpm build`, and Docker image builds — none of this slice's files touch Go services or change build output shape, and the full `verify:local` chain (which also runs load/fault self-tests) was judged out of proportion to a schema-and-two-endpoints slice. Flagged here rather than silently skipped.
