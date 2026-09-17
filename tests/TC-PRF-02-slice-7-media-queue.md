# TC-PRF-02 slice 7 — Media / Meme Queue (§6 #20): acceptance record

**Date:** 2026-09-17
**Owner:** **Sukhdev Singh**
**Task:** `../active/tasks/PRF-02-slice-7-media-queue.md`
**Decisions:** `../reviews/2026-09-17-prf-02-slice-7-media-queue-implementation.md`
**Binding owner decision:** `../reviews/2026-09-17-remaining-eight-modules-and-youtube-v1-amendment.md` Part 1 §8

Written **before** implementation, per `governance/AGENTS.md`. The "Commands run" table is filled
in after the run, from actual output, and is the single place this slice's numbers live.

---

## Acceptance criteria

### A. Creator-only, and no viewer-submission path exists — the load-bearing property

| ID | Criterion |
|---|---|
| MED20.1 | **No shipped `app_private` function of `0146` contains `submit`, `submission`, `submitter`, `viewer_id`, `approve`, `approval` or `reject`**, asserted structurally against `pg_get_functiondef`. No column on `public.media_queue_items` is named anything resembling a submitter/approval field, asserted against `information_schema.columns`. No second table for a submission/approval queue exists, asserted against `information_schema.tables`. **This is the property the required negative test breaks and restores.** |
| MED20.4 | Only `owner`/`admin` may enqueue, update or change the status of an item — `operator`, `moderator` and `viewer` are all refused (`42501`), and a refused enqueue inserts nothing |
| MED20.11 | None of the four creator-facing functions reads tier or calls an entitlement function (§12.6) — asserted structurally against `pg_get_functiondef` for the tokens `entitled`, `tier_` and `channel_entitlement_versions` |

### B. Field validation — title bound, allow-lists, URL shape, duration

| ID | Criterion |
|---|---|
| MED20.5 | Title must be 1–120 characters (reused verbatim from `0109_v1_l17_paid_challenges.sql:67`) — empty and 121-character titles are refused (`22023`) on both enqueue and update |
| MED20.6 | `media_kind` and `mime_type` are closed allow-lists — an unrecognised kind, `text/html` and `image/svg+xml` are all refused (`22023`) |
| MED20.7 | `storage_url`/`thumbnail_url` must be non-empty, ≤2048 characters and `https://`-prefixed (reused from `0123_v1_l19d_provider_qr_codes.sql:192`) — a `http://` URL is refused (`22023`) |
| MED20.8 | `duration_ms` must be non-negative — `-1` is refused (`22023`) |

### C. Configured-but-unset caps — never invented, enforced only when supplied

| ID | Criterion |
|---|---|
| MED20.9 | With `target_max_duration_ms` unset, any non-negative duration is accepted; with it set, a duration under it is accepted and one over it is refused (`22023`). With `target_max_queue_items` set to the current queued count, one more enqueue is refused (`22023`); one at exactly the (count + 1) cap is accepted |

### D. Cross-channel isolation and not-found

| ID | Criterion |
|---|---|
| MED20.10 | Channel B's owner cannot list, update or change the status of channel A's items — listing returns zero rows, and update/status-change return `P0002` |
| MED20.15 | An unknown item id, on the caller's own channel, is refused with `P0002` on both update and status-change |

### E. FIFO rotation and durable retention

| ID | Criterion |
|---|---|
| MED20.13 | A played or disabled item drops out of the overlay's live rotation but is **retained** in the creator's own durable list forever (§12.6) |
| MED20.14 | The overlay's "current" slot is the OLDEST queued+enabled item (FIFO by `created_at`); marking it played promotes the next-oldest to "current" |

### F. The overlay read — current and next, never a queue depth, aggregate-free

| ID | Criterion |
|---|---|
| MED20.2 | **The returned column set is exactly `{queue_slot, title, media_kind, mime_type, storage_url, thumbnail_url, duration_ms}`** — asserted twice: from `pg_get_function_result`, and from a table materialised out of a live call and read back through `information_schema.columns`. Adding ANY column turns this file red by name |
| MED20.3 | No identifying token (`viewer`, `anonymous`, `ip_address`, `remote_addr`, `submitter`, `submission`, `approve`, `reject`) exists on the overlay read's shipped function definition |
| — | The overlay read returns **AT MOST TWO rows** regardless of how many items are queued — verified directly against a channel holding three live items, reusing `support-theater-module.ts:68-72`'s "current and next" bound rather than inventing a number |
| MED20.12 | A wrong-fingerprint token, an unrecognised overlay id, and an expired overlay session each return **zero rows** |

### G. API, contracts and canvas

| ID | Criterion |
|---|---|
| — | Creator routes are session-authenticated, 404 (never 403) for a non-member/forbidden write, 503 when the store is absent |
| — | The overlay route returns 200 with `mediaQueue: []` for an unrecognised token, 401 only for a MISSING bearer token |
| — | A request body carrying `submitterId`, `submittedBy`, `viewerId`, `approved`, `approvalStatus` or `rejectionReason` is refused with 400 by AJV's `additionalProperties: false` **before the store is ever called** — verified directly against the store never being invoked |
| — | A `status` value of `approved`, `rejected`, `pending_review` or `submitted` is refused with 400 by the enum itself, before the store is ever called |
| — | `contracts/validate-fixtures.mjs` and `contracts/validate-openapi.mjs` accept all three new fixtures against their schemas and the full OpenAPI document |
| — | The canvas module is registered on the ONE existing connection and the ONE existing rAF loop as module thirteen of thirteen — no second session, no second transport, no timer of its own |
| — | `render()` writes only `opacity`, `transform` and element `src`/`poster`/text attributes (PRF-03); the rendered subtree contains no `script`, `iframe`, `link`, `style`, `object` or `embed` element, verified directly against the DOM |
| — | The `'next'` entry is loaded only into the hidden, permanently-invisible preload elements and never into the visible current elements, verified directly against the DOM |

