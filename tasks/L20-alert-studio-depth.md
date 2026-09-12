# L20 — Alert Studio depth

**Status:** `Partial — import pipeline built (migration 0106) and locally test-proven; the real 600-template catalogue cannot be imported in its current form (raw HTML per design, forbidden at every tier); only 241 of 600 runtime packages verify at all; capability matrix and asset-quota enforcement from Tasks 1-2 not found in code; nothing here is proven in a deployed environment`
**Level:** L2
**Owner:** [OWNER — product/web, unassigned]
**Depends on:** L03 (existing preset/branding system, Lottie pipeline `0077`)
**Blocks:** none recorded
**Test record:** [`../tests/TC-L20-alert-studio-depth.md`](../tests/TC-L20-alert-studio-depth.md)

## Authority and evidence

Master plan Part 6, "L20 — Alert Studio depth" (lines ~1099–1146), including the per-tier capability table, asset-storage table, and the 2026-09-02 decision on the 600-template catalogue; Part 7 §7.4 (feature register).

## Objective

Extend the shipped preset/branding system to the full studio, using schema-validated templates only, and build the import pipeline for the existing 600-template catalogue.

## Tasks

1. Per-tier capability matrix from the master plan's table: alert library size, global/per-event/per-queue styling, position/resize/overlap-warning behavior, custom text and character ceiling (100/150/300/500 — the same `maxCharLimit` as §3.2, one value not two), custom templates (0/approved/5/12 per channel), animation presets, creator media/sound libraries (0/small/5/20).
2. Asset storage quotas by plan (Free none, Pro 100 MB, Creator 250 MB, Studio 1 GB, Enterprise contract), with type validation, malware scanning, sanitisation/transcoding, size/duration limits and a takedown/reporting path on every upload.
3. Template import pipeline: convert the existing 600-template catalogue into the schema-validated template format, run each through the same type-validation/scanning/sanitisation path the Lottie upload (`0077`) already uses, and expose them through the tiered alert library. Import incrementally, in batches; gate visibility by tier.

## Exact implementation boundary

In scope: the capability matrix, asset-quota enforcement and scanning pipeline (extending, not duplicating, the existing Lottie (`0077`) pipeline), and the import pipeline itself.

Out of scope, permanently: rebuilding or discarding the 600-template catalogue — it is imported, not recreated. Any template-catalogue content that cannot be expressed in the validated schema is not imported; it does not get a bespoke escape hatch.

## Non-negotiable implementation rules

- Arbitrary HTML/CSS/JS is **never** permitted at any tier, for any alert customization. This is explicit in the master plan's capability table ("Never / Never / Never / Never") and is not negotiable at any future tier addition.
- The character ceiling is one value shared with the existing `maxCharLimit` from §3.2 — implementations must not introduce a second, divergent limit.
- No second asset-scanning pipeline is built. The Lottie pipeline (`0077`) is extended for the template-import path; import is incremental and gated by tier from day one.

## Definition gate

Per `governance/AGENTS.md`, L2 work stops after definition pending explicit scope/acceptance/test-plan approval. Owner unassigned: [OWNER].

## Acceptance criteria

- Each tier's capability matrix values (library size, styling scope, character ceiling, custom-template count, media/sound-library size) are enforced server-side and proven by test at the boundary for at least one over-limit case per dimension.
- Asset upload is proven by test to reject an oversized file, a disallowed type, and a file failing malware scanning, for each plan's quota.
- A template imported from the 600-template catalogue that contains non-schema-expressible content (e.g., inline script) is proven by test to be rejected by the import pipeline, not silently stripped and admitted.
- No code path exists that renders arbitrary HTML/CSS/JS from a creator- or template-supplied string; a test/scan confirms this for the alert-rendering surface.
- The character ceiling used by Alert Studio and the `maxCharLimit` used elsewhere (§3.2 / TTS amount-tiering) are proven by test to read from the same single configured value.

## Evidence required for closure

Inline prose citation: exact file paths for the capability-matrix enforcement and asset-quota code; exact reference to the extended Lottie/`0077` pipeline location; import-pipeline test-suite pass count including the non-schema-expressible-content rejection case. No artifact/screenshot directory.

## Rollback

Capability-matrix and quota enforcement are additive checks over existing L03 alert-configuration code; disabling them reverts to today's shipped preset/branding behavior. Template import is incremental and batch-based — a batch can be withheld or reverted without affecting already-imported or previously-shipped built-in themes. No production migration without separate explicit approval.

## Batch 8 implementation slice — 2026-09-07 reconciliation

Verified by reading the code and `contracts/template-catalogue.json`. Corrects the map's "TODO — not started."

**Built and locally test-proven — Task 3 (import pipeline):**
- `packages/db/migrations/0106_v1_l20_template_catalogue_import.sql`: `alert_template_catalogue_entries` table, keyed on `external_key` (e.g. `BSA-001`) deliberately rather than a content hash, so a re-render of a design's artwork updates the existing catalogue row instead of forking a new one. `render_bytes` capped at 2,000,000 bytes, same cap as the Lottie (`0077`) branding upload it deliberately mirrors.
- Content-safety validation reuses, not duplicates, the existing Lottie validator: `apps/api/src/domain/template-import-validation.ts` wraps `apps/api/src/domain/lottie-validation.ts` because the accepted render-document format is the same Lottie-shaped JSON (`v` + `layers`).
- Import/read functions and `apps/api/src/routes/templates.ts`, `scripts/template-import/**` complete the pipeline.
- Test evidence: `apps/api/test/l20-template-import-validation.test.ts` (9 cases, including inline-script rejection), `apps/api/test/l20-templates-routes.test.ts`, `packages/db/tests/l20_template_catalogue_import.sql`.

**The finding that matters — the real 600-template catalogue cannot be imported as it exists today.** Verified directly in `contracts/template-catalogue.json`: `runtimePackageShape` is `visuals-v6/designs/BSA-{id}/{index.html,design.json,review.md}` — raw HTML per design. This task's own capability table forbids arbitrary HTML/CSS/JS at every tier ("Never / Never / Never / Never"), and the import validator correctly rejects that shape — this is the system working as designed, not a bug. Only `design.json` metadata (name, category, tier) is importable today; there is no way to render from it. Separately, `runtimePackagesVerified` is **241 of 600** — 359 packages don't even pass the catalogue's own integrity check, independent of the format problem. Recorded at master plan 3.16 with four owner options; none decided here. This does not block v1, which ships the four built-in themes; L20 was already post-launch scope.

**Not found in code — Tasks 1-2 (capability matrix, asset quotas):** no per-tier capability-matrix enforcement code (library size, styling scope, custom-template count 0/approved/5/12, creator media/sound library size) was found anywhere in `apps/api` or `apps/web`, beyond the single `maxCharLimit` value already shared with L03/L07's TTS work (`apps/api/src/domain/entitlement-policy.ts:6,33-35`) — which does satisfy this task's "one value, not two" non-negotiable rule for the character ceiling specifically. No asset-storage-quota table, malware-scan integration, or takedown/reporting path was found for Alert Studio media uploads (searched for `assetQuota`/`storageMb`/`mediaLibrary`/`storage_quota`, no hits outside the char-limit code). These remain unbuilt; do not record as done.

Evidence: `packages/db/migrations/0106_v1_l20_template_catalogue_import.sql`; `contracts/template-catalogue.json:10,77`; `apps/api/src/domain/template-import-validation.ts`; `apps/api/test/l20-template-import-validation.test.ts` (9 cases); `docs/BharatStudio-MASTER-PLAN.md` §3.16. Nothing here is proven in a deployed environment.
