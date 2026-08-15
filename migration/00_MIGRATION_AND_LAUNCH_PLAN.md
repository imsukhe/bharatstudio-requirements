# Migration and launch plan — legacy Alerts to BharatStudio v1

**Status:** `Active execution plan — new-repository implementation in progress; production migration and cutover not approved`  
**Owner:** Project owner  
**Legacy source:** `/Users/sukhdevsingh/Workspace/Personal /bharatstudio-alerts/repositories/bharatstudio-alerts` at `6679bf6` (`master`)  
**Scope:** v1 full-product launch only. YouTube and Enterprise remain Phase 2.

The clean v1 repositories now contain locally verified implementation slices for
the REST/API foundation, database contracts and security harness, payment
boundary, alert-worker dispatch protocol, scheduler-only contracts, marketing
surface and Companion scaffolds. This document remains the authority for what
may be migrated and how; local implementation evidence does not authorise a
production database migration, provider cutover or public launch.

## 1. Outcome and non-negotiable rules

The legacy repository is a valuable implementation and evidence source, not a folder to copy wholesale. Its current inventory is approximately **176 tracked web files, 110 tracked API files, 125 database files, 17 top-level tests, 24 requirements, 15 task documents, 22 technical-audit files**, and substantial untracked dependency/build output. Some implementation exists; no component is automatically launch-verified merely because a previous document says “complete.”

Migration rules:

1. Preserve the legacy repository untouched and tag/snapshot its current commit before copying anything.
2. Never copy `node_modules`, `.next`, `dist`, `.turbo`, local keys, `.env*`, private overlay URLs, build output, or unreviewed archives.
3. Never mechanically translate TypeScript into Go. Lock behaviour first with characterization tests and a versioned contract; rebuild isolated boundaries in Go.
4. Do not move legacy SQL migrations into a new production database unchanged. They include historical re-creates, RLS disable/rollback, and superseded table transitions. First create a reviewed **clean baseline schema** plus an upgrade path for any retained test/staging data.
5. Extract only specific, still-agreed, unfinished FRD sections into `bharatstudio-requirements/pending/launch/`. All other FRDs remain legacy evidence, completed evidence, Phase 2 source, or archive.
6. Phase 2 directories are a deliberate product boundary. They do not authorise code, UI, scopes, or marketing for YouTube/Enterprise in v1.

## 2. Final repository layout

```text
Bharat Studio/
├── bharatstudio-requirements/
│   ├── active/launch/              # one v1 authority
│   ├── pending/launch/             # narrow agreed unfinished slices only
│   ├── done/                       # reusable evidence inventory
│   ├── phase-2/{youtube,enterprise}/
│   ├── migration/ tasks/ tests/ reviews/ governance/ archive/
├── bharatstudio-infra/
├── bharatstudio-marketing/
├── bharatstudio-alerts/
│   ├── apps/{web,api}/
│   ├── services/{payment-webhook-go,alert-worker-go,youtube-poller-go}/
│   ├── contracts/{openapi,events,json-schema,fixtures,enums,design-tokens}/
│   ├── packages/{db,web-ui}/
│   ├── deployment/ tests/ tasks/ docs/
├── bharatstudio-companion-mobile/
├── bharatstudio-companion-desktop/{windows,macos}/
└── bharatstudio-crons/
```

## 3. Protocol and runtime target

| Boundary | v1 decision |
|---|---|
| Web/mobile/desktop to creator API | HTTPS REST + JSON, OpenAPI versioned |
| Browser source to service | HTTPS + SSE for live overlay delivery; durable outbox plus cursor/replay is the correctness path |
| Razorpay to payment service | HTTPS POST, verified HMAC, `x-razorpay-event-id` deduplication, idempotent receipt persistence before acknowledgement |
| Payment receipt to alert work | transactional outbox → Cloud Tasks → private Go handler |
| Scheduler to target | Cloud Scheduler → private HTTPS endpoint with OIDC |
| Desktop helper to OBS | authenticated localhost OBS WebSocket after explicit pairing |
| Contracts | OpenAPI, JSON Schema event envelopes, JSON fixtures/enums; no cross-language runtime package |

