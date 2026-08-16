# L03-41/42/43 onboarding wizard, dashboard IA split, and billing-shape fix — independent review

**Date:** 2026-08-16
**Reviewer:** Independent fresh-context agent (general-purpose subagent, no exposure to the author's own conclusions — instructed to run all verification itself rather than trust claimed results)
**Author:** Claude (Sonnet 5), same session as the work under review
**Decision state:** `Conditionally complete` — every finding below is fixed and re-verified; deployed, staging, provider-sandbox, real-browser/OBS-accessibility-matrix, and a *second* independent review remain open, exactly as the rest of L03 already records for every other item
**Task:** [`tasks/L03-alerts-web-and-creator-api.md`](../tasks/L03-alerts-web-and-creator-api.md), "L03-41/42/43" entries and the terms-gate amendment below them
**Acceptance:** [`tests/TC-L03-alerts-web-and-creator-api.md`](../tests/TC-L03-alerts-web-and-creator-api.md), cases L03-41 through L03-43

## Scope reviewed

The full uncommitted diff for: the resumable onboarding wizard (`/accept-terms` as step 1, `/onboarding/step-1` create-channel as step 2, `/onboarding/step-2` connect-payout as step 3), the dashboard split from one monolithic `DashboardClient.tsx` into Overview + 5 independently-routed pages (`/dashboard/{alerts,customise,mod,billing,referrals}`), the new shared `AppShell` sidebar/topbar chrome, the auth-aware `TopNav`, and migration `0078` correcting `app_private.get_billing_view`'s no-subscription default shape.

## Method

Per this repository's own rule ("use a fresh independent review context ... do not provide it with the author's conclusions"), the reviewing agent was given only a factual description of what changed and where, explicitly told not to trust any claimed test-pass counts, and instructed to run every verification command itself and quote real output. It was pointed at `git diff`/`git status` directly rather than a prepared summary of "what's correct about this."

## Findings and disposition

1. **Major — terms-acceptance gate not carried into the 5 new dashboard pages or either onboarding step page.** Only the old single-page dashboard had ever checked `getTermsStatus()`; splitting it into 6 pages carried the check into just one of them (Overview), and the pre-existing `/companion`/`/payments`/`/settings`/`/overlay/setup` pages had never had it either. Not a security hole — every mutation route already fails closed server-side via `requireAuthAndTerms` — but exactly the "opaque 403 instead of the gate" failure mode `/accept-terms`'s own header comment claims to prevent, and reachable by ordinary sidebar navigation, not a contrived edge case (a creator whose channel predates a newly-published terms/privacy document version).
   **Fixed:** centralized in `AppShell.tsx` (covers all 9 shell-wrapped pages in one place instead of nine separate checks) plus direct checks added to `/onboarding` (bare redirector), `/onboarding/step-1`, and `/onboarding/step-2` (not AppShell-wrapped). **Re-verified live**: deleted a real user's `user_terms_acceptances` rows, confirmed direct navigation to `/dashboard/billing` *and* to the pre-existing `/companion` both now redirect to `/accept-terms` instead of rendering; restored the rows afterward.
2. **Minor — inconsistent error-state UX.** The 5 new pages showed a bare error string on fetch failure with no path back to `/login`, unlike Overview's "Return to sign in →" link.
   **Fixed:** added the same link to all 5.
3. **Minor — dropped default value.** The queue-creation form's `'Main alerts'` prefill was lost in the extraction to `/dashboard/alerts`, defaulting to an empty field instead (placeholder text still covered it, so not a functional break, just a lost convenience default).
   **Fixed:** restored.
4. **Nit — `run-l03-application-behavior.sh` mode-only diff.** Confirmed pure `chmod +x` (100644→100755, an artifact of the review agent's own verification run needing it executable), no content change. No action needed.
5. **Everything else the reviewer checked** — extraction faithfulness against the pre-split file, server-side authorization for the client-side role gates (traced `moderateAlert`/`updateChannelConfig`/`registerPaymentAccount` into real RLS policies and a `has_channel_role` check, confirmed not merely assumed), the onboarding resumability chain, migration 0078's correctness against the actual CHECK constraint and its regression test's non-vacuousness, security (no injection/XSS/secret-leakage points), and accessibility (labelling, no dead-end disabled states) — **no issues found**, independently re-run rather than taken on the author's word:
   - `apps/web` `tsc --noEmit`: clean.
   - `apps/web` test suite: 55/55.
   - `apps/api` test suite: 143/143.
   - `packages/db/tests/run-l03-application-behavior.sh` against a disposable fresh Docker Postgres 16: exit 0, `L03_APPLICATION_BEHAVIOR=PASS` genuinely present, no `fail`/`error`/`exception` anywhere in the full log (including the bundled Go service suites and overlay-wakeup integration tests).

## Post-review changes not covered by the above (author, after the review)

- Added explanatory copy to the "Connect payout" step's Environment (Test/Live) field after the owner asked why it wasn't auto-detected from the app's own deployment environment — clarified it's the Razorpay account's own test/live mode (a business distinction the creator alone knows, tied to which Razorpay credential they're pasting in), not related to whether this app is in development or production.
- Fixed the onboarding progress indicator sharing a flex row with the brand logo, which kept it centered only in the space left over after the logo rather than on the full page — moved to its own row.
- `/` changed from a static marketing-style homepage (built earlier in this same redesign) to a pure auth redirect (signed in → resolve via `/onboarding`'s existing terms→channel→dashboard chain; signed out → `/login`), on explicit owner direction once that chain existed to redirect into. The separate `bharatstudio-marketing` static site's own "Get started" CTA already links straight to `/login`, not `/`, so this has no cross-repo effect.

Re-verified after all of the above: `apps/web` `tsc --noEmit` clean, test suite 55/55, `pnpm build` 18/18 routes, `apps/api` test suite 143/143. Live-verified both directions of the new `/` redirect (signed-in lands on dashboard, signed-out lands on login) with real sessions.

## Further amendments (author, after the review record above was written)

- **Terms/privacy presentation redesigned**: full document text was rendered
  inline by default (a two-column layout with both documents' complete
  sections always visible above the checkboxes) — owner-directed change to
  compact checkbox rows ("I have read and agree to the *Terms of Service
  (v1.0)*") where the document title is a button opening a modal with the
  full text, closable via an explicit button, Escape, or backdrop click.
  No content was cut — every section is still there, just not rendered by
  default. Verified live: modal opens with full Terms of Service text and
  closes correctly.
- **Owner-reported bug, traced to a stale dev server, not a code defect**:
  visiting `/` with lapsed terms appeared to reach the dashboard instead of
  `/accept-terms`. `/onboarding/page.tsx`'s terms check (added earlier in
  this same review-remediation pass) was already correct in source; the
  running dev server just hadn't been restarted since a later, unrelated
  edit (Turbopack in this environment does not reliably hot-reload — a
  known issue recorded earlier in this task file's history). Restarted and
  re-reproduced the exact scenario (deleted a real user's
  `user_terms_acceptances` rows, visited `/`) — correctly redirects to
  `/accept-terms`. Restored the rows afterward.
- **Clarified, not changed**: the "Connect payout" step's Environment
  (Test/Live) field is the Razorpay account's own test/live mode — a
  business fact only the creator knows (which Razorpay credential they're
  pasting in), unrelated to whether this app itself is running in
  development or production. Added explanatory copy rather than attempting
  to auto-derive it from `NODE_ENV`, which would be semantically wrong.

Re-verified after all of the above: `apps/web` `tsc --noEmit` clean, test
suite 55/55, `pnpm build` 18/18 routes.

## What remains open

Same as the rest of L03: deployed/staging evidence, provider-sandbox checkout, real browser/OBS/accessibility matrix, and — since this review's own findings were fixed *after* the review that found them — a second pass specifically re-confirming those five fixes would be the natural next independent-review scope, though the live re-verification recorded above already covers the two behavioral ones (terms gate, `/` redirect) directly.
