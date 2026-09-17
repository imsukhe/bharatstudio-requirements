# SAF phase 1 — moderation pipeline spine: implementation record

**Date:** 2026-09-17
**Owner:** **Sukhdev Singh**
**Authority:** `../FULL-PRODUCT-DEFINITION.md` §12.2, §12.6, §12.6.2, §12.10, §11.3, §31.13.2 rows
SAF-01/SAF-02/SAF-04/SAF-05/SAF-09
**Task:** `../active/tasks/SAF-01-moderation-pipeline-spine.md`
**Acceptance:** `../tests/TC-SAF-01-moderation-pipeline-spine.md`
**Predecessor:** none — verified at 45-of-46 SAF rows absent before this task, the only existing
artefact being a decorative, never-read `ModerationRule` enum
(`apps/api/src/domain/interaction-types.ts`)

---

## What phase 1 is, in one paragraph

Migration `0151` adds one subsystem — a corpus table (empty by default), a generation counter, and
an evidence-snapshot table — plus a TypeScript pipeline (`apps/api/src/domain/aho-corasick.ts`,
`safety-pipeline.ts`) that normalises text and matches it against the corpus, producing an
independent decision per surface. It is deliberately narrow: it does not wire into any live
surface, does not build L2-L4 matching, PII detection, URL neutralisation, SSML guarding, rate
limiting or policy presets, and ships zero corpus content.

## Why the pipeline logic lives in TypeScript, not SQL

The task asks for a first-party Aho-Corasick implementation and named this as SAF-05's mechanism.
Aho-Corasick's natural implementation is a trie with failure links over in-memory strings — doable
in PL/pgSQL only through contorted recursive CTEs with no real performance benefit, whereas a
straightforward class in application code is both simpler and matches how this pipeline will
eventually run (in-process, on every message, before any provider call). The corpus itself —
`safety_corpus_terms` — stays server-side truth: `bsa_app` has no direct grant on it at all, so
the ONLY way the TypeScript layer can ever obtain corpus terms is
`app_private.get_safety_corpus_terms`, a SECURITY DEFINER function. This is the identical
structural technique migration `0149` (CTL-03) used for "never per-capability queries", adapted
here to "never a second corpus read path" — which is also SAF-01's own database-side guard: a
hypothetical second matching implementation cannot read the corpus directly even if someone wrote
one, because there is no grant path to do so.

The consequence, stated rather than hidden: SAF-01's "one pipeline" guarantee is enforced by TWO
independent mechanisms at two different layers — a database grant (stops a second implementation
from ever reading the corpus) and a source-tree scan in
`apps/api/test/safety-pipeline.test.ts` (stops a second implementation from ever being written in
application code, whether or not it would have read the corpus). Neither one alone would be a
complete guarantee — the database grant does not prevent someone from hand-rolling matching logic
against a hardcoded string list, and the source scan does not prevent a second corpus table from
being created — so both were built.

## Normalisation scope — narrower than the register's fuller SAF-02 text, on purpose

FULL-PRODUCT-DEFINITION.md §12.2.2's SAF-02 text additionally lists homoglyph folding, leet/
separator folding, repeated-character collapse and script transliteration. The task record that
dispatched this phase restated SAF-02 more narrowly — NFKC, zero-width/RTL-override stripping,
combining-mark handling — and that narrower text is what was built. This was a deliberate reading,
not an oversight: homoglyph/leet folding without a phonetic layer behind it risks new false
positives (`assist` colliding with a folded form of something else) that SAF-03's phonetic keys
are the actual answer to, and building it now would be building half of SAF-03 under SAF-02's
name. The gap is recorded here, in the task record, and in the migration's own header — not
silently absorbed into "done".

## Case-folding — an engineering necessity, documented as distinct from the register's own bullets

L1 exact matching over a corpus of creator/staff-typed terms needs a canonical case, or it misses
nearly every real-world match (a term typed in Title Case would never match lowercase chat text).
This is not one of §12.2.2's four named SAF-02 sub-requirements, and is not a numeric limit, price,
provider behaviour, legal wording or retention window, so it does not fall under this task's
"never invent" constraint — but it is called out explicitly in `safety-pipeline.ts`'s own comment
so a future reader never mistakes it for a §31 requirement in its own right.

## SAF-09's decision vocabulary — reused, not invented

`allow / mask / hold / block` is FULL-PRODUCT-DEFINITION.md §12.2.1's own pipeline diagram
vocabulary, reused verbatim rather than invented. `moderator_review`'s `allow / hold` ("queued for
a human or not") is §12.2.4's own phrasing. `payment` and `stored_record` are not decision fields
a term can set at all — they are database CHECK-constrained to the single value `'allow'`, which
is the strongest available proof that "money is never affected by content" and "an actioned
message is always stored in full" (§12.2.4) are guarantees of the schema, not of application
discipline. A direct SQL `INSERT` attempting `payment_decision = 'block'`, bypassing the
`record_safety_moderation_action` function entirely, is still rejected — proven in
`packages/db/tests/saf_pipeline_spine.sql`.

## Retention — why no row is ever written for an unactioned message

