# Alerts + Companion launch-readiness inventory

**Status:** `No-go for public production launch — inventory, not a review record`  
**Date:** 2026-09-18  
**Owner:** Sukhdev Singh  
**Scope:** BharatStudio Alerts, dashboard, browser-source overlays/Master Canvas, Live Support Hub, Companion web console and iOS/Android Companion. The native desktop helper is considered only as a mobile-OBS-control dependency, not as a separate product surface.

## Authority and method

This is a read-only readiness inventory. It applies the controlling authority in this
order:

1. `active/launch/00_LAUNCH_SCOPE_AUTHORITY.md`;
2. `active/launch/01_MASTER_RELEASE_AUTHORITY.md`;
3. `active/launch/05_SUPPORT_AND_EXTERNAL_EVIDENCE_REGISTER.md`; and
4. `FULL-PRODUCT-DEFINITION.md` only for product detail not contradicted above.

Every §31 product requirement was included. The complete row-level inventory remains
[`TRACEABILITY.md`](../../TRACEABILITY.md), rather than being copied into this file and
mistaken for task/test/review evidence. The status letters below have their authority
meaning: `U` usable, `P` partial, `X` built but unreachable, `A` absent, `B` blocked,
and `N` intentionally never built.

Evidence inspected: all active launch authorities, active tasks, L00–L25 task and
acceptance records, reviews, the generated traceability index, the current source
revisions and related Desktop material. Desktop files were treated as historical
reference only: they do not override current authorities or current source evidence.

## Decision today

**Do not launch.** Core local implementation exists, but the product is neither
feature-complete nor externally evidenced. Of 550 v1 rows, only 92 are marked usable;
49 are partial, 22 are unreachable, 372 are absent and 12 are blocked. Every provider,
legal, infrastructure, store, device, staging, recovery and independent-review gate is
still open.

| Surface | Local-code confidence | Production-launch confidence | Reason |
|---|---|---|---|
| Direct tip → ledger → alert | High | **No-go** | Deterministic paths are tested, but Razorpay approval/sandbox/live, tax/legal, IAM and production rehearsal are absent. |
| Creator dashboard and standalone overlay | Medium–high | **No-go** | Local tests cover selected paths; browser/OBS, accessibility, capacity and cross-replica evidence are absent. |
| Master Canvas | Medium in isolation | **No-go** | Runtime exists but creators cannot obtain its browser-source URL; no OBS proof. |
| TTS | Medium | **No-go** | Provider runtime and P0 shared-safety enforcement are not proven/completed. |
| Companion mobile | Medium for TypeScript/unit behavior | **No-go** | No signed native/device/store proof; substantial live-ops workflows are absent. |
| Desktop helper | Medium macOS source / limited portable Windows logic | **No-go** | No current device/OBS proof; WinUI has not been built on Windows; no signing/notarisation. |
| Media, creator assets, templates | Low | **No-go** | GCS/CDN/signed URLs, scan/quarantine/takedown and 359 runtime packages are missing. |
| Release operations | Low | **No-go** | No staging/measurement environment, deployment, incident drill, restore/rollback proof or support operation. |

“High” means repeatable deterministic local proof only. It never means production,
provider, browser/OBS, device, legal, security-review or release proof.

## Current source and local verification

| Repository / evidence | Current result | Limit |
|---|---|---|
| Alerts `7e1de17` | The recorded `pnpm verify:local` passed: OpenAPI/fixtures, migrations `0001–0164`, role-separated SQL proof, API/web tests and builds, load/fault self-tests, Go `-race`/`vet`, and three image builds. | No real provider, deployment, managed PostgreSQL, browser/OBS or independent review. |
| Requirements `856a185` | `TRACEABILITY.md` and `tools/doc_consistency.py` were clean at the latest remediation evidence record. | Traceability is a mapping aid, not proof that mapped features are complete. |
| Companion mobile `54f3e2d` | Fresh in this inventory: typecheck, lint, 13 Jest suites/109 tests and 2 dependency-hardening tests passed. | No iOS/Android signed build, physical-device, push-provider or store evidence. |
| Desktop helper `68452fb` | macOS Swift package and Windows project source exist; portable Windows smoke source exists. | Windows project requires a Windows SDK/WinUI build agent; macOS signing/notarisation/device/OBS evidence is absent. |

## Task-track disposition

The L-tracks are broad implementation bundles rather than a one-to-one measure of
user-flow completion. This table prevents an old “L-track done” label from masking an
open §31 flow; the detailed state in the matrix below remains controlling.

