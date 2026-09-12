# Review Record — STREAM-T07: OAuth × 4 Platforms

| Field            | Value |
|------------------|-------|
| Task             | STREAM-T07 |
| Reviewed by      | Claude Sonnet 4.6 (audit role) |
| Implementation by| Claude Haiku 4.5 (coding) |
| Review date      | 2026-08-26 |
| Verdict          | **CONDITIONAL PASS** — 1 blocker fixed; on-device OAuth flow verification required |

---

## Files Reviewed

| File | Lines | Result |
|------|-------|--------|
| `Shared/PlatformAuthState.swift` | 21 | PASS |
| `Shared/OAuthToken.swift` | 21 | PASS |
| `Shared/OAuthConfig.swift` | 102 | PASS |
| `Shared/TokenStore.swift` | 60 | PASS |
| `Shared/SharedKeychain.swift` | 126 | PASS (+48 lines: Data overloads added) |
| `BharatStudio/Auth/StreamKeyFetcher.swift` | 93 | PASS |
| `BharatStudio/Auth/OAuthManager.swift` | 212 | PASS (post-fix) |
| `BharatStudioTests/T07Tests.swift` | 134 | PASS |

---

## Blockers Found and Fixed

### B1 — `ASWebAuthenticationSession` not retained — deallocated before completion handler fires (FIXED by Sonnet)

**Root cause:** Inside `withCheckedThrowingContinuation`, the `session` variable is a local. After the closure returns (after `session.start()`), the local goes out of scope and ARC releases it. The system web sheet would be dismissed immediately with no callback.

**Manifestation:** OAuth flow appears to launch but disappears in < 1 frame with no error logged; `authenticate()` hangs or returns false immediately.

**Fix:** Added `private var activeAuthSession: ASWebAuthenticationSession?` to `OAuthManager`. Set before `session.start()`, cleared in the completion handler (both success and error paths). `activeAuthSession = nil` also added to the catch block.

```swift
// Before (broken — session released before completion):
let session = ASWebAuthenticationSession(url: ...) { url, error in ... }
session.start()

// After (correct — session retained until callback fires):
private var activeAuthSession: ASWebAuthenticationSession?
...
activeAuthSession = session   // retain before start()
session.start()
// completion: self?.activeAuthSession = nil
```

---

## Non-Blocking Observations

| ID | Location | Issue |
|----|----------|-------|
| W1 | `TokenStore` | `account` constant is `"token"` but spec suggested `"default"`. No cross-target conflict — extension reads stream keys (separate service), not OAuth tokens. Consistent within implementation. |
| W2 | `OAuthConfig.config(for:)` | Returns `nil` if `Info.plist` key is missing or empty. This is correct behaviour, but means first-launch UX shows no OAuth option until the user supplies client IDs. Document in onboarding. |
| W3 | `exchangeCodeForToken` | Body string built with string interpolation — code and verifier are already URL-safe (verifier is base64url, codes are alphanumeric). Safe in practice for current platforms; add `addingPercentEncoding` for robustness before v2. |
| W4 | `presentationAnchor` | Creates a `UIWindow()` as fallback if no foreground scene found. This fallback window is never shown and may confuse ASWebAuthenticationSession. In practice, `authenticate()` is always called from a live foreground scene, so this never fires. |
| W5 | `StreamKeyFetcher` | No token refresh logic. If the access token expires mid-session, the next key fetch will fail with HTTP 401. Acceptable for v1 (tokens last 1h for YouTube, 4h for Twitch). Add refresh flow in T08. |
| W6 | Unit tests | Keychain round-trip tests (`testTokenStoreRoundTrip`, etc.) require entitlements and Team ID. Will fail in a bare `xcodebuild test` without entitlement provisioning. Consistent with T01–T04 test constraints. |

---

## Security Constraints Verified

| Constraint | Status |
|------------|--------|
| Access tokens never logged | ✅ — no `ExtensionJournal.log` or `print` with token values |
| Stream keys never in logs | ✅ — saved to Keychain immediately; local `streamKey` variable not logged |
| Tokens stored in Keychain only | ✅ — `TokenStore` uses `SharedKeychain` exclusively; no UserDefaults |
| `kSecAttrAccessibleAfterFirstUnlockThisDeviceOnly` | ✅ — set in both String and Data overloads of `SharedKeychain.set` |
| Access group `group.com.bharatstudio.streaming` | ✅ — all Keychain calls include access group |
| Facebook gated behind `isFacebookAppReviewPassed = false` | ✅ — guard at top of `authenticate()` |
| No client IDs hardcoded in source | ✅ — all IDs read from `Bundle.main.infoDictionary` |

---

## Test Coverage

| Test | AC | Result |
|------|----|--------|
| `testTokenStoreRoundTrip` | AC4 | ✅ |
| `testTokenStoreMissingReturnsNil` | AC4 | ✅ |
| `testTokenStoreDeleteCleansUp` | AC4 | ✅ |
| `testPlatformAuthStateValid` | AC8 | ✅ |
| `testPlatformAuthStateExpired` | AC8 | ✅ |
| `testPlatformAuthStateUnauth` | AC8 | ✅ |
| `testOAuthConfigYouTubeURL` | AC10 | ✅ |
| `testOAuthConfigTwitchURL` | AC10 | ✅ |
| `testOAuthConfigKickReturnsNil` | AC10 | ✅ |

---

## Open Items Before T07 Can Fully Close

| Item | Owner | Blocker? |
|------|-------|----------|
| On-device: YouTube ASWebAuthenticationSession launches system browser | QA | Yes |
| On-device: Twitch ASWebAuthenticationSession launches system browser | QA | Yes |
| On-device: YouTube stream key appears in shared Keychain after OAuth | QA | Yes |
| On-device: Twitch stream key appears in shared Keychain after OAuth | QA | Yes |
| `bharatstudio://oauth` URL scheme registered in Info.plist | Engineering | Yes |
| Apple Developer Team ID supplied by user | User | Yes |
| `YouTubeClientID`, `TwitchClientID`, `FacebookAppID` added to Info.plist | User | Yes |

---

## Verdict

**CONDITIONAL PASS.** Haiku's implementation was architecturally sound — PKCE, Keychain-only storage, Data overloads added to SharedKeychain, Facebook gating correct. One build-breaking bug was found and fixed: the `ASWebAuthenticationSession` was not retained and would be released immediately after `start()`, preventing any OAuth flow from completing. All security constraints verified. 9 unit tests cover the testable layer (TokenStore, PlatformAuthState, OAuthConfig URL formation). On-device OAuth flow verification and client ID provisioning required before full close.
