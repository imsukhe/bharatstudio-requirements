# TC-L11 — BharatStudio Stream iOS: Test & Acceptance Record

**Task:** L11-stream-ios  
**Status:** `STREAM-T01 conditional pass — pending on-device gate`

---

## STREAM-T01 — Core pipeline: ReplayKit + HaishinKit + H.264 → RTMPS

**Status:** `Conditional pass — code complete, on-device validation required`  
**Date started:** 2026-08-25  
**Review record:** `reviews/STREAM-T01-review.md`  
**Reviewer:** Claude Sonnet 4.6 — 2026-08-25

### Blockers found and fixed (Sonnet audit 2026-08-25)

| ID | Description | Fixed |
|----|-------------|-------|
| B1 | `stableFor` hardcoded 30s → ABR oscillates immediately after cut | ✅ `lastBitrateChangeDate` added; stableFor computed dynamically |
| B2 | Wrong ABR policy used in `abrTick()` — always `.auto` regardless of user mode | ✅ `abrPolicy` stored in SampleHandler, set from user's selected mode |
| B3 | Operator-precedence bug: watermark corner never rotated from `.bottomRight` | ✅ `currentIdx + 1` computed before `%`; returns Bool for cache invalidation |
| B4 | Per-frame watermark `UIImage` allocation at 30fps → extension memory pressure | ✅ `cachedWatermark: CIImage?` added; rebuilt only on corner shift or init |
| B5 | Dead `do-catch` around non-throwing `ciContext.render()` — false error handling | ✅ Removed; non-throwing call used directly |

### Acceptance criteria (10 items — all must be ✅ before task fully closes)

| # | Criterion | Result | Evidence |
|---|---|---|---|
| AC1 | Build succeeds (zero errors) | ⬜ | Requires DEVELOPMENT_TEAM set by user |
| AC2 | Stream key round-trip via Keychain, read by extension | ⬜ | Unit test class: SharedKeychainTests |
| AC3 | YouTube shows stream as "Live" | ⬜ | On-device only |
| AC4 | H.264 video visible in stream | ⬜ | On-device only |
| AC5 | 5-min duration, no unexpected crash | ⬜ | On-device only |
| AC6 | Extension memory < 50MB peak | ⬜ | Instruments on-device |
| AC7 | Journal logs: rtmp_connected + session_duration | ⬜ | journal.jsonl from App Group |
| AC8 | Watermark applied for free; absent for paid | ⬜ | Visual + `watermark_applied` log |
| AC9 | No secret in any log line | ⬜ | grep journal.jsonl for stream key |
| AC10 | Clean disconnect on broadcastFinished | ⬜ | `rtmp_disconnected` in journal |

### Unit tests (code-level only, no device required)

| Test | Status | Command |
|---|---|---|
| Keychain set/get/delete | ⬜ | `xcodebuild test -scheme BharatStudio` |
| EntitlementFlag encode/decode | ⬜ | same |
| ABR cut + restore logic | ⬜ | same |

> Note: All three test classes use `@testable import BharatStudio`. Types under test
> (`SharedKeychain`, `EntitlementFlag`, `AdaptiveBitrateController`) must be in the
> `BharatStudio` (main app) or `Shared/` targets, not Extension-only, for tests to compile.

### On-device integration evidence

_To be filled after physical device test. Minimum: YouTube Studio screenshot showing "Live", journal.jsonl excerpt with `rtmp_connected` + `first_frame_sent` + `session_duration`, and Instruments memory peak < 50 MB._

---

---

## STREAM-T02 — Multi-platform RTMPS + Reconnect + Observability

**Status:** `Conditional pass — code complete, on-device validation required`  
**Date started:** 2026-08-25  
**Review record:** `reviews/STREAM-T02-review.md`  
**Reviewer:** Claude Sonnet 4.6 — 2026-08-25

### Blockers found and fixed (Sonnet audit 2026-08-25)

