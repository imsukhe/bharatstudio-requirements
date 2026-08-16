# BharatStudio full-product v1 master release authority

**Status:** `Proposed — release blocked; implementation and evidence work may continue`
**Owner:** Project owner
**Scope:** One public v1 launch of BharatStudio Alerts plus bundled Companion
**Authority companion:** [`00_LAUNCH_SCOPE_AUTHORITY.md`](./00_LAUNCH_SCOPE_AUTHORITY.md)
**Last reconciled:** 2026-08-15

This is the release decision record for the new workspace. It does not replace
the detailed task/test records and it does not promote local implementation,
disabled infrastructure or document review into production readiness.

## 1. Launch decision

The product is released as one complete v1 product, not an Alerts beta followed
by a later v1 completion. Public release requires every applicable L00–L10
track to reach `Verified` or to carry an explicitly approved conditional
exception with owner, expiry and rollback. YouTube and Enterprise remain Phase
2 and must not be represented as launch features.

### Included in v1

- Alerts public tip page, creator dashboard, creator-direct Razorpay boundary,
  durable queues, moderation/history, browser-source overlay and approved core
  configuration/template-library integration.
- Web Companion Console, React Native iOS/Android Companion, and Windows/macOS
  native helper work within the approved scope and release gates.
- BharatStudio parent marketing site with Alerts/Companion pages, pricing,
  support and legal/policy index surfaces.

### Excluded from v1

- YouTube data/live polling, Super Chat/memberships, catch-up summaries and
  YouTube chat/history ingestion.
- Enterprise workspaces, invites, allocations, reporting, settlement splits,
  enterprise payment routing and enterprise finance/refund authority.
- Client-owned entitlement decisions, Companion in-app checkout, public
  desktop APIs, arbitrary local commands and client-facing gRPC.

### v1 scope addendum — 2026-08-16

Owner direction (interactive session, explicit and twice-confirmed after an
initial self-correction) adds the following to "Included in v1" above,
reversing their earlier absence from this authority:

- Admin DLQ tooling: cross-channel quarantined/held alert-event review,
  replay (including content_flagged release) and terminal discard, for
  platform admins.
- Admin entitlement management: an operable surface to view/update the
  entitlement registry values introduced under L03/L04, with audit history.
- Featured-creator public listing: `GET /featured` and the `featured_consent`
  toggle, restoring what the parent marketing site's `/creators` page
  expects.
- Email delivery: a real provider integration (invoice/subscription
  events, DPDP export delivery, overlay-expiry reminder) — provider
  credentials remain an external gate per §5, but the integration code is
  v1-required.
- Referral/growth engine: creator-to-creator referral with fraud
  signals, credit FSM and self-serve dashboard.
- Lottie/custom branding upload: Studio-tier per-alert-type animation
  upload — object-storage credentials remain an external gate per §5, but
  the integration code is v1-required.

None of these change the non-negotiable invariants in §2 or the explicit
v1 exclusions above (YouTube, Enterprise, client-owned entitlements,
Companion in-app checkout, desktop public APIs, client-facing gRPC remain
excluded). Task/test records for each are tracked under the governing
L0x track in §4; where no existing track fits, treat as an L03 (web/API)
or L08 (marketing-adjacent, for the featured-creator listing) addendum
rather than opening a new track number.

### Entitlement values addendum — 2026-08-16

