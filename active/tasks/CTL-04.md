# CTL-04 — capability control-plane admin UI

**Status:** `Approved for local implementation — depends on CTL-13 passkey gate`

| Field | Value |
|---|---|
| **Scope phase** | `v1`; Phase 0 capability-control-plane foundation. A standalone platform-admin surface for Layer 2 capability registry reads, governed changes, emergency kill, and audit/event history. No Layer 1 correctness entitlement, price, billing, or retention control is exposed. |
| **Owner** | Sukhdev Singh |
| **Tier and gate** | Internal platform-admin only; never creator, moderator, public, or marketing access. Section 20.6 MFA and `00_LAUNCH_SCOPE_AUTHORITY.md` per-task-approval gates are mandatory. |
| **Personal-data class** | No new persisted personal data. UI displays aggregate capability state and existing append-only admin audit metadata; it must not display payment, viewer, supporter, token, email, or unredacted incident-reason data beyond the acting administrator's authorised operational view. |
| **Provider or legal dependency** | CTL-13 uses application-managed passkeys. RP ID/origin allowlist, elevated-session lifetime and recovery policy remain configured-unset deployment/release gates; no provider contact or external evidence is authorised. |
| **Failure behaviour** | Fail closed: API/session/MFA/preview failures render an unavailable state and disable mutation controls. No optimistic capability state, client-side tier decision, or caller-supplied impact count is accepted. |
| **Kill switch** | Existing server-side `global_kill` rules in migration 0155 remain the only kill authority. This page may invoke it only after server-derived preview and explicit reason/confirmation; removing the page changes no server enforcement. |
| **Acceptance test** | `tests/TC-CTL-04-capability-admin-ui.md` |
| **Evidence location** | Proposed paths are recorded in the acceptance and review records. Concrete commands, revisions and redacted output are recorded only after implementation. |
| **Rollback** | Revert newly added admin page/client/tests and API wiring together. Roll back database additions only through a new forward migration; do not edit historical migrations. Existing registry/change-management/kill APIs remain intact. |

## Complete vertical slice

Affected repositories are `bharatstudio-admin` (route, UI, BFF adapter, responsive/accessibility tests) and `bharatstudio-alerts` (authoritative API contract and runtime guard only where necessary). The page must cover master switch, tier change, limits edit, emergency kill, change reason, proposal/approval status, revert, audit/event display, and CTL-05 preview state. It must use existing two-person change-management and emergency-kill APIs; no policy is duplicated in React.

Before implementation, read the relevant local Next.js App Router, route-handler, server/client component and authentication documentation required by `bharatstudio-admin/AGENTS.md`, then inspect the actual API schemas and admin runtime. Tests must include an authenticated browser journey, keyboard/error states, unauthorized/expired/MFA-missing failure, stale preview rejection, API unavailability, and no Layer-1 mutation reachability.

## Dependency and approval boundary

CTL-13 is a hard predecessor because §20.6 requires MFA. This record does not authorize a single-factor production mutation UI. The precise decision question and alternatives are in the linked review record; after the owner answers and approves the defined scope, implementation may start.
