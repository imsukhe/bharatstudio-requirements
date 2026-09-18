# Review — CTL-07 legacy kill-route remediation

**Date:** 2026-09-18
**Owner:** Sukhdev Singh
**Reviewer:** Self-review of the current Alerts worktree; independent review pending.
**Status:** Superseded — merged into `reviews/2026-09-17-ctl-emergency-kill-implementation.md`

This duplicate corrective review was reconciled on 2026-09-18. Its finding and evidence now live
in the existing CTL-07 review record; it is retained only as an archive note.

## Reachability finding

The current API registers both POST /v1/admin/capability-registry/{capabilityKey}/kill, implemented
by routes/capability-change-management.ts through staff_kill_capability_now, and POST
/v1/admin/capability-registry/{capabilityKey}/emergency-kill, implemented by
routes/capability-kill-events.ts through the §20.6.1 event-sourced workflow.

The first path is explicitly documented in current OpenAPI as an immediate, ordinary,
no-expiry/no-ratification kill. The second implements the controlling rule's 24-hour expiry,
second-admin ratification, escalation, immutable audit and review block. Both set the same
capability kill state. This is a real bypass of §20.6.1, not merely duplicate naming.

## Disposition

Remove the legacy route and all contract/runtime references. Do not redirect it, keep it hidden,
or preserve it as a backward-compatible alias: any alias recreates the bypass. This is an
authorized correction directly compelled by §20.6.1; it has no material product decision.

## Required verification after approval

1. Run focused API route and contract tests proving the old URI cannot mutate state and the
   emergency URI retains auth, expiry, ratification, review and unavailable failure behavior.
2. Run the full Alerts deterministic suite, migration harness, role-separated SQL proof,
   OpenAPI/fixture validation, typecheck/build, git diff --check, and a fresh route inventory.
3. Inspect the actual final registrar, OpenAPI, domain/store interfaces and tests for another
   API-reachable call to staff_kill_capability_now; remove every such route.
4. Record redacted command output and revision, then have a fresh reviewer verify the final
   worktree independently. External MFA/staging evidence remains outside the scope of this change.
