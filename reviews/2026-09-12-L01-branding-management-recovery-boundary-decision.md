# Decision — L01 branding management recovery boundary

**State:** `Accepted for local verification; deployment evidence remains open`

The authenticated Lottie management routes must not expose an implementation
error when the durable branding store is unavailable. This authorizes only the
redacted recovery mapping and focused deterministic tests; it does not change
role checks, tier entitlement, asset storage, or external deployment behavior.

## Review outcome — 2026-09-12

The audit reproduced an unhandled durable-store failure risk in authenticated
Lottie list and delete handlers. Both now use the same redacted retryable
availability boundary as upload. The focused test passes 9/9 and proves that
secret-shaped error text cannot reach the response. The deterministic full
verifier also passes. No authorization, tier, or data ownership semantics were
broadened.
