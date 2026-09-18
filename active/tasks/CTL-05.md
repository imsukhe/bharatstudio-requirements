# CTL-05 — authoritative capability-change impact preview

**Status:** `Blocked — YouTube Live selected as source; durable v1 liveness projection is not yet implemented`

| Field | Value |
|---|---|
| **Scope phase** | `v1`; Phase 0 capability-control-plane foundation. Replace caller-supplied emergency-kill impact counts with a server-derived preview of affected channels and currently live channels, available to the approved CTL-04 admin UI. |
| **Owner** | Sukhdev Singh |
| **Tier and gate** | Platform-admin/MFA-only operational control; no creator, public, overlay, Companion or marketing surface. Counts inform a change and never themselves grant a capability. |
| **Personal-data class** | Aggregate operational data only: capability key/version and two non-negative counts. No channel IDs, user IDs, viewer/payment data, settings, or raw incident reason leave PostgreSQL. |
| **Provider or legal dependency** | Owner selected YouTube Live as the source on 2026-09-18. The current YouTube connector/provider access, quota, liveness freshness, durable projection and deployment evidence are required technical gates. CTL-13 MFA policy is a security dependency for the reachable admin route. No legal or retention decision is introduced. |
| **Failure behaviour** | Fail closed. If the preview cannot be derived, is stale, changes capability identity, or its database transaction cannot commit, mutation is rejected and the existing capability state remains unchanged. Counts are never accepted from a client. |
| **Kill switch** | The only state-changing consumer is the existing bounded emergency-kill workflow. The preview endpoint has no write effect. A forward rollback restores the pre-existing interface only if the entire CTL slice is rolled back; production rollout must not reintroduce client-trusted counts. |
| **Acceptance test** | `tests/TC-CTL-05-capability-impact-preview.md` |
| **Evidence location** | Proposed paths and test matrix are in the linked acceptance/review records; reproducible redacted commands are added after implementation. |
| **Rollback** | Revert application endpoints and UI first, then use a new forward migration to drop only new preview functions/tables. Never alter migrations 0149–0164 or their immutable kill-event audit history. |

## Required implementation and proof

The implementation must add a forward migration, RLS/privilege proof, API/OpenAPI schema and positive/negative fixtures, durable API store/runtime wiring, and tests. It must compute counts from current capability resolution with an index-backed bounded plan. A mutation must bind to authoritative current state, not trust a browser timestamp or count. The SQL and API tests prove tenant isolation, one capability cannot be previewed/submitted as another, concurrent state change cannot apply a stale preview, and an administrator cannot fabricate counts.

The live-channel predicate is not assumed: the implementation planner must inspect the existing authoritative stream-session/live-state schema and cite it. If no durable definition exists, that is a separate decision/blocker rather than an invented proxy such as recent activity.

## 2026-09-18 implementation-readiness finding

CTL-13 is conditionally complete locally, so MFA is no longer the dependency. The required source
inspection found no durable stream-session/live-state relation in Alerts. The current Companion
activation contract explicitly states that `streamPaired` is always false because Stream reports no
liveness signal to this API (`bharatstudio-alerts/contracts/openapi/v1.yaml`, Companion activation
schema). Overlay connections, active goals/missions, recent events, and Companion commands are not
authorised substitutes for a creator being live. Therefore the task cannot honestly derive the
required `liveChannelCount` or bind it atomically without a recorded owner choice.

## Owner source selection — 2026-09-18

The owner selected **YouTube Live** as the v1 source for `liveChannelCount`. Source inspection
confirms that `services/youtube-poller-go/internal/youtube/client.go` can query an active YouTube
broadcast, and `internal/poller/poller.go` treats an active broadcast with a non-empty live-chat ID
as live. However, the source is explicitly Phase 2 under `bharatstudio-alerts/AGENTS.md`; its
result is held only in `channelState.liveChatID` process memory and is never written to PostgreSQL.
It therefore cannot be used for a v1 global-kill preview or immutable audit.

CTL-05 must create a separate v1 durable YouTube-liveness projection rather than repurpose that
Phase 2 poller. A successful provider observation of an active broadcast with a non-empty live-chat
ID may transition a connected channel to `live`; a successful no-active-broadcast observation may
transition it to `offline`; provider error, quota exhaustion, expired credential or overdue
observation must be `unknown`, never silently `offline`. Emergency-kill preview must fail closed
while any relevant observation is unknown or stale. The exact freshness lease/cadence, connector
OAuth scope/credential grant and v1 collector deployment boundary are the remaining implementation
decisions and external/configuration gates; no browser, overlay or event-recency proxy is permitted.
