# CTL-07 — emergency kill in full, and real platform-owner identity: implementation record

**Date:** 2026-09-17
**Owner:** **Sukhdev Singh**
**Authority:** `../FULL-PRODUCT-DEFINITION.md` §20.6/§20.6.1 · register row CTL-07 ·
`reviews/2026-09-17-platform-owner-identity-decision.md`
**Task:** `../tasks/CTL-07-emergency-kill-and-owner-identity.md`
**Acceptance:** `../tests/TC-CTL-07-emergency-kill-and-owner-identity.md`
**Predecessors:** `2026-09-17-ctl-phase-1-implementation.md` (migration `0149`) ·
`2026-09-17-ctl-change-management-implementation.md` (migration `0152`) ·
`2026-09-17-ctl-registry-spec-alignment-implementation.md` (migration `0153`) — all read as
authority, none modified.

---

## What this task is, in one paragraph

Migration `0155` does three things over the same subject — the approval model §20.6 describes.
Job 1 gives `approval_kind='owner'` a real identity check it never had (`app_users.is_platform_owner`,
a partial-unique-index singleton, never self-conferred, always audited). Job 2 builds §20.6.1's full
emergency `global_kill` path as its own subsystem — five new append-only tables and the functions
that fire/ratify/extend/review a kill — leaving migration `0152`'s own ordinary
`staff_kill_capability_now` completely untouched. Job 3 closes a bypass found while building Job 2:
a single platform admin could change an EXISTING capability's governance-sensitive fields
(`min_tier`, `kill_switch`, `rollout_percentage`, `limits`, `capacity_class`) through migration
`0153`'s `staff_set_capability_registry_entry`, without ever going through `0152`'s two-person
workflow.

## Schema design decisions, and why each shape was chosen

**The owner flag is a column plus a partial unique index, not a singleton table.** The binding
decision record (`reviews/2026-09-17-platform-owner-identity-decision.md`) states the shape
directly: "modelling it as a singleton table, or hardcoding an owner id, would make expansion a
schema and data change. A flag plus a droppable constraint makes it a one-line change." This
migration implements exactly that and nothing more — no admin UI to set it, no notification when it
changes (only the audit row), because the decision record does not ask for either.

**Owner+admin conjoint is enforced by ADDING a check, not restructuring the existing one.**
`staff_approve_capability_change`'s `is_platform_admin()` gate at the top of its body already
rejected every non-admin caller, owner or not. The new `is_platform_owner()` check is added only
inside the `approval_kind = 'owner'` branch, after the existing `requires_owner_signoff` check —
this is deliberately minimal: the function's control flow, its maker-checker logic, its status
transition, are all untouched. A wider rewrite was considered and rejected as unnecessary risk to a
function three other migrations' tests already exercise heavily.

**Emergency kill is five tables, not one, because the "not editable by anyone" requirement is
physical, not conventional.** §20.6.1 says the log is "not editable by any admin, including the one
who fired it." A single mutable table with a `status` column (the shape `capability_change_requests`
already uses successfully for CTL-06/07) was considered and rejected here specifically: even a
function-gated `UPDATE ... WHERE id = $1 AND status = 'x'` is still, structurally, an `UPDATE`
statement that COULD be issued directly against the table by anyone with sufficient privilege
(a future migration, a support engineer with a database console, a bug in a not-yet-written
function). The chosen shape — one immutable fire-event row plus four append-only child tables
(ratification, extension-propose, extension-approve, review), each carrying a `BEFORE UPDATE OR
DELETE` trigger that raises unconditionally regardless of role — makes "not editable" true at the
level SQL itself enforces, not at the level of which functions happen to be granted. The SQL test
proves this by attempting the forbidden `UPDATE`/`DELETE` from the SAME session that performed the
original `INSERT` — not a lower-privileged session, the actual writer.

