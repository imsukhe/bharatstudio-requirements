# Backend gap remediation authority

**Status:** `Approved for implementation by project owner — verification remains required`
**Owner:** Project owner
**Scope:** Applicable BharatStudio v1 backend/runtime gaps found in the backend gap audit
**Phase 2 exclusions:** YouTube ingestion/polling and Enterprise workspaces/funds movement remain excluded.

## Objective

Close every applicable v1 runtime gap identified by the backend gap audit and the
follow-up review. A gap is not closed by a schema field or UI control alone: the
server, database, worker, deployment contract, tests and recovery evidence must
agree.

## Required outcomes

1. Creator payment-account onboarding and account attribution are explicit,
   server-authoritative and auditable. No money movement is performed without an
   approved provider contract and verified account state.
2. Accepted payment/alert evidence remains append-only and no-drop. Tier limits,
   queue capacity, moderation, quiet mode and provider delay may hold or require
   operator action, never discard accepted evidence.
3. Queue delivery state is independent per queue. Duplicate routing is explicit,
   idempotent and covered by concurrency tests.
4. Unknown payment/refund reconciliation states enter a durable manual-review
   quarantine and cannot poison every future reconciliation pass.
5. Account deactivation, export/access, privacy requests, Terms acceptance and
   retention controls are implemented or the public promise is blocked.
6. Public payment abuse controls, provider verification, CSP/CORS, IAM, secrets,
   Cloud Tasks, DLQ, SSE replay and deployment evidence are defined and tested.
7. Every completed item has dated test evidence, self-review and an independent
   review or an explicit conditional/blocker record.

## Implementation notes added during remediation

- Razorpay deduplication uses the verified `X-Razorpay-Event-Id` /
  `x-razorpay-event-id` header. It is never derived from request time or a
  browser value; payment/refund/dispute IDs remain separate business keys.
- Queue policy is enforced at the durable claim/list/projection boundary.
  Queue modes, priority ageing, approval, quiet windows, source rate limits,
  publication markers and out-of-order replay preserve accepted rows; limits
  may hold or delay a row but cannot turn it into a drop.
- Public tip creation has a production-required Cloudflare Turnstile boundary
  plus route-specific rate limiting. A verification failure occurs before the
  payment service call and remains retryable for the viewer.
- Sarvam TTS synthesis is an explicit provider adapter with a 1.5-second hard
  timeout, bounded Indic locale/text input, a durable cache/artifact path, an
  authenticated alert-worker enrichment caller and chime fallback. The worker
  never blocks or drops a visual alert when TTS fails. Credentials, provider
  sandbox evidence and production artifact-capacity validation remain external
  release gates.
- Deployment manifests pin the API/payment/worker split, direct-vs-pooled
  database endpoints, Cloud Run caps, OIDC audience equality, Cloud Tasks
  retries/DLQ and secret names. They are substitution templates, not proof
  that production has been provisioned.
- Terms/privacy acceptance is enforced as a server precondition for product
  mutations (channel, queue/binding/config, payment-account, alert, Companion,
  overlay-session and notification writes). Account acceptance, export, privacy
  request and closure routes remain available without that precondition. The
  staging/production API refuses to boot without the account enforcement
  adapter. If active legal documents are not seeded, the database gate fails
  closed instead of treating the absence of documents as implicit consent.
- Public-payment HTTP rate limits are defense in depth and are instance-local
  in the API process. Production must also attach a distributed edge/WAF rate
  limit keyed by the real client boundary; scaling Cloud Run instances must not
  be treated as a way to increase the public payment budget.

## Decision boundaries

- TTS playback/fallback is v1; provider synthesis is implemented behind a
  provider boundary but cannot be claimed live until provider credentials and
  sandbox evidence exist.
