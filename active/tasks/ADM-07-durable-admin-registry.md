# ADM-07 — a durable admin registry, and ONE admin identity (register row ADM-07, §20.6)

**Status:** `Implemented — verification recorded, review pending`
**Owner:** **Sukhdev Singh**
**Authority:** `../../FULL-PRODUCT-DEFINITION.md` §20.6 and §20.6.1 · register row ADM-07 ("Admin
OIDC + MFA, durable admin registry (vs allowlist)") · register row CTL-13 ("Admin MFA + durable
admin registry (ADM-07 dependency)")
**Predecessors:** `CTL-01-capability-control-plane.md` (migration `0149`, `app_private.
is_platform_admin()` first consumed) · `CTL-07-emergency-kill-and-owner-identity.md` (migration
`0155`, the identical write-path/audit/self-conferral shape this task reuses for admin, having
already built it for owner) — both read-only authority here.

## Why this task exists

Two admin identities existed with nothing reconciling them:

1. `bharatstudio-admin` (the Next.js console, a separate repository) authorised every login and
   every API call by `isPlatformAdminEmail(email)` against `process.env.PLATFORM_ADMIN_EMAILS` — an
   env var, entirely independent of any database.
2. Every platform-staff function in migrations `0149`-`0155` (in `bharatstudio-alerts`) authorises
   by `app_private.is_platform_admin()`, which reads `public.app_users.is_platform_admin` (migration
   `0073`). The admin repository never referenced `app_users` or `is_platform_admin` at all.

A person could be an admin in one system and not the other, silently, in either direction. Separately,
`is_platform_admin` (migration `0073`) had every READ path already (every `0149`-`0155` staff
function calls it unconditionally) but ZERO application-layer WRITE path — `bsa_app` holds `SELECT`
only on `app_users` (`0003_v1_l03_application.sql:494`), so every SQL test fixture in this repository
seeds the column by direct `INSERT`, because there has never been any other way to become an admin,
first or second, in application code.

## Scope — three jobs, in the order the register row lists them

| Job | What it requires | What was built |
|---|---|---|
| 1 — durable registry, database side | The database becomes the source of truth; the env allowlist stops deciding authorisation; grants/revocations audited and append-only (`0155`'s `platform_owner_audit` posture); never self-conferred; the bootstrap problem named and handled honestly | Migration `0156`: `public.platform_admin_audit` (append-only via the SAME `app_private.reject_table_mutation()` trigger function `0155` installed, reused not recreated) + `app_private.staff_set_platform_admin` (the ONE write path, never self-conferred in either direction, requires an existing admin, mandatory reason, audited) + `app_private.staff_list_platform_admins` (read). `app_private.is_platform_admin()` itself (migration `0073`) is UNTOUCHED — same table, same column, same body |
| 2 — the console uses it | `bharatstudio-admin` authorises against the durable registry, not `PLATFORM_ADMIN_EMAILS`; reuse the existing bearer-token path (`src/lib/admin-api.ts`) rather than inventing a second one | API: `apps/api/src/routes/platform-admin.ts` (`PUT`/`GET /v1/admin/platform-admins`) + `GET /v1/admin/whoami` (added to `apps/api/src/routes/admin.ts`, reusing the existing `requirePlatformAdmin` gate). Admin repo (uncommitted, separate repository): `auth.ts` now exchanges the signed-in Google `id_token` for a real BharatStudio session via `POST /v1/auth/google/exchange` and carries the resulting access token on the NextAuth JWT; `PLATFORM_ADMIN_EMAILS`/`isPlatformAdminEmail` removed from both the `signIn` callback and `admin-api.ts`; `hasAdminSession()` now calls `GET /v1/admin/whoami` for real |
| 3 — MFA, scoped honestly | Build only what is genuinely decidable; do not invent a provider, enrolment flow or recovery-code policy | **Nothing built.** No MFA provider, enrolment flow or recovery-code policy has been decided anywhere in this product's authority documents — see "MFA: what is missing, precisely" below. Misleading copy claiming MFA was already enforced (login page, bootstrap-login error message, README) was found and corrected to state plainly that MFA is not yet implemented, rather than left to imply otherwise |

## Job 1 — the durable registry, exactly what changed and why nothing else did

**`app_private.is_platform_admin()` is not replaced, restructured, or pointed at a new table.** It
already read the correct, durable source (`public.app_users.is_platform_admin`) before this task —
that boolean already backed every `0149`-`0155` authorisation check. The finding was never "the
database doesn't know who is an admin"; it was "the database has no governed way to make someone an
admin, and a second system (the console) never asked it anyway." Migration `0156` therefore adds
exactly one write function and one read function, and changes zero lines of `0073`'s or any other
migration's existing functions. This is the reason every `0149`-`0155` staff function keeps
authorising correctly without being touched: they call `is_platform_admin()`, which is unchanged.

**Never self-conferred, in both directions — and why that makes a lockout guard unnecessary rather
than merely present.** `app_private.staff_set_platform_admin` requires the caller to already be an
admin, and rejects `actor = target_user_id` for both a grant and a revoke (the same blanket rule
`0155`'s `staff_set_platform_owner` uses). A first version of this migration also carried an explicit
"do not revoke the last admin" guard; it was removed once the review noticed it was unreachable dead
code — since the acting admin can never target themselves, the acting admin is, by construction,
always a surviving admin distinct from whatever row is being written, on every call that reaches the
write. Zero-admin lockout is consequently impossible through this function structurally, not merely
guarded against, and the migration's own header documents this rather than shipping a check that
could never fire.

**The bootstrap problem, named rather than papered over.** `staff_set_platform_admin` requires the
CALLER to already be `is_platform_admin()` — by construction it can never create the FIRST admin,
for any actor, including one targeting themselves when the registry is empty. There is no
"if empty, allow it" branch anywhere in the function, because that branch is exactly the
self-conferral hole `0155`'s owner rule was written to close, and a bootstrap exception would
silently reopen it the moment the registry were ever fully revoked. The honest state of the world
after this migration: the FIRST platform admin in any deployment is still, and can only ever be, set
by direct database access — the same access level required to run this migration file itself, and
the SAME access level that was already the only way to set `is_platform_admin` at all before this
task (every fixture in this repository has always seeded it by direct `INSERT`). What changes is
everything AFTER the first admin: before `0156`, every subsequent admin also required raw SQL,
unaudited, with no self-conferral check, no reason, no append-only trail. After `0156`, every admin
from the second onward is granted through a governed, audited, self-conferral-safe function, callable
through the API layer.

## Job 2 — the console, and why the fix is a token-exchange, not a new auth system

Auditing `admin-api.ts` before this task found the "existing bearer-token path" the task instructions
pointed at was not actually reachable in production: `authToken()`'s non-bootstrap branch forwarded
the console's OWN `next-auth` session-token cookie (a locally-signed JWT) as the `Authorization:
Bearer` value sent to the alerts API. The API's `SessionStore.lookup()` (`apps/api/src/auth/
session-store.ts`) only recognises opaque access tokens it minted itself via `app_private.
create_user_session` (hashed and stored in `user_sessions`) — it has no code path that can verify a
`next-auth` JWT at all. That bearer forward would have failed `lookup()` on every real request; only
the `NODE_ENV=development` bootstrap-cookie/auto-login escape hatches were ever reachable end-to-end.

The fix reuses the SAME mechanism every other Google-authenticated BharatStudio client already uses
to obtain a session: `POST /v1/auth/google/exchange` (`apps/api/src/routes/auth.ts`), which verifies
a Google `id_token` and mints a real, `SessionStore`-backed access token. `auth.ts`'s `jwt` callback
now performs that exchange on every Google sign-in (using the `id_token` `next-auth`'s own `account`
object already carries) and stores the resulting access token on the JWT; `admin-api.ts` forwards
THAT token as the bearer, unchanged in every other respect from the "call the API with a bearer
token" shape the task pointed at. `hasAdminSession()` now calls the new `GET /v1/admin/whoami` (gated
by the SAME `requirePlatformAdmin` pre-handler as every existing `/v1/admin/*` route) instead of a
local string comparison — reaching a `200` there is the entire authorisation decision, made once, in
the database.

`PLATFORM_ADMIN_EMAILS` and `isPlatformAdminEmail` are removed from `auth.ts`'s `signIn` callback and
from `admin-api.ts` entirely (`src/lib/admin-policy.ts` and its test are deleted — nothing else
imported them). Any Google account may now complete sign-in; whether it can use the console is
decided exactly once downstream, against the database. This is the deliberate shape of "the env
allowlist stops being an authorisation decision" — decoupling authentication (proving identity) from
authorisation (deciding access), rather than keeping two gates that could drift again.

## Job 3 — MFA: what is missing, precisely

§20.6 states the whole capability panel is *"behind platform-admin auth with MFA (ADM-07)"* and
§20.6.1 states `global_kill` may be fired by *"any platform admin, alone, with MFA already
satisfied."* Auditing this repository and `bharatstudio-alerts/apps/api/src` found zero matches for
`mfa`/`totp`/`two-factor`/`authenticator` anywhere. Nothing here builds any part of that. Specifically
undecided, and consequently not invented:

- **Provider.** No MFA provider (TOTP via an authenticator app, WebAuthn/passkeys, SMS, a third-party
  identity platform) has been chosen anywhere in this product's authority documents.
- **Enrolment flow.** No decision exists for when enrolment is required (at first admin grant? at
  next sign-in? a grace period?), what happens to an admin who never enrols, or whether enrolment is
  self-service or admin-assisted.
- **Recovery-code policy.** No decision exists on whether recovery codes exist, how many, their
  format, storage, or single-use semantics.
- **Session lifetime under MFA.** No decision exists on whether an MFA challenge is per-sign-in,
  time-boxed, or step-up-only for sensitive actions (e.g. `global_kill`).

What this task changed instead, to stop the console and its own documentation from implying MFA is
already enforced: the login page's copy ("use Google with your organization's MFA policy"), the
production bootstrap-login error message ("use Google with MFA in deployed environments"), and the
README's status line all claimed or implied MFA protection that does not exist. Each was corrected to
state plainly that MFA is not yet implemented and to point at this task record for what remains
undecided. **What MFA would attach to, once decided:** the natural integration points are (a)
`auth.ts`'s Google sign-in flow, as an additional step-up challenge before or alongside the
`POST /v1/auth/google/exchange` call this task added, and (b) a second `requireMfaSatisfied`-shaped
pre-handler alongside `requirePlatformAdmin` on `apps/api/src/routes/*` (most directly
`staff_fire_global_kill`, per §20.6.1's own wording) — neither exists today, and this task does not
scaffold either, per its own instruction not to build a stub that looks like MFA.

## Existing guards preserved, unchanged by this task

`CTL-14`/`CTL-15`/`CTL-03` (migration `0149`) — untouched, migration `0156` adds no `capacity_class`-
or retention-bearing column anywhere. `0151`'s `payment_decision`/`stored_record_decision`
`CHECK (= 'allow')` — untouched, out of this task's reach. `0155`'s owner singleton index and
owner+admin conjoint rule — untouched; re-proven with a smoke check in this task's own SQL test
(`adm_admin_registry.sql`), full proof remains `ctl_emergency_kill_and_owner.sql`'s. `apps/web/app/
overlay/canvas/` — untouched; `getSubscriberCount()` remains 16.

## What this task does NOT do

- Does NOT build `CTL-04/05/13` (admin UI capability panel, impact preview, admin MFA enforcement)
  or `CTL-10/11/12` (public capability matrix, marketing wiring) — other lanes, explicitly out of
  scope per this task's own instructions.
- Does NOT widen migration `0152`'s change-management workflow.
- Does NOT build any MFA mechanism — see Job 3 above.
- Does NOT build a "manage admins" UI page in `bharatstudio-admin` — the grant/revoke/list API exists
  (`PUT`/`GET /v1/admin/platform-admins`) for future use, but no console screen consumes it yet; only
  the console's AUTHORISATION wiring (Job 2's actual ask) was changed.
- Does NOT touch `apps/web/app/overlay/canvas/`.
- Does NOT commit anything in `bharatstudio-admin` — that repository's changes are left in its
  working tree for separate review, per this task's own instruction.

## Reuse anchors

| Value / shape | Reused from |
|---|---|
| `app_private.is_platform_admin` (untouched) | `packages/db/migrations/0073_v1_l03_admin_dlq_tooling.sql:38` |
| `app_private.reject_table_mutation()` append-only trigger function | `packages/db/migrations/0155_v1_ctl_emergency_kill_and_owner.sql` (reused, not recreated) |
| Never-self-conferred / audited / mandatory-reason write-path shape | `app_private.staff_set_platform_owner`, `packages/db/migrations/0155_v1_ctl_emergency_kill_and_owner.sql` |
| Session-scoped transaction store pattern | `apps/api/src/db/platform-owner-store.ts` |
| `requirePlatformAdmin` route gate, same 503-unavailable posture | `apps/api/src/routes/platform-owner.ts` |
| Real BharatStudio session minting from a Google identity | `POST /v1/auth/google/exchange`, `apps/api/src/routes/auth.ts` |

## Verification

See `../../tests/TC-ADM-07-durable-admin-registry.md` for acceptance criteria and the full "Commands
run" table with real, freshly-executed numbers, and `../../reviews/2026-09-17-adm-07-implementation.md`
for the implementation record and design decisions.
