# Active v1 template-library authority

**Status:** `Approved catalogue contract; runtime package completion and visual verification pending`
**Scope:** Alerts v1 presentation catalogue only
**Authority:** `../active/launch/00_LAUNCH_SCOPE_AUTHORITY.md`
**Contract:** `/Users/sukhdevsingh/Workspace/Bharat Studio/bharatstudio-alerts/contracts/template-catalogue.json`

## Product decision

The v1 Alerts catalogue is the `visuals-v6` catalogue: 600 designs, 30
families, and 20 variants per family (`BSA-001` through `BSA-600`). The
catalogue is a presentation library, not a payment, queue, or delivery
entitlement. A plan limit may restrict creation or selection of a new
presentation, but it must never delete, delay, suppress, acknowledge, or
otherwise alter an accepted payment, alert event, outbox row, or delivery.

## Entitlement rule

The `tier_availability` value is the minimum tier required for a design:

| Tier | Available variants | Branding |
|---|---:|---|
| Free | v01–v06 | BharatStudio watermark/text required |
| Pro | v01–v06 | BharatStudio watermark/text required |
| Creator | v01–v14 | Creator text/logo options; BharatStudio rules still apply |
| Studio | v01–v20 | Full approved branding controls; no BharatStudio watermark |

The server is authoritative for the effective tier and catalogue version.
Clients may display locked designs but cannot self-grant access. The current
v1 catalogue does not require Lottie; Lottie/advanced animation is a separate
presentation capability and must not be implied by a design metadata record.

## Contract requirements

Each catalogue record must identify its design ID, family, variant, minimum
tier, supported event types, typography metadata, cultural-review status and
runtime package reference. Each runtime package must provide `index.html`,
`design.json` and `review.md`, and must pass entry → hold/update → exit → idle
reset, long-text/multiline, reduced-motion, placement/scale and event-payload
checks before public release.

The runtime package is an implementation prerequisite. Metadata alone cannot
make a design selectable or publicly advertised. Missing or invalid packages
remain unavailable while their accepted alert data stays durable and
replayable.

## Evidence audit — 2026-08-15

Read-only inspection of `/Users/sukhdevsingh/Desktop/Final Alerts/visuals-v6`
found 600 metadata JSON records across 30 families and 12 supported event
types. It found 241 complete `BSA-XXX` runtime packages, leaving 359 designs
without `index.html`, `design.json` and `review.md`. The BSA-037 variant-label
exception was corrected from `v37` to the family-approved `v17` in the source
metadata and review card on 2026-08-15.

These findings do not authorize mass copying or automatic generation. The
remaining work is sequential package authoring, validation, visual review and
catalogue reconciliation. Until that work is complete, L03-09 is no longer
definition-blocked, but it remains implementation- and visual-verification
blocked.

## Execution sequencing — deferred final pass

By owner direction on 2026-08-15, no additional BSA runtime package generation
or visual-library expansion is to start while the non-visual v1 implementation,
integration, security, staging and launch gates are being completed. This is a
sequencing decision, not a reduction of the approved 600-design catalogue.

The two packages already authored locally, BSA-222 and BSA-223, remain local
implementation evidence only. They are not a declaration that the catalogue
is production-complete and they do not change tier availability, payment
durability or delivery guarantees.

The remaining 359 runtime packages are deferred to the final implementation
pass. That pass must author and verify them sequentially, then reconcile the
catalogue manifest and entitlement checks. It must include lifecycle replay,
all 12 event types, supported locales, long/multiline text, reduced motion,
placement and scale, accessibility, browser/OBS rendering, and review evidence
before any package is advertised as selectable in production. The deferred
scope is tracked at:

`../pending/launch/PENDING-04-TEMPLATE-RUNTIME-PACKAGE-COMPLETION.md`

## Traceability

- L03 acceptance: `tests/TC-L03-alerts-web-and-creator-api.md`, L03-09.
- L07 tier display: `tests/TC-L07-companion-web-mobile-desktop.md`, L07-04.
- L09 visual/capacity proof: `tasks/L09-observability-load-failure.md`.
- Full launch gate: `tasks/L10-release-readiness-and-rollout.md`.
