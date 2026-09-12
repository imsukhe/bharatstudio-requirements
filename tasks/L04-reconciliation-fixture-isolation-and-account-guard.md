# L04 — Reconciliation fixture isolation and account-context guard

**Status:** `Implemented locally — executable evidence recorded`
**Level:** L3
**Authority:** L04 payment/reconciliation boundary

## Scope

Repair a locally reproducible disposable-database failure and harden automated
refund reconciliation so it never selects a payment without a provider-account
context accepted by the provider client.

The change is restricted to SQL test fixture isolation and the private
candidate-selection function. It does not modify payment state, create a
provider request, or treat skipped historical records as reconciled.

## Data, security, and rollback

- Migration `0111_v1_l04_refund_reconciliation_account_guard.sql` replaces only
  `app_private.list_refund_reconciliation_candidates(integer)`.
- Candidates must carry a `test`/`live` environment and a linked-account value
  matching the client’s conservative `[A-Za-z0-9._:-]{1,64}` grammar.
- Null or malformed historical account attribution remains durable evidence but
  is excluded from automatic provider fetching. Manual review/data repair is
  required before it can be retried.
- Rollback is a controlled redefinition of that private function to the prior
  behavior; it is not an automatic production rollback because loosening the
  guard would reintroduce accountless provider work.

## Reproducible defect and remedy

The combined disposable SQL suite failed with the unique constraint on
`payment_accounts(channel_id, provider, environment)`: the L04 quarantine
fixture used its own account ID but reused the main application fixture’s
channel/environment slot. After moving it to its own synthetic channel, the
full service integration then exposed a second error: an intentionally plain
payment lacked `connected_account_ref`, and the Go adapter could not scan the
result into its required account field.

The fixture now models a properly attributed captured payment, separately proves
that null attribution is ineligible, and proves that a malformed account value
is also ineligible. The selection function enforces the same grammar used by
the provider client, before headers or network calls are possible.

## Local evidence — 2026-09-09

`pnpm db:test:l03` passed the full migration chain through `0111`, all 18
role-separated SQL proofs, payment and worker SQL integrations, two-listener
overlay wake-up, cross-replica replay, and channel/config concurrency checks.
`go test -race ./... && go vet ./...` passed in `services/payment-webhook-go`.
Whitespace validation (`git diff --check`) also passed.

Provider sandbox, production historic-data remediation, deployment migration,
and staging reconciliation behavior remain external gates.
