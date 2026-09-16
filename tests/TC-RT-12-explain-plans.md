# TC-RT-12 — checked-in EXPLAIN plans for every widget-backing query

**Task:** `../active/tasks/RT-12.md`
**Owner:** Sukhdev Singh
**Status:** `Conditionally complete — local verification passed; external release evidence not applicable`

| Case | Control | Expected evidence |
|---|---|---|
| RT-12.1 | Every widget-backing query has a checked-in plan artefact | `packages/db/explain-plans/goal.explain.md`, `challenge.explain.md`, `hype.explain.md`, `leaderboard.explain.md`, `vote.explain.md`, `paid-vote.explain.md`, `recent-tips.explain.md`, `top-supporters.explain.md`, `supporter-ticker.explain.md`, `mega-tip-banner.explain.md` — ten artefacts covering the nine widgets named in `apps/web/app/overlay/widgets/` (vote counted twice: the free-tally and paid-tally functions both back the vote widget's two configurations) |
| RT-12.2 | Changing a query without refreshing its plan fails the check | `packages/db/explain-plans/check-plans.mjs`: re-extracts each function's CURRENT body from `packages/db/migrations/`, recomputes its sha256, compares to the artefact's recorded `query_hash`; a mismatch is reported by widget name and the script exits non-zero. Verified by construction — the extraction method used to WRITE each artefact's hash and the one `check-plans.mjs` uses to RECOMPUTE it are the identical function, so a query-text edit that changes either one byte of the function body changes the hash and is caught |
| RT-12.3 | Plan assertions are about shape, not timing | `check-plans.mjs` compares only the `query_hash` (a hash of SQL text) — it makes no assertion about any `EXPLAIN ANALYZE` actual-time figure. Each artefact's own "Plan shape:" line names the scan node(s) actually used (index scan vs. sequential scan), which is the assertion a human reviewer checks on a plan refresh; no CI gate compares a duration number, deliberately, because a duration from an unsized local database would be noise |
| RT-12.4 | The artefacts themselves state they are change detectors, not production-size proof | Every one of the ten artefacts carries the disclosure sentence verbatim (see `active/tasks/RT-12.md`'s "What this proves and what it does not") — checked directly in each file, not only asserted in this record |

**Commands (from `bharatstudio-alerts`):**
`node packages/db/explain-plans/check-plans.mjs` (new — the RT-12-specific check; needs no live database) · plus the full slice-wide command set recorded once in the shared review record (`pnpm --filter @bharatstudio/alerts-api build/test`, `pnpm --filter @bharatstudio/alerts-web test`, `pnpm contracts:validate`, `pnpm db:test:all`, `pnpm db:test:l03`, `pnpm measurement:test`, both Go services, `git diff --check`)

**Commands (from `bharatstudio-requirements`):** `python3 tools/doc_consistency.py` · `python3 tools/traceability.py`

**Security/data boundary:** every seeded row used to produce a non-empty EXPLAIN result is synthetic, inserted directly into a throwaway local Postgres container created and destroyed for this capture — never a real channel, payment or supporter identity, and never persisted anywhere this repository's application code reads from.

**External evidence:** none claimed, and explicitly disclaimed inside every artefact. This is local, unsized-database evidence only — see "What this proves and what it does not" in `active/tasks/RT-12.md`. No §19.4 duration budget is claimed met by any artefact here.

## Recorded local evidence

- `node packages/db/explain-plans/check-plans.mjs` (and `pnpm explain:check`) — **`OK: 10/10 plans current`, exit code 0.** Additionally verified to correctly FAIL (exit 1, naming the widget) when one artifact's `query_hash` is deliberately tampered with, then restored — the negative case was exercised, not assumed.
- EXPLAIN capture method: a throwaway `postgres:16-alpine` docker container (`rt12-explain-pg-80132`, removed on completion), roles + all 130 migrations (`packages/db/roles/0001_v1_service_roles.sql` through `packages/db/migrations/0130_v1_rt06_reliability_reconciliation_snapshot.sql`) applied in order, synthetic seed data inserted (one channel/session, 2 goals, 2 challenges, 3 interaction definitions with vote/hype state, 2 viewers, 5 payments, 2 alert events, 1 vote-payment tag), `EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT)` run against each of the ten `app_private.list_overlay_*` functions. The existing dev container (`bharatstudio-alerts-postgres-1`) was not touched.
- **All 10 widgets returned real, non-zero-row EXPLAIN captures — none fell back to a zero-row/empty-table plan.**
- **Correction found during capture:** all ten functions are `security definer` as well as `language sql stable`, and Postgres never inlines a SECURITY DEFINER function — so the literal `EXPLAIN SELECT * FROM app_private.<fn>(...)` call always yields an opaque `Function Scan` node, not the join plan originally assumed reachable this way. Each artifact therefore also captures a supplementary "unwrapped" EXPLAIN of the function body with the seeded literals substituted in, which does show the real scan nodes. 7 of 10 widgets (goal, challenge, vote, paid-vote, recent-tips, supporter-ticker, mega-tip-banner) unwrap to a fully resolved plan (real `Index Scan` nodes throughout); 3 of 10 (hype, leaderboard, top-supporters) call a second security-definer/plpgsql helper internally that stays opaque even unwrapped, disclosed individually in each of those three artifacts. Full detail: the shared review record's §4.
- Remaining slice-wide commands (`pnpm --filter @bharatstudio/alerts-api build/test`, web test, `contracts:validate`, `db:test:all`, `db:test:l03`, `measurement:test`, both Go services, `git diff --check`, `doc_consistency.py`, `traceability.py`) — see the shared review record's "Checks run for the whole slice" section for the single consolidated run covering RT-10, RT-11 and RT-12 together.

## Independent Opus verification — 2026-09-16

Files read directly; checks re-run rather than the report accepted. The implementing
agent's final report arrived truncated — no changed-file list and no test counts — so the
entire state below was established from the worktree, not from its claims.

- `pnpm --filter @bharatstudio/alerts-api build` — passed.
- `pnpm --filter @bharatstudio/alerts-api test` — **564 passed, 0 failed** (baseline 547).
- `pnpm --filter @bharatstudio/alerts-web test` — **332 passed, 0 failed**.
- `pnpm db:test:all` — **57 passed, 0 failed**. `pnpm contracts:validate` — clean.
- Both Go services: `go build ./...` clean, **10 packages `ok`** each under `-race`, vet clean.
- `pnpm explain:check` — **OK: 10/10 plans current**.
- `git diff --check` clean; `python3 tools/doc_consistency.py` — 17 checks, 0 errors, 0 warnings.

**RT-10.4 and RT-11.2 hold by construction, not by a list.** `classifyReadPriority`
short-circuits on `method !== 'GET'`, so no payment write, webhook commit, alert delivery or
overlay event can ever be shed or timed out — they are never classified at all. Every such
path in this API is a POST/PUT/DELETE, or lives in a Go service with its own connections
that this module never touches. A classification *list* could be gotten wrong; a structural
short-circuit cannot. The unclassified default is `derived_read`, the lower priority, which
is the correct fail-safe direction: a misclassified read starving a payment is the exact
failure RT-10 exists to prevent.

**All three values are unset.** `WIDGET_ANALYTICS_MAX_CONCURRENT_READS`,
`WIDGET_ANALYTICS_POOL_MAX` and `WIDGET_ANALYTICS_STATEMENT_TIMEOUT_MS` default to today's
behaviour exactly. The one derivable constraint is enforced: a statement timeout below
**200ms** is rejected at startup, because §19.4 states that as the API read p99 budget and a
timeout beneath it would cancel queries that are still compliant. That number is quoted from
the authority, not chosen.

### The artefacts corrected a premise in the task command, with a citation

The command assumed that because these functions are `language sql stable`, PostgreSQL would
inline them and `EXPLAIN SELECT * FROM app_private.<fn>(...)` would expose the real join and
scan plan. **That is wrong, and the artefacts say why**: all ten are additionally
`security definer`, and the planner never inlines a SECURITY DEFINER SQL function regardless
of STABLE — inlining would run the body with the *caller's* privileges and search_path. The
artefacts cite `inline_function()` in `src/backend/optimizer/util/clauses.c`
(`if (funcform->prosecdef) goto fail;`). The literal command therefore yields an opaque
`Function Scan` node with no visible detail, on every PostgreSQL version.

The resolution captures **both** — the literal EXPLAIN exactly as specified, reproducible
verbatim, and an unwrapped EXPLAIN of the function body with parameters substituted, which
surfaces the real index-versus-sequential-scan nodes the row actually wants. Inner
security-definer calls stay opaque and are noted per widget. This is the correct behaviour
when a command's premise is wrong: report it and solve it visibly, not work around it.

### Finding, fixed during the audit

**`explain:check` existed but was not in `verify:local`.** A check that the full local gate
never runs is the §2 pattern this entire document exists to prevent — code that works,
committed, and unreachable by anyone. Wired into `verify:local` immediately after
`contracts:validate`; it needs no database (it is a static text check) so it adds no
dependency to the gate. Re-run after wiring: **OK: 10/10 plans current**.

**What this evidence is not.** The plans were captured against a minimally-seeded local
database, not §37.4's 500 channels / 2,000,000 payments / 5,000,000 alert events. Each
artefact states that in its own body. They are **plan-shape change detectors**, not evidence
that any §19.4 budget is met at production scale. Nothing local is production, provider,
store, legal, tax, staging, OBS, device, network, quota or release evidence (§35.1 rule 6).

### Correction to the orchestrator's own scoping claim

The task command told the implementer that `apps/api/src/app.ts` used a database pool at
`max: 120`. **That was wrong.** The `max: 120` there is the `fastify-rate-limit` requests-
per-minute cap, not a connection pool; the grep that produced it matched a rate-limit
option. The real shared pool is `createSqlClient` in
`apps/api/src/db/public-channel-repository.ts` at **`max: 10`** — a name that undersells what
it is, since it backs far more than public channels. Verified directly. The implementer
caught it, said so, and used the correct value; no work was built on the wrong number.

### Two limitations recorded rather than smoothed over

**RT-11.1 is Unverified.** That a PostgreSQL `57014` (`query_canceled`) is raised and
translated end-to-end is verified from the library source and by unit test, **not** against a
real live cancellation. Proving it needs a query held long enough to be cancelled against a
real server — doable, but not done, and it is not claimed.

**RT-10's protection reaches five wired stores, not every classified route.** The classifier
can classify any GET, but the isolated pool is wired into five verified read-only stores
(overlay goals, overlay challenges, interaction overlay, paid-vote overlay, payment ledger)
plus the widget layer. Other derived GETs are classified but still share the main pool.
Whether to widen it is an open question referred to the owner. This is the main reason RT-10
is `P`.

## Downgraded U → P on 2026-09-16 — a blind spot found by the next task

PRF-02 added two overlay-backing functions, `app_private.list_channel_master_canvas_modules`
and `app_private.list_overlay_master_canvas_modules`. Neither has an EXPLAIN artefact.
`pnpm explain:check` reports **OK: 10/10 plans current**.

**The checker is artefact-driven.** It enumerates the `*.explain.md` files that exist,
re-extracts each documented function body from its migration, and compares hashes. That
proves every plan it knows about is current. It has no notion of which queries *ought* to
have a plan, so a widget-backing query that never got one is invisible to it and the suite
stays green.

RT-12's row asks for a plan "for **every** widget-backing query, re-checked when the query
changes". The second half is enforced. **The first half is not**, and that is the §2 failure
pattern — a check that exists, runs, passes, and cannot catch the thing it was built for —
appearing inside the check written to prevent regressions, within hours of the row being
marked `U`. Marking it `U` was my error; `P` is the honest state.

**Not fixed here.** Closing it needs both the two missing artefacts captured against a
running database, and a checker that can tell which queries require one — which needs a
declared set rather than a directory listing, since "widget-backing" is not inferable from a
filename. Folded into the next PRF-02 slice, because every module ported adds
widget-backing queries and the gap would otherwise recur once per slice.

## Update 2026-09-16 — PRF-02 slice 2: manifest + scan built, narrowed not fully closed

`active/tasks/PRF-02.md`'s "Slice 2" section and
`reviews/2026-09-16-prf-02-slice-2-implementation.md` carry the full account. Summary for this
record:

**What was built.** `packages/db/explain-plans/required-queries.json` is now the declared set
this "Not fixed here" note above said was needed — every `app_private` function that backs an
overlay/widget-facing route, 15 entries. `packages/db/explain-plans/scan-required-queries.mjs`
scans `apps/api/src/db/*.ts` and `apps/api/src/routes/*.ts` for every
`app_private.list_overlay_*` call actually present and fails the build (exit 1, naming the
call site) if one is missing from the manifest. `check-plans.mjs` was changed to iterate the
manifest — requiring an artefact for every declared entry — instead of a directory listing
that only knew what already had a file, which is the literal mechanism this row's blind spot
exploited. `pnpm explain:check` now runs the scan then the plan check and reports
`15/15 plans current` (was 10/10).

**The negative case was exercised, not assumed.** `app_private.list_overlay_tug_of_war_vote`'s
manifest entry was removed; `pnpm explain:check` failed with
`RT-12 required-queries scan: 1 overlay-facing app_private call(s) missing from
packages/db/explain-plans/required-queries.json: - app_private.list_overlay_tug_of_war_vote
called at apps/api/src/db/vote-payment-sql-store.ts:132 has no manifest entry`; the entry was
restored and the check passed again (`15/15`).

**Two more gaps found and closed, beyond the two this update was scoped to.** Building the
scan honestly (general-purpose, not hand-tuned to the two PRF-02 functions) also found
`app_private.list_overlay_lottie_assets` (migration 0077) and
`app_private.list_overlay_widget_config` (migration 0105) — both predating PRF-02 entirely —
with no artefact either. Both are captured (`lottie-assets.explain.md`,
`widget-config.explain.md`) for the same reason the two named gaps are: a scan tuned to only
the functions already known about would repeat this exact failure one level up.

**Closed or narrowed — stated plainly, per this task's own instruction not to overclaim.**
**Narrowed, not fully closed.** The mechanism makes forgetting a *declared* function's
artefact structurally impossible — that specific failure (a widget-backing query shipping
with no plan and the check staying green) cannot recur for any function the scan can see.
What would still slip past it, named exactly rather than left implicit:

1. **A widget-backing function that does not follow the `list_overlay_*` naming convention.**
   The scan is a regex over that convention (every overlay-facing widget-snapshot function in
   this codebase happens to follow it, 13/13 at the time this was written), not a real
   call-graph analysis. `list_channel_master_canvas_modules` is already the proof this gap is
   real: it is in the manifest only because this task's own command named it explicitly, not
   because the scan would ever nominate a differently-named function. A future creator-facing
   or oddly-named overlay read would ship exactly as invisible to this scan as the original
   two PRF-02 functions were to the directory listing.
2. **A call reached only through indirection** (a function name built as a string, an alias,
   dynamic dispatch) — every call site in this codebase today is a literal
   `app_private.fn_name(` inside a tagged SQL template, so this is a theoretical gap, not an
   observed one, but it is real.
3. **Whether a caught function is genuinely production-scale-sensitive** is still a human
   judgement made once, at capture time — the scan is deliberately over-inclusive rather than
   under-inclusive, so it trades a possible extra artefact for never silently skipping one.

`packages/db/explain-plans/scan-required-queries.mjs`'s own header carries this same list, so
the caveat lives next to the mechanism it describes, not only in this record.

## Update 2026-09-16 — scan-convention-independence: the naming-convention gap closed

The gap named directly above — "A widget-backing function that does not follow the
`list_overlay_*` naming convention" — was found for real, by a direct measurement rather than
by further speculation: Opus enumerated every distinct `app_private.*` call in the seven
dedicated overlay-facing store files (`apps/api/src/db/{challenge-overlay-store,
goal-overlay-store, master-canvas-sql-store, overlay-audio-store, overlay-branding-store,
overlay-store, overlay-wakeup}.ts`). Twelve distinct functions are called there. Five were in
the manifest. **Seven were not**, none matching `list_overlay_*`:
`ack_overlay_cursor`, `can_access_channel`, `get_overlay_events`, `get_overlay_lottie_asset`,
`get_overlay_tts_audio`, `lookup_overlay_token`, `upsert_master_canvas_module`.

**`app_private.get_overlay_events` was the important one.** It is the alert stream itself —
the query `apps/api/src/db/overlay-store.ts`'s `replayRaw` runs on every overlay wake, for
every overlay session — the single hottest overlay read in the product, and it had no EXPLAIN
artefact. It does not follow the `list_overlay_*` convention because migration
`0127_v1_rt02_overlay_events_artifact_column.sql` had to `DROP FUNCTION` and
`CREATE FUNCTION` it (not `CREATE OR REPLACE`) to add an OUT column — PostgreSQL does not
permit `CREATE OR REPLACE FUNCTION` to change OUT columns — so it was never a candidate the
naming-convention scan could ever have nominated, regardless of how long it ran.

### What changed

**`packages/db/explain-plans/scan-required-queries.mjs` is now two-tier**, not
convention-only:

- **Rule 1 (unchanged):** every `app_private.list_overlay_*` call anywhere in
  `apps/api/src/db/*.ts` or `apps/api/src/routes/*.ts` must be in the manifest. Kept as a
  safety net for mixed-purpose files (e.g. `interaction-sql-store.ts`, which backs both
  creator-facing config routes and several `list_overlay_*` widget reads).
- **Rule 2 (new):** within files under `apps/api/src/db/` whose basename matches
  `/overlay|master-canvas/i` — the seven dedicated overlay-facing store files above, by a
  filename rule rather than a hard-coded path list, so an eighth overlay store (e.g.
  `overlay-chat-store.ts`) is caught automatically — **every** `app_private.<fn>(` call, any
  name, must be in the manifest **or** a new `exemptions` array in `required-queries.json`,
  where every entry carries a written reason. A call in neither fails the build, naming the
  call site, exactly as before.

**`packages/db/explain-plans/required-queries.json`** gained one manifest entry and six
exemptions, one classification each (not a blanket six-item sweep):

| Function | Manifested or exempt | Reason |
|---|---|---|
| `get_overlay_events` | **Manifested** — `overlay-events.explain.md` | Read serving the alert-stream surface; the hottest overlay read in the product |
| `lookup_overlay_token` | Exempt | Auth lookup — validates the bearer token, returns session/channel identity only, never widget-facing rows |
| `can_access_channel` | Exempt | Auth predicate (boolean) gating creator-facing session revoke/rotate writes, not a read that serves overlay content |
| `ack_overlay_cursor` | Exempt | Write — marks a delivery acknowledged, upserts a cursor row |
| `upsert_master_canvas_module` | Exempt | Write — creator-facing module toggle; the read it feeds (`list_overlay_master_canvas_modules`) is already manifested |
| `get_overlay_tts_audio` | Exempt | Single-row byte-serving fetch by artifact primary key (audio bytes for one delivery's TTS playback), not an aggregate/listing widget read |
| `get_overlay_lottie_asset` | Exempt | Single-row byte-serving fetch by artifact primary key; the enumerating list it complements (`list_overlay_lottie_assets`) is already manifested |

**`packages/db/explain-plans/check-plans.mjs`'s extraction regex was widened** from
`^create or replace function ` to `^create (?:or replace )?function ` — a byte-for-byte
extraction change was required to even capture `get_overlay_events`'s current body, since
0127's line is `create function app_private.get_overlay_events(`, not
`create or replace function`. Every other existing artefact's migration line still starts
with `create or replace function `, so this widening does not change any of their recorded
hashes — verified: `pnpm explain:check` still reports the other fifteen artefacts current,
unchanged.

**`packages/db/explain-plans/overlay-events.explain.md`** was captured against a throwaway
`postgres:16-alpine` container, roles + all 132 migrations applied in order, a synthetic
overlay session/channel/queue/binding/event/outbox/delivery seeded under the
`00000000-0000-4000-8000-0000000000e*` id range (unused by any other test file or artefact at
capture time), one `ready` delivery with a resolvable TTS artifact. Both the literal
wrapper-call EXPLAIN (opaque `Function Scan`, same reason as all fifteen other artefacts —
`get_overlay_events` is `security definer`) and the unwrapped-body EXPLAIN were captured. The
unwrapped plan for this function is fully resolved with **no** opaque inner `Function Scan`
node — unlike `goal`/`hype`/`leaderboard`/`top-supporters`, whose inner helpers are themselves
`security definer` and stay opaque, `get_overlay_events`'s two inner helper calls
(`current_overlay_session_id()`, `delivery_dispatch_allowed(...)`) are plain `language sql
stable` **without** `security definer`, so the planner inlines both — the first as a
`One-Time Filter`, the second into the delivery index scan's `Filter:` clause. Full detail in
the artefact itself.

**Negative cases exercised, not assumed**, as this task's own instruction required:

- Removed `get_overlay_events`'s manifest entry: `scan-required-queries.mjs` failed with
  `RT-12 required-queries scan: 1 overlay-facing app_private call(s) missing ... -
  app_private.get_overlay_events called at apps/api/src/db/overlay-store.ts:45 has no
  manifest entry (rule2-overlay-store)`. Restored; scan passed again (16 manifest entries).
- Added a call to a fabricated, unmanifested, unexempted function
  (`app_private.rt12_scan_test_probe_fn()`) inside `overlay-audio-store.ts`: the scan failed,
  naming that exact call site (`overlay-audio-store.ts:21`, `rule2-overlay-store`). Reverted
  immediately after; `git status`/`git diff` on that file confirmed clean, and the scan passed
  again.
- The six exempted functions are called throughout the seven overlay store files today and do
  **not** fail the scan — proven by the passing baseline run itself (16 manifest + 6 exemption
  entries, `OK`), not asserted separately.

**`pnpm explain:check` — `OK: ... (16 manifest entries, 6 exemptions)` then
`OK: 16/16 plans current`** (was 15/15). `pnpm db:test:all` — **59/0** (baseline 59/0,
unchanged — `get_overlay_events` already has extensive existing SQL coverage across
`l03_application_behavior.sql`, `l03_tts_fallback_and_amount_ladder.sql`,
`l07-mute-synthesis-cost-gate.sql`, `l07-mute-tts-enforcement.sql` and
`rt02_overlay_events_artifact_column.sql`; no new SQL test file was needed for functional
correctness, only the EXPLAIN artefact this record adds). `pnpm db:test:l03` — passed.
`pnpm --filter @bharatstudio/alerts-api build` — clean. `pnpm --filter @bharatstudio/alerts-api
test` — **585/0** (baseline 585/0, unchanged — no application code was modified, only the
scan/check scripts and the manifest). `git diff --check` — clean.

**Closed or narrowed — stated plainly.** **Closed for the specific defect measured**: every
`app_private` call in the seven dedicated overlay-facing store files named by this task is now
either manifested (with a captured artefact) or exempted (with a written reason); a call in
neither fails the build regardless of its name, proven by the negative-case test above.
**Narrowed, not eliminated, at the wider scope.** What can still slip past, named exactly:

1. **A genuinely overlay-facing function living in a file whose name matches neither
   `overlay` nor `master-canvas`, that also does not follow the `list_overlay_*` convention.**
   This is the direct descendant of the gap just closed, one level up: the dependency moved
   from a function-naming convention to a filename convention. A future store file named, say,
   `alert-stream-store.ts` would need either its name to match the rule or the rule itself
   extended — reviewed on the day it is added, not caught automatically.
2. **A call reached only through indirection** (a function name built as a string, a
   re-export invoked from a file rule 2 does not scan) — every call site in this codebase
   today is a literal `app_private.fn_name(` inside a tagged SQL template in a file one of the
   two rules covers, so this remains a theoretical gap, not an observed one.
3. **Whether a function is genuinely a "read that serves a surface" versus exempt-worthy is a
   human judgement**, made once per function at classification time (this record's table
   above), not machine-verified. A future exemption entered without genuine justification
   would pass the scan silently; the written-reason requirement makes that a reviewable
   decision, not a technical guarantee.

`packages/db/explain-plans/scan-required-queries.mjs`'s own header carries this same
three-item list, so the caveat lives next to the mechanism it describes, not only in this
record. Full classification reasoning:
`reviews/2026-09-16-rt-12-scan-convention-independence.md`.

## Independent Opus verification of the convention-independence fix — 2026-09-16

Both tiers negative-tested rather than trusted, and the extraction-failure path checked for a
third hole.

- `pnpm explain:check` — scan OK, **16/16 plans current** (15/15 before).
  `pnpm db:test:all` — 59/0. `pnpm --filter @bharatstudio/alerts-api test` — 585/0.
  `python3 tools/doc_consistency.py` — 17 checks, 0 errors, 0 warnings.
- **Tier 2 negative test, run by Opus:** a fabricated `app_private.opus_fabricated_widget_read(`
  call added to `overlay-branding-store.ts` — a name that breaks the `list_overlay_*`
  convention entirely — failed the scan naming `overlay-branding-store.ts:30`, the rule that
  caught it (`rule2-overlay-store`), and **both** remediations (manifest with an artefact, or
  exemption with a written reason). Reverted; `git status` confirms the file is clean.
- Six exemptions, each carrying a real reason: two auth lookups, two writes, two single-row
  byte-serving fetches by primary key. None of them is a read that serves a surface.

**A possible third blind spot, checked and absent.** `check-plans.mjs`'s extraction regex had
to widen from `^create or replace function` to `^create (?:or replace )?function`, because
migration `0127` defines `get_overlay_events` with a drop-and-create — a `CREATE OR REPLACE`
cannot change a `returns table` shape. The question that matters is what the checker did
before that, when it could not extract a body: it **pushes an error** (`could not locate
current body of …`) rather than skipping the entry, so this would have failed loudly. It was
a real limitation, not a silent pass.

**Still narrowed, not eliminated, and the boundary is stated.** A function in a file matching
neither `overlay` nor `master-canvas`, which also breaks the `list_overlay_*` convention,
still slips past. That is written into the scan's own header and the review record rather
than left to be discovered. RT-12 stays **P**.

**What this is not.** The plans remain plan-shape change detectors captured on an unsized
local database. None is evidence that any §19.4 budget is met, and `get_overlay_events`
having a plan says nothing about its behaviour at §37.4's sizes. RT-07 is Blocked.

## Correction, 2026-09-16 — scan blind spot closed (rule 3, composition-root scan)

**Owner:** Sukhdev Singh. **Local verification only — not production evidence and not
performance evidence.** No database was touched: rule 3 is an offline source scan. No §19.4
budget is claimed or measured, nothing ran against §37.4's production-scale dataset, and every
plan artefact keeps its §35.1 rule 6 disclosure. RT-07 remains Blocked.

**What changed.** `packages/db/explain-plans/scan-required-queries.mjs` gains **rule 3**, a
composition-root scan that consults no function name and no file name. It starts at
`apps/api/src/index.ts` and `apps/api/src/app.ts`, finds every call whose argument list
contains the `derivedReadSql` token — the single handle to RT-10/RT-11's bounded,
`statement_timeout`-bearing derived-read pool that every widget/dashboard/analytics read is
required to run on — resolves each callee through that file's own `import` statements,
brace-matches the named export's body, and requires every `app_private.<fn>(` inside it to be
manifested or exempted. Nine wired declarations resolve today: eight store factories in
`index.ts` and `registerInteractionRoutes` in `app.ts`. Resolution failures (missing import,
missing export, unbalanced braces, or zero wirings found) exit non-zero rather than printing
`OK`. Rule 1 and rule 2 are unchanged and still run.

**Newly discovered and resolved.** Three calls, all creator-dashboard reads sharing the
derived-read pool: `list_channel_payments`, `get_channel_revenue_kpis`,
`get_creator_activation_state`. All three **exempted with routing + signature + body
evidence** (which registrar reaches them, whether an overlay id / token fingerprint / 
`overlay_sessions` join appears in the migration definition, and RT-12's own Boundaries
assigning the dashboard surface to PRF-11 §31.18.1) — full reasons in
`required-queries.json`. No blanket exemption, no wildcard. Manifest stays 16; exemptions go
6 → 9.

### Negative test — three runs, verbatim

Temporary store file `apps/api/src/db/alert-stream-snapshot-sql-store.ts` (path matches
neither `overlay` nor `master-canvas`), calling the unmanifested
`app_private.read_alert_stream_snapshot(`, wired exactly as a real overlay store is wired —
`alertStreamSnapshots: sql ? createSqlAlertStreamSnapshotStore(derivedReadSql!) : undefined,`
in `apps/api/src/index.ts`.

**1 — OLD scan (`git show HEAD:…/scan-required-queries.mjs`), temporary store present. PASSES,
proving the blind spot was real:**

```
### NEGATIVE TEST 1 -- OLD scan, temporary store present ###
OK: every app_private call found by the convention scan and the overlay-store-file scan is present in required-queries.json (16 manifest entries, 9 exemptions)
exit=0
```

**2 — NEW scan, same temporary store present. FAILS:**

```
### NEGATIVE TEST 2 -- NEW scan, same temporary store present ###

> @bharatstudio/alerts@0.1.0 explain:check /Users/sukhdevsingh/Workspace/Bharat Studio/bharatstudio-alerts/.claude/worktrees/agent-a6c48453cfe33a8da
> node packages/db/explain-plans/scan-required-queries.mjs && node packages/db/explain-plans/check-plans.mjs

RT-12 required-queries scan: 1 overlay-facing app_private call(s) missing from packages/db/explain-plans/required-queries.json:
  - app_private.read_alert_stream_snapshot called at apps/api/src/db/alert-stream-snapshot-sql-store.ts:15 has no manifest entry (rule3-composition-root(apps/api/src/index.ts -> createSqlAlertStreamSnapshotStore)) -- add it to required-queries.json's "queries" array with a captured EXPLAIN artefact, or to its "exemptions" array with a written reason, before this can pass
 ELIFECYCLE  Command failed with exit code 1.
 WARN   Local package.json exists, but node_modules missing, did you mean to install?
exit=1
```

**3 — temporary file deleted, `index.ts` wiring reverted. PASSES again:**

```
### NEGATIVE TEST 3 -- temporary store deleted, wiring reverted ###

> @bharatstudio/alerts@0.1.0 explain:check /Users/sukhdevsingh/Workspace/Bharat Studio/bharatstudio-alerts/.claude/worktrees/agent-a6c48453cfe33a8da
> node packages/db/explain-plans/scan-required-queries.mjs && node packages/db/explain-plans/check-plans.mjs

OK: every app_private call found by rule 1 (convention scan), rule 2 (overlay-store-file scan) and rule 3 (composition-root derived-read scan, 9 wired declaration(s) resolved and scanned) is present in required-queries.json (16 manifest entries, 9 exemptions)
OK: 16/16 plans current
exit=0
```

Note on run 1's counts: the old scan reads the *current* `required-queries.json`, which is why
it already reports 9 exemptions. That does not weaken the result — the temporary store's
function is in neither the manifest nor the exemptions, and the old scan still printed `OK`.

Cleanup verified: `git status --porcelain` after run 3 shows only
`M packages/db/explain-plans/required-queries.json` and
`M packages/db/explain-plans/scan-required-queries.mjs`. The temporary store file, the
temporary `index.ts` import and wiring line, and the temporary copy of the old scan are all
gone.

### Still not caught — stated, not hidden

Item 1 of the previous list is now **closed**: a store file matching neither naming rule is
caught the moment it is wired to `derivedReadSql`, whatever it or its file is called. What
replaces it is narrower and is written into the scan's own header: a derived read wired to the
**main `sql` pool** instead of `derivedReadSql`, in a file matching neither naming rule, is
still invisible to all three rules — though such a read is already a live RT-10/RT-11
violation caught by those rows' own review. Items 2 (indirection) and 3 (the human judgement
inside every exemption) are unchanged and still open.

RT-12 stays **P**; status unchanged (`Conditionally complete — local implementation and
verification; independent review unavailable`). No migration, API route, OpenAPI contract or
Go service was touched.
