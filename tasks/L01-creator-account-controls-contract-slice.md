# L01 — Creator account-controls contract slice

**Status:** `Approved for local implementation; evidence pending`  
**Level:** L3  
**Parent authority:** `L01-contracts-and-database-baseline.md`; `L02-security-rls-and-archive-proof.md`; `L08-marketing-support-legal.md`  
**Test record:** [`../tests/TC-L01-creator-account-controls-contract-slice.md`](../tests/TC-L01-creator-account-controls-contract-slice.md)  
**Review:** [`../reviews/2026-09-09-L01-creator-account-controls-contract-slice-decision.md`](../reviews/2026-09-09-L01-creator-account-controls-contract-slice-decision.md)

## Scope

Publish and harden the existing creator-bearer account-control operations:

- `GET /v1/me/terms`, `POST /v1/me/terms/accept`;
- `GET /v1/me/export`, `POST /v1/me/export/email`;
- `GET`/`POST /v1/me/privacy/requests`; and
- `POST /v1/me/close`.

All success projections must be versioned, exact and bounded. API routes must
not spread persistence objects. The browser must validate the account export
and every account-control response before using it. Export is intentionally
private to the authenticated creator and may include that creator's own IDs,
channels, session metadata and privacy-request metadata; it must never include
session token/hash, email, provider credential, payment instrument, other-user
data, arbitrary store fields, or unbounded collections.

## Boundaries, migration, rollout, rollback

This is runtime projection and contract hardening; it does not add a migration,
change source-of-truth data, alter deletion/retention, or contact a provider.
The L02 256 privacy-history cap is a required precondition. Rollback is a
controlled source/contract revision; it must not silently restore raw store
serialization. Deployment requires the normal API/web rollout and future
staging/browser/IAM/privacy review; those remain external evidence gates.

## Acceptance

- All seven operations declare creator bearer auth, exact request bounds and
  bounded success/error statuses in OpenAPI.
- Fixtures and generated hostile variants reject credential/payment/provider/
  foreign-account/unknown fields and excess collection lengths.
- API tests prove account scope and narrow output even if a store returns
  extra data; browser parser tests prove fail-closed response integrity.
- Contract, focused, SQL, build and root verification evidence is recorded
  accurately, including any external image-registry blocker.
