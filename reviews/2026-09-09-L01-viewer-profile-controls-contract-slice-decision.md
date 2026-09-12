# Decision — L01 viewer profile controls contract slice

**State:** `Locally accepted after independent regression verification`

Authenticated viewer profile controls require the separate viewer bearer
scheme, precise response projections and browser-side validation. This decision
approves contract/test hardening only; provider, production, staging, device,
and legal conclusions remain outside local evidence.

## Security and quality review — 2026-09-09

Reviewed implementation against the authority slice and adversarial tests.

- The badges route no longer serializes a raw store result. Its explicit
  projection excludes account IDs, payment IDs, provider identities and any
  future persistence fields; API and schema negatives prove this.
- Profile visibility now fails closed for incoherent public/private slug state.
  Authenticated callers do not receive an unauthenticated response when only
  the profile dependency is unavailable. Database conflict/invalid-input codes
  remain client-conflict responses; unclassified failures become retryable 503
  without database detail.
- Browser parsing now requires the complete v1, exact-key response and rejects
  privacy-widening/contradictory data before it can update the UI.
- `git diff --check` passed in both Alerts and requirements trees. The complete
  local verifier passed after the focused hostile tests. No production-readiness
  conclusion is warranted: no provider, staging, deployed IAM, real device or
  production privacy/legal evidence was performed.
