# Canvas audit at eleven modules — what is correct, and the one property that grows

**Date:** 2026-09-17
**Owner:** Sukhdev Singh
**Authority:** `FULL-PRODUCT-DEFINITION.md` §6, §12.7, §19.0 RT-01/RT-02/RT-10/RT-11, §19.4, §19.5
**Scope:** read-only audit of the Master Canvas runtime at eleven of twenty modules. No code changed.

## Why this was run

Every slice adds a module to one shared connection and one shared frame loop. The per-slice tests
prove each module in isolation; none of them asks what happens when **eleven** are active at once.
That question only gets more expensive to answer later, so it was asked now.

## Verified correct — stated because it was checked, not assumed

| Property | How it is actually enforced |
|---|---|
| One transport, one loop | Exactly one `createMasterCanvasConnection(` and one `createMasterCanvasRuntime(` call site in the host page, across eleven `registerModule` calls. |
| An unentitled module costs nothing | Modules register with `entitled: false`; the runtime activates only when `entitled && !pageHidden && status !== 'down'`. A Free channel (cap 2) fetches two snapshots, not eleven. |
| Snapshot modules do not go stale | `subscribe()` is a "something changed, go re-read" signal; each module's callback re-fetches. Modules do not poll and do not run their own timers (PRF-02.2). |
| **A reconnect re-reads every module** | `master-canvas-connection.ts:245` — a (re)connect calls `notifyAll()`, then emits a `connected` marker for event-payload subscribers. The claim in `active/tasks/PRF-02.md` is implemented, not aspirational. |

**A wrong suspicion of mine, recorded because the reasoning is the reusable part.** Counting
`fetchSnapshot()` occurrences showed exactly one per module file, which looked like "fetched once
at activation, never again" — a frozen goal bar after any connection blip, and a textbook §2
finding. It was wrong. The single occurrence sits inside a `refetch()` helper that both `activate()`
and the `subscribe()` callback invoke. **Counting call sites measured the wrong thing; following the
call graph answered the question.** A grep count is evidence of textual frequency, never of
behaviour.

## The property that grows, and is not a defect today

A reconnect fires `notifyAll()`, so **every active module re-reads its snapshot at once**. At
eleven modules that is up to eleven concurrent reads per overlay; at the full twenty-module
catalogue it is up to twenty. Across many overlays reconnecting together after one server blip, the
bursts correlate.

This is absorbed by machinery that already exists and was built for exactly this: RT-10's admission
control sheds a `derived_read` before auth, body parsing or handler work, and RT-11's bounded
derived-read pool carries a statement timeout. It is also mitigated by real sharing —
`fetchGoalSnapshot` serves three modules (Goal Ladder, Boss Fight, Milestone Celebration), so the
module count is an upper bound on requests, not the request count.

**It is recorded as an amplification factor that scales linearly with the catalogue, not as a bug.**
The honest statement of what is unknown: the burst has never been measured. RT-07 is Blocked, the
EXPLAIN artefacts are plan-shape detectors on minimal seeds, and the load self-test exercises a
mechanism rather than a load. Nothing here says the canvas does or does not hold up at twenty
modules under real reconnect storms — only that the machinery meant to absorb it is present and
reachable.

## What would settle it, and what must not be done instead

Settling it needs RT-07-class evidence: a real browser in OBS, a real reconnect, a real module
count. **It must not be "settled" by adding a stagger or a jitter now** — that would be inventing a
delay value with no measurement behind it, and §19.5's bounded-data rules are already satisfied.
The correct move is to leave the mechanism simple and measure it when measurement becomes possible.

## What this evidence is not

A read of source at one commit. No browser, no OBS, no device, no network profile, no load. Not
production, provider, store, legal, device or release readiness. RT-07 remains Blocked.
