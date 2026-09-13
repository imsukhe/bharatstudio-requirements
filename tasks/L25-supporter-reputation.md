# L25 — Supporter reputation

**Status:** `Built and locally test-green — apps/api 465/465, SQL suite 49/49 across 120 migrations, all verified 2026-09-13; not proven in a deployed environment; a retention-vs-DPDP decision was made by default and is recorded as open, not resolved`
**Level:** L3
**Owner:** [OWNER — API / database / privacy-legal, unassigned]
**Depends on:** L02 (RLS/retention discipline), L14 (`viewer_identities`, `creator_supporter_relations`), L15 (YouTube Super Chat source), L19 (`bharatstudio_tip` payments/refunds ledger)
**Blocks:** none recorded
**Test record:** [`../tests/TC-L25-supporter-reputation.md`](../tests/TC-L25-supporter-reputation.md)

## Authority and evidence

No existing master-plan section named this work; the only prior "abuse" control anywhere in `bharatstudio-alerts` was a Turnstile CAPTCHA on the tip page, which is bot prevention at the moment of payment, not behavioural reputation. This task is created fresh per this reconciliation's instruction, to give reputation a proper task/test record rather than leaving it undocumented against a migration number alone. Built in `bharatstudio-alerts` commit `377227a` (`feat(0120): supporter reputation, per-source by necessity, plus wiring`), migration `0120_v1_l02b_reputation_signals_and_score.sql`.

## Objective

Give creators a behavioural-abuse verdict on a supporter (refund/chargeback/velocity/content-moderation history) without exposing per-signal detail, without storing a score anywhere, and without leaking one creator's supporter history to another.

## What shipped, verified 2026-09-13 by reading the code directly (not the commit message)

- `reputation_signal_events` table, per-source signal types constrained by design, not convention:
  - `bharatstudio_tip` source: `chargeback`, `velocity_spike`, `content_moderation_strike` may be stored; `refund` is never stored as a row — it is derived live from `public.payments`/`public.refunds` on every read, the same discipline migration 0102 already used for support-goal progress, so a reversed refund needs no un-scoring step.
  - `youtube_superchat` source: `velocity_spike`, `content_moderation_strike` only. `refund` and `chargeback` are structurally forbidden for this source — confirmed: `app_private.record_reputation_signal` raises `errcode 22023` on an attempted `refund` insert for any source, and a table CHECK (`signal_type <> 'chargeback' or source = 'bharatstudio_tip'`) independently rejects a raw-insert chargeback outside `bharatstudio_tip`. Both the function-level refusal and the raw-insert CHECK violation are asserted by test, not just documented.
  - This is not a policy choice; it is a structural fact recorded in the migration header and verified against Google's own channel-report documentation: no webhook reaches BharatStudio for a Super Chat refund, and YouTube's aggregate revenue reports carry no payer dimension, so a Super Chat refund signal cannot be built at any granularity, for anyone.
- No score is stored anywhere. Verified: no `reputation_scores` table and no score/verdict column exists in migration 0120 (confirmed by reading the file) and by the test suite's own `information_schema` query asserting zero columns matching `%score%`. `app_private.reputation_score(viewer_identity_id)` is a stable function, recomputed live as a weighted sum over a 180-day window from `reputation_signal_events` plus the live `payments`/`refunds` join for the derived refund signal. Proven live by test: flipping a refund to `reversed` and back changes the score with zero reputation-table writes.
- Privacy boundary: the system uses cross-creator signal (a viewer who refunds everywhere is the point of the feature); the creator sees only a verdict. The creator-facing route/function returns exactly three keys with no signal, source or channel column in the response shape to leak — confirmed by reading `apps/api/src/routes/reputation.ts`, and the route's `additionalProperties: false` is proven by test to reject a fake store that tries to smuggle extra fields through. Showing "refunded on 5 other channels" would leak another creator's supporter list by inference; this is why the verdict-only boundary exists.
- Thresholds and weights are a first cut with no abuse data to calibrate against — recorded as a known limitation, not a defect.
- Wiring: `apps/api/src/app.ts`/`index.ts` construct and pass the reputation store alongside capability-snapshot and creator-pack stores added in the same batch (held back from earlier per-range commits because nearly every lane touched these files).

## Retention decision — recorded prominently, not resolved

Reputation signals and the live-derived score SURVIVE viewer account deletion, in the same retention class as `creator_supporter_relations`. This is a decision made by default, confirmed in `app_private.request_viewer_account_deletion` (extended by this migration), which lists `reputation_signal_events` among the retained-on-deletion classes and explicitly carries `legalDispositionOpen: true` in the erasure record. The bind is real: retaining the data keeps abuse-prevention deletion-proof; dropping it on deletion would let a refund-abusing viewer launder their reputation by delete-and-recreate. **No legal or DPDP conclusion is written here or anywhere in this record**, per `governance/AGENTS.md:28`. This sits alongside the DPDP question `L14-viewer-identity-and-supporter-history.md` already deferred to counsel from migration 0085 and should be resolved together with it, not separately.

## Not built / explicitly out of scope

- No platform-staff review UI for reputation verdicts (none is required by what shipped; the creator-facing verdict is the only consumer).
- No calibration against real abuse data — thresholds/weights are first-cut.
- No legal/DPDP disposition of the retention decision above.

## Evidence required for closure

Inline prose citation only, per this repository's rule: migration `0120_v1_l02b_reputation_signals_and_score.sql`; source paths `apps/api/src/domain/reputation-store.ts`, `apps/api/src/db/reputation-sql-store.ts`, `apps/api/src/routes/reputation.ts`; test paths `apps/api/test/reputation-routes.test.ts` (146 lines), `packages/db/tests/l02b-reputation-signals.sql` (257 lines). No artifact/screenshot directory; this repository stores no artifacts.

## Rollback

Additive migration; no existing `payments`, `refunds`, `creator_supporter_relations` or viewer-deletion row is rewritten. Disabling the reputation routes/store leaves the underlying payment/refund/viewer-identity data and existing deletion mechanics unaffected. `reputation_signal_events` rows already retained through a deletion event are not themselves reversed by a rollback of this feature — that is the retention decision above, not a rollback concern.
