# Step 0 JIT active-record decision

**Date:** 2026-09-15  
**Owner/decision maker:** Sukhdev Singh  
**Scope:** Governance semantics for Step 0 only

## Decision

Step 0 semantic closure means every §31 identifier is classified exactly once as
`mapped-existing` or `new-record-required`. Every `new-record-required` row carries
item-specific `missing_behavior` and `-` task/acceptance/review targets. A capability
lane creates its ten-field `active/` task, acceptance/test record, and review/decision
record just in time immediately before that capability is implemented.

This does not create 717 placeholder records, change any mapping classification, or
approve Step 0.25. It does not grant release, provider, staging, legal, security,
deployment, or production approval. Existing mapped L-track evidence remains local
inventory credit only and is not release evidence.

## Evidence and enforcement

`tools/traceability.py`, `tools/bootstrap_check.py`, and
`tools/doc_consistency.py` validate the nine-field mapping, lifecycle vocabulary,
item-specific unresolved behavior, safe targets, and complete ten-field metadata for
rows that are actually taken. The mapping and generated audit contain all 783 IDs
exactly once; current reconciliation is 66 mapped-existing and 717
new-record-required, with active-record eligibility 0.

The JIT rule is fail-closed: an all-rows-active policy is invalid, unsafe or missing
active task records fail validation, and a `new-record-required` row cannot carry
evidence targets before its lane is taken. This is an owner self-review; independent
review and all external gates remain open.

**Disposition:** Conditionally complete — semantic mapping/JIT governance closure only;
implementation records remain JIT and Step 0 is not release complete.
