# Reachability register — 2026-09-13

**This supersedes master plan Part 7 as the authority on what is actually usable.**

Part 7 was written 2026-09-02 and is wrong in both directions: it marks things DONE
that were never built (custom sound, built-in themes, the 72-hour replay buffer, the
Companion 8/16/32/64 page-size row) and marks things TODO that shipped long ago (all
eight entitlement dimensions enforced, one-button test alert, runbooks, moderator
seats). Do not trust its status column.

## Why the earlier reviews were wrong

Every prior status pass asked **"does this code exist?"** and answered yes. The real
question is **"can a person trigger it and see the result?"** Almost every gap below
is the same defect: a capability built correctly, tested, committed — and connected
to nothing. Test suites pass because tests seed their own data and call functions
directly, so a green suite is not evidence that any user can reach the feature.

Verdicts: **USABLE** (writer+read+route+UI coherent) · **UNREACHABLE** (code exists,
no human can trigger it or see its output) · **PARTIAL** · **ABSENT** · **BLOCKED**.

---

## 1. THE ROOT CAUSE — one missing write disables the whole viewer-history product

`0084:109` adds `payments.viewer_identity_id` as nullable with no backfill. The only
`payments` INSERT — `record_verified_payment_webhook` (`0007`) — does not list the
column. Nothing anywhere sets it. It is NULL on every row ever written.

Readers filter `viewer_identity_id is not null` (`0105:981`, `0108:401`), so they
return empty rather than erroring. Permanently empty as a result:

| Downstream | State |
|---|---|
| `creator_supporter_relations` (`0084:94`) | never populated — has no writer at all either |
| Streaks, badges (`0107`) | always zero |
| Reputation score and verdict (`0120`) | always `clear` |
| Supporter history | `get_channel_supporter_history` also has no route |

**Fixing this single column write is the highest-leverage change in the codebase.**

Same class: `POST /v1/public/receipts` has no web caller, so no receipt token is
ever minted and `/r/[token]` is dead — removing the only claim path an anonymous
card/UPI tipper had.

---

## 2. UNREACHABLE — built, tested, committed, reachable by nobody

### Connectors — the whole YouTube feature cannot be switched on
| Capability | Missing piece |
|---|---|
| YouTube OAuth connect | no page calls `POST /v1/channels/:id/connectors/youtube/connect` |
| YouTube disconnect | no page calls the DELETE route |
| Connection status / revoked-auth prompt | nothing surfaces it; poller never sets `status='revoked'` on `invalid_grant` |

`/dashboard/sources` is contribution-source toggles only, not connector management.
Poller, quota budget, `streamList`, Super Chat, `!tip`, bot ack are all real and
tested — and unreachable, because a creator cannot connect an account.

### Engagement — the interaction layer has no viewer surface
The tip page (`apps/web/app/tips/[handle]/TipForm.tsx`) is the single choke point.
It sends an amount, a name and a message. Nothing else.

| Capability | Missing piece |
|---|---|
| Interaction menu (viewer picker) | component does not exist anywhere |
| Support votes (free) | no creator UI calls `createVoteOption`; no viewer UI casts a vote |
| Paid support votes | TipForm never sends `interactionDefinitionId` / `voteOptionKey` |
| Mega alert, priority question | no payment path can tag an interaction definition |
| Sticker selection (catalogue + creator packs) | TipForm has zero sticker code (a route comment at `stickers.ts:124` falsely claims a tip-page picker exists) |
| Hype mode | `startHypeMode` is defined in the API client with **zero callers** — it can never be started |
| Widget privacy scope | no UI calls `update_widget_config`; widgets stay `private` forever, and `0105:942` filters public reads on `privacy_scope='public'` |
| Staff creator-pack review (`0122`) | API-only, no admin page — curl or Postman only |
| Template catalogue | GET route exists, no frontend calls it |
| Challenge source-inclusion | route exists; `ChallengesPanel` never wires it (goals and interactions do) |

