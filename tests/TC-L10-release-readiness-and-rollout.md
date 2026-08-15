# L10 acceptance and test record — release readiness and production rollout

**Status:** `Blocked — local evidence exists, but L00–L09, provider, staging, store, legal and independent-review gates are not satisfied`
**Task:** [`../tasks/L10-release-readiness-and-rollout.md`](../tasks/L10-release-readiness-and-rollout.md)
**Master authority:** [`../active/launch/01_MASTER_RELEASE_AUTHORITY.md`](../active/launch/01_MASTER_RELEASE_AUTHORITY.md)

| ID | Setup/action | Expected result | Evidence |
|---|---|---|---|
| L10-01 | Reconcile every task, test, decision and review record against the master release authority | Each item has an accurate lifecycle state, owner, approver, evidence link and no stale readiness claim | Dated release register; not run |
| L10-02 | Verify Razorpay Technology Partner/connected-account approval and run creator-direct provider sandbox flows | Order, webhook, refund, reconciliation and account attribution evidence pass with one acknowledged webhook writer | Provider evidence register; not run |
| L10-03 | Deploy the final topology in staging with pinned region, DB plan, Cloud Run/Tasks/Scheduler values, IAM, domains, WAF, backups and secret rotation | Configuration is reproducible, least-privilege and capacity targets are declared before load testing | Infrastructure deployment record; not run |
| L10-04 | Run iOS/Android store review and Windows/macOS signing/notarisation/distribution checks | Companion clients meet platform policy and release artifacts are reproducible | Store and native release evidence; not run |
| L10-05 | Execute production-like rehearsal: deploy, migrate, tip, webhook, queue, overlay, Companion pairing, failure, rollback and communication | No accepted payment/alert evidence is lost or duplicated; rollback and incident communications work | Rehearsal transcript and reconciliation output; not run |
| L10-06 | Obtain independent security, payment, privacy/legal, accessibility, mobile/desktop, SRE and product review | No unowned critical/high issue remains; conditional findings are explicitly accepted or block release | Signed review register; not run |
| L10-07 | Run limited-cohort go/no-go with capacity guardrails and rollback triggers | Incident commander, freeze window, support/on-call, public status and rollback owners are active before exposure | Go/no-go record; not run |

## Non-negotiable release rule

No document-only assertion, local unit test, or legacy load result can substitute for final staging/provider/store/legal evidence. Until all required rows pass, the product remains unreleased.

## Current disposition — 2026-08-15

The local API/web, PostgreSQL, Go payment, Go worker, scheduler-template and
contract-fixture checks are supporting evidence only. L10 has not been run as a
release rehearsal. The product remains unreleased until every row above has
dated evidence and an owner/approver disposition.

## Local reconciliation update — 2026-08-15

The local portion of L10-01 was rechecked without changing the release scope:

- Active L00–L10 task records retain explicit lifecycle states; no local record
  was promoted to `Verified` from document inspection alone.
- The current contract validator passes 11 fixture mappings, the v1 template
  catalogue contract and 32 OpenAPI paths with local references resolved.
- The Cloud Tasks OIDC contract now carries the worker's explicit canonical
  audience from configuration; it is not derived from the private target URL.
  Worker Go tests/race tests and the infrastructure contract suite pass.
- The 359 missing BSA runtime packages remain intentionally deferred under
  `pending/launch/PENDING-04-TEMPLATE-RUNTIME-PACKAGE-COMPLETION.md`; no new
  visual design package was generated in this pass.

The latest local regression also includes the L04 subscription projection
scenario (`L04-48`), which passed the disposable PostgreSQL harness, plus
Companion mobile Jest 23/23, dependency-hardening 2/2, macOS Swift 7/7 tests and
marketing tests 5/5. Infrastructure and scheduler contract tests are 8/8 and
2/2 respectively. These remain supporting evidence only; no provider,
deployment, store, legal, staging or independent-review gate is closed.

The latest clean macOS rebuild passes 7/7 Companion tests, including the native
policy and REST contract-decoding checks. This verifies only local
lease/command/redaction/response-shape guardrails; it does
not close native pairing, Keychain, OBS, Windows, signing or distribution
requirements.

This closes only the local reconciliation slice of L10-01. Provider approval,
deployed infrastructure/IAM, staging capacity and failure proof, companion
store/signing, legal/support review and independent release review remain
open and continue to block L10.

### Fresh local reconciliation evidence — 2026-08-15

The master authority and L10 evidence snapshot were checked against the L00–L09
task/test/review records and the current active repositories. No stale active
`READY FOR LAUNCH` or equivalent production-readiness claim was found. The
local contract/regression evidence remains supporting evidence only; no L10
release row was promoted to `Verified`.

The remaining blockers are unchanged: provider approval and creator-direct
sandbox/live proof; deployed region/plan/IAM/secrets/domains/backup/rollback;
staging capacity and failure proof; native build/sign/store evidence; dated
legal/privacy/support evidence; operational monitoring; the deferred but
approved 600-design runtime catalogue; and independent release review.

### Automatic continuation reconciliation — 2026-08-15

The local readiness controls were rerun without promoting any release row:
worker Go unit/race/vet passed; cron and infrastructure contracts passed 2/2
and 8/8; mobile passed Jest 23/23, lint/typecheck and dependency-hardening
2/2; macOS passed 7/7; marketing passed 5/5; and `pnpm db:test:l03` passed the
disposable L02–L05 database/overlay chain. No BSA visual package was generated
or modified.

These are supporting local checks only. Provider, deployment/IAM, staging
capacity/failure, native/store, legal/support, observability and independent
review gates remain not run and continue to block release.
