# Review — OPS-08 / OPS-11 activation and revenue instrumentation

**Tasks:** `../active/tasks/OPS-08.md`, `../active/tasks/OPS-11.md`
**Date:** 2026-09-16
**Reviewer:** Orchestrator self-review. **Independent review unavailable** — not claimed.

## Scope authority for this slice

The command that dispatched this work stated that the product/market/creator/streamer scope
review for this slice was already completed by a separate review-only agent and confirmed by
Opus, and gave that review's four binding decisions verbatim (§0–§1 of the command): build
OPS-08 in full and only the derivable half of OPS-11; keep both out of Prometheus; derive
every number rather than store a counter; and bound repeat-supporter rate by the anonymous
identity's TTL. **A standalone persisted artifact carrying that review was searched for and
not found** — `bharatstudio-requirements/reviews/`, `pending/`, and the `bharatstudio-alerts`
tree were all checked (by content grep for `OPS-08`, `OPS-11`, "activation instrumentation",
"revenue instrumentation", "repeat-supporter") before any code was written, and nothing
matched outside `FULL-PRODUCT-DEFINITION.md` itself, `TRACEABILITY.md` and
`active/traceability/semantic-mapping-audit.md`. This record therefore carries Opus's four
decisions as given in the dispatching command, attributed to it, rather than pointing at a
separate file that could not be located — flagged here per the command's own hard rule 6
("if this command is factually wrong about the code, stop and report it") rather than silently
treated as found.

## The four decisions, and how each was honoured

1. **Build OPS-08 in full; build only the derivable OPS-11 KPIs.** Honoured: OPS-08's three
   milestones and OPS-11's average tip / repeat-supporter rate / challenge revenue / vote
   revenue are built; tips-per-viewer-hour, TTS-driven tips, threshold uplift and goal-driven
   tips are not — see `active/tasks/OPS-11.md`'s "what was left out and why".
2. **Durable, creator-reachable record — not Prometheus.** Honoured: both new numbers live
   behind `GET /v1/channels/:channelId/activation-state` and `.../revenue-kpis`, backed by two
   new `app_private` SQL functions, with zero additions to `apps/api/src/observability/
   metrics.ts`. A new structural test (`apps/api/test/l09-reliability-metrics.test.ts`)
   enforces this going forward rather than only today.
3. **Derive, never store a counter.** Honoured throughout: `packages/db/migrations/
   0133_v1_ops08_ops11_activation_and_revenue_kpis.sql` adds two functions and zero tables,
   columns or triggers. Repeat-supporter rate reads `creator_supporter_relations.tip_count`,
   already recomputed net-of-refunds by `0124`'s trigger; average tip, challenge revenue and
   vote revenue all recompute from `payments`/`refunds` (challenge/vote revenue additionally
   reuse `0109`/`0108`'s own existing derivations unchanged) on every call.
4. **Repeat-supporter rate bounded by the anonymous identity's TTL.** Honoured:
   `get_channel_revenue_kpis`'s supporter population excludes any `kind = 'anonymous'` relation
   whose `anonymous_browser_identities.expires_at` has passed, proven structurally in
   `packages/db/tests/ops11_revenue_kpis.sql` (an expired identity with two payments — which
   would otherwise read as a repeat supporter — is excluded from both the numerator and the
   denominator).

## OPS-08 — no new schema needed, and why

Three candidate signals were checked against existing durable records before writing any SQL:
`payment_account_audit` (append-only, `action = 'activated'`, migration `0060`) for payout;
`overlay_sessions` (never deleted, only revoked — `0016`) for overlay/OBS; `alert_events`
(never deleted) for first alert. All three were already sufficient. The one design choice
worth naming: `0093`'s `get_companion_state` already reads a *live* payout/overlay signal for
Companion's own activation-gating purpose (does the account currently have status `active`;
does an unexpired session currently exist). OPS-08 deliberately reads a *sticky* version of
each instead (has this ever happened) — an activation checklist item should not un-check
itself when a creator later revokes a payment account or an overlay session expires from
disuse. `packages/db/tests/ops08_activation_state.sql` proves this distinction directly: it
activates, then revokes, a payment account and asserts `payoutConnected` stays `true`.

## OPS-11 — what was left out, checked rather than assumed

`!tip` conversion was the one KPI the command explicitly asked to be checked rather than
guessed. A repository-wide grep (SQL, TS, Go) for `chat_command`, `'!tip'`, `bang_tip`,
`tip_command`, `chat_origin` in `bharatstudio-alerts` returned nothing. `CON-07` — the chat
command connector that would eventually produce such a marker — is Phase 2 (YouTube), out of
v1 by `00_LAUNCH_SCOPE_AUTHORITY.md`'s explicit v1 exclusions. There is no durable record
today that distinguishes a `!tip`-originated payment from any other tip, so this KPI could not
be built and was left out, not approximated.

The other three excluded KPIs (TTS-driven tips, threshold uplift, goal-driven tips) all share
a structural reason for exclusion beyond "not requested": each requires attributing a specific
tip to a specific *cause* (did the TTS voice line prompt it; did crossing a threshold prompt
it; did a visible goal prompt it), which is new derived *logic*, not a read over data that
already exists — matching the command's own framing exactly. No attempt was made to
approximate any of them with a proxy signal.

## OPS-10 — a resolved scope-instruction conflict

The dispatching command's §1 top line reads "Build: OPS-08 in full, and the derivable half of
OPS-11" and lists only `OPS-08.md`/`OPS-11.md` (plus their `TC-` records and this shared
review) under "3. RECORDS — BEFORE CODE". Its §1(d), titled "OPS-10 — creator funnel only,
viewer side aggregate-only", uses imperative build language ("Build the creator activation
funnel..."; "For the viewer side, build only aggregate counts...") that reads, taken alone, as
a third build target.

**Resolved as: OPS-10 is not built in this slice.** Three things point the same way. First,
the top-line scope statement names only two rows. Second, the records section — which the
command itself frames as authoritative ("RECORDS — BEFORE CODE") — lists no `OPS-10.md` or
`TC-OPS-10-*.md`, and creating an undocumented capability contradicts §31.0/§35.1's own rule
that a capability's presence is never permission to build it without its ten fields recorded
first. Third, §1(d)'s substantive content — the two named privacy rules (no correlation of an
anonymous visit beyond the bounded token; repeat-supporter rate bounded by the TTL) — is
squarely about how to build OPS-11's repeat-supporter rate correctly, which this task already
needed and already honours (see decision 4 above). Read this way, §1(d) is decision context for
OPS-11, not a third build instruction, and the apparent conflict resolves without discarding
either half of the command.

The practical cost of being wrong in either direction was weighed before deciding: building
OPS-10 without its own task/test record would violate the lifecycle rule the command itself
invokes elsewhere; not building it when it was intended only delays two rows that were not
independently scoped, sized, kill-switched or acceptance-tested here — and the viewer-side half
in particular (a new aggregate open/completion counter, bucketed by channel and day) is new
schema, which is exactly the kind of addition §31.0 says needs its own ten-field record before
a build lane picks it up. OPS-10 (both the creator funnel, which is a trivial reuse of OPS-08's
three signals, and the viewer aggregate counter, which is not) is referred to Opus rather than
built.

## Disposition

`Conditionally complete`. Both rows' local implementation is done and verified against a real
Postgres 16 container and the full local test/contract/explain-plan suite (counts recorded in
each `TC-` file). No independent review has occurred. OPS-10 (both halves) and the four
attribution-dependent OPS-11 KPIs remain open, referred rather than attempted.
