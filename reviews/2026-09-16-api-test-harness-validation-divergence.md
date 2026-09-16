# The API test harness validates under different rules than the API

**Date:** 2026-09-16
**Owner:** Sukhdev Singh
**Authority:** `FULL-PRODUCT-DEFINITION.md` §19.0 (the §2 pattern), §31.18.0
**Status:** Found, proven, and **remediated 2026-09-16** — see the Remediation section at
the end of this record. The sweep and the guard that were held open when this was first
written are now done and locally verified. The statement that they were "not yet done"
described this record's state on the morning of 2026-09-16 and no longer describes the
tree; it is preserved below, marked, in the "Outstanding" heading rather than deleted,
because the finding's argument depends on knowing what was open when it was written.
**Task:** [`../active/tasks/QA-HARNESS-01.md`](../active/tasks/QA-HARNESS-01.md) ·
**Acceptance test:** [`../tests/TC-QA-HARNESS-01-api-test-harness-configuration.md`](../tests/TC-QA-HARNESS-01-api-test-harness-configuration.md)

## The finding

`apps/api/src/app.ts:205` configures Fastify's AJV with `removeAdditional: false`.
Twenty-six test files under `apps/api/test/` build their app with a bare `Fastify()`,
whose AJV default is `removeAdditional: true`. Fifty call sites in total.

The two configurations disagree on the single most common validation case in this API —
a body schema with `additionalProperties: false` receiving an undeclared field:

| Harness | Result |
|---|---|
| bare `Fastify()` (26 test files) | `status=200`, the field is silently **stripped** before the handler runs |
| `app.ts` config (production) | `status=400`, `FST_ERR_VALIDATION`, the request is **rejected** |

Measured directly, both branches in one script, not inferred.

## Why this matters more than a test-config nit

**A route test that sends an undeclared field and asserts success passes for a reason
that does not exist in production.** The same request against the running API is a 400.
The test is not weakly proving the right thing; it is confidently proving the wrong
thing, and it will keep doing so as the route changes underneath it.

It is the §2 pattern once more, inverted: not code no one can reach, but a check that
exercises a configuration no one runs.

## A correction to a claim I made earlier, which was wrong

`apps/api/src/routes/metrics.ts` carried this, written by me:

> "That did NOT break the scheduler — Fastify configures AJV with `removeAdditional: true`,
> so `additionalProperties: false` silently STRIPS an unknown field instead of rejecting
> it, and `window` would simply have vanished before the handler ran (proven in
> `test/l09-metrics-routes.test.ts`)."

Every clause after the dash is wrong. This app sets `removeAdditional: false`. An
undeclared field is **rejected**, not stripped. `l09-metrics-routes.test.ts` builds a
bare `Fastify()` at five call sites, so what it proved was the harness's default, not
this application's behaviour.

The practical inversion matters: I recorded declaring `window` on
`/internal/metrics/reconcile` as good hygiene over a harmless situation. It was not
harmless. Before that change, the `reliability-reconciliation` schedule — which sends
`{ idempotencyKey, window }` — would have been **rejected with 400 on every run** in a
deployment. The fix was load-bearing and I wrote it up as optional politeness.

The route's current schema declares `window`, so there is no live defect on this route
today. What was defective was the reasoning, and the reasoning is what the next person
reads.

## Outstanding, not done *(as written on the morning of 2026-09-16 — all four items are now done; see Remediation)*

1. **A shared harness that cannot drift.** The AJV options should live in one module that
   both `app.ts` and the test helper import, so the two can never disagree again. A
   helper that merely copies the options today is the same failure with a longer fuse.
2. **The sweep:** 50 bare `Fastify()` call sites across 26 files moved onto it.
3. **A guard**, so the next test file cannot reintroduce a bare `Fastify()` for route
   validation. Without it this recurs, which is the whole lesson of §19.0.
4. **Re-run every route test after the sweep.** Some assertions currently passing may be
   asserting stripped-field behaviour; those are findings, not breakage, and each must be
   read rather than force-fixed.

## What this evidence is not

Local only. The measurement is of Fastify and AJV behaviour on this machine at these
pinned versions. It is not production, provider, deployment or release evidence, and no
claim is made here about what any deployed instance has actually rejected or accepted.

---

# Remediation — 2026-09-16

**Owner:** **Sukhdev Singh**
**Task:** [`../active/tasks/QA-HARNESS-01.md`](../active/tasks/QA-HARNESS-01.md)
**Acceptance test:** [`../tests/TC-QA-HARNESS-01-api-test-harness-configuration.md`](../tests/TC-QA-HARNESS-01-api-test-harness-configuration.md)
**Repository state:** `bharatstudio-alerts` at `317f1ce`; worktree left uncommitted by
instruction.

