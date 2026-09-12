# Decision — L16 vote-option cardinality alignment

**State:** `Accepted for local completion; external deployment evidence pending`

The v1 rendering contract and browser reject tallies exceeding 16 options;
the authoritative creation procedure must enforce the same invariant under a
per-definition lock. This is a correctness and availability bound, not a
product-capability change.

Review confirms migration 0116 preserves the existing function signature,
authorization checks, validation, grants, and client outcome while adding the
parent-row serialization lock and cardinality guard. Full deterministic local
verification exits 0; production/staging concurrency evidence is not claimed.