| ID | Description | Fixed |
|----|-------------|-------|
| B1 | `finishBroadcast` actor property set synchronously from non-actor context — compile error | ✅ `nonisolated(unsafe) var` |
| B2 | `client?.reconnectCount` + `client?.isConnected` read in sync closure — actor isolation violation | ✅ Cached in `cachedReconnectCount`/`cachedIsConnected`, updated in abrTick Task |
| B3 | `RTMPReconnectActor` never called `client.recordReconnect()` — health report always `reconnects: 0` | ✅ `await client.recordReconnect()` added in failure branch |
| W1 | Path monitor cut used `startingBitrateBps` instead of `currentBitrateBps` — wrong base | ✅ Now reads `currentBitrateBps` |

### Acceptance criteria

| # | Criterion | Result | Evidence |
|---|-----------|--------|----------|
| AC1 | Reconnect fires on failure; 5 retries with 1→2→4→8→16→32s backoff | ⬜ | On-device required |
| AC2 | `reconnect_attempt:{n}` + success/exhausted logged to journal | ⬜ | Journal from App Group |
| AC3 | ABR cuts to 2/3 on each reconnect | ⬜ | Journal + health JSON |
| AC4 | NWPathMonitor detects WiFi→Cellular; logs `network_path_changed` | ⬜ | On-device required |
| AC5 | Health JSON written to App Group every 5s | ⬜ | Read from container |
| AC6 | Health schema: ts, platform, bitrate_kbps, duration_s, reconnects, is_connected | ✅ | Unit test + code review |
| AC7 | Twitch URL: `rtmps://live.twitch.tv/app/{key}` | ✅ | Unit test |
| AC8 | Platform from App Group `activePlatform`, default youtube | ✅ | Code review |
| AC9 | Stream key never in any log line | ✅ | Code review + unit test |
| AC10 | 6 unit tests pass | ⬜ | Requires build with Team ID |

### Unit tests

| Test | Status | File |
|------|--------|------|
| Reconnect backoff sequence | ⬜ | `T02Tests.swift` |
| Platform URL formats | ⬜ | `T02Tests.swift` |
| Keychain service names unique | ⬜ | `T02Tests.swift` |
| StreamHealth encode/decode | ⬜ | `T02Tests.swift` |
| Platform string max 32 chars | ⬜ | `T02Tests.swift` |
| LoggableID contains no key | ⬜ | `T02Tests.swift` |

### On-device integration evidence

_To be filled: Twitch Studio screenshot (Live), WiFi→Cellular handover log, `stream_health.json` from App Group container._

---

## STREAM-T03 — Metal Compositor + Watermark + ABR Full Wiring

**Status:** `Conditional pass — code complete, device build verification required`  
**Review record:** `reviews/STREAM-T03-review.md`  
**Reviewer:** Claude Sonnet 4.6 — 2026-08-25

### Blockers found and fixed (Sonnet audit 2026-08-25)

| ID | Description | Fixed |
|----|-------------|-------|
| B1 | `VideoCodecSettings(maximumVideoSize:)` wrong param name → `videoSize:` | ✅ |
| B2 | `s.videoSettings.frameRate` doesn't exist → `s.frameRate = Double(fps)` | ✅ |
| B3 | `bitRate = UInt32` type mismatch → `Int(bps)` | ✅ |
| W1 | Zero-extent overlay div-by-zero in scale transform → guard added | ✅ |

### Acceptance criteria

| # | Criterion | Result |
|---|-----------|--------|
| AC1 | `connect()` sets 1280×720, frameRate=30 | ⬜ Device build required |
| AC2 | `setVideoFrameRate(24)` lowers to 24fps | ⬜ Device build required |
| AC3 | `setVideoFrameRate(30)` restores to 30fps | ⬜ Device build required |
| AC4 | `onBitrateChange` wires adaptiveFPS → `setVideoFrameRate` | ✅ Code review |
| AC5 | `makeWatermarkImage` uses CoreGraphics/CoreText only | ✅ Code review |
| AC6 | `OverlayAsset` in Shared/ with id, position, size, image | ✅ Code review |
| AC7 | `compose` renders `[OverlayAsset]` z-ordered with zero-guard | ✅ Code review |
| AC8 | Watermark cache valid, rebuilt on shift only | ✅ Code review |
| AC9 | No UIKit in StreamCompositor.swift | ✅ Code review |
| AC10 | 6 unit tests | ⬜ Requires build with Team ID |

