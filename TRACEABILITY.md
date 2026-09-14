# Traceability index

**Generated 2026-09-14 by `tools/traceability.py`. Do not edit by hand.**

Six columns per `FULL-PRODUCT-DEFINITION.md` §35.4:
`requirement → task → acceptance record → review → evidence → release gate`.

This file reports only what the generator can find by searching the repository for
each requirement ID. A blank cell means **no file in that corpus mentions this ID** —
which is not the same as no work existing. See the finding below.

## What exists in this repository

| Corpus | Files |
|---|---:|
| `tasks/` task records | 62 |
| `tests/` test records | 62 |
| `reviews/` reviews | 72 |
| `done/` legacy evidence | 3 |
| `active/` authority and task records | 7 |
| `active/launch/` external evidence register | 6 |

**739 requirement rows in the register.**

## The finding: two ID systems that do not meet

Substantial prior work exists — task records, test records and reviews — but it is
keyed on the **L-track** system (`L01`…`L32`, plus `WP-`, `FORM-`, `FRD-` work-package
identifiers). The register in §31 is keyed on **area prefixes** (`PAY-`, `CMP-`, `RT-`,
…). Almost nothing references both, so the two bodies of work cannot currently be
joined.

| Register rows with a … | Count | Of 739 |
|---|---:|---:|
| task record naming the ID | 2 | 739 |
| test record naming the ID | 0 | 739 |
| review naming the ID | 0 | 739 |
| `done/` legacy evidence naming the ID | 0 | 739 |
| external evidence register naming the ID | 1 | 739 |
| `active/` record naming the ID | 1 | 739 |
| an explicit L-track pointer in its text | 1 | 739 |

**So the gap is a missing mapping, not (only) missing work.** Building that mapping —
register ID → L-track record where one exists, and a new `active/` record where one
does not — is the first task in §34's Step 0, and until it exists §34 is a proposed
roadmap rather than a schedulable plan.

The §31.0 contract still holds independently: a row is schedulable only when its
`active/` record carries all ten fields. That is true of **1** rows today.

## Rows