---

## The required negative test

Applied, its failure observed, and the file restored **byte-identical** (verified by `sha256sum`
before and after, and by `diff` returning empty).

| # | Property | Mutation | Expected |
|---|---|---|---|
| 1 | **No viewer-submission path** — no shipped function may contain a `viewer_id` (or `submit`/`submission`/`submitter`/`approve`/`approval`/`reject`) token | Added a `declare`-block comment containing the word `viewer_id` inside `app_private.enqueue_media_queue_item`'s plpgsql body (between its `declare` and `begin`, and PostgreSQL's `pg_get_functiondef` reproduces `prosrc` verbatim, comments included, for a `language plpgsql` body — unlike file-level migration comments, which never enter `prosrc` at all) | FAILED, by name, on MED20.1's structural token scan |

**The four outputs.**

1. Pre-mutation hash: `sha256 aa41d36d915afa28994cb436a61d1e86c6cac704469d91e78ccf2874f7c0eb62`
   (`packages/db/migrations/0146_v1_prf02_media_queue.sql`).
2. Mutation applied: inserted the line
   `  -- INJECTED FOR MED20.1 NEGATIVE-TEST EVIDENCE (removed before commit): a`
   `  -- viewer_id concept must never appear inside a shipped function body.`
   inside `enqueue_media_queue_item`'s `declare` block.
3. Test result against a freshly migrated database (roles + all migrations through `0146` + `00_base_world.sql`,
   then `prf02_slice7_media_queue.sql` run directly): the run stopped on the first `do $$ ... $$`
   block (`MED20.1`), verbatim:

```
ERROR:  app_private.enqueue_media_queue_item contains a "viewer_id" token -- Media / Meme Queue is CREATOR-ONLY (owner decision, 2026-09-17): no submission endpoint, no approval queue, no moderation queue, no rejection reason, no submitter identity field may ever exist
CONTEXT:  PL/pgSQL function inline_code_block line 19 at RAISE
```

4. Restored byte-identical: `sha256 aa41d36d915afa28994cb436a61d1e86c6cac704469d91e78ccf2874f7c0eb62`
   (matches step 1 exactly), confirmed additionally by `diff` returning no output and by re-running
   the full SQL suite afterward (`SQL SUITE: pass=68 fail=0`).

**MED20.1's assertion was WRITTEN for this slice**, because no existing test in this repository
could catch a viewer-submission path being added later — every other structural scan in this
codebase (e.g. `0142`'s no-chance-mechanic scan) checks for a different vocabulary entirely. It
scans every shipped `app_private` function definition from `pg_get_functiondef` for `submit`,
`submission`, `submitter`, `viewer_id`, `approve`, `approval` and `reject`, and fails by function
name — with two further, independent structural checks against `information_schema.columns` and
`information_schema.tables` so a forbidden concept introduced as a COLUMN or a second TABLE, rather
than inside a function body, is caught too.

---

## Commands run

Filled in from actual output after the run.

| Command | Exact result line |
|---|---|
| `sh packages/db/tests/run-sql-suite.sh` | `SQL SUITE: pass=68 fail=0` (was 67 before this slice; `PASS prf02_slice7_media_queue`) |
| `pnpm --filter @bharatstudio/alerts-api build` (typecheck) | exits 0, no output |
| `pnpm --filter @bharatstudio/alerts-api test` | `ℹ tests 707` · `ℹ pass 707` · `ℹ fail 0` (was 692; +15 new route tests in `prf02-slice7-media-queue-routes.test.ts`) |
| `npx tsc --noEmit -p apps/web/tsconfig.json` (typecheck) | exits 0, no output |
| `pnpm --filter @bharatstudio/alerts-web test` | `ℹ tests 577` · `ℹ pass 577` · `ℹ fail 0` (was 560 before slice 6/7; +8 logic tests, +8 module tests, +1 integration test since slice 6's 560) |
| `pnpm explain:check` | `OK: every app_private call ... is present in required-queries.json (22 manifest entries, 9 exemptions)` then `OK: 22/22 plans current` (was 21/21) |
| `pnpm contracts:validate` | `Validated 53 fixtures ...` (was 50) · `Validated OpenAPI 3.1 document with 92 paths, 105 operation contracts ...` (was 88 paths / 100 operations) · `Validated 3 negative OpenAPI operation-contract cases.` |
| `node .github/scripts/api-test-harness-check.mjs` | `API test harness check: all checks passed against current code.` |

**Grep proof for MED-20 (no-viewer-submission), run over this slice's own diff:**
`git diff -- <changed files> \| grep -niE "submit\|submission\|submitter\|viewer_id\|approve\|approval\|reject"`
returns matches **only** inside comments/documentation and inside AJV/JSON-Schema bodies that
explicitly REJECT such a field with 400 (`additionalProperties: false` schemas in
`apps/api/src/routes/media-queue.ts` and the OpenAPI/JSON-Schema contracts) — never as an actual
SQL column, TypeScript field, function name, route path or object key anywhere in the diff.

---

**Local verification only.** Nothing here is production, provider, store, legal, device, network or
release readiness. `RT-07` remains `Blocked`; the EXPLAIN artefact
(`packages/db/explain-plans/media-queue.explain.md`) is a plan-shape change detector captured
against a minimally-seeded local database (102 channels, 400 media queue items, 100 overlay
sessions), not §37.4 production-scale evidence.
