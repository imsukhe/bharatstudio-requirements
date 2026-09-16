# TC-OPS-11 — revenue KPIs (derivable subset only)

**Task:** `../active/tasks/OPS-11.md`
**Owner:** Sukhdev Singh
**Status:** `Conditionally complete — local implementation and verification; independent review unavailable`

| Case | Control | Expected evidence |
|---|---|---|
| OPS-11.1 | Baseline with TTL exclusion already applied | Five real payments across three supporter identities (one live-anonymous repeat, one TTL-expired-anonymous repeat, one platform single); average tip = 220000 paise over 5; `supporterCount = 2` (the expired identity is excluded even though it would otherwise read as a repeat supporter); `repeatSupporterCount = 1`, `repeatSupporterRate = 0.5` |
| OPS-11.2 | Refund end-to-end moves two numbers from one event | A full refund on the live-anonymous supporter's second payment drops average tip (4/800000/200000) **and** `repeatSupporterCount`/`repeatSupporterRate` (0/0) on the same read — migration `0124`'s trigger recomputes `tip_count` net of refunds, so there is no counter to reconcile |
| OPS-11.3 | Partial refund recomputes correctly | A 40000-paise partial refund on the platform supporter's payment recomputes average tip to 190000 (4/760000) |
| OPS-11.4 | A second refund on an already-refunded payment recomputes correctly | A further 20000-paise refund on the same payment (now 60000 total) recomputes average tip to 185000 (4/740000) — no accumulation error, no stale total |
| OPS-11.5 | Challenge revenue reuses `0109` unchanged | `challenge_revenue_paise` for a channel with one active challenge equals the sum of `app_private.challenge_progress_paise()` over that challenge's window — one payment inside the window, several earlier ones outside it correctly excluded |
| OPS-11.6 | Vote revenue reuses `0108`'s join chain | `vote_revenue_paise` equals the net paise of the one payment tagged via `app_private.tag_vote_payment`, and a refund on that same payment reduces it on the next read |
| OPS-11.7 | Financial amounts are owner/admin only | An operator and a moderator both get **no row** back (not a zeroed row, not a 403) — the same posture as `list_channel_payments` (`0071`). An admin (not only the owner) is allowed |
| OPS-11.8 | Route: happy path and window parameters | `GET /v1/channels/:channelId/revenue-kpis` returns `200`; `windowStart`/`windowEnd` query parameters reach the store unchanged; omitted parameters pass `null` (all-time) |
| OPS-11.9 | Route: refused caller gets 404, not a distinguishable error | Same `404` for "channel not found" and "caller lacks owner/admin visibility" — cannot be used to enumerate membership |
| OPS-11.10 | Route: unauthenticated | Returns `401` |
| OPS-11.11 | Route: store failure degrades safely | A throwing store returns a retryable `503` |
| OPS-11.12 | No revenue number reaches Prometheus | `ApiMetrics` exposes no method whose name contains `revenue`, `activation`, `kpi`, `tip`, `supporter`, `payout`, `average` or `repeat` — a structural assertion, not a render-and-grep one, extending the existing `renderPrometheus` never-emits-an-identifier test |
| OPS-11.13 | `!tip` conversion — confirmed not buildable | Repo-wide grep for `chat_command`/`tip_command`/`bang_tip`/`'!tip'` across SQL, TS and Go returns no match; `CON-07` (the feature that would produce one) is Phase 2, excluded from v1 |
| OPS-11.14 | Contract | `contracts/openapi/v1.yaml` documents `/v1/channels/{channelId}/revenue-kpis` and the `RevenueKpis` schema, and `contracts:validate` passes |

**Commands (in `bharatstudio-alerts`):** `pnpm db:test:all`; `pnpm --filter
@bharatstudio/alerts-api build`; `pnpm --filter @bharatstudio/alerts-api test`; `pnpm
contracts:validate`; `pnpm explain:check`.

## Recorded local evidence — 2026-09-16

- `pnpm db:test:all` — **61 passed, 0 failed** (baseline 59). `packages/db/tests/
  ops11_revenue_kpis.sql` covers OPS-11.1–OPS-11.7 directly against a real Postgres 16
  container, including the full refund → partial refund → second-refund sequence in order so
  each assertion proves the *next* read is already correct, not that a job caught up to it.
