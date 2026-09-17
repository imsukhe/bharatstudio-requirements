# TC-SAF-10 — URL neutralisation, SSML-injection guard, PII detection: acceptance record

**Date:** 2026-09-17
**Owner:** **Sukhdev Singh**
**Task:** `../active/tasks/SAF-10-url-ssml-pii-guards.md`
**Decision:** `../reviews/2026-09-17-saf-url-ssml-pii-implementation.md`
**Authority:** `../FULL-PRODUCT-DEFINITION.md` S12.2.5, S12.10, S5.3, S31.13.2 rows
SAF-10/SAF-11/SAF-12

Written to accompany implementation, per `governance/AGENTS.md`. The "Commands run" table is
filled in from actual output against a real `postgres:16-alpine` container and a real `tsx --test`
run, and is the single place this task's numbers live.

---

## Acceptance criteria

### A. SAF-10 — URL neutralisation, per-creator allow/deny domains

| ID | Criterion |
|---|---|
| SAF10.1 | `safety_domain_rules` ships empty — migration 0154 inserts zero rows |
| SAF10.2 | A fresh channel's domain-rule read returns zero rows before any insert |
| SAF10.3 | `bsa_app` has NO SELECT/INSERT/UPDATE/DELETE grant on `safety_domain_rules` — the only reachable read path is `app_private.get_url_domain_rules` |
| SAF10.4 | **Behavioural**: connecting as `bsa_app` and attempting a direct `SELECT` on `safety_domain_rules` raises `insufficient_privilege` |
| SAF10.5 | Owner/admin may add a domain rule to their own channel; operator/moderator/viewer may not (`insufficient_privilege`) |
| SAF10.6 | A domain can hold at most one rule per channel — a unique index (`channel_id`, `domain`) rejects a second, contradictory rule with `unique_violation` — **this is the structural precedence proof**: allow/deny ambiguity cannot be written to the database |
| SAF10.7 | Two different channels may independently hold their own rule for the same literal domain text |
| SAF10.8 | The domain CHECK constraint (RFC 1035 hostname shape, lowercase-only) rejects an uppercase domain, a domain with invalid characters, and a domain with no dot |
| SAF10.9 | Channel isolation: channel A's rules never leak to channel B and vice versa |
| SAF10.10 | `delete_url_domain_rule` is channel-owned only — owner/admin may delete their own channel's rule; a viewer may not; channel A cannot delete channel B's rule through its own call (`P0002`, not found) |
| SAF10.11 | **TypeScript**: `neutralizeUrls` — an unlisted domain is neutralised by DEFAULT (the reused, already-decided TTS-side baseline, `apps/api/src/tts/provider.ts:28,36`), never invented fresh |
| SAF10.12 | An empty rule list neutralises every URL by the baseline — never zero, and never "deny everything" via an inverted-empty-array bug |
| SAF10.13 | An allow-listed domain passes through untouched; a deny-listed domain is always neutralised |
| SAF10.14 | **Precedence, TypeScript-level**: deny, allow and default each resolve correctly and independently across three DIFFERENT domains in the same message |
| SAF10.15 | Domain comparison is case-insensitive and resists zero-width-character evasion, via the ONE shared `normalizeForSafetyMatching` call (SAF-01) |
| SAF10.16 | The neutralisation audit trail (`neutralizedHosts`) records HOSTS ONLY, never the raw URL, path or query string |

### B. SAF-11 — SSML-injection guard

| ID | Criterion |
|---|---|
| SAF11.1 | `sanitizeTtsText` (pre-existing, `apps/api/src/tts/provider.ts:33-40`) strips every `<[^>]*>`-shaped tag for a battery of SSML injection payloads (`<speak>`, `<prosody>`, `<voice>`, `<break>`, nested tags, `<say-as>`, `<audio src=...>`, malformed nesting) — no complete tag survives |
| SAF11.2 | An unterminated tag (`<speak` with no closing `>`) may leave a literal `<` character, but forms no COMPLETE, parseable tag — inert either way, since SSML/XML syntax requires a well-formed `<...>` pair |
| SAF11.3 | The FULL synthesis round trip (`createTtsService` -> `createSarvamTtsProvider` -> fake fetcher) never sends a `<` or `>` character to the provider, for every well-formed SSML payload, regardless of cache/quota state |
| SAF11.4 | SAF-04's "original text is never destroyed" and SAF-11's "a message can never become synthesis instructions" are proven to be two DIFFERENT strings on two DIFFERENT paths — the stored original may still contain SSML markup (correctly, per SAF-04); what reaches the synthesiser never does |
| SAF11.5 | `apps/api/src/routes/tts.ts` is the sole live caller of `TtsService.synthesize` in this codebase, and `createTtsService.synthesize` calls `sanitizeTtsText` before EVERY provider dispatch, with no branch that skips it |
| SAF11.6 | **No new production code was added for SAF-11** — verified: `git diff` against base shows zero changes to `apps/api/src/tts/provider.ts` |