**Auto-revert restores from the SAME audit-snapshot mechanism CTL-08 revert already uses, not a
bespoke "previous kill_switch" flag.** `staff_fire_global_kill` captures `pre_kill_audit_id` — the
`capability_registry_audit` row immediately before its own write — at fire time. `apply_due_kill_
revert` restores the FULL row from that snapshot (kind, limits, beta, marketing_* included, not just
`kill_switch`), the identical technique `staff_revert_capability_registry_entry` uses for its own
"restore the immediately-prior version" job. This was chosen over storing the pre-kill field values
directly on `capability_kill_events` (which would have worked, but would duplicate a restore
mechanism this schema already has, tested, and trusted) — one restore mechanism, two callers (revert
and auto-revert), exactly what Job 3's restructure makes possible (see below).

**Reconciling §20.6.1's "auto-reverts... unless ratified" against "there is no indefinite kill" —
read together, documented as a judgment call, not silently resolved one way.** Taken in isolation,
bare ratification appears to remove the 24-hour ceiling entirely, which would make an indefinitely
re-ratified kill possible — directly contradicting the row two lines below it. This migration reads
ratification and extension as two DIFFERENT actions: ratification is a single additional admin's
agreement (clears the 4-hour escalation flag, nothing else); only a completed two-person EXTENSION,
with its own stated and bounded (24h-from-its-own-request) new expiry, ever moves the deadline. This
is the one place in this task where the source document's own two rows are in tension and a reading
had to be chosen — recorded here explicitly, with the reasoning, rather than picked silently.

**Extension is maker-checker (propose + approve), reusing CTL-07 rule 1's shape exactly.** §20.6.1
says "only by the two-person path" without specifying the mechanism. Rather than invent a new shape,
this migration reuses the propose/approve pattern `capability_change_requests`/`capability_change_
approvals` already established for ordinary changes — a `capability_kill_extension_requests` row
(one admin, a stated new expiry, a reason) finalised by a `capability_kill_extension_approvals` row
(a second, DISTINCT admin). Consistency with an already-tested, already-understood pattern was
preferred over a new one.

**Affected/live channel counts are caller-supplied, not computed.** §20.6.1's own row names them as
part of the log; computing them live would mean iterating every channel's resolved entitlement for
this capability, which is exactly the per-capability query CTL-03's resolved-blob cache (migration
`0149`) exists to make impossible from the API layer. §20.6's own text places "every change previews
an impact count" as a separate, already-decided-to-exist admin-UI feature (CTL-04/05, a different
repository) — this migration takes the count as an input the caller (that future UI) supplies, the
same way `reason` is already a caller-supplied value on every governance action in this schema.

**Job 3's restructure — extract, don't guard.** The first attempt guarded `staff_set_capability_
registry_entry` directly with an "if the capability already exists, reject" check at the top of the
function. `packages/db/tests/ctl_registry_spec_alignment.sql`'s own CTL-08 assertions caught the
break immediately: `staff_revert_capability_registry_entry` calls that same function to restore a
capability's prior version, and reverting is explicitly legitimate under §20.6 even though the
capability obviously already exists. The fix — extracting the write body into an unguarded internal
helper (`set_capability_registry_entry_unchecked`, never granted to `bsa_app`) and putting the new
governance check ONLY on the public entry point — was chosen because it makes the distinction the
code actually needs explicit: "single-admin, immediate, ANY state" (revert, and Job 2's own
auto-revert) versus "single-admin, immediate, CREATE ONLY" (the public PUT route). A parameter flag
("skip the check") on one function was considered and rejected: it would leave the governance check
reachable-but-optional from the SAME public surface, one missed default away from reintroducing the
exact bypass this job exists to close. Two functions with two different grants makes the distinction
structural, not a flag a future caller could forget to set.

