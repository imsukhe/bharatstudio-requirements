# CTL-04 — capability control-plane admin UI

**Status:** `Conditionally complete locally for registry/change-management UI — CTL04.4 remains blocked on CTL-05`

| Field | Value |
|---|---|
| **Scope phase** | `v1`; Phase 0 capability-control-plane foundation. A standalone platform-admin surface for Layer 2 capability registry reads, governed changes, emergency kill, and audit/event history. No Layer 1 correctness entitlement, price, billing, or retention control is exposed. |
| **Owner** | Sukhdev Singh |
| **Tier and gate** | Internal platform-admin only; never creator, moderator, public, or marketing access. Section 20.6 MFA and `00_LAUNCH_SCOPE_AUTHORITY.md` per-task-approval gates are mandatory. |
| **Personal-data class** | No new persisted personal data. UI displays aggregate capability state and existing append-only admin audit metadata; it must not display payment, viewer, supporter, token, email, or unredacted incident-reason data beyond the acting administrator's authorised operational view. |
| **Provider or legal dependency** | CTL-13 application-managed passkeys, approved five-minute ceremony, fifteen-minute elevation and two-person recovery are implemented locally. Production RP ID/origin allowlist and real device/deployment/security evidence remain release gates; no provider contact or external evidence is authorised. |
| **Failure behaviour** | Fail closed: API/session/MFA/preview failures render an unavailable state and disable mutation controls. No optimistic capability state, client-side tier decision, or caller-supplied impact count is accepted. |
| **Kill switch** | Existing server-side `global_kill` rules in migration 0155 remain the only kill authority. This page may invoke it only after server-derived preview and explicit reason/confirmation; removing the page changes no server enforcement. |
| **Acceptance test** | `tests/TC-CTL-04-capability-admin-ui.md` |
| **Evidence location** | Proposed paths are recorded in the acceptance and review records. Concrete commands, revisions and redacted output are recorded only after implementation. |
| **Rollback** | Revert newly added admin page/client/tests and API wiring together. Roll back database additions only through a new forward migration; do not edit historical migrations. Existing registry/change-management/kill APIs remain intact. |

## Complete vertical slice

Affected repositories are `bharatstudio-admin` (route, UI, BFF adapter, responsive/accessibility tests) and `bharatstudio-alerts` (authoritative API contract and runtime guard only where necessary). The page must cover master switch, tier change, limits edit, emergency kill, change reason, proposal/approval status, revert, audit/event display, and CTL-05 preview state. It must use existing two-person change-management and emergency-kill APIs; no policy is duplicated in React.

Before implementation, read the relevant local Next.js App Router, route-handler, server/client component and authentication documentation required by `bharatstudio-admin/AGENTS.md`, then inspect the actual API schemas and admin runtime. Tests must include an authenticated browser journey, keyboard/error states, unauthorized/expired/MFA-missing failure, stale preview rejection, API unavailability, and no Layer-1 mutation reachability.

## Dependency and approval boundary

CTL-13 is a hard predecessor because §20.6 requires MFA; its local implementation is now
conditionally complete. This record does not authorize a single-factor production mutation UI.
CTL-05 remains blocked on a durable YouTube-liveness projection, so the UI may only display an
honest unavailable preview state and must not fabricate or submit impact counts until that task is
complete.

## 2026-09-18 implementation design — approved local CTL-04 portion

The console is a same-origin, narrowly scoped BFF. It may read only the registry entries,
governed change list and immutable emergency-kill event list, and may write only a governed
change proposal, staff/owner approval, rejection or revert. It must not proxy arbitrary
`/v1/admin/*` paths, expose an API bearer to the browser, use the single-admin registry PUT
endpoint for an existing capability, or expose Layer-1 plans, prices, billing, retention,
payments, channel IDs or viewer/supporter data.

The edit form is an existing-capability form only. It sends master switch, tier, rollout,
capacity class, limits and the remaining registry fields through
`POST /v1/admin/capability-registry/changes`; the Alerts API remains the sole maker-checker,
validation and policy authority. Approval, rejection and revert use their exact existing
endpoints. The browser receives a minimal operational projection (no actor UUIDs or bearer
material), with server-confirmed results before it reports success.

Until CTL-05 is implemented, the emergency card displays the accurate state **"impact preview
unavailable — emergency firing disabled"**, submits no request and exposes no client-supplied
counts. This is deliberately a safe partial control-plane surface, not completion of CTL04.4:
only a CTL-05 server-derived preview plus a replacement fire route can make emergency firing
reachable. Upstream 401/403/428/503 failures must remain an unavailable/error state with no
optimistic mutation. No new data model or migration is introduced by this CTL-04 portion; its
rollback is a single forward application rollback of the admin BFF, page and tests.

## Local implementation evidence — 2026-09-18

Implemented in `bharatstudio-admin` on `master` (working tree pending the next audited commit):
`app/admin/capabilities/`, the narrow `app/api/admin/capabilities/**` BFF routes, server-side
schema/projection helpers and responsive browser tests. The BFF deliberately exposes only
registry/change/kill-history reads and proposal, approval, rejection and revert writes. It strips
actor IDs from its browser projection, requires the console mutation marker for every write, checks
that a proposed key already exists, and never includes an emergency-fire route or either client
impact-count field. The console uses the existing server-side passkey-MFA gate; its local bootstrap
bypass remains development-only.

Reproducible redacted evidence, all passing:

- `pnpm typecheck` — 0 TypeScript errors.
- `pnpm test` — 3 files / 8 unit tests passed.
- `pnpm test:e2e` — 8 desktop/mobile browser tests passed, including unauthenticated denial,
  keyboard proposal entry, mobile action reachability, no optimistic success, a direct missing-CSRF
  marker denial, and proof that no count reaches the proposal route.
- `pnpm build` — production build emitted `/admin/capabilities` plus only the five narrow
  `/api/admin/capabilities` BFF paths.
- In Alerts: `pnpm contracts:validate` — 78 fixtures, 158 paths / 185 operations and 3 negative
  operation cases passed; `pnpm --dir apps/api exec tsx --test test/capability-change-management-routes.test.ts test/capability-kill-events-routes.test.ts test/capability-registry-admin-routes.test.ts` — 26 focused API tests passed.
- `git diff --check` passed in both repositories.

Fresh self-review found and fixed: an upstream-unavailable local-MFA harness regression; mobile
responsive action hit-testing; a stale bootstrap message that claimed MFA was not enforced; a BFF
scope bypass that could have proposed a new capability; and missing anti-CSRF request marking on
new mutation routes. This is local/self-review evidence only. CTL04.4 is still unfulfilled because
the current Alerts emergency route accepts caller-supplied counts; CTL-05 must replace it with a
server-derived, atomic preview/fire path before the emergency control can be enabled.
