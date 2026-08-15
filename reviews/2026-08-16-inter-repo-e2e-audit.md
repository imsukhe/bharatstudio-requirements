# Inter-repository, architecture and end-to-end audit — 2026-08-16

**Status:** `Conditionally complete locally; production blocked`

**Scope:** Third-pass deep audit of repository boundaries, cross-repository
paths, runtime ownership, API/OpenAPI/client wire contracts, payment-to-worker
delivery, scheduler routing, Companion consumers and failure/recovery paths.
This is remediation and evidence, not a production approval.

## Repositories and ownership checked

| Repository | Owns | Must not own |
|---|---|---|
| `bharatstudio-alerts` | Alerts web, TypeScript Creator API, DB contracts/migrations, Go payment ingress and Go alert worker | scheduler credentials, public worker ingress, Enterprise/YouTube v1 behavior |
| `bharatstudio-crons` | disabled schedule catalogue, OIDC target metadata and operator runbook | SQL, provider credentials, business mutation or database access |
| `bharatstudio-infra` | service IDs, deployment/IAM/secret references, task/scheduler topology and observability contract | secret values, product logic, migrations |
| `bharatstudio-companion-mobile` | iOS/Android client contract and UI boundary | payment/queue truth, local entitlement authority, raw notification payload display |
| `bharatstudio-companion-desktop` | Windows/macOS local helper policy and native transport boundary | public listener, arbitrary commands, OBS credential disclosure, server authority |
| `bharatstudio-marketing` | public static parent/product/support/legal pages | dashboard data, payment state, private architecture or provider secrets |
| `bharatstudio-requirements` | authority, tasks, acceptance evidence and review records | runtime code, generated assets, secrets |

## Findings fixed in this pass

| ID | Severity | Finding | Disposition |
|---|---:|---|---|
| IR-2026-08-16-01 | High | The cron catalogue named archive routes as if they were executable even though the Alerts API rejects them and no archive handler is enabled. | Added `implementationStatus` to every schedule; event/audit archive entries are `planned` and mechanically disabled. The runbook now states that valid JSON is not evidence that a target exists. |
| IR-2026-08-16-02 | High | Scheduler target names (`bharatstudio-alerts`, `bharatstudio-payment-webhook`, `bharatstudio-alert-worker`) were not explicitly tied to the deployment manifest IDs (`alerts-api`, `payment-webhook`, `alert-worker`). | Added required `target.serviceId` to the scheduler contract and all six schedules; tests assert payment/refund, worker pump and Alerts maintenance mappings. |
| IR-2026-08-16-03 | High | Companion action clients and server disagreed about whether a queue target was optional; the API implementation rejects a missing target. | Made `targetId` required and UUID-shaped in the API, OpenAPI and Web client. Missing-target API coverage remains fail-closed. |
| IR-2026-08-16-04 | High | Windows decoded the action result under stale `resultEventId`, while the shared Web/mobile/API contract uses `eventId`. | Corrected Windows and added macOS model coverage plus a portable Windows smoke test. |
| IR-2026-08-16-05 | Medium | Payment ingress → worker pump had unit coverage but no HTTP boundary test for the canonical path, trace propagation and retry response. | Added TLS `httptest` coverage through the real `WorkerPumpClient` for success and worker-503 retry behavior. |
| IR-2026-08-16-06 | Medium | Phase-2 documents contained absolute paths to the archived legacy repository, which could be mistaken for active source paths. | Replaced active phase-2 path references with legacy filenames plus the central evidence-register link. Historical migration evidence retains the original source path intentionally. |
| IR-2026-08-16-07 | High | Scheduler entries described target URLs and cadence but not the HTTP method/body required by the owning handlers; the Alerts maintenance handler requires an idempotency key and window. | Added a required JSON `POST` request template with stable `schedule:<id>:<window>` idempotency key and concrete-window placeholder to the scheduler contract, fixtures, runbook and L06 acceptance record. |

## End-to-end flow verdicts

### Payment → durable ledger → worker → overlay

Local code and synthetic database evidence show the intended sequence:

1. Razorpay webhook signature and `X-Razorpay-Event-Id` are verified.
2. The payment boundary persists the append-only webhook/payment/outbox state.
3. The payment boundary calls the private worker pump with a bounded OIDC client.
4. A pump failure returns retryable `503`; durable state remains replayable.
5. The worker creates stable Cloud Tasks identities and the task handler claims,
   publishes and releases delivery state without acknowledging on presentation
   failure.
6. Overlay SSE reconnect/cursor replay is the presentation recovery path; the
   overlay never becomes the source of financial truth.

The new HTTP boundary tests cover steps 3–4 locally. Disposable PostgreSQL and
Go tests cover the durable state transitions. Real Razorpay, Cloud Run OIDC,
Cloud Tasks, deployed cross-replica SSE, OBS browser source and capacity proof
remain open release gates.

### Scheduler → owning service

Payment/refund reconciliation targets the Go payment service, outbox recovery
targets the Go Alert Worker, and only overlay-session maintenance targets the
Alerts API. Archive schedules are placeholders and remain disabled. The
scheduler has no database credentials and cannot create a false success by
calling an unsupported owner.

### Companion web/mobile/desktop → API

All clients consume bounded v1 projections and server-owned roles/leases. The
action target is now mandatory and the action-result event identity is
`eventId` across consumers. Web/mobile/macOS local contract tests pass; the
Windows smoke test is present but requires a Windows/.NET runner. Native
pairing, secure OS credential storage, real OBS, push providers, device and
store evidence remain unfinished by design and are not claimed here.

## Component and flow evidence

- Alerts API and Web suites, production build and OpenAPI/fixture validation.
- Payment and worker Go unit tests, race tests, vet and the new TLS HTTP
  boundary tests.
- Disposable PostgreSQL L02/L03 security/application harness, including
  duplicate webhook, queue delivery, maintenance and multi-queue behavior.
- Cron schedule contract tests, including planned-schedule disabling and
  canonical service IDs.
- Mobile Jest/lint/typecheck/config/dependency checks.
- macOS Swift tests and Windows portable contract smoke source.
- Infrastructure and marketing contract tests.

## Remaining risks and required evidence

1. Deploy the three service boundaries and prove private OIDC/IAM negative
   paths, not only local route behavior.
2. Provision the approved Neon region/compute/connection topology and prove
   direct `LISTEN/NOTIFY` behavior across replicas; pooled listeners remain
   forbidden.
3. Run Razorpay sandbox checkout, duplicate webhook, delayed webhook, refund,
   reconciliation and provider retry tests with approved credentials.
4. Run Cloud Tasks partial-failure, retry, dead-letter and worker-restart
   rehearsals with durable-row reconciliation.
5. Run authenticated browser/OBS, SSE reconnect/resync, accessibility,
   localisation, long-text and reduced-motion matrices.
6. Run iOS/Android physical-device APNs/FCM/background/reconnect tests and
   Windows/macOS pairing, Keychain/Credential Manager, OBS, signing and
   distribution tests.
7. Complete legal/privacy/support/provider review and an independent fresh
   release review.

**Verdict:** No new uncontained cross-repository data-loss, tenant-isolation or
wire-contract defect remains in the locally testable slice after this pass.
The product is not production-ready until the external/deployed/device gates
above have real evidence; local tests must not be interpreted as those proofs.
