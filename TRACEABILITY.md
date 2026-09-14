# Traceability index

**Generated 2026-09-14 by `tools/traceability.py`. Do not edit by hand.**

Six columns per `FULL-PRODUCT-DEFINITION.md` §35.4:
`requirement → task → acceptance record → review → evidence → release gate`.

A blank cell is a real gap, not an omission. Per §37.2 a row with a gap in any
column is not done, whatever its state letter says.

**614 requirement rows across 38 areas.**

## Coverage summary

| Column | Populated | Missing |
|---|---:|---:|
| Task file in `tasks/` or `active/` | 2 | 612 |
| Acceptance record (§37.3 scenarios) | 0 | 614 |
| Review (who traced the user path) | 0 | 614 |
| Evidence artefact (§37.8) | 0 | 614 |

Acceptance, review and evidence are uniformly empty because **no build work has
started**. The §37.11 suite column below states what each row will need; it is a
requirement, not a claim that anything has been run.

## Rows

| ID | Section | State | Pri | Task file | Required suites (§37.11) | Acceptance | Review | Evidence | Release gate |
|---|---|:-:|:-:|---|---|---|---|---|---|
| PAY-01 | §31.2 Payments and money | U | — |  | PAY-E1..E8 · raid burst · duplicate-webhook and dispatcher-down chaos · isolation |  |  |  | none |
| PAY-02 | §31.2 Payments and money | U | — |  | PAY-E1..E8 · raid burst · duplicate-webhook and dispatcher-down chaos · isolation |  |  |  | none |
| PAY-03 | §31.2 Payments and money | U | — |  | PAY-E1..E8 · raid burst · duplicate-webhook and dispatcher-down chaos · isolation |  |  |  | none |
| PAY-04 | §31.2 Payments and money | U | — |  | PAY-E1..E8 · raid burst · duplicate-webhook and dispatcher-down chaos · isolation |  |  |  | none |
| PAY-05 | §31.2 Payments and money | U | — |  | PAY-E1..E8 · raid burst · duplicate-webhook and dispatcher-down chaos · isolation |  |  |  | none |
| PAY-06 | §31.2 Payments and money | U | — |  | PAY-E1..E8 · raid burst · duplicate-webhook and dispatcher-down chaos · isolation |  |  |  | none |
| PAY-07 | §31.2 Payments and money | U | — |  | PAY-E1..E8 · raid burst · duplicate-webhook and dispatcher-down chaos · isolation |  |  |  | none |
| PAY-08 | §31.2 Payments and money | U | — |  | PAY-E1..E8 · raid burst · duplicate-webhook and dispatcher-down chaos · isolation |  |  |  | none |
| PAY-09 | §31.2 Payments and money | U | — |  | PAY-E1..E8 · raid burst · duplicate-webhook and dispatcher-down chaos · isolation |  |  |  | none |
| PAY-10 | §31.2 Payments and money | U | — |  | PAY-E1..E8 · raid burst · duplicate-webhook and dispatcher-down chaos · isolation |  |  |  | none |
| PAY-11 | §31.2 Payments and money | U | — |  | PAY-E1..E8 · raid burst · duplicate-webhook and dispatcher-down chaos · isolation |  |  |  | none |
| PAY-12 | §31.2 Payments and money | P | P1 |  | PAY-E1..E8 · raid burst · duplicate-webhook and dispatcher-down chaos · isolation |  |  |  | release |
| PAY-13 | §31.2 Payments and money | X | P0 |  | PAY-E1..E8 · raid burst · duplicate-webhook and dispatcher-down chaos · isolation |  |  |  | release |
| PAY-14 | §31.2 Payments and money | X | P0 |  | PAY-E1..E8 · raid burst · duplicate-webhook and dispatcher-down chaos · isolation |  |  |  | release |
| PAY-15 | §31.2 Payments and money | X | P0 |  | PAY-E1..E8 · raid burst · duplicate-webhook and dispatcher-down chaos · isolation |  |  |  | release |
| PAY-16 | §31.2 Payments and money | X | P0 |  | PAY-E1..E8 · raid burst · duplicate-webhook and dispatcher-down chaos · isolation |  |  |  | release |
| PAY-17 | §31.2 Payments and money | P | P1 |  | PAY-E1..E8 · raid burst · duplicate-webhook and dispatcher-down chaos · isolation |  |  |  | release |
| PAY-18 | §31.2 Payments and money | X | P2 |  | PAY-E1..E8 · raid burst · duplicate-webhook and dispatcher-down chaos · isolation |  |  |  | none |
| PAY-19 | §31.2 Payments and money | A | P2 |  | PAY-E1..E8 · raid burst · duplicate-webhook and dispatcher-down chaos · isolation |  |  |  | none |
| PAY-20 | §31.2 Payments and money | A | P1 |  | PAY-E1..E8 · raid burst · duplicate-webhook and dispatcher-down chaos · isolation |  |  |  | release |
| PAY-21 | §31.2 Payments and money | A | P2 |  | PAY-E1..E8 · raid burst · duplicate-webhook and dispatcher-down chaos · isolation |  |  |  | none |
| PAY-22 | §31.2 Payments and money | U | — |  | PAY-E1..E8 · raid burst · duplicate-webhook and dispatcher-down chaos · isolation |  |  |  | none |
| PAY-23 | §31.2 Payments and money | U | — |  | PAY-E1..E8 · raid burst · duplicate-webhook and dispatcher-down chaos · isolation |  |  |  | none |
| PAY-24 | §31.2 Payments and money | U | — |  | PAY-E1..E8 · raid burst · duplicate-webhook and dispatcher-down chaos · isolation |  |  |  | none |
| PAY-25 | §31.2 Payments and money | U | — |  | PAY-E1..E8 · raid burst · duplicate-webhook and dispatcher-down chaos · isolation |  |  |  | none |
| PAY-26 | §31.2 Payments and money | A | P1 |  | PAY-E1..E8 · raid burst · duplicate-webhook and dispatcher-down chaos · isolation |  |  |  | release |
| PAY-27 | §31.2 Payments and money | A | P1 |  | PAY-E1..E8 · raid burst · duplicate-webhook and dispatcher-down chaos · isolation |  |  |  | release |
| PAY-30 | §31.2 Payments and money | N | — |  | PAY-E1..E8 · raid burst · duplicate-webhook and dispatcher-down chaos · isolation |  |  |  | none |
| PAY-28 | §31.2 Payments and money | B | — |  | PAY-E1..E8 · raid burst · duplicate-webhook and dispatcher-down chaos · isolation |  |  |  | none |
| PAY-29 | §31.2 Payments and money | B | — |  | PAY-E1..E8 · raid burst · duplicate-webhook and dispatcher-down chaos · isolation |  |  |  | none |
| ALQ-01 | §31.3 Alerts, queues, overlay | U | — |  | PAY-E1..E8 · raid burst |  |  |  | none |
| ALQ-02 | §31.3 Alerts, queues, overlay | U | — |  | PAY-E1..E8 · raid burst |  |  |  | none |
| ALQ-03 | §31.3 Alerts, queues, overlay | U | — |  | PAY-E1..E8 · raid burst |  |  |  | none |
| ALQ-04 | §31.3 Alerts, queues, overlay | P | P0 |  | PAY-E1..E8 · raid burst |  |  |  | release |
| ALQ-05 | §31.3 Alerts, queues, overlay | U | — |  | PAY-E1..E8 · raid burst |  |  |  | none |
| ALQ-06 | §31.3 Alerts, queues, overlay | U | — |  | PAY-E1..E8 · raid burst |  |  |  | none |
| ALQ-07 | §31.3 Alerts, queues, overlay | U | — |  | PAY-E1..E8 · raid burst |  |  |  | none |
| ALQ-08 | §31.3 Alerts, queues, overlay | U | — |  | PAY-E1..E8 · raid burst |  |  |  | none |
| ALQ-09 | §31.3 Alerts, queues, overlay | U | — |  | PAY-E1..E8 · raid burst |  |  |  | none |
| ALQ-10 | §31.3 Alerts, queues, overlay | U | — |  | PAY-E1..E8 · raid burst |  |  |  | none |
| ALQ-11 | §31.3 Alerts, queues, overlay | U | — |  | PAY-E1..E8 · raid burst |  |  |  | none |
| ALQ-12 | §31.3 Alerts, queues, overlay | U | — |  | PAY-E1..E8 · raid burst |  |  |  | none |
| ALQ-13 | §31.3 Alerts, queues, overlay | U | — |  | PAY-E1..E8 · raid burst |  |  |  | none |
| ALQ-14 | §31.3 Alerts, queues, overlay | U | — |  | PAY-E1..E8 · raid burst |  |  |  | none |
| ALQ-15 | §31.3 Alerts, queues, overlay | A | P2 |  | PAY-E1..E8 · raid burst |  |  |  | none |
| ALQ-16 | §31.3 Alerts, queues, overlay | A | P1 |  | PAY-E1..E8 · raid burst |  |  |  | release |
| ALQ-17 | §31.3 Alerts, queues, overlay | A | P2 |  | PAY-E1..E8 · raid burst |  |  |  | none |
| ALQ-18 | §31.3 Alerts, queues, overlay | A | P0 |  | PAY-E1..E8 · raid burst |  |  |  | release |
| ALQ-19 | §31.3 Alerts, queues, overlay | A | P2 |  | PAY-E1..E8 · raid burst |  |  |  | none |
| TTS-01 | §31.4 TTS | U | — |  | OVL-E6, OVL-E7 · TTS-down chaos · safety corpus on both routes |  |  |  | none |
| TTS-02 | §31.4 TTS | U | — |  | OVL-E6, OVL-E7 · TTS-down chaos · safety corpus on both routes |  |  |  | none |
| TTS-03 | §31.4 TTS | U | — |  | OVL-E6, OVL-E7 · TTS-down chaos · safety corpus on both routes |  |  |  | none |
| TTS-04 | §31.4 TTS | U | — |  | OVL-E6, OVL-E7 · TTS-down chaos · safety corpus on both routes |  |  |  | none |
| TTS-05 | §31.4 TTS | U | — |  | OVL-E6, OVL-E7 · TTS-down chaos · safety corpus on both routes |  |  |  | none |
| TTS-06 | §31.4 TTS | A | **P0** |  | OVL-E6, OVL-E7 · TTS-down chaos · safety corpus on both routes |  |  |  | release |
| TTS-07 | §31.4 TTS | A | P1 |  | OVL-E6, OVL-E7 · TTS-down chaos · safety corpus on both routes |  |  |  | release |
| TTS-08 | §31.4 TTS | A | P1 |  | OVL-E6, OVL-E7 · TTS-down chaos · safety corpus on both routes |  |  |  | release |
| TTS-09 | §31.4 TTS | P | P1 |  | OVL-E6, OVL-E7 · TTS-down chaos · safety corpus on both routes |  |  |  | release |
| TTS-10 | §31.4 TTS | A | P1 |  | OVL-E6, OVL-E7 · TTS-down chaos · safety corpus on both routes |  |  |  | release |
| TTS-11 | §31.4 TTS | A | P1 |  | OVL-E6, OVL-E7 · TTS-down chaos · safety corpus on both routes |  |  |  | release |
| TTS-12 | §31.4 TTS | A | P1 |  | OVL-E6, OVL-E7 · TTS-down chaos · safety corpus on both routes |  |  |  | release |
| TTS-13 | §31.4 TTS | A | P1 |  | OVL-E6, OVL-E7 · TTS-down chaos · safety corpus on both routes |  |  |  | release |
| TTS-14 | §31.4 TTS | A | P2 |  | OVL-E6, OVL-E7 · TTS-down chaos · safety corpus on both routes |  |  |  | none |
| TTS-15 | §31.4 TTS | A | P1 |  | OVL-E6, OVL-E7 · TTS-down chaos · safety corpus on both routes |  |  |  | release |
| TTS-16 | §31.4 TTS | A | **P0 with TTS-06** |  | OVL-E6, OVL-E7 · TTS-down chaos · safety corpus on both routes |  |  |  | none |
| TTS-17 | §31.4 TTS | A | P1 |  | OVL-E6, OVL-E7 · TTS-down chaos · safety corpus on both routes |  |  |  | release |
| VID-01 | §31.5 Viewer identity, history, trust | A | **P0** |  | PAY-E1..E8 · isolation |  |  |  | release |
| VID-02 | §31.5 Viewer identity, history, trust | A | **P0** |  | PAY-E1..E8 · isolation |  |  |  | release |
| VID-03 | §31.5 Viewer identity, history, trust | X | **P0** |  | PAY-E1..E8 · isolation |  |  |  | release |
| VID-04 | §31.5 Viewer identity, history, trust | U | — |  | PAY-E1..E8 · isolation |  |  |  | none |
| VID-05 | §31.5 Viewer identity, history, trust | P | P0 |  | PAY-E1..E8 · isolation |  |  |  | release |
| VID-06 | §31.5 Viewer identity, history, trust | X | P1 |  | PAY-E1..E8 · isolation |  |  |  | release |
| VID-07 | §31.5 Viewer identity, history, trust | X | P1 |  | PAY-E1..E8 · isolation |  |  |  | release |
| VID-08 | §31.5 Viewer identity, history, trust | U | — |  | PAY-E1..E8 · isolation |  |  |  | none |
| VID-09 | §31.5 Viewer identity, history, trust | U | — |  | PAY-E1..E8 · isolation |  |  |  | none |
| VID-10 | §31.5 Viewer identity, history, trust | U | — |  | PAY-E1..E8 · isolation |  |  |  | none |
| VID-11 | §31.5 Viewer identity, history, trust | U | — |  | PAY-E1..E8 · isolation |  |  |  | none |
| VID-21 | §31.5 Viewer identity, history, trust | A | P1 |  | PAY-E1..E8 · isolation |  |  |  | release |
| VID-22 | §31.5 Viewer identity, history, trust | A | P1 |  | PAY-E1..E8 · isolation |  |  |  | release |
| VID-12 | §31.5 Viewer identity, history, trust | A | P1 |  | PAY-E1..E8 · isolation |  |  |  | release |
| VID-13 | §31.5 Viewer identity, history, trust | X | P1 |  | PAY-E1..E8 · isolation |  |  |  | release |
| VID-14 | §31.5 Viewer identity, history, trust | A | P1 |  | PAY-E1..E8 · isolation |  |  |  | release |
| VID-15 | §31.5 Viewer identity, history, trust | A | P1 |  | PAY-E1..E8 · isolation |  |  |  | release |
| VID-16 | §31.5 Viewer identity, history, trust | A | P1 |  | PAY-E1..E8 · isolation |  |  |  | release |
| VID-17 | §31.5 Viewer identity, history, trust | A | P1 |  | PAY-E1..E8 · isolation |  |  |  | release |
| VID-18 | §31.5 Viewer identity, history, trust | A | P1 |  | PAY-E1..E8 · isolation |  |  |  | release |
| VID-19 | §31.5 Viewer identity, history, trust | A | P0 |  | PAY-E1..E8 · isolation |  |  |  | release |
| VID-20 | §31.5 Viewer identity, history, trust | A | P1 |  | PAY-E1..E8 · isolation |  |  |  | release |
| ENG-01 | §31.6 Engagement — interactions, widgets, goals, challenges | P | P0 |  | OVL-E1..E12 · target concurrency · 8h soak · benchmark |  |  |  | release |
| ENG-02 | §31.6 Engagement — interactions, widgets, goals, challenges | P | P1 |  | OVL-E1..E12 · target concurrency · 8h soak · benchmark |  |  |  | release |
| ENG-03 | §31.6 Engagement — interactions, widgets, goals, challenges | U | — |  | OVL-E1..E12 · target concurrency · 8h soak · benchmark |  |  |  | none |
| ENG-04 | §31.6 Engagement — interactions, widgets, goals, challenges | U | — |  | OVL-E1..E12 · target concurrency · 8h soak · benchmark |  |  |  | none |
| ENG-05 | §31.6 Engagement — interactions, widgets, goals, challenges | U | — |  | OVL-E1..E12 · target concurrency · 8h soak · benchmark |  |  |  | none |
| ENG-06 | §31.6 Engagement — interactions, widgets, goals, challenges | U | — |  | OVL-E1..E12 · target concurrency · 8h soak · benchmark |  |  |  | none |
| ENG-07 | §31.6 Engagement — interactions, widgets, goals, challenges | P | P1 |  | OVL-E1..E12 · target concurrency · 8h soak · benchmark |  |  |  | release |
| ENG-08 | §31.6 Engagement — interactions, widgets, goals, challenges | U | — |  | OVL-E1..E12 · target concurrency · 8h soak · benchmark |  |  |  | none |
| ENG-09 | §31.6 Engagement — interactions, widgets, goals, challenges | A | **P0** |  | OVL-E1..E12 · target concurrency · 8h soak · benchmark |  |  |  | release |
| ENG-10 | §31.6 Engagement — interactions, widgets, goals, challenges | A | P0 |  | OVL-E1..E12 · target concurrency · 8h soak · benchmark |  |  |  | release |
| ENG-11 | §31.6 Engagement — interactions, widgets, goals, challenges | A | P0 |  | OVL-E1..E12 · target concurrency · 8h soak · benchmark |  |  |  | release |
| ENG-12 | §31.6 Engagement — interactions, widgets, goals, challenges | A | P0 |  | OVL-E1..E12 · target concurrency · 8h soak · benchmark |  |  |  | release |
| ENG-13 | §31.6 Engagement — interactions, widgets, goals, challenges | X | P1 |  | OVL-E1..E12 · target concurrency · 8h soak · benchmark |  |  |  | release |
| ENG-14 | §31.6 Engagement — interactions, widgets, goals, challenges | X | P1 |  | OVL-E1..E12 · target concurrency · 8h soak · benchmark |  |  |  | release |
| ENG-15 | §31.6 Engagement — interactions, widgets, goals, challenges | P | P2 |  | OVL-E1..E12 · target concurrency · 8h soak · benchmark |  |  |  | none |
| ENG-16 | §31.6 Engagement — interactions, widgets, goals, challenges | U | — |  | OVL-E1..E12 · target concurrency · 8h soak · benchmark |  |  |  | none |
| ENG-17 | §31.6 Engagement — interactions, widgets, goals, challenges | X | P1 |  | OVL-E1..E12 · target concurrency · 8h soak · benchmark |  |  |  | release |
| ENG-18 | §31.6 Engagement — interactions, widgets, goals, challenges | A | P1 |  | OVL-E1..E12 · target concurrency · 8h soak · benchmark |  |  |  | release |
| ENG-19 | §31.6 Engagement — interactions, widgets, goals, challenges | A | P2 |  | OVL-E1..E12 · target concurrency · 8h soak · benchmark |  |  |  | none |
| ENG-20 | §31.6 Engagement — interactions, widgets, goals, challenges | A | P2 |  | OVL-E1..E12 · target concurrency · 8h soak · benchmark |  |  |  | none |
| ENG-21 | §31.6 Engagement — interactions, widgets, goals, challenges | A | P1 |  | OVL-E1..E12 · target concurrency · 8h soak · benchmark |  |  |  | release |
| ENG-22 | §31.6 Engagement — interactions, widgets, goals, challenges | A | P2 |  | OVL-E1..E12 · target concurrency · 8h soak · benchmark |  |  |  | none |
| ENG-23 | §31.6 Engagement — interactions, widgets, goals, challenges | A | P1 |  | OVL-E1..E12 · target concurrency · 8h soak · benchmark |  |  |  | release |
| ENG-24 | §31.6 Engagement — interactions, widgets, goals, challenges | A | P2 |  | OVL-E1..E12 · target concurrency · 8h soak · benchmark |  |  |  | none |
| CHL-01 | §31.6 Engagement — interactions, widgets, goals, challenges | U | — |  | — |  |  |  | none |
| CHL-02 | §31.6 Engagement — interactions, widgets, goals, challenges | U | — |  | — |  |  |  | none |
| CHL-03 | §31.6 Engagement — interactions, widgets, goals, challenges | A | P1 |  | — |  |  |  | release |
| CHL-04 | §31.6 Engagement — interactions, widgets, goals, challenges | A | P1 |  | — |  |  |  | release |
| CHL-05 | §31.6 Engagement — interactions, widgets, goals, challenges | A | P1 |  | — |  |  |  | release |
| CHL-06 | §31.6 Engagement — interactions, widgets, goals, challenges | A | P2 |  | — |  |  |  | none |
| CHL-07 | §31.6 Engagement — interactions, widgets, goals, challenges | A | P2 |  | — |  |  |  | none |
| CHL-08 | §31.6 Engagement — interactions, widgets, goals, challenges | B | — |  | — |  |  |  | none |
| MED-01 | §31.7 Stickers, media, Alert Studio | U | — |  | INT-E4 · asset serving · takedown drill |  |  |  | none |
| MED-02 | §31.7 Stickers, media, Alert Studio | U | — |  | INT-E4 · asset serving · takedown drill |  |  |  | none |
| MED-03 | §31.7 Stickers, media, Alert Studio | U | — |  | INT-E4 · asset serving · takedown drill |  |  |  | none |
| MED-04 | §31.7 Stickers, media, Alert Studio | P | P1 |  | INT-E4 · asset serving · takedown drill |  |  |  | release |
| MED-05 | §31.7 Stickers, media, Alert Studio | X | P1 |  | INT-E4 · asset serving · takedown drill |  |  |  | release |
| MED-06 | §31.7 Stickers, media, Alert Studio | X | **P0** |  | INT-E4 · asset serving · takedown drill |  |  |  | release |
| MED-07 | §31.7 Stickers, media, Alert Studio | U | — |  | INT-E4 · asset serving · takedown drill |  |  |  | none |
| MED-08 | §31.7 Stickers, media, Alert Studio | U | — |  | INT-E4 · asset serving · takedown drill |  |  |  | none |
| MED-09 | §31.7 Stickers, media, Alert Studio | X | P1 |  | INT-E4 · asset serving · takedown drill |  |  |  | release |
| MED-10 | §31.7 Stickers, media, Alert Studio | A | P1 |  | INT-E4 · asset serving · takedown drill |  |  |  | release |
| MED-11 | §31.7 Stickers, media, Alert Studio | U | — |  | INT-E4 · asset serving · takedown drill |  |  |  | none |
| MED-12 | §31.7 Stickers, media, Alert Studio | U | — |  | INT-E4 · asset serving · takedown drill |  |  |  | none |
| MED-13 | §31.7 Stickers, media, Alert Studio | A | P1 |  | INT-E4 · asset serving · takedown drill |  |  |  | release |
| MED-14 | §31.7 Stickers, media, Alert Studio | A | P1 |  | INT-E4 · asset serving · takedown drill |  |  |  | release |
| MED-15 | §31.7 Stickers, media, Alert Studio | A | P2 |  | INT-E4 · asset serving · takedown drill |  |  |  | none |
| MED-22 | §31.7 Stickers, media, Alert Studio | A | P2 |  | INT-E4 · asset serving · takedown drill |  |  |  | none |
| MED-23 | §31.7 Stickers, media, Alert Studio | A | P2 |  | INT-E4 · asset serving · takedown drill |  |  |  | none |
| MED-24 | §31.7 Stickers, media, Alert Studio | A | P2 |  | INT-E4 · asset serving · takedown drill |  |  |  | none |
| MED-25 | §31.7 Stickers, media, Alert Studio | A | P2 |  | INT-E4 · asset serving · takedown drill |  |  |  | none |
| MED-26 | §31.7 Stickers, media, Alert Studio | A | P2 |  | INT-E4 · asset serving · takedown drill |  |  |  | none |
| MED-27 | §31.7 Stickers, media, Alert Studio | A | P2 |  | INT-E4 · asset serving · takedown drill |  |  |  | none |
| MED-16 | §31.7 Stickers, media, Alert Studio | A | P2 |  | INT-E4 · asset serving · takedown drill |  |  |  | none |
| MED-17 | §31.7 Stickers, media, Alert Studio | P | P2 |  | INT-E4 · asset serving · takedown drill |  |  |  | none |
| MED-18 | §31.7 Stickers, media, Alert Studio | P | P2 |  | INT-E4 · asset serving · takedown drill |  |  |  | none |
| MED-19 | §31.7 Stickers, media, Alert Studio | A | P2 |  | INT-E4 · asset serving · takedown drill |  |  |  | none |
| MED-20 | §31.7 Stickers, media, Alert Studio | A | P2 |  | INT-E4 · asset serving · takedown drill |  |  |  | none |
| MED-21 | §31.7 Stickers, media, Alert Studio | U | — |  | INT-E4 · asset serving · takedown drill |  |  |  | none |
| CMP-01 | §31.8 Companion | U | — |  | CMP-E1..E8 both platforms · localisation · crash-free gate |  |  |  | none |
| CMP-02 | §31.8 Companion | U | — |  | CMP-E1..E8 both platforms · localisation · crash-free gate |  |  |  | none |
| CMP-03 | §31.8 Companion | U | — |  | CMP-E1..E8 both platforms · localisation · crash-free gate |  |  |  | none |
| CMP-04 | §31.8 Companion | U | — |  | CMP-E1..E8 both platforms · localisation · crash-free gate |  |  |  | none |
| CMP-05 | §31.8 Companion | U | — |  | CMP-E1..E8 both platforms · localisation · crash-free gate |  |  |  | none |
| CMP-06 | §31.8 Companion | U | — |  | CMP-E1..E8 both platforms · localisation · crash-free gate |  |  |  | none |
| CMP-07 | §31.8 Companion | X | **P0** |  | CMP-E1..E8 both platforms · localisation · crash-free gate |  |  |  | release |
| CMP-08 | §31.8 Companion | U | — |  | CMP-E1..E8 both platforms · localisation · crash-free gate |  |  |  | none |
| CMP-09 | §31.8 Companion | B | — |  | CMP-E1..E8 both platforms · localisation · crash-free gate |  |  |  | none |
| CMP-10 | §31.8 Companion | B | — |  | CMP-E1..E8 both platforms · localisation · crash-free gate |  |  |  | none |
| CMP-11 | §31.8 Companion | B | — |  | CMP-E1..E8 both platforms · localisation · crash-free gate |  |  |  | none |
| CMP-12 | §31.8 Companion | A | P1 |  | CMP-E1..E8 both platforms · localisation · crash-free gate |  |  |  | release |
| CMP-36 | §31.8 Companion | A | P1 |  | CMP-E1..E8 both platforms · localisation · crash-free gate |  |  |  | release |
| CMP-37 | §31.8 Companion | P | P1 |  | CMP-E1..E8 both platforms · localisation · crash-free gate |  |  |  | release |
| CMP-13 | §31.8 Companion | P | P0 |  | CMP-E1..E8 both platforms · localisation · crash-free gate |  |  |  | release |
| CMP-14 | §31.8 Companion | A | P0 |  | CMP-E1..E8 both platforms · localisation · crash-free gate |  |  |  | release |
| CMP-15 | §31.8 Companion | P | P0 |  | CMP-E1..E8 both platforms · localisation · crash-free gate |  |  |  | release |
| CMP-16 | §31.8 Companion | A | P0 |  | CMP-E1..E8 both platforms · localisation · crash-free gate |  |  |  | release |
| CMP-17 | §31.8 Companion | A | P0 |  | CMP-E1..E8 both platforms · localisation · crash-free gate |  |  |  | release |
| CMP-18 | §31.8 Companion | A | P1 |  | CMP-E1..E8 both platforms · localisation · crash-free gate |  |  |  | release |
| CMP-19 | §31.8 Companion | A | P1 |  | CMP-E1..E8 both platforms · localisation · crash-free gate |  |  |  | release |
| CMP-20 | §31.8 Companion | A | P1 |  | CMP-E1..E8 both platforms · localisation · crash-free gate |  |  |  | release |
| CMP-21 | §31.8 Companion | A | P1 |  | CMP-E1..E8 both platforms · localisation · crash-free gate |  |  |  | release |
| CMP-22 | §31.8 Companion | A | P1 |  | CMP-E1..E8 both platforms · localisation · crash-free gate |  |  |  | release |
| CMP-23 | §31.8 Companion | P | P1 |  | CMP-E1..E8 both platforms · localisation · crash-free gate |  |  |  | release |
| CMP-24 | §31.8 Companion | A | P1 |  | CMP-E1..E8 both platforms · localisation · crash-free gate |  |  |  | release |
| CMP-25 | §31.8 Companion | P | P1 |  | CMP-E1..E8 both platforms · localisation · crash-free gate |  |  |  | release |
| CMP-26 | §31.8 Companion | U | — |  | CMP-E1..E8 both platforms · localisation · crash-free gate |  |  |  | none |
| CMP-27 | §31.8 Companion | A | P2 |  | CMP-E1..E8 both platforms · localisation · crash-free gate |  |  |  | none |
| CMP-28 | §31.8 Companion | A | P2 |  | CMP-E1..E8 both platforms · localisation · crash-free gate |  |  |  | none |
| CMP-29 | §31.8 Companion | P | P1 |  | CMP-E1..E8 both platforms · localisation · crash-free gate |  |  |  | release |
| CMP-30 | §31.8 Companion | A | P1 |  | CMP-E1..E8 both platforms · localisation · crash-free gate |  |  |  | release |
| CMP-31 | §31.8 Companion | A | P1 |  | CMP-E1..E8 both platforms · localisation · crash-free gate |  |  |  | release |
| CMP-32 | §31.8 Companion | U | — |  | CMP-E1..E8 both platforms · localisation · crash-free gate |  |  |  | none |
| CMP-33 | §31.8 Companion | U | — |  | CMP-E1..E8 both platforms · localisation · crash-free gate |  |  |  | none |
| CMP-34 | §31.8 Companion | U | — |  | CMP-E1..E8 both platforms · localisation · crash-free gate |  |  |  | none |
| CMP-35 | §31.8 Companion | A | P2 |  | CMP-E1..E8 both platforms · localisation · crash-free gate |  |  |  | none |
| CMP-38 | §31.8 Companion | A | **P0** |  | CMP-E1..E8 both platforms · localisation · crash-free gate |  |  |  | release |
| CMP-39 | §31.8 Companion | A | **P0** |  | CMP-E1..E8 both platforms · localisation · crash-free gate |  |  |  | release |
| CMP-40 | §31.8 Companion | A | **P0** |  | CMP-E1..E8 both platforms · localisation · crash-free gate |  |  |  | release |
| CMP-41 | §31.8 Companion | A | **P0** |  | CMP-E1..E8 both platforms · localisation · crash-free gate |  |  |  | release |
| CMP-42 | §31.8 Companion | A | P1 |  | CMP-E1..E8 both platforms · localisation · crash-free gate |  |  |  | release |
| CMP-43 | §31.8 Companion | A | P1 |  | CMP-E1..E8 both platforms · localisation · crash-free gate |  |  |  | release |
| CMP-44 | §31.8 Companion | A | P1 |  | CMP-E1..E8 both platforms · localisation · crash-free gate |  |  |  | release |
| CMP-45 | §31.8 Companion | A | P1 |  | CMP-E1..E8 both platforms · localisation · crash-free gate |  |  |  | release |
| CMP-46 | §31.8 Companion | A | P2 |  | CMP-E1..E8 both platforms · localisation · crash-free gate |  |  |  | none |
| CMP-47 | §31.8 Companion | A | P3 |  | CMP-E1..E8 both platforms · localisation · crash-free gate |  |  |  | none |
| CMP-48 | §31.8 Companion | A | P3 |  | CMP-E1..E8 both platforms · localisation · crash-free gate |  |  |  | none |
| CMP-49 | §31.8 Companion | A | **P0** |  | CMP-E1..E8 both platforms · localisation · crash-free gate |  |  |  | release |
| CMP-50 | §31.8 Companion | A | P1 |  | CMP-E1..E8 both platforms · localisation · crash-free gate |  |  |  | release |
| CMP-51 | §31.8 Companion | A | P1 |  | CMP-E1..E8 both platforms · localisation · crash-free gate |  |  |  | release |
| CMP-52 | §31.8 Companion | A | P1 |  | CMP-E1..E8 both platforms · localisation · crash-free gate |  |  |  | release |
| CMP-53 | §31.8 Companion | A | **P0** |  | CMP-E1..E8 both platforms · localisation · crash-free gate |  |  |  | release |
| CMP-54 | §31.8 Companion | A | P2 |  | CMP-E1..E8 both platforms · localisation · crash-free gate |  |  |  | none |
| CMP-55 | §31.8 Companion | A | **P0** |  | CMP-E1..E8 both platforms · localisation · crash-free gate |  |  |  | release |
| CMP-56 | §31.8 Companion | A | P1 |  | CMP-E1..E8 both platforms · localisation · crash-free gate |  |  |  | release |
| CMP-57 | §31.8 Companion | A | P1 |  | CMP-E1..E8 both platforms · localisation · crash-free gate |  |  |  | release |
| CMP-58 | §31.8 Companion | A | P1 |  | CMP-E1..E8 both platforms · localisation · crash-free gate |  |  |  | release |
| CMP-59 | §31.8 Companion | A | P1 |  | CMP-E1..E8 both platforms · localisation · crash-free gate |  |  |  | release |
| CMP-60 | §31.8 Companion | A | **P0** |  | CMP-E1..E8 both platforms · localisation · crash-free gate |  |  |  | release |
| CMP-61 | §31.8 Companion | A | P1 |  | CMP-E1..E8 both platforms · localisation · crash-free gate |  |  |  | release |
| CMP-62 | §31.8 Companion | A | P1 |  | CMP-E1..E8 both platforms · localisation · crash-free gate |  |  |  | release |
| CMP-63 | §31.8 Companion | A | **P0** |  | CMP-E1..E8 both platforms · localisation · crash-free gate |  |  |  | release |
| CMP-64 | §31.8 Companion | A | P1 |  | CMP-E1..E8 both platforms · localisation · crash-free gate |  |  |  | release |
| CMP-65 | §31.8 Companion | A | P1 |  | CMP-E1..E8 both platforms · localisation · crash-free gate |  |  |  | release |
| CMP-66 | §31.8 Companion | A | P1 |  | CMP-E1..E8 both platforms · localisation · crash-free gate |  |  |  | release |
| CMP-67 | §31.8 Companion | A | P2 |  | CMP-E1..E8 both platforms · localisation · crash-free gate |  |  |  | none |
| CMP-68 | §31.8 Companion | A | P1 |  | CMP-E1..E8 both platforms · localisation · crash-free gate |  |  |  | release |
| CMP-69 | §31.8 Companion | A | P1 |  | CMP-E1..E8 both platforms · localisation · crash-free gate |  |  |  | release |
| CMP-70 | §31.8 Companion | A | P1 |  | CMP-E1..E8 both platforms · localisation · crash-free gate |  |  |  | release |
| CMP-71 | §31.8 Companion | A | P1 |  | CMP-E1..E8 both platforms · localisation · crash-free gate |  |  |  | release |
| CMP-72 | §31.8 Companion | A | **P0** |  | CMP-E1..E8 both platforms · localisation · crash-free gate |  |  |  | release |
| CMP-73 | §31.8 Companion | A | P1 |  | CMP-E1..E8 both platforms · localisation · crash-free gate |  |  |  | release |
| CMP-74 | §31.8 Companion | A | **P0** |  | CMP-E1..E8 both platforms · localisation · crash-free gate |  |  |  | release |
| CMP-75 | §31.8 Companion | A | P1 |  | CMP-E1..E8 both platforms · localisation · crash-free gate |  |  |  | release |
| CMP-76 | §31.8 Companion | A | P1 |  | CMP-E1..E8 both platforms · localisation · crash-free gate |  |  |  | release |
| CMP-77 | §31.8 Companion | A | P1 |  | CMP-E1..E8 both platforms · localisation · crash-free gate |  |  |  | release |
| CMP-78 | §31.8 Companion | B | **P0** |  | CMP-E1..E8 both platforms · localisation · crash-free gate |  |  |  | release |
| CMP-79 | §31.8 Companion | A | **P0** |  | CMP-E1..E8 both platforms · localisation · crash-free gate |  |  |  | release |
| CMP-80 | §31.8 Companion | A | **P0** |  | CMP-E1..E8 both platforms · localisation · crash-free gate |  |  |  | release |
| CMP-81 | §31.8 Companion | A | P1 |  | CMP-E1..E8 both platforms · localisation · crash-free gate |  |  |  | release |
| CMP-82 | §31.8 Companion | A | **P0** |  | CMP-E1..E8 both platforms · localisation · crash-free gate |  |  |  | release |
| CMP-83 | §31.8 Companion | A | P1 |  | CMP-E1..E8 both platforms · localisation · crash-free gate |  |  |  | release |
| CMP-84 | §31.8 Companion | A | P1 |  | CMP-E1..E8 both platforms · localisation · crash-free gate |  |  |  | release |
| CMP-85 | §31.8 Companion | A | P1 |  | CMP-E1..E8 both platforms · localisation · crash-free gate |  |  |  | release |
| CMP-86 | §31.8 Companion | A | P1 |  | CMP-E1..E8 both platforms · localisation · crash-free gate |  |  |  | release |
| CMP-87 | §31.8 Companion | A | P2 |  | CMP-E1..E8 both platforms · localisation · crash-free gate |  |  |  | none |
| CMP-88 | §31.8 Companion | A | **P0** |  | CMP-E1..E8 both platforms · localisation · crash-free gate |  |  |  | release |
| CMP-89 | §31.8 Companion | A | P1 |  | CMP-E1..E8 both platforms · localisation · crash-free gate |  |  |  | release |
| CMP-90 | §31.8 Companion | A | P1 |  | CMP-E1..E8 both platforms · localisation · crash-free gate |  |  |  | release |
| CMP-91 | §31.8 Companion | A | **P0** |  | CMP-E1..E8 both platforms · localisation · crash-free gate |  |  |  | release |
| CMP-92 | §31.8 Companion | A | **P0** |  | CMP-E1..E8 both platforms · localisation · crash-free gate |  |  |  | release |
| CMP-93 | §31.8 Companion | A | P1 |  | CMP-E1..E8 both platforms · localisation · crash-free gate |  |  |  | release |
| CON-01 | §31.9 Connectors and chat | U | — | L15-live-platform-connectors-and-chat-commands.md | post-v1 (Phase 4) |  |  |  | none |
| CON-02 | §31.9 Connectors and chat | X | **P0** |  | post-v1 (Phase 4) |  |  |  | release |
| CON-03 | §31.9 Connectors and chat | A | **P0** |  | post-v1 (Phase 4) |  |  |  | release |
| CON-04 | §31.9 Connectors and chat | U | — |  | post-v1 (Phase 4) |  |  |  | none |
| CON-05 | §31.9 Connectors and chat | U | — |  | post-v1 (Phase 4) |  |  |  | none |
| CON-06 | §31.9 Connectors and chat | U | — |  | post-v1 (Phase 4) |  |  |  | none |
| CON-07 | §31.9 Connectors and chat | U | — | L15-live-platform-connectors-and-chat-commands.md | post-v1 (Phase 4) |  |  |  | none |
| CON-22 | §31.9 Connectors and chat | A | P1 |  | post-v1 (Phase 4) |  |  |  | release |
| CON-08 | §31.9 Connectors and chat | B | — |  | post-v1 (Phase 4) |  |  |  | none |
| CON-09 | §31.9 Connectors and chat | U | — |  | post-v1 (Phase 4) |  |  |  | none |
| CON-10 | §31.9 Connectors and chat | A | P1 |  | post-v1 (Phase 4) |  |  |  | release |
| CON-11 | §31.9 Connectors and chat | X | P1 |  | post-v1 (Phase 4) |  |  |  | release |
| CON-12 | §31.9 Connectors and chat | U | — |  | post-v1 (Phase 4) |  |  |  | none |
| CON-13 | §31.9 Connectors and chat | A | P1 |  | post-v1 (Phase 4) |  |  |  | release |
| CON-14 | §31.9 Connectors and chat | A | P1 |  | post-v1 (Phase 4) |  |  |  | release |
| CON-15 | §31.9 Connectors and chat | A | P1 |  | post-v1 (Phase 4) |  |  |  | release |
| CON-16 | §31.9 Connectors and chat | A | P2 |  | post-v1 (Phase 4) |  |  |  | none |
| CON-17 | §31.9 Connectors and chat | A | P1 |  | post-v1 (Phase 4) |  |  |  | release |
| CON-18 | §31.9 Connectors and chat | B | — |  | post-v1 (Phase 4) |  |  |  | none |
| CON-19 | §31.9 Connectors and chat | B | — |  | post-v1 (Phase 4) |  |  |  | none |
| CON-20 | §31.9 Connectors and chat | A | P3 |  | post-v1 (Phase 4) |  |  |  | none |
| CON-21 | §31.9 Connectors and chat | A | P1 |  | post-v1 (Phase 4) |  |  |  | release |
| ENT-01 | §31.10 Entitlements, billing, admin, ops | U | — |  | LIF-E1..E3 · isolation |  |  |  | none |
| ENT-02 | §31.10 Entitlements, billing, admin, ops | U | — |  | LIF-E1..E3 · isolation |  |  |  | none |
| ENT-03 | §31.10 Entitlements, billing, admin, ops | X | P1 |  | LIF-E1..E3 · isolation |  |  |  | release |
| ENT-04 | §31.10 Entitlements, billing, admin, ops | P | P1 |  | LIF-E1..E3 · isolation |  |  |  | release |
| ENT-05 | §31.10 Entitlements, billing, admin, ops | U | — |  | LIF-E1..E3 · isolation |  |  |  | none |
| ENT-06 | §31.10 Entitlements, billing, admin, ops | U | — |  | LIF-E1..E3 · isolation |  |  |  | none |
| ENT-07 | §31.10 Entitlements, billing, admin, ops | U | — |  | LIF-E1..E3 · isolation |  |  |  | none |
| ENT-08 | §31.10 Entitlements, billing, admin, ops | A | P1 |  | LIF-E1..E3 · isolation |  |  |  | release |
| ENT-09 | §31.10 Entitlements, billing, admin, ops | A | P1 |  | LIF-E1..E3 · isolation |  |  |  | release |
| ADM-01 | §31.10 Entitlements, billing, admin, ops | U | — |  | DSH-E1..E5 · LIF-E4..E6 · isolation |  |  |  | none |
| ADM-02 | §31.10 Entitlements, billing, admin, ops | U | — |  | DSH-E1..E5 · LIF-E4..E6 · isolation |  |  |  | none |
| ADM-03 | §31.10 Entitlements, billing, admin, ops | U | — |  | DSH-E1..E5 · LIF-E4..E6 · isolation |  |  |  | none |
| ADM-04 | §31.10 Entitlements, billing, admin, ops | P | P2 |  | DSH-E1..E5 · LIF-E4..E6 · isolation |  |  |  | none |
| ADM-05 | §31.10 Entitlements, billing, admin, ops | X | P0 |  | DSH-E1..E5 · LIF-E4..E6 · isolation |  |  |  | release |
| ADM-06 | §31.10 Entitlements, billing, admin, ops | X | P1 |  | DSH-E1..E5 · LIF-E4..E6 · isolation |  |  |  | release |
| ADM-07 | §31.10 Entitlements, billing, admin, ops | A | P0 |  | DSH-E1..E5 · LIF-E4..E6 · isolation |  |  |  | release |
| ADM-08 | §31.10 Entitlements, billing, admin, ops | U | — |  | DSH-E1..E5 · LIF-E4..E6 · isolation |  |  |  | none |
| ADM-09 | §31.10 Entitlements, billing, admin, ops | U | — |  | DSH-E1..E5 · LIF-E4..E6 · isolation |  |  |  | none |
| OPS-01 | §31.10 Entitlements, billing, admin, ops | U | — |  | — |  |  |  | none |
| OPS-02 | §31.10 Entitlements, billing, admin, ops | X | **P0** |  | — |  |  |  | release |
| OPS-03 | §31.10 Entitlements, billing, admin, ops | U | — |  | — |  |  |  | none |
| OPS-04 | §31.10 Entitlements, billing, admin, ops | B | — |  | — |  |  |  | none |
| OPS-05 | §31.10 Entitlements, billing, admin, ops | U | — |  | — |  |  |  | none |
| OPS-06 | §31.10 Entitlements, billing, admin, ops | U | — |  | — |  |  |  | none |
| OPS-07 | §31.10 Entitlements, billing, admin, ops | A | P0 |  | — |  |  |  | release |
| OPS-08 | §31.10 Entitlements, billing, admin, ops | A | P0 |  | — |  |  |  | release |
| OPS-09 | §31.10 Entitlements, billing, admin, ops | P | P0 |  | — |  |  |  | release |
| OPS-10 | §31.10 Entitlements, billing, admin, ops | A | P0 |  | — |  |  |  | release |
| OPS-11 | §31.10 Entitlements, billing, admin, ops | A | P0 |  | — |  |  |  | release |
| OPS-12 | §31.10 Entitlements, billing, admin, ops | U | — |  | — |  |  |  | none |
| OPS-13 | §31.10 Entitlements, billing, admin, ops | U | — |  | — |  |  |  | none |
| OPS-14 | §31.10 Entitlements, billing, admin, ops | B | — |  | — |  |  |  | none |
| OPS-15 | §31.10 Entitlements, billing, admin, ops | U | — |  | — |  |  |  | none |
| MKT-01 | §31.11 Marketing, legal, support | U | — |  | — |  |  |  | none |
| MKT-02 | §31.11 Marketing, legal, support | U | — |  | — |  |  |  | none |
| MKT-03 | §31.11 Marketing, legal, support | U | — |  | — |  |  |  | none |
| MKT-04 | §31.11 Marketing, legal, support | U | — |  | — |  |  |  | none |
| MKT-05 | §31.11 Marketing, legal, support | A | P1 |  | — |  |  |  | release |
| MKT-06 | §31.11 Marketing, legal, support | A | P2 |  | — |  |  |  | none |
| MKT-07 | §31.11 Marketing, legal, support | B | — |  | — |  |  |  | none |
| MKT-08 | §31.11 Marketing, legal, support | A | P0 |  | — |  |  |  | release |
| MKT-09 | §31.11 Marketing, legal, support | U | — |  | — |  |  |  | none |
| HUB-01 | §31.13 Live Support Hub | P | P0 |  | HUB-E1..E5 · 3G profile · accessibility |  |  |  | release |
| HUB-02 | §31.13 Live Support Hub | A | P0 |  | HUB-E1..E5 · 3G profile · accessibility |  |  |  | release |
| HUB-03 | §31.13 Live Support Hub | A | P0 |  | HUB-E1..E5 · 3G profile · accessibility |  |  |  | release |
| HUB-04 | §31.13 Live Support Hub | A | P0 |  | HUB-E1..E5 · 3G profile · accessibility |  |  |  | release |
| HUB-05 | §31.13 Live Support Hub | X | P0 |  | HUB-E1..E5 · 3G profile · accessibility |  |  |  | release |
| HUB-06 | §31.13 Live Support Hub | A | P1 |  | HUB-E1..E5 · 3G profile · accessibility |  |  |  | release |
| HUB-07 | §31.13 Live Support Hub | A | P1 |  | HUB-E1..E5 · 3G profile · accessibility |  |  |  | release |
| HUB-08 | §31.13 Live Support Hub | P | P1 |  | HUB-E1..E5 · 3G profile · accessibility |  |  |  | release |
| HUB-09 | §31.13 Live Support Hub | A | P1 |  | HUB-E1..E5 · 3G profile · accessibility |  |  |  | release |
| HUB-10 | §31.13 Live Support Hub | A | P1 |  | HUB-E1..E5 · 3G profile · accessibility |  |  |  | release |
| HUB-11 | §31.13 Live Support Hub | A | P1 |  | HUB-E1..E5 · 3G profile · accessibility |  |  |  | release |
| HUB-12 | §31.13 Live Support Hub | A | P2 |  | HUB-E1..E5 · 3G profile · accessibility |  |  |  | none |
| HUB-13 | §31.13 Live Support Hub | A | P2 |  | HUB-E1..E5 · 3G profile · accessibility |  |  |  | none |
| HUB-14 | §31.13 Live Support Hub | A | P1 |  | HUB-E1..E5 · 3G profile · accessibility |  |  |  | release |
| HUB-15 | §31.13 Live Support Hub | A | P1 |  | HUB-E1..E5 · 3G profile · accessibility |  |  |  | release |
| HUB-16 | §31.13 Live Support Hub | A | P1 |  | HUB-E1..E5 · 3G profile · accessibility |  |  |  | release |
| HUB-17 | §31.13 Live Support Hub | A | P1 |  | HUB-E1..E5 · 3G profile · accessibility |  |  |  | release |
| HUB-18 | §31.13 Live Support Hub | P | P1 |  | HUB-E1..E5 · 3G profile · accessibility |  |  |  | release |
| HUB-19 | §31.13 Live Support Hub | P | P0 |  | HUB-E1..E5 · 3G profile · accessibility |  |  |  | release |
| HUB-20 | §31.13 Live Support Hub | A | P2 |  | HUB-E1..E5 · 3G profile · accessibility |  |  |  | none |
| HUB-21 | §31.13 Live Support Hub | A | P2 |  | HUB-E1..E5 · 3G profile · accessibility |  |  |  | none |
| HUB-22 | §31.13 Live Support Hub | A | P2 |  | HUB-E1..E5 · 3G profile · accessibility |  |  |  | none |
| HUB-23 | §31.13 Live Support Hub | A | P1 |  | HUB-E1..E5 · 3G profile · accessibility |  |  |  | release |
| CUS-01 | §31.14 Customisation and gating | P | P0 |  | DSH-E1..E5 · accessibility |  |  |  | release |
| CUS-02 | §31.14 Customisation and gating | A | P0 |  | DSH-E1..E5 · accessibility |  |  |  | release |
| CUS-03 | §31.14 Customisation and gating | P | P1 |  | DSH-E1..E5 · accessibility |  |  |  | release |
| CUS-04 | §31.14 Customisation and gating | P | P1 |  | DSH-E1..E5 · accessibility |  |  |  | release |
| CUS-05 | §31.14 Customisation and gating | A | P2 |  | DSH-E1..E5 · accessibility |  |  |  | none |
| CUS-06 | §31.14 Customisation and gating | A | P1 |  | DSH-E1..E5 · accessibility |  |  |  | release |
| LOB-01 | §31.15 Lobby Engine | A | P1 |  | — |  |  |  | release |
| LOB-02 | §31.15 Lobby Engine | A | P1 |  | — |  |  |  | release |
| LOB-03 | §31.15 Lobby Engine | A | P1 |  | — |  |  |  | release |
| LOB-04 | §31.15 Lobby Engine | A | P1 |  | — |  |  |  | release |
| LOB-05 | §31.15 Lobby Engine | A | P1 |  | — |  |  |  | release |
| LOB-06 | §31.15 Lobby Engine | A | P1 |  | — |  |  |  | release |
| LOB-07 | §31.15 Lobby Engine | A | P1 |  | — |  |  |  | release |
| LOB-08 | §31.15 Lobby Engine | A | P1 |  | — |  |  |  | release |
| LOB-09 | §31.15 Lobby Engine | A | P1 |  | — |  |  |  | release |
| LOB-10 | §31.15 Lobby Engine | A | P1 |  | — |  |  |  | release |
| LOB-11 | §31.15 Lobby Engine | A | P1 |  | — |  |  |  | release |
| LOB-12 | §31.15 Lobby Engine | A | P1 |  | — |  |  |  | release |
| LOB-13 | §31.15 Lobby Engine | A | P2 |  | — |  |  |  | none |
| LOB-14 | §31.15 Lobby Engine | A | P2 |  | — |  |  |  | none |
| LOB-15 | §31.15 Lobby Engine | A | P2 |  | — |  |  |  | none |
| LOB-16 | §31.15 Lobby Engine | A | P2 |  | — |  |  |  | none |
| LOB-17 | §31.15 Lobby Engine | A | P2 |  | — |  |  |  | none |
| LOB-18 | §31.15 Lobby Engine | A | P2 |  | — |  |  |  | none |
| LOB-19 | §31.15 Lobby Engine | A | P1 |  | — |  |  |  | release |
| LOB-20 | §31.15 Lobby Engine | A | P3 |  | — |  |  |  | none |
| LOB-21 | §31.15 Lobby Engine | A | P2 |  | — |  |  |  | none |
| LOB-22 | §31.15 Lobby Engine | A | P3 |  | — |  |  |  | none |
| LOB-23 | §31.15 Lobby Engine | N | — |  | — |  |  |  | none |
| GIV-01 | §31.16 Giveaways and tournaments | A | P1 |  | — |  |  |  | release |
| GIV-02 | §31.16 Giveaways and tournaments | A | P1 |  | — |  |  |  | release |
| GIV-03 | §31.16 Giveaways and tournaments | A | P1 |  | — |  |  |  | release |
| GIV-04 | §31.16 Giveaways and tournaments | A | P1 |  | — |  |  |  | release |
| GIV-05 | §31.16 Giveaways and tournaments | A | P1 |  | — |  |  |  | release |
| GIV-06 | §31.16 Giveaways and tournaments | A | P1 |  | — |  |  |  | release |
| GIV-07 | §31.16 Giveaways and tournaments | A | P1 |  | — |  |  |  | release |
| TRN-01 | §31.16 Giveaways and tournaments | A | P2 |  | — |  |  |  | none |
| TRN-02 | §31.16 Giveaways and tournaments | A | P2 |  | — |  |  |  | none |
| TRN-03 | §31.16 Giveaways and tournaments | A | P2 |  | — |  |  |  | none |
| TRN-04 | §31.16 Giveaways and tournaments | A | P2 |  | — |  |  |  | none |
| TRN-05 | §31.16 Giveaways and tournaments | A | P2 |  | — |  |  |  | none |
| TRN-06 | §31.16 Giveaways and tournaments | A | P2 |  | — |  |  |  | none |
| AUD-01 | §31.17 Custom audio and creator media | A | P1 |  | — |  |  |  | release |
| AUD-02 | §31.17 Custom audio and creator media | A | P1 |  | — |  |  |  | release |
| AUD-03 | §31.17 Custom audio and creator media | A | P1 |  | — |  |  |  | release |
| AUD-04 | §31.17 Custom audio and creator media | A | P1 |  | — |  |  |  | release |
| AUD-05 | §31.17 Custom audio and creator media | A | P2 |  | — |  |  |  | none |
| AUD-06 | §31.17 Custom audio and creator media | A | P1 |  | — |  |  |  | release |
| AUD-07 | §31.17 Custom audio and creator media | A | P1 |  | — |  |  |  | release |
| AUD-08 | §31.17 Custom audio and creator media | A | P1 |  | — |  |  |  | release |
| AUD-09 | §31.17 Custom audio and creator media | A | P1 |  | — |  |  |  | release |
| AUD-10 | §31.17 Custom audio and creator media | A | P1 |  | — |  |  |  | release |
| AUD-11 | §31.17 Custom audio and creator media | N | — |  | — |  |  |  | none |
| RT-01 | §31.18 Performance | X | **P0** |  | OVL-E1..E12 · target concurrency · 8h soak · benchmark |  |  |  | release |
| RT-02 | §31.18 Performance | X | **P0** |  | OVL-E1..E12 · target concurrency · 8h soak · benchmark |  |  |  | release |
| RT-03 | §31.18 Performance | X | **P0** |  | OVL-E1..E12 · target concurrency · 8h soak · benchmark |  |  |  | release |
| RT-04 | §31.18 Performance | X | **P0** |  | OVL-E1..E12 · target concurrency · 8h soak · benchmark |  |  |  | release |
| RT-05 | §31.18 Performance | X | **P0** |  | OVL-E1..E12 · target concurrency · 8h soak · benchmark |  |  |  | release |
| RT-06 | §31.18 Performance | A | **P0** |  | OVL-E1..E12 · target concurrency · 8h soak · benchmark |  |  |  | release |
| RT-07 | §31.18 Performance | A | **P0** |  | OVL-E1..E12 · target concurrency · 8h soak · benchmark |  |  |  | release |
| RT-08 | §31.18 Performance | X | **P0** |  | OVL-E1..E12 · target concurrency · 8h soak · benchmark |  |  |  | release |
| RT-09 | §31.18 Performance | A | **P0** |  | OVL-E1..E12 · target concurrency · 8h soak · benchmark |  |  |  | release |
| RT-10 | §31.18 Performance | A | **P0** |  | OVL-E1..E12 · target concurrency · 8h soak · benchmark |  |  |  | release |
| RT-11 | §31.18 Performance | A | P1 |  | OVL-E1..E12 · target concurrency · 8h soak · benchmark |  |  |  | release |
| RT-12 | §31.18 Performance | A | **P0** |  | OVL-E1..E12 · target concurrency · 8h soak · benchmark |  |  |  | release |
| RT-13 | §31.18 Performance | A | P1 |  | OVL-E1..E12 · target concurrency · 8h soak · benchmark |  |  |  | release |
| PRF-01 | §31.18 Performance | A | P0 |  | OVL-E1..E12 · target concurrency · 8h soak · benchmark |  |  |  | release |
| PRF-02 | §31.18 Performance | A | P0 |  | OVL-E1..E12 · target concurrency · 8h soak · benchmark |  |  |  | release |
| PRF-03 | §31.18 Performance | P | P0 |  | OVL-E1..E12 · target concurrency · 8h soak · benchmark |  |  |  | release |
| PRF-04 | §31.18 Performance | A | P0 |  | OVL-E1..E12 · target concurrency · 8h soak · benchmark |  |  |  | release |
| PRF-05 | §31.18 Performance | A | P0 |  | OVL-E1..E12 · target concurrency · 8h soak · benchmark |  |  |  | release |
| PRF-06 | §31.18 Performance | A | P0 |  | OVL-E1..E12 · target concurrency · 8h soak · benchmark |  |  |  | release |
| PRF-07 | §31.18 Performance | A | P1 |  | OVL-E1..E12 · target concurrency · 8h soak · benchmark |  |  |  | release |
| PRF-08 | §31.18 Performance | A | P0 |  | OVL-E1..E12 · target concurrency · 8h soak · benchmark |  |  |  | release |
| PRF-09 | §31.18 Performance | P | P0 |  | OVL-E1..E12 · target concurrency · 8h soak · benchmark |  |  |  | release |
| PRF-10 | §31.18 Performance | P | P1 |  | OVL-E1..E12 · target concurrency · 8h soak · benchmark |  |  |  | release |
| PRF-11 | §31.18 Performance | P | P0 |  | OVL-E1..E12 · target concurrency · 8h soak · benchmark |  |  |  | release |
| PRF-12 | §31.18 Performance | A | P1 |  | OVL-E1..E12 · target concurrency · 8h soak · benchmark |  |  |  | release |
| PRF-13 | §31.18 Performance | U | — |  | OVL-E1..E12 · target concurrency · 8h soak · benchmark |  |  |  | none |
| PRF-14 | §31.18 Performance | A | P1 |  | OVL-E1..E12 · target concurrency · 8h soak · benchmark |  |  |  | release |
| PRF-15 | §31.18 Performance | P | P1 |  | OVL-E1..E12 · target concurrency · 8h soak · benchmark |  |  |  | release |
| PRF-16 | §31.18 Performance | A | P1 |  | OVL-E1..E12 · target concurrency · 8h soak · benchmark |  |  |  | release |
| PRF-17 | §31.18 Performance | A | **P0** |  | OVL-E1..E12 · target concurrency · 8h soak · benchmark |  |  |  | release |
| PRF-18 | §31.18 Performance | A | P1 |  | OVL-E1..E12 · target concurrency · 8h soak · benchmark |  |  |  | release |
| PRF-19 | §31.18 Performance | A | P1 |  | OVL-E1..E12 · target concurrency · 8h soak · benchmark |  |  |  | release |
| WMK-01 | §31.18 Performance | A | **P0** |  | OVL-E8..E11 |  |  |  | release |
| WMK-02 | §31.18 Performance | A | **P0** |  | OVL-E8..E11 |  |  |  | release |
| WMK-03 | §31.18 Performance | A | P1 |  | OVL-E8..E11 |  |  |  | release |
| WMK-04 | §31.18 Performance | A | P1 |  | OVL-E8..E11 |  |  |  | release |
| WMK-05 | §31.18 Performance | A | **P0** |  | OVL-E8..E11 |  |  |  | release |
| WMK-06 | §31.18 Performance | A | **P0** |  | OVL-E8..E11 |  |  |  | release |
| WMK-07 | §31.18 Performance | N | — |  | OVL-E8..E11 |  |  |  | none |
| CTL-01 | §31.19 Control plane and admin | A | **P0** |  | LIF-E4..E6 · isolation |  |  |  | release |
| CTL-02 | §31.19 Control plane and admin | A | **P0** |  | LIF-E4..E6 · isolation |  |  |  | release |
| CTL-03 | §31.19 Control plane and admin | A | P0 |  | LIF-E4..E6 · isolation |  |  |  | release |
| CTL-04 | §31.19 Control plane and admin | A | P0 |  | LIF-E4..E6 · isolation |  |  |  | release |
| CTL-05 | §31.19 Control plane and admin | A | P1 |  | LIF-E4..E6 · isolation |  |  |  | release |
| CTL-06 | §31.19 Control plane and admin | A | P1 |  | LIF-E4..E6 · isolation |  |  |  | release |
| CTL-07 | §31.19 Control plane and admin | A | P1 |  | LIF-E4..E6 · isolation |  |  |  | release |
| CTL-08 | §31.19 Control plane and admin | A | P1 |  | LIF-E4..E6 · isolation |  |  |  | release |
| CTL-09 | §31.19 Control plane and admin | A | P0 |  | LIF-E4..E6 · isolation |  |  |  | release |
| CTL-14 | §31.19 Control plane and admin | A | **P0** |  | LIF-E4..E6 · isolation |  |  |  | release |
| CTL-15 | §31.19 Control plane and admin | A | **P0** |  | LIF-E4..E6 · isolation |  |  |  | release |
| CTL-10 | §31.19 Control plane and admin | A | P0 |  | LIF-E4..E6 · isolation |  |  |  | release |
| CTL-11 | §31.19 Control plane and admin | A | P0 |  | LIF-E4..E6 · isolation |  |  |  | release |
| CTL-12 | §31.19 Control plane and admin | A | P1 |  | LIF-E4..E6 · isolation |  |  |  | release |
| CTL-13 | §31.19 Control plane and admin | A | P0 |  | LIF-E4..E6 · isolation |  |  |  | release |
| WID-01 | §31.20 New widgets | A | P1 |  | — |  |  |  | release |
| WID-02 | §31.20 New widgets | A | P2 |  | — |  |  |  | none |
| WID-03 | §31.20 New widgets | A | P1 |  | — |  |  |  | release |
| WID-04 | §31.20 New widgets | A | P2 |  | — |  |  |  | none |
| WID-05 | §31.20 New widgets | A | P2 |  | — |  |  |  | none |
| WID-06 | §31.20 New widgets | A | P2 |  | — |  |  |  | none |
| WID-07 | §31.20 New widgets | A | P2 |  | — |  |  |  | none |
| COS-01 | §31.21 Co-Stream Room | A | P1 |  | — |  |  |  | release |
| COS-02 | §31.21 Co-Stream Room | A | P1 |  | — |  |  |  | release |
| COS-03 | §31.21 Co-Stream Room | A | P1 |  | — |  |  |  | release |
| COS-04 | §31.21 Co-Stream Room | A | P2 |  | — |  |  |  | none |
| COS-05 | §31.21 Co-Stream Room | A | P1 |  | — |  |  |  | release |
| COS-06 | §31.21 Co-Stream Room | A | P1 |  | — |  |  |  | release |
| COS-07 | §31.21 Co-Stream Room | A | P1 |  | — |  |  |  | release |
| COS-08 | §31.21 Co-Stream Room | A | P2 |  | — |  |  |  | none |
| COS-09 | §31.21 Co-Stream Room | A | P1 |  | — |  |  |  | release |
| COS-10 | §31.21 Co-Stream Room | A | P2 |  | — |  |  |  | none |
| COS-11 | §31.21 Co-Stream Room | A | P1 |  | — |  |  |  | release |
| COS-12 | §31.21 Co-Stream Room | A | P1 |  | — |  |  |  | release |
| COS-13 | §31.21 Co-Stream Room | A | P1 |  | — |  |  |  | release |
| COS-14 | §31.21 Co-Stream Room | A | P2 |  | — |  |  |  | none |
| COS-15 | §31.21 Co-Stream Room | N | — |  | — |  |  |  | none |
| SND-01 | §31.22 Sound Moments and Rules Engine | A | P1 |  | — |  |  |  | release |
| SND-02 | §31.22 Sound Moments and Rules Engine | A | P1 |  | — |  |  |  | release |
| SND-03 | §31.22 Sound Moments and Rules Engine | A | P1 |  | — |  |  |  | release |
| SND-04 | §31.22 Sound Moments and Rules Engine | A | P1 |  | — |  |  |  | release |
| SND-05 | §31.22 Sound Moments and Rules Engine | A | P2 |  | — |  |  |  | none |
| SND-06 | §31.22 Sound Moments and Rules Engine | P | P1 |  | — |  |  |  | release |
| SND-07 | §31.22 Sound Moments and Rules Engine | A | P0 |  | — |  |  |  | release |
| RUL-01 | §31.22 Sound Moments and Rules Engine | A | P1 |  | — |  |  |  | release |
| RUL-02 | §31.22 Sound Moments and Rules Engine | A | P1 |  | — |  |  |  | release |
| RUL-03 | §31.22 Sound Moments and Rules Engine | P | P1 |  | — |  |  |  | release |
| SEC-01 | §31.22 Sound Moments and Rules Engine | A | **P0** |  | — |  |  |  | release |
| SEC-02 | §31.22 Sound Moments and Rules Engine | A | P1 |  | — |  |  |  | release |
| SEC-03 | §31.22 Sound Moments and Rules Engine | P | P1 |  | — |  |  |  | release |
| MIG-01 | §31.22 Sound Moments and Rules Engine | A | P1 |  | — |  |  |  | release |
| MIG-02 | §31.22 Sound Moments and Rules Engine | A | P1 |  | — |  |  |  | release |
| MIG-03 | §31.22 Sound Moments and Rules Engine | A | P0 |  | — |  |  |  | release |
| RTE-01 | §31.24 Payment routing | A | P1 |  | none — phase R or blocked |  |  |  | release |
| RTE-02 | §31.24 Payment routing | A | P1 |  | none — phase R or blocked |  |  |  | release |
| RTE-03 | §31.24 Payment routing | A | P1 |  | none — phase R or blocked |  |  |  | release |
| RTE-04 | §31.24 Payment routing | A | P1 |  | none — phase R or blocked |  |  |  | release |
| RTE-05 | §31.24 Payment routing | A | P1 |  | none — phase R or blocked |  |  |  | release |
| RTE-06 | §31.24 Payment routing | A | P1 |  | none — phase R or blocked |  |  |  | release |
| RTE-07 | §31.24 Payment routing | A | P1 |  | none — phase R or blocked |  |  |  | release |
| RTE-08 | §31.24 Payment routing | A | P2 |  | none — phase R or blocked |  |  |  | none |
| RTE-09 | §31.24 Payment routing | B | P2 |  | none — phase R or blocked |  |  |  | none |
| RTE-10 | §31.24 Payment routing | B | P3 |  | none — phase R or blocked |  |  |  | none |
| RTE-11 | §31.24 Payment routing | B | P2 |  | none — phase R or blocked |  |  |  | none |
| RTE-12 | §31.24 Payment routing | B | P2 |  | none — phase R or blocked |  |  |  | none |
| RTE-13 | §31.24 Payment routing | N | — |  | none — phase R or blocked |  |  |  | none |
| RTE-14 | §31.24 Payment routing | N | — |  | none — phase R or blocked |  |  |  | none |
| RTE-15 | §31.24 Payment routing | A | P2 |  | none — phase R or blocked |  |  |  | none |
| RTE-16 | §31.24 Payment routing | A | P2 |  | none — phase R or blocked |  |  |  | none |
| RTE-17 | §31.24 Payment routing | A | P2 |  | none — phase R or blocked |  |  |  | none |
| LIF-01 | §31.25 Subscription lifecycle | A | P1 |  | LIF-E1..E3 · DSH-E4 · durable-record access |  |  |  | release |
| LIF-02 | §31.25 Subscription lifecycle | A | P1 |  | LIF-E1..E3 · DSH-E4 · durable-record access |  |  |  | release |
| LIF-03 | §31.25 Subscription lifecycle | A | P1 |  | LIF-E1..E3 · DSH-E4 · durable-record access |  |  |  | release |
| LIF-04 | §31.25 Subscription lifecycle | A | P1 |  | LIF-E1..E3 · DSH-E4 · durable-record access |  |  |  | release |
| LIF-05 | §31.25 Subscription lifecycle | A | P1 |  | LIF-E1..E3 · DSH-E4 · durable-record access |  |  |  | release |
| LIF-06 | §31.25 Subscription lifecycle | A | **P1** |  | LIF-E1..E3 · DSH-E4 · durable-record access |  |  |  | release |
| LIF-07 | §31.25 Subscription lifecycle | A | P1 |  | LIF-E1..E3 · DSH-E4 · durable-record access |  |  |  | release |
| LIF-08 | §31.25 Subscription lifecycle | A | P1 |  | LIF-E1..E3 · DSH-E4 · durable-record access |  |  |  | release |
| LIF-09 | §31.25 Subscription lifecycle | A | P2 |  | LIF-E1..E3 · DSH-E4 · durable-record access |  |  |  | none |
| LIF-10 | §31.25 Subscription lifecycle | P | P0 |  | LIF-E1..E3 · DSH-E4 · durable-record access |  |  |  | release |
| SOC-01 | §31.26 Social Relay | A | P2 |  | none — phase R or blocked |  |  |  | none |
| SOC-02 | §31.26 Social Relay | A | P2 |  | none — phase R or blocked |  |  |  | none |
| SOC-03 | §31.26 Social Relay | A | P2 |  | none — phase R or blocked |  |  |  | none |
| SOC-04 | §31.26 Social Relay | A | P2 |  | none — phase R or blocked |  |  |  | none |
| SOC-05 | §31.26 Social Relay | A | P2 |  | none — phase R or blocked |  |  |  | none |
| SOC-06 | §31.26 Social Relay | A | P2 |  | none — phase R or blocked |  |  |  | none |
| SOC-07 | §31.26 Social Relay | A | P2 |  | none — phase R or blocked |  |  |  | none |
| SOC-08 | §31.26 Social Relay | A | P3 |  | none — phase R or blocked |  |  |  | none |
| SOC-09 | §31.26 Social Relay | A | P3 |  | none — phase R or blocked |  |  |  | none |
| SOC-10 | §31.26 Social Relay | A | P3 |  | none — phase R or blocked |  |  |  | none |
| SOC-11 | §31.26 Social Relay | A | P3 |  | none — phase R or blocked |  |  |  | none |
| SOC-12 | §31.26 Social Relay | A | P3 |  | none — phase R or blocked |  |  |  | none |
| SOC-13 | §31.26 Social Relay | A | P3 |  | none — phase R or blocked |  |  |  | none |
| SOC-14 | §31.26 Social Relay | A | P2 |  | none — phase R or blocked |  |  |  | none |
| SOC-15 | §31.26 Social Relay | A | P2 |  | none — phase R or blocked |  |  |  | none |
| SOC-16 | §31.26 Social Relay | N | — |  | none — phase R or blocked |  |  |  | none |
| SOC-17 | §31.26 Social Relay | N | — |  | none — phase R or blocked |  |  |  | none |
| PCK-01 | §31.27 Packs and creator-ops | A | P2 |  | LIF-E1..E3 · DSH-E4 |  |  |  | none |
| PCK-02 | §31.27 Packs and creator-ops | A | P1 |  | LIF-E1..E3 · DSH-E4 |  |  |  | release |
| PCK-03 | §31.27 Packs and creator-ops | A | P2 |  | LIF-E1..E3 · DSH-E4 |  |  |  | none |
| PCK-04 | §31.27 Packs and creator-ops | A | P2 |  | LIF-E1..E3 · DSH-E4 |  |  |  | none |
| PCK-05 | §31.27 Packs and creator-ops | A | P2 |  | LIF-E1..E3 · DSH-E4 |  |  |  | none |
| PCK-06 | §31.27 Packs and creator-ops | A | P2 |  | LIF-E1..E3 · DSH-E4 |  |  |  | none |
| PCK-07 | §31.27 Packs and creator-ops | A | P2 |  | LIF-E1..E3 · DSH-E4 |  |  |  | none |
| PCK-08 | §31.27 Packs and creator-ops | A | P3 |  | LIF-E1..E3 · DSH-E4 |  |  |  | none |
| PCK-09 | §31.27 Packs and creator-ops | A | **P1** |  | LIF-E1..E3 · DSH-E4 |  |  |  | release |
| PCK-10 | §31.27 Packs and creator-ops | A | P3 |  | LIF-E1..E3 · DSH-E4 |  |  |  | none |
| PCK-11 | §31.27 Packs and creator-ops | A | P2 |  | LIF-E1..E3 · DSH-E4 |  |  |  | none |
| PCK-12 | §31.27 Packs and creator-ops | A | **P0** |  | LIF-E1..E3 · DSH-E4 |  |  |  | release |
| PCK-13 | §31.27 Packs and creator-ops | A | P2 |  | LIF-E1..E3 · DSH-E4 |  |  |  | none |
| PCK-14 | §31.27 Packs and creator-ops | A | P2 |  | LIF-E1..E3 · DSH-E4 |  |  |  | none |
| PCK-15 | §31.27 Packs and creator-ops | A | P3 |  | LIF-E1..E3 · DSH-E4 |  |  |  | none |
| JOB-01 | §31.27 Packs and creator-ops | A | P2 |  | — |  |  |  | none |
| JOB-02 | §31.27 Packs and creator-ops | A | P3 |  | — |  |  |  | none |
| JOB-03 | §31.27 Packs and creator-ops | A | P2 |  | — |  |  |  | none |
| JOB-04 | §31.27 Packs and creator-ops | A | P3 |  | — |  |  |  | none |
| JOB-05 | §31.27 Packs and creator-ops | A | P3 |  | — |  |  |  | none |
| JOB-06 | §31.27 Packs and creator-ops | A | P3 |  | — |  |  |  | none |
| JOB-07 | §31.27 Packs and creator-ops | A | P3 |  | — |  |  |  | none |
| JOB-08 | §31.27 Packs and creator-ops | A | P3 |  | — |  |  |  | none |
| JOB-09 | §31.27 Packs and creator-ops | A | P3 |  | — |  |  |  | none |
| JOB-10 | §31.27 Packs and creator-ops | N | — |  | — |  |  |  | none |
| JOB-11 | §31.27 Packs and creator-ops | N | — |  | — |  |  |  | none |
| INT-01 | §31.28 Interop, packages and bridges (§9) | A | P2 |  | INT-E1..E7 · package fuzz corpus |  |  |  | none |
| INT-02 | §31.28 Interop, packages and bridges (§9) | A | P2 |  | INT-E1..E7 · package fuzz corpus |  |  |  | none |
| INT-03 | §31.28 Interop, packages and bridges (§9) | A | P2 |  | INT-E1..E7 · package fuzz corpus |  |  |  | none |
| INT-04 | §31.28 Interop, packages and bridges (§9) | A | P2 |  | INT-E1..E7 · package fuzz corpus |  |  |  | none |
| INT-05 | §31.28 Interop, packages and bridges (§9) | A | P2 |  | INT-E1..E7 · package fuzz corpus |  |  |  | none |
| INT-06 | §31.28 Interop, packages and bridges (§9) | A | P2 |  | INT-E1..E7 · package fuzz corpus |  |  |  | none |
| INT-07 | §31.28 Interop, packages and bridges (§9) | A | P2 |  | INT-E1..E7 · package fuzz corpus |  |  |  | none |
| INT-08 | §31.28 Interop, packages and bridges (§9) | A | P2 |  | INT-E1..E7 · package fuzz corpus |  |  |  | none |
| INT-09 | §31.28 Interop, packages and bridges (§9) | A | P2 |  | INT-E1..E7 · package fuzz corpus |  |  |  | none |
| INT-10 | §31.28 Interop, packages and bridges (§9) | A | P2 |  | INT-E1..E7 · package fuzz corpus |  |  |  | none |
| INT-11 | §31.28 Interop, packages and bridges (§9) | A | **P0 rule, P2 build** |  | INT-E1..E7 · package fuzz corpus |  |  |  | none |
| INT-12 | §31.28 Interop, packages and bridges (§9) | A | P3 |  | INT-E1..E7 · package fuzz corpus |  |  |  | none |
| INT-13 | §31.28 Interop, packages and bridges (§9) | A | P3 |  | INT-E1..E7 · package fuzz corpus |  |  |  | none |
| INT-14 | §31.28 Interop, packages and bridges (§9) | A | P3 |  | INT-E1..E7 · package fuzz corpus |  |  |  | none |
| INT-15 | §31.28 Interop, packages and bridges (§9) | A | P3 |  | INT-E1..E7 · package fuzz corpus |  |  |  | none |
| INT-16 | §31.28 Interop, packages and bridges (§9) | A | P3 |  | INT-E1..E7 · package fuzz corpus |  |  |  | none |
| INT-17 | §31.28 Interop, packages and bridges (§9) | B | — |  | INT-E1..E7 · package fuzz corpus |  |  |  | none |
| INT-18 | §31.28 Interop, packages and bridges (§9) | B | — |  | INT-E1..E7 · package fuzz corpus |  |  |  | none |
| INT-19 | §31.28 Interop, packages and bridges (§9) | A | **P0** |  | INT-E1..E7 · package fuzz corpus |  |  |  | release |
| INT-20 | §31.28 Interop, packages and bridges (§9) | N | — |  | INT-E1..E7 · package fuzz corpus |  |  |  | none |
| CST-01 | §31.29 Customisation depth by tier (§15.4) | A | P1 |  | OVL-E1..E12 · HUB-E1..E5 · accessibility · +40% expansion |  |  |  | release |
| CST-02 | §31.29 Customisation depth by tier (§15.4) | A | **P0** |  | OVL-E1..E12 · HUB-E1..E5 · accessibility · +40% expansion |  |  |  | release |
| CST-03 | §31.29 Customisation depth by tier (§15.4) | A | P1 |  | OVL-E1..E12 · HUB-E1..E5 · accessibility · +40% expansion |  |  |  | release |
| CST-04 | §31.29 Customisation depth by tier (§15.4) | A | P1 |  | OVL-E1..E12 · HUB-E1..E5 · accessibility · +40% expansion |  |  |  | release |
| CST-05 | §31.29 Customisation depth by tier (§15.4) | A | P1 |  | OVL-E1..E12 · HUB-E1..E5 · accessibility · +40% expansion |  |  |  | release |
| CST-06 | §31.29 Customisation depth by tier (§15.4) | A | P2 |  | OVL-E1..E12 · HUB-E1..E5 · accessibility · +40% expansion |  |  |  | none |
| CST-07 | §31.29 Customisation depth by tier (§15.4) | A | P2 |  | OVL-E1..E12 · HUB-E1..E5 · accessibility · +40% expansion |  |  |  | none |
| CST-08 | §31.29 Customisation depth by tier (§15.4) | A | P2 |  | OVL-E1..E12 · HUB-E1..E5 · accessibility · +40% expansion |  |  |  | none |
| CST-09 | §31.29 Customisation depth by tier (§15.4) | A | P2 |  | OVL-E1..E12 · HUB-E1..E5 · accessibility · +40% expansion |  |  |  | none |
| CST-10 | §31.29 Customisation depth by tier (§15.4) | A | P2 |  | OVL-E1..E12 · HUB-E1..E5 · accessibility · +40% expansion |  |  |  | none |
| CST-11 | §31.29 Customisation depth by tier (§15.4) | A | P1 |  | OVL-E1..E12 · HUB-E1..E5 · accessibility · +40% expansion |  |  |  | release |
| CST-12 | §31.29 Customisation depth by tier (§15.4) | A | P3 |  | OVL-E1..E12 · HUB-E1..E5 · accessibility · +40% expansion |  |  |  | none |
| CST-13 | §31.29 Customisation depth by tier (§15.4) | A | P3 |  | OVL-E1..E12 · HUB-E1..E5 · accessibility · +40% expansion |  |  |  | none |
| CST-14 | §31.29 Customisation depth by tier (§15.4) | A | P1 |  | OVL-E1..E12 · HUB-E1..E5 · accessibility · +40% expansion |  |  |  | release |
| CST-15 | §31.29 Customisation depth by tier (§15.4) | A | P2 |  | OVL-E1..E12 · HUB-E1..E5 · accessibility · +40% expansion |  |  |  | none |
| CST-16 | §31.29 Customisation depth by tier (§15.4) | A | P3 |  | OVL-E1..E12 · HUB-E1..E5 · accessibility · +40% expansion |  |  |  | none |
| CST-17 | §31.29 Customisation depth by tier (§15.4) | A | P2 |  | OVL-E1..E12 · HUB-E1..E5 · accessibility · +40% expansion |  |  |  | none |
| CST-18 | §31.29 Customisation depth by tier (§15.4) | A | P1 |  | OVL-E1..E12 · HUB-E1..E5 · accessibility · +40% expansion |  |  |  | release |
| CST-19 | §31.29 Customisation depth by tier (§15.4) | A | P2 |  | OVL-E1..E12 · HUB-E1..E5 · accessibility · +40% expansion |  |  |  | none |
| CST-20 | §31.29 Customisation depth by tier (§15.4) | A | P3 |  | OVL-E1..E12 · HUB-E1..E5 · accessibility · +40% expansion |  |  |  | none |
| CST-21 | §31.29 Customisation depth by tier (§15.4) | A | P2 |  | OVL-E1..E12 · HUB-E1..E5 · accessibility · +40% expansion |  |  |  | none |
| CST-22 | §31.29 Customisation depth by tier (§15.4) | A | P2 |  | OVL-E1..E12 · HUB-E1..E5 · accessibility · +40% expansion |  |  |  | none |
| CST-23 | §31.29 Customisation depth by tier (§15.4) | A | P3 |  | OVL-E1..E12 · HUB-E1..E5 · accessibility · +40% expansion |  |  |  | none |
| CST-24 | §31.29 Customisation depth by tier (§15.4) | A | **P0 rule** |  | OVL-E1..E12 · HUB-E1..E5 · accessibility · +40% expansion |  |  |  | none |
| CST-25 | §31.29 Customisation depth by tier (§15.4) | A | P2 |  | OVL-E1..E12 · HUB-E1..E5 · accessibility · +40% expansion |  |  |  | none |
| CST-26 | §31.29 Customisation depth by tier (§15.4) | A | P1 |  | OVL-E1..E12 · HUB-E1..E5 · accessibility · +40% expansion |  |  |  | release |
| CST-27 | §31.29 Customisation depth by tier (§15.4) | A | P3 |  | OVL-E1..E12 · HUB-E1..E5 · accessibility · +40% expansion |  |  |  | none |
| CST-28 | §31.29 Customisation depth by tier (§15.4) | A | P2 |  | OVL-E1..E12 · HUB-E1..E5 · accessibility · +40% expansion |  |  |  | none |
| CST-29 | §31.29 Customisation depth by tier (§15.4) | A | **P0 rule** |  | OVL-E1..E12 · HUB-E1..E5 · accessibility · +40% expansion |  |  |  | none |
| CST-30 | §31.29 Customisation depth by tier (§15.4) | A | P1 |  | OVL-E1..E12 · HUB-E1..E5 · accessibility · +40% expansion |  |  |  | release |
| BOT-01 | §31.30 BharatStudio Bot (§36) | A | P2 |  | BOT-E1..E5 · rate-limit compliance · shared corpus with TTS |  |  |  | none |
| BOT-02 | §31.30 BharatStudio Bot (§36) | A | P2 |  | BOT-E1..E5 · rate-limit compliance · shared corpus with TTS |  |  |  | none |
| BOT-03 | §31.30 BharatStudio Bot (§36) | A | P2 |  | BOT-E1..E5 · rate-limit compliance · shared corpus with TTS |  |  |  | none |
| BOT-04 | §31.30 BharatStudio Bot (§36) | A | P2 |  | BOT-E1..E5 · rate-limit compliance · shared corpus with TTS |  |  |  | none |
| BOT-05 | §31.30 BharatStudio Bot (§36) | A | P2 |  | BOT-E1..E5 · rate-limit compliance · shared corpus with TTS |  |  |  | none |
| BOT-06 | §31.30 BharatStudio Bot (§36) | A | **P0 with TTS-06** |  | BOT-E1..E5 · rate-limit compliance · shared corpus with TTS |  |  |  | none |
| BOT-07 | §31.30 BharatStudio Bot (§36) | A | P2 |  | BOT-E1..E5 · rate-limit compliance · shared corpus with TTS |  |  |  | none |
| BOT-08 | §31.30 BharatStudio Bot (§36) | A | P2 |  | BOT-E1..E5 · rate-limit compliance · shared corpus with TTS |  |  |  | none |
| BOT-09 | §31.30 BharatStudio Bot (§36) | N | — |  | BOT-E1..E5 · rate-limit compliance · shared corpus with TTS |  |  |  | none |
| BOT-10 | §31.30 BharatStudio Bot (§36) | A | P3 |  | BOT-E1..E5 · rate-limit compliance · shared corpus with TTS |  |  |  | none |
| BOT-11 | §31.30 BharatStudio Bot (§36) | A | P2 |  | BOT-E1..E5 · rate-limit compliance · shared corpus with TTS |  |  |  | none |
| BOT-12 | §31.30 BharatStudio Bot (§36) | A | P2 |  | BOT-E1..E5 · rate-limit compliance · shared corpus with TTS |  |  |  | none |
| BOT-13 | §31.30 BharatStudio Bot (§36) | A | P3 |  | BOT-E1..E5 · rate-limit compliance · shared corpus with TTS |  |  |  | none |
| BOT-14 | §31.30 BharatStudio Bot (§36) | A | P3 |  | BOT-E1..E5 · rate-limit compliance · shared corpus with TTS |  |  |  | none |
| BOT-15 | §31.30 BharatStudio Bot (§36) | A | P2 |  | BOT-E1..E5 · rate-limit compliance · shared corpus with TTS |  |  |  | none |
| BOT-16 | §31.30 BharatStudio Bot (§36) | A | P2 |  | BOT-E1..E5 · rate-limit compliance · shared corpus with TTS |  |  |  | none |
| BOT-17 | §31.30 BharatStudio Bot (§36) | B | — |  | BOT-E1..E5 · rate-limit compliance · shared corpus with TTS |  |  |  | none |
| STO-01 | §31.31 Storage and media platform | A | **P0 for audio** |  | INT-E4 · asset serving · takedown drill |  |  |  | none |
| STO-02 | §31.31 Storage and media platform | A | P0 |  | INT-E4 · asset serving · takedown drill |  |  |  | release |
| STO-03 | §31.31 Storage and media platform | A | P1 |  | INT-E4 · asset serving · takedown drill |  |  |  | release |
| STO-04 | §31.31 Storage and media platform | A | P2 |  | INT-E4 · asset serving · takedown drill |  |  |  | none |
| STO-05 | §31.31 Storage and media platform | A | P1 |  | INT-E4 · asset serving · takedown drill |  |  |  | release |

## Areas

| Prefix | Rows |
|---|---:|
| ADM | 9 |
| ALQ | 19 |
| AUD | 11 |
| BOT | 17 |
| CHL | 8 |
| CMP | 93 |
| CON | 22 |
| COS | 15 |
| CST | 30 |
| CTL | 15 |
| CUS | 6 |
| ENG | 24 |
| ENT | 9 |
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
| RT | 13 |
| RTE | 17 |
| RUL | 3 |
| SEC | 3 |
| SND | 7 |
| SOC | 17 |
| STO | 5 |
| TRN | 6 |
| TTS | 17 |
| VID | 22 |
| WID | 7 |
| WMK | 7 |
