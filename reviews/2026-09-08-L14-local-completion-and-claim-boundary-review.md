# L14 local completion and claim-boundary decision

**Decision state:** `Approved — owner instruction to complete all locally actionable Alerts work recorded 2026-09-08`
**Level:** L3
**Owner:** Project owner / Alerts API and web

## Scope

Reconcile the locally present `0107` receipt, claim, badge, and public-profile
work; complete only the missing viewer-facing profile controls and test
coverage; and correct the claim route so it cannot accept a browser-supplied
provider identity. No YouTube OAuth flow, provider credential, payment write,
or legal conclusion is introduced.

## Security and privacy boundary

The client may choose only the provider name. A trusted server-side L15
adapter must supply the verified provider user id and optional display name
for the authenticated viewer before a claim reaches the SQL procedure. Until
that adapter is wired, the route must fail closed. Public-profile controls
remain opt-in/default-private, require a slug to publish, and never display
monetary history. Receipt tokens remain opaque and only their hash is stored.

## Data, migration, rollback, and tests

No schema change is needed: the additive `0107` tables/functions already
provide the durable state. The API dependency is optional and fails closed;
removing it disables claims rather than relaxing the boundary. The web profile
controls are additive and can be hidden without affecting tipping or viewer
auth. Required evidence: focused and full API/web tests, API and web
TypeScript/build checks, the disposable SQL suite, source audit, and central
test/task updates. DPDP legal review, verified-provider configuration, and
staging/browser evidence remain explicit external gates.

## QA reachability decision — 2026-09-14

**State:** `Approved for local implementation by active QA goal; evidence pending`

The existing anonymous receipt contract is approved, but its reachable
post-payment handoff is absent. The narrow correction is to mint a receipt in
both direct-tip and TipIntent UI flows only after the durable public payment-status endpoint reports `paid`; its
opaque token is used only to link the payer to the already-existing receipt
page. The correction has no authorization, provider, data-retention, or
financial-state change. Failure is deliberately non-fatal because payment
truth remains the verified webhook/ledger. Browser, staging, and independent
review evidence remain separate gates.

**Local verification — 2026-09-14:** shared receipt-client tests cover the
strict browser contract and failure boundary; both UI confirmation paths are
compiled against it. `pnpm verify:local` exited 0 after 125 migrations, 52 SQL
proofs, 501 API and 327 web tests, integration/race/load/fault checks, and
three image builds. This is a self-review only; no real browser, provider,
staging, or independent security conclusion is claimed.

## Execution and self-audit — 2026-09-08

The audit rejected the original browser-supplied claim identity design. The
route now admits only a provider selector and resolves identity through the
trusted server-side verifier; it returns `503` without one. Focused API
evidence is **7/7**, focused profile UI evidence is **2/2**, web typecheck and
production build pass, and the full disposable SQL suite is **44/44** after
**110** migrations. No provider, legal, staging, browser/OBS, or independent
review result is asserted.
