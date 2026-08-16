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

### Marketing migration completion pass — 2026-08-16

The marketing repository was migrated from the earlier minimal six-page shell
to the approved parent-brand structure while preserving the existing dark,
creator-focused visual language and keeping the public boundary intact.

Implemented public routes:

- Parent BharatStudio home with Products and Resources dropdown navigation;
- Alerts product page and Companion product page;
- consolidated feature map, pricing and download/start page;
- compatibility, creator docs, Companion docs and Alerts setup pages;
- resources hub and dated product-update placeholder;
- support and public status surfaces;
- legal hub, privacy, terms, refunds, contact, licences and data-rights request
  pages;
- robots, sitemap, static-host headers and vulnerability contact.

The old public homepage's theme and creator-oriented content direction were
used as design input, but unsupported historical claims (old pricing,
commission promises, tax claims, unrelated studio features and unavailable
integrations) were not carried into the v1 marketing surface. The Alerts
product page is now the product-specific conversion surface; the new root
homepage is the BharatStudio parent surface.

Local verification on 2026-08-16:

- `npm test`: 5/5 checks passed;
- 21 published HTML routes checked for title, description, stylesheet,
  BharatStudio identity and absence of secrets/provider internals;
- every root-relative link in those routes resolved against a checked-in
  target;
- download CTA uses a local Alerts route rather than an unconfirmed product
  hostname;
- robots and sitemap contain the complete published route set;
- static CSP, no-script boundary, permissions policy, HSTS and security.txt
  checks remain green;
- local browser preview visually checked the parent homepage at desktop
  viewport; no console-driven client integration is required.

This completes the local marketing implementation/migration slice. It does
not close the external release gates: final copy approval, dated legal and
retention policies, Razorpay/provider and CA/legal evidence, staffed support
and incident rehearsal, domain/HTTPS/email deployment, analytics consent,
structured-data/SEO crawl, accessibility scan, store links and publish/
rollback rehearsal remain required before public production release.

### Visual-system correction and framework migration — 2026-08-17

**Finding.** The 2026-08-16 migration preserved the correct IA, copy and
pricing, but the visual system was reinvented rather than carried over from
the legacy site: legacy used brand gold `#F7C948`, CTA blue `#3B7EF6`,
near-black surfaces (`#0A0A0F`/`#111118`), Rajdhani (display) + DM Sans (body)
+ JetBrains Mono, and spring-physics CSS motion (documented in the legacy
`globals.css` as "canonical token per FRD-009 §3"). The current static build
used an unrelated orange/green palette and Inter, with no motion tokens.
Confirmed by direct token comparison, not visual impression.

**Owner decision, 2026-08-17:**

1. **Re-skin and restore, not a copy audit.** Fix the visual system on all
   existing routes, and additionally restore the legacy pages dropped from
   the current build: `/streamers`, `/creators` (gallery), `/compare`,
   `/affiliate`, and real per-post `/resources/blog/[slug]` routes. Content on
   restored pages follows the same migration discipline already applied to
   the rest of the site: stale claims (old pricing, unrelated studio
   features, unavailable integrations) are not carried forward.
2. **Design tokens restored verbatim.** Gold/blue/near-black palette, the
   three original font families, spring-physics motion — as the base for
   every page, including net-new pages the legacy site never had (Companion).
   No new palette, no new type system. Companion-specific content, having no
   legacy reference, is authored fresh in the same visual language rather
   than left unstyled or skipped, matching how the rest of the migration has
   already treated genuinely new v1 surfaces.
3. **CSP revised from `script-src 'none'` to a scoped `script-src 'self'`.**
   Required to restore the homepage's animated alert-demo interaction.
   Binding rules: no inline `<script>`, no `unsafe-inline`/`unsafe-eval`,
   `connect-src` scoped to approved same-origin/BharatStudio targets only, no
   third-party analytics/chat domains without a separate privacy review, CSP
   violation reporting configured before production rollout. Payment, auth
   and provider-credential code remain out of this repository — the CSP
   change enables presentation-layer interactivity only, not a boundary
   change on what this repository is allowed to own.
4. **Architecture migrates from static HTML to a framework**, matching the
   legacy site's own `next/font/google` mechanism for the exact font
   restoration (self-hosted at build time, no manual asset sourcing, no
   separate CDN dependency). This is a tooling change only; per owner
   instruction, the rebuilt site must not introduce new design choices
   ("follow same theme, no AI slop") — every token, font and layout decision
   is sourced from the legacy system, not reinvented during the migration.

