# L02 credential revocation before consent review

**Decision state:** `Implemented and locally verified; independent review and deployed evidence open`
**Level:** L3
**Date:** 2026-09-09
**Reviewer:** Self-review; independent reviewer unavailable.
**Authority:** `tasks/L02-security-rls-and-archive-proof.md`

## Finding

**P1 — fixed.** The reusable `requireAuthAndTerms` gate was applied to
credential containment endpoints. When a user had not yet accepted an updated
Terms/Privacy document, they could read their sessions/devices but could not
revoke a compromised session, remove a push token, or rotate/revoke an overlay
bearer token.

## Disposition

The four containment operations now use authenticated access only. They retain
their route-level schemas and their store-level owner scoping; no unauthenticated
or cross-user access was added. New credential issuance/configuration remains
on the existing consent gate.

## Reproducible redacted evidence

- `cd bharatstudio-alerts/apps/api && npx tsc --noEmit && npx tsx --test
  test/terms-gate.test.ts` — **3/3** pass; the pending-consent proof records
  successful session/device/overlay revoke and overlay rotation calls.
- `cd bharatstudio-alerts/apps/api && npm test && npm run build` — **401/401**
  API tests and production TypeScript build pass.
- `git diff --check` passed in Alerts and central requirements.

## Risk, rollback, and gates

This makes only authenticated, owner-scoped containment actions available
before consent; it does not weaken creation, payment, configuration, or
privileged-role writes. Reverting would restore the lockout flaw. Production
session provider, deployment/IAM, independent security review and real-device
evidence remain release gates; no production-readiness claim is made.
