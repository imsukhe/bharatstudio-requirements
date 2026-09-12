# Decision — L01 viewer session lifecycle contract slice

**Decision:** Approve the separate viewer-session lifecycle publication.

The four operations are already runtime-tested as caller-scoped. The contract
must preserve the separate token namespace, fail closed with 401/404/503 where
the runtime does, and disclose deletion retention without creating a new
authentication artifact. This is a local documentation/fixture decision, not
an identity-provider or production-data approval.

## Corrective finding

The initial contract review exposed an unbounded SQL session-list function.
The published bounded response is retained; a forward migration must impose the
100-row limit in the database, ordered by newest activity, and a role-separated
SQL test must prove the bound before this decision is accepted as implemented.

## Implementation review — 2026-09-09

The finding was remediated rather than documented around. Migration `0112`
keeps the existing caller predicate, adds deterministic newest-first ordering
and a 100-row bound, and restores explicit role grants. The L14 test was added
to the standard disposable runner and now proves 101-to-100 truncation, oldest
row exclusion, and cross-viewer isolation. The lifecycle OpenAPI operations and
strict fixtures add no identity/token response fields. The full local verifier
passes; all deployed/provider/staging/production gates remain outside this
local acceptance.
