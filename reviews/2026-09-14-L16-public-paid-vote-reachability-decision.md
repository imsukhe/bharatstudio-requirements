# Decision — L16 public paid-vote reachability correction

**Decision state:** `Approved for local implementation and self-review; no deployed evidence implied`

## Problem and decision

The L16 paid-vote SQL, checkout tag, tally, and overlay reads exist, but a normal public tip page cannot discover or select them. Worse, a rejected explicit tag was deliberately downgraded to a generic payment. That downgrade is unsafe for user intent: it can capture money after the product has represented the purchase as a vote.

The corrective contract is intentionally narrow: an unauthenticated channel-scoped read returns only active paid support-vote definitions and their option labels; an optional tip-form control selects one; and an explicit selected tag must validate durably before any provider order is made. A generic no-selection tip remains unaffected.

## Security and privacy

The database function is SECURITY DEFINER with fixed search path and exposes an allowlist projection only. It excludes queue ids, moderation, visual/config JSON, identities, payment amounts/tallies, and all cross-channel data. A validation failure is a redacted `400`, with no provider/order side effect. Read failure hides the optional control; it does not weaken checkout or infer a selection.

## Verification and rollback

Required evidence is the L16-08 SQL/API/browser cases, full deterministic verifier, image/build check, diff check, and self-audit of the call order. The change is additive and removable at the route/UI level. Staging, real payment-provider checkout, browser/OBS and independent review remain explicitly open.