Do not introduce GraphQL, client-facing gRPC, Kafka, a generic broker, public helper API, or direct database access from companion clients in v1.

## 4. Existing implementation: disposition map

### 4.1 Web application — legacy `apps/web` (176 tracked files)

| Legacy area | New home | Disposition | Required work |
|---|---|---|---|
| `(marketing)` routes, marketing components, SEO routes | `bharatstudio-marketing` | **Selective rewrite/copy after content audit** | Split parent BharatStudio pages from Alerts-specific pages; replace stale price/product copy; remove exposed internals; retain generic layout/components only after tests. |
| Dashboard, onboarding, config, queues, payments, settings, team | `bharatstudio-alerts/apps/web` | **Selective migration** | Keep UI behaviour only where v1 authority permits; replace Next route-handler database calls with Creator API client calls; exclude Enterprise UI and YouTube controls. |
| `/tips/[handle]`, `/overlay/*`, `/hud`, test alert | `bharatstudio-alerts/apps/web` | **Selective migration + security rewrite** | Retain UI/reference tests; rebuild token/session, SSE reconnect/resync, long-text layout and safe preview against final API contracts. |
| `apps/web/src/app/api/*` route handlers | `bharatstudio-alerts/apps/api` or Go services | **Rewrite, do not move as web routes** | Move domain endpoints to the TypeScript Creator API; move payment webhook/receipt to Go; preserve client routes only as BFF proxies if formally needed. |
| NextAuth/Google login | Alerts API + web/mobile clients | **Rebuild against final auth contract** | Google Sign-In only; no YouTube scopes in v1; add session revoke/device handling and platform callback tests. |
| Workspace/Enterprise pages and components | Phase 2 Enterprise | **Do not migrate into v1 UI** | Preserve as evidence only; normal creator/collaborator roles are re-specified separately if approved. |
| YouTube routes/components | Phase 2 YouTube | **Do not migrate** | No scopes, route, UI, data or flags in v1 besides non-YouTube auth. |

### 4.2 API application — legacy `apps/api` (110 tracked files)

| Legacy area | New home | Disposition | Required work |
|---|---|---|---|
| Fastify bootstrap, auth, CORS, headers, validation, rate limit | `bharatstudio-alerts/apps/api` | **Selective rewrite/reuse** | Retain proven policy/test intent, rebuild with clean service-specific composition and final OpenAPI. |
| Creator, channel, configuration, alert, overlay, referral, billing control routes | `bharatstudio-alerts/apps/api` | **Selective migration** | Reimplement only v1 endpoints; consistent RBAC/RLS context; no direct client DB assumptions. |
| `routes/tips`, `routes/webhooks/razorpay`, Razorpay client | `services/payment-webhook-go` + Creator API public order endpoint | **Go rewrite with parity tests** | Separate order creation, provider adapter, webhook verification, immutable ledger, refund/reversal, reconciliation trigger, idempotency, audit and receipt response deadline. |
| `workers/alert-delivery`, queue dispatch, overlay fan-out, TTS coordination | `services/alert-worker-go` | **Go rewrite with characterization and shadow proof** | Replace interval/lease model with Cloud Tasks per-event dispatch; preserve all queue modes, frozen config snapshot, holding, aggregation, priority, approval, TTS fallbacks, replay, no-drop semantics. |
| `workers/reconciliation`, expiry/archive/audit archive | private v1 API endpoints invoked by `bharatstudio-crons` | **Extract handler contracts; rewrite schedules later** | A cron cannot hold DB credentials. Private handler owns idempotent mutation; scheduler owns only invocation/retry schedule. |
| `workers/youtube-polling`, YouTube client, cursor tests | `services/youtube-poller-go` and Phase 2 requirements | **Do not migrate in v1** | Preserve code/tests/evidence only. Rebuild only after YouTube scope/quotas/leases are approved. |
| load tests / trace / metrics / circuit-breaker / R2 / token encryption | appropriate Alerts services/tests | **Selective reuse, revalidate** | Carry test fixtures and metric names where valid; remeasure against final region/database/provider configuration. |

