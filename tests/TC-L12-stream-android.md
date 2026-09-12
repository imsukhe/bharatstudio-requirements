# TC-L12 — BharatStudio Stream Android: Acceptance criteria

**Status:** `Draft — awaiting per-WP sign-off`
**Level:** L3
**Task:** [`L12-stream-android.md`](../tasks/L12-stream-android.md)
**Architecture authority:** Doc 153
**Date:** 2026-08-28

---

## How to use this record

Each acceptance criterion block maps to one work package. A WP is `Conditionally complete` when all
automated criteria pass, `Complete` when the physical-device or staging gate evidence is also filed and
reviewed. No WP may be claimed complete without a linked gate-report artifact (Appendix C of Doc 153).

---

## WP-0 — Repository scaffold

| # | Criterion | Method | Pass condition |
|---|---|---|---|
| 0-1 | Gradle build succeeds on all modules | `./gradlew assembleDebug` | Exit 0; zero errors |
| 0-2 | Version catalog present; all deps pinned | Inspect `libs.versions.toml` | No `+` or `SNAPSHOT` in versions |
| 0-3 | Lockfile present and committed | `./gradlew dependencies --write-locks` | `*.lockfile` committed; `--verify-dependencies` passes |
| 0-4 | Dependency-direction rule enforced | CI check (custom Gradle plugin or Forbidden-APIs) | Build fails if `app` imports `transport-*` Android classes |
| 0-5 | Lint passes | `./gradlew lint` | Zero errors, zero high-severity warnings |
| 0-6 | detekt passes | `./gradlew detekt` | Zero violations |
| 0-7 | Unit tests pass on all modules | `./gradlew test` | Exit 0 |
| 0-8 | Secret scan passes | `gitleaks detect` or equivalent | Zero confirmed secrets |
| 0-9 | SBOM skeleton generated | `./gradlew cyclonedxBom` or equivalent | `sbom.json` present; each dep has name/version/license |
| 0-10 | CI pipeline defined and green | GitHub Actions / CI config | All checks green on first commit |

---

## WP-1 — A0 kernel (physical-device gate)

| # | Criterion | Method | Pass condition |
|---|---|---|---|
| 1-1 | FGS start sequence correct | Code review + unit test | `RECORD_AUDIO` check → consent → `startForegroundService` while Activity visible → `startForeground` before `getMediaProjection` |
| 1-2 | MediaProjection token used once, never cached | Code + unit test | Token consumed in `onStartCommand`; null after use |
| 1-3 | Monotonic PTS never resets across reconnect | Unit test (TimestampTracker) | PTS strictly increasing across simulated reconnect |
| 1-4 | A0 gate passed on physical device | Gate report (Doc 153 Appendix C format) | SHIP result; publisher commit/SBOM/license recorded |
| 1-5 | No illegal FGS start from background | Code review | No notification action directly starts capture |

---

## WP-2 — RTMP transport

| # | Criterion | Method | Pass condition |
|---|---|---|---|
| 2-1 | Protocol vector tests pass | `./gradlew :transport-rtmp:test` | All vectors green including extended-timestamp + control-message set |
| 2-2 | TLS rejection test | Unit test | Connection to non-TLS endpoint fails cleanly; no plaintext fallback |
| 2-3 | Reconnect preserves monotonic PTS | Property test | PTS never decreases across N reconnects |
| 2-4 | Queue is bounded; keyframe-aware drop | Unit test | Queue never exceeds configured bound; only non-keyframe frames dropped when full |
| 2-5 | Partial read/write handled | Unit test with truncated buffers | No data corruption on partial I/O |
| 2-6 | Sanitizers pass | Build with ASan/HWASAN (NDK) | Zero memory errors reported |

---

## WP-3 — Broadcast coordinator

| # | Criterion | Method | Pass condition |
|---|---|---|---|
| 3-1 | State-machine exhaustive transitions | Unit test | All valid transitions covered; invalid ones throw/log |
| 3-2 | ABR uses only approved signals | Code review | No carrier/country/time/event in ABR logic |
| 3-3 | No Android imports in `broadcast-core` | CI dependency check | Build fails on any `android.*` import in `broadcast-core` |
| 3-4 | Journal survives process death | Unit test (journal write → simulate kill → read) | `endedUnexpectedly` recoverable; no silent loss |

---

## WP-4 — Audio (A1 gate)

| # | Criterion | Method | Pass condition |
|---|---|---|---|
| 4-1 | `RECORD_AUDIO` checked before AudioRecord | Code + unit test | Correct permission check sequence; no silent fail |
| 4-2 | `(mic \|\| appAudio) ? FOREGROUND_SERVICE_TYPE_MICROPHONE : 0` | Code review | Exact condition used in `startForeground` flags |
| 4-3 | Ring buffer is primitive `ShortArray`, bounded | Code review | No `ArrayDeque<Short>` or unbounded allocation |
| 4-4 | PTS from `AudioRecord.getTimestamp(TIMEBASE_MONOTONIC)` | Code review + unit test | No wall-clock PTS; monotonic clamp applied |
| 4-5 | Mic-only fallback on AudioPlaybackCapture failure | Unit test (mock failure) | Stream continues audio-only via mic; UI shows honest copy |
| 4-6 | A1 gate passed on physical device | Gate report | PASS result with mic + AudioPlaybackCapture + fallback evidence |

---

## WP-5 — Compositor / watermark (A2 gate)

