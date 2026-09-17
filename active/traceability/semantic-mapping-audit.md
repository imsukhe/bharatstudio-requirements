# Step 0 semantic mapping audit

Generated from `active/traceability/register-map.tsv`; mapping inventory only.

| ID | Section | Lifecycle | Basis / missing behavior | Targets |
|---|---|---|---|---|
| PAY-01 | register | mapped-existing | L04 task/test/review trio covers §31.2 atomic order→webhook→ledger→alert boundary; local migration and provider fixture evidence is recorded; external provider/staging gates remain open | tasks/L04-go-payment-boundary.md, tests/TC-L04-go-payment-boundary.md, reviews/2026-08-14-L04-provider-boundary-review.md |
| PAY-10 | register | new-record-required | Missing from reviewed L-track evidence: Donor-safe status projection (UUID, amount, INR, state, updated) | - |
| PAY-11 | register | new-record-required | Missing from reviewed L-track evidence: Payments ledger + CSV export (explicitly not a CA tax report) — **untiered and uncapped**, §12.6 | - |
| PAY-12 | register | new-record-required | Missing from reviewed L-track evidence: Provider capability snapshots; features gate on capability, not name | - |
| PAY-13 | register | new-record-required | Missing from reviewed L-track evidence: Razorpay partner OAuth | - |
| PAY-14 | register | new-record-required | Missing from reviewed L-track evidence: Payment account activation | - |
| PAY-15 | register | new-record-required | Missing from reviewed L-track evidence: Reconciliation sweep + refund sweep actually running | - |
| PAY-16 | register | new-record-required | Missing from reviewed L-track evidence: Manual-review quarantine resolution UI | - |
| PAY-17 | register | new-record-required | Missing from reviewed L-track evidence: Dynamic **Order QR** on the tip page — server side exists, the surface half does not (§8.2.1) | - |
| QR-01 | register | new-record-required | Missing from reviewed L-track evidence: **Three QR kinds** implemented distinctly: Channel QR (tip-page short link), Order QR (one payment, expiring), Campaign QR (campaign page) | - |
| QR-02 | register | new-record-required | Missing from reviewed L-track evidence: **The overlay QR is always a Channel QR** — an Order QR on stream would expire mid-scan, bind every viewer to one stranger's order, and break on reload | - |
| QR-03 | register | new-record-required | Missing from reviewed L-track evidence: A Channel QR never embeds an amount; a Campaign QR may carry a suggested amount as a page parameter the supporter can change; an Order QR carries the exact amount | - |
| QR-04 | register | new-record-required | Missing from reviewed L-track evidence: Order QR shows remaining validity and offers one explicit regeneration — never a silent refresh mid-scan | - |
| QR-05 | register | new-record-required | Missing from reviewed L-track evidence: Rotating the channel short link invalidates every Channel QR in circulation: confirmation naming that consequence, and audited | - |
| QR-06 | register | new-record-required | Missing from reviewed L-track evidence: Device routing — mobile UPI Intent, desktop Order QR, tablet offers both rather than guessing | - |
| QR-07 | register | new-record-required | Missing from reviewed L-track evidence: **UPI-intent return path proven on real devices** across Android, iOS and several UPI apps; a supporter who does not return cleanly still lands on a page that tells them the truth (`ENV-05`) | - |
| QR-08 | register | new-record-required | Missing from reviewed L-track evidence: Preferred-app memory: the **browser half** (server allowlist exists). Stores which app was chosen, never a credential or account identifier, per device | - |
| QR-09 | register | new-record-required | Missing from reviewed L-track evidence: A return from a UPI app is **never** success — only the HMAC-verified webhook confirms (`PAY-02`) | - |
| QR-10 | register | new-record-required | Missing from reviewed L-track evidence: Honest waiting state with a bounded wait, then a recovery screen carrying the receipt link | - |
| QR-11 | register | new-record-required | Missing from reviewed L-track evidence: Receipt link works with no login, from any device, at any later time (`VID-04`) | - |
| QR-12 | register | new-record-required | Missing from reviewed L-track evidence: QR download and copy from the tip-page editor and the §7.3 copy affordances, at print resolution | - |
| QR-13 | register | new-record-required | Missing from reviewed L-track evidence: Per-attempt funnel record: path offered, path taken, app chosen where the OS reports it, return completed, intent-to-webhook time, failure class. **No account identifiers, no VPAs, no banking data** | - |
| QR-14 | register | new-record-required | Missing from reviewed L-track evidence: Payment path functional with JavaScript degraded — a link and a QR always work (§19.9) | - |
| QR-15 | register | new-record-required | Missing from reviewed L-track evidence: No "mark as paid", no generic QR fallback, no screenshot-based confirmation | - |
| PAY-18 | register | new-record-required | Missing from reviewed L-track evidence: Preferred UPI app memory (browser half) | - |
| PAY-19 | register | new-record-required | Missing from reviewed L-track evidence: Direct UPI intent `upi://pay?pa&pn&tr&am&cu` | - |
| PAY-20 | register | new-record-required | Missing from reviewed L-track evidence: Payout/settlement status visible to creator | - |
| PAY-21 | register | new-record-required | Missing from reviewed L-track evidence: Payment failure classification surfaced to creator | - |
| PAY-22 | register | new-record-required | Missing from reviewed L-track evidence: Subscriptions: annual = 10 months charged / 12 served | - |
| PAY-23 | register | new-record-required | Missing from reviewed L-track evidence: Past-due 30-day grace preserves price; rejoin at current pricing | - |
| PAY-24 | register | new-record-required | Missing from reviewed L-track evidence: Downgrade pauses newest queues, never deletes; `paused_reason` distinguishes cause | - |
| PAY-25 | register | new-record-required | Missing from reviewed L-track evidence: Referral credit = service-time (30-day reward, 14-day hold, 5/30-day cap, 12 banked, same-subnet fraud signal) | - |
| PAY-26 | register | new-record-required | Missing from reviewed L-track evidence: Top-up purchase, ledger and balances (§10.2) | - |
| PAY-27 | register | new-record-required | Missing from reviewed L-track evidence: Season Passes (§10.4) | - |
| PAY-30 | register | new-record-required | Missing from reviewed L-track evidence: Paid room-code unlocking | - |
| PAY-28 | register | new-record-required | Missing from reviewed L-track evidence: Paytm / Cashfree / PhonePe | - |
| PAY-29 | register | new-record-required | Missing from reviewed L-track evidence: Recurring memberships | - |
| ALQ-01 | register | mapped-existing | L05 task/test/review trio covers §31.3 durable queues, outbox, per-queue deliveries and independent sequence/progress; migration 0004 and multi-queue harness evidence are recorded | tasks/L05-go-alert-worker-and-cloud-tasks.md, tests/TC-L05-go-alert-worker-and-cloud-tasks.md, reviews/2026-08-14-L05-worker-boundary-review.md |
| ALQ-02 | register | mapped-existing | L05 task/test/review trio covers §31.3 overlay SSE, Last-Event-Id cursor replay and acknowledgement boundary; migration 0022 and reconnect/replay harness evidence are recorded | tasks/L05-go-alert-worker-and-cloud-tasks.md, tests/TC-L05-go-alert-worker-and-cloud-tasks.md, reviews/2026-08-14-L05-worker-boundary-review.md |
| ALQ-03 | register | mapped-existing | L05 task/test/review trio covers §31.3 cross-replica LISTEN/NOTIFY wake-up with two independent listeners and durable replay as correctness path; L05-32 integration evidence is recorded | tasks/L05-go-alert-worker-and-cloud-tasks.md, tests/TC-L05-go-alert-worker-and-cloud-tasks.md, reviews/2026-08-14-L05-worker-boundary-review.md |
| ALQ-04 | register | mapped-existing | L03 task/test/review trio covers §31.3 direct DATABASE_URL_DIRECT listener separation, pooled LISTEN rejection, and durable replay correctness; L03-07a/07c integration evidence is recorded | tasks/L03-alerts-web-and-creator-api.md, tests/TC-L03-alerts-web-and-creator-api.md, reviews/2026-08-14-L03-definition-review.md |
| ALQ-05 | register | mapped-existing | L03 task/test/review trio covers §31.3 server FIFO/priority-with-aging and client stacked/pills/aggregated grouping; corrected L03 findings review and L03-27 evidence are recorded | tasks/L03-alerts-web-and-creator-api.md, tests/TC-L03-alerts-web-and-creator-api.md, reviews/2026-08-16-L03-corrected-findings-remediation-review.md |
| ALQ-06 | register | mapped-existing | L03 task/test/review trio covers §31.3 quiet/approval/rate/hold/no-drop semantics; corrected L03 findings review and L03-26/L03-27 evidence are recorded | tasks/L03-alerts-web-and-creator-api.md, tests/TC-L03-alerts-web-and-creator-api.md, reviews/2026-08-16-L03-corrected-findings-remediation-review.md |
| ALQ-07 | register | mapped-existing | L05 task/test/review trio covers §31.3 no-drop behavior across queue limits and subscription tiers; L05-26/L05-28/L05-36 acceptance and durable retry evidence are recorded CORRECTED 2026-09-18 (U -> P): no writer ever transitions an exhausted delivery to a terminal state — `retry_event_delivery` always resets to `failed_retriable`, uncapped, so a permanently stuck row is indistinguishable from a healthy in-flight retry and recovery depends on an admin noticing. The never-deleted durability guarantee is real and schema-enforced; the operational no-drop guarantee is not. Audit: reviews/2026-09-18-alq-reachability-audit.md | tasks/L05-go-alert-worker-and-cloud-tasks.md, tests/TC-L05-go-alert-worker-and-cloud-tasks.md, reviews/2026-08-14-L05-worker-boundary-review.md |
| ALQ-08 | register | mapped-existing | L05 task/test/review trio covers §31.3 multi-queue bindings and immutable per-delivery source/priority/override snapshots; migrations 0004/0020 and independent-queue harness evidence are recorded | tasks/L05-go-alert-worker-and-cloud-tasks.md, tests/TC-L05-go-alert-worker-and-cloud-tasks.md, reviews/2026-08-14-L05-worker-boundary-review.md |
| ALQ-09 | register | mapped-existing | L05 task/test/review trio covers §31.3 per-binding allow_duplicates consent and atomic duplicate-delivery guard; L05-15 and migration 0021 evidence are recorded | tasks/L05-go-alert-worker-and-cloud-tasks.md, tests/TC-L05-go-alert-worker-and-cloud-tasks.md, reviews/2026-08-14-L05-worker-boundary-review.md |
| ALQ-10 | register | mapped-existing | L03 task/test/review trio covers §31.3 creator moderation plus admin DLQ replay/discard/audit; migration 0073 and L03-35/10/10a/10c evidence are recorded | tasks/L03-alerts-web-and-creator-api.md, tests/TC-L03-alerts-web-and-creator-api.md, reviews/2026-08-16-L03-corrected-findings-remediation-review.md |
| ALQ-11 | register | mapped-existing | L03 task/test/review trio covers §31.3 owner/admin financial, operator/moderator content and viewer status reads with DB/RLS role boundaries; migration 0039 and L03-10 evidence are recorded | tasks/L03-alerts-web-and-creator-api.md, tests/TC-L03-alerts-web-and-creator-api.md, reviews/2026-08-16-L03-corrected-findings-remediation-review.md |
| ALQ-12 | register | mapped-existing | L03 task/test/review trio covers §31.3 fragment-only overlay transport, scoped/hash session lifecycle, and authorized create/revoke/rotate; L03-06/L03-06a evidence is recorded | tasks/L03-alerts-web-and-creator-api.md, tests/TC-L03-alerts-web-and-creator-api.md, reviews/2026-08-14-L03-definition-review.md |
| ALQ-13 | register | mapped-existing | L03 task/test/review trio covers §31.3 nine safe anchors, scale/width bounds and reduced motion; L03-25/L03-27 evidence is recorded | tasks/L03-alerts-web-and-creator-api.md, tests/TC-L03-alerts-web-and-creator-api.md, reviews/2026-08-14-L03-definition-review.md |
| ALQ-14 | register | mapped-existing | L03 task/test/review trio covers §31.3 truncation, continuation, safe multiline rendering and no clipping; L03-09/L03-27 evidence is recorded | tasks/L03-alerts-web-and-creator-api.md, tests/TC-L03-alerts-web-and-creator-api.md, reviews/2026-08-14-L03-definition-review.md |
| ALQ-15 | register | new-record-required | Missing from reviewed L-track evidence: Per-item skip action | - |
| ALQ-16 | register | new-record-required | Missing from reviewed L03 evidence: no implemented or locally proved 1-hour reconnect policy coalesces the recovered burst into a summary plus bounded catch-up instead of firing an hour of alerts; no configured/displayed summary rule or OVL-E5 proof exists. | - |
| ALQ-17 | register | new-record-required | Missing from reviewed L-track evidence: Time-bounded replay window (the "72-hour buffer" that never existed) | - |
| ALQ-18 | register | new-record-required | Missing from reviewed L03/L16 evidence: no Master Canvas runtime combines modules into one OBS browser source, one connection and one requestAnimationFrame loop; no pure-module composition/error isolation, protected one-per-canvas Free watermark/reserved zone, paid-brand-free composition, or ALQ-18/PRF-02/OVL-E8, OVL-E9 and OVL-E10 local proof exists. CORRECTED 2026-09-18 (A -> X): the runtime is NOT absent — `apps/web/app/overlay/canvas/master-canvas-runtime.ts` and the rendered `[overlayId]` route compose ~17 modules over one connection and one rAF loop. It is unreachable: every reference to `overlay/canvas` outside that directory is a code comment, and no product surface generates the URL for a creator. The §2 pattern, so X not A. Audit: reviews/2026-09-18-alq-reachability-audit.md | - |
| ALQ-19 | register | new-record-required | Missing from reviewed L-track evidence: Vertical / second-output canvas | - |
| TTS-01 | register | new-record-required | Missing from reviewed L03 task/test/review evidence: Full Sarvam synthesis across 13 locales with 2MB/60s caps remains unverified | - |
| TTS-02 | register | mapped-existing | L03 task/test/review trio covers §31.11 quota metering/hard stop via authority 06 and migration 0081; local evidence only, provider reachability remains external | tasks/L03-alerts-web-and-creator-api.md, tests/TC-L03-alerts-web-and-creator-api.md, reviews/2026-09-13-reachability-register.md |
| TTS-03 | register | new-record-required | Missing from reviewed L03 task/test/review evidence: End-to-end shared maxCharLimit enforcement across the amount-tiered ladder remains unverified | - |
| TTS-04 | register | mapped-existing | L03 task/test/review trio covers §31.11 migration 0096 browser/chime fallback; local evidence only, provider reachability remains external | tasks/L03-alerts-web-and-creator-api.md, tests/TC-L03-alerts-web-and-creator-api.md, reviews/2026-09-13-reachability-register.md |
| TTS-05 | register | mapped-existing | L05 task/test/review trio covers §31.11 bounded 1.5-second playback, nonblocking visual rendering and acknowledgement; L05-31 focused policy tests are recorded | tasks/L05-go-alert-worker-and-cloud-tasks.md, tests/TC-L05-go-alert-worker-and-cloud-tasks.md, reviews/2026-08-14-L05-worker-boundary-review.md |
| TTS-06 | register | new-record-required | Missing from reviewed L03 task/test/review evidence: Shared safety corpus/pipeline, homoglyph/leet/repeat/script/transliteration checks, L1-L4 decisions, PII/blocked-user/policy handling, per-surface audit/appeal, and closed-for-speech behavior remain unverified | - |
| TTS-07 | register | new-record-required | Missing from reviewed L-track evidence: Quota bar visible from ~70% consumption | - |
| TTS-08 | register | new-record-required | Missing from reviewed L-track evidence: Upgrade prompt on exhaustion | - |
| TTS-09 | register | new-record-required | Missing from reviewed L15/L03 evidence: Dashboard/mobile wiring and cancel-in-flight proof remain unverified | - |
| TTS-10 | register | new-record-required | Missing from reviewed L-track evidence: TTS character top-ups | - |
| TTS-11 | register | new-record-required | Missing from reviewed L-track evidence: Voice routing rule set: amount, length, script, supporter, event class (§11.10) | - |
| TTS-12 | register | new-record-required | Missing from reviewed L-track evidence: Unicode-range script detection in the live path — no model, no network call | - |
| TTS-13 | register | new-record-required | Missing from reviewed L-track evidence: Dashboard control with a "what this would have cost last week" preview | - |
| TTS-14 | register | new-record-required | Missing from reviewed L-track evidence: Companion mode display and mid-stream switch, plus timed "premium everything" | - |
| TTS-15 | register | new-record-required | Missing from reviewed L-track evidence: Route and reason recorded per alert and shown in history and the quota view | - |
| TTS-16 | register | new-record-required | Missing from reviewed L03 task/test/review evidence: Dual-route identical safety enforcement, including browser-voice path parity, remains unverified | - |
| TTS-17 | register | new-record-required | Missing from reviewed L-track evidence: Companion and dashboard notice at the moment of fallback; no grace buffer exists and none may be added (§11.11) | - |
| VID-01 | register | mapped-existing | L04/L14 task/test/review trio covers §31.4 server cookie fingerprint and webhook writer of payments.viewer_identity_id; anonymous attribution evidence is recorded | tasks/L04-L14-anonymous-payment-identity-attribution.md, tests/TC-L04-L14-anonymous-payment-identity-attribution.md, reviews/2026-09-14-L04-L14-anonymous-payment-identity-attribution-decision.md |
| VID-02 | register | mapped-existing | L04/L14 task/test/review trio covers §31.4 creator_supporter_relations writer and relation recomputation; refund-safe evidence is recorded | tasks/L04-L14-anonymous-payment-identity-attribution.md, tests/TC-L04-L14-anonymous-payment-identity-attribution.md, reviews/2026-09-14-L04-L14-anonymous-payment-identity-attribution-decision.md |
| VID-03 | register | mapped-existing | L14 task/test/review trio covers §31.4 receipt minting from confirmation page; local receipt evidence is recorded without live OAuth claim | tasks/L14-viewer-identity-and-supporter-history.md, tests/TC-L14-viewer-identity-and-supporter-history.md, reviews/2026-09-08-L14-local-completion-and-claim-boundary-review.md |
| VID-04 | register | mapped-existing | L14 task/test/review trio covers §31.4 opaque receipt token, SHA-256 fingerprint and live refund reflection; local evidence only | tasks/L14-viewer-identity-and-supporter-history.md, tests/TC-L14-viewer-identity-and-supporter-history.md, reviews/2026-09-08-L14-local-completion-and-claim-boundary-review.md |
| VID-05 | register | new-record-required | Missing from reviewed L04/L14 evidence: Event writer and L15 verifier linkage for all anonymous/platform/account identity levels remain unverified | - |
| VID-06 | register | mapped-existing | L14 task/test/review trio covers §31.4 first-claim-wins idempotent platform claiming, contested handling, trusted identity verifier; no live OAuth claim | tasks/L14-viewer-identity-and-supporter-history.md, tests/TC-L14-viewer-identity-and-supporter-history.md, reviews/2026-09-08-L14-local-completion-and-claim-boundary-review.md |
| VID-07 | register | new-record-required | Missing from reviewed L14/L17/L18 evidence: Full eight-badge opt-in non-financial policy and streak producers remain unverified | - |
| VID-08 | register | mapped-existing | L14 privacy task/test/review trio covers §31.4 private opt-in searchable profile and viewer profile/search pages | tasks/L14-public-viewer-privacy-and-bounds-hardening.md, tests/TC-L14-public-viewer-privacy-and-bounds-hardening.md, reviews/2026-09-09-L14-public-viewer-privacy-and-bounds-hardening-decision.md |
| VID-09 | register | mapped-existing | L14 privacy task/test/review trio covers §31.4 viewer-scoped newest-100 relations with deterministic tie-break and denial boundaries | tasks/L14-public-viewer-privacy-and-bounds-hardening.md, tests/TC-L14-public-viewer-privacy-and-bounds-hardening.md, reviews/2026-09-09-L14-public-viewer-privacy-and-bounds-hardening-decision.md |
| VID-10 | register | new-record-required | Missing from reviewed L14 evidence: No single reviewed task/test/review trio covers both the newest-100 session cap and the 30-minute single-use enumeration-safe reset semantics; the pieces are separately documented. | - |
| VID-11 | register | new-record-required | Missing from reviewed L-track evidence: DPDP erased-vs-retained split — **the logic exists in code; no deletion flow ships or is promised** (§33.1, §32). Deactivation is what ships. State is B, not U: a capability nobody may reach is not usable | - |
| VID-21 | register | new-record-required | Missing from reviewed L-track evidence: Archival deletion: no hard deletes, identity fields moved aside, returner treated as new. **Engineering preference, not approved policy** — blocked on the privacy/legal gate (§32) | - |
| VID-22 | register | new-record-required | Missing from reviewed L-track evidence: Irreversible hashing of archived identity (legal-gated) | - |
| VID-12 | register | new-record-required | Missing from reviewed L-track evidence: DPDP data export | - |
| VID-13 | register | new-record-required | Missing from reviewed L-track evidence: Reputation: verdict-only (3 keys), score never stored, 180-day window | - |
| VID-14 | register | new-record-required | Missing from reviewed L-track evidence: Reputation write path (chargeback, velocity, moderation strike producers) | - |
| VID-15 | register | new-record-required | Missing from reviewed L-track evidence: Creator-facing reputation display | - |
| VID-16 | register | new-record-required | Missing from reviewed L-track evidence: Flag / report a supporter | - |
| VID-17 | register | new-record-required | Missing from reviewed L-track evidence: Block a supporter | - |
| VID-18 | register | new-record-required | Missing from reviewed L-track evidence: Anonymous non-platform tip claim path | - |
| VID-19 | register | new-record-required | Missing from reviewed L-track evidence: YouTube identity attribution carried onto payments | - |
| VID-20 | register | new-record-required | Missing from reviewed L-track evidence: YouTube handle-vs-channel-ID trust model and namespaces (§12.3 identity rules) | - |
| ENG-01 | register | mapped-existing | L16 task/test/review trio covers §31.5 eight interaction types and tier counts 3/6/8/8; local catalogue evidence only | tasks/L16-interaction-menu-goals-and-widgets.md, tests/TC-L16-interaction-menu-goals-and-widgets.md, reviews/2026-09-08-L16-widget-completion-review.md |
| ENG-02 | register | mapped-existing | L16 task/test/review trio covers §31.5 seven widget types and tier counts 1/3/7/7; local catalogue evidence only | tasks/L16-interaction-menu-goals-and-widgets.md, tests/TC-L16-interaction-menu-goals-and-widgets.md, reviews/2026-09-08-L16-widget-completion-review.md |
| ENG-03 | register | mapped-existing | L16 task/test/review trio covers §31.5 live clamped support-goal progress across stream/daily/monthly/open windows | tasks/L16-interaction-menu-goals-and-widgets.md, tests/TC-L16-interaction-menu-goals-and-widgets.md, reviews/2026-09-08-L16-widget-completion-review.md |
| ENG-04 | register | mapped-existing | L16 task/test/review trio covers §31.5 recent-tips, top-supporters, ticker and mega-tip banner pages | tasks/L16-interaction-menu-goals-and-widgets.md, tests/TC-L16-interaction-menu-goals-and-widgets.md, reviews/2026-09-08-L16-widget-completion-review.md |
| ENG-05 | register | mapped-existing | L16 task/test/review trio covers §31.5 single-channel leaderboard rank and coarse bucket without exact amount | tasks/L16-interaction-menu-goals-and-widgets.md, tests/TC-L16-interaction-menu-goals-and-widgets.md, reviews/2026-09-08-L16-widget-completion-review.md |
| ENG-06 | register | mapped-existing | L16 task/test/review trio covers §31.5 shared overlay fragment-token and REST snapshot/SSE invalidation path | tasks/L16-overlay-widget-response-integrity.md, tests/TC-L16-overlay-widget-response-integrity.md, reviews/2026-09-09-L16-overlay-widget-response-integrity-decision.md |
| ENG-07 | register | mapped-existing | L16 task/test/review trio covers §31.5 paid-vote payment binding and refund-derived tally | tasks/L16-interaction-menu-goals-and-widgets.md, tests/TC-L16-interaction-menu-goals-and-widgets.md, reviews/2026-09-14-L16-public-paid-vote-reachability-decision.md |
| ENG-08 | register | mapped-existing | L16 task/test/review trio covers §31.5 vote-option cap 16 serialized in creating procedure | tasks/L16-vote-option-cardinality-and-overlay-contract-alignment.md, tests/TC-L16-vote-option-cardinality-and-overlay-contract-alignment.md, reviews/2026-09-09-L16-vote-option-cardinality-and-overlay-contract-alignment-decision.md |
| ENG-09 | register | new-record-required | Missing from reviewed L-track evidence: **Viewer interaction menu** | - |
| ENG-10 | register | new-record-required | Missing from reviewed L-track evidence: Support-vote creator UI (create options) | - |
| ENG-11 | register | new-record-required | Missing from reviewed L-track evidence: Support-vote viewer UI (cast) | - |
| ENG-12 | register | new-record-required | Missing from reviewed L-track evidence: Mega alert + priority question viewer trigger | - |
| ENG-13 | register | new-record-required | Missing from reviewed L-track evidence: Hype mode start control | - |
| ENG-14 | register | new-record-required | Missing from reviewed L-track evidence: Widget privacy-scope control | - |
| ENG-15 | register | new-record-required | Missing from reviewed L-track evidence: Widget preview / sample data for all widget types | - |
| ENG-16 | register | new-record-required | Missing from reviewed L16 evidence: Only Super Chat Phase 4/live provider integration remains absent | - |
| ENG-17 | register | new-record-required | Missing from reviewed L-track evidence: Contribution-source toggles wired into Challenges panel | - |
| ENG-18 | register | new-record-required | Missing from reviewed L-track evidence: Priority Question "Unanswered" tab + Mark Answered (§10.6) | - |
| ENG-19 | register | new-record-required | Missing from reviewed L-track evidence: Community boss battle | - |
| ENG-20 | register | new-record-required | Missing from reviewed L-track evidence: Team / squad goals | - |
| ENG-21 | register | new-record-required | Missing from reviewed L-track evidence: Milestone queue (prepare thank-you / sponsor reveal / transition) | - |
| ENG-22 | register | new-record-required | Missing from reviewed L-track evidence: Stream streaks (daily/weekly) | - |
| ENG-23 | register | new-record-required | Missing from reviewed L-track evidence: Like goal, member goal, chat goal, watch-time goal | - |
| ENG-24 | register | new-record-required | Missing from reviewed L-track evidence: Prediction widget, no gambling mechanic | - |
| CHL-01 | register | mapped-existing | L17 task/test/review trio covers §31.6 non-refundable creator-set challenge alternative with append-only state machine, confirmed-payment/refund-derived progress, dashboard and existing overlay widget; provider/refund/browser/OBS staging gates remain open | tasks/L17-paid-challenges.md, tests/TC-L17-paid-challenges.md, reviews/2026-09-08-L17-nonrefundable-challenge-decision.md |
| CHL-02 | register | new-record-required | Missing from reviewed L17 evidence: Locked provider-refund copy and merchant-refund capability are absent; do not credit the blocked refundable task | - |
| CHL-03 | register | new-record-required | Missing from reviewed L-track evidence: Viewer-proposed challenges (plan calls this the better default) | - |
| CHL-04 | register | new-record-required | Missing from reviewed L-track evidence: Completion evidence submission | - |
| CHL-05 | register | new-record-required | Missing from reviewed L-track evidence: Dispute record | - |
| CHL-06 | register | new-record-required | Missing from reviewed L17 evidence: Public standalone challenge board page remains unimplemented | - |
| CHL-07 | register | new-record-required | Missing from reviewed L-track evidence: `!challenge` chat command | - |
| CHL-08 | register | new-record-required | Missing from reviewed L-track evidence: Refundable multi-contributor challenges | - |
| MED-01 | register | mapped-existing | §31.7 L01 task/test/review trio covers local id/name/category projection with server paid-order/channel/tier/enablement revalidation | tasks/L01-public-sticker-contract-slice.md, tests/TC-L01-public-sticker-contract-slice.md, reviews/2026-09-09-L01-public-sticker-contract-slice-decision.md |
| MED-02 | register | new-record-required | Missing from reviewed L-track evidence: Creator packs, tier quotas 10/25/50 (implementation choice, needs sign-off) | - |
| MED-03 | register | new-record-required | Missing from reviewed L22 evidence: scan/attestation/pending_review are documented in the L22 task, TC L22-03–05 remain Open/Not run, and the original decision review is open; later ordering does not reconcile a full tier moderation triad. | - |
| MED-04 | register | new-record-required | Missing from reviewed L22 evidence: the task claims the is_platform_admin route after 0122, but the TC lacks executed E2E route/RLS staff-vs-channel-admin proof and the review records verification pending with audit-order conflict. | - |
| MED-05 | register | new-record-required | Missing from reviewed L-track evidence: Staff review admin UI | - |
| MED-06 | register | new-record-required | Missing from reviewed L-track evidence: **Viewer sticker / GIF picker on the tip page** | - |
| MED-07 | register | mapped-existing | §31.7 L01 task/test/review trio covers viewer response without asset bytes/media URLs, exposing only opaque catalogue/sticker IDs | tasks/L01-public-sticker-contract-slice.md, tests/TC-L01-public-sticker-contract-slice.md, reviews/2026-09-09-L01-public-sticker-contract-slice-decision.md |
| MED-08 | register | new-record-required | Missing from reviewed L-track evidence: Template import rejects inline script / non-schema content outright | - |
| MED-09 | register | new-record-required | Missing from reviewed L-track evidence: Template catalogue frontend | - |
| MED-10 | register | new-record-required | Missing from reviewed L-track evidence: 359 of 600 runtime packages missing; individual authoring required, no mass-copy | - |
| MED-11 | register | new-record-required | Missing from reviewed L-track evidence: Raw-HTML template shape forbidden at every tier | - |
| MED-12 | register | new-record-required | Missing from reviewed L-track evidence: `render_bytes` capped at 2,000,000 | - |
| MED-13 | register | new-record-required | Missing from reviewed L-track evidence: Asset storage quotas Free none / Pro 100MB / Creator 250MB / Studio 1GB | - |
| MED-14 | register | new-record-required | Missing from reviewed L-track evidence: Malware scan stage 2 | - |
| MED-15 | register | new-record-required | Missing from reviewed L-track evidence: Custom sound upload — **stays off until the whole §18.3 gate closes** | - |
| MED-22 | register | new-record-required | Missing from reviewed L-track evidence: Quarantine on upload; unscanned bytes never served, failure state is quarantined | - |
| MED-23 | register | new-record-required | Missing from reviewed L-track evidence: Immutable provenance record per asset (uploader, time, IP, client, filename, hash, attestation version, every transition) | - |
| MED-24 | register | new-record-required | Missing from reviewed L-track evidence: Takedown workflow: intake route, response target, one-action CDN disable, counter-notice, retained evidence | - |
| MED-25 | register | new-record-required | Missing from reviewed L-track evidence: Repeat-infringement policy written before the first complaint, up to upload suspension | - |
| MED-26 | register | new-record-required | Missing from reviewed L-track evidence: Impersonation and voice-imitation prohibition in terms and attestation, same takedown route | - |
| MED-27 | register | new-record-required | Missing from reviewed L-track evidence: One rehearsed end-to-end takedown drill before the flag opens for anyone | - |
| MED-16 | register | new-record-required | Missing from reviewed L-track evidence: Built-in themes / theme packs | - |
| MED-17 | register | new-record-required | Missing from reviewed L-track evidence: Per-event styling beyond `displayStyle` brackets | - |
| MED-18 | register | new-record-required | Missing from reviewed L-track evidence: Drag/resize/layer tools (numeric config exists) | - |
| MED-19 | register | new-record-required | Missing from reviewed L-track evidence: Media and sound libraries | - |
| MED-20 | register | new-record-required | Missing from reviewed L-track evidence: Curated meme/media queue module | - |
| MED-21 | register | new-record-required | Missing from reviewed L-track evidence: GCS/CDN media storage is decided but unbuilt. CORRECTED 2026-09-17 (U -> A): no GCS client, bucket, credential or signed-URL code exists anywhere in bharatstudio-alerts and no migration carries a GCS column, so `bytea` is the ONLY media path, not a legacy rollback. The GCS/CDN decision stands; the claim that it was in place did not. Audit: reviews/2026-09-17-med-21-gcs-storage-stale-claim-audit.md | - |
| CMP-01 | register | mapped-existing | L07 task/test/review trio covers §31.8 CMP-01 requirement; supporting migration/API/mobile test topics are recorded; external evidence remains open | tasks/L07-companion-web-mobile-desktop.md, tests/TC-L07-companion-web-mobile-desktop.md, reviews/2026-08-15-L07-L08-L10-release-surface-review.md |
| CMP-02 | register | mapped-existing | L07 task/test/review trio covers §31.8 CMP-02 requirement; supporting migration/API/mobile test topics are recorded; external evidence remains open | tasks/L07-companion-web-mobile-desktop.md, tests/TC-L07-companion-web-mobile-desktop.md, reviews/2026-08-15-L07-L08-L10-release-surface-review.md |
| CMP-03 | register | mapped-existing | L07 task/test/review trio covers §31.8 CMP-03 requirement; supporting migration/API/mobile test topics are recorded; external evidence remains open | tasks/L07-companion-web-mobile-desktop.md, tests/TC-L07-companion-web-mobile-desktop.md, reviews/2026-08-15-L07-L08-L10-release-surface-review.md |
| CMP-04 | register | mapped-existing | L07 task/test/review trio covers §31.8 17-action catalogue and entitlement/activation separation; migrations 0089/0093/0100 and L07-04 acceptance evidence are recorded | tasks/L07-companion-web-mobile-desktop.md, tests/TC-L07-companion-web-mobile-desktop.md, reviews/2026-08-15-L07-L08-L10-release-surface-review.md |
| CMP-05 | register | mapped-existing | L07 task/test/review trio covers §31.8 finite three-action contract via migration 0041 and L07-04 unsupported-command rejection; no native OBS claim | tasks/L07-companion-web-mobile-desktop.md, tests/TC-L07-companion-web-mobile-desktop.md, reviews/2026-08-15-L07-L08-L10-release-surface-review.md |
| CMP-06 | register | new-record-required | Missing from reviewed L07 evidence: TC L07-03 pairing/revoke/expiry role-scope/audit flow is Not run and the review keeps real pairing/native/device evidence open; no reconciled end-to-end pairing lifecycle proof exists. | - |
| CMP-07 | register | mapped-existing | L07 task/test/review trio covers §31.8 CMP-07 requirement; supporting migration/API/mobile test topics are recorded; external evidence remains open | tasks/L07-companion-web-mobile-desktop.md, tests/TC-L07-companion-web-mobile-desktop.md, reviews/2026-08-15-L07-L08-L10-release-surface-review.md |
| CMP-08 | register | mapped-existing | §31.8 L07 task/test/review trio covers the local macOS OBS WebSocket-v5 boundary: loopback 4455 restrictions, no credential/userinfo/query/fragment route, challenge-response and bounded envelopes, with Swift 12/12 tests; residual gates are real OBS integration, server pairing, Keychain/device behavior, signing, and staging | tasks/L07-companion-web-mobile-desktop.md, tests/TC-L07-companion-web-mobile-desktop.md, reviews/2026-08-15-L07-L08-L10-release-surface-review.md |
| CMP-09 | register | new-record-required | Missing from reviewed L07 evidence: Windows XML policy mirrors the rules, but no Windows SDK/.NET compilation, runtime/DPAPI pairing/signing or device evidence exists; the Windows gate remains open. | - |
| CMP-10 | register | new-record-required | Missing from reviewed L-track evidence: Mirror actions (start/stop/screenshot) | - |
| CMP-11 | register | new-record-required | Missing from reviewed L-track evidence: Stream actions (go live / end) | - |
| CMP-12 | register | new-record-required | Missing from reviewed L-track evidence: Implicit channel provisioning for Companion-only signup | - |
| CMP-36 | register | new-record-required | Missing from reviewed L-track evidence: Issue a distinct Companion grant row on Alerts subscription (`0100` mechanism) | - |
| CMP-37 | register | mapped-existing | L07 task/test/review trio covers §31.8 Free approved actions and one control lease via L07-04/L07-15; no cross-tier/device/deployed claim | tasks/L07-companion-web-mobile-desktop.md, tests/TC-L07-companion-web-mobile-desktop.md, reviews/2026-08-15-L07-L08-L10-release-surface-review.md |
| CMP-13 | register | new-record-required | Missing from reviewed L-track evidence: Stream health panel (all six signals, heartbeat ages) | - |
| CMP-14 | register | new-record-required | Missing from reviewed L-track evidence: Prepare Stream / go-live checklist (§5.1) | - |
| CMP-15 | register | new-record-required | Missing from reviewed L-track evidence: Run full test with per-hop report | - |
| CMP-16 | register | new-record-required | Missing from reviewed L-track evidence: Live Deck top strip + degraded-mode strip (§5.2) | - |
| CMP-17 | register | new-record-required | Missing from reviewed L-track evidence: Panic / Clutch Mode | - |
| CMP-18 | register | new-record-required | Missing from reviewed L-track evidence: Current and next queue item, live | - |
| CMP-19 | register | new-record-required | Missing from reviewed L-track evidence: Per-item replay / skip | - |
| CMP-20 | register | new-record-required | Missing from reviewed L-track evidence: Scene presets | - |
| CMP-21 | register | new-record-required | Missing from reviewed L-track evidence: Goal controls from Companion | - |
| CMP-22 | register | new-record-required | Missing from reviewed L-track evidence: Quick note / stream markers | - |
| CMP-23 | register | new-record-required | Missing from reviewed L07 evidence: the recent-tip, payment-status and refund-status endpoint/surface/projection path lacks a required web caller and reconciled Companion acceptance proof. | - |
| CMP-24 | register | new-record-required | Missing from reviewed L-track evidence: Six monetisation push notification types | - |
| CMP-25 | register | new-record-required | Missing from reviewed L07 evidence: the authority requires a six-per-type preference matrix; no six-type matrix or acceptance proof exists beyond the three coarse toggles. | - |
| CMP-26 | register | mapped-existing | L07 task/test/review trio covers §31.8 CMP-26 requirement; supporting migration/API/mobile test topics are recorded; external evidence remains open | tasks/L07-companion-web-mobile-desktop.md, tests/TC-L07-companion-web-mobile-desktop.md, reviews/2026-08-15-L07-L08-L10-release-surface-review.md |
| CMP-27 | register | new-record-required | Missing from reviewed L-track evidence: Offline queue-of-intent | - |
| CMP-28 | register | new-record-required | Missing from reviewed L-track evidence: Helper diagnostics (port, OBS version, ws auth state) | - |
| CMP-29 | register | new-record-required | Missing from reviewed L-track evidence: Disabled-slot explanations naming the failing layer | - |
| CMP-30 | register | new-record-required | Missing from reviewed L-track evidence: Wrap Stream post-stream workflow (§5.5) | - |
| CMP-31 | register | new-record-required | Missing from reviewed L-track evidence: Companion rename before any standalone store listing | - |
| CMP-32 | register | mapped-existing | L07 task/test/review trio covers §31.8 privacy-minimised notification payloads without tip/donor/payment content; L07-32/L07-33 policy and route evidence are recorded | tasks/L07-companion-web-mobile-desktop.md, tests/TC-L07-companion-web-mobile-desktop.md, reviews/2026-08-15-L07-L08-L10-release-surface-review.md |
| CMP-33 | register | mapped-existing | L07 task/test/review trio covers §31.8 mobile secure storage using WHEN_UNLOCKED_THIS_DEVICE_ONLY with no plaintext fallback; L07-24 secure-store acceptance evidence is recorded | tasks/L07-companion-web-mobile-desktop.md, tests/TC-L07-companion-web-mobile-desktop.md, reviews/2026-08-15-L07-L08-L10-release-surface-review.md |
| CMP-34 | register | mapped-existing | L07 task/test/review trio covers §31.8 fingerprint-plus-ciphertext push-token storage with raw token exclusion; L07-33 route, crypto and migration evidence is recorded | tasks/L07-companion-web-mobile-desktop.md, tests/TC-L07-companion-web-mobile-desktop.md, reviews/2026-08-15-L07-L08-L10-release-surface-review.md |
| CMP-35 | register | new-record-required | Missing from reviewed L-track evidence: Desktop READMEs claim no pairing endpoint exists — stale since `0082`; update them | - |
| CMP-38 | register | new-record-required | Missing from reviewed L-track evidence: **No purchase surface of any kind in either build** — no price, no upgrade CTA, no iOS link-out; enforced by a CI string/route check, not by review | - |
| CMP-39 | register | new-record-required | Missing from reviewed L-track evidence: Localisation framework: zero hardcoded user-visible strings (CI-enforced), ICU MessageFormat, no fragment concatenation | - |
| CMP-40 | register | new-record-required | Missing from reviewed L-track evidence: Hindi as a complete UI language at launch, native-speaker reviewed against a fixed product glossary | - |
| CMP-41 | register | new-record-required | Missing from reviewed L-track evidence: `Intl` for every number, currency, date and duration — Indian 2,2,3 rupee grouping | - |
| CMP-42 | register | new-record-required | Missing from reviewed L-track evidence: Locale as device default with in-app override, persisted and sent on every API call | - |
| CMP-43 | register | new-record-required | Missing from reviewed L-track evidence: Server-side localisation of API errors, health text and push bodies from request/device locale | - |
| CMP-44 | register | new-record-required | Missing from reviewed L-track evidence: Pseudo-locale CI build and +40% text-expansion layout tests | - |
| CMP-45 | register | new-record-required | Missing from reviewed L-track evidence: Bundled Indic fonts with conjunct/matra rendering verified on both platforms | - |
| CMP-46 | register | new-record-required | Missing from reviewed L-track evidence: Wave-two languages behind registry rows: Marathi, Bengali, Telugu, Tamil, Kannada | - |
| CMP-47 | register | new-record-required | Missing from reviewed L-track evidence: Wave-three languages: Gujarati, Malayalam, Punjabi, Odia, Assamese | - |
| CMP-48 | register | new-record-required | Missing from reviewed L-track evidence: RTL/Urdu — separate layout track, not a translation task | - |
| CMP-49 | register | new-record-required | Missing from reviewed L-track evidence: APNs + FCM token lifecycle: register, rotate, restore, revoke on sign-out, prune on feedback | - |
| CMP-50 | register | new-record-required | Missing from reviewed L-track evidence: Two priority classes only (live health failure, payment/delivery failure); everything else normal priority | - |
| CMP-51 | register | new-record-required | Missing from reviewed L-track evidence: Android notification channels per type | - |
| CMP-52 | register | new-record-required | Missing from reviewed L-track evidence: Contextual permission prompt (never at launch); denied-permission is a supported state with a settings deep link | - |
| CMP-53 | register | new-record-required | Missing from reviewed L-track evidence: Foreground reconciliation — no correctness depends on a push arriving | - |
| CMP-54 | register | new-record-required | Missing from reviewed L-track evidence: Quiet hours with high-priority override | - |
| CMP-55 | register | new-record-required | Missing from reviewed L-track evidence: **Sign in with Apple** alongside Google Sign-In, with account linking and private-relay addresses handled | - |
| CMP-56 | register | new-record-required | Missing from reviewed L-track evidence: Optional biometric app lock | - |
| CMP-57 | register | new-record-required | Missing from reviewed L-track evidence: Session-expiry re-auth sheet returning to the same screen; distinct messaging from control-lease expiry | - |
| CMP-58 | register | new-record-required | Missing from reviewed L-track evidence: "Hide sensitive values" toggle honoured app-wide | - |
| CMP-59 | register | new-record-required | Missing from reviewed L-track evidence: Sign-out clears token, cache, push registration, biometric enrolment and revokes the lease server-side | - |
| CMP-60 | register | new-record-required | Missing from reviewed L-track evidence: Five-tab IA (Live / Prepare / Queue / Money / More) with the degraded strip persistent across all tabs | - |
| CMP-61 | register | new-record-required | Missing from reviewed L-track evidence: Deep links resolve to a stateful screen, cold start included | - |
| CMP-62 | register | new-record-required | Missing from reviewed L-track evidence: Universal Links + App Links with association files hosted and verified on `bharatstudio.in` | - |
| CMP-63 | register | new-record-required | Missing from reviewed L-track evidence: First-run flow: sign in → pair → guided Prepare Stream → contextual permissions → first test alert | - |
| CMP-64 | register | new-record-required | Missing from reviewed L-track evidence: Every empty state authored (no stream, no tips, no queue, no devices, notifications denied, offline, paused) | - |
| CMP-94 | register | new-record-required | Missing from reviewed L-track evidence: **Recent Actions on the Live Deck** — session-scoped list of the last actions taken by anyone on this channel, one-tap undo where reversible (§7.5) | - |
| CMP-95 | register | new-record-required | Missing from reviewed L-track evidence: Object detail on tap follows the §7.2 contract — queue item, tip, supporter, health signal | - |
| CMP-96 | register | new-record-required | Missing from reviewed L-track evidence: "Why didn't this fire?" from the Companion queue, same per-hop diagnosis as DSH-17 | - |
| CMP-65 | register | new-record-required | Missing from reviewed L-track evidence: Enforce iOS 15.1 / Android API 26 floors at install | - |
| CMP-66 | register | new-record-required | Missing from reviewed L-track evidence: Landscape usable; degraded strip and panic control never hidden | - |
| CMP-67 | register | new-record-required | Missing from reviewed L-track evidence: Tablet = scaled phone layout with max content width | - |
| CMP-68 | register | new-record-required | Missing from reviewed L-track evidence: Dynamic Type / font scaling to largest sizes with no truncation or sub-minimum targets | - |
| CMP-69 | register | new-record-required | Missing from reviewed L-track evidence: Screen-reader labels on every control in the selected language | - |
| CMP-70 | register | new-record-required | Missing from reviewed L-track evidence: Colour never the only health signal; reduced-motion honoured | - |
| CMP-71 | register | new-record-required | Missing from reviewed L-track evidence: Dark default, complete light mode, full safe-area handling | - |
| CMP-72 | register | new-record-required | Missing from reviewed L-track evidence: Release channels: internal → TestFlight/Play internal → staged rollout with crash-rate halt | - |
| CMP-73 | register | new-record-required | Missing from reviewed L-track evidence: App-version + build-number scheme recorded against commit and API contract version | - |
| CMP-74 | register | new-record-required | Missing from reviewed L-track evidence: API back-compatibility for old builds; breaking an old build is a dated, deliberate act | - |
| CMP-75 | register | new-record-required | Missing from reviewed L-track evidence: Server-driven forced-upgrade floor (security/protocol only) plus dismissible soft prompt, never mid-stream | - |
| CMP-76 | register | new-record-required | Missing from reviewed L-track evidence: OTA JS-bundle policy: signed, versioned, staged, rollback-able; never features, monetisation or reviewed behaviour | - |
| CMP-77 | register | new-record-required | Missing from reviewed L-track evidence: Per-release rollback plan; local-state migrations additive or reversible | - |
| CMP-78 | register | new-record-required | Missing from reviewed L-track evidence: **Reconcile in-app account deletion (store requirement) with the blocked deletion policy — before submission** | - |
| CMP-79 | register | new-record-required | Missing from reviewed L-track evidence: Permission purpose strings, specific, in every shipped language | - |
| CMP-80 | register | new-record-required | Missing from reviewed L-track evidence: Data-safety / privacy-nutrition declarations matching the published policy exactly | - |
| CMP-81 | register | new-record-required | Missing from reviewed L-track evidence: UGC obligations documented for review: report, block, moderate | - |
| CMP-82 | register | new-record-required | Missing from reviewed L-track evidence: Reviewer demo account with seeded data reaching a live-looking Live Deck | - |
| CMP-83 | register | new-record-required | Missing from reviewed L-track evidence: Age rating and content descriptors set from moderation reality | - |
| CMP-84 | register | new-record-required | Missing from reviewed L-track evidence: Offline as a first-class state showing last-known values with their age | - |
| CMP-85 | register | new-record-required | Missing from reviewed L-track evidence: Offline queue reconciliation per action; irreversible and financial actions refused offline, never queued | - |
| CMP-86 | register | new-record-required | Missing from reviewed L-track evidence: Exponential reconnect with jitter, always reconciling rather than assuming continuity | - |
| CMP-87 | register | new-record-required | Missing from reviewed L-track evidence: Battery and metered-data discipline over a three-hour stream | - |
| CMP-88 | register | new-record-required | Missing from reviewed L-track evidence: Crash reporting with release tagging, CI symbol upload, crash-free-sessions gate; payloads scrubbed of money, identity and message content | - |
| CMP-89 | register | new-record-required | Missing from reviewed L-track evidence: Privacy-respecting product analytics with working opt-out | - |
| CMP-90 | register | new-record-required | Missing from reviewed L-track evidence: §19.4 budgets measured per release on the reference mid-range Android | - |
| CMP-91 | register | new-record-required | Missing from reviewed L-track evidence: End-to-end tests both platforms: sign in, pair, prepare, test alert, Clutch, queue action, offline reconcile | - |
| CMP-92 | register | new-record-required | Missing from reviewed L-track evidence: CI builds both platforms every merge, producing installable artifacts | - |
| CMP-93 | register | new-record-required | Missing from reviewed L-track evidence: Store release checklist: localised screenshots and descriptions, demo account, declarations | - |
| CON-01 | register | new-record-required | Missing from reviewed L-track evidence: YouTube OAuth token storage, refresh, encryption | - |
| CON-02 | register | new-record-required | Missing from reviewed L-track evidence: **Connect / disconnect UI** | - |
| CON-03 | register | new-record-required | Missing from reviewed L-track evidence: **Revoked-auth detection + creator prompt** | - |
| CON-04 | register | new-record-required | Missing from reviewed L-track evidence: Live status discovery, `streamList` polling, 3-failure fallback with reset | - |
| CON-05 | register | new-record-required | Missing from reviewed L-track evidence: Quota budget, fair share, day-exhaust on 403 | - |
| CON-06 | register | new-record-required | Missing from reviewed L-track evidence: Super Chat / Super Sticker / member / milestone / gifted normalisation | - |
| CON-07 | register | new-record-required | Missing from reviewed L-track evidence: `!tip`, `!tip 100`, `!tip 100 message` → opaque short link | - |
| CON-22 | register | new-record-required | Missing from reviewed L-track evidence: Bare `!tip` replies with the short link and no amount; viewer chooses on the page | - |
| CON-08 | register | new-record-required | Missing from reviewed L-track evidence: Bot chat acknowledgement (flag default off) | - |
| CON-09 | register | new-record-required | Missing from reviewed L-track evidence: Connector entitlement counts 0/1/2/3 | - |
| CON-10 | register | new-record-required | Missing from reviewed L-track evidence: Connector count / limit shown in UI | - |
| CON-11 | register | new-record-required | Missing from reviewed L-track evidence: Ingest-failure admin surface UI | - |
| CON-12 | register | new-record-required | Missing from reviewed L-track evidence: Financial truth never derived from a platform event — webhook only | - |
| CON-13 | register | new-record-required | Missing from reviewed L-track evidence: Member reconciliation via `members.list` (never chat as truth) | - |
| CON-14 | register | new-record-required | Missing from reviewed L-track evidence: Like goals via `videos.list` (cadence measured, not assumed) | - |
| CON-15 | register | new-record-required | Missing from reviewed L-track evidence: Controlled broadcast lifecycle: create/bind → verify ingest `active` → testing → live | - |
| CON-16 | register | new-record-required | Missing from reviewed L-track evidence: Assisted gifting as reminder/deep link only | - |
| CON-17 | register | new-record-required | Missing from reviewed L-track evidence: Chat display and filtering — tierable. **Retention is not** (§12.6.2): what we ingest and index is a uniform product decision, identical on every tier | - |
| CON-18 | register | new-record-required | Missing from reviewed L-track evidence: Twitch EventSub | - |
| CON-19 | register | new-record-required | Missing from reviewed L-track evidence: Kick | - |
| CON-20 | register | new-record-required | Missing from reviewed L-track evidence: Optional YouTube `/live` support page | - |
| CON-21 | register | new-record-required | Missing from reviewed L-track evidence: YouTube identity/trust model and namespaces (§12.3 identity rules) | - |
| CON-31 | register | new-record-required | Missing from reviewed L-track evidence: **One fetch, many surfaces** — no surface calls YouTube; the server polls once per channel and fans out over the channel-keyed SSE (§4.2) | - |
| CON-32 | register | new-record-required | Missing from reviewed L-track evidence: IFrame Player API for overlay and dashboard presence and playback — client-side, official, zero quota | - |
| CON-33 | register | new-record-required | Missing from reviewed L-track evidence: Official YouTube live-chat **embed** for the creator to read chat in the dashboard and Companion — zero quota, display only, never a data source | - |
| CON-34 | register | new-record-required | Missing from reviewed L-track evidence: Stream health from the desktop helper / OBS WebSocket, never from a YouTube call | - |
| CON-35 | register | new-record-required | Missing from reviewed L-track evidence: Cadence as a budget: poll only while live, back off when idle, tier by creator size, defined degradation (slow → pause, always with a visible reason) | - |
| CON-36 | register | new-record-required | Missing from reviewed L-track evidence: **Per-call, per-endpoint, per-channel quota instrumentation**, exported as a histogram (RT-06). Ships with the connector — the quota application is worthless without it | - |
| CON-37 | register | new-record-required | Missing from reviewed L-track evidence: Measure `streamList` against a real Google project: units per hour, per channel, per message volume, and behaviour during a chat burst | - |
| CON-38 | register | new-record-required | Missing from reviewed L-track evidence: Derive the supported concurrent-creator ceiling at the free allowance and at each increase tier, then file the quota application with measured numbers | - |
| CON-40 | register | new-record-required | Missing from reviewed L-track evidence: **Subscription registry with reference counting** — a datum is polled only while refcount > 0; reuses the RT-02 channel-keyed subscriber map rather than a second registry | - |
| CON-41 | register | new-record-required | Missing from reviewed L-track evidence: Visibility-driven subscribe and unsubscribe: hidden module, inactive scene, background tab, backgrounded Companion | - |
| CON-42 | register | new-record-required | Missing from reviewed L-track evidence: Unsubscribe hysteresis (~60s grace) so scene flicking does not thrash subscriptions | - |
| CON-43 | register | new-record-required | Missing from reviewed L-track evidence: **Cross-channel batching** — one global poller, chunked IDs, one call per chunk instead of one per channel | - |
| CON-44 | register | new-record-required | Missing from reviewed L-track evidence: Field batching — request the parts needed together in one call, never two calls for one screen | - |
| CON-45 | register | new-record-required | Missing from reviewed L-track evidence: Tip page: live player and chat are click-to-load embeds; a live badge subscribes only while the page has a visitor and drops after idle | - |
| CON-46 | register | new-record-required | Missing from reviewed L-track evidence: Chat ingestion subscribed **by feature in use**, never by liveness; a tips-and-overlay creator opens no chat connection | - |
| CON-47 | register | new-record-required | Missing from reviewed L-track evidence: Budget manager: per-datum priority, global degradation rather than per-creator starvation, visible slowdown, negative caching for offline channels | - |
| CON-48 | register | new-record-required | Missing from reviewed L-track evidence: Cold subscriber gets last-known value with its age immediately; a render never waits on an upstream call | - |
| CON-49 | register | new-record-required | Missing from reviewed L-track evidence: Anti-pattern enforcement (§4.4.6) — no client calls, no per-surface fetch, no offline polling, no fixed global timer, no per-visitor subscription | - |
| CON-39 | register | new-record-required | Missing from reviewed L-track evidence: Page scraping and InnerTube — **never build.** ToS-prohibited automated access, no contract, no stability, unverifiable financial provenance, and it moves the consequence onto the creator's channel (§4) | - |
| ENT-01 | register | new-record-required | Missing from reviewed L-track evidence: Eight entitlement dimensions, closed set, all enforced | - |
| ENT-02 | register | new-record-required | Missing from reviewed L-track evidence: Moderator seats 0/0/2/5, new grants only, existing grandfathered | - |
| ENT-03 | register | new-record-required | Missing from reviewed L-track evidence: Moderator seat management UI | - |
| ENT-04 | register | new-record-required | Missing from reviewed L-track evidence: Internal ceilings: pending visuals 20/50/150/500 (500 pending §12.7 verification) · bindings 3/5/10/**50** · presets 1/2/4/**20** · read-only sessions 2/3/5/8 (held pending load evidence) · control sessions 1/1/2/4. *Updated 2026-09-14 to match §30.2.* | - |
| ENT-05 | register | new-record-required | Missing from reviewed L-track evidence: Grandfathering 12 months + 30-day renewal grace | - |
| ENT-06 | register | new-record-required | Missing from reviewed L-track evidence: Referral engine with fraud signal | - |
| ENT-07 | register | new-record-required | Missing from reviewed L-track evidence: Billing panel, upgrade/downgrade/reactivate/payment-method | - |
| ENT-08 | register | new-record-required | Missing from reviewed L-track evidence: Top-up entitlement additivity, ledger, spend caps | - |
| ENT-09 | register | new-record-required | Missing from reviewed L-track evidence: AI credit ledger, classes, reservations (§11.7) | - |
| ADM-01 | register | new-record-required | Missing from reviewed L-track evidence: Admin console separate from creator dashboard, consumes platform-admin API only | - |
| ADM-02 | register | new-record-required | Missing from reviewed L-track evidence: DLQ inspection, controlled replay/discard, audited, reason required | - |
| ADM-03 | register | new-record-required | Missing from reviewed L-track evidence: Entitlement + channel-capacity management | - |
| ADM-04 | register | new-record-required | Missing from reviewed L-track evidence: DB-backed billing plan catalogue with append-only history | - |
| ADM-05 | register | new-record-required | Missing from reviewed L-track evidence: Reconciliation quarantine review UI | - |
| ADM-06 | register | new-record-required | Missing from reviewed L-track evidence: Featured-creator curation writer | - |
| ADM-07 | register | new-record-required | Missing from reviewed L-track evidence: Admin OIDC + MFA, durable admin registry (vs allowlist) | - |
| ADM-08 | register | new-record-required | Missing from reviewed L-track evidence: Redaction by default; destructive ops need confirmation + reason + audit ref | - |
| ADM-09 | register | new-record-required | Missing from reviewed L-track evidence: Admin console responsive at 320px/iPad/desktop, keyboard nav | - |
| OPS-01 | register | mapped-existing | L06 task/test/review trio covers §31.14 schedules with owner, OIDC, retry/DLQ, idempotency, monitoring and rollback; local evidence only, no deployed/legal claim | tasks/L06-scheduler-boundary.md, tests/TC-L06-scheduler-boundary.md, reviews/2026-08-14-L06-scheduler-boundary-review.md |
| OPS-02 | register | new-record-required | Missing from reviewed L-track evidence: **Schedules actually enabled** | - |
| OPS-03 | register | mapped-existing | L06 task/test/review trio covers §31.14 schedule:<id>:<window> idempotency and receipt/business-completion separation; local evidence only | tasks/L06-scheduler-boundary.md, tests/TC-L06-scheduler-boundary.md, reviews/2026-08-14-L06-scheduler-boundary-review.md |
| OPS-04 | register | mapped-existing | L06 task/test/review trio covers §31.14 archived schedules remaining disabled pending legal approval; local evidence only, legal/deployment gates remain open | tasks/L06-scheduler-boundary.md, tests/TC-L06-scheduler-boundary.md, reviews/2026-08-14-L06-scheduler-boundary-review.md |
| OPS-05 | register | new-record-required | Missing from reviewed L-track evidence: Email outbox with Resend; invoice, subscription, DPDP export, overlay-expiry mails | - |
| OPS-06 | register | new-record-required | Missing from reviewed L09 evidence: no reconciled triad proves each critical alert has an owner and a tested runbook; seven local runbooks are listed, but critical-scenario execution and actionable dashboard policy remain open. | - |
| OPS-07 | register | new-record-required | Missing from reviewed L-track evidence: On-call rotation | - |
| OPS-08 | register | new-record-required | Missing from reviewed L-track evidence: Activation instrumentation (payout + OBS + first alert) | - |
| OPS-09 | register | new-record-required | Missing from reviewed L09 evidence: deployed scrape/dashboard/threshold evidence remains open, so the seven metrics do not yet form a reconciled executable end-to-end contract. | - |
| OPS-10 | register | new-record-required | Missing from reviewed L-track evidence: Creator activation funnel and viewer funnel instrumentation | - |
| OPS-11 | register | new-record-required | Missing from reviewed L-track evidence: Revenue KPIs: tips/viewer-hour, average tip, repeat-supporter rate, TTS-driven tips, threshold uplift, goal-driven tips, `!tip` conversion, challenge and vote revenue | - |
| OPS-12 | register | mapped-existing | L09 task/test/review trio covers §31.14 bounded trace-ID discipline and propagation; local observability evidence only, no deployed claim | tasks/L09-observability-load-failure.md, tests/TC-L09-observability-load-failure.md, reviews/2026-08-15-L09-observability-review.md |
| OPS-13 | register | mapped-existing | L09 task/test/review trio covers §31.14 service-identity metric labels without user IDs; local observability evidence only, no deployed claim | tasks/L09-observability-load-failure.md, tests/TC-L09-observability-load-failure.md, reviews/2026-08-15-L09-observability-review.md |
| OPS-14 | register | mapped-existing | L10 task/test/review trio covers §31.14 static manifest placeholder validation and deployment blocking; TC evidence is local only | tasks/L10-release-readiness-and-rollout.md, tests/TC-L10-release-readiness-and-rollout.md, reviews/2026-08-15-L07-L08-L10-release-surface-review.md |
| OPS-15 | register | mapped-existing | L08 task/test/review trio covers §31.14 checked-in static security headers for CSP/framing/referrer/permissions; local evidence only | tasks/L08-marketing-support-legal.md, tests/TC-L08-marketing-support-legal.md, reviews/2026-08-15-L07-L08-L10-release-surface-review.md |
| MKT-01 | register | new-record-required | Missing from reviewed L08 evidence: the authority requires per-page /alerts, /mirror and /stream information architecture plus a durable 301 matrix; the existing route/redirect coverage is incomplete. | - |
| MKT-02 | register | new-record-required | Missing from reviewed L08 evidence: TC lacks provider-fee source-of-truth and dual-sided calculation proof, and Razorpay Technology Partner approval remains pending; provider dependency is unresolved. | - |
| MKT-03 | register | mapped-existing | L08 task/test/review trio covers §31.15 static rendered HTML competitor exclusion; local evidence only | tasks/L08-marketing-support-legal.md, tests/TC-L08-marketing-support-legal.md, reviews/2026-08-15-L07-L08-L10-release-surface-review.md |
| MKT-04 | register | mapped-existing | L08 task/test/review trio covers §31.15 exclusion of Enterprise tier, CTA and contact-sales flow; local evidence only | tasks/L08-marketing-support-legal.md, tests/TC-L08-marketing-support-legal.md, reviews/2026-08-15-L07-L08-L10-release-surface-review.md |
| MKT-05 | register | new-record-required | Missing from reviewed L-track evidence: Watermark claim vs reality — the pricing page says tip page + overlay, and only the overlay has one. §30.6 settles it as correct: build the tip-page line rather than weaken the claim | - |
| MKT-06 | register | new-record-required | Missing from reviewed L-track evidence: `/features` frames Alerts and Companion as co-equal; Companion is bundled | - |
| MKT-07 | register | new-record-required | Missing from reviewed L-track evidence: Legal sign-off: pricing/feature claims, DPDP deletion, plaintext reset URL in email | - |
| MKT-08 | register | new-record-required | Missing from reviewed L-track evidence: Support surface and staffing | - |
| MKT-09 | register | new-record-required | Missing from reviewed L-track evidence: Public copy matches versioned decisions with dated history | - |
| HUB-01 | register | new-record-required | Missing from reviewed L-track evidence: Mobile support tray, verified payment state, receipts, QR/UPI | - |
| HUB-02 | register | new-record-required | Missing from reviewed L-track evidence: Amount presets | - |
| HUB-03 | register | new-record-required | Missing from reviewed L-track evidence: Five explicit status states (pending → verified → queued → shown → held) | - |
| HUB-04 | register | new-record-required | Missing from reviewed L-track evidence: Safe message preview before checkout | - |
| HUB-05 | register | new-record-required | Missing from reviewed L-track evidence: Approved sticker / sound picker | - |
| HUB-06 | register | new-record-required | Missing from reviewed L-track evidence: Live supporter wall with opt-in names | - |
| HUB-07 | register | new-record-required | Missing from reviewed L-track evidence: Free reactions, rate-limited and sampled | - |
| HUB-08 | register | new-record-required | Missing from reviewed L-track evidence: Community goal ladder with milestone tiers | - |
| HUB-09 | register | new-record-required | Missing from reviewed L-track evidence: Goal source labels. The tips label is v1; **Super Chat and membership labels are Phase 4** and must not render a source that cannot yet exist | - |
| HUB-10 | register | new-record-required | Missing from reviewed L-track evidence: Pick-a-side vote with published rules and close time | - |
| HUB-11 | register | new-record-required | Missing from reviewed L-track evidence: Stream mission card | - |
| HUB-12 | register | new-record-required | Missing from reviewed L-track evidence: Live "what changed" feed | - |
| HUB-13 | register | new-record-required | Missing from reviewed L-track evidence: Embedded YouTube player (IFrame Player API — no data scopes, no quota, §4.2). **Phased P2 conservatively**: the launch authority excludes YouTube capabilities and §34 says no YouTube surface before Phase 4; whether a no-API embed is inside that exclusion is open (§33.2) | - |
| HUB-14 | register | new-record-required | Missing from reviewed L-track evidence: Free lane: one free vote, check-in streak, challenge proposal, cheer card | - |
| HUB-15 | register | new-record-required | Missing from reviewed L-track evidence: "Where does my support go?" creator explainer | - |
| HUB-16 | register | new-record-required | Missing from reviewed L-track evidence: Payment-retry recovery screen | - |
| HUB-17 | register | new-record-required | Missing from reviewed L-track evidence: Low-bandwidth / no-player mode | - |
| HUB-18 | register | new-record-required | Missing from reviewed L-track evidence: Indian language support | - |
| HUB-19 | register | new-record-required | Missing from reviewed L-track evidence: Accessibility: reduced motion, no autoplay sound, SR labels | - |
| HUB-20 | register | new-record-required | Missing from reviewed L-track evidence: Shareable mini-card, campaign links, referral attribution | - |
| HUB-21 | register | new-record-required | Missing from reviewed L-track evidence: Event-specific layout presets | - |
| HUB-22 | register | new-record-required | Missing from reviewed L-track evidence: Post-stream supporter recap and receipt export | - |
| HUB-23 | register | new-record-required | Missing from reviewed L-track evidence: Milestone unlocks framed as a creator promise, never a contract | - |
| DSH-10 | register | new-record-required | Missing from reviewed L-track evidence: **Screen inventory built as named screens** (§7.1), not jobs | - |
| DSH-11 | register | new-record-required | Missing from reviewed L-track evidence: **Detail-view contract** (§7.2): Summary · Timeline · Relations · Actions · Audit, in that order, for every noun | - |
| DSH-12 | register | new-record-required | Missing from reviewed L-track evidence: **Activity Log** (§7.5): one chronological view over every audited action, filterable by actor, type, range and object | - |
| DSH-13 | register | new-record-required | Missing from reviewed L-track evidence: Platform-staff actions affecting this channel visible to the creator in the Activity Log | - |
| DSH-14 | register | new-record-required | Missing from reviewed L-track evidence: Activity Log role-scoping by projection and RLS — operational entries without financial amounts | - |
| DSH-15 | register | new-record-required | Missing from reviewed L-track evidence: Activity Log free and uncapped at every tier (§12.6); only team filtering, saved views and scheduled export are tierable | - |
| DSH-16 | register | new-record-required | Missing from reviewed L-track evidence: **"Why this number?"** explain panel on every derived figure, showing the computation and its rows | - |
| DSH-17 | register | new-record-required | Missing from reviewed L-track evidence: **"Why didn't this fire?"** per-hop alert diagnosis naming the failing hop, never "unknown" | - |
| DSH-18 | register | new-record-required | Missing from reviewed L-track evidence: Trace ID and timeline on every payment and alert row | - |
| DSH-19 | register | new-record-required | Missing from reviewed L-track evidence: Copy affordances: tip link, short link, overlay URL, QR image, receipt link | - |
| DSH-20 | register | new-record-required | Missing from reviewed L-track evidence: Send a test alert from any screen | - |
| DSH-21 | register | new-record-required | Missing from reviewed L-track evidence: **Show me on stream** — brief real-overlay preview with auto-revert | - |
| DSH-22 | register | new-record-required | Missing from reviewed L-track evidence: Undo toast with a real window on every reversible action | - |
| DSH-23 | register | new-record-required | Missing from reviewed L-track evidence: Export-this-view as a background job, never by rendering rows (§12.7) | - |
| DSH-24 | register | new-record-required | Missing from reviewed L-track evidence: Pin any card to Home | - |
| DSH-25 | register | new-record-required | Missing from reviewed L-track evidence: **Supporter profile** (§7.4): history, streak, badges, shown/hidden messages, consent state, private notes, mute-TTS, block stickers, block, report | - |
| DSH-26 | register | new-record-required | Missing from reviewed L-track evidence: Supporter amounts follow §12.3 — no public lifetime total; visibility consent governs anything on stream | - |
| DSH-27 | register | new-record-required | Missing from reviewed L-track evidence: **Command palette and global search** across supporters, payments, receipts, assets, modules and actions | - |
| DSH-28 | register | new-record-required | Missing from reviewed L-track evidence: **Support handoff bundle** — redacted diagnostics, no amounts, identities or message content (§12.4) | - |
| DSH-29 | register | new-record-required | Missing from reviewed L-track evidence: Asset detail shows **where each asset is used** | - |
| DSH-30 | register | new-record-required | Missing from reviewed L-track evidence: Empty, loading, error and denied states authored for every screen (§7.7) | - |
| DSH-31 | register | new-record-required | Missing from reviewed L-track evidence: Denied states name the unlocking tier or the missing role — never a dead control, never a silent hide (§15.3) | - |
| SAF-01 | register | new-record-required | Missing from reviewed L-track evidence: **One corpus, one pipeline, every surface** — tips, TTS, chat, display names, sticker captions, lobby names, bot replies, and Super Chat when it lands in Phase 4 | - |
| SAF-02 | register | new-record-required | Missing from reviewed L-track evidence: L0 normalisation: NFKC, zero-width and RTL-override stripping, combining-mark flood, homoglyph folding, leet and separator folding, repeated-character collapse | - |
| SAF-03 | register | new-record-required | Missing from reviewed L-track evidence: Script detection and **phonetic keys per Indic script**, so a slur in Devanagari, Latin transliteration or code-mixed text is one term | - |
| SAF-04 | register | new-record-required | Missing from reviewed L-track evidence: Original text never destroyed — normalisation produces a parallel matching form | - |
| SAF-05 | register | new-record-required | Missing from reviewed L-track evidence: L1 Aho–Corasick over the compiled corpus, global plus per-creator, whole-word and substring rules kept separate | - |
| SAF-06 | register | new-record-required | Missing from reviewed L-track evidence: L2 bounded edit distance plus phonetic match for obfuscation | - |
| SAF-07 | register | new-record-required | Missing from reviewed L-track evidence: L3 local classifier on our own compute for threats, harassment, scam patterns, raid coordination | - |
| SAF-08 | register | new-record-required | Missing from reviewed L-track evidence: L4 AI on the **residual band only** | - |
| SAF-09 | register | new-record-required | Missing from reviewed L-track evidence: **Per-surface decisions** — payment, display, TTS, stored record, moderator review are independent and separately audited | - |
| SAF-10 | register | new-record-required | Missing from reviewed L-track evidence: URL neutralisation with per-creator allow and deny domains | - |
| SAF-11 | register | new-record-required | Missing from reviewed L-track evidence: SSML-injection guard — a message can never become synthesis instructions | - |
| SAF-12 | register | new-record-required | Missing from reviewed L-track evidence: PII detection: phone, UPI ID, email, address, card-like strings, plus the no-accidental-doxxing rule | - |
| SAF-13 | register | new-record-required | Missing from reviewed L-track evidence: Rate, flood, repeated-text and emoji-flood controls; slow, raid and high-toxicity modes | - |
| SAF-14 | register | new-record-required | Missing from reviewed L-track evidence: Policy presets: family-friendly, gaming, mature audience, sponsor-safe | - |
| SAF-15 | register | new-record-required | Missing from reviewed L-track evidence: **Fails closed for speech, open for money** — safety unavailable means TTS is silent; payment and receipt are never blocked | - |
| SAF-16 | register | new-record-required | Missing from reviewed L-track evidence: Degraded state visible to the creator, never to the audience | - |
| SAF-17 | register | new-record-required | Missing from reviewed L-track evidence: **Untiered** (§30.1) — no pack, tier or add-on may sell better safety | - |
| SAF-18 | register | new-record-required | Missing from reviewed L-track evidence: Audit per action: original, normalised, deciding layer, matched rule or score, confidence, **policy version**, human actor — surfaced in the Activity Log | - |
| SAF-19 | register | new-record-required | Missing from reviewed L-track evidence: Supporter-visible appeal path for a block; reversals audited | - |
| SAF-20 | register | new-record-required | Missing from reviewed L-track evidence: **Verdict cache** keyed `HMAC(secret, normalised ‖ language ‖ policy_version)`, storing verdicts and never text | - |
| SAF-21 | register | new-record-required | Missing from reviewed L-track evidence: PII-flagged messages are **never cached** | - |
| SAF-22 | register | new-record-required | Missing from reviewed L-track evidence: Cross-channel cache with creator-specific rules applied **after** the lookup | - |
| SAF-23 | register | new-record-required | Missing from reviewed L-track evidence: **Term-level caching** — an AI verdict on a novel term is promoted into the L1 corpus after review, so it costs nothing again | - |
| SAF-24 | register | new-record-required | Missing from reviewed L-track evidence: Residual batching within a short window; signal-based escalation (new author, length, mixed script, link, amount) | - |
| SAF-25 | register | new-record-required | Missing from reviewed L-track evidence: Spoken messages get the full ladder; scrolling chat may stop at L3 absent signal — every surface still runs L0–L3 | - |
| SAF-26 | register | new-record-required | Missing from reviewed L-track evidence: Periodic distillation of L3 from accumulated L4 verdicts | - |
| SAF-27 | register | new-record-required | Missing from reviewed L-track evidence: Negative caching of common benign phrases | - |
| SAF-28 | register | new-record-required | Missing from reviewed L-track evidence: Compiled per-channel matcher rebuilt on change, held in memory | - |
| SAF-29 | register | new-record-required | Missing from reviewed L-track evidence: Per-channel and global AI budgets that stop escalation, **never L0–L3** | - |
| SAF-31 | register | new-record-required | Missing from reviewed L-track evidence: **Seed corpus**: English + Hindi/Hinglish, 300–800 reviewed terms each, tiered T1/T2/T3. Public lists are candidates only, never shipped unreviewed | - |
| SAF-32 | register | new-record-required | Missing from reviewed L-track evidence: Per-term record: surface · language · script · phonetic key · severity · whole-word or substring · source · added-by · reviewed-by · date · policy version | - |
| SAF-33 | register | new-record-required | Missing from reviewed L-track evidence: **Allowlist of legitimate words containing a banned substring** — the Scunthorpe fix | - |
| SAF-34 | register | new-record-required | Missing from reviewed L-track evidence: Named native-speaker owner per language, who streams | - |
| SAF-35 | register | new-record-required | Missing from reviewed L-track evidence: Wave-two corpora matching the §5.6.2 language waves | - |
| SAF-36 | register | new-record-required | Missing from reviewed L-track evidence: **Growth flywheel**: offline classification → candidate → native-speaker review → corpus entry → new policy version | - |
| SAF-37 | register | new-record-required | Missing from reviewed L-track evidence: **Near-miss telemetry** — unmatched text within edit-distance 1–2 of a banned term logged as a candidate | - |
| SAF-38 | register | new-record-required | Missing from reviewed L-track evidence: Corpus changes versioned, audited, reversible; additions name their reviewer, removals name their reason | - |
| SAF-39 | register | new-record-required | Missing from reviewed L-track evidence: **AI is not in the live path for chat** — deterministic online, AI offline and batched; an exhausted budget degrades discovery, never protection | - |
| SAF-40 | register | new-record-required | Missing from reviewed L-track evidence: Unicode TR39 confusables mapping, vowel-elision keys, skeleton form, Double Metaphone for Latin and a syllable key for Indic | - |
| SAF-41 | register | new-record-required | Missing from reviewed L-track evidence: **Evidence snapshot at action time**: original, normalised, rule, layer, confidence, policy version, actor, ±N surrounding messages | - |
| SAF-42 | register | new-record-required | Missing from reviewed L-track evidence: Raw unactioned chat on the shortest retention class; action records and their snapshots on the long one | - |
| SAF-43 | register | new-record-required | Missing from reviewed L-track evidence: Appeal record stored with the action, including outcome and reviewer | - |
| SAF-44 | register | new-record-required | Missing from reviewed L-track evidence: Creator-scoped flag and block lists | - |
| SAF-45 | register | new-record-required | Missing from reviewed L-track evidence: **No global shared blacklist, ever** (§16.3) | - |
| SAF-46 | register | new-record-required | Missing from reviewed L-track evidence: Cross-creator risk **signal** only: decaying, unattributed, never auto-actioning, OAuth identity only, never payment identity | - |
| REP-01 | register | new-record-required | Missing from reviewed L-track evidence: Supporter reputation **derived, never stored as a score** (§19.6) | - |
| REP-02 | register | new-record-required | Missing from reviewed L-track evidence: Inputs: payments minus refunds · tenure · consistency · actioned events · appeal outcomes | - |
| REP-03 | register | new-record-required | Missing from reviewed L-track evidence: Negative signals private to that creator; positive signals subject to visibility consent; never a public lifetime total | - |
| REP-04 | register | new-record-required | Missing from reviewed L-track evidence: Consumers: auto-approve trusted supporters · TTS eligibility hints · queue priority · lobby attendance priority · voice-routing named supporter | - |
| REP-05 | register | new-record-required | Missing from reviewed L-track evidence: Decays, appealable, never cross-creator negative, never permanent, **never purchasable** | - |
| REF-01 | register | new-record-required | Missing from reviewed L-track evidence: Reconcile provider-initiated refunds from the webhook, idempotent on the provider event ID — **ships first, needs no new permission** | - |
| REF-02 | register | new-record-required | Missing from reviewed L-track evidence: **In-product refund initiation via partner OAuth with a refund scope** on the linked account | - |
| REF-03 | register | new-record-required | Missing from reviewed L-track evidence: Never hold creator API keys to refund as them (§25.5) | - |
| REF-04 | register | new-record-required | Missing from reviewed L-track evidence: Full refund record per §10.10.2 — our id and idempotency key, provider ids, amount, status transitions, speeds requested and processed, reason code and text, initiator, origin, event ids, ARN, timing, failure code, balance context, links to alert, receipt and supporter | - |
| REF-05 | register | new-record-required | Missing from reviewed L-track evidence: State machine: requested → accepted → processing → processed, with rejected, failed and bank-reversed branches; webhook-driven, never time-inferred | - |
| REF-06 | register | new-record-required | Missing from reviewed L-track evidence: Cumulative partial-refund tracking; never exceed the payment | - |
| REF-07 | register | new-record-required | Missing from reviewed L-track evidence: Derived numbers recompute with no special handling — the §19.6 payoff | - |
| REF-08 | register | new-record-required | Missing from reviewed L-track evidence: Receipt reflects live refund state (`VID-04`) | - |
| REF-09 | register | new-record-required | Missing from reviewed L-track evidence: Refund appears in the Activity Log and the payment detail timeline | - |
| REF-10 | register | new-record-required | Missing from reviewed L-track evidence: **No on-stream change** — the alert and the TTS that already played are not rewritten | - |
| REF-11 | register | new-record-required | Missing from reviewed L-track evidence: Refund of a Compatibility-Routing signal is impossible and **fails loudly** (§25.3) | - |
| REF-12 | register | new-record-required | Missing from reviewed L-track evidence: Refund ordered behind its payment; never applied to an unrecorded payment | - |
| REF-13 | register | new-record-required | Missing from reviewed L-track evidence: **Chargebacks and disputes are a separate state machine**, provider-driven, with an evidence pack | - |
| REF-14 | register | new-record-required | Missing from reviewed L-track evidence: Repeated-refund risk signal, private to that creator, never automatic, never cross-creator | - |
| REF-15 | register | new-record-required | Missing from reviewed L-track evidence: Owner and admin may refund; operator and moderator never | - |
| REF-16 | register | new-record-required | Missing from reviewed L-track evidence: Reason required, undo window before submission rather than a confirmation dialog | - |
| REF-17 | register | new-record-required | Missing from reviewed L-track evidence: Supporter sees status and expected credit window from the receipt link, with no login | - |
| REF-18 | register | new-record-required | Missing from reviewed L-track evidence: **No refund copy states a tax consequence** until the CA review closes | - |
| REF-19 | register | new-record-required | Missing from reviewed L-track evidence: Insufficient-balance and post-settlement refunds surfaced as an explained state, not a generic failure | - |
| REF-20 | register | new-record-required | Missing from reviewed L-track evidence: Every provider field and behaviour in §10.10 carries a dated source per §27.2 before it is built against | - |
| SAF-30 | register | new-record-required | Missing from reviewed L-track evidence: Metrics as histograms: cache hit rate overall and per language, residual rate, **cost per thousand messages**, terms promoted per week, creator-reported false negatives, L3-vs-L4 agreement | - |
| CUS-01 | register | new-record-required | Missing from reviewed L-track evidence: Four-switch model (entitled / enabled / configured / active) applied universally | - |
| CUS-02 | register | new-record-required | Missing from reviewed L-track evidence: Per-widget full config surface (§15.2) | - |
| CUS-03 | register | new-record-required | Missing from reviewed L-track evidence: Locked capabilities shown with the unlocking tier, never hidden or dead | - |
| CUS-04 | register | new-record-required | Missing from reviewed L-track evidence: Downgrade preserves configuration; over-limit items read-only | - |
| CUS-05 | register | new-record-required | Missing from reviewed L-track evidence: Preset bundles that are fully editable afterwards | - |
| CUS-06 | register | new-record-required | Missing from reviewed L-track evidence: Per-source alert styling. UPI-tip styling is v1; a **Super Chat style is Phase 4**, since there is no such source in v1 | - |
| LOB-01 | register | new-record-required | Missing from reviewed L-track evidence: Session create: game, region, mode, platform, time, seats, reserves, policy | - |
| LOB-02 | register | new-record-required | Missing from reviewed L-track evidence: Public waitlist; code never on stream | - |
| LOB-03 | register | new-record-required | Missing from reviewed L-track evidence: Ready check | - |
| LOB-04 | register | new-record-required | Missing from reviewed L-track evidence: Single-use, short-lived private seat token | - |
| LOB-05 | register | new-record-required | Missing from reviewed L-track evidence: Code revealed only after readiness confirmed | - |
| LOB-06 | register | new-record-required | Missing from reviewed L-track evidence: No-show expiry and automatic reserve promotion | - |
| LOB-07 | register | new-record-required | Missing from reviewed L-track evidence: Six eligibility modes, policy locked and displayed before joining | - |
| LOB-08 | register | new-record-required | Missing from reviewed L-track evidence: Redacted audit log incl. moderator override reason | - |
| LOB-09 | register | new-record-required | Missing from reviewed L-track evidence: Aggregate-only public overlay module | - |
| LOB-10 | register | new-record-required | Missing from reviewed L-track evidence: Companion operator console | - |
| LOB-11 | register | new-record-required | Missing from reviewed L-track evidence: Automatic deletion of temporary lobby data | - |
| LOB-12 | register | new-record-required | Missing from reviewed L-track evidence: Time-bound suspensions with appeal; never keyed on payment identity | - |
| LOB-13 | register | new-record-required | Missing from reviewed L-track evidence: Session templates | - |
| LOB-14 | register | new-record-required | Missing from reviewed L-track evidence: Language / region / platform / accessibility filters | - |
| LOB-15 | register | new-record-required | Missing from reviewed L-track evidence: Voluntary skill bands, friend-group locking | - |
| LOB-16 | register | new-record-required | Missing from reviewed L-track evidence: Creator squads with attributed operator actions | - |
| LOB-17 | register | new-record-required | Missing from reviewed L-track evidence: Lobby reputation, no public shaming | - |
| LOB-18 | register | new-record-required | Missing from reviewed L-track evidence: Post-match pulse with private reporting | - |
| LOB-19 | register | new-record-required | Missing from reviewed L-track evidence: Clip consent before featuring a player | - |
| LOB-20 | register | new-record-required | Missing from reviewed L-track evidence: Cross-creator combined queues | - |
| LOB-21 | register | new-record-required | Missing from reviewed L-track evidence: Recurring community nights with reminders | - |
| LOB-22 | register | new-record-required | Missing from reviewed L-track evidence: Screened Guest Queue (audio-only, time-boxed) | - |
| LOB-23 | register | new-record-required | Missing from reviewed L-track evidence: Paid roulette, wagering, prize pools, paid WebRTC, viewer uploads | - |
| GIV-01 | register | new-record-required | Missing from reviewed L-track evidence: Creator-defined prize, entry method, window, draw method, published up front | - |
| GIV-02 | register | new-record-required | Missing from reviewed L-track evidence: Free entry route always available; no paid-only entry | - |
| GIV-03 | register | new-record-required | Missing from reviewed L-track evidence: Deterministic seeded draw, seed and entrant count recorded | - |
| GIV-04 | register | new-record-required | Missing from reviewed L-track evidence: Override possible but logged and labelled | - |
| GIV-05 | register | new-record-required | Missing from reviewed L-track evidence: Terms: creator is promoter, responsible for eligibility, tax and delivery | - |
| GIV-06 | register | new-record-required | Missing from reviewed L-track evidence: Overlay: entry count, timer, consented winner, no address on stream | - |
| GIV-07 | register | new-record-required | Missing from reviewed L-track evidence: Legal review before any chance-based format ships in India | - |
| TRN-01 | register | new-record-required | Missing from reviewed L-track evidence: Single-elimination brackets up to 8 (Creator) | - |
| TRN-01b | register | new-record-required | Missing from reviewed L-track evidence: Double elimination, round robin, points, seeding, sponsor slots (Studio) | - |
| TRN-02 | register | new-record-required | Missing from reviewed L-track evidence: Seeding by attendance, creator pick, or published-seed random | - |
| TRN-03 | register | new-record-required | Missing from reviewed L-track evidence: Check-in windows, scheduling, reminders | - |
| TRN-04 | register | new-record-required | Missing from reviewed L-track evidence: Score reporting with dispute note | - |
| TRN-05 | register | new-record-required | Missing from reviewed L-track evidence: Standings overlay module | - |
| TRN-06 | register | new-record-required | Missing from reviewed L-track evidence: Sponsor slot with exposure log | - |
| AUD-01 | register | new-record-required | Missing from reviewed L-track evidence: Custom alert sounds, tier-gated | - |
| AUD-02 | register | new-record-required | Missing from reviewed L-track evidence: Widget / module / milestone sounds | - |
| AUD-03 | register | new-record-required | Missing from reviewed L-track evidence: Supporter-triggerable soundboard, cooldown and queue | - |
| AUD-04 | register | new-record-required | Missing from reviewed L-track evidence: Per-bracket and per-source sound selection | - |
| AUD-05 | register | new-record-required | Missing from reviewed L-track evidence: BRB / countdown music bed | - |
| AUD-06 | register | new-record-required | Missing from reviewed L-track evidence: Rights attestation checkbox with recorded timestamp | - |
| AUD-07 | register | new-record-required | Missing from reviewed L-track evidence: Terms text placing copyright liability on the creator | - |
| AUD-08 | register | new-record-required | Missing from reviewed L-track evidence: Upload audit record, immediate disable, takedown handling | - |
| AUD-09 | register | new-record-required | Missing from reviewed L-track evidence: Duration, size and format caps; scan pipeline applied | - |
| AUD-10 | register | new-record-required | Missing from reviewed L-track evidence: Asset storage quota enforcement (MED-13 dependency) | - |
| AUD-11 | register | new-record-required | Missing from reviewed L-track evidence: Shared or discoverable music library | - |
| RT-01 | register | active-record | - | active/tasks/RT-01.md, tests/TC-RT-01-overlay-idle-replay.md, reviews/2026-09-15-rt-01-overlay-idle-replay.md |
| RT-02 | register | active-record | - | active/tasks/RT-02.md, tests/TC-RT-02-overlay-channel-fanout.md, reviews/2026-09-15-rt-02-overlay-channel-fanout.md |
| RT-03 | register | active-record | - | active/tasks/RT-03.md, tests/TC-RT-03-checks-synthesis-release.md, reviews/2026-09-16-rt-03-checks-synthesis-release.md |
| RT-04 | register | active-record | - | active/tasks/RT-04.md, tests/TC-RT-04-webhook-commit-and-leased-dispatcher.md, reviews/2026-09-16-rt-04-webhook-commit-and-leased-dispatcher.md |
| RT-05 | register | active-record | - | active/tasks/RT-05.md, tests/TC-RT-05-dispatcher-is-the-only-scanner.md, reviews/2026-09-16-rt-05-dispatcher-is-the-only-scanner.md |
| RT-06 | register | active-record | - | active/tasks/RT-06.md, tests/TC-RT-06-budget-histograms.md, reviews/2026-09-16-rt-06-budget-histograms.md |
| RT-07 | register | new-record-required | Missing from reviewed L-track evidence: Real evidence: Chromium-in-OBS harness · low-end Android · 3G profile · staged test at **2,000 concurrent overlays** · **8-hour OBS soak** with flat memory and node count | - |
| RT-08 | register | active-record | - | active/tasks/RT-08.md, tests/TC-RT-08-enable-outbox-recovery-schedule.md, reviews/2026-09-16-rt-08-enable-outbox-recovery-schedule.md |
| RT-09 | register | new-record-required | Missing from reviewed L-track evidence: No "lag-free / fast / smooth / one source replaces twelve" claim publishable until RT-01..RT-07 close — enforced through the marketing snapshot (§20.4) | - |
| RT-10 | register | active-record | - | active/tasks/RT-10.md, tests/TC-RT-10-backpressure.md, reviews/2026-09-16-rt-10-rt-11-rt-12-read-path-discipline.md |
| RT-11 | register | active-record | - | active/tasks/RT-11.md, tests/TC-RT-11-read-timeout.md, reviews/2026-09-16-rt-11-read-timeout.md |
| RT-12 | register | active-record | - | active/tasks/RT-12.md, tests/TC-RT-12-explain-plans.md, reviews/2026-09-16-rt-12-explain-plans.md |
| RT-13 | register | new-record-required | Missing from reviewed L-track evidence: Per-channel live-transport cap counted across Canvas and standalone widgets; over-cap widgets degrade to slow snapshot polling with a visible notice (§21.3) | - |
| PRF-01 | register | new-record-required | Missing from reviewed L09 evidence: no explicit histogram buckets or cross-instance aggregation prove p95/p99 on every budgeted path; no CI-enforced performance budget/fail threshold exists, and L09-03 staging topology scrape/latency is Not run. Averages/duration totals cannot falsify the p99 budget. | - |
| PRF-02 | register | new-record-required | Missing from reviewed L03/L16 evidence: no Master Canvas runtime combines modules into one OBS browser source, one connection and one requestAnimationFrame loop; no pure-module composition/error isolation, protected one-per-canvas Free watermark/reserved zone, paid-brand-free composition, or ALQ-18/PRF-02/OVL-E8, OVL-E9 and OVL-E10 local proof exists. | - |
| PRF-03 | register | new-record-required | Missing from reviewed L-track evidence: Composite-only animation; no layout-triggering properties | - |
| PRF-04 | register | new-record-required | Missing from reviewed L03 evidence: no authoritative DOM-cardinality/recycling policy spans Master Canvas modules, no 8-hour OBS soak measures flat node count/memory, and no OVL-E1 proof exists; bounded display grouping/timer cleanup is not DOM recycling or a flat long-run node count. | - |
| PRF-05 | register | new-record-required | Missing from reviewed L-track evidence: Idle modules fully unsubscribed | - |
| PRF-06 | register | new-record-required | Missing from reviewed L03 evidence: no server-side sampling or source-specific rate-limit/backpressure policy exists for live reactions/chat, with no reaction/chat ingress source path or per-source coalescing proof and no PRF-06/raid-load evidence; generic HTTP limiting/presentation settings do not establish reaction/chat sampling. | - |
| PRF-07 | register | new-record-required | Missing from reviewed L-track evidence: Burst coalescing on long-gap replay | - |
| PRF-08 | register | new-record-required | Missing from reviewed L16 evidence: no server-side read-through cache for derived aggregate projections is keyed/bounded per channel/widget or invalidated from durable events; WidgetPoller retains interval polling/fallback, and no cache invalidation, stampede, stale-read, or correctness proof establishes the universal §19.6 requirement. | - |
| PRF-09 | register | mapped-existing | §31.18 L03 task/test/review trio covers fail-closed `DATABASE_URL_DIRECT` validation rejecting same app/direct endpoint, invalid scheme and pooled/pooler forms; LISTEN wake-up optimization and durable cursor replay correctness are evidenced, while deployed cross-replica/capacity/OBS staging remains open | tasks/L03-alerts-web-and-creator-api.md, tests/TC-L03-alerts-web-and-creator-api.md, reviews/2026-08-16-L03-corrected-findings-remediation-review.md |
| PRF-10 | register | new-record-required | Missing from reviewed L03 evidence: no reviewed proof establishes a universal bounded-page cursor contract across every live surface; the history-specific composite implementation does not close that universal/bounded gap. | - |
| PRF-11 | register | new-record-required | Missing from reviewed L03/L16 evidence: no reviewed composite-index inventory or checked-in EXPLAIN ANALYZE output proves every widget-backing query’s index plan; no query-change recheck guard or PRF-11/RT-12 universal proof exists. | - |
| PRF-12 | register | new-record-required | Missing from reviewed L-track evidence: Asset budgets: Lottie complexity, audio length, server-side image pre-scaling | - |
| PRF-13 | register | new-record-required | Missing from reviewed L-track evidence: No third-party scripts in the overlay | - |
| PRF-14 | register | new-record-required | Missing from reviewed L-track evidence: Per-module error boundaries; twice-failed module stays down with a note | - |
| PRF-15 | register | new-record-required | Missing from reviewed L-track evidence: Companion: optimistic UI, virtualised lists, no re-render storms | - |
| PRF-16 | register | new-record-required | Missing from reviewed L-track evidence: Published one-source-vs-many benchmark, re-run in CI | - |
| PRF-17 | register | new-record-required | Missing from reviewed L03/L16 evidence: no authoritative end-to-end §12.7 inventory/test proves every surface bounded—dashboard summary-first, per-tab lazy/cursor pagination and >50 virtualised; tip page optional widgets/social after first paint; Master Canvas bounded queue; every widget server-side aggregated/capped; Companion virtualisation/no continuous React state. | - |
| PRF-18 | register | new-record-required | Missing from reviewed L-track evidence: Exports run as background jobs, never by rendering rows into a page | - |
| PRF-19 | register | new-record-required | Missing from reviewed L03/L01 evidence: no every-endpoint field-projection/payload-cap inventory or `select *` enforcement is proven; selected projections do not close the universal endpoint requirement. | - |
| WMK-01 | register | new-record-required | Missing from reviewed L03/L16 evidence: no Canvas renderer implements exactly one protected top layer after every module outside module/error boundaries; no fault test proves module failure preserves watermark, and no WMK-01/ALQ-18/PRF-02/OVL-E8 local proof exists. | - |
| WMK-02 | register | new-record-required | Missing from reviewed L03 evidence: no Canvas editor has a reserved protected fixed-corner safe zone and refuses module placement/resize/overlap into it; no one-watermark coordinate ownership/collision test or WMK-02/OVL-E9 proof exists. | - |
| WMK-03 | register | new-record-required | Missing from reviewed L-track evidence: Watermark on a standalone widget only when it is the channel's only active overlay source | - |
| WMK-04 | register | new-record-required | Missing from reviewed L-track evidence: Tip-page attribution line on Free only (MKT-05) | - |
| WMK-05 | register | new-record-required | Missing from reviewed L03/L20 evidence: no authoritative per-tier rendering/surface inventory or tests establish zero marketing attribution for every paid tier across overlay/Canvas, standalone widgets, tip page, end-cards, QR, TTS and promotional email; no narrow legal/transactional issuer-identity carve-out enforcement/projection test exists for WMK-05; no WMK-05 all-surface/completeness proof exists. | - |
| WMK-06 | register | new-record-required | Missing from reviewed L-track evidence: Branding never injected mid-stream on lapse; Free fallback mark appears only on the next clean overlay reload after pause | - |
| WMK-07 | register | new-record-required | Missing from reviewed L-track evidence: No external-layer detection, scene inspection or covering-check telemetry — ever | - |
| CTL-01 | register | new-record-required | Missing from reviewed L-track evidence: Capability registry table with versioned, audited rows | - |
| CTL-02 | register | new-record-required | Missing from reviewed L-track evidence: Resolution order engine (kill → denylist → rollout → tier → override) | - |
| CTL-03 | register | new-record-required | Missing from reviewed L-track evidence: Per-channel resolved blob, versioned and cached; never per-capability queries | - |
| CTL-04 | register | new-record-required | Missing from reviewed L-track evidence: Admin UI: master switch, retier, edit limits, kill | - |
| CTL-05 | register | new-record-required | Missing from reviewed L-track evidence: Impact preview ("affects 214 channels, 3 live") | - |
| CTL-06 | register | new-record-required | Missing from reviewed L-track evidence: Staged effective-time changes | - |
| CTL-07 | register | new-record-required | Missing from reviewed L-track evidence: Two-staff approval on every change; **owner sign-off for paid→Free moves**; single-admin `global_kill` for incidents | - |
| CTL-08 | register | new-record-required | Missing from reviewed L-track evidence: One-action revert to previous version | - |
| ENV-01 | register | active-record | - | active/tasks/ENV-01.md, tests/TC-ENV-01-measurement-environment.md, reviews/2026-09-15-env-01-measurement-control.md |
| ENV-02 | register | active-record | - | active/tasks/ENV-02.md, tests/TC-ENV-02-measurement-environment.md, reviews/2026-09-15-env-02-measurement-control.md |
| ENV-03 | register | active-record | - | active/tasks/ENV-03.md, tests/TC-ENV-03-measurement-environment.md, reviews/2026-09-15-env-03-measurement-control.md |
| ENV-04 | register | active-record | - | active/tasks/ENV-04.md, tests/TC-ENV-04-measurement-environment.md, reviews/2026-09-15-env-04-measurement-control.md |
| ENV-05 | register | active-record | - | active/tasks/ENV-05.md, tests/TC-ENV-05-measurement-environment.md, reviews/2026-09-15-env-05-measurement-control.md |
| ENV-06 | register | active-record | - | active/tasks/ENV-06.md, tests/TC-ENV-06-measurement-environment.md, reviews/2026-09-15-env-06-measurement-control.md |
| ENV-07 | register | active-record | - | active/tasks/ENV-07.md, tests/TC-ENV-07-measurement-environment.md, reviews/2026-09-15-env-07-measurement-control.md |
| ENV-08 | register | active-record | - | active/tasks/ENV-08.md, tests/TC-ENV-08-measurement-environment.md, reviews/2026-09-15-env-08-measurement-control.md |
| ENV-09 | register | active-record | - | active/tasks/ENV-09.md, tests/TC-ENV-09-measurement-environment.md, reviews/2026-09-15-env-09-measurement-control.md |
| CTL-09 | register | new-record-required | Missing from reviewed L-track evidence: Layer 1 correctness dimensions rejected from this panel | - |
| CTL-14 | register | new-record-required | Missing from reviewed L-track evidence: **Registry rejects any capability whose subject is a durable creator record (§12.6)** — no row may be created that gates storing, viewing, searching, fetching or exporting one. Enforced in the registry, not by review | - |
| CTL-15 | register | new-record-required | Missing from reviewed L-track evidence: Retention is a single platform-wide value, not a per-tier limit; the schema offers no per-tier retention field to set | - |
| CTL-10 | register | new-record-required | Missing from reviewed L-track evidence: `GET /v1/public/capability-matrix` published snapshot | - |
| CTL-11 | register | new-record-required | Missing from reviewed L-track evidence: Marketing build reads the snapshot; webhook revalidation | - |
| CTL-12 | register | new-record-required | Missing from reviewed L-track evidence: Marketing sections behind flags (`kind = marketing_section`) | - |
| CTL-13 | register | new-record-required | Missing from reviewed L-track evidence: Admin MFA + durable admin registry (ADM-07 dependency) | - |
| WID-01 | register | new-record-required | Missing from reviewed L-track evidence: Companion tap source (+1 win / +1 loss) | - |
| WID-02 | register | new-record-required | Missing from reviewed L-track evidence: Lobby/tournament auto-fill of results | - |
| WID-03 | register | new-record-required | Missing from reviewed L-track evidence: Wins This Season, Session Record, Win Streak | - |
| WID-04 | register | new-record-required | Missing from reviewed L-track evidence: Personal Best, Rank Progress, Season Objective | - |
| WID-05 | register | new-record-required | Missing from reviewed L-track evidence: Head-to-Head, Scoreboard | - |
| WID-06 | register | new-record-required | Missing from reviewed L-track evidence: Match Countdown, Tournament Standings, Squad Roster | - |
| WID-07 | register | new-record-required | Missing from reviewed L-track evidence: Hours Streamed, Milestone Ticker, Top Clip, Recap Card | - |
| COS-01 | register | new-record-required | Missing from reviewed L-track evidence: Room create, explicit mutual accept, short-lived grants | - |
| COS-02 | register | new-record-required | Missing from reviewed L-track evidence: Public `/live/collab/<id>` page with two IFrame players | - |
| COS-03 | register | new-record-required | Missing from reviewed L-track evidence: Eight layout modes | - |
| COS-04 | register | new-record-required | Missing from reviewed L-track evidence: Switch Window with published range, countdown, override | - |
| COS-05 | register | new-record-required | Missing from reviewed L-track evidence: One audio source at a time, viewer-switchable | - |
| COS-06 | register | new-record-required | Missing from reviewed L-track evidence: Shared event rail, timer, scorecard | - |
| COS-07 | register | new-record-required | Missing from reviewed L-track evidence: Side-assigned supporter alerts | - |
| COS-08 | register | new-record-required | Missing from reviewed L-track evidence: Chat tabs per creator | - |
| COS-09 | register | new-record-required | Missing from reviewed L-track evidence: Companion control room incl. one-tap safe layout | - |
| COS-10 | register | new-record-required | Missing from reviewed L-track evidence: OBS collaboration overlay scene export | - |
| COS-11 | register | new-record-required | Missing from reviewed L-track evidence: Contribution selector (A / B / shared goal) | - |
| COS-12 | register | new-record-required | Missing from reviewed L-track evidence: Instant revoke; page degrades to single or ended state | - |
| COS-13 | register | new-record-required | Missing from reviewed L-track evidence: Explicit "feeds are not frame-synced" UI treatment | - |
| COS-14 | register | new-record-required | Missing from reviewed L-track evidence: Clip handoff consent | - |
| COS-15 | register | new-record-required | Missing from reviewed L-track evidence: Silent payment splitting | - |
| SND-01 | register | new-record-required | Missing from reviewed L-track evidence: Moment = sound + animation + sticker + TTS style + effect, creator-curated | - |
| SND-02 | register | new-record-required | Missing from reviewed L-track evidence: Amount-tiered moment catalogue | - |
| SND-03 | register | new-record-required | Missing from reviewed L-track evidence: Loudness normalisation and duration caps | - |
| SND-04 | register | new-record-required | Missing from reviewed L-track evidence: Per-sound, per-viewer, stream-wide cooldowns | - |
| SND-05 | register | new-record-required | Missing from reviewed L-track evidence: Themed packs incl. Indic and festival | - |
| SND-06 | register | new-record-required | Missing from reviewed L-track evidence: Companion mute / skip / pause / emergency safe mode | - |
| SND-07 | register | new-record-required | Missing from reviewed L-track evidence: No remote URL execution in the overlay | - |
| RUL-01 | register | new-record-required | Missing from reviewed L-track evidence: Rules engine: thresholds, modes, cooldowns, caps, priority, approval | - |
| RUL-02 | register | new-record-required | Missing from reviewed L-track evidence: Never-interrupt-gameplay mode | - |
| RUL-03 | register | new-record-required | Missing from reviewed L-track evidence: Overlay-offline hold-and-replay | - |
| GOA-01 | register | new-record-required | Missing from reviewed L-track evidence: **Completion latch** — `goal_completed` written once, idempotently, with the closing contribution and the derived total. Actions fire from the event, never from a recomputed boolean | - |
| GOA-02 | register | new-record-required | Missing from reviewed L-track evidence: A refund never un-completes a goal; it is recorded against it and the progress display shows the true derived figure | - |
| GOA-03 | register | new-record-required | Missing from reviewed L-track evidence: Manual reopen is explicit, audited and reason-required — never an automatic consequence of arithmetic | - |
| GOA-04 | register | new-record-required | Missing from reviewed L-track evidence: Goal triggers: 100% · percentage and absolute thresholds · first contribution · the closer · biggest single · stretch steps · stalled N minutes · expired unmet · ladder step · all/any goals complete | - |
| GOA-05 | register | new-record-required | Missing from reviewed L-track evidence: Session triggers: session total · Nth supporter · new top supporter · first-time · returning supporter | - |
| GOA-06 | register | new-record-required | Missing from reviewed L-track evidence: Platform triggers — Super Chat, membership, gifting, like and viewer milestones | - |
| GOA-07 | register | new-record-required | Missing from reviewed L-track evidence: Community triggers — challenge, lobby, tournament, giveaway | - |
| GOA-08 | register | new-record-required | Missing from reviewed L-track evidence: Operational triggers — stream start/end, scene change, Clutch enter/leave, sponsor segment | - |
| GOA-09 | register | new-record-required | Missing from reviewed L-track evidence: Per-trigger controls: enabled · threshold · once-per-stream / every time / max N · cooldown · minimum contribution · quiet window · which contribution sources count | - |
| GOA-10 | register | new-record-required | Missing from reviewed L-track evidence: Overlay actions: celebration, confetti, bounded takeover, banner, ticker, progress flourish, module swap, theme swap, closer card, scene preset | - |
| GOA-11 | register | new-record-required | Missing from reviewed L-track evidence: Audio actions: Sound Moment, sting, TTS announcement **through the §12.2 pipeline**, audio duck | - |
| GOA-12 | register | new-record-required | Missing from reviewed L-track evidence: Goal-lifecycle actions: complete · **auto-advance the ladder** · **auto-create next** (`+₹X`, `×N`, template, repeat) · **roll overflow in or discard** · convert to stretch · extend · pause · archive · reset | - |
| GOA-13 | register | new-record-required | Missing from reviewed L-track evidence: Creator actions: Companion push · Live Deck banner · suggested next action · **stream marker** into the Wrap Stream summary | - |
| GOA-14 | register | new-record-required | Missing from reviewed L-track evidence: Supporter actions: thank-you card naming the closer **with visibility consent** · badge grant · receipt note | - |
| GOA-15 | register | new-record-required | Missing from reviewed L-track evidence: Outbound actions, **approve-then-send by default**: YouTube chat announcement, Discord, Telegram, WhatsApp opt-in, social card | - |
| GOA-16 | register | new-record-required | Missing from reviewed L-track evidence: OBS actions via the local helper: scene switch, source toggle, replay-buffer save, approved Streamer.bot or SAMMI action | - |
| GOA-17 | register | new-record-required | Missing from reviewed L-track evidence: Sponsor actions: reveal card, log exposure with timestamp for proof-of-delivery | - |
| GOA-18 | register | new-record-required | Missing from reviewed L-track evidence: **Ordered action sequences with per-step delays**, not a set | - |
| GOA-19 | register | new-record-required | Missing from reviewed L-track evidence: Conditions: only live · named scenes · not in Clutch · not during a sponsor segment · tier · overlay connected · outside quiet hours | - |
| GOA-20 | register | new-record-required | Missing from reviewed L-track evidence: **Interlocks, not creator-configurable**: Clutch suppresses loud and full-screen and defers rather than drops · never interrupt an alert mid-play · never-interrupt-gameplay holds takeovers · all text through §12.2 · our rate limits, not the platform's rejection | - |
| GOA-21 | register | new-record-required | Missing from reviewed L-track evidence: Prepare-not-fire default for anything outbound or public (§5.4); low-risk local actions may auto-fire | - |
| GOA-22 | register | new-record-required | Missing from reviewed L-track evidence: Text templates with `{goal_name}` `{target}` `{raised}` `{remaining}` `{percent}` `{closer}` `{top_supporter}` `{supporter_count}` `{session_total}` `{next_goal}`, per language | - |
| GOA-23 | register | new-record-required | Missing from reviewed L-track evidence: Every action configurable to §15.2 depth — sound, animation, duration, easing, safe-zone position, colour, size, or absent | - |
| GOA-24 | register | new-record-required | Missing from reviewed L-track evidence: **Sequence preview** fires the whole composition on the overlay in a marked test mode that auto-reverts | - |
| GOA-25 | register | new-record-required | Missing from reviewed L-track evidence: Presets — Quiet · Standard · Hype — each fully editable afterwards (§15.3) | - |
| GOA-26 | register | new-record-required | Missing from reviewed L-track evidence: Overflow rolled into the next goal or discarded, creator's choice, recorded either way | - |
| GOA-27 | register | new-record-required | Missing from reviewed L-track evidence: Goal detail view follows the §7.2 contract, with a timeline of every contribution and every rule that fired | - |
| GOA-28 | register | new-record-required | Missing from reviewed L-track evidence: **"Why this number?"** explains a goal total from its contributions including refunds (§7.3) | - |
| GOA-29 | register | new-record-required | Missing from reviewed L-track evidence: YouTube goal actions are Phase 4 and narrower than expected: announce, pin, one title update per stream, poll. **Never a purchase or a gift** (§4) | - |
| SEC-01 | register | new-record-required | Missing from reviewed L-track evidence: Short-lived signed overlay capabilities with renewal | - |
| SEC-02 | register | new-record-required | Missing from reviewed L-track evidence: Session/device binding where practical | - |
| SEC-03 | register | new-record-required | Missing from reviewed L-track evidence: Scheduled rotation; never in screenshots, logs or tickets | - |
| MIG-01 | register | new-record-required | Missing from reviewed L-track evidence: Shadow mode with a migration report (delivered, missed, latency, unsupported) | - |
| MIG-02 | register | new-record-required | Missing from reviewed L-track evidence: Test/sandbox mode that never reaches viewers | - |
| MIG-03 | register | new-record-required | Missing from reviewed L-track evidence: Global emergency-disable button | - |
| RTE-01 | register | new-record-required | Missing from reviewed L-track evidence: Routing abstraction: a route is a signal source, not a rail | - |
| RTE-02 | register | new-record-required | Missing from reviewed L-track evidence: Health-state machine (active / degraded / paused / direct available) | - |
| RTE-03 | register | new-record-required | Missing from reviewed L-track evidence: `routed_signal_received → alert_queued → alert_delivered` state class, distinct from `verified_payment` | - |
| RTE-04 | register | new-record-required | Missing from reviewed L-track evidence: Capability restrictions in routing mode (§25.3) enforced server-side | - |
| RTE-05 | register | new-record-required | Missing from reviewed L-track evidence: Per-provider kill switch with confidence threshold | - |
| RTE-06 | register | new-record-required | Missing from reviewed L-track evidence: Explicit in-product acceptance of the Beta terms on enabling a route | - |
| RTE-07 | register | new-record-required | Missing from reviewed L-track evidence: Duplicate/false-signal detection disabling auto-alerts | - |
| RTE-08 | register | new-record-required | Missing from reviewed L-track evidence: Migration prompt when a Direct integration becomes available | - |
| RTE-09 | register | new-record-required | Missing from reviewed L-track evidence: Paytm Business route — **Gated on §25.6 signal mechanism** | - |
| RTE-10 | register | new-record-required | Missing from reviewed L-track evidence: Google Pay Business route (assisted activation) — **Gated on §25.6** | - |
| RTE-11 | register | new-record-required | Missing from reviewed L-track evidence: PhonePe Supervisor route — **Consent-gated on C1–C7** | - |
| RTE-12 | register | new-record-required | Missing from reviewed L-track evidence: HDFC Cashier route — **Consent-gated on C1–C7** | - |
| RTE-13 | register | new-record-required | Missing from reviewed L-track evidence: Amazon Pay consumer-credential route | - |
| RTE-14 | register | new-record-required | Missing from reviewed L-track evidence: Generic QR fallback / "mark as paid" | - |
| RTE-15 | register | new-record-required | Missing from reviewed L-track evidence: Consent flow: explicit, unbundled, revocable, re-confirmed on scope change | - |
| RTE-16 | register | new-record-required | Missing from reviewed L-track evidence: KMS/HSM envelope encryption for any delegated secret, no human read path | - |
| RTE-17 | register | new-record-required | Missing from reviewed L-track evidence: Credential-compromise incident procedure, rehearsed | - |
| LIF-01 | register | new-record-required | Missing from reviewed L-track evidence: Five-state lifecycle (active / grace 14d / paused / retained 90d / expired) | - |
| LIF-02 | register | new-record-required | Missing from reviewed L-track evidence: Grace-period notices in dashboard and Companion, never on stream | - |
| LIF-03 | register | new-record-required | Missing from reviewed L-track evidence: Paused: connectors stop, configuration read-only, nothing deleted | - |
| LIF-04 | register | new-record-required | Missing from reviewed L-track evidence: Retained 90d applies to **encrypted connector secrets only**; configuration, mappings, templates and durable records persist under the uniform retention policy (§12.6.2) and stay exportable | - |
| LIF-05 | register | new-record-required | Missing from reviewed L-track evidence: Expired: credential revocation and paid-only secret deletion, after repeated notice | - |
| LIF-06 | register | new-record-required | Missing from reviewed L-track evidence: Overlay quiet safe state — no payment wall, no on-stream branding change | - |
| LIF-07 | register | new-record-required | Missing from reviewed L-track evidence: Never-charged-for list enforced (receipts, exports, recovery, disconnect, security) — and the full §12.6 durable-record set in every lifecycle state including Expired | - |
| LIF-08 | register | new-record-required | Missing from reviewed L-track evidence: Renewal restores configuration without reconnecting, unless the token expired | - |
| LIF-09 | register | new-record-required | Missing from reviewed L-track evidence: Desktop bridge caches a signed entitlement for 24h | - |
| LIF-10 | register | new-record-required | Missing from reviewed L-track evidence: Free and native behaviour independent of subscription and Platform status | - |
| SOC-01 | register | new-record-required | Missing from reviewed L-track evidence: Event model: 8 relayable event types, approve-then-send default | - |
| SOC-02 | register | new-record-required | Missing from reviewed L-track evidence: Per-destination queue with cooldown; never send-per-event | - |
| SOC-03 | register | new-record-required | Missing from reviewed L-track evidence: Obey returned rate-limit headers (Discord) rather than hard-coded limits | - |
| SOC-04 | register | new-record-required | Missing from reviewed L-track evidence: Health states per destination, mirroring §25.2 | - |
| SOC-05 | register | new-record-required | Missing from reviewed L-track evidence: Discord webhook + rich embeds + bot commands | - |
| SOC-06 | register | new-record-required | Missing from reviewed L-track evidence: YouTube: broadcast metadata, chat announcements, polls, pinned moments | - |
| SOC-07 | register | new-record-required | Missing from reviewed L-track evidence: YouTube post-stream wrap with timestamps | - |
| SOC-08 | register | new-record-required | Missing from reviewed L-track evidence: Instagram: Reels/feed publish, clip-to-Reel draft, comment inbox | - |
| SOC-09 | register | new-record-required | Missing from reviewed L-track evidence: WhatsApp: opt-in, approved templates, 24h window respected, template cost shown | - |
| SOC-10 | register | new-record-required | Missing from reviewed L-track evidence: Twitch EventSub + Channel Point mapping | - |
| SOC-11 | register | new-record-required | Missing from reviewed L-track evidence: Kick OAuth 2.1 connector within granted scopes | - |
| SOC-12 | register | new-record-required | Missing from reviewed L-track evidence: Snapchat Creative Kit hand-off, creator taps final share | - |
| SOC-13 | register | new-record-required | Missing from reviewed L-track evidence: Telegram bot channel alerts | - |
| SOC-14 | register | new-record-required | Missing from reviewed L-track evidence: Upload-forced-private disclosure until Google audits the project | - |
| SOC-15 | register | new-record-required | Missing from reviewed L-track evidence: Lapse: manual share kept, auto-send stopped, no message to the audience | - |
| SOC-16 | register | new-record-required | Missing from reviewed L-track evidence: Auto-posting every tip/follower/alert anywhere | - |
| SOC-17 | register | new-record-required | Missing from reviewed L-track evidence: YouTube Community posts, IG personal accounts, unsolicited DMs, WhatsApp groups, Snapchat background posting | - |
| PCK-01 | register | new-record-required | Missing from reviewed L-track evidence: Pack as a capability-registry row, additive, lifecycle-aware | - |
| PCK-02 | register | new-record-required | Missing from reviewed L-track evidence: AI Credits pack — ₹49/₹149/₹399, paid tiers only. Ships once the **measured** cost model exists; the ledger half is in `0081` | - |
| PCK-03 | register | new-record-required | Missing from reviewed L-track evidence: Socials Pack — ₹129/mo, Creator+. Target initial set, but cannot precede Social Relay (Phase 7) | - |
| PCK-04 | register | new-record-required | Missing from reviewed L-track evidence: Events Pack — ₹129/mo, Creator+. Hidden until lobby/tournament features exist | - |
| PCK-05 | register | new-record-required | Missing from reviewed L-track evidence: Team Seats pack — ₹129/mo, Creator+. Hidden until seat management ships (F18) | - |
| PCK-06 | register | new-record-required | Missing from reviewed L-track evidence: Storage Pack — ₹49/mo for +500MB of **new-upload** space, Pro+. Never affects historical records. **Nearest to ready**; needs MED-13/AUD-10 enforcement first | - |
| PCK-07 | register | new-record-required | Missing from reviewed L-track evidence: Sponsor Pack — ₹149/mo, Creator+. Hidden until the sponsor manager exists | - |
| PCK-08 | register | new-record-required | Missing from reviewed L-track evidence: Multi-Channel Pack — ₹199/mo per added channel, Creator+. Target initial set, but **last of the four to be ready**: blocked on the tenant-isolation suite (§37.6). The ₹598-vs-₹599 comparison with Studio is deliberate (§28.3.3) | - |
| PCK-09 | register | new-record-required | Missing from reviewed L-track evidence: **Finance Pack** — statement, GST-ready export, TDS notes, payout reconciliation. Hidden until the CA/tax evidence row closes; sells the *prepared statement*, never access to the underlying records | - |
| PCK-10 | register | new-record-required | Missing from reviewed L-track evidence: Pack attach-rate reporting to inform future tier composition | - |
| PCK-11 | register | new-record-required | Missing from reviewed L-track evidence: Hidden packs exist as registry rows so they become visible without a release | - |
| PCK-12 | register | new-record-required | Missing from reviewed L-track evidence: No pack, top-up or tier may sell retention, history depth, record search or export — enforced by CTL-14 | - |
| PCK-13 | register | new-record-required | Missing from reviewed L-track evidence: Pack system launches with whatever is ready — arrival order Storage → AI Credits → Socials → Multi-Channel — not held for a fixed set of four | - |
| PCK-14 | register | new-record-required | Missing from reviewed L-track evidence: A lapsed pack pauses added capacity only; over-quota assets go read-only and stay viewable and exportable | - |
| PCK-15 | register | new-record-required | Missing from reviewed L-track evidence: Multi-Channel Pack blocked until the §37.6 tenant-isolation suite passes | - |
| JOB-01 | register | new-record-required | Missing from reviewed L-track evidence: Content calendar + public schedule page with notify-me | - |
| JOB-02 | register | new-record-required | Missing from reviewed L-track evidence: Consistency view: streak, hours, rest days framed kindly | - |
| JOB-03 | register | new-record-required | Missing from reviewed L-track evidence: Sponsor deliverable tracker with proof | - |
| JOB-04 | register | new-record-required | Missing from reviewed L-track evidence: Clip request queue | - |
| JOB-05 | register | new-record-required | Missing from reviewed L-track evidence: Clip-to-social pipeline ending in a draft, never auto-post | - |
| JOB-06 | register | new-record-required | Missing from reviewed L-track evidence: Title/thumbnail performance against our own stream records | - |
| JOB-07 | register | new-record-required | Missing from reviewed L-track evidence: Shareable gear/setup profile | - |
| JOB-08 | register | new-record-required | Missing from reviewed L-track evidence: Collab record | - |
| JOB-09 | register | new-record-required | Missing from reviewed L-track evidence: Community FAQ auto-answers in chat | - |
| JOB-10 | register | new-record-required | Missing from reviewed L-track evidence: Editor payouts / staff revenue splitting | - |
| JOB-11 | register | new-record-required | Missing from reviewed L-track evidence: Full CRM · scheduled cross-posting to all networks · analytics competing with YouTube Studio | - |
| INT-01 | register | new-record-required | Missing from reviewed L-track evidence: **Declarative Canvas Package format** — signed, versioned, runtime-pinned; no JS, no network fetch, no external font or asset URL, no executing CSS, no runtime-reaching expressions | - |
| INT-02 | register | new-record-required | Missing from reviewed L-track evidence: Package validator and signature verification at import and at render | - |
| INT-03 | register | new-record-required | Missing from reviewed L-track evidence: Allowed-animation set — animations are chosen, never authored as code | - |
| INT-04 | register | new-record-required | Missing from reviewed L-track evidence: First-party curated package library authored by us | - |
| INT-05 | register | new-record-required | Missing from reviewed L-track evidence: Private creator packages, tenant-scoped, never shown to another creator | - |
| INT-06 | register | new-record-required | Missing from reviewed L-track evidence: Asset import (SVG, PNG, WebP, audio, video, Lottie) on the §18.3 gate: attestation, quarantine, scan, provenance, takedown | - |
| INT-07 | register | new-record-required | Missing from reviewed L-track evidence: Transcode, normalise and pre-scale on import; content-addressed tenant-scoped storage (§19.1) | - |
| INT-08 | register | new-record-required | Missing from reviewed L-track evidence: Migration wizard: inventory → map → side-by-side preview and diff → publish on approval → reversible | - |
| INT-09 | register | new-record-required | Missing from reviewed L-track evidence: Unmapped items named explicitly; an uncertain mapping shown as uncertain | - |
| INT-10 | register | new-record-required | Missing from reviewed L-track evidence: Connector outbox per destination: queue, backoff, dead-letter, kill switch, idempotency key, redacted delivery log | - |
| INT-11 | register | new-record-required | Missing from reviewed L-track evidence: A bridge failure never delays, cancels, duplicates or alters a BharatStudio alert | - |
| INT-12 | register | new-record-required | Missing from reviewed L-track evidence: Streamlabs bridge — **selected low-frequency event types only**, rate-limited and coalesced below the documented ~2/min guidance, labelled a transition tool | - |
| INT-13 | register | new-record-required | Missing from reviewed L-track evidence: Streamer.bot local adapter in the Companion helper: `localhost` only, explicit pairing, creator-chosen action allow-list | - |
| INT-14 | register | new-record-required | Missing from reviewed L-track evidence: SAMMI local adapter, same shape | - |
| INT-15 | register | new-record-required | Missing from reviewed L-track evidence: Mix It Up local adapter, same shape | - |
| INT-16 | register | new-record-required | Missing from reviewed L-track evidence: StreamElements configuration migration only | - |
| INT-17 | register | new-record-required | Missing from reviewed L-track evidence: StreamElements event bridge — **gate:** confirmed API/partner position | - |
| INT-18 | register | new-record-required | Missing from reviewed L-track evidence: Third-party paid marketplace publishing — **gate:** author payouts, GST on third-party digital goods, content review at scale, takedown and dispute handling, defensible "verified" badge | - |
| INT-19 | register | new-record-required | Missing from reviewed L-track evidence: Never embed a third-party browser-source URL, HTML, JS, CSS or iframe in the Canvas — enforced by the package validator, not by review | - |
| INT-20 | register | new-record-required | Missing from reviewed L-track evidence: Never scrape a competitor dashboard, import a browser-source secret, or execute copied widget code | - |
| CST-01 | register | new-record-required | Missing from reviewed L-track evidence: Three-level model (0 presets / 1 safe presentation / 2 advanced / 3 brand and team) as registry rows, retierable without a release | - |
| CST-02 | register | new-record-required | Missing from reviewed L-track evidence: **Protected string class enforced by the customisation system** — payment, legal, consent, security and error text are never exposed for override | - |
| CST-03 | register | new-record-required | Missing from reviewed L-track evidence: Overlay level 1: free colour, our fonts, position and anchor, show/hide, z-order, opacity, radius, animation, reduced-motion variant, performance mode | - |
| CST-04 | register | new-record-required | Missing from reviewed L-track evidence: Amount / name / message rendering controls incl. hidden amounts and bracket-name-only | - |
| CST-05 | register | new-record-required | Missing from reviewed L-track evidence: **Indic script fallback order per text role** | - |
| CST-06 | register | new-record-required | Missing from reviewed L-track evidence: Overlay level 2: font per role, per-bracket and per-source styling, burst behaviour, do-not-interrupt windows | - |
| CST-07 | register | new-record-required | Missing from reviewed L-track evidence: Per-scene-profile placement and theming; overlay theme follows the OBS scene | - |
| CST-08 | register | new-record-required | Missing from reviewed L-track evidence: Per-aspect-ratio variants (16:9 / 9:16 / 4:3) of one canvas | - |
| CST-09 | register | new-record-required | Missing from reviewed L-track evidence: **Conditional themes** — festival date ranges, time of day | - |
| CST-10 | register | new-record-required | Missing from reviewed L-track evidence: **Sponsor-safe mode** — swap to a neutral theme for a segment and back | - |
| CST-11 | register | new-record-required | Missing from reviewed L-track evidence: **Adversarial preview** — long Indic name, 500-char message, emoji flood | - |
| CST-12 | register | new-record-required | Missing from reviewed L-track evidence: **Brand kit** — palette, type, logo saved once, applied across every surface | - |
| CST-13 | register | new-record-required | Missing from reviewed L-track evidence: Multi-surface templates and package authoring with team approval | - |
| CST-14 | register | new-record-required | Missing from reviewed L-track evidence: Tip page level 1: cover image, avatar shape, tagline, lane order, labelled amount presets, privacy display | - |
| CST-15 | register | new-record-required | Missing from reviewed L-track evidence: Tip page level 2: message settings, pack selection, event layouts, campaign and referral pages, multilingual copy sets | - |
| CST-16 | register | new-record-required | Missing from reviewed L-track evidence: Tip page level 3: full theme with background media, multiple campaign pages with own goal, copy, countdown and schedule | - |
| CST-17 | register | new-record-required | Missing from reviewed L-track evidence: Per-page OG image, title and description | - |
| CST-18 | register | new-record-required | Missing from reviewed L-track evidence: Dashboard: theme, accent, density, landing tab, notification and locale preferences | - |
| CST-19 | register | new-record-required | Missing from reviewed L-track evidence: Dashboard: pinned cards, **named saved views**, saved export column sets, shortcut map | - |
| CST-20 | register | new-record-required | Missing from reviewed L-track evidence: Dashboard: logo and brand accent, per-role default views. **No background images at any tier** | - |
| CST-21 | register | new-record-required | Missing from reviewed L-track evidence: Moderator **preferences** — layout, columns, density, quick-action order | - |
| CST-22 | register | new-record-required | Missing from reviewed L-track evidence: Moderator **policies** — blocked terms per language, link allow/deny, auto-hold, escalation, canned responses, handover notes | - |
| CST-23 | register | new-record-required | Missing from reviewed L-track evidence: Team-managed policy libraries, approval workflows, centrally set moderator layouts | - |
| CST-24 | register | new-record-required | Missing from reviewed L-track evidence: **Permission classes are never customisable** — presets and libraries only inside owner/admin/operator/moderator/viewer | - |
| CST-25 | register | new-record-required | Missing from reviewed L-track evidence: Companion: top-strip stats, health signals shown, saved deck presets | - |
| CST-26 | register | new-record-required | Missing from reviewed L-track evidence: Companion accessibility at level 0 — one-hand mode, colour-blind palette, haptics, language override | - |
| CST-27 | register | new-record-required | Missing from reviewed L-track evidence: Companion team decks pushed to every operator | - |
| CST-28 | register | new-record-required | Missing from reviewed L-track evidence: Receipts and transactional mail: creator logo, accent, thank-you copy per language, reply-to, brand kit — inside §30.6.4 | - |
| CST-29 | register | new-record-required | Missing from reviewed L-track evidence: No customisation increases what a live surface loads (§12.7); themes are data the renderer already holds | - |
| CST-30 | register | new-record-required | Missing from reviewed L-track evidence: Every theme passes contrast and +40% text-expansion checks (§37.7) — a failing theme is a defect, not a taste question | - |
| BOT-01 | register | new-record-required | Missing from reviewed L-track evidence: Command engine: names, aliases, cooldowns, role permissions | - |
| BOT-02 | register | new-record-required | Missing from reviewed L-track evidence: Scheduled and timed messages | - |
| BOT-03 | register | new-record-required | Missing from reviewed L-track evidence: Six-area UI and no more (Commands, Moderation, Automations, Languages, Connected channels, Import) | - |
| BOT-04 | register | new-record-required | Missing from reviewed L-track evidence: Deterministic multilingual aliases with Unicode and transliteration matching | - |
| BOT-05 | register | new-record-required | Missing from reviewed L-track evidence: Localised replies per channel or per the viewer's command language | - |
| BOT-06 | register | new-record-required | Missing from reviewed L-track evidence: Blocked-term lists by language including transliterated variants — **one corpus shared with §12.2 TTS safety, never a second list** | - |
| BOT-07 | register | new-record-required | Missing from reviewed L-track evidence: Deterministic spam, flood, repeated-text, emoji and link controls | - |
| BOT-08 | register | new-record-required | Missing from reviewed L-track evidence: Import wizard for simple commands from creator-supplied exports; honest "cannot import" table | - |
| BOT-09 | register | new-record-required | Missing from reviewed L-track evidence: Never import scripts, raw JS, shell commands, arbitrary HTTP calls or third-party credentials | - |
| BOT-10 | register | new-record-required | Missing from reviewed L-track evidence: Automation recipes from a narrow allow-list of actions | - |
| BOT-11 | register | new-record-required | Missing from reviewed L-track evidence: One event action at first release: command → overlay or Companion action | - |
| BOT-12 | register | new-record-required | Missing from reviewed L-track evidence: Rate-limited and coalesced writes; degrade to silence with a visible notice, never a delayed backlog dump | - |
| BOT-13 | register | new-record-required | Missing from reviewed L-track evidence: AI layer on §11 credits: translate, summarise, suggest, classify — **recommend or soft-action only** | - |
| BOT-14 | register | new-record-required | Missing from reviewed L-track evidence: AI audit record: original text, action, reason, confidence, policy version, appeal and reversal path | - |
| BOT-15 | register | new-record-required | Missing from reviewed L-track evidence: Moderation correctness untiered (§30.1); a Free creator's chat is not less safe | - |
| BOT-16 | register | new-record-required | Missing from reviewed L-track evidence: Bot UI languages follow the §5.6.2 waves; no separate language set | - |
| BOT-17 | register | new-record-required | Missing from reviewed L-track evidence: Blocked on the Google chat-write scope (`CON-08`, §32) and on YouTube being post-v1 | - |
| STO-01 | register | new-record-required | Missing from reviewed L-track evidence: GCS + CDN with content-addressed keys and signed URLs | - |
| STO-02 | register | new-record-required | Missing from reviewed L-track evidence: Postgres holds metadata, moderation state and attestation only | - |
| STO-03 | register | new-record-required | Missing from reviewed L-track evidence: Normalisation pipeline (audio loudness, GIF→MP4/WebM, image pre-scale) | - |
| STO-04 | register | new-record-required | Missing from reviewed L-track evidence: Tenant-scoped dedup (`channel_id` + sha256); global dedup only for BharatStudio-owned or explicitly licensed assets (§19.1) | - |
| STO-05 | register | new-record-required | Missing from reviewed L-track evidence: Keep existing Lottie bytea working; new media to GCS; opportunistic backfill | - |
| PAY-02 | register | mapped-existing | L04 task/test/review trio fully covers §31.2 HMAC raw-body verification and provider event dedup; supporting webhook parser and event-identity regression topics are recorded | tasks/L04-go-payment-boundary.md, tests/TC-L04-go-payment-boundary.md, reviews/2026-08-14-L04-provider-boundary-review.md |
| PAY-03 | register | mapped-existing | L04 task/test/review trio fully covers §31.2 amount floor and server/database enforcement; supporting request validation and persistence-boundary topics are recorded | tasks/L04-go-payment-boundary.md, tests/TC-L04-go-payment-boundary.md, reviews/2026-08-14-L04-provider-boundary-review.md |
| PAY-04 | register | mapped-existing | L04 task/test/review trio fully covers §31.2 bounded intent expiry and checkout timeout; supporting migration 0006 expiry and provider request-bound topics are recorded | tasks/L04-go-payment-boundary.md, tests/TC-L04-go-payment-boundary.md, reviews/2026-08-14-L04-provider-boundary-review.md |
| PAY-05 | register | mapped-existing | L04 task/test/review trio fully covers §31.2 idempotency contract and repeat-safe order handling; supporting local intent uniqueness and API tests are recorded | tasks/L04-go-payment-boundary.md, tests/TC-L04-go-payment-boundary.md, reviews/2026-08-14-L04-provider-boundary-review.md |
| PAY-06 | register | mapped-existing | L04 task/test/review trio fully covers §31.2 alertConsent persistence and projection gate; supporting immutable intent and no-alert/outbox regression topics are recorded | tasks/L04-go-payment-boundary.md, tests/TC-L04-go-payment-boundary.md, reviews/2026-08-14-L04-provider-boundary-review.md |
| PAY-07 | register | mapped-existing | L04 task/test/review trio fully covers §31.2 payment reconciliation policy; supporting payment-level recovery, expiry and mismatch quarantine topics are recorded | tasks/L04-go-payment-boundary.md, tests/TC-L04-go-payment-boundary.md, reviews/2026-08-14-L04-provider-boundary-review.md |
| PAY-08 | register | mapped-existing | L04 task/test/review trio fully covers §31.2 refunds and disputes as append-only compensating evidence; supporting migrations 0013/0031 and monotonic status tests are recorded | tasks/L04-go-payment-boundary.md, tests/TC-L04-go-payment-boundary.md, reviews/2026-08-14-L04-provider-boundary-review.md |
| PAY-09 | register | mapped-existing | L04 task/test/review trio fully covers §31.2 reserved default binding and exact-provider-binding precedence; supporting binding resolution and account-context guard topics are recorded | tasks/L04-go-payment-boundary.md, tests/TC-L04-go-payment-boundary.md, reviews/2026-08-14-L04-provider-boundary-review.md |

**Reconciliation:** 66 mapped-existing + 717 new-record-required = 783; active-record eligibility is 0.
