# TC-PRF-02 slice 6 — Reaction Cloud (§6 #5) and PRF-06 reactions: acceptance record

**Date:** 2026-09-16, **amended 2026-09-17** (the reaction rate limit moved from the channel
to the sender — section B is rewritten and section H is new)
**Owner:** **Sukhdev Singh**
**Task:** `../active/tasks/PRF-02-slice-6-reaction-cloud.md`
**Decisions:** `../reviews/2026-09-16-prf-02-slice-6-reaction-cloud-decisions.md`
**Amending decisions (2026-09-17):** `../reviews/2026-09-17-prf-02-reaction-sender-rate-limit-decisions.md`
**Binding owner decisions:** `../reviews/2026-09-16-prf-02-slice-6-owner-decisions.md` 1 and 2,
as amended by the owner's 2026-09-17 direction (per-sender, not per-channel)

Written **before** implementation, per governance/AGENTS.md. The "Commands run" table is
filled in after the run, from the actual output, and is the single place this slice's numbers
live.

---

## Acceptance criteria

### A. Schema and the send path (`packages/db/migrations/0139_v1_prf02_prf06_reaction_sampling.sql`)

| ID | Criterion |
|---|---|
| S6.1 | A reaction can be sent for an enabled, tier-eligible **platform catalogue** entry and is recorded |
| S6.2 | A reaction can be sent for an enabled, active, in-limit **creator pack** entry and is recorded |
| S6.3 | An unknown entry id is rejected (`unknown_entry`), nothing inserted |
| S6.4 | A creator-**disabled** catalogue entry is rejected (`not_available`), nothing inserted |
| S6.5 | A tier-**ineligible** catalogue entry is rejected (`not_available`), nothing inserted |
| S6.6 | Another channel's creator-pack entry is rejected (`unknown_entry`), nothing inserted |
| S6.7 | An unrecognised `entry_source` raises rather than silently choosing one |
| S6.8 | `channel_reaction_sends` accepts exactly one of `sticker_id` / `pack_sticker_id` — both, or neither, violates a check constraint |

### B. Rate limiting — PER SENDER, 60/minute (owner direction, 2026-09-17)

**S6.9–S6.14 as written on 2026-09-16 are WITHDRAWN.** They asserted the per-channel cap that
the owner has now removed; re-stating them would be asserting the bug. They are replaced
one-for-one below, keeping the same IDs so nothing in the register dangles.

| ID | Criterion |
|---|---|
| S6.9 | The **61st** send by one sender inside a one-minute window returns `rate_limited` and inserts nothing; the first 60 are recorded |
| S6.10 | The window is one minute: back-dating `window_started_at` past `interval '1 minute'` lets the next send through and resets the counter to 1 |
| S6.11 | **There is no per-channel cap at all.** A channel with `queue.rateLimitPerMinute = 1` configured still accepts far more than one reaction in a minute, because reactions no longer read channel configuration |
| S6.12 | **A different sender in the same channel is unaffected** by another sender's exhausted budget — the whole point of the change, proven rather than asserted |
| S6.13 | A send with **no resolvable sender identity** returns `sender_unidentified`, inserts nothing, and is refused **before** any catalogue-eligibility check runs |
| S6.14 | The shipped function definition contains `interval '1 minute'` and the literal `60`, and contains **neither** `rateLimitPerMinute` **nor** `rateLimitPerMin` — asserted against `pg_get_functiondef`, so the channel cap cannot come back unnoticed |
| S6.44 | The sender key resolves through the **existing** anonymous browser identity: a fingerprint known to `anonymous_browser_identities` keys on its `viewer_identities` row, and one claimed into an account keys on the **account's** identity, so a claimed viewer's several browsers share one budget |
| S6.45 | `app_private.resolve_reaction_sender_key` **never inserts**: resolving an unknown fingerprint leaves `anonymous_browser_identities` and `viewer_identities` row counts unchanged and falls back to the opaque `token:` key |
| S6.46 | `public.reaction_sender_rate_limits` has **exactly three columns** — `sender_key`, `window_started_at`, `send_count` — and no `channel_id`, entry, per-send timestamp or any other column, so the limiter row cannot record what a viewer sent or to whom |
| S6.47 | `public.channel_reaction_sends` is **unchanged by `0141`**: still no viewer, anonymous-token, session or IP column, and the send is still recorded without any sender value |
| S6.48 | `app_private.list_overlay_reaction_cloud` still declares **exactly** `(entry_source text, entry_id uuid, display_name text, reaction_count bigint)` after `0141` — asserted unchanged |
| S6.49 | `public.channel_reaction_rate_limits` and the three-argument `record_channel_reaction(uuid, text, uuid)` **no longer exist** after `0141` |

