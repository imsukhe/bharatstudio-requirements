# SAF-10/SAF-11/SAF-12 — URL neutralisation, SSML-injection guard, PII detection: implementation record

**Date:** 2026-09-17
**Owner:** **Sukhdev Singh**
**Authority:** `../FULL-PRODUCT-DEFINITION.md` S12.2.5, S12.10, S5.3, S31.13.2 rows
SAF-10/SAF-11/SAF-12
**Task:** `../active/tasks/SAF-10-url-ssml-pii-guards.md`
**Acceptance:** `../tests/TC-SAF-10-url-ssml-pii-guards.md`
**Predecessor:** `2026-09-17-saf-phase-1-implementation.md` (migration 0151) — the pipeline spine
this task extends

---

## What this task is, in one paragraph

Migration `0154` adds two new tables — `safety_domain_rules` (SAF-10, per-creator URL allow/deny
domains, empty by default) and `safety_pii_detections` (SAF-12, a class-only audit trail with no
text/value column of any kind) — plus two new TypeScript modules
(`apps/api/src/domain/url-neutralization.ts`, `pii-detection.ts`) that both call the existing
`normalizeForSafetyMatching` rather than reimplementing SAF-01's normalisation. SAF-11 required no
schema and no new production code at all: reading `apps/api/src/tts/provider.ts` first, as the
task instructed, found its existing `sanitizeTtsText` already structurally sufficient to make SSML
inert. Nothing is wired into a live surface — the same posture `0151` took.

## SAF-11 — reading first found the guard already built, and that is the correct outcome to report

The task's hard constraint was explicit: read `provider.ts` before designing, and do not duplicate
or contradict `sanitizeTtsText`. Doing so surfaced that `sanitizeTtsText`'s `MARKUP_LIKE_TAG`
regex (`/<[^>]*>/gu`) already strips every well-formed tag unconditionally, on every path —
`apps/api/src/routes/tts.ts` is the sole live caller of `TtsService.synthesize`, and
`createTtsService.synthesize` calls `sanitizeTtsText` before every provider dispatch with no
skip branch. SSML/XML syntax is entirely defined by `<...>` tag delimiters; a parser needs a
complete `<...>` pair to recognise a tag at all, so removing every one removes every possible
instruction a synthesiser could interpret. Building a second SSML-stripping implementation here
would have been exactly the "second implementation to drift out of sync" SAF-01 forbids, for a
guarantee that was already correct. The honest, disciplined choice was to add zero production
code and instead build a dedicated, exhaustive proof
(`apps/api/test/saf-ssml-injection-guard.test.ts`) — a battery of SSML injection payloads (nested
tags, attribute injection, malformed/unterminated tags, an `<audio src=...>` exfiltration
attempt) through both `sanitizeTtsText` directly and the full synthesis round trip via a fake
provider fetcher, asserting no `<`/`>` character ever reaches a provider. One test explicitly
separates SAF-04's guarantee (the stored original may still contain SSML markup, correctly) from
SAF-11's guarantee (what reaches the synthesiser never does) — the two are proven to be different
strings on different paths, so a future reader cannot conflate "the original is preserved" with
"the original is safe to speak".

## SAF-10 — URL neutralisation, and why the default is "neutralise", not "do nothing"

FULL-PRODUCT-DEFINITION.md S12.2.5 lists "URL removal or neutralisation" as a general pipeline
requirement, and `apps/api/src/tts/provider.ts:28,36` already, and unconditionally, replaces every
URL-shaped token with a placeholder before TTS dispatch — a pre-existing, decided behaviour for
that one surface. SAF-10 extends the SAME baseline ("neutralise by default") to a surface that had
zero URL handling before this migration (0151's own verified-before-starting note: SAF was
45-of-46 absent), and adds the actual per-creator configurability the register asks for: a domain
on the ALLOW list is exempt (passed through untouched); a domain on the DENY list is always
neutralised. This is a deliberate design decision, stated rather than left implicit: the "never
invent... empty deny means deny nothing" constraint in the task record is scoped to the DENY LIST
mechanism specifically (an empty deny array must never accidentally mean "deny every domain" via
an inverted-empty-array bug) — it does not claim the whole feature does nothing when unconfigured,
because the underlying "neutralise" baseline it modulates is a REUSED, already-decided value
(`provider.ts:28,36`), not something invented for this task. Both are proven separately in
`apps/api/test/url-neutralization.test.ts`.

