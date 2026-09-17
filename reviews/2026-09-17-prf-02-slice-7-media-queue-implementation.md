# PRF-02 slice 7 — Media / Meme Queue (§6 #20): the decisions this implementation took, and what each rests on

**Date:** 2026-09-17
**Owner:** **Sukhdev Singh**
**Task:** `../active/tasks/PRF-02-slice-7-media-queue.md`
**Acceptance:** `../tests/TC-PRF-02-slice-7-media-queue.md`
**Binding owner decision:** `2026-09-17-remaining-eight-modules-and-youtube-v1-amendment.md` Part 1 §8
**Reviewer:** self-review only. **No independent review occurred**, and none is claimed.

The owner decision that authorised this slice is short by design — "the creator queues their own
media, viewers cannot submit" — and left the schema, the overlay projection shape, the URL-safety
mechanism and two numeric caps to the implementation. Every one of those fills is recorded below
with the thing it rests on, because the standing constraint is that no numeric limit, provider
behaviour or legal wording may be invented.

---

## 1. The overlay read is "current and next", reusing an EXISTING bound rather than inventing a queue-depth number

**Decision.** `app_private.list_overlay_media_queue` returns at most two rows, labelled `'current'`
and `'next'`, and no aggregate queue-depth count anywhere.

**What this rests on.** The task instructions pointed at "the overlay's bounded event pool and the
§12.7 client-side cap" as a hint to find a real number in the code rather than inventing one.
Searching found no reusable numeric constant for a queue's item count specifically, but found an
exact, already-shipped INSTANCE of the shape needed:
`apps/web/app/overlay/canvas/modules/support-theater-module.ts:68-72`'s own comment states the
module "renders exactly the CURRENT displayed group ... and exactly ONE next-up entry — never a
queue depth, never a second item deeper in the queue," directly instantiating §12.7's Overlay row
text, "current and next alert state." Reusing that shape rather than picking a number (2, 3, or a
configurable N) is the same discipline the giveaway/tournament card's own reuse of `0109`'s title
bound followed — an ALREADY-DECIDED shape, not a number this implementation chose.

**Why "next" is used for preloading and never rendered.** The owner decision does not mention
pre-loading at all; this is an implementation choice, made explicit rather than left implicit,
because a queue of broadcast media (unlike an alert stream) has an obvious latency cost if the
following asset is not already decoded when the creator advances the queue. `media-queue-module.ts`
holds "next" only in a permanently-hidden preload element pair and never shows it — verified
directly in `media-queue-module.test.ts`.

---

## 2. Storage is metadata-only (§19.1), and this slice does NOT build an upload pipeline

**Decision.** `public.media_queue_items` carries `storage_url`/`thumbnail_url` TEXT columns
pointing at an already-hosted GCS/CDN asset. There is no `bytea` column and no upload/transcode
code anywhere in this slice.

