# TC-SAF-01 — moderation pipeline spine, phase 1: acceptance record

**Date:** 2026-09-17
**Owner:** **Sukhdev Singh**
**Task:** `../active/tasks/SAF-01-moderation-pipeline-spine.md`
**Decision:** `../reviews/2026-09-17-saf-phase-1-implementation.md`
**Authority:** `../FULL-PRODUCT-DEFINITION.md` §12.2, §12.6, §12.6.2, §12.10, §11.3, §31.13.2 rows
SAF-01/SAF-02/SAF-04/SAF-05/SAF-09

Written to accompany implementation, per `governance/AGENTS.md`. The "Commands run" table is
filled in from actual output against a real `postgres:16-alpine` container and a real `tsx --test`
run, and is the single place this phase's numbers live.

---

## Acceptance criteria

### A. SAF-01 — one corpus, one pipeline, structurally

| ID | Criterion |
|---|---|
| SAF01.1 | Exactly one corpus table (`safety_corpus_terms`) backs every surface — no second corpus table or content store exists anywhere in this migration |
| SAF01.2 | `bsa_app` has NO SELECT/INSERT/UPDATE/DELETE grant on `safety_corpus_terms`, `safety_corpus_generation` or `safety_moderation_actions` — revoked from both `public` and `bsa_app` — the only reachable read path is `app_private.get_safety_corpus_terms` |
| SAF01.3 | **Behavioural**: connecting as `bsa_app` and attempting a direct `SELECT` on the corpus or evidence tables raises `insufficient_privilege` |
| SAF01.4 | Exactly one L0 normalisation function exists in the TypeScript source tree (`normalizeForSafetyMatching`, `apps/api/src/domain/safety-pipeline.ts`) — a source scan fails the build if `.normalize(` appears anywhere else unexempted |
| SAF01.5 | Exactly one Aho-Corasick implementation exists (`apps/api/src/domain/aho-corasick.ts`) — a source scan fails the build if the identifier `AhoCorasick` appears anywhere outside that file and its one caller |
| SAF01.6 | `runSafetyPipeline` (`apps/api/src/domain/safety-pipeline.ts`) is the one exported entry point that normalises and matches — it is surface-agnostic (takes text + corpus, not a surface name), so tips/TTS/chat/display names would all call the same function once wired |

### B. SAF-02 — L0 normalisation (NFKC, zero-width/RTL-override stripping, combining-mark handling)

| ID | Criterion |
|---|---|
| SAF02.1 | Unicode NFKC is applied |
| SAF02.2 | Zero-width characters (U+200B-D, U+FEFF) are stripped from the matching form |
| SAF02.3 | RTL/LTR override characters (U+202A-E, U+2066-9) are stripped from the matching form |
| SAF02.4 | Combining marks (Zalgo floods) are stripped from the matching form |
| SAF02.5 | Case-folding is applied as a documented engineering necessity for L1 exact matching, explicitly distinguished from the four §12.2.2-named sub-requirements above |

### C. SAF-04 — the original is never destroyed

| ID | Criterion |
|---|---|
| SAF04.1 | `runSafetyPipeline`'s result always carries `original` exactly as given, on both the matched and unmatched result shapes |
| SAF04.2 | The normalised form is a **separate** field (`normalized`), never written back over `original` |
| SAF04.3 | `safety_moderation_actions.original_text` and `.normalised_text` are independent `NOT NULL` columns — structurally impossible for a row to carry one without the other |
| SAF04.4 | **Behavioural**: a message whose normalised form visibly differs from its original (zero-width characters removed) persists BOTH forms exactly as given, byte for byte, in a real database |
| SAF04.5 | **Structural**: `information_schema.columns` confirms both columns are `NOT NULL` |

### D. SAF-05 — L1 Aho-Corasick, global plus per-creator, whole-word aware

| ID | Criterion |
|---|---|
| SAF05.1 | `app_private.get_safety_corpus_terms` returns global terms (`channel_id` null) UNION this channel's own terms, in one call |
| SAF05.2 | A channel-owned term never leaks to a different channel — proven with two isolated channels |
| SAF05.3 | Whole-word matching does not match inside a longer, unrelated word (`assist` does not match inside `assistant`) |
| SAF05.4 | Substring matching (whole_word = false) matches inside a longer word by design |
| SAF05.5 | The automaton matches multiple patterns in one pass (multi-pattern Aho-Corasick, not N separate scans) |
| SAF05.6 | The automaton is first-party — no third-party dependency was added for it |

