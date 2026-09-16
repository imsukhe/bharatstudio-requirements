# OPS-11 — revenue KPIs (derivable subset only)

**Authority:** [`../../FULL-PRODUCT-DEFINITION.md`](../../FULL-PRODUCT-DEFINITION.md) §31 (OPS-11 row and its "deserves emphasis" note), §31.0, §19.6, §12.3, §12.6, §12.7, §35.1, §37.2; [`../launch/00_LAUNCH_SCOPE_AUTHORITY.md`](../launch/00_LAUNCH_SCOPE_AUTHORITY.md) (role-scoped financial-visibility rule)
**Status:** `Conditionally complete — local implementation and verification; independent review unavailable`

| Field | Value |
|---|---|
| **Scope phase** | `v1`. Four of the eight KPIs the §31 OPS-11 row names: **average tip, repeat-supporter rate, challenge revenue, vote revenue** — every one computable from `payments − refunds` and existing relations with no new attribution logic. The other four (tips-per-viewer-hour, TTS-driven tips, threshold uplift, goal-driven tips) and `!tip` conversion are explicitly **not** built — see "What was left out and why" below |
| **Owner** | **Sukhdev Singh** |
| **Tier and gate** | All tiers with payment/alerts enabled. **Owner/admin only** — financial amounts, gated by `00_LAUNCH_SCOPE_AUTHORITY.md`'s role-scoped read-visibility rule, enforced inside `app_private.get_channel_revenue_kpis` (`has_channel_role(..., array['owner','admin'])`), not only in application code |
| **Personal-data class** | None new. The function reads existing payment/refund/challenge/vote-tag/supporter-relation rows; it returns aggregate numbers only, never a per-payment or per-supporter row, and never a supporter identifier |
| **Provider or legal dependency** | None |
| **Failure behaviour** | A read failure here can never affect a payment, an alert, a delivery or a response — the same isolation as OPS-08: a `stable` SQL function called only from `GET /v1/channels/:channelId/revenue-kpis`, with the route's own `try/catch` returning a retryable `503` rather than throwing (`apps/api/test/insights-routes.test.ts`) |
| **Kill switch** | No independent flag — a read endpoint with no write side effect. Revert `apps/api/src/routes/insights.ts`'s revenue-kpis route, the `RevenueKpis`/`getRevenueKpis` domain/db code, the DI wiring, and the OpenAPI entry. `payments`, `refunds`, `creator_supporter_relations`, `challenges` and `vote_payment_tags` and every existing writer of them are untouched |
| **Acceptance test** | `tests/TC-OPS-11-revenue-kpis.md` |
| **Evidence location** | `tests/TC-OPS-11-revenue-kpis.md`, `reviews/2026-09-16-ops-activation-and-revenue-instrumentation.md`, `packages/db/migrations/0133_v1_ops08_ops11_activation_and_revenue_kpis.sql`, `packages/db/tests/ops11_revenue_kpis.sql`, `apps/api/src/domain/insights-store.ts`, `apps/api/src/db/insights-store.ts`, `apps/api/src/routes/insights.ts`, `apps/api/test/insights-routes.test.ts`, `apps/api/test/l09-reliability-metrics.test.ts` (the new "no revenue/activation method" structural assertion), `contracts/openapi/v1.yaml` (`RevenueKpis` schema, `/v1/channels/{channelId}/revenue-kpis`) — all in `bharatstudio-alerts` |
| **Rollback** | Additive only. The migration is rolled back by a **new forward migration** that drops `app_private.get_channel_revenue_kpis(uuid, timestamptz, timestamptz)` — never by editing or deleting `0133_v1_ops08_ops11_activation_and_revenue_kpis.sql`. TS/route/contract changes are reverted by deleting/reverting the files listed under Evidence location |

## Where these numbers live — not Prometheus