| Track | Scope today | Evidence classification / pending work |
|---|---|---|
| L00 | Legacy inventory/freeze | Proposed/local inventory; final authority reconciliation remains. |
| L01 | Contracts/database baseline | Local evidence available; independent security and deployed-database proof absent. |
| L02 | RLS/archive/retention | Isolated PostgreSQL proof conditionally passes; deployment roles/secrets and independent review absent. |
| L03 | Alerts web and Creator API | Local implementation slices pass; browser/accessibility, provider, cross-replica and staging remain. |
| L04 | Go payment boundary | Local persistence/provider-contract slices pass; Razorpay approval, sandbox/live and deployed IAM/staging remain. |
| L05 | Worker/Cloud Tasks | Local routing/lease/pump slices pass; real Cloud Tasks, cross-replica overlay, capacity and fault rehearsal remain. |
| L06 | Scheduler | Local disabled-template/operations contract passes; deployed OIDC/IAM, recovery and monitoring rehearsal remain. |
| L07 | Companion web/mobile/helper | Source scaffolds and selected local suites pass; native security, Windows, signing, stores, devices and audit remediation remain. |
| L08 | Marketing/support/legal | Static surfaces pass; legal approval, hosting, support operation and public-copy evidence remain. |
| L09 | Observability/load/failure | Local instrumentation/self-tests pass; deployed dashboards, declared capacity targets and fault proof remain. |
| L10 | Release readiness | **Blocked** by all L00–L09 evidence plus external gates. |
| L14 | Viewer identity/privacy/history | Multiple local slices exist, but attribution, claims, rights, reputation and deletion/export remain in the §31 gaps. |
| L15 | YouTube connectors/chat | Local code may exist, but the launch amendment makes Google OAuth verification and quota v1 release blockers; do not claim provider readiness. |
| L16 | Interactions/widgets | Several reads and widgets exist; viewer/creator interaction, paid-vote, automation and reachability work remain. |
| L17 | Paid challenges | Base local slice exists; disputes, evidence, viewer proposal and refundable multi-contributor design are incomplete/blocked. |
| L18 | Memberships | Blocked until a supported recurring-payment capability exists. |
| L19 | Provider abstraction | Partial: capability abstraction is not a complete live money-moving multi-rail path; alternatives are not authorised v1 direct rails. |
| L20 | Alert Studio depth | Partial/mostly absent under media, template, storage and customisation rows. |
| L21 | Enterprise workspace | Explicitly out of v1 and externally/commercially blocked. |
| L22 | Stickers/safe media | Curated catalogue work exists; safe bytes, picker, storage and takedown posture remain incomplete. |
| L23 | AI assist | Not a v1 launch dependency; bounded AI/credits safety and provider/cost work remain unscheduled/post-v1. |
| L24 | Companion action catalogue | Foundation exists; the full mobile creator cockpit and device evidence remain open. |
| L25 | Supporter reputation | Some logic may exist; policy, producers, viewer/creator surfaces and privacy/appeal evidence remain incomplete. |

## What is built and locally exercised

These paths must be preserved, but none may be marketed as production-ready.

| Flow | Current locally evidenced scope | Principal remaining gate |
|---|---|---|
| Payments | `PAY-01`–`PAY-11`, `PAY-22`–`PAY-25`, `QR-09`, `QR-11`: order/idempotency/expiry, HMAC/dedup contract, append-only payment/refund evidence, receipt projection, alert consent, ledger/export and subscription code. `AUD-PAY-01/02` recently repaired Turnstile hand-off and retry-safe TipIntent checkout. | Razorpay exact-flow approval, sandbox/live webhooks/refunds/reconciliation, tax/legal and deployed browser proof. |
| Delivery | `ALQ-01`–`ALQ-03`, `ALQ-05`–`ALQ-14`: durable outbox/per-queue delivery, replay/ack, role-scoped reads, queue modes, token revoke/rotation and standalone overlay mechanics. | Direct database listener configuration, cross-replica/OBS/network-loss/capacity proof. |
| TTS base | `TTS-01`–`TTS-05`: synthesis/cache, metering, character ladder, fallback and visual-delivery isolation. | `TTS-06` and `TTS-16` safety pipeline is P0 absent; no provider/deployed rehearsal. |
| Viewer essentials | `VID-04`, `VID-08`–`VID-10`: receipt privacy token, opt-in profiles/search, bounded relation/session/reset behavior. | Attribution, claiming, export/deletion, reputation, safety and legal gates. |
| Engagement base | `ENG-03`–`ENG-06`, `ENG-08`, `CHL-01/02`: goal arithmetic, core widget reads, privacy-safe leaderboard, fragment-token overlay protocol and base challenge state. | Viewer interaction, automation/trigger, paid-vote and creator-control legs remain open. |
| Curated-media boundary | `MED-01`–`MED-03`, `MED-07/08`, `MED-11/12`: curated-ID-only selection, server validation, raw-template rejection and render limit. | No safely served creator media, picker/catalogue UI, scanning or storage runtime. |
| Companion foundation | `CMP-01`–`CMP-06`, `CMP-08`, `CMP-26`: server-owned lease/layout/action model, pairing, macOS helper implementation and mobile handler-wiring coverage. | No signed/device/store proof and a large missing Live Deck/operations surface. |
| Recent corrective work | `AUD-MC-01`, `AUD-OVL-01`, `AUD-PAY-01`, `AUD-PAY-02`, `AUD-RT-03`, `AUD-SB-01`: local regressions and hostile self-review recorded. | All are conditionally complete/self-reviewed; independent, browser/OBS, provider and deployed-runtime evidence remains open. |

