# Decision — L14 viewer client response integrity

**Date:** 2026-09-09  
**State:** `Approved for local implementation by the owner's active QA goal`

Unchecked TypeScript casts do not validate runtime network data. Dashboard,
session, and deletion response parsing must fail closed on malformed nested
payloads, matching the existing public-profile parser pattern. This approves
only browser-side validation and tests; it does not alter backend behavior or
claim deployed/provider evidence.

## Implementation review — 2026-09-09

The client no longer uses unchecked casts for the three audited response types.
It has bounded, strict parsers matching the published contracts and fails
closed before UI state is populated. Focused hostile tests, web typecheck,
`git diff --check`, and the root verifier pass. External evidence remains open.
