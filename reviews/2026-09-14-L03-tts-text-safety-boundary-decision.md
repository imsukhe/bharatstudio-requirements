# Decision — L03 TTS text safety boundary

**State:** `Accepted for local verification; policy and deployment evidence remain open`

The reachability register identifies spoken user-controlled text as a safety
risk. This decision authorizes technical input neutralization only. It does not
constitute a language/content policy, provider moderation claim, or production
readiness approval.

## Review outcome — 2026-09-14

The review reproduced technical payload variants that could otherwise be spoken
or produce distinct cache keys. The adapter now has a small deterministic
neutralization boundary, and the service avoids provider dispatch for text that
becomes empty. Tests prove all stated technical cases and the complete local
verifier passes. Profanity, context, user blocking, and non-English moderation
are intentionally retained as unapproved policy work rather than implied by
this implementation.
