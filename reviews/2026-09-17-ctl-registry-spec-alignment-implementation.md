# CTL registry spec alignment — implementation record

**Date:** 2026-09-17
**Owner:** **Sukhdev Singh**
**Authority:** `../FULL-PRODUCT-DEFINITION.md` §20 (§20.1-§20.6 in full) — read in full before writing
migration 0153, per this task's own instruction. Also §12.6/§12.6.1/§12.6.2, §31.
**Task:** `../active/tasks/CTL-01-capability-control-plane.md`, its "CORRECTION, 2026-09-17" section
**Acceptance:** `../tests/TC-CTL-01-registry-spec-alignment.md`
**Predecessor:** `2026-09-17-ctl-phase-1-implementation.md` (migration 0149, built against §30
instead of §20 — the error this slice exists to correct) and migration 0152 (change management,
built correctly but on top of 0149's incomplete field set)

---

## What this slice is, in one paragraph

Migration `0149` shipped a sound resolver and two sound structural guards (CTL-14, CTL-15) on an
incomplete field set, because the task record that dispatched it cited §30 instead of §20 — the
section that actually specifies this control plane. Migration `0153` closes the two gaps
`CTL-01-capability-control-plane.md`'s own correction section named: §20.2's field set (`kind`,
`limits`, `beta`, `marketing_visible`, `marketing_label`, `marketing_blurb`) and §20.3's resolution
order (the missing allowlist stage). It touches 0149 and 0152 in the narrowest way each one's own
already-verified test suite allows, and is explicit, in both the migration header and this record,
about the one place it chose NOT to fully close a gap rather than half-build it.

## Why two write functions for the registry, not one widened function

`app_private.staff_upsert_capability_registry_entry` (0149) is referenced by `packages/db/tests/
ctl_capability_registry.sql` in two ways a widened signature or output breaks outright, not just
drifts: a `has_function_privilege` probe cast against the literal text `'app_private.
staff_upsert_capability_registry_entry(text, text, text, boolean, integer, text)'` (dropping that
exact 6-argument overload makes the `regprocedure` cast itself raise `undefined_function`, not fail
an assertion), and an exact `information_schema.parameters` string match on its 8-column output.
Both are "0149's guards must still pass" in the most literal sense available. Postgres also forbids
the tempting middle path — creating a second overload that differs from the first only by trailing
default arguments — because a 6-argument call then becomes ambiguous between the two candidates.
So this migration adds a genuinely separate function, `staff_set_capability_registry_entry`, for
the full 12-field row: same table, same `is_platform_admin()` gate, same versioning/audit/
generation-bump triggers (table-level, proven by 0149's own test to fire regardless of write path —
a bare SQL `UPDATE` with no function involved still bumps the version). The original function is
not deprecated, wrapped, or shadowed; any existing or future caller that only needs the original
six fields keeps using it, unmodified, forever.

The same reasoning applies to `resolve_channel_capabilities`, but there the conclusion is the
opposite: its OUTPUT (`resolved, generation, resolved_at`) is exact-match tested, but that test
does not care what's inside the function BODY, so a body-only `CREATE OR REPLACE` — adding exactly
one new `CASE` branch for the allowlist stage — is both safe and correct. This is why the diff
against 0149's own source, reproduced verbatim in the migration's comments around that function, is
one branch, not a rewrite.

## The allowlist's precedence position, and the judgment call behind it

§20.3 groups "allowlist / rollout %" into a single step 3, both described as "on for this channel
regardless of tier." 0149's existing `rollout_percentage` is an EXCLUSION only (a channel outside
its bucket loses the capability; a channel inside it still needs to pass every downstream stage,
including tier) — the task record's own Gap 2 section calls this out explicitly and scopes the fix
to adding the missing INCLUSION half, not reinterpreting rollout's existing, already-tested
semantics. `capability_allowlist` is therefore a new, independent per-channel grant, evaluated
after denylist and ahead of BOTH rollout-exclusion and tier: an allowlisted channel bypasses the
percentage bucket (the only coherent reading of an explicit grant — an allowlist that a random
bucket could still exclude would not be much of an allowlist) and the tier gate, but cannot resurrect
what kill or denylist already decided, and — like kill/denylist/rollout before it — is never
reachable by the override stage, which remains reserved for replacing the tier default specifically,
exactly as 0149 already established. This is a judgment call about where exactly "joins the same
precedence tier as kill/denylist/rollout" cashes out for override reachability; it is recorded here
explicitly rather than left to be inferred from the diff.

## The one 0152 function touched, and why revert specifically needed it