### 4.3 Database package — legacy `packages/db` (125 tracked files)

| Legacy asset | New home | Disposition | Required work |
|---|---|---|---|
| Drizzle schema files | `bharatstudio-alerts/packages/db/schema-reference/` initially | **Reference, then clean re-authoring** | Build an approved v1 logical model; do not make multi-language services share Drizzle runtime code. |
| migrations `0000`–`0083` | `bharatstudio-alerts/packages/db/legacy-migrations/` as immutable evidence | **Preserve, do not execute as new baseline** | Produce reviewed v1 `baseline.sql` / migration chain and documented upgrade strategy. |
| RLS roles/policies/scripts | final Alerts database migration + security tests | **Selective re-authoring** | Reconcile existing 6+2+5 bypass union, request context, `SECURITY DEFINER` privileges, and archival proof. |
| pubsub/listen/advisory locking | final service-specific DB design | **Rewrite** | Do not reuse pooled session-lock pattern. Cloud Tasks removes dispatch polling. v1 uses a dedicated direct listener only as best-effort wake-up; the connection is included in the database budget. Do not use `LISTEN/NOTIFY` through a transaction-pooled endpoint. Durable outbox/cursor replay remains authoritative; a broker requires a later measured capacity decision. |
| cross-replica SSE fan-out and entitlement invalidation | `bharatstudio-requirements/pending/launch/PENDING-03-MIGRATION-CROSS-CUTTING-GAPS.md` | **Launch blocker** | Prove overlay delivery from one API/worker replica to an overlay connected to another. Live notification is best-effort; replay, version checks and TTL fallback must work when notification delivery is unavailable. |
| test bootstrap, seed and fixtures | `bharatstudio-alerts/tests/characterization` + contracts fixtures | **Selective migration** | Sanitize and minimize; no production data. |

### 4.4 Legacy packages, deployment and evidence

| Legacy asset | New home | Disposition |
|---|---|---|
| `packages/queue` | alert worker Go implementation | Replace; it is TypeScript-only runtime logic. Preserve tests/behaviour matrix. |
| `packages/email` | Alerts notification module | Selectively migrate templates after legal/brand copy review. |
| `packages/tsconfig` | each TypeScript repo | Do not centralize cross-language config; copy only relevant config locally. |
| deployment Dockerfiles/cloudbuild/runbooks | `bharatstudio-infra` plus per-service deployment descriptors | Rewrite from final service topology; retain old files as evidence. |
| RLS, load, trace, restoration, DLQ, reconciliation, fanout evidence docs | `bharatstudio-requirements/done/` index + task references | Do not bulk copy. Cite exact legacy evidence on the relevant task. |
| `bharatstudio-crons` legacy scaffold | new `bharatstudio-crons` | Supersede its old business-logic ownership language; scheduler-only is authoritative now. |
| alert template library | no active repo yet | Keep outside migration. Integrate only an approved/quality-reviewed catalogue later. |

## 5. Required new baseline before copying production code

1. **Legacy freeze:** record commit `6679bf6`, Git status, source inventory, and secret scan result.
2. **Contract baseline:** write OpenAPI for v1 Creator API; JSON Schemas for payment receipt, alert event, dispatch command, overlay SSE event, error envelope and entitlement result; create shared golden fixtures.
3. **Database baseline:** derive v1 schema and roles from approved v1 scope. Preserve old migrations in evidence but do not run the historical chain against a clean environment.
4. **Behaviour characterization:** use current tests plus new black-box cases for payment, queue/delivery, overlay replay, RLS, entitlement downgrade, and archival integrity.
5. **Service implementation:** Go services must pass the same fixture and end-to-end behaviour suite before either receives production traffic.
6. **Environment and cutover:** each service begins in isolated local/staging configuration; use shadow/read-only comparison where possible; use a feature flag and rollback route for every cutover.

### 5.1 Required cross-cutting decisions carried into implementation

