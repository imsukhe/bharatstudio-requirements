# Decision and review — CTL-04 / CTL-05 / CTL-13 capability-admin control plane

**Date:** 2026-09-18  
**Owner:** Sukhdev Singh  
**Reviewer:** Self-review of current worktrees; no independent review has occurred.  
**Status:** `Approved for local implementation — Option B selected by owner 2026-09-18`

## Findings from the actual current source

1. Alerts has durable registry/change-management/emergency-kill primitives and API routes, but `emergency-kill` currently requires caller-supplied `affectedChannelCount` and `liveChannelCount` (`apps/api/src/routes/capability-kill-events.ts`). This does not satisfy §20.6's preview requirement and leaves an audit log with untrustworthy impact values.
2. `bharatstudio-admin` has no capability registry, impact-preview or emergency-kill page/client adapter. Existing entitlements UI is Layer 1 and must not be repurposed as Layer 2 controls.
3. ADM-07 has a durable database admin registry, but explicitly documents no MFA implementation, enrollment/recovery policy or approved identity-provider assurance model. The console itself states MFA is not enforced. §20.6 requires MFA for this panel.

## Owner decision

**Selected: Option B — application-managed passkeys.** BharatStudio stores public WebAuthn
credentials and requires user-verified passkey assertions for privileged console sessions. This
selection authorizes the local database/API/console implementation.

The selection does **not** invent production configuration. The RP ID and origin allowlist remain
unset by default, and absence is a fail-closed deployment state. The owner later approved and the
implementation now fixes the five-minute ceremony, fifteen-minute elevation and audited recovery
policy recorded below. Existing local development bootstrap remains development-only and is never
accepted in a deployed environment.

## Proposed implementation checklist after approval

- Read the current worktrees and relevant Next/Auth.js documentation before coding.
- Implement CTL-13's approved MFA gate before exposing CTL-04/05 mutation UI.
- Add a forward-only SQL preview with direct-privilege/RLS proof and an API endpoint/schema.
- Bind emergency kill to server-derived counts inside the state-changing transaction; remove browser-supplied count fields from contract, runtime and tests.
- Build the standalone admin route, accessibility/degraded states and audit/history flow.
- Run migration/role/contract/API/race/browser/build/rollback checks and a fresh hostile review.

## Approval boundary

The owner selected Option B and approved the defined local scope, acceptance, affected repositories,
data impact, test plan and rollback. CTL-04, CTL-05 and CTL-13 may now be implemented locally.
Production configuration, real-device/provider evidence and independent review remain open release
gates.

## Owner policy decision update — 2026-09-18

The owner approved the previously open local policy values: ceremony challenge lifetime is five
minutes; privileged-session elevation is fifteen minutes; and recovery is an audited, two-person
process with no recovery codes or self-service reset. A locked-out platform admin may request only
their own recovery. Two distinct, recently passkey-verified platform admins must approve before
completion: the designated platform owner and a non-owner platform admin. Requests expire after
24 hours. Completion must atomically revoke the target's active passkeys and sessions; the target
must authenticate again and enrol a new passkey. The recovery record is minimised to identifiers,
timestamps and append-only action state—no free-form recovery reason, recovery secret, provider
token or credential response is retained. The still-unapproved production RP ID and origin list
remain fail-closed deployment configuration gates.

## Implementation review update — 2026-09-18

Self-review inspected the actual Alerts and admin-console worktrees after local implementation.
The previously missing MFA boundary is now a session-bound, durable, fail-closed application-managed
passkey system. The review caught and corrected one migration portability defect before it landed in
the full SQL suite. Corrected focused database proof, API route tests, contract validation and both
application builds passed. This is neither independent review nor production/device evidence.

Final self-review found an initially omitted class of operational admin routes (DLQ, entitlement,
ingest-failure and creator-pack review) which had retained a role-only guard. They now compose the
same durable session MFA check; only `whoami` and the deliberate MFA bootstrap ceremony endpoints
remain role-only. The stale creator-pack test fixture was repaired and now also asserts a
role-authorised but MFA-unverified 428 denial. A final `pnpm verify:local` after the recovery
addition completed with 89 isolated SQL proofs, 158 OpenAPI paths/185 operation contracts,
web/measurement checks, Go race/vet checks and all three command-image builds; the separately-run
admin console typecheck, 4-test suite and production build pass.

This remains self-review, not independent review or production evidence. Open gates: configured
production RP ID/origin, real browser/device ceremony evidence, deployed migration/forward-rollback
rehearsal, external security review, and independent fresh review.

