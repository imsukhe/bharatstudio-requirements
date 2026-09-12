# TC-L16 — Vote-option cardinality and overlay contract alignment

**Status:** `Pass — locally reproducible 2026-09-09; external evidence pending`  
**Task:** [`../tasks/L16-vote-option-cardinality-and-overlay-contract-alignment.md`](../tasks/L16-vote-option-cardinality-and-overlay-contract-alignment.md)

| ID | Action | Expected result |
| --- | --- | --- |
| L16-VOC-01 | Create 16 valid options through the SQL procedure | Each is accepted. |
| L16-VOC-02 | Attempt a 17th option | Procedure returns `invalid`; no row is inserted. |
| L16-VOC-03 | Hold the definition lock while another creation is attempted | Creation serializes and cannot bypass the cap. |
| L16-VOC-04 | Run contract/browser/API/SQL/full local verification | Published and executable limits remain aligned. |

**Evidence:** migration 0116 applies in the isolated suite; the new SQL proof
passes alongside 45 existing proofs (46/46 total), confirms the sequential cap
and stored-procedure lock, and the full verifier exits 0. A multi-process
staging concurrency rehearsal remains an external follow-up, not a completed
claim.
