# CTL twelve-field change workflow — implementation record

**Date:** 2026-09-17
**Owner:** **Sukhdev Singh**
**Authority:** `../FULL-PRODUCT-DEFINITION.md` §20.1, §20.6/§20.6.1, §31.19 rows CTL-06/07/08/09
**Task:** `../active/tasks/CTL-06-twelve-field-change-workflow.md`
**Acceptance:** `../tests/TC-CTL-06-twelve-field-change-workflow.md`
**Predecessors:** migration `0152` (change management, six fields), `0153` (§20.2's remaining
six fields on the registry, workflow-widening explicitly deferred), `0155` (real owner identity,
emergency kill, and the single-admin bypass closure that made this task's absence of a governed
path for the six new fields a real, live gap rather than a theoretical one)

---

## What this slice is, in one paragraph

`0153` added six §20.2 fields to `capability_registry` and reported, explicitly, that threading
them through `0152`'s two-staff-approved workflow was real follow-up work it was not doing. `0155`
then closed the single-admin bypass on the ONE write path those six fields had
(`staff_set_capability_registry_entry`, now `42501` on an existing capability). The combination
left the six fields with literally no governed change path on a live capability — this migration
(`0157`) is that follow-up, built the way `0153`'s own header sketched it: not a parallel function
family, but a genuine widening of the existing one, using the `DROP FUNCTION` + `CREATE FUNCTION`
technique this schema already had a precedent for (`get_overlay_events`, migration `0127`).

## The frozen-output-shape problem — solved properly this time, and why that matters