This entry records the decision before implementation, per this repository's
own governance requirement for an L2+ scope/architecture change. Implementation
evidence follows as a dated continuation of this entry, not a new task record.

### Foundation build and verification — 2026-08-17 (in progress)

**Real, build-verified evidence, not a status claim:**

- Next.js 16.3.0 App Router scaffolded (`output: 'export'`, static, matches
  the legacy app's own Next version). Design tokens, fonts (`next/font/google`
  self-hosting Rajdhani/DM Sans/JetBrains Mono, verbatim), and motion tokens
  restored from the legacy `globals.css` exactly — confirmed by direct
  side-by-side token comparison, not visual impression.
- `Nav`, `Footer`, `AlertCard`, `AlertDemoWidget` ported from the legacy
  marketing components (`nav.tsx`, `footer.tsx`, `alert-card.tsx`,
  `alert-demo.tsx`), with two adaptations required by this repository's own
  boundary, not design changes: the nav no longer fetches auth/session state
  (marketing must not own dashboard/session), and IA updated for the
  multi-product structure (Products/Resources dropdowns) the Alerts-only
  legacy nav never needed.
- **Every inline `style={{}}` prop rewritten to a named CSS class** — a real,
  verified finding, not a formality: React inline styles render as `style=""`
  HTML attributes, and CSP `style-src` governs those the same as `<style>`
  blocks. Confirmed zero `style="` attributes across all 23 built pages.
- **A real, load-bearing conflict found and resolved, not assumed away:**
  Next.js App Router's static export emits genuine inline
  `<script>self.__next_f.push(...)</script>` hydration payload on every page —
  confirmed by inspecting actual build output. This is structural to the
  framework, not something this build introduced, and it directly conflicts
  with the approved CSP's ban on inline script / `unsafe-inline`. Resolved
  with a build-time hash generator (`scripts/generate-csp-headers.mjs`, wired
  into `npm run build`) that computes each page's exact inline-script SHA-256
  hashes and writes one dedicated `Content-Security-Policy` block per route to
  `out/_headers`. **This was verified necessary, not assumed sufficient**:
  Cloudflare Pages merges multiple matching `_headers` rules by comma-joining
  duplicate header values, and CSP treats comma-joined policies as
  independent, each enforced — a single global `script-src 'self'` rule
  merged with a per-page hash addition would still block the hashed script,
  because the global policy carries no hash exception. Confirmed via
  Cloudflare's own documentation, not inferred.
- Hash computation cross-verified independently: the generator's Node
  `crypto` output was re-computed with a separate Python implementation
  against the same built HTML and produced byte-identical hashes.
- A custom `app/not-found.tsx` replaces Next's default 404 page, which itself
  uses inline styles internally — same CSP conflict, same fix, and gives a
  broken link the real design system instead of framework boilerplate.
- **Real build succeeds** (`npm run build`): 23 static pages, zero errors,
  zero TypeScript errors, generator confirms "23 route-specific CSP blocks (6
  inline-script hashes total)."
- Local visual verification via a real served build in a browser: homepage
  renders the restored gold/blue/near-black palette, Rajdhani display type,
  the floating pill nav with working Products/Resources dropdowns, and a
  genuinely functional `AlertDemoWidget` (auto-cycling sample alert, live
  name-personalization input, Free/Pro toggle). Zero console errors on the
  built page itself; the only network 404s observed are Next's own Link-
  prefetch mechanism correctly reporting that not-yet-migrated routes have no
  RSC payload — an accurate signal, not a defect.

**Explicitly NOT complete — do not read the above as the migration being
done:**

- Only the homepage (`/`) and the shared `Nav`/`Footer`/`AlertCard`/
  `AlertDemoWidget` components are real Next.js pages. The other 22 routes
  (`/apps/alerts/`, `/apps/companion/`, `/pricing/`, `/features/`,
  `/compatibility/`, `/docs/`, `/docs/companion/`, `/setup/`, `/resources/`,
  `/resources/blog/`, `/support/`, `/status/`, `/download/`, all six
  `/legal/*` pages) are still the prior static HTML, unconverted, still on the
  wrong palette/fonts.
- The five pages the legacy site had and the current build dropped —
  `/streamers`, `/creators` (gallery), `/compare`, `/affiliate`, real per-post
  `/resources/blog/[slug]` — are not yet restored.
