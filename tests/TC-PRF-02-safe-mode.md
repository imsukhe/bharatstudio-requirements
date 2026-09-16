# TC-PRF-02-safe-mode — acceptance record for safe mode (§6 module #12, the other half)

**Task:** `../active/tasks/PRF-02-safe-mode.md`
**Authority:** `../reviews/2026-09-16-prf-02-slice-6-owner-decisions.md` decision 3
**Owner:** **Sukhdev Singh**
**Status:** `Conditionally complete — every case below ran and passed locally; independent review
unavailable`

These cases were written **before** the implementation, from the owner decision and the boundary in
the task record. Nothing here is production, provider, store, legal, device, network or release
readiness; local verification is local verification.

---

## SQL layer — `packages/db/tests/prf02_safe_mode.sql` (id block `...5a00-...5aff`)

| Case | Asserts |
|---|---|
| **SM.1** | A channel's safe mode defaults to **off** — asserted across every channel in the database, base-world's included, so "existing rows are unaffected" is a claim about rows this file did not write |
| **SM.2** | With safe mode **off**, `app_private.initial_delivery_status(channel)` returns `'ready'` and a manual alert's delivery is written `ready` with `hold_reason` null |
| **SM.3** | With safe mode **on**, it returns `'held'` and both new deliveries are written `held` with `hold_reason = 'moderation'` — the existing reason, not a new one. The delivery created *before* the switch is untouched |
| **SM.4** | Safe mode is **per channel**: A on and B off produce `held` and `ready` respectively |
| **SM.5** | A safe-mode-held delivery is **not dispatchable** — absent from `list_ready_event_deliveries` and refused by `claim_event_delivery`; the control delivery created with safe mode off still is, so the zero is a real exclusion and not a fixture artefact |
| **SM.6** | **Turning safe mode off releases nothing.** Both held deliveries are still `held`, still `hold_reason = 'moderation'`, and their summed `state_version` has not moved. The next NEW delivery is `ready` |
| **SM.7** | The existing per-event path still releases one: `apply_moderation_action(..., 'approve')` takes one held delivery to `ready` with `hold_reason` null while **the other stays held** — which is what "reviewed individually" means and what proves no bulk release happened |
| **SM.8** | `set_channel_safe_mode` is gated: owner and admin may; a `viewer`-role member, a non-member, and an actor id that does not match the session identity each raise `42501`, and the stored value is unchanged after every refusal |
| **SM.9** | Toggling is idempotent (true twice, false twice), the read agrees, and the read answers **zero rows** — not a row reading false — for a viewer, a non-member and a non-existent channel |
| **SM.10** | **Never tier-gated** (§12.6): the toggle succeeds with the channel on the `free` entitlement tier |
| **SM.11** | **Never automatic**: `pg_get_functiondef` of `initial_delivery_status` and `set_channel_safe_mode` contains none of `interval`, `count(`, `sum(`, `avg(`, `rate`, `spike`, `threshold`, `window`, `percent`, and neither references `is_paused` |
| **SM.12** | `list_overlay_moderator_status` carries the flag, scoped by the overlay session; channel A's session never sees channel B's |
| **SM.13** | A wrong fingerprint, a foreign session and an expired session each still return **zero rows**, never a row reading `false` |

## SQL layer — `packages/db/tests/prf02_slice5_moderator_status.sql`, extended in place

| Case | Change |
|---|---|
| **S5.4** | The declared-result assertion is **updated, not deleted**: exactly `TABLE(held_count bigint, safe_mode boolean)`, plus the live-call column-set assertion `held_count bigint, safe_mode boolean`. A third column of any name still fails this file (proved — see "Negative test 2") |
| **S5.5** | Still asserts the definition never references `is_paused` and never references `closed_at`. The blanket "no safe-mode token" assertion is **replaced by its inverse**: the definition must now read `safe_mode_enabled`, so a build that silently dropped the flag fails here |
| **S5.11** (new) | Safe mode is visible through this read and stays channel-scoped: A on / B off, and turning it on then off changes the held count by exactly zero in both directions |
| **S5.1 / S5.2 / S5.3 / S5.6** | Unchanged and still passing |

## API layer — `apps/api/test/prf02-safe-mode-routes.test.ts`