### Payments and ops
| Capability | Missing piece |
|---|---|
| **All six cron schedules** | `bharatstudio-crons/schedules/v1.json` has `"enabled": false` on every entry; README calls it "a disabled staging template". Includes `outbox-recovery`, the delivery pump. |
| Payment account activation | `activate_creator_payment_account` has zero non-test callers — accounts register `pending` (`0060:111-112`) and never activate |
| Manual-review quarantine | `resolve_reconciliation_manual_review` has zero callers; queue fills, never drains |
| Featured-creator curation | read function only; nothing sets the flag, so the list can never change |
| Provider capability snapshot | written on every capability check, read by nothing |
| Preferred UPI app memory | server allowlist only; the browser half its own comment references does not exist |
| Razorpay partner OAuth | `app.ts:268` passes `undefined` for `oauthConfig`; the route 503s in every environment |

### Viewer identity
| Capability | Missing piece |
|---|---|
| Platform-identity claim | route and DB logic complete; no page calls it |
| Badges / streaks route | no web component calls it |
| Receipt minting | no caller (see §1) |
| Reputation write path | `record_reputation_signal` has zero non-test callers — no chargeback hook in payment-webhook-go, no velocity or moderation-strike producer in youtube-poller-go |
| Reputation display | GET verdict route live; nothing in the web app or admin renders it |
| Anonymous browser identity | table exists, zero inserts outside tests |

---

## 3. ABSENT — never built (plan may claim otherwise)

**Falsely marked DONE in Part 7:** custom sound upload (zero "sound" hits repo-wide),
built-in themes (zero "theme" hits), 72-hour replay buffer (replay is cursor-based
with no time bound), Companion action/layout page size 8/16/32/64 (real values are
4/8/16 at route, type and DB CHECK).

**Content safety on TTS** — the largest risk item. `provider.ts:28-29` strips C0/DEL
control characters and bounds to 500 chars. That is the entire filter. No profanity
filter, URL removal, Unicode normalisation, blocked terms, blocked users, SSML
injection guard, RTL-override or zero-width stripping. A ₹10 tip puts arbitrary text
through a paid voice to a live audience.

**Also absent:** flag/report a supporter · block a supporter · DPDP data export ·
amount presets · saved page profiles (banner, socials, colours, logo) · desktop
QR-first layout · viewer-proposed challenges (`0109:192-196` hard-gates owner/admin)
· challenge completion evidence · challenge dispute record · `!challenge` · chat
display, retention, filtering · Twitch · Kick · payout/settlement status for creators
· TTS quota bar · asset storage quotas · media and sound libraries · custom templates
· per-item queue skip · malware scanning stage 2 (documented no-op) · on-call rotation
· activation instrumentation (nothing records "OBS connected" or "first alert
rendered"; `metrics.ts:31-32` has only `recordReconnectReplay` and `recordTtsFailure`).

---

## 4. GENUINELY USABLE

Tip page and payment capture end to end · webhook verification, dedup and the single
atomic transaction (delivery + payments + intent + alert_events + outbox) ·
multi-account attribution guard · payments ledger and CSV export · refund status
tracking, with derive-don't-store verified in two independent read paths (`0102:131-143`,
`0120:114-115`) · alert queues, bindings, modes, quiet hours, rate controls · SSE
overlay with cursor replay and cross-replica fan-out · overlay token design
(fragment-only, sha256 stored, per-overlay lookup, revoke and rotate) · moderation
approve/hold/suppress/replay with audit, including a correct lease-and-CAS that makes
the suspected suppress race impossible (`0004:29-42` keeps `status='ready'` and takes
a lease; `0030:40` guards release on `status='ready'`) · TTS synthesis, cache, quota
metering, amount ladder, chime and browser fallbacks · support goals · overlay widget
reads · external contribution aggregation (Super Chat → goals via `0117:433`) ·
creator-published challenges with state machine and honest failure disclosure shown
on-stream · sticker catalogue and creator packs (creator side) · AI assist with audit
· admin DLQ console · entitlement management · email outbox · viewer accounts, login,
password reset, DPDP deletion, opt-in profiles and search.

---

## 5. BLOCKED

Memberships (no recurring payments) · enterprise (Razorpay Route questions unsent) ·
Windows Companion (never compiled, `NETSDK1100`) · the 600 templates (raw HTML,
forbidden at every tier) · refund initiation (no escrow, no rail supports it) ·
bot chat acknowledgement (defaults off pending Google write-scope verification).

