# TC-CTL-04 — capability-admin UI acceptance plan

**Task:** `../active/tasks/CTL-04.md`  
**Status:** `Defined — implementation approved; execution evidence pending`

| ID | Required proof |
|---|---|
| CTL04.1 | MFA-satisfied platform admin reaches the capability list and sees server state, not fabricated defaults. |
| CTL04.2 | Non-admin, expired session, missing MFA assurance and unavailable upstream all deny or disable mutations without leaking capability, channel, payment or user data. |
| CTL04.3 | Master switch, retier and limits edits submit only through existing proposal/approval routes with a reason; Layer 1 correctness dimensions and prices have no editable path. |
| CTL04.4 | Emergency kill presents CTL-05 server-derived aggregate impact, requires explicit reason/confirmation, and cannot submit caller-supplied counts. |
| CTL04.5 | Revert, proposal state and immutable audit/event history are visible with pagination/error/retry behavior. |
| CTL04.6 | Browser tests cover keyboard navigation, form labels/errors, narrow desktop/mobile layout, loading/degraded state and no optimistic success before API confirmation. |
| CTL04.7 | Contract fixture, admin build/typecheck/lint/unit/browser suites and relevant Alerts API contract/integration tests pass. |

## Evidence protocol

Run against synthetic seeded admin/capability data only. Record exact redacted commands, test counts, revisions, screenshots or browser artifacts where generated, API/SQL role proofs and any external MFA/staging gap after implementation. A local browser test is not MFA-provider or production proof.
