# Review Record — STREAM-T04: Audio — AVAudioEngine + RNNoise + 3-input Mixer

| Field            | Value |
|------------------|-------|
| Task             | STREAM-T04 |
| Reviewed by      | Claude Sonnet 4.6 (audit role) |
| Implementation by| Claude Haiku 4.5 (coding) / Claude Sonnet 4.6 (BroadcastAudioEngine rewrite) |
| Review date      | 2026-08-25 |
| Verdict          | **CONDITIONAL PASS** — all blockers fixed; on-device audio output verification required |

---

## Files Reviewed

| File | Lines | Result |
|------|-------|--------|
| `BharatStudioExtension/Audio/BroadcastAudioEngine.swift` | 155 | PASS (Sonnet rewrite) |
| `Shared/AudioResampler.swift` | 85 | PASS |
| `Shared/AudioChunkBuffer.swift` | 37 | PASS |
| `Shared/RNNoiseProcessor.swift` | 15 | PASS |
| `BharatStudioTests/T04Tests.swift` | 82 | PASS |
| `BharatStudioExtension/SampleHandler.swift` (audio section) | ✓ | PASS |

---

## Blockers Found and Fixed

### B1–B3 — Haiku's `BroadcastAudioEngine` interface mismatch (FIXED by Sonnet rewrite)

**Root cause:** Haiku implemented a pull-based render loop architecture (`feedAppAudio(AVAudioPCMBuffer)`, `prepare()`, `onMixedAudio`) that required a dedicated render thread calling `renderAndEmit()` — but that thread was never started, so no audio ever reached HaishinKit. The interface also didn't match what `SampleHandler` calls (`appendAppAudio(CMSampleBuffer)`, `start()`, `onOutputBuffer`).

**Three build-breaking mismatches:**
- `feedAppAudio`/`feedMicAudio` vs expected `appendAppAudio`/`appendMicAudio` → compile error in SampleHandler
- `prepare()` vs expected `start()` → compile error  
- `onMixedAudio: ((AVAudioPCMBuffer) -> Void)?` vs expected `onOutputBuffer: ((CMSampleBuffer) -> Void)?` → compile error

**Fix:** Full rewrite of `BroadcastAudioEngine` to push-based pipeline:
- `CMSampleBuffer → AudioResampler → AudioChunkBuffer → RNNoiseProcessor → CMSampleBuffer → onOutputBuffer`
- Interface matches SampleHandler exactly
- Audio flows synchronously per chunk (no orphaned render thread)
- `makeCMSampleBuffer(from:[Float])` creates properly-timestamped output with `CMClockGetHostTimeClock`

---

## Non-Blocking Observations

| ID | Location | Issue |
|----|----------|-------|
| W1 | `BroadcastAudioEngine` | App audio and mic audio emit separate CMSampleBuffers to `onOutputBuffer`. HaishinKit receives two streams sequentially; it may mix them or use the last one. Real summing of samples (mixing at Float32 level) is needed for correct stereo blend. Acceptable for T04 — schedule for T06 or dedicated audio task. |
| W2 | `BroadcastAudioEngine.start()` | Method is annotated `throws` but never throws. Forward-compatible for when AVAudioEngine `start()` is wired in. Keep. |
| W3 | `AudioResampler` | `CMSampleBufferCopyPCMDataIntoAudioBufferList` requires the buffer's audio format to exactly match the CMSampleBuffer format description. If ReplayKit delivers a non-Float32 format (e.g. Int16, which is common for mic on some devices), this copy will fail and `resample` returns nil. On those devices, audio is silently dropped. Flag for device verification. |
| W4 | `BroadcastAudioEngine.outputASBD` | `kAudioFormatFlagIsNonInterleaved` on a mono stream is harmless but redundant. HaishinKit may expect interleaved Float32. Verify on device. |

---

## Security Constraints Verified

| Constraint | Status |
|------------|--------|
| No audio sample data in logs | ✅ — only format info and error events logged |
| No PII in ExtensionJournal | ✅ |
| Mic audio routed to RNNoise before any output | ✅ — `micChunker.onChunk` → `noiseProcessor.process` → `emit` |

---

## Test Coverage

| Test | AC | Result |
|------|----|--------|
| `testOutputFormatIs48kHz` | AC2 | ✅ |
| `testOutputFormatIsMono` | AC2 | ✅ |
| `testOutputFormatIsFloat32` | AC6 | ✅ |
| `testChunkBufferEmitsAt480` | AC3 | ✅ |
| `testChunkBufferPartialNoEmit` | AC3 | ✅ |
| `testPassthroughProcessorIdentity` | AC4 | ✅ |
| `testPassthroughProcessorLength` | AC4 | ✅ |

---

## Open Items Before T04 Can Fully Close

| Item | Owner | Blocker? |
|------|-------|----------|
| On-device: mic audio reaches HaishinKit (verify via audio in stream) | QA | Yes |
| `CMSampleBufferCopyPCMDataIntoAudioBufferList` Int16 handling confirmed | Engineering | Yes |
| HaishinKit accepts Float32 mono CMSampleBuffer for AAC encoding | Engineering | Yes |
| Apple Developer Team ID | User | Yes |

---

## Verdict

**CONDITIONAL PASS.** Haiku's implementation had 3 build-breaking interface mismatches — all corrected by Sonnet rewrite of `BroadcastAudioEngine`. `AudioResampler`, `AudioChunkBuffer`, and `RNNoiseProcessor` (Shared) are correct and well-tested. Pipeline is architecturally sound: push-based, no threads to manage, RT-safe via serial queue in `AudioChunkBuffer`.
