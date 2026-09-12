# L24 — Companion action catalogue and standalone mode

**Status:** `Server catalogue, entitlement/activation gate, macOS OBS wiring, and standalone-entitlement schema built and locally test-suite-green — Windows OBS UI unbuilt and the Windows target has never compiled; nothing in this task is proven in a deployed environment`
**Level:** L3
**Owner:** [OWNER — API/native desktop helpers, unassigned]
**Depends on:** L07 (pairing, secure storage, control-session lease — all already built)
**Blocks:** Companion being sold separately (Part 13, decision 9, per master plan) — decision 9 is now DECIDED (2026-09-07: Companion is a separate product, price configurable); Part 13 decision 11 (Companion's required rename) is now unblocked and unresolved, see below
**Test record:** [`../tests/TC-L24-companion-action-catalogue-and-standalone-mode.md`](../tests/TC-L24-companion-action-catalogue-and-standalone-mode.md)

## Authority and evidence

Master plan Part 6, "L24 — Companion action catalogue and standalone mode" (lines ~1179–1276), including the two-layer entitlement/activation gate, the action catalogue table, and the "every Companion route is channel-scoped" resolution (implicit channel provisioning, no second scope); Part 7 §7.11 (Companion feature register, items 23–28 owned by this task). Existing constraint: migration `0041` restricts `companion_commands.action` to exactly `pause_queue`, `resume_queue`, `send_test_alert` (verified in `bharatstudio-alerts`); migration `0042` validates layout slots against "active same-channel queue targets" only.

## Objective

Turn Companion's fixed three-action contract into a conditional catalogue: show Alerts actions when the account actually runs Alerts, show OBS/Mirror/Stream actions to everyone, gated on a two-layer entitlement × activation check — without building a second scope or authorization model.

## Current implementation evidence — 2026-09-07

Verified by reading the code and running the drift-check script (no test suite re-run performed in this repo; counts below are the last-known local pass counts, not re-executed here per this repo's own no-runtime-output rule).

- **Migration `bharatstudio-alerts/packages/db/migrations/0089_v1_l24_companion_action_catalogue.sql`** widens `companion_commands_v1_action_check` (kept `NOT VALID`) from the three original actions to **seventeen**, across four groups: alerts (`pause_queue`, `resume_queue`, `send_test_alert`), obs (`obs_set_scene`, `obs_toggle_source`, `obs_toggle_mute`, `obs_start_stream`, `obs_stop_stream`, `obs_start_record`, `obs_stop_record`, `obs_save_replay_buffer`, `obs_set_transition`), mirror (`mirror_start`, `mirror_stop`, `mirror_screenshot`), stream (`stream_go_live`, `stream_end`); `app_private.companion_action_group()` maps every action to its group.
- **Migration `0093_v1_l24_companion_activation_signals.sql`** adds the activation signals: `helper_paired`, `obs_connected` (45-second staleness window), `payment_account_connected`; `mirror_reachable` and `stream_paired` are modelled as always-`false` because nothing reports them yet.
- **Migration `0100_v1_l24_companion_entitlement_separation.sql`** adds the `companion_grant_policies` data table (`source_key`, `granted`, `action_limit`, `action_groups`) making Companion entitlement independent of and configurable apart from the Alerts tier — per its own in-migration comment, unbundling an Alerts plan from Companion becomes "one UPDATE per source_key," not a migration; a per-channel `channel_entitlement_versions.values.companionActionGroups` override (0089) still takes precedence when present. Seeded to be behavior-identical to pre-0100 defaults.
- **Target-type validation** (task 2) is enforced in SQL, but as conditional logic inside a SECURITY DEFINER function rather than as a `target_type` column with a per-type CHECK. `app_private.update_companion_layout` (`packages/db/migrations/0089_v1_l24_companion_action_catalogue.sql:320-348`) rejects an Alerts slot that carries a `targetLabel` at all, requires an Alerts target to be a UUID of a queue that is open **and belongs to the calling channel**, requires OBS slots to carry a bounded printable-ASCII `targetLabel` of 1-200 characters, and permits mirror/stream slots to carry neither. `apps/api/src/routes/companion.ts:196` maps those exceptions to `companion_layout_target_shape_invalid` — the route translates the error, it does not own the rule.

  This is a **deviation in mechanism from the task's original wording** ("give 0042's layout slots a target-type discriminator"), and it is recorded as such — but it is not a weaker guarantee, and an earlier draft of this record wrongly described it as application-layer-only. The layout table has no direct write grant, so the definer function is the only write path; and the rule is genuinely conditional per action group (Alerts slots must NOT carry a label, OBS slots MUST), which a single column CHECK expresses poorly. A discriminator column would still be worth adding if a second write path ever exists.
- **Two-layer gate** implemented in `bharatstudio-alerts/apps/api/src/routes/companion.ts` (`/actions` route): Layer 1 entitlement (`resolveEntitledGroups`, server-authoritative catalogue membership) and Layer 2 activation (reading the Companion state endpoint's live signals) are separate checks; the client picker/grid is documented and coded as convenience only.
- **Allowlist mirrored in five hand-maintained places**, enforced by `bharatstudio-alerts/scripts/companion-action-catalogue-drift-check.mjs`: (1) migration 0089's SQL CHECK + `companion_action_group()`, (2) `apps/api/src/routes/companion.ts` (`ACTION_GROUPS`), (3) `bharatstudio-companion-desktop/macos/Sources/BharatStudioCompanionMacOS/CompanionPolicy.swift`, (4) `bharatstudio-companion-desktop/windows/CompanionPolicy.cs`, (5) `bharatstudio-companion-mobile/src/api/CompanionApi.ts`. Run directly during this reconciliation: all five sources report 17 actions with matching groups — `No drift: every parsed source has the same action set with the same group assignments.` — exit 0.
- **macOS**: `bharatstudio-companion-desktop/macos/Sources/BharatStudioCompanionMacOS/CompanionOBSActionMapper.swift` wires the previously-unused `OBSWebSocketClient.swift` through the fixed allowlist; `CompanionOBSStatusReporter.swift` reports OBS connection status on a 15-second heartbeat (`heartbeatIntervalSeconds: TimeInterval = 15`).
- **Windows gap, stated plainly**: `bharatstudio-companion-desktop/windows/MainWindow.xaml` has no OBS UI section at all — its only OBS-related text is a single placeholder InfoBar message ("Pair this helper from BharatStudio before any local OBS control is enabled"). The WinUI target has **never been compiled**: `windows/README.md` records `dotnet build` failing with `NETSDK1100` on this (macOS) development machine, "expected — Windows targeting requires a Windows build agent." Only the portable pairing/policy/contract logic (`CompanionPolicy.cs` and siblings) is verified, via a smoke-test project, not the WinUI target itself.
- Test-suite pass counts as last recorded locally (not re-executed in this pass): `apps/api` 285/285, `apps/web` 187/187, SQL suite 36/36, macOS 34/34, mobile 79/79, marketing 8/8, poller build+vet clean across 7 packages. Total migrations: 102 (`bharatstudio-alerts/packages/db/migrations`, confirmed by direct listing).
- None of the above has been proven in a deployed environment — no staging or production run, no real OBS-instance handshake against the shipped mapper, no Windows build artifact. That gate is L09's, not this task's, and remains unmet.

## Tasks

1. Migration: extend the `0041` CHECK allowlist beyond the three existing actions. Keep it `NOT VALID` for the reason it already is — historical command rows stay append-only evidence.
2. Migration: give `0042`'s layout slots a target-type discriminator with per-type validation (OBS actions carry a different target shape than queue targets); scene/source/input/transition names are free text and need the same bounds treatment every other `0042` field received.
3. Entitlement: add OBS / Mirror / Stream action groups to the tier matrix using the existing per-tier list pattern (the same pattern as `allowedQueueModes`) — this does not need a ninth entitlement dimension.
4. Activation state: extend the Companion state endpoint (which already returns overlay connection and pending count) to add payment-account-connected, helper-paired, OBS-connected, Mirror-reachable, Stream-paired.
5. Implicit channel provisioning on signup through a Companion entry point — no new non-channel scope.
6. Generic OBS control in the native helpers (macOS SwiftUI, Windows WinUI 3) behind the existing paired, signed, scoped command boundary.
7. Catalogue UI: picker filtered by entitlement, grid slots disabled by activation, with an explanation of *why* a slot is disabled — never a silent grey-out.

## Exact implementation boundary

In scope: the bounded allowlist actions named in the master plan's table — `obs_set_scene`, `obs_toggle_source`, `obs_toggle_mute`, `obs_start_stream`/`obs_stop_stream`, `obs_start_record`/`obs_stop_record`, `obs_save_replay_buffer`, `obs_set_transition`; `mirror_start`/`mirror_stop`/`mirror_screenshot`; `stream_go_live`/`stream_end`. The two-layer gate (entitlement: server-authoritative catalogue membership; activation: Companion state endpoint) exactly as specified. Implicit-channel provisioning for Companion-only signups, reusing the existing channel-as-unit-of-entitlement model — a non-channel scope is explicitly rejected by the master plan ("new routes, new RLS policies, a parallel entitlement path, and two authorization models to keep in sync forever. Rejected.").

Out of scope, permanently: any raw OBS WebSocket passthrough or "flexible" pass-through request surface. The action set is a fixed, server-validated allowlist now and in every future extension — the allowlist is extended, the constraint is never removed.

## Non-negotiable implementation rules

L07's acceptance criteria are the boundary and hold **verbatim** for this task:

> "Desktop helper is local-only, consented, revocable, and has no general-purpose local/public API"

> "no arbitrary command execution"

**How the 17-action allowlist preserves this boundary:** the catalogue is a fixed switch over a closed enum in every layer — the SQL `CHECK` constraint (0089), the API's `ACTION_GROUPS` map, and each native helper's `CompanionPolicy` enum-plus-switch — never a generic request forwarder or raw OBS WebSocket passthrough. Growing the allowlist from 3 to 17 actions changes which enum members exist; it does not add a code path that accepts an arbitrary command string, a raw WebSocket frame, or an unvalidated target. `companion-action-catalogue-drift-check.mjs` exists specifically so the five hand-maintained mirrors of that closed enum cannot silently diverge into something broader than what the server allows.

In addition, specific to this task:

- Gating is two-layer, always: entitlement (may this action exist in the catalogue at all — server-authoritative) **and** activation (is the thing this action points at actually live — via the Companion state endpoint). Neither layer alone is sufficient; gating on "is Alerts subscribed?" alone is explicitly wrong, because Free is an Alerts subscription at ₹0 and a paid subscriber without a connected payment account would otherwise see live-looking queue buttons.
- The client-side filter (picker/grid) is convenience only, never authority — every action the client can send must be rejected server-side unless both layers pass.
- No historical `companion_commands` row is rewritten or deleted by any migration in this task.
- Every Companion route stays channel-scoped. A Companion-only signup gets an implicit channel with no payment account connected and no tip page published — never a second, parallel scope.
- A disabled action slot must show *why* it is disabled (which layer failed) — a silent grey-out is not acceptable.

## Open questions — not decided here

1. **Companion's rename (Part 13, decision 11).** Master plan `docs/BharatStudio-MASTER-PLAN.md` Part 13, decision 11: "NOW REQUIRED — unblocked by decision 9" (decision 9, 2026-09-07, made Companion a separate product). *Bitfocus Companion* owns the term in the OBS-controller category; internal collisions also exist (L13's "CompanionApp TCP 27190"; `companion-desktop/windows-mirror-test/` belongs to Mirror). Needed before any store listing or marketing page ships. Owner: [OWNER], unassigned.
2. **Whether Companion's price is bundled with Alerts or sold standalone** remains deliberately open per the 2026-09-07 owner decision (master plan 3.13) — `companion_grant_policies` (0100) makes this configurable by data, not schema, but no pricing decision has been made.
3. **Windows compilation.** No Windows build agent exists in this environment; the WinUI target's actual buildability is unverified beyond the portable logic layer. This blocks any Windows release-readiness claim, independent of the rename/pricing questions above.

## Definition gate

Per `governance/AGENTS.md`, L3 work stops after definition pending explicit scope/acceptance/affected-files/data-impact/test-plan/rollback approval. Owner unassigned: [OWNER]. Note: substantial implementation already exists (see Current implementation evidence above); this gate note is preserved because the task file's owner/approval fields were never formally closed, not because the code is unbuilt.

## Acceptance criteria

Status per criterion — see `../tests/TC-L24-companion-action-catalogue-and-standalone-mode.md` for the acceptance-case-level detail:

- A Companion-only account with no payment connection sees zero Alerts actions and a working OBS grid. **Code path exists** (`companion.ts` two-layer gate, 0100's channel-scoped entitlement); not proven against a real deployed signup in this reconciliation.
- A Free Alerts account sees its queue controls enabled and OBS controls disabled until a helper is paired. **Code path exists** (`obs_connected`/`helper_paired` in 0093); not proven against a real deployed account.
- Every action the client can send is rejected server-side unless both layers pass — the client filter is convenience, never authority. **Built**; direct-API bypass test claimed in the `apps/api` 285/285 count (not re-run in this reconciliation — see evidence caveat below).
- Layout validation rejects an OBS action whose target shape does not match its action type. **Built**, in SQL, at `0089_v1_l24_companion_action_catalogue.sql:320-348` (see task 2 for why the mechanism differs from the original wording).
- No historical `companion_commands` row is rewritten or deleted by any migration in this task. **Confirmed**: both 0089 and 0093/0100 are additive/`NOT VALID` migrations; no `DELETE`/destructive `UPDATE` against historical rows found in either file.
- L07's verbatim constraints continue to pass under L07's own existing test suite after this task's changes — no regression. **Not independently re-run in this reconciliation**; last-known-green counts cited above, not re-executed.

## Evidence required for closure

Inline prose citation, now largely satisfied by the Current implementation evidence section above: migration filenames `0089_v1_l24_companion_action_catalogue.sql` (17-action allowlist, `NOT VALID`), `0093_v1_l24_companion_activation_signals.sql` (activation signals), `0100_v1_l24_companion_entitlement_separation.sql` (`companion_grant_policies`, standalone entitlement); `apps/api/src/routes/companion.ts` (two-layer gate, entitlement tier matrix, Companion state endpoint); native OBS control at `bharatstudio-companion-desktop/macos/Sources/BharatStudioCompanionMacOS/{CompanionOBSActionMapper,OBSWebSocketClient,CompanionOBSStatusReporter}.swift` (macOS, built) and `bharatstudio-companion-desktop/windows/CompanionPolicy.cs` (Windows, portable logic only — no OBS UI, WinUI target never compiled); catalogue UI mirrored in `bharatstudio-companion-mobile/src/api/CompanionApi.ts` and the drift-checked web/mobile sources; `bharatstudio-alerts/scripts/companion-action-catalogue-drift-check.mjs`, run directly during this reconciliation — exit 0, 17 actions, 5 sources, no drift. Remaining gap: exact pass/fail counts for the specific acceptance-case-level tests (e.g. the direct-API bypass test, the target-type-mismatch rejection test) were not re-run or individually re-cited in this pass — only whole-suite last-known counts are available (see status line and evidence caveat above). No artifact/screenshot directory.

## Rollback

All three migrations (0089, 0093, 0100) are additive/`NOT VALID` extensions of existing constraints — no historical `companion_commands` or layout row is rewritten or deleted (confirmed by direct reading: no `DELETE`/destructive `UPDATE` against historical rows in any of the three). The OBS/Mirror/Stream action groups can be removed from the tier matrix independently of the Alerts action set, reverting to today's three-action contract without any data loss. `companion_grant_policies` (0100) is a new, additive data table; reverting standalone-entitlement behavior is an UPDATE to that table's seed rows, not a migration rollback. Implicit channel provisioning uses the existing channel table and entitlement model, so it introduces no new schema to roll back beyond a provisioning-source flag. The Windows gap (no OBS UI, uncompiled WinUI target) carries no rollback risk because nothing shipped there to roll back. No production migration or deployment has occurred; none of this has been proven in a deployed environment.

## Batch 8 amendment — 2026-09-07 (post-reconciliation)

No new L24 migration shipped in batch 8: `packages/db/migrations` still shows only `0089`, `0093`, `0100` for L24 (repo total is now 106 migrations, up from 102, entirely from other lanes — L16's `0105`, L20's `0106`, L03's `0103`/`0104`). The target-shape-validation correction already recorded above in this file stands unchanged. Windows gap (no OBS UI, WinUI target never compiled) is unchanged. No update to real test counts is recorded here beyond the repo-wide figures cited in this reconciliation's other task files, since no L24-owned code changed.

## Security correction — 2026-09-09

Self-audit found that the API interpreted an explicit empty or malformed
`channel_entitlement_versions.values.companionActionGroups` value as if the
override were absent. The documented precedence rule is that an explicit
override always wins, so this could have fallen through to a permissive live
Companion policy. `apps/api/src/routes/companion.ts` now treats key presence as
the override selector and fails closed to an empty group set for empty or
malformed values. The direct API regression test proves both cases return
`403 companion_action_group_not_entitled` before action activation/execution.

This is an API-only authorization correction: no migration or stored data was
changed. Rollback is a code revert only, though reverting would reintroduce
the fail-open policy-precedence defect and is therefore not recommended.
See `reviews/2026-09-09-L24-explicit-override-fail-closed-review.md` for the
finding, evidence, and remaining release gates.