- The v1 SSE contract must specify the durable cursor, replay boundary, per-overlay acknowledgement, reconnect behaviour and cross-replica publication path.
- A pooled Neon connection must never be used for a session-scoped `LISTEN` subscription. v1 uses a dedicated direct listener connection with startup assertion, reconnect, metrics and a staging cross-replica test. Its connection count is part of capacity sizing. Listener failure disables live wake-up and falls back to outbox/cursor replay; a broker is not added unless measured staging capacity requires it.
- Entitlement cache invalidation must not rely solely on PostgreSQL notifications. A version/updated-at check or bounded TTL must converge after missed notifications.
- Cloud Tasks replaces the polling leader, not idempotency. Task retries and concurrent handler execution remain possible and must be safe.
- D-2 is binding: multi-queue source routing ships in v1. `L-31` proves source-to-priority correlation and `L-32` proves per-source overrides before bindings UI release; per-queue outbox state, not a global event status, controls independent progress.

## 6. Launch work packages and dependency-based sequencing

The detailed checklists live in `../tasks/`. Work may proceed in parallel when its approved contracts and dependencies are complete. Do not implement dependent behaviour against an unapproved contract, and do not allow parallel changes to the same files without an explicit owner. Final launch remains gated by L10; parallel execution does not weaken acceptance or review requirements.

| Wave | Package | Start condition | Outcome |
|---:|---|---|---|
| 0 | Governance and legacy freeze | Immediate | immutable evidence/index; no active ambiguity |
| 1 | Contracts and database baseline | L00 authority/evidence complete | v1 API/event/schema source of truth |
| 2A | Security/RLS/archive residual closure | L01 security contracts | production-safe DB roles and proven archive path |
| 2B | Mobile framework spike, OS-floor decision, store accounts and legal/provider applications | L01 scope/contracts; owner approval for floors | removes external lead-time risk before app implementation |
| 2C | Alerts web and Creator API extraction | L01 API contracts | dashboard, overlay and tip UI use final REST contracts |
| 2D | Worker characterization, infrastructure and observability harness | L01 event/queue contracts | reduces rework before Go services and full staging |
| 3A | Go payment boundary | L01 + payment contracts; may overlap L03 implementation | webhook/receipt/order/refund/recovery parity in staging |
| 3B | Go alert worker and Cloud Tasks | L01 queue contracts; payment receipt contract | no-drop task-driven dispatch/replay proof |
| 3C | Scheduled invocation boundary | private handler contracts | OIDC handlers and scheduler-only repository proof |
| 4 | Companion web/mobile/desktop implementation and marketing/support build | respective contracts; early legal work already running | authorised, accessible, secure v1 product surfaces |
| 5 | Integrated observability, load, failure and recovery | all runtime candidates deployed to staging | proof against declared targets |
| 6 | Final legal/provider/store review and production rollout | implementation and staging evidence | all gates, approvals, rollback rehearsal |

### 6.1 Active implementation queue — execution order

This queue is the operational continuation list. A release gate is not a
substitute for an unfinished implementation item. Each item must be built,
tested locally, and recorded against its task before the next dependent item
is treated as complete. Items marked `external` are prepared in parallel but
cannot be claimed as passed from local code.

