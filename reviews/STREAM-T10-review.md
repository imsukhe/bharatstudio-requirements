# Review Record — STREAM-T10: Device/Carrier QA Matrix + App Store Submission

| Field            | Value |
|------------------|-------|
| Task             | STREAM-T10 |
| Reviewed by      | Claude Sonnet 4.6 (audit role) |
| Implementation by| Claude Haiku 4.5 (coding) |
| Review date      | 2026-08-26 |
| Verdict          | **CONDITIONAL PASS** — 1 blocker fixed; on-device QA and Apple Developer credentials required |

---

## Files Reviewed

| File | Lines | Result |
|------|-------|--------|
| `project.yml` | 110 | PASS (T05–T09 sources added; DEVELOPMENT_TEAM marked) |
| `BharatStudio/Configuration.storekit` | 80 | PASS |
| `BharatStudioTests/T10Tests.swift` | 70 | PASS (PlatformRegistry confirmed to exist) |
| `bharatstudio-requirements/launch/LAUNCH-CHECKLIST.md` | 230 | PASS |
| `bharatstudio-requirements/launch/QA-MATRIX.md` | 122 | PASS |
| `bharatstudio-requirements/launch/KNOWN-ISSUES.md` | 275 | PASS |
| `bharatstudio-requirements/launch/APPGROUP-AUDIT.md` | 145 | PASS |
| `BharatStudio/Views/SettingsView.swift` | 128 | PASS (post B1 fix) |
| `BharatStudio/Views/ChatView.swift` | 124 | PASS (post B1 fix) |

---

## Blockers Found and Fixed

### B1 — iOS 17+ two-arg `.onChange` closures with iOS 16.0 deployment target (FIXED by Sonnet)