**Fixing the two existing test files this restructure affects, not routing around them.**
`packages/db/tests/ctl_registry_spec_alignment.sql` (migration `0153`'s own test) called
`staff_set_capability_registry_entry` repeatedly on the SAME existing capability key to construct
intermediate states for its own CTL-08 revert proof, and once to simulate engaging a kill switch for
its allowlist-precedence proof — both patterns the new governance check now correctly rejects. Three
call sites were changed: the kill-switch simulation now calls `staff_kill_capability_now` (the real,
unaffected kill path); the two state-construction calls now call the internal unchecked helper
directly, reachable only because that test file runs as the database superuser (the same posture it
already relies on to directly `INSERT` into `capability_allowlist`, a table also revoked from
`bsa_app`). Neither change weakens what that file proves — CTL-08 revert's own behaviour is
unchanged, and the file's assertions about it are unchanged; only the SETUP mechanism for two
intermediate states moved to account for the new rule.
`packages/db/tests/ctl_change_management.sql` (migration `0152`'s own test) had its existing "two
staff + one owner" proof marked delta (`...6c04`) as the approver without any owner-identity concept
existing yet. Delta is now marked `is_platform_owner = true` in that file's own fixture so the
existing proof continues to prove what it always claimed to (an owner approval succeeding), and a
new sixth user (`...6c05`, admin but not owner) was added to prove the negative case that file could
not previously express.

**The gap Job 3 leaves is reported, not quietly worked around.** After this restructure, there is NO
governed path anywhere in this schema for changing `kind`/`limits`/`beta`/`marketing_*` on an
EXISTING capability — migration `0153`'s own header already recorded that these six fields are not
threaded through `0152`'s propose/approve/apply workflow, and this task does not build that
extension (a real, separately-scoped follow-up). Closing the single-admin bypass on the ORIGINAL five
fields necessarily closes it on all twelve, because `staff_set_capability_registry_entry` is one
function covering the whole §20.2 row — narrowing the new check to "only the five governance-
sensitive fields" was considered and rejected as inventing a field-level distinction §20.6's own text
("every capability change") does not make.

## Verification

See `../tests/TC-CTL-07-emergency-kill-and-owner-identity.md` for the acceptance criteria and the
full "Commands run" table with real, freshly-executed numbers: SQL suite 79/0 (baseline 78/0), API
865/0 (baseline 852/0), web 644/0 (unchanged), typecheck 0 errors, contracts 127 paths/148 operations
(+8/+8 from this task's own measured pre-change baseline of 119/140 at this checkout — see that
file's own note on the discrepancy against the dispatch instructions' stated 117/137), explain 31/31
(baseline 30/30), harness pass.

## Blockers surfaced, not worked around

1. **Notification and billing exemption (§20.6.1) are not built.** Neither mechanism exists anywhere
   in this schema to attach to — no Companion/email dispatch primitive for "tell this channel's
   creator," and no billing/metering read anywhere in `apps/api/src` consults
   `capability_registry.kill_switch` at all. Recorded precisely, including what each would attach to
   when built, in the task record's own "what was not built" section.
2. **`kind`/`limits`/`beta`/`marketing_*` have no governed change path for an existing capability**,
   now that the single-admin bypass on them is closed along with the original five fields (see
   above). A follow-up extending `0152`'s propose/approve/apply workflow to cover them — mirroring
   `0153`'s own `staff_set`/`get`/`list` split — is the correct fix, not something to invent here.
3. **ADM-07 (admin MFA) remains unaudited**, the same blocker the owner-identity decision record's
   own "what this does not decide" section already named. §20.6.1's "MFA already satisfied" row is
   unaffected by this migration either way; it depends on ADM-07, which this task does not touch.

## 2026-09-18 correction review — legacy route removed

Fresh reachability review found the legacy ordinary HTTP kill route invoked
`staff_kill_capability_now` without this record's expiry, second-admin ratification, escalation or
post-incident review. It has been removed from Fastify registration, the domain/store interface,
OpenAPI and tests. The negative route test, full local pipeline and route inventory passed; the only
remaining API-reachable kill is the bounded event-sourced emergency flow. CTL-13 now supplies its
durable passkey gate. This is a self-review and does not close the separate notification, billing,
live-impact or independent-external-review gaps named above.
