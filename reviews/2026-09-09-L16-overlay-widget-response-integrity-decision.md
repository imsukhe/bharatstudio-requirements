# Decision — L16/L17 overlay widget response integrity

**State:** `Locally accepted after full deterministic verification`

Overlay browser sources receive remote JSON and must independently validate it
before rendering. Exact client parsing reduces inadvertent identity/payment or
future-store-field exposure without altering the server's token-scoped overlay
authorization or product semantics. This is local browser evidence only;
deployed OBS/browser and staged overlay proof remain open.

## Post-change review — 2026-09-09

The browser no longer relies on a TypeScript type guard that admitted surplus
remote fields or NaN/Infinity values. All affected guards now reject exact-key
and primitive invariant violations before React receives a render value. This
does not alter server ownership or authorization. Focused hostile/full API/web
tests and the subsequently rerun complete verifier, including images, pass. No
live OBS/device or staging claim is made.
