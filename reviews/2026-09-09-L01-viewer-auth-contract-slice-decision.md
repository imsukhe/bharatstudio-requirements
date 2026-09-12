# Decision — L01 viewer authentication contract slice

**Decision:** Approve publication of the bounded unauthenticated viewer-auth
surface as a separate v1 contract slice.

The runtime already treats viewer tokens separately from creator sessions. The
published contract must preserve that boundary, use a dedicated security scheme
for future authenticated viewer routes, and state only fixed non-enumerating
password-reset outcomes. No production/session/provider behavior is approved or
changed by this documentation decision.

## Implementation review — 2026-09-09

The contract now has four viewer-auth operations with exact bounded request and
success/error shapes. `viewerBearerAuth` is declared separately from the
creator session scheme for subsequent authenticated viewer operations. Three
new synthetic fixtures have no live secret material and are tested against
identity/email/access-token injection. Contract and both application suites
pass. The slice makes no claim about provider, deployment, or production
identity readiness.
