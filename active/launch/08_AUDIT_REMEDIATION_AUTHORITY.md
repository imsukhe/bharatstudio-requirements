# Audit remediation authority — checkout and overlay recovery

**Status:** `Approved for implementation by project owner — verification remains required`  
**Owner:** **Sukhdev Singh**  
**Date:** 2026-09-18  
**Applies to:** BharatStudio Alerts v1 checkout and browser-source overlay runtime  
**Parent authorities:** `00_LAUNCH_SCOPE_AUTHORITY.md`, `01_MASTER_RELEASE_AUTHORITY.md`, and `06_BACKEND_GAP_REMEDIATION_AUTHORITY.md`

## Owner approval and purpose

The project owner asked to start fixing the source-confirmed checkout and overlay
findings reported in the 2026-09-18 code-level end-to-end audit. This authority
approves corrective work only. It does not change a price, payment provider,
entitlement, retention period, legal posture, deployment target, or public product
promise.

Every child task must retain the existing invariants: payment truth remains the
verified provider/webhook and append-only ledger; durable replay remains the overlay
correctness path; an outage may delay a visual update but may not manufacture or drop
accepted payment evidence; and browser clients never receive private provider secrets.

## Approved corrective requirements

| ID | Requirement | Data and security boundary | External gate |
|---|---|---|---|
| AUD-PAY-01 | Both public checkout journeys obtain a Cloudflare Turnstile response when a browser-visible site key is configured, send it only to the existing order endpoint, and never start an order without it when verification is configured. | Token is ephemeral, not persisted, not logged, and is sent only to the existing API. The site key is public; the verification secret remains API-only. | A real Cloudflare site key paired to the configured API secret must be supplied in a non-production/prod deployment before that environment can be claimed ready. |
| AUD-OVL-01 | A standalone overlay resolves API-owned TTS artifacts against its configured API origin, not the web-page origin. | Existing fragment token/bearer request only; no new data or route. | Browser/OBS rehearsal remains external evidence. |
| AUD-MC-01 | Master Canvas retries a failed initial module/layout read on its existing shared transport lifecycle and refreshes server-authoritative module entitlement/layout without adding a transport per module. | Existing overlay token and scoped reads only; fail closed while confirmation is unavailable. | Browser/OBS recovery rehearsal remains external evidence. |
| AUD-SB-01 | Safe Soundboard cannot replay an old latest-record merely because a module was hidden/shown, and a creator trigger invalidates an idle Canvas promptly through the existing overlay wake-up path. | Creator-owned clip metadata only; no viewer identity, content-review claim, or new storage. | CDN/GCS configuration and browser audio-autoplay evidence remain separate gates. |
| AUD-RT-03 | A post-registration direct-listener loss cannot be represented as healthy; affected overlay waits use bounded durable-replay fallback until listener recovery is confirmed. | Existing channel IDs and overlay-session metadata only; no new personal data. | Real PostgreSQL/network-loss rehearsal remains external evidence. |
| AUD-PAY-02 | A TipIntent must not become used until the same durable, idempotent payment-order attempt has succeeded; transient order failures remain safely retryable with the original key, while a different key cannot create a second order. The direct tip form must retain its attempt key across Razorpay dismissal/failure rather than minting a new order. | The existing opaque token/hash, order UUID, idempotency key and anonymous cookie hash are reused. No card/bank data, provider secret or new browser-stored identity is introduced. | Real payment-provider sandbox, timeout/unknown-outcome and browser checkout evidence remains external. |

## Boundaries and rollback

- No existing migration will be edited, moved, or squashed. A migration is allowed
  only if a child task proves it needs a new durable invariant; none is authorised by
  `AUD-PAY-01`.
- No production deployment, credential, Cloudflare configuration, Razorpay action,
  or external call is authorised by this authority.
- Each child task names its exact file rollback. Code rollback is a normal source
  revert; any future database reversal must be a new forward migration.
- The authority is not proof of staging, provider, OBS/device, accessibility, legal,
  tax, or production readiness.

## Evidence and closure

Each task needs a linked task, acceptance record, and review record before code. It
may become `Conditionally complete` only after relevant deterministic checks, a fresh
hostile review, reproducible redacted evidence, and traceability/doc-consistency
reconciliation. Independent review is not implied by self-review.
