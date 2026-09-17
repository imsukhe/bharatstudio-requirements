# Platform owner identity — owner decision, 2026-09-17

**Owner:** Sukhdev Singh
**Status:** `Approved`
**Authority:** `FULL-PRODUCT-DEFINITION.md` §20.6, §20.6.1 · register row `CTL-07` ·
`active/launch/00_LAUNCH_SCOPE_AUTHORITY.md` (*"Database projections and RLS enforce this
boundary; UI hiding alone is insufficient"*)

## The question

§20.6 requires **"owner sign-off for moving a paid capability into Free"** and §20.6.1 escalates
an unratified emergency kill **"to the owner at the 4-hour mark"**. An owner distinct from a
platform admin is therefore required in two separate places.

`public.app_users` carries only `is_platform_admin` (migration `0073`). Migration `0152`
consequently authorises `approval_kind='owner'` with the *same* check as `'staff'` — so the
three-distinct-person control is real (a UNIQUE constraint forces separate approvers) but
**nothing verifies that the owner approver is the owner.**

## The decision

**One owner for now, expandable later.**

## The shape that implements it

The capability and the restriction are deliberately carried by *different* objects, so that
expanding later is a constraint change and never a data migration:

| Concern | Mechanism |
|---|---|
| **Capability** — who is an owner | `public.app_users.is_platform_owner boolean not null default false` |
| **"One, for now"** | A partial unique index admitting at most one true row |
| **Expanding later** | **Drop the index.** The column, every grant, every approval row and all history stay exactly as they are |

Modelling it as a singleton table, or hardcoding an owner id, would make expansion a schema and
data change. A flag plus a droppable constraint makes it a one-line change.

## Two rules that follow, and are not inferable from "add a flag"

1. **An owner approval requires `is_platform_owner` AND `is_platform_admin`.** §20.6 states the
   whole panel is *"behind platform-admin auth with MFA (ADM-07)"*, so an owner who is not an
   admin cannot reach the panel to approve anything. The two flags are orthogonal in the schema
   and conjoint at the approval check — being owner does **not** imply admin, and the check
   demands both rather than assuming one.
2. **Owner is never self-conferred.** Whatever sets `is_platform_owner` is audited like every
   other capability change. An admin who can promote themselves to owner has dissolved the
   distinction the flag exists to create.

## What this does NOT decide

Nothing about ADM-07's MFA itself, which remains absent and unaudited. Owner identity makes the
*authority* check correct; it does not make the *authentication* stronger. `CTL-13` still
depends on `ADM-07`, which has never been audited — verify it before building the admin UI.
