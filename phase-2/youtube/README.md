# Phase 2 — YouTube

**Status:** `Deferred / not in v1`  
**Legacy source filenames:** `requirements/16_YOUTUBE_UNIFIED_EVENTS_AND_SUPPORTER_IDENTITY.md` and `tasks/youtube/P16-youtube-unified-events-and-supporter-identity.md` from the frozen legacy snapshot. They are evidence only; see [`../../done/LEGACY_EVIDENCE_REGISTER.md`](../../done/LEGACY_EVIDENCE_REGISTER.md).

Phase 2 owns YouTube OAuth scopes, polling, cursors, live data, SuperChat/membership/engagement normalization, supporter identity, catch-up summaries, associated Companion views, quota allocation, and recovery.

Before any code is written, this folder needs a freshly approved narrow FRD slice, quota evidence, provider-scope confirmation, a Go worker design, cursor/replay/load tests, privacy review, and rollback plan. No v1 surface may request YouTube data permissions or display YouTube integration controls.
