# L03 — TTS text safety boundary

**Status:** `Locally verified; language-policy and deployment evidence remain open`
**Level:** L3
**Parent authority:** `L03-alerts-web-and-creator-api.md`; `L05-go-alert-worker-and-cloud-tasks.md`; `2026-09-13-reachability-register.md §3`
**Test record:** [`../tests/TC-L03-tts-text-safety-boundary.md`](../tests/TC-L03-tts-text-safety-boundary.md)
**Review:** [`../reviews/2026-09-14-L03-tts-text-safety-boundary-decision.md`](../reviews/2026-09-14-L03-tts-text-safety-boundary-decision.md)

## Scope, security impact, and acceptance

The provider adapter receives supporter-controlled text and must not turn
control characters, bidirectional overrides, zero-width controls, URLs, or
markup-like payloads into spoken output or cache-key variants. Normalize text
with Unicode NFKC, remove technical control/invisible direction characters,
replace URL tokens with a fixed neutral phrase, strip markup-like tags, collapse
whitespace, then retain the existing non-empty/500-character bound. Apply the
same output to provider dispatch and cache keys.

This does not introduce a language-specific profanity list, user blocklist,
moderation decisions, or a retention/data-model change. Those require a
separate product/legal language-policy authority. It preserves raw visual alert
content and changes only optional TTS narration; a safe rejection continues to
use the existing chime fallback. Rollback is the isolated sanitizer change;
there is no migration or external prerequisite.

Acceptance requires deterministic hostile-text cases, cache-key normalization
proof, provider payload proof, API build, full local verification, and a review
that explicitly retains the language-policy gap.

## Reproducible local evidence — 2026-09-14

- `sanitizeTtsText` now uses NFKC normalization; removes C0/C1, zero-width and
  bidirectional controls; replaces URL tokens with `shared link`; strips
  markup-like tags; collapses whitespace; and retains the non-empty/500-char
  invariant. The sanitized text is both the adapter payload and cache-key input.
- Text which becomes empty is not sent to the provider. The TTS service returns
  its existing non-blocking chime fallback instead.
- Focused provider tests pass 5/5: hostile payload neutralization, Unicode
  equivalent cache reuse, and empty-after-neutralization fallback are covered.
- API TypeScript build and `pnpm verify:local` pass across contracts,
  deployment validation, 116 migrations, 46 SQL proofs, load/fault, API/web,
  Go race/vet, and command-image checks.

No claim is made that this is language moderation, provider-side safety, a
blocked-user system, or live audio/device proof. Those gates remain open.