### C. SAF-12 — PII detection

| ID | Criterion |
|---|---|
| SAF12.1 | `detectPii` classifies a phone number (TRAI numbering plan), a UPI VPA (NPCI shape, distinct from an email), an email, a card-like digit run (ISO/IEC 7812-1 length range), and an Indian PIN code (the documented, narrow "address" proxy) |
| SAF12.2 | A clean message with none of the five shapes detects nothing |
| SAF12.3 | Multiple classes in one message are all reported, deduplicated |
| SAF12.4 | Detection resists zero-width-character evasion via the ONE shared `normalizeForSafetyMatching` call (SAF-01) |
| SAF12.5 | **Structural, TypeScript**: `PiiDetectionResult` has exactly one field, `classes` — for every one of the five PII shapes tested, `JSON.stringify(result)` never contains the matched value |
| SAF12.6 | **Structural, database**: `safety_pii_detections` has EXACTLY the columns `channel_id, created_at, id, pii_classes` — no text/value column of any kind, asserted against the live catalogue |
| SAF12.7 | `pii_classes` CHECK-constrains to the five fixed class names — attempting to smuggle a raw phone number or email through `record_pii_detection` raises `check_violation` before the row can exist |
| SAF12.8 | An empty `pii_classes` array is rejected — there is nothing to record for "detected nothing" |
| SAF12.9 | `bsa_app` has NO grant on `safety_pii_detections` at all; **behavioural**: a direct `SELECT` as `bsa_app` raises `insufficient_privilege` |
| SAF12.10 | `record_pii_detection`'s parameter list is exactly `(target_channel_id, target_pii_classes)` — no text/value IN parameter exists |
| SAF12.11 | No TypeScript store wraps `record_pii_detection` in this phase, matching `0151`'s own precedent for `record_safety_moderation_action` (verified: no caller of either exists anywhere in `apps/api/src`) |

### D. Scope discipline held

