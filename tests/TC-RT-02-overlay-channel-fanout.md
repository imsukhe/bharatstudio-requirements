# TC-RT-02 — overlay channel-keyed fanout

**Task:** `../active/tasks/RT-02.md`
**Owner:** Sukhdev Singh
**Status:** `Conditionally complete — local verification passed; external release evidence not applicable`

| Case | Control | Expected evidence |
|---|---|---|
| RT-02.1 | Channel-scoped wake | A notification for channel A wakes only channel A's subscribers; a channel B session performs zero additional store reads from it. |
| RT-02.2 | Per-channel dedup | Two sessions of the same channel, at the same cursor, cause exactly one store/replay read; both receive the same events. |
| RT-02.3 | Per-session URL composition | Each session's emitted `ttsAudioUrl` carries its own overlayId, never another session's, including the `ttsAudioUrl: null` (no artifact) case. |
| RT-02.4 | Mid-window revocation | A session revoked mid-window stops receiving events (clean close, no error frame) while a sibling session on the same channel continues. |
| RT-02.5 | Leader failure isolation | A leader replay that throws, or resolves `null`, does not propagate to followers; they fall back to their own read. |
| RT-02.6 | Cursor discrimination | Two sessions at different cursors (or channels, or limits) are never coalesced — separate reads. |
| RT-02.7 | Admission ceiling | With a ceiling configured and reached, a new stream gets `503 overlay_admission_limited`, `retryable: true`, before `reply.hijack()` — never a hang; after a disconnect the next client is admitted. |
| RT-02.8 | Malformed/unroutable notification | A malformed notification, and one with no usable `channelId`, wake nobody and throw nothing. |
| RT-02.9 | Registry leak check | Subscriber/channel admission counts return to baseline after every stream closes, repeatedly. |
| RT-02.10 | Abort mid-shared-read | Abort/disconnect during a shared (leader) read does not reject the other sessions sharing it. |
| RT-02.11 | RT-01 non-regression | A connected idle stream still performs zero store reads over a long fake-clock window. |
| RT-02.SQL | Migration 0127 | `app_private.get_overlay_events`'s new `tts_audio_artifact_id` column resolves the artifact id, is null with no artifact row, stays null under mute; every other filter (revoked/expired session, paused/closed queue, suppressed/cancelled delivery, channel scoping) is unchanged. |

**Commands:**
`pnpm --filter @bharatstudio/alerts-api build` · `pnpm --filter @bharatstudio/alerts-api test` · `pnpm --filter @bharatstudio/alerts-web test` · `pnpm contracts:validate` · `pnpm db:test:all` · `pnpm db:test:l03` · `pnpm measurement:test` · `(cd services/alert-worker-go && go test -race ./... && go vet ./...)` · `(cd services/payment-webhook-go && go test -race ./... && go vet ./...)` · `git diff --check`

**Security/data boundary:** no new personal-data field or retention rule (§31.0). Channel and overlay identifiers never enter metric labels or logs (`observability/metrics.ts` RT-02 counters are outcome-labelled only; `logSafeError` used for every new failure path). The artifact-id column move (migration 0127) closes the exact leak this task names — a shared/deduplicated replay handing one session's `ttsAudioUrl` (and therefore its overlayId) to a different session — rather than opening one.

**External evidence:** none claimed. No provider, staging, OBS, device, network or production evidence is asserted by this record; §37.7/RT-07 remain separately gated.

## Recorded local evidence — 2026-09-15

All commands run from `/Users/sukhdevsingh/Workspace/Bharat Studio/bharatstudio-alerts`, against the already-uncommitted worktree (RT-01 work and unrelated in-flight changes preserved, not reverted).