## High-impact issues by category

| Type | Open issue / scope | Effect |
|---|---|---|
| Reachability | `ALQ-18` Master Canvas composes roughly 17 modules but no creator product surface generates its `/overlay/canvas/...` URL. | The “one source” promise is unshippable. |
| Money operations | `PAY-12`–`PAY-21`, `QR-01`–`QR-14` are partial/absent/unreachable: provider activation/OAuth, scheduled reconciliation/refund sweep, manual quarantine, three QR types, return path and payout visibility. | Happy-path payment code cannot safely operate a public money product. |
| Safety / privacy | `TTS-06`, `TTS-16`, broad `SAF-*` enforcement, viewer rights and legal deletion/export work remain absent or blocked. | No safe production posture for speech, uploads, moderation, rights or appeals. |
| Storage / media | `STO-01`–`STO-05`, `MED-04`–`MED-21`: GCS/CDN/signed URL system, quarantine/scan/takedown, viewer picker and runtime packages are missing. | Custom audio/media and most template promise cannot work safely. |
| Companion | `CMP-12+`: Prepare Stream, full per-hop test, health/degraded states, Clutch Mode, queue controls, money, notifications, diagnostics, localisation/accessibility and offline recovery are incomplete. | A mobile UI is not yet a dependable creator cockpit. |
| Lifecycle / performance / operations | `LIF-*`, remaining `ENT-*`, `OPS-*`, `RT-*`, `PRF-*` and environment lanes are incomplete. | No evidence-backed lapse behavior, capacity boundary, restore/rollback or incident operation. |
| Evidence integrity | `CMP-07` remains `X` in the register while current mobile source has handler wiring with a regression guard. Historical Desktop reports also predate recent fixes. | Do not auto-promote: reconcile through a device E2E task/review first. |
| Template catalogue | Active template authority records 241 complete packages and 359 missing; raw HTML cannot be imported as runtime package code. | Catalogue is incomplete and needs approved declarative-package authoring. |

## External actions and credentials required

| Required action/evidence | Affected flows |
|---|---|
| Razorpay Technology Partner / creator-direct written approval plus enabled sandbox and live exact-flow accounts | Payments, refunds, account activation, subscriptions and public launch. |
| File and receive Google OAuth verification plus YouTube Data API quota | YouTube amendment work; both are expressly unfiled v1 launch blockers. |
| Dated CA/legal/privacy approval for terms, DPDP, retention, refunds, grievance, tax/GST/TDS and viewer rights | Public payment, accounts, marketing, media and app-store posture. |
| Cloudflare Turnstile site key paired with API secret, then real-browser checkout proof | Public checkout abuse defence. |
| Cloud Run/managed database/IAM/secrets/domain/WAF/backup/rollback design and configuration | Every service runtime. |
| Safe non-production measurement/staging environment with synthetic data, OBS/device harnesses, network shaping, load/fault and restore proof | Reliability and performance claims. |
| Apple/Google accounts, signing/declarations/review; Windows build agent; macOS signing/notarisation | Companion distribution. |
| Support case tooling, staffing/escalation/redaction and incident rehearsal | Operationally safe public launch. |
| Independent application/security review | All conditionally complete self-reviewed work. |

## Exhaustive §31 flow matrix

Every row in the product register belongs to one of the following sections; the table
accounts for all **783** requirements by current state. The exact IDs, item scope,
phase, task, acceptance record and review links are in `TRACEABILITY.md`.

