# Build bootstrap authority — the two steps that precede the build plan

**Status:** `Proposed — requires owner approval before any lane starts`
**Owner:** Project owner
**Date:** 2026-09-14
**Scope:** The governance work that must exist before `FULL-PRODUCT-DEFINITION.md` §34
becomes a schedulable plan
**Companions:** [`00_LAUNCH_SCOPE_AUTHORITY.md`](./00_LAUNCH_SCOPE_AUTHORITY.md) ·
[`01_MASTER_RELEASE_AUTHORITY.md`](./01_MASTER_RELEASE_AUTHORITY.md) ·
[`05_SUPPORT_AND_EXTERNAL_EVIDENCE_REGISTER.md`](./05_SUPPORT_AND_EXTERNAL_EVIDENCE_REGISTER.md)

## Why this file exists

`FULL-PRODUCT-DEFINITION.md` §31.0 says no register row may be started without an
`active/` record carrying ten fields. §34 Step 0 is the work that *creates* those
records — so under the rule as written, the plan's own first step could never begin.
That is a genuine bootstrap deadlock and it is resolved here rather than by an
undocumented exception.

It also fixes a second circularity: §37 requires a production-shaped reference
environment for the Phase 0.5 exit evidence, while §32 lists deployment as blocked. The
distinction that resolves it is stated in §3 below.

## 1. Bootstrap exemption, narrowly drawn

**Two steps are exempt from the §31.0 ten-field precondition**, because they are the
steps that produce it:

| Step | Work |
|---|---|
| **Step −1** | Approve and link the external-evidence register (§2 below) |
| **Step 0** | Build the register-ID ↔ L-track mapping and write the `active/` records |

The exemption covers **those two steps only**. It is not a precedent, it does not extend
to any capability row, and each exempt step carries its own task record in
`active/tasks/` with the same ten fields — the difference is that the record is written
*as* the step, not before it.

**Nothing else may start until Step 0 closes.** That is the same rule §34 already states;
this file makes it enforceable by giving Step 0 an authority to be approved under.

## 2. Step −1 — the external-evidence register must become effective

`05_SUPPORT_AND_EXTERNAL_EVIDENCE_REGISTER.md` declares itself
`Proposed operational authority` and `Not effective until approved and linked from the
master release authority`. Until that happens it **does not govern**, which means every
plan that cites it as the home of external evidence is citing an authority that is not
yet in force.

Closing Step −1 requires, in order:

1. Owner approval of the register as written, or an amended version.
2. An explicit link and status line in `01_MASTER_RELEASE_AUTHORITY.md` adopting it.
3. A named owner per evidence row — the register lists role names today, not people.

Until all three are done, `FULL-PRODUCT-DEFINITION.md` §37.8's rule that external
evidence lives only in that register is a statement about a file with no force.

## 3. Step 0.25 — the environment, and the circularity it resolves

**A non-production environment is not blocked. Production deployment is.**

§32's "Deployment" row is about shipping to production: resolved `REQUIRED_*`
placeholders, IAM/OIDC, staging recovery, capacity, observability and a rehearsed
rollback. None of that is required to stand up a **production-shaped, non-production**
environment for measurement, and treating them as one item is what made the Phase 0.5
exit criteria unreachable.

The environment workstream is therefore its own scheduled lane, not a by-product of
Phase 0.5, and it must exist **before** Phase 0.5 can produce exit evidence:

| Deliverable | Detail |
|---|---|
| Cloud Run at the production configuration | Same concurrency cap, same instance settings, one region |
| A seeded database at the §37.4 size | 500 channels · 2,000,000 payments · 5,000,000 alert events · 200,000 supporter identities, production index definitions |
| Provider sandboxes | Razorpay test credentials wired end to end |
| The OBS harness | Pinned OBS version on a mid-range Windows machine, plus headless Chromium for CI trend-tracking |
| The device lab | One named mid-range Android and one iPhone at the supported floors |
| Network profiles | 4G and 3G shaping, per §37.4 |
| The pass/fail artefact pipeline | The JSON document §37.4 specifies, produced automatically per run |

**Owner:** unassigned — this is the first named gap this file exists to surface.
**Exit:** one full §37.5 target-concurrency run completes and emits a valid artefact,
before any Phase 0.5 row claims an exit number.

## 4. Freeze checkpoint — before anything irreversible

The owner decision of 2026-09-14 files external gates after the build works. That is an
accepted schedule risk, and it is only safe with a checkpoint, because provider, legal,
tax or store feedback can force redesign of things that are expensive to change late.

**Before any schema freeze, public copy freeze, or store submission**, the following are
reviewed against current assumptions and the review is recorded:

| Area | What late feedback could force |
|---|---|
| **Payment boundary** | Razorpay's answer on the creator-direct flow could change the settlement or account model — a schema-level change |
| **Deletion and retention** | The DPDP position could require a different archival shape, or genuine erasure, after data exists |
| **Mobile purchase boundary** | A store's reading of the no-purchase rule could require an in-app route, and the in-app deletion requirement (`CMP-78`) is already known to conflict with the deletion block |
| **Tax representation** | The CA's conclusion could change what pricing and receipts may say |
| **Terms and consent wording** | Counsel could change consent text that is already embedded in flows |

The checkpoint's output is a written go/no-go per area, with any reversibility risk that
is being accepted named explicitly. **A freeze without this review is not approved.**

## 5. What this file does not do

It approves nothing by itself. It records what must be approved, by whom, and in what
order, so that the first step of the build plan is startable under the same governance
as every step after it.
