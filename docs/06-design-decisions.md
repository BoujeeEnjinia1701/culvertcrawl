---
doc_id: CVC-DEC-001
title: CulvertCrawl design decisions register
project: CulvertCrawl
doc_type: Design decisions register
version: "0.3"
status: Draft
date: '2026-10-02'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-30'
  author: Amish Chadha
  change: Register opened with the open decisions from the review note, the decision records and the build plan work
- version: "0.2"
  date: '2026-10-01'
  author: Amish Chadha
  change: Budget treated as a value-engineering target
- version: "0.3"
  date: '2026-10-02'
  author: Amish Chadha
  change: 'Amish approved the recommendations for all seven open decisions on 2026-10-02 (CVC-DDR-003 accepted); moved to decisions made'
---

# CulvertCrawl design decisions register

Every design decision still to be made, and every decision made, in one place. Each decision is argued in full in its decision record under `docs/decisions/`; this register is the index Amish works from. The build plan (`docs/05-build-plan.md`) describes the design as it stands and does not list open decisions.

## Open decisions

None. All open decisions were decided on 2026-10-02.

## To confirm when parts are bought

| # | What to confirm | Why it matters | Source |
| --- | --- | --- | --- |
| 1 | The worm gear motor's output shaft is 8 mm D and at least 38 mm long, its output face has two tapped holes, and the shaft sits about 8 mm above the gearbox base and 14 mm from its back | They set the drive pad, the seal counterbore and the side plate holes | CVC-DDR-003, P3 |
| 2 | The belt kit runs at 200 mm sprocket centres with 36 mm belts, and its sprocket can be bored 8 mm D with a set screw | There is no tensioner; the centres set the belt tension | CVC-DDR-003, P2, P11 |
| 3 | The dome's flange is 72 mm across and 5 mm thick | It sets the bezel recess and the O-ring groove | CVC-DDR-003, P6 |
| 4 | The camera board's hole pattern and the lens's position on its thread | They set the camera mount holes and put the lens centre at the dome centre | CVC-DDR-003, P5 |
| 5 | The laser module is 12 mm across and the cone mirror's base is 20 mm or less | They set the diode housing bore and fit inside the window | CVC-DDR-003, P8 |
| 6 | The slip ring has an anti-rotation tab or lead the anchor can catch, and passes 100 Mbit/s Ethernet | It sets the anchor bracket; the data link depends on it | CVC-DDR-003, P12 |
| 7 | The rugged case's inside size and moulded ribs | The chassis base board and panel must drop in with about 2 mm to spare | CVC-DDR-003, P14 |
| 8 | The battery's size laid on its side (181 x 167 x 77 mm in the model) and that its maker allows it on its side | It sets the battery bay | CVC-DDR-003, P14 |
| 9 | The tether's aramid member can be broken out and tied off at the eye bolt, and its outside diameter suits the M10 penetrator | Recovery pulls go through it | CVC-DDR-003, P10 |

## Value engineering

Value-engineering target: USD 910 (a hypothetical control target, not a limit). Estimated cost of the constructable design: USD 1,034 (USD 124 over the target). The estimate was USD 906 before the design for construction.

Main cost drivers (the parts added to make the design buildable): the reel frame, bearings, hubs and counter reader (USD 43), the front bezel and the side plates and small made parts (USD 32), the surface box chassis (USD 20), the eye bolt and screws (USD 10), the hull rim and pads (USD 8), the laser fin, window and cap (USD 8), the larger ballast plate (USD 4) and the deck (USD 3). Prices are indicative; the softest (hull, tether, cone mirror) can still move the total by USD 20 to USD 80 either way.

Savings worth trying: a bought cable reel, a printed bezel and a smaller case, then real quotes for the soft prices.

## Decisions made

| Date | Decision | Decided by | Record |
| --- | --- | --- | --- |
| 2026-09-25 | TRL 2 review items 1 to 8: budget $900, pipe range 300 to 900 mm, 12.8 V LiFePO4 surface battery, tracks, 48 V surface power, Class 2 laser ring and fisheye camera, processing on the laptop, pitch unchanged | Amish: "proceed with all of your recommendations across all batches. Make sure we don't proceed to TRL 4 on any of them." | CVC-DDR-001 |
| 2026-09-25 | Heavier ballast plate for reach (R2), with upstream entry in flooded pipes as operating guidance; ring plane moved to 300 mm ahead (R5); the $1 overrun accepted | Amish: "i accept all your recommendations, go with them across all repos." | CVC-DDR-002 |
| 2026-09-26 | Value-engineering target set to $910 to match the then priced BOM ($906) | Amish: "i approve all the budget items." | CVC-DDR-002 v0.2 |
| 2026-09-30 | Make the design physically buildable while drawing the build plan; changes recorded in CVC-DDR-003 (accepted on 2026-10-02, below) | Amish: "If you are realising that the design cannot be built as per concept - fix the design assumptions to match and be physically feasible as you draw the illustrations." | CVC-DDR-003 |
| 2026-09-30 | Outstanding decisions are kept in this register, not in the build plan | Amish: "don't log outstanding decisions in this build plan - that is not the place for it. that should be in a separate design document logged and named as such" | STANDARDS section 18 |
| 2026-10-02 | Design for construction accepted: all fourteen changes P1 to P14 and their knock-on changes, as made | Amish: "i approve your recommendations for all 555 open decisions." | CVC-DDR-003, Tables 1 and 2 |
| 2026-10-02 | Laser boom held by two M3 bolts at the fin bracket for the prototype; a tool-free clamp is to be decided after the first pipe trials | Amish: "i approve your recommendations for all 555 open decisions." | CVC-DDR-003, A2; CVC-DDR-001 item 11; CVC-DDR-002 item 6 |
| 2026-10-02 | The fin's shadow at the invert (6.4 % of the ring in 300 mm pipe) is accepted | Amish: "i approve your recommendations for all 555 open decisions." | CVC-DDR-003, A3 |
| 2026-10-02 | The 0.86 kg heavier crawler (6.63 kg) is accepted | Amish: "i approve your recommendations for all 555 open decisions." | CVC-DDR-003, A4 |
| 2026-10-02 | First output: the deflection report; second, observations logged in NASSCO PACP vocabulary; FHWA condition ratings later | Amish: "i approve your recommendations for all 555 open decisions." | CVC-DDR-001 item 9; CVC-DDR-002 item 4 |
| 2026-10-02 | First partner user group for field trials: a county road department, with a university transportation program as backup; first candidate to approach for the backup: the Texas A&M Transportation Institute | Amish: "i approve your recommendations for all 555 open decisions." | CVC-DDR-001 item 10; CVC-DDR-002 item 5 |
| 2026-10-02 | The lid status light stays in the renders only, and the control case position is render layout only; neither is added to the model | Amish: "i approve your recommendations for all 555 open decisions." | Review note, 2026-09-26, items 3 and 5 |