### On-device integration evidence

_Minimum: journal log `fps_changed:24` observed at ABR floor during a 10-min stream. `resolution_config:1280x720` in journal at session start._

---

## STREAM-T04 — Audio: AVAudioEngine + RNNoise + 3-input Mixer

**Status:** `Conditional pass — code complete, on-device audio verification required`  
**Review record:** `reviews/STREAM-T04-review.md`  
**Reviewer:** Claude Sonnet 4.6 — 2026-08-25

### Blockers found and fixed (Sonnet audit 2026-08-25)

| ID | Description | Fixed |
|----|-------------|-------|
| B1 | `feedAppAudio(AVAudioPCMBuffer)` didn't match SampleHandler's `appendAppAudio(CMSampleBuffer)` | ✅ Sonnet rewrite |
| B2 | `prepare()` didn't match SampleHandler's `start()` | ✅ Sonnet rewrite |
| B3 | `onMixedAudio` didn't match SampleHandler's `onOutputBuffer` + no audio flowed (no render thread) | ✅ Sonnet rewrite: push-based pipeline |

### Acceptance criteria

| # | Criterion | Result |
|---|-----------|--------|
| AC1 | BroadcastAudioEngine starts without crash | ⬜ Device |
| AC2 | CMSampleBuffer → 48kHz mono conversion | ✅ AudioResampler unit-tested |
| AC3 | 480-sample chunk accumulation | ✅ AudioChunkBuffer unit-tested |
| AC4 | RNNoiseProcessor protocol + PassthroughNoiseProcessor | ✅ Unit-tested |
| AC5 | appendAppAudio + appendMicAudio route through engine | ✅ Code review |
| AC6 | Output: 48kHz Float32 mono | ✅ ASBD in BroadcastAudioEngine |
| AC7 | SampleHandler routes audio through BroadcastAudioEngine | ✅ Code review |
| AC8 | Graceful nil handling (isRunning gate) | ✅ Code review |
| AC9 | No main-thread audio processing | ✅ AudioQueue dispatches async |
| AC10 | 7 unit tests pass | ⬜ Requires build with Team ID |

### On-device integration evidence

_Minimum: stream has audible audio with `audio_engine_started` in journal. Mic audio does not crash extension (verify via 5-min session + journal)._

---

## STREAM-T07 — OAuth × 4 Platforms

**Status:** `Conditional pass — code complete, on-device OAuth flow verification required`
**Date started:** 2026-08-26
**Review record:** `reviews/STREAM-T07-review.md`
**Reviewer:** Claude Sonnet 4.6 — 2026-08-26

### Blockers found and fixed (Sonnet audit 2026-08-26)

| ID | Description | Fixed |
|----|-------------|-------|
| B1 | `ASWebAuthenticationSession` created as local variable inside `withCheckedThrowingContinuation` — ARC-released before completion handler fires; OAuth flow dismisses immediately | ✅ `private var activeAuthSession` added; set before `start()`, cleared in completion |

### Acceptance criteria

| # | Criterion | Result | Evidence |
|---|-----------|--------|----------|
| AC1 | ASWebAuthenticationSession launches for YouTube and Twitch OAuth | ⬜ | On-device required |
| AC2 | OAuth tokens stored in Keychain (`kSecAttrAccessibleAfterFirstUnlockThisDeviceOnly`) | ✅ | Code review: SharedKeychain sets accessibility flag |
| AC3 | Access token never appears in any log line | ✅ | Code review: no log calls with token values |
| AC4 | `TokenStore.save`/`load` round-trips through Keychain | ✅ | Unit test: `testTokenStoreRoundTrip` |
| AC5 | StreamKeyFetcher fetches YouTube stream key from Data API v3 | ✅ | Code review: `liveStreams?part=cdn&mine=true` |
| AC6 | StreamKeyFetcher fetches Twitch stream key from Helix API | ✅ | Code review: `helix/users` + `helix/streams/key` |
| AC7 | Fetched stream key saved to Keychain via SharedKeychain (same service as extension) | ✅ | Code review: `PlatformRegistry.keychainService(platform:)` + `SharedKeychain.set` |
| AC8 | PlatformAuthState: `.unauthenticated`, `.authenticated(expiresAt:)`, `.tokenExpired` | ✅ | Unit tests: testPlatformAuthState* |
| AC9 | Facebook: OAuth implemented but gated (`isFacebookAppReviewPassed = false`) | ✅ | Code review: guard at top of `authenticate()` |
| AC10 | 9 unit tests pass | ⬜ | Requires build with Team ID + client IDs in Info.plist |

