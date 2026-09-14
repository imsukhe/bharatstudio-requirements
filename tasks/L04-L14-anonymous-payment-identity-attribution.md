# L04/L14 — Anonymous payment identity attribution

**Status:** `Conditionally complete locally; independent/provider/browser staging evidence pending`
**Level:** L3
**Parent authority:** `L04-go-payment-boundary.md`; `L14-viewer-identity-and-supporter-history.md`; `2026-09-13-reachability-register.md §1`
**Test record:** [`../tests/TC-L04-L14-anonymous-payment-identity-attribution.md`](../tests/TC-L04-L14-anonymous-payment-identity-attribution.md)
**Review:** [`../reviews/2026-09-14-L04-L14-anonymous-payment-identity-attribution-decision.md`](../reviews/2026-09-14-L04-L14-anonymous-payment-identity-attribution-decision.md)

## Scope, data boundary, migration, and acceptance

At public checkout, mint or rotate a server-generated opaque anonymous-browser
token only after a payment order is accepted. Store only a SHA-256 fingerprint
and bounded expiry server-side; send the raw token solely as a first-party,
secure, HTTP-only, SameSite=Lax cookie. The checkout service receives only the
resolved `viewer_identity_id` in its private request. The verified webhook
transaction writes that identity exactly once into new payments and any
corresponding alert event, then atomically derives the per-channel supporter
relation. Existing/anonymous-no-cookie payments remain nullable and unchanged;
no browser can submit a UUID or claim another identity.

This applies to both public order entry points: the channel tip checkout and
the opaque TipIntent confirmation checkout. TipIntent request data remains
server-authoritative; this slice adds only the same browser-derived anonymous
fingerprint to its existing private payment call.

Migration is forward-only: a security-definer lookup-or-create procedure and a
new version of the payment webhook procedure/private Go-store query. It must
preserve append-only payment facts, webhook idempotency, anonymous no-login
tipping, financial privacy, and cross-channel isolation. Retention follows the
existing anonymous expiry design; identity cookies have no analytics purpose.

Test plan: clean PostgreSQL proof of mint/reuse/expiry, webhook idempotency,
payment/event/relation attribution, null fallback, and cross-channel isolation;
API test proving no identity UUID is accepted; Go payment-store contract test;
full deterministic verifier. Rollback is a forward deployment rollback to the
previous immutable image plus disabling cookie minting: the nullable identity
column means payments continue normally, and retained linked records are not
rewritten. No production migration, provider, browser-device, or legal closure
is claimed here.

## Local implementation and evidence — 2026-09-14

Implemented through migration `0124_v1_l04_l14_anonymous_payment_identity_attribution.sql`, the public checkout route, and the payment-webhook Go store. The raw cookie token stays browser-only; the private boundary receives only a SHA-256 hexadecimal fingerprint. A durable payment trigger recomputes the per-channel net supporter relation from captured/refunded ledger rows whenever identity or settlement state changes, avoiding authorization-before-capture ordering defects and duplicate increments.

Final reproducible local evidence: `pnpm verify:local` exited 0 on 2026-09-14 after the expiry-replay correction. It applied 125 migrations, passed 52 isolated PostgreSQL proofs (including cookie identity reuse, expiry replacement, duplicate webhook, authorization→capture, and full-refund attribution), validated 39 fixtures plus 67 OpenAPI paths/74 operations/3 negative operation cases, ran 501 API tests, race-enabled Go checks, deterministic overlay/race/load/fault integration checks, and built the three declared images. Synthetic-only fixtures; no raw tokens, provider credentials, customer data, production database, device browser, store, or staging system were used.

The task remains conditional under governance because no independent reviewer, real browser, provider sandbox, staging migration/rollback, or privacy/legal retention evidence has been supplied.
