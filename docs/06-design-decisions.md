---
doc_id: CVC-DEC-001
title: CulvertCrawl design decisions register
project: CulvertCrawl
doc_type: Design decisions register
version: "0.1"
status: Draft
date: '2026-09-30'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-30'
  author: Amish Chadha
  change: Register opened with the open decisions from the review note, the decision records and the build plan work
---

# CulvertCrawl design decisions register

Every design decision still to be made, and every decision made, in one place. Each decision is argued in full in its decision record under `docs/decisions/`; this register is the index Amish works from. The build plan (`docs/05-build-plan.md`) describes the design as it stands and does not list open decisions.

## Open decisions

| # | Decision needed | Options | Recommendation | Affects in the build | Source |
| --- | --- | --- | --- | --- | --- |
| 1 | Accept the design-for-construction changes P1 to P14 | Accept all; accept some and revisit others | Accept all | The whole build plan follows them | CVC-DDR-003, Table 1 |
| 2 | Budget: the priced BOM is $1,034 against $910 (R12 not met) | (a) raise `budget_usd` to about $1,040; (b) keep $910 and look for savings; (c) keep $910 and accept R12 not met until real quotes exist | (a) | Nothing in the build; it decides whether the plan can be bought as written | CVC-DDR-003, A1 |
| 3 | Removable laser boom for tight or bent pipes (it overhangs the tracks by about 300 mm) | (a) two bolts at the fin bracket, as modelled; (b) a tool-free clamp | (a) for the prototype; decide (b) after the first pipe trials | Fin bracket (build plan section 3.9) | CVC-DDR-001 item 11; CVC-DDR-002 item 6; CVC-DDR-003, A2 |
| 4 | Accept the fin's shadow at the invert (6.4 % of the ring in 300 mm pipe) | (a) accept; (b) move the fin off the vertical | (a) | Fin and bracket | CVC-DDR-003, A3 |
| 5 | Accept the 0.86 kg heavier crawler | (a) accept; (b) thin the ballast plate to 12 mm | (a) | Ballast plate | CVC-DDR-003, A4 |
| 6 | Which output users need first: a PACP-style observation log, FHWA condition ratings or a deflection report | Any one of the three first | None made | Software only; not part of the TRL 3 build | CVC-DDR-001 item 9; CVC-DDR-002 item 4 |
| 7 | First partner user group for field trials | County road department, watershed group or university transportation program | None made | Not part of the TRL 3 build | CVC-DDR-001 item 10; CVC-DDR-002 item 5 |
| 8 | Appearance model differences from `model.py` (lid status light, render layout of the control case) | Keep for the renders only, or add to the model | Status light: renders only; case position: render layout only | None | Review note, 2026-09-26, items 3 and 5 |

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

## Decisions made

| Date | Decision | Decided by | Record |
| --- | --- | --- | --- |
| 2026-09-25 | TRL 2 review items 1 to 8: budget $900, pipe range 300 to 900 mm, 12.8 V LiFePO4 surface battery, tracks, 48 V surface power, Class 2 laser ring and fisheye camera, processing on the laptop, pitch unchanged | Amish: "proceed with all of your recommendations across all batches. Make sure we don't proceed to TRL 4 on any of them." | CVC-DDR-001 |
| 2026-09-25 | Heavier ballast plate for reach (R2), with upstream entry in flooded pipes as operating guidance; ring plane moved to 300 mm ahead (R5); the $1 overrun accepted | Amish: "i accept all your recommendations, go with them across all repos." | CVC-DDR-002 |
| 2026-09-26 | Budget set to $910 to cover the then priced BOM ($906) | Amish: "i approve all the budget items." | CVC-DDR-002 v0.2 |
| 2026-09-30 | Make the design physically buildable while drawing the build plan; changes recorded in CVC-DDR-003 and open for review (open decision 1) | Amish: "If you are realising that the design cannot be built as per concept - fix the design assumptions to match and be physically feasible as you draw the illustrations." | CVC-DDR-003 |
| 2026-09-30 | Outstanding decisions are kept in this register, not in the build plan | Amish: "don't log outstanding decisions in this build plan - that is not the place for it. that should be in a separate design document logged and named as such" | STANDARDS section 18 |