### C. The overlay read — server-side sampling, bounded, non-identifying

| ID | Criterion |
|---|---|
| S6.15 | A valid overlay session returns one row per distinct entry with its exact count, ordered `count desc, display_name asc, entry_id asc` |
| S6.16 | **The returned column set is exactly `{entry_source, entry_id, display_name, reaction_count}`** — asserted twice: from `pg_get_function_result`, and from a table materialised out of a live call and read back through `information_schema.columns` |
| S6.17 | A bad, foreign, expired or revoked overlay token returns **zero rows** |
| S6.18 | Reactions older than the one-minute window are not counted |
| S6.19 | A cross-channel reaction is never counted |
| S6.20 | **Sampling is server-side:** with a ceiling of `k` passed, the function returns at most `k` rows even when more distinct entries have reactions, and the rows it returns are the top `k` by count |
| S6.21 | A `null` ceiling imposes no limit — every distinct entry comes back |
| S6.22 | A ceiling below 1 fails closed (zero rows), never open |
| S6.23 | The shipped function definition contains no viewer-identifying token at all — asserted against `pg_get_functiondef` |

### D. API

| ID | Criterion |
|---|---|
| S6.24 | `POST /v1/public/channels/:handle/reactions` returns `201` on a recorded reaction |
| S6.25 | It returns `429 reaction_rate_limited` when the store says `rate_limited` |
| S6.26 | It returns `400 unknown_reaction_entry` / `403 reaction_entry_not_available` for the two rejection outcomes |
| S6.27 | It returns `404` for an unknown handle and `503` when the store is unwired |
| S6.28 | With Turnstile required and no/invalid token it returns `403 bot_verification_required` — the existing envelope, unchanged |
| S6.29 | An undeclared body property is **rejected** (`additionalProperties: false`), proven under `createTestFastify` so the test validates under the server's own AJV rules |
| S6.30 | `GET /v1/overlay-widgets/:overlayId/reaction-cloud` returns `401` without a bearer token, `503` when unwired, and `200 { entries: [...] }` otherwise |
| S6.31 | The route projects a **second, independent** time: a store that hands up an extra field cannot put it in the response |
| S6.50 | The route obtains the sender fingerprint **exactly** the way the two public checkout POSTs do: it reads `__Host-bsa-anonymous`, mints one with `randomBytes(32).toString('base64url')` and sets the same cookie header when absent, and passes **only** the SHA-256 hex hash to the store |
| S6.51 | The route answers `400 reaction_sender_unidentified` (`retryable: false`) when the store says `sender_unidentified` — never a silent accept, and never a per-IP fallback |
| S6.52 | The sender fingerprint appears in **no** response body, **no** log line and **no** metric label |

### E. Canvas renderer

| ID | Criterion |
|---|---|
| S6.32 | The module registers on the **ONE** existing `MasterCanvasConnection` and the **ONE** existing rAF loop — no second session, no second transport, no timer of its own |
| S6.33 | `render()` writes only `transform` and `opacity` — enforced by `node .github/scripts/canvas-static-check.mjs`, not by review |
| S6.34 | The DOM is bounded: a fixed recycled pool of glyph elements, never one node per reaction |
| S6.35 | The guard rejects any payload carrying a key it does not expect, including a viewer identifier |
| S6.36 | An empty cloud renders nothing (`opacity: 0`), and hides again when the cloud empties — it does not latch |
| S6.37 | Registered in the canvas host page's `BUILT_MODULE_KEYS` and never activated unless the entitlement endpoint returns `reaction_cloud` |
| S6.38 | The canvas integration test proves all ten modules still share one connection and one loop |

### F. Contracts and RT-12