| ID | Work item | Current state | Next executable action | Depends on |
|---|---|---|---|---|
| I-01 | Alerts web core: dashboard, tip page, overlay setup, queues, config, history, moderation and billing | Local slices implemented | Run browser/accessibility contract matrix and close any local defects | L03/L04 contracts |
| I-02 | Web Companion Console: activity, health, connection state, plan locks, sessions, recovery and approved controls | Local screen slice implemented 2026-08-15 | Run authenticated browser/accessibility and multi-channel checks; add only approved missing API surfaces | I-01 |
| I-03 | Source binding and multi-queue UI | Local UI/API behind flag | Verify L31/L32 in staging, then enable the reviewed UI | L03/L05, staging |
| I-04 | Visual-template runtime and catalogue | Deferred by owner; BSA generation not run now | Complete the approved 600-design runtime packages, then browser/long-text/reduced-motion review | L03 core, pending visual authority |
| I-05 | Razorpay public checkout handoff | Local boundary implemented | Configure sandbox, execute order/payment/webhook/expiry/refund scenarios, reconcile evidence | L04, provider credentials |
| I-06 | Payment webhook and recovery service | Go local tests pass | Deploy private service, verify HMAC/dedup/account attribution/retry and provider replay | L04, IAM/provider |
| I-07 | Alert worker and Cloud Tasks dispatch | Go local tests pass | Deploy handler/tasks, prove no-drop, retry, lease, TTS fallback and cross-replica replay | L05, IAM/capacity |
| I-08 | Scheduler-only jobs and maintenance handlers | Local contracts/handlers partial | Deploy OIDC scheduler, then rehearse expiry/reconciliation/refund/archive recovery | L06, IAM/provider |
| I-09 | Mobile Companion screen implementation | Local screen/API/runtime/projection slices implemented; notification preference/device API now exists; native/device work remains | Wire approved control callbacks into final UI, complete native permission/background hooks, then run device/accessibility checks | I-02, final REST, L07-33 |
| I-10 | Mobile Google sign-in and secure session storage | Local exchange, secure store, controller and bootstrap adapter implemented | Select/configure native identity bridge, verify Keychain/Keystore on devices, and test revoke/expiry/restart | owner floors, release accounts |
| I-11 | Mobile push, offline/reconnect/background sync | Privacy-minimised policy, native APNs/FCM adapter and authenticated server preference/device registration contract implemented locally | Inject provider credentials, wire consented UI registration and background hooks, prove physical-device delivery/revocation/key rotation, and keep push best-effort with no financial/alert buffering | I-10, L07-33, provider/device evidence |
| I-12 | Mobile control-session lease and action/page enforcement | Server/API and mobile acquire/renew/revoke manager implemented | Wire manager to rendered controls, prove conflict/retry and server action enforcement without affecting alerts | I-10, L03/L07 |
| I-13 | Desktop Windows helper | Policy/response decoder and loopback OBS client source boundary implemented; SDK unavailable here | Build WinUI 3 UI, approved pairing transport, Credential Manager/DPAPI storage, lease-bound scoped commands and diagnostics; compile/package/sign on Windows | approved pairing protocol, Windows SDK |
| I-14 | Desktop macOS helper | Swift policy, Keychain store and loopback OBS v5 client slices implemented | Build approved pairing transport, REST/session lifecycle, lease-bound reconnect/revocation and redacted diagnostics; run real OBS/device/signing evidence | approved pairing protocol, macOS device/signing |
| I-15 | Desktop packaging/update/crash recovery | Not implemented | Configure MSIX/signing and macOS signing/notarisation, update rollback and crash evidence | I-13/I-14, release accounts |
| I-16 | BharatStudio marketing/support/legal surfaces | Static marketing shell/local tests pass | Finalise public product/pricing/support/legal copy, CSP/SEO/accessibility and provider disclosures | L08, counsel/content |
| I-17 | Observability, load, failure and recovery | Local instrumentation/tests pass | Deploy topology, measure declared targets, inject provider/DB/worker/overlay failures, rehearse rollback | I-05–I-16 deployed |
| I-18 | Full-product integrated acceptance | Not started | Execute end-to-end matrix across Alerts web, mobile, desktop, payment, queues, overlay and support flows | I-01–I-17 |
| I-19 | External launch approvals | External and not locally claimable | Razorpay/provider, app stores, legal/privacy, production IAM/domain approval | I-05/I-10/I-15/I-16 |
| I-20 | Production migration and launch | Blocked | Run final authority checklist, migration rehearsal, rollback rehearsal and public release | I-18/I-19 |

The current continuation point is **I-02**, followed by **I-09**. Work on
I-03, I-04 and I-05–I-08 can proceed in parallel where their contracts are
already complete, but none may be skipped because another workstream is
waiting on an external approval. No item permits YouTube or Enterprise work;
those remain Phase 2.

## 7. Phase 2 handoff

No v1 task may silently absorb YouTube or Enterprise work. Their complete legacy plan references, preconditions, and first reopening tasks are recorded in:

- `../phase-2/youtube/`
- `../phase-2/enterprise/`

When reopened, each begins with a new narrow authority slice, a task, an acceptance record and an independent review. The existing P16 and P28 task plans are starting evidence, not automatically approved execution plans.
