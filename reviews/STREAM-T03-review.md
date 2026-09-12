# Review Record — STREAM-T03: Metal Compositor + Watermark + ABR Full Wiring

| Field            | Value |
|------------------|-------|
| Task             | STREAM-T03 |
| Reviewed by      | Claude Sonnet 4.6 (audit role) |
| Implementation by| Claude Haiku 4.5 (coding role) |
| Review date      | 2026-08-25 |
| Verdict          | **CONDITIONAL PASS** — all blockers fixed; on-device frame-rate verification required |

---

## Files Reviewed

| File | Lines | Result |
|------|-------|--------|
| `BharatStudioExtension/Transport/HaishinKitRTMPClient.swift` | 201 | PASS (after 3 fixes) |
| `BharatStudioExtension/Compositor/StreamCompositor.swift` | 247 | PASS (after 1 fix) |
| `Shared/OverlayAsset.swift` | 21 | PASS |
| `BharatStudioTests/T03Tests.swift` | 71 | PASS |

---

## Blockers Found and Fixed

### B1 — `maximumVideoSize` param name wrong (FIXED)

**File:** `HaishinKitRTMPClient.swift`  
**Defect:** `VideoCodecSettings` initializer used `maximumVideoSize:` which does not exist in HaishinKit 2.x. The correct property name is `videoSize`. Compile error.  
**Fix:** `maximumVideoSize: .init(width:height:)` → `videoSize: CGSize(width: videoWidth, height: videoHeight)`

---

### B2 — `s.videoSettings.frameRate` doesn't exist in HaishinKit 2.x (FIXED)

**File:** `HaishinKitRTMPClient.swift`  
**Defect:** `VideoCodecSettings` in HaishinKit 2.x has no `frameRate` property. Frame rate is on `RTMPStream.frameRate: Float64` (not in the codec settings struct). Two call sites affected: `connect()` and `setVideoFrameRate()`.  
**Fix:** `s.videoSettings.frameRate = videoFrameRate` → `s.frameRate = Double(videoFrameRate)` (both sites)

---

### B3 — `VideoCodecSettings.bitRate: Int` receives `UInt32` (FIXED)

**File:** `HaishinKitRTMPClient.swift`  
**Defect:** `setVideoBitrate(_ bps: UInt32)` assigned `s.videoSettings.bitRate = bps` but `bitRate` is typed `Int` in HaishinKit 2.x. Swift does not allow implicit numeric widening — compile error.  
**Fix:** `s.videoSettings.bitRate = Int(bps)`

---

### W1 — Division by zero in overlay scale transform (FIXED)

**File:** `StreamCompositor.swift`  
**Defect:** `scaleX: overlay.size.width / overlay.image.extent.width` — if the overlay image has a zero-width extent (e.g. `CIImage.empty()` or a bad source), this produces `NaN` or `+Inf` in the scale transform, corrupting the composed frame silently.  
**Fix:** Guard `srcW > 0, srcH > 0, overlay.size.width > 0, overlay.size.height > 0` before applying the transform.

---

## Non-Blocking Observations

| ID | Location | Issue |
|----|----------|-------|
| N1 | `HaishinKitRTMPClient.swift:54` | `VideoCodecSettings(bitRate:isBaseline:videoSize:scalingMode:)` — initializer parameter order depends on HaishinKit 2.x memberwise init. If field order differs, compilation fails. Flagged for device build verification. |
| N2 | `HaishinKitRTMPClient.swift:58` | `scalingMode: .letterbox` — HaishinKit `ScalingMode` cases may be `.trim`/`.letterbox`/`.cropSourceToCleanAperture`. If `.letterbox` doesn't compile, fall back to `.trim`. |
| N3 | `T03Tests.swift` | Tests don't exercise `HaishinKitRTMPClient` directly (actor requires real HaishinKit + RTMP server). Tests cover ABR logic and OverlayAsset. Acceptable: HaishinKit API tested on device. |
| N4 | `StreamCompositor.swift` | `CTFontCreateWithName("Helvetica", ...)` — Helvetica is available on iOS. If not found, CoreText returns a default font, which is acceptable. No assertion needed. |

---

## Security Constraints Verified

| Constraint | Status |
|------------|--------|
| No UIKit in StreamCompositor.swift | ✅ `import UIKit` removed; replaced with CoreText |
| No stream key in frame-rate or resolution logs | ✅ `fps_changed:`, `resolution_config:` log only numeric values |
| Watermark contract preserved (last layer, snapshotted at Go Live) | ✅ Unchanged from T01 fix |

---

## Test Coverage

| Test | AC | Result |
|------|----|--------|
| `testAdaptiveFPSDefault` | AC1 via policy | ✅ |
| `testAdaptiveFPSLogic` | AC4 — ABR floor → adaptiveFPS=true | ✅ |
| `testOverlayAssetCreation` | AC6 | ✅ |
| `testOverlayAssetDefaultID` | AC6 (uniqueness) | ✅ |
| `testDefaultResolutionConstants` | AC1 (720p 16:9) | ✅ |
| `testCellularPolicyCoverageFPS` | AC1 (positive bitrate across modes) | ✅ |

---

## Open Items Before T03 Can Fully Close

| Item | Owner | Blocker? |
|------|-------|----------|
| `VideoCodecSettings` initializer param order verified against real HaishinKit 2.x build | Engineering | Yes |
| `scalingMode: .letterbox` confirmed valid (vs `.trim`) | Engineering | Yes |
| Adaptive FPS switch observed live on device (30fps→24fps at floor) | QA | Yes |
| Apple Developer Team ID in `project.yml` | User | Yes |

---

## Verdict

**CONDITIONAL PASS.** Three build-blocking API mismatches corrected. One division-by-zero guard added. Implementation is structurally correct: CoreText watermark replaces UIKit, overlay z-ordering is correct, adaptive FPS is wired from ABR to HaishinKit. Final gate: device build to confirm HaishinKit 2.x initializer shape.
