# L17 non-refundable challenge implementation decision

**Decision state:** `Implemented local alternative; original refundable paid-challenge scope remains blocked pending product/provider decision`
**Level:** L3
**Owner:** Project owner / Alerts API, database, web

## Finding

`0109_v1_l17_paid_challenges.sql` deliberately implements creator-set,
non-refundable stake/bounty goals rather than the task's viewer-proposed,
refund-capability-gated paid challenges. Repository evidence shows no current
provider rail can initiate or track a merchant refund. Recording 0109 as a
pass for the original task would falsely claim refund, proposal, payment-link,
and dispute capability.

## Approved local boundary

Keep the existing additive `challenges` and `challenge_status_events` state
machine only as a non-refundable creator goal: draft → active → succeeded /
failed / cancelled; confirmed payments determine progress; refunds observed
from the creator's own provider dashboard reduce progress. Failure copy must
state that the contribution is a tip and no refund is promised. No provider
refund operation, escrow, viewer proposal, payment link, dispute workflow, or
chat command is introduced locally.

## Verification and rollback

The local state machine, role/tier gate, refund-derived progress, append-only
status history, dashboard, and overlay have executable SQL/API/web tests.
The change is additive; hiding the challenge surfaces disables it without
changing payment/refund records. A future refundable challenge must receive a
new explicit authority slice after L19 proves a provider capability snapshot,
refund initiation/status adapter, sandbox evidence, and consumer copy review.
