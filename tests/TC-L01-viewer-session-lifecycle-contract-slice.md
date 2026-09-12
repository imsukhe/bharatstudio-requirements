# TC-L01 — Viewer session lifecycle contract slice

**Status:** `Pass — local executable evidence`
**Task:** [`../tasks/L01-viewer-session-lifecycle-contract-slice.md`](../tasks/L01-viewer-session-lifecycle-contract-slice.md)

| Case | Expected result | Evidence |
| --- | --- | --- |
| Viewer session auth | Each lifecycle operation declares `viewerBearerAuth`, not creator bearer auth. | Pass: four lifecycle operations declare the dedicated scheme in v1 OpenAPI. |
| Session scope | List response contains bounded own-session metadata/current flag; cross-scope revocation is 404. | Pass: API route tests verify scope; migration `0112` plus L14 SQL proof verify current-viewer isolation and newest-100 cap. |
| Logout | Current session revocation returns 204 with no response body. | Pass: API viewer-route test and OpenAPI 204 contract. |
| Deletion disclosure | Request returns erased/retained disclosure and `legalDispositionOpen: true`; no token or account identity. | Pass: fixture and route test validate disclosure; hostile access-token fixture injection rejects. |
| Session-list bound | A synthetic 101-session viewer list returns exactly the newest 100 rows through the private SQL function. | Pass: `l14_viewer_identity.sql` through the root runner after migration `0112`. |
| Negative fixtures and regression | Identity/token injections reject; validators and full local verifier pass. | Pass: session identity and deletion-token injections reject; `pnpm verify:local` passes on 2026-09-09. |