| Register flow group | U | P | X | A | B | N | Launch interpretation |
|---|---:|---:|---:|---:|---:|---:|---|
| Payments and money (§31.2) | 17 | 6 | 5 | 13 | 2 | 2 | Strongest local core; still provider and operations blocked. |
| Alerts, queues, overlay (§31.3) | 12 | 2 | 1 | 4 | 0 | 0 | Durable baseline exists; Canvas and recovery/measurement gaps remain. |
| TTS (§31.4) | 5 | 1 | 0 | 11 | 0 | 0 | Base code exists; safety and quota experience do not. |
| Viewer identity/history/trust (§31.5) | 4 | 1 | 4 | 11 | 2 | 0 | Receipt/profile pieces exist; rights/trust identity system incomplete. |
| Engagement/widgets/challenges (§31.6) | 8 | 4 | 3 | 16 | 1 | 0 | Basic goals/widgets exist; interaction/automation incomplete. |
| Stickers/media/Alert Studio (§31.7) | 7 | 3 | 3 | 14 | 0 | 0 | Curated boundary only; media runtime absent. |
| Companion (§31.8) | 11 | 6 | 1 | 74 | 4 | 0 | Foundation exists; creator-cockpit launch scope mostly unbuilt. |
| Connectors and chat (§31.9) | 7 | 0 | 2 | 28 | 3 | 1 | Controlling YouTube amendment and external approval apply. |
| Entitlements, billing, admin and ops (§31.10) | 17 | 3 | 4 | 7 | 2 | 0 | Some controls exist; full admin/lifecycle/ops evidence absent. |
| Marketing, legal and support (§31.11) | 5 | 0 | 0 | 3 | 1 | 0 | Static work exists; legal/support launch evidence open. |
| Live Support Hub (§31.13) | 2 | 5 | 1 | 106 | 0 | 2 | Largest unbuilt public-surface body. |
| Customisation and gating (§31.14) | 0 | 3 | 0 | 3 | 0 | 0 | Registry and tier-depth implementation is incomplete. |
| Lobby Engine (§31.15) | 0 | 0 | 0 | 22 | 0 | 1 | Post-v1/P3, not launch-ready. |
| Giveaways/tournaments (§31.16) | 0 | 0 | 0 | 14 | 0 | 0 | Post-v1/P3, not launch-ready. |
| Custom audio and creator media (§31.17) | 0 | 0 | 0 | 10 | 0 | 1 | Storage and safety prerequisites absent. |
| Performance (§31.18) | 5 | 11 | 0 | 22 | 0 | 1 | Local self-tests are not performance evidence. |
| Control plane/admin (§31.19) | 0 | 0 | 0 | 24 | 0 | 0 | Recent source slices require register reconciliation and independent review. |
| New widgets (§31.20) | 0 | 0 | 0 | 7 | 0 | 0 | No release claim without full user routes. |
| Co-Stream Room (§31.21) | 0 | 0 | 0 | 14 | 0 | 1 | Post-v1/P3, not launch-ready. |
| Sound Moments/rules (§31.22) | 0 | 3 | 0 | 42 | 0 | 0 | Media/runtime prerequisites prevent a public claim. |
| Payment routing (§31.24) | 0 | 0 | 0 | 11 | 4 | 2 | Research-only; never substitute for direct Razorpay. |
| Subscription lifecycle (§31.25) | 0 | 1 | 0 | 9 | 0 | 0 | Incomplete lapse behavior is a launch risk. |
| Social Relay (§31.26) | 0 | 0 | 0 | 15 | 0 | 2 | P3/post-v1; do not market. |
| Packs and creator ops (§31.27) | 0 | 0 | 0 | 24 | 0 | 2 | P3/post-v1; do not market. |
| Interop, packages and bridges (§31.28) | 0 | 0 | 0 | 17 | 2 | 1 | P2/research only; do not build or claim bridges now. |
| Customisation depth by tier (§31.29) | 0 | 0 | 0 | 30 | 0 | 0 | P2 depth work is entirely absent. |
| BharatStudio Bot (§31.30) | 0 | 0 | 0 | 15 | 1 | 1 | P2 and gated on chat-write scope. |
| Storage/media platform (§31.31) | 0 | 0 | 0 | 5 | 0 | 0 | P0 storage work is absent. |

The summary table intentionally does not promote a count to a release status. The
authoritative per-flow row in `TRACEABILITY.md` is the required lookup for any task
selection, acceptance status, owner, phase or evidence claim.

## Required sequence before reconsidering launch

1. Finish the P0 functional flows in active-authority order: control/capability plane,
   safety, payment recovery/activation, Canvas reachability, storage/media safety,
   Companion critical live-deck behavior and lifecycle behavior.
2. Reconcile source/register discrepancies using authority → task → acceptance → review;
   never promote a state from a passing unit suite.
3. Build the safe measurement environment and run genuine cross-service, device, OBS,
   network-loss, rollback/restore and capacity rehearsals.
4. Obtain all provider, legal/CA/privacy, infrastructure, store, support and independent
   review evidence and attach it to the external-evidence register.
5. Run L10’s release rehearsal and go/no-go criteria. Until then the correct public
   status is unreleased.
