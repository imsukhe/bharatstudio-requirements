# L10 — Release readiness and production rollout

**Status:** `Blocked pending L00–L09 evidence and external release gates`  
**Level:** L4  
**Owner:** Project owner  
**Depends on:** L00–L09  
**Blocks:** public release
**Master authority:** [`../active/launch/01_MASTER_RELEASE_AUTHORITY.md`](../active/launch/01_MASTER_RELEASE_AUTHORITY.md)
**Test record:** [`../tests/TC-L10-release-readiness-and-rollout.md`](../tests/TC-L10-release-readiness-and-rollout.md)
**Review record:** [`../reviews/2026-08-15-L07-L08-L10-release-surface-review.md`](../reviews/2026-08-15-L07-L08-L10-release-surface-review.md)
**Local regression record:** [`../reviews/2026-08-15-local-regression-and-surface-verification.md`](../reviews/2026-08-15-local-regression-and-surface-verification.md)

## Objective

Release the complete v1 product only when every product, payment, security, provider, legal, store, operational and rollback gate has evidence.

## Tasks

1. Reconcile all requirements, tasks, tests, decisions and review records. Mark every decision accurately: Proposed/Approved/Implemented/Verified/Superseded/Blocked.
2. Confirm Razorpay Technology Partner approval and production creator-direct connected-account test evidence.
3. Confirm production infrastructure region/configuration, database capacity, Cloud Run/Tasks/Scheduler values, IAM, domains, certificates, WAF, backups and secret rotation.
4. Complete iOS/Android store review requirements and Windows/macOS signing/notarisation/distribution paths.
5. Complete legal/CA/provider evidence, public policy publication and support/on-call staffing/contacts.
6. Execute a production-like rehearsal: deployment, schema migration, payment sandbox, queue dispatch, overlay, Companion pairing, failure/rollback and communications.
7. Obtain recorded review evidence for security, payments, privacy/legal, accessibility, mobile/desktop release, SRE and final product acceptance.
8. Establish limited launch cohort, capacity guardrails, incident commander, freeze window, go/no-go meeting, rollback triggers and public status communication.

## Go/no-go criteria

- All L00–L09 acceptance criteria have evidence; no unowned critical/high finding remains.
- v1 contains no Enterprise capability/claim. *(Amended 2026-09-07 — see below; was "v1 contains no YouTube or Enterprise capability/claim.")*
- Payment, queue, overlay and scheduler recovery are proven in final staging.
- Provider/legal/store gates are affirmative, current and documented.
- Deployment and rollback are rehearsed; monitoring/on-call/support are live.
- Google OAuth app verification is approved for the YouTube read scopes and the high-sensitivity chat-write scope. *(Added 2026-09-07.)*
- YouTube Data API quota is confirmed sufficient for projected concurrent live-chat polling. *(Added 2026-09-07.)*

### Amendment — YouTube go/no-go, 2026-09-07

The go/no-go line above read, verbatim: "v1 contains no YouTube or Enterprise
capability/claim." That is now false for YouTube. The connector, encrypted
OAuth token storage with PKCE, the normalisation layer, the Go poller, the
delivery path and the TipIntent short link all exist: migrations
`packages/db/migrations/0086_v1_l15_youtube_connectors.sql`,
`0091_v1_l15_youtube_delivery_and_idempotency.sql`,
`0094_v1_l15_youtube_delivery_and_failure_recording.sql`,
`0097_v1_l15_tipintent_short_link.sql`,
`0099_v1_l15_ingest_failure_admin_surface.sql`,
`0101_v1_l07_l15_tts_mute_enforcement_and_tipintent_wiring.sql` (in
`bharatstudio-alerts`), plus `services/youtube-poller-go` (Go poller,
build+vet clean per the master plan). The sentence is amended to: **"v1
contains no Enterprise capability/claim."** Enterprise stays excluded from v1;
nothing about that changes.

Two external go/no-go gates are added that did not exist before, because
shipped code is not the same thing as a shippable claim:

- **Google OAuth app verification** must be approved for the read scopes AND
  the high-sensitivity chat-write scope before any YouTube capability is a
  launch claim.
- **YouTube Data API quota** must be confirmed sufficient for projected
  concurrent live-chat polling before any YouTube capability is a launch
  claim.

Both are **UNFILED as of 2026-09-07** (confirmed with the owner). The YouTube
code's test status — however green — does not satisfy either gate; these are
external provider approvals, not implementation evidence, and this repository
does not draw provider/legal conclusions from code (`governance/AGENTS.md`).
The YouTube code cannot ship as a v1 launch claim without both approvals on
file, regardless of test status. See
`active/launch/05_SUPPORT_AND_EXTERNAL_EVIDENCE_REGISTER.md` for the tracked
external-evidence rows for these two items alongside the other unfiled
external gates.

## Rollback

Use pre-approved versioned deployments, feature flags, provider endpoint contingency, traffic caps, migration recovery procedure and public incident communications. Do not erase financial, alert or audit evidence during rollback.

