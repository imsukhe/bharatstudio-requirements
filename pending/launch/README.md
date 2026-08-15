# Pending v1 requirement slices

**Status:** `Index only — no legacy FRD text has been copied yet.`

Only the following narrowly-scoped legacy sections are candidates for extraction. An extraction is permitted only after it is confirmed still agreed, genuinely incomplete, and relevant to v1. The extraction must retain its legacy source path, heading, decision status, owner, dependencies, and acceptance evidence.

| Pending slice | Legacy source | Why it remains active |
|---|---|---|
| Alert queue no-drop, delivery/replay and display semantics | `requirements/11_ALERT_CONFIG_QUEUE_EVENT_DURABILITY.md`; `tasks/alerts/P11-alert-config-queue-completion-plan.md` | Core v1 safety contract; code exists but Cloud Tasks rewrite and end-to-end proof remain open. |
| Razorpay creator-direct payment, webhook recovery, refund/reconciliation | `requirements/20_RAZORPAY_PAYMENT_RECONCILIATION_AND_REFUND_RECOVERY.md`; payment routes/tests | v1 money path; Go migration, provider evidence, and recovery proof remain open. |
| RLS/least privilege and archive-integrity proof | `requirements/FRD-029-rls-phase1.md`; `RLS_ROW_LEVEL_SECURITY.md`; `DELETION_POLICY.md` | Launch blocking residual tests remain open. |
| Pricing, entitlements, grandfathering and customer-facing copy | `requirements/17_TIERED_CREATOR_EXPERIENCE_AND_PUBLIC_TIPPING_SURFACES.md`; master authority §1.4 | v1 price/limit behaviour must be reconciled and tested. |
| Alerts overlay, browser-source security and reconnect/resync | `requirements/08_OBS_WEBSOCKET_INTEGRATION.md`; queue FRD; overlay source/tests | Browser source is v1; remote OBS control is constrained to the Companion helper. |
| Cross-cutting migration blockers: pooler-safe SSE fan-out/cache invalidation, Razorpay webhook event identity, and D-2 multi-queue source routing | `pending/launch/PENDING-03-MIGRATION-CROSS-CUTTING-GAPS.md`; migration plan; L01/L04/L05/L09 | New v1 requirements slice. These are unfinished implementation/proof items, not a reason to copy entire legacy FRDs. |
| Companion v1 mobile/web/helper boundary | `requirements/18_BHARATSTUDIO_COMPANION_APP.md` v1 sections; `tasks/companion/P18-...` Phase 1 only | Required v1 surfaces; later YouTube, Enterprise, workflow and AI portions are excluded. |
| Marketing, support, legal and operations launch requirements | active sections of marketing/legal/support/operations FRDs and task plans | Required public release surfaces and launch gates; no old copy is authoritative without fresh review. |

## Extraction template

Every extracted file must include:

```text
Legacy source: <absolute legacy path + heading>
Decision status: Proposed | Approved | Implemented | Verified | Superseded
Why active: <specific unfinished acceptance criterion>
v1 scope / non-goals
Acceptance evidence
Owner and review gate
```

Anything not listed above belongs in `done/`, `phase-2/`, or legacy archive—not this folder.
