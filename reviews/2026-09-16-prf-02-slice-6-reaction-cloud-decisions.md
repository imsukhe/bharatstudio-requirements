# Review and decision record — PRF-02 slice 6, Reaction Cloud (§6 #5) and PRF-06 reactions

**Date:** 2026-09-16
**Owner:** **Sukhdev Singh**
**Reviewer:** self-review only. **No independent review occurred** — governance/AGENTS.md's
"if independent review is unavailable, say so, self-review, and leave the task
`Conditionally complete` or `Blocked`" applies, and this record says so rather than implying
a review that did not happen.
**Task:** `../active/tasks/PRF-02-slice-6-reaction-cloud.md`
**Acceptance:** `../tests/TC-PRF-02-slice-6-reaction-cloud.md`
**Binding decisions:** `2026-09-16-prf-02-slice-6-owner-decisions.md` decisions 1 and 2 —
read, not restated, not extended.

This record holds the decisions the **implementer** had to make because no authority states
one. Every numeric value in the build traces to something already decided; where a number
would have had to be invented, the mechanism ships unset instead and that is recorded here.

---

## D1 — Both halves of the curated catalogue are sendable, in one reaction table

Owner decision 1 names "first-party plus staff-reviewed creator packs". Those are two
different tables today (`sticker_catalogue_entries`, migration `0110`;
`creator_sticker_packs`, migration `0119`) with two different eligibility rules, and `0119`
deliberately kept its selection table independent of `0110`'s ("Coexistence, not shared
mutual exclusion").

`channel_reaction_sends` therefore carries **two nullable foreign keys and a
`num_nonnulls(...) = 1` check** rather than two tables or one polymorphic text id. One table
because the Reaction Cloud is one cloud and a two-table aggregate would have to be a union in
every read; exactly-one-of because a reaction is one entry, and the database rather than the
application is where that stays true.

The send function takes `(channel, entry_source, entry_id)` with `entry_source` constrained
to `'catalogue'` / `'creator_pack'`, and validates each against **the same live rules the
existing public read already applies** — `sticker_tier_rank` plus `channel_sticker_disables`
for the catalogue; `enabled`, `status = 'active'` and `creator_pack_tier_limit`'s rank window
for packs. No new eligibility rule was written, and no pack review behaviour changed.

## D2 — The read window is the SAME one minute the rate limit uses, not a second number

§19.5 requires a sample; it does not say over what interval. Rather than invent one, the
overlay read aggregates over `interval '1 minute'` — **the identical window migrations `0032`
and `0063` already enforce**, and the one owner decision 2 names. One already-decided interval
does two jobs; a second interval would have been a second invented number.

## D3 — The projection is an aggregate, and that is what makes sampling server-side

The read is `count(*)` grouped by catalogue entry. There is no code path on which an
individual reaction row, or its timestamp, reaches the client — not "we chose not to send
them", but "the function's declared `returns table` has no column for them". The configured
ceiling then caps how many **aggregate rows** are returned, inside the security-definer
function, before anything crosses the API boundary.

This is the §19.5 obligation read literally: "sampled and rate-limited server-side **before
they reach the canvas**", and "a representative sample, **never every event**".

## D4 — The ceiling ships configured-but-unset, following `config.ts`'s existing pattern

`REACTION_CLOUD_SAMPLE_MAX` is read by the same `optionalPositiveInt` helper in
`apps/api/src/config.ts` that already produces `overlayMaxInstanceSubscribers`,
`overlayMaxChannelSubscribers`, `derivedReadMaxConcurrent`, `derivedReadPoolMax` and
`derivedReadStatementTimeoutMs` — five of the six values the owner decision refers to, all in
one file, all `number | undefined`, all documented as "unset means today's behaviour, never a
value this codebase invents". The sixth is `0131`'s own "configured but unset" posture on the
module cap.

Unset is passed to SQL as `null`, and PostgreSQL's `LIMIT NULL` means no limit — so unset
imposes no ceiling beyond the query's own structural bound (at most one row per catalogue
entry the channel can reach, which is itself bounded by the catalogue and by
`creator_pack_tier_limit`). Shipping it set changes exactly one thing.

