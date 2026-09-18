# AUD-PAY-01 — public checkout Turnstile hand-off

**Status:** `Conditionally complete — locally verified; independent review and external browser evidence pending`  
**Owner:** **Sukhdev Singh**  
**Authority:** `../launch/08_AUDIT_REMEDIATION_AUTHORITY.md` (AUD-PAY-01); `../launch/06_BACKEND_GAP_REMEDIATION_AUTHORITY.md`  
**Acceptance record:** `../../tests/TC-AUD-PAY-01-turnstile-checkout-handoff.md`  
**Review record:** `../../reviews/2026-09-18-aud-pay-01-turnstile-checkout-handoff.md`

## Scope

Repair the two client journeys that already call the server-enforced public payment
Turnstile boundary:

1. `apps/web/app/tips/[handle]/TipForm.tsx` — ordinary creator tip order.
2. `apps/web/app/t/[token]/TipIntentConfirm.tsx` — immutable tip-intent order.

Add one shared client-only Turnstile adapter under `apps/web/app/tips/`, update the
web CSP and public build-variable example, correct the already-accepted
`turnstileToken` and `403` outcome in OpenAPI, and add focused component/unit tests.
The runtime API schema already accepts the field; this task brings the published
contract into parity. It does not alter a route's payment semantics, payment-provider
payload, database table, migration, stored payment record, provider secret, or Razorpay
Checkout invocation.

## Security, privacy, and failure behaviour

- `NEXT_PUBLIC_TURNSTILE_SITE_KEY` is browser-visible by Cloudflare design; it is not
  a secret. `PUBLIC_PAYMENT_TURNSTILE_SECRET` remains API-only and is never referenced
  by web code.
- A Turnstile response is held in React memory only, is not logged, placed in storage,
  URL state, telemetry, or receipt data, and is sent solely in the existing JSON body.
- When a site key is configured, the submit button must not create an order until the
  challenge callback yields a non-empty response. Expiry/error clears that response.
- A completed order attempt resets the browser challenge before a later attempt; this
  prevents relying on a single-use response token.
- A production build with no site key fails closed in the UI with an actionable generic
  checkout-unavailable state rather than making an order request guaranteed to be
  rejected by the API. Development/test without a key keeps the existing no-challenge
  local path because the API itself does not require verification there by default.
- Cloudflare receives the browser interaction required for its challenge. That existing
  provider boundary needs real deployment/privacy review; no legal or provider claim is
  made by local tests.

## API contract and service boundary

The direct-tip `CreateTipOrderRequest` OpenAPI schema and its declared `403` response
are corrected to match the existing Fastify schema and runtime. Both public order
request schemas carry only an optional bounded `turnstileToken`; server policy decides
whether it is mandatory. The client never decides that a token is valid and never sends
an order/provider ID itself.

## Deployment, kill switch, rollback

- Deployment prerequisite: set a real `NEXT_PUBLIC_TURNSTILE_SITE_KEY` at the web
  build/deploy boundary paired with the API's already-required secret in every
  environment where `PUBLIC_PAYMENT_TURNSTILE_REQUIRED=true` or `NODE_ENV=production`.
- Existing server-side kill switch remains `PUBLIC_PAYMENT_TURNSTILE_REQUIRED=false`
  outside production only. This task introduces no bypass.
- Rollback: revert the shared web adapter, both form call sites, focused tests, and the
  public `.env.example` line together. No data repair and no migration is needed.

## Required verification

- Component tests: ordinary and tip-intent flows serialize the challenge response;
  challenge expiry/error blocks the payment-order request; production missing-key state
  fails closed; no token is stored in browser storage.
- API regression: existing guard pass/fail cases remain green.
- Full web typecheck, web suite, production build; API suite and contract validation.
- Fresh hostile review checks token minimisation, script origin, single-use/reset path,
  order reachability, disabled/error accessibility, and that no secret entered web code.

## External evidence gate

Only a real Cloudflare challenge in a safe non-production deployment can prove the
site-key/secret pair and challenge browser behaviour. That is a required release gate,
not an implementation blocker.

## Implementation and traceability reconciliation — 2026-09-18

**Changed runtime/contract paths:**

- `apps/web/app/tips/turnstile-challenge.tsx` and its component test;
- both existing public checkout components and their focused tests;
- `apps/web/.env.example`, `apps/web/public/_headers`, and the header regression;
- `contracts/openapi/v1.yaml` plus its parser-based contract regression.

No migration, table, stored payment field, Razorpay payload, API verification secret,
or API route implementation changed. `git diff --check` was clean. The final hostile
self-review found two issues in the first implementation (direct-tip OpenAPI omitted
the runtime-accepted token/`403`; CSP omitted Cloudflare's script/frame origins); both
were fixed and regression-tested before this state change.

This is a corrective subtask under the existing `PAY-01` atomic payment boundary; it
does not replace its L04 task/test/review trio or change the §31 register state. The
new audit ID is linked through `08_AUDIT_REMEDIATION_AUTHORITY.md`, and
`TRACEABILITY.md` was regenerated without changing register mappings.
