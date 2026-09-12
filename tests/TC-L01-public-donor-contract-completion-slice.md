# TC-L01 — Public donor contract completion slice

**Status:** `Pass — local contract and focused API evidence; external gates remain open`  
**Task:** [`../tasks/L01-public-donor-contract-completion-slice.md`](../tasks/L01-public-donor-contract-completion-slice.md)

| ID | Setup/action | Expected result |
|---|---|---|
| L01-PD-01 | Validate the four new OpenAPI operations | Every path parameter, request body, header and non-204 success response is typed and referenced locally |
| L01-PD-02 | Validate ready, used/expired and unknown TipIntent fixtures | Only ready contains amount/name/message; used/expired are identity-only and unknown is the standard bounded error |
| L01-PD-03 | Validate receipt mint/resolve fixtures | Mint response exposes only opaque token; resolve returns only the reviewed receipt projection |
| L01-PD-04 | Validate a TipIntent order confirmation request | It admits only the idempotency header and optional Turnstile token, and the response has no provider credential/instrument fields |
| L01-PD-05 | Re-run focused runtime route tests | Existing no-auth, opacity, single-use, state and client-controlled-amount negatives remain passing |
| L01-PD-06 | Re-run route inventory | All four operations move from outside the published surface to covered; no stale documented operation is introduced |

No fixture or test data may contain provider credentials, real personal data, or
a token usable against a deployed environment.

## Evidence — 2026-09-09

L01-PD-01 through L01-PD-06 passed locally. `pnpm contracts:validate` reports
16 fixtures, 39 paths, 46 operations and three structural negative cases; the
added fixtures also prove closed TipIntent states reject amount disclosure and
confirmation rejects a client-supplied amount. `cd apps/api && npx tsc --noEmit
&& npx tsx --test test/l14-viewer-profile-routes.test.ts
test/l15-tipintent-public-routes.test.ts` passed 15/15. The runtime inventory
is 159/46/113/0 (literal/covered/pending/stale). Provider sandbox, Turnstile,
Google OAuth, deployed operations and independent review remain out of scope
for this local evidence.
