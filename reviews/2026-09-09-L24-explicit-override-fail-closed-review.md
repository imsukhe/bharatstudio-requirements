# L24 explicit Companion override fail-closed review

**Decision state:** `Implemented and locally verified; independent review and deployment evidence remain open`
**Level:** L3
**Date:** 2026-09-09
**Reviewer:** Self-review; no independent reviewer was available.
**Scope:** API authorization precedence for
`channel_entitlement_versions.values.companionActionGroups` in direct
Companion action requests.

## Finding

**P1 — fixed.** `readExplicitGroupOverride` returned `null` for an empty
array, an array containing an invalid group, or a non-array value. The caller
interpreted `null` as “no explicit override” and consulted the live policy.
Consequently, a persisted explicit deny-all or malformed override could be
replaced at runtime by a permissive policy, contrary to migration 0100's
documented explicit-override precedence.

## Disposition

`bharatstudio-alerts/apps/api/src/routes/companion.ts` now distinguishes an
absent key from a present key. An absent key uses the live policy; a present
empty or malformed value resolves to an empty action-group set and returns
the existing `403 companion_action_group_not_entitled` response. No database
or financial data was changed.

`bharatstudio-alerts/apps/api/test/companion-entitlement-grant-policy.test.ts`
adds direct HTTP cases for both an empty and malformed override under a
permissive live policy. They verify the request is denied before activation or
command execution.

## Reproducible redacted evidence

- `cd bharatstudio-alerts/apps/api && npx tsc --noEmit && npx tsx --test
  test/companion-entitlement-grant-policy.test.ts` — **6/6** pass.
- `cd bharatstudio-alerts && sh packages/db/tests/run-sql-suite.sh` — **44/44**
  isolated SQL proofs after **110** migrations.
- `git diff --check` passed in Alerts and central requirements.

## Risk, rollback, and gates

The change is fail-closed and API-only. Reverting it would restore a
policy-precedence authorization defect, so normal rollback is not appropriate;
an operational issue should instead be resolved by correcting the persisted
override or live policy. Independent review, staging deployment, real
Companion/native-helper evidence, and Windows compilation remain open. This
review makes no production-readiness claim.

## Follow-up finding — full-test gate (P1 fixed)

The same hostile route review found that `/companion/full-test` called the
store's `send_test_alert` action directly. The store persists a command but is
not the API's entitlement/activation gate, so that endpoint could create a
synthetic alert while the alerts group was unentitled or the overlay inactive.

The route now resolves the same alerts-group entitlement and overlay-active
state before it creates the command. `l07-companion-feature-store.test.ts`
uses a store fake that would otherwise accept the command, proving an inactive
overlay returns `409 companion_action_not_active` before the store runs.
Focused API evidence is **18/18** and the full API suite is **399/399** plus
TypeScript build. This remains local self-review evidence only.

## Follow-up regression — full-test entitlement (P1 verified)

The route-level proof now also covers an explicitly unentitled alerts group.
The test injects a policy whose only result is `granted: false` and an empty
action-group set; its store fake would otherwise create the synthetic alert.
`POST /v1/channels/:channelId/companion/full-test` returns
`403 companion_action_group_not_entitled`, proving the endpoint stops before
the command write. The existing inactive-overlay proof continues to return
`409 companion_action_not_active` before that write.

- `cd bharatstudio-alerts/apps/api && npx tsc --noEmit && npx tsx --test
  test/l07-companion-feature-store.test.ts` — **13/13** pass.
- `cd bharatstudio-alerts/apps/api && npm test && npm run build` — **400/400**
  API tests pass and the production TypeScript build passes.

This supersedes the earlier 18/18 and 399/399 local counts for this review.