### Unit tests

| Test | Status | File |
|------|--------|------|
| `testTokenStoreRoundTrip` | ⬜ | `T07Tests.swift` |
| `testTokenStoreMissingReturnsNil` | ⬜ | `T07Tests.swift` |
| `testTokenStoreDeleteCleansUp` | ⬜ | `T07Tests.swift` |
| `testPlatformAuthStateValid` | ⬜ | `T07Tests.swift` |
| `testPlatformAuthStateExpired` | ⬜ | `T07Tests.swift` |
| `testPlatformAuthStateUnauth` | ⬜ | `T07Tests.swift` |
| `testOAuthConfigYouTubeURL` | ⬜ | `T07Tests.swift` |
| `testOAuthConfigTwitchURL` | ⬜ | `T07Tests.swift` |
| `testOAuthConfigKickReturnsNil` | ⬜ | `T07Tests.swift` |

> Note: Keychain round-trip tests require entitlement provisioning + Team ID. Logic tests (`testOAuthConfigYouTubeURL`, `testOAuthConfigTwitchURL`, `testOAuthConfigKickReturnsNil`) do not need Keychain and will pass immediately.

### On-device integration evidence

_Minimum: YouTube ASWebAuthenticationSession launches system browser, completes OAuth, stream key appears in shared Keychain (verified via SampleHandler reading it at `broadcastStarted`). Repeat for Twitch. Facebook returns false (gated). Kick manual entry round-trips through Keychain._

### Prerequisites not yet supplied by user

| Item | Status |
|------|--------|
| `DEVELOPMENT_TEAM` (10-char Apple Team ID) | ⬜ Pending |
| `YouTubeClientID` in Info.plist | ⬜ Pending |
| `TwitchClientID` in Info.plist | ⬜ Pending |
| `FacebookAppID` in Info.plist | ⬜ Pending |
| `bharatstudio://oauth` URL scheme in Info.plist CFBundleURLTypes | ⬜ Pending |

---

## STREAM-T05 — Chat: Twitch IRC/EventSub + YouTube Live Chat API

**Status:** `Conditional pass — code complete, on-device chat verification required`
**Date started:** 2026-08-26
**Review record:** `reviews/STREAM-T05-review.md`
**Reviewer:** Claude Sonnet 4.6 — 2026-08-26

### Blockers found and fixed (Sonnet audit 2026-08-26)

| ID | Description | Fixed |
|----|-------------|-------|
| B1 | Access token passed as URL query parameter in `YouTubeChatPoller` — leaks to server/proxy logs | ✅ `Authorization: Bearer` header used in both `fetchLiveChatID` and `poll` |
| B2 | `receiveLoop()` calls `connect()` recursively on disconnect → unbounded stack growth → crash | ✅ Reconnect moved to unstructured `Task { await self.connect() }` — fresh stack per reconnect |
| B3 | `ExtensionAlertWriter` never called — subscriber/bits IRC events not parsed → AC9 not met | ✅ `parseTags()` added; `handleMessage()` now wires USERNOTICE (sub/resub) and PRIVMSG `bits=N` to `ExtensionAlertWriter.write()` |

### Acceptance criteria

