# L11 — BharatStudio Stream: iOS Live Streaming App

**Status:** `In progress — STREAM-T01 executing`  
**Level:** L3  
**Owner:** iOS / streaming / IAP / auth / privacy  
**Repository:** `bharatstudio-stream-ios`  
**Architecture authority:** Doc 134 (`134-iOS-Live-Streaming-MASTER.md`)  
**Feasibility gate plan:** Doc 136 (`136-iOS-Streaming-Feasibility-Spike-Plan.md`)  
**UI/UX spec:** Doc 137 (`137-iOS-UIUX-Design-System-Evidence-Based-Spec.md`)  
**Blocks:** iOS App Store v1 streaming launch

---

## Objective

Ship BharatStudio Stream — a mobile-first iOS live streaming app that lets mobile gamers stream to YouTube, Twitch, Facebook Live, and Kick directly from their iPhone, with no PC or OBS required.

**Wedge**: "Go live from mobile gameplay, no PC/OBS."  
**Launch market**: India-first private beta (30–50 creators), then SEA → MENA → LatAm → US/UK/EU.

---

## Locked decisions (from Doc 134 — do not re-litigate)

| Decision | Value |
|---|---|
| Extension architecture | Approach B: extension-only pipeline, no background-audio keepalive |
| RTMP library | HaishinKit (MIT); ADR 001 signed |
| Video codec | H.264 v1; H.265 gated (Doc 136 S1) |
| Audio | AVAudioEngine manual-rendering in br.appex; RNNoise at 48kHz/480-sample mono |
| ABR | Protocol-split: RTMP send-buffer / SRT bstats; Larix thresholds |
| Entitlement v1 | On-device StoreKit 2 (deterrent, not DRM) |
| Watermark | Last compositor layer; snapshotted at Go Live; corner-shift every 3min |
| Pricing | ₹19d / ₹49w / ₹99m / ₹279q / ₹999y |
| Global arch | Market-policy layer; no `if country == "India"` in code |
| Localization | 21 languages / 6 tiers (en+hi ship in v1) |
| BharatStudio login | Mandatory for all tiers (free + paid) — no anonymous streaming |

---

## Task sequence

| ID | Name | Status | Blocks |
|---|---|---|---|
| STREAM-T01 | Core pipeline: ReplayKit + HaishinKit + H.264 → RTMPS | 🟡 Conditional pass — on-device gate pending | All |
| STREAM-T02 | Multi-platform RTMPS + reconnect + observability | 🟡 Conditional pass — on-device gate pending | T03 |
| STREAM-T03 | Metal compositor + free-tier watermark + ABR wiring | 🟡 Conditional pass — device build verification pending | T04 |
| STREAM-T04 | Audio: AAC + RNNoise + 3-input mixer | 🟡 Conditional pass — on-device audio verification pending | T05 |
| STREAM-T05 | Chat: Twitch IRC/EventSub + YouTube Data API | 🟡 Conditional pass — on-device chat integration verification pending | T07 |
| STREAM-T06 | Scenes (AVAssetReader loop) + overlays | 🟡 Conditional pass — on-device video loop + compositor wiring verification pending | T08 |
| STREAM-T07 | OAuth × 4 platforms (Twitch/YouTube/Kick/Facebook) | 🟡 Conditional pass — on-device OAuth flow verification pending | T08 |
| STREAM-T08 | Full settings UI + AVSampleBuffer preview + onboarding | 🟡 Conditional pass — on-device UI verification + deployment target confirmation pending | T09 |
| STREAM-T09 | StoreKit 2 IAP full wiring + entitlement enforcement | 🟡 Conditional pass — StoreKit sandbox + on-device entitlement enforcement verification pending | T10 |
| STREAM-T10 | Device/carrier QA matrix + App Store submission | 🟡 Conditional pass — physical QA + Apple Developer credentials required | Launch |

---

## Phase-0 feasibility gates (Doc 136) — must run in parallel with T01

| Gate ID | What | Fallback |
|---|---|---|
| S0 | RTMP + H.264 + extension stability on device | — (must pass) |
| S1 | H.265/Enhanced RTMP per platform | Ship H.264 only |
| S2 | Face cam + ReplayKit simultaneously | No face cam v1 |
| S3 | SRT + FEC | SRT without FEC |
| S4 | Global ABR reliability matrix | Fixed conservative presets |

---

## Test record

[`../tests/TC-L11-stream-ios.md`](../tests/TC-L11-stream-ios.md) — one record per task; evidence appended as tasks complete.

## Review record

[`../reviews/`](../reviews/) — Sonnet 4.6 review after each task closes.

---

## Mandatory login — approved 2026-08-28

BharatStudio login is mandatory before a user can set up or use any streaming features,
including the free plan. This replaces any prior assumption that free streaming is account-free.

Supported identity methods:
- Sign in with Apple (required for App Store submission)
- Google Sign-In (ASWebAuthenticationSession + PKCE)
- Passkeys (ASAuthorizationPlatformPublicKeyCredentialProvider)

One immutable `bharatstudio_user_id` shared across iOS, Android, Alerts, and future web.
BharatStudio identity is separate from destination OAuth (YouTube/Twitch/Kick/Facebook).
