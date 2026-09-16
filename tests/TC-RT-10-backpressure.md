# TC-RT-10 — backpressure: payment traffic outranks widget/dashboard/analytics reads

**Task:** `../active/tasks/RT-10.md`
**Owner:** Sukhdev Singh
**Status:** `Conditionally complete — local verification passed; external release evidence not applicable`

| Case | Control | Expected evidence |
|---|---|---|
| RT-10.1 | A widget/analytics burst cannot exhaust the capacity a payment path needs | `RT-10.1/RT-10.2: a widget-read burst cannot exhaust a ceiling shared with nothing else — the second concurrent governed read is shed with a clear retryable 503, never a hang` (`rt10-read-backpressure.test.ts`) — a real `buildApp` instance, a governed `/v1/overlay-goals/:overlayId` route held open by its store, a ceiling of 1: the second concurrent request to the SAME governed surface is shed while the first is still in flight, and completes normally once released. `RT-10.4`'s companion test (below) proves the payment write path is architecturally never subject to the same ceiling at all |
| RT-10.2 | A shed low-priority read returns a clear retryable response, never a hang or a partial render presented as complete | Same test: asserts `statusCode === 503`, `errorCode === 'derived_read_shed'`, `retryable === true`, and a `retry-after` header present. The route never reaches its handler (admission happens in `onRequest`, before body parsing/auth/store calls), so nothing partial is ever rendered — it is refused outright, not degraded |
| RT-10.3 | An unclassified route fails safe toward the lower priority | `RT-10.1/RT-10.3: classifyReadPriority is GET-only, and an unnamed GET route fails safe toward the lower (derived_read) priority` (`rt10-read-backpressure.test.ts`): a GET route the classifier has never seen (`/v1/some-new-surface-nobody-classified-yet`) returns `'derived_read'`, never `'exempt'` — the fail-safe default is proven directly, not merely asserted in a comment |
| RT-10.4 | Payments, webhooks, alert deliveries and overlay events are never shed, delayed or degraded by backpressure | `RT-10.4: every non-GET request is structurally outside the governed class...` (unit: every write method returns `null` from the classifier, regardless of route) and `RT-10.4: a payment-order write is never shed, even while the derived-read ceiling is fully exhausted` (integration: a real `POST /v1/public/channels/:handle/tips/orders` succeeds with `201` while the governor's ceiling is configured to `0` — the write is proven never to pass through the governor at all, not merely "usually admitted") |
| RT-10.SHARED | Admission governor unit behaviour | `RT-10: unset ceiling never sheds`, `RT-10.1/RT-10.2: a configured ceiling sheds once at capacity, and a released slot frees capacity for the next request`, `RT-10: tryAdmit never throws and never performs I/O — a metrics callback failure cannot break admission` (`rt10-read-backpressure.test.ts`) |

**Commands (from `bharatstudio-alerts`):**
`pnpm --filter @bharatstudio/alerts-api build` · `pnpm --filter @bharatstudio/alerts-api test` · `pnpm --filter @bharatstudio/alerts-web test` · `pnpm contracts:validate` · `pnpm db:test:all` · `pnpm db:test:l03` · `pnpm measurement:test` · both Go services' `go build ./... && go test -race ./... && go vet ./...` (unaffected — this row touches no Go code) · `git diff --check`

**Commands (from `bharatstudio-requirements`):** `python3 tools/doc_consistency.py` · `python3 tools/traceability.py`

**Security/data boundary:** no new personal-data field. `bsa_derived_read_admission_total`'s only label is a bounded `outcome` (`admitted`/`shed`) — never a route, channel, overlay or payment identifier, same discipline as every RT-02/RT-06 counter.

**External evidence:** none claimed. This row is TypeScript-only, in-process admission control and connection-pool isolation, verified locally. It makes no claim about behaviour under real production load, real Cloud Run multi-instance scaling, or a real database connection budget at the concurrency target (2,000 overlays) — that is RT-07, `Blocked`. See the shared review record for exactly what PostgreSQL/Cloud SQL/Cloud Run documentation was read and what it does and does not establish locally.

## Recorded local evidence

- `pnpm --filter @bharatstudio/alerts-api build` — clean.
- `pnpm --filter @bharatstudio/alerts-api test` — **564 passed, 0 failed** (547 RT-06 baseline + 7 RT-10 + 10 RT-11).
- `pnpm contracts:validate` — 40 fixtures + the v1 template catalogue contract, 68 OpenAPI paths/75 operation contracts, 3 negative cases — **unchanged**; this task added no route and no route added a new response shape to the OpenAPI contract (the `503 derived_read_shed` body reuses the existing generic error envelope shape every other route's `503` already uses).
- See `tests/TC-RT-11-read-timeout.md` and `tests/TC-RT-12-explain-plans.md` for the remaining commands (`db:test:all`, `db:test:l03`, `measurement:test`, both Go services, `git diff --check`, `doc_consistency.py`, `traceability.py`) — run once for the whole three-row slice, recorded there to avoid repeating identical output three times.
