# Review and decision record — PRF-02 / PRF-06 reaction sends: the rate limit moves from the CHANNEL to the SENDER

**Date:** 2026-09-17
**Owner:** **Sukhdev Singh**
**Reviewer:** self-review only. **No independent review occurred.** `governance/AGENTS.md`'s
"if independent review is unavailable, say so, self-review, and leave the task
`Conditionally complete` or `Blocked`" applies, and this record says so rather than
implying a review that did not happen.
**Task:** `../active/tasks/PRF-02-slice-6-reaction-cloud.md`
**Acceptance:** `../tests/TC-PRF-02-slice-6-reaction-cloud.md`
**Supersedes, in part:** `2026-09-16-prf-02-slice-6-reaction-cloud-decisions.md` **D6 and D7**
— see "What this supersedes" below. Everything else in that record stands unchanged.
**Authority:** `FULL-PRODUCT-DEFINITION.md` §6 module #5, §12.7, §19.5, HUB-07; the owner
decision quoted verbatim below.
**Migration:** `packages/db/migrations/0141_v1_prf02_reaction_sender_rate_limit.sql`
**State:** `Proposed → Approved` by the owner for the limit's *shape*; `Implemented`,
**not** `Verified` — no register state letter is self-assigned here.

---

## The owner's direction, verbatim

> "all these should not be limited at channel level bcs then we are limiting money for them
> these should be limited at sender/user level to avoid misuse or attacks, so plan a safe
> number for user - for creator dont limit it too much that with higher viewer etc they dont
> face issue."

Two things were wrong with what slice 6 shipped, and the owner named the first of them:

1. **A channel-level cap throttles the creator.** `record_channel_reaction` (migration
   `0139`) counted reactions per channel against one budget. A popular stream exhausts that
   budget and then refuses *legitimate* viewers — the more successful the creator, the worse
   the surface behaves. That is backwards.
2. **`rateLimitPerMinute` is the creator's alert-source setting** (`queue.rateLimitPerMinute`
   in the channel config schema, enforced for queue dispatch by migrations `0032`/`0063`).
   Borrowing it for reactions gave one creator-facing number a second, unrelated meaning, so
   a creator tuning their alert queue would silently retune their Reaction Cloud.

---

## R1 — The per-channel cap is REMOVED, not lowered, not made optional

`0141` drops `public.channel_reaction_rate_limits` and drops the three-argument
`app_private.record_channel_reaction(uuid, text, uuid)`. The replacement function reads
**no** channel configuration at all: `rateLimitPerMinute` and its legacy `rateLimitPerMin`
alias appear nowhere in it, and the SQL acceptance file asserts their **absence** from the
shipped function definition rather than their presence. A creator's reaction throughput now
scales with their audience and there is no channel budget that can cap it.

This is the point of the change, so it is proven by a test that fails if the cap returns,
not by a comment.

## R2 — The limit is per SENDER and has no channel in it

`public.reaction_sender_rate_limits` is keyed on `sender_key` **alone**. There is
deliberately no `channel_id` column:

- **It matches the words.** The owner said "limited at sender/user level" and the number was
  delegated as "a safe number for user" — neither is qualified by channel.
- **It is the stricter reading.** Per-sender-per-channel would let one sender spend 60 a
  minute on every channel at once; per-sender is one budget for the person.
- **It is the more private one, and this is the deciding reason.** A row keyed
  `(channel_id, sender_key)` would state "this browser interacted with this creator inside
  this minute" — a small but real record of *where* a viewer was. Keyed on the sender alone,
  the row states only "this sender has sent N times in the current window" and cannot answer
  which creator, which sticker, or which of anything.

## R3 — The number is 60 per minute, and it is an owner-delegated choice with a named anchor

The owner delegated the figure explicitly ("plan a safe number for user"). It is recorded
here as a **delegated choice**, not as a free invention, and it is anchored:

**Anchor:** `POST /v1/public/channels/:handle/paid-votes` — the closest public-write sibling
on the same unauthenticated tip-page surface — already carries
`config: { rateLimit: { max: 60, timeWindow: '1 minute' } }` in
`apps/api/src/routes/public.ts`. The reaction send is the same kind of request from the same
kind of caller, so it gets the same figure rather than a new one.

