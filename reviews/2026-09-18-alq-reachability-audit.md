# ALQ reachability audit — 2026-09-18

Scope: the fourteen §31.3 Alerts & Queue rows claiming state `U` that had never been
re-verified since they were first written, plus `ALQ-18`, which claimed `A`.

Method: static reachability reading of `bharatstudio-alerts` at `4ed08d2`. For each row,
three things were established separately and never conflated — **mechanism** (does the
implementation exist), **reachability** (is there a caller path from a surface a user or an
external system can actually reach), and **enforcement** (is a claimed guarantee held where
it cannot be bypassed: a CHECK constraint, a trigger, an RLS policy, a `security definer`
function's declared `returns table` type, or a grant — not application code, not a comment,
not a test).

This is the §2 failure pattern check: code that exists, passes its tests and is committed,
but that nothing reachable ever triggers, is not usable however good its tests are.

## Outcome

Twelve of the fifteen rows are supported by the evidence as claimed. Two are not, and both
are corrected below. One (`ALQ-04`) already claimed `P` and remains `P`.

Notably strong, and worth recording because these are the guarantees most often overstated:

- **`ALQ-09`** duplicate-delivery consent is a `before insert ... for each row` trigger
  (`packages/db/migrations/0021_v1_l03_duplicate_consent_guard.sql:68-70`) raising `42501`.
  No caller can bypass it, including a buggy application path.
- **`ALQ-11`** role-scoped financial reads mask the amount inside the `security definer`
  function's own SELECT (`packages/db/migrations/0039_v1_l03_role_scoped_financial_reads.sql:32-69`),
  resolved from `channel_memberships`. Privacy is a property of the query, not a filter a
  caller could forget.
- **`ALQ-10`** the audit insert is unconditional and lives inside the same SQL function as
  the state change (`0062_v1_l03_l05_queue_policy_enforcement.sql:~112`), so an audited
  action cannot be performed unaudited.
- **`ALQ-12`** overlay tokens are looked up by sha256 fingerprint, never by raw-token
  comparison; the route schema accepts the credential only in `Authorization`, and the web
  client reads it from `window.location.hash`.

## Correction 1 — `ALQ-07` (U -> P)

"No-drop guarantee on every tier" is half true, and the half that is true is the half that
was easy.

What holds: a delivery row is never physically deleted. There is no DELETE path on
`event_outbox_deliveries` in any migration, and the admin "discard" action
(`0073_v1_l03_admin_dlq_tooling.sql:200-260`) writes a status marker plus an audit row
rather than removing evidence. That part is schema-enforced and genuinely untierable.

What does not hold: nothing ever moves an exhausted delivery to a terminal, detectable
state. `retry_event_delivery` (`0015_v1_l05_outbox_projection_refresh.sql:47-84`) always
resets to `failed_retriable`, uncapped, and no writer anywhere transitions a row to
`quarantined` on attempt exhaustion. A permanently stuck delivery is therefore
indistinguishable, to any automated observer, from a healthy in-flight retry. The only exit
is a human admin noticing and calling `/v1/admin/dlq/:id/discard`.

"Not deleted" is a durability guarantee. "Not dropped" was being read as an operational
one, and operationally the recovery is human-driven. The remaining work is the automatic
terminal transition that makes exhaustion visible — the `quarantined` status the CHECK
constraint already allows and nothing ever sets. Recorded P1.

## Correction 2 — `ALQ-18` (A -> X)

The row claimed the Master Canvas single-browser-source runtime was absent. It is not
absent; it is unreachable, which is a different failure and a much smaller remaining job.

What exists: `apps/web/app/overlay/canvas/master-canvas-runtime.ts` (single
`requestAnimationFrame` loop with a module registry), the rendered route
`apps/web/app/overlay/canvas/[overlayId]/page.tsx` composing roughly seventeen registered
modules over one connection via `master-canvas-connection.ts`, and the server module list at
`apps/api/src/routes/master-canvas.ts:146-174`.

What is missing: **no product surface hands a creator the URL.** Every reference to
`overlay/canvas` outside that route's own directory is a code comment — verified directly by
grepping `apps/` for the string and inspecting each hit. `apps/web/app/overlay/setup/` builds
the standalone `/overlay/{overlayId}` URL only. A creator cannot discover the canvas browser
source through the product, so the entire module catalogue is dark in practice.

This is the §2 pattern exactly, and the same shape as the `MED-21` correction of 2026-09-17,
inverted: there the register claimed something existed that did not, here it claims something
is absent that is built and unreachable. `X`, not `A`. Priority stays P0 — the impact is
unchanged, but the work is one URL-generation surface, not a runtime.

## Overstated claim found

`services/alert-worker-go/docs/CLOUD_TASKS_OPERATIONS.md` presents the dead-letter queue as
"configured, access-restricted, monitored and replayable" in a completed-state table, while
`deployment/cloud-tasks/queues.yaml` is explicitly marked an unapplied declarative starting
point. Combined with `ALQ-07` above, the DLQ is documented as more operationally ready than
the code enforces. Not corrected here — it belongs with the `ALQ-07` remediation.

## Limits of this audit

Static reading only; no suite was executed as part of it. `ALQ-04`'s real deployed
`DATABASE_URL_DIRECT` value was not and cannot be verified locally — only that
`apps/api/src/config.ts:163-181` would reject an obviously pooled endpoint, and only when
`nodeEnv` is staging or production; in dev and test that validation is skipped entirely.
Nothing here is evidence of production, provider or release readiness.
