# Decision — L04/L14 anonymous payment identity attribution

**State:** `Implemented and locally verified; conditionally complete pending independent/external evidence`

This fixes the confirmed all-null identity writer defect without making login a
payment prerequisite or accepting client-selected identities. The reviewed
boundary is an opaque first-party cookie fingerprint and the existing trusted
payment-webhook transaction. Provider verification, deployment/browser-device
evidence, and DPDP counsel remain separate gates.

## Self-review — 2026-09-14

**Reviewer:** active QA goal agent (self-review; no independent reviewer was available).

Three high-severity findings were identified and corrected before closure: an authorization event could set identity before capture, preventing the later-created alert from receiving it; a one-time aggregate increment could miss or double-count settlement/refund sequences; and an expired fingerprint could not create a new identity because it was uniquely indexed. The accepted implementation projects payment and alert independently on every verified payment event, recomputes the supporter relation from durable payment/refund state via a trigger, and retires an expired fingerprint to an unrelated opaque tombstone before creating a replacement identity. The disposable PostgreSQL proof exercises expiry replacement, duplicate, authorization→capture, and full-refund sequences. A security suite also flagged the new `SECURITY DEFINER` helper as PUBLIC-executable until its explicit revoke was added; the suite then passed.

Evidence is the final 2026-09-14 `pnpm verify:local` exit 0 run, including 125 migration application, 52 SQL proofs, 501 API + 325 web tests, race-enabled Go tests and three image builds. The web client now defaults checkout/status requests to credentialed same-site fetch so the secure cookie is actually reusable across web/API origins. Disposition: no locally reproducible finding remains in this slice; independent code review, real browser/provider sandbox, staging migration/rollback, and DPDP/legal retention review remain release gates.
