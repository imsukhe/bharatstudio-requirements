# Review — AUD-MC-01 Master Canvas bootstrap reconciliation retry

**Status:** `Conditionally complete — self-review passed; independent review unavailable`  
**Reviewer:** Sukhdev Singh (self-review until independent review is available)  
**Scope:** `AUD-MC-01-master-canvas-bootstrap-retry.md`

## Required review checklist

- Inspect the final page, connection, and reconciler—not only implementation notes.
- Force module/layout failures independently, then a later lifecycle connection; verify
  precise last-known-good/fail-closed application without guessed entitlement/layout.
- Force many lifecycle signals during one unresolved read; prove bounded coalescing.
- Dispose before delayed completion; prove neither value applies and the transport
  listener count returns to the pre-bootstrap state.
- Verify no polling, second fetch stream, per-module session, extra bearer-token path,
  new endpoint, migration, or change to overlay acknowledgement/replay occurred.
- Re-run recorded checks, inspect `git diff --check`, and record exact redacted
  commands/results, paths, findings/disposition, rollback proof, and review independence.

## Required disposition

Real browser/OBS network-failure recovery is external evidence. It must remain pending
unless actually performed in a safe environment; local state-machine coverage is not a
substitute.

## Fresh hostile self-review — 2026-09-18

**Reviewer:** Sukhdev Singh (self-review; independent review unavailable).  
**Reviewed worktrees:** Alerts base `d5cebc6`; requirements base `4294a00`.

| Finding | Severity | Disposition and evidence |
|---|---|---|
| A transient initial modules/layout fetch failure left Master Canvas permanently default/stale until a whole page reload. | P1 delivery/recovery defect | Fixed by an immediate bounded reconciliation plus retry on only the existing shared transport's successful connection lifecycle. Unit tests prove failure then recovery with independent module/layout handling. |
| Connection/reconnect bursts could turn recovery into overlapping read fan-out. | P1 performance seam | Fixed by single-flight reconciliation with one coalesced follow-up pair. Tests prove multiple signals during an unresolved read perform exactly two read pairs, never more. |
| A new connection hook on the ordinary module interface would grant every module configuration-recovery authority and break unrelated mocks/contracts. | P2 boundary defect | Fixed during implementation: `subscribeToConnection` is a Canvas-page-only structural extension returned by the factory, while modules retain the narrow `MasterCanvasConnection` interface. Typecheck passed. |
| A synchronous loader/apply exception could strand a first reconciler version and suppress later recovery. | P1 resilience defect | Fixed before closure with settled microtask wrappers, `finally` state release, independent guarded application, and focused regression. |
| A hidden OBS browser source could retain a configuration-only connection. | P1 resource/lifecycle defect | Fixed by the visibility-aware recovery binder; it unsubscribes on hidden, reopens/reconciles once on visible, and disposes listeners/late state application on teardown. Focused test proves all paths. |

**Negative checks:** no bootstrap timer/polling call, storage use, token copy, new API endpoint,
event-payload subscription, or second transport appears in the new recovery files. The
page keeps existing scoped bearer fetches and server-authoritative parsers. The Canvas
source header was corrected so no stale "read once" claim remains. `git diff --check`
passed.

**Rollback/recovery:** revert the two bootstrap helper/test pairs, connection lifecycle
extension/test, and Canvas page wiring together. No migration, stored state, event replay,
or provider action needs repair. The prior default-horizontal/fail-closed behaviour is
recoverable solely through source rollback.

**External/release gate:** a safe browser/OBS source with controlled initial configuration
read failure and connection drop must visibly recover while preserving the one-transport
bound before runtime/OBS readiness can be claimed. No such external evidence is claimed.
