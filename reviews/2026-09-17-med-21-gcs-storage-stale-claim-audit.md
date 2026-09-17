# MED-21 is marked usable and nothing implements it — GCS/CDN media storage audit

**Date:** 2026-09-17
**Owner:** Sukhdev Singh
**Type:** Hostile audit finding — stale claim / false readiness evidence
**Severity:** High. It misreports a register row as usable, and it silently blocked three
modules in PRF-02 slice 7.
**Scope audited:** `bharatstudio-alerts` at `932a87b` (main checkout, clean)
**Authority:** `FULL-PRODUCT-DEFINITION.md` §19.1, register rows `MED-21`, `MED-19`,
`AUD-10` · `active/launch/01_MASTER_RELEASE_AUTHORITY.md` "Amendment — 2026-09-14 —
uploaded media storage"

## How this surfaced

Not by looking for it. Three independent PRF-02 slice-7 lanes — Safe Soundboard (audio
bytes), Sponsor Card (logo bytes) and Media / Meme Queue (media bytes) — each needed to turn
stored bytes into something a browser can fetch. Two of them independently reported that no
such path exists, and the third refused to render media for the same reason rather than
inventing an address scheme. Three agents hitting one wall from three directions is what made
it worth auditing rather than working around.

## The claim

Register row `MED-21`, state letter **`U` (usable)**:

> Lottie + custom branding upload, Studio-tier, live gate. **`bytea` storage is legacy** —
> new writes go to GCS per §19.1; the `bytea` path stays as the rollback route until backfill
> completes

§19.1 elaborates: all new media writes go to GCS; serving is "GCS behind the CDN with
short-lived signed URLs"; the `bytea` path "stays functional, so a GCS or CDN failure
degrades to the old path"; and "the switch is a per-channel flag, revertible in one action".
`01_MASTER_RELEASE_AUTHORITY.md` was **amended on 2026-09-14** to carry this, stating
"Postgres holds metadata only."

## What is actually there

Measured directly at `932a87b`, not inferred:

| Claim | Measured reality |
|---|---|
| New media writes go to GCS | **No GCS client exists.** No `@google-cloud/storage` dependency in any `package.json`; no match for `@google-cloud/storage`, `signedUrl`, `getSignedUrl`, `createBucket` or `storage.bucket` anywhere in `apps/`, `packages/`, `services/` or `scripts/` |
| Served behind CDN with signed URLs | **No signed-URL code of any kind** |
| `bytea` is the legacy path | **`bytea` is the only path.** Live in `0067` (TTS enrichment), `0077` (Lottie branding), `0119` (creator sticker packs), `0122` (staff pack review) |
| Per-channel switch flag | **Absent** |
| "Postgres holds metadata only" | **False.** Postgres holds the bytes |
| Schema half at least present | **Absent.** Zero migrations contain `gcs_object_key`, `gcs_bucket` or `storage_backend` |

§19.1's own **"Done when"** is *"zero new writes to `bytea`, the backfill queue is empty, and
one asset has been served from both paths in the same session."* Every write is `bytea`;
there is no backfill queue; there is no second path to serve from.

## What kind of failure this is

This is §2 at authority scale — the pattern where code exists, is tested and is committed,
but nothing reachable triggers it. Here it is one step worse: **there is no code at all.** A
decision was taken, written into §19.1, and used to amend a launch authority, and the register
row was then set to `U` as though the decision were the implementation.

**The decision itself is not in question and is not reopened.** GCS/CDN for bytes with
Postgres holding metadata is the right design and stays the design. What is wrong is the
claim that it is in place.

## Disposition

1. **`MED-21`'s state letter is wrong.** `U` asserts a working capability. Nothing works.
   The letter is corrected to **`A` (absent)** — the decision exists, the implementation does
   not. Recorded here rather than changed silently.
2. **§19.1's migration/serving/rollback table describes a target, not a present state**, and
   is annotated to say so, with its effective status dated.
3. **The 2026-09-14 amendment to `01_MASTER_RELEASE_AUTHORITY.md` stands as an approved
   decision** but must not be read as evidence of a built capability.
4. **A prerequisite task is required** before any module can render or play stored media.
   It is plausibly **externally blocked**, not merely unbuilt: a bucket, a service account
   and credentials are ENV-class prerequisites, and `ENV-03/04/05/06/08` are already Blocked.
   That must be confirmed, not assumed, before the task is scheduled.

## Consequence for PRF-02 slice 7, stated so it is not rediscovered

| Module | Effect |
|---|---|
| #6 Safe Soundboard | Creator-uploaded audio cannot be played. First-party clips are affected identically — they are bytes too |
| #11 Sponsor Card | Name, toggle and schedule work end-to-end. The **logo cannot be displayed** |
| #20 Media / Meme Queue | The card lists the queue — title, kind, duration. It **cannot show or play the media** |

Each of those three shipped the half that does not depend on storage, and named the half that
does. That is the correct outcome and must not be presented as the module being complete.

## What was NOT done, deliberately

No GCS client was stood up as a side effect of this audit. Standing up storage infrastructure
touches credentials, a bucket, a deployment contract and a cost, and none of that is
authorised by a decision to build three canvas modules. It needs its own authority, its own
task and an answer on whether the ENV prerequisites are obtainable.

## One exact question for the owner

**Is a GCS bucket plus service-account credentials obtainable now, or is it blocked with
`ENV-03/04/05/06/08`?** If obtainable, this becomes a scheduled prerequisite task and the
three modules complete behind it. If blocked, `MED-19`, `MED-21`, `AUD-10` and the media half
of three slice-7 modules are all Blocked-external on the same root cause, and should be
grouped under it rather than tracked separately.