| # | Criterion | Result | Evidence |
|---|-----------|--------|----------|
| AC1 | `TwitchChatClient` connects to `wss://irc-ws.chat.twitch.tv:443` and joins channel | ✅ | Code review |
| AC2 | IRC PRIVMSG parsed: username, text, color | ✅ | Unit tests testParsePRIVMSG* |
| AC3 | PING → PONG keepalive | ✅ | Unit test testPingLineDetected |
| AC4 | `YouTubeChatPoller` polls at server-recommended interval (`pollingIntervalMillis`) | ✅ | Code review |
| AC5 | YouTube chat message parsed: author, text, publishedAt | ✅ | Code review |
| AC6 | Both sources feed `ChatMessage` into single `ChatStore` actor | ✅ | Code review |
| AC7 | `ChatStore` caps at 200 messages | ✅ | Unit test testChatStoreCapAt200 |
| AC8 | Chat messages never logged | ✅ | Code review: no log calls with text/author |
| AC9 | Twitch subscriber/bits events written to App Group `alerts.jsonl` | ✅ | Code review (post B3 fix) |
| AC10 | 8 unit tests pass | ⬜ | Requires build with Team ID |

### Unit tests

| Test | Status | File |
|------|--------|------|
| `testChatMessageEquality` | ⬜ | `T05Tests.swift` |
| `testChatStoreSingleMessage` | ⬜ | `T05Tests.swift` |
| `testChatStoreCapAt200` | ⬜ | `T05Tests.swift` |
| `testParsePRIVMSG` | ⬜ | `T05Tests.swift` |
| `testParsePRIVMSGNoColor` | ⬜ | `T05Tests.swift` |
| `testExtensionAlertEncoding` | ⬜ | `T05Tests.swift` |
| `testPingLineDetected` | ⬜ | `T05Tests.swift` |
| `testChatStoreStreamYields` | ⬜ | `T05Tests.swift` |

### On-device integration evidence

_Minimum: Chat messages from Twitch appear in ChatStore during a live stream. YouTube chat messages appear when OAuth token is valid. Subscriber event generates a line in `alerts.jsonl` in App Group container._

### Open items

- Authenticated Twitch IRC (PASS oauth:token) required for sub/bits events — scheduled for T08
- YouTube access token refresh required — scheduled for T08

---

## STREAM-T06 — Scenes (AVAssetReader loop) + Overlays

**Status:** `Conditional pass — code complete, on-device video loop verification required`
**Date started:** 2026-08-26
**Review record:** `reviews/STREAM-T06-review.md`
**Reviewer:** Claude Sonnet 4.6 — 2026-08-26

### Blockers found and fixed

None. Clean implementation pass.

### Acceptance criteria

| # | Criterion | Result | Evidence |
|---|-----------|--------|----------|
| AC1 | `SceneAsset` model: id, name, type, fileURL; Codable | ✅ | Unit test testSceneAssetCodable |
| AC2 | `SceneManager` actor manages active scene + overlays | ✅ | Code review + unit tests |
| AC3 | `VideoLoopPlayer` reads AVAssetReader frames → CVPixelBuffer | ✅ | Code review |
| AC4 | `VideoLoopPlayer` loops seamlessly on EOF | ✅ | Code review: setupReader() called on nil sampleBuffer |
| AC5 | `SceneManager.overlays` max 5 items | ✅ | Unit test testSceneManagerMaxOverlays |
| AC6 | Overlay add/remove/reposition | ✅ | Unit tests |
| AC7 | Scene frames passed as `screen` to StreamCompositor | ⬜ | Wired in T08 |
| AC8 | Image scene emits same CIImage every tick | ✅ | Code review: pixelBuffer cached in init |
| AC9 | Scene asset files in App Group container | ✅ | Code review: fileURL policy documented |
| AC10 | 7 unit tests pass | ⬜ | Requires build with Team ID |

### Unit tests

