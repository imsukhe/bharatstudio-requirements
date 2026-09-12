# L13 — BharatStudio Stream Mirroring: macOS + Windows Desktop Apps

| Field | Value |
|---|---|
| Level | L3 |
| Status | Implemented (2026-08-28) |
| Owner | Platform Engineering |

## Scope

Full screen mirroring desktop applications for macOS (Swift 6/SwiftUI) and Windows (WinUI 3/C#). Both apps receive live video from an iPhone or Android device and display it on the desktop with low latency, recording, and screenshot capabilities.

## Technology Decisions

### macOS
- **Language/Framework:** Swift 6, SwiftUI
- **Minimum OS:** macOS 13.0 (Ventura)+
- **Architecture:** Universal Binary (arm64 + x86_64)
- **iPhone USB capture:** CMIO (Camera Media I/O) virtual device via Apple's built-in USB mirroring stack
- **AirPlay reception:** AirPlay 1 RTSP receiver listening on port 7000; mDNS advertisement via Network framework
- **Decode + display:** VideoToolbox H.264/HEVC hardware decode → AVSampleBufferDisplayLayer (zero-copy GPU path)
- **Audio:** CoreAudio for AirPlay audio; routed from AVSampleBufferAudioRenderer
- **Recording:** AVAssetWriter writing H.264 + AAC into .mp4
- **Android USB:** scrcpy subprocess (bundled binary) over adb
- **Companion TCP:** TCP server on port 27190 receiving stream from CompanionApp (TestStreamDCopy)

### Windows
- **Language/Framework:** C# 12, WinUI 3, Windows App SDK 1.5
- **Runtime:** .NET 8
- **Minimum OS:** Windows 10 22H2 (build 19045)+
- **iPhone USB capture:** libimobiledevice (native DLL bundled) for USB tunnel; SCREAMING host device interface
- **AirPlay reception:** AirPlay 1 RTSP receiver on port 7000; DNS-SD via Bonjour SDK or managed mDNS
- **Decode + display:** MediaFoundation H.264/HEVC software+hardware decode → Direct3D 11 SwapChain panel
- **Audio:** WASAPI for low-latency audio output
- **Recording:** MediaFoundation Sink Writer → .mp4
- **Android USB:** scrcpy subprocess (bundled binary) over adb
- **Companion TCP:** TCP server on port 27190 receiving stream from CompanionApp (TestStreamDCopy)

### Both Platforms
- AirPlay 1 RTSP receiver (port 7000) with per-install random MAC address for AirPlay handshake
- scrcpy integration for Android USB and Android WiFi (wireless scrcpy)
- CompanionApp TCP 27190 connection mode
- License key stored in Keychain (macOS) / Windows Credential Manager (Windows)
- No DRM circumvention; no hardcoded device IDs

## Connection Modes Implemented

| Mode | macOS Path | Windows Path |
|---|---|---|
| iPhone USB | CMIO virtual device | libimobiledevice USB tunnel |
| iPhone WiFi | AirPlay 1 RTSP (port 7000) | AirPlay 1 RTSP (port 7000) |
| Android USB | scrcpy over adb | scrcpy over adb |
| Android WiFi | wireless scrcpy | wireless scrcpy |

## Security

- No DRM circumvention at any layer
- No hardcoded device identifiers; per-install random MAC for AirPlay
- License keys stored in OS credential store (Keychain / Credential Manager)
- No network egress beyond local LAN for mirroring paths

## Acceptance Criteria

1. iPhone USB connects within 5 s of cable plug on the macOS CMIO path
2. AirPlay receiver appears in iOS Control Center → Screen Mirroring after mDNS advertisement
3. Android USB mirrors after `adb devices` shows the device as "device" (authorized)
4. CompanionApp TCP 27190 receives a live stream from the TestStreamDCopy iOS app
5. Recording produces a valid MP4 file with correct bitrate metadata
6. No CPU regression: macOS render path stays under 5% CPU for decode + display of a 1080p30 stream

## Remaining Work (Phase 5)

- Physical device QA on real iPhone hardware (all USB + AirPlay paths)
- Apple Developer code-signing and notarization for macOS distribution
- Windows EV (Extended Validation) code-signing certificate for Windows distribution
- Installer packaging: DMG + pkg for macOS; MSIX or Inno Setup for Windows
