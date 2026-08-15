# L09 observability review

**Date:** 2026-08-15  
**Reviewer:** Codex self-review  
**Independent reviewer:** Not performed in this pass  
**Decision state:** `Instrumentation slice complete; L09 remains open`

## Findings and dispositions

| ID | Finding | Severity | Disposition |
|---|---|---:|---|
| L09-R1 | A public metrics endpoint could expose route/query identifiers or operational topology | High | Fixed locally: API, payment and worker metrics require internal service identity; query strings and unknown attacker-controlled paths are collapsed into bounded labels; tests check authorization and identifier absence |
| L09-R2 | In-memory API counters are not a replacement for durable monitoring | High | Open: integrate scrape target, dashboards, alerts, retention and cross-service trace correlation in staging |
| L09-R3 | No load or fault result can be inferred from local unit/API tests | High | Open: run final-region staging measurements after L04/L05/L07/L08 deployment candidates exist |
| L09-R4 | Independent review is unavailable in this pass | Process | Recorded; L09 remains conditional/open |
| L09-R5 | The payment-to-worker internal hop did not carry a bounded trace identifier | Medium | Fixed locally: verified webhook derives `razorpay:<provider-event-id>` and sends it as `X-BSA-Trace-Id`; ingress tests pass. Full cross-service correlation remains open in staging |
| L09-R6 | Payment checkout metrics used a stale route label and collapsed real checkout traffic into `/_other` | Medium | Fixed locally: normalization now preserves `/internal/v1/tips/orders` while removing query strings; regression test passes |
| L09-R7 | Worker HTTP metrics did not distinguish accepted delivery work from ignored claims, retryable failures or partial pump failures | Medium | Fixed locally: authenticated business counters use fixed task/pump outcome allowlists and collapse unknown values; worker tests and `go vet` pass. Durable scrape, dashboard and alert policy evidence remains open |
| L09-R8 | Payment HTTP metrics did not distinguish accepted, duplicate, invalid and retryable webhook outcomes | Medium | Fixed locally: the webhook boundary records fixed outcome categories only; metrics tests prove provider identifiers and unknown labels are not emitted. Durable scrape, dashboard and alert policy evidence remains open |
| L09-R9 | Payment checkout and reconciliation outcomes were visible only through HTTP status, making provider recovery and order-initiation health difficult to alert on separately | Medium | Fixed locally: checkout and payment/refund reconciliation handlers emit bounded business outcome categories with no financial identifiers. Durable scrape, dashboard and alert policy evidence remains open |
| L09-R10 | Instrumentation existed without a declarative dashboard/alert boundary, so a deployment could omit ownership, forbidden labels or actionable recovery signals | High | Fixed locally: `bharatstudio-infra/deployment/v1/observability.template.json` declares private scrape targets, five dashboard domains, eight alert categories, owners/actions and forbidden identifier/payload labels. Thresholds and live routing remain deployment gates | SRE/security; measure thresholds and rehearse in staging |

## Evidence

- `pnpm --filter @bharatstudio/alerts-api test`: 27 tests pass.
- `pnpm --filter @bharatstudio/alerts-api build`: pass.
- Payment and alert-worker `go test ./...` and `go vet ./...`: pass, including authenticated metrics and bounded-route tests.
- No staging, production, provider, Cloud Tasks, mobile/desktop or cross-replica load evidence was used.
- `services/payment-webhook-go/internal/ingress` tests prove server-derived trace propagation across the private worker-pump request without trusting inbound trace headers.
- `services/alert-worker-go/internal/observability` tests prove business outcomes are bounded and redacted; handler wiring records task and pump outcomes without identifiers.
- `services/payment-webhook-go/internal/observability` and ingress tests prove webhook business outcomes are bounded and redacted; provider identifiers are not metric labels.
- Race-enabled local verification passes for both Go services; this is concurrency evidence only and does not replace deployed load, scrape, dashboard or fault-recovery proof.

## Fresh local audit — 2026-08-15

The API/payment/worker instrumentation, redaction and trace contracts,
cross-replica overlay proof, infrastructure observability template and L09
acceptance record were re-read together. No new locally verifiable defect was
found.

The local guarantee is limited and explicit: accepted payment/alert evidence
is durable before asynchronous dispatch, metrics and logs omit sensitive
identifiers/payloads, and overlay wake-up is an optimisation with cursor/replay
fallback. It is not a claim that the final Cloud Run/Neon topology can sustain
a particular rate.

L09 remains conditional/open for measured final-region capacity, deployed
private scrape and dashboards, actionable alert routing, end-to-end trace
collection, database/task/provider/SSE failure injection, backup/restore,
rollback and incident communication rehearsal. The six-hundred-design visual
generation backlog is intentionally outside this audit.
