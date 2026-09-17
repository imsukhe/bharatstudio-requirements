# TC-ADM-07 — the one-time, audited admin bootstrap seed

**Task:** `../active/tasks/ADM-07-bootstrap-seed.md`
**Test file:** `packages/db/tests/adm_bootstrap_seed.sql` (real database, `packages/db/tests/
run-sql-suite.sh`, own isolated clone, fixture range `...7300`-`...73ff`)

| # | Claim | Assertion in `adm_bootstrap_seed.sql` |
|---|---|---|
| 1 | Not reachable through the API layer | `has_function_privilege('public', ...)` and `has_function_privilege('bsa_app', ...)` both false for `staff_bootstrap_platform_admin()` |
| 2 | Unset config seeds nothing, and the system says so | `app.bootstrap_admin_email` never set in-session → `seeded=false`, `reason_code='bootstrap_identity_unset'`, `user_id=null`; registry stays empty; zero audit rows |
| 3 | Configured but no matching signed-in user seeds nothing | config set to an email no `app_users` row holds → `reason_code='bootstrap_identity_not_found'` |
| 4 | An unverified email match does not count | config set to `7304`'s email (`email_verified=false`) → `reason_code='bootstrap_identity_not_found'`; `7304.is_platform_admin` stays false |
| 5 | The real seed succeeds, normalised | config set to `7300`'s email with mixed case and surrounding whitespace → `seeded=true`, `user_id=7300`, `reason_code='seeded'`; `7300.is_platform_admin` becomes true |
| 6 | Audit row written like any other grant | exactly one `platform_admin_audit` row for `7300`; `previous_value=false`, `new_value=true` |
| 7 | Distinguishable from an ordinary grant, structurally | bootstrap row: `changed_by = target_user_id` (unforgeable — the governed path rejects `actor=target` unconditionally) and reason carries the fixed `'ADM-07 BOOTSTRAP SEED (migration 0159):'` marker; later, an ordinary grant of `7303` via `staff_set_platform_admin` is asserted to have `changed_by <> target_user_id` and no bootstrap marker |
| 8 | Audit row is append-only | `UPDATE`/`DELETE` on the bootstrap row both raise `feature_not_supported` (0A000), via the same `platform_admin_audit_append_only` trigger `0155`/`0156` installed |
| 9 | `is_platform_admin()` (0073, unmodified) authorises the seeded identity | `set_config('app.user_id', 7300, ...)` then `app_private.is_platform_admin()` returns true |
| 10 | Idempotent + inert once an admin exists | second call, same config still set → `seeded=false`, `reason_code='admin_already_present'`, `user_id=null`; audit row count unchanged; `7300.is_platform_admin` still true |
| 11 | Not a standing authorisation path | with `7300` already admin, config re-pointed at `7303` → still `reason_code='admin_already_present'`; `7303.is_platform_admin` stays false (the seed cannot be redirected to grant someone else once inert) |
| 12 | `0149`-`0158` still authorise, using the bootstrapped identity | `7300` successfully calls a representative gated function from `0149` (`staff_list_capability_registry_audit`), `0151` (`create_safety_corpus_term`), `0153` (`staff_list_capability_registry_entries`), `0155` Job 2 (`staff_list_kill_events`), `0156` (`staff_list_platform_admins`, which also surfaces the bootstrap audit reason for `7300`) |
| 13 | A never-admin caller is still rejected the same way | `7301` (never granted anything) gets `insufficient_privilege` on `staff_list_capability_registry_audit` and `staff_list_platform_admins` |

## Result

`sh packages/db/tests/run-sql-suite.sh` (all 159 migrations + all `packages/db/tests/*.sql` files,
each in its own cloned database): **83/83 pass, 0 fail**, including `adm_bootstrap_seed` (new) and
`adm_admin_registry` (`0156`'s own suite, unmodified, still green — proves `0156` was not disturbed).
Migration-apply log for `0159` printed `ADM-07 bootstrap (migration 0159): no admin seeded --
app.bootstrap_admin_email is not configured for this deployment` while building the shared test
template, confirming the unset path fires correctly with no ambient configuration.
