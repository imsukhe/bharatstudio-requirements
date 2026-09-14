# TC-L04/L14 — Anonymous payment identity attribution

**Status:** `Locally verified — external/independent evidence pending`
**Task:** [`../tasks/L04-L14-anonymous-payment-identity-attribution.md`](../tasks/L04-L14-anonymous-payment-identity-attribution.md)

| ID | Action | Expected result |
| --- | --- | --- |
| L04L14-01 | Create checkout without an identity cookie | Opaque identity is minted after order acceptance; raw token is not persisted/logged. |
| L04L14-01a | Confirm an opaque TipIntent without an identity cookie | It uses the same opaque cookie/fingerprint boundary without permitting TipIntent body tampering. |
| L04L14-01b | Send TipForm/TipIntent browser requests across same-site web/API origins | Credentialed fetch preserves the secure first-party cookie; an explicit credential-free read remains possible. |
| L04L14-02 | Repeat checkout with a valid cookie / expired cookie | Valid identity reuses; expired token creates a new identity. |
| L04L14-03 | Verify captured payment twice | One payment/event/relation has the resolved identity; duplicate creates no second effect. |
| L04L14-04 | Verify a legacy/no-identity checkout | Payment/alert remains valid with null identity. |
| L04L14-05 | Attempt identity UUID/body/header injection | It is ignored/rejected; only server cookie fingerprint is authoritative. |
| L04L14-06 | Run SQL/API/Go/full verification | Migration and every local component remain green. |

## Local result — 2026-09-14

| ID | Result and reproducible evidence |
| --- | --- |
| L04L14-01 | **Pass.** `apps/api/test/app.test.ts` proves a fresh successful tip checkout emits a `__Host-bsa-anonymous` HTTP-only, Secure, SameSite=Lax cookie only after order success; no raw token is sent to the payment service. |
| L04L14-01a | **Pass.** `apps/api/test/l15-tipintent-public-routes.test.ts` proves the server-authoritative TipIntent confirmation path mints the identical cookie/fingerprint boundary and reuses it across a distinct single-use link. |
| L04L14-01b | **Pass.** `apps/web/app/tips/tip-client.test.ts` proves all shared checkout/status requests default to `credentials: 'include'`, and a caller can explicitly use `omit`. Real browser same-site cookie and CORS deployment remain staging gates. |
| L04L14-02 | **Pass.** The direct and TipIntent API proofs replay the issued cookie and observe the same SHA-256 fingerprint without a replacement cookie. The SQL proof expires a synthetic fingerprint, confirms a distinct replacement identity and exactly one new active fingerprint, and confirms the old identity remains only as durable linkage. Browser cookie expiry remains a device/browser gate. |
| L04L14-03 | **Pass.** `packages/db/tests/l04_l14_anonymous_payment_identity.sql` verifies duplicate capture produces one identity, payment, alert and relation. It also proves authorization→capture→full-refund order: capture gains the identity, and the net relation is recomputed to 5,000 paise / one non-refunded tip. |
| L04L14-04 | **Pass by compatibility boundary.** The pre-existing nullable `viewer_identity_id` paths and unchanged original procedures remain callable; the wrapper writes only when a valid opaque fingerprint resolves. |
| L04L14-05 | **Pass.** The public order schema rejects client identity fields, and the API proof confirms only cookie-derived server hash is forwarded. |
| L04L14-06 | **Pass.** `pnpm verify:local` exited 0: 125 migration application, 52/52 isolated SQL proofs, contracts/deployment checks, race/load/fault/integration tests, API/web checks (501 direct API tests), Go race/vet checks and three image builds. |
