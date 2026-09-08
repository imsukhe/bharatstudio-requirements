# PLATFORM-WP0 — Platform governance, threat model, and architecture definition

**Status:** `Approved — owner authorized implementation on 2026-08-28`
**Level:** L3
**Owner:** Platform engineering / security
**Depends on:** `pending/platform/PLATFORM-00-SHARED-IDENTITY-AND-ENTITLEMENTS-AUTHORITY.md`
**Blocks:** PLATFORM-WP1 through PLATFORM-WP6

## Objective

Define the new BharatStudio Platform's ownership boundary and safe implementation plan before repository creation or runtime code. The outcome is a reviewable, reversible basis for a shared account and mobile-store entitlement authority; it does not implement it.

## Authority and records

- **Authority:** [`../pending/platform/PLATFORM-00-SHARED-IDENTITY-AND-ENTITLEMENTS-AUTHORITY.md`](../pending/platform/PLATFORM-00-SHARED-IDENTITY-AND-ENTITLEMENTS-AUTHORITY.md)
- **Acceptance:** [`../tests/TC-PLATFORM-WP0-governance-architecture-definition.md`](../tests/TC-PLATFORM-WP0-governance-architecture-definition.md)
- **Review/decision:** [`../reviews/2026-08-28-platform-wp0-definition-review.md`](../reviews/2026-08-28-platform-wp0-definition-review.md)

## Initial implementation boundary and implemented-layout reconciliation

At definition time, these were the initial files permitted for WP-1 onward. The owner subsequently authorized the approved local Platform implementation; its actual Go command/package layout is listed immediately after this original boundary so the record cannot be mistaken for the current tree:

- `/Users/sukhdevsingh/Workspace/Bharat Studio/bharatstudio-platform/AGENTS.md`
- `/Users/sukhdevsingh/Workspace/Bharat Studio/bharatstudio-platform/CLAUDE.md`
- `/Users/sukhdevsingh/Workspace/Bharat Studio/bharatstudio-platform/README.md`
- `/Users/sukhdevsingh/Workspace/Bharat Studio/bharatstudio-platform/.gitignore`
- `/Users/sukhdevsingh/Workspace/Bharat Studio/bharatstudio-platform/contracts/openapi/v1.yaml`
- `/Users/sukhdevsingh/Workspace/Bharat Studio/bharatstudio-platform/contracts/events/v1/*.schema.json`
- `/Users/sukhdevsingh/Workspace/Bharat Studio/bharatstudio-platform/contracts/fixtures/**/*`
- `/Users/sukhdevsingh/Workspace/Bharat Studio/bharatstudio-platform/packages/db/migrations/*.sql`
- `/Users/sukhdevsingh/Workspace/Bharat Studio/bharatstudio-platform/services/platform-api/**/*` (superseded by the Go command layout below)
- `/Users/sukhdevsingh/Workspace/Bharat Studio/bharatstudio-platform/services/platform-store-ingress/**/*` (superseded by the Go command layout below)
- `/Users/sukhdevsingh/Workspace/Bharat Studio/bharatstudio-platform/services/platform-reconciler/**/*` (superseded by the Go command layout below)
- `/Users/sukhdevsingh/Workspace/Bharat Studio/bharatstudio-platform/services/platform-eraser/**/*` (superseded by the Go command layout below)
- `/Users/sukhdevsingh/Workspace/Bharat Studio/bharatstudio-platform/deployment/**/*`
- `/Users/sukhdevsingh/Workspace/Bharat Studio/bharatstudio-platform/tests/**/*`
- the four linked central records and their WP-specific successors.

The current approved local implementation is under `cmd/platform-api`, `cmd/platform-store-ingress`, `cmd/platform-reconciler`, `cmd/platform-eraser`, `internal/`, `packages/db/migrations/`, `contracts/`, `deployment/`, `tests/`, `go.mod`, `go.sum`, and `Dockerfile`. It remains confined to the Platform repository and does not authorize external provisioning or changes to Alerts, Android, or iOS.

No file in Alerts, Android, iOS, or another repository is in scope. At definition time the Platform repository did not exist; it was created immediately after approval with its required instruction files. This historical statement does not limit the present repository layout above.

## Work items

1. Keep the stated user, store, installation/device, session, provider, and entitlement identities distinct; document every trust boundary and data flow.
2. Create a threat model covering account takeover, OAuth/OIDC/PKCE/nonce replay, passkey challenge replay, malicious linking/unlinking, refresh reuse, token/key confusion, JWKS cache failure, store-notification forgery/reorder/replay, purchase-account conflict, refund/revoke lag, pack URL leakage, capability replay, data export/deletion abuse, logging/telemetry leakage, privilege escalation, and Platform outage.
3. Establish the service/database/contract model, no-direct-database rule, data minimisation/retention and deletion/tombstone design stated by the authority.
4. Establish clean migration, deterministic test, deployment, incident-revocation, and rollback plans. Do not provision any environment or credentials.
5. Create WP-1 contract work only after this record, the acceptance record, and the decision record are explicitly approved.

## Acceptance criteria

All `TC-PLATFORM-WP0` cases passed as a document/review gate. The owner explicitly approved the scope/non-goals, affected-file boundary, data model and retention, security/privacy design, migration plan, test plan, rollback plan, service/deployment model, and external prerequisites on 2026-08-28.

## Rollback

This pass only adds requirements records. Rollback is a documented `Superseded` decision and archival under the governance archive policy; no runtime/database/provider state exists to roll back.

## Evidence status

At the WP-0 definition gate, read-only evidence completed: governance instructions, current requirements authority, Alerts architecture/deployment conventions, and the two permitted mobile master documents. No runtime implementation, provider configuration, migration, deployment, or production claim had occurred at that point. Subsequent WP evidence is recorded in the linked authority, acceptance, and review records.