**Why 60 is safe in both directions.** One send per second *sustained across a full minute*
is far above genuine human tapping — a viewer hammering a reaction button in bursts stays
well inside it — while a script that wants to flood a cloud needs orders of magnitude more
than one per second to matter, and is refused. It does not restore the problem R1 removed,
because it is the *sender's* ceiling: ten thousand viewers can still send 600,000 reactions
a minute to one channel.

## R4 — The sender key is the EXISTING anonymous browser identity, obtained the way checkout already obtains it

**Not IP.** Indian mobile carriers use CGNAT heavily: thousands of unrelated viewers share
one address, so an IP-keyed reaction limit would refuse genuine viewers *as a group* — the
same "throttles the creator's audience" failure the owner just rejected, only worse because
it is invisible.

**The existing flow, followed exactly.** The two public checkout POSTs in
`apps/api/src/routes/public.ts` (the tip-order route and the TipIntent redemption route) each
do the same three steps, and the reaction route now does the identical three:

1. read the `__Host-bsa-anonymous` cookie via `anonymousTokenFromCookie(request.headers.cookie)`
   — accepted only if it matches `/^[A-Za-z0-9_-]{43}$/`;
2. when absent, mint one with `randomBytes(32).toString('base64url')` and return it with the
   same `anonymousCookie()` header (`__Host-`, `HttpOnly`, `Secure`, `SameSite=Lax`,
   `Max-Age=2592000`);
3. hash it with `anonymousTokenHash()` — SHA-256, hex — and pass **only the hash** onward.

The raw token never enters the database. That is migration `0124`'s own property and it is
preserved, not re-implemented: the same three helpers already in that file are called, and no
second identity mechanism, cookie, header or fingerprint is introduced.

**The signed-in / claimed case.** `app_private.resolve_reaction_sender_key(text)` resolves the
fingerprint against `anonymous_browser_identities` → `viewer_identities` (migration `0084`,
used by `0124`). If that browser's identity has been claimed into an account
(`viewer_identities.merged_into_account_id`), the key becomes the **account's** viewer
identity — so a signed-in viewer's several browsers share one budget instead of multiplying
it. That is "use the signed-in viewer identity when there is one", expressed inside the
schema that already exists.

**No identity row is ever minted by a reaction.** The resolver only **reads**
`anonymous_browser_identities`; a fingerprint it does not recognise falls back to the opaque
key `'token:' || <sha-256 hex>`, which creates nothing. This is a deliberate departure from
`app_private.resolve_anonymous_payment_identity`, which *does* insert: letting a free
interaction mint durable 30-day identity rows would expand the identity table's population
for a surface §6 #5 requires to be non-identifying. Reactions therefore consume the identity
graph and never grow it.

## R5 — Privacy: admission control only, and the send row is unchanged

- The sender key is used to **decide whether to accept a send, and for nothing else**. It is
  not returned by any read, not written to the reaction row, not logged, and not used as a
  metric label.
- **`public.channel_reaction_sends` is untouched by `0141`.** It still has no viewer column,
  no token column, no session column and no IP column. `0139`'s D7 property survives this
  change completely.
- **The overlay projection is unchanged and asserted unchanged.**
  `app_private.list_overlay_reaction_cloud` still declares exactly
  `returns table (entry_source text, entry_id uuid, display_name text, reaction_count bigint)`.
  `0141` does not touch that function, and the SQL acceptance file continues to assert the
  column set twice over — from `pg_get_function_result` and from a table materialised out of
  a live call.
- **The limiter table holds three columns and no more:** `sender_key`, `window_started_at`,
  `send_count`. No channel, no entry, no per-send timestamp, no history. The count is clamped
  at 61 so it cannot accumulate into a measure of how hard someone tried.

## R6 — How long the rate-limit state persists, and why that is the minimum

**A row's content never outlives its one-minute window.** On the sender's next send, an
elapsed window is overwritten in place — `window_started_at` becomes now and `send_count`
becomes 1 — so nothing from the previous window survives. For a sender who never returns, the
row is removed by a bounded sweep (`delete ... where window_started_at <= now - interval '1
minute'`, capped per call) that every send performs, so the table converges on **currently
active senders only**.

