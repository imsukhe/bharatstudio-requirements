# TC-RT-03 — checks, then synthesis, then one release

**Task:** `../active/tasks/RT-03.md`
**Owner:** Sukhdev Singh
**Status:** `Conditionally complete — local verification passed; external release evidence not applicable`

| Case | Control | Expected evidence |
|---|---|---|
| RT-03.1 | Checks before synthesis | `apps/api/src/routes/tts.ts` already resolves eligibility (moderation/mute/routing, §11.10 fold-in per `0103`), then quota (`meter()`, hard stop), and only then calls `service.synthesize()` — proven by existing not-eligible/quota-denied tests asserting `providerCalled === false` / `meterCalled === false`, unchanged by this task. Assert ordering (call sequence), not wall-clock. |
| RT-03.2 | One release, together | `internal/handler/cloud_tasks.go` calls `Enricher.Enrich` once, then `Store.Release` once, unconditionally of the enrichment outcome — no second event, no late join. `TestCloudTaskHandlerReleasesRegardlessOfEnrichOutcome` (success/timeout/terminal) each assert exactly one `Store.Release` call and one 200/`accepted` response. |
| RT-03.3 | **Timeout is never retried** | `TestClientNeverRetriesATimeout` (`internal/tts/client_test.go`): a handler that never responds within the client's timeout budget yields `EnrichClass = timeout_ambiguous`, `Attempts = 1`, and the server receives exactly one request — proving no retry. |
| RT-03.4 | Unambiguous failure is retried, then succeeds with audio | `TestClientRetriesUnambiguousFailureThenSucceeds` (a synthetic connection-refused `*net.OpError` on attempt 1, a real server on attempt 2) and `TestClientRetriesA5xxOnce`/`TestClientRetries429OnlyWithRetryAfter` (a 5xx or a 429-with-`Retry-After` on attempt 1, 200 on attempt 2) each assert `Attempts = 2`, final `Class = success`. |
| RT-03.5 | Terminal failure is not retried, releases without audio | `TestClientNeverRetriesATerminalFailure` (401 with no `Retry-After`): `Class = terminal`, `Attempts = 1`, exactly one server request. At the route layer, `tts-quota-metering.test.ts`'s `tier_not_entitled`/`quota_exhausted` cases already return `chime` without reaching the provider, unchanged. |
| RT-03.6 | **A failed synthesis of every class leaves the creator's premium-character balance unchanged** | `packages/db/tests/rt03_tts_quota_reservation_release.sql`: reserve then release restores the exact pre-reservation balance; a second release is a safe no-op (never negative, never manufactures quota); a partial release leaves the correct remainder. At the route layer, `tts-quota-metering.test.ts`'s new tests assert `quotaMeter.release(eventId, characterCount)` is called with exactly the metered character count on a provider throw and on a provider chime-mode result, and is never called on success or on a pre-synthesis quota denial (nothing was reserved). |
| RT-03.7 | Muted queue never invokes synthesis | `apps/api/test/l07-mute-synthesis-cost-gate.test.ts` (pre-existing, `0103`, mechanically extended with the new `release` fake method, no assertion changed): an event whose entire fan-out is muted reaches neither the quota meter nor the provider. `packages/db/tests/l07-mute-synthesis-cost-gate.sql` (pre-existing, untouched) is the SQL-level proof. |
| RT-03.8 | Synthesis failure never degrades the task outcome or re-delivers | `TestCloudTaskHandlerReleasesRegardlessOfEnrichOutcome`: for `success`/`timeout_ambiguous`/`terminal` outcomes, `Store.Retry` is called zero times and the response is always `200`/`accepted` — a synthesis failure can never turn `ObserveTaskOutcome` into `retryable`, and `Store.Release` is called exactly once, never duplicated. |
| RT-03.9 | Overlay orders its display queue by alert creation time | `apps/web/app/overlay/overlay-policy.test.ts`'s new test: an item created first but arriving second (simulating slow synthesis) is selected ahead of an item created second but arriving first. |
| RT-03.10 | Quota exhaustion falls to browser voice immediately, no grace | Unchanged pre-existing behaviour (`0081`/`0096`, ladder 20K/40K/60K, §11.11) — `tts-quota-metering.test.ts`'s `quota_exhausted` case still returns `chime`/`reason: quota_exhausted` with no delay and no grace allowance; this task adds no wait and no buffer anywhere in that path. |
| RT-03.11 | Go `-race` clean on new concurrency | `go test -race ./...` in `services/alert-worker-go`, all packages `ok`, including `internal/tts` (1.960s) and `internal/handler`. |
| RT-03.SQL | Reservation/release invariants | `packages/db/tests/rt03_tts_quota_reservation_release.sql`: boundary reserve, exact release, double-release no-op, partial release, zero-character no-op, negative-count rejection (`22023`), unknown-event-id rejection (`23503`) — same fail-closed shape as `meter_tts_usage`. |

