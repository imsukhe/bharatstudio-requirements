# Phase 2 YouTube — reopening plan

**Status:** `Deferred`  
**Not a v1 task or implementation authority**  
**Legacy sources:**

- `/Users/sukhdevsingh/Workspace/Personal /bharatstudio-alerts/repositories/bharatstudio-alerts/requirements/16_YOUTUBE_UNIFIED_EVENTS_AND_SUPPORTER_IDENTITY.md`
- `/Users/sukhdevsingh/Workspace/Personal /bharatstudio-alerts/repositories/bharatstudio-alerts/requirements/21_CATCHUP_OFFLINE_GROWTH_ENGINE.md`
- `/Users/sukhdevsingh/Workspace/Personal /bharatstudio-alerts/repositories/bharatstudio-alerts/tasks/youtube/P16-youtube-unified-events-and-supporter-identity.md`

## Reopening gate

Before implementation, create one new narrow approved FRD slice and resolve all of the following with dated primary/provider evidence:

1. Exact event set and user value: live chat, SuperChat, Super Stickers, memberships, subscriber/view changes, stream/broadcast metadata, catch-up summary.
2. OAuth scopes, verification/audit requirements, token encryption/rotation/revocation, channel ownership and Google policy.
3. Per-channel quota model, live-creator admission policy, polling interval/freshness promise, backoff/degradation and cost limit.
4. Go worker architecture: cursor ownership, sharding, bounded concurrency, overlap/reconciliation, durable idempotency, retry/lease recovery and no concurrent duplicate polling.
5. Data minimisation and supporter identity: no username-only merge; display-name history, confidence state, manual link/unlink audit, chat retention opt-in and raw payload policy.
6. How YouTube events enter existing Alert queue semantics without affecting payment correctness, and how summaries distinguish financial/engagement data.

## Work sequence

| ID | Work | Required evidence |
|---|---|---|
| YT-00 | Publish approved scope, consent, quota and privacy authority | provider/legal/security review |
| YT-01 | Define OpenAPI/event schemas and data model | contract/versioning tests |
| YT-02 | Implement encrypted channel connection/token lifecycle | revocation/access/log-redaction tests |
| YT-03 | Implement Go cursor/poller with bounded concurrency/shards | duplicate/cursor/crash/lease tests |
| YT-04 | Normalize/dedupe/store events and reconcile overlap | provider/channel/event uniqueness tests |
| YT-05 | Route eligible events to queues and overlay safely | no-drop, configuration snapshot, offline/replay tests |
| YT-06 | Build source/unified history and catch-up summaries | financial/engagement separation and baseline reset tests |
| YT-07 | Build Companion views only after API/data proof | RBAC/offline/privacy tests |
| YT-08 | Load, quota, failure and privacy review | production-equivalent staging evidence |
| YT-09 | Limited opt-in rollout and rollback | audit/monitoring/runbook/review evidence |

## Explicit non-goals until separately approved

- YouTube moderation actions/sync, public leaderboards, broad chat retention/search, multi-source workflows, Twitch/Kick/Discord, and any non-YouTube source.