| Case | Asserts |
|---|---|
| **SMR.1** | An unauthenticated read and write are both rejected |
| **SMR.2** | The read returns exactly `{ schemaVersion, safeMode: { schemaVersion, enabled } }` |
| **SMR.3** | On/off is one idempotent `PUT` returning the new state; the route forwards the value it was given, never a computed toggle (`calls` asserted as `[true, true, false]`) |
| **SMR.4** | A body carrying `threshold`, `windowSeconds`, `rateLimitPerMinute`, `auto`, `triggeredBy`, `expiresAt`, `durationSeconds` or `reason` is a **400 before the store is called at all** (`storeCalls === 0`) |
| **SMR.5** | **Nothing is coerced into a switch position.** `{}`, `null`, `"true"`, `"false"`, `1`, `0`, `"on"`, `"yes"`, `"0"`, `2`, `{}`, `[]` are all 400 and none reaches the store; only real `true`/`false` are accepted. See "Finding" below — this case failed first |
| **SMR.6** | A caller without the role is `404 not_found` on both verbs, never `403` |
| **SMR.7** | An unwired store is `503 safe_mode_store_unavailable`, `retryable: true` — never a 200 claiming safe mode is off |
| **SMR.8** | A throwing store is `503` and the thrown message never reaches the body |
| **SMR.9** | A malformed channel id is 400; no response carries a tier, a queue-paused flag or a threshold |

## API layer — `apps/api/test/prf02-slice5-moderator-status-routes.test.ts`, extended in place

| Case | Change |
|---|---|
| **S5.11** | The outbound narrowing now passes `safeMode` through and **still** strips every private field a store might hand up — a store returning `{ heldCount, safeMode, supporterName, message, amountPaise, deliveryId, eventId, queueId, channelId, viewerIdentityId, isPaused, paused }` yields exactly `{ schemaVersion, heldCount, safeMode }` |
| **S5.13** (new) | `safeMode` travels; `'true'`, `1`, `null` and `undefined` are projected to `null` rather than coerced |
| **S5.14** (new) | `POST`/`PUT`/`PATCH`/`DELETE` on the overlay read are 404 — an overlay token can read the state and can never set it |
| **projectModeratorStatus** | Emits exactly three keys; an answer with no `safeMode` is no answer |

## Renderer — `moderator-status-logic.test.ts` and `moderator-status-module.test.ts`

| Case | Asserts |
|---|---|
| **SMW.1** | `isModeratorStatus` requires exactly `{schemaVersion, heldCount, safeMode}`; a missing flag, a non-boolean flag, a private field, and `isPaused`/`paused`/`queuePaused` are all rejected |
| **SMW.2** | Safe mode on with nothing held: the card is **visible** and reads `safe mode on` |
| **SMW.3** | Safe mode on with three held: `safe mode on · 3 held for review` — safe mode first, because it is the cause |
| **SMW.4** | Safe mode off with five held: `5 held for review` — slice 5's exact string, unchanged |
| **SMW.5** | Safe mode off with nothing held: **nothing rendered**, container opacity `0`, label empty. Slice 5's no-all-clear decision preserved, and asserted across every label the module can emit |
| **SMW.6** | No rendered text ever contains `message`, `chat`, `comment` or `paused` |
| **SMW.7** | The card un-hides and re-hides as the flag flips, and stays up (reading only the count) when safe mode goes off while alerts are still held |

## Canvas integration — `master-canvas-integration.test.ts`

| Case | Asserts |
|---|---|
| **SMI.1** | Nine entitled modules still open one transport connection, nine subscribers, one pending frame |
| **SMI.2** (new) | Safe mode paints on the same shared connection and rAF loop: one connection, one subscriber, **one snapshot read per activation**, one pending frame. Recorded honestly: re-activating the module reopens the stream (`fetchCalls` 2), which is the connection's own documented "idle modules cost nothing" behaviour, not a cost safe mode added |

## Contracts

`overlay-moderator-status-response` carries `safeMode` (required, boolean); `channel-safe-mode-response`
is new. `contracts/validate-fixtures.mjs` keeps all seven private-field negatives, **still refuses
`isPaused`/`paused`/`queuePaused`** on the overlay response, refuses a missing or non-boolean
`safeMode`, accepts `heldCount: 0` with `safeMode: true`, and refuses eight automatic-engagement
fields plus `isPaused`/`paused` on the creator response. OpenAPI documents the changed overlay
response and both creator operations.

## EXPLAIN / RT-12

