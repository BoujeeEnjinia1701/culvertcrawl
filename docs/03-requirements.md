---
doc_id: CVC-REQ-001
title: CulvertCrawl requirements
project: CulvertCrawl
doc_type: Requirements
version: "0.4"
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
- version: "0.4"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002)
---

# CulvertCrawl requirements

These requirements were checked by calculation at TRL 3 in CVC-CAL-001 v0.2 (`docs/04-calcs/01-sizing.md`). After the design changes Amish accepted on 2026-09-25 (CVC-DDR-002: 0.46 kg more ballast and the laser ring plane moved to 300 mm ahead), R2 and R5 are met on paper with thin margins, and only R12 is not met (by $6, of which Amish accepted $1 as within pricing uncertainty). Targets are still to be validated with users (see CVC-PRB-001). The budget in R12 and the pipe range in R1 and R5 were decided by Amish on 2026-09-25 (CVC-DDR-001). The status column is a calculated estimate, not a measurement.

The **design case** used throughout is a straight 600 mm (24 in) corrugated steel culvert, 50 m long, on a 5 % slope, with a wet silt invert and up to 150 mm of water flowing at 0.5 m/s. Unless stated, the crawler enters at the outlet and drives uphill against the flow, the worst direction. In 150 mm of water the 106 mm crawler is fully submerged. As operating guidance (CVC-DDR-002), crews should enter flooded pipes from the upstream end where access allows; the design case keeps the worst direction.

## Requirements

| ID | Requirement | Target | Verification (TRL 3 or later) | Status (CVC-CAL-001) |
| --- | --- | --- | --- | --- |
| R1 | Fit the target pipes | Drive in round pipes of 300 to 900 mm (12 to 36 in) inside diameter; crawler no wider than 180 mm and no taller than 140 mm | Model check in 300 mm and 900 mm pipe sections | Met (170 x 106 mm, 610 mm long; 50 mm or more clearance) |
| R2 | Reach | Drive 50 m into the design case pipe and back, pulling the tether, with 20 % traction reserve | Traction and tether drag calculation; later pull test | Met on paper, thin margin (52 m wet and uphill; 56 m dry uphill; more than 90 m downhill); about 10 m if submerged track friction is 0.45 |
| R3 | Recover without entry | Crawler can be pulled out by the tether if disabled; tether break strength 1 kN or more, at least 5 times the worst stuck-pull estimate | Tether datasheet; pull calculation | Met (about 50 N locked-track pull, factor 20); jamming by debris not calculable |
| R4 | Video | 1080p video at 25 frames per second or more, live at the operator and recorded, with distance and time overlay; lighting to show the far wall of a 900 mm pipe | Camera and link budget; later image review | Met on paper (25 fps from a 50 fps stream, 53 % link use, about 370 lx); Pi 4 throughput not verifiable at TRL 3 |
| R5 | Cross-section profile | Measure the wall profile in the ring plane and report mean diameter and ovality (deflection) to within 1 % of nominal diameter, every 0.1 m of travel or less | Error budget; later calibration pipes | Met on paper: 0.24 % at 300 mm, 0.62 % at 600 mm, 0.97 % at 900 mm (thin margin); spacing 6 mm |
| R6 | Locate observations | Distance from the pipe mouth within 1 % or 0.2 m, whichever is larger; pitch and roll within 1 degree | Encoder and IMU datasheets | Not verifiable at TRL 3 (tether slack and wheel slip) |
| R7 | Drive in water and silt | Operate in 150 mm of water flowing at 0.5 m/s over a silt invert; survive full submersion to 1 m for 30 min (IP68 target) | Drag and buoyancy calculation; later tank test | At risk: holds in the flow on paper; IP68 not verifiable at TRL 3 |
| R8 | Climb | Hold position on a 5 % slope with power off; cross a 40 mm step or joint offset | Worm gear self-locking; track geometry | At risk: hold met; step limit between 35 and 53 mm |
| R9 | Endurance | 4 h or more of mixed driving and profiling per charge | Energy budget | Met (6.4 h nominal, 5.1 h derated) |
| R10 | Portable and quick | Whole kit 25 kg or less, no single case over 10 kg, carried by two people in one trip; set up from vehicle to driving in 10 min or less | Mass estimate; setup sequence | Met on mass (18.1 kg; heaviest case 6.3 kg); setup time not verifiable at TRL 3 |
| R11 | Electrical and laser safety | Tether and crawler 48 V DC nominal (below the 60 V DC extra-low-voltage limit), fused, with overcurrent cutoff and an emergency stop at the surface; laser Class 2 or lower under IEC 60825-1 | Design review | Met by design (10 A and 2 A fuses, 1.5 A cutoff) |
| R12 | Affordable | Full kit (crawler, 60 m tether, reel, surface box) $900 or less in parts, operator laptop excluded (decided by Amish, 2026-09-25) | Priced BOM (`bom/bom.csv`) | **Not met** ($906, $6 over). Amish accepted the first $1 as within pricing uncertainty, to revisit with real quotes (CVC-DDR-002); the $5 added by the DDR-002 ballast and boom is awaiting Amish |
| R13 | Open and repairable | Common parts; every tether and module joint pluggable; open file formats (MP4 video, CSV profiles, JSON observation log with PACP-style codes) | Design review | Met by design |

## Requirements not met or at risk

- **R12 is not met by $6** ($906 against $900). Amish accepted the $1 overrun at CVC-CAL-001 v0.1 as within pricing uncertainty (CVC-DDR-002); the ballast plate and longer boom he approved add $5, which is awaiting Amish (recommendation: accept on the same basis and revisit with real quotes).
- **R2 (reach) is met on paper with a thin margin.** With the ballast plate enlarged to 2.13 kg (was 1.67 kg), the fully submerged crawler reaches 52 m driving uphill against 0.5 m/s flow (was 39 m). The result is very sensitive to track friction under water: at 0.45 it falls to about 10 m. Measuring that friction is TRL 4 work and is on hold. Entering flooded pipes from the upstream end is now operating guidance.
- **R5 at 900 mm is met on paper with a thin margin.** With the ring plane 300 mm ahead (was 200 mm), the top of a 900 mm pipe is 70.1 degrees off the camera axis (was 76.5 degrees) and the vertical diameter error is 0.97 % (was 1.59 %).
- **R7 and R8 are at risk:** seals (IP68) and the 40 mm step cannot be settled on paper.
- **R6 cannot be verified at TRL 3.**

## Assumptions

- Track-to-silt friction coefficient about 0.6 and track motion resistance about 0.15 of weight; tether-to-pipe friction coefficient about 0.5.
- Crawler mass about 5.8 kg with ballast (3.05 kg net when submerged); tether about 55 g/m; both are estimates until parts are selected.
- 50 m reach covers most road crossings; 60 m of tether allows 10 m from the reel to the mouth.
- A 1 % profile accuracy resolves the roughly 5 % deflection limit used for plastic pipe acceptance with a 5 to 1 margin.
- The operator's own laptop runs the viewing and profiling software.