`0153`'s own header named the alternative it considered and rejected: "the alternative (parallel
`staff_propose_capability_registry_change` / `staff_get_capability_change_full` / `staff_list_
capability_changes_full` functions ... is real, designed, and NOT built here." This task's own
instructions explicitly asked for the frozen-shape problem to be solved "properly," widening the
declared `returns table` and updating every caller and assertion — not bolting on a second
function — and to argue explicitly if a second function were concluded to be better. It is not
better here: a second function family would mean two propose endpoints, two get/list pairs, two
OpenAPI operation sets, and a permanent question for every future caller ("which one do I call for
a capability that might need both?"). `DROP FUNCTION` + `CREATE FUNCTION` under the SAME name,
proven safe by this repository's own `get_overlay_events` precedent (cited in `packages/db/
explain-plans/check-plans.mjs`'s own extraction-method comment), is the correct fix, and this
migration does exactly that for the entire `capability_change_row` family — eight functions,
identically widened to 24 columns, re-granted to `bsa_app` after each `DROP` (which discards
grants a `CREATE OR REPLACE` would have preserved).

## Merge semantics — the one substantive design decision this task made, argued explicitly

The task's own instructions did not specify HOW the six new fields should behave when a propose
call does not mention them. Two choices existed:

1. **Full-replace, always required** (matching `0149`'s `staff_upsert_capability_registry_entry`
   and `0153`'s `staff_set_capability_registry_entry` — "supply the complete desired state, nothing
   silently preserved"). This is the idiom the rest of this schema already uses for DIRECT,
   immediate writes.
2. **Merge, `NULL` = "untouched"** — a change-request system proposes a DELTA, not necessarily a
   complete row.

Choice 1 would have been simpler to state, but it is actively dangerous applied to a STAGED,
governed CHANGE (as opposed to an immediate direct write): the existing `packages/db/tests/
ctl_registry_spec_alignment.sql` file already contains a test — written by `0153`, for `0153`'s own
narrower workflow — asserting that "0152's unmodified apply path must PRESERVE kind/beta/
marketing_visible" on an ordinary six-field-only change. Adopting full-replace semantics for the
widened workflow would have made that a **regression**: an admin changing only `rolloutPercentage`
would silently wipe a capability's `kind`/`limits`/`beta`/`marketing_*` back to their column
defaults the moment their change applied, with no warning, no error, and no field in the request
that told them so. That is the opposite of §20.1's *"changing a limit is an audited admin
action"* — it would make changing ANY field an unaudited deletion of five others. Merge semantics
(choice 2) was the only option that both closes this task's assigned gap AND keeps that
pre-existing regression test passing without weakening it — I verified this by leaving `packages/
db/tests/ctl_registry_spec_alignment.sql` completely untouched and re-running its own suite (it
passes; see Verification below), rather than "fixing" that test to accept the new behaviour.

**The cost of that decision, named rather than hidden:** `marketing_label`/`marketing_blurb` are
themselves nullable, real-valued columns — `NULL` there means "no label," a legitimate target
state. Merge semantics makes that state unreachable through this governed workflow once a label
has ever been set (proposing `NULL` reads as "don't touch," not "clear it"). This is a real,
narrow limitation, documented in the migration header, this task's own record, and the OpenAPI
schema's field descriptions. It was not solved with a second "explicit clear" flag because that
is exactly the kind of unrequested feature-scope-creep the task's hard constraints (ship no
invented values, stay narrowly scoped) argue against — a real future need, not invented now.

A second, related consequence, also named rather than solved: `capability_registry_marketing_
copy_check` (marketing_visible requires label+blurb) cannot be validated at PROPOSE time under
merge semantics, because the eventual merged row depends on state at APPLY time, which may be
staged arbitrarily far in the future. The registry's own check constraint remains the actual
enforcement, firing at apply time on the rare change whose merge would violate it — a slightly
later feedback point than an admin UI would ideally want, reported as a known characteristic of
this design, not silently accepted as invisible.

## Why `apply_due_capability_change` calling the unguarded helper is not a second path around approval

This is the question this task's own instructions were most insistent on getting right (three
separate "prove no second path" callouts in the dispatch). The reasoning, stated once, carefully:
`app_private.set_capability_registry_entry_unchecked` (migration `0155`'s Job 3a) has NO
`is_platform_admin()` check of its own — it is reachable only from another `SECURITY DEFINER`
function this schema's own migrations define, never directly by `bsa_app` (confirmed: no grant
exists, re-asserted in this task's own test file). `apply_due_capability_change` is one such
caller. But `apply_due_capability_change` ITSELF enforces nothing new — it is gated entirely by
`capability_change_requests.status = 'approved'` and `effective_at <= now()`, a status that, for
`change_kind = 'update'`, can ONLY be set by `staff_approve_capability_change` recording two
distinct `staff` approvals (and, when `requires_owner_signoff`, a real-identity `owner` approval)
— the SAME function, UNTOUCHED body, this migration only widens the declared output of. So the
full causal chain from "capability actually changes" back to "who authorized it" is: `set_
capability_registry_entry_unchecked` (no gate) ← `apply_due_capability_change` (gated on
`status = 'approved'`) ← `status` set by `staff_approve_capability_change` (gated on two-staff/
owner). Widening the SET of fields `apply_due_capability_change` writes does not touch any link in
that chain. This is exactly the same reasoning `0155`'s own revert and kill-auto-revert already
relied on for calling the same unguarded helper — this migration adds a third caller to an already
-established, already-reviewed pattern, not a new one.

## What was verified, concretely, not merely asserted

`packages/db/tests/ctl_change_management_twelve_fields.sql` (new, fixture range `7100`-`71ff`)
runs a genuine propose → two-staff-approve → apply cycle carrying real, distinct values for all
twelve fields and asserts the registry reflects every one of them (not just the original six); a
SEPARATE scenario proves the merge-semantics claim by running an ordinary eight-argument propose
call against the SAME capability afterward and asserting the twelve-field state from the FIRST
change survives untouched; a THIRD scenario proves a paid→Free move proposed through the widened
14-argument call still requires real owner identity (a non-owner admin's `owner` approval attempt
is rejected, the real owner's succeeds, and the resulting registry row shows both the tier move
AND the six new fields applied together); a FOURTH proves revert restores all twelve from a prior
audited state; the file closes with independent re-scans of CTL-09 (both constraint definitions),
CTL-14, CTL-15, CTL-03, and an explicit check that `staff_set_capability_registry_entry` still
rejects an existing capability (the bypass stays closed) and that the unguarded helper stays
ungranted to `bsa_app`.

The explain-plan artifact for `staff_list_capability_changes` — the one query in this migration's
family shaped like the widget-backing aggregates this repository's `explain-plans/` directory
otherwise exists to catch — was not merely left as-is (which would have silently kept documenting
`0152`'s now-superseded 18-column definition, still technically hash-matching because `0152`'s own
file is untouched and the check only re-extracts whatever migration file the artifact's own
"Defined at" line names). It was re-anchored to migration `0157` (where the function actually
lives now) and re-captured with a real `EXPLAIN (ANALYZE, BUFFERS)` against a real
`postgres:16-alpine` container with all 156 migrations applied — the numbers in that artifact
(costs, buffer counts, timings, the `width` change from 302/177 to 432/328) are freshly measured,
not carried forward or estimated.

## Verification, real numbers

Every command in `TC-CTL-06-twelve-field-change-workflow.md`'s own table was run against a real
`postgres:16-alpine` container and real `tsc`/`tsx --test` runs, not asserted from source reading —
80/0 SQL (79 pre-existing files unchanged, one new), 866/0 API (865 pre-existing, one new test),
644/0 web (untouched), 0 TypeScript errors on both packages checked separately, contracts
validated at 127 paths / 148 operations (unchanged — no new route), explain-plans at 31/31 (one
entry re-anchored and genuinely re-captured, not merely re-pointed), and `harness:check` green.
`measurement:test` was not separately re-verified, for the same pre-existing environmental reason
this task's own predecessor records already documented under the same base-commit lineage.

## Disposition

`CTL-06`/`CTL-07`/`CTL-08`/`CTL-09`'s register-letter status is unchanged by this record, per this
task's own instruction: this documents what was built, not a state change. §20.1's *"changing a
limit is an audited admin action"* is now implementable for all twelve §20.2 fields, not six.
`CTL-10/11/12` remain blocked on the `marketing_section` `kind`-enum gap `0153` already reported —
this migration adds no ninth value. `ADM-07` (platform-admin definition) is untouched, a different
lane's own record.
