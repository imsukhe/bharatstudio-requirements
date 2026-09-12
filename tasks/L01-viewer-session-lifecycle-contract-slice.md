# L01 — Viewer session lifecycle contract slice

**Status:** `Implemented locally — executable evidence recorded`
**Level:** L3
**Authority:** L01 versioned API contracts

## Scope

Publish the existing authenticated viewer lifecycle operations: logout, own
session list, own-session revocation, and account-deletion request. All use the
dedicated opaque viewer bearer scheme and never use the creator-session scheme.

## Privacy and security

- Session lists contain only the caller's session metadata and a current flag;
  no viewer account ID, token hash, or credential appears in the projection.
- Revocation returns 404 for a session outside the caller's scope.
- Logout returns no content after revoking the current viewer session.
- Deletion result is an explicit erased-versus-retained disclosure with the
  legal disposition marker; it contains no new credential or session.

## Change control

Contract audit found that `app_private.list_viewer_sessions` had no database
limit although the response contract is bounded. This slice therefore also
adds a forward migration that limits active-session listing to the newest 100
rows for the authenticated viewer, plus a 101-session SQL proof. No provider
interaction or deployment configuration changes.

Rollback is a controlled redefinition of that private function to its prior
unbounded behavior. It is not automatic: removing the bound would reintroduce
the response-amplification risk and invalidate the published contract.

## Acceptance

1. All four operations have typed responses, viewer auth, and exact statuses.
2. Session and deletion fixtures validate with injected identity/token fields
   rejected.
3. API/web/contract and full deterministic local verifier evidence remains
   green after the contract update.
4. A viewer with more than 100 active sessions receives only the newest 100;
   another viewer cannot influence the set.

## Local evidence — 2026-09-09

Migration `0112_v1_l01_viewer_session_list_bound.sql` defines the private
viewer-session query with newest-activity ordering plus `LIMIT 100`, retaining
the original current-viewer authorization predicate and explicit `bsa_app`
grant. `l14_viewer_identity.sql` now creates 101 active synthetic sessions,
proves exactly 100 results, proves the deliberately oldest row is absent, and
proves a second viewer reads none. The root disposable runner now includes that
L14 proof (19 SQL files total) rather than silently omitting it.

`pnpm verify:local` passed after the change: contracts 26 fixtures/53
paths/60 operations; deployment one positive/four hostile negatives; 19 SQL
proofs plus service/overlay integrations; L09 load/fault; API **402/402**;
web **289/289**; all Go race/vet suites; and API/payment/worker images.
This is local proof only and does not constitute migration deployment,
provider, staging, production, device, store, capacity, or rollback evidence.