## Current evidence snapshot — 2026-08-15

Local implementation/regression evidence is available for the TypeScript API/web
foundation, dedicated Web Companion Console, PostgreSQL migration harness, Go
payment boundary, Go alert-worker contracts, scheduler-only template and
authenticated local metrics/readiness. The mobile lockfile has compatible
dependency overrides, but its remaining React Native/Metro/image-size audit
findings are still a release security gate.
It does not satisfy final release gates.

### Local container/manifest correction — 2026-09-09

The API Cloud Run image reference had no checked-in API Dockerfile, and the
manifest did not bind all values required by API production configuration.
`bharatstudio-alerts` now supplies the root-built, non-root API image and the
manifest verifier requires its compiled entrypoint plus the missing bindings.
All three declared service images build locally and the API image returns its
health response with the manifest's `HOST=0.0.0.0` binding. Reproducible
commands and the non-claiming boundary are recorded in
[`TC-L10-release-readiness-and-rollout.md`](../tests/TC-L10-release-readiness-and-rollout.md).

This closes a local implementation defect; it does not advance L10-03 or the
release status. Cloud Run deployment, IAM, actual secret versions, direct
database readiness, migration/rollback rehearsal, capacity and failure proof
remain external/staging gates.

The latest local continuation also covers the native APNs/FCM adapter and
server notification preference/device contract, macOS loopback OBS v5 client,
Windows OBS source boundary/static project validation, and local provider image
builds. These additions do not close physical-device, Windows SDK, pairing,
OBS runtime, provider, IAM, store or legal gates.

The local reconciliation pass also verified the current 35-path OpenAPI
contract count and corrected the Cloud Tasks worker OIDC audience wiring so the
configured verifier audience is explicit and independent of the target URL.
These are implementation/evidence corrections, not deployment or approval
evidence.

The release remains blocked on:

- L00 owner freeze/authority reconciliation and L01/L02 independent review;
- Razorpay Technology Partner/connected-account approval and creator-direct
  provider sandbox/live evidence;
- deployed Neon plan/region, Cloud Run/Cloud Tasks/Scheduler topology, direct
  listener configuration, IAM, domains, secrets, backups and measured capacity;
- cross-replica overlay replay, queue burst, notification outage, crash,
  dead-letter and rollback rehearsal;
- Companion web/mobile/native implementation, signing, store review and
  desktop distribution evidence;
- dated legal/CA/provider/privacy/support review and published policy/copy
  evidence;
- independent security, payment, accessibility, SRE and product review.

No local test, legacy load result, document assertion or disabled schedule may
be used to claim public launch readiness.

## Fresh local reconciliation — 2026-08-15

The L10 task/test pair, master release authority, L00–L09 records, support and
external-evidence register, infrastructure template and current repository
readiness claims were rechecked together.

Confirmed:

- the release decision remains one complete public v1 launch of Alerts plus
  bundled Companion;
- YouTube and Enterprise remain explicitly Phase 2 and are not launch claims;
- the 359 missing BSA runtime packages remain a tracked L03/PENDING-04 launch
  requirement, with visual generation intentionally deferred rather than
  silently removed;
- no local implementation, disabled schedule, legacy load result or document
  assertion promotes L10 to launch-ready;
- L07, L08 and L09 local slices now have dated audit evidence, while their
  native/store/legal/provider/deployment/capacity/staging gates remain open;
- the master authority remains `Proposed — release blocked; implementation and
  evidence work may continue`.

No additional locally verifiable L10 authority inconsistency was found. L10
remains blocked until every applicable acceptance row has dated evidence,
owners/approvers and rollback/recovery proof, including Razorpay/provider,
Neon/Cloud Run/Cloud Tasks, native releases, legal/privacy/support, staging
capacity/failure rehearsal, observability and independent review.

### Fresh local package and smoke rerun — 2026-09-09

The Alerts API/web test/build matrix, static deployment negatives, contracts
and all three service images were rerun. The API liveness image smoke returned
the expected bounded health envelope; API runs as `node` and both Go images as
`nonroot:nonroot`. Exact commands and the non-claiming result are recorded in
`TC-L10-release-readiness-and-rollout.md`. This does not change the L10 status
or satisfy any deployed/provider/staging/release gate.

### Automatic continuation reconciliation — 2026-08-15

The next local release-control pass found no stale active readiness claim. The
following supporting checks passed: alert-worker Go unit/race/vet, cron contract
2/2, infrastructure contract 8/8, mobile Jest 23/23 plus lint/typecheck and
dependency-hardening 2/2, macOS Swift 7/7, marketing 5/5, and the disposable
L02–L05 PostgreSQL/overlay integration chain. No BSA visual package was
generated or modified.

This does not advance L10. The release remains blocked on provider approval and
sandbox/live evidence, deployed infrastructure/IAM/region/capacity, staging
failure and rollback rehearsal, native/store release evidence, legal/privacy/
support approval, observability deployment and independent review.
