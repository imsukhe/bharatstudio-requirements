# Review — ADM-07 admin bootstrap seed implementation (migration 0159)

**Date:** 2026-09-17
**Owner:** Sukhdev Singh
**Reviewer:** self-review only — independent fresh review was not available in this run; per
governance policy this task is left `Conditionally complete`, not `Verified`, pending that review.
**Scope:** migration `0159` (`app_private.staff_bootstrap_platform_admin()`), `packages/db/tests/
adm_bootstrap_seed.sql`.

## Base

Worktree fast-forwarded to `f9ebccf` (`GOA trigger engine spine: interlocks that cannot be switched
off`) before any work, per the base-fix instruction. Confirmed via `git log --oneline -1`.

## Finding, and disposition

Confirmed the problem as stated in the owner decision record and in `0156`'s own header: the
empty-registry lockout is real and predates `0156`. Built a single additive function,
`app_private.staff_bootstrap_platform_admin()`, in a new migration file (`0159`). No existing
migration file was modified. No `apps/api` file, route, or config was touched — the owner decision's
"if none is needed, do not invent one" is satisfied by inventing none; the seed is reachable only
through direct database access (same posture the migration itself requires to apply).

## Deviation from the most literal reading of "deployment-provided value" — stated, not buried

The task brief did not name a mechanism, only that the value must be "configured but unset" and
must reuse the console's own existing identity shape rather than invent one. Two candidate
mechanisms existed:

1. An `apps/api` environment variable, read at Fastify boot and passed into the DB call.
2. A Postgres custom GUC (`current_setting('app.bootstrap_admin_email', true)`), set at the database/
   deployment level, read only by the migration/function itself.

This implementation chose (2). Reasoning: this codebase already has a live, load-bearing convention
for exactly this shape of value — `app.user_id`, `app.channel_id`, `app.overlay_session_id`
(migration `0002`) and `app.viewer_id` (migration `0084`) are all custom GUCs read via
`current_setting(..., true)`, all previously request-scoped. Using the same convention at deployment
scope avoids inventing a new configuration-loading mechanism in `apps/api`, keeps the entire feature
one self-contained SQL migration, and keeps it structurally unreachable from the API layer (an env
var read by Fastify would need to travel through application code to reach the database, widening
the surface for no benefit — the seed is a database bootstrap action, not a user-facing one). This is
a judgement call, not a decision found verbatim in the owner record; flagged here for review rather
than presented as the only possible reading.

## Identity shape — reused, not invented

Matched against `public.app_users.email`/`email_verified`, the column the Google exchange already
populates (`apps/api/src/auth/google.ts` → `app_private.create_user_session`, migration `0075`),
normalised identically (`trim().toLowerCase()`) and gated on `email_verified = true`, mirroring
`0075`'s own "an unverified claim never overwrites a verified one" trust bar. `external_subject`
(the Google `sub`) was considered and rejected as the match key: it is opaque and unknowable to a
deployment operator before the intended admin has ever signed in, whereas the operator can
reasonably know the person's email address in advance. This is the reasoning the task brief pointed
at ("look at how a user is identified there and reuse it") rather than a free invention.

## Hard constraints — checked explicitly

- No hardcoded email, no default identity, no invented session lifetime — `current_setting(...,
  true)` returns `NULL` when unset; no fallback value appears anywhere in the migration.
- `app_private.is_platform_admin()` (`0073`) not modified — confirmed by diff (this migration
  contains no `create or replace function app_private.is_platform_admin` statement) and by the SQL
  test calling it directly against the newly-seeded row.
- `0149`-`0158` guards preserved — confirmed by running the FULL SQL suite (83/83 pass), including
  `adm_admin_registry.sql` (`0156`'s own suite, unmodified) and `ctl_emergency_kill_and_owner.sql`
  (`0155`'s), both still green, plus this task's own representative-function checks across `0149`,
  `0151`, `0153`, `0155`, `0156`.
- `apps/web/app/overlay/canvas/` untouched — `git diff --stat` against `f9ebccf` confirms the only
  files added are `packages/db/migrations/0159_v1_adm_bootstrap_seed.sql` and `packages/db/tests/
  adm_bootstrap_seed.sql` (plus this staged governance set).
- No MFA built or implied — this task adds no console-facing copy of any kind.
- Route tests use `createTestFastify()` — not applicable; no route was added.

## Verification — real numbers

- `sh packages/db/tests/run-sql-suite.sh` (all 159 migrations, all test files, isolated clones):
  **83 pass / 0 fail** (baseline was 82/0; +1 for `adm_bootstrap_seed.sql`).
- `pnpm contracts:validate`: pass (77 fixtures + template catalogue, OpenAPI 3.1 with 135 paths/159
  operations, 3 negative cases) — unaffected, as expected (no contract/fixture file touched).
- `pnpm explain:check`: **32/32 plans current**, matching baseline exactly — no new overlay-facing
  read was added, so no new explain-plan artifact was required.
- `pnpm harness:check`: pass ("all checks passed against current code").
- `apps/api` test suite (`pnpm test` in `apps/api`): **891 pass / 0 fail**, matching baseline exactly.
- `apps/web` test suite (`pnpm test` in `apps/web`): **644 pass / 0 fail**, matching baseline exactly.
- Typecheck, run separately per the task's instruction: `tsc --noEmit` in `apps/api`
  (`tsconfig.json`) — 0 errors. `tsc --noEmit` in `apps/web` (`tsconfig.json`) — 0 errors. (No root
  `typecheck` script exists in this repository; both app-level `tsc` invocations were run directly
  since neither app's TypeScript was touched by this task.)
- `measurement:test` was not run — the task's own baseline note records it as failing
  environmentally in agent sandboxes and passing on `main`; not chased, per instruction.

## Disposition

`Conditionally complete`: implementation and its own tests are green against real baseline numbers,
but no independent fresh review has occurred. Governance records written to
`.governance-staging/` inside the worktree (`/Users/sukhdevsingh/Workspace/Bharat Studio/
bharatstudio-alerts/.claude/worktrees/agent-a9abc6bd71c094de3/.governance-staging/`) because the
sandbox refused a direct write to the `bharatstudio-requirements` checkout ("Edit the worktree copy
of this file instead of the shared-checkout path") — matching the task brief's own contingency,
which records a previous lane hitting the identical restriction. The coordinator should copy
`.governance-staging/active/tasks/ADM-07-bootstrap-seed.md`, `.governance-staging/tests/
TC-ADM-07-bootstrap-seed.md`, and this file into their corresponding `active/tasks/`, `tests/`, and
`reviews/` paths in the real `bharatstudio-requirements` checkout.
