# CTL phase 2 Lane A — change management: implementation record

**Date:** 2026-09-17
**Owner:** **Sukhdev Singh**
**Authority:** `../FULL-PRODUCT-DEFINITION.md` §31.19 rows CTL-06/CTL-07/CTL-08/CTL-09 ·
`active/launch/00_LAUNCH_SCOPE_AUTHORITY.md`
**Task:** `../active/tasks/CTL-06-change-management.md`
**Acceptance:** `../tests/TC-CTL-06-change-management.md`
**Predecessor:** `2026-09-17-ctl-phase-1-implementation.md` (migration `0149`, landed `518d592`) —
read as authority, never modified.

---

## What this task is, in one paragraph

Migration `0152` adds a governance layer in front of the ONE write path migration `0149` already
ships (`app_private.staff_upsert_capability_registry_entry`): a staged-change table
(`capability_change_requests`), an approval ledger (`capability_change_approvals`), and six
`app_private` functions covering propose/list/get/approve/reject/kill/revert. Every actual
mutation of `capability_registry` still funnels through 0149's single function — this migration
invents no parallel write path, no parallel versioning, no parallel audit trigger. It is
deliberately narrow: no admin UI, no public matrix, and — per its own task record — no invented
`is_platform_owner` role.

## Schema design decisions, and why each shape was chosen

**One change-request table covering three kinds (`update`, `kill`, `revert`), not three tables.**
`change_kind` distinguishes an ordinary governed change (which goes through
`pending_approval → approved → applied`) from the two single-action kinds, which are always
inserted directly at `status = 'applied'`. A single table gives one unified audit/history surface
for "every governance action ever taken on this capability," which is what a future admin panel
(CTL-04, a different repository) will want to render as one timeline, not three.

**`proposed_capacity_class` copies 0149's whitelist token-for-token rather than referencing it.**
PostgreSQL has no cross-table check-constraint reuse. The alternative — validating in application
code that `capacityClass` is in the allowed set before calling the SQL function — was rejected for
the same reason CTL-14 itself rejected a blacklist-of-forbidden-tokens approach: a second copy of
the rule that CAN drift from the first is exactly the failure mode a structural guard exists to
prevent. The SQL test (`packages/db/tests/ctl_change_management.sql`) proves this is a genuine
second CHECK constraint, not the same one referenced twice, by scanning
`capability_change_requests_proposed_capacity_class_check`'s own `pg_get_constraintdef` — a drift
between it and 0149's `capability_registry_capacity_class_check` would be caught the moment
someone widens one and not the other.

**CTL-06's read-time correctness is a shared helper (`capability_change_row`), not per-function
logic.** Every function that returns a change-request row does so by calling
`app_private.apply_due_capability_change(id)` first, then selecting through
`app_private.capability_change_row(id)`. This means "check whether this row is due and apply it"
is written exactly once and cannot be forgotten in a new function later — the same reasoning 0149
applied to auditing (a trigger, not per-call-site inserts). `staff_list_capability_changes`
additionally runs a pass over every `approved`-and-due row before its own listing query, so a list
is never stale even for rows nobody has individually read yet.

