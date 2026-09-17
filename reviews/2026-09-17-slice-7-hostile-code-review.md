# Hostile code review of PRF-02 slice 7 — five findings, two guards mutation-tested

**Date:** 2026-09-17
**Owner:** Sukhdev Singh
**Type:** Adversarial review of shipped code, requested after slice 7 landed
**Scope:** `bharatstudio-alerts` at `53d402a` — migrations `0143`–`0147` and everything wired to them
**Method:** reachability analysis, return-type audit, and **mutation testing of guards** rather than reading them

The brief was to grill the code, so the standard applied was not "does it pass" but
**"what does it do that nobody authorised, and what does it claim that is not true."**

---

## F1 — HIGH. The Media Queue renders arbitrary remote URLs on the Master Canvas

`public.media_queue_items.storage_url` and `thumbnail_url` are validated as exactly two
things: a `https://` prefix and length ≤ 2048. **No host allowlist, no CDN restriction, no
signature.** `media-queue-module.ts` then assigns them directly to `.src` at four sites
(`currentImgEl`, `currentVideoEl`, `preloadImgEl`, `preloadVideoEl`).

A creator can therefore queue an item pointing at any host on the internet, and the Master
Canvas fetches and renders it inside the OBS browser source.

**Against §9.1.1:** *"BharatStudio never embeds an arbitrary third-party browser-source URL,
HTML, JavaScript, CSS or iframe inside the Master Canvas. Ever."* — and *"there is no tier, no
attestation and no 'advanced mode' that makes it acceptable."*
**Against §19.1:** *"GCS behind the CDN with short-lived signed URLs. No public bucket path in
either case."* An arbitrary creator-supplied URL is neither.

**The module's own defence, stated fairly.** Its header argues an `<img>`/`<video>` `src` is
decode-only, grants the serving host no code execution and no DOM access, and that the mime
allow-list is closed — `image/png|jpeg|gif|webp`, `video/mp4|webm`, with `image/svg+xml`
excluded *because SVG can carry inline script*. **That reasoning is sound and this is not an
XSS vector.** But it is a narrowing of §9.1.1 that an implementing agent chose and no owner
approved. Three of the five harms §9.1.1 names still apply to a remote image — OBS
performance, reliability, visual branding — and two more follow: the remote host learns the
creator's IP, and the content can be swapped *after* the creator queued it.

**Why this matters beyond the rule.** It explains an inconsistency noticed earlier and not
understood at the time: three slice-7 modules honestly report that they cannot display media
without GCS, and this one appears to work. It appears to work **because it bypasses the
storage architecture entirely.**

| Module | URL handling | Verdict |
|---|---|---|
| Safe Soundboard (`0143`) | Server resolves a content-addressed key against **its own** configured CDN base; `null` today | Correct |
| Sponsor Card (`0145`) | Holds `logoStorageKey` and refuses to render it | Correct |
| Media Queue (`0146`) | Accepts any `https://` URL and renders it | **Outlier** |

**Disposition:** fixed in migration `0148` by mirroring `0143`'s pattern exactly — an object
key constrained to `^[A-Za-z0-9/_.-]{1,255}$` with no `..`, resolved server-side against
`config.mediaCdnBaseUrl`. The honest consequence is that the Media Queue **joins the other
three as unable to display media until GCS/CDN exists**. Preserving the appearance of working
was explicitly rejected.

---

## F2 — HIGH, and it is mine. I reported this module's behaviour wrongly

I told the owner the Media Queue *"lists the queue and cannot show or play the media"*, and I
wrote that into commit `e631291`'s message and into §6's row #20.

**It was true of the discarded duplicate lane, not the one that shipped.** When two
implementations of this module existed, I verified the discarded one's renderer and then kept
the other on separate evidence. The claim was never re-checked against the code that landed.

`e631291`'s message cannot be rewritten — later commits build on it — so the correction lives
here and in §6's row. **Root cause worth keeping:** when choosing between duplicate
implementations, every claim carried forward must be re-verified against the surviving code,
not the one that was examined first.

---

## F3 — MEDIUM. The Safe Soundboard can render nothing anywhere, and one cause is undisclosed

Three independent causes, only two of them documented:

1. `mediaCdnBaseUrl` unset → `playbackUrl` null. **Documented.**
2. Upload caps unset → every upload refused `caps_not_configured`. **Documented**, and it is
   what keeps the module compatible with §18.3/`MED-15`.
3. **The first-party catalogue has no reachable way to be populated.** *Undocumented.*
   `app_private.import_soundboard_catalogue_entry` is defined and granted to `bsa_app`, but
   **no product code calls it** — no route, no seed, no migration-level call. Migration `0143`
   describes its caller as *"a trusted internal import path, never end-user input"*. That
   import path does not exist.

**Checked before blaming it:** `0143` copies `0110`'s `import_sticker_catalogue_entry`
faithfully, and that function has the same property — no product caller either. So this is
**consistent existing practice, not a defect introduced by this slice.** The practical
consequence stands regardless: `soundboard_catalogue_entries` is empty in every environment,
so §6's *"First-party clips are unaffected"* reads as "they work" when they cannot.

---

## F4 — LOW. An untested seam between SQL and the store

`apps/api/src/db/safe-soundboard-store.ts` maps Postgres `errcode 55000` →
`{ outcome: 'caps_not_configured' }`. Neither layer covers that mapping: the SQL tests stop at
SQL, and the route tests stub the store. If the errcode changed, both suites stay green and
production breaks. This is the exact shape of a lesson this repository already learned —
*route tests that stub the store prove nothing about SQL function bodies.*

---

## F5 — LOW. Configuration changes require an overlay reload

Both the layout read and the module-entitlement read are one-shot IIFEs on mount. Only module
**data** is live, via `connection.subscribe()`. A creator who switches to vertical, or toggles
a module, sees nothing until the OBS browser source restarts. The layout is **consistent with
the pre-existing entitlement read**, so this is not new — but nothing says so anywhere.

---

## What survived the grilling

Stated because a review that only lists faults misrepresents the work.

- **Every route is registered and every store wired** — five for five. No `app_private`
  function shipped in `0143`–`0147` is unreachable; the two that looked test-only were an
  internal helper called seven times inside its own migration, and the catalogue importer in
  F3.
- **All five overlay reads carry no viewer, supporter or session identifier.** Privacy is
  enforced on the declared `returns table` type, not on renderer discipline.
- **Sponsor's no-counter guard genuinely fails when violated.** Injected an
  `impression_count` column; it failed with *"SP11.18: public.sponsor_cards must not carry a
  count, impression, exposure, view, shown, display or duration column of any kind; found:
  impression_count"*. File restored byte-identical, `sha256 1ab9e762…` before and after.
- **The Pro tier gate genuinely fails when bypassed.** Forced
  `vertical_canvas_layout_entitled` to `select true`; caught with *"a free-tier channel must
  not be vertical-entitled, got t"*. Restored, `sha256 2d4dc364…` verified.
- **Upload inertness is proven at SQL level**, not merely stubbed: `0143` raises `55000` when
  either cap is null and the SQL test asserts that sqlstate.
- **The mime allow-list is genuinely closed** and excludes `image/svg+xml` for the right
  stated reason.
- **The layout is genuinely not a module** — no `registerModule`, and `getSubscriberCount()`
  stays 16.
