# PRF-02 slice 7 follow-up — Media Queue URL hardening: implementation decision record

**Date:** 2026-09-17
**Owner:** **Sukhdev Singh**
**Task:** `../active/tasks/PRF-02-slice-7-media-url-hardening.md`
**Acceptance record:** `../tests/TC-PRF-02-slice-7-media-url-hardening.md`
**Triggering review:** `../reviews/2026-09-17-slice-7-hostile-code-review.md` (F1 HIGH, F4 LOW)
**Base:** `bharatstudio-alerts` at `53d402a` on local `master`

---

## F1 — decision: mirror migration 0143 exactly, do not invent a new pattern

The hostile review's own table made the comparison explicit: Safe Soundboard (0143) and Sponsor
Card (0145) both refuse to render until a GCS/CDN base exists; Media Queue (0146) was the outlier
because it accepted a caller-supplied `https://` URL with no host restriction. The fix is migration
`0148`, which does exactly four things, none of them novel:

1. Replaces `storage_url`/`thumbnail_url` with `gcs_object_key`/`thumbnail_gcs_object_key`, carrying
   migration 0143's exact check-constraint text: `gcs_object_key ~ '^[A-Za-z0-9/_.-]{1,255}$' and
   gcs_object_key !~ '\.\.'`. This character set has no slot for `:`, `//`, or a host — a value
   satisfying it cannot be a URL, by construction, not by validation-that-could-be-bypassed.
2. Moves URL resolution out of SQL entirely, into
   `apps/api/src/db/media-queue-overlay-store.ts`'s `resolveMediaPlaybackUrl(cdnBaseUrl, objectKey)`
   — a direct copy of `resolveSoundboardPlaybackUrl`'s shape, concatenating a host-less key onto a
   base that is itself validated https at config load time (`apps/api/src/config.ts`). Reuses
   `config.mediaCdnBaseUrl` verbatim; no second CDN-base config value was introduced anywhere.
3. Deletes existing `media_queue_items` rows (a `storage_url` cannot be losslessly turned into a
   content-key fragment — the scheme and host that made it a URL are precisely what the new
   character set forbids), announced via `RAISE NOTICE` with the exact count, mirroring migration
   0147's precedent for its own destructive-but-announced cleanup.
4. Makes `apps/web/app/overlay/canvas/modules/media-queue-module.ts` render nothing for an entry
   whose resolved `playbackUrl` is null — `hasSomethingToShow` (media-queue-logic.ts) now requires
   both a live entry AND a non-null `playbackUrl`.

