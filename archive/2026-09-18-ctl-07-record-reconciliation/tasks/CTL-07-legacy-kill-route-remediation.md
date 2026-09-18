# CTL-07 — emergency-kill legacy-path remediation

**Status:** Superseded — merged into `tasks/CTL-07-emergency-kill-and-owner-identity.md`

This duplicate corrective task was reconciled on 2026-09-18. Its scope, evidence and review now
live in the existing CTL-07 authority/task/test/review trio; it is retained only as an archive note.

| Field | Value |
|---|---|
| **Scope phase** | v1; Phase 0 capability-control-plane remediation. Remove the reachable legacy kill HTTP path and its runtime surface so every API-reachable emergency global kill uses §20.6.1's bounded, auditable emergency-kill workflow. |
| **Owner** | Sukhdev Singh |
| **Tier and gate** | Internal platform-admin only; this narrows a privileged API surface. Existing platform-admin authorization remains, but the route must not serve as a non-MFA production control-plane claim. |
| **Personal-data class** | No new data. Existing append-only kill event/audit records remain untouched. Removed route payload reason must not be reintroduced through logs, metrics or compatibility aliases. |
| **Provider or legal dependency** | None. CTL-13 MFA remains a separate console/deployment gate and does not prevent removal of a weaker API path. |
| **Failure behaviour** | Requests to the removed path return a normal not-found response; they never fall back to emergency-kill, change capability state, or leak a capability's existence. Emergency-kill store failures remain fail-closed 503. |
| **Kill switch** | The full §20.6.1 emergency path remains the sole API-reachable capability kill. Its 24-hour expiry, second-admin ratification, escalation, immutable event log and post-incident-review gate are unchanged. |
| **Acceptance test** | tests/TC-CTL-07-emergency-kill-and-owner-identity.md |
| **Evidence location** | reviews/2026-09-18-ctl-legacy-kill-route-remediation.md; concrete revision and redacted commands are added after implementation. |
| **Rollback** | Revert only the new route/OpenAPI/domain/store test removals if a verified compatibility need is later approved. Never restore the legacy path as a production kill mechanism; use the full emergency workflow. No historical migration is edited. |

## Exact change

Remove POST /v1/admin/capability-registry/:capabilityKey/kill from the Alerts route registrar,
OpenAPI contract, domain/store interface, injected dependencies and route tests. Preserve ordinary
change proposal/approval, one-action revert, and all §20.6.1 emergency-kill routes. Add negative
API and contract tests proving that the old URI is not registered and cannot cause a capability
mutation, while the full emergency path remains reachable only under existing platform-admin
authorization.

## Why this is a correction, not a product choice

Section 20.6.1 defines global_kill as the sole emergency exception with mandatory expiry,
ratification, escalation, immutable logging and post-incident review. The current legacy route,
documented by migration 0152 as an ordinary, no-expiry, no-ratification kill, is a second,
looser way to make the same state change. It cannot coexist with the controlling rule. No new
policy, provider, pricing, retention or external behavior is introduced by removing it.
