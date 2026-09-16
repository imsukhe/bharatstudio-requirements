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