**Why not keep `storage_url` and add an allowlist instead?** Considered and rejected: an allowlist of
approved third-party hosts is itself a new, unapproved product surface (exactly the "advanced mode"
section 9.1.1 explicitly forbids: "there is no tier, no attestation and no 'advanced mode' that makes
it acceptable"), and it would diverge from the established, owner-approved soundboard pattern instead
of reusing it.

**Why delete existing rows instead of writing a migration script to fetch and re-host each asset?**
No such re-hosting pipeline exists in this codebase (migration 0146's own header: the creator's media
upload pipeline is register item `INT-07`, `new-record-required`, explicitly out of scope for this
slice). Building one now to rescue rows that were never actually playable (every environment's
`mediaCdnBaseUrl` has been unset since 0146 shipped, so a `storage_url` row was never resolved by
this product's own CDN anyway) would be new, unauthorised scope. The honest fix is the deletion,
announced.

### The creator write path: a key is supplied directly, not derived

Unlike the soundboard's upload path (`upload_channel_soundboard_clip` derives
`'soundboard/' || channel_id || '/' || sha256` server-side from a content hash), Media Queue's
`enqueue_media_queue_item` still accepts a caller-supplied key directly — because, as above, there is
no upload/hashing pipeline for this module to derive one from. This is a deliberate, recorded
asymmetry, not an oversight: the security property (no arbitrary origin reachable) holds regardless
of who supplies the key, because the character-set CHECK constraint makes a URL structurally
inexpressible no matter the source. A future INT-07 upload pipeline can switch to a derived key
without changing this migration's schema shape.

### Proof no caller- or row-supplied value can become the origin

`resolveMediaPlaybackUrl`:

    export function resolveMediaPlaybackUrl(cdnBaseUrl, objectKey) {
      if (!cdnBaseUrl || !objectKey) return null;
      return `${cdnBaseUrl.replace(/\/+$/, '')}/${objectKey}`;
    }

`cdnBaseUrl` comes ONLY from `config.mediaCdnBaseUrl`, read once at process startup from
`MEDIA_CDN_BASE_URL`, validated https at that point (`apps/api/src/config.ts`) — never per-request,
never caller-influenced. `objectKey` comes from a database column whose CHECK constraint forbids a
colon or a double slash. The string template concatenates the two with a single slash separator;
there is no code path by which either half can be replaced by a caller- or row-supplied host. Three
independent narrowings enforce this end to end: the SQL CHECK constraint, the AJV route pattern
(`apps/api/src/routes/media-queue.ts`), and the client-side `isHttpsUrl`/`isNullableHttpsUrl` guards
in `media-queue-logic.ts`.

---

## F4 — decision: the existing integration.ts pattern, not a new one

`channel-store-concurrency.integration.ts` already establishes exactly the shape this seam needs: a
`BSA_*_SQL_DSN` env var, a real `postgres()` connection, the real `createSql*Store` factory, seeded
via raw SQL, asserted with `node:test`, wired into `packages/db/tests/run-l03-application-behavior.sh`.
No `apps/api` test currently connects to a live database (`apps/api/test/*.test.ts` all construct
Fastify via `createTestFastify()` with stubbed stores), so a plain SQL-suite addition genuinely cannot
exercise the TypeScript mapping in `safe-soundboard-store.ts:138` — only a Node process that imports
that file and calls it can. This is why the task record's fallback clause ("if none exists, put it in
the SQL suite... if that is genuinely impossible say so precisely") does not apply here: the pattern
DOES already exist, and reusing it was the correct choice.

**Debugging note, kept for anyone extending this file:** the first draft's `cleanup()` was missing the
`queue_bindings`/`alert_queues` deletes that `channel-store-concurrency.integration.ts`'s own cleanup
already includes — `app_private.create_channel` seeds a default alert queue, and without deleting it
first, the channel delete fails on an FK constraint, cleanup throws mid-sequence, and the Postgres
connection pool is left open, hanging the process past its timeout rather than exiting with a clear
failure. Fixed by copying the exact FK-order cleanup sequence from the existing file rather than
guessing at one.

---

## Verification, run for real

| Check | Result |
|---|---|
| Fresh postgres:16-alpine, roles + migrations 0001-0148 applied, `prf02_slice7_media_queue.sql` | pass — "all assertions passed" |
| `pnpm db:test:all` | sql 72/0 (baseline: 72/0) |
| `cd apps/api && npx tsc -p tsconfig.json --noEmit` | 0 errors |
| `cd apps/web && npx tsc --noEmit -p tsconfig.json` | 0 errors |
| `pnpm --filter @bharatstudio/alerts-api test` | 775/0 (baseline: 775/0) |
| `pnpm --filter @bharatstudio/alerts-web test` | 644/0 (baseline: 643/0 — one new test added: a playbackUrl:null entry renders nothing) |
| `pnpm contracts:validate` | 63 fixtures / 104 paths / 121 operations / 3 negative cases (baseline: 63/104/121) |
| `pnpm explain:check` | 26/26 plans current (baseline: 26/26) — `media-queue.explain.md` re-captured against migration 0148's actual function body against a real seeded database (102 channels, 400 items), not left pointing at the superseded 0146 text |
| `pnpm harness:check` | pass |
| `packages/db/tests/run-l03-application-behavior.sh` (full pipeline: SQL suite + Go integration legs + overlay-wakeup/overlay-cross-replica/channel-store-concurrency/safe-soundboard-caps-not-configured TS integration legs) | pass — 25 SQL files (MAX_MIGRATION unset run), 3 Go suites, 4 TS integration legs, all pass, including the new safe-soundboard-caps-not-configured leg (1/0), confirmed idempotent across repeated runs |

**One unrelated failure observed and NOT part of this task's scope:** the root `pnpm test` script
chains `api test && web test && measurement:test`; `scripts/measurement/run_local_measurement.test.mjs`
fails in this environment because it hard-codes `PATH=/opt/homebrew/bin:/usr/bin:/bin` and expects
Docker to be unavailable there (asserting exit code 2, "blocked") — in this sandbox Docker IS
available, so the script does not hit its expected "blocked" branch. No file under `scripts/` was
touched by this task; `git status` confirms zero changes outside the files this decision record and
its task record list. The api and web legs relevant to this task both passed with the exact counts
above, run independently via `pnpm --filter`.

---

## Docker usage note

All EXPLAIN captures and integration-test verification above were run against real, disposable
postgres:16-alpine containers created and destroyed by this session — never against
`bharatstudio-alerts-postgres-1` or any other long-lived container already running on this machine.
