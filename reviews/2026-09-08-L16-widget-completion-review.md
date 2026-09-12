# L16 widget-overlay completion decision

**Decision state:** `Implemented locally; self-audit remediation recorded 2026-09-09 — independent review and deployed evidence remain open`
**Level:** L2
**Owner:** Project owner / Alerts web
**Scope:** Add only the four missing browser-source pages for `recent_tips`, `top_supporters`, `supporter_ticker`, and `mega_tip_banner`.

## Boundary

The pages consume only the existing authenticated, overlay-session-scoped routes
in `apps/api/src/routes/interactions.ts` and the existing `0108` SQL read
functions. They use the established URL-fragment bearer-token pattern and
polling snapshot model; no new SSE stream, provider call, payment write, user
identity disclosure, or entitlement change is allowed.

## Acceptance and audit

- Every page renders only the already normalised route shape and treats malformed
  or unavailable data as a transparent empty overlay.
- The top-supporters and ticker surfaces never render exact monetary amounts or
  direct account identity; the database response shape excludes both.
- Recent-tips and mega-tip pages show only the consented display data already
  permitted by `0108`.
- Web tests, API tests, disposable SQL proof, TypeScript/build checks, and a
  focused source-boundary audit must pass before the L16 record changes status.

## Risk and rollback

The pages are additive and use no persistence. Removing their routes/pages
returns the product to the prior transparent-unavailable widget behaviour;
payment, alert, queue, and overlay-delivery history are unaffected. This is
self-review only; browser/OBS/staging evidence remains an external gate.

## Execution and self-audit — 2026-09-08

The four pages and their strict response guards were implemented within the
approved boundary. The audit found empty collection shells and missing
transparent widget styling before verification; both were corrected. It also
found a stale API assertion that expected a store-unavailable `503` before an
unauthenticated request was rejected. The test now correctly asserts the
existing fail-closed `401` boundary. An unrelated L17 dashboard test timing
race found by the full web run was corrected before the result below was
recorded.

Redacted reproducible results: API `npm test && npm run build` **396/396**;
web `npm test && npx tsc --noEmit && npm run build` **287/287** plus a
production route list containing all four paths; disposable PostgreSQL
`sh packages/db/tests/run-sql-suite.sh` **44/44** after **110** migrations;
`git diff --check` passed. No provider, production, staging, browser/OBS, or
independent-review claim is made.

## Runtime-composition audit and disposition — 2026-09-09

**Reviewer:** self-review (no independent reviewer was available).
**Scope:** the L16 paid-vote checkout/tally path and the four added protected
widget reads, from SQL adapter through `buildApp` and `index.ts`.

**Finding P1 (fixed):** handler tests injected `PaidSupportVoteStore`,
`PaidVoteOverlayStore`, `VotePaymentTagStore`, and SQL directly, while the
production composition root omitted them. Consequently, the claimed L16
feature was unreachable in a normal API process.

**Disposition:** `apps/api/src/app.ts` now accepts and forwards those
dependencies; `apps/api/src/index.ts` creates the durable SQL-backed adapters;
`apps/api/test/l16-runtime-composition.test.ts` exercises all affected paths
through `buildApp`. Stale comments that asserted the routes were unwired were
also corrected so future audits are not directed to a superseded boundary.

**Reproducible redacted evidence:** API `npm test && npm run build`
**398/398**; web `npm test && npx tsc --noEmit && npm run build` **289/289**
with zero React `act(...)` warnings; disposable PostgreSQL
`sh packages/db/tests/run-sql-suite.sh` **44/44** after **110** migrations;
`git diff --check` passed.

**Remaining release gates:** independent review, staging deployment, real
browser/OBS session, provider/store sandbox, and rollback rehearsal remain
open. No production-readiness claim is made.
