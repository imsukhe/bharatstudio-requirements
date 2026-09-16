# RT-03 correction — the quota release was not what its own comments claimed

**Date:** 2026-09-16
**Owner:** Sukhdev Singh
**Authority:** `FULL-PRODUCT-DEFINITION.md` §19.0 RT-03, §3.2, §10.2, §10.3, §11.11, §12.2
**Records:** `active/tasks/RT-03.md` (Correction, 2026-09-16) · `tests/TC-RT-03-checks-synthesis-release.md` (Correction and re-verification, 2026-09-16)
**Migration:** `packages/db/migrations/0134_v1_rt03_tts_reservation_ledger.sql`

## How this was found

Not by a check, and not by a failing test. By re-reading migration `0128`'s own
comments against the `TtsQuotaMeter` interface's own written contract. `0128`
stated both defects in prose and shipped anyway, delegating one of them to
"any future caller" and describing the other as "a safe no-op" on an assumption
that does not hold generally.

The general lesson is not about TTS. **A correctness property recorded in a
comment is not enforced.** Every §2 finding in this register has that shape; this
one had it inside a migration that was itself written to fix a §2-shaped defect.

## The two defects

| | Defect | Consequence |
|---|---|---|
| 1 | `release_tts_usage_reservation(uuid, integer)` had no idempotency. `greatest(...,0)` floors a negative counter and does nothing else. | A second release against a month holding **other** usage subtracts twice and credits the creator characters nobody reserved. |
| 2 | Release credited `date_trunc('month', current_timestamp)`, not the month the reservation was charged to. | A UTC month boundary between reserve and release (either side of one provider call) leaves the old month charged **and** credits the new month characters it never reserved. |

Both produce the same outcome — quota manufactured from nothing — and both
contradict the interface comment that already said release "must never
manufacture quota that was not reserved".

## Why the existing test passed

`packages/db/tests/rt03_tts_quota_reservation_release.sql` asserted defect 1's
absence explicitly, and passed. It released a month whose counter had already
reached `0`, which is the single arrangement where the floor hides the missing
property: `0 - 500` clamps to `0` and looks idempotent. Against a month holding
`300` characters of other usage, the same double release yields `0`, eating a
charge that was never released.

Defect 2 was never tested at all — the rollover case had no test, only the
comment asserting it was safe.

A green check blind to the case it was never told about. Third occurrence of
that pattern in this register (after `explain:check`'s standalone script and
RT-12's convention blindness), and the first inside a billing path.

## The fix, and what it deliberately gives up

Reservations become durable rows (`public.alert_tts_usage_reservations`), with a
composite foreign key to `alert_tts_usage_monthly (channel_id, billing_month)` so
a reservation can only ever name a monthly row that exists. `meter_tts_usage`
returns the reservation id as a fourth column; `release_tts_usage_reservation(uuid)`
consumes it exactly once, against the month recorded on the reservation.

**The `(uuid, integer)` signature is dropped, not deprecated.** Leaving it
callable would preserve exactly the defect the migration exists to close.
Removing the unsafe path is the enforcement; a comment telling future callers
not to use it is what failed the first time.

**Release is now all-or-nothing per reservation.** `0128` accepted an arbitrary
character count, making "release less than was reserved" expressible. No caller
ever used it, and it is not a §10.2 entry type. Removing it removes a class of
arithmetic error rather than testing around it.

**This supersedes `active/tasks/RT-03.md`'s design decision 2**, which recorded
that release should operate on the counter rather than a new table. That
reasoning was correct for a release keyed by character count and wrong for the
properties this correction needs: a counter cannot carry per-reservation state.
The new table is still **not** a §10.2 entry-type ledger — no `entry_type`
column, no grant/settle/refund/expiry vocabulary — and `alert_tts_usage_monthly`
remains the source of truth for the balance.

## Verification

`pnpm db:test:all` → `SQL SUITE: pass=61 fail=0` · `pnpm --filter
@bharatstudio/alerts-api test` → `tests 590  pass 590  fail 0` · `pnpm
db:test:l03` → `pass 2  fail 0` · `pnpm --filter @bharatstudio/alerts-api build`
→ clean · `pnpm contracts:validate` → 70 paths, 77 operation contracts ·
`pnpm explain:check` → `16/16 plans current`.

**Negative-tested, one defect at a time, migration restored byte-identical after
each run.** `released_at` guard disabled → `FAIL rt03_tts_quota_reservation_release`,
`pass=60 fail=1`. Release re-pointed at the current month → `FAIL
rt03_tts_quota_reservation_release`, `pass=60 fail=1`. Neither failed under the
previous version of that test. The contrast is the evidence; the green alone is
not.

## Found in passing, and fixed

Two further items, both recorded here because they were fixed in the same pass
rather than parked:

1. **§19.0 RT-03 carried a stale claim.** Its block ended "The current worker
   still violates it, because it runs enrichment before release with no failure
   classification, no retry policy and no ordering guarantee" — untrue since the
   RT-03 build landed, and contradicted by the register carrying RT-03 as `U`.
   Replaced with a dated built-and-verified block plus this correction.

2. **`tools/doc_consistency.py`'s `restated-count` check had a false positive its
   own comment denied.** The comment says the pattern ignores migration numbers;
   it excluded only `19xx`/`20xx`, so "migration `0134` makes reservations
   durable rows" tripped it. Narrowed by excluding the zero-padded `0\d{3}`
   shape only — a register row count can never carry a leading zero, so the
   check loses nothing. Negative-tested: an inserted "the register holds 783
   rows today" still errors, and the file was restored identical afterwards.

## What this evidence is not

Local only. Not production, provider, invoice, settlement, app-store, legal,
tax, staging, OBS, device, network, quota or release evidence. It makes no claim
about what any TTS provider has actually billed, and no claim that any creator
was or was not affected.
