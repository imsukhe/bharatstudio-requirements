# TC-L01 — Viewer authentication contract slice

**Status:** `Pass — local executable evidence`
**Task:** [`../tasks/L01-viewer-auth-contract-slice.md`](../tasks/L01-viewer-auth-contract-slice.md)

| Case | Expected result | Evidence |
| --- | --- | --- |
| Signup/login contract | Bounded email/password/device requests and the opaque viewer session response are typed. | Pass: `ViewerSignupRequest`, `ViewerLoginRequest`, and `ViewerAuthSessionResponse` validate in v1 OpenAPI and fixture checks. |
| Reset-request privacy | The accepted response carries no account, email, token, or existence indicator. | Pass: the dedicated fixture has only schema version/status/message; hostile email addition is rejected. |
| Reset-completion privacy | The successful reset response carries no session or credential material. | Pass: the dedicated fixture has only schema version/status/message; hostile access-token addition is rejected. |
| Negative fixtures | Added identity, email, password, reset-token, or access-token fields are rejected. | Pass: fixture validator rejects injected viewer identity, email, and access token; strict request schemas mark secrets write-only. |
| Regression | OpenAPI validators and runtime API/web tests continue to pass. | Pass 2026-09-09: contracts 24 fixtures/49 paths/56 operations; API 402/402; web 289/289. |
