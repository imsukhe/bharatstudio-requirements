# CTL — the capability control plane (phase 1: registry, resolver, guards)

**Status:** `Approved for implementation — phase 1 dispatched 2026-09-17`
**Owner:** Sukhdev Singh
**Authority:** `../../FULL-PRODUCT-DEFINITION.md` §12.6, §30, §31 register rows `CTL-01`–`CTL-15` ·
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
