# TC-L14 — Viewer client response-integrity hardening

**Status:** `Pass — local client and root-verifier evidence`  
**Task:** [`../tasks/L14-viewer-client-response-integrity.md`](../tasks/L14-viewer-client-response-integrity.md)

| ID | Action | Expected result |
| --- | --- | --- |
| L14-VC-01 | Parse a valid dashboard/session/deletion response | Narrow typed result is returned. |
| L14-VC-02 | Supply malformed nested fields, unknown keys, or invalid enum values | Client rejects the response before state/rendering. |
| L14-VC-03 | Run focused web and root local verification | All local regression gates pass. |

## Evidence — 2026-09-09

L14-VC-01 passed: valid dashboard, session and deletion payloads parse into the
existing narrow client types. L14-VC-02 passed: malformed date, leaked account
ID, leaked access token, wrong boolean/enum, and extra nested properties are
rejected with `Server response was invalid`. L14-VC-03 passed: focused web
typecheck/test **2/2** and the complete root verifier completed successfully.
All test values are synthetic and local only.