A final accessibility/copy pass also removed the stale console claim that MFA was not enforced and
made successful passkey enrollment a status announcement rather than an error alert. The narrow BFF
allowlist has a direct unit proof rejecting traversal and arbitrary admin/token-relay paths. Admin
console typecheck, test and production build were rerun after those corrections.

## CTL-05 blocker review — 2026-09-18

The required source inspection found no authoritative durable live-channel state in the Alerts
schema or runtime. The current Companion activation contract says `streamPaired` is always false
because Stream sends no liveness signal. It would be an unapproved material product decision to use
an overlay connection, a stream mission, event recency, or a browser value as “live.” CTL-05 is
therefore blocked only on an owner-recorded source/predicate/lease-and-staleness decision; its
aggregate preview and emergency-kill binding must not be implemented with fabricated counts.

## CTL-05 source decision update — 2026-09-18

The owner selected YouTube Live. Review of the actual implementation found that the YouTube Data
API adapter does have an active-broadcast query and the poller uses a non-empty `liveChatID` as its
live signal, but the repository boundary explicitly reserves that service for Phase 2 and the signal
is process-local. Reusing it would create a non-durable, restart-sensitive audit source and violate
the repository phase boundary. The correct v1 direction is a separately deployed durable liveness
projection, with provider failure/staleness represented as `unknown` and a fail-closed impact
preview. Freshness/cadence, OAuth scope/credential grant and deployment ownership are still not
recorded, so this review does not authorize runtime implementation of CTL-05 yet.

## Recovery implementation self-review — 2026-09-18

The fresh SQL review found and corrected a real PL/pgSQL control-flow defect: `RETURN QUERY` alone
does not stop a function, so the completed branch originally fell through to the first-approval
update. The corrected migration has explicit returns after both result branches. A fresh isolated
166-migration suite passed all 89 SQL proofs afterward. Review also verified that owner/staff
approvals have distinct unique kinds, self-approval is rejected under row lock, each approver has
recent durable MFA, completion revokes all non-revoked target sessions/passkeys in the same
transaction, and only minimised identifiers/timestamps/actions are retained. API/contract tests,
Admin typecheck/unit/build and `git diff --check` passed locally. This is self-review only; it is
not real browser/device, deployed rollback, independent or external-security evidence.

## CTL-04 implementation self-review — 2026-09-18

Inspected the final `bharatstudio-admin` worktree rather than relying on implementation intent.
The new `/admin/capabilities` route is behind the durable passkey-MFA admin layout. Its same-origin
BFF is narrow, typed and server-side: it projects registry/change/kill-history data without actor
UUIDs, exposes only an existing-capability proposal plus governed approval/rejection/revert writes,
and never becomes a general bearer-token relay. A crafted proposal for a new key is rejected by a
server-side existing-entry check; every mutation requires a console request marker; existing registry
PUT is never exposed. Browser code has no emergency-fire URL or impact count field, so the unsafe
legacy fire contract cannot be reached from the console.

Fresh review found and repaired five reproducible local issues: development bootstrap was unable to
reach its passkey-protected test surface without an upstream API; responsive capability actions were
not reliably reachable on emulated mobile; bootstrap error copy claimed MFA was absent; a direct BFF
proposal could have widened to a new capability; and new mutation routes lacked an explicit
same-origin marker. After repair, `pnpm typecheck`, 8 unit tests, 8 desktop/mobile browser tests,
`pnpm build`, contract validation and 26 focused Alerts capability-route tests passed; `git diff
--check` passed. This verifies all locally executable CTL-04 portions except CTL04.4. The emergency
card is intentionally disabled pending CTL-05 and is not represented as completed. This remains
self-review only—not provider, device, deployed, production or independent-security evidence.

## CTL-05 provider fact check — 2026-09-18

The existing `youtube.readonly` OAuth scope is sufficient for the read-only `liveBroadcasts.list`
operation; no broader permission is needed. However, Google rates that method at one quota unit per
call and its documented default daily project quota is 10,000 units. A continuous one-minute
observation schedule costs 1,440 units/day per connected channel; a five-minute schedule costs 288,
before current chat ingestion or other API calls. The liveness cadence, staleness lease, quota
allocation/admission cap and accountable deployment owner are therefore material operating
decisions, not defaults this review may invent. Official sources: [authorization](https://developers.google.com/youtube/v3/live/docs/liveBroadcasts/list), [quota costs](https://developers.google.com/youtube/v3/determine_quota_cost).