### E. SAF-09 — per-surface decisions

| ID | Criterion |
|---|---|
| SAF09.1 | The decision type carries five independent fields: payment, display, TTS, stored record, moderator review |
| SAF09.2 | `payment` is **always** `'allow'`, regardless of any match — never derived from a corpus term |
| SAF09.3 | `stored_record` is **always** `'allow'` on a row that exists at all — an actioned message is always stored in full |
| SAF09.4 | `display` and `tts` can differ from each other on the SAME text, in the SAME pipeline run |
| SAF09.5 | **Database-structural**: `safety_moderation_actions.payment_decision` and `.stored_record_decision` are `CHECK`-constrained to the single value `'allow'` — attempting any other value raises `check_violation` |
| SAF09.6 | `record_safety_moderation_action`'s parameter list has no `target_payment_decision` or `target_stored_record_decision` IN parameter at all — a caller cannot even attempt to set either |
| SAF09.7 | When multiple corpus terms match, the most severe decision wins per surface independently |

### F. Corpus empty by default

| ID | Criterion |
|---|---|
| CORPUS.1 | This migration inserts **zero** rows into `safety_corpus_terms` |
| CORPUS.2 | A fresh channel's corpus read returns zero rows before any insert |
| CORPUS.3 | `runSafetyPipeline` with an empty corpus array always returns `matched: false`, for any input text |
| CORPUS.4 | The Aho-Corasick automaton with zero patterns matches nothing, for any input |
| CORPUS.5 | No slur, profanity or otherwise-forbidden content appears anywhere in the migration, the seed data, or the tests |

### G. Retention (§12.10/§12.6.2.1) — raw unactioned text is never stored

| ID | Criterion |
|---|---|
| RET.1 | `safety_moderation_actions.matched_term_ids` requires at least one element (`coalesce(array_length(...), 0) >= 1`) — there is no way to insert an evidence row for a message that matched nothing |
| RET.2 | An empty array and a NULL array are both rejected |
| RET.3 | `policy_version` is read from `safety_corpus_generation` INSIDE `record_safety_moderation_action` — not a caller-supplied argument, verified against `information_schema.parameters` |
| RET.4 | A corpus write strictly advances the generation counter, and the next evidence row records the new value |

### H. Corpus management — store and routes

| ID | Criterion |
|---|---|
| CM.1 | `GET /v1/channels/:channelId/safety/corpus-terms` returns global + own terms for an authenticated member |
| CM.2 | `POST /v1/channels/:channelId/safety/corpus-terms` creates a channel-owned term — owner/admin only |
| CM.3 | `DELETE /v1/channels/:channelId/safety/corpus-terms/:termId` removes a channel-owned term only — a global or another channel's term is a 404, not a different error shape |
| CM.4 | A viewer/operator cannot create or delete a corpus term (`42501`/`insufficient_privilege` at the database layer, mapped to 404 at the route layer to avoid membership enumeration) |
| CM.5 | An ordinary channel owner cannot create a GLOBAL term — staff only, and there is no HTTP route for it in this phase |
| CM.6 | A store failure degrades to a retryable 503 on every route, never a crash; an unwired store is 503-safe |
| CM.7 | An invalid `channelId`/`termId`/decision-enum value is rejected 400 at the schema layer before the store is ever called |

### I. Scope discipline held

| ID | Criterion |
|---|---|
| SCOPE.1 | Nothing in `apps/api/src/domain/safety-pipeline.ts` or the migration is called from any TTS, payment, chat or alert route — `runSafetyPipeline` has zero callers outside its own tests |
| SCOPE.2 | `apps/web/app/overlay/canvas/` is untouched |
| SCOPE.3 | `CTL-*`/`GOA-*` records and migrations `0149`/`0150` are untouched |
| SCOPE.4 | No corpus content (slur lists, seed terms) was invented |

---

## Commands run

