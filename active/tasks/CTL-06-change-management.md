# CTL — change management, phase 2 Lane A (rows CTL-06, CTL-07, CTL-08, CTL-09)

**Status:** `Implemented — verification recorded, review pending`
**Owner:** **Sukhdev Singh**
**Authority:** `../../FULL-PRODUCT-DEFINITION.md` §31.19 rows `CTL-06`, `CTL-07`, `CTL-08`, `CTL-09` ·
`active/launch/00_LAUNCH_SCOPE_AUTHORITY.md` (*"Database projections and RLS enforce this
boundary; UI hiding alone is insufficient."*) · `governance/AGENTS.md` (append-only correction
discipline)
**Predecessor:** `CTL-01-capability-control-plane.md` (phase 1, migration `0149`, landed
`518d592`) — this task extends the registry that migration built; it does not modify it.

## Why this is Lane A of CTL phase 2

`CTL-01-capability-control-plane.md`'s own phase-2 table assigns Lane A (`CTL-06`/`07`/`08`/`09`)
to this repository's API, genuinely parallel with Lane B (`CTL-10`/`11`/`12`, public capability
matrix) and Lane C (`CTL-04`/`05`/`13`, admin UI + MFA, a different repository) because the three
lanes touch disjoint files and disjoint concerns. `CTL-09`'s row ("layer 1 correctness dimensions
rejected from this panel") is the one row in this group that is genuinely load-bearing rather than
a workflow nicety: it is `CTL-14`'s exact structural mechanism, extended to the one new surface
that can originate a `capacity_class` value outside the phase-1 registry's own write function.

## Scope — migration `0152`, one governance layer over `capability_registry`

| Row | What it requires | What was built |
|---|---|---|
| `CTL-06` | A change can be authored now and take effect later | `capability_change_requests.effective_at`, staged in the future or defaulted to now; applied lazily on the next read through this plane (no scheduler required for correctness) |
| `CTL-07` | Two-staff approval on every change; owner sign-off for paid→Free moves; single-admin `global_kill` for incidents | Three separately-enforced authority rules — see below |
| `CTL-08` | One-action revert to the previous version | `app_private.staff_revert_capability_registry_entry`, one call, restores the immediately-prior `capability_registry_audit` snapshot as a NEW forward version |
| `CTL-09` | The panel rejects Layer 1 correctness dimensions | `capability_change_requests.proposed_capacity_class` carries the identical closed whitelist as `capability_registry.capacity_class` (`CTL-14`) |

### `CTL-07`'s three rules, each with its own mechanism

1. **Two-staff, maker-checker.** `app_private.staff_approve_capability_change` requires two
   DISTINCT `is_platform_admin()` approvers of `approval_kind = 'staff'`
   (`UNIQUE(change_request_id, approver_id)` on `capability_change_approvals` plus an explicit
   count check) before status can reach `approved`. The proposer of a change is explicitly
   rejected from approving their own change.
2. **Owner sign-off, paid→Free only.** `requires_owner_signoff` is computed once, at propose
   time: true only when an EXISTING capability whose current `min_tier` is `pro`/`creator`/
   `studio` is proposed to move to `null`/`free`. When true, `approved` additionally requires
   `>=1` approval of kind `owner`.
3. **Single-admin `global_kill`.** `app_private.staff_kill_capability_now` requires only ONE
   `is_platform_admin()` caller and applies immediately — it never enters the
   `pending_approval`/staff-approval machinery at all. "`global_kill`" here reaches
   phase-1's existing PER-CAPABILITY `kill_switch` through a fast single-admin path; there is no
   separate all-capabilities master switch anywhere in this schema, and one was not invented for
   this row (see Blocker below for the related, but distinct, identity gap).

### The blocker this task surfaces rather than works around

`app_users` carries exactly ONE staff concept — `is_platform_admin` (boolean, migration `0073`).
There is no `is_platform_owner` or any rank distinguishing "the platform owner" from ordinary
platform staff, and `app_private.has_channel_role`'s owner/admin/... roles are PER CHANNEL,
meaningless for a platform-wide `capability_registry` row. `approval_kind = 'owner'` is therefore
authorised by the SAME `is_platform_admin()` check as `'staff'` — the WORKFLOW STEP (a distinct,
required, explicitly-invoked third approval, structurally separated from the two staff approvals
by `UNIQUE(change_request_id, approver_id)` forcing three different people) is real and enforced;
the IDENTITY check behind "owner" is not, because the distinction does not exist in this schema
yet. Per this task's own constraint ("if the distinction you need does not exist, that is a
blocker to report, not a role to mint"), no `is_platform_owner` column was added. Fixing this is a
follow-up task with its own authority record — not something to invent inside a change-management
migration.

## What this task does NOT do

- Does NOT migrate the seven existing hand-rolled gates onto the registry.
- Does NOT build the admin UI, impact preview, or admin MFA (`CTL-04`/`05`/`13` — Lane C, a
  different repository).
- Does NOT build the public capability matrix or marketing wiring (`CTL-10`/`11`/`12` — Lane B).
- Does NOT modify migration `0149`, `0150`, or any `SAF-*`/`GOA-*` record. Every reference to
  `CTL-01`/`02`/`03`/`14`/`15` in migration `0152` is a read of that migration's existing shapes.
- Does NOT touch `apps/web/app/overlay/canvas/` — `getSubscriberCount()` remains 16.

## Reuse anchors

| Value / shape | Reused from |
|---|---|
| `app_private.is_platform_admin` (staff gate, every function) | `packages/db/migrations/0073_v1_l03_admin_dlq_tooling.sql:38` |
| `app_private.current_user_id` | `packages/db/migrations/0002_v1_security_rls_archive.sql` |
| The ONE registry write path (`app_private.staff_upsert_capability_registry_entry`) — never a parallel mutation of `capability_registry` | `packages/db/migrations/0149_v1_ctl_capability_control_plane.sql` |
| `capacity_class` closed whitelist (CTL-14's mechanism), copied verbatim onto `proposed_capacity_class` | `packages/db/migrations/0149_v1_ctl_capability_control_plane.sql` |
| Session-scoped transaction (`set_config('app.user_id', ...)`) store pattern | `apps/api/src/db/admin-store.ts`, `apps/api/src/db/staff-creator-pack-review-store.ts` |
| Platform-admin route gate (`requirePlatformAdmin`), same unavailable-503 posture | `apps/api/src/routes/admin.ts` |
| Append-only correction discipline ("correct them with linked compensating records"), applied to registry history for `CTL-08` | `governance/AGENTS.md` |

## Verification

See `../../tests/TC-CTL-06-change-management.md` for acceptance criteria and the full "Commands
run" table with real, freshly-executed numbers, and `../../reviews/2026-09-17-ctl-change-
management-implementation.md` for the implementation record and design decisions.