All four outstanding items above are done. Taken in order:

## 1. A shared harness that cannot drift — done

`apps/api/src/fastify-ajv-options.ts` is now the single definition:

```ts
export function fastifyAjvOptions(): NonNullable<FastifyServerOptions['ajv']> {
  return { customOptions: { removeAdditional: false } };
}
```

`apps/api/src/app.ts` imports and calls it in `buildApp`; `apps/api/test/create-test-fastify.ts`
imports and calls the same function. **The option value did not change** — production
behaviour after the extraction is byte-identical, only the location moved. It returns a fresh
object per call so no Fastify instance can mutate configuration another is about to read.

This record's own warning that "a helper that merely copies the options today is the same
failure with a longer fuse" was not hypothetical: **five of the call sites had already copied
them inline** (`prf02-stream-mission-routes`, `l16b-public-vote-payment-tag`,
`l15-tipintent-public-routes`, `billing-payment-method-routes`,
`l19c-payment-provider-live-wiring`). Those copies are gone, and the guard in item 3 fails if
another appears.

## 2 & 3. The sweep and the guard — done

**Sweep: 54 construction call sites across 29 test files.** This record said "50 across 26";
that count was correct when measured, three PRF-02 test files before `317f1ce` landed. The
larger number is drift in the tree, not a correction to the finding.

The helper is exported as `createTestFastify`, not `buildTestApp`: nineteen test files already
define their own local `buildTestApp(...)` wrapper, and a shared import of that name shadowed
into `RangeError: Maximum call stack size exceeded`. Found by running the suite, not by reading
it — worth recording because the collision is invisible to inspection.

**Guard:** `.github/scripts/api-test-harness-check.mjs`, run as `pnpm harness:check`, wired as
a named step in the existing `node-static-checks` CI job and added to `pnpm verify:local` —
the same shape as `canvas-static-check.mjs` and `budget-gate-check.mjs`. No new job, no new
convention.

It fails if any file under `apps/api/test/` can reach the Fastify factory at all (default
import, namespace import, a named `fastify`/`default` specifier, `import('fastify')`,
`require('fastify')`, or a `Fastify(`-shaped construction in code, with comments and string
literals stripped first); if `removeAdditional` is restated anywhere under `apps/api/` outside
the one module; if either importer stops importing or calling `fastifyAjvOptions()`; or if it
would pass vacuously — helper unused, test directory missing or empty. A check that passes
because it found nothing to check is not a passing check.

Negative test, a bare `Fastify()` reintroduced in `apps/api/test/reputation-routes.test.ts`:

```
  FAIL apps/api/test/reputation-routes.test.ts:3 — default import of 'fastify' (the server factory). A bare `Fastify()` validates with AJV's `removeAdditional: true` default, silently stripping body fields this API rejects with 400. Use `createTestFastify` from ./create-test-fastify.js.
  FAIL apps/api/test/reputation-routes.test.ts:19 — constructs a Fastify instance directly. Every Fastify instance under apps/api/test must come from `createTestFastify` (test/create-test-fastify.ts), which imports the app's own AJV options.

2 violation(s) found.
```

Exit status 1. Restored, re-run: `API test harness check: all checks passed against current
code.`, exit status 0.

## 4. Re-run every route test after the sweep — done, three findings

Three tests failed on the first post-sweep run. **All three were case (a): assertions of
harness-only stripped-field behaviour, now correctly failing.** Each was corrected to match
production, and each correction carries an in-file comment recording what the test used to
claim, so the next reader sees the inversion rather than a clean-looking assertion.

| Test | What it used to claim | What it asserts now |
|---|---|---|
| `l09-metrics-routes.test.ts` — *"an unknown body field is stripped by Fastify, not rejected"* | `POST /internal/metrics/reconcile` with an extra field returns **503**: body accepted, handler reached, field silently removed | **400 `FST_ERR_VALIDATION`**. Renamed *"an unknown body field is rejected with 400, not silently stripped"* |
| `l14-viewer-profile-routes.test.ts` — *"platform claim requires viewer auth, ignores browser identity fields…"* | `POST /v1/viewer/platform-claims` carrying a browser-injected `providerUserId` returns **201**, the field silently dropped | **400 `FST_ERR_VALIDATION`**, and `claimPlatformIdentity` is never called |
| `l23-assist-routes.test.ts` — *"an unrecognised top-level body field is not silently forwarded to the provider seam"* | The request **succeeded** and the provider was invoked with the stray field stripped | **400 `FST_ERR_VALIDATION`**, provider seam never reached. Renamed *"…is rejected, never reaching the provider seam"* |