**What CTL-06 does NOT give you, named explicitly rather than left implicit.** A due change that
NOBODY reads through this plane stays `approved`-but-unapplied indefinitely — `capability_registry`
itself is untouched until something calls in here, and 0149's own `resolve_channel_capabilities`/
`get_channel_capabilities` (both frozen, unmodified) read `capability_registry` directly. This
task's own instruction was explicit: "if you need a sweeper too, say so, but read-time correctness
comes first." Read-time correctness is built and proven (`packages/db/tests/
ctl_change_management.sql`'s central CTL-06 test: propose a change with `effective_at` in the past,
approve it, then perform ONLY a plain `staff_get_capability_change` read — no apply/sweep call
anywhere in the test — and assert both the change's own `status = 'applied'` and
`capability_registry`'s live row already reflect the new values). A periodic sweep — the same
shape as RT-04/RT-05's leased outbox dispatcher, a cron calling
`app_private.apply_due_capability_change` over every due row — would close the "nobody happened to
look" latency gap and is recommended as a genuine follow-up, not built here.

**CTL-07's three rules are three code paths, not one collapsed approval check.** This was the
single biggest risk in this task's own instructions ("do not collapse them into one approval
rule"). Concretely:
- `staff_approve_capability_change` is the ONLY function that records a `staff`/`owner` approval,
  and only for `change_kind = 'update'` rows in `pending_approval` — `kill` and `revert` rows
  never reach it (there is no code path by which a `kill` row could accumulate approvals, because
  it is inserted at `status = 'applied'` directly, never `pending_approval`).
- `staff_kill_capability_now` is a SEPARATE function with its own `is_platform_admin()` gate and
  no approval-table interaction at all — single-admin by construction, not by a count check that
  happens to equal 1.
- `staff_revert_capability_registry_entry` is a THIRD separate function, also single-admin,
  reading `capability_registry_audit` rather than the approval ledger at all.

Collapsing these into one parameterised "approve" function with a mode flag was considered and
rejected: it would make it possible to accidentally route a kill through the two-staff path (or
vice versa) by a wiring mistake, exactly the ambiguity three separate functions with three
separate grants structurally rule out.

**The owner-sign-off blocker was surfaced, not solved by minting a role.** `app_users` has exactly
one staff boolean (`is_platform_admin`, migration `0073`) and no owner/staff rank. Two options were
considered: (a) add `app_users.is_platform_owner boolean` in this migration, or (b) build the
WORKFLOW shape (a distinct required `owner` approval kind, structurally separated from `staff`
approvals by the same `UNIQUE(change_request_id, approver_id)` constraint that already forces
maker-checker) while gating it on the same `is_platform_admin()` check available today, and name
the resulting identity gap explicitly. This task's own hard constraint chose (b) for me: "do not
invent who counts as staff or owner... if the distinction you need does not exist, that is a
blocker to report, not a role to mint." (a) would also have been a scope violation of the
migration's own stated boundary (a role/permission model change, not a change-management schema
change) and would have made an unreviewed identity decision inside a migration whose authority
record does not cover it. The workflow control (three distinct people, one of them explicitly
labelled `owner`) is real value even without the identity check — it is what makes accidentally
completing a pricing-tier-down move with two ordinary approvals impossible, which is the actual
CTL-07 failure mode named in the register row.

**CTL-08's revert reuses 0149's write function rather than writing `capability_registry` directly.**
Restoring prior field values by directly `UPDATE`ing `capability_registry` from this migration was
considered and rejected: it would either need to duplicate 0149's versioning/audit trigger logic
(there is none to duplicate — the triggers already fire on any write to the table, so a direct
`UPDATE` gets them for free) or risk drifting from 0149's own validation (the same CHECK
constraints on `capability_registry` apply either way, so there was no actual duplication risk
there) — but calling `staff_upsert_capability_registry_entry` keeps the "one write path" property
literally true rather than "true except for reverts," which the test file proves by checking that
a revert bumps `version` and produces exactly one new `capability_registry_audit` row, with the
two prior rows byte-for-byte unchanged.

## Verification

See `../tests/TC-CTL-06-change-management.md` for the acceptance criteria and the full "Commands
run" table with real, freshly-executed numbers: SQL suite 75/0 (baseline 74/0), API 797/0
(baseline 790/0), web 644/0 (unchanged), typecheck 0 errors, contracts 66 fixtures/113 paths/131
operations (baseline 65/107/124), explain 28/28 (baseline 27/27), harness pass.

## Blocker surfaced, not worked around

See `CTL-06-change-management.md`'s own "Blocker" section: no `is_platform_owner` (or any staff/
owner rank distinction) exists in `app_users`. `approval_kind = 'owner'` is currently authorised by
the same `is_platform_admin()` check as `'staff'` — the three-distinct-person WORKFLOW control is
real and tested; the IDENTITY guarantee behind the word "owner" is not. A follow-up task, with its
own authority record, is the correct place to decide what that distinction should be (a new
boolean column, a role enum, an external approval system) — not this migration.
