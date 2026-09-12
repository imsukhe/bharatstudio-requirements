# Alerts local residual-gates review

**Decision state:** `Local audit complete; remaining items require an authority, provider, connector, asset-pipeline, or model-data decision`
**Date:** 2026-09-08

## L18 — memberships

The active launch authority excludes YouTube channel/data/live/membership
work. No live L15 membership connector or verified source-event contract is
available, so creating period rows from guessed event fields would be unsafe.
Native recurring remains explicitly v2 and requires dated provider pricing
evidence. Local implementation is therefore not started.

## L19 — provider capability snapshots and rails

The interface reports Razorpay's repository-evidenced `supportsRefunds: false`;
there is no trusted provider refresh adapter, refund initiation/status API, or
Razorpay OAuth credential flow to populate a durable snapshot. A snapshot
schema without a freshness policy, trusted writer, and real provider source
would create false entitlement evidence, so it is not inserted merely to
satisfy a table name. The hosted checkout contract currently exposes no
verified supported parameter to lead with a locally remembered UPI app; a
browser selector that cannot affect checkout is rejected as misleading.
Paytm/Cashfree/PhonePe remain blocked on written provider conditions.

## L20 and L22 creator packs

Central PENDING-04 defers the 359 missing runtime template packages and
forbids mass-generated/placeholder imports. The existing structural Lottie
validation is not malware scanning, asset attestation, Studio review, or
takedown operations. Implementing quotas/moderation without the approved
storage/scanner/retention design would be incomplete; the L22 curated-only
slice is recorded separately.

## L23 — bounded AI

No approved model/provider, data-classification and retention policy,
redaction contract, cost ceiling, or human-confirmation audit schema exists.
Because the task covers creator text/configuration and must not directly alter
financial/challenge state, a generic model call or local mock would not be
an implementation. It remains definition-gated.

## Final local evidence

The complete local test pass after the recorded corrections was: API
`npm test && npm run build` **398/398**; web `npm test && npx tsc --noEmit &&
npm run build` **289/289** with zero React `act(...)` warnings; disposable PostgreSQL
`sh packages/db/tests/run-sql-suite.sh` **44/44** after **110** migrations;
`git diff --check` passed. This does not assert provider, legal, staging,
deployment, browser/OBS, sandbox refund, or independent-review evidence.

## Dependency-audit correction — 2026-09-09

**Reviewer:** self-review (no independent reviewer was available).

The first package-manager production audit found vulnerable transitive
`fast-uri` packages, a vulnerable direct Fastify release, a vulnerable direct
Ajv release, and then a patched-Next transitive `sharp` release. These were
locally actionable supply-chain findings, so they were corrected before this
review was closed:

- Fastify is pinned to `5.12.3`; Ajv is pinned to `8.20.0`; Next.js is pinned
  to `16.3.3`.
- The root pnpm overrides force `fast-uri@^3.0.1` to `3.1.6`,
  `fast-uri@^4.0.0` to `4.1.3`, and Next's transitive `sharp` to `0.35.4`.
- `pnpm install --lockfile-only` followed by `pnpm install --frozen-lockfile`
  regenerated and installed the reviewed lock state. `pnpm why -r sharp`
  reports only `sharp@0.35.4` below Next.js.

**Reproducible redacted evidence:** from the Alerts repository root,
`pnpm audit --prod --audit-level=low` and `pnpm audit --audit-level=low` both
reported `No known vulnerabilities found`. The dependency-installed full
verification passed: API `npm test && npm run build` **398/398**; web
`npm test && npx tsc --noEmit && npm run build` **289/289** (zero React
`act(...)` warnings); disposable PostgreSQL
`sh packages/db/tests/run-sql-suite.sh` **44/44** after **110** migrations;
and `git diff --check` passed.

The install reports a deprecated `node-domexception` subdependency and pnpm's
standard ignored-build-script notice for `esbuild`; neither is an audit
vulnerability, and neither has been silently allowlisted. The release gates
above remain open; this evidence is a local dependency and regression check,
not a production-readiness assertion.
