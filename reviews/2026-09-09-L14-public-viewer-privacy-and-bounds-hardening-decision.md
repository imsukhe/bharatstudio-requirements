# Decision — L14 public viewer privacy and bounded-read hardening

**Date:** 2026-09-09  
**State:** `Approved for local implementation by the owner's active QA goal`

An immutable internal account identifier is unnecessary in the opt-in public
profile response and creates a correlation/privacy risk. The public projection
is therefore narrowed to the display name and stable public slug. Separately,
all collection reads exposed by the viewer API must be bounded; the private
dashboard receives a deterministic 100-row ceiling. The root QA command must
also execute the isolated SQL suite because its individual fixtures are not
safe to combine in a shared database.

This decision authorizes forward local migrations, contract narrowing, and
test-harness wiring only. It explicitly does not approve a provider flow,
production migration, privacy-law conclusion, deletion-retention conclusion,
or production-readiness claim. Evidence must distinguish local disposable
proof from those external gates.

## Implementation review — 2026-09-09

The implementation matches the approved scope. Public SQL functions no longer
select or return `viewer_accounts.id`; the API domain and SQL adapter cannot
accidentally remap it. The hostile contract check makes reintroducing it fail.
The dashboard function remains viewer-scoped and now has deterministic,
bounded ordering. The independent SQL suite remains per-database isolated and
is called by the root verifier rather than being merged unsafely into a shared
fixture database. `git diff --check`, focused tests, both SQL suites, and the
complete root verifier passed. External gates remain open.