- `npm test` (the static-site link/metadata suite) has not been re-run
  against the new build; its assumptions were written for the flat-HTML
  architecture and likely need updating for the Next.js output shape.
- Deployment to Cloudflare Pages has not been exercised — the generated
  `_headers` file's real-world behaviour (as opposed to its documented
  behaviour) is unverified against an actual Cloudflare edge.

## Full migration complete — 2026-08-16

Continuing under the owner's explicit "please complete all one by one without
pause" directive from the prior session. All remaining work listed above as
NOT complete is now done, with real evidence, not a status claim alone.

**All 24 re-skinned routes are real Next.js pages** using the established
double-bezel/panel/grid CSS system, zero inline styles: `/apps/alerts/`,
`/apps/companion/`, `/features/`, `/pricing/`, `/compatibility/`, `/docs/`,
`/docs/companion/`, `/setup/`, `/resources/`, `/resources/blog/` (+ 4 real
posts), `/support/`, `/status/`, `/download/`, `/legal/` and its six
sub-pages. Six new shared CSS patterns were added to `globals.css` to cover
content shapes not present on the homepage: `.steps`/`.step` (numbered
guides), `.notice` (warning callout), `.article` (long-form prose), `.faq`
(native `<details>` accordion), `.coming`/`.muted`/`.check` (status badges),
`.price-grid`/`.price-card`, `.table-wrap`/`.comparison`.

**All 5 dropped legacy pages are restored**, each with a real, individually
justified architecture decision rather than a blind copy-paste:

- `/streamers` — the legacy source itself is a redirect to `/features`
  (already consolidated before this migration), so this ships the same
  redirect, not new content. `next/navigation`'s `redirect()` was tried first
  and **empirically failed** under `output: 'export'` (produces a broken
  `__next_error__` fallback page with the wrong title — no server exists at
  request time to issue the 3xx). Fixed with a `<meta http-equiv="refresh">`
  tag, rendered directly in the page body and confirmed via the built HTML to
  be correctly hoisted into `<head>` by React 19 — no inline `<script>`,
  fully CSP-compliant, verified live in a browser (auto-navigates to
  `/features/`).
- `/creators` — the legacy version was a Server Component fetching live rows
  from an internal Fastify API (`GET /api/v1/creators/featured`) at request
  time. That does not carry over: this repo is a static export with no
  server at request time, `connect-src` has no approved creator-directory
  origin, and the repo boundary (`REPOSITORY-STRUCTURE.md`) says this site
  does not own live account data. Ships the same graceful zero-creators
  fallback state the legacy component already had built in for an empty API
  response — honest, not fabricated sample data. A future decision to open
  an approved API origin in `connect-src` would let this page go live.
- `/compare` — ported with its `CommissionCalculator` (real interactive
  `'use client'` component, sliders/inputs, no inline style) and the full
  three-section comparison table (manual methods / scraping tools / other
  platforms), preserving every existing hedge/pending-review caveat
  verbatim (Razorpay Technology Partner status pending, commission-range
  estimate disclaimers, D-C053 no-competitor-names). **One factual
  correction made against the source**: the legacy page's "other platforms"
  price comparison cited BharatStudio's own price range as ₹199–₹449; this
  repo's approved `/pricing` is ₹199–₹499 (Studio). Corrected to match the
  current approved figure per governance's "latest approved document is the
  source of truth" rule — everything else on the page is unchanged.
- `/affiliate` — ported in full (reward tiers, 3-step how-it-works, 5-step
  qualification disclosure, disqualification list, FAQ, mock dashboard
  preview). The programme is explicitly not-yet-live in the source content
  ("rolling out soon", "Preview only — not a live page") and stays that way
  here; no new availability claims were added. Sign-up CTAs point at this
  site's own `/download/` funnel instead of the legacy monorepo's
  app-relative `/login`, matching how every other page here links to the
  product.