## SAF-10 — allow/deny precedence made structurally impossible to contradict

`safety_domain_rules_channel_domain_idx`, a UNIQUE index on `(channel_id, domain)`, means a
channel can never hold two rules for the same literal domain — attempting to add `allow` for a
domain that already has `deny` (or vice versa) raises `unique_violation` before the ambiguity
could exist at all. This is the identical technique `0151` used for "no second corpus read path":
make the contradictory state impossible to write, rather than writing runtime logic to resolve it
after the fact. Proven behaviourally in `packages/db/tests/saf_url_ssml_pii.sql`. Because the
database never allows two rules for one domain, the TypeScript-level "deny wins" branch in
`neutralizeUrls` is defence in depth, not the primary guarantee — the primary guarantee is that the
ambiguous input state cannot exist. The TypeScript-level precedence test instead proves the more
useful thing: deny, allow and default resolve correctly and independently across three DIFFERENT
domains in the same message.

## SAF-12 — PII detection: format-level, not a classifier, and why "address" is narrowed

Every regex in `apps/api/src/domain/pii-detection.ts` is a public, structural format standard, not
an invented threshold: TRAI's mobile numbering plan (phone), NPCI's UPI VPA shape (distinguished
from an email by the absence of a dotted TLD after `@`), a practical email grammar, ISO/IEC
7812-1's PAN length range (card-like), and India Post's PIN code format. "Address" in the register
text (S5.3, S12.2.5) means free-text street-address extraction, which is an NLP/classifier
problem — `SAF-07`/`SAF-08` territory, explicitly out of scope for this task's hard constraints.
Narrowing it to PIN-code presence only, and documenting the narrowing rather than silently
shipping a false sense of coverage, follows the exact precedent `0151` itself set when it narrowed
SAF-02's fuller register text to NFKC/zero-width/RTL/combining-mark handling only, deferring
homoglyph/leet/repeat-collapse to SAF-03/SAF-06 (see that migration's own header).

## SAF-12 — the structural guarantee that detecting never means storing

Two independent layers, the same "prove it, don't just document it" posture `0151` used for
SAF-01: (1) TypeScript — `PiiDetectionResult` has exactly one field, `classes`, and
`apps/api/test/pii-detection.test.ts` proves for every one of the five PII shapes that
`JSON.stringify` of the detection result never contains the matched value. (2) Database —
`safety_pii_detections` has no text/value column of any kind (`channel_id, created_at, id,
pii_classes` — enumerated and asserted exactly against `information_schema.columns` in
`packages/db/tests/saf_url_ssml_pii.sql`), and `pii_classes` is CHECK-constrained to five fixed
class names, so an attempt to smuggle a raw phone number or email through the one function that
writes this table (`record_pii_detection`) is rejected with `check_violation` before the row can
exist — proven behaviourally, not merely by inspecting the column list. This is deliberately a
SEPARATE table from `0151`'s `safety_moderation_actions`, not a reuse of its `original_text`/
`normalised_text` columns: those columns exist specifically because SAF-04 requires the
corpus-match evidence snapshot to preserve the original, and reusing them for a PII-only
detection (which may have no corpus-term match at all) would mean writing the very message text
SAF-12 exists to keep out of storage. The migration's own header states this reasoning explicitly.

## No TypeScript store wraps `record_pii_detection`, and why that is not a gap

`0151` built no TypeScript adapter for its own `record_safety_moderation_action` — grep confirms
no caller of it exists anywhere in `apps/api/src` today. This task follows that exact precedent
for `record_pii_detection` rather than inventing a wrapper with no consumer and no way to be
exercised outside a direct SQL call (nothing is wired to a live surface in this phase, so no
caller would exist for either function's TypeScript wrapper). `detectPii` (the actual detection
logic) is fully built and tested; the DB-side recording primitive is proven directly in
`packages/db/tests/saf_url_ssml_pii.sql`, exactly as `record_safety_moderation_action` was in
`saf_pipeline_spine.sql`.

## SAF-10's store and routes — the corpus pattern, reused exactly

`apps/api/src/domain/url-domain-rule-store.ts`, `apps/api/src/db/url-domain-rule-store.ts` and
`apps/api/src/routes/url-domain-rules.ts` mirror `apps/api/src/domain/safety-corpus-store.ts`,
`db/safety-corpus-store.ts` and `routes/safety-corpus.ts` structurally: list/create/remove only,
no update (a rule is deleted and re-added), `list()` on `derivedReadSql`, writes on the main pool.
The consequence, found and handled rather than avoided: `scan-required-queries.mjs`'s rule 3 sweeps
`create_url_domain_rule`/`delete_url_domain_rule` into the same manifest requirement as the read
(both are writes, not widget-backing reads) — both added to `required-queries.json`'s `exemptions`
array with a written reason, the identical mechanism `0151`'s own
`create_safety_corpus_term`/`delete_safety_corpus_term` exemptions already established.

## Explain-plan artefact

`packages/db/explain-plans/safety-domain-rules.explain.md` captures `app_private.get_url_domain_rules`
against a real `postgres:16-alpine` container: two calls (cold and warm) over a two-row seed (one
`deny`, one `allow`, both on the one channel — SAF-10 has no "global" scope), showing the same
opaque `Function Scan` wrapper over a `Seq Scan` every other artefact in this directory shows at
this row count. Captured even though nothing routes this read through an overlay session — the
task's own instruction requires the artefact regardless, the identical posture
`safety-corpus-terms.explain.md` already recorded.

## Scope held

Nothing in this task touches `apps/web/app/overlay/canvas/`, any `capability*`/`ctl_*` file,
`TRACEABILITY.md`, `FULL-PRODUCT-DEFINITION.md`, `active/launch/**`, `active/traceability/**`, or
any `CTL-*`/`GOA-*` record — confirmed by `git status`/`git diff` against base `eac0150` showing
zero changes to any of those paths. Migration `0153` (the sibling lane's own number) was neither
created nor touched. `0151`'s `payment_decision`/`stored_record_decision` CHECK constraints on
`safety_moderation_actions` are unchanged (migration `0154` is purely additive — two new tables,
no `ALTER TABLE` against anything `0151` created).

## What is deliberately NOT done, restated

- `SAF-03`/`SAF-06`/`SAF-07`/`SAF-08`/`SAF-13`/`SAF-14` — not built.
- No starter domain list, no free-text address parser (narrowed to PIN-code presence, documented).
- No live surface (TTS, payment, chat, alert) calls `neutralizeUrls` or `detectPii`. A grep across
  `apps/api/src` for callers of either function outside their own test files returns zero results.
- SAF-11: zero new production code, by design (see above) — not an oversight.

Wiring any of this onto a live surface is a separate task with its own record, per the task's own
instruction.

## Verified numbers (see the acceptance record for the full command table)

sql 77/0 (baseline 76/0, +1) · api 845/0 (baseline 815/0, +30 new) · web 644/0 (unchanged) ·
typecheck 0 errors · contracts: 70 fixtures, 117 paths, 137 operations (baseline 68/115/134) ·
explain 30/30 (baseline 29/29) · harness pass · canvas subscriber count untouched (zero diff to
`apps/web/app/overlay/canvas/`).
