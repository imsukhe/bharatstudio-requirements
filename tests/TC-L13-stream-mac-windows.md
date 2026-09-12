# TC-L13 — Test Cases: BharatStudio Stream Mirroring macOS + Windows

Covers acceptance criteria defined in `tasks/L13-stream-mac-windows.md`.

---

## TC-L13-01: iPhone USB → Mac CMIO Connection

**Platforms:** macOS  
**Preconditions:** iPhone running iOS 16+; USB cable; Mac running the app; no prior trust prompt pending.

**Steps:**
1. Plug iPhone into Mac via USB.
2. On iPhone, tap "Trust This Computer" when prompted.
3. In BharatStudio Mirror, select "iPhone USB" from the source picker.

**Expected:**
- Stream appears on screen within 5 seconds of the trust tap.
- Status bar shows "iPhone USB — Connected" and a live FPS counter.

**Pass criteria:** Stream visible within 5 s; no crash; FPS ≥ 24.

---

## TC-L13-02: iPhone AirPlay → Mac

**Platforms:** macOS  
**Preconditions:** iPhone and Mac on the same Wi-Fi network; app running.

**Steps:**
1. Launch BharatStudio Mirror — it advertises via mDNS automatically.
2. On iPhone, open Control Center → Screen Mirroring.
3. Tap "BharatStudio Mirror" in the device list.

**Expected:**
- iPhone screen appears on Mac within 3 s of tapping.
- Audio (if enabled) plays through Mac speakers.
- Status bar shows "AirPlay — Connected".

**Pass criteria:** Device appears in Screen Mirroring list; stream starts without error.

---

## TC-L13-03: Android USB → Mac scrcpy Connection

**Platforms:** macOS  
**Preconditions:** Android phone with USB debugging enabled; adb installed and in PATH; USB cable.

**Steps:**
1. Plug Android into Mac.
2. Run `adb devices` — confirm device shows as "device" (authorized).
3. In BharatStudio Mirror, select "Android USB" from the source picker.

**Expected:**
- scrcpy subprocess launches and stream appears within 5 s.
- Status bar shows "Android USB — Connected".

**Pass criteria:** Stream visible; scrcpy subprocess exits cleanly when source is changed.

---

## TC-L13-04: Companion App TCP 27190 → Mac Receiver

**Platforms:** macOS  
**Preconditions:** TestStreamDCopy iOS app on iPhone configured to stream to Mac IP; Mac running BharatStudio Mirror with Companion App mode selected.

**Steps:**
1. In BharatStudio Mirror, enable "Companion App" mode — TCP listener starts on port 27190.
2. On iPhone, open TestStreamDCopy, enter Mac IP, tap "Start Stream".

**Expected:**
- Mac receives TCP connection on port 27190.
- Stream decoded and displayed within 2 s of connection.
- Status bar shows "Companion TCP — Connected".

**Pass criteria:** Stream visible; no dropped-connection errors in log for a 60 s session.

---

## TC-L13-05: All Four Connection Modes on Windows

**Platforms:** Windows  
**Preconditions:** Same as TC-L13-01 through TC-L13-04, on a Windows 10 22H2+ machine.

**Steps:** Repeat TC-L13-01, TC-L13-02, TC-L13-03, and TC-L13-04 on Windows using BharatStudio Mirror (Windows build).

**Expected:** Each mode behaves identically to the macOS counterpart within the same timing thresholds.

**Pass criteria:** All four modes pass; libimobiledevice DLL loads without error; MediaFoundation decoder initializes for H.264.

---

## TC-L13-06: Cable Unplug → Reconnect FSM

**Platforms:** macOS, Windows  
**Preconditions:** Active iPhone USB stream in progress.

**Steps:**
1. Unplug USB cable during an active stream.
2. Observe UI — should show "Disconnected / Reconnecting…" state.
3. Plug cable back in within 30 s.

**Expected:**
- Stream pauses and reconnecting indicator appears within 1 s of unplug.
- Stream resumes automatically within 10 s of reconnect without user interaction.
- No crash; session state (recording if active) preserved.

**Pass criteria:** Reconnection succeeds within 10 s; FSM returns to "Connected" state.

---

## TC-L13-07: Recording Start/Stop → Valid MP4

**Platforms:** macOS, Windows  
**Preconditions:** Active stream of any connection mode.

**Steps:**
1. Click "Record" button — recording indicator appears.
2. Let recording run for 30 s.
3. Click "Stop Recording".
4. Locate output file in the configured output directory.

**Expected:**
- MP4 file created with a timestamped name.
- File opens in QuickTime / Windows Media Player without errors.
- `ffprobe` reports correct video codec (H.264), duration ~30 s, and non-zero bitrate.
- Audio track present if source had audio.

**Pass criteria:** Valid MP4 produced; duration within ±2 s of actual recording length; file not corrupt.

---

## TC-L13-08: Screenshot Saved Correctly

**Platforms:** macOS, Windows  
**Preconditions:** Active stream.

**Steps:**
1. Click "Screenshot" button (or keyboard shortcut).
2. Locate output file in the configured output directory.

**Expected:**
- PNG file created with a timestamped name.
- Image dimensions match the stream resolution.
- File is not blank or corrupt.

**Pass criteria:** PNG opens correctly; non-zero pixel content; saved within 1 s of button press.

---

## TC-L13-09: FPS/Bitrate Stats Displayed Correctly

**Platforms:** macOS, Windows  
**Preconditions:** Active stream.

**Steps:**
1. Enable stats overlay (toggle in UI or View menu).
2. Observe stats for 10 s.

**Expected:**
- FPS counter updates every second and reflects actual decoded frame rate (e.g., 30 fps ± 2).
- Bitrate figure updates every second and is non-zero for an active stream.
- Stats overlay does not noticeably impact CPU usage (no > 1% increase).

**Pass criteria:** FPS and bitrate both non-zero and updating; values plausible for the stream source.

---

## TC-L13-10: iOS Developer Mode NOT Required for Any Working Path

**Platforms:** macOS, Windows  
**Preconditions:** iPhone with Developer Mode OFF (Settings → Privacy & Security → Developer Mode = off).

**Steps:**
1. Connect iPhone via USB with Developer Mode disabled.
2. Verify CMIO / libimobiledevice USB path streams successfully.
3. Connect iPhone via AirPlay (Wi-Fi) with Developer Mode disabled.
4. Verify AirPlay path streams successfully.

**Expected:**
- Both USB and AirPlay paths function without prompting the user to enable Developer Mode.
- No error message referencing Developer Mode appears in the app.

**Pass criteria:** Full stream works on a stock consumer iPhone with Developer Mode off; log contains no "developer mode required" warning.
