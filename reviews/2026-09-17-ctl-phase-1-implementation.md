# CTL phase 1 — capability control plane: implementation record

**Date:** 2026-09-17
**Owner:** **Sukhdev Singh**
**Authority:** `../FULL-PRODUCT-DEFINITION.md` §12.6, §12.6.2, §30, §31 rows CTL-01/CTL-02/CTL-03/CTL-14/CTL-15 · `active/launch/00_LAUNCH_SCOPE_AUTHORITY.md`
**Task:** `../active/tasks/CTL-01-capability-control-plane.md`
**Acceptance:** `../tests/TC-CTL-01-capability-control-plane.md`
**Predecessor:** `2026-09-17-slice-7-hostile-code-review.md` and the verified area audit that
established CTL at 0 of 15 usable

---

## What phase 1 is, in one paragraph

Migration `0149` adds one subsystem — a capability registry table, a resolution-order engine,
a per-channel resolved-blob cache, and two structural guards — none of which existed anywhere in
this repository before today. It is deliberately narrow: it does not migrate any of the seven
hand-rolled entitlement gates already shipping (`events_pack_entitled`,
`soundboard_module_entitled`, `soundboard_tier_rank`, `vertical_canvas_layout_entitled`,
`canvas_layout_tier_rank`, `sticker_tier_rank`, `template_tier_rank` — all untouched, all still
passing their own tests), does not build an admin UI or change-management workflow, and exposes
exactly one API route: a read of the resolved blob.

## Schema design decisions, and why each shape was chosen

**One registry table, not per-capability tables.** `public.capability_registry` holds every
capability as a row (`capability_key`, `capacity_class`, `kill_switch`, `rollout_percentage`,
`min_tier`) rather than one table per gated feature. This is what makes a single
`jsonb_object_agg` produce the whole resolved blob in one query (CTL-03) — the alternative (a
table per feature, mirroring the seven hand-rolled gates) would have reproduced exactly the
per-feature duplication CTL-01 exists to end.

**Two CTL-02 support tables, not columns on the registry row.** `capability_denylist` and
`capability_overrides` are both `(capability_key, channel_id)`-keyed tables rather than array
columns on `capability_registry`, because a channel-scoped exception is a many-to-many
relationship (many channels can be denylisted from one capability; one channel can be denylisted
from many capabilities) that a single row's array column would represent awkwardly and index
poorly. Both are revoked from `bsa_app` for the same CTL-03 reason the registry itself is.

