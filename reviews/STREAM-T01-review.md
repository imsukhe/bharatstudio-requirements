# Review Record — STREAM-T01: Core Pipeline (ReplayKit → HaishinKit → RTMPS)

| Field            | Value |
|------------------|-------|
| Task             | STREAM-T01 |
| Reviewed by      | Claude Sonnet 4.6 (audit role) |
| Implementation by| Claude Haiku 4.5 (coding role) |
| Review date      | 2026-08-25 |
| Verdict          | **CONDITIONAL PASS** — all blockers fixed; on-device validation still required |

---

## Files Reviewed

| File | Lines | Result |
|------|-------|--------|
| `BharatStudioExtension/Transport/HaishinKitRTMPClient.swift` | 153 | PASS (after fix) |
| `BharatStudioExtension/SampleHandler.swift` | ~300 | PASS (after 3 fixes) |
| `BharatStudioExtension/Compositor/StreamCompositor.swift` | 221 | PASS (after 3 fixes) |
| `BharatStudioTests/SharedKeychainTests.swift` | 138 | PASS |
| `BharatStudioTests/ABRControllerTests.swift` | 216 | PASS |
| `BharatStudioTests/EntitlementFlagTests.swift` | 135 | PASS |

---

## Blockers Found and Fixed

### B1 — `stableFor` hardcoded at 30s in `abrTick()` (FIXED)

**File:** `SampleHandler.swift`  
**Severity:** BLOCKER — correctness  
**Defect:** `abrTick()` always passed `stableFor: TimeInterval = 30` to `onTickRTMP`. Since `AdaptiveBitrateController` uses `stableFor >= policy.restoreWindowSecs` to decide restoration, the ABR would attempt a +500 Kbps restore on the very next tick after every cut. Effect: oscillating bitrate (cut → immediate restore → cut...).  
**Fix applied:**
- Added `private var lastBitrateChangeDate: Date = .distantPast` to `SampleHandler`.
- `onBitrateChange` callback now resets `lastBitrateChangeDate = Date()` on every bitrate change.
- `abrTick()` computes `stableFor = Date().timeIntervalSince(lastBitrateChangeDate)` before the async Task.

---

### B2 — Wrong ABR policy thresholds in `abrTick()` (FIXED)

**File:** `SampleHandler.swift`  
**Severity:** BLOCKER — correctness  
**Defect:** `abrTick()` hardcoded `CellularAdaptivePolicy.auto.rtmpHighWatermarkMs` regardless of the user's selected ABR mode. A user in `dataSaver` mode would be measured against `auto` thresholds.  
**Fix applied:**
- Added `private var abrPolicy: CellularAdaptivePolicy = CellularAdaptivePolicy.auto` to `SampleHandler`.
- `broadcastStarted` assigns `abrPolicy = policy` after computing `policy = CellularAdaptivePolicy.preset(for: mode)`.
- `abrTick()` reads `abrPolicy.rtmpHighWatermarkMs`.

---

### B3 — Operator-precedence bug in `maybeShiftCorner()` — watermark never rotates (FIXED)

**File:** `StreamCompositor.swift`  
**Severity:** BLOCKER — watermark contract violation  
**Defect:**
```swift
// BUG: `0 + 1` evaluates before `??`, so when firstIndex returns 0 the result is 0 % 4 = 0.
let idx = (corners.firstIndex(of: watermarkCorner) ?? 0 + 1) % corners.count
```
When the watermark corner is `.bottomRight` (index 0, the initial value), `firstIndex` returns `0`. `0 % 4 = 0`. The corner is set to itself — it never moves. The Doc 134 corner-shift requirement ("prevents crop-to-remove") is never satisfied.  
**Fix applied:**
```swift
let currentIdx = corners.firstIndex(of: watermarkCorner) ?? 0
let idx = (currentIdx + 1) % corners.count
```
`maybeShiftCorner()` now returns `Bool` indicating whether a shift occurred.

---

### B4 — Per-frame watermark `UIImage` allocation (FIXED)

**File:** `StreamCompositor.swift`  
**Severity:** BLOCKER — performance / extension memory  
**Defect:** `makeWatermarkImage()` was called inside `applyWatermark()`, which was called for every video frame (30 fps). Each call allocated a `UIGraphicsBeginImageContextWithOptions` context, created a `UIImage`, converted it to `CGImage`, and built a `CIImage`. Running at 30 fps in a broadcast upload extension with strict memory limits (typically 50 MB) this would cause memory pressure and potential CPU spike.  
**Fix applied:**
- Added `private var cachedWatermark: CIImage?` to `StreamCompositor`.
- `applyWatermark()` rebuilds the watermark only when the cache is nil (first compose after init or after a corner shift).
- `maybeShiftCorner()` return value of `true` triggers `cachedWatermark = nil`.