| # | Criterion | Method | Pass condition |
|---|---|---|---|
| 5-1 | Watermark present in encoded output | A2 gate — encoded-output hash comparison | Watermark pixel fingerprint confirmed in encoded frame |
| 5-2 | Rotation-safe: portrait 9:16 and landscape both encode correctly | A2 gate | Both orientations produce valid H.264 stream |
| 5-3 | Density/reconfiguration: no crash on rotation mid-stream | Emulator + physical device | Zero crashes; stream continues after rotate |
| 5-4 | Scene/overlay import validated (no path traversal, no oversized asset) | Unit test | Malformed imports rejected; no exception leaks path |

---

## WP-6 — Encoder admission (A3 gate)

| # | Criterion | Method | Pass condition |
|---|---|---|---|
| 6-1 | Device admitted at correct ladder tier (low/mid/high) | A3 gate on low/mid/high physical devices | Correct preset selected per device class |
| 6-2 | Thermal throttle → graceful downgrade | Thermal stress test | Bitrate reduces; stream continues; no crash/ANR |
| 6-3 | Blacklist persists across restarts | Unit test | Blacklisted encoder not retried after restart |

---

## WP-7 — UI / onboarding / a11y

| # | Criterion | Method | Pass condition |
|---|---|---|---|
| 7-1 | Login required before any streaming feature | UI test | Stream start unavailable until authenticated session established |
| 7-2 | HI (Hindi) strings complete — no English fallback strings | `./gradlew lint` + manual spot-check | Zero missing HI keys |
| 7-3 | a11y: TalkBack navigates all primary flows | Manual TalkBack on physical device | No inaccessible controls; meaningful content descriptions |
| 7-4 | Recovery copy present for all error states | Code review + UI test | Every error state has honest copy + action |
| 7-5 | Compose semantic tests pass | `./gradlew :app:testDebugUnitTest` | Zero failures |

---

## WP-8 — Destination OAuth

| # | Criterion | Method | Pass condition |
|---|---|---|---|
| 8-1 | No embedded WebView OAuth | Code review | All OAuth uses `CustomTabsIntent` or system browser |
| 8-2 | PKCE used for all OAuth flows | Code review | `code_challenge` + `code_verifier` present in all flows |
| 8-3 | OAuth tokens stored Keystore-wrapped in DataStore | Code review | No plaintext token in SharedPreferences / files / logs |
| 8-4 | H.264 viewer playback evidence for each destination | Gate report per destination | Watchable recorded stream confirmed for each advertised destination |
| 8-5 | Stream key / OAuth token never appears in logs | Secret scan + log review | Zero secrets in redacted log artifact |

---

## WP-9 — Platform client / billing / identity (v1, not v1.x)

| # | Criterion | Method | Pass condition |
|---|---|---|---|
| 9-1 | Credential Manager passkey + Google Sign-In only | Code review | No password field; no embedded WebView auth; no SMS-only recovery path |
| 9-2 | Play purchase bound via `setObfuscatedAccountId` | Code review + sandbox test | Correct API usage; server rejects cross-account token |
| 9-3 | Anti-rebinding tombstone: delete-A → create-B → same token refused | Platform staging test | Conflict detected; new binding refused |
| 9-4 | Backup/D2D excludes token/key DataStore | `dataExtractionRules` review + restore test | Restored device shows no valid token; triggers clear-and-reconnect |
| 9-5 | Keystore invalidation → wipe + re-auth | Test: lock-screen change → restart app | `KeyPermanentlyInvalidatedException` caught; stale ciphertext wiped; re-auth prompted |
| 9-6 | Active free stream survives Platform outage | Integration test (mock Platform down) | Stream continues; no termination; reconnects on Platform recovery |
| 9-7 | Platform staging: full lifecycle | Platform staging evidence | Login/passkey/Google/refresh/revocation/outage/replay/account lifecycle all pass |
| 9-8 | Play sandbox: all product types | Sandbox evidence | Pending/cancel/refund/void/restore/conflict/expiry all handled correctly |
| 9-9 | Modified APK cannot obtain server-delivered pack | Security test | Protected value rejected; local-only gates are best-effort only (documented) |

---

## WP-10 — Network resilience / ABR (A7 gate)

| # | Criterion | Method | Pass condition |
|---|---|---|---|
| 10-1 | Network handoff is fresh socket on selected `Network` | Code review | `network.socketFactory` / `network.bindSocket` used; no socket migration |
| 10-2 | ABR uses only approved signals | Code review | No carrier/country/time/event signals |
| 10-3 | 90-minute endurance on Jio/Airtel 4G simulation | A7 gate | Stream alive at 90 min; metrics within SLA; no memory/queue growth |
| 10-4 | Reconnect preserves monotonic PTS | A7 gate | PTS never decreases across measured handoffs |

---

## WP-11 — Observability

| # | Criterion | Method | Pass condition |
|---|---|---|---|
| 11-1 | Zero secrets in redacted log artifact | Automated log scan (RedactingTree) + manual review | No token/key/stream-key/PII in log output |
| 11-2 | Kill-switch exercised in staging | Staging rehearsal | Feature disabled remotely; app degrades gracefully |
| 11-3 | Support bundle contains no raw sensitive data | Manual review of bundle | Diagnostic bundle passes secret-scan |

---

## Cross-cutting (all WPs)

| # | Criterion | Method | Pass condition |
|---|---|---|---|
| X-1 | V-17 validation (Android 17/API 37) | Physical/beta device through A1/A2/A7; `AudioHardening` logcat | Explicit decision: "supported" or "not supported at launch" |
| X-2 | No secret committed to git | `gitleaks` on all commits | Zero confirmed secrets |
| X-3 | SBOM entries complete (name/version/license/CVE-owner) | SBOM review | Every dependency has a CVE owner and license |
| X-4 | Security review before RC | Independent review | Zero open critical/high findings |
