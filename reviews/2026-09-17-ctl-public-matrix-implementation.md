# CTL-10/CTL-11/CTL-12 — public capability matrix implementation record

**Date:** 2026-09-17
**Owner:** **Sukhdev Singh**
**Authority:** `../FULL-PRODUCT-DEFINITION.md` §20.2, §20.4, §20.5, §31 register rows `CTL-10`,
`CTL-11`, `CTL-12` — read in full before writing migration 0160, per this task's own instruction.
**Task:** `../active/tasks/CTL-10-public-capability-matrix.md`
**Acceptance:** `../tests/TC-CTL-10-public-capability-matrix.md`
**Unblocked by:** `2026-09-17-three-owner-decisions-goa17-marketing-bootstrap.md` §2
**Predecessor:** `2026-09-17-ctl-phase-1-implementation.md` (0149), `2026-09-17-ctl-registry-spec-
alignment-implementation.md` (0153, the migration that first reported the `marketing_section`
blocker), `2026-09-17-ctl-twelve-field-workflow-implementation.md` (0157)

---

## What this slice is, in one paragraph

Three register rows blocked since migration 0153 on one open modeling question (does a marketing
page-region flag belong in `kind`'s enum) are now buildable, because the owner decision above
settled it: a marketing section is not a capability and gets its own field. Migration 0160 adds
that field (`is_marketing_section`), the append-only published-snapshot mechanism CTL-10/CTL-11
need, the public unauthenticated read, and the route/store/contract layer above it — in
`bharatstudio-alerts` — plus a build-time fetch script and typed loader in the separate
`bharatstudio-marketing` repository (uncommitted, reported below) for CTL-11's other half.

## The structural problem `is_marketing_section` created, and how it was resolved

`capability_registry.capacity_class` (migration 0149) is `NOT NULL` and CTL-14's closed
active-capacity whitelist — it exists only to make "gate a durable creator record" unrepresentable.
A marketing section is neither an active-capacity concept nor a durable record; forcing it to pick
a whitelist value would corrupt CTL-14's guard, not just be inaccurate. This migration relaxes
`capacity_class` to nullable and adds one combined check constraint
(`capability_registry_row_shape_check`) requiring exactly one of two shapes per row — see the task
record for the full reasoning. CTL-14's whitelist enum itself is untouched, and is re-proven
(behaviourally and structurally) over the relaxed column in the SQL test.

## Why a dedicated write path for marketing sections, not migration 0157's workflow

`app_private.staff_propose_capability_change` (0152/0157) always writes `proposed_capacity_class`
verbatim — full-replace, never coalesced from the current row, for every change proposed through
that workflow. Routing a marketing-section row's fields through it would force a non-null
`capacity_class` back onto the row on the very next propose/approve/apply cycle, violating the
row-shape constraint this migration adds. Reaching that workflow for marketing-section rows would
require widening `staff_propose_capability_change`/`apply_due_capability_change`'s signatures,
which carry their own exact-signature evidence (0157's own header names two assertions a widened
signature would break) — out of scope here. Migration 0160 therefore ships two new, narrow
functions instead: `staff_create_marketing_section` (new rows only) and
`staff_set_capability_marketing_section` (existing marketing-section rows only — its first action
after the admin gate is refusing, 42501, any row where `is_marketing_section` is false, which is
what makes it structurally incapable of touching a real capability's governed fields). This is the
same posture migration 0153 took when it first shipped single-admin-immediate writes for
`kind`/`limits`/`beta`/`marketing_visible`/`marketing_label`/`marketing_blurb`, before 0157 later
layered two-person governance on top for real capabilities specifically — a propose/approve/apply
variant scoped to marketing-section rows is real, bounded follow-up work, reported rather than
built here.

## CTL-10's public-leak proof, twice over

Structurally: `app_private.get_public_capability_matrix()`'s `OUT` parameter list has exactly seven
columns — `capacity_class`/`limits`/`rollout_percentage`/`kill_switch`/`beta`/`version`/any audit or
channel column literally cannot be selected through this function, in any future edit that does not
also change this signature. Behaviourally: the SQL test populates a capability with every forbidden
field set to a real value, publishes it, and asserts the public read returns only the seven allowed
values. The explain-plan artifact (`packages/db/explain-plans/public-capability-matrix.explain.md`)
adds a third proof: the unwrapped plan never scans `capability_registry` at all — only
`capability_matrix_snapshots` — so the leak-proofing is visible as a plan shape, not only as a
column-set assertion.

## CTL-11's webhook: outbound-only, and why the marketing repository cannot receive one

`routes/capability-matrix-admin.ts` triggers the marketing webhook only AFTER the database publish
already committed — a version number and timestamp, never capability data — and a webhook failure
never fails the publish response. `bharatstudio-marketing` is a `next export` static site deployed
to Cloudflare Pages, with no server and no database credential (its own repository charter,
restated in `next.config.ts`). It cannot host an inbound Route Handler at all under static export.
"Webhook revalidation" there is therefore a Cloudflare Pages Deploy Hook — external,
dashboard-configured, not in-repo code — which triggers a full rebuild; `scripts/
fetch-capability-matrix.mjs` (new, this task) runs at the start of that rebuild and fetches the same
public `GET /v1/public/capability-matrix` route any other caller uses, falling back to an empty
matrix (never failing the build) when unreachable. This was verified against a real `npm run build`
in that repository (32 static routes generated, CSP regenerated, 8/8 existing site tests still
pass) — not merely asserted.

## What was deliberately not done

- No live marketing page (`app/pricing`, `app/features`) was rewired onto the matrix. The real
  `capability_registry` has zero rows with `marketing_visible = true` today; rewiring a live page to
  a currently-empty source would blank it, and this task's hard constraints forbid inventing
  marketing copy to fill the gap in the meantime.
- No `.env.local` or deployment secret was set — `ALERTS_API_BASE_URL` (marketing repo) and
  `MARKETING_REVALIDATE_WEBHOOK_URL`/`_SECRET` (alerts repo) are both configured-but-unset, per this
  task's "never invent a deployment value" constraint.
- No propose/approve/apply variant for marketing-section governance — reported above.
- `apps/web/app/overlay/canvas/` untouched; `getSubscriberCount()` unchanged (confirmed by the
  unchanged `apps/web` test count, 644/644).

## Verification

See `../tests/TC-CTL-10-public-capability-matrix.md`'s "Commands run" table for the full real-number
account: SQL 83/0, API 904/0, web 644/0 (unchanged), typecheck clean, contracts/explain/harness all
green, and a real `bharatstudio-marketing` build + test pass. Self-reviewed only in this session —
no independent reviewer was available; disposition is Conditionally complete per
`governance/AGENTS.md`.
