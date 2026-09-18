# Review — AUD-OVL-01 standalone overlay API-origin audio resolution

**Status:** `Conditionally complete — self-review passed; independent review unavailable`  
**Reviewer:** Sukhdev Singh (self-review until independent review is available)  
**Scope:** `AUD-OVL-01-standalone-overlay-api-origin.md`

## Required review checklist

- Inspect the actual final worktree rather than an implementation report.
- Confirm relative API payload URLs resolve against only the validated configured API
  origin, not `window.location.origin` or a value supplied by an event payload.
- Attempt external, web-origin, credential-bearing, encoded-path, malformed, and
  wrong-route inputs; no result may reach the authenticated fetch.
- Confirm both Canvas and standalone consume one pure helper, with no duplicate
  security boundary remaining.
- Confirm no overlay bearer token, audio body, donor field, API route, migration,
  payment path, or provider setting changed.
- Re-run recorded checks, inspect `git diff --check`, record exact redacted commands,
  results, changed paths, rollback proof, findings/disposition, and external gate.

## Required disposition

Do not mark complete until the reviewer records whether review was independent. A real
separate-origin browser/OBS rehearsal is an external evidence gate and must not be
represented as completed by unit or build checks.

## Fresh hostile self-review — 2026-09-18

**Reviewer:** Sukhdev Singh (self-review; independent review unavailable).  
**Reviewed worktrees:** Alerts base `d5cebc6`; requirements base `4294a00`.

| Finding | Severity | Disposition and evidence |
|---|---|---|
| Standalone overlay resolved API-emitted relative TTS paths against `window.location.origin`; separate web/API deployments fetched the web application and silently fell through to chime. | P1 delivery defect | Fixed by `safeOverlayAudioUrl(value, configuredApiOrigin)`, called from standalone with the existing validated API origin. Focused regression proves the result is the API origin without consulting a browser-page origin. |
| Canvas and standalone carried duplicated URL allowlists, allowing a future security/behaviour divergence. | P2 maintenance/security seam | Fixed by one overlay-owned pure helper consumed by Canvas Support Theater and standalone. Canvas lifecycle/audio tests passed with actual two-parameter route fixtures. |
| A malicious/corrupt event payload could attempt an arbitrary absolute URL or malformed route. | P1 security seam | Fixed fail-closed: cross-origin, credentials, query/hash, percent-encoded path, malformed, wrong-route, wrong-segment-count, and invalid configured-origin inputs return no fetch URL. API bearer authorisation remains the final server boundary. |

**Negative checks:** source search found no standalone `window.location.origin` audio
resolution and no remaining duplicate `safeAudioUrl`; the only audio helper is used by
both surfaces. The repair adds no storage, no token persistence, no API/provider call,
no migration, and no route/event-contract change. `git diff --check` passed.

**Rollback/recovery:** revert the shared helper, its test, the Canvas import/call,
standalone import/call, and the two corrected Canvas fixtures together. No durable data
or forward migration needs repair. Existing API-origin configuration validation and
browser-TTS/chime degradation remain in force.

**External/release gate:** a safe environment with distinct web/API origins must be
opened as an OBS/browser source and play a real scoped artifact before cross-origin
runtime readiness can be claimed. That evidence has not been run or claimed here.
