# Legacy evidence register

**Status:** `Evidence inventory, not an active implementation authority`  
**Source repository:** `/Users/sukhdevsingh/Workspace/Personal /bharatstudio-alerts/repositories/bharatstudio-alerts` at `6679bf6`.

## L00 freeze candidate — 2026-08-14

This is a read-only freeze candidate. The owner must confirm it before L01 begins. No Git tag, production archive, database action or implementation copy was performed.

| Field | Recorded evidence |
|---|---|
| Commit | `6679bf6bd8348b87ef76cb59877f285130abb648` |
| Branch | `master` |
| Working tree | Clean at inspection time; branch is ahead of `origin/master` by 12 commits |
| Tracked files | 582 |
| Top-level inventories | `apps` 286; `packages` 138; `requirements` 24; `tasks` 15; `tests` 17; `technical_audit` 22; `deployment` 8; `archive` 25; root 36 |
| Excluded/generated paths observed | `node_modules/`, `.turbo/`, `.env.local` (ignored), local/build output and archived material; none are migration inputs |
| Secret scan | No secret values were printed or copied. Filename scan found expected secret-handling utilities and `.env.example`. `archive/2026-08-13-superseded-by-master-release-authority/TASKS.md` is retained as legacy archive evidence, and `pnpm-lock.yaml` remains with the reproducible legacy snapshot; both are explicitly excluded from migration and must not be copied. |
| Migration disposition | Existing source-map table below remains authoritative for selective reuse; no wholesale copy is approved. |

| Legacy area | Current treatment | Reuse condition |
|---|---|---|
| `apps/web` dashboard/tip/overlay/onboarding UI | Selective source/reference | Must match v1 scope and call final API contracts; no direct DB route handlers. |
| `apps/api` creator/config/security routes | Selective source/reference | Re-author under final TS Creator API boundary and test against contracts. |
| Razorpay/tips/webhooks/refunds | Characterization source | Must be rebuilt in Go and pass provider sandbox, idempotency, reversal and recovery tests. |
| Alert worker/queue/overlay/TTS | Characterization source | Must be rebuilt as Cloud Tasks Go dispatch without weakening no-drop semantics. |
| database schema/migrations/RLS scripts | Historical evidence | New clean v1 baseline required; no historical chain is copied as the new production baseline. |
| API, web, worker, DB tests and load harnesses | Reusable test evidence | Sanitize fixtures, port relevant behaviour tests and repeat in staging. |
| deployment/runbook/observability docs | Evidence and checklist input | Reconcile against final topology, region, providers and service roles. |
| requirements/tasks/reviews | Source map only | Extract only narrowly approved, still-pending sections into `pending/launch/`. |
| alert-library repository | Deferred external asset | Do not move or integrate until catalogue quality/licensing/entitlement approval. |
| YouTube code, requirements, tasks, migrations | Phase 2 source | No v1 copy, scope, OAuth permission, UI or runtime. |
| Enterprise code, requirements, tasks, migrations | Phase 2 source | No v1 copy, UI, role, pricing, allocation or payment behaviour. |