- Email delivery and referrals are implemented only where required by a current
  v1 promise; otherwise they remain explicitly deferred and must not be implied
  by public copy. **Superseded 2026-08-16**: 01_MASTER_RELEASE_AUTHORITY.md's
  "v1 scope addendum — 2026-08-16" makes both v1-required. See that document's
  entitlement-values-style addenda for the resolved design of each (referral
  credit mechanism in particular: owner-approved as a service-time credit —
  extends current_period_end, no refund, no recurring_price_paise mutation —
  not legacy's refund-based "free month," which is incompatible with this
  repo's payment-boundary invariants).
- The no-op replay publisher is intentional. Durable database publication plus
  SSE wake-up is the correctness design; staging must prove the complete path.
- Workspace/Enterprise and YouTube code must not be added to v1 remediation.

## Entitlement values — recorded 2026-09-07 (Part 12 item 3)

The eight closed-set entitlement dimensions and the TTS quota ladder are published as
implemented. Source of truth: `BharatStudio-MASTER-PLAN.md` v3.0 §3.2 (authoritative
per the launch task's instruction). This section records, not re-derives, those values.

| Key | Free | Pro | Creator | Studio |
|---|---|---|---|---|
| `queueCount` | 1 | 2 | 3 | 5 |
| `ttsEnabled` | false | true | true | true |
| `allowedQueueModes` | `fifo` | `fifo, stacked, pills, aggregated` | + `priority` | same as Creator |
| `maxVisibleItems` | 3 | 5 | 8 | 12 |
| `maxCharLimit` | 100 | 150 | 300 | 500 |
| `maxDisplayMs` | 6,000 | 8,000 | 12,000 | 20,000 |
| `quietMode` | false | true | true | true |
| `approvalRequired` | false | false | true | true |
| TTS quota, chars/month | 0 | 20,000 | 40,000 | 60,000 |
| Moderator seats | 0 | 0 | 2 | 5 |

`queueCount` was retiered from the now-**superseded** 1/3/5/10 figures by migration
`0080_v1_l03_entitlement_retier_and_dimensions.sql`, which also re-runs
`app_private.enforce_queue_count_entitlement` for every existing channel so the
retier pauses excess queues rather than deleting them (confirmed at
`packages/db/migrations/0080_v1_l03_entitlement_retier_and_dimensions.sql:227,307`).

`approval` is **not** a queue mode. `EntitlementPolicy` in
`apps/api/src/domain/entitlement-policy.ts:1` types `QueueMode` as
`'fifo' | 'stacked' | 'pills' | 'aggregated' | 'priority'` and carries
`approvalRequired` as an independent boolean on the same policy object, checked at
the same file's `validateConfigEntitlement`. Studio and Creator share the same mode
list by design — Studio's added power is `approvalRequired` plus the other
dimensions, not an extra mode. This ladder was corrected by migration
`0083_v1_l03_queue_mode_ladder_correction.sql`; an earlier version of the master
plan's own table (and, transiently, the marketing site built from it) had `+
approval` on Studio and omitted `pills` — both wrong, both fixed in code before this
record was written.

TTS quotas (0 / 20,000 / 40,000 / 60,000) are metered and hard-stopped at the quota
boundary per `app_private.tier_tts_monthly_quota` in migration
`0081_v1_l03_tts_usage_metering.sql:36-46`, backed by the
`public.alert_tts_usage_monthly` table in the same migration.

**TTS overage was amended 2026-09-07** (`BharatStudio-MASTER-PLAN.md` §3.12,
reversing part of the 2026-09-02 decision recorded in §3.2 above and in Part 13
decision 1 of that document). The original decision was a hard stop with an upgrade
prompt and explicitly no silent downgrade to the browser voice. That is now
reversed: a paid tier that exhausts its monthly quota falls back to the on-device
Web Speech API rather than going silent, and the quota consumption itself is
unaffected (browser fallback never counts against the metered quota). Shipped in
migration `0096_v1_l03_tts_fallback_and_amount_ladder.sql`, which adds
`app_private.store_alert_tts_fallback_reason` and threads `ttsFallbackReason`
through `get_overlay_events` so the overlay client knows a premium-TTS attempt was
skipped and why, and can speak `payload.message` locally instead. The same
migration also adds a platform-enforced, amount-tiered character-limit ladder
(`app_private.tts_amount_char_limit`) that is folded into
`app_private.get_alert_tts_input` — whichever of that ladder and the entitlement's
`maxCharLimit` is tighter wins.

Moderator seats (0/0/2/5) are recorded per owner decision 2026-09-02; role-scoping
and moderator audit trail already exist under L02/L03 per the master plan (no
migration citation independently verified in this pass — see Contradictions below).

Test coverage located, not independently run in this pass: `apps/api/test/
entitlement-policy.test.ts`, `apps/api/test/entitlement-limits.test.ts`,
`apps/api/test/companion-entitlement-grant-policy.test.ts`, and the TTS suite
(`tts-quota-metering.test.ts`, `tts-provider.test.ts`, `tts-routes.test.ts`,
`tts-fallback-reason.test.ts`, plus `apps/web/app/overlay/tts-runtime.test.ts` and
`apps/web/app/overlay/[overlayId]/tts-fallback.test.ts`) — all present in the
`bharatstudio-alerts` repo tree. None of this has been verified in a deployed or
staging environment; nothing in this program has been.

## Closure rule

The master release authority remains blocked until all applicable remediation
items are `Verified`, or have a named owner, expiry, mitigation and rollback under
an approved conditional exception. Razorpay approval, production credentials,
legal/CA advice, app-store review and deployed staging cannot be manufactured by
local code and remain external gates.
