# STEP-0 — Register-to-L-track mapping and `active/` records

**Authority:** [`../launch/07_BUILD_BOOTSTRAP_AUTHORITY.md`](../launch/07_BUILD_BOOTSTRAP_AUTHORITY.md) §1
**Status:** `Proposed — not started`

Written under the §1 bootstrap exemption: this is one of the two steps that produce the
`active/` records, so its own record is written as the step rather than before it. It
carries the same ten §31.0 fields as every row it will create.

| Field | Value |
|---|---|
| **Scope phase** | `v1` — it precedes and gates every v1 lane |
| **Owner** | **UNASSIGNED** — must be named before this starts |
| **Tier and gate** | None. Governance work, not a creator-facing capability. No registry row |
| **Personal-data class** | None. It maps identifiers between documents |
| **Provider or legal dependency** | None |
| **Failure behaviour** | If the mapping is wrong, a lane credits evidence to the wrong requirement. Mitigated by review: every mapped pair is checked by someone who traced the user path (§35.1 rule 1), not by string match alone |
| **Kill switch** | Not applicable. The mapping is data; a wrong entry is corrected, not disabled |
| **Acceptance test** | `tools/traceability.py` reports every register row as either mapped to an existing L-track record or carrying a new `active/` record with all ten fields; `tools/doc_consistency.py` gains the Missing-row-metadata check and passes |
| **Evidence location** | `TRACEABILITY.md`, regenerated in CI, plus the per-row records under `active/tasks/` |
| **Rollback** | The mapping is additive. Reverting means deleting the added records; no product state changes |

## The work

1. **Inventory.** 62 task records, 62 test records, 72 reviews in `tasks/`, `tests/`,
   `reviews/`, keyed on `L01`…`L32` plus `WP-`, `FORM-`, `FRD-` identifiers. The §31
   register holds its rows under area prefixes. Two of them currently meet.
2. **Map.** For each register row, find the L-track record that already covers it, if
   one does. A mapping is proposed by search and **confirmed by a person**.
3. **Credit.** Where a mapped record carries a test record and a review, the register row
   inherits them as acceptance and review evidence — subject to §37.10, which still
   forbids crediting a local suite as launch evidence.
4. **Create.** Where nothing covers a row, write an `active/tasks/<ID>.md` with the ten
   fields. Only for rows a lane is about to take; a stub with ten empty fields is not a
   record and the checker must reject it.
5. **Enforce.** Turn on the two §35.3 checks that this unblocks — Missing row metadata,
   and a stricter phase check that reads the phase from the `active/` record rather than
   only the register column.

## Explicitly not in scope

Filling ten fields for all 634 rows. That would be documentation theatre. Rows are
recorded when a lane takes them; the mapping exists so that taking one is cheap.