`capability_registry_audit.new_row` is `to_jsonb(new)` — it captures every column of the row
automatically, so once `kind`/`limits`/`beta`/`marketing_visible`/`marketing_label`/
`marketing_blurb` exist on the table, every audit snapshot taken after this migration carries them
with zero schema work on the audit table itself. `staff_kill_capability_now` needed no change at
all: it calls the original write function with exactly six positional arguments, and that
function's own `ON CONFLICT DO UPDATE SET` clause never mentions the six new columns — an unlisted
column in an UPDATE's SET clause keeps its current value by plain SQL semantics, so kill already
preserved them correctly before this migration touched anything. `staff_revert_capability_registry_
entry` is different: restoring "the immediately previous version" is exactly the operation that
SHOULD pull the new fields from the prior audit snapshot too, and leaving it unfixed would have
been a genuine, narrow correctness bug — a revert that silently left six fields at their
post-change values while correctly restoring the other five. Its external signature
(`(text, text) -> ` the same 18-column table 0152 shipped) is untouched, confirmed against `ctl_
change_management.sql` — no exact-match assertion covers this specific function's output, only `
staff_get_capability_change`/`staff_list_capability_changes` do, and neither was touched. The fix
is a body-only `CREATE OR REPLACE` that extracts six more keys from the same `prev_row` jsonb it
already reads, with `coalesce`-to-a-sane-default for the case where the audit row being restored
predates this migration (its jsonb simply lacks those keys, `->>` returns null, and the coalesce is
a "this old snapshot has no opinion" fallback, not a preserve-current-value sentinel anywhere in
the write path).

## What was deliberately NOT threaded through 0152's staged-change workflow, and why

The two-staff-approved `propose → approve → apply` workflow (CTL-06/07) is not widened to stage or
approve changes to the six new fields in this migration. `staff_get_capability_change` and
`staff_list_capability_changes` both carry an exact-output-column assertion in `ctl_change_
management.sql`, and both return through `capability_change_row` via `select *` — widening any of
the three cascades into the other two, breaking that assertion. The alternative (parallel
`staff_propose_capability_registry_change` / `staff_get_capability_change_full` / `staff_list_
capability_changes_full` functions, entirely independent of the frozen ones, mirroring this slice's
own `staff_set/get/list_capability_registry_entry` split) is real, designed, and NOT built here —
sketched during design as the correct follow-up, but the width of that follow-up (a new table
alteration already partly done here, five more functions, a parallel store/route/openapi surface)
made it a second slice's worth of work under this task's own "say so precisely rather than half-do
it" instruction. What IS built: the six fields are settable and readable through an immediate,
single-admin, still fully versioned-and-audited path (`staff_set/get/list_capability_registry_
entry`), the exact same posture `staff_kill_capability_now`/`staff_revert_capability_registry_entry`
already use for their own immediate, non-staged writes — not a lesser mechanism, a different one,
matching a precedent this schema already had before this migration existed.

## BLOCKER — `kind` has no `marketing_section` value, and CTL-12 needs one

§20.2's own enum (`widget | module | feature | hub_lane | lobby_mode | ai_feature`) is the sole
authority for this field's value set, and it does not contain `marketing_section`, which CTL-12
(`bharatstudio-requirements/active/tasks/CTL-01-capability-control-plane.md`'s own phase-2 Lane B
row) needs verbatim: *"marketing sections behind flags (`kind = marketing_section`)"*. Per this
task's own hard constraint — use a named value set verbatim, report what it does not cover, never
invent a ninth value to paper over the gap — this migration does NOT add `marketing_section` to the
enum. `CTL-10/11/12` (public capability matrix, marketing wiring) stay blocked on this until
whoever owns §20.2 makes an explicit, reviewed call: widen §20.2's enum, or give marketing sections
a different field entirely. Reported here and in the migration header; not solved by a migration
choosing an interpretation on its own.

## Verification, and the one item left to real numbers

Every command in `TC-CTL-01-registry-spec-alignment.md`'s own table was run against a real
`postgres:16-alpine` container and a real `tsx --test` run, not asserted from source reading —
77/0 SQL (76 pre-existing files unchanged, one new), 822/0 API (815 pre-existing, 7 new), 644/0 web
(untouched), 0 TypeScript errors on both packages checked separately, contracts validated at
117 paths / 137 operations (up from 115/134, the three new operations this slice's own three new
routes add), explain-plans unchanged at 29/29 (no new function joined the `derivedReadSql`-backed,
overlay/dashboard-read manifest this migration's staff-only additions are not part of), and
`harness:check` green. `measurement:test` fails for the same pre-existing environmental reason this
task's own instructions named in advance — confirmed unrelated to this slice's diff, not chased
further.

## Disposition

`CTL-01` and `CTL-07`'s register-letter status is unchanged by this record, per this task's own
closing line: this documents what was built, not a state change. §20.2 and the allowlist half of
§20.3 are now represented in the schema and proven by a real test suite; §20.6.1's emergency-kill
rails remain migration 0154's, untouched here; the `marketing_section` gap blocks `CTL-10/11/12`
until it is resolved by an explicit decision, not by this migration's own judgment.