L03's task record (`tasks/L03-alerts-web-and-creator-api.md`) shipped
server-side enforcement for the `queueCount` entitlement key but left its
per-tier values unset, recording explicitly: "Other tier dimensions remain
unavailable until their approved entitlement keys and values are carried
into the active authority." That leaves `queueCount` enforcement a no-op
for every tier today (an unset limit means unlimited) and leaves downgrade
enforcement (pausing a channel's excess queues when its tier drops) with
nothing concrete to enforce against.

Owner direction (interactive session) approves the following `queueCount`
values, carrying over BharatStudio Alerts legacy's FRD-011-cited figures
(§5.2 "active queues per channel", §4.1 "five/ten queues per channel") as
the v1 basis, since the queue-based alert model these figures were written
against is unchanged in the rebuild:

| Tier    | queueCount |
|---------|-----------:|
| Free    | 1          |
| Pro     | 3          |
| Creator | 5          |
| Studio  | 10         |

This is the single source of truth for `queueCount` (implemented as
`app_private.tier_queue_count(tier)` in the database, not duplicated
elsewhere). Every other `configFeatures` dimension the entitlement
validator already supports in code (`allowedQueueModes`, `maxVisibleItems`,
`maxCharLimit`, `maxDisplayMs`, `ttsEnabled`, `quietMode`,
`approvalRequired`) remains explicitly unapproved and unset — per the
validator's own tested behaviour, an unset key never invents a
restriction, so this is a deliberate scope boundary, not a silent gap.
A future addendum must carry those values into this authority before any
of them are seeded.

### Referral credit mechanism addendum — 2026-08-16

The "v1 scope addendum" above requires a referral/growth engine but does
not specify how a referral credit is redeemed. Investigation found that
BharatStudio Alerts legacy's mechanism — a full Razorpay refund of the
next charge, "1 month free" — is structurally incompatible with this
repository: there is no refund-creation code anywhere in
`services/payment-webhook-go` (only read access to provider refunds
exists), `channel_subscriptions.recurring_price_paise` is CHECK-locked to
the three approved tier prices, and
`app_private.apply_channel_subscription_state` explicitly raises if a
subscription's price ever changes without a brand-new subscription.
Building the legacy mechanism would mean adding new outbound
money-movement code to the payment boundary — directly against
non-negotiable invariant #2 below (financial truth comes from the
server/payment ledger, not an inferred discount).

Owner decision (interactive session): a referral credit is a
**service-time credit, not a refund** — it extends the beneficiary
subscription's `current_period_end` by an owner-approved number of days,
recorded in a new ledger table and applied through the existing
entitlement-publish path with `recurring_price_paise` never touched. This
is a different product promise than legacy's "free month via refund" and
is the approved v1 design, not an inference from legacy code. Reward
size, fraud-signal set, and credit caps remain to be fixed in the L03
task record for this feature (legacy's specific numbers — 1 month, 12
active credits, 5/month, 14-day hold, 90-day expiry — are reference
values only, not carried over as authority).

This also resolves the conflict this addendum created with
`06_BACKEND_GAP_REMEDIATION_AUTHORITY.md`'s "Decision boundaries" section,
which had referrals as explicitly deferred; that document is updated to
point back here.

## 2. Non-negotiable release invariants

1. An accepted payment or alert evidence record is never dropped, deleted,
   silently acknowledged or rewritten because of tier, queue, rate, session,
   overlay, Companion, TTS, provider delay or capacity pressure. Limits may
   hold, delay, aggregate under an approved rule or require operator action.
2. Financial truth comes from the server/payment ledger, verified Razorpay
   webhook/reconciliation evidence and compensating records—not browser
   callbacks, support assertions or scheduler delivery receipts.
3. Per-queue delivery state is independent. Multi-queue source routing requires
   explicit duplicate consent on every participating binding; source/priority
   and override snapshots are immutable after acceptance.
4. Durable outbox/cursor replay is the overlay correctness path. SSE/`NOTIFY` is
   a wake-up optimisation only; pooled session-scoped `LISTEN` is forbidden.
5. RLS, service identity, server-owned entitlements and role-scoped projections
   enforce access. UI hiding, client checks and public documentation are not
   security boundaries.
6. Schedules, Cloud Tasks and observability templates remain disabled until
   private targets, IAM/OIDC, monitoring, retries, dead letters, recovery and
   staging evidence are recorded.
7. Public copy may claim only implemented and approved v1 behavior. Legal,
   tax, privacy, provider and app-store conclusions require dated primary or
   professional evidence.

## 3. Lifecycle and evidence rule

Each material track follows:

`Proposed → Approved → Implemented → Verified → Superseded`

It may instead be `Blocked` when an external dependency or unresolved defect
prevents progress. A status transition requires the task record, acceptance
record, dated evidence, reviewer/finding/disposition, owner and rollback or
recovery evidence where relevant. No document may approve itself by merely
describing the desired result.

## 4. Track authority and current disposition

