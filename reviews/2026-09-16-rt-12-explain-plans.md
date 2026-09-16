# RT-12 — checked-in EXPLAIN plans for every widget-backing query: decision record

**Task:** `../active/tasks/RT-12.md`
**Reviewer:** Sukhdev Singh (owner self-review; independent reviewer unavailable)

**This row's design reasoning, market/provider research (§6 of the owning command), decision log, "proven vs. not proven" statement, the data-plane capture results, Referred-to-Opus list, and disposition all live in the single shared record for this three-row slice:**

→ [`2026-09-16-rt-10-rt-11-rt-12-read-path-discipline.md`](./2026-09-16-rt-10-rt-11-rt-12-read-path-discipline.md) — see its §4 "Data-plane capture (RT-12)" specifically for what the throwaway-database EXPLAIN capture did and did not seed successfully per widget.

Per §5 of the owning command ("Shared design reasoning and the §6 market review belong in one review record, with the other two pointing at it — do not duplicate a review into three that can drift apart"), this file exists only so `active/tasks/RT-12.md`'s Evidence location and the mapping validator's filename convention (`reviews/2026-09-16-rt-12-*.md`) are both satisfied, without a second copy of the same reasoning to drift out of sync.

**Disposition:** `Conditionally complete — local evidence; independent review unavailable` (same disposition, owner and follow-up gate as the shared record — see it directly rather than a restated summary here).
