# Decision — L04 reconciliation account-context guard

**Decision:** Accept the local remediation and retain historic records with
missing or malformed account attribution outside automatic reconciliation.

## Finding

The combined SQL/service rehearsal exposed two linked defects: a supposed
isolated fixture competed for the production-model unique payment-account slot,
and a historical payment without account attribution could be selected by the
refund reconciliation function. The latter caused a database scan failure and
would otherwise be incapable of forming a correctly scoped provider request.

## Disposition

Migration `0111` admits only candidates with a valid immutable account context
and expected environment. This is fail-closed: records with incomplete legacy
metadata are neither silently reconciled nor mutated. The fixture owns a unique
synthetic channel and includes both null and malformed-account negatives.

## Evidence reviewed

- Full `pnpm db:test:l03` pass: 18 SQL proofs, real payment/worker adapter
  integrations, two-listener/cross-replica overlay checks, and SQL concurrency
  checks.
- Payment service `go test -race ./... && go vet ./...` pass.
- `git diff --check` pass for the migration and fixture changes.

## Remaining gates

Production legacy-data policy, a deployment migration rehearsal, provider
sandbox calls and staging reconciliation need their own evidence. This local
decision makes no production-readiness claim.
