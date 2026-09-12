# Decision — L01 overlay goal/challenge read contracts

**State:** `Locally accepted after full deterministic verification`

The overlay token is intentionally scoped to browser-source rendering, not a
license to expose storage shape. Explicit server serialization plus browser
validation is authorized to prevent future store changes from expanding this
response. No authorization or payment/product behavior is changed.

## Post-change review — 2026-09-09

The raw-store serialization finding is remediated by named response fields and
direct hostile store-object tests. The dependency status correction prevents
clients from interpreting an infrastructure failure as bad authorization.
Schemas independently reject payment, account, provider and refund widening.
Focused checks and the subsequently rerun complete verifier, including images,
pass. No deployed/browser-device/staging claim is made.
