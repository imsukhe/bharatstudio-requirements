# RT-02 — overlay channel-keyed fanout: decision record

**Task:** `../active/tasks/RT-02.md`
**Reviewer:** Sukhdev Singh (owner self-review; independent reviewer unavailable)
**Scope:** Replace the flat, instance-wide overlay wake-up waiter set with a channel-keyed subscriber registry; add per-channel single-flight deduplicated durable replay; add explicit, optional per-instance/per-channel admission ceilings with a retryable rejection; keep RT-01 (idle-poll removal, bounded jittered fallback) intact and passing unchanged.

## 1. Product/market review (§2 of the operator's command)

Bounded, official-documentation-only research into how comparable products handle live event delivery and per-channel/per-broadcaster fanout, and what that implies for RT-02's design. Sources and access dates below; this is evidence for a backend delivery-path correction, not a market or product recommendation.

- **Twitch EventSub** — subscriptions are scoped per broadcaster: every channel-specific subscription condition requires `broadcaster_user_id` (e.g. channel-follow), so Twitch's own fanout unit is "one broadcaster's subscribers," the same granularity RT-02 adopts as "one channel's sessions." Delivery is at-least-once, with Twitch resending a notification it is unsure was received and reusing the same message id on resend so the receiver can deduplicate; a webhook subscription can be revoked if the delivery failure rate is too high. Sources: [EventSub Subscription Types](https://dev.twitch.tv/docs/eventsub/eventsub-subscription-types/), [EventSub overview](https://dev.twitch.tv/docs/eventsub/) — accessed 2026-09-15. (`dev.twitch.tv/docs/pubsub/`, the older, now-superseded PubSub system, returned HTTP 403 to automated fetch and was not evidenced directly; EventSub is Twitch's current documented system and the more relevant comparator.)
- **Discord Gateway sharding** — a deterministic formula (`shard_id = (guild_id >> 22) % num_shards`) routes every guild's (≈ "channel's") events to exactly one shard; a shard is capped at 2,500 guilds, and apps beyond that must shard. This is the same principle RT-02 uses at one level down (channel-keyed routing within one instance, not instance-level sharding), and it is a stronger, load-bearing precedent for "route by owning entity, never broadcast to everyone" than a hint — it is how a live-events platform at much larger scale keeps fanout bounded. Source: [Discord Gateway — Sharding](https://docs.discord.com/developers/events/gateway) (redirected from `discord.com/developers/docs/events/gateway`) — accessed 2026-09-15.
- **YouTube Live Chat Messages API** — the base mechanism is polling (`liveChatMessages.list`), with the server telling the client a `pollingIntervalMillis` to wait before polling again; the docs note this exists to avoid unnecessary quota consumption, and recommend `streamList` specifically to reduce "constant polling." This is a directly on-point negative example: it is the same shape of problem RT-01 already fixed (idle overlays polling every few seconds) and a reminder of why RT-02's channel-keyed wake, not broadcast-then-filter, is the right shape for the next scaling step. `liveChatId` scopes/isolates delivery per broadcast, the same "one key, one fanout group" pattern. Source: [`liveChatMessages.list`](https://developers.google.com/youtube/v3/live/docs/liveChatMessages/list) — accessed 2026-09-15.
- **OBS Browser Source** — no official OBS Project documentation page describing reconnect/reload/dedup semantics for the browser source was reachable (an attempted `obsproject.com/kb/...` URL 404'd; the OBS developer-docs domain returned 403 to automated fetch). Community evidence (GitHub issues under the official `obsproject` organisation, and forum threads) indicates the browser source reloads the page on scene switch or a manual "Refresh Cache" action, which is consistent with why RT-01's durable-cursor-replay-on-reconnect design (already shipped, unmodified by this task) is the correctness mechanism for alert-loss risk, not anything RT-02 changes. Treated as secondary/community evidence only, not cited as authoritative product behaviour, per this task's "official documentation only" instruction — recorded honestly as a gap rather than overclaimed.
- **Streamlabs / StreamElements** — neither publishes architecture-level documentation of alert/overlay fanout internals; their public docs cover widget configuration and setup, not delivery mechanics. No finding to record beyond that absence.
- **Kick** — no stable, authoritative public API documentation was located covering live-event fanout. No finding to record.

**Evaluation against the operator's specific criteria:**

| Criterion | Finding |
|---|---|
| Switcher friction | None expected and none found — this is a backend delivery-path fix with zero creator- or supporter-facing surface; no comparable product's *user-facing* switcher behaviour is implicated |
| Creator-visible latency | Improved, not degraded: channel-keyed wake removes cross-channel replay contention that would otherwise add latency under load on busy instances, consistent with Twitch's and Discord's per-owning-entity routing |
| Alert-loss risk on reconnect | Unchanged by RT-02 — durable cursor replay (RT-01, already shipped) remains the correctness path; RT-02 only changes which sessions wake and how many reads one notification causes. A malformed/unroutable notification (RT-02.8) wakes nobody, exactly as a dropped/garbled Twitch or Discord message would rely on the receiver's own durable state, not the notification, for recovery |
| Multi-widget/multi-source behaviour | Not applicable — Master Canvas/PRF-02 (the multi-widget-to-one-connection consolidation) is explicitly out of scope for this task |
| Accessibility and localisation | None expected, none found — no user-facing copy or interaction changes |
| Reliability | Strengthened: explicit admission ceilings with a retryable `503` (never a hang) mirror the posture of Twitch's failure-triggered subscription revocation and Discord's `max_concurrency`-gated connection admission — an explicit, observable limit rather than an unbounded queue or a silent stall |

**Referred to Opus:** none. The research produced no recommendation that would require a product, pricing, legal, provider or scope decision beyond what `FULL-PRODUCT-DEFINITION.md` §19.0/§19.4/§19.5 already specifies and this task already implements. Said plainly, per the operator's instruction, rather than manufacturing a recommendation: **nothing actionable beyond the existing authority surfaced.**

## 2. Design decisions this command did not settle

1. **`OverlayStore.resolveSession` and `OverlayStore.replayRaw` are optional interface members**, not required ones. The real SQL-backed store (`createSqlOverlayStore`) always implements both, so production traffic always gets channel-keyed fanout, per-wake revalidation, and per-channel dedup. Making them optional let every pre-existing overlay-SSE test in `apps/api/test/app.test.ts` (~15 tests covering CORS, reconnect timing, cursor resumption, replica behaviour, bounded-close semantics — none of them about channel fanout) keep its original fixture and assertions, falling back to the documented pre-RT-02 per-session path (`fetchEvents`'s `store!.replay(...)` branch) when a store doesn't implement the new methods. `OverlayWakeup` itself was **not** given a compatibility shim — its `subscribe`/`wait`/`release`/`close`/`health` shape is the only shape, exactly as the command specified, because that interface change is small and mechanical to adapt every call site to (done: ~11 fixtures in `app.test.ts`, all converted via one `fakeWakeup()` test helper).
2. **Admission-ceiling configuration** (`OVERLAY_MAX_INSTANCE_SUBSCRIBERS`, `OVERLAY_MAX_CHANNEL_SUBSCRIBERS`) is read in `apps/api/src/config.ts` as optional positive integers with no default and no value invented — consistent with the explicit instruction not to invent a deployment number. Left unset in every environment until an operator sets one.
3. **Metrics wiring**: `apps/api/src/index.ts` now constructs `ApiMetrics` once, up front, and passes the same instance into both `createDirectOverlayWakeup` (for the notification-routed/unroutable counter, which fires from inside the direct-listener module, not a request handler) and `buildApp` — previously `buildApp` constructed its own `ApiMetrics` internally if none was supplied. This is the smallest change that lets one counter set see both request-time and listener-time events; it does not change any existing counter's behaviour.
4. **The channel-scoping "fallback" key** (`channelKey = session?.channelId ?? overlayId`, `apps/api/src/routes/overlay.ts`) uses the overlayId itself as the wake-up registry key when a store has no `resolveSession`. This only affects test doubles (the real store always resolves a channel), and preserves the pre-RT-02 granularity (one wake registration per overlay session) for anything still on that path.
5. **`contracts/openapi/v1.yaml` was not changed.** The route's response spec for `GET /v1/overlays/{overlayId}/events` does not currently document `401`/`503` at all (a pre-existing gap, not introduced here), and `ErrorEnvelope.errorCode` has no enumerated value list. Per the command's own instruction ("if and only if that file enumerates error codes for this route; check, then match whatever the file already does"), there was nothing to add `overlay_admission_limited` to without diverging from the file's existing, already-incomplete precedent for this route — doing so would have been scope creep on a pre-existing gap, not a required part of this task.

## 3. Pre-existing breakage found and fixed, not introduced by this task

`integration/overlay-wakeup.integration.ts` called `wakeup.wait(overlayId, timeoutMs)` — a shape matching **neither** the git-HEAD-committed `OverlayWakeup.wait(overlayId, timeoutMs, signal)` interface nor the uncommitted RT-01 session's `waitForNotification(overlayId, timeoutMs, signal)` rename. `git log` shows this file unmodified since the repository's first commit, so it was already broken (the method it calls has never existed under that name since the RT-01 rename) before this task began, and would have failed `pnpm db:test:l03` regardless of RT-02. Fixed to the new `subscribe(channelId).wait(timeoutMs)` shape and strengthened into a genuine RT-02 integration proof (two independent real Postgres LISTEN connections, both receiving the same raw `NOTIFY`, only the matching channel's subscription resolving) rather than merely patched to compile.

Two pre-existing SQL test files (`packages/db/tests/l07-mute-tts-enforcement.sql`, `packages/db/tests/l07-mute-synthesis-cost-gate.sql`) asserted `payload ->> 'ttsAudioUrl'` directly against `app_private.get_overlay_events` — a SQL-level contract this task's migration 0127 intentionally changes (per the operator's explicit instruction to move URL composition out of SQL). Both updated to read the new `tts_audio_artifact_id` column; no assertion was removed, only re-pointed at the column that now carries the same information.

## 4. Independent review

**Unavailable.** This is self-review by the implementing owner. No second reviewer inspected the worktree, the diff, or the evidence in this record. Per `governance/AGENTS.md`, this leaves the task `Conditionally complete` rather than `Verified`, and no release or launch claim follows from it.

**Disposition:** `Conditionally complete — local evidence; independent review unavailable`
**Owner:** Sukhdev Singh
**Follow-up/release gate:** An independent reviewer must inspect the actual worktree diff against this record before any state change beyond `Conditionally complete`. No external (staging, OBS, device, network, provider) evidence is claimed; RT-07's separate gates are untouched by this task.
**Decision lifecycle:** `Approved → Implemented → Verified` (conditionally complete pending independent review)

## Owner decision — 2026-09-16 — admission ceiling values stay unset

The orchestrator raised the one open decision this task could not settle: no approved
authority states a per-instance or per-channel overlay subscriber ceiling, and none is
derivable from §19.0's 2,000-concurrent-overlay design target or the Cloud Run
800-request cap.

**The owner decided the ceilings ship unset.** `OVERLAY_MAX_INSTANCE_SUBSCRIBERS` and
`OVERLAY_MAX_CHANNEL_SUBSCRIBERS` have no default; admission is bounded only by the
platform's own request-concurrency cap, exactly as it was before this task. The
enforcement mechanism, the retryable `503 overlay_admission_limited` and the slot-release
path are built and tested, so choosing a value later is configuration, not code.

The value is blocked behind `active/tasks/ENV-08.md` (the staged run at target
concurrency), which is itself blocked on a staging environment. Nothing else in RT-02
depends on it.

## Register state, decided by the orchestrator after audit — 2026-09-16

- **RT-01: `X` → `U`.** The idle poll is gone and an idle overlay with a connected
  listener performs no store read.
- **RT-02: `X` → `P`, deliberately not `U`.** Channel-keyed fanout and per-channel
  deduplicated replay are done and locally verified, but the row also asks for *explicit*
  admission limits, and with the ceilings unset there is no limit in effect. Marking it
  `U` would let a reader conclude limits are enforced. `P` is the honest letter and it
  keeps the row visible until ENV-08 closes.

Neither letter is a release claim. RT-07 still gates every performance statement.

## Independent review

Still unavailable. The orchestrator's audit was adversarial and independent of the
implementer, and it re-ran every check itself rather than accepting the implementation
report — but it is not a third-party review, and this task remains
`Conditionally complete` on that basis.
