# CTL-10 / CTL-11 / CTL-12 — the public capability matrix

**Status:** `Implemented — 2026-09-17`
**Owner:** Sukhdev Singh
**Authority:** `../../FULL-PRODUCT-DEFINITION.md` §20.2, §20.4 ("How the marketing site follows
automatically"), §20.5 ("Full site behind flags"), §31 register rows `CTL-10`, `CTL-11`, `CTL-12`
**Unblocked by:** `../../reviews/2026-09-17-three-owner-decisions-goa17-marketing-bootstrap.md` §2
("`marketing_section` — a separate field, not a seventh `kind`")
**Predecessor:** `CTL-01-capability-control-plane.md` (migration 0149, the registry/resolver/
CTL-03 cache), migration 0153 (§20.2's full field set), migration 0157 (the twelve-field two-
person change-management workflow)
**Decision:** `../../reviews/2026-09-17-ctl-public-matrix-implementation.md`
**Acceptance:** `../../tests/TC-CTL-10-public-capability-matrix.md`

---

## What was blocked, and what unblocked it

`CTL-10`/`CTL-11`/`CTL-12` were blocked on a single open question: whether a marketing page-region
flag (needed for `CTL-12`'s "full site behind flags", §20.5) was a seventh value in
`capability_registry.kind`'s enum, or something else. Migration 0153's own header named this
explicitly as a blocker rather than inventing an answer. The owner decision above settled it:
**a marketing section gets its own field**, not a `kind` value — `kind` stays a taxonomy of
capabilities (widget/module/feature/hub_lane/lobby_mode/ai_feature); a marketing section is a page
region, not something a creator is entitled to.

## Scope — one migration, one lane

`CTL-10` · `CTL-11` · `CTL-12`. Migration **`0160`**.

| Row | What it required |
|---|---|
| `CTL-10` | `GET /v1/public/capability-matrix` — public, unauthenticated, a **published snapshot** |
| `CTL-11` | The marketing build reads the snapshot at build time; **webhook revalidation** |
| `CTL-12` | Marketing sections behind flags, via their **own field** (`is_marketing_section`) |

## What CTL-10 required, structurally

`GET /v1/public/capability-matrix` is the one capability surface with no token at all, so it must
expose **only** `capabilityId`/`marketingLabel`/`marketingBlurb`/`minTier` (§20.4's own line) plus
`isMarketingSection` (CTL-12) and the snapshot's own version/timestamp — never `capacityClass`,
`limits`, denylists, allowlists, rollout percentages, kill state, audit rows, or anything channel-
specific. This is enforced as a property of `app_private.get_public_capability_matrix()`'s
**declared return type** (seven `OUT` columns, nothing else reachable through the function at all),
not a serializer trim — re-asserted in the SQL test against `information_schema.parameters`, and
again at the contract layer (`PublicCapabilityMatrixEntry`, `additionalProperties: false`).

A **published snapshot**, not a live query: `public.capability_matrix_snapshots` is an append-only
table (migration 0155's `reject_table_mutation` trigger, reused verbatim). `app_private.
staff_publish_capability_matrix_snapshot` computes one new version from every `capability_registry`
row where `marketing_visible AND NOT kill_switch`; `get_public_capability_matrix` reads only the
latest one, never joining `capability_registry` at all. `snapshotVersion`/`publishedAt` repeat on
every entry so a stale CDN copy is identifiable, not silently wrong.

## CTL-12 — the structural split

`capability_registry.capacity_class` (CTL-14's closed active-capacity whitelist, NOT NULL since
migration 0149) was relaxed to nullable, and a new combined check constraint
(`capability_registry_row_shape_check`) requires exactly one of two shapes per row: an ordinary
capability (`is_marketing_section = false`, `capacity_class` required) or a marketing section
(`is_marketing_section = true`, `kind` and `capacity_class` both null). CTL-14's whitelist itself is
untouched. A marketing-section row is created only via `app_private.staff_create_marketing_section`
and updated only via `app_private.staff_set_capability_marketing_section` — the latter's first
action after the admin gate is checking `is_marketing_section`, refusing (42501) any row where it is
false, so neither function can ever become a path that changes a real capability's kill_switch/
marketing_visible/marketing_label/marketing_blurb outside migration 0157's two-person workflow.
`app_private.resolve_channel_capabilities` (the CTL-03 per-channel resolver) was widened by exactly
one filter, `where not reg.is_marketing_section`, so a page-region flag never enters a creator's
resolved capability blob.

## CTL-11 — webhook revalidation, and why it is outbound-only

`apps/api/src/routes/capability-matrix-admin.ts` triggers a marketing revalidation webhook AFTER a
publish has already committed to the database — a version number and timestamp only, never
capability data, and a webhook failure never fails the publish response (the snapshot is already
durable and servable). `bharatstudio-marketing` is a `next export` static site deployed to
Cloudflare Pages with no server and no database credential (its own repository charter) — it cannot
host an inbound webhook **receiver** at all. "Webhook revalidation" there is realized as a
Cloudflare Pages Deploy Hook (external, dashboard-configured): the alerts API's outbound call
targets that Deploy Hook URL, which triggers Cloudflare to re-run `npm run build`, which re-runs
`scripts/fetch-capability-matrix.mjs` — a build-time fetch from the same public
`GET /v1/public/capability-matrix` route, writing `data/capability-matrix.json` for any page to
import via `lib/capability-matrix.ts`. See that script's own header for the full reasoning.

## What this does NOT do (deliberately)

- Does not migrate `app/pricing` or `app/features` in `bharatstudio-marketing` off their existing
  hand-authored copy onto the matrix. The live `capability_registry` has zero real rows with
  `marketing_visible = true` today (only this task's own SQL-test fixtures, in an isolated test
  database) — rewiring a live pricing/legal page to a currently-empty source would blank it. This
  task's own hard constraints forbid inventing marketing copy to fill the gap. Adopting the matrix
  on those pages is real, bounded follow-up work once CTL-04/05/13's admin UI (a separate lane) lets
  staff actually publish real rows.
- Does not build a propose/approve/apply (two-person) governance variant for marketing-section
  rows — reported in migration 0160's own header as bounded follow-up, the same way migration 0153
  reported its own single-admin-immediate gap before 0157 closed it for real capabilities.
- Does not touch `apps/web/app/overlay/canvas/` — this plane has no overlay-facing surface, same
  posture every CTL migration before it has taken.

## Governed-field guard preserved

`app_private.staff_set_capability_registry_entry` (migration 0155, Job 3) still rejects any call
targeting an EXISTING capability_key — unchanged by this task. Migration 0157's twelve-field
propose/approve/apply workflow is untouched: neither of this task's two new write functions can
reach a real capability's governed fields (see the structural guard above).
