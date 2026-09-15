# TC-STEP-0.25 — Measurement environment evidence

**Owner:** Sukhdev Singh
**Status:** Conditionally complete — local controls verified; external gates remain open

## Per-ID controls

| ID | Command | Result / gate |
|---|---|---|
| ENV-01 | node ../bharatstudio-infra/tools/validate-measurement-manifest.mjs --template | Infra suite passed; Cloud Run/IAM open |
| ENV-02 | ../bharatstudio-alerts/scripts/measurement/run-local-measurement.sh --artifact /tmp/ENV-02.json | PostgreSQL16, 126 migrations, bounded load, cleanup passed |
| ENV-03 | infra validator template | Razorpay sandbox blocked |
| ENV-04 | infra validator template | OBS/Chromium blocked |
| ENV-05 | infra validator template | Device lab blocked |
| ENV-06 | infra validator template | Network shaping blocked |
| ENV-07 | Alerts runner artifact | p50/p95/p99 and redaction recorded locally |
| ENV-08 | Alerts runner --full | Target concurrency staging blocked; exit 2 |
| ENV-09 | bootstrap_check.py | Owner/change control verified |

Infra tests: 24 passed. Alerts measurement tests: 3 passed; seam tests: 4 passed. All local evidence is conditional and external evidence is not claimed.