| Track | Area | Governing task/test | Current disposition | Main remaining gate |
|---|---|---|---|---|
| L00 | Legacy freeze and inventory | `tasks/L00-*`, `tests/TC-L00-*` | Proposed/local inventory | final authority reconciliation |
| L01 | Contracts and database baseline | `tasks/L01-*`, `tests/L01-*` | Local evidence available | independent/security and deployed DB proof |
| L02 | RLS, archive and retention | `tasks/L02-*`, `tests/L02-*` | Isolated PostgreSQL proof conditionally passing | independent security/application review and deployment role/secret evidence |
| L03 | Alerts web and Creator API | `tasks/L03-*`, `tests/TC-L03-*` | Local implementation slices passing | browser/accessibility, provider, cross-replica and staging |
| L04 | Go payment boundary | `tasks/L04-*`, `tests/TC-L04-*` | Local persistence/provider-contract slices passing | Razorpay approval, sandbox/live and deployed IAM/staging |
| L05 | Go dispatch and Cloud Tasks | `tasks/L05-*`, `tests/TC-L05-*` | Local routing/lease/pump slices passing | live Cloud Tasks, cross-replica overlay, capacity/failure rehearsal |
| L06 | Scheduler boundary | `tasks/L06-*`, `tests/TC-L06-*` | Local disabled templates/operations contract passing | deployed OIDC/IAM, target recovery and monitoring rehearsal |
| L07 | Companion web/mobile/desktop | `tasks/L07-*`, `tests/TC-L07-*` | Web/mobile/macOS scaffolds passing | Windows, native security, store/signing/device evidence and audit remediation |
| L08 | Marketing/support/legal | `tasks/L08-*`, `tests/TC-L08-*` | Static parent/product surface passing | external evidence, support operations, public copy/hosting |
| L09 | Observability/load/failure | `tasks/L09-*`, `tests/TC-L09-*` | Local instrumentation and contract passing | deployed dashboards, declared targets, capacity/fault proof |
| L10 | Release readiness | `tasks/L10-*`, `tests/TC-L10-*` | Blocked | all L00–L09 and external gates |

The 359 missing BSA runtime packages remain a deliberately tracked launch
requirement under [`PENDING-04-TEMPLATE-RUNTIME-PACKAGE-COMPLETION.md`](../../pending/launch/PENDING-04-TEMPLATE-RUNTIME-PACKAGE-COMPLETION.md).
New visual generation is deferred by owner direction until the final
implementation pass; this authority does not reduce the approved catalogue
scope.

## 5. Release-blocking external and deployment gates

The following cannot be closed from local tests or assumptions:

- written Razorpay Technology Partner/connected-account approval and creator-
  direct sandbox/live order, webhook, refund and reconciliation evidence;
- chosen Neon region/compute plan, Cloud Run min/max/concurrency, direct and
  pooled connection budgets, secrets, domains, WAF, backups and rollback;
- private OIDC/IAM for payment, worker, scheduler, Cloud Tasks and metrics;
- staging proof of duplicate/out-of-order webhook/task, queue burst, cross-
  replica SSE, notification outage, offline overlay, crash, DLQ, TTS/provider
  delay and restore/rollback behavior;
- React Native store accounts/signing/review, Windows build/signing and
  macOS signing/notarisation/distribution;
- dated CA/legal/privacy/provider/app-store review, approved policy versions,
  support staffing/on-call and incident rehearsal;
- independent or explicitly documented self-review evidence as allowed by the
  current governance decision.

The canonical support and external-evidence register is
[`05_SUPPORT_AND_EXTERNAL_EVIDENCE_REGISTER.md`](./05_SUPPORT_AND_EXTERNAL_EVIDENCE_REGISTER.md).

## 6. Go/no-go rule

The release owner may approve public launch only when:

1. every applicable L00–L09 acceptance case has dated evidence and a recorded
   disposition;
2. no unowned critical/high issue remains and all conditional exceptions have
   an expiry, owner and mitigation;
3. provider, legal/tax/privacy, store, infrastructure, support, monitoring,
   backup/restore and rollback gates are affirmative;
4. a production-like rehearsal reconciles payment ledger, webhook deliveries,
   refunds, outbox, per-queue deliveries, overlay cursors and audit records;
5. launch cohort, capacity guardrails, incident commander, freeze window,
   rollback triggers and public status communication are active.

Until then, the product is unreleased. No `READY FOR LAUNCH` wording may appear
in a status file or public surface.

## 7. Change control

Any change to launch scope, payment flow, tier limits, pricing, data retention,
platform, protocol, architecture, or public claims requires an update to this
authority and the affected task/test/review records before implementation.
Superseded material is archived with a reason; it is never silently deleted.
