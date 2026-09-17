# SAF-10/SAF-11/SAF-12 — URL neutralisation, SSML-injection guard, PII detection

**Status:** `Approved for implementation — dispatched 2026-09-17`
**Owner:** Sukhdev Singh
**Authority:** `../../FULL-PRODUCT-DEFINITION.md` S31.13.2 register rows `SAF-10`, `SAF-11`,
`SAF-12` - S12.2.5 (everything else required before launch) - S12.10 (evidence and retention) -
S5.3 (no-accidental-doxxing detector) - S12.2.6 (fail-closed for speech)
**Predecessor:** `SAF-01-moderation-pipeline-spine.md` (migration `0151`) - the pipeline spine this
task extends, not replaces. Read before designing: `apps/api/src/domain/safety-pipeline.ts`,
`aho-corasick.ts`, `safety-corpus-store.ts`, `packages/db/migrations/0151_v1_saf_moderation_pipeline_spine.sql`.

## Register text

| Row | Requirement |
|---|---|
| `SAF-10` | URL neutralisation with per-creator allow and deny domains |
| `SAF-11` | SSML-injection guard - a message can never become synthesis instructions |
| `SAF-12` | PII detection: phone, UPI ID, email, address, card-like strings, plus the no-accidental-doxxing rule (S5.3) |

## What matters most in each

**`SAF-11` has a live blast radius.** TTS already exists (`apps/api/src/tts/`), reachable from a
live route (`apps/api/src/routes/tts.ts`, `POST /internal/v1/tts/events/:eventId`). If a
supporter's message could carry SSML the synthesiser executes, a tip message becomes synthesis
instructions. **Read first, before designing**: `apps/api/src/tts/provider.ts`'s existing
`sanitizeTtsText` (lines 33-40) already strips every `<...>`-shaped markup token unconditionally
before any provider dispatch - SSML syntax is entirely defined by `<...>` tag delimiters, so this
mechanism is already structurally sufficient, and it predates this task. **Do not duplicate or
contradict it.**

**`SAF-12` is a privacy control, and S12.10 applies.** Detecting PII must not mean storing PII.
Follow `0151`'s posture: raw unactioned text is never written. A detection result records THAT a
class was found, never the value found.

**`SAF-10` needs per-creator allow and deny domains** - creator-configurable data, not a hardcoded
list. Ship empty, exactly as `0151`'s corpus ships empty. Empty deny means "deny nothing", never
"deny everything".

## What this task deliberately does NOT build

- `SAF-03` (Indic phonetic), `SAF-06` (L2 edit distance), `SAF-07`/`SAF-08` (classifier, AI),
  `SAF-13` (rate/flood), `SAF-14` (policy presets) - later lanes.
- **No starter domain list.** `safety_domain_rules` (migration `0154`) ships schema-only, zero
  rows.
- **SAF-12's "address" is narrowed to Indian PIN code presence only.** Free-text street-address
  extraction is an NLP/classifier problem - `SAF-07`/`SAF-08` territory, explicitly out of scope
  here. Narrowed and documented, the same way `0151` narrowed `SAF-02`'s fuller register text
  (its own migration header records why), not silently dropped.
- **Not wired into any live payment, TTS, chat or alert path.** Built and proven in isolation, the
  identical posture `0151` took. `SAF-11`'s finding that the existing guard is already sufficient
  does not change this - nothing new is switched onto the live TTS route by this task either.

## Constraints

- Never invent a numeric limit, price, provider behaviour, legal wording, retention window or
  domain list. Where a bound is needed, reuse a decided value and cite file:line (RFC 1035
  hostname-label shape/length for domains, ISO/IEC 7812-1 PAN length range for card-like strings,
  TRAI's mobile numbering plan for phone, India Post's PIN code format for the address proxy - all
  public structural standards, not invented thresholds), or ship configured-but-unset.
- **Extend the one pipeline.** `0151` enforces SAF-01 two ways: `bsa_app` has no grant on its
  tables, and an app-level scan fails if `.normalize(` or the `AhoCorasick` identifier appears
  outside its owning file. This task's work must not trip that scan, and must not create a second
  normalisation or matching path - new modules call `normalizeForSafetyMatching`, never
  reimplement it.
- **Preserve `0151`'s database-enforced guarantees**: `payment_decision check (= 'allow')` and
  `stored_record_decision check (= 'allow')` on `safety_moderation_actions` untouched.
  `original_text`/`normalised_text` stay both `NOT NULL`.
- Migration number `0154` and fixture UUID range `...6e00-...6eff` pre-assigned by the coordinator
  - a sibling lane runs concurrently in a separate worktree, owning migration `0153` and the
  capability registry (`capability*`/`ctl_*` untouched by this task).
- Route tests use the shared `createTestFastify()`; never construct Fastify directly.
- Do NOT touch `apps/web/app/overlay/canvas/` (`getSubscriberCount()` must stay unchanged), any
  `capability*`/`ctl_*` file, `TRACEABILITY.md`, `FULL-PRODUCT-DEFINITION.md`,
  `active/launch/**`, `active/traceability/**`, or any `CTL-*`/`GOA-*` record.

---

## Implementation note — 2026-09-17

Implemented: migration `0154`
(`bharatstudio-alerts` `packages/db/migrations/0154_v1_saf_url_ssml_pii_guards.sql`) - two new
tables (`safety_domain_rules` for SAF-10, `safety_pii_detections` for SAF-12) - plus TypeScript
additions (`apps/api/src/domain/url-neutralization.ts`, `pii-detection.ts`), a domain-rule store
and routes (mirroring `0151`'s corpus store/routes exactly), contracts, and an explain-plan
artefact. **SAF-11 required zero new production code** - the existing `sanitizeTtsText` guard was
found, on reading it first, to already be structurally sufficient; this task's SAF-11 contribution
is a dedicated proof suite (`apps/api/test/saf-ssml-injection-guard.test.ts`) tying that existing
mechanism explicitly to the register row. Built and verified against a real `postgres:16-alpine`
database. Nothing wired into a live surface. Full record:
`../../reviews/2026-09-17-saf-url-ssml-pii-implementation.md`. Acceptance:
`../../tests/TC-SAF-10-url-ssml-pii-guards.md`. `SAF-*` state letters are not self-assigned here -
this note records what was built, not a state change.
