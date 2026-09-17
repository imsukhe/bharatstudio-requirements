# CTL — widening the change-management workflow to all twelve §20.2 fields

**Status:** `Implemented — verification recorded, review pending`
**Owner:** **Sukhdev Singh**
**Authority:** `../../FULL-PRODUCT-DEFINITION.md` §20.1 (*"changing a limit is an audited admin
action"*) and §20.6/§20.6.1 (*"two-person approval for every capability change"*) · §31.19 rows
`CTL-06`, `CTL-07`, `CTL-08`, `CTL-09`
**Predecessors:** `CTL-06-change-management.md` (migration `0152`, the propose → two-staff-approve
→ apply workflow, over the original six registry fields only) · `CTL-01-capability-control-
plane.md`'s own correction section (migration `0153`, the §20.2 field set — six more fields added
to `capability_registry`, deliberately NOT threaded through `0152`'s workflow) ·
`CTL-07-emergency-kill-and-owner-identity.md` (migration `0155`, real owner identity, §20.6.1's
full emergency-kill path, and the single-admin bypass closure on `staff_set_capability_registry_
entry` that made this task urgent)

## The gap, in one paragraph

Migration `0149` shipped six registry fields and one governed write path. Migration `0152` built
propose → two-staff-approve → apply over exactly those six. Migration `0153` added six more §20.2
fields (`kind`, `limits`, `beta`, `marketing_visible`, `marketing_label`, `marketing_blurb`) to
`capability_registry`, but did not widen `0152`'s workflow to carry them — widening `staff_get_
capability_change`/`staff_list_capability_changes`'s frozen exact-output-column shape was test-
breaking, so `0153` shipped a separate single-admin, immediate write function (`staff_set_
capability_registry_entry`) for the six new fields instead, and reported the propose/approve/apply
gap as real, bounded follow-up work. Migration `0155` then correctly closed the single-admin
bypass: `staff_set_capability_registry_entry` now rejects any call targeting an EXISTING
capability (`42501`) — §20.6 requires two-person approval for every capability change, and a
single admin changing a live capability's fields, even six of the twelve, was exactly that
bypass. Net effect: the six fields `0153` added had NO governed change path at all on an existing
capability. §20.1's *"changing a limit is an audited admin action"* was unimplementable until this
task.

## Scope — migration `0157`, widening `0152`'s workflow, not replacing it

| Row | What it requires | What was built |
|---|---|---|
| `CTL-06` | Staged effective-time changes, read-time correctness | Unchanged mechanism (`effective_at`, `app_private.apply_due_capability_change`); re-proven over a change that carries twelve-field content |
| `CTL-07` | Two-staff approval; owner sign-off for paid→Free; single-admin `global_kill` | All three rules' bodies are byte-for-byte `0152`'s/`0155`'s own — only their declared output widens; re-proven, including through the widened 14-argument propose call |
| `CTL-08` | One-action revert | `0155`'s own body (already restored all twelve from the prior audit snapshot) — output widened only; re-proven |
| `CTL-09` | The panel rejects Layer 1 correctness dimensions | `proposed_capacity_class`'s whitelist untouched; both-definitions structural scan re-run over the widened table |

`capability_change_requests.proposed_kind`/`proposed_limits`/`proposed_beta`/`proposed_marketing_
visible`/`proposed_marketing_label`/`proposed_marketing_blurb` **already existed** — migration
`0153` added them, nullable, unused, precisely so a `capability_registry_audit` snapshot taken
after `0153` would carry the full row and `CTL-08` revert could restore it. This task is the first
one to actually READ them from a propose call and WRITE them on apply. No `ALTER TABLE` was needed
for these six columns.

## The frozen-output-shape problem, solved the way this task's own instructions required

`0153` avoided widening `staff_get_capability_change`/`staff_list_capability_changes` because
`packages/db/tests/ctl_change_management.sql` carries an exact `information_schema.parameters`
assertion on their OUT column list, and `CREATE OR REPLACE FUNCTION` cannot change a function's
return type. This task does exactly what `0153` deferred: `DROP FUNCTION` + `CREATE FUNCTION` for
every function in the `capability_change_row` family (the helper itself, `staff_propose_
capability_change`, `staff_get_capability_change`, `staff_list_capability_changes`, `staff_
approve_capability_change`, `staff_reject_capability_change`, `staff_kill_capability_now`,
`staff_revert_capability_registry_entry`) — all eight widened to the SAME 24-column shape (the
original 18 plus the six new columns, placed after `proposed_min_tier`), re-granted to `bsa_app`
(a `DROP FUNCTION` discards existing grants; `CREATE OR REPLACE` would have preserved them, so
every dropped function needed its grant restated). No second function was added anywhere in this
migration; every caller keeps calling the same name.

`staff_propose_capability_change`'s input signature widened too (8 → 14 parameters). The six new
trailing parameters default to `NULL`, so every pre-existing 8-positional-argument call site in
`packages/db/tests/ctl_change_management.sql`, `ctl_registry_spec_alignment.sql` and `ctl_
emergency_kill_and_owner.sql` kept compiling and running, unmodified — PostgreSQL's regprocedure
signature resolution names the FULL parameter type list regardless of defaults, so the one
required edit to `ctl_change_management.sql` was its grants-lockdown assertion's signature text,
not any call site.

## Merge semantics for the six new fields — the design decision this task had to make explicitly

The original six `proposed_*` fields keep FULL-REPLACE semantics, unchanged since `0152`. Widening
the six NEW fields to that same idiom would force every ordinary six-field change (a tier tweak, a
rollout bump) to also restate `kind`/`limits`/`beta`/`marketing_*` on every call, and — far more
seriously — would make an ordinary six-field propose call silently WIPE those six fields to
`NULL`/`false`/`{}` on apply, via the widened write path, unless the caller happened to know and
re-state the capability's current values. `packages/db/tests/ctl_registry_spec_alignment.sql`'s
own pre-existing test ("0152's unmodified apply path must PRESERVE kind/beta/marketing_visible")
already demanded the opposite. So: a `NULL` `proposed_kind`/`proposed_limits`/`proposed_beta`/
`proposed_marketing_visible`/`proposed_marketing_label`/`proposed_marketing_blurb` means "this
change does not touch this field" — `app_private.apply_due_capability_change` reads the
capability's CURRENT registry row and coalesces each of the six onto whatever was proposed. A
caller who wants to change one of the six supplies a real (non-`NULL`) value; an explicit `false`
or `{}` is real, not a sentinel, and is written verbatim.

**The one named limitation this creates:** `marketing_label`/`marketing_blurb` are themselves
nullable, real-valued columns (`NULL` there legitimately means "no label set"). Under this
sentinel scheme, a governed change cannot explicitly CLEAR a previously-set label/blurb back to
`NULL` — proposing `NULL` is indistinguishable from "do not touch this field." Not solved here;
would need an explicit "clear this field" flag in a future migration if ever needed.

**A related, deliberately-unsolved case:** `capability_registry_marketing_copy_check`
(`marketing_visible = true` requires both label and blurb non-null) cannot be evaluated at
PROPOSE time under merge semantics, because the eventual merged state depends on the registry row
as it exists at APPLY time (which may be staged arbitrarily far in the future, CTL-06, and may
change before then). `capability_registry`'s own check constraint remains the actual enforcement,
firing at apply time — a change that would produce an invalid merged marketing state fails with
`check_violation` when applied, surfaced through whichever read next triggers CTL-06's lazy apply,
not at propose or approve time.

## The one write path `apply_due_capability_change` now uses, and why it is not a second path that skips approval

Before this task, `apply_due_capability_change` called `0149`'s six-argument `staff_upsert_
capability_registry_entry` — a function that structurally cannot mention the six new fields, which
is exactly why they survived every change `0152`'s workflow ever applied, by accident of that
function's narrower `SET` clause. Carrying twelve fields through apply requires a write path that
CAN set all twelve — that is `0155`'s `app_private.set_capability_registry_entry_unchecked`, the
internal helper revoked from `public` and NOT granted to `bsa_app` at all, reachable only from
another `SECURITY DEFINER` function this migration's own role owns. It is NOT `staff_set_
capability_registry_entry`, which since `0155` rejects any call targeting an existing capability.
Calling the unguarded helper from `apply_due_capability_change` is not a new bypass, for the same
reason `0155`'s own revert and kill-auto-revert already call it directly: by the time `apply_due_
capability_change` reaches that line, the request's status is ALREADY `'approved'` — which for
`change_kind = 'update'` means `staff_approve_capability_change` has already recorded two DISTINCT
staff approvals (and, when `requires_owner_signoff`, a real owner-identity approval) BEFORE this
function is ever called. Widening WHAT apply writes does not widen WHO may cause it to write.

## What this task does NOT do

- Does NOT change `CTL-07`'s three authority rules themselves — `staff_approve_capability_change`'s
  body is byte-for-byte `0155`'s own.
- Does NOT change `staff_kill_capability_now`'s registry write (still six positional arguments to
  `0149`'s own function, still preserving the six new fields by the same unlisted-column-in-`SET`
  mechanism `0153` already proved) — only its declared output widens, and its own `capability_
  change_requests` audit row leaves the six new `proposed_*` columns `NULL` (a kill never touches
  them; not manufactured here).
- Does NOT change who counts as a platform admin (`ADM-07`, a different lane).
- Does NOT build `CTL-04/05/13` (admin UI, impact preview, admin MFA — Lane C, a different
  repository) or `CTL-10/11/12` (public capability matrix, marketing wiring — Lane B; additionally
  still blocked on §20.2's `kind` enum lacking `marketing_section`, per `0153`'s own report — no
  ninth `kind` value is invented here either).
- Does NOT touch `apps/web/app/overlay/canvas/` — `getSubscriberCount()` remains 16.
- Does NOT ship any numeric `limits` value, price, provider behaviour, legal wording, or retention
  window — `limits` remains an admin-filled jsonb, empty by default.

## Reuse anchors

| Value / shape | Reused from |
|---|---|
| `app_private.is_platform_admin` (staff gate, every function) | `packages/db/migrations/0073_v1_l03_admin_dlq_tooling.sql:38` |
| `app_private.is_platform_owner` (owner-identity gate) | `packages/db/migrations/0155_v1_ctl_emergency_kill_and_owner.sql` |
| The unguarded internal write helper `set_capability_registry_entry_unchecked` | `packages/db/migrations/0155_v1_ctl_emergency_kill_and_owner.sql` (Job 3a) |
| `capacity_class`/`proposed_capacity_class` closed whitelist (CTL-14/CTL-09) | `packages/db/migrations/0149_v1_ctl_capability_control_plane.sql`, `0152_v1_ctl_change_management.sql` |
| DROP+CREATE technique for a widened OUT column list | `packages/db/migrations/0127` (`get_overlay_events`), per `packages/db/explain-plans/check-plans.mjs`'s own comment |
| Session-scoped transaction store pattern | `apps/api/src/db/capability-change-management-store.ts` (unchanged pattern, widened columns) |

## Verification

See `../../tests/TC-CTL-06-twelve-field-change-workflow.md` for acceptance criteria and the full
"Commands run" table with real, freshly-executed numbers, and `../../reviews/2026-09-17-ctl-
twelve-field-workflow-implementation.md` for the implementation record and design decisions.
