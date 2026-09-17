# PRF-02 slice 7 — Sponsor Card (§6 #11): implementation record

**Date:** 2026-09-17
**Owner:** **Sukhdev Singh**
**Authority:** `../FULL-PRODUCT-DEFINITION.md` §6 module #11, §9.1.1, §12.6, §12.7, §19.1, §30.3, §34
**Binding decision:** `2026-09-17-remaining-eight-modules-and-youtube-v1-amendment.md` Part 1 §3
**Task:** `../active/tasks/PRF-02-slice-7-sponsor-card.md`
**Acceptance:** `../tests/TC-PRF-02-slice-7-sponsor-card.md`

---

## What this slice is

The Sponsor Card renders a sponsor name and, optionally, a logo, on a creator-set schedule, and
counts nothing. §6's original row ("scheduled placement with an exposure event log") is
superseded: the exposure log is dropped outright, and an internal-only, not-billable counter was
considered and declined — any number rendered eventually gets screenshotted into a sponsorship
negotiation, and a label saying it is not auditable protects nobody. This dissolves both
definitions the module was blocked on (what counts as an exposure; who may rely on the log)
because nothing is counted.

## Reuse anchors, named as the task requires

| Value / shape | Reused from |
|---|---|
| Sponsor name bound, 1–120 characters | `packages/db/migrations/0109_v1_l17_paid_challenges.sql:67`, `check (char_length(title) between 1 and 120)` — the same bound `0135` already reused for `objective` |
| sha256 hex format, `^[0-9a-f]{64}$` | `packages/db/migrations/0110_v1_l22_sticker_catalogue.sql`, `content_sha256` column check |
| Tenant-scoped content-addressed key shape (`channel_id` + sha256) | `FULL-PRODUCT-DEFINITION.md` §19.1's target design (`store bytes in GCS at a TENANT-SCOPED content-addressed key (channel_id + sha256)`) — implemented here as a PostgreSQL **generated column**, so the two halves can never drift apart |
| "One row per channel, upsert, single toggle" shape | The same shape module #12's safe-mode switch and module #10's (concurrently built) QR Card use — a single-purpose creator config, not a session lifecycle like the Stream Mission or Giveaway/Tournament cards |
| No second tier gate; `sponsor_card` is already a module key | `packages/db/migrations/0131_v1_prf02_master_canvas_modules.sql:43` — `'sponsor_card'` is already in the twenty-key catalogue check constraint. §30.3's placement table has no row naming Sponsor Card specifically (only the generic Free 2 / Pro 5 / Creator 12 / Studio all module-count cap applies), so none is invented here — the identical reasoning `0135`/`0136` record for Stream Mission and Moderator Status |
| Owner/admin role check, `has_channel_role` | Used identically throughout — `0109`, `0131`, `0135`, `0140`, `0142` |
| "Not-found and not-authorised are the same answer" (`P0002`) | `0135`'s `end_stream_mission`, reused verbatim |

## The one blocker: logo bytes have nowhere to live yet

The instruction requires the logo to be "an asset, not a remote URL" and to follow §19.1: GCS/CDN
for bytes, Postgres holds metadata only, no `bytea` column. That is schema guidance this migration
follows exactly — `logo_content_sha256`, `logo_mime_type`, `logo_byte_size` are stored, and
`logo_storage_key` is generated from `channel_id` and the sha256, never independently writable.

**But no GCS/CDN client, bucket, credential or signed-URL code exists anywhere in this
repository.** Verified:

```
grep -rln "gcs\|GCS\|@google-cloud/storage\|signedUrl" apps/api/src   → no matches
grep -rl  "bytea" packages/db/migrations/*.sql                         → every existing asset
                                                                          table (0067, 0077, 0106,
                                                                          0110, 0119, 0122) stores
                                                                          bytes as bytea, which
                                                                          this task explicitly
                                                                          forbids reusing here
```

Building a GCS client, bucket policy, or signed-URL issuance path is standing up new
infrastructure — an ops/infra decision, a credential, and network egress from a backend whose own
architecture is otherwise DB-only. That is exactly the class of gap
`apps/api/src/domain/asset-scan-pipeline.ts` already documents for malware scanning in this same
codebase ("requires a scanning backend that does not exist anywhere in this repository... an
infra/ops decision... out of bounds for this lane's ownership boundary") — the identical judgement
applied to a different missing dependency.

**What ships as a result:** the sponsor name, enable/disable toggle and schedule window are fully
functional end to end (schema, API, contracts, canvas). The logo is **optional** everywhere
(nullable columns, `null` accepted at every layer) and its metadata shape is complete and tested,
but there is no route in this slice that accepts logo bytes and no way to actually populate real
logo metadata today outside a test fixture. This is reported here, not worked around by inventing
a storage client or by quietly adding a `bytea` column the task explicitly forbade.

**Exact blocking question for the owner:** should this slice (a) stand up a minimal GCS client as
new infrastructure now, (b) wait for a separate infra task to land one first and wire the logo
write path on afterward with zero schema change, or (c) ship the card name/toggle/schedule now and
track the logo as its own follow-up? No number, provider choice or credential can be chosen from
here.

## No-counter proof, stated plainly

Grep of this slice's full diff for `count`, `impression`, `exposure`, `views`, `shown_at`,
`displayed_at`, `duration` (run and its output pasted into the return contract) turns up **zero**
matches outside comments explaining their absence. `packages/db/tests/prf02_slice7_sponsor_card.sql`
case SP11.18 makes this a standing test: it scans every function this migration ships
(`pg_get_functiondef`) and every column on `public.sponsor_cards`
(`information_schema.columns`) for those tokens, so a future edit that adds one turns the suite red
by name rather than by a reviewer noticing a comment changed.

## Timezone: not invented

"Scheduled placement" ships as an absolute UTC `timestamptz` window (`schedule_starts_at`,
`schedule_ends_at`) — "show this sponsor between these two instants" — never a recurring
daily/local-time window ("every day 7–9pm"), because that would need a creator-timezone concept.
Grepped for `timezone`, `time_zone`, `tz_name` across `packages/db/migrations/*.sql`: no such
concept is decided anywhere in this repository (the one incidental hit, migration `0062`, is
unrelated queue-policy vocabulary, not a timezone field). None is invented here.

## Verification

See `../tests/TC-PRF-02-slice-7-sponsor-card.md`'s "Commands run" table for the actual numbers from
this run.