**Why this is the minimum rather than merely short.** A fixed-window limiter cannot decide
"is this the 61st send inside this minute?" without holding, for the length of that window,
one counter per sender who sent inside it. One minute is exactly the window the decision
names; one integer is exactly the state the decision needs. Anything less cannot answer the
question, and anything more — a per-send row, a longer window, a last-seen timestamp — would
be retaining data the limit does not use. §12.7's bounded-data rule is satisfied for the same
reason: the state is bounded by the number of senders active in the last minute, not by
history.

## R7 — A send with no resolvable sender identity is REFUSED

`record_channel_reaction` returns `'sender_unidentified'` and the route answers **400
`reaction_sender_unidentified`, `retryable: false`** — before any catalogue-eligibility check
runs, so an unidentified caller cannot even probe which stickers a channel has.

**Why refuse rather than fall back to the global per-IP limit.** Falling back would mean the
one path with no per-sender ceiling is the path an attacker controls: dropping a cookie would
be the cheapest way to get the weaker limit, so the fallback would *be* the attack. Refusing
keeps a single rule. Nothing is silently accepted as unlimited.

**Why this is not a usability problem.** The route mints the cookie when none is present, so
an ordinary first-time visitor is identified on their very first send. `sender_unidentified`
is reachable only when a caller reaches the store with a malformed or absent fingerprint —
a client bypassing the route, or a wiring fault — and failing closed is the right answer to
both.

## R8 — The residual, stated rather than glossed

**A client that discards cookies evades the per-sender limit.** It presents a new fingerprint
on every request, so every request is a new sender with a fresh budget. The only thing left
standing against it is the **pre-existing global limit** in `apps/api/src/app.ts`
(`@fastify/rate-limit`, 120 requests per minute, keyed by IP by default), which this work
neither adds nor changes. That backstop *is* IP-keyed and therefore *is* subject to the CGNAT
concern — but it predates this change, applies to every route, and narrowing or re-keying it
is not in this scope. Recorded as a known residual, not as a solved problem.

The evasion costs the attacker nothing but buys them nothing durable either: because the
resolver never inserts (R4), a cookie-discarding flooder cannot grow
`anonymous_browser_identities`, and because the limiter row is keyed on the fingerprint it
presents, each discarded identity's row is swept within a minute.

---

## What this supersedes

- **`2026-09-16-prf-02-slice-6-reaction-cloud-decisions.md` D6**, in its second half only. The
  send path is still unauthenticated and still reuses `PublicAbuseGuard` behind the existing
  `publicPaymentTurnstileRequired` flag — unchanged. What is superseded is "**no anonymous
  identity cookie**" and "the per-channel one-minute SQL limit is owner decision 2's
  mechanism": the route now reads and issues the existing anonymous-identity cookie, and the
  per-channel limit is gone.
- **D6's closing paragraph** ("one viewer can consume the whole channel's minute … a
  per-viewer limit would need a viewer identifier, which §6 #5 forbids on this surface") is
  **withdrawn as wrong**. §6 #5 forbids a viewer identifier in the *reaction record and the
  overlay read*, which is where "non-identifying" has to hold. It does not forbid an opaque
  admission-control key that touches neither. The owner's 2026-09-17 direction settles it.
- **D7 stands entirely.** No viewer identifier is stored on the reaction row — still not
  merely withheld, still absent from the table.
- **Owner decision 2 of 2026-09-16** is superseded on its rate-limit half only ("reuse the
  per-channel mechanism … `rateLimitPerMinute`"). Its display-ceiling half — the canvas sample
  ceiling ships **configured but unset** — is untouched and still true.

## Open question — NOT decided here, and NOT to be defaulted

**Retention for `channel_reaction_sends` is still undecided, and removing the channel cap
makes it matter more.** Reaction write volume now scales with audience size: the mechanism
that used to bound total inserts per channel per minute is gone by design, so a popular
stream writes far more reaction rows than it would have before.

No retention period is invented here. In this product retention is a **trust, privacy and
legal policy**, never a technical default — someone must decide whether a reaction is
ephemeral telemetry or a durable creator record (§12.6) before any retention or deletion job
can exist. Until that decision is made, the table grows without bound and that is a stated
consequence of this change, owned by the owner.

---

## What this record is not

Self-review only; no independent review. Nothing here is production, provider, store, legal,
device, network or release readiness. **No register state letter was self-assigned** —
PRF-02, PRF-06 and HUB-07 letters are decided after audit, by the owner.