| ID | Criterion |
|---|---|
| S6.39 | OpenAPI carries both paths and their component schemas; `pnpm contracts:validate` passes |
| S6.40 | The published response schema **refuses** every viewer-identifying field by name — `viewerId`, `viewerIdentityId`, `anonymousIdentityId`, `sessionId`, `ipAddress`, `createdAt`, `sentAt`, `lastReactionAt` |
| S6.41 | `packages/db/explain-plans/required-queries.json` carries `app_private.list_overlay_reaction_cloud` and its artefact exists; `pnpm explain:check` passes |
| S6.42 | `pnpm harness:check` passes — no `apps/api/test/` file constructs a bare `Fastify()` |

### G. The negative test the task requires, run explicitly

| ID | Criterion |
|---|---|
| S6.43 | Adding a viewer-identifying column to `list_overlay_reaction_cloud`'s returned set makes `packages/db/tests/prf02_slice6_reaction_cloud.sql` **fail by name**, and removing it makes it pass again. Both outputs recorded in the implementation report |
| S6.53 | **(2026-09-17)** Raising the per-sender ceiling from 60 so the 61st send is accepted makes the same SQL file **fail by name**; restoring it byte-identically makes it pass. Proves the limit is enforced, not described |

---

## Commands run — real counts, this worktree, 2026-09-16

| Command | Result line |
|---|---|
| `pnpm db:test:all` | `SQL SUITE: pass=64 fail=0` (includes `PASS prf02_slice6_reaction_cloud`) |
| `pnpm --filter @bharatstudio/alerts-api test` | `ℹ tests 642 · ℹ pass 642 · ℹ fail 0` |
| `pnpm --filter @bharatstudio/alerts-web test` | `ℹ tests 502 · ℹ pass 502 · ℹ fail 0` |
| `pnpm --filter @bharatstudio/alerts-api build` | `tsc -p tsconfig.json` — no output, exit 0 |
| `pnpm contracts:validate` | `Validated 44 fixtures ...` / `Validated OpenAPI 3.1 document with 76 paths, 84 operation contracts, and all local $ref targets.` / `Validated 3 negative OpenAPI operation-contract cases.` |
| `pnpm explain:check` | `OK: every app_private call found by rule 1 ... rule 3 (composition-root derived-read scan, 12 wired declaration(s) resolved and scanned) is present in required-queries.json (19 manifest entries, 9 exemptions)` / `OK: 19/19 plans current` |
| `pnpm harness:check` | `API test harness check: all checks passed against current code.` |
| `node .github/scripts/canvas-static-check.mjs` | `PRF-03/PRF-04 canvas static check: all checks passed against current code.` |

### S6.43 — the non-identifying negative test, run explicitly

`app_private.list_overlay_reaction_cloud`'s declared result was temporarily widened to
`(entry_source, entry_id, display_name, reaction_count, viewer_identity_id uuid)`, with
`viewer_identity_id` selected as `(array_agg(send.id))[1]` — a per-send row id, exactly the kind
of value §6 #5 forbids on this surface. `packages/db/tests/prf02_slice6_reaction_cloud.sql` was
then run against a freshly migrated database:

```
RESULT: FAIL prf02_slice6_reaction_cloud
ERROR:  the overlay reaction-cloud read must return catalogue entry ids and counts and nothing
        else (§6 #5: non-identifying, enforced as a property of the query). Declared result is
        "TABLE(entry_source text, entry_id uuid, display_name text, reaction_count bigint,
        viewer_identity_id uuid)", expected exactly "TABLE(entry_source text, entry_id uuid,
        display_name text, reaction_count bigint)"
CONTEXT:  PL/pgSQL function inline_code_block line 13 at RAISE
```

The column was then removed and the same test re-run against a freshly migrated database:

```
RESULT: PASS prf02_slice6_reaction_cloud
 prf02_slice6_reaction_cloud: all cases passed
```

The restored function body hashes to
`b8d58671d0559da00418427be6fecf85e1a087e459ecf2b644f48414e59beb62`, which is the `query_hash`
recorded in `packages/db/explain-plans/reaction-cloud.explain.md` — so the restore is
byte-identical to the captured artefact, not merely behaviourally equivalent, and
`pnpm explain:check` passes afterwards.

### What these runs are not

Local checks in one worktree. Nothing here is production, provider, store, legal, device, network
or release readiness. The EXPLAIN artefact is a plan-shape change detector captured against a
small local database (two channels, five catalogue entries, 810 reaction rows); §19.4's budgets
stay unclaimed and RT-07 stays Blocked. No independent review occurred.