**A durable, creator-reachable read. Prometheus gets nothing added.** §12.6 requires durable
creator records to be viewable/searchable/exportable and never tier-gated; §12.4/RT-06
forbid an identifier-shaped label (a channel id, which any of these numbers would need to
mean anything as a metric); and `apps/api/src/observability/metrics.ts`'s own header already
states this boundary for the existing L09/RT-06 metrics. `apps/api/test/l09-reliability-
metrics.test.ts` gained a new structural test — `ApiMetrics exposes no revenue or activation
method` — that fails by naming the offending method if a revenue number is ever wired into
that type, rather than relying on a render-and-grep check that only catches it after the fact.

## Derive, never store — followed exactly, not just asserted

Every number is computed live from `payments − refunds`, `creator_supporter_relations`,
`challenges` and `vote_payment_tags` on every call — nothing here is incremented anywhere:

- **Average tip.** Mean of `greatest(gross_amount_paise − processed_refunds, 0)` over
  captured/refunded/partially-refunded payments in the requested window (or all time), payments
  refunded to net zero excluded from the average, not zeroed into it.
- **Repeat-supporter rate.** Reads `creator_supporter_relations.tip_count` directly — already
  recomputed net-of-refunds by migration `0124`'s trigger on every payment insert/status
  change, so a refund that drops a supporter below "repeat" changes this rate on the next
  read, with no counter to correct. **Deliberately not windowed by payment date** — it is a
  relationship-population statistic, not a per-period revenue figure.
- **Challenge revenue.** Sums `app_private.challenge_progress_paise()` (migration `0109`,
  unchanged) over every challenge whose `started_at` falls in the window. Reuses `0109`'s own
  windowed-sum-over-payments definition exactly — no new payment-to-challenge attribution was
  added, because `0109`'s own header explains why none exists to add (a challenge's progress
  is its channel's payments during its active window, not a per-payment tag; this is existing,
  approved product behaviour, not something this task introduced).
- **Vote revenue.** Sums net paise over every `vote_payment_tags` row for the channel via the
  exact join chain `0108`'s `paid_support_vote_tally` already established
  (`vote_payment_tags → payment_order_intents → payments`, minus processed refunds), just
  aggregated across every definition/option in the channel instead of one at a time.

## The privacy boundary on repeat-supporter rate (Opus's decision, binding)

An anonymous supporter must not be tracked as "repeat" past `anonymous_browser_identities
.expires_at` (30 days, migration `0124`, matching `apps/api/src/db/viewer-store.ts`'s own
30-day session TTL default). `get_channel_revenue_kpis`'s supporter population excludes any
relation whose identity is `kind = 'anonymous'` and already expired; `kind = 'platform'` /
`'account'` identities carry no such TTL and are always included. `packages/db/tests/
ops11_revenue_kpis.sql` proves this structurally: a second anonymous identity with two
payments (which would read as a repeat supporter) is excluded from both the numerator and the
denominator once expired, and the baseline assertion would fail (`supporter_count` would read
3, not 2) if the exclusion were missing.

## What was left out and why

- **`!tip` conversion — checked, not buildable.** Grepped the entire `bharatstudio-alerts`
  tree (SQL, TS, Go) for any existing `!tip`-origin marker (`chat_command`, `tip_command`,
  `bang_tip`, a literal `'!tip'`) — none exists. `CON-07` (the chat-command connector that
  would produce one) is Phase 2/YouTube, explicitly excluded from v1 by
  `00_LAUNCH_SCOPE_AUTHORITY.md`. No durable record in this codebase distinguishes a
  `!tip`-originated payment from any other tip today, so there is nothing to derive from —
  left out, per the command's own instruction to check and say so rather than invent a marker.
- **Tips-per-viewer-hour, TTS-driven tips, threshold uplift, goal-driven tips — referred, not
  built.** Each needs a cause-attribution write path ("did the goal bar moving cause this
  tip?") that is new derived logic, not a read over an existing record, and each needs its own
  decision record first per the command's explicit instruction. Not attempted here.
- **OPS-10 (creator and viewer funnel) — referred, not built in this slice.** See the review
  record's "OPS-10" section for the scope-instruction conflict this surfaced and how it was
  resolved.
