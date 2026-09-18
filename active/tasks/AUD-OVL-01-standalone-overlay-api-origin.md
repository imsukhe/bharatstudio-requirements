# AUD-OVL-01 — standalone overlay API-origin audio resolution

**Status:** `Conditionally complete — locally verified; independent review and external browser/OBS evidence pending`  
**Owner:** **Sukhdev Singh**  
**Authority:** `../launch/08_AUDIT_REMEDIATION_AUTHORITY.md` (AUD-OVL-01)  
**Acceptance record:** `../../tests/TC-AUD-OVL-01-standalone-overlay-api-origin.md`  
**Review record:** `../../reviews/2026-09-18-aud-ovl-01-standalone-overlay-api-origin.md`

## Scope

Repair the standalone browser-source overlay's TTS artifact resolution. The API emits
the scoped artifact as a relative `/v1/overlay-audio/{overlayId}/{artifactId}` URL,
but the rollback/standalone overlay currently resolves that path against the web-page
origin. When web and API use separate origins, its authenticated fetch therefore
targets the web application instead of the API and falls through to a chime.

Create one pure overlay-owned URL boundary, move the existing Canvas-safe audio URL
check onto it, and make the standalone overlay pass its configured API origin to that
boundary. Add deterministic regressions for separate web/API origins and hostile URL
inputs. This task does not change audio routes, bearer-token behaviour, event payloads,
TTS entitlement/fallback policy, data storage, migrations, or any provider adapter.

## Security, privacy, and failure behaviour

- Only a URL whose origin is exactly the configured API origin and whose path starts
  with `/v1/overlay-audio/` can reach the authenticated artifact fetch.
- Relative event values resolve against the configured API origin, never the OBS
  browser-source/web-page origin. External, web-origin, malformed, credentialed, and
  non-artifact URLs fail closed to the existing non-blocking fallback path.
- Existing fragment bearer-token handling is unchanged: the token remains in browser
  memory/URL fragment and is attached only to the existing API fetch. No token, donor
  data, audio bytes, or new analytics are stored or logged by this repair.
- If API-origin configuration is unavailable/invalid, the standalone overlay retains
  its current no-audio safe failure rather than guessing a host or falling back to a
  user's localhost in non-development environments.

## Service boundary, deployment, kill switch, and rollback

The web client owns URL construction only; the API remains sole owner of artifact
authorisation, scoped overlay ID checks, and artifact byte delivery. There is no API
contract change and no migration. Deployment uses the existing `NEXT_PUBLIC_API_ORIGIN`
configuration. The existing standalone overlay remains the mid-stream rollback surface.

Rollback is a source revert of the shared URL helper, its two call sites, and regression
test. It requires no data repair or forward migration. This task introduces no new
feature flag or client bypass; configuration failure remains fail-closed.

## Required verification

- Unit tests prove a relative artifact URL becomes the configured API URL even when
  the browser page is on a different origin; canonical same-API URLs remain allowed.
- Tests reject an arbitrary external/web origin, credential-bearing input, wrong path,
  malformed input, and a non-HTTP(S) API origin.
- Canvas continues to use the same shared boundary so the two overlay surfaces cannot
  silently diverge again.
- Run relevant web tests, web typecheck/build, and API regression suite; inspect the
  final diff for origin confusion, token leakage, route changes, or unrelated edits.

## External evidence gate

A real browser-source/OBS rehearsal with separate web and API deployment origins is
still required before claiming runtime/OBS readiness. Local deterministic tests can
only prove URL selection and fail-closed behaviour.

## Implementation and traceability reconciliation — 2026-09-18

Added `apps/web/app/overlay/alert-audio-url.ts` as the single pure URL boundary and
its deterministic regression. The standalone rollback overlay now passes its existing
validated `getApiOrigin()` value into that helper. Canvas Support Theater now imports
the same helper; its synthetic event URLs were corrected to the actual two-parameter
artifact-route shape. The previous Canvas-local duplicate helper was removed while its
non-blocking chime remains unchanged.

No API route, event payload, database migration, bearer-token mechanism, provider
configuration, payment flow, entitlement rule, or audio fallback policy changed.
`git diff --check` passed. This is a corrective subtask under existing overlay/TTS
authorities; it does not change the §31 register mapping. It is linked through
`08_AUDIT_REMEDIATION_AUTHORITY.md` and `TRACEABILITY.md` is regenerated after closure.
