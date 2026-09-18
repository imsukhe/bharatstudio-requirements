# Review — AUD-PAY-01 public checkout Turnstile hand-off

**Status:** `Conditionally complete — self-review passed; independent review unavailable`  
**Reviewer:** Sukhdev Singh (self-review until an independent reviewer is available)  
**Scope:** `AUD-PAY-01-turnstile-checkout-handoff.md`

## Review checklist

- Confirm both public order paths carry only the opaque challenge response and preserve
  immutable tip-intent body constraints.
- Confirm direct-tip OpenAPI now matches the existing Fastify request schema and its
  bot-verification `403`, rather than documenting a client payload the runtime rejects.
- Confirm the public site key is the only browser configuration added; no verification
  secret, provider credential, payment state, or donor data crosses into new storage.
- Confirm script origin is the approved Cloudflare challenge endpoint; failures and
  expiry fail closed without a checkout request; request completion resets the response.
- Confirm no payment order, webhook handling, ledger, migration, or provider checkout
  contract changes.
- Re-run the recorded deterministic tests against the actual final worktree, then inspect
  the changed paths and diff for token leaks, regression in no-key development, and
  inaccessible submit/error states.

## Required disposition fields after review

Record reviewer, commands/results, changed paths, findings/severity/disposition,
rollback proof, commit/version, external Cloudflare site-key/staging gate, and whether
the review was independent. Do not upgrade the task beyond `Conditionally complete`
without those facts.

## Fresh hostile self-review — 2026-09-18

**Reviewer:** Sukhdev Singh (self-review; no independent reviewer was available).  
**Reviewed worktrees:** Alerts base `d5cebc6`; requirements base `4294a00`.

| Finding | Severity | Disposition and evidence |
|---|---|---|
| Both public payment paths made no route request from the existing client, so production guard policy rejected every checkout. | P1 | Fixed by the shared explicit-rendering adapter, callback-only in-memory token state, and both form call sites. Focused tests prove neither form posts before a response and that a returned token reaches only the existing order body. |
| Initial repair left `CreateTipOrderRequest` and the direct route's declared responses behind the Fastify runtime. | P1 contract drift | Fixed before closure: OpenAPI now includes optional bounded `turnstileToken` and `403`; `contracts/test-openapi-validator.mjs` parses and asserts both properties. `pnpm contracts:validate` passed after the correction. |
| Existing CSP would block the necessary Cloudflare script and iframe. | P1 deployment-static defect | Fixed before closure: `_headers` allows only `https://challenges.cloudflare.com` in `script-src` and `frame-src`; static header test asserts both. This matches Cloudflare's official CSP guidance. |
| A response token could be reused after an ambiguous request result. | P1 abuse/retry seam | Fixed before closure: each request `finally` clears local state and increments the adapter reset nonce. Both form tests assert the corresponding widget reset after their order attempt. |
| Site key absent from a production build. | P1 configuration failure | Browser refuses the order request and shows an accessible generic unavailable state; focused form test proves no order request. Deployment remains gated on setting the real public site key paired to the API secret. |

**Negative checks:** `git diff --check` passed; a source scan found no API-only secret
identifier in web runtime/configuration and no `turnstileToken` persistence to local or
session storage. No migration exists in the diff. No change reaches provider order
creation until the existing server verifier accepts the response.

**Rollback/recovery:** reverting the exact paths listed in the task restores the
pre-correction code with no durable repair. Outside production, the pre-existing
server configuration switch remains the only verification kill switch; no client bypass
was introduced. The missing-site-key client branch is tested as the safe configuration
failure mode.

**External/release gate:** a safe environment must use a real Cloudflare site key paired
to the API verifier secret and exercise both checkout pages in a real browser. Cloudflare
documents explicit rendering, one-time response handling, and the required CSP script/
frame origins at https://developers.cloudflare.com/turnstile/get-started/client-side-rendering/
and https://developers.cloudflare.com/turnstile/reference/content-security-policy/ . That
provider/browser evidence has not been claimed or performed here.
