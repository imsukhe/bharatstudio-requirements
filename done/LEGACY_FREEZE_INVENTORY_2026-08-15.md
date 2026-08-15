# Legacy Alerts freeze and inventory evidence

**Date:** 2026-08-15
**Source:** `/Users/sukhdevsingh/Workspace/Personal /bharatstudio-alerts/repositories/bharatstudio-alerts`
**Task:** [`../tasks/L00-legacy-freeze-and-inventory.md`](../tasks/L00-legacy-freeze-and-inventory.md)
**Evidence type:** Read-only inventory; no legacy files were modified and no credential values were printed.

## Reproducible source reference

| Item | Observed value |
|---|---|
| Commit | `6679bf6bd8348b87ef76cb59877f285130abb648` |
| Branch | `master` |
| Working tree | Clean; zero `git status --short` entries |
| Tracked files | 582 |
| Top-level entries | 49 |
| Package/lock manifests | 9 |
| Migration-path files | 89 |
| Test/spec-path files | 54 |
| Deployment-related files | 15 |
| Tracked secret-like paths | `.env.example` only; no secret value was inspected or copied |
| Untracked generated paths | None in the source working tree |

The source commit is already recorded by the migration plan. Creating a new tag or immutable archive remains an owner decision; this evidence does not create one.

## Top-level disposition

| Source area | Disposition | Authoritative destination or reason |
|---|---|---|
| `apps/web` | Selective migration/rewrite | `bharatstudio-alerts/apps/web` for approved Alerts surfaces; parent marketing routes go to `bharatstudio-marketing` after content/security review |
| `apps/api` | Selective rewrite | `bharatstudio-alerts/apps/api` for Creator API; provider money boundary is rebuilt in `services/payment-webhook-go` |
| `packages/db` | Reference and clean re-authoring | `bharatstudio-alerts/packages/db`; historical migrations remain evidence and are not a new baseline |
| `packages/queue`, dispatch workers | Rewrite | `services/alert-worker-go`; Cloud Tasks and durable replay are authoritative |
| `workers/youtube-polling` and YouTube routes | Phase 2 | `phase-2/youtube`; no v1 scopes, routes or data |
| Enterprise/workspace UI and funds movement | Phase 2 | `phase-2/enterprise`; no v1 Enterprise money movement |
| `deployment`, `docker`, `cloudbuild*` | Reference/rewrite | `bharatstudio-infra` and service-local deployment descriptors after topology approval |
| `tests`, fixtures and technical audits | Selective evidence migration | `bharatstudio-requirements/done/`, `contracts/fixtures/`, and task-specific test records after sanitisation |
| `requirements`, `reviews`, `tasks` | Evidence only | Central requirements authority; no old decision becomes active without explicit supersession/review |
| `archive` | Archive/reference | Retain as historical evidence; never use as active implementation authority |
| `.env.example` | Reference only | No values copied; recreate environment contract with secret names and fail-closed rules |
| `node_modules`, `.next`, `dist`, build/cache output | Exclude | Generated artifacts are not migration inputs |

The detailed service-level disposition and no-copy rules remain in [`../migration/00_MIGRATION_AND_LAUNCH_PLAN.md`](../migration/00_MIGRATION_AND_LAUNCH_PLAN.md). This table intentionally does not promote legacy implementation into the active v1 scope.

## Secret and generated-output scan

- Tracked filename scan found only `.env.example`; no `.env`, key, PEM, P12, credentials or secrets directory was found in tracked paths.
- No values from `.env.example` were copied into the new workspace or this record.
- The source working tree had no untracked generated output at the time of capture.
- The new workspace must continue to reject `.env*` values, private overlay URLs, local keys, dependency directories and build output from migration.

## Closure state

Completed locally: source reference capture, clean-status capture, inventory counts, redacted path scan and disposition map.

Still open by rule: owner confirmation of the freeze reference/tag/archive and owner review of this source map. L00 therefore remains `Pending owner freeze confirmation`; no document-only inventory is treated as L00 closure.
