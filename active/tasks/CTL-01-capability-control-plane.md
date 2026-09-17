# CTL — the capability control plane (phase 1: registry, resolver, guards)

**Status:** `Approved for implementation — phase 1 dispatched 2026-09-17`
**Owner:** Sukhdev Singh
**Authority:** `../../FULL-PRODUCT-DEFINITION.md` **§20 (the control plane — this is the specifying section)**, §12.6, §31 register rows `CTL-01`–`CTL-15` ·
`active/launch/00_LAUNCH_SCOPE_AUTHORITY.md` (v1 channel read permissions; *"UI hiding alone is
insufficient"*)
**Predecessor:** `reviews/2026-09-17-slice-7-hostile-code-review.md` and the verified area audit
that established CTL at **0 of 15 usable**

## Why this is first in Track A

Verified at `bharatstudio-alerts` `7d8682f`: **no capability registry, resolver, resolved-blob
cache, admin surface or public matrix endpoint exists anywhere in the repository.**

What exists instead is **seven hand-rolled entitlement functions**, each invented per feature:

```
app_private.events_pack_entitled          app_private.sticker_tier_rank
app_private.soundboard_module_entitled    app_private.template_tier_rank
app_private.soundboard_tier_rank          app_private.canvas_layout_tier_rank
app_private.vertical_canvas_layout_entitled
```

**Four of those seven were written on 2026-09-17**, in a single day, by four different lanes —
which is the clearest possible evidence of the problem. Every new gated feature currently mints
its own tier ladder. Building more features before the control plane means writing each gate
twice: once bespoke now, once again when it is migrated onto the registry.

## Phase 1 scope — one lane, deliberately not parallel

`CTL-01` · `CTL-02` · `CTL-03` · `CTL-14` · `CTL-15`. Migration **`0149`**.

These five are one subsystem, not five tasks: `CTL-02`'s resolver reads `CTL-01`'s table,
`CTL-03` caches what `CTL-02` resolves, and `CTL-14`/`CTL-15` are structural constraints **on**
that table rather than features beside it. Splitting them across lanes would reproduce exactly
the four merge-splice classes that cost hours on 2026-09-17, for no parallelism gain.

| Row | What it requires |
|---|---|
| `CTL-01` | Capability registry table with **versioned, audited** rows |
| `CTL-02` | Resolution order engine — **kill → denylist → rollout → tier → override**, in that order |
| `CTL-03` | Per-channel **resolved blob**, versioned and cached. *Never per-capability queries* |
| `CTL-14` | The registry **rejects any capability whose subject is a durable creator record** (§12.6) |
| `CTL-15` | Retention is a **single platform-wide value**; the schema offers no per-tier retention field |

### `CTL-14` and `CTL-15` are the load-bearing ones

They are not validation niceties — they are the schema refusing to be able to express a
forbidden thing:

- **`CTL-14`.** §12.6 forbids ever tier-gating storing, viewing, searching, fetching or exporting
  a creator's own durable records. A registry that *can* express "gate record export at Studio"
  is a loaded gun. The rejection must be structural and must be proven by a test that fails when
  the guard is removed — not asserted in a comment.
- **`CTL-15`.** §12.6.2 makes retention a schedule by data class, uniform across tiers. The
  registry must offer **no per-tier retention field at all**, so a per-tier retention limit is
  unrepresentable rather than merely discouraged.

## What phase 1 does NOT do

It does **not** migrate the seven existing hand-rolled gates onto the registry. Those keep
working untouched. Migrating them is a later, separate task with its own record, once the
resolver is proven — swapping live entitlement logic and introducing the plane it swaps onto in
one change would make a failure impossible to attribute.

It does not build the admin UI (`CTL-04`/`05`/`13`), change management (`CTL-06`/`07`/`08`/`09`)
or the public matrix (`CTL-10`/`11`/`12`). Those are phase 2 and are genuinely parallel because
they land in three different repositories.

## Phase 2 — parallel after phase 1 lands

- **Lane A** — `CTL-06` staged effective-time · `CTL-07` two-staff approval, owner sign-off for
  paid→Free, single-admin `global_kill` for incidents · `CTL-08` one-action revert · `CTL-09`
  layer-1 correctness dimensions rejected from the panel → alerts API.
- **Lane B** — `CTL-10` `GET /v1/public/capability-matrix` · `CTL-11` marketing build reads the
  snapshot, webhook revalidation · `CTL-12` `kind = marketing_section` → alerts + marketing repo.
- **Lane C** — `CTL-04` admin UI · `CTL-05` impact preview · `CTL-13` admin MFA + durable admin
  registry → admin repo. **`CTL-13` depends on `ADM-07`, which has not been audited. Verify
  `ADM-07`'s real state before starting Lane C**, or it will be built on an assumption.

## Constraints

- Never invent a numeric limit, price, provider behaviour, legal wording, retention window or
  deployment value. Reuse a decided value and cite file:line, or ship configured-but-unset.
- A tier decision is server-side truth. `00_LAUNCH_SCOPE_AUTHORITY.md`: *"Database projections
  and RLS enforce this boundary; UI hiding alone is insufficient."*
- No state letter is self-assigned. `CTL-*` letters move only after audit.


---

## Implementation note — 2026-09-17

Phase 1 implemented: migration `0149` (`bharatstudio-alerts` `packages/db/migrations/
0149_v1_ctl_capability_control_plane.sql`). Registry, resolver, resolved-blob cache, and both
structural guards (CTL-14 closed-whitelist `capacity_class`, CTL-15 no-retention-column-anywhere)
built and verified against a real `postgres:16-alpine` database. The seven hand-rolled gates
named in this record's own scope section are untouched. No admin UI, change management or public
matrix was built. Full record: `../../reviews/2026-09-17-ctl-phase-1-implementation.md`.
Acceptance: `../../tests/TC-CTL-01-capability-control-plane.md`. `CTL-*` state letters are not
self-assigned here, per this record's own closing line — this note records what was built, not a
state change.


---

## CORRECTION, 2026-09-17 — this record cited the wrong section, and phase 1 paid for it

**This task record originally cited §30. The section that actually specifies the capability
registry is §20** ("The control plane — flags, tiers and limits as data"). Migration `0149`
cites §12.6, §12.6.1, §12.6.2, §30.3, §31 and §7.5 — and **§20 nowhere**, because this record
never sent it there. Everything below follows from that single error. The agents built exactly
what they were briefed, verified their guards and mutation-tested them; the guards are sound.
They were simply measured against the wrong specification.

### Gap 1 — the registry is missing most of §20.2's declared fields

§20.2 lists the row shape explicitly. `0149` shipped `capability_key, capacity_class,
description, kill_switch, rollout_percentage, min_tier, version` and is missing:

| §20.2 field | Consequence of its absence |
|---|---|
| **`kind`** (widget / module / feature / hub_lane / lobby_mode / ai_feature) | `CTL-12` is literally *"marketing sections behind flags (`kind = marketing_section`)"* — **CTL-10/11/12 cannot be built on this registry at all.** `capacity_class` is a different taxonomy: §12.6.1's eight capacity concepts, not §20.2's kinds. Both are needed; neither replaces the other |
| **`limits` jsonb** | §20.1's central promise — *"changing a limit is an audited admin action"* — is unimplementable |
| **`allowlist`** | §20.3 step 3 is *"allowlist / rollout % → on for this channel regardless of tier"*. Only the exclusion half exists, so there is no way to turn a capability **on** below its tier |
| `beta`, `marketing_visible`, `marketing_label`, `marketing_blurb` | `CTL-10`/`11`/`12` have nothing to read |

### Gap 2 — `global_kill` is the dangerous half of §20.6.1 without the rails

§20.6.1 specifies the emergency path completely, and its own reasoning is the tension:
*"Requiring two people to stop an actively harmful capability is how a five-minute incident
becomes a fifty-minute one. Requiring nobody is how an admin silently removes a paid feature."*
Its resolution is **"a single-actor action with a hard expiry and a mandatory second look."**

`0152` built the single-actor action and the mandatory reason. It did **not** build: the
24-hour maximum with auto-revert, ratification by a second admin within 4 hours, escalation to
the owner at 4 hours, the immutable log carrying affected and live channel counts plus ratifier
and expiry, creator notification with "never billed for a capability that is off", or the
72-hour post-incident review that blocks further kills by that actor.

**So one admin can currently switch a capability off for every channel and nothing brings it
back or forces a second look.** That is exactly the failure §20.6.1 exists to prevent, and it
is the highest-priority item in CTL.

### Gap 3 — the owner concept is required by the document, not optional

§20.6 requires *"owner sign-off for moving a paid capability into Free"* and §20.6.1 escalates
an unratified kill *"to the owner at the 4-hour mark"*. An owner distinct from a platform admin
is required in two places. `app_users` carries only `is_platform_admin` (migration `0073`), so
`approval_kind='owner'` is currently authorised by the same check as `'staff'`.

### Disposition

`CTL-01` and `CTL-07` are **NOT done** and their register letters do not move. Migration `0153`
brings the registry to §20.2's field set and completes §20.3's resolution order; migration
`0154` builds §20.6.1 properly together with the owner identity. `CTL-10`/`11`/`12` stay
blocked until `kind` and the marketing fields exist.


---

## Implementation note — 2026-09-17, migration 0153

Migration `0153` implemented: `bharatstudio-alerts` `packages/db/migrations/
0153_v1_ctl_registry_spec_alignment.sql`. Closes both gaps this record's own correction section
named: `capability_registry` gained `kind`, `limits`, `beta`, `marketing_visible`,
`marketing_label`, `marketing_blurb` (§20.2), and `public.capability_allowlist` gives §20.3's
resolution order its missing "on for this channel regardless of tier" stage, positioned after
denylist and ahead of rollout/tier, proven not to beat kill or denylist and proven to beat both
rollout-exclusion and tier. `capacity_class` (CTL-14's own column) is untouched and kept
alongside `kind`, deliberately not collapsed into it. CTL-14 and CTL-15 re-verified over the
widened schema. Migration 0152's own functions are untouched except
`staff_revert_capability_registry_entry` (body-only, external signature unchanged), which now
restores the six new fields from the prior version too. The two-staff-approved CTL-06/07
propose/approve/apply workflow itself is NOT widened to stage/approve the six new fields in this
migration — they are settable only through the immediate single-admin
`staff_set_capability_registry_entry` (same posture as the existing kill/revert endpoints) —
reported as scoped out, not half-built. `kind`'s §20.2 enum does not contain
`marketing_section`, which CTL-12 needs; not invented here, reported as a blocker. Full record:
`../../reviews/2026-09-17-ctl-registry-spec-alignment-implementation.md`. Acceptance:
`../../tests/TC-CTL-01-registry-spec-alignment.md`. Per this record's own closing line, `CTL-*`
state letters are not self-assigned here — this note records what was built, not a state change.