| Command | Result |
|---|---|
| Base fix (`git reset --hard 849bb02`) | Applied; worktree confirmed at `849bb02 GOA-01/02/03: a refund could un-complete a goal, and now cannot` |
| Full SQL suite (`sh packages/db/tests/run-sql-suite.sh`, 75 files incl. this phase's own `saf_pipeline_spine.sql`), real `postgres:16-alpine` container | pass=75 fail=0 (baseline 74/0) |
| `apps/api` route/unit suite (`tsx --test apps/api/test/**/*.test.ts`) | tests 808, pass 808, fail 0 (baseline 790/0; +18, all new: `safety-pipeline.test.ts` (10), `safety-corpus-routes.test.ts` (8)) |
| `apps/web` suite | tests 644, pass 644, fail 0 (baseline 644/0, unchanged — no web files touched) |
| `apps/api` TypeScript typecheck (`tsc -p tsconfig.json --noEmit`, separate from the test runner) | 0 errors |
| `apps/web` TypeScript typecheck (`tsc --noEmit -p tsconfig.json`) | 0 errors |
| `node contracts/validate-fixtures.mjs` | Validated 67 fixtures plus the v1 template catalogue contract (baseline 63) |
| `node contracts/validate-openapi.mjs` | Validated OpenAPI 3.1 document with 109 paths, 127 operation contracts (baseline 107/124) |
| `node contracts/test-openapi-validator.mjs` | Validated 3 negative OpenAPI operation-contract cases |
| `node packages/db/explain-plans/scan-required-queries.mjs` | OK, 28 manifest entries, 11 exemptions (baseline 27/9) |
| `node packages/db/explain-plans/check-plans.mjs` | OK: 28/28 plans current (baseline 27/27) |
| `pnpm harness:check` (`node .github/scripts/api-test-harness-check.mjs`) | all checks passed; 39 files reference `createTestFastify` (`safety-corpus-routes.test.ts` uses it directly, the same shape `l16-goals-routes.test.ts` uses) |

**Not run:** `go test`/`go vet` on the three Go services, `pnpm build`, Docker image builds, and
`scripts/load/*` self-tests — none of this phase's files touch Go services or change build output
shape. `pnpm test`'s `measurement:test` sub-step was not separately re-verified in this run beyond
the `apps/api`/`apps/web` sub-steps `pnpm test` actually exercises (both recorded above); per the
dispatching task's own instruction, an agent-sandbox failure of that specific sub-step is a known
pre-existing environmental gap (see `TC-CTL-01-capability-control-plane.md`'s own identical note),
not something this phase's files could affect (`scripts/measurement/` has no diff against base
commit `849bb02`).

## SAF-04 — the mechanism and the test that fails if the original is overwritten

Mechanism: `runSafetyPipeline`'s result type always carries `original` as a field distinct from
`normalized` (JS strings are immutable, so `normalizeForSafetyMatching` cannot mutate its input —
it can only return a new string). Durably: `safety_moderation_actions.original_text` and
`.normalised_text` are two independent `NOT NULL` columns with no shared upstream "text" column
that could be normalised in place. Test:
`apps/api/test/safety-pipeline.test.ts`'s `"SAF-04: runSafetyPipeline always returns the exact
original text, untouched..."` (TypeScript layer) and
`packages/db/tests/saf_pipeline_spine.sql`'s SAF-04 behavioural block (database layer, real
`INSERT`/`SELECT` round trip proving byte-for-byte persistence of both forms).

## SAF-09 — the type and the test proving two surfaces decide differently

Type: `SafetyPerSurfaceDecision` (`apps/api/src/domain/safety-pipeline.ts`) — `payment` and
`storedRecord` are TypeScript literal-typed to `'allow'` (cannot even be assigned another value at
compile time); `display`, `tts` are `SafetyDecisionValue` (`allow|mask|hold|block`);
`moderatorReview` is `allow|hold`. Test:
`apps/api/test/safety-pipeline.test.ts`'s `"SAF-09: per-surface decisions are independent..."`
(asserts `display !== tts` on one matched result) and
`packages/db/tests/saf_pipeline_spine.sql`'s SAF-09 behavioural block (one evidence row with
`display_decision = 'mask'` and `tts_decision = 'block'` on the same row).

## SAF-01 — how a second matching implementation is prevented, and the test that catches it

Database layer: `bsa_app` has no grant on any of the three tables this migration creates —
enforced by `REVOKE`, proven behaviourally in `packages/db/tests/saf_pipeline_spine.sql` (connect
as `bsa_app`, attempt `SELECT`, expect `insufficient_privilege`). Application layer:
`apps/api/test/safety-pipeline.test.ts` scans every file under `apps/api/src` and fails if
`.normalize(` (L0) or the identifier `AhoCorasick` (L1) appears anywhere outside the one file each
belongs to, with one written, cited exemption for a pre-existing, unrelated call
(`apps/api/src/tts/provider.ts`'s `sanitizeTtsText`, confirmed by reading it — a technical
transport-safety filter, not a safety-matching implementation).