A value below 1 cannot reach the function — `optionalPositiveInt` throws at startup — and if
one somehow did, the function's `case` fails **closed** (zero rows), never open.

## D5 — Ordering is deterministic, because a sample that reorders itself is not a sample

`order by reaction_count desc, display_name asc, entry_id asc`. Without the last two keys a
ceiling would slice an arbitrary subset out of a tie and the cloud would flicker between
frames at a fixed underlying state. The entry id is the final tiebreak because it is unique.

## D6 — The send path is unauthenticated, reusing the abuse guard, and no new model

Stated in full in the task record's "Authentication of the send path" section. In summary:
the tip page is unauthenticated by construction, §30.3 makes free reactions available at
every tier, and §6 #5 requires the surface to be non-identifying — so an account requirement
would contradict two decided things. The existing `PublicAbuseGuard` (Turnstile) is reused
behind the existing `publicPaymentTurnstileRequired` flag with the existing
`bot_verification_required` 403 envelope, and the per-channel one-minute SQL limit is owner
decision 2's mechanism. **No viewer session, no anonymous identity cookie, and no new flag.**

Note the consequence, stated rather than glossed: because the rate limit is per channel and
the owner explicitly excluded a per-viewer figure, one viewer can consume the whole channel's
minute. That is the decided design, not an oversight — a per-viewer limit would need a viewer
identifier, which §6 #5 forbids on this surface, and a number the creator does not control,
which owner decision 2 forbids.

## D7 — No viewer identifier is stored at all, not merely withheld from the read

The constraint is that "non-identifying" be a property of the query. It is, and it is also a
property of the **table**: `channel_reaction_sends` has no viewer column, no anonymous-token
column, no session column and no IP column. There is nothing for a future read to expose.
`created_at` exists because an append-only row without a timestamp cannot be windowed, and it
is never returned, never grouped on, and never joined out — asserted directly against the
function's returned column set.

## D8 — The route split: the send in `public.ts`, the read in `master-canvas.ts`

The send goes in `routes/public.ts` because that file already receives the abuse guard and the
Turnstile flag, already resolves `:handle` (including released handles), and already owns the
public-surface envelope. Putting it in `routes/stickers.ts` would have meant threading the
abuse guard into a tenth positional dependency to get a protection that already exists next
door.

The overlay read goes in `routes/master-canvas.ts` beside the other Canvas module reads, for
the reason slice 5 already recorded: that file owns the bearer-token helper and the Canvas
envelope, and `routes/interactions.ts` already takes fifteen positional dependencies.

## D9 — An unrecognised overlay token answers `200` with an empty list, not `401`

Unlike the Moderator Status Card, this read has no meaningful "authorised but empty"/"not
authorised" distinction to preserve: an empty cloud and an unauthorised read both mean "paint
nothing", and there is no count whose zero the renderer must treat differently. So the route
returns `200 { entries: [] }` for both, and the module renders nothing either way. A missing
bearer token is still `401` — that is a malformed request, not an empty answer.

## D10 — The store files are named so RT-12's scan cannot miss the read, and does not catch the write

`apps/api/src/db/reaction-cloud-overlay-store.ts` is caught by all three
`scan-required-queries.mjs` rules independently: rule 1 by the `list_overlay_*` function name,
rule 2 by the `overlay` in the filename, rule 3 because `index.ts` constructs it with
`derivedReadSql`. The manifest entry and the EXPLAIN artefact are therefore mandatory, which
is the intent.

`apps/api/src/db/reaction-send-store.ts` is a **write** on the main pool, not a derived read,
so none of the three rules applies and no artefact is required. That is correct rather than
convenient: RT-12's manifest is about widget-backing reads, and an EXPLAIN of an insert under
a row lock would be a plan-shape artefact of something that is not a read path.

---

## What this record is not

Self-review only, no independent review. Nothing here is production, provider, store, legal,
device, network or release readiness. The EXPLAIN artefact is a plan-shape change detector
captured against a small local database; §19.4's budgets stay unclaimed and RT-07 stays
Blocked. **No register state letter was self-assigned** — PRF-02, PRF-06 and HUB-07 letters
are decided after audit, by the owner.
