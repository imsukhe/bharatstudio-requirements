# TC-CTL-04 — capability-admin UI acceptance plan

**Task:** `../active/tasks/CTL-04.md`  
**Status:** `Conditionally satisfied locally except CTL04.4 — CTL-05 dependency remains open`

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

## 2026-09-18 scoped execution note

The initial local console proof covers CTL04.1, CTL04.2, CTL04.3 and CTL04.5–7 for the
registry/change-history portion. It must assert that the emergency card is disabled and that no
browser route exists which can forward `affectedChannelCount` or `liveChannelCount`. CTL04.4
remains blocked—not waived—until CTL-05 supplies an authoritative preview and atomic fire
endpoint. The final acceptance run must replace that negative assertion with the real preview,
reason/confirmation and stale-preview test.

## 2026-09-18 execution result

`CTL04.1`, `.2`, `.3`, `.5`, `.6` and `.7` have local evidence in the linked task/review record.
The deterministic console browser proof uses synthetic data only; it exercises authenticated local
bootstrap, the existing passkey-protected page boundary, keyboard and narrow-device interactions,
upstream-safe/degraded UI behavior, proposal-only mutation, and a missing request-marker denial.
The Alerts focused API proof separately verifies platform-admin/MFA gates, fail-closed stores,
schema rejection, maker-checker/revert behavior and immutable kill-event behavior. No provider,
real WebAuthn device, staging, deployed migration, external security review or production evidence
is claimed. `CTL04.4` remains blocked exactly as described above.
