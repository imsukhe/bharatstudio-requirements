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
