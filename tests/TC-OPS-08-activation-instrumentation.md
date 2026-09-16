# TC-OPS-08 — activation instrumentation (payout + OBS/overlay + first alert)

**Task:** `../active/tasks/OPS-08.md`
**Owner:** Sukhdev Singh
**Status:** `Conditionally complete — local implementation and verification; independent review unavailable`

| Case | Control | Expected evidence |
|---|---|---|
| OPS-08.1 | Nothing done yet | All three signals read `false`; all three timestamps read `null` |
| OPS-08.2 | Payout milestone flips independently | An `'activated'` row in `payment_account_audit` sets `payoutConnected = true` and stamps `payoutConnectedAt`; the other two milestones stay `false` |
| OPS-08.3 | Payout milestone is sticky, not live | Revoking the payment account afterwards (`payment_accounts.status = 'revoked'`) must **not** un-set `payoutConnected` — an activation checklist item does not un-happen |
| OPS-08.4 | Overlay milestone counts any-ever, not currently-valid | An `overlay_sessions` row that is already expired/revoked at the moment it is created still flips `overlayConnected = true` |
| OPS-08.5 | First-alert milestone | One `alert_events` row is sufficient to flip `firstAlertFired = true` and stamp `firstAlertFiredAt` |
| OPS-08.6 | Read access has no financial gate | A moderator (operational role, no financial visibility elsewhere in the product) can still read activation state — it carries no amount |
| OPS-08.7 | Non-members get nothing | A user with no membership on the channel receives no row (not a zeroed row, not an error) |
| OPS-08.8 | Route: happy path | `GET /v1/channels/:channelId/activation-state` returns `200` with the derived state for an authenticated member |
| OPS-08.9 | Route: not found | Returns `404` when the store has no row for the caller |
| OPS-08.10 | Route: unauthenticated | Returns `401` with no session |
| OPS-08.11 | Route: store failure degrades safely | A throwing store returns a retryable `503`, never a thrown error/crash — proves instrumentation failure cannot propagate |
| OPS-08.12 | Route: unwired store | With no store configured at all, both routes return `503`, not a crash |
| OPS-08.13 | Contract | `contracts/openapi/v1.yaml` documents `/v1/channels/{channelId}/activation-state` and the `ActivationState` schema, and `contracts:validate` passes |

**Commands (in `bharatstudio-alerts`):** `pnpm db:test:all` (runs
`packages/db/tests/ops08_activation_state.sql` as part of the full glob); `pnpm --filter
@bharatstudio/alerts-api build`; `pnpm --filter @bharatstudio/alerts-api test`; `pnpm
contracts:validate`.

## Recorded local evidence — 2026-09-16

- `pnpm db:test:all` — **61 passed, 0 failed** (baseline 59; +2 for `ops08_activation_state.sql`
  and `ops11_revenue_kpis.sql`). `ops08_activation_state.sql` covers OPS-08.1–OPS-08.7 above
  directly, against a real Postgres 16 container seeded from the shared migration/base-world
  template, not a mock.
- `pnpm --filter @bharatstudio/alerts-api build` — passed, no type errors.
- `pnpm --filter @bharatstudio/alerts-api test` — **590 passed, 0 failed** (baseline 585;
  +5 — four new cases in `apps/api/test/insights-routes.test.ts` covering OPS-08.8–OPS-08.12,
  and one in `apps/api/test/l09-reliability-metrics.test.ts` shared with OPS-11, below).
- `pnpm contracts:validate` — passed. OpenAPI document grew from 68 to 70 paths, 75 to 77
  operation contracts, with all local `$ref` targets resolving.
- `pnpm explain:check` — **16/16 plans current**, unchanged. `get_creator_activation_state`
  matches neither RT-12 scan rule (not `list_overlay_*`, not in a file whose basename contains
  "overlay"/"master-canvas"), so no manifest/exemption entry was required — verified by reading
  `packages/db/explain-plans/scan-required-queries.mjs` before relying on this, not assumed.
