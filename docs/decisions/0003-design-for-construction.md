---
doc_id: CVC-DDR-003
title: CulvertCrawl design for construction
project: CulvertCrawl
doc_type: Design decision record
version: "0.2"
status: Draft
date: '2026-10-01'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-30'
  author: Amish Chadha
  change: Changes that make the concept physically buildable, with the reason for each; made under Amish's 2026-09-30 instruction to make the design physically buildable; open for his review
- version: "0.2"
  date: '2026-10-01'
  author: Amish Chadha
  change: Budget treated as a value-engineering target
---

# 0003: Design for construction

- **Date:** 2026-09-30
- **Status:** Draft. The changes in Table 1 were made under Amish's 2026-09-30 instruction to make the design physically buildable; open for his review. The items in Table 3 are proposed, awaiting Amish.

## Context

On 2026-09-30 Amish asked for every repo to have an illustrated build plan that shows how each component is made and how it fits the next, and wrote: "If you are realising that the design cannot be built as per concept - fix the design assumptions to match and be physically feasible as you draw the illustrations." The concept model of CVC-DDR-002 showed what CulvertCrawl does, but checking it with build123d found parts that overlapped, parts with no fixing, and parts that could not be made as drawn. Table 1 lists them (P1 to P14) and what was done about each.

The changes keep what CulvertCrawl does: the same 240 x 88 x 74 mm hull, the same 170 mm width over the tracks and 106 mm height, the same camera axis, dome and fisheye camera, the same laser ring 300 mm ahead of the dome centre, the same 48 V tether, surface battery, fuses and emergency stop, and the same reel and surface box sizes. Nothing here changes the pitch or the safety case. Every change is in `cad/src/model.py`, which now runs 94 constructability checks (`python cad/src/model.py --check`): parts that must touch do touch, and parts that must stay apart do so by at least the stated clearance. All 94 pass.

## Decision

*Table 1. Changes made to the model, the BOM and the calculations.*

