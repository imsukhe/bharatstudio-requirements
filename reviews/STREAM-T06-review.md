# Review Record — STREAM-T06: Scenes (AVAssetReader loop) + Overlays

| Field            | Value |
|------------------|-------|
| Task             | STREAM-T06 |
| Reviewed by      | Claude Sonnet 4.6 (audit role) |
| Implementation by| Claude Haiku 4.5 (coding) |
| Review date      | 2026-08-26 |
| Verdict          | **CONDITIONAL PASS** — no blockers; on-device video loop + compositor integration verification required |

---

## Files Reviewed

| File | Lines | Result |
|------|-------|--------|
| `Shared/SceneAsset.swift` | 31 | PASS |
| `BharatStudioExtension/Scene/SceneFrameProvider.swift` | 12 | PASS |
| `BharatStudioExtension/Scene/VideoLoopPlayer.swift` | 67 | PASS |
| `BharatStudioExtension/Scene/ImageScenePlayer.swift` | 50 | PASS |
| `BharatStudioExtension/Scene/SceneManager.swift` | 75 | PASS |
| `BharatStudioTests/T06Tests.swift` | 119 | PASS |

---

## Blockers Found and Fixed

None. Implementation is architecturally sound and matches the spec.

---

## Non-Blocking Observations

| ID | Location | Issue |
|----|----------|-------|
| W1 | `VideoLoopPlayer.setupReader()` | Calls `asset.tracks(withMediaType: .video)` synchronously. For local App Group files this returns immediately; for remote URLs this would block. Acceptable for v1 (scenes are always local files). Prefer `asset.loadTracks(withMediaType:)` async API in v2. |
| W2 | `VideoLoopPlayer.init()` | Calls `setupReader()` from actor `init`. Permitted by Swift's actor init rules (self is uniquely owned before escape). Compiles correctly. |
| W3 | `ImageScenePlayer.init?()` | Uses `CIContext()` (software renderer) for the one-time init render. Acceptable — called once per scene switch, not per frame. |
| W4 | `SceneManager.setActiveScene` | `ImageScenePlayer(imageURL:)` is failable — if the image fails to load, `frameProvider` is set to nil silently. The scene activates (activeScene is set) but `currentFrame()` returns nil. UI should handle this by checking `currentFrame() == nil`. |
| W5 | `T06Tests.swift` | Tests use `CIImage.empty()` as overlay image. `empty()` has zero extent; the compositor's guard already handles this. Tests verify array operations only, not rendering — appropriate for unit scope. |
| W6 | `VideoLoopPlayer` | Frame pacing is the compositor's responsibility; `nextFrame()` returns whatever AVAssetReader has at the moment it's called. If called faster than the video frame rate, duplicate frames are returned (not an error). If called slower, frames are dropped. This is correct behavior for a push-based compositor. |

---

## Security Constraints Verified

| Constraint | Status |
|------------|--------|
| No user content logged | ✅ — no log calls in any scene file |
| Scene file paths not logged | ✅ |
| App Group access via `AppGroup.identifier` constant | ✅ — `SceneManager` uses the constant; file URLs passed by caller |

---

## Test Coverage

| Test | AC | Result |
|------|----|--------|
| `testSceneAssetCodable` | AC1 | ✅ |
| `testSceneTypeCoverage` | AC1 | ✅ |
| `testSceneManagerInitialState` | AC2 | ✅ |
| `testSceneManagerAddOverlay` | AC5, AC6 | ✅ |
| `testSceneManagerMaxOverlays` | AC5 | ✅ |
| `testSceneManagerRemoveOverlay` | AC6 | ✅ |
| `testSceneManagerUpdateOverlayPosition` | AC6 | ✅ |

---

## Open Items Before T06 Can Fully Close

| Item | Owner | Blocker? |
|------|-------|----------|
| On-device: video scene loops seamlessly without frame tear | QA | Yes |
| On-device: SceneManager.currentFrame() feeds StreamCompositor correctly (T08 wiring) | Engineering | Yes — gated on T08 |
| Image scene: failable init failure surfaced in UI | Engineering | No (W4) |
| Apple Developer Team ID | User | Yes |

---

## Verdict

**CONDITIONAL PASS.** No blockers. `VideoLoopPlayer` correctly handles EOF → restart via `setupReader()`, returns `CVPixelBuffer` via `CMSampleBuffer.imageBuffer`. `ImageScenePlayer` correctly pre-renders to CVPixelBuffer in init. `SceneManager` actor enforces the 5-overlay cap and provides `addOverlay`/`removeOverlay`/`updateOverlay` correctly. All 7 unit tests cover the testable pure-logic surface. Compositor integration (SampleHandler wiring) is deferred to T08 as specified.