§12.10: *"snapshot the evidence at action time, do not retain the firehose."* §12.6.2 classifies
raw chat/message logs as the shortest retention class, whose window is set by a privacy/legal gate
still Open in `active/launch/05_SUPPORT_AND_EXTERNAL_EVIDENCE_REGISTER.md` — so no honest window
exists to apply, the same situation §12.6.2.1 resolved for reaction sends (migration `0141`) by
simply not writing the row. The identical lever is applied here: `safety_moderation_actions` is
written ONLY when `runSafetyPipeline` produces a match (a clean message's decision is
`allow`/`allow`/`allow`/`allow`/`allow` by construction, and the application layer has nothing to
record for it). The table itself enforces this independently of application discipline:
`matched_term_ids` requires `coalesce(array_length(matched_term_ids, 1), 0) >= 1` — an empty or
NULL array is rejected, so there is no way to construct a "message reviewed, nothing matched" row
even by accident. This check constraint had a real, caught defect during implementation:
`array_length(ARRAY[]::uuid[], 1)` returns SQL `NULL`, not `0`, and an uncoalesced
`>= 1` comparison against `NULL` is neither true nor false — PostgreSQL treats a `NULL` `CHECK`
result as satisfied, which would have silently ACCEPTED an empty array. Caught by the SQL test
itself (the expected-`check_violation` assertion failed because the forbidden insert succeeded),
fixed with `coalesce(..., 0)`, re-verified.

## Corpus management scope

Creator-facing: list (global + own), create (own channel, owner/admin), delete (own channel's own
term, owner/admin). No update — a term is deleted and re-added rather than edited in place, which
keeps the generation-bump-on-any-write mechanism simple. Global-corpus management
(`channel_id` null) is a data-layer primitive only (`app_private.create_safety_corpus_term`
already supports it, staff-gated) with no HTTP route in this phase — the identical CTL-04
admin-UI deferral migration `0149` established, reused rather than re-litigated.

## `apps/api/src/db/safety-corpus-store.ts` — two pools in one file, and why

Every other dual-pool surface in this codebase splits into two files (a creator-facing store on
the main `sql` pool, an overlay-facing store on `derivedReadSql`). This store has no overlay
counterpart to split into — it is corpus management, not an overlay-rendered widget — so `list()`
(the read) and `create()`/`remove()` (writes) share one file, with `list()` wired to
`derivedReadSql` (RT-10/RT-11's bounded, statement-timeout-bearing pool, appropriate for a
dashboard-style corpus read) and the two writes on the main pool. The consequence, found and
handled rather than avoided: `packages/db/explain-plans/scan-required-queries.mjs`'s rule 3 scans
the WHOLE factory function body once it sees `derivedReadSql` in the composition root's call —
sweeping `create_safety_corpus_term` and `delete_safety_corpus_term` (both plain writes) into the
same manifest requirement as the read. Both were added to `required-queries.json`'s `exemptions`
array with a written reason (a write, not a widget-backing read) rather than manifested with an
EXPLAIN artefact they do not need — the same mechanism the codebase already uses for exactly this
class of case (`app_private.can_access_channel`'s own exemption entry is the direct precedent).

## Explain-plan artefact

`packages/db/explain-plans/safety-corpus-terms.explain.md` captures
`app_private.get_safety_corpus_terms` against a real `postgres:16-alpine` container: two calls (a
cold and a warm read) over a two-row seed, showing the usual opaque `Function Scan` wrapper over a
`Seq Scan` at this row count. Captured even though nothing routes this read through an overlay
session — the task's own instruction requires the artefact regardless, the identical posture
`capability-resolution.explain.md` already recorded for `app_private.get_channel_capabilities`.

## Scope held

Nothing in this phase touches `apps/web/app/overlay/canvas/`, any `CTL-*`/`GOA-*` record, or
migrations `0149`/`0150` — confirmed by `git status`/`git diff` against base `849bb02` showing
zero changes to any of those paths. No slur, profanity or otherwise-forbidden content was written
anywhere — the corpus ships with zero rows, and every test term used throughout
(`zzz_channel_a_term`, `rt12_global_term`, etc.) is a synthetic placeholder chosen specifically to
be inert.

## What is deliberately NOT done, restated

- `SAF-03`/`SAF-06`/`SAF-07`/`SAF-08` (phonetic keys through L4 AI) — not built.
- `SAF-10`-`SAF-14` (URL neutralisation, SSML guard, PII detection, rate/flood control, policy
  presets) — not built.
- No live surface (TTS, payment, chat, alert) calls `runSafetyPipeline`. A grep across
  `apps/api/src` for callers of that function outside its own test file returns zero results.
- No corpus content.

Wiring the pipeline onto a live surface is a separate task with its own record, per the task's own
instruction — building the plane and switching a live surface onto it in the same change would
make a failure impossible to attribute to one or the other.

## Verified numbers (see the acceptance record for the full command table)

sql 75/0 (baseline 74/0) · api 808/0 (baseline 790/0, +18 new) · web 644/0 (unchanged) ·
typecheck 0/0 · contracts: 67 fixtures, 109 paths, 127 operations (baseline 63/107/124) ·
explain 28/28 (baseline 27/27) · harness pass · canvas subscriber count untouched (zero diff to
`apps/web/app/overlay/canvas/`).