| ID | Criterion |
|---|---|
| SCOPE.1 | `apps/web/app/overlay/canvas/` is untouched (zero diff) |
| SCOPE.2 | No file/identifier matching `capability*`/`ctl_*` is touched |
| SCOPE.3 | Migration `0153` was not created or touched (sibling lane's own number) |
| SCOPE.4 | No starter domain list, no invented PII regex thresholds presented as policy — every bound cited to a public structural standard |
| SCOPE.5 | `apps/api/test/safety-pipeline.test.ts`'s SAF-01 structural scans (no second `.normalize(` call site, no second `AhoCorasick` identifier, both outside their one owning file) still pass — new modules call `normalizeForSafetyMatching`, never reimplement it |
| SCOPE.6 | `payment_decision`/`stored_record_decision` CHECK constraints on `safety_moderation_actions` (migration 0151) are unchanged |

---

## Commands run

| Command | Result |
|---|---|
| Base fix (`git reset --hard eac0150`) | Applied; worktree confirmed at `eac0150 SAF phase 1: a moderation pipeline where there was none` |
| Full SQL suite (`sh packages/db/tests/run-sql-suite.sh`, 77 files incl. this task's own `saf_url_ssml_pii.sql`), real `postgres:16-alpine` container | pass=77 fail=0 (baseline 76/0; +1 new file) |
| `apps/api` route/unit suite (`tsx --test test/**/*.test.ts`) | tests 845, pass 845, fail 0 (baseline 815/0; +30, all new: `url-neutralization.test.ts` (8), `pii-detection.test.ts` (9), `saf-ssml-injection-guard.test.ts` (5), `url-domain-rules-routes.test.ts` (8)) |
| `apps/web` suite | tests 644, pass 644, fail 0 (baseline 644/0, unchanged — no web files touched) |
| `apps/api` TypeScript typecheck (`tsc -p tsconfig.json --noEmit`, separate from the test runner) | 0 errors |
| `node contracts/validate-fixtures.mjs` | Validated 70 fixtures plus the v1 template catalogue contract (baseline 68) |
| `node contracts/validate-openapi.mjs` | Validated OpenAPI 3.1 document with 117 paths, 137 operation contracts (baseline 115/134) |
| `node contracts/test-openapi-validator.mjs` | Validated 3 negative OpenAPI operation-contract cases |
| `node packages/db/explain-plans/scan-required-queries.mjs` | OK, 30 manifest entries, 13 exemptions (baseline 29/11) |
| `node packages/db/explain-plans/check-plans.mjs` | OK: 30/30 plans current (baseline 29/29) |
| `pnpm harness:check` (`node .github/scripts/api-test-harness-check.mjs`) | all checks passed; 40 files reference `createTestFastify` |

**Not run:** `go test`/`go vet` on the Go services, `pnpm build`, Docker image builds, and
`scripts/load/*` self-tests — none of this task's files touch Go services or change build output
shape. `measurement:test` was not separately re-verified beyond the `apps/api`/`apps/web`
sub-steps recorded above — a known pre-existing environmental gap in agent sandboxes (same note as
`TC-SAF-01-moderation-pipeline-spine.md` and `TC-CTL-01-capability-control-plane.md`), not
something this task's files could affect.

## SAF-11 — the mechanism, the test, and how it relates to the existing `sanitizeTtsText`

Mechanism: `sanitizeTtsText` (`apps/api/src/tts/provider.ts:33-40`, pre-existing, unmodified by
this task) strips every `<[^>]*>`-shaped token unconditionally, on every path, before any provider
dispatch. SSML/XML syntax is entirely defined by `<...>` tag delimiters — removing every
well-formed tag removes every possible piece of markup a synthesiser could interpret as an
instruction, and this codebase never asks a provider to parse the result as SSML (no `ssml: true`
flag, no `<speak>`-wrapped document is ever requested). Test:
`apps/api/test/saf-ssml-injection-guard.test.ts`, five tests covering a battery of SSML payloads
through `sanitizeTtsText` directly, the unterminated-tag edge case, the full synthesis round trip
via a fake provider fetcher, the SAF-04/SAF-11 two-different-strings distinction, and the
single-live-caller structural fact the whole proof depends on. Relation to the pre-existing single
assertion in `apps/api/test/tts-provider.test.ts` ("TTS neutralizes technical controls, URLs and
markup before provider dispatch"): this file does not replace that test, it is a dedicated,
SAF-11-labelled, more exhaustive version tying the same underlying mechanism explicitly to the
register row.

## SAF-12 — the proof a detected value is never stored or logged

TypeScript: `PiiDetectionResult` (`apps/api/src/domain/pii-detection.ts`) has exactly one field,
`classes: PiiClass[]` — there is no field capable of holding a matched substring. Test:
`apps/api/test/pii-detection.test.ts`'s "the detection result never contains the matched value" —
for phone, UPI id, email, card number and PIN code, `JSON.stringify(detectPii(text))` is asserted
to never contain the secret value embedded in the input text. Database:
`safety_pii_detections` (migration 0154) has no text/value column at all — `pii_classes` is
CHECK-constrained to five fixed class names. Test: `packages/db/tests/saf_url_ssml_pii.sql`
enumerates the table's actual columns via `information_schema.columns` and asserts the exact set
(`channel_id, created_at, id, pii_classes`), then behaviourally proves an attempt to smuggle a raw
phone number or email through `pii_classes` is rejected with `check_violation`.

## SAF-10 — the proof empty deny means deny-nothing, and no domain list was invented

`packages/db/migrations/0154_v1_saf_url_ssml_pii_guards.sql` inserts zero rows into
`safety_domain_rules`. `neutralizeUrls`'s default behaviour (an unlisted domain is neutralised) is
the pre-existing, already-decided TTS baseline (`apps/api/src/tts/provider.ts:28,36`), cited not
invented — SAF-10 adds the per-creator allow/deny layer on top. An empty deny list adds no
MORE neutralisation beyond that baseline; an empty allow list exempts nothing that was not
explicitly configured. Test: `apps/api/test/url-neutralization.test.ts`'s "an empty domain-rule
list neutralises every URL by the baseline, never zero and never deny-everything via some
inverted-empty-array bug", plus the SQL suite's SAF10.1/SAF10.2 empty-by-default assertions.

## SAF-10 — how allow/deny precedence is structural, not a runtime tie-break

`safety_domain_rules_channel_domain_idx`, a UNIQUE index on `(channel_id, domain)`, makes it
impossible to store two contradictory rules for the same domain on the same channel — attempting
to add `allow` for a domain that already has `deny` on that channel raises `unique_violation`
before either rule could contradict the other. Proven behaviourally in
`packages/db/tests/saf_url_ssml_pii.sql`. The runtime precedence claim (deny wins if a domain
could somehow hold both) is therefore never actually exercised by real data — paired instead with
a TypeScript-level test proving deny/allow/default resolve correctly across three DIFFERENT
domains in one message (`apps/api/test/url-neutralization.test.ts`'s "precedence" test).

## One pipeline preserved

`apps/api/test/safety-pipeline.test.ts`'s two structural scans (no second `.normalize(` call site,
no second `AhoCorasick` identifier, both outside their one owning file) pass unchanged —
`url-neutralization.ts` and `pii-detection.ts` both call the existing
`normalizeForSafetyMatching` rather than reimplementing normalisation, and neither constructs an
Aho-Corasick automaton (both use plain regex matching, a different, and here more appropriate,
technique for URL/PII format detection — no multi-pattern corpus is involved).