**What this rests on.** The task's hard constraint is explicit and specific to this module:
"Do NOT add a `bytea` column," and `MED-21` independently records that the `bytea` path (migrations
`0067`, `0077`, `0106`, `0110`, `0119`) is legacy, kept only as a rollback route. This is a
DIFFERENT posture from the sibling Soundboard module (§6 #6), whose own owner decision explicitly
reuses migration `0110`'s bytea-based creator-pack storage as its reuse anchor — that reuse anchor
is simply not available to this module given the hard constraint governing it.

**What this means was NOT built, and why that is correct rather than incomplete.** §19.1's actual
upload pipeline — "transcode, normalise and pre-scale on import; content-addressed tenant-scoped
storage" — is register item `INT-07`, independently marked `new-record-required` and not part of
this task. This slice assumes an asset already has a URL by the time it reaches
`enqueue_media_queue_item`, the identical posture migration `0123`'s `attach_provider_qr` already
takes for an already-hosted QR image (it validates the URL's shape; it does not mint one). Building
`INT-07` is future work, referred rather than improvised here.

---

## 3. §9.1.1 permits a first-party media URL; it does not ban every URL

**The apparent tension, stated plainly.** This task's own hard-constraint summary reads "no
third-party code, URL, iframe, script or stylesheet may reach the Master Canvas; the module
definition must have no field capable of carrying one" — read most literally, that could be taken
to forbid a `storageUrl` field of any kind, which would make this module unbuildable, since §19.1
explicitly requires one.

**Resolution, checked against the authoritative text rather than the paraphrase.**
`FULL-PRODUCT-DEFINITION.md` §9.1.1's actual rule is: "BharatStudio never embeds an **ARBITRARY
THIRD-PARTY** browser-source URL, HTML, JavaScript, CSS or iframe inside the Master Canvas." The
operative qualifier is "arbitrary third-party" — the rule bans embedding a foreign PAGE (an iframe
`src` or a script `src`, which grants the serving host code execution and DOM access inside the
Canvas), not every URL of any kind. §9.2 confirms this reading directly: a first-party Canvas
package explicitly "bundles ... images, video, audio and Lottie assets." The §6 #19 (Chat) row in
the SAME owner-decision document being corrected on 2026-09-17 for exactly this over-broad reading
("§9.1.1 scopes strictly to 'inside the Master Canvas'" — the row had wrongly been blocked on a
misreading of the rule) is independent, same-day confirmation that a literal-maximalist reading of
§9.1.1 is the error mode to avoid, not the safe default.

**What makes this module's URL structurally different from an iframe/script anyway.**
`storageUrl`/`thumbnailUrl` are handed ONLY to an `<img>`/`<video>` element's `src` in
`media-queue-module.ts` — never to a script, an iframe or a stylesheet, and there is no code path in
that file capable of doing so. `mime_type` is a closed allow-list (image/png, image/jpeg,
image/webp, image/gif, video/mp4, video/webm) enforced at the CHECK constraint, at
`enqueue_media_queue_item`'s re-validation, and at the route's AJV schema — no `text/html`, no
`image/svg+xml` (SVG can carry inline script), no `application/*` of any kind. A browser decoding a
response as `image/png` or `video/mp4` cannot execute it as code or use it to control the embedding
page, regardless of which host serves the bytes — a strictly weaker capability than an iframe or a
script tag, and the only capability this column can ever carry. `storage_url`/`thumbnail_url` are
additionally required `https://`-only (reused from `0123`'s exact validation shape, see §4 below).

**What this implementation did NOT add, and named as a gap rather than building it.** No
CDN-origin allow-list (restricting `storage_url` to a specific first-party hostname) exists — no
such origin is decided anywhere in the register, and inventing one would be inventing
infrastructure this task's own constraints forbid. The mime-type allow-list is the structural
defence that does not depend on which host serves the bytes; an origin allow-list would be a
SECOND, narrower defence layered on top of it, and is referred to the owner in §7 below rather than
guessed at.

---

## 4. URL validation reuses `0123`'s exact shape rather than inventing one

**Decision.** `storage_url`/`thumbnail_url` must be non-empty, at most 2048 characters, and
`https://`-prefixed, checked with `left(value, 8) = 'https://'`.

**What this rests on.** `packages/db/migrations/0123_v1_l19d_provider_qr_codes.sql:192` validates
`target_qr_image_url` with the identical `left(target_qr_image_url, 8) <> 'https://'` shape for an
already-hosted QR image URL — the closest existing precedent in this codebase for "a URL pointing
at externally-hosted media, validated for scheme only." Reused verbatim rather than re-derived.

---

## 5. The two numeric caps ship configured but unset — and this task's own definition of "unset" governs, not the sibling module's

**Decision.** Neither a maximum media duration nor a maximum number of items a channel may queue at
once has a decided value. Both ship as nullable parameters to `enqueue_media_queue_item`, threaded
from `apps/api/src/config.ts` (`mediaQueueMaxItemDurationMs`, `mediaQueueMaxItemsPerChannel`),
mirroring the exact mechanism `reactionCloudSampleMax` already uses.

**Why "unset" means "no additional ceiling" here, and NOT "the control is inert" — recorded because
it is a deliberate divergence from a neighbouring decision, not an oversight.** The sibling
Soundboard module's (§6 #6) own owner decision ships its equivalent caps "configured but unset" in
a stricter sense: "for an upload path" it means "the upload control is inert until a cap exists."
This task's OWN instructions define the phrase differently and explicitly for the work assigned
here: "ship configured but unset (unset = today's behaviour, never a guessed default)" — the
identical wording, mechanism and intent `apps/api/src/config.ts` already documents for
`overlayMaxInstanceSubscribers`, `derivedReadMaxConcurrent` and `reactionCloudSampleMax`. Those
three are all "unset = no additional ceiling, bounded only by what is already true," never "unset =
disabled." Given the task's own definition governs the work it assigned, and Media / Meme Queue is
creator-only with none of the Soundboard's anonymous-upload-volume risk profile to weigh against it,
this implementation took the more permissive (mechanism-built, value-absent) reading. This is stated
as a choice between two legitimate readings, not as the only possible one — see §7 below.

---

## 6. FIFO order and no reordering — an absence, not an oversight

**Decision.** Items play in the order they were queued (`created_at` ascending); there is no
reorder function, no priority column and no "move to front" endpoint.

**What this rests on.** The owner decision authorises "the creator queues their own media" and says
nothing about reordering. Building a reorder surface would be inventing a product feature nobody
decided — the identical discipline `0142`'s header applies to why a bracket TREE was not built
(no display-name concept invented to make it buildable). FIFO is the one ordering that requires no
additional column, no additional decision and no additional function.

---

## 7. Referred to the owner

- **Neither configured-but-unset cap (media duration, queue-item count) has an actual value.** Both
  are deployment configuration only. Whether either should ever differ by tier — which §12.6 would
  forbid for STORING an item but does not obviously forbid for a canvas-RENDER cap, the same
  distinction §12.6 itself draws — is unresolved and is the owner's to decide, not an implementer's.
- **Whether `storage_url` should additionally be restricted to a specific first-party CDN origin**
  (beyond the https-only + closed-mime-type structural defence already built) is a decision this
  implementation did not make, because no such origin exists anywhere in the register yet. If and
  when GCS/CDN infrastructure (`INT-07`) is decided, this migration's `enqueue_media_queue_item`
  has a clear extension point (`target_storage_url`'s validation) for an owner-supplied origin.
- **Reordering the queue** was not asked for and is not built (§6 above). If the product wants one,
  that is a new decision, following the identical "an entry method stored with nothing enforcing it
  is decoration" discipline `0142`'s own header states for a different feature.
