# L15 — Live-platform connectors and chat commands

**Status:** `YouTube v1 slice built and locally test-proven (poller, ingestion, TipIntent short-link flow, ingest-failure admin surface); bot chat-acknowledgement code exists but ships flag-off and unverified — Google has not approved the chat-write scope; Twitch/Kick remain out of scope per task boundary; nothing here is proven in a deployed environment`
**Level:** L3
**Owner:** [OWNER — API / Go services / integrations, unassigned]
**Depends on:** L01 (constraint widening on `alert_events.source_type`). Reference implementations exist in `stream-ios`/`stream-android`.
**Blocks:** L14 (Level 2 identity, YouTube linking), L16 (leaderboards), L17 (`!challenge`), L18 (native membership ingestion)
**Test record:** [`../tests/TC-L15-live-platform-connectors-and-chat-commands.md`](../tests/TC-L15-live-platform-connectors-and-chat-commands.md)

## Authority and evidence

Master plan Part 6, "L15 — Live-platform connectors and chat commands" (lines ~802–853); Part 7 §7.8 (connectors/chat commands feature register, phased v1 vs Phase 2); the 2026-09-02 decision recorded there: **YouTube ships in v1, including the chat bot; Twitch and Kick remain Phase 2.** This amends L10's prior "v1 contains no YouTube... capability/claim" for YouTube only.

## Objective

Ingest YouTube (v1), and Twitch/Kick (Phase 2) events as canonical LiveEvents, and let a viewer start a tip from chat.

## Tasks

1. Widen `alert_events.source_type` CHECK from `('payment','manual','companion')` to include `youtube` (v1), `twitch`, `kick` (Phase 2); add `source_event_type` and `source_user_id` columns. One migration; queue/delivery/moderation/overlay layers do not change.
2. `live_platform_connections` + `oauth_token_metadata`, encrypted tokens in the existing vault reference pattern.
3. YouTube (v1): OAuth; live status; `streamList` low-latency chat polling (build `services/youtube-poller-go` from scratch — currently empty); text messages; Super Chats; Super Stickers; member events; member milestone chats; gifted memberships; polls where authorised; moderation events; bot text messages.
4. Twitch (Phase 2): EventSub for chat, subs, sub-end, gifts, resubs, Cheers/Bits, Channel Points, follows, stream state.
5. Kick (Phase 2, label Beta): official OAuth + signed webhooks — chat, follows, subscription new/renewal/gift, channel rewards, stream state, moderation; verify signatures; dedupe on Kick event message IDs.
6. Normalise natives (Super Chat, Super Sticker, Cheer, Sub, Resub, Gift Sub, Channel Points, Kick subs) into LiveEvent.
7. `!tip`, `!tip 100`, `!tip 100 message` → create TipIntent → bot replies with an opaque short link (amount/name/message stay server-side, never in the URL).
8. Confirmation page at the short link — no form, direct UPI-app buttons.
9. Bot acknowledgement back into chat on verified capture.
10. `!challenge` / `!challenge 500 message` — gated on L17, Phase 2 timing follows Twitch/Kick.
11. Connector entitlement: one generic "External Live Platform Connector" count — Free 0, Pro 1, Creator 2, Studio 3.
12. Keep the QR and short-URL fallback working when chat is unavailable, always.

## Exact implementation boundary

In scope for v1: items 1–3, 6–9, 11–12 for YouTube only, plus the `source_type` widening (which also reserves `twitch`/`kick` values for Phase 2 without building those connectors now).

Out of scope for v1: Twitch EventSub connector, Kick connector, `!challenge` (gated on L17 timing), optional YouTube `/live` support page. These are Phase 2 and tracked here as explicitly deferred, not silently dropped.

External, non-code dependencies that gate this task and must be tracked as blocking, not absorbed into engineering estimates: Google OAuth app verification (published privacy policy on the verified domain, demo video, per-scope justification — the chat-write scope for bot acknowledgement is high-sensitivity and can bounce) and the YouTube Data API quota increase. Both should start immediately and in parallel with everything else in this task.

## Non-negotiable implementation rules

- A Super Chat and a BharatStudio tip of the same amount must produce LiveEvents the queue engine cannot distinguish except by `source`.
- A duplicate platform webhook must produce no second event (dedupe on Kick event message IDs where applicable; standard idempotency elsewhere).
- Revoking the OAuth grant on the platform side must degrade to a clean disconnected state, never an error loop.
- Financial truth always comes from the payment provider, never from a platform event. A Super Chat/Cheer/etc. is never treated as a payment-provider-confirmed capture.
- The opaque short-link token carries no amount, name or message in the URL.

## Definition gate

