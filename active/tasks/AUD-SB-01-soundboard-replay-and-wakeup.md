# AUD-SB-01 — Safe Soundboard replay and overlay wake-up

**Status:** `Conditionally complete — locally verified`  
**Owner:** **Sukhdev Singh**  
**Authority:** `../launch/08_AUDIT_REMEDIATION_AUTHORITY.md` (AUD-SB-01)  
**Acceptance record:** `../../tests/TC-AUD-SB-01-soundboard-replay-and-wakeup.md`  
**Review record:** `../../reviews/2026-09-18-aud-sb-01-soundboard-replay-and-wakeup.md`

## Scope

Repair two confirmed Safe Soundboard behaviours:

1. A Canvas hide/show clears the in-memory `lastPlayedId`, so the durable
   latest-play snapshot can replay the same historical audio on reactivation.
2. `app_private.trigger_soundboard_play` inserts the durable latest-play row but does
   not invoke the existing channel-scoped overlay wake-up notification; an idle Canvas
   may wait for the SSE fallback poll interval before reading it.

Keep `lastPlayedId` for the lifetime of a page instance while still stopping current
audio and hiding the caption on deactivation. Add a new forward migration after the
current highest migration that replaces only the creator-trigger function to call the
already-existing security-definer `app_private.notify_overlay_wakeup(channelId, playId)`
after its successful durable insert. PostgreSQL delivers the notification only on
transaction commit; no direct browser/provider/CDN action is introduced.

## Data, security, and failure behaviour

- No new table, column, personal data, audio bytes, viewer/supporter field, or new
  overlay payload is added. The notification reuses opaque channel ID and play ID,
  both already used by the bounded wake-up path; it contains no clip URL/content.
- The existing trigger function retains owner/admin, exact-one-source, entry enabled,
  tier, tenant, and input validation before insert/notify. Any rejected trigger emits
  no row and no notification.
- A committed play's wake-up is latency optimisation only. Overlay snapshot reads and
  the bounded SSE fallback remain correctness paths. A notification/listener failure
  must never roll back or falsely reject a valid creator trigger.
- Latest-supersedes remains unchanged: same `playId` never plays twice in one page
  lifetime; a genuinely different `playId` replaces/stops current audio after a
  reactivation. Caption expiration and autoplay/CDN failure remain non-blocking.

## Migration, rollback, and deployment

Create a new numbered forward-only migration; never edit/squash `0143` or existing
database history. It redefines the function body and preserves existing grants.
Rollback is a new forward migration restoring the prior function body only if needed;
source rollback cannot undo an already-applied schema function. No configuration,
credential, external deployment, CDN setting, provider call, or feature flag changes.

## Required verification

- Module tests cover same play before/after deactivate/reactivate (no duplicate audio),
  different later play (one new audio), caption/audio teardown, and normal repeat poll.
- SQL proof covers valid trigger insert plus wake-up invocation in the same transaction,
  rejected trigger with no wake-up call, preserved grants/security-definer/search path,
  and no extra data-return surface.
- API route/store regressions prove the creator response stays `201 { playId }` with no
  direct notification endpoint or client-supplied wake-up parameter.
- Run migration harness, web/API suites, typecheck/build, contract/harness checks, and
  a hostile review for notification atomicity, replay, privacy, RLS/grants, and rollback.

## External evidence gate

The disposable local PostgreSQL listener rehearsal passed, but deployed browser/OBS,
CDN/GCS and autoplay evidence is still required to measure wake latency and confirm
real listener/audio behaviour. Local tests do not claim deployed or production
evidence.

## Reproducible redacted evidence — 2026-09-18

Working-tree baseline: Alerts `d5cebc6`; this corrective slice remains uncommitted.

- Changed `apps/web/app/overlay/canvas/modules/safe-soundboard-module.ts` and its
  module test: hide/show stops current media and clears the caption while preserving
  the page-lifetime latest-play de-duplication key; a later different play still
  replaces audio.
- Added `packages/db/migrations/0163_v1_aud_sb_overlay_wakeup.sql`. It replaces only
  `app_private.trigger_soundboard_play`, preserving validation, security-definer
  search path and grants, and calls the existing opaque wake-up helper after the
  durable insert.
- Extended `integration/overlay-wakeup.integration.ts` to seed an isolated channel,
  invoke the real security-definer trigger in a real transaction, observe the matching
  listener after commit, verify the durable row, then prove an invalid source returns
  `22023` and wakes nobody.
- Extended `packages/db/tests/prf02_slice7_safe_soundboard.sql` to inspect the
  installed function for insert-before-notify ordering and preserved execution
  boundary/grants.

| Command | Result |
|---|---|
| `cd bharatstudio-alerts/apps/web && pnpm exec tsx --test --import ./app/test-support/dom-env.ts app/overlay/canvas/modules/safe-soundboard-module.test.ts` | 10/10 passed |
| `cd bharatstudio-alerts && pnpm db:test:all` | SQL suite: 87 passed, 0 failed; includes `prf02_slice7_safe_soundboard` |
| `cd bharatstudio-alerts && packages/db/tests/run-l03-application-behavior.sh` | 25 SQL behavior files plus payment worker, alert worker, direct two-listener wake-up (including actual Soundboard trigger), cross-replica, concurrency and safe-soundboard real-store integrations passed |
| `cd bharatstudio-alerts && pnpm --filter @bharatstudio/alerts-web test` | 658 passed, 0 failed |
| `cd bharatstudio-alerts && pnpm --filter @bharatstudio/alerts-api test` | 934 passed, 0 failed |
| `cd bharatstudio-alerts && pnpm --filter @bharatstudio/alerts-api build && pnpm --filter @bharatstudio/alerts-web build` | API TypeScript build and web production build (34 routes) passed |
| `cd bharatstudio-alerts && pnpm contracts:validate && pnpm harness:check && git diff --check` | 78 fixtures, 151 paths/178 operations, 3 negative contract cases, harness and whitespace check passed |

The local evidence is self-reviewed, not independent review, and does not establish
provider, staging, deployment, browser/OBS, CDN/GCS or production readiness.
