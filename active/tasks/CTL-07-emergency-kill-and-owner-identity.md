# CTL — emergency kill in full, and real platform-owner identity (row CTL-07, §20.6.1)

**Status:** `Implemented — verification recorded, review pending`
**Owner:** **Sukhdev Singh**
**Authority:** `../../FULL-PRODUCT-DEFINITION.md` §20.6 and §20.6.1 in full · register row `CTL-07` ·
`reviews/2026-09-17-platform-owner-identity-decision.md` (owner decision, binding) ·
`active/launch/00_LAUNCH_SCOPE_AUTHORITY.md` (*"Database projections and RLS enforce this
boundary; UI hiding alone is insufficient"*)
**Predecessors:** `CTL-01-capability-control-plane.md` (phase 1, migration `0149`) ·
`CTL-06-change-management.md` (phase 2 Lane A, migration `0152`) — both read-only authority here.
Migration `0153` (§20.2 field set) is extended, not modified.

## Why this task exists

Two blockers were surfaced, not solved, by earlier CTL work and are closed here:

1. `CTL-06-change-management.md`'s own "Blocker" section: `approval_kind = 'owner'` was authorised
   by the same `is_platform_admin()` check as `'staff'` — no `is_platform_owner` concept existed.
2. Migration `0152` built the single-actor kill action and the mandatory reason; §20.6.1 specifies
   far more (hard expiry, auto-revert, ratification, escalation, bounded extension, an immutable
   log, and a mandatory post-incident review that blocks further kills). None of that was built.

A third, previously undetected bypass was found while implementing this task and is closed in the
same migration: `staff_set_capability_registry_entry` (migration `0153`) let a single platform
admin change `min_tier`/`kill_switch`/`rollout_percentage`/`limits`/`capacity_class` on an
**existing** capability immediately, bypassing §20.6's two-person approval and the paid→Free owner
sign-off entirely.

## Scope — migration `0155`, three jobs

| Job | What it requires | What was built |
|---|---|---|
| 1 — owner identity | `is_platform_owner`, "one for now, expandable later," owner+admin conjoint, never self-conferred | `app_users.is_platform_owner` + a partial unique singleton index (`app_users_platform_owner_singleton_idx` — drop it to expand, no data migration); `app_private.staff_set_platform_owner` (never self-conferred, audited in `platform_owner_audit`); `app_private.staff_approve_capability_change` (migration `0152`) now also requires `app_private.is_platform_owner()` for `approval_kind='owner'` |
| 2 — emergency kill | §20.6.1's full table: expiry, auto-revert, ratification, escalation, extension, immutable log, review, never-a-tier-change | Five new tables (`capability_kill_events` and four related, each append-only via a structural trigger) and eight new functions (`staff_fire_global_kill`, `staff_ratify_kill_event`, `staff_propose_kill_extension`, `staff_approve_kill_extension`, `staff_file_kill_review`, `staff_get_kill_event`, `staff_list_kill_events`, plus the shared internal helpers) |
| 3 — close the bypass | Two-person approval for every capability change, still allow revert | `app_private.set_capability_registry_entry_unchecked` (new, internal, ungoverned) + `staff_set_capability_registry_entry` (now rejects any call on an EXISTING capability) + `staff_revert_capability_registry_entry` (now calls the unchecked helper directly) |

## Job 1 — the platform owner identity, exactly as decided

`reviews/2026-09-17-platform-owner-identity-decision.md` is the binding shape; this migration
implements it verbatim, adding nothing beyond it:

- `public.app_users.is_platform_owner boolean not null default false`.
- **"One, for now"** is a partial unique index (`create unique index ... on app_users
  (is_platform_owner) where is_platform_owner`), not a singleton table and not a hardcoded id —
  every row the index admits carries the same value (`true`), so uniqueness alone forces at most
  one. Expanding later is dropping that one index; no data migration, no column change, no history
  rewrite.
- **Owner+admin conjoint.** `app_private.staff_approve_capability_change` requires
  `is_platform_admin()` at the top of its body for every approval kind (unchanged from `0152`), and
  additionally requires `app_private.is_platform_owner()` only for `approval_kind='owner'`. The two
  flags are orthogonal in the schema; being owner does not imply admin, and an owner who is not also
  an admin is rejected at the SAME gate every other caller is, before the owner-specific branch is
  ever reached.
- **Never self-conferred.** `app_private.staff_set_platform_owner` rejects `actor = target_user_id`
  (403), requires `is_platform_admin()`, requires a non-empty reason, and records every change in
  `public.platform_owner_audit` — itself append-only via the same structural trigger every new table
  in this migration uses (see Job 2 below). `bsa_app` holds no `UPDATE` grant on `app_users` at all
  (`0003_v1_l03_application.sql:494`, `SELECT` only), so this function is not merely the recommended
  path, it is the only reachable one.

## Job 2 — §20.6.1's emergency kill path, row by row

Every value below is copied verbatim from §20.6.1's own table; none is invented.

| §20.6.1 row | Value | Mechanism |
|---|---|---|
| Who may fire | Any platform admin, alone, MFA already satisfied | `app_private.staff_fire_global_kill` — no approval round |
| What it does | Off immediately; creator settings/data/history untouched | Sets only `kill_switch`; every other field read from the current row and passed straight through unchanged |
| Reason required | Mandatory, refused without one | `char_length(trim(reason)) > 0` |
| Maximum duration | 24 hours, auto-reverts at expiry unless ratified | `expires_at` is always exactly `fired_at + 24 hours` (a `CHECK` constraint, not a convention); read-time auto-revert (below) |
| Ratification | A second admin within 4 hours; unratified still runs to 24h but escalates to the owner at 4h | `capability_kill_ratifications`, `UNIQUE(kill_event_id)`, firer excluded; `escalated_to_owner` computed read-time |
| Extension | Only the two-person path, a stated new expiry; no indefinite kill | `capability_kill_extension_requests` (propose) + `capability_kill_extension_approvals` (approve, a second distinct admin); each grant capped at its own request time + 24 hours |
| Logging | Immutable, append-only: actor, timestamp, capability, reason, affected/live counts, ratifier, expiry, revert | `capability_kill_events` + the four related tables, each carrying a `BEFORE UPDATE OR DELETE` trigger that raises unconditionally for every role |
| Notification | Told same-hour in Companion/email; never billed for an off capability | **Not built** — neither mechanism exists in this schema; see "What was not built" below |
| Post-incident review | Mandatory within 72 hours, written, attached; unreviewed blocks the actor's next kill | `capability_kill_reviews`, `UNIQUE(kill_event_id)`; `staff_fire_global_kill` itself refuses a new fire (409/`55000`) while any prior kill by the same actor has no review row |

**Reconciling two rows, stated explicitly.** "Auto-reverts... unless ratified" and "no indefinite
kill" are read together, not independently: bare ratification records agreement and clears the
4-hour escalation flag, but does NOT by itself move the expiry — only a completed two-person
EXTENSION, with its own stated and bounded new expiry, does that. This is a judgment call
reconciling two decided rows in the same table, not an invented value; both numbers used (24h, 4h)
are the ones §20.6.1 states. See migration `0155`'s own header for the full reasoning.

**Read-time correctness, no sweeper required.** `app_private.apply_due_kill_revert` runs at the
start of every read/write entry point (via the shared `capability_kill_event_row` helper), the same
CTL-06 discipline migration `0152` established for staged changes. A kill event past its effective
expiry is restored to its exact pre-kill state (via the `capability_registry_audit` snapshot
captured at fire time, the identical technique CTL-08 revert already uses) on the very next plain
read — proven in the SQL test with no apply/sweep call anywhere in that test.

**Never a tier, limit or pricing change — structurally.** `staff_fire_global_kill`'s parameter list
is `(capability_key, reason, affected_channel_count, live_channel_count)` — there is no
`min_tier`/`limits`/`rollout_percentage`/`capacity_class` parameter anywhere on it or on any other
Job 2 function, so such a change cannot be requested through this path even by accident. Proven via
`information_schema.parameters`, the same technique CTL-14/CTL-09 use for their own whitelists.

### What was not built, named precisely rather than invented

Neither the Companion/email notification nor the billing exemption ("never billed for a capability
that is off") has a mechanism to attach to anywhere in this schema today: no notification-dispatch
primitive exists for "tell this channel's creator something happened," and no billing/metering read
anywhere in `apps/api/src` consults `capability_registry.kill_switch` at all — there is no call site
to add a guard to. Both are real, bounded follow-up work (an outbox-shaped dispatch on
`capability_kill_events` insert for the first; a `kill_switch` guard in whatever metering read is
eventually built for the second), not stubbed or simulated here.

## Job 3 — closing the single-admin bypass, by restructuring, not guarding

An inline guard was prototyped inside `staff_set_capability_registry_entry` and reverted: it broke
CTL-08 revert, which legitimately calls that same function to restore a prior audited state. The fix
extracts the write body into `app_private.set_capability_registry_entry_unchecked` (internal, never
granted to `bsa_app`), puts the new governance check only on the public
`staff_set_capability_registry_entry` (rejects any call on a capability that already exists), and
routes both `staff_revert_capability_registry_entry` (CTL-08) and Job 2's own auto-revert-at-expiry
through the unchecked helper directly — both are restoring a known prior audited state, never
proposing a fresh ungoverned one.

**The gap this leaves, named rather than papered over.** `kind`/`limits`/`beta`/`marketing_*`
(§20.2's six fields migration `0153` added) are not threaded through migration `0152`'s
propose/approve/apply workflow — that was already true before this task (`0153`'s own header records
it as a bounded follow-up). After this job, that is the ONLY governed path §20.6 describes for those
six fields, and it does not exist yet for them — so an admin cannot change them on an EXISTING
capability through any path in this schema until that follow-up is built. Not solved here: §20.6
says "every capability change," and this task takes that at its word rather than carving out a
narrower, unauthorised exception.

## Existing guards preserved

`CTL-14` (`capacity_class` closed whitelist, migration `0149`) — untouched, no new
`capacity_class`-bearing column added anywhere. `CTL-03` (`bsa_app` has zero table-level grant on
any capability-registry-family table) — every new table in this migration follows the identical
posture. `CTL-15` (no per-tier retention field) — `capability_kill_events.expires_at` and
`capability_kill_extension_requests.new_expires_at` are kill-event deadlines (how long an ADMIN
ACTION stays in effect), not data-retention windows on anything a creator owns; re-proven
structurally over this migration's own new tables in the SQL test, not merely asserted in prose.
`0151`'s `payment_decision`/`stored_record_decision` `CHECK (= 'allow')` — untouched, out of this
migration's reach. `apps/web/app/overlay/canvas/` — untouched; `getSubscriberCount()` remains 16.

## What this task does NOT do

- Does NOT build `CTL-04/05/13` (admin UI, impact preview, admin MFA) or `CTL-10/11/12` (public
  capability matrix, marketing wiring) — other repositories/lanes.
- Does NOT build the Companion/email notification or the billing kill-switch guard — see above.
- Does NOT extend migration `0152`'s propose/approve/apply workflow to cover `kind`/`limits`/`beta`/
  `marketing_*` — a real, bounded, separately-scoped follow-up.
- Does NOT touch `apps/web/app/overlay/canvas/`.

## Reuse anchors

| Value / shape | Reused from |
|---|---|
| `app_private.is_platform_admin` | `packages/db/migrations/0073_v1_l03_admin_dlq_tooling.sql:38` |
| `app_private.current_user_id` | `packages/db/migrations/0002_v1_security_rls_archive.sql` |
| CTL-06 read-time-correctness discipline (lazy apply ahead of every read, no sweeper) | `packages/db/migrations/0152_v1_ctl_change_management.sql` |
| CTL-08's restore-from-audit-snapshot technique | `packages/db/migrations/0152_v1_ctl_change_management.sql` |
| CTL-07 rule 1's maker-checker shape (propose + approve, two distinct people) | `packages/db/migrations/0152_v1_ctl_change_management.sql` |
| Session-scoped transaction store pattern | `apps/api/src/db/capability-change-management-store.ts` |
| `requirePlatformAdmin` route gate, same 503-unavailable posture | `apps/api/src/routes/capability-change-management.ts` |

## Verification

See `../../tests/TC-CTL-07-emergency-kill-and-owner-identity.md` for acceptance criteria and the
full "Commands run" table with real, freshly-executed numbers, and
`../../reviews/2026-09-17-ctl-emergency-kill-implementation.md` for the implementation record and
design decisions.
