# TC-L15 — Live-platform connectors and chat commands acceptance

**Status:** `Execution partial — source_type widening, dedupe/unique-index, entitlement-gate, short-link and bot-ack-off cases have local evidence; revoke-flow and Google OAuth/quota confirmation remain open`
**Task:** [`../tasks/L15-live-platform-connectors-and-chat-commands.md`](../tasks/L15-live-platform-connectors-and-chat-commands.md)
**Authority:** `bharatstudio-alerts/docs/BharatStudio-MASTER-PLAN.md` Part 6 (L15) and Part 7 §7.8
**Repository:** `/Users/sukhdevsingh/Workspace/Bharat Studio/bharatstudio-alerts` (`services/youtube-poller-go` to be built)
**Data:** Synthetic YouTube webhook/chat fixtures only. No real creator OAuth tokens or live YouTube accounts are used in this test suite.

## Preconditions

1. L01's `source_type` contract change is defined and reviewed.
2. Google OAuth app verification status and Data API quota-increase status are recorded (dated), whatever they are — this test suite does not require them to be complete to exercise synthetic fixtures, but production readiness does.
3. Disposable PostgreSQL test harness available for `alert_events.source_type` widening and connector tables.

## Acceptance cases

| ID | Setup and action | Expected result | Failure/retry and evidence |
|---|---|---|---|
| L15-01 | Simulate a Super Chat webhook and a BharatStudio tip of the identical amount on the same channel | Both produce LiveEvents the queue engine cannot distinguish except by `source` field | Local design evidence only: `services/youtube-poller-go/internal/domain/live_event.go` normalises Super Chat into `EventSuperChat` (`youtube.super_chat`) distinguished only by type/source field; a direct fixture comparing the two side by side against the queue engine was not found. Not fully proven |
| L15-02 | Replay the identical YouTube webhook payload twice | No second event/row is created; dedupe holds | Pass, local evidence: `alert_events_external_source_unique` partial unique index on `(channel_id, source_type, source_id)` scoped to `youtube`/`twitch`/`kick`, `packages/db/migrations/0091_v1_l15_youtube_delivery_and_idempotency.sql:52` |
| L15-03 | Revoke a channel's YouTube OAuth grant on the (simulated) platform side, then poll | Connector reaches a clean disconnected state; no error loop or repeated failed retries | Local design evidence: `services/youtube-poller-go/internal/poller/poller.go:217` drops state for revoked/removed connections each cycle; a dedicated revoke-then-poll test asserting no error loop was not found. Not fully proven |
| L15-04 | Compare a Super Chat event's effect on payment truth vs. a confirmed Razorpay webhook | Financial truth (captured/refunded state) is derived only from the payment provider; the Super Chat event alone never marks a payment captured | Satisfied by construction: YouTube ingestion writes only to `alert_events`/connector tables; payment capture/refund state is written solely by the existing Razorpay webhook path (L04), unmodified by this task. No shared write path found |
| L15-05 | Send `!tip 100 message` in a simulated chat message | A TipIntent is created; bot reply contains only an opaque short link, no amount/name/message in the URL | Pass, local evidence: `apps/api/src/routes/public.ts:364` mints `shortLink` as `{origin}/t/{token}` with amount/name/message kept server-side; `services/youtube-poller-go/internal/poller/tipintent_test.go` covers the TipIntent creation path |
| L15-06 | Open the short-link confirmation page | Amount, name and message render server-side without a form; no query-string leakage of tip data | Pass, local evidence: `apps/web/app/t/[token]/TipIntentConfirm.tsx` reads by opaque token; no form fields for amount/name/message |
| L15-07 | Configure a Pro channel (entitlement: 1 connector) and attempt to connect a second external live-platform connector | Second connection is rejected server-side by entitlement count | Pass, local evidence: `packages/db/tests/l15_youtube_connectors.sql` asserts `youtube_connector_entitlement_limit` returns 0/1/2/3 for free/pro/creator/studio and exercises the per-tier connector boundary |
| L15-08 | Apply the `alert_events.source_type` CHECK-widening migration to a harness pre-populated with existing `payment`/`manual`/`companion` rows | Existing rows are unaffected; migration is additive and reversible without data loss | Pass by design: `packages/db/migrations/0086_v1_l15_youtube_connectors.sql` widens the CHECK via `NOT VALID` + `VALIDATE`, the standard additive pattern this repo uses elsewhere (see L03's own `NOT VALID` conventions) |

## Closure rules

Closes only when every row has a real pass/fail result with inline evidence (migration filename, exact `services/youtube-poller-go` and connector file paths, test-suite pass counts) replacing "Not run — TODO," plus dated written confirmation (or explicit absence) of Google OAuth app verification and Data API quota status. No artifact/screenshot directory exists or may be created; evidence is inline prose citation only.

## Cleanup and rollback

All fixtures run against the disposable PostgreSQL harness, torn down after the run. The `source_type` widening is additive; no production database is touched by this suite.