- `pnpm --filter @bharatstudio/alerts-api build` — passed (`tsc -p tsconfig.json`, no errors).
- `pnpm --filter @bharatstudio/alerts-api test` — **524 passed, 0 failed** (baseline established by Opus before this task: 511 passed, 0 failed; net +13 from this task's new tests, confirmed stable across 4 consecutive runs with no flakes). Command: `tsx --test test/**/*.test.ts`.
  - `test/overlay-wakeup.test.ts` — grew from 6 to 10 tests: added RT-02.1 (channel-scoped wake), RT-02.8 (malformed/channel-less notification), RT-02.9 (admission-slot leak check across 50 subscribe/release cycles), an independent per-instance-vs-per-channel ceiling test, an "unset limits never reject" RT-01-posture test, and an `onNotification` hook outcome test; the pre-existing reconnect/health/listener-rejection/abort tests were mechanically adapted from `waitForNotification(overlayId, ms)` to `subscribe(channelId).wait(ms)` with no assertion change beyond that shape.
  - `test/overlay-replay-coalescer.test.ts` — new file, 5 tests: RT-02.2 (exactly one read shared by two concurrent same-key callers), RT-02.6 (four distinct keys, four reads, none coalesced), RT-02.5 in both its forms (a `null` leader result, and a thrown/aborted leader read — RT-02.10) each triggering an isolated follower fallback read rather than propagating, and a same-key-after-settle case proving no stale sharing.
  - `test/app.test.ts` — 4 new route-level tests, run against the full `buildApp`/Fastify `inject()` path: RT-02.2+RT-02.3 combined (a gated concurrent read proves exactly one `replayRaw` call, and each of two sessions' SSE bodies carries only its own `overlayId` in `ttsAudioUrl`, including the null case), RT-02.1 restated at the route level with a real `createOverlayWakeup` instance and a real `pg_notify`-shaped payload (channel A's notification never reaches channel B's stream; channel A gets exactly one extra `replayRaw` call, channel B gets zero), RT-02.4 (a session capped to two `resolveSession` successes stops cleanly with `replay-complete` after exactly 2 of its own events while a sibling session on the same channel keeps replaying), and RT-02.7 (a real `createOverlayWakeup` with `maxInstanceSubscribers: 1` returns `503 overlay_admission_limited`/`retryable: true` for a second concurrent stream, and admits a third stream once the first's window closes and releases its slot).
  - RT-02.11 (RT-01 non-regression): the pre-existing "connected idle overlay performs no replay query when the wake-up wait times out" test in `app.test.ts` still passes unchanged, now running through the new `resolveSession`-aware route path (`fakeOverlays()` gained a `resolveSession` implementation; `replayRaw` was deliberately **not** added to it, so the coalescing path is exercised only by the dedicated RT-02 tests above and every pre-existing `replay()`-overriding test keeps its original behaviour through the documented fallback in `fetchEvents`).
- `pnpm --filter @bharatstudio/alerts-web test` — **331 passed, 0 failed**. Untouched by this task (no web-app change); run to confirm no incidental regression.
- `pnpm contracts:validate` — passed: 40 fixtures + the v1 template catalogue contract validated, OpenAPI 3.1 document (68 paths, 75 operation contracts) validated, 3 negative operation-contract cases validated. `contracts/openapi/v1.yaml` was **not** modified — its `ErrorEnvelope`/`errorCode` schema is a free-form string (no enumerated error-code list for this or any route), so there was nothing to add `overlay_admission_limited` to, matching the file's existing precedent of not enumerating `overlay_store_unavailable`/`overlay_replay_unavailable` either.
- `pnpm db:test:all` (`sh packages/db/tests/run-sql-suite.sh`) — **54 files passed, 0 failed**, including the new `packages/db/tests/rt02_overlay_events_artifact_column.sql` and the two pre-existing files migration 0127 required a matching update to (`l07-mute-tts-enforcement.sql`, `l07-mute-synthesis-cost-gate.sql` — both asserted `payload ->> 'ttsAudioUrl'` directly against `get_overlay_events`; updated to read the new `tts_audio_artifact_id` column, same mute-aware null, no assertion removed).
- `pnpm db:test:l03` (`sh packages/db/tests/run-l03-application-behavior.sh`, full mode, not `DB_SQL_TESTS_ONLY`) — **passed end to end, exit 0**: 20 curated SQL files passed (including the new file, added to the curated list), the Go integration legs passed (`payment-webhook-go/internal/ingress`, `payment-webhook-go/internal/reconcile`, `alert-worker-go/internal/store`), `integration/overlay-wakeup.integration.ts` passed against a real two-listener Postgres connection, `integration/overlay-cross-replica.integration.ts` (pre-existing, unrelated to this fix's edits) passed, and the apps/api concurrency integration suite (2 tests) passed. `integration/overlay-wakeup.integration.ts` pre-dated this task and called a `wakeup.wait(overlayId, timeoutMs)` shape that matched **neither** the pre-RT-01 (`waitForNotification`) nor the git-HEAD-committed (`wait(overlayId, …)`) `OverlayWakeup` contract — it was already broken before this task started (confirmed: unmodified since the repository's first commit, `git log`). Fixed as part of this task to the new `subscribe(channelId).wait(timeoutMs)` shape, and strengthened to prove cross-listener channel isolation against a real database (two independent LISTEN connections both receive the same raw Postgres `NOTIFY`; only the matching channel's subscription resolves).
- `pnpm measurement:test` — passed: 5 Node tests + 4 Python "runner seam" tests, all passing (unaffected by this task).
- `(cd services/alert-worker-go && go test -race ./... && go vet ./...)` — passed, all packages `ok` (cached where unchanged), `go vet` clean. Untouched by this task.
- `(cd services/payment-webhook-go && go test -race ./... && go vet ./...)` — passed, all packages `ok` (cached where unchanged), `go vet` clean. Untouched by this task.
- `git diff --check` — clean, no whitespace errors.

**External blocker:** none. PostgreSQL 16 was available locally via Docker (`postgres:16-alpine`), so `db:test:all` and `db:test:l03` ran to completion rather than being recorded as blocked.

**Rollback proof:** not separately rehearsed as a live drill in this session — the rollback path is stated in the task record's Rollback field (revert the listed application files; roll back migration 0127 with a new forward migration, never by editing/deleting it) and is mechanically the same shape RT-01's own rollback proof used.

## Independent Opus verification — 2026-09-16

The orchestrator re-ran the checks itself against the actual worktree rather than accepting
the implementation report, and read the changed files directly.

- `pnpm --filter @bharatstudio/alerts-api build` — passed.
- `pnpm --filter @bharatstudio/alerts-api test` — **524 passed, 0 failed** (Opus's own
  pre-task baseline on the same worktree was 511/0).
- `pnpm --filter @bharatstudio/alerts-web test` — **331 passed, 0 failed**.
- `pnpm db:test:all` — **54 passed, 0 failed**, run twice (before and after the
  naming correction below).
- `pnpm contracts:validate` — passed: 40 fixtures, 68 OpenAPI paths, 75 operation
  contracts, 3 negative cases.
- `pnpm measurement:test` — 5 passed, 0 failed.
- `(cd services/alert-worker-go && go test -race ./... && go vet ./...)` — passed.
- `(cd services/payment-webhook-go && go test -race ./... && go vet ./...)` — passed.
- `git diff --check` — clean.
- `python3 tools/doc_consistency.py` — 17 checks, 0 errors, 0 warnings.
- `python3 tools/traceability.py` — regenerated; register-map and semantic-mapping-audit
  parity re-established for RT-01 and RT-02 (the generator refused the state change until
  all three files agreed, which is the fail-closed behaviour working).

**Migration 0127 diffed against 0101's function body.** Only three things differ: the
`returns table` shape, the removal of the inline `ttsAudioUrl`, and the new mute-aware
`tts_audio_artifact_id` expression. Every `from`, `join`, `left join lateral`, `where`,
`order by` and `limit` clause is identical, so the L07 mute rule, the revoked/expired
session filters, the paused/closed queue filters, `delivery_dispatch_allowed` and the
channel scoping are unchanged by construction, not merely by test.

**The two edited pre-existing SQL tests were audited line by line**, because editing a test
to match new code is where a regression hides. Every change is a mechanical column swap
(`payload ->> 'ttsAudioUrl'` → `tts_audio_artifact_id::text`). No assertion was removed,
no `raise exception` deleted, no condition inverted, and the `ttsAudioDurationMs`
assertion is untouched.

**One finding, low severity, fixed.** Those two files still named their variables
`muted_url` / `sibling_url` / `restored_url` and raised exceptions saying "carried a
ttsAudioUrl" while in fact reading an artifact id — a failure message that would send a
future reader hunting for a URL the function no longer returns. Renamed to
`*_artifact_id` with matching message text; `pnpm db:test:all` re-run, still 54/0.

**No reproducible defect was found** in the registry, the coalescer, the route, the store
or the migration.

**What this evidence is not.** Every line above is local. None of it is production,
provider, app-store, legal, tax, staging, OBS, device, network, quota or release evidence,
and none of it may be cited as performance evidence (§35.1 rule 6). RT-07 remains the row
that gates any performance claim, and it is blocked.