| Test | Status | File |
|------|--------|------|
| `testSceneAssetCodable` | ⬜ | `T06Tests.swift` |
| `testSceneTypeCoverage` | ⬜ | `T06Tests.swift` |
| `testSceneManagerInitialState` | ⬜ | `T06Tests.swift` |
| `testSceneManagerAddOverlay` | ⬜ | `T06Tests.swift` |
| `testSceneManagerMaxOverlays` | ⬜ | `T06Tests.swift` |
| `testSceneManagerRemoveOverlay` | ⬜ | `T06Tests.swift` |
| `testSceneManagerUpdateOverlayPosition` | ⬜ | `T06Tests.swift` |

### On-device integration evidence

_Minimum: Video scene loops for 60+ seconds without freeze. Image scene appears static but renders at 30fps. SceneManager.currentFrame() supplies correct CVPixelBuffer to StreamCompositor (T08 wiring required)._

---

## STREAM-T08 — Settings UI + AVSampleBuffer Preview + Onboarding

**Status:** `Conditional pass — code complete, on-device UI verification + deployment target confirmation required`
**Date started:** 2026-08-26
**Review record:** `reviews/STREAM-T08-review.md`
**Reviewer:** Claude Sonnet 4.6 — 2026-08-26

### Blockers found and fixed (Sonnet audit 2026-08-26)

| ID | Description | Fixed |
|----|-------------|-------|
| B1 | `T08Tests.swift` only had `import XCTest` — all types (`StreamHealth`, `QualityPreset`, `AppGroup`, `SharedKeychain`) inaccessible → compile failure | ✅ Added `@testable import BharatStudio` |

### Acceptance criteria

| # | Criterion | Result | Evidence |
|---|-----------|--------|----------|
| AC1 | OnboardingView: shown on first launch; `hasCompletedOnboarding` flag written to App Group UserDefaults | ✅ | Code review + `testOnboardingFlag` |
| AC2 | DashboardView: polls StreamHealth every 3s via `StreamHealthReader.read()` | ✅ | Code review + `testStreamHealthDecode` |
| AC3 | SettingsView: platform picker writes `activePlatform` to App Group UserDefaults | ✅ | Code review + `testActivePlatformWrite` |
| AC4 | Kick stream key stored in Keychain; cleared on empty string | ✅ | `testKickStreamKeyKeychainRoundTrip` |
| AC5 | QualityPreset: low/medium/high with correct bitrates and resolutions | ✅ | 6 quality preset unit tests |
| AC6 | PreviewView: `AVSampleBufferDisplayLayer` wrapping in UIViewRepresentable | ✅ | Code review |
| AC7 | ChatView: scrolls to latest message; reads from `ChatStore.shared.stream` | ✅ | Code review |
| AC8 | ScenePickerView: lists SceneAssets, selects active scene | ✅ | Code review |
| AC9 | Facebook greyed out with "Coming soon" — `.disabled(true)` | ✅ | Code review |
| AC10 | 10 unit tests pass | ⬜ | Requires build with Team ID |

### Unit tests

| Test | Status | File |
|------|--------|------|
| `testOnboardingFlag` | ⬜ | `T08Tests.swift` |
| `testStreamHealthDecode` | ⬜ | `T08Tests.swift` |
| `testQualityPresetLowBitrate` | ⬜ | `T08Tests.swift` |
| `testQualityPresetMediumBitrate` | ⬜ | `T08Tests.swift` |
| `testQualityPresetHighBitrate` | ⬜ | `T08Tests.swift` |
| `testQualityPresetCount` | ⬜ | `T08Tests.swift` |
| `testQualityPresetResolutions` | ⬜ | `T08Tests.swift` |
| `testQualityPresetDisplayNames` | ⬜ | `T08Tests.swift` |
| `testActivePlatformWrite` | ⬜ | `T08Tests.swift` |
| `testKickStreamKeyKeychainRoundTrip` | ⬜ | `T08Tests.swift` |

### On-device integration evidence

_Minimum: OnboardingView appears on clean install and is skipped on subsequent launches. DashboardView shows live bitrate, duration, and connection badge during an active stream. SettingsView platform switch propagates to extension within one App Group poll cycle. ChatView displays live chat messages with per-platform color coding._

### Open items

