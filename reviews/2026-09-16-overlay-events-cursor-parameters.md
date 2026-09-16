# `get_overlay_events`'s cursor parameters — why they are inert, and why that is not a bug

**Date:** 2026-09-16
**Owner:** Sukhdev Singh
**Authority:** `FULL-PRODUCT-DEFINITION.md` §19.0 RT-01/RT-02, §12.7
**Status:** Analysis complete. The one safe change is identified and **deliberately not yet
applied** — an agent was working in the same tree, and editing under it is the exact mistake
this session already recorded twice.

## Correcting my own earlier finding

I recorded this as "dead `target_after_created_at` / `target_after_delivery_id` params in
`get_overlay_events`", which reads as an oversight to be deleted. The deadness is real; the
framing was wrong, and the real reason is load-bearing enough that deleting the parameters
without understanding it could have reintroduced a defect the schema history already fixed.

## What actually happened, traced through the migrations

| Migration | Status predicate | Cursor used as a filter? |
|---|---|---|
| `0003`–`0054` | includes `acknowledged` | **yes** |
| `0055` | — | **no**, and the header says why |
| `0062` | includes `acknowledged` | **yes** |
| `0064`, `0067`, `0096`, `0101`, `0127` (current) | `('ready', 'displayed')` — `acknowledged` **excluded** | **no** |

`0055`'s header states the constraint that governs all of this:

> "The cursor is an acknowledgement checkpoint, not an eligibility filter: an older row that is
> still unacknowledged must remain replayable or it can be skipped permanently after the newer
> cursor is acknowledged."

That is a real correctness rule, not a preference. Deliveries can be published out of order, so
filtering by cursor position can strand an older unacknowledged delivery forever once a newer
one is acknowledged.

The current design satisfies that rule **by a different mechanism**: acknowledgement is expressed
in `delivery.status`, and the query simply excludes `acknowledged`. Acknowledgement *is* the
eligibility filter, so a positional cursor filter is redundant — and, per `0055`, would be
actively harmful if reintroduced alongside it.

So the parameters are vestigial from the `0062`-era shape, carried through four recreates.
Nothing reads them. Nothing should.

## What is genuinely wrong

1. **The signature lies to its caller.** `apps/api/src/db/overlay-store.ts:45` parses a cursor out
   of `Last-Event-ID` and passes it into two parameters that are ignored. A reader of that call
   site reasonably concludes replay resumes from the cursor. It does not.
2. **`0127`, the current definition, does not explain any of this.** The rationale lives in
   `0055`, seventy-two migrations earlier. A maintainer reading the live definition sees two
   parameters doing nothing and no reason given — the same "a comment is not enforcement" problem
   as RT-03, one step removed.

## The change to make, and the one not to make

**Safe, and intended:** drop the two inert parameters in a new forward migration, update the one
caller, refresh the EXPLAIN artefact and the manifest entry (the signature appears in
`required-queries.json`). Carry `0055`'s rationale forward into the new migration's header so the
next recreate cannot lose it again — that is the actual fix, more than the parameter removal.

**Not to be done unilaterally:** the HTTP replay surface accepts `Last-Event-ID` and does not use
it as a resume point. That is correct per `0055`, but it is a contract-level statement about what
a documented header does, and changing or documenting it publicly is a product decision, not a
refactor. Recorded as an open question rather than decided here.

## Open question for the owner

> `Last-Event-ID` is accepted by the overlay replay endpoint and deliberately does not act as a
> resume point, because an unacknowledged delivery must stay replayable regardless of cursor
> position (`0055`). Should the endpoint keep accepting the header silently, reject it, or state
> in the OpenAPI contract that it is accepted and intentionally not a resume point?

## What this evidence is not

Local reading of migration history and one call site. No database was measured, no replay was
exercised against a running overlay, and nothing here is production, provider, device or
release evidence. No claim is made that any overlay has ever missed or duplicated a delivery.