**CTL-14's guard is a closed whitelist, not a blacklist scan of free text.** The task named
SP11.18/MED20.1 (`packages/db/tests/prf02_slice7_sponsor_card.sql`,
`packages/db/tests/prf02_slice7_media_queue.sql`) as the precedent style — scanning
`pg_get_functiondef`/`information_schema.columns` for forbidden tokens. That technique is
reused for the STRUCTURAL half of CTL-14 (scanning the constraint definition itself), but the
PRIMARY mechanism is stronger: `capacity_class` is a `CHECK ... IN (...)` whitelist containing
only the eight active-capacity concepts §12.6.1 rule 3 names (plus `master_canvas_module`, an
existing §30.3 concept). A blacklist of forbidden tokens on free text risks both false positives
(the word "configuration" is a completely ordinary thing to say about a legitimate capacity
concept — e.g. "AI usage quota configuration UI") and false negatives (a registrant could phrase
around any specific banned word). A closed whitelist has neither failure mode: there is no
enum value that means "gate a durable record," so no description, however worded, can select
one. This is why CTL14.1-CTL14.4 in the acceptance record pair a *behavioural* proof (the nine
forbidden classes rejected) with a *structural* one (the whitelist's own definition scanned) —
belt and suspenders, but the whitelist is the belt.

**CTL-15 is proven by absence, scanned structurally, not by a "no default" convention.** No
column named anything retention-shaped exists on any of the six tables this migration creates.
The SQL test scans `information_schema.columns` for `retention|retain|ttl|expir` across all six
and asserts zero matches — the same technique as CTL-14's structural half, applied to schema
shape instead of a single constraint's definition. This is deliberately NOT "retention exists
but defaults to null/unlimited" — that shape would still let someone later set a per-tier value.
The column does not exist to set.

**CTL-03's cache is a real table with a real invalidation signal, not a documented convention.**
A single-row `capability_registry_generation` counter, bumped by a statement-level trigger on any
write to the registry or either CTL-02 support table, is the invalidation clock. A per-channel
cache row in `capability_resolutions` is valid only while its stored `(generation, channel_tier)`
matches current state — checked inside `app_private.resolve_channel_capabilities` before any
join across the registry tables runs at all. This is why CTL03.2 (identical `resolved_at` on an
unchanged second read) and CTL03.4 (a channel's own tier change invalidates its cache even with
generation unchanged) are both real, measured behaviours, not asserted from a comment: the EXPLAIN
capture in `packages/db/explain-plans/capability-resolution.explain.md` shows the cache-hit path
at `shared hit=5` buffers versus the cache-miss path's `shared hit=595 read=5 dirtied=3 written=2`
— roughly two orders of magnitude fewer buffer touches, and zero `Seq Scan` on
`capability_registry`/`capability_denylist`/`capability_overrides` at all on the hit path.

**CTL-02's precedence is a CASE chain, not five independent booleans ANDed together.** kill and
denylist each force `false` unconditionally; rollout forces `false` for a channel outside its
deterministic bucket; only once all three have passed does the tier default get computed, and
only then may an explicit `capability_overrides` row replace that default. The SQL test proves
this is the real evaluation order, not just the intended one, by constructing four cases where an
ACTIVE override is left in place and showing kill, then denylist, then rollout each still force
`false` despite it — the override only ever wins when nothing upstream of it already decided.

## Why bsa_app has zero direct grants on all five tables

CTL-03 says "never per-capability queries." A documented convention ("always call
`get_channel_capabilities`, never query the tables directly") is exactly the kind of rule that
survives code review and then gets violated the first time someone is in a hurry. Revoking
`SELECT`/`INSERT`/`UPDATE`/`DELETE` from `bsa_app` on `capability_registry`,
`capability_registry_audit`, `capability_denylist`, `capability_overrides` and
`capability_resolutions` makes the convention a database-enforced fact: the running API's own
role cannot express a per-capability query even if a future engineer writes one by accident — it
fails at the connection's own privilege level, not at code review. `packages/db/tests/
ctl_capability_registry.sql` proves this both from the catalogue (`has_table_privilege`) and
behaviourally (`SET ROLE bsa_app` then a direct `SELECT`, expecting `insufficient_privilege`).

## Reuse anchors, named as the task requires

| Value / shape | Reused from |
|---|---|
| `app_private.current_channel_tier` | `packages/db/migrations/0086_v1_l15_youtube_connectors.sql:139` |
| `app_private.has_channel_role`, `app_private.current_user_id` | `packages/db/migrations/0002_v1_security_rls_archive.sql` |
| `app_private.is_platform_admin` (staff gate) | `packages/db/migrations/0073_v1_l03_admin_dlq_tooling.sql:38` |
| Staff write + same-transaction audit-row pattern | `app_private.staff_review_creator_pack_sticker` / `public.staff_creator_pack_review_audit`, `packages/db/migrations/0122_v1_l22c_staff_creator_pack_review.sql` — CTL's own audit differs by using a TRIGGER instead of an explicit insert inside the function, deliberately: a direct-SQL write (e.g. a test fixture) must still be audited, which an explicit-insert-only function cannot guarantee |
| `*_tier_rank` helper shape (new, one-per-feature, not shared) | `app_private.canvas_layout_tier_rank`, `packages/db/migrations/0147_v1_prf02_vertical_layout.sql:182` — every existing `*_tier_rank` function in this schema is already scoped one-per-feature; `capability_tier_rank` follows the same posture rather than becoming the first shared one |
| Structural forbidden-token scan technique | `packages/db/tests/prf02_slice7_sponsor_card.sql` (SP11.18), `packages/db/tests/prf02_slice7_media_queue.sql` (MED20.1) — reused for CTL-14's structural half and CTL-15 in full |
| Exact returned-column-set assertion via `information_schema.parameters` | `packages/db/tests/prf02_slice7_vertical_layout.sql` |
| Creator-facing read role set (owner/admin/operator/moderator/viewer), non-member = zero rows | `app_private.get_channel_canvas_layout`, migration 0147 |
| `insights`-shaped creator/dashboard read wired to `derivedReadSql`, not the main pool | `apps/api/src/db/insights-store.ts` / `apps/api/src/routes/insights.ts` — `capability-store.ts`/`routes/capabilities.ts` mirror this shape exactly, including the "both not-found and not-a-member map to the same 404" posture |
| `createTestFastify`-backed test harness, actually reached via `buildApp` | `apps/api/test/insights-routes.test.ts` — `capability-routes.test.ts` follows the identical structure |

## Blocker/decision surfaced, not worked around

`pnpm test`'s `measurement:test` sub-step fails in this execution environment: `scripts/
measurement/run_local_measurement.py` reads a manifest template from a sibling
`bharatstudio-infra` checkout that does not exist in this worktree layout. Confirmed pre-existing
and unrelated to this phase — zero diff under `scripts/measurement/`, and the failure reproduces
identically running the script directly, before any CTL file existed in the process invocation.
This is the same sub-step `TC-PRF-02-slice-7-vertical-layout.md` already flagged (there, a
different exact symptom — Docker reachability, not a missing sibling checkout). No fix was
attempted: provisioning a `bharatstudio-infra` sibling worktree is outside this task's scope and
outside `bharatstudio-alerts`' own repository boundary.

## Verification

See `../tests/TC-CTL-01-capability-control-plane.md` for the acceptance criteria and the full
"Commands run" table with real, freshly-executed numbers (SQL suite 73/0, API 779/0, web 644/0,
both typechecks 0 errors, contracts 64 fixtures/105 paths/122 operations, explain 27/27, harness
pass).
