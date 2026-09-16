# TC-QA-HARNESS-01 — the API test harness validates under the API's own AJV options

**Task:** [`../active/tasks/QA-HARNESS-01.md`](../active/tasks/QA-HARNESS-01.md)
**Finding record:** [`../reviews/2026-09-16-api-test-harness-validation-divergence.md`](../reviews/2026-09-16-api-test-harness-validation-divergence.md)
**Owner:** **Sukhdev Singh**
**Date run:** 2026-09-16
**Where:** local worktree of `bharatstudio-alerts` at `317f1ce`, macOS (Darwin 25.5.0), Node 22 via `tsx`, pnpm 10.32.1, fastify 5.12.3
**Result:** `Pass (local only)`

## Scope

Proves that every Fastify instance built under `apps/api/test/` takes its AJV configuration
from the same module `apps/api/src/app.ts` uses, and that a regression is caught automatically.
It proves nothing about any deployed instance.

## AC-1 — one definition, two importers

| | |
|---|---|
| Definition | `apps/api/src/fastify-ajv-options.ts`, exporting `fastifyAjvOptions()` |
| Importer 1 | `apps/api/src/app.ts` (`ajv: fastifyAjvOptions()` inside `buildApp`) |
| Importer 2 | `apps/api/test/create-test-fastify.ts` |
| Copies elsewhere | none — `removeAdditional` occurs in exactly one file under `apps/api/` |

The option value is byte-identical to what `app.ts` carried before the extraction:
`{ customOptions: { removeAdditional: false } }`. **Pass.**

## AC-2 — the sweep

54 construction call sites across 29 test files moved from `Fastify(...)` to
`createTestFastify(...)`. Five of the 54 had previously copied the AJV options inline; those
copies are gone. **Pass.**

## AC-3 — the suite runs green against production validation rules

Three tests failed on the first post-sweep run. All three were **case (a)**: assertions of
harness-only stripped-field behaviour. Each was corrected to production behaviour, with an
in-file comment recording what it used to claim.

| Test | Used to claim | Now asserts |
|---|---|---|
| `apps/api/test/l09-metrics-routes.test.ts` — *"an unknown body field is stripped by Fastify, not rejected"* | `POST /internal/metrics/reconcile` with an extra field returns **503** (body accepted, handler reached, field silently removed) | **400 `FST_ERR_VALIDATION`** — refused at the schema layer; renamed to *"an unknown body field is rejected with 400, not silently stripped"* |
| `apps/api/test/l14-viewer-profile-routes.test.ts` — *"platform claim requires viewer auth, ignores browser identity fields…"* | `POST /v1/viewer/platform-claims` with a browser-injected `providerUserId` returns **201**, the field having been silently dropped | **400 `FST_ERR_VALIDATION`**, and `claimPlatformIdentity` is never called at all. The security property is unchanged and in fact stricter; the status code and the mechanism were wrong |
| `apps/api/test/l23-assist-routes.test.ts` — *"an unrecognised top-level body field is not silently forwarded to the provider seam"* | The request **succeeded** and the provider was called with the stray field stripped | **400 `FST_ERR_VALIDATION`** and the provider seam is never reached; renamed to *"…is rejected, never reaching the provider seam"* |

**No case (b) was found — no route schema was missing a property a real caller sends, and no
route schema was loosened.** Nothing was left failing for a human decision.

`pnpm --filter @bharatstudio/alerts-api test`:

```
ℹ tests 617
ℹ suites 0
ℹ pass 617
ℹ fail 0
ℹ cancelled 0
ℹ skipped 0
ℹ todo 0
```

**Pass.**

## AC-4 — the guard fails on a reintroduced bare `Fastify()`

Negative test: `import Fastify from 'fastify'` and one `const app = Fastify();` reintroduced in
`apps/api/test/reputation-routes.test.ts`, then `pnpm harness:check`:

```
Scanning 77 test file(s) under apps/api/test (excluding the helper itself)
Single AJV definition: apps/api/src/fastify-ajv-options.ts
Importers: apps/api/src/app.ts, apps/api/test/create-test-fastify.ts
Test files referencing createTestFastify: 28
---
  FAIL apps/api/test/reputation-routes.test.ts:3 — default import of 'fastify' (the server factory). A bare `Fastify()` validates with AJV's `removeAdditional: true` default, silently stripping body fields this API rejects with 400. Use `createTestFastify` from ./create-test-fastify.js.
  FAIL apps/api/test/reputation-routes.test.ts:19 — constructs a Fastify instance directly. Every Fastify instance under apps/api/test must come from `createTestFastify` (test/create-test-fastify.ts), which imports the app's own AJV options.

2 violation(s) found. See bharatstudio-requirements/reviews/2026-09-16-api-test-harness-validation-divergence.md.
 ELIFECYCLE  Command failed with exit code 1.
```

Exit status 1. File restored, `pnpm harness:check` re-run:

```
Scanning 77 test file(s) under apps/api/test (excluding the helper itself)
Single AJV definition: apps/api/src/fastify-ajv-options.ts
Importers: apps/api/src/app.ts, apps/api/test/create-test-fastify.ts
Test files referencing createTestFastify: 29
---
honesty: static source-text check over apps/api only. It proves the harness and the app share one AJV configuration in this checkout. It is not a measurement of any deployed instance and is not release, provider or deployment evidence.

API test harness check: all checks passed against current code.
```

Exit status 0. **Pass.**

## AC-5 — nothing else regressed

| Command | Result |
|---|---|
| `pnpm --filter @bharatstudio/alerts-api test` | exit 0 — `ℹ pass 617`, `ℹ fail 0` |
| `pnpm --filter @bharatstudio/alerts-api build` | exit 0 — `tsc -p tsconfig.json`, no diagnostics |
| `pnpm contracts:validate` | exit 0 — `Validated 42 fixtures…`, `Validated OpenAPI 3.1 document with 74 paths, 82 operation contracts…`, `Validated 3 negative OpenAPI operation-contract cases.` |
| `pnpm explain:check` | exit 0 — `OK: every app_private call … is present in required-queries.json (18 manifest entries, 9 exemptions)`, `OK: 18/18 plans current` |
| `pnpm harness:check` | exit 0 — see AC-4 |
| `git diff --check` | exit 0 |

**Pass.**

## Honesty

Local only, one machine, one checkout, the repository's pinned versions. This is not
production, provider, store, legal, device, network or release evidence, and it makes no claim
about what any deployed instance has accepted or rejected. The CI step added to
`node-static-checks` is committed but has never executed on GitHub (`OPS-CI-01` records that
this repository's workflow has never run there).