`packages/db/explain-plans/moderator-status.explain.md` re-captured against `0138`'s function body,
new `query_hash`, and the manifest entry re-pointed at `0138`. The only plan change is one
`SubPlan 2` — a single-row lookup on `public.channels`. No new manifested read was added: the
creator store is on the main pool and matches none of the three scan rules, the same structural
position `db/stream-mission-store.ts` occupies.

## Commands run — real output, this worktree, 2026-09-16

| Command | Result line |
|---|---|
| `pnpm db:test:all` | `SQL SUITE: pass=64 fail=0` |
| `pnpm --filter @bharatstudio/alerts-api test` | `ℹ tests 628` / `ℹ pass 628` / `ℹ fail 0` |
| `pnpm --filter @bharatstudio/alerts-web test` | `ℹ tests 482` / `ℹ pass 482` / `ℹ fail 0` |
| `pnpm --filter @bharatstudio/alerts-api build` | `tsc -p tsconfig.json` — no output, exit 0 |
| `pnpm contracts:validate` | `Validated 43 fixtures plus the v1 template catalogue contract…` / `Validated OpenAPI 3.1 document with 75 paths, 84 operation contracts, and all local $ref targets.` / `Validated 3 negative OpenAPI operation-contract cases.` |
| `pnpm explain:check` | `OK: every app_private call found by rule 1 (convention scan), rule 2 (overlay-store-file scan) and rule 3 (composition-root derived-read scan, 11 wired declaration(s) resolved and scanned) is present in required-queries.json (18 manifest entries, 9 exemptions)` / `OK: 18/18 plans current` |
| `pnpm harness:check` | `API test harness check: all checks passed against current code.` |

Additionally, and not required: `pnpm db:test:l03` was run as a regression check on the three
re-declared delivery-inserting functions, because one of them is the verified-payment-webhook path.
`L03_APPLICATION_BEHAVIOR=PASS`, `L03_PAYMENT_LEDGER_READ=PASS`, `L03_FEATURED_CREATOR_LISTING=PASS`,
`L03_ADMIN_DLQ_TOOLING=PASS`, `L03_ADMIN_ENTITLEMENT_MANAGEMENT=PASS`, `L03_TTS_EVENT_ENRICHMENT=PASS`,
plus the Go payment-webhook/alert-worker store suites `ok`.

## Negative tests

**1. The never-automatic guard (SM.11).** `app_private.initial_delivery_status` was replaced in a
throwaway database with the exact change the owner forbade — safe mode engaging on a spike, with an
invented threshold of 10 and an invented one-minute window. The repository was never modified.

Broken:

```
ERROR:  app_private.initial_delivery_status contains "interval" -- safe mode is NEVER automatic (owner decision, 2026-09-16). No threshold, window, rate or aggregate may decide when it engages; if one is needed that is a new owner decision, not a constant chosen here
```

Restored (the throwaway database dropped, the shipped definition re-run):

```
PASS prf02_safe_mode
 prf02_safe_mode.sql: all assertions passed
```

**2. Slice 5's column-set assertion, to prove extending it did not weaken it.** A third column
(`channel_id uuid`) was added to `list_overlay_moderator_status` in a throwaway database.

Broken:

```
ERROR:  the overlay moderator-status read must return the held COUNT and the safe-mode FLAG and nothing else (§6: never private content, enforced as a property of the query). Declared result is "TABLE(held_count bigint, safe_mode boolean, channel_id uuid)", expected exactly "TABLE(held_count bigint, safe_mode boolean)"
```

Restored: `PASS prf02_slice5_moderator_status` (`prf02_slice5_moderator_status.sql: all assertions
passed`), and the same file passes in the full suite above.

## Finding — a real defect this work found in itself, recorded rather than smoothed over

**`enabled: null` silently turned safe mode OFF in the first version of the route.** With the API's
normal `type: 'boolean'` declaration and Fastify's default AJV `coerceTypes`, `null` was **measured**
to coerce to `false` and return `200` — so an uninitialised form field or a cleared client state
would have released a channel's held alert flow onto a live broadcast with nobody asking. The route
now declares the two allowed **values** (`enum: [true, false]`) instead of a type, which removes AJV
coercion entirely. This is stricter than every other boolean field in this API and that deviation is
deliberate and recorded in the route's own header; the cost is that a client sending `"true"` now
gets a 400. SMR.5 is the case that caught it and the case that keeps it caught.
