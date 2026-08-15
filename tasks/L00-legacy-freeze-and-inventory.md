# L00 — Legacy freeze and inventory

**Status:** `Pending owner freeze confirmation — read-only inventory and source map captured`  
**Level:** L3  
**Owner:** Project owner / architecture  
**Depends on:** Launch scope authority  
**Blocks:** all implementation migration
**Test record:** [`../tests/TC-L00-legacy-freeze-and-inventory.md`](../tests/TC-L00-legacy-freeze-and-inventory.md)

## Objective

Make the legacy Alerts repository a reproducible evidence source before any selective copy or rewrite begins.

## Scope

- Record source commit, branch, working-tree state, tracked-file inventory and dependency/build exclusions.
- Run secret scanning and inventory credential-bearing paths without printing secret values.
- Record test commands, current pass/fail result, database/provider assumptions and untracked generated folders.
- Add a source-map entry for every future copy/rewrite candidate.

## Tasks

1. Create a read-only Git tag or immutable archive reference for legacy commit `6679bf6` after confirming the owner wants the tag.
2. Capture `git status`, tracked file counts, package manifests, migrations, test entry points and deployment files.
3. Classify every legacy top-level item as `migrate`, `rewrite`, `reference`, `phase-2`, `archive`, or `exclude`.
4. Scan for keys, `.env` files, `keys/`, private tokens/URLs and generated output; create a redacted remediation record if found.
5. Record exact legacy file/heading links in the central evidence register; do not copy implementation during this task.

## Current evidence — 2026-08-15

- Read-only freeze/inventory record: [`../done/LEGACY_FREEZE_INVENTORY_2026-08-15.md`](../done/LEGACY_FREEZE_INVENTORY_2026-08-15.md).
- The recorded source commit is `6679bf6bd8348b87ef76cb59877f285130abb648` on `master`; the source working tree was clean.
- The source map preserves the selective migration/rewrite/phase-2/archive/exclude decisions in [`../migration/00_MIGRATION_AND_LAUNCH_PLAN.md`](../migration/00_MIGRATION_AND_LAUNCH_PLAN.md).
- No legacy implementation was copied as part of this evidence capture.

The remaining closure action is owner confirmation of the immutable freeze reference and source-map review. A new Git tag/archive is not created automatically.

## Acceptance criteria

- The legacy commit and source-map are reproducible.
- No secret is copied into the new workspace or task output.
- Every later task can name its exact legacy source and disposition.
- Owner confirms the freeze record before L01 begins.

## Rollback

No runtime change. Remove only newly-created inventory documents if the owner rejects them; never modify legacy history.