The `l14` one is the sharpest instance of this record's thesis. It is a **security** test — it
exists to prove an attacker cannot inject `providerUserId` — and it was passing by asserting
`201`, that is, by asserting the API *accepted* the attacker's field and quietly discarded it.
The real API refuses the request outright. The property the test protects still holds, and
holds more strictly than the test claimed; what was wrong was the mechanism and the status
code, which is exactly the reasoning a future reader would have inherited.

**No case (b) was found.** No route schema was missing a property a real caller sends. **No
route schema was loosened, and nothing was changed merely to make a test pass.** Nothing was
left failing for a human decision.

## Verification (exact result lines)

| Command | Result |
|---|---|
| `pnpm --filter @bharatstudio/alerts-api test` | exit 0 — `ℹ tests 617`, `ℹ pass 617`, `ℹ fail 0`, `ℹ cancelled 0`, `ℹ skipped 0`, `ℹ todo 0` |
| `pnpm --filter @bharatstudio/alerts-api build` | exit 0 — `tsc -p tsconfig.json`, no diagnostics emitted |
| `pnpm contracts:validate` | exit 0 — `Validated 42 fixtures plus the v1 template catalogue contract with Draft 2020-12, format enforcement and v1 capability exclusion (including invalid-UUID rejection).`; `Validated OpenAPI 3.1 document with 74 paths, 82 operation contracts, and all local $ref targets.`; `Validated 3 negative OpenAPI operation-contract cases.` |
| `pnpm explain:check` | exit 0 — `OK: every app_private call found by rule 1 (convention scan), rule 2 (overlay-store-file scan) and rule 3 (composition-root derived-read scan, 11 wired declaration(s) resolved and scanned) is present in required-queries.json (18 manifest entries, 9 exemptions)`; `OK: 18/18 plans current` |
| `pnpm harness:check` | exit 0 — `API test harness check: all checks passed against current code.` |

## Scope respected, and one divergence deliberately left open

No migration, no Go service, no OpenAPI contract and no `apps/web` file was touched. No route's
runtime behaviour changed.

Left open on purpose: `bodyLimit: 64 * 1024` is still an `app.ts`-only option and is **not**
shared with the test helper, so a route test does not inherit the server's body-size boundary
unless it passes one. That is a second, much narrower harness/server divergence of the same
family as this finding. It is recorded here rather than silently fixed or silently ignored, and
it is outside QA-HARNESS-01's scope.

## What this evidence is not

Unchanged from the section above, and it applies to the remediation too. Local only, one
machine, one checkout, the repository's pinned Fastify/AJV versions. It is not production,
provider, store, legal, device, network or release readiness, and no claim is made about what
any deployed instance has actually rejected or accepted. The CI step is committed, not
executed: per `OPS-CI-01`, this repository's workflow has never run on GitHub, and a committed
step is not a step that has passed there. The worktree was left uncommitted by instruction.


## Second divergence in the same family, 2026-09-16 — `bodyLimit`

The AJV fix did **not** close this family, and that is the useful finding. `app.ts` set
`bodyLimit: 64 * 1024` inline while the harness took Fastify's own 1 MiB default. Measured,
both branches: a 200 KB body is `200 OK` under the default and `413` under the server's value.
Every test migrated onto the new helper kept inheriting the looser limit, because the helper
shared the AJV options and nothing else.

**The lesson is that this bug is per-option.** Fixing one shared setting says nothing about the
next one; only a guard that enumerates them does. `FASTIFY_BODY_LIMIT_BYTES` now has one
definition, both importers are required to *use* it rather than merely import it, and
route-level limits stay where they belong — a route that legitimately accepts more names its own
constant, which the guard permits while forbidding a numeric literal.

**A guard rule of mine was wrong first, and running it is what found that.** Requiring the
constant to "appear" in each importer passed when the helper imported it and stopped using it: an
import line is a mention, not a use. The AJV rule gets this right for free by requiring a *call*;
a constant has no call, so the check now strips import statements before looking. Both negative
tests then failed as they should, and each file was restored byte-identical.

Evidence: `bharatstudio-alerts` `4dac1aa`. `api 617/0`, `tsc` clean, `harness:check` passes; no
test depended on the looser limit.