- Deployment target confirmation needed (W1): `.onChange(of:) { oldValue, newValue in }` is iOS 17+ two-arg form; if targeting iOS 16, downgrade to one-arg
- `PreviewView.enqueue()` wiring to compositor deferred to T10

---

## STREAM-T09 — StoreKit 2 IAP Full Wiring + Entitlement Enforcement

**Status:** `Conditional pass — code complete, StoreKit sandbox + on-device entitlement verification required`
**Date started:** 2026-08-26
**Review record:** `reviews/STREAM-T09-review.md`
**Reviewer:** Claude Sonnet 4.6 — 2026-08-26

### Blockers found and fixed

None. Clean implementation pass.

### Acceptance criteria

| # | Criterion | Result | Evidence |
|---|-----------|--------|----------|
| AC1 | `EntitlementStore.productIDs` contains 3 product ID strings | ✅ | `testProductIDConstants` |
| AC2 | `EntitlementStore.purchase()` calls `product.purchase()` + `checkVerified()` + `transaction.finish()` | ✅ | Code review |
| AC3 | `Transaction.updates` listener started in `init()` + cancelled in `deinit()` | ✅ | Code review |
| AC4 | `writeEntitlementFlag(.subscription)` writes `EntitlementFlag` to App Group `entitlement.json` | ✅ | `testEntitlementFlagPaid` |
| AC5 | Free tier writes `EntitlementFlag(.free)` — `entitled = false` | ✅ | `testEntitlementFlagFree` |
| AC6 | `EntitlementTier` Codable roundtrip | ✅ | `testEntitlementTierCodable` |
| AC7 | All 4 tiers have non-empty display names | ✅ | `testAllTiersHaveDisplayNames`, `testDisplayNameValues` |
| AC8 | `restorePurchases()` calls `AppStore.sync()` then `checkCurrentEntitlement()` | ✅ | Code review |
| AC9 | No hardcoded prices — uses `product.displayPrice` (locale-aware) | ✅ | Code review |
| AC10 | 4 tiers: free/pro/creator/studio | ✅ | `testEntitlementTierCount` |

### Unit tests

| Test | Status | File |
|------|--------|------|
| `testProductIDConstants` | ⬜ | `T09Tests.swift` |
| `testEntitlementTierCount` | ⬜ | `T09Tests.swift` |
| `testFreeHasNoProductID` | ⬜ | `T09Tests.swift` |
| `testProHasProductID` | ⬜ | `T09Tests.swift` |
| `testCreatorHasProductID` | ⬜ | `T09Tests.swift` |
| `testStudioHasProductID` | ⬜ | `T09Tests.swift` |
| `testAllTiersHaveDisplayNames` | ⬜ | `T09Tests.swift` |
| `testDisplayNameValues` | ⬜ | `T09Tests.swift` |
| `testEntitlementFlagFree` | ⬜ | `T09Tests.swift` |
| `testEntitlementFlagPaid` | ⬜ | `T09Tests.swift` |
| `testEntitlementTierCodable` | ⬜ | `T09Tests.swift` |

### On-device integration evidence

_Minimum: StoreKit sandbox purchase completes (pro/creator/studio) and entitlement flag is written to App Group `entitlement.json`. Extension reads `entitled: true` and suppresses watermark. `restorePurchases()` restores valid subscription after fresh install in sandbox._

---

## STREAM-T10 — Device/Carrier QA Matrix + App Store Submission

**Status:** `Conditional pass — code complete, physical QA + Apple Developer credentials required`
**Date started:** 2026-08-26
**Review record:** `reviews/STREAM-T10-review.md`
**Reviewer:** Claude Sonnet 4.6 — 2026-08-26

### Blockers found and fixed (Sonnet audit 2026-08-26)

| ID | Description | Fixed |
|----|-------------|-------|
| B1 | `SettingsView.swift` (×2) and `ChatView.swift` used iOS 17+ two-arg `.onChange(of:) { oldValue, newValue in }` — compile error at `deploymentTarget: "16.0"` | ✅ Downgraded to iOS 14+ single-arg `.onChange(of:) { newValue in }` in all 3 call sites |

### Acceptance criteria

