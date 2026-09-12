# L18 — Memberships

**Status:** `TODO — not started`
**Level:** L3 (native platform normalisation) / v2 for BharatStudio-native recurring
**Owner:** [OWNER — API/payments, unassigned]
**Depends on:** L15 (connector membership events), L14 (member state on the supporter relation)
**Blocks:** none recorded
**Test record:** [`../tests/TC-L18-memberships.md`](../tests/TC-L18-memberships.md)

## Authority and evidence

Master plan Part 6, "L18 — Memberships" (lines ~980–1018); Part 7 §7.10 (all rows TODO; BharatStudio-native recurring explicitly v2, gated on recurring-mandate pricing).

## Objective

Normalise native platform memberships (YouTube, Twitch, Kick) first; only then consider BharatStudio-native recurring support, and only once recurring-payment economics are confirmed.

## Tasks

1. `external_memberships`, `membership_periods`, `membership_renewal_events`.
2. Ingest membership events from each L15 connector (YouTube: member identity, level, total duration, duration at level; Twitch: tier, new/resub/gift, cumulative months where provided; Kick: new/renewal/gift, renewal duration, expiry where available — reconcile conservatively).
3. Surface member state on the supporter relation (L14's `creator_supporter_relations`).
4. Member badges (L14).
5. *(v2, out of this task's build scope)* BharatStudio-native recurring: mandate creation, state machine per Part 4 §4.8 ("Membership (TODO — L18). Store periods and renewal events, never a single current boolean."), cancellation, receipts, entitlement grant.

## Exact implementation boundary

In scope now: items 1–4, for whichever connectors are live per L15's phasing (YouTube in v1; Twitch/Kick as Phase 2 connectors land).

Out of scope now: BharatStudio-native recurring membership (task 5). This is v2 and explicitly gated — it must not be built, priced, or marketed as available until the recurring-rate pricing question below is resolved with dated primary evidence.

## Non-negotiable implementation rules

- Membership state is stored as periods and renewal events, never as a single current boolean.
- Money for BharatStudio-native recurring support (when eventually built) still flows viewer → creator's connected recurring-payment provider → creator. BharatStudio never holds recurring support money; it only consumes the provider webhook to grant entitlement.
- BharatStudio-native recurring membership requires viewer login (cancellation, receipts, plan management, recovery, cross-device entitlement all need it) — it is not offered anonymously.
- **Do not assume standard UPI 0% pricing applies to UPI AutoPay / recurring mandates.** This is a payment/pricing conclusion and, per `governance/AGENTS.md`, requires dated primary evidence (e.g., a provider's published UPI Subscription pricing) before any recurring-membership price is set or shipped. This task records the requirement; it does not resolve the rate.

## Definition gate

Per `governance/AGENTS.md`, stop after definition pending explicit approval. Owner unassigned: [OWNER]. **Open decision — not decided here:** the confirmed recurring-payment rate (e.g., Paytm's separately published UPI Subscription pricing) for any BharatStudio-native recurring tier. No recurring-membership price may be approved from memory; it requires dated primary provider evidence or written provider confirmation before L18's v2 phase begins.

## Acceptance criteria

- Membership events from each live connector (per L15 phasing) normalise into `external_memberships` / `membership_periods` / `membership_renewal_events` without loss of level/duration/cumulative-months data reported by the source platform.
- Member state visible on a creator's supporter relation reflects only that creator's channel — consistent with L14's cross-creator privacy rule — proven by test.
- Member badges (L14) update from confirmed membership renewal events, not from an unconfirmed platform signal.
- No BharatStudio-native recurring mandate, price, or "Join Support Club" UI element ships as part of this task's v1 scope; a scan/test confirms no recurring-payment code path exists until v2 is separately approved.

## Evidence required for closure

Inline prose citation: exact migration filenames for the three new tables; exact connector-ingestion file paths per platform; test-suite pass count for period/renewal normalisation and cross-creator exclusion. No artifact/screenshot directory.

## Rollback

All three tables are new and additive, populated only by connector ingestion; disabling ingestion for a connector does not affect payment/alert history. No BharatStudio-native recurring mandate exists in v1 scope, so there is no recurring-money rollback surface to reason about yet. No production migration without separate explicit approval.

## Implementation slice — 2026-09-07 reconciliation

Verified against `bharatstudio-alerts` as read on 2026-09-07: a repo-wide search for `external_memberships`, `membership_periods`, `membership_renewal_events` in `packages/db/migrations`, `apps/` and `services/` returns nothing. `creator_supporter_relations.member_state` exists (from L14, migration 0084) as a column, but nothing writes to it from a membership event — no connector ingestion path for membership normalisation exists. Status stands as TODO — not started; no progress is recorded against this task.