- `/resources/blog/[slug]` — all 4 real posts ported verbatim from
  `blog/posts.ts` (dated 2026-07-15 through 2026-08-01), rendered through a
  purpose-built `BlogContent` component extending the legacy renderer with
  `###` and ordered-list support the original never implemented (the source
  content uses both; without this fix they would have rendered as literal
  `### ` text). **One content correction made during porting**: the source
  post said "your YouTube avatar" — caught by this repo's own established
  test suite (`site.test.mjs` bans naming YouTube/SuperChat/Enterprise,
  consistent with `/compare`'s no-competitor-names rule) and corrected to
  "your channel avatar."

**Navigation completeness fixed**: `Nav.tsx`'s Products dropdown didn't
include `/compare/` or `/creators/`, and Resources didn't include
`/resources/blog/` — real reachability gaps, not new design, now added
(with the mobile stagger CSS extended from 8 to 10 items to match). Footer
already linked Compare/Referral/Blog but not Creators — added.

**Build configuration fix, found and verified, not assumed**: static export
without `trailingSlash: true` emits `<route>.html` files, not
`<route>/index.html` — confirmed by inspecting `out/` after a first build,
which produced `out/apps/alerts.html` while every internal link and the
sitemap use the `/apps/alerts/` trailing-slash form. Added
`trailingSlash: true` to `next.config.ts`; rebuilt; confirmed the output
tree now matches every link.

**Real evidence, this pass:**

- `npm run build` succeeds: 32 routes (24 re-skinned + `/streamers` redirect
  + `/creators` + `/compare` + `/affiliate` + 4 real blog posts), zero
  TypeScript errors. `generate-csp-headers.mjs` reports "32 route-specific
  CSP blocks (64 inline-script hashes total)."
- `tests/site.test.mjs` was rewritten for the new architecture (previous
  version read flat `public/*.html`, which no longer exists as page
  content) and all 6 tests pass against the real `out/` build output: safe
  metadata + no leaked secrets across all 28 checked routes, all internal
  links resolve to a real built target, zero `style="` attributes anywhere
  in built HTML, the `/streamers` redirect's target is present, discovery
  files (`robots.txt`/`sitemap.xml`) present and cover every route,
  `_headers` has a complete per-route CSP block for every route with no
  `unsafe-inline`/`unsafe-eval` and the approved base directives.
- `sitemap.xml` rewritten to list all 27 real routes (`/streamers/` excluded
  — it 301-equivalents to `/features/`, not a separate indexable URL).
- Old `public/*` static HTML directories (`apps/`, `features/`, `docs/`,
  `setup/`, `resources/`, `support/`, `status/`, `download/`, `legal/`,
  `compatibility/`, `pricing/`) deleted — superseded by the Next.js `app/`
  routes; `public/` now holds only pass-through assets (favicon, fonts,
  icons, images) and discovery files (robots.txt, sitemap.xml,
  security.txt). `out/` added to `.gitignore` (build artifact, was
  untracked and un-ignored).
- Browser verification across representative pages (not just the homepage):
  `/compare/` (comparison tables + gold/blue theme render correctly, mobile
  horizontal scroll on the table works as intended), `/affiliate/` (full
  page including the mock dashboard preview and FAQ, zero console errors),
  `/creators/` (honest empty-state gallery), `/pricing/` (all 4 tiers with
  correct current prices), a real blog post (markdown-rendered content,
  correct date formatting), `/streamers/` (meta-refresh redirect confirmed
  to fire live in-browser), homepage (nav dropdown shows the newly added
  Compare/Creators/Blog links). Zero console errors observed on any checked
  page.

**Still not exercised** (unchanged from the prior entry, genuinely out of
this pass's scope): deployment to a real Cloudflare Pages edge — the
generated `_headers` file's behaviour is verified against Cloudflare's
documented semantics and the local test suite, not against production
Cloudflare infrastructure.

### Prod-readiness audit remediation — 2026-08-17

A page-by-page, component-by-component review of all 27 built routes and 7
shared components (two independent inventory passes, one per product-page
cluster and one per secondary/support/legal cluster) was run against five
design/UX critique lenses and benchmarked against five live competitor
sites (Ko-fi, Streamlabs, StreamElements, Buy Me a Coffee, Fourthwall,
visited 2026-08-16). The full report is a local file, not checked into
either repository. Findings that were plumbing/structure, not new public
claims, were fixed and pushed directly to `bharatstudio-marketing` `master`
at commit `34ae1ff` (owner explicitly authorised skipping the per-fix
approval pause after the scope was surfaced):

- `/pricing` plan-selection CTAs previously all pointed at the same
  `/download` URL with no state carried forward — every tier click lost
  the visitor's choice. `/download` now reads a `?plan=` query param
  (added by `/pricing`'s CTAs) and reflects it back before the visitor
  continues into Alerts.
- `/download`'s Alerts-web and Android cards both used an identical bare
  "A" icon-box glyph — the only visual differentiator on that page. Android
  now uses a distinct glyph, and its "coming soon" copy tense now matches
  the iOS card's (both correctly future-tense, not implying the surface is
  already live).
- `/legal/data-rights` was a complete, correct page with zero inbound links
  from anywhere on the site (repo-wide grep confirmed). Now linked from
  `/support`'s "Data concern" card, the `/legal` hub, and the sitewide
  footer.
- `/setup` — the page every "get started" CTA on the site ultimately routes
  a visitor through — had zero outbound calls to action in its own body.
  Added a closing "Open Alerts" / "Contact support" pair.
- `/features`'s hero had no CTA at all, the only hero on the site with
  none. Added "See pricing" / "Compare plans".
- `/compare` and `/status` previously opened with bespoke intro markup
  instead of the shared `page-hero` wrapper every other page uses,
  producing a visibly different vertical rhythm and a smaller H1 on
  `/status`. Both now use the shared wrapper.
- `CommissionCalculator` (used on `/compare`) was hardcoded to the Pro
  plan's ₹199 fee with no way to change it — a visitor considering
  Creator/Studio saw a savings estimate that wasn't theirs. Added a plan
  selector (Pro/Creator/Studio) using the already-approved `/pricing`
  figures; no new prices introduced.
- The `⚠` warn-state cell in `CompareTable`'s Section B previously carried
  meaning through color alone (an amber icon with only an `aria-label` for
  screen readers). Added a visible "Caution" text label in the cell itself.
- Consolidated the comparison-table pattern that existed as two separate
  implementations (`CompareTable` on `/compare`, a bespoke inline table on
  `/pricing`): added `MultiCompareTable` to `components/CompareTable.tsx`
  alongside the existing `CompareTable` (unchanged, zero regression risk to
  `/compare`'s three existing tables) and switched `/pricing` to use it.
  Output confirmed byte-identical to the original inline table.

**One item in this pass touches L08-02/L08-04 directly and does not close
either gate.** `/apps/alerts` and `/features` previously never mentioned
the AI-voice/11-Indian-languages, Lottie-animation, 4-built-in-themes or
72-hour-buffer claims, despite being the pages whose job is to describe the
Alerts feature set — those claims existed only on `/compare`, itself
legacy-ported content with hedged/pending-review language per the prior
migration entry above. The owner explicitly authorised propagating the
same, unchanged wording onto `/apps/alerts` and `/features` after this
scope concern was raised in chat. **This does not constitute the L08-02
pricing-copy-vs-authority review or the L08-04 feature-claims legal/CA
review — both remain `not run`.** It only removes an inconsistency between
pages that were describing the same product differently; the underlying
claims carry the same pending-review status they already had on `/compare`.
`D-C053` (no competitor names in rendered HTML) was preserved throughout —
no page gained a named-competitor reference.

**Real evidence, this pass:**

- `tsc --noEmit` clean after every edit.
- `npm run build` succeeds: 31/31 static routes prerender, CSP header
  generator reports 32 route-specific blocks (64 inline-script hashes),
  unchanged from before this pass.
- `tests/site.test.mjs` — all 8 tests pass, including internal-link
  resolution (confirms the new `/legal/data-rights` links and the
  `?plan=` query-param CTAs resolve) and the `/creators` honest-empty-state
  test (unaffected by this pass).
- Every change spot-checked live in a local browser: screenshots and DOM
  queries confirmed the plan-forwarding banner renders correctly for a
  `?plan=studio` link, the icon collision is resolved, the shared
  `page-hero` wrapper renders identically to sibling pages, the warn-label
  text renders next to (not instead of) the icon, the `CommissionCalculator`
  plan selector recomputes the total correctly on change, and the
  `/pricing` table swap to `MultiCompareTable` produces identical visible
  output to the original inline table.
- Commit `34ae1ff` on `bharatstudio-marketing` `master` (pushed directly,
  fast-forward, no merge commit — branch `marketing-audit-fixes-2026-08-16`
  was created, reviewed, and merged into `master` before push per the
  owner's explicit instruction).

**Still open, unchanged by this pass:** everything L08-02 through L08-05
already listed as `not run` — dated legal/CA/provider review of the
pricing and feature claims, SEO/accessibility scans, and the icon-box
rollout was intentionally scoped down (see prior conversation record) to
avoid inventing semantically-unbacked glyphs across every remaining grid
on the site; the ones added this pass reuse the alerts page's own
established glyph set where a real semantic match existed.