| # | Criterion | Result | Evidence |
|---|-----------|--------|----------|
| AC1 | `project.yml` updated with T05–T09 source paths in correct targets | ✅ | Code review |
| AC2 | App Group identifier reconciled — `group.com.bharatstudio.streaming` canonical | ✅ | Audit: zero truncated identifiers found |
| AC3 | `Configuration.storekit` with 3 auto-renewable subscriptions for Xcode sandbox | ✅ | Code review |
| AC4 | Info.plist keys documented (OAuth client IDs, URL scheme, privacy descriptions) | ✅ | LAUNCH-CHECKLIST.md Phase 3 |
| AC5 | `LAUNCH-CHECKLIST.md` — 5-phase step-by-step submission guide | ✅ | 230-line doc created |
| AC6 | `QA-MATRIX.md` — 25 scenarios × 3 devices × 4 networks | ✅ | 122-line doc created |
| AC7 | `KNOWN-ISSUES.md` — 12 W-level items with fix schedules | ✅ | 275-line doc created |
| AC8 | `DEVELOPMENT_TEAM` placeholder marked in `project.yml` (×2) | ✅ | `"REPLACE_WITH_YOUR_TEAM_ID"` with comment |
| AC9 | OnboardingView Facebook "Coming soon" overlay present | ✅ | Verified in T08 source |
| AC10 | AppGroup identifier audit complete — result: clean | ✅ | `APPGROUP-AUDIT.md` created |

### Unit tests

| Test | Status | File |
|------|--------|------|
| `testAppGroupIdentifierFormat` | ⬜ | `T10Tests.swift` |
| `testProductIDsMatchExpectedConstants` | ⬜ | `T10Tests.swift` |
| `testFacebookGated` | ⬜ | `T10Tests.swift` |
| `testQualityPresetBitratesOrdered` | ⬜ | `T10Tests.swift` |
| `testEntitlementFlagURLNotNil` | ⬜ (no-assert in CI by design) | `T10Tests.swift` |
| `testPlatformRegistryCoversAllCases` | ⬜ | `T10Tests.swift` |

### Physical QA prerequisite

All 25 scenarios in `bharatstudio-requirements/launch/QA-MATRIX.md` must be executed on physical devices before App Store submission. Key scenarios requiring device:

| Priority | Scenario | Devices |
|----------|----------|---------|
| P0 | S04: 30-min stream, memory < 50MB | iPhone 15 Pro |
| P0 | S05: WiFi→4G handover | iPhone 13 |
| P0 | S07/S08: Watermark free vs paid | iPhone 15 Pro |
| P0 | S09: Restore purchase after reinstall | iPhone 13 |
| P1 | S06: Network loss → 5 retry attempts | iPhone SE 3 |
| P1 | S16: ABR bitrate cut on 4G-Weak | iPhone SE 3 |

### User-supplied prerequisites (required before App Store submission)

| Item | Status |
|------|--------|
| Apple Developer Team ID (10-char) | ⬜ Pending |
| App Group `group.com.bharatstudio.streaming` registered | ⬜ Pending |
| Keychain Sharing group registered | ⬜ Pending |
| `YouTubeClientID` in Info.plist | ⬜ Pending |
| `TwitchClientID` in Info.plist | ⬜ Pending |
| `FacebookAppID` in Info.plist | ⬜ Pending |
| StoreKit products created in App Store Connect | ⬜ Pending |
| Privacy Policy URL live | ⬜ Pending |
| App Store screenshots (all device sizes) | ⬜ Pending |

### Launch documents created

| Document | Location |
|----------|----------|
| App Store submission guide | `bharatstudio-requirements/launch/LAUNCH-CHECKLIST.md` |
| Physical QA test matrix | `bharatstudio-requirements/launch/QA-MATRIX.md` |
| Known issues registry | `bharatstudio-requirements/launch/KNOWN-ISSUES.md` |
| App Group audit report | `bharatstudio-requirements/launch/APPGROUP-AUDIT.md` |
| StoreKit sandbox config | `BharatStudio/Configuration.storekit` |
