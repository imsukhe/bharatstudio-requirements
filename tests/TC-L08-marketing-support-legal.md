# L08 acceptance and test record — marketing, support, legal and launch communications

**Status:** `Static parent/product surface locally implemented — content, operations and external evidence pending`
**Task:** [`../tasks/L08-marketing-support-legal.md`](../tasks/L08-marketing-support-legal.md)
**Repositories:**
- `/Users/sukhdevsingh/Workspace/Bharat Studio/bharatstudio-marketing`
- `/Users/sukhdevsingh/Workspace/Bharat Studio/bharatstudio-requirements`

| ID | Setup/action | Expected result | Evidence |
|---|---|---|---|
| L08-01 | Crawl BharatStudio home, Alerts, Companion, pricing, support and legal pages | Parent brand and product pages are distinct; no internal architecture, secrets, unavailable YouTube/Enterprise claims or unsupported free-forever claims appear | Dated crawl and content review; not run |
| L08-02 | Compare pricing, annual renewal, cancellation, grandfathering, refund and retention copy with the approved authority | All public wording matches the current versioned decision; historical versions retain effective dates | Copy diff and approval record; not run |
| L08-03 | Submit support, refund, account closure, security concern and incident-contact requests | Each route has an owner, acknowledgement, triage, escalation and audit path | Support drill and runbook evidence; not run |
| L08-04 | Review payment, privacy, DPDP, GST/TDS/KYC, international-payment, Razorpay connected-account and app-store claims | CA/legal/provider findings are written, owned and either resolved or block release | Legal/provider register; not run |
| L08-05 | Run SEO, accessibility, robots, sitemap, structured-data, analytics-consent and public-secret scans | Search/indexing and accessibility checks pass; analytics are privacy-safe; no credentials or private routes are exposed | Dated scan outputs; not run |
| L08-06 | Publish and roll back a versioned policy/content change | Effective date, approval, rollback and historical copy remain auditable; no silent replacement occurs | Publish/rollback rehearsal; not run |
| L08-07 | Run the local static-site checks against the parent, Alerts, Companion, pricing, support and legal index pages | Pages have bounded metadata/navigation, discovery files are present, and no private/payment/Phase-2 terms are exposed in public HTML | `bharatstudio-marketing/public/`, `bharatstudio-marketing/tests/site.test.mjs`; `npm test` (5/5); pass locally on 2026-08-15 |
| L08-08 | Review the support/external-evidence register before public launch | One canonical register defines safe intake, internal triage, escalation, redaction, owner/evidence status and release gates; it makes no unsupported legal/provider approval claim and does not publish internal support targets as contractual SLAs | `active/launch/05_SUPPORT_AND_EXTERNAL_EVIDENCE_REGISTER.md`; document review; local pass, external/legal/provider/support rehearsal pending |
| L08-09 | Resolve every internal absolute link published by the six static pages | Each `/`-rooted navigation link resolves to a checked-in page or stylesheet; a missing product page cannot pass the local marketing gate | `bharatstudio-marketing/tests/site.test.mjs`; `npm test` (5/5), including the internal-link resolution test; pass locally on 2026-08-15 |
| L08-10 | Inspect the static-host security boundary and vulnerability contact | Cloudflare-compatible headers deny scripts, outbound connections, framing and unnecessary browser permissions; `security.txt` provides a dated contact and canonical URL without exposing secrets or private routes | `bharatstudio-marketing/public/_headers`, `public/.well-known/security.txt`, `tests/site.test.mjs`; local static-site test; pass locally on 2026-08-15 |

## Release blockers

- Razorpay/provider approval and tax/legal review must be affirmative and current.
- Support/on-call ownership and public policy versions must exist before public launch.

### Fresh local audit evidence — 2026-08-15

The checked-in public parent/product pages and launch register were re-read
against the L08 objective and public-boundary rules. No additional local
failure was found. `bharatstudio-marketing` `npm test` passes 5/5, including
metadata/navigation, internal-link resolution, discovery-file presence and
public-secret/Phase-2 term checks.

