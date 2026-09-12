# L12 — BharatStudio Stream: Android Live Streaming App

**Status:** `Approved for definition — WP-0 implementation authorized; subsequent WPs require per-WP approval`
**Level:** L3
**Owner:** Android lead / streaming / IAP / auth / privacy / security
**Repository:** `bharatstudio-stream-android`
**Architecture authority:** Doc 153 (`153-Android-Live-Streaming-0-to-1-MASTER.md`)
**Platform identity authority:** `pending/platform/PLATFORM-00-SHARED-IDENTITY-AND-ENTITLEMENTS-AUTHORITY.md`
**Blocks:** Android Play Store v1 streaming launch
**Opened:** 2026-08-28
**Last updated:** 2026-08-28

---

## Objective

Ship BharatStudio Stream — a mobile-first Android live streaming app that lets mobile gamers stream to YouTube, Twitch, Kick, Facebook, and custom RTMP directly from their Android device, with no PC or OBS required.

**Wedge:** "Go live from mobile gameplay, no PC/OBS. Starts every time. Tells you the truth."
**Launch market:** India-first private beta, then SEA → MENA → LatAm → US/UK/EU.

---

## Scope change record (2026-08-28)

Owner direction issued 2026-08-28 (interactive session, system prompt): **BharatStudio login is mandatory for free and paid users.** This reverses Doc 153 §10.3.1/B8's prior framing ("Gated on backend existence; no v1 free-streaming impact") and amends PLATFORM-00's "Free local streaming is account-free" to mean the **stream transport path** does not call Platform — but **app access** requires an authenticated session.

Reconciled interpretation (all three remain true):
1. Login is required at first launch and on session expiry before any streaming feature is accessible.
2. The active stream encode/capture/RTMP transport path never calls Platform.
3. An active free stream must not be terminated solely because Platform becomes temporarily unreachable while streaming (use approved offline-grace model from §10.3.1).

This is recorded as DL-6 in Doc 153 Appendix F. WP-9 is now a v1 requirement (not v1.x), though its implementation is still gated on Platform contract existence.

---

## Locked decisions (from Doc 153 — do not re-litigate)

| Decision | Value |
|---|---|
| Module structure | `app`, `broadcast-core`, `broadcast-android`, `transport-rtmp`, `data`, `backend-contract`, `test-fixtures`; dependency direction downward only |
| Codec v1 | H.264/AVC + AAC-LC |
| Transport v1 | RTMPS (RTMP over TLS) |
| Audio | Mic + AudioPlaybackCapture mixed; 48 kHz mono; mic-only fallback |
| ABR | Measured-signal only (encoder/queue/ack/RTT/reconnect) |
| FGS order | `RECORD_AUDIO` granted → projection consent → `startForegroundService` while Activity visible → `startForeground` with correct types → `getMediaProjection` + `AudioRecord` |
| Microphone FGS type | `(mic \|\| appAudio) ? FOREGROUND_SERVICE_TYPE_MICROPHONE : 0` |
| Identity | Credential Manager passkey-first + Google Sign-In; no passwords; no embedded WebView auth |
| Pricing catalogue | ₹9/day · ₹19/week · ₹49/month · ₹139/3-month · ₹249/6-month · ₹499/year |
| Free tier | Custom RTMP; portrait; HI+EN; watermark on; 720p max |
| Login scope | Required at app entry for all users including free; stream transport path never calls Platform |
| Deferred | HEVC (A4/v1.x), face-cam (A5/v1.x), SRT/RIST/FEC (A6/v2), relay/multistream/cloud |

---

## Work package sequence

| ID | Name | Status | Gate | Blocks |
|---|---|---|---|---|
| WP-0 | Repository scaffold (Gradle multi-module, version catalog/lockfile/SBOM, CI, security baseline) | 🔵 Authorized — in progress | — | All |
| WP-1 | A0 kernel spike (projection → EGL → H.264 → RTMPS; publisher selection) | ⚪ Pending WP-0 | A0 | WP-2, WP-3 |
| WP-2 | Production RTMP transport | ⚪ Pending WP-1/A0 | Protocol vectors + TLS | WP-3 |
| WP-3 | Broadcast coordinator, session lifecycle, journal, capability model | ⚪ Pending WP-1 | State-machine tests | WP-4–WP-11 |
| WP-4 | Audio system (mic + playback capture, ring buffers, AAC-LC, monotonic PTS) | ⚪ Pending WP-3 | A1 | WP-5 |
| WP-5 | EGL compositor, scenes, overlays, watermark, rotation | ⚪ Pending WP-3 | A2 | WP-6 |
| WP-6 | MediaCodec device admission, low-end ladder, thermal/memory safety | ⚪ Pending WP-3 | A3 | WP-7 |
| WP-7 | Compose UI, login/onboarding/account/settings, EN+HI, a11y | ⚪ Pending WP-9 skeleton | Compose/a11y tests | WP-9 |
| WP-8 | Destination OAuth + Custom RTMP; H.264 viewer playback/VOD proof | ⚪ Pending WP-3 | Per-destination login verified | WP-9 |
| WP-9 | Platform client (Credential Manager, Play Billing, entitlement, account lifecycle) | ⚪ Pending Platform contract | Platform staging evidence | WP-7, RC |
| WP-10 | ABR + network handoff + 90-min endurance | ⚪ Pending WP-3 | A7 | RC |
| WP-11 | Telemetry, log redaction, dashboards, support bundle, kill-switch | ⚪ Pending WP-3 | Zero secrets in log; kill-switch exercised | RC |

---

## Required release gates (all must pass before RC)

- A0 publisher selection with physical-device evidence
- A1 audio evidence (mic + AudioPlaybackCapture + fallback)
- A2 compositor/watermark/rotation evidence
- A3 low/mid/high device admission evidence
- A7 ABR/handoff/90-min endurance evidence
- H.264 viewer playback + VOD/replay for each advertised destination (YouTube/Twitch/Kick/Facebook/Custom RTMP)
- Platform staging: login, passkey, Google auth, token refresh/revocation, outage, replay, account lifecycle
- Play sandbox: all product types, pending/cancel/refund/void/restore/conflict/expiry
- V-17 physical/beta validation before claiming Android 17 support

---

## Explicitly deferred (not Android v1 — retain gate/evidence wording)

- HEVC default → A4/v1.x
- Face-cam → A5/v1.x
- SRT/RIST/FEC/MPEG-TS → A6/v2
- Relay, multistream, cloud recording, server-side UPI Alerts

---

## Open approvals (Appendix B of Doc 153)

B1 Pricing · B2 Entitlement matrix · B3 Data retention + tombstone window · B4 Region/consent content
B5 Stale-patch policy · B6 OEM battery-opt prompt · B7 Portrait toggle UX · B8 Backend identity detail (now v1, not v1.x)

---

## Predecessor / dependencies

| Dependency | Status | Owned by |
|---|---|---|
| Platform API contract published | ⚠ Pending — `bharatstudio-platform` does not yet exist | Platform owner |
| Play Console app created; product IDs configured | ⚠ Pending | Project owner |
| Android signing keystore (upload + release) | ⚠ Pending | Project owner |
| Physical test devices (Android 10–16 matrix + Android 17 beta) | ⚠ Pending | Android lead |
| Destination developer accounts (YouTube / Twitch / Kick / Facebook) | ⚠ Pending | Project owner |