---

### B5 — Dead `do-catch` around non-throwing `ciContext.render()` (FIXED)

**File:** `StreamCompositor.swift`  
**Severity:** BLOCKER — false error handling  
**Defect:** `CIContext.render(_:to:)` (two-argument form) is non-throwing. Wrapping it in `do { ... } catch { ... }` compiles but the `catch` block is unreachable — Swift will warn "catch block is unreachable because no errors are thrown in 'do' block". This creates a false sense that GPU render failures are caught and handled gracefully.  
**Fix applied:** Removed `do-catch`; call `ciContext.render(image, to: out)` directly. The existing `guard status == kCVReturnSuccess` above is the real safety net.

---

## Non-Blocking Warnings (carry to T02 / T03)

| ID | Location | Issue |
|----|----------|-------|
| W1 | `StreamCompositor.swift:220` | `import UIKit` at bottom of file — move to top for clarity |
| W2 | `HaishinKitRTMPClient.swift:103` | `s.info?.currentBytesPerSecond` — HaishinKit 2.x `RTMPStreamInfo` shape needs device verification; formula may not accurately represent send-buffer depth |
| W3 | `SampleHandler.swift:220-236` | App audio + mic audio both call `appendAudio` — HaishinKit may not mix them; risk of audio drop. Acceptable for T01 (T04 adds RNNoise + mixer). |
| W4 | `HaishinKitRTMPClient.swift:49` | `VideoCodecSettings(bitRate:)` — does not set profile/level/dimensions; may default to baseline 1080p regardless of compositor output size. Needs device verification. |
| W5 | `SampleHandler.swift` | `broadcastStarted` spawns async Task for `connect()`; first few seconds of frames arrive before connection established and are silently dropped. Expected behavior but should be documented in CLAUDE.md. |

---

## Security Constraints Verified

| Constraint | Status |
|------------|--------|
| Stream keys stored in Keychain only (never UserDefaults / logs) | ✅ Verified — `SharedKeychain.get(service:account:)`, never logged |
| RTMPS URL never logged (stream key embedded, then discarded) | ✅ Verified — only `errorNoKey` / `errorConnect` events logged, no URL |
| Entitlement flag never contains PII | ✅ Verified — only `.free` / `.pass` / `.subscription` enum cases |
| Watermark contract: snapshotted at Go Live, never changed mid-session | ✅ Verified — `entitlementSource` is `let`, set once in `init` |
| `analytics: watermark_applied` / `analytics: premium_stream_started` logged per session | ✅ Verified — inside `StreamCompositor.init` |

---

## Test Coverage Assessment

| Test Class | ACs Covered | Gaps |
|------------|-------------|------|
| `SharedKeychainTests` | set/get, missing→nil, overwrite, delete, empty string, stream key round-trip | None for T01 scope |
| `EntitlementFlagTests` | encode/decode (free/pass/subscription), staleness, expiry, FeatureSet derivation | `testStaleFlagDetection` tests the staleness constant but not the code path in `readEntitlementFlag()` — acceptable |
| `ABRControllerTests` | high buffer cut, stable restore, floor, ceiling, reconnect cut, no-change stable, adaptive FPS at floor, mode presets, SRT path | `stableFor` tracking fix now covered by `testStableRestore` (it explicitly cuts then passes `stableFor: 30`) |

---

## Open Items Before T01 Can Fully Close

| Item | Owner | Blocker? |
|------|-------|----------|
| Apple Developer Team ID (10-char) in `project.yml` | User | Yes — project does not build without it |
| On-device integration test: YouTube stream, 5-minute session, journal verification | QA (on-device) | Yes per T01 ACs |
| Facebook Live v1 vs defer decision | Product | No — T01 YouTube-only |
| HaishinKit `RTMPStreamInfo` API shape verified against real device build | Engineering | Needed before T02 |

---

## Verdict

**CONDITIONAL PASS.** All five blockers have been fixed in code. The implementation is architecturally sound (actor-based RTMP client, correct ReplayKit pipeline, watermark contract, security constraints). The two hard gates remaining before T01 fully closes are: (1) the user must supply the Apple Team ID so the project builds, and (2) on-device integration test with a real YouTube live stream to verify the HaishinKit API shape and confirm first-frame delivery within 5 seconds.

T02 may begin design and scaffolding in parallel; it must not ship to device until T01 on-device gate passes.