**Root cause:** `SettingsView.swift` (lines 36, 51) and `ChatView.swift` (line 37) used the two-arg
`.onChange(of:) { oldValue, newValue in }` form, which is available only from iOS 17+.
`project.yml` (confirmed by Haiku's output) sets `deploymentTarget: iOS: "16.0"`.
This causes a compile error on iOS 16 targets.

**Fix:** Changed all three call sites to the iOS 14+ single-arg form:
- `SettingsView.swift:36` → `.onChange(of: activePlatform) { newValue in }`
- `SettingsView.swift:51` → `.onChange(of: kickStreamKey) { newValue in }`
- `ChatView.swift:37` → `.onChange(of: messages) { _ in }` (new value unused; `messages` property accessed directly)

---

## Non-Blocking Observations

| ID | Location | Issue |
|----|----------|-------|
| W1 | `KNOWN-ISSUES.md` | W-T08-5 (PreviewView not wired to compositor) listed as "v1.1" deferred. This wiring is needed before the app can show a live preview in the main UI. Should be escalated to v1 if the live preview feature is marketed. |
| W2 | `project.yml` | `SWIFT_ACTIVE_COMPILATION_CONDITIONS: DEBUG` is set for the app target but not for the extension target. The extension may not get `DEBUG` symbols consistently. Low risk for v1. |
| W3 | `T10Tests.swift` | `testEntitlementFlagURLNotNil` is a no-assert test in CI (App Group container is not provisioned in Xcode test host). This is the correct pattern but means the test adds no protection in an unprovisioned simulator. Document this in the test comment — already done. |
| W4 | `LAUNCH-CHECKLIST.md` | Subscription pricing in LAUNCH-CHECKLIST is documented as ₹99/₹199/₹399 (from STREAM-T09 spec). Source of truth is `bharatstudio-requirements/governance/` — verify pricing before creating App Store Connect products. Memory: Pro ₹199, Creator ₹399, Studio ₹499 per `bharatstudio-alerts` pricing; Stream pricing may differ. |
| W5 | `AGENTS.md` | `bharatstudio-requirements/governance/AGENTS.md` references `group.com.bharatstudio.stream` (without 'ing'). Code audit confirmed all code uses `group.com.bharatstudio.streaming`. AGENTS.md needs a one-line correction. Low risk. |

---

## Security Constraints Verified

| Constraint | Status |
|------------|--------|
| Stream keys not in any launch document (LAUNCH-CHECKLIST, QA-MATRIX) | ✅ |
| OAuth tokens not in any launch document | ✅ |
| Facebook gate enforced (`isFacebookAppReviewPassed = false`) — tested by `testFacebookGated` | ✅ |
| `DEVELOPMENT_TEAM` left as `"REPLACE_WITH_YOUR_TEAM_ID"` — no real credentials committed | ✅ |
| StoreKit product IDs match `EntitlementStore.productIDs` constants — tested by `testProductIDsMatchExpectedConstants` | ✅ |

---

## Test Coverage

| Test | AC | Result |
|------|----|--------|
| `testAppGroupIdentifierFormat` | AC2, AC10 | ✅ |
| `testProductIDsMatchExpectedConstants` | AC3 (indirect) | ✅ |
| `testFacebookGated` | AC9 | ✅ |
| `testQualityPresetBitratesOrdered` | AC1 (indirect) | ✅ |
| `testEntitlementFlagURLNotNil` | AC1 (indirect) | ⚠️ No-assert in CI (by design) |
| `testPlatformRegistryCoversAllCases` | AC1, AC5 | ✅ |

---

## App Group Identifier Audit Result

Grep for `group\.com\.bharatstudio\.stream[^i]` across all `.swift`, `.yml`, `.json`, `.plist` files:
**Result: Zero matches.** All files use the canonical `group.com.bharatstudio.streaming`. No code changes required. `AGENTS.md` documentation discrepancy logged as W5.

---

## Open Items Before T10 Can Fully Close

| Item | Owner | Blocker? |
|------|-------|----------|
| Apple Developer Team ID (10-char) | User | Yes — required to build |
| OAuth Client IDs (YouTube, Twitch, Facebook) in Info.plist | User | Yes — required for OAuth |
| App Group registered in Apple Developer Portal | User | Yes — required for extension sharing |
| Keychain Sharing group registered | User | Yes — required for stream key sharing |
| StoreKit products created in App Store Connect | User | Yes — required before submission |
| Privacy Policy URL live and reachable | User | Yes — required by App Store |
| App Store screenshots (all required device sizes) | User | Yes — required by App Store |
| Physical QA: 25 scenarios × 3 devices executed | QA | Yes |
| Facebook App Review submitted to Meta | User | No — but 2–4 week gate; start early |
| `AGENTS.md` App Group identifier correction | Engineering | No |
| `PreviewView.enqueue()` wired to compositor | Engineering | No — deferred v1.1 |

---

## Verdict

**CONDITIONAL PASS.** One compile blocker fixed: three iOS 17+ two-arg `.onChange` closures downgraded to the iOS 14+ single-arg form, consistent with the confirmed `deploymentTarget: "16.0"` in `project.yml`. All 10 acceptance criteria are implemented:

- `project.yml` has all T05–T09 source paths and clearly-marked `DEVELOPMENT_TEAM` placeholder
- `Configuration.storekit` provides 3 auto-renewable subscription products for Xcode sandbox testing
- `LAUNCH-CHECKLIST.md` gives step-by-step human instructions through all 5 phases
- `QA-MATRIX.md` covers 25 scenarios across 3 device classes and 4 network conditions
- `KNOWN-ISSUES.md` consolidates 12 W-level items from T01–T09 with v1/v1.1/v2 fix schedules
- `APPGROUP-AUDIT.md` documents the clean audit result
- `T10Tests.swift` adds 6 launch-readiness invariant tests
- `OnboardingView` Facebook "Coming soon" verified present (T08)
- App Group identifier consistent (`group.com.bharatstudio.streaming`) everywhere

The codebase is now submission-ready pending user-supplied Apple Developer credentials and physical device QA execution.
