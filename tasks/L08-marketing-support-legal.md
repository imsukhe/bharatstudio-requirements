# L08 — Marketing, support, legal and launch communications

**Status:** `Static parent/product shell implemented — final content, support, legal/provider and public-host evidence pending`  
**Level:** L3  
**Owner:** Marketing / product / support / legal  
**Depends on:** L01 approved scope/contracts for early work; final public release sign-off depends on L03, L04 and L07  
**Blocks:** public launch
**Test record:** [`../tests/TC-L08-marketing-support-legal.md`](../tests/TC-L08-marketing-support-legal.md)
**Review record:** [`../reviews/2026-08-15-L07-L08-L10-release-surface-review.md`](../reviews/2026-08-15-L07-L08-L10-release-surface-review.md)
**Local regression record:** [`../reviews/2026-08-15-local-regression-and-surface-verification.md`](../reviews/2026-08-15-local-regression-and-surface-verification.md)

## Objective

Create a parent BharatStudio marketing surface and the public/legal/support readiness needed to sell Alerts and Companion accurately.

## Work sequencing

Early legal, provider, privacy, support and public-copy work starts after the v1 authority and contracts are approved. It must not wait for the Companion implementation. Final legal/provider/store sign-off remains a release gate after payment, mobile, desktop and infrastructure evidence exist.

## Tasks

1. Build parent IA: home, Alerts, Companion, pricing, compare, resources, support, legal, account/help entry points, sitemap, robots, metadata and structured data.
2. Clearly separate public Marketing from Alerts product application and public tip pages. Keep public tip checkout under Alerts, not Marketing.
3. Publish tier comparison from one server-owned entitlement/pricing source; show locked/available features accurately and do not promise free-forever or unavailable YouTube/Enterprise features.
4. Prepare support taxonomy, contact flows, status/incident process, refund request flow, account closure/deactivation wording, security/privacy concern flow and escalation runbooks.
5. Start legal/CA/provider review immediately after scope approval: entity and creator-direct payment disclosures, Razorpay TP/connected-account requirements, refunds, privacy/retention wording, terms, tax/GST/TDS/KYC implications, international-payment claims and app-store boundaries.
6. Create the legal/provider evidence register, open external applications, identify owners and record lead times; do not wait for code completion to submit provider or store-account requests.
7. Run SEO/content/accessibility checks; set privacy-safe analytics and consent configuration; no internal architecture/secrets/provider keys in public copy.
8. Create launch comms, creator onboarding guides, OBS setup, overlay troubleshooting, Companion/desktop-helper limitations and change/incident templates.
9. After L03/L04/L07 and infrastructure proof, perform final legal/provider/store review against the implemented product and publish dated versions of all required policies.

## Current implementation evidence — 2026-08-15

- Added the static Cloudflare-compatible parent surface under `/Users/sukhdevsingh/Workspace/Bharat Studio/bharatstudio-marketing/public/`: BharatStudio home, Alerts, Companion, pricing, support and legal index pages, plus shared responsive styles.
- Added `robots.txt`, `sitemap.xml` and a small static-site test suite. `npm test` passes five checks (5/5) covering page metadata/navigation, internal-link resolution, discovery files, the static deployment security boundary and the absence of private/payment/Phase-2 terms in public pages on 2026-08-15.
- The static-site gate now resolves every root-relative link published by those pages against the checked-in public tree. A missing product or support target therefore fails locally instead of reaching publication as a broken navigation path.
- The pages use only the approved v1 plan prices and product boundaries. They contain no checkout, provider credentials, creator dashboard, internal architecture or payment-webhook logic.
- This is a local content/structure implementation only. It does not establish SEO ranking, legal/provider approval, support SLA readiness, analytics consent deployment, domain/certificate configuration or final public copy approval.
- Added the single launch register at `active/launch/05_SUPPORT_AND_EXTERNAL_EVIDENCE_REGISTER.md`. It defines safe support intake, internal triage targets, payment/alert escalation, redaction and the dated evidence required for Razorpay, tax, privacy/retention, terms/refunds, app stores, public hosting, support operations and analytics. It deliberately leaves external/legal/provider rows open until evidence exists.
- Added a static-host deployment boundary under `bharatstudio-marketing/public/_headers` and `public/.well-known/security.txt`. Cloudflare-compatible headers deny scripts, browser integrations, framing and content-type sniffing, limit referrers/permissions, and publish a dated vulnerability-reporting contact. This is a public-surface hardening slice only; Cloudflare deployment, DNS/HTTPS, contact monitoring and security-response rehearsal remain open.

## Fresh local audit — 2026-08-15

The parent marketing surface, six public pages, static-site test, pricing/legal
copy, support boundary and `05_SUPPORT_AND_EXTERNAL_EVIDENCE_REGISTER.md`
were reviewed together. No additional locally verifiable content or boundary
gap was found.

Confirmed locally:

- BharatStudio is presented as the parent brand with separate Alerts and
  Companion product surfaces;
- public tip/payment checkout is not implemented in the static marketing site;
- pricing shows only the approved v1 planning schedule and does not claim
  YouTube, Enterprise, free-forever or provider approval;
- public pages do not expose architecture, webhook logic, credentials or raw
  payment/OBS data;
- support and privacy contacts instruct users not to send passwords, tokens or
  provider secrets;
- robots, sitemap, metadata/navigation and root-relative link resolution pass
  the local static-site test.
- the checked-in static deployment boundary denies scripts, outbound browser
  connections, framing, camera/microphone/geolocation/payment permissions and
  content sniffing; `security.txt` has a dated contact and canonical URL.

L08 remains open for final copy approval, dated terms/privacy/refund and
retention versions, Razorpay/provider and written CA/legal evidence, staffed
support tooling and incident rehearsal, domain/HTTPS/email proof, deployed
analytics-consent and SEO/accessibility scans, and the final publish/rollback
rehearsal. The local site test must not be treated as a legal or SEO approval.

## Acceptance criteria

- Marketing accurately presents BharatStudio, Alerts and Companion with no v1-excluded claims.
- Price, annual renewal, cancellation, grandfathering, payment/refund and data wording match approved authority.
- Early legal/provider applications and review evidence exist before implementation is considered complete; final legal/provider/store gates have dated evidence or the release is blocked.
- Support can receive, triage, respond to and audit every launch-class issue.

## Rollback

Static site pages can be rolled back independently. Pricing/legal changes require versioning, approval and published effective date; never silently replace a policy needed for historical evidence.

### Automatic continuation verification — 2026-08-15

`bharatstudio-marketing` `npm test` passed 5/5. Metadata/navigation, internal
link resolution, discovery files, static-host security headers and the support
surface checks remain green. This is local static-site evidence only; it does
not close legal/provider review, staffed support, domain/HTTPS/email,
analytics-consent deployment, SEO/accessibility scans or publish/rollback
rehearsal.
