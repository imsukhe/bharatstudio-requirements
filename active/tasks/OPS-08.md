# OPS-08 — activation instrumentation (payout + OBS/overlay + first alert)

**Authority:** [`../../FULL-PRODUCT-DEFINITION.md`](../../FULL-PRODUCT-DEFINITION.md) §31 (OPS-08 row), §31.0, §19.6, §7 (§7.1 dashboard screen inventory), §12.4, §12.6, §12.7, §35.1, §37.2; [`../launch/00_LAUNCH_SCOPE_AUTHORITY.md`](../launch/00_LAUNCH_SCOPE_AUTHORITY.md) (role-scoped read visibility)
**Status:** `Conditionally complete — local implementation and verification; independent review unavailable`

| Field | Value |
|---|---|
| **Scope phase** | `v1`. Three activation-milestone signals (payout connected, overlay/OBS connected, first alert fired), each read live from an existing durable record. No new table, column, trigger or counter |
| **Owner** | **Sukhdev Singh** |
| **Tier and gate** | All tiers. Readable by any active channel member (owner/admin/operator/moderator/viewer) — it carries no financial amount, so it is not gated by the owner/admin financial-visibility rule the way OPS-11 is |
| **Personal-data class** | None. Three booleans and three timestamps derived from rows that already exist for other reasons (`payment_account_audit`, `overlay_sessions`, `alert_events`); no new personal-data surface is created |
| **Provider or legal dependency** | None |
| **Failure behaviour** | A read failure here can never affect a payment, an alert, a delivery or a response, because the read is fully decoupled from every write path: `app_private.get_creator_activation_state` is a `stable` SQL function called only from the new `GET /v1/channels/:channelId/activation-state` route, which touches no other code path. A store/database failure is caught in the route handler and returns a retryable `503`, never a thrown error (`apps/api/src/routes/insights.ts`, `apps/api/test/insights-routes.test.ts`'s "an insights-store failure never surfaces as a crash" case) |
| **Kill switch** | No independent flag — this is a read endpoint with no write side effect. To remove it: revert `apps/api/src/routes/insights.ts`'s activation-state route, `apps/api/src/domain/insights-store.ts`'s `ActivationState`/`getActivationState`, `apps/api/src/db/insights-store.ts`'s implementation, the `app.ts`/`index.ts` wiring, and the OpenAPI path/schema. The three underlying tables and every existing writer of them are completely untouched either way |
| **Acceptance test** | `tests/TC-OPS-08-activation-instrumentation.md` |
| **Evidence location** | `tests/TC-OPS-08-activation-instrumentation.md`, `reviews/2026-09-16-ops-activation-and-revenue-instrumentation.md`, `packages/db/migrations/0133_v1_ops08_ops11_activation_and_revenue_kpis.sql`, `packages/db/tests/ops08_activation_state.sql`, `apps/api/src/domain/insights-store.ts`, `apps/api/src/db/insights-store.ts`, `apps/api/src/routes/insights.ts`, `apps/api/test/insights-routes.test.ts`, `contracts/openapi/v1.yaml` (`ActivationState` schema, `/v1/channels/{channelId}/activation-state`) — all in `bharatstudio-alerts` |
| **Rollback** | Additive only. The migration is rolled back by a **new forward migration** that drops `app_private.get_creator_activation_state(uuid)` — never by editing or deleting `0133_v1_ops08_ops11_activation_and_revenue_kpis.sql`. The TS/route/contract changes are reverted by deleting/reverting the files listed under Evidence location; no table, trigger or existing function is touched, so reverting this task changes nothing about payout onboarding, overlay sessions or alert delivery |

## What this is

Three activation milestones a creator can be shown on setup ("have I connected payout, have
I loaded the overlay in OBS, has my first alert fired") — the exact three named in the §31
OPS-08 row. Each is already knowable from a durable record this codebase already writes for
an unrelated reason:

| Milestone | Source | Why it is sticky, not live |
|---|---|---|
| Payout connected | `payment_account_audit`, `action = 'activated'` (migration `0060`) | Append-only — no update/delete grant to `bsa_app`. `0093`'s `get_companion_state.payment_account_connected` reads *current* `payment_accounts.status`, which flips back to false on a later revoke; an activation checklist item must not un-happen, so this reads "ever activated" instead |
| Overlay/OBS connected | `overlay_sessions`, any row ever created (migration `0001`/`0003`) | Sessions are only ever revoked, never deleted (`app_private.run_overlay_session_maintenance`, `0016`), so `EXISTS(...)` regardless of current validity is a safe "ever loaded as a browser source" signal |
| First alert fired | `alert_events`, any row ever created | Rows are never deleted |

No new schema was needed, and none was added — matching the command's own instruction to
stop and report rather than invent a table if one of the three turned out not to be
derivable. All three were derivable.

## Where it belongs

§7.1's dashboard screen inventory has no dedicated "activation" screen; the closest fit is
**Home / Today** ("today's support, goal progress, stream state, queue depth, six health
signals, anything needing attention. Pinnable cards"), which is exactly the kind of onboarding
nudge this data is for. This task builds only the instrument (the API) — the same posture
RT-06 took for its own histograms ("this task builds the instrument, it produces no
readings"). No dashboard screen was built in this slice; see the review record.

## Boundaries

**In scope:** `app_private.get_creator_activation_state`, `GET
/v1/channels/:channelId/activation-state`, its domain/db/route wiring, its OpenAPI contract
entry, and the SQL test proving all four states (nothing done, each milestone independently,
all three done) plus the "sticky, not live" behaviour under a payout revoke.

**Explicitly out of scope:** any dashboard UI rendering this data; the **creator** half of
OPS-10 (the same three signals reframed as a funnel with conversion rates between them) — see
the review record for why this was referred rather than built in this slice; any push
notification or nudge driven by this state.
