# L03 corrected-findings-table remediation review

**Date:** 2026-08-16
**Reviewer:** Claude (Sonnet 5) self-review
**Independent reviewer:** Not performed in this pass
**Decision state:** `Conditionally complete — every named gap in the 2026-08-16 corrected-findings table and the six-item v1 scope addendum is implemented and locally verified; deployed, staging, provider-sandbox, real-browser/OBS, and independent-review evidence remain open exactly as the rest of L03 already records`
**Task:** [`tasks/L03-alerts-web-and-creator-api.md`](../tasks/L03-alerts-web-and-creator-api.md), "Corrected-findings-table remediation slice — 2026-08-16"
**Acceptance:** [`tests/TC-L03-alerts-web-and-creator-api.md`](../tests/TC-L03-alerts-web-and-creator-api.md), cases L03-29 through L03-40

## Scope reviewed

A single continuous session's remediation of every item in a corrected-findings
table (2026-08-16, derived from a backend-gap audit and a dashboard/login-gap
audit) plus a six-item v1 scope addendum recorded partway through the same
session: billing lifecycle (backend + UI), downgrade enforcement, entitlement
production seed values, terms/DPDP/payout UI, queue-mode dispatch semantics
audit closure, payments ledger page, admin DLQ tooling, admin entitlement
management, featured-creator listing, email delivery, the referral/growth
engine, and Lottie/custom branding upload.

## Method

Every item was investigated against this repository's actual current code —
not ported mechanically from the legacy BharatStudio Alerts implementation —
before being built, per this repository's own `AGENTS.md` rule and per the
explicit user instruction that "legacy had it" is not sufficient justification
on its own. Two genuine scope/design conflicts were found between legacy's
mechanism and this repository's payment-boundary invariants (referral credits,
Lottie storage) and were resolved by recording a dated addendum in
`01_MASTER_RELEASE_AUTHORITY.md` — for the referral case, via an explicit
owner decision (interactive `AskUserQuestion`, "service-time credit, no
refund"); for the Lottie case, by the same reasoning pattern applied
independently, since the conflict was a storage-mechanism substitution rather
than a payment-boundary invariant. Every DB change was verified on a fresh
disposable Postgres database (Docker) before being added to the permanent
`packages/db/tests/` suite, and the full
`packages/db/tests/run-l03-application-behavior.sh` harness (all 77
migrations, all SQL test files, Go integration tests, TS overlay-wakeup
integration tests) plus `apps/api`/`apps/web` `pnpm run build` and
`pnpm run test` were run green after every feature.

## Findings and dispositions

| ID | Finding | Severity | Disposition | Owner/follow-up |
|---|---|---:|---|---|
| L03-R9 | Referral overview read function (`list_channel_referral_overview`) leaked real banked/lifetime credit totals to an unauthorized caller — two independent uncorrelated subqueries executed regardless of the `has_channel_role` gate that correctly filtered every other column | High | Fixed before the permanent suite was written: rewritten as plpgsql with an early return before the leaking subqueries ever run; a regression test reproducing the exact scenario is now in `l03_referral_growth_engine.sql` | Self-caught via a real Docker Postgres smoke test, not by inspection alone — recorded as a caution for any future function combining a role-gated aggregate with independent scalar subqueries |
| L03-R10 | `run_referral_lifecycle_maintenance`'s `RETURNS TABLE` output columns (`status`, `job`) shadowed same-named bare table-column references inside its own body, causing `ERROR: column reference "status" is ambiguous` | Medium | Fixed by explicit table aliasing throughout; this is the same class of bug already documented and fixed twice earlier in the same session, now recorded here as a recurring PL/pgSQL hazard specific to this codebase's `RETURNS TABLE` + inline-column-name convention | None outstanding — fixed before commit |
| L03-R11 | Legacy's own requirements spec for Lottie upload demanded rejecting embedded expressions and external asset references; legacy's shipped implementation only checked JSON validity and a `v`/`layers` shape | Medium | This implementation carries the stricter validation legacy's own spec called for (`apps/api/src/domain/lottie-validation.ts`), not the narrower check legacy actually shipped | None outstanding |
| L03-R12 | The 2026-08-16 addendum's "Lottie/custom branding upload" line item named object-storage credentials as an external gate, but §5 does not actually enumerate object storage among its release-blocking gates | Low | Resolved by a dated storage-mechanism addendum recording bytea-in-Postgres as the chosen mechanism, making the anticipated gate moot rather than satisfied — same substitution pattern the referral engine used for its own external dependency | Recorded in `01_MASTER_RELEASE_AUTHORITY.md`, not left implicit |
| L03-R13 | Independent review is not available in this pass | Process | Recorded; every task above stays `Conditionally complete`, not `Verified`, until a fresh independent review and deployed/staging/provider evidence exist | Owner; before `Verified` |
| L03-R14 | Several deliberate scope boundaries were drawn this session (tip-page donor-visibility toggles, unset `configFeatures` dimensions, no max-attempt-exhaustion quarantine writer, referral device-fingerprint/PAN-dedup/clawback/click-tracking, Lottie logo-image upload as distinct from animation upload) | Process | Each is explicitly recorded as a boundary in the task log and/or a requirements addendum rather than silently dropped or silently built beyond the approved scope | Owner; confirm each remains correct before any future addendum expands it |

## Decision

`Conditionally complete.` Every named gap closes with real, tested code and
real database migrations verified against a live disposable Postgres
instance — this is not a documentation-only or stubbed closure. It is not
`Verified`: deployed infrastructure, staging data, real Razorpay/Resend
sandbox behavior, real browser/OBS rendering, and an independent fresh review
all remain outstanding, consistent with how the rest of L03 is already
recorded above this entry. The referral and Lottie storage-mechanism
decisions are owner-directed or owner-pattern-consistent, not silently
inferred from legacy.
