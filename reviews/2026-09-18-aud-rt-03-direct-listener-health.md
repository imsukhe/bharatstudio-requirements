# Review — AUD-RT-03 direct listener health

**Status:** `Conditionally complete after self-review`  
**Reviewer:** Sukhdev Singh (self-review until independent review is available)  
**Scope:** `AUD-RT-03-direct-listener-health.md`

## Required review checklist

- Inspect the actual direct adapter and package-supported connection close callback;
  prove no invisible convenience-listener reconnection can leave health stale.
- Exercise initial failure, post-registration close, close during waits, replacement
  registration, stale callbacks and shutdown. Confirm one loss produces one sequence.
- Verify the overlay route's catch/fallback remains bounded and durable replay is
  unchanged, with no new browser/client connection or public control path.
- Confirm hard-coded/internal channel handling, no new data/permissions/configuration
  or migrations, clean resource shutdown, exact tests/evidence and rollback posture.
- Record source paths, outputs, findings/disposition and independent-review status.

## Self-review disposition — 2026-09-18

**Result:** No reproducible local finding remains for AUD-RT-03.

- Inspected the final adapter against the installed PostgreSQL client 3.4.9 source
  and declaration: the prior convenience listener owned an invisible replacement
  socket, whereas the corrected direct adapter owns the listener and propagates its
  connection close to the health state machine. Its notification hook is intentionally
  isolated and covered by real-database integration because that runtime hook is not
  present in the package declaration.
- Inspected attempt handling: close/rejection uses one attempt ID, invalidates it
  before scheduling replacement, and registration/close callbacks check identity.
  The focused regression proves one failure/reconnect sequence, false health until
  current re-registration, stale callback immunity, matching-channel delivery and no
  shutdown reconnect.
- Ran the disposable PostgreSQL harness. It terminated the actual direct listener
  backend after registration, observed an in-flight wait reject
  `overlay_listener_unavailable`, observed `connected=false`, then observed exactly
  one replacement and delivered a matching notification. This exercises the real
  adapter rather than a test double.
- Confirmed the existing API overlay route turns that rejection into its bounded
  jitter/durable-replay path, and existing metric rendering reads the same health
  object. No migration, new public endpoint, browser connection, polling loop,
  permission, payload, provider action, personal data, dynamic channel or config was
  added. Full suites/builds/contracts/harness/diff check passed; exact output is in
  the linked task and acceptance record.

Rollback is a source revert only; no database state is changed by this task. The
existing durable replay path remains the correctness mechanism during listener loss.

## Remaining external disposition

Independent review is unavailable, so this is self-review only. Managed PostgreSQL
and network-loss, browser/OBS replay latency, staging, deployment and production
evidence remains external; do not claim it from local failure injection.