---

## Commands run — 2026-09-17 amendment (per-sender rate limit), this worktree

| Command | Result line |
|---|---|
| `pnpm db:test:all` | `SQL SUITE: pass=66 fail=0` (includes `PASS prf02_slice6_reaction_cloud`) |
| `pnpm --filter @bharatstudio/alerts-api test` | `ℹ tests 673 · ℹ pass 673 · ℹ fail 0` |
| `pnpm --filter @bharatstudio/alerts-web test` | `ℹ tests 537 · ℹ pass 537 · ℹ fail 0` |
| `pnpm --filter @bharatstudio/alerts-api build` | `tsc -p tsconfig.json` — no output, exit 0 |
| `pnpm contracts:validate` | `Validated 47 fixtures ...` / `Validated OpenAPI 3.1 document with 81 paths, 91 operation contracts, and all local $ref targets.` / `Validated 3 negative OpenAPI operation-contract cases.` |
| `pnpm explain:check` | `OK: every app_private call found by rule 1 ... rule 3 (composition-root derived-read scan, 13 wired declaration(s) resolved and scanned) is present in required-queries.json (20 manifest entries, 9 exemptions)` / `OK: 20/20 plans current` |
| `pnpm harness:check` | `API test harness check: all checks passed against current code.` |

The passing run is the positive proof of S6.9 and S6.12 together: sender B's first
**60** sends are recorded and sends **61–65 are all refused**, and then a **different** sender,
on the **same** channel, inside the **same** window, has **10 further sends accepted** while
sender B stays refused. Channel C carries `queue.rateLimitPerMinute = 1` throughout and still
takes 70 reactions in that minute (S6.11) — under the old per-channel cap it would have taken
one.

### S6.53 / S6.12 — the per-sender limit is enforced, proven by breaking it twice

**Break 1 — raise the ceiling** so the 61st send is accepted
(`if window_count > 60` → `> 61` in `0141`):

```
FAIL prf02_slice6_reaction_cloud
ERROR:  the per-sender limit must allow exactly 60 sends in one window, got 65
```

**Break 2 — collapse every sender onto one key** (`'token:' || target_token_hash` →
`'token:shared'`), which is behaviourally the channel-level cap the owner removed:

```
FAIL prf02_slice6_reaction_cloud
ERROR:  the per-sender limit must allow exactly 60 sends in one window, got 31
```

Break 2 reproduces the exact failure the owner described: with a shared budget, one sender's
earlier traffic (31 sends elsewhere in the fixture) eats another sender's allowance, and the
second sender is refused after 31 instead of 60.

`0141` was restored from its pre-break copy after each break and hashes to
`a7255eb9a5d3520be731dac9dc3d2a25dc78bbb640d38bd7cc37af5ce9345303` — byte-identical, not
merely behaviourally equivalent — after which `pnpm db:test:all` returns
`SQL SUITE: pass=66 fail=0` again.

### S6.48 — the overlay projection still cannot return a sender identifier

`app_private.list_overlay_reaction_cloud` was temporarily redefined with `0139`'s exact body
plus a fifth column, `sender_key text`, selected straight out of
`public.reaction_sender_rate_limits` — that is, a real attempt to leak the admission-control
key through the overlay read. Against a freshly migrated database:

```
FAIL prf02_slice6_reaction_cloud
ERROR:  the overlay reaction-cloud read must return catalogue entry ids and counts and nothing
        else (§6 #5: non-identifying, enforced as a property of the query). Declared result is
        "TABLE(entry_source text, entry_id uuid, display_name text, reaction_count bigint,
        sender_key text)", expected exactly "TABLE(entry_source text, entry_id uuid,
        display_name text, reaction_count bigint)"
```

The widened definition was removed, `0141` restored to the same hash above, and the suite
returns `SQL SUITE: pass=66 fail=0`.

### What the 2026-09-17 runs are not

Local checks in one worktree. Nothing here is production, provider, store, legal, device,
network or release readiness. No independent review occurred. **Retention for
`channel_reaction_sends` remains undecided**, and removing the per-channel cap means reaction
write volume now scales with audience size — a named open question for the owner, not a
technical default to be filled in by an implementer.
