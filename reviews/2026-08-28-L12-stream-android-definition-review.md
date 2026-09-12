# L12 Android Streaming — Definition review

**Date:** 2026-08-28
**Reviewer:** Android lead (self-review; independent review unavailable at definition stage)
**Scope:** L12 task definition, TC-L12 acceptance criteria, scope-change reconciliation, WP-0 implementation readiness
**Status:** `Conditionally complete — independent review pending; WP-0 authorized to proceed`

---

## Review findings

### F1 — Scope change reconciliation required (RESOLVED)
**Severity:** High
**Finding:** The mission direction "login required for free users" conflicts with PLATFORM-00's locked "Free local streaming is account-free" decision.
**Disposition:** Resolved by interpretation in L12 task record: login required at app entry (UX gate); stream transport path never calls Platform; active stream must survive Platform outage via offline-grace model. Recorded as DL-6 in Doc 153.

### F2 — WP-9 is now v1, not v1.x
**Severity:** High
**Finding:** Doc 153 B8 previously flagged backend identity as "v1.x, blocks premium/backend release, not v1 streaming." The new login-required direction makes it v1.
**Disposition:** Recorded in L12 task and DL-6. WP-9 is still gated on Platform contract existence — cannot start until `bharatstudio-platform` repo and API contract exist. This is an explicit external blocker.

### F3 — Pricing not yet approved (OPEN)
**Severity:** Medium (blocks Play release, not development)
**Finding:** B1 pricing unchanged from Doc 153. Proposed ₹9d/₹19w/₹49m/₹139q/₹249h/₹499y.
**Disposition:** Open. Blocks Play Console configuration and any release exposing premium. Independent of WP-0.

### F4 — Android 17 support explicitly gated
**Severity:** Low
**Finding:** V-17 validation task exists but no physical Android 17 device is confirmed available.
**Disposition:** Correctly recorded as an external blocker in DEVICE-AND-NETWORK-MATRIX.md. No WP claims Android 17 support until V-17 passes.

### F5 — Platform API contract absent
**Severity:** High (blocks WP-9)
**Finding:** `bharatstudio-platform` repository does not exist. WP-9 requires the approved Platform API contract before implementation.
**Disposition:** Recorded as explicit external blocker in L12 task. WP-0 through WP-8 and WP-10/11 are independent of this. WP-9 and the mandatory-login UI in WP-7 may stub the Platform interface behind the `backend-contract` module while waiting.

---

## WP-0 authorization assessment

WP-0 covers: Gradle multi-module scaffold, version catalog + lockfile + SBOM, CI (lint/detekt/unit/dependency-rule/secret-scan), module-boundary rules.

This is classified L2/L3 (security baseline in CI pipeline). The scope is fully specified in Doc 153 §4.1 and §11.4. Acceptance criteria are defined in TC-L12 §WP-0. No external dependency is required. Rollback: not applicable.

**Decision: WP-0 is authorized to proceed immediately.**

---

## Open items before WP-0 can close

All TC-L12 §WP-0 criteria (0-1 through 0-10) must pass. CI pipeline must be green.

## Open items before subsequent WPs

- WP-1: Physical device available with Android 10–16 range
- WP-9: Platform API contract published + Platform staging environment available
- WP-7 (login UI): `backend-contract` module interface defined (stub acceptable)
- All B1–B8 approvals before any premium/billing feature ships

---

## Remaining work

This is a self-review only. An independent review is required before RC. Recorded as `Conditionally complete` at definition stage.
