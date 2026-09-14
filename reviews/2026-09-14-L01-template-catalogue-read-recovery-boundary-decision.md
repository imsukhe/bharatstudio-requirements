# Decision — L01 template catalogue read recovery boundary

**State:** `Accepted for local verification; deployment evidence remains open`

This authorizes only the deterministic availability mapping and redaction test
for the existing template-catalogue read. It does not authorize custom template
runtime, raw HTML import, entitlement changes, or deployment claims.

## Review outcome — 2026-09-14

The review reproduced the catalogue store's rejection path and confirmed it
previously bypassed the declared unavailable envelope. The route now fails
closed as a redacted retryable 503. Focused tests, the API build, and the full
deterministic verifier pass. Template-runtime reachability was intentionally
not altered because it remains a separately governed, deferred surface.