Per `governance/AGENTS.md`, implementation stops after definition pending explicit approval on scope, acceptance criteria, affected files, data impact, test plan and rollback. **Open decision — not decided here:** owner is unassigned [OWNER]. The exact Google OAuth verification timeline and quota-increase outcome are external and cannot be committed to a date by this task; record as an open external dependency, not a resolved date.

## Acceptance criteria

- A Super Chat and a BharatStudio tip of the same amount produce LiveEvents that the queue engine cannot distinguish except by `source`.
- A duplicate platform webhook produces no second event.
- Revoking the OAuth grant on the platform side degrades to a clean disconnected state, not an error loop.
- Financial truth always comes from the payment provider, never from a platform event.
- The `source_type` CHECK widening is additive (`NOT VALID` pattern per existing conventions) and does not rewrite historical `alert_events` rows.
- Connector entitlement count (0/1/2/3 by tier) is enforced server-side, proven by test at the boundary (e.g., a Pro channel rejects a second connector).

## Evidence required for closure

Inline prose citation: exact migration filename for the `source_type` widening; exact service/file paths for `services/youtube-poller-go` and the OAuth/token-vault integration; webhook-dedupe and revoke-flow test-suite pass counts; written confirmation (dated) of Google OAuth app verification status and Data API quota increase, cited as external evidence, not assumed.

## Rollback

The `source_type` CHECK widening is additive and reversible without data loss (existing rows keep `payment`/`manual`/`companion`). Connector tables (`live_platform_connections`, `oauth_token_metadata`) are new and can be dropped without touching payment/alert history. A connector can be disabled per channel (OAuth revoke path) without affecting other channels or the queue/delivery pipeline. No production database migration runs without separate explicit approval.

## Implementation slice — 2026-09-07 reconciliation

Reconciled against `bharatstudio-alerts` as read on 2026-09-07; local build/test evidence only.

**Built and locally test-proven:**
- `packages/db/migrations/0086_v1_l15_youtube_connectors.sql`: `source_type` widened via `NOT VALID` + `VALIDATE` (additive, no rewrite of existing rows), encrypted connector-token storage reusing the existing `NotificationTokenProtector` vault pattern, connector counts 0/1/2/3 by tier.
- `packages/db/migrations/0091_v1_l15_youtube_delivery_and_idempotency.sql`: `alert_events_external_source_unique` — a partial unique index on `(channel_id, source_type, source_id)` scoped deliberately to `youtube`/`twitch`/`kick` only, not `payment` (the file's own header explains why a unique index over `payment` would break per-source rate limiting); `queue_bindings.source_type` widened to match; least-privilege `bsa_connector_poller` role added.
- `packages/db/migrations/0094_v1_l15_youtube_delivery_and_failure_recording.sql`: durable delivery path plus a `youtube_event_ingest_failures` failure-taxonomy table.
- `packages/db/migrations/0097_v1_l15_tipintent_short_link.sql`: opaque TipIntent short link. Confirmed end to end — `apps/api/src/routes/public.ts:364` mints `shortLink: \`\${origin}/t/\${token}\`` with no amount/name/message in the URL, and `apps/web/app/t/[token]/TipIntentConfirm.tsx` is the no-form confirmation page.
- `packages/db/migrations/0099_v1_l15_ingest_failure_admin_surface.sql`: acknowledge-only admin surface over the failure table, gated by `is_platform_admin()`, following the existing admin-DLQ precedent from migration 0073.
- `packages/db/migrations/0101_v1_l07_l15_tts_mute_enforcement_and_tipintent_wiring.sql`: TipIntent poller wiring and dedup, plus a TTS-mute enforcement gap closed on the way.
- `services/youtube-poller-go` is a real, non-empty Go service (`internal/poller`, `internal/chatcommand`, `internal/youtube`), not the empty placeholder the master plan described at baseline.
- Bot chat-acknowledgement exists in code (`internal/chatcommand/ack.go`, `internal/youtube/client.go:196`) but ships behind a still-default-off flag: `internal/poller/tipintent_test.go` proves zero chat posts with the flag off and exercises the on-path only in test. `client.go:201` records in-code that this is gated because the chat-write scope for bot acknowledgement is not yet approved by Google — matching this task's own external-dependency framing, not resolved by this reconciliation.

**Confirmed still out of scope per this task's own boundary, not a gap:** Twitch EventSub connector, Kick connector, `!challenge` command. These are unbuilt and that is correct per the task's stated v1/Phase-2 split.

**Open, not decided here:** Google OAuth app-verification status and the YouTube Data API quota-increase outcome were not found recorded anywhere in this repository as dated written confirmation. Both remain open external dependencies; this reconciliation does not assert either is resolved or unresolved beyond "no dated evidence on file."
