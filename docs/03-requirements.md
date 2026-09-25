---
doc_id: CVC-REQ-001
title: CulvertCrawl requirements
project: CulvertCrawl
doc_type: Requirements
version: "0.2"
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
---

# CulvertCrawl requirements

These are first-pass requirements for the concept. Targets are proposals for review, not yet validated with users (see CVC-PRB-001), and will be checked by calculation at TRL 3. The status column gives the first-order result from the design precis (CVC-PRC-001); every status is an estimate.

The **design case** used throughout is a straight 600 mm (24 in) corrugated steel culvert, 50 m long, on a 5 % slope, with a wet silt invert and up to 150 mm of water flowing at 0.5 m/s.

## Requirements

| ID | Requirement | Target | Verification (TRL 3 or later) | Status (estimate) |
| --- | --- | --- | --- | --- |
| R1 | Fit the target pipes | Drive in round pipes of 300 to 900 mm (12 to 36 in) inside diameter; crawler no wider than 180 mm and no taller than 140 mm | Model check in 300 mm and 900 mm pipe sections | Met by design (170 x 125 mm) |
| R2 | Reach | Drive 50 m into the design case pipe and back, pulling the tether, with 20 % traction reserve | Traction and tether drag calculation; later pull test | Met, margin thin (about 56 m at 20 % reserve) |
| R3 | Recover without entry | Crawler can be pulled out by the tether if disabled; tether break strength 1 kN or more, at least 5 times the worst stuck-pull estimate | Tether datasheet; pull calculation | Met by specification |
| R4 | Video | 1080p video at 25 frames per second or more, live at the operator and recorded, with distance and time overlay; lighting to show the far wall of a 900 mm pipe | Camera and link budget; later image review | Met on paper; lighting in 900 mm pipe unverified |
| R5 | Cross-section profile | Measure the wall profile in the ring plane and report mean diameter and ovality (deflection) to within 1 % of nominal diameter, every 0.1 m of travel or less | Error budget; later calibration pipes | Met at 300 to 600 mm; **at risk at 900 mm** (about 1 % or worse at the top of the pipe) |
| R6 | Locate observations | Distance from the pipe mouth within 1 % or 0.2 m, whichever is larger; pitch and roll within 1 degree | Encoder and IMU datasheets | Met on paper |
| R7 | Drive in water and silt | Operate in 150 mm of water flowing at 0.5 m/s over a silt invert; survive full submersion to 1 m for 30 min (IP68 target) | Drag and buoyancy calculation; later tank test | Driving met on paper; **IP68 unverified**; traction when fully submerged is about half of dry |
| R8 | Climb | Hold position on a 5 % slope with power off; cross a 40 mm step or joint offset | Worm gear self-locking; track geometry | Hold met by design; step crossing unverified |
| R9 | Endurance | 4 h or more of mixed driving and profiling per charge | Energy budget | Met (about 6 h) |
| R10 | Portable and quick | Whole kit 25 kg or less, no single case over 10 kg, carried by two people in one trip; set up from vehicle to driving in 10 min or less | Mass estimate; setup sequence | Met on mass (about 18 kg); setup time unverified |
| R11 | Electrical and laser safety | Tether and crawler 48 V DC nominal (below the 60 V DC extra-low-voltage limit), fused, with overcurrent cutoff and an emergency stop at the surface; laser Class 2 or lower under IEC 60825-1 | Design review | Met by design |
| R12 | Affordable | Full kit (crawler, 60 m tether, reel, surface box) $800 or less in parts, operator laptop excluded | Priced BOM (`bom/bom.csv`) | **Not met** (about $900, about 13 % over) |
| R13 | Open and repairable | Common parts; every tether and module joint pluggable; open file formats (MP4 video, CSV profiles, JSON observation log with PACP-style codes) | Design review | Met by design |

## Requirements not met or at risk

- **R12 (cost) is not met.** The first priced BOM is about $900 against $800. Options are in `docs/REVIEW.md`; the budget change is proposed, awaiting Amish.
- **R5 is at risk at 900 mm.** With the laser ring 200 mm ahead of the lens, the top of a 900 mm pipe is seen about 76 degrees off the camera axis, at the edge of a fisheye lens, where 1 % is marginal.
- **R7 submersion is unverified.** IP68 to 1 m is a target for a hull with rotating shaft seals; seal leakage is the most likely failure. Laser profiling does not work below the water surface (refraction), so the profile covers only the wall above the water line.
- **R2 margin is thin.** Reach depends on tether drag; a heavier tether, bends or a corrugated invert could cut reach below 50 m.

## Assumptions

- Track-to-silt friction coefficient about 0.6 and track motion resistance about 0.15 of weight; tether-to-pipe friction coefficient about 0.5.
- Crawler mass about 5.5 kg with ballast; tether about 55 g/m; both are estimates until parts are selected.
- 50 m reach covers most road crossings; 60 m of tether allows 10 m from the reel to the mouth.
- A 1 % profile accuracy resolves the roughly 5 % deflection limit used for plastic pipe acceptance with a 5 to 1 margin.
- The operator's own laptop runs the viewing and profiling software.