This does not satisfy the remaining release evidence: professional
legal/provider review, policy effective dates and historical publication,
support case/incident rehearsal, domain/SSL/email deployment, analytics consent,
accessibility/SEO crawl and rollback proof.

### Automatic continuation rerun — 2026-08-15

`bharatstudio-marketing` `npm test` passed 5/5. The local static surface and
security-boundary checks remain green; no public content, provider credential,
private route or Phase-2 feature claim was introduced. External legal/provider,
support, domain/HTTPS/email, analytics-consent, SEO/accessibility and rollback
evidence remain open.

### Marketing migration verification — 2026-08-16

| ID | Setup/action | Expected result | Evidence |
|---|---|---|---|
| L08-11 | Run `npm test` after the parent/product migration | All static checks pass against the full published route set | `bharatstudio-marketing/tests/site.test.mjs`; 5/5 passed locally on 2026-08-16 |
| L08-12 | Crawl the 21 checked-in HTML routes for metadata, stylesheet and brand identity | Every published page has a title, description, stylesheet and BharatStudio identity | `bharatstudio-marketing/public/`; local test pass on 2026-08-16 |
| L08-13 | Resolve every root-relative link from the 21 routes | No published internal navigation link points to a missing checked-in target | `tests/site.test.mjs` internal-link test; pass locally on 2026-08-16 |
| L08-14 | Inspect the migrated homepage in a local browser preview | Parent brand is visually distinct from Alerts and Companion; dark creator-focused visual system is preserved; dropdown navigation is present | Local browser DOM/screenshot review of `/` on 2026-08-16 |
| L08-15 | Inspect the download and boundary copy | No unconfirmed product hostname, provider secret, internal architecture or unavailable integration is published | `public/download/index.html`, `public/features/index.html`; local content scan pass on 2026-08-16 |
| L08-16 | Compare discovery files with the route set | Sitemap includes all published public routes and robots points to it | `public/robots.txt`, `public/sitemap.xml`; local test pass on 2026-08-16 |

### Prod-readiness audit remediation — 2026-08-17

| ID | Setup/action | Expected result | Evidence |
|---|---|---|---|
| L08-17 | Run the full local verification chain (`tsc --noEmit`, `npm run build`, `npm test`) after the audit-remediation edit set | Type-check clean, all 31 static routes prerender with CSP headers regenerated, all site tests pass | `tsc --noEmit` clean; `npm run build` 31/31 routes, 32 CSP blocks; `tests/site.test.mjs` 8/8 pass locally on 2026-08-17 |
| L08-18 | Confirm the new internal links (`/legal/data-rights` from `/support`, `/legal`, and the footer; `?plan=` query-param CTAs from `/pricing` to `/download`) resolve | No new broken internal link is introduced | `tests/site.test.mjs` internal-link resolution test; pass locally on 2026-08-17 |
| L08-19 | Browser-verify the plan-forwarding banner, icon-collision fix, shared `page-hero` adoption on `/compare`/`/status`, warn-label text, `CommissionCalculator` plan selector, and the `/pricing` → `MultiCompareTable` swap | Each renders correctly and the table swap produces output identical to the prior inline table | Local browser screenshots + DOM queries on 2026-08-17; `git diff` review of `components/CompareTable.tsx` and `app/pricing/page.tsx` |
| L08-20 | Confirm no competitor name was introduced in any rendered HTML while propagating the AI-voice/languages/Lottie/themes/buffer claims from `/compare` onto `/apps/alerts` and `/features` | `D-C053` (no competitor names) holds; wording is unchanged from the existing `/compare` copy, not a new claim | Diff review of `app/apps/alerts/page.tsx`, `app/features/page.tsx` against `app/compare/page.tsx`'s existing text on 2026-08-17 — **does not satisfy L08-02 or L08-04**, both remain `not run` |