**External, unfiled — the real critical path:** Google OAuth verification, YouTube
Data API quota, legal sign-off, Razorpay Route enquiry.

---

## 6. Recommended order

1. `payments.viewer_identity_id` writer — unlocks supporter relations, streaks,
   badges, reputation and history in one change.
2. TTS content safety — the only item here with real-world harm potential.
3. YouTube connect/disconnect UI plus a revoked-auth prompt — makes a whole built
   subsystem usable and stops silent permanent failure.
4. TipForm as the interaction surface — stickers, paid votes, mega alert, priority
   question all unblock together.
5. Enable the cron schedules (needs the IAM and staging evidence L06 requires).
6. Payment-account activation, and a resolution path for the quarantine queue.
7. Receipt minting on the tip confirmation page.

Items 1, 3, 4 and 7 are wiring, not new design — the hard parts are built and tested.

---

## 7. Companion — the mobile app's controls are not connected

`CompanionShell` declares `onAction`, `onRunFullTest`, `onMuteTts`, `onCancelTts` and
`onModerate` as optional props. `App.tsx:143-165` passes **none of them** — only
`onSignIn`, `onSelectChannel`, `onRevokeSession` and
`onUpdateNotificationPreferences`.

So on mobile every OBS action, the run-full-test button, mute and cancel TTS, and
approve/reject moderation **render and do nothing**. Because the props are optional,
TypeScript is silent; because component tests inject their own mock handlers, the
97/97 suite passes. This is the same defect as §1 in a different layer, and it is
why "mobile is the furthest along" was wrong — its screens are the most complete and
its controls are inert.

| Capability | Verdict |
|---|---|
| Bounded actions, OBS control (mobile) | UNREACHABLE — `App.tsx` never passes `onAction` |
| Run full test (mobile) | UNREACHABLE — no `onRunFullTest`; ABSENT on web |
| Mute / cancel TTS (mobile) | UNREACHABLE — no `onMuteTts` / `onCancelTts`; absent on web |
| Approve / reject (mobile) | UNREACHABLE — no `onModerate` |
| Moderator seat management | UNREACHABLE — `PUT /v1/channels/:id/members/:userId` has zero callers on **any** surface, despite `0104` enforcing the limits |
| Control-session lease | PARTIAL — web never acquires one |
| Implicit channel provisioning | ABSENT — Companion cannot be sold standalone at any price |
| Stream health panel, helper diagnostics, offline queue-of-intent, per-item replay/skip | ABSENT |
| Terms, channel wizard, payout, billing actions, referral, grandfathering | web only; absent on mobile |
| Mirror and Stream actions | **BLOCKED**, not unreachable — `0093` hard-codes activation false because Mirror and Stream emit no liveness signal; the gate rejects every call by design |
| Activation instrumentation | ABSENT — `0093` keeps only live heartbeat columns, overwritten on each report. No durable "OBS connected" or "first alert rendered" event exists anywhere in any migration. |

Also confirmed: the six monetisation push notification types the plan names (tip above
threshold, queue stalled, overlay disconnected, payment failed, refund failed, TTS
quota exhausted) do not exist; the four that do are connection and session events.
Several Companion API endpoints (`companion/tips`, `companion/payments`, `tts/mute`,
`tts/cancel`) have no web caller.

---

## 8. How to stop this recurring

Every defect in §2 and §7 would be caught by one check that does not exist: **a test
that exercises a capability the way a user reaches it**, rather than calling the
function directly. Concretely worth adding:

- A lint or CI script that flags exported API-client functions with zero callers
  (`startHypeMode`, `updateWidgetConfig`), and SQL functions granted to an app role
  with no application caller (`activate_creator_payment_account`,
  `record_reputation_signal`, `resolve_reconciliation_manual_review`).
- A React check that flags declared-but-never-passed optional handler props.
- One end-to-end smoke path per product surface that drives the real UI.

Test count is not evidence of reachability. 496 + 324 + 97 passing tests coexisted
with everything above.
