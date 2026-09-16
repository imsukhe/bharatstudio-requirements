# The API test harness validates under different rules than the API

**Date:** 2026-09-16
**Owner:** Sukhdev Singh
**Authority:** `FULL-PRODUCT-DEFINITION.md` §19.0 (the §2 pattern), §31.18.0
**Status:** Found and proven. Comment corrected; the 26-file sweep and the guard that
would prevent recurrence are **not yet done** — they were deliberately held because
another agent was writing to the same tree, and a sweep measured against a moving tree
is void.

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

## Outstanding, not done

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
