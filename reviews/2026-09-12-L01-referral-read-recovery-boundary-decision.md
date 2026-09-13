# Decision — L01 referral read recovery boundary

**State:** `Accepted for local verification; deployment evidence remains open`

This authorizes only safe availability mapping and deterministic redaction
tests for referral reads. It does not broaden referral visibility, modify
referral state, or claim external deployment evidence.

## Review outcome — 2026-09-12

The audit found that a durable referral-store rejection bypassed the route's
existing unavailable envelope. Both read operations now return a redacted,
retryable 503 on rejection. Focused tests prove no secret-shaped failure text
is emitted, and the full deterministic verifier passes. Access and projection
semantics remain unchanged.