- `pnpm --filter @bharatstudio/alerts-api build` — passed.
- `pnpm --filter @bharatstudio/alerts-api test` — **590 passed, 0 failed** (baseline 585).
  `apps/api/test/insights-routes.test.ts` covers OPS-11.8–OPS-11.11;
  `apps/api/test/l09-reliability-metrics.test.ts`'s new `ApiMetrics exposes no revenue or
  activation method` test covers OPS-11.12.
- OPS-11.13 (`!tip` conversion) verified by direct repo-wide grep before writing any code —
  recorded in the review record's "what was left out and why" section, not asserted from
  memory.
- `pnpm contracts:validate` — passed (68→70 paths, 75→77 operation contracts).
- `pnpm explain:check` — **16/16 plans current**, unchanged; `get_channel_revenue_kpis` does
  not match either RT-12 scan rule (verified by reading the scanner, not assumed).

## What this does not prove

No p95/p99 or load evidence — these are low-QPS, lazy-loaded dashboard reads (§12.7), not an
overlay/widget hot path, and RT-06/RT-07's performance-evidence boundary is untouched by this
task. No production/staging run — every number above is a local Postgres 16 container and a
local Node test run, per §35.1 rule 6 ("no local artefact is ever promoted to launch
evidence").

## Independent Opus verification — 2026-09-16

- `pnpm --filter @bharatstudio/alerts-api test` — **590 passed, 0 failed** (baseline 585).
- `pnpm db:test:all` — **61 passed, 0 failed** (baseline 59, +2 new SQL files).
- `pnpm contracts:validate` — clean; OpenAPI grew 68 → **70 paths**, 75 → **77 operations**.
- `pnpm explain:check` — 16/16. `python3 tools/doc_consistency.py` — 17/0/0.
- **Zero** revenue- or activation-shaped terms in `apps/api/src/observability/metrics.ts`,
  checked directly. `ApiMetrics` gained no methods, and a new structural test asserts none of
  its method names is revenue- or activation-shaped — so the boundary is enforced rather than
  remembered.

**No new schema was needed, and that was verified before SQL was written.** Both rows derive
from records that already exist: activation from `payment_account_audit`, `overlay_sessions`
and `alert_events`; revenue from `payments − refunds` and the existing relations, reusing
`0109`/`0108`/`0124`'s derivations unchanged. §19.6's derive-don't-store rule held without a
single counter being added, so no refund has anything to chase.

**Activation milestones are deliberately sticky** — once achieved, they stay achieved — rather
than reusing `0093`'s *live* payout and overlay signals. Proven by revoking a payout after
activation and asserting the milestone stays true. That is the right semantic: an activation
funnel records that a creator got there, not whether they are there this second. A live signal
would make a creator who rotated a payout account appear never to have activated.

**The anonymous TTL is enforced structurally.** Repeat-supporter rate excludes any
`kind='anonymous'` relation whose identity has passed its 30-day expiry, proven in the SQL
test rather than asserted in prose.

**`!tip` conversion was confirmed unbuildable and left out rather than approximated.** A
repo-wide search across SQL, TypeScript and Go found no chat-command-origin marker on a
payment, and `CON-07` is Phase 2, excluded from v1. Approximating it — inferring intent from
timing, say — would have produced a number that looked like measurement and was not.

### Two flags the implementer raised, both correct, both mine

It could not find the "completed scope review" the command told it to read, searched three
locations, and flagged the absence instead of fabricating a pointer. And the command's
top-line scope named OPS-08 and OPS-11 while a later subsection used "build" language for
OPS-10; it took the narrower reading, applied OPS-10's privacy rules where OPS-11 needed them
anyway, and reported the contradiction.

Both are recorded in `reviews/2026-09-16-ops-instrumentation-scope-review.md`, along with the
process correction: **a review agent's findings are written to `reviews/` before the
implementation agent is dispatched.**

**What this evidence is not.** Local only. These are instruments with no traffic through them
— the pipeline has value from the first real payment, the *readings* have none yet. Nothing
here is production, provider, store, legal, tax, staging, OBS, device, network, quota or
release evidence.
