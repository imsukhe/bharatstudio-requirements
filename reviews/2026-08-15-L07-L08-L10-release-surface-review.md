# Conditional review — L07 Companion, L08 public launch surface, L10 release

**Date:** 2026-08-15
**Reviewer:** Codex implementation review
**Status:** `Conditional — no independent approval claimed`
**Scope:** Task definitions and acceptance records for L07, L08 and L10.
**Master authority:** [`../active/launch/01_MASTER_RELEASE_AUTHORITY.md`](../active/launch/01_MASTER_RELEASE_AUTHORITY.md)

## Findings

| ID | Finding | Severity | Disposition |
|---|---|---:|---|
| R-01 | L07 now has an explicit React Native decision, iOS/Android floor decision point, native desktop split, entitlement-safety rules, multi-channel selection behavior and device/store acceptance cases. Mobile scaffold/shell/client checks pass, and a provisional macOS SwiftUI shell passes `swift test`; Windows remains unbuilt without a Windows toolchain. | Medium | RN 0.87.0/CLI 20.2.0, exact Node floor, and a narrowly patched Metro parser are locally verified. The registry still reports eight high findings because `image-size@2.0.2` has no published fixed version; the patch is mitigation only. Real auth/API integration, native signing, store/device evidence and final macOS floor remain pending. |
| R-02 | L08 separates early content/legal/provider/support work from final release sign-off and now has test cases for public claims, pricing, support, legal/provider review, SEO/privacy and rollback. | High | Release remains blocked until dated external/legal/provider evidence exists. |
| R-03 | L10 now has an evidence-based release record covering provider, infrastructure, native releases, rehearsal, independent review and go/no-go. | High | Release remains blocked; no document-only readiness claim is permitted. |
| R-04 | No test record in this review substitutes for staging, app-store, provider, legal or capacity evidence. | High | Preserved as explicit non-negotiable rule. |
| R-05 | The launch authority referred to existing approved grandfathering rules, but no active grandfathering decision was present in the requirements tree. | High | Corrected the authority to make grandfathering an explicit pre-launch decision and copy/versioning gate; no pricing implementation may infer treatment for existing subscribers. |
| R-06 | The public support page referenced a future support runbook, but support intake, internal response targets, escalation/data-redaction rules and external evidence ownership were not held in one canonical register. | High | Added `active/launch/05_SUPPORT_AND_EXTERNAL_EVIDENCE_REGISTER.md`. It is proposed/internal, leaves legal/provider rows open, and blocks public launch until owners, evidence and rehearsal are recorded. |

## Decision status

- L07: `Proposed / mobile and macOS scaffold slices implemented; product integration and release evidence pending`.
- L08: `Proposed / content and external review not started`.
- L10: `Blocked pending L00–L09 evidence`.

## Required follow-up

1. Owner confirms React Native patch/OS floors, package identifiers and release-account ownership.
2. Marketing/support/legal owners are assigned and provider/CA/legal applications are opened early.
3. L09 staging targets and L10 evidence owners are recorded before any production-readiness claim.
4. Obtain an independent review before changing any of these tasks to `Approved` or `Verified`.
5. Resolve or formally risk-accept the remaining mobile `image-size`/Metro dependency advisory before release. The local `patch-package` mitigation is validated on a clean install with 2/2 dependency checks, 23/23 mobile tests, lint, TypeScript and React Native config checks; it does not clear the registry advisory. Do not apply the audit tool's forced React Native 0.72 downgrade blindly.
6. Approve and version the grandfathering rule before publishing paid pricing or checkout/refund copy.

## Fresh L07 local audit — 2026-08-15

The Companion web/API implementation, React Native client, macOS SwiftUI
scaffold, Windows implementation contract, server-owned control-session
lease, role/RLS guards and acceptance matrix were rechecked together. No new
locally verifiable L07 defect was found.

The review does not elevate L07 beyond its existing conditional state. Native
pairing/OBS authentication, secure platform credential storage, device and
offline/reconnect testing, Windows build/signing, macOS signing/notarisation,
iOS/Android store evidence, accessibility/privacy review and the unresolved
mobile dependency advisory still require evidence. The Companion surface must
remain independently disableable and must never be used as a prerequisite for
payment receipt, durable alert ingestion or delivery.

The mobile transport boundary was then hardened locally: `CompanionApi` now
aborts requests after a bounded default timeout and maps transport or malformed
response failures to `request_failed` without forwarding raw details. Mobile
tests pass 23/23, dependency-hardening checks pass 2/2, lint/typecheck and
React Native config checks pass. This does not change the release disposition;
device offline/reconnect/crash, native helper and store evidence remain open.

## Fresh mobile response-contract hardening — 2026-08-15

The mobile Companion API decoder was tightened to match the OpenAPI v1
response shapes rather than accepting merely type-compatible values. It now
requires UUID identifiers, rejects unknown fields at each decoded envelope and
slot, enforces the documented queue/name/page bounds, rejects duplicate or
out-of-range layout slots, validates UUID action targets/event IDs, and returns
new typed projections instead of forwarding untrusted response objects.

Local evidence: mobile Jest 23/23, ESLint, TypeScript, dependency-hardening
2/2 and React Native config checks pass. This is client-boundary evidence only;
it does not close authenticated device, offline/reconnect/crash, native
pairing/OBS, Windows, signing/store or deployed API evidence.

## Fresh L08 local audit — 2026-08-15

The BharatStudio parent site, Alerts/Companion public pages, pricing/legal and
support copy, static-site tests and support/external-evidence register were
rechecked. No new locally verifiable L08 defect was found. The local site
checks pass 5/5 and the public surface remains limited to approved v1
positioning and planning prices without provider secrets or Phase-2 claims.

L08 remains conditional/open for dated legal and tax/provider evidence, final
privacy/terms/refund/retention publication, support ownership and incident
rehearsal, domain/HTTPS/mailbox proof, deployed analytics-consent and
SEO/accessibility scans, and publish/rollback evidence. A static content pass
does not approve the money flow or legal wording.

## Fresh L10 reconciliation — 2026-08-15

The L10 authority and acceptance record were rechecked against the current
L00–L09 task/test/review records and active repositories. The full-product
launch decision is explicit and unchanged: one public v1 launch for Alerts plus
bundled Companion; YouTube and Enterprise are Phase 2; no disabled schedule or
local test can be read as production readiness.

No additional locally verifiable L10 inconsistency was found. L10 remains
blocked by the approved master authority's gates: provider approval and
creator-direct payment evidence, final infrastructure/IAM/capacity/failure
proof, native/device/store distribution, legal/privacy/support publication and
rehearsal, the approved visual runtime catalogue completion, and independent
release review.

## Windows project-boundary update — 2026-08-15

The Windows Companion directory now contains the approved WinUI 3/C#/XAML
project boundary, an inactive/unpaired shell, an `asInvoker` manifest and a
fail-closed lease/command/redaction policy core. The implementation deliberately
does not add OBS networking, credential persistence, pairing transport, public
listeners, arbitrary local commands or support upload.

This is a local source-boundary improvement, not Windows release evidence. The
current workspace lacks the Windows SDK/.NET toolchain and final package assets;
Windows compilation, MSIX packaging, Credential Manager/DPAPI integration,
signing, pairing, OBS authentication and device/security verification remain
open L07/L10 gates. Independent review was not performed in this pass.
