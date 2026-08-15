# BharatStudio agent operating policy

This is the canonical policy for every BharatStudio repository. Each repository-root `AGENTS.md` points here and may add only repository-boundary rules.

## Start every task

1. Read this policy, the repository-root `AGENTS.md`, `CLAUDE.md`, current authority, relevant task, test, and decision record.
2. Inspect repository state before changing files.
3. Classify the request: L0 question/inspection; L1 docs/no behaviour; L2 product/UI/internal feature; L3 API/database/payment/auth/privacy/security/migration; L4 release/irreversible external change. Use the higher level when unclear.

## Required lifecycle

For L2–L4 work, before implementation create or update only the minimum artifact set:

- one authority/requirement;
- one executable task;
- one test/acceptance record;
- one review/decision record.

Do not create duplicate documents. Use the latest approved, owner-assigned authority. Archived/superseded material is evidence only. A material decision follows `Proposed → Approved → Implemented → Verified → Superseded`, or is `Blocked`/`Rejected`.

Interactive work must stop after definition and wait for explicit user approval before implementation. Approval must cover scope, acceptance criteria, affected files, data impact, test plan, and rollback. A changed user journey, audience, pricing, payment model, legal posture, data boundary, platform, timeline, or success measure is scope drift: pause, state the delta, request confirmation, and update the artifacts before proceeding.

## Review, evidence, and closure

L2–L4 requires self-review and an independent fresh review when available. Record reviewer, scope, finding, severity, evidence, disposition, owner, and follow-up/release gate. If independent review is unavailable, say so, self-review, and leave the task `Conditionally complete` or `Blocked`.

Do not claim completion without accepted criteria, relevant checks, review dispositions, rollback/recovery evidence where relevant, and explicit remaining work.

## Data, money, security, and privacy

- Never expose or commit secrets, tokens, private URLs, payment data, or personal data. Use synthetic data unless consented otherwise.
- Never migrate a shared/production database by default. Preserve migration history; do not delete, rewrite, or squash migrations without explicit approval.
- Payment, tax, TDS, GST, KYC/AML, privacy, app-store, provider-policy and legal conclusions require dated primary evidence or written professional/provider advice. Do not approve them from memory.
- Specify purpose, minimisation, retention, access control, erasure/deactivation policy, and auditability for personal data.
- Treat payment events and financial evidence as append-only; correct them with linked compensating records.

## Archive policy

When work is superseded, move it to `archive/<YYYY-MM-DD>-<reason>/`, add a note naming its replacement and reason, and update links/indexes. Never delete automatically.
