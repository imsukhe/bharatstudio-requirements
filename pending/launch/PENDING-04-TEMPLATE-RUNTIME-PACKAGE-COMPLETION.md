# Pending — template runtime package completion

**Status:** Deferred until the final v1 implementation pass  
**Owner:** BharatStudio product/engineering owner  
**Authority:** [`../../active/launch/04_TEMPLATE_LIBRARY_AUTHORITY.md`](../../active/launch/04_TEMPLATE_LIBRARY_AUTHORITY.md)  
**Acceptance:** [`../../tests/TC-L03-alerts-web-and-creator-api.md`](../../tests/TC-L03-alerts-web-and-creator-api.md), L03-09

## Decision

Do not generate additional BSA alert packages during the current non-visual
implementation, integration, security, staging or launch-gate work. The
approved v1 scope remains the full `visuals-v6` catalogue of 600 designs; this
item is deferred work, not a scope reduction or cancellation.

The already-authored BSA-222 and BSA-223 packages remain local evidence only.
They must not be treated as proof that the catalogue is production-complete.

## Remaining scope

The catalogue audit currently reports 241 complete runtime packages and 359
missing packages. The deferred completion pass covers every missing package,
currently beginning with BSA-224 and continuing through the remaining missing
IDs up to BSA-600. The exact set must be recalculated from the manifest at the
start of that pass; no ID may be skipped because an earlier package is invalid.

## Required final-pass method

1. Freeze the non-visual v1 contracts, tier rules, event payloads, locale
   rules, accessibility rules and runtime lifecycle contract.
2. Select the first missing or failed package in numeric order and author it
   as a standalone package containing `index.html`, `design.json` and
   `review.md`. Do not use mass-copying, palette-only variants or generated
   placeholder packages.
3. Verify entry, hold/update, exit, idle/reset and replay behavior, including
   long and multiline text, all 12 event types, supported locales, reduced
   motion, safe placement, resize/scale and accessibility behavior.
4. Run browser/OBS rendering and visual review evidence for each completed
   batch; record failures and repair them before advancing.
5. Reconcile the manifest, package counts, tier entitlements and catalogue
   validation output. A metadata record without a verified runtime package is
   unavailable for production selection.
6. Complete independent design/native-language/accessibility review and attach
   the final evidence before L03-09 or the full launch gate can be marked
   verified.

## Non-negotiable guarantee

Template or tier limits must never delete, delay, suppress, acknowledge or
otherwise change an accepted payment, alert event, outbox row or delivery.
While a package is missing or under review, the system must retain the event
and use the approved fallback/unavailable state defined by the runtime and
delivery contracts.
