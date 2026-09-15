# RT-01 — overlay idle replay decision

**Task:** `../active/tasks/RT-01.md`  
**Reviewer:** Sukhdev Singh (owner self-review; independent reviewer unavailable)  
**Scope:** Remove connected-idle replay polling while preserving initial replay, notification wake, durable cursor replay, and bounded post-disconnect fallback.  
**Finding:** Connected idle streams now wait for a notification result without replay polling; only listener failure or absent listener enters bounded jitter fallback. Initial replay, two deterministic disconnected fallback replays, reconnect-to-idle transition, cursor/auth boundaries, abort cleanup and no-drop replay failure behavior are locally verified.  
**Severity:** P0 reliability/performance  
**Evidence:** `tests/TC-RT-01-overlay-idle-replay.md`; Alerts API build and 511-test suite passed, including connected-idle zero-query, exact 750ms fallback/reconnect, real loopback SSE request-close abort, abortable sleep cleanup, and listener waiter cleanup tests. No external evidence claimed.  
**Disposition:** `Conditionally complete — local evidence; independent review unavailable`  
**Owner:** Sukhdev Singh  
**Follow-up/release gate:** Terra fresh review must verify the actual worktree and retain the local evidence; no external gate is claimed.  
**Decision lifecycle:** `Approved → Implemented → Verified` (conditionally complete pending independent review)
