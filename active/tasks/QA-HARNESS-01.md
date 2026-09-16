# QA-HARNESS-01 — the API test harness must validate under the API's own rules

**Authority:** `FULL-PRODUCT-DEFINITION.md` §19.0 (the §2 pattern), §31.18.0
**Finding record:** [`../../reviews/2026-09-16-api-test-harness-validation-divergence.md`](../../reviews/2026-09-16-api-test-harness-validation-divergence.md)
**Status:** `Conditionally complete — local implementation and verification; independent review unavailable (self-reviewed); the CI step has never executed on GitHub`

| Field | Value |
|---|---|
| **Scope phase** | `v1`; test-infrastructure and CI enforcement. Classified **L2**: no route's runtime behaviour changes, no migration, no Go service, no OpenAPI contract, no `apps/web` file |
| **Owner** | **Sukhdev Singh** |
| **Tier and gate** | All tiers; no release claim. No capability-registry row — this is a build/test gate, not a runtime capability |
| **Personal-data class** | None. No new data field, no new retention rule, no new log line. Every fixture used is synthetic |
| **Provider or legal dependency** | None |
| **Failure behaviour** | A failing `pnpm harness:check` blocks the `node-static-checks` CI job and `pnpm verify:local`. Nothing at runtime depends on it |
| **Kill switch** | Remove the `harness:check` entry from `package.json` and the `harness:check` step from `.github/workflows/ci.yml`. The shared module and the helper are ordinary source files and can stay |
| **Acceptance test** | [`../../tests/TC-QA-HARNESS-01-api-test-harness-configuration.md`](../../tests/TC-QA-HARNESS-01-api-test-harness-configuration.md) |
| **Evidence location** | The acceptance test record above, the `Remediation` section of the finding record, and the files themselves in `bharatstudio-alerts/` |
| **Rollback** | Revert the change. The three new files (`apps/api/src/fastify-ajv-options.ts`, `apps/api/test/create-test-fastify.ts`, `.github/scripts/api-test-harness-check.mjs`) are referenced only by `apps/api/src/app.ts`, the API test files, `package.json` and `ci.yml`; nothing else in the repository reads them |

## Why this exists

`apps/api/src/app.ts` set Fastify's AJV to `removeAdditional: false` inline. Fastify's own
default is `removeAdditional: true`. Under `additionalProperties: false` — the shape nearly
every body schema in this API uses — the two disagree on the commonest validation case there
is: a bare `Fastify()` silently **strips** an undeclared body field and the request succeeds;
this application **rejects** it with `400 FST_ERR_VALIDATION`.

At the point of the sweep, **54 call sites across 29 test files** built their app with a bare
`Fastify()`. The finding record's "50 across 26" was measured three PRF-02 test files earlier,
before commit `317f1ce`; the larger number is drift in the tree, not a correction to the
finding. Five of those call sites had already noticed the problem and **copied** the options
inline — which the finding record correctly names as the same defect with a longer fuse, since
a copy drifts the first time either side changes.

## What this task built

### (a) One definition — `apps/api/src/fastify-ajv-options.ts`

Exports `fastifyAjvOptions()`, returning `{ customOptions: { removeAdditional: false } }`.
**The value is unchanged**; only its location moved. `src/app.ts` calls it; the test helper
calls it. There is no second copy anywhere under `apps/api/`, and the guard fails if one
appears.

Returned fresh per call rather than exported as a shared object literal, so no Fastify
instance can mutate configuration another instance is about to read.

### (b) The helper — `apps/api/test/create-test-fastify.ts`

`createTestFastify(options)` builds a Fastify instance with `ajv` taken from
`fastifyAjvOptions()` — imported, never restated — and passes every other server option
through. `ajv` is deliberately not overridable.

Named `createTestFastify` and not `buildTestApp` because nineteen test files already define
their own local `buildTestApp(...)` wrapper; a shared import of that name shadowed into
infinite recursion (`RangeError: Maximum call stack size exceeded`). That was caught by running
the suite, not by reading it.

### (c) The sweep — 54 call sites, 29 files

Every `Fastify()` and every inline `Fastify({ ajv: … })` under `apps/api/test/` now goes
through the helper. Comments that described the old bare-`Fastify()` arrangement were rewritten
rather than left to mislead the next reader.

Three tests then failed, all of them **asserting harness-only behaviour**; each assertion was
corrected to match production, and each correction carries an in-file comment saying what the
test used to claim. No route schema was loosened. Details and exact outputs are in the
acceptance test record.

### (d) The guard — `.github/scripts/api-test-harness-check.mjs` (`pnpm harness:check`)

Wired exactly like the repository's existing static checks (`canvas-static-check.mjs`,
`budget-gate-check.mjs`): a `.github/scripts/*.mjs` file, a root `package.json` script, a named
step in the existing `node-static-checks` CI job, and a place in `pnpm verify:local`. No new
CI job and no new convention were invented.

It fails if any file under `apps/api/test/` can reach the Fastify factory (default import,
namespace import, a named `fastify`/`default` specifier, `import('fastify')`,
`require('fastify')`, or a `Fastify(`-shaped construction in code), if `removeAdditional` is
restated anywhere under `apps/api/` outside the one module, if either importer stops importing
or calling `fastifyAjvOptions()`, or if the check would pass vacuously (helper unused, test
directory missing or empty).

## Boundaries — what this task did NOT do

- No route schema was loosened, and nothing was changed to make a test pass.
- No migration, no Go service, no OpenAPI contract, no `apps/web` file was touched.
- `bodyLimit: 64 * 1024` remains an `app.ts`-only option and is **not** shared with the helper.
  A route test needing a body-size boundary must pass it explicitly. This is a known,
  deliberate, remaining divergence between the harness and the server — much narrower than the
  AJV one, and outside this task's scope. Recorded here rather than left unmentioned.
- The guard's coverage stops at `apps/api/test/`. `apps/web` has its own test conventions and
  no Fastify.
- The CI step is committed, not executed. Per `OPS-CI-01`, this repository's workflow has never
  run on GitHub; a committed step is not a step that has passed there.

## Honesty

Every result recorded under this task is a local run on one machine at the repository's pinned
versions. None of it is production, provider, store, legal, device, network or release
readiness, and no claim is made about what any deployed instance has actually accepted or
rejected.
