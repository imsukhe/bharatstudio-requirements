# Capability-admin control-plane slice — CTL-04, CTL-05, CTL-13

**Status:** `Approved for local implementation — passkey MFA selected 2026-09-18; deployment configuration and external evidence remain gated`
**Owner:** Sukhdev Singh
**Authority:** `00_LAUNCH_SCOPE_AUTHORITY.md`; `01_MASTER_RELEASE_AUTHORITY.md`; `../../FULL-PRODUCT-DEFINITION.md` §20.2–§20.6.1 and §31 rows CTL-04, CTL-05 and CTL-13.

## Purpose and boundary

This slice closes the remaining administrative surface of the capability control plane: an authenticated platform administrator can inspect capabilities, make a governed change, see a server-derived impact preview, and use the emergency-kill path. It does **not** alter Layer 1 correctness entitlements, pricing, payment billing, retention, provider configuration, or creator data. Existing API change-management and emergency-kill rules remain the policy source of truth.

The slice is deliberately gated on CTL-13. Section 20.6 requires this high-value panel to be behind platform-admin authentication **with MFA**. The existing durable admin registry (ADM-07) explicitly states that MFA policy, enrollment, recovery and provider are undecided. Building a reachable mutation console before that decision would conflict with the authority rather than complete it.

## Proposed implementation shape

1. A forward-only Alerts migration adds a bounded, index-backed, security-definer impact-preview function. It derives affected-channel and currently-live-channel counts from authoritative channel/capability state; callers cannot supply or override the counts. It exposes no channel, member, payment, viewer, or configuration data.
2. Alerts API exposes a platform-admin-only preview endpoint and changes emergency kill to consume the server-derived counts in the same transaction as the kill. A stale/cross-capability preview cannot be submitted as evidence. Existing emergency-expiry, ratification, audit and review rules stay intact.
3. The standalone `bharatstudio-admin` console receives a capability registry page with read-only state, change proposal/approval workflow, preview-before-mutation, reason input, emergency-kill confirmation, error/recovery states, and audit/event visibility. It never implements Layer 1 edits or prices.
4. CTL-13 supplies the chosen MFA enforcement and durable admin registry integration before the UI route can be reachable outside local development.

## Data, security and operations

The preview processes channel identifiers only inside PostgreSQL and returns two aggregate integers plus the capability key/version. No personal data, amounts, payment records, or creator settings are returned or logged. All mutations retain existing append-only audit behavior and reason rules. Metrics use outcome-only bounded labels; logs must not include an admin token, a channel identifier, or free-text incident reason. Failure fails closed: unavailable/invalid preview disables the mutation control and returns a retryable error without changing capability state. A forward rollback migration removes only newly added functions/tables after dependent application code is rolled back; existing migrations are never edited or removed.

## Approval and external gates

The owner selected application-managed passkeys in
`../../reviews/2026-09-18-ctl-admin-control-plane-decision.md`. Local implementation is
approved. This slice still has no approved production deployment, RP ID/origin/elevation-lifetime
configuration, recovery-policy approval, or external evidence claim.
