# TC-CTL-05 — capability-impact preview acceptance plan

**Task:** `../active/tasks/CTL-05.md`  
**Status:** `Blocked — YouTube Live selected; durable v1 projection and freshness contract remain open`

| ID | Required proof |
|---|---|
| CTL05.1 | Preview returns only capability key/version plus affected and live non-negative aggregate counts. It never returns identifiers or payments. |
| CTL05.2 | Counts are derived server-side from the authoritative durable capability/live-state definition; a client cannot supply, alter or replay them. |
| CTL05.3 | Privileges/RLS deny non-admin and direct table access; invalid capability and unavailable store fail safely without enumeration. |
| CTL05.4 | An emergency kill records the authoritative counts atomically; mismatched/stale capability state cannot be submitted as a different preview. |
| CTL05.5 | Concurrent preview/change/kill operations preserve the existing append-only audit, expiry, ratification and revert behavior. |
| CTL05.6 | Migration harness, role-separated SQL proof, API positive/negative contract fixtures, integration/replay/race tests, explain-plan proof and rollback forward migration pass. |

## Evidence protocol

Use synthetic channels and live-state fixtures. Include the exact `EXPLAIN` plan and a test that fails if the browser-count parameters or direct-count database write are restored. Do not report a locally synthesized count as production live-channel evidence.

The implementation-readiness inspection confirms there is no current durable live predicate: the
Companion activation API documents `streamPaired` as always false. The owner selected YouTube Live,
but the existing active-broadcast lookup is Phase 2 and in-memory only. This record must not accept
that process state, an overlay connection, active mission, event recency or a client-provided count
as a substitute. The completed v1 proof must exercise durable `live`/`offline`/`unknown` transitions,
stale/error fail-closed preview, atomic audit binding and a separate v1 collector—not the Phase 2
poller.
