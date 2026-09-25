---
doc_id: CVC-REQ-001
title: CulvertCrawl requirements
project: CulvertCrawl
doc_type: Requirements
version: "0.3"
status: Draft
date: '2026-09-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-24'
  author: Amish Chadha
  change: Initial scaffold
- version: "0.2"
  date: '2026-09-25'
  author: Amish Chadha
  change: First measurable requirements for TRL 2, with first-order status against the concept
- version: "0.3"
  date: '2026-09-25'
  author: Amish Chadha
  change: TRL 3. Record Amish's 2026-09-25 decisions (CVC-DDR-001); R12 target $900; status from CVC-CAL-001
---

# CulvertCrawl requirements

These requirements were checked by calculation at TRL 3 in CVC-CAL-001 (`docs/04-calcs/01-sizing.md`). Three are not met: R2 (reach in the wet, uphill design case), R5 at 900 mm and R12 (by $1). Targets are still to be validated with users (see CVC-PRB-001). The budget in R12 and the pipe range in R1 and R5 were decided by Amish on 2026-09-25 (CVC-DDR-001). The status column is a calculated estimate, not a measurement.

The **design case** used throughout is a straight 600 mm (24 in) corrugated steel culvert, 50 m long, on a 5 % slope, with a wet silt invert and up to 150 mm of water flowing at 0.5 m/s. Unless stated, the crawler enters at the outlet and drives uphill against the flow, the worst direction. In 150 mm of water the 106 mm crawler is fully submerged.

## Requirements

| ID | Requirement | Target | Verification (TRL 3 or later) | Status (CVC-CAL-001) |
| --- | --- | --- | --- | --- |
| R1 | Fit the target pipes | Drive in round pipes of 300 to 900 mm (12 to 36 in) inside diameter; crawler no wider than 180 mm and no taller than 140 mm | Model check in 300 mm and 900 mm pipe sections | Met (170 x 106 mm; 50 mm or more clearance) |
| R2 | Reach | Drive 50 m into the design case pipe and back, pulling the tether, with 20 % traction reserve | Traction and tether drag calculation; later pull test | **Not met** (about 39 m wet and uphill; 52 m dry uphill; more than 80 m downhill) |
| R3 | Recover without entry | Crawler can be pulled out by the tether if disabled; tether break strength 1 kN or more, at least 5 times the worst stuck-pull estimate | Tether datasheet; pull calculation | Met (about 50 N locked-track pull, factor 20); jamming by debris not calculable |
| R4 | Video | 1080p video at 25 frames per second or more, live at the operator and recorded, with distance and time overlay; lighting to show the far wall of a 900 mm pipe | Camera and link budget; later image review | Met on paper (25 fps from a 50 fps stream, 53 % link use, about 370 lx); Pi 4 throughput not verifiable at TRL 3 |
| R5 | Cross-section profile | Measure the wall profile in the ring plane and report mean diameter and ovality (deflection) to within 1 % of nominal diameter, every 0.1 m of travel or less | Error budget; later calibration pipes | Met at 300 mm (0.35 %) and 600 mm (0.87 %); **not met at 900 mm** (1.59 %); spacing 6 mm |
| R6 | Locate observations | Distance from the pipe mouth within 1 % or 0.2 m, whichever is larger; pitch and roll within 1 degree | Encoder and IMU datasheets | Not verifiable at TRL 3 (tether slack and wheel slip) |
| R7 | Drive in water and silt | Operate in 150 mm of water flowing at 0.5 m/s over a silt invert; survive full submersion to 1 m for 30 min (IP68 target) | Drag and buoyancy calculation; later tank test | At risk: holds in the flow on paper; IP68 not verifiable at TRL 3 |
| R8 | Climb | Hold position on a 5 % slope with power off; cross a 40 mm step or joint offset | Worm gear self-locking; track geometry | At risk: hold met; step limit between 35 and 53 mm |
| R9 | Endurance | 4 h or more of mixed driving and profiling per charge | Energy budget | Met (6.4 h nominal, 5.1 h derated) |
| R10 | Portable and quick | Whole kit 25 kg or less, no single case over 10 kg, carried by two people in one trip; set up from vehicle to driving in 10 min or less | Mass estimate; setup sequence | Met on mass (17.6 kg; heaviest case 6.3 kg); setup time not verifiable at TRL 3 |
| R11 | Electrical and laser safety | Tether and crawler 48 V DC nominal (below the 60 V DC extra-low-voltage limit), fused, with overcurrent cutoff and an emergency stop at the surface; laser Class 2 or lower under IEC 60825-1 | Design review | Met by design (10 A and 2 A fuses, 1.5 A cutoff) |
| R12 | Affordable | Full kit (crawler, 60 m tether, reel, surface box) $900 or less in parts, operator laptop excluded (decided by Amish, 2026-09-25) | Priced BOM (`bom/bom.csv`) | **Not met** ($901, $1 over) |
| R13 | Open and repairable | Common parts; every tether and module joint pluggable; open file formats (MP4 video, CSV profiles, JSON observation log with PACP-style codes) | Design review | Met by design |

## Requirements not met or at risk

- **R2 (reach) is not met.** Fully submerged in the design case, the crawler has half its dry traction, and driving uphill against 0.5 m/s flow it reaches about 39 m. The result is very sensitive to track friction under water. Adding about 0.40 kg of ballast, or entering from the upstream end, would meet 50 m on paper; both are proposed in `docs/REVIEW.md`, awaiting Amish.
- **R5 is not met at 900 mm.** The top of a 900 mm pipe is 76.5 degrees off the camera axis, where the fisheye is least accurate. Moving the ring plane to 300 mm ahead gives 0.97 % on paper; proposed, awaiting Amish.
- **R12 is not met by $1** ($901 against $900), inside the pricing uncertainty.
- **R7 and R8 are at risk:** seals (IP68) and the 40 mm step cannot be settled on paper.
- **R6 cannot be verified at TRL 3.**

## Assumptions

- Track-to-silt friction coefficient about 0.6 and track motion resistance about 0.15 of weight; tether-to-pipe friction coefficient about 0.5.
- Crawler mass about 5.3 kg with ballast (2.66 kg net when submerged); tether about 55 g/m; both are estimates until parts are selected.
- 50 m reach covers most road crossings; 60 m of tether allows 10 m from the reel to the mouth.
- A 1 % profile accuracy resolves the roughly 5 % deflection limit used for plastic pipe acceptance with a 5 to 1 margin.
- The operator's own laptop runs the viewing and profiling software.
