# L14 — Viewer identity and supporter history

**Status:** `Local receipt, claim-boundary, badge, and opt-in-profile mechanisms reconciled through migration 0107; actual provider-verified claiming, DPDP legal disposition, independent review, and deployment evidence remain open`
**Level:** L3
**Owner:** [OWNER — API / database / privacy-legal, unassigned]
**Depends on:** L01 (contracts/baseline); L15 for Level 2 identity and for Level 3 YouTube linking (YouTube is in v1 per L15's 2026-09-02 decision; Twitch/Kick linking is Phase 2)
**Blocks:** L16 (leaderboards need supporter identity), L18 (member state on the supporter relation)
**Test record:** [`../tests/TC-L14-viewer-identity-and-supporter-history.md`](../tests/TC-L14-viewer-identity-and-supporter-history.md)

## Authority and evidence

Master plan `docs/BharatStudio-MASTER-PLAN.md` Part 6, "L14 — Viewer identity and supporter history" (lines ~750–800); Part 7 §7.9 (feature register, all rows TODO, all in v1 per the 2026-09-02 decision); Part 8 in full ("GUEST AND VIEWER ACCOUNTS" — the three-level model, the 2026-09-02 decision to ship all three levels in v1, and the binding privacy rules). Verified against all 79 migrations as of that plan: no viewer identity table exists today; the only viewer data is `donor_display_name`/`donor_message` free text on the payment row.

## Objective

Give a viewer optional identity so their support history survives across devices and platforms, without ever making login a condition of tipping. Ship all three identity strengths (anonymous browser-scoped, platform-scoped, BharatStudio account) in v1, per Part 8's 2026-09-02 decision.

## Tasks

1. `viewer_identities` table, discriminator: anonymous / platform / account.
2. `viewer_platform_identities` — unique `(provider, provider_user_id)`, linked to a viewer identity.
3. `anonymous_browser_identities` — opaque cookie token, no PII, expiring.
4. `creator_supporter_relations` — `(channel_id, viewer_identity_id)` with first support, last support, lifetime amount **to this creator only**, tip count, challenge count, current member state.
5. Add `viewer_identity_id` to `alert_events` and `payments`, nullable, backfilled null.
6. Receipt entity plus a viewer-facing receipt page reachable from a payment without login.
7. Optional viewer account: signup, login, session, password reset, DPDP-compliant deletion.
8. Platform account linking via OAuth, plus historical claiming: linking YouTube `UC123` attaches that platform identity's existing history to the account, idempotently.
9. Streaks: consecutive-stream support counted per platform identity.
10. Public badges, opt-in and non-financial (Supporter since 2026, N-month member, Challenge Champion, N Challenges Completed, Stream Streak ×N, Founding Supporter, Top 10 Supporter).
11. Opt-in searchable viewer profile.

## Exact implementation boundary

In scope: the three tables/entities above, receipt page, viewer auth surface (signup/login/session/reset/delete), OAuth linking for YouTube only at launch (Twitch/Kick linking arrives per-connector as L15 Phase 2 lands), historical claiming, streaks, badges, opt-in profile/search.

Out of scope for this task: Twitch/Kick platform linking (blocked on those connectors, Phase 2); any change to payment capture, refund, or webhook logic (owned by L04/L19); any creator-facing UI beyond the existing per-channel supporter view already described in the privacy rules below.

## Non-negotiable implementation rules

- Tipping works end to end with no viewer login — unchanged from today, always.
- A creator sees a viewer's relationship with **their own channel only**: first/last support, lifetime support to this creator, tip count, challenge count, current member state. A creator must **never** see cross-creator spend.
- A viewer sees their own lifetime support across all creators, receipts, refunds, challenges, memberships, streaks.
- Public profiles are opt-in, default-off. Exact lifetime spend is private by default and never published.
- Never claim history from a typed display name. Only from an OAuth-verified platform identity.
- Account deletion removes profile and linkage but preserves the immutable payment/audit record (per governance's append-only rule for financial/audit evidence).

## Definition gate

This is L3 work: per `governance/AGENTS.md`, implementation must stop after definition and wait for explicit approval covering scope, acceptance criteria, affected files, data impact, test plan and rollback.

**Open decision — not decided here.** DPDP-compliant viewer account deletion and the viewer-data retention/erasure design are privacy/legal conclusions. Per `governance/AGENTS.md` ("privacy... conclusions require dated primary evidence or written professional/provider advice — do not approve them from memory"), this task records the requirement and defers the specific deletion/retention mechanics to counsel review before implementation; no legal conclusion is asserted by this file. Master plan Part 8 flags this as widening L08 (legal review of viewer data handling and deletion) — that review is a precondition of closing this task, not an output of it.

**Open decision — owner unassigned.** No owner is named for L14 in the master plan; record as [OWNER] pending assignment.

## Acceptance criteria

- Tipping works end to end with no viewer login, unchanged from today.
- A `!tip` from a known platform user attaches to a Level-2 identity with no signup.
- Linking YouTube to a new BharatStudio account attaches prior `UC123` history exactly once and is idempotent on repeat (test both first-claim and repeat-claim).
- A creator API response containing supporter data is proven by test to exclude any other channel's amounts.
- Deleting a viewer account removes profile and linkage but preserves the immutable payment/audit record.
- A contested-claim case (two accounts attempting to claim the same platform identity) is handled deterministically and covered by test.

## Evidence required for closure

Inline prose citation only — no artifact/screenshot directory exists in this repository and none may be created. Closure requires: exact migration filenames for the new tables/columns; exact file paths for the receipt page, auth routes and linking flow; the disposable-database or CI test-suite pass count covering the acceptance criteria above (idempotent claim, contested claim, cross-channel exclusion, deletion-preserves-audit); and the L08 legal review disposition for DPDP deletion, cited by date and reviewer.

## Rollback

New tables and nullable added columns only; no existing migration is rewritten. `viewer_identity_id` on `alert_events`/`payments` is nullable and backfilled null, so it does not require a data migration on existing rows and can be dropped without loss to payment/alert history. Viewer auth surface can be disabled independently of Alerts tipping (the boundary rule above makes this testable). No production database is migrated under this task without separate explicit approval per `governance/AGENTS.md`.

## Superseded historical reconciliation — 2026-09-07

This was a point-in-time reconciliation against `bharatstudio-alerts` as read
on 2026-09-07. It is retained for traceability but is superseded where noted by
the 2026-09-08 completion reconciliation below; it is not current delivery
status, staging/production evidence, or a DPDP conclusion.

**Built and locally test-proven:**
- `viewer_identities`, `viewer_accounts`, `creator_supporter_relations` and `merged_into_account_id` (for a future claim) in `packages/db/migrations/0084_v1_l14_viewer_identity.sql`. The discriminated-identity design (anonymous/platform/account under one `viewer_identities` row) is documented in that file's header; `viewer_accounts` is a deliberately separate auth surface from `app_users`, not a role on it.
- `viewer_sessions`, DPDP-style deletion mechanics with an explicit erased-vs-retained split (`viewer_deletion_requests`), and `profile_visibility` defaulting to `'private'` in `packages/db/migrations/0085_v1_l14_viewer_sessions_and_deletion.sql`.
- Password reset in `packages/db/migrations/0088_v1_l14_viewer_password_reset.sql`: 30-minute single-use SHA-256-fingerprinted tokens, all sessions revoked on use, enumeration-safe silent no-op on unknown email.
- A real security defect and its fix, both in the shipped history: 0088's `enqueue_viewer_password_reset_email` was left executable by `PUBLIC` (only `request_viewer_password_reset`/`consume_viewer_password_reset_token` were revoke-scoped). It was caught by this repo's own standing invariant test (`packages/db/tests/l02_security_remediations.sql:63`) and fixed in `packages/db/migrations/0092_v1_l14_password_reset_execute_boundary.sql`, which revokes execute from `PUBLIC` without rewriting 0088.
- Cross-creator isolation — "a creator must never see cross-creator spend" — is proven twice: `packages/db/tests/l14_viewer_identity.sql:109` asserts a creator's `get_channel_supporter_history` call returns exactly their own channel's row and zero rows for a channel they do not own; `packages/db/tests/l16_security_boundary.sql` repeats the same assertion running as the actual `bsa_app` application role (not the postgres superuser), plus proves `bsa_app` has no direct table grant on `viewer_accounts`.
- API routes at `apps/api/src/routes/viewer.ts` (222 lines) and web surfaces at `apps/web/app/viewer/{signup,login,sessions,forgot-password,reset-password,delete-account,dashboard}` implement signup, login, session list/revoke, password reset request/consume and account deletion.

**Not built — do not record as done:** `apps/api/src/domain/viewer-store.ts` states its own scope boundary in-code ("Platform-account OAuth linking/historical claiming, badges and streaks are out of this batch's scope"). Verified absent from the codebase: a receipt entity or viewer-facing receipt page (no `receipt` route/component exists), YouTube OAuth linking and historical claiming (task item 8, and the idempotent/contested-claim acceptance criteria), streaks, public badges, and opt-in searchable profile UI (the `profile_visibility`/`profile_slug` columns exist in 0085, but no search surface consumes them). L14's acceptance criteria for idempotent-claim, contested-claim and streak/badge behavior are therefore unmet, not merely untested.

**Open, not decided here:** the L08 legal-review disposition for DPDP-compliant deletion remains unfiled — no dated counsel review was found in this repository. This task cannot close on the deletion-mechanism acceptance criterion until that review exists.

## Local completion reconciliation — 2026-09-08

The preceding reconciliation became stale after
`packages/db/migrations/0107_v1_l14_receipts_claims_badges_profiles.sql`
landed. This addendum records the code and the security correction found by
the 2026-09-08 audit; it does not convert an external provider or legal gate
into a local pass.

**Implemented and locally verified:**

- Opaque, no-account receipts: `payment_receipts` stores only a SHA-256 token
  fingerprint; `apps/api/src/db/viewer-profile-store.ts`,
  `apps/api/src/routes/viewer.ts`, and `apps/web/app/r/[token]/page.tsx`
  mint/resolve/render the receipt. It is one token per captured payment and
  accounts for processed refunds live.
- First-claim-wins, idempotent, audit-recorded platform claims are implemented
  in `0107`; `packages/db/tests/l14-receipts-claims-badges-profiles.sql`
  proves first claim, repeat claim, contested claim, and no re-pointing.
  The API no longer trusts a browser `providerUserId`: it uses the optional
  `ViewerPlatformIdentityVerifier` boundary in
  `apps/api/src/domain/viewer-platform-identity-verifier.ts`. Until an L15
  adapter supplies a server-verified identity for the authenticated viewer,
  `POST /v1/viewer/platform-claims` returns `503` rather than allowing a
  claim. This is a deliberate safety gate, not a completed YouTube OAuth
  integration.
- `0107` computes refund-safe supporter/streak/founding/top-ten badges live;
  public profile SQL is structurally default-private and selects no monetary
  field. The authenticated control is at `/viewer/profile`; the public
  minimal profile route is `/viewer/profiles/[slug]`. Neither displays support
  amounts, payment history, or receipts.

**Reproducible redacted local evidence:**

- `cd apps/api && npx tsc -p tsconfig.json --noEmit && npx tsx --test
  test/l14-viewer-profile-routes.test.ts` — **7/7** pass, including no-auth,
  no-verifier fail-closed, browser identity ignored in favour of trusted
  verifier, opaque receipt, public-profile, and own-badge cases.
- `cd apps/web && npx tsc --noEmit && npx tsx --test
  --experimental-test-module-mocks --import ./app/test-support/dom-env.ts
  app/viewer/profile/page.test.tsx && npm run build` — **2/2** new focused
  tests, typecheck, and production build pass. The test proves private is the
  default and the UI sends only visibility plus a normalised slug.
- `sh packages/db/tests/run-sql-suite.sh` — fresh PostgreSQL applies **110**
  migrations and reports **44/44** isolated proofs, including
  `l14-receipts-claims-badges-profiles` and the existing cross-creator
  boundary proof.

**Still open and not claimed as done:** an L15 provider adapter with actual
OAuth/provider evidence; membership and challenge badge variants whose source
truth is L18/L17; DPDP/L08 counsel disposition for deletion; deployed
browser/OBS/staging evidence; independent security review. Rollback is to
omit the optional verifier and hide the additive profile routes; tipping,
payments, and existing viewer auth remain unaffected.

## Regression recheck — 2026-09-09

After the frozen dependency install, the complete local recheck passed API
**398/398**, web **289/289** with typecheck and production build, and
disposable SQL **44/44** after 110 migrations. This refreshes evidence only;
the OAuth, legal, deployment, and independent-review gates remain open.

## Batch 10 addendum — 2026-09-13

Migration `0120_v1_l02b_reputation_signals_and_score.sql` (new supporter-reputation work, tracked at `L25-supporter-reputation.md`) extends this task's own migration-0085 erasure record with a further retained-on-deletion class (`reputation_signal_events`, and the score/verdict derived live from it), explicitly flagged `legalDispositionOpen: true`. This does not change any status or evidence already recorded above for viewer identity itself; it is cross-referenced here because it deepens the same open DPDP/deletion question this task already deferred to counsel. See `L02-security-rls-and-archive-proof.md` batch 10 section and `L25-supporter-reputation.md` for detail. No legal conclusion is asserted.

## QA reachability correction — 2026-09-14

The receipt API/page was implemented but the confirmed-tip UI never invoked
`POST /v1/public/receipts`; no ordinary anonymous payer could obtain its opaque
link. This L3 correction wires both existing direct-tip and opaque TipIntent
confirmation UIs to mint the one-time receipt after the server confirms a payment. It sends the
already-known opaque intent id, validates only the returned opaque token, and
links to `/r/<token>` without logging, storing server-side, or exposing payment
details. Receipt minting is advisory: an outage or an already-minted response
must never turn a confirmed payment into an error or retry it. No schema,
payment mutation, provider, pricing, retention, or legal posture changes.

Acceptance: either confirmed payment journey requests a receipt once, displays only a
validated opaque receipt link on success, and keeps the payment-confirmed
state on any receipt failure. Tests must prove the browser contract and the
full local verifier must remain green. Rollback is hiding the UI handoff; the
additive existing receipt data remains untouched.

**Local evidence — 2026-09-14:** `apps/web/app/tips/receipt-client.test.ts`
proves the mint request contains only `intentId`, uses credentialed fetch,
accepts the exact opaque-token format, and treats unavailable/malformed
responses as no receipt rather than a payment error. Both direct-tip and
TipIntent confirmation components invoke that shared helper only from their
`paid` status path. `pnpm verify:local` exited 0 after 125 migrations, 52
isolated SQL proofs, 501 API tests, 327 web tests, Go race/vet checks,
integration/load/fault checks, and the three declared image builds. This is
synthetic local evidence only; real browser/cookie, staging, provider, legal,
and independent-review gates remain open.
