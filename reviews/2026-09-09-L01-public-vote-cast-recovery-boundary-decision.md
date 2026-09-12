# Decision — L01 public vote recovery boundary

**State:** `Accepted for local completion; external deployment evidence pending`

Unexpected durable-store failure is an operational condition distinct from a
client-invalid vote. This decision permits only redacted retryable recovery.

Review confirms availability and client-invalid outcomes remain distinct and
that no backing-store error detail is exposed. Full local verification exits 0;
external deployment evidence remains open.
