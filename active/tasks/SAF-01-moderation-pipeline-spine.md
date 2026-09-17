# SAF phase 1 — the moderation pipeline spine

**Status:** `Approved for implementation — phase 1 dispatched 2026-09-17`
**Owner:** Sukhdev Singh
**Authority:** `../../FULL-PRODUCT-DEFINITION.md` §31.13.2 register rows `SAF-01`, `SAF-02`, `SAF-04`,
`SAF-05`, `SAF-09` · §12.2 (content safety, one pipeline every surface) · §11.3 (live safety and
moderation) · §12.10 (evidence and retention for moderation actions) · §12.6/§12.6.2/§12.6.2.1
(durable creator records, uniform retention, and the reaction-send precedent for the shortest
retention class)
**Predecessor:** none — SAF is 45-of-46 absent (verified before dispatch: a repo-wide search
found zero matches for corpus, Aho-Corasick, phonetic, homoglyph, PII, SSML or `policy_version`).
The only moderation-shaped thing anywhere in the product is `apps/api/src/domain/interaction-types.ts`'s
`ModerationRule` enum (`'none'|'review'|'block_list'`), stored and never read — decorative, not a
pipeline.

## Why this is the foundation, not an extension

§12.2's own current-state note: *"`provider.ts:28-29` strips C0/DEL control characters and bounds
to 500 characters. That is the entire filter."* Everything else — corpus, normalisation, matching,
per-surface decisions, evidence — does not exist. This task builds the spine five rows can stand
on; it does not extend anything that was there before.

## Phase 1 scope — five rows, deliberately not the whole register

`SAF-01` · `SAF-02` · `SAF-04` · `SAF-05` · `SAF-09`. Migration **`0151`**.

| Row | What it requires |
|---|---|
| `SAF-01` | **One corpus, one pipeline, every surface** — tips, TTS, chat, display names all go through the same path |
| `SAF-02` | **L0 normalisation**: NFKC, zero-width and RTL-override stripping, combining-mark handling |
| `SAF-04` | **Original text is never destroyed** — normalisation produces a PARALLEL matching form |
| `SAF-05` | **L1 Aho–Corasick** over the compiled corpus, global plus per-creator, whole-word aware |
| `SAF-09` | **Per-surface decisions** — payment, display, TTS and stored record can decide differently on the same text |

### The two load-bearing guarantees

- **`SAF-04` — the original is evidence.** §12.10 requires an evidence snapshot at action time:
  original text, normalised form, matched rule, layer, confidence, policy version, actor. A
  pipeline that destroys the original cannot satisfy that, ever — normalisation must produce a
  parallel matching form alongside the original, never overwrite it, made structurally impossible
  to violate and proven with a test.
- **`SAF-09` — one verdict per surface, not one verdict.** The same message can be fine to store,
  fine to display, and wrong to synthesise aloud. The decision type must carry a decision **per
  surface**, not a single boolean callers reinterpret.
- **`SAF-01` — one pipeline, structurally.** If two call sites normalise or match differently, the
  guarantee is gone. The single path must be structural — one entry point, and a test that fails
  if a second matching implementation appears.

## What this phase deliberately does NOT build

- `SAF-03` (Indic phonetic keys), `SAF-06` (L2 edit distance), `SAF-07` (L3 local classifier),
  `SAF-08` (L4 AI), `SAF-10` (URL neutralisation), `SAF-11` (SSML-injection guard), `SAF-12` (PII
  detection), `SAF-13` (rate/flood control), `SAF-14` (policy presets). Later lanes; several need
  decisions that do not exist yet.
- Homoglyph folding, leet/separator folding and repeated-character collapse — present in the
  register's fuller `SAF-02` text, but this task's own scope narrows `SAF-02` to NFKC,
  zero-width/RTL-override stripping and combining-mark handling only. The wider evasion
  techniques overlap `SAF-03`'s phonetic-key territory and are deferred to whichever lane builds
  `SAF-03`/`SAF-06`, recorded here rather than silently dropped.
- **Not wired into any live payment, TTS, chat or alert path.** The pipeline is built and proven
  in isolation. Switching a live surface onto it is a separate task with its own record, so a
  failure is attributable to one change, not two at once.
- **No corpus content.** A slur list is content, not code, and nobody has decided it. The corpus
  ships empty — this migration inserts zero rows — and empty means "matches nothing", never
  "match everything" and never a guessed starter list.

## Constraints

- Never invent a numeric limit, price, provider behaviour, legal wording, retention window or
  deployment value. Reuse a decided value and cite file:line, or ship configured-but-unset. (The
  500-character evidence-text bound is reused verbatim from
  `packages/db/migrations/0006_v1_l04_payment_order_intents.sql:36`'s `donor_message` check.)
- **Retention**: §12.10 — *"snapshot the evidence at action time, do not retain the firehose."*
  Raw unactioned text belongs to §12.6.2's shortest retention class, whose window is set by a
  privacy/legal gate that is still Open. So raw unactioned text is never stored at all — the same
  reasoning §12.6.2.1 already applied to reaction sends (migration `0141`).
- Privacy as a property of the query; assert exact returned column sets in SQL tests.
- Route tests use the shared `createTestFastify()`; never construct Fastify directly.
- Do not touch `apps/web/app/overlay/canvas/`, `CTL-*`/`GOA-*` records, or migrations
  `0149`/`0150`.
- Migration number `0151` and fixture UUID range `...6b00-...6bff` were pre-assigned by the
  coordinator (two concurrent lanes ran alongside this one in separate worktrees, on migrations
  `0149` and `0150`).

## Phase 2 — deliberately not this task

Wiring the pipeline onto a live surface (TTS first, per §12.2.6's fail-closed-for-speech rule);
`SAF-03` phonetic keys; `SAF-06`-`SAF-08` the rest of the matching ladder; `SAF-10`-`SAF-14` the
remaining pre-launch requirements; `SAF-15`-`SAF-29` failure behaviour, caching and audit surface;
`SAF-31`-`SAF-35` the seed corpus itself (content, not code — needs its own governance decision).

---

## Implementation note — 2026-09-17

Phase 1 implemented: migration `0151`
(`bharatstudio-alerts` `packages/db/migrations/0151_v1_saf_moderation_pipeline_spine.sql`) plus
the TypeScript pipeline (`apps/api/src/domain/aho-corasick.ts`, `safety-pipeline.ts`), corpus
management store and routes, contracts, and an explain-plan artifact. Built and verified against
a real `postgres:16-alpine` database. Nothing wired into a live surface. Full record:
`../../reviews/2026-09-17-saf-phase-1-implementation.md`. Acceptance:
`../../tests/TC-SAF-01-moderation-pipeline-spine.md`. `SAF-*` state letters are not self-assigned
here — this note records what was built, not a state change.
