# ADM-07 — a durable admin registry, and ONE admin identity: implementation record

**Date:** 2026-09-17
**Owner:** **Sukhdev Singh**
**Authority:** `../FULL-PRODUCT-DEFINITION.md` §20.6/§20.6.1 · register rows ADM-07, CTL-13
**Task:** `../active/tasks/ADM-07-durable-admin-registry.md`
**Acceptance:** `../tests/TC-ADM-07-durable-admin-registry.md`
**Predecessors:** `2026-09-17-ctl-emergency-kill-implementation.md` (migration `0155`) — the
never-self-conferred/audited/mandatory-reason write-path shape this task reuses for admin, and the
`reject_table_mutation()` append-only trigger function this task's own audit table reuses without
recreating.

---

## What this task is, in one paragraph

Two admin identities existed with nothing reconciling them: `bharatstudio-admin` (a separate
Next.js repository) authorised by `process.env.PLATFORM_ADMIN_EMAILS`, entirely independent of any
database; every platform-staff SQL function in `bharatstudio-alerts` authorised by
`app_private.is_platform_admin()`, reading `public.app_users.is_platform_admin` (migration `0073`),
which the console never referenced. Migration `0156` adds the one thing `0073` never built — a
governed, audited, self-conferral-safe application-layer WRITE path for that already-durable column
(`app_private.staff_set_platform_admin` + `public.platform_admin_audit` + a list function) — without
touching `is_platform_admin()` itself, so every `0149`-`0155` authorisation check keeps working
unmodified. `bharatstudio-admin` is then wired to ask the API's new `GET /v1/admin/whoami` (backed
by the SAME column) instead of its own env var, via a real BharatStudio session obtained by
exchanging the signed-in Google identity through the alerts API's existing `POST
/v1/auth/google/exchange`. No MFA mechanism is built; what exists instead is an honest audit of
what MFA would require and a fix to console copy that previously implied it was already enforced.

## Schema design decisions, and why each shape was chosen

**`is_platform_admin()` is reused verbatim, not restructured — the central design decision of this
task.** The most invasive fix available was to introduce a new `admin_registry` table and repoint
every `0149`-`0155` function's authorisation check at it. That was rejected immediately: it would
have required editing five migrations' worth of already-shipped, already-tested functions for a
problem that was never "the database's source of truth is wrong" — `app_users.is_platform_admin`
already WAS the correct, single source of truth for every one of those functions. The actual defect
was narrower and entirely upstream of `is_platform_admin()`: no governed way existed to WRITE that
column, and a second system never asked the database at all. Fixing the actual defect (add a write
path; wire the console to read the existing one) leaves `is_platform_admin()`'s signature and
semantics byte-for-byte unchanged, which is also why "every `0149`-`0155` staff function still
authorises correctly" did not need to be re-derived per function — it follows structurally from not
having touched the one thing they all call.

**The audit table reuses `0155`'s trigger function instead of declaring its own.**
`app_private.reject_table_mutation()` (installed by migration `0155` for `platform_owner_audit` and
the five `capability_kill_*` tables) is a generic, parameterless "this table is append-only, for
every role, unconditionally" trigger function — nothing about it is specific to ownership or kill
events. Migration `0156`'s own header notes it is reused, not recreated, and the migration contains
no new `CREATE FUNCTION ... reject` of its own. This is the smallest correct change: one new
`CREATE TRIGGER` line referencing an existing function, versus duplicating trigger logic that would
then need its own proof of correctness.

**Self-conferral is a blanket `actor <> target` check, not a grant-direction-specific one — and
this is what let a planned lockout guard be DELETED rather than kept.** The first draft of
`staff_set_platform_admin` carried an explicit "if this revocation would leave zero admins, reject"
check, modelled on a real operational concern (a legitimate chain of revocations bricking the
registry). Working through the actual reachable states during implementation found that check could
never fire: the function already requires the caller to be `is_platform_admin()`, and already
rejects `actor = target_user_id` unconditionally (covering self-revocation, not only
self-promotion) — so on every call that reaches the write, the acting admin is necessarily a
surviving admin distinct from the target. The dead branch was removed and replaced with a structural
explanation in the migration header, on the principle that a check that can never execute is worse
than no check: it invites false confidence and untested code paths. This is recorded here as a
design correction made DURING implementation, not merely a decision made in advance.

**The bootstrap problem is left exactly where it already was, not "solved."** A tempting fix would
have been a policy like "if the registry is empty, the first caller may self-grant." That was
rejected outright: it is the identical self-conferral hole `0155`'s owner rule exists to close,
reopened conditionally. Because `is_platform_admin` had ZERO write path before this task (every test
fixture in this repository seeds it by direct `INSERT`), the honest baseline is that raw database
access was ALREADY the only way to become the first (or, before this task, ANY) admin. This task
narrows that gap to exactly "the first admin only" rather than removing it, and says so plainly in
both the migration header and the task record, rather than describing the bootstrap step as solved
when it structurally cannot be, by design, without reopening self-conferral.

## The console fix, and a defect found while implementing it, not before

The task's own audit (pre-supplied) correctly identified that `bharatstudio-admin` never referenced
`app_users`/`is_platform_admin`, and pointed at `src/lib/admin-api.ts`'s existing bearer-token
forward as the path to reuse rather than replace. Implementing "just make that forward carry the
right token" required first establishing what token it WAS carrying, which surfaced a second,
previously unrecorded defect: in the non-bootstrap branch, `admin-api.ts` forwarded the console's own
`next-auth`-signed session-token cookie as the `Authorization: Bearer` value sent to the alerts API.
Reading `apps/api/src/auth/session-store.ts` shows `SessionStore.lookup()` only recognises opaque
tokens it minted itself via `app_private.create_user_session` (SHA-256-hashed and matched against
`user_sessions`) — there is no code path anywhere in the API that can verify a `next-auth` JWT. That
bearer forward could never have succeeded against a real deployment; only the `NODE_ENV=development`
escape hatches (`bsa_admin_session` cookie / `BSA_ADMIN_AUTO_LOGIN`) were ever reachable end-to-end.
This means the console's admin-data-fetching surfaces (DLQ, entitlements, plans, audit, alert
catalogue) were, before this task, only ever exercised in local development or with a shared static
token — a finding this task surfaces rather than silently working around, since it changes what
"the existing bearer-token path" actually was.

**The fix is a token exchange, reusing an existing endpoint, not a new auth system.** `POST
/v1/auth/google/exchange` (`apps/api/src/routes/auth.ts`) already existed — it is how every other
Google-authenticated BharatStudio client (the main creator/viewer apps) obtains a real, verifiable
session from a Google `id_token`. `next-auth`'s own `account` object already carries that
`id_token` on first sign-in; `auth.ts`'s `jwt` callback now calls the exchange endpoint and stores
the resulting access token on the JWT. This was chosen over minting a second, admin-console-specific
session mechanism (e.g., a custom JWT the API would need a NEW verification path for) specifically
because the task instructions warned against inventing a second path when one already existed and
worked — the previous code's bug was which token it forwarded, not that forwarding a bearer token
was the wrong shape.

**The email allowlist is removed from sign-in, not narrowed.** A middle option — keep
`PLATFORM_ADMIN_EMAILS` as a coarse pre-filter at Google sign-in, on top of the new database check —
was considered and rejected. Keeping it, even as a "belt and suspenders" pre-filter, keeps a second
place admin status can be recorded and can drift from the database again, which is precisely the
defect this task exists to close. `signIn` no longer branches on it at all; any Google account may
authenticate, and `hasAdminSession()`'s real `GET /v1/admin/whoami` call is the ONLY authorisation
decision, made once. `src/lib/admin-policy.ts` (and its test) were deleted rather than left as dead
code, on the same reasoning — unused allowlist code sitting in the repository is exactly the kind of
thing a future change could accidentally wire back in.

## MFA — an honest scope decision, not a stub

§20.6 and §20.6.1 both state MFA is already a gate ("behind platform-admin auth with MFA", "with MFA
already satisfied"). Grepping `bharatstudio-alerts/apps/api/src` and this repository for
`mfa`/`totp`/`two-factor`/`authenticator` returns nothing. Building any part of an MFA flow — even a
minimal one — was rejected outright: a provider, an enrolment flow, and a recovery-code policy are
none of them decided anywhere in this product's authority documents, and inventing any of the three
would be exactly the kind of unauthorised business decision this task's own hard constraints forbid
("no invented MFA provider, no invented recovery-code count, no invented session lifetime"). A
half-built MFA screen that does not actually gate anything would be worse than no MFA screen at all
— it would let the console's own UI imply a security property that does not hold, which is precisely
what was found and fixed instead: login-page copy, a bootstrap-login error message, and the README's
status line all claimed or implied MFA was already enforced. Each was corrected to state plainly that
it is not, with a pointer to this task record for what remains undecided, and named integration
points (a step-up challenge alongside the new Google-exchange sign-in flow; a second pre-handler
alongside `requirePlatformAdmin` on the API, most directly `staff_fire_global_kill`) recorded for
whenever those decisions are made.

## What was not built, and why

- **A "manage admins" UI page in `bharatstudio-admin`.** The grant/revoke/list API
  (`PUT`/`GET /v1/admin/platform-admins`) exists and is tested at the route layer, but Job 2's actual
  ask — "make the console use it" — was read as fixing the console's AUTHORISATION wiring, not
  building a new operational screen nobody asked for. Building one would have been scope expansion
  beyond what either the register row or the task instructions named.
- **Any MFA mechanism.** See above.
- **A "don't revoke the last admin" runtime guard.** Removed after being found unreachable — see the
  schema design section above.
- **Widening migration `0152`'s propose/approve/apply workflow, or `CTL-04/05/13`/`CTL-10/11/12`.**
  Explicitly out of scope per this task's own instructions; not touched.

## Verification

`../tests/TC-ADM-07-durable-admin-registry.md` carries the full acceptance criteria and the "Commands
run" table with real, freshly-executed numbers (SQL suite against a real `postgres:16-alpine`
container; `apps/api`/`apps/web` typecheck and test suites; `bharatstudio-admin`'s own `tsc`/`vitest`;
contracts/explain/harness checks).

## Independent review

Not performed as a separate pass in this session — self-review only, per `governance/AGENTS.md`'s
"if independent review is unavailable, say so, self-review, and leave the task `Conditionally
complete`" instruction. This task's `Status` line reflects that: `Implemented — verification
recorded, review pending`.
