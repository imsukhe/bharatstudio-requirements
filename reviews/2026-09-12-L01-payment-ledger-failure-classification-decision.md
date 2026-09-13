# Decision — L01 payment ledger failure classification

**State:** `Accepted for local verification; deployment evidence remains open`

This authorizes a narrow error-classification correction for a financial read
surface: client cursor errors remain 400, while durable-store outages receive a
safe retryable availability response. No ledger mutation or provider adapter is
in scope.

## Review outcome — 2026-09-12

The review confirmed the former catch-all incorrectly reclassified an outage as
a client cursor error. A typed cursor error now makes the boundary explicit;
all other failures are redacted, retryable 503s. Focused tests and the full
deterministic verifier pass. Financial data and provider behavior were not
changed.