| # | Problem in the concept | Change made | Why this way |
| --- | --- | --- | --- |
| P1 | The lid overhung the 4 mm walls by 3 mm and had nothing to seal on or screw into: a 4 mm wall cannot carry both an O-ring groove and a tapped hole. | The hull is machined from a solid block with a rim 12 mm wide and 10 mm deep inside the top. The lid O-ring sits in a groove in the rim top (8.3 to 10.7 mm in from the outside); ten M4 screws go into the rim outside the O-ring line. The lid is now flush, 240 x 88 x 6 mm, with an M10 pressure-test plug. | A face seal inside the screw line keeps every screw hole outside the sealed space. The rim still leaves a 64 mm opening for the tray to pass. |
| P2 | The track side plates (3 mm, inside each belt) overlapped the hull walls by 2 mm, the belts ran 1 mm from the hull, and the plates had no fixing. | Belts narrowed from 40 to 36 mm with the same outer edge (85 mm from the centre line), so the width over the tracks, the contact geometry in a round pipe and every fit calculation are unchanged. A made 3 mm side plate lies flat on each hull side and ballast side, 2 mm from the belt. | The plate needs a 3 mm gap that the concept did not leave; moving the outer edge would have changed R1 and the reach figures. |
| P3 | The gearboxes passed 3 mm through the rear wall and touched the tether gland; nothing held the motors; the shafts had no seal housing. | Gearboxes sit 2 mm inside the rear wall with their output shafts 14 mm from their rear ends. Each output face sits on a 6 mm drive pad inside the side wall and is held by two M4 countersunk screws that pass through the side plate, the wall and the pad. A 16 mm counterbore in the wall's outside face holds an 8 x 16 x 5 mm double lip seal, kept in by the side plate. Small O-rings under the side plate seal the two screw holes. | The motor is fixed by its own tapped output face; the side plate does three jobs (track guard, seal retainer, screw head bearing face). |
| P4 | The 48 to 12 V converter block sat inside the motor cans; the electronics floated. | A 2 mm aluminium tray on four floor pads (M3 screws). The Pi 4 sits on 4 mm spacers; a deck on 20 mm standoffs above it carries the motor driver, the converters and the IMU. | Uses the Pi's own mounting holes; the tray is the heat path to the floor. |
| P5 | The camera sat behind a solid front wall with no fixing. | Front wall 10 mm thick with a 50 mm bore; a printed camera mount screwed to its inside face holds the board so the lens centre is at the dome centre. | The thicker wall carries the bezel screws and the dome O-ring groove. |
| P6 | The dome flange overlapped the lid lip and had no clamp; the 88 mm LED ring board floated in front of the hull. | A machined aluminium front bezel (new BOM line 14) clamps the dome flange on an O-ring with four M4 screws. Eight stock 1 W LEDs on 10 mm boards sit in pockets in its face and are potted; their leads and the laser's enter the hull through a 5 mm potted hole in the front wall. LED positions are 22.5 degrees off the vertical so none sits where the fin passes. | Stock LED boards; the bezel is also the LEDs' heat sink. Same 88 mm envelope and 106 mm height. |
| P7 | The laser boom started at the tip of the dome, touching it at a point, with no fixing and no path for the laser wires. | The boom is solvent-welded along the top edge of an 8 mm clear acrylic fin. The fin bolts with two M3 bolts to an aluminium angle bracket screwed to the nose of the ballast plate. The laser wires run down the fin's back edge. The boom starts 7 mm in front of the dome. | The fin lies in a vertical plane through the camera axis, so the camera sees it edge on; it hides 6.4 % of the ring in a 300 mm pipe and 2.1 % in a 900 mm pipe, all at the invert. Re-running the profiling Monte Carlo with the fin in place gives 0.25, 0.57 and 0.97 % of diameter at 300, 600 and 900 mm (CVC-CAL-001 v0.5): R5 is still met. |
| P8 | The cone mirror sat bare beyond the diode housing with nothing holding it. | A clear acrylic window tube and an aluminium end cap: the mirror is bonded to the cap, the window joins cap and housing, and the ring leaves through the window wall. The ring plane stays 300 mm ahead of the dome centre; the crawler is 1 mm longer (611 mm). | This is the window and end cap the appearance model proposed on 2026-09-26 (review item 1); construction needs it. |
| P9 | The ballast plate had no fixing; its turned-up lip (bending 14 mm steel) is press work, not a small-shop job, and it ran into the LED ring. | Plate 255 x 88 x 14 mm with a square nose: as wide as the hull so the side plates screw into tapped holes in its sides, and 25 mm longer at the rear for the eye bolt. About 2.45 kg (was 2.13 kg). | The side plates now tie the hull to the ballast; no hole goes through the hull floor. |
| P10 | The tether's strength member had no anchor (only the gland), and the gland collided with the gearboxes. | An M8 forged eye bolt in the rear of the ballast plate takes the aramid strength member; an M10 IP68 penetrator in the rear wall, 77 mm above the contact line (was on the camera axis at 62 mm), seals the cable and sits between the gearboxes and the rim. | Recovery pulls go to the steel plate, not to a seal. |
| P11 | The idler axle had nothing to screw into. | An M6 shoulder bolt through the idler and the side plate into a blind tapped boss inside the hull wall (2 mm of metal left). | No through hole; the belt kit's 200 mm centres set the tension. |
| P12 | Reel: the A-frame tubes clashed with the flanges; the axle had no bearings; the drum was not fixed to the flanges or the axle; the slip ring body was free to turn. | Two 6 mm aluminium side frames on three spacer tubes and M6 tie rods; two 20 mm flanged bearings; a hollow 20 mm axle (the tether's inner end runs through it to the slip ring); a 225 mm PVC drum clamped between two 6 mm HDPE flanges by four M6 tie rods; a shaft hub bolted to each flange; a crank; an M8 knob brake on the left frame; a bracket that stops the slip ring stator turning. | Every part is cut from plate, pipe or tube or bought; the 320 mm reel size is kept. |
| P13 | The payout counter floated in the air in front of the reel, and its encoder had nothing to read it. | A bar clamped between the two halves of the front spacer carries the counter; a small USB encoder reader in the counter sends the count to the laptop. | The appearance model's counter bracket (review item 4), made buildable. |
| P14 | Surface box: the battery block was taller than the case and nothing inside was fixed. | A drop-in chassis: a 6 mm plywood base board, four aluminium posts and a 2 mm aluminium panel. The battery lies on its side, strapped to the base board; the converter and monitor screw to it; the stop, fuses and connectors are on the panel, which the lid closes over with 19 mm to spare. | The bought case is not drilled, so it stays waterproof, and the whole chassis lifts out. |

*Table 2. Knock-on changes.*

| Item | Change | Reason |
| --- | --- | --- |
| Mass | Crawler 6.63 kg (was 5.77 kg), 3.77 kg net when submerged (was 3.05 kg); hull and lid 1.26 kg and ballast 2.45 kg from model volumes. Kit 22.2 kg (was 18.1 kg); heaviest item the reel with tether, 7.8 kg. R10 still met. | Rim, pads, thicker front wall, wider and longer ballast plate, side plates, bezel; reel frames and box chassis. |
| Reach | Wet uphill 75 m (was 52 m); dry uphill 64 m; 23 m if submerged track friction is 0.45 (was about 10 m). Sprocket torque at the traction limit 0.84 N·m, within the 1 N·m motor rating. Locked-track recovery pull 59 N, factor 17 on the 1 kN tether. | Heavier crawler. |
| Profiling | 0.25, 0.57 and 0.97 % of diameter at 300, 600 and 900 mm, with the fin's shadow modelled. | P7. |
| Cost | BOM 15 lines, $1,034 against the $910 value-engineering target (`budget_usd`): $124 over. R12 is over the target. `budget_usd` is not changed; cost drivers and savings are in the Value engineering section of the design decisions register. | Parts added for construction: bezel (line 14), side plates and small made parts (line 15), reel frame, bearings and counter reader (line 10, $125 to $168), box chassis (line 11, $185 to $205), hull machining (line 1, $70 to $78), laser fin, window and cap (line 7, $47 to $55), ballast (line 8, $18 to $22), deck (line 4, $110 to $113), eye bolt and screws (line 13, $30 to $40). |
| Drawings | CVC-DWG-001 Rev P3; making sketches CVC-DWG-101 to 119; concept blueprint CVC-DWG-010 Rev P2. | Follow the model. |
| Documents | CVC-CAL-001 v0.5, CVC-REQ-001 v0.7, CVC-PRC-001 v0.7. | Follow the model. |
| Thermal and power | Unchanged: the same loads, tether and battery. | |

*Table 3. Proposed, awaiting Amish.*

| # | Question | Options | Recommendation |
| --- | --- | --- | --- |
| A2 | The boom is now held by two M3 bolts at the fin bracket, so it can come off for repair. Whether it should be quick-release in the field is the open removable-boom question (CVC-DDR-002, item 6). | (a) keep the two bolts; (b) a tool-free clamp at the bracket. | (a) for the prototype; decide (b) after the first pipe trials. |
| A3 | The fin hides a strip of the ring at the invert (6.4 % of the ring in 300 mm pipe). In a dry pipe the lowest wall point is not measured; the water or sediment chord is still seen at both ends. | (a) accept; (b) move the fin off the vertical to one side. | (a): the ellipse fit and R5 are unaffected, and the invert is usually under water or silt. |
| A4 | The crawler is 0.86 kg heavier. This helps reach but raises motor torque at the traction limit from 0.73 to 0.84 N·m against the 1 N·m rating. | (a) accept; (b) thin the ballast plate to 12 mm to hold the concept mass. | (a): the margin on reach is the thinnest in the design, and the motor is still within its rating. |

## Consequences

- `design_state: constructable` in `project.yaml`. The build plan CVC-BLD-001 shows every component and step in pictures generated from the model (`cad/src/build_plan_media.py`); the open items are in the design decisions register CVC-DEC-001.
- Cost is reported against the value-engineering target: USD 910 (a hypothetical control target, not a limit) against an estimated USD 1,034 for the constructable design, USD 124 over. Savings worth trying (a bought cable reel, a printed bezel, a smaller case) are in the register.
- Requirement status (CVC-CAL-001 v0.5): 1 over its value-engineering target (R12, cost), 2 at risk (R7, R8), 1 not verifiable at TRL 3 (R6), 9 met on paper (R1, R2, R3, R4, R5, R9, R10, R11, R13); R5 at 900 mm keeps its thin margin.
- The photoreal renders (`media/render-*.png`), `media/card.png`, `media/social-preview.png` and the appearance model `cad/src/product_model.py` still show the concept lid lip, LED ring, bare cone and reel frame; they need updating on Amish's Mac, where Blender is.
- Shaft length, gearbox face holes, the belt kit's tension at 200 mm centres, the slip ring and the case's inside size are checked when parts are bought (register, "To confirm").
