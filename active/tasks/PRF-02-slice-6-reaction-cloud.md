# PRF-02 slice 6 — Reaction Cloud (§6 catalogue module #5) and PRF-06 server-side sampling and rate limiting

**Status:** `Conditionally complete — implemented and locally verified; AMENDED 2026-09-17 (the reaction rate limit moved from the channel to the sender); independent review unavailable; no register state letter assigned`
**Owner:** **Sukhdev Singh**
**Classification:** L3 (new database objects, a new public/unauthenticated write path, a new overlay read path)
**Authority:** `../../FULL-PRODUCT-DEFINITION.md` §6 module #5, §9.1.1, §12.7, §19.5, §30.3, HUB-07, PRF-06
**Binding owner decisions:** `../../reviews/2026-09-16-prf-02-slice-6-owner-decisions.md` decisions 1 and 2
**Predecessor scope review:** `../../reviews/2026-09-16-prf-02-slice-5-scope-review.md` (classified #5 `BLOCKED-DECISION`; decisions 1 and 2 are what unblocked it)
**Acceptance record:** `../../tests/TC-PRF-02-slice-6-reaction-cloud.md`
**Decision record:** `../../reviews/2026-09-16-prf-02-slice-6-reaction-cloud-decisions.md`
**Amending decision record (2026-09-17):** `../../reviews/2026-09-17-prf-02-reaction-sender-rate-limit-decisions.md`
— supersedes the rate-limit half of owner decision 2 and D6 of the 2026-09-16 record. **Read it
before this file's rate-limit paragraphs; where the two disagree, the 2026-09-17 record wins.**
**Parent task:** `PRF-02.md` (slices 1–5). This slice is recorded in its own file rather than
appended to `PRF-02.md` because a concurrent agent owns migration `0138` and that file.

**No register state letter is assigned by this task.** PRF-02 and HUB-07 letters are decided
after audit, by the owner, not by an implementer.

---

## What is being built

A complete vertical slice of §6 catalogue module #5, **Reaction Cloud**, plus the PRF-06
obligation it depends on ("Server-side sampling and rate limiting for reactions and chat",
`v1`, `A`, P0) for the reactions half only. Chat is untouched and stays out.

| Layer | Object |
|---|---|
| Schema | `packages/db/migrations/0139_v1_prf02_prf06_reaction_sampling.sql` — **migration number assigned to this task; `0138` belongs to a concurrent agent and is never written or renumbered here** |
| Schema (2026-09-17 amendment) | `packages/db/migrations/0141_v1_prf02_reaction_sender_rate_limit.sql` — forward migration only. `0139` is applied and is **never edited** |
| Send path | `app_private.record_channel_reaction(uuid, text, uuid, text)` — rate-limited **per sender** in SQL (60/minute). The fourth argument is the SHA-256 fingerprint of the existing anonymous browser token; the raw token never reaches the database |
| Sender key | `app_private.resolve_reaction_sender_key(text)` — reads `anonymous_browser_identities` / `viewer_identities` (`0084`, `0124`); **never inserts** |
| Overlay read | `app_private.list_overlay_reaction_cloud(uuid, text, integer)` — sampled and aggregated server-side |
| API | `POST /v1/public/channels/:handle/reactions` (public, unauthenticated) and `GET /v1/overlay-widgets/:overlayId/reaction-cloud` (overlay session bearer token) |
| Contracts | OpenAPI paths and component schemas, JSON-Schema, fixtures, negative privacy cases in `contracts/validate-fixtures.mjs` |
| RT-12 | `packages/db/explain-plans/reaction-cloud.explain.md` and a `required-queries.json` entry |
| Canvas | `apps/web/app/overlay/canvas/modules/reaction-cloud-logic.ts` and `reaction-cloud-module.ts`, registered on the ONE existing connection and the ONE existing rAF loop |
| Tests | SQL, API route, renderer, pure-logic and canvas-integration layers |

---

## The owner decisions this slice is bound by

Quoted as constraints. None was decided by this implementer, and none is extended here.

1. **A reaction is a send of an entry from the EXISTING curated sticker catalogue** —
   `sticker_catalogue_entries` (migration `0110`) plus staff-reviewed creator packs
   (`creator_sticker_packs`, migration `0119`, reviewed by `0122`/`0125`). No reaction
   catalogue, no asset, no upload path, no change to how packs are reviewed.
2. ~~**Rate limiting reuses the built mechanism** — the per-channel, creator-configurable
   `rateLimitPerMinute` …~~ **SUPERSEDED 2026-09-17.** The owner replaced this: *"all these
   should not be limited at channel level bcs then we are limiting money for them these
   should be limited at sender/user level to avoid misuse or attacks, so plan a safe number
   for user - for creator dont limit it too much that with higher viewer etc they dont face
   issue."* The per-channel cap is **removed entirely** — a creator's reaction throughput
   must scale with their audience — and the limit is now **60 sends per minute per sender**,
   keyed on the existing anonymous browser identity. `rateLimitPerMinute` goes back to
   meaning only what it always meant: the creator's alert-source setting. See
   `../../reviews/2026-09-17-prf-02-reaction-sender-rate-limit-decisions.md` R1–R4.
3. **The canvas display ceiling ships "configured but unset"** — the mechanism is built, the
   value is read from configuration, and unset means today's behaviour. Never a guessed
   default.
4. **No number may be invented.** Any numeric limit that is neither a configured-but-unset
   value nor a figure the owner decided or explicitly delegated stops the work and is
   reported. The 60/minute per-sender figure is an **owner-delegated** choice ("plan a safe
   number for user"), anchored to `POST /v1/public/channels/:handle/paid-votes`, the closest
   public-write sibling, which already uses `max: 60, timeWindow: '1 minute'`.

---

## Hard constraints, each visible in code rather than in a comment

- **Sampling is SERVER-SIDE (§19.5).** The overlay read itself returns at most the sample.
  The client never receives the full stream and then drops some. The projection is an
  aggregate — `count(*)` grouped by catalogue entry — so per-event rows cannot leave the
  database on this path at all, and the row count is capped by the configured ceiling
  inside the security-definer function.
- **§12.7 bounded data.** The overlay read returns a bounded set, never a history: at most
  one row per catalogue entry reachable by the channel, over the same already-decided
  one-minute window, ordered deterministically and capped by the ceiling when it is set.
- **"Non-identifying" is a property of the QUERY (§6 #5).** The overlay projection returns
  catalogue entry ids, their already-public display names, and counts. No viewer id, no
  anonymous identity, no session id, no IP, and **no timestamp of any precision at all** —
  the returned column set is asserted in the SQL acceptance test.
- **§9.1.1.** No third-party code runs on the overlay. The module's options are plain values
  and function references; the type has no slot for a URL, HTML, CSS or a script.
- **No tier gate on storing, viewing, searching, fetching or exporting a durable creator
  record.** Reactions are free at every tier (§30.3: "Free reactions, supporter wall —
  yes/yes/yes/yes"). The only gate is the pre-existing §30.3 module cap in migration `0131`,
  which governs how many Canvas modules a tier may activate and is untouched here.

---

## Authentication of the send path

Recorded here because it is a question the task asked to be answered rather than assumed.

**Viewers are not authenticated to send a reaction, and no new authentication model is
introduced.** The surface a reaction is sent from is the public tip page
(`apps/web/app/tips/[handle]`), which is unauthenticated by construction — the same surface
that already carries the public sticker picker (`GET /v1/public/channels/:channelId/stickers`,
migration `0110`'s `list_public_stickers_for_channel`, explicitly "no auth/role check (the tip
page is unauthenticated)").

Requiring a viewer account would also contradict two decided things at once: §30.3 makes free
reactions available at every tier, and §6 #5 requires the surface to be non-identifying — an
account is an identity.

**What is reused instead**, both already built, neither invented here:

- **`PublicAbuseGuard`** (`apps/api/src/domain/public-abuse.ts`, Cloudflare Turnstile),
  behind the SAME existing `publicPaymentTurnstileRequired` configuration flag and returning
  the SAME `403 bot_verification_required` envelope the two public payment POSTs already use
  (`apps/api/src/routes/public.ts:306` and `:606`). No new flag, no new secret, no new
  envelope.
- **The anonymous-identity cookie flow the two public checkout POSTs already use** —
  `anonymousTokenFromCookie` / `anonymousCookie` / `anonymousTokenHash` in
  `apps/api/src/routes/public.ts`. The reaction route performs the **identical** three steps
  (read `__Host-bsa-anonymous`; mint with `randomBytes(32).toString('base64url')` and set the
  same cookie header when absent; SHA-256 it and pass only the hash onward). No second
  identity mechanism, cookie, header or fingerprint is introduced, and the raw token still
  never enters the database.
- **The per-sender one-minute rate limit in SQL** (60/minute), which is the 2026-09-17
  owner decision's mechanism.

No Fastify route rate limit is attached to this route. The per-sender SQL limit is the
reaction-specific figure; the pre-existing global `@fastify/rate-limit` registration in
`apps/api/src/app.ts` (120/minute, IP-keyed) continues to apply to this route as it does to
every other, unchanged by this work.

---

## Failure behaviour, kill switch, rollback

**Failure behaviour**

- **Rate limit reached.** `record_channel_reaction` returns `rate_limited`; the route answers
  `429` with `reaction_rate_limited` and `retryable: true`. Nothing is inserted. The limit is
  **per sender** and per one-minute window: 60 sends. A different sender on the same channel
  is unaffected, and there is no channel budget at all.
- **No resolvable sender identity.** `record_channel_reaction` returns
  `sender_unidentified` **before any catalogue-eligibility check runs**, and the route
  answers `400 reaction_sender_unidentified` with `retryable: false`. It is **not** silently
  accepted, and it does **not** fall back to the global per-IP limit — a fallback would make
  cookie-dropping the cheapest route to the weaker limit. Unreachable in the ordinary flow,
  because the route mints the cookie when none is present.
- **Channel configuration no longer affects reactions at all.** `rateLimitPerMinute` and its
  legacy `rateLimitPerMin` alias are not read by the reaction path; the SQL acceptance file
  asserts their **absence** from the shipped function definition.
- **An unknown, disabled, tier-ineligible or other-channel catalogue entry.** Rejected with a
  distinct outcome, never silently dropped and never inserted. A viewer can only ever send an
  id that the channel's own live enabled+eligible set contains at the moment of the send.
- **A bad, revoked, expired or foreign overlay token.** `list_overlay_reaction_cloud` returns
  **zero rows** — the `overlay_sessions` row is the outer `FROM`, the same shape every other
  `list_overlay_*` function uses. The route answers `200` with an empty `entries` array; the
  module renders nothing.
- **The store is unwired or a query throws.** `503` with `retryable: true` — never a `500`,
  never a `401` (which would misreport an outage as an auth failure), never a leaked error
  string.
- **The module throws twice.** The runtime's existing generic per-module error boundary
  (unchanged since slice 1) marks it `down`; every other module keeps rendering on the same
  loop.
- **The entitlement endpoint never returns `reaction_cloud`.** PRF-02.10's existing rule,
  unchanged: never activated, never subscribed, never fetched, never rendered.

**Kill switch:** the server-owned module toggle, same as every other Canvas-only module.
Disabling the `reaction_cloud` row via `app_private.upsert_master_canvas_module` (unchanged
from slice 1) removes it from `list_overlay_master_canvas_modules`'s answer and the runtime
never activates it. Separately, a creator who disables every sticker for their channel leaves
the send path with nothing sendable — the existing `channel_sticker_disables` control, reused,
not duplicated.

**Rollback:**

- Delete `apps/web/app/overlay/canvas/modules/reaction-cloud-logic.ts`,
  `reaction-cloud-logic.test.ts`, `reaction-cloud-module.ts`, `reaction-cloud-module.test.ts`;
  `apps/api/src/domain/reaction-cloud-store.ts`;
  `apps/api/src/db/reaction-cloud-overlay-store.ts`; `apps/api/src/db/reaction-send-store.ts`;
  `apps/api/test/prf02-slice6-reaction-cloud-routes.test.ts`;
  `packages/db/tests/prf02_slice6_reaction_cloud.sql`;
  `packages/db/explain-plans/reaction-cloud.explain.md`;
  `contracts/json-schema/overlay-reaction-cloud-response.schema.json`;
  `contracts/json-schema/public-reaction-send-response.schema.json`;
  `contracts/fixtures/overlay-reaction-cloud-response.json`;
  `contracts/fixtures/public-reaction-send-response.json`.
- Revert the additive hunks in `apps/api/src/app.ts`, `apps/api/src/index.ts`,
  `apps/api/src/config.ts`, `apps/api/src/routes/master-canvas.ts`,
  `apps/api/src/routes/public.ts`,
  `apps/web/app/overlay/canvas/[overlayId]/page.tsx`,
  `apps/web/app/overlay/canvas/master-canvas-integration.test.ts`,
  `contracts/openapi/v1.yaml`, `contracts/validate-fixtures.mjs` and
  `packages/db/explain-plans/required-queries.json`.
- Migration `0139` is additive-only: two new tables, two new functions, two new indexes, and
  **no alteration of any existing table, column, constraint, trigger, function or row**.
  Reversible with `drop function app_private.list_overlay_reaction_cloud(uuid, text, integer);`,
  `drop function app_private.record_channel_reaction(uuid, text, uuid);`,
  `drop table public.channel_reaction_sends;` and
  `drop table public.channel_reaction_rate_limits;`.
  **No production migration without separate explicit approval.**
- Migration `0141` (2026-09-17) is a **forward migration**; `0139` is applied and is not
  edited. It drops `public.channel_reaction_rate_limits` and the three-argument
  `record_channel_reaction`, and creates `public.reaction_sender_rate_limits`,
  `app_private.resolve_reaction_sender_key(text)` and the four-argument
  `record_channel_reaction`. It does **not** touch `public.channel_reaction_sends` or
  `app_private.list_overlay_reaction_cloud` — the stored reaction and the overlay projection
  are byte-for-byte what `0139` shipped. Rollback is `0139`'s own definitions re-applied after
  `drop function app_private.record_channel_reaction(uuid, text, uuid, text);`,
  `drop function app_private.resolve_reaction_sender_key(text);` and
  `drop table public.reaction_sender_rate_limits;`. The only data lost is in-flight
  one-minute counters, which are not a record of anything.
  **No production migration without separate explicit approval.**

---

## Boundaries

**In scope:** everything in the table at the top of this file.

**Explicitly out of scope, not touched:**

- **Chat.** PRF-06 names "reactions and chat"; §6 #19 (Chat) is `BLOCKED-EXTERNAL` in the
  slice-5 review and §9.1.1 forbids the embed inside the Canvas. Only the reactions half is
  built.
- **Any new sticker, asset, upload path, or change to pack review.** Owner decision 1's
  explicit exclusion.
- ~~**Any per-viewer rate limit or per-viewer figure.**~~ **REVERSED 2026-09-17** — the
  per-sender limit is now the whole mechanism. Still out of scope: any **IP-keyed** reaction
  limit (CGNAT makes it refuse genuine viewers as a group), any new identity mechanism, and
  any change to the pre-existing global `@fastify/rate-limit` registration.
- **Retention or deletion of reaction rows.** Choosing a retention period is choosing a
  number nobody decided. Referred, below.
- **The tip page's reaction sender UI.** This slice builds the API and the Canvas renderer;
  the tip-page control is a separate surface (§8, HUB-07) and is referred, below.
- **Migration `0138` and everything in it** — owned by a concurrent agent, never written,
  read as authority, or renumbered here.
- `active/traceability/register-map.tsv`; `apps/api/src/observability/`; the standalone OBS
  widget routes; the canvas designer UI; every other unbuilt catalogue module.

---

## Referred to Opus / the owner

- **No retention policy for `channel_reaction_sends`, and 2026-09-17 makes it matter more.**
  Removing the per-channel cap means reaction **write volume now scales with audience size**:
  the mechanism that used to bound total inserts per channel per minute is gone by design, so
  a popular stream writes far more reaction rows than before. No retention period is invented
  here. Retention in this product is a **trust, privacy and legal policy, never a technical
  default** — someone has to decide whether a reaction is ephemeral telemetry or a durable
  creator record (§12.6) before any retention or deletion job can exist. **Named open
  question, owned by the owner.**
- **The tip-page reaction control does not exist.** The API accepts sends; nothing in
  `apps/web/app/tips/[handle]` calls it yet. HUB-07 is the register row for that surface and
  it is a different surface from the Canvas.
- **The display ceiling has no value.** It ships unset, as decided. Whoever can measure a
  real reaction rate against a real Canvas owns the number.
- **`MASTER_CANVAS_BUILT_MODULE_KEYS` in `apps/api/src/domain/master-canvas-store.ts` is
  still stale**, as slice 5 already referred. Left stale here too rather than silently
  diverging from that precedent.
