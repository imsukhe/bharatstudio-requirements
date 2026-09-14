# L22 curated sticker catalogue review

**Decision state:** `Implemented local curated-catalogue slice; creator-pack and L20 moderation requirements remain open`
**Level:** L2
**Owner:** Project owner / Alerts API, database, web

## Boundary

`0110_v1_l22_sticker_catalogue.sql` supplies only BharatStudio-approved
catalogue entries and a creator's enable/disable choice for those entries. A
viewer supplies an opaque catalogue id, never bytes or a media URL. Structural
validation reuses `template-import-validation.ts`/`lottie-validation.ts`; it
does not introduce an asset upload path or second scanner.

## Open requirements

Creator-uploaded packs, tier size quotas, scan-plus-attest, Studio review,
asset takedown, and L20 operational scanning are absent. They cannot be
represented as fulfilled by a catalogue-only implementation. The work is
additive; disabling selection routes has no payment or alert-history rollback.

## QA decision update — 2026-09-14

**State:** `Approved for local QA remediation by active goal; verification pending`

The later L22c staff-review implementation was audited independently of the
catalogue boundary above. A stable transaction timestamp plus random audit UUID
does not provide a chronological order. The approved correction is additive:
`0125` introduces a monotonic audit order and uses it only for staff audit
listing. It preserves all audit decision data and authorization checks. The
review does not change the separate open operational malware-scan, staging, or
independent trust-and-safety gates.

**Local verification:** migration `0125` and the deterministic same-transaction review proof passed as part of the 2026-09-14 `pnpm verify:local` exit-0 run (125 migrations; 52 isolated SQL proofs). This is self-reviewed local evidence only; the open operational gates remain open.