| ID | Section | Phase | State | Pri | Task | Acceptance | Review | Evidence | L-track hint | Required suites (§37.11) | Release gate |
|---|---|:-:|:-:|:-:|---|---|---|---|---|---|---|
| PAY-01 | §31.2 Payments and money | v1 | U | — |  |  |  |  |  | PAY-E1..E8 · raid burst · duplicate-webhook and dispatcher-down chaos · isolation | none |
| PAY-02 | §31.2 Payments and money | v1·G | U | — |  |  |  |  |  | PAY-E1..E8 · raid burst · duplicate-webhook and dispatcher-down chaos · isolation | release |
| PAY-03 | §31.2 Payments and money | v1 | U | — |  |  |  |  |  | PAY-E1..E8 · raid burst · duplicate-webhook and dispatcher-down chaos · isolation | none |
| PAY-04 | §31.2 Payments and money | v1·G | U | — |  |  |  |  |  | PAY-E1..E8 · raid burst · duplicate-webhook and dispatcher-down chaos · isolation | release |
| PAY-05 | §31.2 Payments and money | v1 | U | — |  |  |  |  |  | PAY-E1..E8 · raid burst · duplicate-webhook and dispatcher-down chaos · isolation | none |
| PAY-06 | §31.2 Payments and money | v1 | U | — |  |  |  |  |  | PAY-E1..E8 · raid burst · duplicate-webhook and dispatcher-down chaos · isolation | none |
| PAY-07 | §31.2 Payments and money | v1 | U | — |  |  |  |  |  | PAY-E1..E8 · raid burst · duplicate-webhook and dispatcher-down chaos · isolation | none |
| PAY-08 | §31.2 Payments and money | v1·G | U | — |  |  |  |  |  | PAY-E1..E8 · raid burst · duplicate-webhook and dispatcher-down chaos · isolation | release |
| PAY-09 | §31.2 Payments and money | v1·G | U | — |  |  |  |  |  | PAY-E1..E8 · raid burst · duplicate-webhook and dispatcher-down chaos · isolation | release |
| PAY-10 | §31.2 Payments and money | v1 | U | — |  |  |  |  |  | PAY-E1..E8 · raid burst · duplicate-webhook and dispatcher-down chaos · isolation | none |
| PAY-11 | §31.2 Payments and money | v1·G | U | — |  |  |  |  |  | PAY-E1..E8 · raid burst · duplicate-webhook and dispatcher-down chaos · isolation | release |
| PAY-12 | §31.2 Payments and money | v1·G | P | P1 |  |  |  |  |  | PAY-E1..E8 · raid burst · duplicate-webhook and dispatcher-down chaos · isolation | release |
| PAY-13 | §31.2 Payments and money | v1·G | X | P0 |  |  |  |  |  | PAY-E1..E8 · raid burst · duplicate-webhook and dispatcher-down chaos · isolation | release |
| PAY-14 | §31.2 Payments and money | v1 | X | P0 |  |  |  |  |  | PAY-E1..E8 · raid burst · duplicate-webhook and dispatcher-down chaos · isolation | release |
| PAY-15 | §31.2 Payments and money | v1 | X | P0 |  |  |  |  |  | PAY-E1..E8 · raid burst · duplicate-webhook and dispatcher-down chaos · isolation | release |
| PAY-16 | §31.2 Payments and money | v1 | X | P0 |  |  |  |  |  | PAY-E1..E8 · raid burst · duplicate-webhook and dispatcher-down chaos · isolation | release |
| PAY-17 | §31.2 Payments and money | v1 | P | P1 |  |  |  |  |  | PAY-E1..E8 · raid burst · duplicate-webhook and dispatcher-down chaos · isolation | release |
| PAY-18 | §31.2 Payments and money | v1 | X | P2 |  |  |  |  |  | PAY-E1..E8 · raid burst · duplicate-webhook and dispatcher-down chaos · isolation | none |
| PAY-19 | §31.2 Payments and money | v1 | A | P2 |  |  |  |  |  | PAY-E1..E8 · raid burst · duplicate-webhook and dispatcher-down chaos · isolation | none |
| PAY-20 | §31.2 Payments and money | v1 | A | P1 |  |  |  |  |  | PAY-E1..E8 · raid burst · duplicate-webhook and dispatcher-down chaos · isolation | release |
| PAY-21 | §31.2 Payments and money | v1 | A | P2 |  |  |  |  |  | PAY-E1..E8 · raid burst · duplicate-webhook and dispatcher-down chaos · isolation | none |
| PAY-22 | §31.2 Payments and money | v1 | U | — |  |  |  |  |  | PAY-E1..E8 · raid burst · duplicate-webhook and dispatcher-down chaos · isolation | none |
| PAY-23 | §31.2 Payments and money | v1 | U | — |  |  |  |  |  | PAY-E1..E8 · raid burst · duplicate-webhook and dispatcher-down chaos · isolation | none |
| PAY-24 | §31.2 Payments and money | v1 | U | — |  |  |  |  |  | PAY-E1..E8 · raid burst · duplicate-webhook and dispatcher-down chaos · isolation | none |
| PAY-25 | §31.2 Payments and money | v1 | U | — |  |  |  |  |  | PAY-E1..E8 · raid burst · duplicate-webhook and dispatcher-down chaos · isolation | none |
| PAY-26 | §31.2 Payments and money | v1 | A | P1 |  |  |  |  |  | PAY-E1..E8 · raid burst · duplicate-webhook and dispatcher-down chaos · isolation | release |
| PAY-27 | §31.2 Payments and money | v1 | A | P1 |  |  |  |  |  | PAY-E1..E8 · raid burst · duplicate-webhook and dispatcher-down chaos · isolation | release |
| PAY-30 | §31.2 Payments and money | N | N | — |  |  |  |  |  | PAY-E1..E8 · raid burst · duplicate-webhook and dispatcher-down chaos · isolation | none |
| PAY-28 | §31.2 Payments and money | v1 | B | — |  |  |  |  |  | PAY-E1..E8 · raid burst · duplicate-webhook and dispatcher-down chaos · isolation | none |
| PAY-29 | §31.2 Payments and money | v1 | B | — |  |  |  |  |  | PAY-E1..E8 · raid burst · duplicate-webhook and dispatcher-down chaos · isolation | none |
| ALQ-01 | §31.3 Alerts, queues, overlay | v1 | U | — |  |  |  |  |  | PAY-E1..E8 · raid burst | none |
| ALQ-02 | §31.3 Alerts, queues, overlay | v1 | U | — |  |  |  |  |  | PAY-E1..E8 · raid burst | none |
| ALQ-03 | §31.3 Alerts, queues, overlay | v1 | U | — |  |  |  |  |  | PAY-E1..E8 · raid burst | none |
| ALQ-04 | §31.3 Alerts, queues, overlay | v1 | P | P0 |  |  |  |  |  | PAY-E1..E8 · raid burst | release |
| ALQ-05 | §31.3 Alerts, queues, overlay | v1 | U | — |  |  |  |  |  | PAY-E1..E8 · raid burst | none |
| ALQ-06 | §31.3 Alerts, queues, overlay | v1 | U | — |  |  |  |  |  | PAY-E1..E8 · raid burst | none |
| ALQ-07 | §31.3 Alerts, queues, overlay | v1 | U | — |  |  |  |  |  | PAY-E1..E8 · raid burst | none |
| ALQ-08 | §31.3 Alerts, queues, overlay | v1 | U | — |  |  |  |  |  | PAY-E1..E8 · raid burst | none |
| ALQ-09 | §31.3 Alerts, queues, overlay | v1 | U | — |  |  |  |  |  | PAY-E1..E8 · raid burst | none |
| ALQ-10 | §31.3 Alerts, queues, overlay | v1 | U | — |  |  |  |  |  | PAY-E1..E8 · raid burst | none |
| ALQ-11 | §31.3 Alerts, queues, overlay | v1 | U | — |  |  |  |  |  | PAY-E1..E8 · raid burst | none |
| ALQ-12 | §31.3 Alerts, queues, overlay | v1 | U | — |  |  |  |  |  | PAY-E1..E8 · raid burst | none |
| ALQ-13 | §31.3 Alerts, queues, overlay | v1 | U | — |  |  |  |  |  | PAY-E1..E8 · raid burst | none |
| ALQ-14 | §31.3 Alerts, queues, overlay | v1 | U | — |  |  |  |  |  | PAY-E1..E8 · raid burst | none |
| ALQ-15 | §31.3 Alerts, queues, overlay | v1 | A | P2 |  |  |  |  |  | PAY-E1..E8 · raid burst | none |
| ALQ-16 | §31.3 Alerts, queues, overlay | v1 | A | P1 |  |  |  |  |  | PAY-E1..E8 · raid burst | release |
| ALQ-17 | §31.3 Alerts, queues, overlay | v1 | A | P2 |  |  |  |  |  | PAY-E1..E8 · raid burst | none |
| ALQ-18 | §31.3 Alerts, queues, overlay | v1 | A | P0 |  |  |  |  |  | PAY-E1..E8 · raid burst | release |
| ALQ-19 | §31.3 Alerts, queues, overlay | v1 | A | P2 |  |  |  |  |  | PAY-E1..E8 · raid burst | none |
| TTS-01 | §31.4 TTS | v1 | U | — |  |  |  |  |  | OVL-E6, OVL-E7 · TTS-down chaos · safety corpus on both routes | none |
| TTS-02 | §31.4 TTS | v1·G | U | — |  |  |  |  |  | OVL-E6, OVL-E7 · TTS-down chaos · safety corpus on both routes | release |
| TTS-03 | §31.4 TTS | v1 | U | — |  |  |  |  |  | OVL-E6, OVL-E7 · TTS-down chaos · safety corpus on both routes | none |
| TTS-04 | §31.4 TTS | v1·G | U | — |  |  |  |  |  | OVL-E6, OVL-E7 · TTS-down chaos · safety corpus on both routes | release |
| TTS-05 | §31.4 TTS | v1 | U | — |  |  |  |  |  | OVL-E6, OVL-E7 · TTS-down chaos · safety corpus on both routes | none |
| TTS-06 | §31.4 TTS | v1 | A | **P0** |  |  |  |  |  | OVL-E6, OVL-E7 · TTS-down chaos · safety corpus on both routes | release |
| TTS-07 | §31.4 TTS | v1·G | A | P1 |  |  |  |  |  | OVL-E6, OVL-E7 · TTS-down chaos · safety corpus on both routes | release |
| TTS-08 | §31.4 TTS | v1 | A | P1 |  |  |  |  |  | OVL-E6, OVL-E7 · TTS-down chaos · safety corpus on both routes | release |
| TTS-09 | §31.4 TTS | v1 | P | P1 |  |  |  |  |  | OVL-E6, OVL-E7 · TTS-down chaos · safety corpus on both routes | release |
| TTS-10 | §31.4 TTS | v1 | A | P1 |  |  |  |  |  | OVL-E6, OVL-E7 · TTS-down chaos · safety corpus on both routes | release |
| TTS-11 | §31.4 TTS | v1 | A | P1 |  |  |  |  |  | OVL-E6, OVL-E7 · TTS-down chaos · safety corpus on both routes | release |
| TTS-12 | §31.4 TTS | v1 | A | P1 |  |  |  |  |  | OVL-E6, OVL-E7 · TTS-down chaos · safety corpus on both routes | release |
| TTS-13 | §31.4 TTS | v1 | A | P1 |  |  |  |  |  | OVL-E6, OVL-E7 · TTS-down chaos · safety corpus on both routes | release |
| TTS-14 | §31.4 TTS | v1 | A | P2 |  |  |  |  |  | OVL-E6, OVL-E7 · TTS-down chaos · safety corpus on both routes | none |
| TTS-15 | §31.4 TTS | v1·G | A | P1 |  |  |  |  |  | OVL-E6, OVL-E7 · TTS-down chaos · safety corpus on both routes | release |
| TTS-16 | §31.4 TTS | v1 | A | **P0 with TTS-06** |  |  |  |  |  | OVL-E6, OVL-E7 · TTS-down chaos · safety corpus on both routes | release |
| TTS-17 | §31.4 TTS | v1 | A | P1 |  |  |  |  |  | OVL-E6, OVL-E7 · TTS-down chaos · safety corpus on both routes | release |
| VID-01 | §31.5 Viewer identity, history, trust | v1 | A | **P0** |  |  |  |  |  | PAY-E1..E8 · isolation | release |
| VID-02 | §31.5 Viewer identity, history, trust | v1 | A | **P0** |  |  |  |  |  | PAY-E1..E8 · isolation | release |
| VID-03 | §31.5 Viewer identity, history, trust | v1 | X | **P0** |  |  |  |  |  | PAY-E1..E8 · isolation | release |
| VID-04 | §31.5 Viewer identity, history, trust | v1 | U | — |  |  |  |  |  | PAY-E1..E8 · isolation | none |
| VID-05 | §31.5 Viewer identity, history, trust | v1 | P | P0 |  |  |  |  |  | PAY-E1..E8 · isolation | release |
| VID-06 | §31.5 Viewer identity, history, trust | v1 | X | P1 |  |  |  |  |  | PAY-E1..E8 · isolation | release |
| VID-07 | §31.5 Viewer identity, history, trust | v1 | X | P1 |  |  |  |  |  | PAY-E1..E8 · isolation | release |
| VID-08 | §31.5 Viewer identity, history, trust | v1 | U | — |  |  |  |  |  | PAY-E1..E8 · isolation | none |
| VID-09 | §31.5 Viewer identity, history, trust | v1 | U | — |  |  |  |  |  | PAY-E1..E8 · isolation | none |
| VID-10 | §31.5 Viewer identity, history, trust | v1 | U | — |  |  |  |  |  | PAY-E1..E8 · isolation | none |
| VID-11 | §31.5 Viewer identity, history, trust | v1·G | B | — |  |  |  |  |  | PAY-E1..E8 · isolation | release |
| VID-21 | §31.5 Viewer identity, history, trust | v1·G | B | P1 |  |  |  |  |  | PAY-E1..E8 · isolation | release |
| VID-22 | §31.5 Viewer identity, history, trust | v1·G | A | P1 |  |  |  |  |  | PAY-E1..E8 · isolation | release |
| VID-12 | §31.5 Viewer identity, history, trust | v1·G | A | P1 |  |  |  |  |  | PAY-E1..E8 · isolation | release |
| VID-13 | §31.5 Viewer identity, history, trust | v1·G | X | P1 |  |  |  |  |  | PAY-E1..E8 · isolation | release |
| VID-14 | §31.5 Viewer identity, history, trust | v1 | A | P1 |  |  |  |  |  | PAY-E1..E8 · isolation | release |
| VID-15 | §31.5 Viewer identity, history, trust | v1 | A | P1 |  |  |  |  |  | PAY-E1..E8 · isolation | release |
| VID-16 | §31.5 Viewer identity, history, trust | v1 | A | P1 |  |  |  |  |  | PAY-E1..E8 · isolation | release |
| VID-17 | §31.5 Viewer identity, history, trust | v1 | A | P1 |  |  |  |  |  | PAY-E1..E8 · isolation | release |
| VID-18 | §31.5 Viewer identity, history, trust | v1 | A | P1 |  |  |  |  |  | PAY-E1..E8 · isolation | release |
| VID-19 | §31.5 Viewer identity, history, trust | P2 | A | P0 |  |  |  |  |  | PAY-E1..E8 · isolation | release |
| VID-20 | §31.5 Viewer identity, history, trust | P2 | A | P1 |  |  |  |  |  | PAY-E1..E8 · isolation | release |
| ENG-01 | §31.6 Engagement — interactions, widgets, goals, challenges | v1 | P | P0 |  |  |  |  |  | OVL-E1..E12 · target concurrency · 8h soak · benchmark | release |
| ENG-02 | §31.6 Engagement — interactions, widgets, goals, challenges | v1 | P | P1 |  |  |  |  |  | OVL-E1..E12 · target concurrency · 8h soak · benchmark | release |
| ENG-03 | §31.6 Engagement — interactions, widgets, goals, challenges | v1 | U | — |  |  |  |  |  | OVL-E1..E12 · target concurrency · 8h soak · benchmark | none |
| ENG-04 | §31.6 Engagement — interactions, widgets, goals, challenges | v1 | U | — |  |  |  |  |  | OVL-E1..E12 · target concurrency · 8h soak · benchmark | none |
| ENG-05 | §31.6 Engagement — interactions, widgets, goals, challenges | v1 | U | — |  |  |  |  |  | OVL-E1..E12 · target concurrency · 8h soak · benchmark | none |
| ENG-06 | §31.6 Engagement — interactions, widgets, goals, challenges | v1 | U | — |  |  |  |  |  | OVL-E1..E12 · target concurrency · 8h soak · benchmark | none |
| ENG-07 | §31.6 Engagement — interactions, widgets, goals, challenges | v1 | P | P1 |  |  |  |  |  | OVL-E1..E12 · target concurrency · 8h soak · benchmark | release |
| ENG-08 | §31.6 Engagement — interactions, widgets, goals, challenges | v1 | U | — |  |  |  |  |  | OVL-E1..E12 · target concurrency · 8h soak · benchmark | none |
| ENG-09 | §31.6 Engagement — interactions, widgets, goals, challenges | v1 | A | **P0** |  |  |  |  |  | OVL-E1..E12 · target concurrency · 8h soak · benchmark | release |
| ENG-10 | §31.6 Engagement — interactions, widgets, goals, challenges | v1 | A | P0 |  |  |  |  |  | OVL-E1..E12 · target concurrency · 8h soak · benchmark | release |
| ENG-11 | §31.6 Engagement — interactions, widgets, goals, challenges | v1 | A | P0 |  |  |  |  |  | OVL-E1..E12 · target concurrency · 8h soak · benchmark | release |
| ENG-12 | §31.6 Engagement — interactions, widgets, goals, challenges | v1 | A | P0 |  |  |  |  |  | OVL-E1..E12 · target concurrency · 8h soak · benchmark | release |
| ENG-13 | §31.6 Engagement — interactions, widgets, goals, challenges | v1 | X | P1 |  |  |  |  |  | OVL-E1..E12 · target concurrency · 8h soak · benchmark | release |
| ENG-14 | §31.6 Engagement — interactions, widgets, goals, challenges | v1·G | X | P1 |  |  |  |  |  | OVL-E1..E12 · target concurrency · 8h soak · benchmark | release |
| ENG-15 | §31.6 Engagement — interactions, widgets, goals, challenges | v1 | P | P2 |  |  |  |  |  | OVL-E1..E12 · target concurrency · 8h soak · benchmark | none |
| ENG-16 | §31.6 Engagement — interactions, widgets, goals, challenges | P2 | U | — |  |  |  |  |  | OVL-E1..E12 · target concurrency · 8h soak · benchmark | none |
| ENG-17 | §31.6 Engagement — interactions, widgets, goals, challenges | v1 | X | P1 |  |  |  |  |  | OVL-E1..E12 · target concurrency · 8h soak · benchmark | release |
| ENG-18 | §31.6 Engagement — interactions, widgets, goals, challenges | v1 | A | P1 |  |  |  |  |  | OVL-E1..E12 · target concurrency · 8h soak · benchmark | release |
| ENG-19 | §31.6 Engagement — interactions, widgets, goals, challenges | v1 | A | P2 |  |  |  |  |  | OVL-E1..E12 · target concurrency · 8h soak · benchmark | none |
| ENG-20 | §31.6 Engagement — interactions, widgets, goals, challenges | v1 | A | P2 |  |  |  |  |  | OVL-E1..E12 · target concurrency · 8h soak · benchmark | none |
| ENG-21 | §31.6 Engagement — interactions, widgets, goals, challenges | v1 | A | P1 |  |  |  |  |  | OVL-E1..E12 · target concurrency · 8h soak · benchmark | release |
| ENG-22 | §31.6 Engagement — interactions, widgets, goals, challenges | v1 | A | P2 |  |  |  |  |  | OVL-E1..E12 · target concurrency · 8h soak · benchmark | none |
| ENG-23 | §31.6 Engagement — interactions, widgets, goals, challenges | v1 | A | P1 |  |  |  |  |  | OVL-E1..E12 · target concurrency · 8h soak · benchmark | release |
| ENG-24 | §31.6 Engagement — interactions, widgets, goals, challenges | v1 | A | P2 |  |  |  |  |  | OVL-E1..E12 · target concurrency · 8h soak · benchmark | none |
| CHL-01 | §31.6 Engagement — interactions, widgets, goals, challenges | v1 | U | — |  |  |  |  |  | — | none |
| CHL-02 | §31.6 Engagement — interactions, widgets, goals, challenges | v1·G | U | — |  |  |  |  |  | — | release |
| CHL-03 | §31.6 Engagement — interactions, widgets, goals, challenges | v1 | A | P1 |  |  |  |  |  | — | release |
| CHL-04 | §31.6 Engagement — interactions, widgets, goals, challenges | v1·G | A | P1 |  |  |  |  |  | — | release |
| CHL-05 | §31.6 Engagement — interactions, widgets, goals, challenges | v1 | A | P1 |  |  |  |  |  | — | release |
| CHL-06 | §31.6 Engagement — interactions, widgets, goals, challenges | v1 | A | P2 |  |  |  |  |  | — | none |
| CHL-07 | §31.6 Engagement — interactions, widgets, goals, challenges | v1 | A | P2 |  |  |  |  |  | — | none |
| CHL-08 | §31.6 Engagement — interactions, widgets, goals, challenges | v1 | B | — |  |  |  |  |  | — | none |
| MED-01 | §31.7 Stickers, media, Alert Studio | v1 | U | — |  |  |  |  |  | INT-E4 · asset serving · takedown drill | none |
| MED-02 | §31.7 Stickers, media, Alert Studio | v1·G | U | — |  |  |  |  |  | INT-E4 · asset serving · takedown drill | release |
| MED-03 | §31.7 Stickers, media, Alert Studio | v1 | U | — |  |  |  |  |  | INT-E4 · asset serving · takedown drill | none |
| MED-04 | §31.7 Stickers, media, Alert Studio | v1 | P | P1 |  |  |  |  |  | INT-E4 · asset serving · takedown drill | release |
| MED-05 | §31.7 Stickers, media, Alert Studio | v1 | X | P1 |  |  |  |  |  | INT-E4 · asset serving · takedown drill | release |
| MED-06 | §31.7 Stickers, media, Alert Studio | v1 | X | **P0** |  |  |  |  |  | INT-E4 · asset serving · takedown drill | release |
| MED-07 | §31.7 Stickers, media, Alert Studio | v1 | U | — |  |  |  |  |  | INT-E4 · asset serving · takedown drill | none |
| MED-08 | §31.7 Stickers, media, Alert Studio | v1 | U | — |  |  |  |  |  | INT-E4 · asset serving · takedown drill | none |
| MED-09 | §31.7 Stickers, media, Alert Studio | v1 | X | P1 |  |  |  |  |  | INT-E4 · asset serving · takedown drill | release |
| MED-10 | §31.7 Stickers, media, Alert Studio | v1 | A | P1 |  |  |  |  |  | INT-E4 · asset serving · takedown drill | release |
| MED-11 | §31.7 Stickers, media, Alert Studio | v1 | U | — |  |  |  |  |  | INT-E4 · asset serving · takedown drill | none |
| MED-12 | §31.7 Stickers, media, Alert Studio | v1 | U | — |  |  |  |  |  | INT-E4 · asset serving · takedown drill | none |
| MED-13 | §31.7 Stickers, media, Alert Studio | v1·G | A | P1 |  |  |  |  |  | INT-E4 · asset serving · takedown drill | release |
| MED-14 | §31.7 Stickers, media, Alert Studio | v1 | A | P1 |  |  |  |  |  | INT-E4 · asset serving · takedown drill | release |
| MED-15 | §31.7 Stickers, media, Alert Studio | v1 | A | P2 |  |  |  |  |  | INT-E4 · asset serving · takedown drill | none |
| MED-22 | §31.7 Stickers, media, Alert Studio | v1 | A | P2 |  |  |  |  |  | INT-E4 · asset serving · takedown drill | none |
| MED-23 | §31.7 Stickers, media, Alert Studio | v1 | A | P2 |  |  |  |  |  | INT-E4 · asset serving · takedown drill | none |
| MED-24 | §31.7 Stickers, media, Alert Studio | v1·G | A | P2 |  |  |  |  |  | INT-E4 · asset serving · takedown drill | release |
| MED-25 | §31.7 Stickers, media, Alert Studio | v1 | A | P2 |  |  |  |  |  | INT-E4 · asset serving · takedown drill | none |
| MED-26 | §31.7 Stickers, media, Alert Studio | v1·G | A | P2 |  |  |  |  |  | INT-E4 · asset serving · takedown drill | release |
| MED-27 | §31.7 Stickers, media, Alert Studio | v1 | A | P2 |  |  |  |  |  | INT-E4 · asset serving · takedown drill | none |
| MED-16 | §31.7 Stickers, media, Alert Studio | v1 | A | P2 |  |  |  |  |  | INT-E4 · asset serving · takedown drill | none |
| MED-17 | §31.7 Stickers, media, Alert Studio | v1 | P | P2 |  |  |  |  |  | INT-E4 · asset serving · takedown drill | none |
| MED-18 | §31.7 Stickers, media, Alert Studio | v1 | P | P2 |  |  |  |  |  | INT-E4 · asset serving · takedown drill | none |
| MED-19 | §31.7 Stickers, media, Alert Studio | v1 | A | P2 |  |  |  |  |  | INT-E4 · asset serving · takedown drill | none |
| MED-20 | §31.7 Stickers, media, Alert Studio | v1 | A | P2 |  |  |  |  |  | INT-E4 · asset serving · takedown drill | none |
| MED-21 | §31.7 Stickers, media, Alert Studio | v1 | U | — |  |  |  |  |  | INT-E4 · asset serving · takedown drill | none |
| CMP-01 | §31.8 Companion | v1 | U | — |  |  |  |  |  | CMP-E1..E8 both platforms · localisation · crash-free gate | none |
| CMP-02 | §31.8 Companion | v1 | U | — |  |  |  |  |  | CMP-E1..E8 both platforms · localisation · crash-free gate | none |
| CMP-03 | §31.8 Companion | v1 | U | — |  |  |  |  |  | CMP-E1..E8 both platforms · localisation · crash-free gate | none |
| CMP-04 | §31.8 Companion | v1 | U | — |  |  |  |  |  | CMP-E1..E8 both platforms · localisation · crash-free gate | none |
| CMP-05 | §31.8 Companion | v1 | U | — |  |  |  |  |  | CMP-E1..E8 both platforms · localisation · crash-free gate | none |
| CMP-06 | §31.8 Companion | v1 | U | — |  |  |  |  |  | CMP-E1..E8 both platforms · localisation · crash-free gate | none |
| CMP-07 | §31.8 Companion | v1 | X | **P0** |  |  |  |  |  | CMP-E1..E8 both platforms · localisation · crash-free gate | release |
| CMP-08 | §31.8 Companion | v1 | U | — |  |  |  |  |  | CMP-E1..E8 both platforms · localisation · crash-free gate | none |
| CMP-09 | §31.8 Companion | v1 | B | — |  |  |  |  |  | CMP-E1..E8 both platforms · localisation · crash-free gate | none |
| CMP-10 | §31.8 Companion | v1 | B | — |  |  |  |  |  | CMP-E1..E8 both platforms · localisation · crash-free gate | none |
| CMP-11 | §31.8 Companion | v1 | B | — |  |  |  |  |  | CMP-E1..E8 both platforms · localisation · crash-free gate | none |
| CMP-12 | §31.8 Companion | v1 | A | P1 |  |  |  |  |  | CMP-E1..E8 both platforms · localisation · crash-free gate | release |
| CMP-36 | §31.8 Companion | v1 | A | P1 |  |  |  |  |  | CMP-E1..E8 both platforms · localisation · crash-free gate | release |
| CMP-37 | §31.8 Companion | v1 | P | P1 |  |  |  |  |  | CMP-E1..E8 both platforms · localisation · crash-free gate | release |
| CMP-13 | §31.8 Companion | v1 | P | P0 |  |  |  |  |  | CMP-E1..E8 both platforms · localisation · crash-free gate | release |
| CMP-14 | §31.8 Companion | v1 | A | P0 |  |  |  |  |  | CMP-E1..E8 both platforms · localisation · crash-free gate | release |
| CMP-15 | §31.8 Companion | v1 | P | P0 |  |  |  |  |  | CMP-E1..E8 both platforms · localisation · crash-free gate | release |
| CMP-16 | §31.8 Companion | v1 | A | P0 |  |  |  |  |  | CMP-E1..E8 both platforms · localisation · crash-free gate | release |
| CMP-17 | §31.8 Companion | v1 | A | P0 |  |  |  |  |  | CMP-E1..E8 both platforms · localisation · crash-free gate | release |
| CMP-18 | §31.8 Companion | v1 | A | P1 |  |  |  |  |  | CMP-E1..E8 both platforms · localisation · crash-free gate | release |
| CMP-19 | §31.8 Companion | v1 | A | P1 |  |  |  |  |  | CMP-E1..E8 both platforms · localisation · crash-free gate | release |
| CMP-20 | §31.8 Companion | v1 | A | P1 |  |  |  |  |  | CMP-E1..E8 both platforms · localisation · crash-free gate | release |
| CMP-21 | §31.8 Companion | v1 | A | P1 |  |  |  |  |  | CMP-E1..E8 both platforms · localisation · crash-free gate | release |
| CMP-22 | §31.8 Companion | v1 | A | P1 |  |  |  |  |  | CMP-E1..E8 both platforms · localisation · crash-free gate | release |
| CMP-23 | §31.8 Companion | v1 | P | P1 |  |  |  |  |  | CMP-E1..E8 both platforms · localisation · crash-free gate | release |
| CMP-24 | §31.8 Companion | v1 | A | P1 |  |  |  |  |  | CMP-E1..E8 both platforms · localisation · crash-free gate | release |
| CMP-25 | §31.8 Companion | v1 | P | P1 |  |  |  |  |  | CMP-E1..E8 both platforms · localisation · crash-free gate | release |
| CMP-26 | §31.8 Companion | v1 | U | — |  |  |  |  |  | CMP-E1..E8 both platforms · localisation · crash-free gate | none |
| CMP-27 | §31.8 Companion | v1 | A | P2 |  |  |  |  |  | CMP-E1..E8 both platforms · localisation · crash-free gate | none |
| CMP-28 | §31.8 Companion | v1 | A | P2 |  |  |  |  |  | CMP-E1..E8 both platforms · localisation · crash-free gate | none |
| CMP-29 | §31.8 Companion | v1 | P | P1 |  |  |  |  |  | CMP-E1..E8 both platforms · localisation · crash-free gate | release |
| CMP-30 | §31.8 Companion | v1 | A | P1 |  |  |  |  |  | CMP-E1..E8 both platforms · localisation · crash-free gate | release |
| CMP-31 | §31.8 Companion | v1·G | A | P1 |  |  |  |  |  | CMP-E1..E8 both platforms · localisation · crash-free gate | release |
| CMP-32 | §31.8 Companion | v1 | U | — |  |  |  |  |  | CMP-E1..E8 both platforms · localisation · crash-free gate | none |
| CMP-33 | §31.8 Companion | v1 | U | — |  |  |  |  |  | CMP-E1..E8 both platforms · localisation · crash-free gate | none |
| CMP-34 | §31.8 Companion | v1·G | U | — |  |  |  |  |  | CMP-E1..E8 both platforms · localisation · crash-free gate | release |
| CMP-35 | §31.8 Companion | v1 | A | P2 |  |  |  |  |  | CMP-E1..E8 both platforms · localisation · crash-free gate | none |
| CMP-38 | §31.8 Companion | v1 | A | **P0** |  |  |  |  |  | CMP-E1..E8 both platforms · localisation · crash-free gate | release |
| CMP-39 | §31.8 Companion | v1 | A | **P0** |  |  |  |  |  | CMP-E1..E8 both platforms · localisation · crash-free gate | release |
| CMP-40 | §31.8 Companion | v1 | A | **P0** |  |  |  |  |  | CMP-E1..E8 both platforms · localisation · crash-free gate | release |
| CMP-41 | §31.8 Companion | v1 | A | **P0** |  |  |  |  |  | CMP-E1..E8 both platforms · localisation · crash-free gate | release |
| CMP-42 | §31.8 Companion | v1 | A | P1 |  |  |  |  |  | CMP-E1..E8 both platforms · localisation · crash-free gate | release |
| CMP-43 | §31.8 Companion | v1 | A | P1 |  |  |  |  |  | CMP-E1..E8 both platforms · localisation · crash-free gate | release |
| CMP-44 | §31.8 Companion | v1 | A | P1 |  |  |  |  |  | CMP-E1..E8 both platforms · localisation · crash-free gate | release |
| CMP-45 | §31.8 Companion | v1 | A | P1 |  |  |  |  |  | CMP-E1..E8 both platforms · localisation · crash-free gate | release |
| CMP-46 | §31.8 Companion | v1 | A | P2 |  |  |  |  |  | CMP-E1..E8 both platforms · localisation · crash-free gate | none |
| CMP-47 | §31.8 Companion | v1 | A | P3 |  |  |  |  |  | CMP-E1..E8 both platforms · localisation · crash-free gate | none |
| CMP-48 | §31.8 Companion | v1 | A | P3 |  |  |  |  |  | CMP-E1..E8 both platforms · localisation · crash-free gate | none |
| CMP-49 | §31.8 Companion | v1·G | A | **P0** |  |  |  |  |  | CMP-E1..E8 both platforms · localisation · crash-free gate | release |
| CMP-50 | §31.8 Companion | v1 | A | P1 |  |  |  |  |  | CMP-E1..E8 both platforms · localisation · crash-free gate | release |
| CMP-51 | §31.8 Companion | v1 | A | P1 |  |  |  |  |  | CMP-E1..E8 both platforms · localisation · crash-free gate | release |
| CMP-52 | §31.8 Companion | v1 | A | P1 |  |  |  |  |  | CMP-E1..E8 both platforms · localisation · crash-free gate | release |
| CMP-53 | §31.8 Companion | v1 | A | **P0** |  |  |  |  |  | CMP-E1..E8 both platforms · localisation · crash-free gate | release |
| CMP-54 | §31.8 Companion | v1 | A | P2 |  |  |  |  |  | CMP-E1..E8 both platforms · localisation · crash-free gate | none |
| CMP-55 | §31.8 Companion | v1·G | A | **P0** |  |  |  |  |  | CMP-E1..E8 both platforms · localisation · crash-free gate | release |
| CMP-56 | §31.8 Companion | v1 | A | P1 |  |  |  |  |  | CMP-E1..E8 both platforms · localisation · crash-free gate | release |
| CMP-57 | §31.8 Companion | v1 | A | P1 |  |  |  |  |  | CMP-E1..E8 both platforms · localisation · crash-free gate | release |
| CMP-58 | §31.8 Companion | v1 | A | P1 |  |  |  |  |  | CMP-E1..E8 both platforms · localisation · crash-free gate | release |
| CMP-59 | §31.8 Companion | v1 | A | P1 |  |  |  |  |  | CMP-E1..E8 both platforms · localisation · crash-free gate | release |
| CMP-60 | §31.8 Companion | v1 | A | **P0** |  |  |  |  |  | CMP-E1..E8 both platforms · localisation · crash-free gate | release |
| CMP-61 | §31.8 Companion | v1 | A | P1 |  |  |  |  |  | CMP-E1..E8 both platforms · localisation · crash-free gate | release |
| CMP-62 | §31.8 Companion | v1 | A | P1 |  |  |  |  |  | CMP-E1..E8 both platforms · localisation · crash-free gate | release |
| CMP-63 | §31.8 Companion | v1 | A | **P0** |  |  |  |  |  | CMP-E1..E8 both platforms · localisation · crash-free gate | release |
| CMP-64 | §31.8 Companion | v1 | A | P1 |  |  |  |  |  | CMP-E1..E8 both platforms · localisation · crash-free gate | release |
| CMP-94 | §31.8 Companion | v1 | A | P1 |  |  |  |  |  | CMP-E1..E8 both platforms · localisation · crash-free gate | release |
| CMP-95 | §31.8 Companion | v1 | A | P1 |  |  |  |  |  | CMP-E1..E8 both platforms · localisation · crash-free gate | release |
| CMP-96 | §31.8 Companion | v1 | A | P2 |  |  |  |  |  | CMP-E1..E8 both platforms · localisation · crash-free gate | none |
| CMP-65 | §31.8 Companion | v1 | A | P1 |  |  |  |  |  | CMP-E1..E8 both platforms · localisation · crash-free gate | release |
| CMP-66 | §31.8 Companion | v1 | A | P1 |  |  |  |  |  | CMP-E1..E8 both platforms · localisation · crash-free gate | release |
| CMP-67 | §31.8 Companion | v1 | A | P2 |  |  |  |  |  | CMP-E1..E8 both platforms · localisation · crash-free gate | none |
| CMP-68 | §31.8 Companion | v1 | A | P1 |  |  |  |  |  | CMP-E1..E8 both platforms · localisation · crash-free gate | release |
| CMP-69 | §31.8 Companion | v1 | A | P1 |  |  |  |  |  | CMP-E1..E8 both platforms · localisation · crash-free gate | release |
| CMP-70 | §31.8 Companion | v1 | A | P1 |  |  |  |  |  | CMP-E1..E8 both platforms · localisation · crash-free gate | release |
| CMP-71 | §31.8 Companion | v1 | A | P1 |  |  |  |  |  | CMP-E1..E8 both platforms · localisation · crash-free gate | release |
| CMP-72 | §31.8 Companion | v1 | A | **P0** |  |  |  |  |  | CMP-E1..E8 both platforms · localisation · crash-free gate | release |
| CMP-73 | §31.8 Companion | v1 | A | P1 |  |  |  |  |  | CMP-E1..E8 both platforms · localisation · crash-free gate | release |
| CMP-74 | §31.8 Companion | v1 | A | **P0** |  |  |  |  |  | CMP-E1..E8 both platforms · localisation · crash-free gate | release |
| CMP-75 | §31.8 Companion | v1 | A | P1 |  |  |  |  |  | CMP-E1..E8 both platforms · localisation · crash-free gate | release |
| CMP-76 | §31.8 Companion | v1 | A | P1 |  |  |  |  |  | CMP-E1..E8 both platforms · localisation · crash-free gate | release |
| CMP-77 | §31.8 Companion | v1 | A | P1 |  |  |  |  |  | CMP-E1..E8 both platforms · localisation · crash-free gate | release |
| CMP-78 | §31.8 Companion | v1·G | B | **P0** |  |  |  | active/launch/07_BUILD_BOOTSTRAP_AUTHORITY.md |  | CMP-E1..E8 both platforms · localisation · crash-free gate | release |
| CMP-79 | §31.8 Companion | v1 | A | **P0** |  |  |  |  |  | CMP-E1..E8 both platforms · localisation · crash-free gate | release |
| CMP-80 | §31.8 Companion | v1·G | A | **P0** |  |  |  |  |  | CMP-E1..E8 both platforms · localisation · crash-free gate | release |
| CMP-81 | §31.8 Companion | v1 | A | P1 |  |  |  |  |  | CMP-E1..E8 both platforms · localisation · crash-free gate | release |
| CMP-82 | §31.8 Companion | v1 | A | **P0** |  |  |  |  |  | CMP-E1..E8 both platforms · localisation · crash-free gate | release |
| CMP-83 | §31.8 Companion | v1 | A | P1 |  |  |  |  |  | CMP-E1..E8 both platforms · localisation · crash-free gate | release |
| CMP-84 | §31.8 Companion | v1 | A | P1 |  |  |  |  |  | CMP-E1..E8 both platforms · localisation · crash-free gate | release |
| CMP-85 | §31.8 Companion | v1 | A | P1 |  |  |  |  |  | CMP-E1..E8 both platforms · localisation · crash-free gate | release |
| CMP-86 | §31.8 Companion | v1 | A | P1 |  |  |  |  |  | CMP-E1..E8 both platforms · localisation · crash-free gate | release |
| CMP-87 | §31.8 Companion | v1 | A | P2 |  |  |  |  |  | CMP-E1..E8 both platforms · localisation · crash-free gate | none |
| CMP-88 | §31.8 Companion | v1 | A | **P0** |  |  |  |  |  | CMP-E1..E8 both platforms · localisation · crash-free gate | release |
| CMP-89 | §31.8 Companion | v1·G | A | P1 |  |  |  |  |  | CMP-E1..E8 both platforms · localisation · crash-free gate | release |
| CMP-90 | §31.8 Companion | v1 | A | P1 |  |  |  |  |  | CMP-E1..E8 both platforms · localisation · crash-free gate | release |
| CMP-91 | §31.8 Companion | v1 | A | **P0** |  |  |  |  |  | CMP-E1..E8 both platforms · localisation · crash-free gate | release |
| CMP-92 | §31.8 Companion | v1 | A | **P0** |  |  |  |  |  | CMP-E1..E8 both platforms · localisation · crash-free gate | release |
| CMP-93 | §31.8 Companion | v1·G | A | P1 |  |  |  |  |  | CMP-E1..E8 both platforms · localisation · crash-free gate | release |
| CON-01 | §31.9 Connectors and chat | P2·G | U | — | tasks/L15-live-platform-connectors-and-chat-commands.md |  |  |  |  | post-v1 (Phase 4) | release |
| CON-02 | §31.9 Connectors and chat | P2 | X | **P0** |  |  |  |  |  | post-v1 (Phase 4) | release |
| CON-03 | §31.9 Connectors and chat | P2 | A | **P0** |  |  |  |  |  | post-v1 (Phase 4) | release |
| CON-04 | §31.9 Connectors and chat | P2 | U | — |  |  |  |  |  | post-v1 (Phase 4) | none |
| CON-05 | §31.9 Connectors and chat | P2·G | U | — |  |  |  |  |  | post-v1 (Phase 4) | release |
| CON-06 | §31.9 Connectors and chat | P2 | U | — |  |  |  |  |  | post-v1 (Phase 4) | none |
| CON-07 | §31.9 Connectors and chat | P2 | U | — | tasks/L15-live-platform-connectors-and-chat-commands.md |  |  |  |  | post-v1 (Phase 4) | none |
| CON-22 | §31.9 Connectors and chat | P2 | A | P1 |  |  |  |  |  | post-v1 (Phase 4) | release |
| CON-08 | §31.9 Connectors and chat | P2 | B | — |  |  |  |  |  | post-v1 (Phase 4) | none |
| CON-09 | §31.9 Connectors and chat | P2 | U | — |  |  |  |  |  | post-v1 (Phase 4) | none |
| CON-10 | §31.9 Connectors and chat | P2 | A | P1 |  |  |  |  |  | post-v1 (Phase 4) | release |
| CON-11 | §31.9 Connectors and chat | P2 | X | P1 |  |  |  |  |  | post-v1 (Phase 4) | release |
| CON-12 | §31.9 Connectors and chat | P2 | U | — |  |  |  |  |  | post-v1 (Phase 4) | none |
| CON-13 | §31.9 Connectors and chat | P2 | A | P1 |  |  |  |  |  | post-v1 (Phase 4) | release |
| CON-14 | §31.9 Connectors and chat | P2 | A | P1 |  |  |  |  |  | post-v1 (Phase 4) | release |
| CON-15 | §31.9 Connectors and chat | P2 | A | P1 |  |  |  |  |  | post-v1 (Phase 4) | release |
| CON-16 | §31.9 Connectors and chat | P2 | A | P2 |  |  |  |  |  | post-v1 (Phase 4) | none |
| CON-17 | §31.9 Connectors and chat | P2 | A | P1 |  |  |  |  |  | post-v1 (Phase 4) | release |
| CON-18 | §31.9 Connectors and chat | P2 | B | — |  |  |  |  |  | post-v1 (Phase 4) | none |
| CON-19 | §31.9 Connectors and chat | P2 | B | — |  |  |  |  |  | post-v1 (Phase 4) | none |
| CON-20 | §31.9 Connectors and chat | P2 | A | P3 |  |  |  |  |  | post-v1 (Phase 4) | none |
| CON-21 | §31.9 Connectors and chat | P2 | A | P1 |  |  |  |  |  | post-v1 (Phase 4) | release |
| CON-31 | §31.9 Connectors and chat | P2 | A | **P0 rule for Phase 4** |  |  |  |  |  | post-v1 (Phase 4) | release |
| CON-32 | §31.9 Connectors and chat | P2·G | A | P2 |  |  |  |  |  | post-v1 (Phase 4) | release |
| CON-33 | §31.9 Connectors and chat | P2·G | A | P2 |  |  |  |  |  | post-v1 (Phase 4) | release |
| CON-34 | §31.9 Connectors and chat | P2 | A | P1 |  |  |  |  |  | post-v1 (Phase 4) | release |
| CON-35 | §31.9 Connectors and chat | P2 | A | P1 |  |  |  |  |  | post-v1 (Phase 4) | release |
| CON-36 | §31.9 Connectors and chat | P2·G | A | **P0 for Phase 4** |  |  |  |  |  | post-v1 (Phase 4) | release |
| CON-37 | §31.9 Connectors and chat | P2·G | A | **P0 for Phase 4** |  |  |  |  |  | post-v1 (Phase 4) | release |
| CON-38 | §31.9 Connectors and chat | P2·G | A | P2 |  |  |  |  |  | post-v1 (Phase 4) | release |
| CON-40 | §31.9 Connectors and chat | P2 | A | **P0 for Phase 4** |  |  |  |  |  | post-v1 (Phase 4) | release |
| CON-41 | §31.9 Connectors and chat | P2 | A | P1 |  |  |  |  |  | post-v1 (Phase 4) | release |
| CON-42 | §31.9 Connectors and chat | P2 | A | P1 |  |  |  |  |  | post-v1 (Phase 4) | release |
| CON-43 | §31.9 Connectors and chat | P2 | A | **P0 for Phase 4** |  |  |  |  |  | post-v1 (Phase 4) | release |
| CON-44 | §31.9 Connectors and chat | P2 | A | P1 |  |  |  |  |  | post-v1 (Phase 4) | release |
| CON-45 | §31.9 Connectors and chat | P2 | A | P1 |  |  |  |  |  | post-v1 (Phase 4) | release |
| CON-46 | §31.9 Connectors and chat | P2 | A | **P0 for Phase 4** |  |  |  |  |  | post-v1 (Phase 4) | release |
| CON-47 | §31.9 Connectors and chat | P2 | A | **P0 for Phase 4** |  |  |  |  |  | post-v1 (Phase 4) | release |
| CON-48 | §31.9 Connectors and chat | P2 | A | P1 |  |  |  |  |  | post-v1 (Phase 4) | release |
| CON-49 | §31.9 Connectors and chat | P2 | A | P1 |  |  |  |  |  | post-v1 (Phase 4) | release |
| CON-39 | §31.9 Connectors and chat | N | N | — |  |  |  |  |  | post-v1 (Phase 4) | none |
| ENT-01 | §31.10 Entitlements, billing, admin, ops | v1 | U | — |  |  |  |  |  | LIF-E1..E3 · isolation | none |
| ENT-02 | §31.10 Entitlements, billing, admin, ops | v1 | U | — |  |  |  |  |  | LIF-E1..E3 · isolation | none |
| ENT-03 | §31.10 Entitlements, billing, admin, ops | v1 | X | P1 |  |  |  |  |  | LIF-E1..E3 · isolation | release |
| ENT-04 | §31.10 Entitlements, billing, admin, ops | v1·G | P | P1 |  |  |  |  |  | LIF-E1..E3 · isolation | release |
| ENT-05 | §31.10 Entitlements, billing, admin, ops | v1 | U | — |  |  |  |  |  | LIF-E1..E3 · isolation | none |
| ENT-06 | §31.10 Entitlements, billing, admin, ops | v1 | U | — |  |  |  |  |  | LIF-E1..E3 · isolation | none |
| ENT-07 | §31.10 Entitlements, billing, admin, ops | v1 | U | — |  |  |  |  |  | LIF-E1..E3 · isolation | none |
| ENT-08 | §31.10 Entitlements, billing, admin, ops | v1 | A | P1 |  |  |  |  |  | LIF-E1..E3 · isolation | release |
| ENT-09 | §31.10 Entitlements, billing, admin, ops | v1 | A | P1 |  |  |  |  |  | LIF-E1..E3 · isolation | release |
| ADM-01 | §31.10 Entitlements, billing, admin, ops | v1 | U | — |  |  |  |  |  | DSH-E1..E5 · LIF-E4..E6 · isolation | none |
| ADM-02 | §31.10 Entitlements, billing, admin, ops | v1 | U | — |  |  |  |  |  | DSH-E1..E5 · LIF-E4..E6 · isolation | none |
| ADM-03 | §31.10 Entitlements, billing, admin, ops | v1 | U | — |  |  |  |  |  | DSH-E1..E5 · LIF-E4..E6 · isolation | none |
| ADM-04 | §31.10 Entitlements, billing, admin, ops | v1 | P | P2 |  |  |  |  |  | DSH-E1..E5 · LIF-E4..E6 · isolation | none |
| ADM-05 | §31.10 Entitlements, billing, admin, ops | v1 | X | P0 |  |  |  |  |  | DSH-E1..E5 · LIF-E4..E6 · isolation | release |
| ADM-06 | §31.10 Entitlements, billing, admin, ops | v1 | X | P1 |  |  |  |  |  | DSH-E1..E5 · LIF-E4..E6 · isolation | release |
| ADM-07 | §31.10 Entitlements, billing, admin, ops | v1 | A | P0 |  |  |  |  |  | DSH-E1..E5 · LIF-E4..E6 · isolation | release |
| ADM-08 | §31.10 Entitlements, billing, admin, ops | v1 | U | — |  |  |  |  |  | DSH-E1..E5 · LIF-E4..E6 · isolation | none |
| ADM-09 | §31.10 Entitlements, billing, admin, ops | v1 | U | — |  |  |  |  |  | DSH-E1..E5 · LIF-E4..E6 · isolation | none |
| OPS-01 | §31.10 Entitlements, billing, admin, ops | v1 | U | — |  |  |  |  |  | — | none |
| OPS-02 | §31.10 Entitlements, billing, admin, ops | v1 | X | **P0** |  |  |  |  |  | — | release |
| OPS-03 | §31.10 Entitlements, billing, admin, ops | v1 | U | — |  |  |  |  |  | — | none |
| OPS-04 | §31.10 Entitlements, billing, admin, ops | v1·G | B | — |  |  |  |  |  | — | release |
| OPS-05 | §31.10 Entitlements, billing, admin, ops | v1·G | U | — |  |  |  |  |  | — | release |
| OPS-06 | §31.10 Entitlements, billing, admin, ops | v1 | U | — |  |  |  |  |  | — | none |
| OPS-07 | §31.10 Entitlements, billing, admin, ops | v1 | A | P0 |  |  |  |  |  | — | release |
| OPS-08 | §31.10 Entitlements, billing, admin, ops | v1 | A | P0 |  |  |  |  |  | — | release |
| OPS-09 | §31.10 Entitlements, billing, admin, ops | v1 | P | P0 |  |  |  |  |  | — | release |
| OPS-10 | §31.10 Entitlements, billing, admin, ops | v1 | A | P0 |  |  |  |  |  | — | release |
| OPS-11 | §31.10 Entitlements, billing, admin, ops | v1 | A | P0 |  |  |  |  |  | — | release |
| OPS-12 | §31.10 Entitlements, billing, admin, ops | v1 | U | — |  |  |  |  |  | — | none |
| OPS-13 | §31.10 Entitlements, billing, admin, ops | v1 | U | — |  |  |  |  |  | — | none |
| OPS-14 | §31.10 Entitlements, billing, admin, ops | v1 | B | — |  |  |  |  |  | — | none |
| OPS-15 | §31.10 Entitlements, billing, admin, ops | v1 | U | — |  |  |  |  |  | — | none |
| MKT-01 | §31.11 Marketing, legal, support | v1 | U | — |  |  |  |  |  | — | none |
| MKT-02 | §31.11 Marketing, legal, support | v1·G | U | — |  |  |  |  |  | — | release |
| MKT-03 | §31.11 Marketing, legal, support | v1 | U | — |  |  |  |  |  | — | none |
| MKT-04 | §31.11 Marketing, legal, support | v1 | U | — |  |  |  |  | L10 | — | none |
| MKT-05 | §31.11 Marketing, legal, support | v1 | A | P1 |  |  |  |  |  | — | release |
| MKT-06 | §31.11 Marketing, legal, support | v1 | A | P2 |  |  |  |  |  | — | none |
| MKT-07 | §31.11 Marketing, legal, support | v1·G | B | — |  |  |  |  |  | — | release |
| MKT-08 | §31.11 Marketing, legal, support | v1 | A | P0 |  |  |  |  |  | — | release |
| MKT-09 | §31.11 Marketing, legal, support | v1 | U | — |  |  |  |  |  | — | none |
| HUB-01 | §31.13 Live Support Hub | v1 | P | P0 |  |  |  |  |  | HUB-E1..E5 · 3G profile · accessibility | release |
| HUB-02 | §31.13 Live Support Hub | v1 | A | P0 |  |  |  |  |  | HUB-E1..E5 · 3G profile · accessibility | release |
| HUB-03 | §31.13 Live Support Hub | v1 | A | P0 |  |  |  |  |  | HUB-E1..E5 · 3G profile · accessibility | release |
| HUB-04 | §31.13 Live Support Hub | v1 | A | P0 |  |  |  |  |  | HUB-E1..E5 · 3G profile · accessibility | release |
| HUB-05 | §31.13 Live Support Hub | v1 | X | P0 |  |  |  |  |  | HUB-E1..E5 · 3G profile · accessibility | release |
| HUB-06 | §31.13 Live Support Hub | v1 | A | P1 |  |  |  |  |  | HUB-E1..E5 · 3G profile · accessibility | release |
| HUB-07 | §31.13 Live Support Hub | v1 | A | P1 |  |  |  |  |  | HUB-E1..E5 · 3G profile · accessibility | release |
| HUB-08 | §31.13 Live Support Hub | v1 | P | P1 |  |  |  |  |  | HUB-E1..E5 · 3G profile · accessibility | release |
| HUB-09 | §31.13 Live Support Hub | P2 | A | P1 |  |  |  |  |  | HUB-E1..E5 · 3G profile · accessibility | release |
| HUB-10 | §31.13 Live Support Hub | v1 | A | P1 |  |  |  |  |  | HUB-E1..E5 · 3G profile · accessibility | release |
| HUB-11 | §31.13 Live Support Hub | v1 | A | P1 |  |  |  |  |  | HUB-E1..E5 · 3G profile · accessibility | release |
| HUB-12 | §31.13 Live Support Hub | v1 | A | P2 |  |  |  |  |  | HUB-E1..E5 · 3G profile · accessibility | none |
| HUB-13 | §31.13 Live Support Hub | P2 | A | P2 |  |  |  |  |  | HUB-E1..E5 · 3G profile · accessibility | none |
| HUB-14 | §31.13 Live Support Hub | v1 | A | P1 |  |  |  |  |  | HUB-E1..E5 · 3G profile · accessibility | release |
| HUB-15 | §31.13 Live Support Hub | v1 | A | P1 |  |  |  |  |  | HUB-E1..E5 · 3G profile · accessibility | release |
| HUB-16 | §31.13 Live Support Hub | v1 | A | P1 |  |  |  |  |  | HUB-E1..E5 · 3G profile · accessibility | release |
| HUB-17 | §31.13 Live Support Hub | v1 | A | P1 |  |  |  |  |  | HUB-E1..E5 · 3G profile · accessibility | release |
| HUB-18 | §31.13 Live Support Hub | v1 | P | P1 |  |  |  |  |  | HUB-E1..E5 · 3G profile · accessibility | release |
| HUB-19 | §31.13 Live Support Hub | v1 | P | P0 |  |  |  |  |  | HUB-E1..E5 · 3G profile · accessibility | release |
| HUB-20 | §31.13 Live Support Hub | v1 | A | P2 |  |  |  |  |  | HUB-E1..E5 · 3G profile · accessibility | none |
| HUB-21 | §31.13 Live Support Hub | v1 | A | P2 |  |  |  |  |  | HUB-E1..E5 · 3G profile · accessibility | none |
| HUB-22 | §31.13 Live Support Hub | v1 | A | P2 |  |  |  |  |  | HUB-E1..E5 · 3G profile · accessibility | none |
| HUB-23 | §31.13 Live Support Hub | v1 | A | P1 |  |  |  |  |  | HUB-E1..E5 · 3G profile · accessibility | release |
| DSH-10 | §31.13 Live Support Hub | v1 | A | **P0** |  |  |  |  |  | DSH-E1..E5 · isolation · role boundaries | release |
| DSH-11 | §31.13 Live Support Hub | v1 | A | **P0** |  |  |  |  |  | DSH-E1..E5 · isolation · role boundaries | release |
| DSH-12 | §31.13 Live Support Hub | v1 | A | **P0** |  |  |  |  |  | DSH-E1..E5 · isolation · role boundaries | release |
| DSH-13 | §31.13 Live Support Hub | v1 | A | P1 |  |  |  |  |  | DSH-E1..E5 · isolation · role boundaries | release |
| DSH-14 | §31.13 Live Support Hub | v1 | A | **P0** |  |  |  |  |  | DSH-E1..E5 · isolation · role boundaries | release |
| DSH-15 | §31.13 Live Support Hub | v1 | A | **P0** |  |  |  |  |  | DSH-E1..E5 · isolation · role boundaries | release |
| DSH-16 | §31.13 Live Support Hub | v1 | A | P1 |  |  |  |  |  | DSH-E1..E5 · isolation · role boundaries | release |
| DSH-17 | §31.13 Live Support Hub | v1 | A | **P0** |  |  |  |  |  | DSH-E1..E5 · isolation · role boundaries | release |
| DSH-18 | §31.13 Live Support Hub | v1 | A | P1 |  |  |  |  |  | DSH-E1..E5 · isolation · role boundaries | release |
| DSH-19 | §31.13 Live Support Hub | v1 | A | P1 |  |  |  |  |  | DSH-E1..E5 · isolation · role boundaries | release |
| DSH-20 | §31.13 Live Support Hub | v1 | A | P1 |  |  |  |  |  | DSH-E1..E5 · isolation · role boundaries | release |
| DSH-21 | §31.13 Live Support Hub | v1 | A | P2 |  |  |  |  |  | DSH-E1..E5 · isolation · role boundaries | none |
| DSH-22 | §31.13 Live Support Hub | v1 | A | P1 |  |  |  |  |  | DSH-E1..E5 · isolation · role boundaries | release |
| DSH-23 | §31.13 Live Support Hub | v1 | A | P1 |  |  |  |  |  | DSH-E1..E5 · isolation · role boundaries | release |
| DSH-24 | §31.13 Live Support Hub | v1 | A | P2 |  |  |  |  |  | DSH-E1..E5 · isolation · role boundaries | none |
| DSH-25 | §31.13 Live Support Hub | v1 | A | **P0** |  |  |  |  |  | DSH-E1..E5 · isolation · role boundaries | release |
| DSH-26 | §31.13 Live Support Hub | v1 | A | **P0** |  |  |  |  |  | DSH-E1..E5 · isolation · role boundaries | release |
| DSH-27 | §31.13 Live Support Hub | v1 | A | P1 |  |  |  |  |  | DSH-E1..E5 · isolation · role boundaries | release |
| DSH-28 | §31.13 Live Support Hub | v1 | A | P1 |  |  |  |  |  | DSH-E1..E5 · isolation · role boundaries | release |
| DSH-29 | §31.13 Live Support Hub | v1 | A | P2 |  |  |  |  |  | DSH-E1..E5 · isolation · role boundaries | none |
| DSH-30 | §31.13 Live Support Hub | v1 | A | **P0** |  |  |  |  |  | DSH-E1..E5 · isolation · role boundaries | release |
| DSH-31 | §31.13 Live Support Hub | v1 | A | **P0** |  |  |  |  |  | DSH-E1..E5 · isolation · role boundaries | release |
| SAF-01 | §31.13 Live Support Hub | v1 | A | **P0** |  |  |  |  |  | — | release |
| SAF-02 | §31.13 Live Support Hub | v1 | A | **P0** |  |  |  |  |  | — | release |
| SAF-03 | §31.13 Live Support Hub | v1 | A | **P0** |  |  |  |  |  | — | release |
| SAF-04 | §31.13 Live Support Hub | v1 | A | **P0** |  |  |  |  |  | — | release |
| SAF-05 | §31.13 Live Support Hub | v1 | A | **P0** |  |  |  |  |  | — | release |
| SAF-06 | §31.13 Live Support Hub | v1 | A | P1 |  |  |  |  |  | — | release |
| SAF-07 | §31.13 Live Support Hub | v1 | A | P1 |  |  |  |  |  | — | release |
| SAF-08 | §31.13 Live Support Hub | v1 | A | P1 |  |  |  |  |  | — | release |
| SAF-09 | §31.13 Live Support Hub | v1 | A | **P0** |  |  |  |  |  | — | release |
| SAF-10 | §31.13 Live Support Hub | v1 | A | **P0** |  |  |  |  |  | — | release |
| SAF-11 | §31.13 Live Support Hub | v1 | A | **P0** |  |  |  |  |  | — | release |
| SAF-12 | §31.13 Live Support Hub | v1 | A | **P0** |  |  |  |  |  | — | release |
| SAF-13 | §31.13 Live Support Hub | v1 | A | P1 |  |  |  |  |  | — | release |
| SAF-14 | §31.13 Live Support Hub | v1 | A | P1 |  |  |  |  |  | — | release |
| SAF-15 | §31.13 Live Support Hub | v1 | A | **P0** |  |  |  |  |  | — | release |
| SAF-16 | §31.13 Live Support Hub | v1 | A | P1 |  |  |  |  |  | — | release |
| SAF-17 | §31.13 Live Support Hub | v1 | A | **P0** |  |  |  |  |  | — | release |
| SAF-18 | §31.13 Live Support Hub | v1 | A | **P0** |  |  |  |  |  | — | release |
| SAF-19 | §31.13 Live Support Hub | v1 | A | P1 |  |  |  |  |  | — | release |
| SAF-20 | §31.13 Live Support Hub | v1 | A | P1 |  |  |  |  |  | — | release |
| SAF-21 | §31.13 Live Support Hub | v1 | A | **P0** |  |  |  |  |  | — | release |
| SAF-22 | §31.13 Live Support Hub | v1 | A | P1 |  |  |  |  |  | — | release |
| SAF-23 | §31.13 Live Support Hub | v1 | A | P1 |  |  |  |  |  | — | release |
| SAF-24 | §31.13 Live Support Hub | v1 | A | P2 |  |  |  |  |  | — | none |
| SAF-25 | §31.13 Live Support Hub | v1 | A | P2 |  |  |  |  |  | — | none |
| SAF-26 | §31.13 Live Support Hub | v1 | A | P3 |  |  |  |  |  | — | none |
| SAF-27 | §31.13 Live Support Hub | v1 | A | P2 |  |  |  |  |  | — | none |
| SAF-28 | §31.13 Live Support Hub | v1 | A | P1 |  |  |  |  |  | — | release |
| SAF-29 | §31.13 Live Support Hub | v1 | A | P1 |  |  |  |  |  | — | release |
| SAF-31 | §31.13 Live Support Hub | v1 | A | **P0** |  |  |  |  |  | — | release |
| SAF-32 | §31.13 Live Support Hub | v1 | A | **P0** |  |  |  |  |  | — | release |
| SAF-33 | §31.13 Live Support Hub | v1 | A | **P0** |  |  |  |  |  | — | release |
| SAF-34 | §31.13 Live Support Hub | v1 | A | P1 |  |  |  |  |  | — | release |
| SAF-35 | §31.13 Live Support Hub | v1 | A | P2 |  |  |  |  |  | — | none |
| SAF-36 | §31.13 Live Support Hub | v1 | A | P1 |  |  |  |  |  | — | release |
| SAF-37 | §31.13 Live Support Hub | v1 | A | P1 |  |  |  |  |  | — | release |
| SAF-38 | §31.13 Live Support Hub | v1 | A | P1 |  |  |  |  |  | — | release |
| SAF-39 | §31.13 Live Support Hub | v1 | A | **P0** |  |  |  |  |  | — | release |
| SAF-40 | §31.13 Live Support Hub | v1 | A | **P0** |  |  |  |  |  | — | release |
| SAF-41 | §31.13 Live Support Hub | v1 | A | **P0** |  |  |  |  |  | — | release |
| SAF-42 | §31.13 Live Support Hub | v1 | A | **P0** |  |  |  |  |  | — | release |
| SAF-43 | §31.13 Live Support Hub | v1 | A | P1 |  |  |  |  |  | — | release |
| SAF-44 | §31.13 Live Support Hub | v1 | A | P1 |  |  |  |  |  | — | release |
| SAF-45 | §31.13 Live Support Hub | v1 | N | — |  |  |  |  |  | — | none |
| SAF-46 | §31.13 Live Support Hub | v1·G | A | P2 |  |  |  |  |  | — | release |
| REP-01 | §31.13 Live Support Hub | v1 | A | P1 |  |  |  |  |  | — | release |
| REP-02 | §31.13 Live Support Hub | v1 | A | P1 |  |  |  |  |  | — | release |
| REP-03 | §31.13 Live Support Hub | v1 | A | **P0** |  |  |  |  |  | — | release |
| REP-04 | §31.13 Live Support Hub | v1 | A | P2 |  |  |  |  |  | — | none |
| REP-05 | §31.13 Live Support Hub | v1 | A | **P0** |  |  |  |  |  | — | release |
| REF-01 | §31.13 Live Support Hub | v1 | P | **P0** |  |  |  |  |  | — | release |
| REF-02 | §31.13 Live Support Hub | v1·G | A | P1 |  |  |  |  |  | — | release |
| REF-03 | §31.13 Live Support Hub | v1 | N | — |  |  |  |  |  | — | none |
| REF-04 | §31.13 Live Support Hub | v1 | A | **P0** |  |  |  |  |  | — | release |
| REF-05 | §31.13 Live Support Hub | v1 | A | **P0** |  |  |  |  |  | — | release |
| REF-06 | §31.13 Live Support Hub | v1 | A | **P0** |  |  |  |  |  | — | release |
| REF-07 | §31.13 Live Support Hub | v1 | U | — |  |  |  |  |  | — | none |
| REF-08 | §31.13 Live Support Hub | v1 | U | — |  |  |  |  |  | — | none |
| REF-09 | §31.13 Live Support Hub | v1 | A | P1 |  |  |  |  |  | — | release |
| REF-10 | §31.13 Live Support Hub | v1 | A | **P0** |  |  |  |  |  | — | release |
| REF-11 | §31.13 Live Support Hub | v1 | A | P1 |  |  |  |  |  | — | release |
| REF-12 | §31.13 Live Support Hub | v1 | A | **P0** |  |  |  |  |  | — | release |
| REF-13 | §31.13 Live Support Hub | v1·G | A | P1 |  |  |  |  |  | — | release |
| REF-14 | §31.13 Live Support Hub | v1 | A | P2 |  |  |  |  |  | — | none |
| REF-15 | §31.13 Live Support Hub | v1 | A | **P0** |  |  |  |  |  | — | release |
| REF-16 | §31.13 Live Support Hub | v1 | A | P1 |  |  |  |  |  | — | release |
| REF-17 | §31.13 Live Support Hub | v1 | A | P1 |  |  |  |  |  | — | release |
| REF-18 | §31.13 Live Support Hub | v1·G | A | **P0** |  |  |  |  |  | — | release |
| REF-19 | §31.13 Live Support Hub | v1·G | A | P1 |  |  |  |  |  | — | release |
| REF-20 | §31.13 Live Support Hub | v1·G | A | **P0** |  |  |  |  |  | — | release |
| SAF-30 | §31.13 Live Support Hub | v1 | A | P1 |  |  |  |  |  | — | release |
| CUS-01 | §31.14 Customisation and gating | v1 | P | P0 |  |  |  |  |  | DSH-E1..E5 · role-boundary suite | release |
| CUS-02 | §31.14 Customisation and gating | v1 | A | P0 |  |  |  |  |  | DSH-E1..E5 · role-boundary suite | release |
| CUS-03 | §31.14 Customisation and gating | v1 | P | P1 |  |  |  |  |  | DSH-E1..E5 · role-boundary suite | release |
| CUS-04 | §31.14 Customisation and gating | v1 | P | P1 |  |  |  |  |  | DSH-E1..E5 · role-boundary suite | release |
| CUS-05 | §31.14 Customisation and gating | v1 | A | P2 |  |  |  |  |  | DSH-E1..E5 · role-boundary suite | none |
| CUS-06 | §31.14 Customisation and gating | P2 | A | P1 |  |  |  |  |  | DSH-E1..E5 · role-boundary suite | release |
| LOB-01 | §31.15 Lobby Engine | P3 | A | P1 |  |  |  |  |  | — | release |
| LOB-02 | §31.15 Lobby Engine | P3 | A | P1 |  |  |  |  |  | — | release |
| LOB-03 | §31.15 Lobby Engine | P3 | A | P1 |  |  |  |  |  | — | release |
| LOB-04 | §31.15 Lobby Engine | P3 | A | P1 |  |  |  |  |  | — | release |
| LOB-05 | §31.15 Lobby Engine | P3 | A | P1 |  |  |  |  |  | — | release |
| LOB-06 | §31.15 Lobby Engine | P3 | A | P1 |  |  |  |  |  | — | release |
| LOB-07 | §31.15 Lobby Engine | P3 | A | P1 |  |  |  |  |  | — | release |
| LOB-08 | §31.15 Lobby Engine | P3 | A | P1 |  |  |  |  |  | — | release |
| LOB-09 | §31.15 Lobby Engine | P3 | A | P1 |  |  |  |  |  | — | release |
| LOB-10 | §31.15 Lobby Engine | P3 | A | P1 |  |  |  |  |  | — | release |
| LOB-11 | §31.15 Lobby Engine | P3 | A | P1 |  |  |  |  |  | — | release |
| LOB-12 | §31.15 Lobby Engine | P3 | A | P1 |  |  |  |  |  | — | release |
| LOB-13 | §31.15 Lobby Engine | P3 | A | P2 |  |  |  |  |  | — | none |
| LOB-14 | §31.15 Lobby Engine | P3 | A | P2 |  |  |  |  |  | — | none |
| LOB-15 | §31.15 Lobby Engine | P3 | A | P2 |  |  |  |  |  | — | none |
| LOB-16 | §31.15 Lobby Engine | P3 | A | P2 |  |  |  |  |  | — | none |
| LOB-17 | §31.15 Lobby Engine | P3 | A | P2 |  |  |  |  |  | — | none |
| LOB-18 | §31.15 Lobby Engine | P3 | A | P2 |  |  |  |  |  | — | none |
| LOB-19 | §31.15 Lobby Engine | P3 | A | P1 |  |  |  |  |  | — | release |
| LOB-20 | §31.15 Lobby Engine | P3 | A | P3 |  |  |  |  |  | — | none |
| LOB-21 | §31.15 Lobby Engine | P3 | A | P2 |  |  |  |  |  | — | none |
| LOB-22 | §31.15 Lobby Engine | P3 | A | P3 |  |  |  |  |  | — | none |
| LOB-23 | §31.15 Lobby Engine | N | N | — |  |  |  |  |  | — | none |
| GIV-01 | §31.16 Giveaways and tournaments | P3 | A | P1 |  |  |  |  |  | — | release |
| GIV-02 | §31.16 Giveaways and tournaments | P3 | A | P1 |  |  |  |  |  | — | release |
| GIV-03 | §31.16 Giveaways and tournaments | P3 | A | P1 |  |  |  |  |  | — | release |
| GIV-04 | §31.16 Giveaways and tournaments | P3 | A | P1 |  |  |  |  |  | — | release |
| GIV-05 | §31.16 Giveaways and tournaments | P3·G | A | P1 |  |  |  |  |  | — | release |
| GIV-06 | §31.16 Giveaways and tournaments | P3 | A | P1 |  |  |  |  |  | — | release |
| GIV-07 | §31.16 Giveaways and tournaments | P3·G | A | P1 |  |  |  |  |  | — | release |
| TRN-01 | §31.16 Giveaways and tournaments | P3 | A | P2 |  |  |  |  |  | — | none |
| TRN-01b | §31.16 Giveaways and tournaments | P3 | A | P2 |  |  |  |  |  | — | none |
| TRN-02 | §31.16 Giveaways and tournaments | P3 | A | P2 |  |  |  |  |  | — | none |
| TRN-03 | §31.16 Giveaways and tournaments | P3 | A | P2 |  |  |  |  |  | — | none |
| TRN-04 | §31.16 Giveaways and tournaments | P3 | A | P2 |  |  |  |  |  | — | none |
| TRN-05 | §31.16 Giveaways and tournaments | P3 | A | P2 |  |  |  |  |  | — | none |
| TRN-06 | §31.16 Giveaways and tournaments | P3 | A | P2 |  |  |  |  |  | — | none |
| AUD-01 | §31.17 Custom audio and creator media | v1 | A | P1 |  |  |  |  |  | — | release |
| AUD-02 | §31.17 Custom audio and creator media | v1 | A | P1 |  |  |  |  |  | — | release |
| AUD-03 | §31.17 Custom audio and creator media | v1 | A | P1 |  |  |  |  |  | — | release |
| AUD-04 | §31.17 Custom audio and creator media | v1 | A | P1 |  |  |  |  |  | — | release |
| AUD-05 | §31.17 Custom audio and creator media | v1 | A | P2 |  |  |  |  |  | — | none |
| AUD-06 | §31.17 Custom audio and creator media | v1 | A | P1 |  |  |  |  |  | — | release |
| AUD-07 | §31.17 Custom audio and creator media | v1·G | A | P1 |  |  |  |  |  | — | release |
| AUD-08 | §31.17 Custom audio and creator media | v1 | A | P1 |  |  |  |  |  | — | release |
| AUD-09 | §31.17 Custom audio and creator media | v1 | A | P1 |  |  |  |  |  | — | release |
| AUD-10 | §31.17 Custom audio and creator media | v1·G | A | P1 |  |  |  |  |  | — | release |
| AUD-11 | §31.17 Custom audio and creator media | N | N | — |  |  |  |  |  | — | none |
| RT-01 | §31.18 Performance | v1 | X | **P0** |  |  |  |  |  | OVL-E1..E12 · target concurrency · 8h soak · benchmark | release |
| RT-02 | §31.18 Performance | v1 | X | **P0** |  |  |  |  |  | OVL-E1..E12 · target concurrency · 8h soak · benchmark | release |
| RT-03 | §31.18 Performance | v1 | X | **P0** |  |  |  |  |  | OVL-E1..E12 · target concurrency · 8h soak · benchmark | release |
| RT-04 | §31.18 Performance | v1 | X | **P0** |  |  |  |  |  | OVL-E1..E12 · target concurrency · 8h soak · benchmark | release |
| RT-05 | §31.18 Performance | v1 | X | **P0** |  |  |  |  |  | OVL-E1..E12 · target concurrency · 8h soak · benchmark | release |
| RT-06 | §31.18 Performance | v1 | A | **P0** |  |  |  |  |  | OVL-E1..E12 · target concurrency · 8h soak · benchmark | release |
| RT-07 | §31.18 Performance | v1·G | A | **P0** |  |  |  |  |  | OVL-E1..E12 · target concurrency · 8h soak · benchmark | release |
| RT-08 | §31.18 Performance | v1 | X | **P0** |  |  |  |  |  | OVL-E1..E12 · target concurrency · 8h soak · benchmark | release |
| RT-09 | §31.18 Performance | v1 | A | **P0** |  |  |  |  |  | OVL-E1..E12 · target concurrency · 8h soak · benchmark | release |
| RT-10 | §31.18 Performance | v1 | A | **P0** |  |  |  |  |  | OVL-E1..E12 · target concurrency · 8h soak · benchmark | release |
| RT-11 | §31.18 Performance | v1 | A | P1 |  |  |  |  |  | OVL-E1..E12 · target concurrency · 8h soak · benchmark | release |
| RT-12 | §31.18 Performance | v1 | A | **P0** |  |  |  |  |  | OVL-E1..E12 · target concurrency · 8h soak · benchmark | release |
| RT-13 | §31.18 Performance | v1 | A | P1 |  |  |  |  |  | OVL-E1..E12 · target concurrency · 8h soak · benchmark | release |
| PRF-01 | §31.18 Performance | v1 | A | P0 |  |  |  |  |  | OVL-E1..E12 · target concurrency · 8h soak · benchmark | release |
| PRF-02 | §31.18 Performance | v1 | A | P0 |  |  |  |  |  | OVL-E1..E12 · target concurrency · 8h soak · benchmark | release |
| PRF-03 | §31.18 Performance | v1 | P | P0 |  |  |  |  |  | OVL-E1..E12 · target concurrency · 8h soak · benchmark | release |
| PRF-04 | §31.18 Performance | v1 | A | P0 |  |  |  |  |  | OVL-E1..E12 · target concurrency · 8h soak · benchmark | release |
| PRF-05 | §31.18 Performance | v1 | A | P0 |  |  |  |  |  | OVL-E1..E12 · target concurrency · 8h soak · benchmark | release |
| PRF-06 | §31.18 Performance | v1 | A | P0 |  |  |  |  |  | OVL-E1..E12 · target concurrency · 8h soak · benchmark | release |
| PRF-07 | §31.18 Performance | v1 | A | P1 |  |  |  |  |  | OVL-E1..E12 · target concurrency · 8h soak · benchmark | release |
| PRF-08 | §31.18 Performance | v1·G | A | P0 |  |  |  |  |  | OVL-E1..E12 · target concurrency · 8h soak · benchmark | release |
| PRF-09 | §31.18 Performance | v1 | P | P0 |  |  |  |  |  | OVL-E1..E12 · target concurrency · 8h soak · benchmark | release |
| PRF-10 | §31.18 Performance | v1 | P | P1 |  |  |  |  |  | OVL-E1..E12 · target concurrency · 8h soak · benchmark | release |
| PRF-11 | §31.18 Performance | v1 | P | P0 |  |  |  |  |  | OVL-E1..E12 · target concurrency · 8h soak · benchmark | release |
| PRF-12 | §31.18 Performance | v1 | A | P1 |  |  |  |  |  | OVL-E1..E12 · target concurrency · 8h soak · benchmark | release |
| PRF-13 | §31.18 Performance | v1 | U | — |  |  |  |  |  | OVL-E1..E12 · target concurrency · 8h soak · benchmark | none |
| PRF-14 | §31.18 Performance | v1 | A | P1 |  |  |  |  |  | OVL-E1..E12 · target concurrency · 8h soak · benchmark | release |
| PRF-15 | §31.18 Performance | v1 | P | P1 |  |  |  |  |  | OVL-E1..E12 · target concurrency · 8h soak · benchmark | release |
| PRF-16 | §31.18 Performance | v1 | A | P1 |  |  |  |  |  | OVL-E1..E12 · target concurrency · 8h soak · benchmark | release |
| PRF-17 | §31.18 Performance | v1 | A | **P0** |  |  |  |  |  | OVL-E1..E12 · target concurrency · 8h soak · benchmark | release |
| PRF-18 | §31.18 Performance | v1 | A | P1 |  |  |  |  |  | OVL-E1..E12 · target concurrency · 8h soak · benchmark | release |
| PRF-19 | §31.18 Performance | v1 | A | P1 |  |  |  |  |  | OVL-E1..E12 · target concurrency · 8h soak · benchmark | release |
| WMK-01 | §31.18 Performance | v1 | A | **P0** |  |  |  |  |  | OVL-E8..E11 | release |
| WMK-02 | §31.18 Performance | v1 | A | **P0** |  |  |  |  |  | OVL-E8..E11 | release |
| WMK-03 | §31.18 Performance | v1 | A | P1 |  |  |  |  |  | OVL-E8..E11 | release |
| WMK-04 | §31.18 Performance | v1 | A | P1 |  |  |  |  |  | OVL-E8..E11 | release |
| WMK-05 | §31.18 Performance | v1·G | A | **P0** |  |  |  |  |  | OVL-E8..E11 | release |
| WMK-06 | §31.18 Performance | v1 | A | **P0** |  |  |  |  |  | OVL-E8..E11 | release |
| WMK-07 | §31.18 Performance | N | N | — |  |  |  |  |  | OVL-E8..E11 | none |
| CTL-01 | §31.19 Control plane and admin | v1 | A | **P0** |  |  |  |  |  | LIF-E4..E6 · isolation | release |
| CTL-02 | §31.19 Control plane and admin | v1 | A | **P0** |  |  |  |  |  | LIF-E4..E6 · isolation | release |
| CTL-03 | §31.19 Control plane and admin | v1 | A | P0 |  |  |  |  |  | LIF-E4..E6 · isolation | release |
| CTL-04 | §31.19 Control plane and admin | v1 | A | P0 |  |  |  |  |  | LIF-E4..E6 · isolation | release |
| CTL-05 | §31.19 Control plane and admin | v1 | A | P1 |  |  |  |  |  | LIF-E4..E6 · isolation | release |
| CTL-06 | §31.19 Control plane and admin | v1 | A | P1 |  |  |  |  |  | LIF-E4..E6 · isolation | release |
| CTL-07 | §31.19 Control plane and admin | v1 | A | P1 |  |  |  |  |  | LIF-E4..E6 · isolation | release |
| CTL-08 | §31.19 Control plane and admin | v1 | A | P1 |  |  |  |  |  | LIF-E4..E6 · isolation | release |
| ENV-01 | §31.19 Control plane and admin | v1 | A | **P0** |  |  |  |  |  | — | release |
| ENV-02 | §31.19 Control plane and admin | v1 | A | **P0** |  |  |  |  |  | — | release |
| ENV-03 | §31.19 Control plane and admin | v1·G | A | **P0** |  |  |  |  |  | — | release |
| ENV-04 | §31.19 Control plane and admin | v1 | A | **P0** |  |  |  |  |  | — | release |
| ENV-05 | §31.19 Control plane and admin | v1 | A | **P0** |  |  |  |  |  | — | release |
| ENV-06 | §31.19 Control plane and admin | v1 | A | P1 |  |  |  |  |  | — | release |
| ENV-07 | §31.19 Control plane and admin | v1 | A | **P0** |  |  |  |  |  | — | release |
| ENV-08 | §31.19 Control plane and admin | v1 | A | **P0** |  |  |  |  |  | — | release |
| ENV-09 | §31.19 Control plane and admin | v1 | A | **P0** |  |  |  |  |  | — | release |
| CTL-09 | §31.19 Control plane and admin | v1 | A | P0 |  |  |  |  |  | LIF-E4..E6 · isolation | release |
| CTL-14 | §31.19 Control plane and admin | v1 | A | **P0** |  |  |  |  |  | LIF-E4..E6 · isolation | release |
| CTL-15 | §31.19 Control plane and admin | v1 | A | **P0** |  |  |  |  |  | LIF-E4..E6 · isolation | release |
| CTL-10 | §31.19 Control plane and admin | v1 | A | P0 |  |  |  |  |  | LIF-E4..E6 · isolation | release |
| CTL-11 | §31.19 Control plane and admin | v1 | A | P0 |  |  |  |  |  | LIF-E4..E6 · isolation | release |
| CTL-12 | §31.19 Control plane and admin | v1 | A | P1 |  |  |  |  |  | LIF-E4..E6 · isolation | release |
| CTL-13 | §31.19 Control plane and admin | v1 | A | P0 |  |  |  |  |  | LIF-E4..E6 · isolation | release |
| WID-01 | §31.20 New widgets | v1 | A | P1 |  |  |  |  |  | — | release |
| WID-02 | §31.20 New widgets | v1 | A | P2 |  |  |  |  |  | — | none |
| WID-03 | §31.20 New widgets | v1 | A | P1 |  |  |  |  |  | — | release |
| WID-04 | §31.20 New widgets | v1 | A | P2 |  |  |  |  |  | — | none |
| WID-05 | §31.20 New widgets | v1 | A | P2 |  |  |  |  |  | — | none |
| WID-06 | §31.20 New widgets | v1 | A | P2 |  |  |  |  |  | — | none |
| WID-07 | §31.20 New widgets | v1 | A | P2 |  |  |  |  |  | — | none |
| COS-01 | §31.21 Co-Stream Room | P3 | A | P1 |  |  |  |  |  | — | release |
| COS-02 | §31.21 Co-Stream Room | P3 | A | P1 |  |  |  |  |  | — | release |
| COS-03 | §31.21 Co-Stream Room | P3 | A | P1 |  |  |  |  |  | — | release |
| COS-04 | §31.21 Co-Stream Room | P3 | A | P2 |  |  |  |  |  | — | none |
| COS-05 | §31.21 Co-Stream Room | P3 | A | P1 |  |  |  |  |  | — | release |
| COS-06 | §31.21 Co-Stream Room | P3 | A | P1 |  |  |  |  |  | — | release |
| COS-07 | §31.21 Co-Stream Room | P3 | A | P1 |  |  |  |  |  | — | release |
| COS-08 | §31.21 Co-Stream Room | P3 | A | P2 |  |  |  |  |  | — | none |
| COS-09 | §31.21 Co-Stream Room | P3 | A | P1 |  |  |  |  |  | — | release |
| COS-10 | §31.21 Co-Stream Room | P3 | A | P2 |  |  |  |  |  | — | none |
| COS-11 | §31.21 Co-Stream Room | P3 | A | P1 |  |  |  |  |  | — | release |
| COS-12 | §31.21 Co-Stream Room | P3 | A | P1 |  |  |  |  |  | — | release |
| COS-13 | §31.21 Co-Stream Room | P3 | A | P1 |  |  |  |  |  | — | release |
| COS-14 | §31.21 Co-Stream Room | P3 | A | P2 |  |  |  |  |  | — | none |
| COS-15 | §31.21 Co-Stream Room | N | N | — |  |  |  |  |  | — | none |
| SND-01 | §31.22 Sound Moments and Rules Engine | v1 | A | P1 |  |  |  |  |  | — | release |
| SND-02 | §31.22 Sound Moments and Rules Engine | v1 | A | P1 |  |  |  |  |  | — | release |
| SND-03 | §31.22 Sound Moments and Rules Engine | v1 | A | P1 |  |  |  |  |  | — | release |
| SND-04 | §31.22 Sound Moments and Rules Engine | v1 | A | P1 |  |  |  |  |  | — | release |
| SND-05 | §31.22 Sound Moments and Rules Engine | v1 | A | P2 |  |  |  |  |  | — | none |
| SND-06 | §31.22 Sound Moments and Rules Engine | v1 | P | P1 |  |  |  |  |  | — | release |
| SND-07 | §31.22 Sound Moments and Rules Engine | v1 | A | P0 |  |  |  |  |  | — | release |
| RUL-01 | §31.22 Sound Moments and Rules Engine | v1 | A | P1 |  |  |  |  |  | — | release |
| RUL-02 | §31.22 Sound Moments and Rules Engine | v1 | A | P1 |  |  |  |  |  | — | release |
| RUL-03 | §31.22 Sound Moments and Rules Engine | v1 | P | P1 |  |  |  |  |  | — | release |
| SEC-01 | §31.22 Sound Moments and Rules Engine | v1 | A | **P0** |  |  |  |  |  | — | release |
| SEC-02 | §31.22 Sound Moments and Rules Engine | v1 | A | P1 |  |  |  |  |  | — | release |
| SEC-03 | §31.22 Sound Moments and Rules Engine | v1 | P | P1 |  |  |  |  |  | — | release |
| MIG-01 | §31.22 Sound Moments and Rules Engine | v1 | A | P1 |  |  |  |  |  | — | release |
| MIG-02 | §31.22 Sound Moments and Rules Engine | v1 | A | P1 |  |  |  |  |  | — | release |
| MIG-03 | §31.22 Sound Moments and Rules Engine | v1 | A | P0 |  |  |  |  |  | — | release |
| RTE-01 | §31.24 Payment routing | R | A | P1 |  |  |  |  |  | none — phase R or blocked | release |
| RTE-02 | §31.24 Payment routing | R | A | P1 |  |  |  |  |  | none — phase R or blocked | release |
| RTE-03 | §31.24 Payment routing | R | A | P1 |  |  |  |  |  | none — phase R or blocked | release |
| RTE-04 | §31.24 Payment routing | R | A | P1 |  |  |  |  |  | none — phase R or blocked | release |
| RTE-05 | §31.24 Payment routing | R | A | P1 |  |  |  |  |  | none — phase R or blocked | release |
| RTE-06 | §31.24 Payment routing | R | A | P1 |  |  |  |  |  | none — phase R or blocked | release |
| RTE-07 | §31.24 Payment routing | R | A | P1 |  |  |  |  |  | none — phase R or blocked | release |
| RTE-08 | §31.24 Payment routing | R | A | P2 |  |  |  |  |  | none — phase R or blocked | none |
| RTE-09 | §31.24 Payment routing | R | B | P2 |  |  |  |  |  | none — phase R or blocked | none |
| RTE-10 | §31.24 Payment routing | R | B | P3 |  |  |  |  |  | none — phase R or blocked | none |
| RTE-11 | §31.24 Payment routing | R | B | P2 |  |  |  |  |  | none — phase R or blocked | none |
| RTE-12 | §31.24 Payment routing | R | B | P2 |  |  |  |  |  | none — phase R or blocked | none |
| RTE-13 | §31.24 Payment routing | N | N | — |  |  |  |  |  | none — phase R or blocked | none |
| RTE-14 | §31.24 Payment routing | N | N | — |  |  |  |  |  | none — phase R or blocked | none |
| RTE-15 | §31.24 Payment routing | R | A | P2 |  |  |  |  |  | none — phase R or blocked | none |
| RTE-16 | §31.24 Payment routing | R | A | P2 |  |  |  |  |  | none — phase R or blocked | none |
| RTE-17 | §31.24 Payment routing | R | A | P2 |  |  |  |  |  | none — phase R or blocked | none |
| LIF-01 | §31.25 Subscription lifecycle | v1 | A | P1 |  |  |  |  |  | LIF-E1..E3 · DSH-E4 · durable-record access | release |
| LIF-02 | §31.25 Subscription lifecycle | v1 | A | P1 |  |  |  |  |  | LIF-E1..E3 · DSH-E4 · durable-record access | release |
| LIF-03 | §31.25 Subscription lifecycle | v1 | A | P1 |  |  |  |  |  | LIF-E1..E3 · DSH-E4 · durable-record access | release |
| LIF-04 | §31.25 Subscription lifecycle | v1 | A | P1 |  |  |  |  |  | LIF-E1..E3 · DSH-E4 · durable-record access | release |
| LIF-05 | §31.25 Subscription lifecycle | v1 | A | P1 |  |  |  |  |  | LIF-E1..E3 · DSH-E4 · durable-record access | release |
| LIF-06 | §31.25 Subscription lifecycle | v1 | A | **P1** |  |  |  |  |  | LIF-E1..E3 · DSH-E4 · durable-record access | release |
| LIF-07 | §31.25 Subscription lifecycle | v1 | A | P1 |  |  |  |  |  | LIF-E1..E3 · DSH-E4 · durable-record access | release |
| LIF-08 | §31.25 Subscription lifecycle | v1·G | A | P1 |  |  |  |  |  | LIF-E1..E3 · DSH-E4 · durable-record access | release |
| LIF-09 | §31.25 Subscription lifecycle | v1 | A | P2 |  |  |  |  |  | LIF-E1..E3 · DSH-E4 · durable-record access | none |
| LIF-10 | §31.25 Subscription lifecycle | v1 | P | P0 |  |  |  |  |  | LIF-E1..E3 · DSH-E4 · durable-record access | release |
| SOC-01 | §31.26 Social Relay | P3 | A | P2 |  |  |  |  |  | none — phase R or blocked | none |
| SOC-02 | §31.26 Social Relay | P3 | A | P2 |  |  |  |  |  | none — phase R or blocked | none |
| SOC-03 | §31.26 Social Relay | P3 | A | P2 |  |  |  |  |  | none — phase R or blocked | none |
| SOC-04 | §31.26 Social Relay | P3 | A | P2 |  |  |  |  |  | none — phase R or blocked | none |
| SOC-05 | §31.26 Social Relay | P3 | A | P2 |  |  |  |  |  | none — phase R or blocked | none |
| SOC-06 | §31.26 Social Relay | P3 | A | P2 |  |  |  |  |  | none — phase R or blocked | none |
| SOC-07 | §31.26 Social Relay | P3 | A | P2 |  |  |  |  |  | none — phase R or blocked | none |
| SOC-08 | §31.26 Social Relay | P3 | A | P3 |  |  |  |  |  | none — phase R or blocked | none |
| SOC-09 | §31.26 Social Relay | P3 | A | P3 |  |  |  |  |  | none — phase R or blocked | none |
| SOC-10 | §31.26 Social Relay | P3 | A | P3 |  |  |  |  |  | none — phase R or blocked | none |
| SOC-11 | §31.26 Social Relay | P3·G | A | P3 |  |  |  |  |  | none — phase R or blocked | release |
| SOC-12 | §31.26 Social Relay | P3 | A | P3 |  |  |  |  |  | none — phase R or blocked | none |
| SOC-13 | §31.26 Social Relay | P3 | A | P3 |  |  |  |  |  | none — phase R or blocked | none |
| SOC-14 | §31.26 Social Relay | P3·G | A | P2 |  |  |  |  |  | none — phase R or blocked | release |
| SOC-15 | §31.26 Social Relay | P3 | A | P2 |  |  |  |  |  | none — phase R or blocked | none |
| SOC-16 | §31.26 Social Relay | N | N | — |  |  |  |  |  | none — phase R or blocked | none |
| SOC-17 | §31.26 Social Relay | N | N | — |  |  |  |  |  | none — phase R or blocked | none |
| PCK-01 | §31.27 Packs and creator-ops | P3 | A | P2 |  |  |  |  |  | LIF-E1..E3 · DSH-E4 | none |
| PCK-02 | §31.27 Packs and creator-ops | P3 | A | P1 |  |  |  |  |  | LIF-E1..E3 · DSH-E4 | release |
| PCK-03 | §31.27 Packs and creator-ops | P3 | A | P2 |  |  |  |  |  | LIF-E1..E3 · DSH-E4 | none |
| PCK-04 | §31.27 Packs and creator-ops | P3 | A | P2 |  |  |  |  |  | LIF-E1..E3 · DSH-E4 | none |
| PCK-05 | §31.27 Packs and creator-ops | P3 | A | P2 |  |  |  |  |  | LIF-E1..E3 · DSH-E4 | none |
| PCK-06 | §31.27 Packs and creator-ops | P3 | A | P2 |  |  |  |  |  | LIF-E1..E3 · DSH-E4 | none |
| PCK-07 | §31.27 Packs and creator-ops | P3 | A | P2 |  |  |  |  |  | LIF-E1..E3 · DSH-E4 | none |
| PCK-08 | §31.27 Packs and creator-ops | P3 | A | P3 |  |  |  |  |  | LIF-E1..E3 · DSH-E4 | none |
| PCK-09 | §31.27 Packs and creator-ops | P3·G | A | **P1** |  |  |  |  |  | LIF-E1..E3 · DSH-E4 | release |
| PCK-10 | §31.27 Packs and creator-ops | P3 | A | P3 |  |  |  |  |  | LIF-E1..E3 · DSH-E4 | none |
| PCK-11 | §31.27 Packs and creator-ops | P3 | A | P2 |  |  |  |  |  | LIF-E1..E3 · DSH-E4 | none |
| PCK-12 | §31.27 Packs and creator-ops | P3 | A | **P0** |  |  |  |  |  | LIF-E1..E3 · DSH-E4 | release |
| PCK-13 | §31.27 Packs and creator-ops | P3 | A | P2 |  |  |  |  |  | LIF-E1..E3 · DSH-E4 | none |
| PCK-14 | §31.27 Packs and creator-ops | P3·G | A | P2 |  |  |  |  |  | LIF-E1..E3 · DSH-E4 | release |
| PCK-15 | §31.27 Packs and creator-ops | P3 | A | P3 |  |  |  |  |  | LIF-E1..E3 · DSH-E4 | none |
| JOB-01 | §31.27 Packs and creator-ops | P3 | A | P2 |  |  |  |  |  | — | none |
| JOB-02 | §31.27 Packs and creator-ops | P3 | A | P3 |  |  |  |  |  | — | none |
| JOB-03 | §31.27 Packs and creator-ops | P3 | A | P2 |  |  |  |  |  | — | none |
| JOB-04 | §31.27 Packs and creator-ops | P3 | A | P3 |  |  |  |  |  | — | none |
| JOB-05 | §31.27 Packs and creator-ops | P3 | A | P3 |  |  |  |  |  | — | none |
| JOB-06 | §31.27 Packs and creator-ops | P3 | A | P3 |  |  |  |  |  | — | none |
| JOB-07 | §31.27 Packs and creator-ops | P3 | A | P3 |  |  |  |  |  | — | none |
| JOB-08 | §31.27 Packs and creator-ops | P3 | A | P3 |  |  |  |  |  | — | none |
| JOB-09 | §31.27 Packs and creator-ops | P3 | A | P3 |  |  |  |  |  | — | none |
| JOB-10 | §31.27 Packs and creator-ops | N | N | — |  |  |  |  |  | — | none |
| JOB-11 | §31.27 Packs and creator-ops | N | N | — |  |  |  |  |  | — | none |
| INT-01 | §31.28 Interop, packages and bridges (§9) | P2 | A | P2 |  |  |  |  |  | INT-E1..E7 · package fuzz corpus | none |
| INT-02 | §31.28 Interop, packages and bridges (§9) | P2·G | A | P2 |  |  |  |  |  | INT-E1..E7 · package fuzz corpus | release |
| INT-03 | §31.28 Interop, packages and bridges (§9) | P2 | A | P2 |  |  |  |  |  | INT-E1..E7 · package fuzz corpus | none |
| INT-04 | §31.28 Interop, packages and bridges (§9) | P2 | A | P2 |  |  |  |  |  | INT-E1..E7 · package fuzz corpus | none |
| INT-05 | §31.28 Interop, packages and bridges (§9) | P2 | A | P2 |  |  |  |  |  | INT-E1..E7 · package fuzz corpus | none |
| INT-06 | §31.28 Interop, packages and bridges (§9) | P2 | A | P2 |  |  |  |  |  | INT-E1..E7 · package fuzz corpus | none |
| INT-07 | §31.28 Interop, packages and bridges (§9) | P2 | A | P2 |  |  |  |  |  | INT-E1..E7 · package fuzz corpus | none |
| INT-08 | §31.28 Interop, packages and bridges (§9) | P2 | A | P2 |  |  |  |  |  | INT-E1..E7 · package fuzz corpus | none |
| INT-09 | §31.28 Interop, packages and bridges (§9) | P2 | A | P2 |  |  |  |  |  | INT-E1..E7 · package fuzz corpus | none |
| INT-10 | §31.28 Interop, packages and bridges (§9) | P2 | A | P2 |  |  |  |  |  | INT-E1..E7 · package fuzz corpus | none |
| INT-11 | §31.28 Interop, packages and bridges (§9) | P2 | A | **P0 rule, P2 build** |  |  |  |  |  | INT-E1..E7 · package fuzz corpus | release |
| INT-12 | §31.28 Interop, packages and bridges (§9) | P2 | A | P3 |  |  |  |  |  | INT-E1..E7 · package fuzz corpus | none |
| INT-13 | §31.28 Interop, packages and bridges (§9) | P2 | A | P3 |  |  |  |  |  | INT-E1..E7 · package fuzz corpus | none |
| INT-14 | §31.28 Interop, packages and bridges (§9) | P2 | A | P3 |  |  |  |  |  | INT-E1..E7 · package fuzz corpus | none |
| INT-15 | §31.28 Interop, packages and bridges (§9) | P2 | A | P3 |  |  |  |  |  | INT-E1..E7 · package fuzz corpus | none |
| INT-16 | §31.28 Interop, packages and bridges (§9) | P2 | A | P3 |  |  |  |  |  | INT-E1..E7 · package fuzz corpus | none |
| INT-17 | §31.28 Interop, packages and bridges (§9) | R | B | — |  |  |  |  |  | INT-E1..E7 · package fuzz corpus | none |
| INT-18 | §31.28 Interop, packages and bridges (§9) | R | B | — |  |  |  |  |  | INT-E1..E7 · package fuzz corpus | none |
| INT-19 | §31.28 Interop, packages and bridges (§9) | P2 | A | **P0** |  |  |  |  |  | INT-E1..E7 · package fuzz corpus | release |
| INT-20 | §31.28 Interop, packages and bridges (§9) | N | N | — |  |  |  |  |  | INT-E1..E7 · package fuzz corpus | none |
| CST-01 | §31.29 Customisation depth by tier (§15.4) | P2 | A | P1 |  |  |  |  |  | OVL-E1..E12 · HUB-E1..E5 · accessibility · +40% expansion | release |
| CST-02 | §31.29 Customisation depth by tier (§15.4) | P2·G | A | **P0** |  |  |  |  |  | OVL-E1..E12 · HUB-E1..E5 · accessibility · +40% expansion | release |
| CST-03 | §31.29 Customisation depth by tier (§15.4) | P2 | A | P1 |  |  |  |  |  | OVL-E1..E12 · HUB-E1..E5 · accessibility · +40% expansion | release |
| CST-04 | §31.29 Customisation depth by tier (§15.4) | P2 | A | P1 |  |  |  |  |  | OVL-E1..E12 · HUB-E1..E5 · accessibility · +40% expansion | release |
| CST-05 | §31.29 Customisation depth by tier (§15.4) | P2 | A | P1 |  |  |  |  |  | OVL-E1..E12 · HUB-E1..E5 · accessibility · +40% expansion | release |
| CST-06 | §31.29 Customisation depth by tier (§15.4) | P2 | A | P2 |  |  |  |  |  | OVL-E1..E12 · HUB-E1..E5 · accessibility · +40% expansion | none |
| CST-07 | §31.29 Customisation depth by tier (§15.4) | P2 | A | P2 |  |  |  |  |  | OVL-E1..E12 · HUB-E1..E5 · accessibility · +40% expansion | none |
| CST-08 | §31.29 Customisation depth by tier (§15.4) | P2 | A | P2 |  |  |  |  |  | OVL-E1..E12 · HUB-E1..E5 · accessibility · +40% expansion | none |
| CST-09 | §31.29 Customisation depth by tier (§15.4) | P2 | A | P2 |  |  |  |  |  | OVL-E1..E12 · HUB-E1..E5 · accessibility · +40% expansion | none |
| CST-10 | §31.29 Customisation depth by tier (§15.4) | P2 | A | P2 |  |  |  |  |  | OVL-E1..E12 · HUB-E1..E5 · accessibility · +40% expansion | none |
| CST-11 | §31.29 Customisation depth by tier (§15.4) | P2 | A | P1 |  |  |  |  |  | OVL-E1..E12 · HUB-E1..E5 · accessibility · +40% expansion | release |
| CST-12 | §31.29 Customisation depth by tier (§15.4) | P2 | A | P3 |  |  |  |  |  | OVL-E1..E12 · HUB-E1..E5 · accessibility · +40% expansion | none |
| CST-13 | §31.29 Customisation depth by tier (§15.4) | P2 | A | P3 |  |  |  |  |  | OVL-E1..E12 · HUB-E1..E5 · accessibility · +40% expansion | none |
| CST-14 | §31.29 Customisation depth by tier (§15.4) | P2·G | A | P1 |  |  |  |  |  | OVL-E1..E12 · HUB-E1..E5 · accessibility · +40% expansion | release |
| CST-15 | §31.29 Customisation depth by tier (§15.4) | P2 | A | P2 |  |  |  |  |  | OVL-E1..E12 · HUB-E1..E5 · accessibility · +40% expansion | none |
| CST-16 | §31.29 Customisation depth by tier (§15.4) | P2 | A | P3 |  |  |  |  |  | OVL-E1..E12 · HUB-E1..E5 · accessibility · +40% expansion | none |
| CST-17 | §31.29 Customisation depth by tier (§15.4) | P2 | A | P2 |  |  |  |  |  | OVL-E1..E12 · HUB-E1..E5 · accessibility · +40% expansion | none |
| CST-18 | §31.29 Customisation depth by tier (§15.4) | P2 | A | P1 |  |  |  |  |  | OVL-E1..E12 · HUB-E1..E5 · accessibility · +40% expansion | release |
| CST-19 | §31.29 Customisation depth by tier (§15.4) | P2 | A | P2 |  |  |  |  |  | OVL-E1..E12 · HUB-E1..E5 · accessibility · +40% expansion | none |
| CST-20 | §31.29 Customisation depth by tier (§15.4) | P2 | A | P3 |  |  |  |  |  | OVL-E1..E12 · HUB-E1..E5 · accessibility · +40% expansion | none |
| CST-21 | §31.29 Customisation depth by tier (§15.4) | P2 | A | P2 |  |  |  |  |  | OVL-E1..E12 · HUB-E1..E5 · accessibility · +40% expansion | none |
| CST-22 | §31.29 Customisation depth by tier (§15.4) | P2·G | A | P2 |  |  |  |  |  | OVL-E1..E12 · HUB-E1..E5 · accessibility · +40% expansion | release |
| CST-23 | §31.29 Customisation depth by tier (§15.4) | P2 | A | P3 |  |  |  |  |  | OVL-E1..E12 · HUB-E1..E5 · accessibility · +40% expansion | none |
| CST-24 | §31.29 Customisation depth by tier (§15.4) | P2 | A | **P0 rule** |  |  |  |  |  | OVL-E1..E12 · HUB-E1..E5 · accessibility · +40% expansion | release |
| CST-25 | §31.29 Customisation depth by tier (§15.4) | P2 | A | P2 |  |  |  |  |  | OVL-E1..E12 · HUB-E1..E5 · accessibility · +40% expansion | none |
| CST-26 | §31.29 Customisation depth by tier (§15.4) | P2 | A | P1 |  |  |  |  |  | OVL-E1..E12 · HUB-E1..E5 · accessibility · +40% expansion | release |
| CST-27 | §31.29 Customisation depth by tier (§15.4) | P2 | A | P3 |  |  |  |  |  | OVL-E1..E12 · HUB-E1..E5 · accessibility · +40% expansion | none |
| CST-28 | §31.29 Customisation depth by tier (§15.4) | P2 | A | P2 |  |  |  |  |  | OVL-E1..E12 · HUB-E1..E5 · accessibility · +40% expansion | none |
| CST-29 | §31.29 Customisation depth by tier (§15.4) | P2 | A | **P0 rule** |  |  |  |  |  | OVL-E1..E12 · HUB-E1..E5 · accessibility · +40% expansion | release |
| CST-30 | §31.29 Customisation depth by tier (§15.4) | P2 | A | P1 |  |  |  |  |  | OVL-E1..E12 · HUB-E1..E5 · accessibility · +40% expansion | release |
| BOT-01 | §31.30 BharatStudio Bot (§36) | P2 | A | P2 |  |  |  |  |  | BOT-E1..E5 · rate-limit compliance · shared corpus with TTS | none |
| BOT-02 | §31.30 BharatStudio Bot (§36) | P2 | A | P2 |  |  |  |  |  | BOT-E1..E5 · rate-limit compliance · shared corpus with TTS | none |
| BOT-03 | §31.30 BharatStudio Bot (§36) | P2 | A | P2 |  |  |  |  |  | BOT-E1..E5 · rate-limit compliance · shared corpus with TTS | none |
| BOT-04 | §31.30 BharatStudio Bot (§36) | P2 | A | P2 |  |  |  |  |  | BOT-E1..E5 · rate-limit compliance · shared corpus with TTS | none |
| BOT-05 | §31.30 BharatStudio Bot (§36) | P2 | A | P2 |  |  |  |  |  | BOT-E1..E5 · rate-limit compliance · shared corpus with TTS | none |
| BOT-06 | §31.30 BharatStudio Bot (§36) | P2 | A | **P0 with TTS-06** |  |  |  |  |  | BOT-E1..E5 · rate-limit compliance · shared corpus with TTS | release |
| BOT-07 | §31.30 BharatStudio Bot (§36) | P2 | A | P2 |  |  |  |  |  | BOT-E1..E5 · rate-limit compliance · shared corpus with TTS | none |
| BOT-08 | §31.30 BharatStudio Bot (§36) | P2 | A | P2 |  |  |  |  |  | BOT-E1..E5 · rate-limit compliance · shared corpus with TTS | none |
| BOT-09 | §31.30 BharatStudio Bot (§36) | N | N | — |  |  |  |  |  | BOT-E1..E5 · rate-limit compliance · shared corpus with TTS | none |
| BOT-10 | §31.30 BharatStudio Bot (§36) | P2 | A | P3 |  |  |  |  |  | BOT-E1..E5 · rate-limit compliance · shared corpus with TTS | none |
| BOT-11 | §31.30 BharatStudio Bot (§36) | P2 | A | P2 |  |  |  |  |  | BOT-E1..E5 · rate-limit compliance · shared corpus with TTS | none |
| BOT-12 | §31.30 BharatStudio Bot (§36) | P2 | A | P2 |  |  |  |  |  | BOT-E1..E5 · rate-limit compliance · shared corpus with TTS | none |
| BOT-13 | §31.30 BharatStudio Bot (§36) | P2 | A | P3 |  |  |  |  |  | BOT-E1..E5 · rate-limit compliance · shared corpus with TTS | none |
| BOT-14 | §31.30 BharatStudio Bot (§36) | P2 | A | P3 |  |  |  |  |  | BOT-E1..E5 · rate-limit compliance · shared corpus with TTS | none |
| BOT-15 | §31.30 BharatStudio Bot (§36) | P2 | A | P2 |  |  |  |  |  | BOT-E1..E5 · rate-limit compliance · shared corpus with TTS | none |
| BOT-16 | §31.30 BharatStudio Bot (§36) | P2 | A | P2 |  |  |  |  |  | BOT-E1..E5 · rate-limit compliance · shared corpus with TTS | none |
| BOT-17 | §31.30 BharatStudio Bot (§36) | P2·G | B | — |  |  |  |  |  | BOT-E1..E5 · rate-limit compliance · shared corpus with TTS | release |
| STO-01 | §31.31 Storage and media platform | v1 | A | **P0 for audio** |  |  |  |  |  | INT-E4 · asset serving · takedown drill | release |
| STO-02 | §31.31 Storage and media platform | v1 | A | P0 |  |  |  |  |  | INT-E4 · asset serving · takedown drill | release |
| STO-03 | §31.31 Storage and media platform | v1 | A | P1 |  |  |  |  |  | INT-E4 · asset serving · takedown drill | release |
| STO-04 | §31.31 Storage and media platform | v1 | A | P2 |  |  |  |  |  | INT-E4 · asset serving · takedown drill | none |
| STO-05 | §31.31 Storage and media platform | v1 | A | P1 |  |  |  |  |  | INT-E4 · asset serving · takedown drill | release |

