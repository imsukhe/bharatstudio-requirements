# Support and external-evidence register — Alerts v1

**Status:** `Proposed operational authority; not a legal approval and not a release approval`
**Owner:** Project owner; Support, Payments, Security, Product and Legal/CA reviewers
**Scope:** BharatStudio Alerts and bundled Companion v1 only
**Effective date:** Not effective until approved and linked from the master release authority

This is the single working register for launch support operations and external
reviews. It records what must be proven; it does not turn an unreviewed tax,
privacy, payment-provider, app-store or legal assumption into product policy.

## 1. Public support boundary

The public site may expose only the approved support contacts and safe guidance:

| Category | Public entry | Required intake | Do not request |
|---|---|---|---|
| Account/access | `support@bharatstudio.in` | account email, approximate time, safe reference, device/app version | Google password, OAuth token, overlay token |
| Payment/receipt | `support@bharatstudio.in` | public receipt/reference, creator handle, amount/date if needed | card/UPI credentials, Razorpay secret, full webhook body |
| Refund concern | `support@bharatstudio.in` | local receipt/reference, reason, requested amount, creator/payment context | payment credentials or provider dashboard secrets |
| Privacy/data concern | `privacy@bharatstudio.in` | request type, account/contact needed to locate the record, minimum supporting evidence | unnecessary identity documents or unrelated account data |
| Security incident | `support@bharatstudio.in` | minimal description, time, affected surface, safe contact | exploit payloads containing secrets or live credentials |
| Service/alert incident | `support@bharatstudio.in` | channel/overlay reference, approximate time, visible symptom, browser/helper version | raw logs, tokens or private OBS credentials |

Support must use a case ID, not an email body or payment ID, as the primary
operational reference. Case records are access-controlled, audited, retained
under the approved retention schedule and never used as a substitute for the
financial ledger or alert outbox.

## 2. Triage and escalation contract

These are internal operating targets for staging rehearsal. They must not be
published as contractual SLAs until the owner approves staffing, hours and
support tooling.

| Priority | Examples | Internal first acknowledgement target | Escalation |
|---|---|---:|---|
| P0 | suspected payment integrity issue, security incident, broad alert loss risk, production outage | 1 hour during staffed coverage; immediate page for active payment/security risk | Payments/Security/SRE owner immediately; preserve evidence and disable affected path if required |
| P1 | creator cannot receive tips, repeated overlay failure, refund/reconciliation exception | 4 staffed hours | Owning engineering/service owner same business day |
| P2 | setup issue, configuration problem, Companion/helper issue without payment impact | 1 business day | Support lead, then product owner |
| P3 | documentation, feature request, cosmetic issue | 2 business days | Support/product backlog |

No tier, queue limit, Companion limit or support delay may delete, suppress,
acknowledge or rewrite an accepted payment/alert record. P0/P1 cases require a
trace/case link to the owning durable record and an operator audit entry.

## 3. Standard incident flow

1. Create a case with a random case ID and classify the category/priority.
2. Redact secrets and unnecessary personal/payment data before storing notes.
3. Check service readiness, provider status, durable payment/outbox state and
   existing incidents through approved operator surfaces.
4. For payment concerns, never treat a browser callback or support assertion as
   capture/refund truth; use the payment ledger and provider evidence.
5. For alert concerns, inspect delivery/outbox/cursor state. Recovery is replay,
   retry or queue pause according to the worker runbook; it is never deletion.
6. Escalate using the owner table and record the decision, evidence and action.
7. Close only after the customer-facing result, durable state and audit entry
   agree. Link any compensating financial record rather than editing history.

## 4. External evidence register

| Evidence area | Required decision/evidence | Owner | Status before public launch |
|---|---|---|---|
| Razorpay Technology Partner / connected-account capability | Written provider approval and enabled test/live account capability for the exact creator-direct flow | Payments + provider | Open; no live routing claim |
| Razorpay webhook/order/refund behavior | Dated sandbox evidence for signature, event ID, order status, refund, retry and connected-account attribution | Payments | Local contract pass; provider staging open |
| Tax/GST/TDS/payment classification | Written CA/tax counsel conclusion for the actual money flow, settlement and records | Owner + CA | Open; do not infer from code |
| Privacy/DPDP and retention | Approved policy, purpose/access/retention/deactivation wording and rights-handling process | Privacy/legal owner | Open; public index is not final policy |
| Terms/acceptable use/refunds | Dated approved terms, refund rules, creator responsibilities and historical-version handling | Legal/product | Open |
| App-store compliance | Apple/Google declarations, permissions, account and payment-boundary review for Companion | Mobile owner + legal | Open; store review not run |
| Public domain/SSL/email | Domain ownership, HTTPS, support/privacy mailbox, DNS and rollback evidence | Infra/support | Open |
| Support operations | Staffed coverage, case system, escalation owners, redaction, incident drill and response targets | Support owner | Internal targets proposed; rehearsal open |
| Analytics/SEO consent | Privacy-safe analytics configuration, consent behavior and public crawl/security scan | Marketing/privacy | Local static checks pass; deployment scan open |

An item may move from `Open` only when the dated evidence, reviewer, scope,
finding, disposition and follow-up are attached. Legal/provider rows require
primary provider evidence or written professional advice; self-review is not a
substitute.

## 5. Release gate

Public launch is blocked until:

- payment/provider and tax/legal rows are approved for the implemented flow;
- privacy, terms, refund and deactivation wording is published with effective
  dates and historical versions retained;
- support owners, coverage, case/audit tooling and incident rehearsal pass;
- public-host/domain/SSL and privacy-safe analytics evidence pass;
- the master release authority records each row's reviewer and disposition.

Until then, the marketing site must describe this surface as a support and
policy index, not as proof that the underlying approval exists.

