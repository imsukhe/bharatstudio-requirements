# TC-L18 — Memberships acceptance

**Status:** `TODO — not started, no evidence exists yet (verified 2026-09-07 against bharatstudio-alerts: no membership tables or connector-ingestion code exist)`
**Task:** [`../tasks/L18-memberships.md`](../tasks/L18-memberships.md)
**Authority:** `bharatstudio-alerts/docs/BharatStudio-MASTER-PLAN.md` Part 6 (L18), Part 4 §4.8, Part 7 §7.10
**Repository:** `/Users/sukhdevsingh/Workspace/Bharat Studio/bharatstudio-alerts`
**Data:** Synthetic connector membership-event fixtures only (YouTube member events per L15 phasing). No real platform membership data.

## Preconditions

1. L15 connector(s) live (or stubbed) to supply membership events for this suite.
2. L14's `creator_supporter_relations` available or stubbed for member-state surfacing.
3. Disposable PostgreSQL test harness available for `external_memberships`, `membership_periods`, `membership_renewal_events`.

## Acceptance cases

| ID | Setup and action | Expected result | Failure/retry and evidence |
|---|---|---|---|
| L18-01 | Ingest a YouTube member-milestone event reporting level and total duration | `external_memberships`/`membership_periods` normalise level and duration without loss | Not run — TODO |
| L18-02 | Ingest a renewal event for an existing member | A new `membership_renewal_events` row is created; prior periods are not overwritten (stored as periods, never a single current boolean) | Not run — TODO |
| L18-03 | Query member state on the supporter relation for channel A while the viewer is also a member on channel B | Response reflects only channel A's member state | Not run — TODO |
| L18-04 | Award a member badge from a confirmed renewal event vs. an unconfirmed platform signal | Badge updates only from the confirmed renewal event | Not run — TODO |
| L18-05 | Scan the codebase/config for any BharatStudio-native recurring-mandate price or "Join Support Club" UI element | None exists in v1 scope; scan/test confirms absence | Not run — TODO |

## Closure rules

Closes only when every row has a real pass/fail result with inline evidence (migration filenames for the three tables, connector-ingestion file paths, test-suite pass counts) replacing "Not run — TODO." No artifact/screenshot directory exists or may be created. This record does not close L18's v2 (BharatStudio-native recurring) scope — that remains explicitly out of this test suite until a confirmed recurring rate is on file per the task's Definition gate.

## Cleanup and rollback

All fixtures run against the disposable PostgreSQL harness, torn down after the run. New tables are additive; no production database or real platform membership data is touched by this suite.