## Phase distribution

| Phase | Count |
|---|---:|
| N | 14 |
| P2 | 97 |
| P2·G | 12 |
| P3 | 83 |
| P3·G | 6 |
| R | 17 |
| v1 | 461 |
| v1·G | 49 |

## Areas

| Prefix | Rows |
|---|---:|
| ADM | 9 |
| ALQ | 19 |
| AUD | 11 |
| BOT | 17 |
| CHL | 8 |
| CMP | 96 |
| CON | 41 |
| COS | 15 |
| CST | 30 |
| CTL | 15 |
| CUS | 6 |
| DSH | 22 |
| ENG | 24 |
| ENT | 9 |
| ENV | 9 |
| GIV | 7 |
| HUB | 23 |
| INT | 20 |
| JOB | 11 |
| LIF | 10 |
| LOB | 23 |
| MED | 27 |
| MIG | 3 |
| MKT | 9 |
| OPS | 15 |
| PAY | 30 |
| PCK | 15 |
| PRF | 19 |
| REF | 20 |
| REP | 5 |
| RT | 13 |
| RTE | 17 |
| RUL | 3 |
| SAF | 46 |
| SEC | 3 |
| SND | 7 |
| SOC | 17 |
| STO | 5 |
| TRN | 7 |
| TTS | 17 |
| VID | 22 |
| WID | 7 |
| WMK | 7 |

## L-tracks with an existing task record

These are the records the mapping above should be joined to.

| L-track | Task files |
|---|---:|
| L00 | 1 |
| L01 | 25 |
| L02 | 2 |
| L03 | 2 |
| L04 | 3 |
| L05 | 1 |
| L06 | 1 |
| L07 | 1 |
| L08 | 1 |
| L09 | 1 |
| L10 | 3 |
| L11 | 1 |
| L12 | 1 |
| L13 | 1 |
| L14 | 4 |
| L15 | 1 |
| L16 | 3 |
| L17 | 1 |
| L18 | 1 |
| L19 | 1 |
| L20 | 1 |
| L21 | 1 |
| L22 | 1 |
| L23 | 1 |
| L24 | 1 |
| L25 | 1 |
