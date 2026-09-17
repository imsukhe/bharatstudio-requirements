# ADM-07 — the one-time, audited admin bootstrap seed (register row ADM-07, §20.6)

**Status:** `Implemented — verification recorded, review pending`
**Owner:** **Sukhdev Singh**
**Authority:** `../../reviews/2026-09-17-three-owner-decisions-goa17-marketing-bootstrap.md` §3
(binding) · `ADM-07-durable-admin-registry.md` (migration `0156`, read-only predecessor — this task
does not touch it) · `CTL-07-emergency-kill-and-owner-identity.md` (migration `0155`, the owner +
append-only audit pattern this task reuses).

## Why this task exists

`app_private.staff_set_platform_admin` (migration `0156`) requires the caller to already be a
platform admin, and has no empty-registry branch — proven behaviourally in
`packages/db/tests/adm_admin_registry.sql`'s own "BOOTSTRAP" section (zeroing the registry, then
showing both self-targeting and third-party grants fail `42501` for every caller, with no special
case). A fresh deployment therefore has no admin and no reachable way to create one except direct
database access. This predates `0156`; `0156` neither introduced it nor fixed it — its own header
names the gap and defers it explicitly.

## What was built

Migration `0159`: `app_private.staff_bootstrap_platform_admin()`, a single SQL function.

**Inert whenever any admin exists.** The very first check, before configuration is even read, is
whether any `app_users` row already has `is_platform_admin = true`. If so, the function returns
`seeded=false, reason_code='admin_already_present'` and does nothing else — no config read, no
write, no audit row. This is what makes it safe to call on every deploy, forever, without becoming
a second standing authorisation path.

**Identity source — a deployment-provided value, configured but unset by default.**
`current_setting('app.bootstrap_admin_email', true)` — the same custom-GUC convention already used
in this codebase for request-scoped identity (`app.user_id`, `app.channel_id`,
`app.overlay_session_id` — migration `0002`; `app.viewer_id` — migration `0084`), used here at
deployment scope instead (e.g. `alter database ... set app.bootstrap_admin_email = '...'`, set by
infra/ops outside application code, before or after this migration runs). `missing_ok=true` returns
`NULL`, not an empty string and not a guessed default, when unset — "unset" is a real,
distinguishable state, not an invented sentinel.

**Not a new identity concept.** The configured value is matched against
`public.app_users.email`/`email_verified` — the exact column the Google sign-in exchange
(`apps/api/src/auth/google.ts`, `POST /v1/auth/google/exchange`) already populates via
`app_private.create_user_session` (migration `0075`), normalised the same way `google.ts` already
normalises it (`trim().toLowerCase()`) before comparison, and only when Google verified it — the
same trust bar `0075`'s own upsert logic uses. No new column, no new table, no new identity shape.

**Cannot bootstrap a user who has never signed in.** If the configured email matches no existing,
verified, non-closed `app_users` row, the function is a no-op
(`reason_code='bootstrap_identity_not_found'`) — it does not create a user and installs no trigger
to defer the write to a future sign-in. The operator is expected to have the intended first admin
sign in once, then (re-)run the function; re-running it is always safe (see INERT above).

**Audited like any other grant.** `public.platform_admin_audit` (`0156`) is not altered — no new
column. The bootstrap row uses the same five audited fields `staff_set_platform_admin` writes, and
is rejected by the same `platform_admin_audit_append_only` trigger (`app_private.
reject_table_mutation`, installed by `0155`, reused unmodified by `0156` and again here) on any
later `UPDATE`/`DELETE`.

**Distinguishable from an ordinary grant, structurally.** `staff_set_platform_admin` rejects
`actor = target_user_id` unconditionally, so `changed_by = target_user_id` can never appear on a row
it writes. The bootstrap row is the one case with no other admin to act as a distinct actor, so it
records `changed_by = target_user_id` by construction — an unforgeable signature through the
governed path — plus a fixed reason-text marker (`'ADM-07 BOOTSTRAP SEED (migration 0159): ...'`)
for a human scanning the table directly.

**Reachability — narrower than every other function in `0149`-`0158`.** Every other `staff_*`
function is granted `EXECUTE` to `bsa_app` because it is reached through the API layer, gated by
`is_platform_admin()`/`is_platform_owner()` inside its own body. This function has no caller gate
(there is no admin yet to gate against), so it is granted to **neither** `public` nor `bsa_app` —
unreachable through the API layer, by any authenticated caller, under any circumstance. Only direct
database access (the same access level already required to apply this migration) can invoke it. No
API route, config endpoint, or `apps/api` change of any kind was added — the owner decision's
"if none is needed, do not invent one" is satisfied by inventing none.

**Runs once at apply time, and says so.** The bottom of migration `0159` calls the function inside a
`DO` block that `RAISE NOTICE`s the outcome (seeded, or the exact reason it did not) — visible in
migration-apply logs on every deployment. The function remains callable afterwards, by direct DB
access only, for as many redeploys as it takes for the configured identity to exist.

## Why this is not the allowlist ADM-07 (the durable-registry task) deleted

`PLATFORM_ADMIN_EMAILS` was a standing authorisation decision consulted on every request — being on
the list made every subsequent request from that identity an admin request, indefinitely, regardless
of database state. This function performs one audited write, after which `app_private.
is_platform_admin()` (unmodified since `0073`) is the only authority. Once a single admin row
exists, the function is permanently inert: the configured GUC is never consulted again, on any
request, by anything. A break-glass credential that stays valid while the registry is empty was
considered by the owner and declined for exactly this reason (owner decision record §3) — no such
path exists here.

## Existing guards, unchanged

`app_private.is_platform_admin()` (`0073`) — same table, same column, same body. Every
`CTL-14`/`CTL-15`/`CTL-03` guard (`0149`), `0151`'s `payment_decision`/`stored_record_decision`
`CHECK (= 'allow')`, `0155`'s owner singleton index and immutable-audit triggers, `0156`'s
no-self-conferral and one-identity posture — none read or write anything this task adds; all
continue to authorise exactly as before. `public.platform_admin_audit` is not altered.

## What was deliberately not built

No MFA, and no copy implying it exists — `ADM-07` (the durable-registry task) already built none
and corrected console copy overstating it; this task adds nothing that changes that state. No API
route, no config surface beyond the one deployment GUC. No new identity column or table.

## Verification

See `../../tests/TC-ADM-07-bootstrap-seed.md` for the full test-to-assertion mapping and
`../../reviews/2026-09-17-adm-bootstrap-seed-implementation.md` for the review record and real
verification numbers.