**Commands:**
`pnpm --filter @bharatstudio/alerts-api build` · `pnpm --filter @bharatstudio/alerts-api test` · `pnpm --filter @bharatstudio/alerts-web test` · `pnpm contracts:validate` · `pnpm db:test:all` · `pnpm db:test:l03` · `pnpm measurement:test` · `(cd services/alert-worker-go && go build ./... && go test -race ./... && go vet ./...)` · `(cd services/payment-webhook-go && go test -race ./... && go vet ./...)` · `git diff --check`

**Security/data boundary:** no new personal-data field or retention rule (§31.0). The Go-side classification token (`success`/`timeout_ambiguous`/`terminal`) is logged via the existing bounded `Logger.Event(component, outcome, traceId)` shape — never an event, channel, payment or provider identifier. No new log or metric was added on the TypeScript side; existing `logSafeError` usage in `apps/api/src/routes/tts.ts` is unchanged.

**External evidence:** none claimed. No provider, staging, OBS, device, network or production evidence is asserted by this record; §37.7/RT-07 remain separately gated, and no "lag-free"/"fast"/"smooth" claim is made anywhere in this record or the task record (§19.0's claim ban stands until RT-01..RT-07 all close).

## Recorded local evidence — 2026-09-16

All commands run from `/Users/sukhdevsingh/Workspace/Bharat Studio/bharatstudio-alerts`, against the already-uncommitted worktree at commit `012aff3` (no unrelated file reverted or stashed; only the files this task's record names were touched).

- `pnpm --filter @bharatstudio/alerts-api build` — passed (`tsc -p tsconfig.json`, no errors).
- `pnpm --filter @bharatstudio/alerts-api test` — **528 passed, 0 failed** (baseline `524/0`; net +4 from this task's new `tts-quota-metering.test.ts` RT-03.6 cases). Command: `tsx --test test/**/*.test.ts`.
- `pnpm --filter @bharatstudio/alerts-web test` — **332 passed, 0 failed** (baseline `331/0`; net +1, the new `overlay-policy.test.ts` RT-03.9 case).
- `pnpm contracts:validate` — passed: 40 fixtures + the v1 template catalogue contract, OpenAPI 3.1 document (68 paths, 75 operation contracts), 3 negative operation-contract cases. `contracts/openapi/v1.yaml` was not modified — this task added no new route and no new error code to any route's documented response set.
- `pnpm db:test:all` (`sh packages/db/tests/run-sql-suite.sh`) — **55 files passed, 0 failed** (baseline `54/0`; net +1, the new `rt03_tts_quota_reservation_release.sql`).
- `pnpm db:test:l03` (`sh packages/db/tests/run-l03-application-behavior.sh`, full mode) — **passed end to end, exit 0**: **21 curated SQL files passed** (baseline 20; the new file added to the curated list in `run-l03-application-behavior.sh`), the Go integration legs passed (`payment-webhook-go/internal/ingress`, `payment-webhook-go/internal/reconcile`, `alert-worker-go/internal/store`), `integration/overlay-wakeup.integration.ts` and `integration/overlay-cross-replica.integration.ts` passed, and the apps/api concurrency integration suite (2 tests) passed.
  - **One collision found and fixed during this task, not left in place:** the first draft of `rt03_tts_quota_reservation_release.sql` reused the synthetic id `00000000-0000-4000-8000-000000001301`, which `l03_queue_mode_ladder.sql` already uses. `db:test:all` (per-file isolated databases) did not surface it; the sequential `db:test:l03` run did (`duplicate key value violates unique constraint "app_users_pkey"`). Fixed by moving every synthetic id in the new file to a confirmed-unused `...0000f003...` block (checked against every existing `packages/db/tests/*.sql` file before and after the change) and re-running both suites clean.
- `pnpm measurement:test` — passed: 5 Node tests + 4 Python runner-seam tests (unaffected by this task; baseline unchanged).
- `(cd services/alert-worker-go && go build ./... && go test -race ./... && go vet ./...)` — `go build ./...` passed (covers `cmd/alert-worker`, the location a previous attempt at this row left broken, per the operator's warning). `go test -race ./...` passed, all packages `ok`, including `internal/tts` (1.960s, new classification/retry tests) and `internal/handler` (new `TestCloudTaskHandlerReleasesRegardlessOfEnrichOutcome`/`TestCloudTaskHandlerReleasesWithNoEnricherConfigured`). `go vet ./...` clean.
  - **One test-authoring mistake found and fixed during this task:** an early draft of `TestClientNeverRetriesATimeout` had its HTTP handler block forever on `<-request.Context().Done()` with `defer server.Close()`, which hung `go test` past 120 seconds in this environment (`httptest.Server.Close()` blocks until outstanding requests complete). Fixed by bounding the handler with a 300ms fallback (`select { case <-request.Context().Done(): case <-time.After(300 * time.Millisecond): }`) so `Close()` can never block indefinitely; re-run confirmed `internal/tts` completes in under a second.
- `(cd services/payment-webhook-go && go test -race ./... && go vet ./...)` — passed, all packages `ok` (cached where unchanged). Untouched by this task.
- `git diff --check` — clean, no whitespace errors.

**External blocker:** none. PostgreSQL 16 was available locally via Docker (`postgres:16-alpine`), so `db:test:all` and `db:test:l03` ran to completion rather than being recorded as blocked.

**Rollback proof:** not separately rehearsed as a live drill in this session. The rollback path is stated in the task record's Rollback field (revert the listed application files; delete the new SQL test file directly; roll back migration `0128` with a new forward migration, never by editing/deleting it) — mechanically the same shape RT-01/RT-02's own rollback proofs used.

## Independent Opus verification — 2026-09-16

Re-run against the actual worktree, with the changed files read directly rather than the
implementation report taken at face value.

- `pnpm --filter @bharatstudio/alerts-api test` — **528 passed, 0 failed** (Opus's own
  pre-task baseline on the committed tree: 524/0).
- `pnpm --filter @bharatstudio/alerts-web test` — **332 passed, 0 failed** (baseline 331/0).
- `pnpm db:test:all` — **55 passed, 0 failed**, run twice (before and after the correction
  below), including the new `rt03_tts_quota_reservation_release.sql`.
- `(cd services/alert-worker-go && go build ./... && go test -race ./... && go vet ./...)` —
  build clean **including `cmd/alert-worker`**, 10 packages `ok` under `-race`, vet clean.
  Checked explicitly because a prior interrupted attempt left the module non-building at
  exactly that call site.

**The timeout rule holds by construction, not by convention.** `classifyTransportError`
never returns `enrichRetryableUnambiguous` for a timeout or context deadline, so `Enrich`'s
single retry is unreachable from the ambiguous class. That is the rule protecting a
creator's premium characters from being spent twice, and it is structural rather than a
branch someone can later reorder by accident.

**The release is wired to every synthesis-failure path in `apps/api/src/routes/tts.ts`** —
the provider throwing, and the provider answering `chime`. It is deliberately **not** wired
to a failure after a successful synthesis (a `storeAudio` failure), because at that point
the provider has done the work and billed for it; releasing there would manufacture quota.

### Finding, fixed during the audit

Migration `0128`'s comment claimed the `greatest(...,0)` floor meant a release "can never
manufacture quota that was not actually reserved, even if release were ever called twice."
**That is false.** The floor guarantees only that the counter cannot go negative. A double
release, while the month's counter holds other usage, would return twice the characters and
hand the creator quota they never reserved. The guarantee that actually holds lives in the
caller — `tts.ts` releases on mutually exclusive paths, at most once per metered request.
The comment now states the real guarantee and names the invariant any future caller must
keep. An overstated comment on a money-adjacent function is how a later change quietly
becomes a billing defect. `pnpm db:test:all` re-run after the correction: 55/0.

### Known limitation, recorded rather than hidden

A reservation made in one billing month and released in the next is a no-op — the creator
keeps the charge for that one failed synthesis. It requires a synthesis failure spanning
midnight on the first of a month. Recorded here and in the migration; not fixed, because
fixing it means storing per-reservation state, which is a larger change than RT-03's scope.

### Referred to the owner — NOT fixed here, out of RT-03's scope

**A cache hit consumes premium characters.** `apps/api/src/routes/tts.ts` calls
`quotaMeter.meter(...)` before `service.synthesize(...)`, and `createTtsService.synthesize`
(`apps/api/src/tts/provider.ts:94-96`) returns `{ mode: 'audio', cacheHit: true }` straight
from `alert_tts_cache` without reaching the provider. The route never inspects `cacheHit`.
So a repeated message is charged to the creator's ladder every time, while costing the
platform nothing. This is not a *failure*, so RT-03.6 does not cover it, and whether the
creator's character ladder represents platform provider cost or a product allowance is a
pricing decision — adjacent to the open §33.2 item on what a rupee of credit buys. Raised
to the owner; deliberately not decided or changed here.

**What this evidence is not.** Every line is local. None of it is production, provider,
app-store, legal, tax, staging, OBS, device, network, quota or release evidence, and none
may be cited as performance evidence (§35.1 rule 6).

---

## Correction and re-verification, 2026-09-16 — RT-03.6 tightened (migration `0134`)

**RT-03.6's evidence line above is superseded, and the reason matters more than
the replacement.** The clause "a second release is a safe no-op (never
negative, never manufactures quota)" was recorded as proven. It was not. The
test that proved it released a billing month whose counter had already reached
`0`, the single arrangement where `greatest(...,0)` floors the second
subtraction and hides the fact that `release_tts_usage_reservation(uuid, integer)`
had no idempotency of its own. Against a month holding other usage, the same
double release subtracted twice and manufactured quota. The check was blind to
the case it was never told about.

A second, unproven property was also claimed by the `TtsQuotaMeter` interface
comment rather than by a test: that a release never manufactures quota after a
billing-month rollover. It did — a release always credited the *current* month,
so a rollover between reserve and release left the old month charged and the new
month credited characters it never reserved.

**Replacement evidence.** `packages/db/tests/rt03_tts_quota_reservation_release.sql`
(rewritten) now proves, against migration `0134`:

| Case | What it asserts |
|---|---|
| Reserve → release | The exact pre-reservation balance is restored. |
| **Double release while another reservation is open** | The month's counter stays at the other reservation's charge. This is the case the previous test could not see. |
| The other reservation afterwards | Still releases exactly once, for exactly its own charge — a duplicate release of one reservation does not disturb another. |
| **Release after a billing-month rollover** | Credits the month the reservation names, with the current month left untouched at its own usage. |
| Null reservation id | Safe no-op. |
| Zero-character meter | Charges nothing and writes no reservation at all, so no zero-character row can exist to be released. |
| Negative character count | Rejected, `22023`. |
| Unknown reservation id | Raises `23503` rather than silently releasing against nothing. |
| `bsa_app` direct table access | Refused (`insufficient_privilege`) — the ledger is reachable only through the two security-definer functions. |

The "partial release" case is **gone, not relocated**: release is now
all-or-nothing per reservation, so releasing less than was reserved is no longer
expressible. See `active/tasks/RT-03.md`'s Correction for why that narrowing was
deliberate.

**Route-layer evidence** (`apps/api/test/tts-quota-metering.test.ts`): the
assertions now name the reservation id rather than a character count —
`release(reservationId)` is called with the id the meter returned on a provider
throw and on a provider chime-mode result, on a cache hit, and never on success
or on a pre-synthesis quota denial.

**Commands and outputs, 2026-09-16.**

- `pnpm db:test:all` → `SQL SUITE: pass=61 fail=0`
- `pnpm --filter @bharatstudio/alerts-api test` → `tests 590  pass 590  fail 0`
- `pnpm db:test:l03` → `pass 2  fail 0`
- `pnpm --filter @bharatstudio/alerts-api build` → clean (`tsc -p tsconfig.json`)
- `pnpm contracts:validate` → 70 paths, 77 operation contracts, 40 fixtures
- `pnpm explain:check` → `16/16 plans current`, 16 manifest entries + 6 exemptions

**Negative verification — each defect reintroduced separately, then reverted.**

| Defect reintroduced | Result |
|---|---|
| `released_at` guard disabled (0128's non-idempotency) | `FAIL rt03_tts_quota_reservation_release` · `SQL SUITE: pass=60 fail=1` |
| Release re-pointed at `date_trunc('month', current_timestamp)` (0128's month bug) | `FAIL rt03_tts_quota_reservation_release` · `SQL SUITE: pass=60 fail=1` |

The migration was restored byte-identical after each run (`diff` clean). Neither
defect was caught by the previous version of this test; both runs are recorded
because that contrast, not the green, is the evidence that the new test is worth
having.

**What this evidence is not.** Local only. It is not production, provider,
invoice, settlement, app-store, legal, tax, staging, OBS, device, network,
quota or release evidence, and it makes no claim about what any TTS provider
has actually billed.
