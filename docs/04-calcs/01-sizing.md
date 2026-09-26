---
doc_id: CVC-CAL-001
title: CulvertCrawl sizing calculations
project: CulvertCrawl
doc_type: Calculation note
version: "0.3"
status: Draft
date: '2026-09-26'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: First TRL 3 sizing note (fit, mass, buoyancy, traction and reach, recovery, power, profiling error, video link, thermal, cost)
- version: "0.2"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002). Ballast 230 x 80 x 14 mm; ring plane 300 mm ahead; 2,000 Monte Carlo trials; results rerun
- version: "0.3"
  date: '2026-09-26'
  author: Amish Chadha
  change: Budget approved by Amish ($900 to $910, CVC-DDR-002); script rerun; R12 not met to met
---

# CulvertCrawl sizing calculations

Version 0.2 applies the design changes Amish accepted on 2026-09-25 (CVC-DDR-002): the ballast plate grows from 210 x 80 x 12 mm to 230 x 80 x 14 mm (1.67 to 2.13 kg), and the laser ring plane moves from 200 to 300 mm ahead of the camera. On paper the crawler now fits every target pipe, reaches 52 m in the wet uphill design case (was 39 m), profiles 300 to 900 mm pipe to within 1 % of diameter (0.97 % at 900 mm, was 1.59 %), runs 6.4 h per charge and stays within safe extra-low voltage. R2 and R5 are met with thin margins. Version 0.3 records the budget Amish approved on 2026-09-26: `budget_usd` is $910, which covers the $906 priced BOM, so R12 is now met and no requirement is not met. R7 (IP68) and R8 (40 mm step) are at risk, and R6 (distance) cannot be verified until hardware exists, which is TRL 4 work and on hold by Amish's instruction.

Every number in this note is printed by `docs/04-calcs/sizing.py` (run from the repo root: `python docs/04-calcs/sizing.py`), which also writes `docs/04-calcs/results.csv`. The script reads its dimensions from `cad/src/model.py` (`PARAMS`) and the cost from `bom/bom.csv`, so the note, the model and the BOM share one source. All values are first-principles estimates; nothing here is measured.

## 1. Assumptions

*Table 1. Inputs. All are assumptions for a paper design.*

| Input | Value | Basis |
| --- | --- | --- |
| Design case | Straight 600 mm corrugated steel culvert, 50 m, 5 % grade, wet silt invert, 150 mm of water at 0.5 m/s | CVC-REQ-001 |
| Track to silt friction | 0.6, dry or submerged (sensitivity at 0.45) | Typical rubber on wet fine soil |
| Track motion resistance | 0.15 of normal load | Soft silt |
| Tether to invert friction | 0.5 | PU jacket on wet steel or silt |
| Traction reserve | 20 % | R2 |
| Tether | 7 mm OD, 55 g/m in air, 2 x 0.75 mm² class 5 copper at 26 Ω/km (IEC 60228 maximum at 20 °C) | Estimate until a cable is chosen |
| Crawler loads | Drive 12 W, LEDs 8 W, Pi, camera and network 6.5 W, laser, IMU and sensors 1.5 W; 50 W peak | TRL 2 load list, kept |
| Converters | Buck 91 %, boost 92 %; surface electronics 1 W | Datasheet class |
| Battery | 12.8 V 20 Ah LiFePO4, 90 % depth of discharge, 20 % derating for cold and ageing | Decided (CVC-DDR-001) |
| Crawler drag | Cd 1.1 on 170 x 106 mm frontal area | Bluff box |
| Camera | IMX708 at 2304 x 1296, 50 frames per second, LEDs and laser on alternate frames | Chosen here to meet R4 and R5 together |
| Lens | 180 degree equidistant circular fisheye, image circle 1296 px, so 0.139 degree per pixel | See section 6 |
| Profiling errors (1 sigma) | Ring center 0.3 px random; lens model residual 0.3 px at the image edge; ring plane tilt 0.1 degree; ring plane distance 0.3 mm; crawler yaw uniform within 2 degrees | Calibration in a reference pipe assumed |
| Ring plane | 300 mm ahead of the dome center (200 mm in v0.1) | Decided (CVC-DDR-002) |
| Ballast | Steel plate 230 x 80 x 14 mm, 8 mm above the track contact line (210 x 80 x 12 mm at 10 mm in v0.1) | Decided (CVC-DDR-002) |

## 2. Geometry and fit (R1)

The model (`cad/src/model.py`, drawing CVC-DWG-001) gives a crawler 170 mm wide over the tracks, 106 mm high over the lid screws and 610 mm long from the rear strain relief to the cone mirror (track length 270 mm); the longer laser boom adds 100 mm. The fit check below is for straight pipe; the boom overhangs the tracks by about 300 mm, so tight bends and offset joints need the removable boom question settled (still open). The outer track edges bear on the curved invert. Table 2 shows that the crawler clears the wall by at least 50 mm in every target pipe.

*Table 2. Fit in the target pipes.*

| Pipe | Track contact line above invert | Camera axis above invert | Least clearance to wall | Normal load factor |
| --- | --- | --- | --- | --- |
| 300 mm | 26.4 mm | 88.4 mm | 50 mm | 1.214 |
| 600 mm | 12.3 mm | 74.3 mm | 66 mm | 1.043 |
| 900 mm | 8.1 mm | 70.1 mm | 69 mm | 1.018 |

The track edges meet the 600 mm wall at 16.5 degrees, so the sum of the normal forces is 1.043 times the weight. This raises both traction and track resistance in proportion. The TRL 2 figure of 125 mm height is replaced by 106 mm.

## 3. Mass and buoyancy (R7, R10)

*Table 3. Crawler mass.*

| Item | Mass | Basis |
| --- | --- | --- |
| Hull and lid | 1.09 kg | Model volume, 6061 at 2.70 kg/L |
| Tracks, sprockets, side plates | 1.00 kg | Hobby track sets |
| Worm gear motors | 0.70 kg | 2 x 0.35 kg, 5840 class |
| Electronics stack | 0.20 kg | |
| Camera, dome, LED ring | 0.15 kg | |
| Laser projector and boom | 0.11 kg | 100 mm longer acrylic boom (0.10 kg in v0.1) |
| Ballast plate | 2.13 kg | Model volume, steel at 7.85 kg/L (1.67 kg in v0.1) |
| Fasteners, glands, seals, strain relief | 0.40 kg | Allowance |
| **Crawler** | **5.77 kg** | 5.31 kg in v0.1; TRL 2 estimate was 5.5 kg |

Fully submerged, the crawler displaces 2.73 L, so its net mass is 3.05 kg (2.66 kg in v0.1): 53 % of the dry normal load is left for traction. In the design case the water is 138 mm deep above the track contact line, deeper than the 106 mm crawler, so the crawler **is fully submerged**. The TRL 2 reach estimate did not account for this.

The whole kit weighs 18.1 kg (crawler 5.8 kg, tether 3.3 kg, reel and frame 2.5 kg, surface box 6.3 kg, gamepad 0.2 kg). The heaviest single case is the surface box at 6.3 kg; the reel with tether is 5.8 kg.

## 4. Traction and reach (R2, R8)

Reach is the tether length whose drag uses up the traction left after track resistance, grade and water drag. When the crawler drives uphill it must also lift the tether up the grade, so the drag per meter is the tether weight times (0.5 cos α + sin α). The TRL 2 estimate used 0.5 x weight only and did not model water. Table 4 gives the result in each direction.

*Table 4. Reach in a straight 600 mm pipe on a 5 % grade, with 20 % traction reserve.*

| Case | Usable traction | Track resistance | Grade | Water drag | Tether drag | **Reach** |
| --- | --- | --- | --- | --- | --- | --- |
| Dry, uphill (enter at the outlet) | 28.3 N | 8.8 N | 2.83 N | 0 | 0.296 N/m | **56 m** |
| Dry, downhill (enter at the inlet) | 28.3 N | 8.8 N | -2.83 N | 0 | 0.242 N/m | 92 m |
| Design case wet, uphill against 0.5 m/s flow | 14.9 N | 4.7 N | 1.49 N | 4.19 N | 0.089 N/m | **52 m** |
| Design case wet, downhill with the flow | 14.9 N | 4.7 N | -1.49 N | -1.21 N | 0.073 N/m | 178 m |

- **R2 is met on paper, with a thin margin.** Submerged and driving upstream, the crawler reaches 52 m against a 50 m target (39 m in v0.1, before the 0.46 kg of added ballast). With no reserve, the dry uphill reach is 80 m.
- **The wet result is very sensitive to track friction under water.** At a friction coefficient of 0.45 instead of 0.6, wet uphill reach falls to about 10 m. This is the least certain input in the note, and measuring it is TRL 4 work, on hold by Amish's instruction.
- Entering from the upstream end (downhill, with the flow) gives more than 90 m in both cases, and is now operating guidance for flooded pipes (CVC-DDR-002). On the way back the reel winds the tether in, and the crawler still has a 4.6 N margin reversing upstream.
- The plate now sits 8 mm above the track contact line (10 mm in v0.1), so ground clearance under the skid is 2 mm less.
- Sprocket torque at the dry traction limit is 0.73 N·m per motor (0.67 N·m in v0.1), including 85 % belt efficiency, within a 1 N·m worm gear motor. Top speed at 80 rpm is 0.29 m/s.

**R8.** On a 5 % grade the crawler needs 2.83 N to hold against 35.4 N of static friction, and the self-locking worm gears hold it with power off. The water drag on a stationary, submerged crawler in 0.5 m/s flow is 2.5 N against 18.7 N of static friction. For the 40 mm step, a conservative rule for a flat track limits the step to the idler radius, 35 mm; a friction bound, r(1 + sin(atan μ)), gives 53 mm at μ = 0.6 and 48 mm at μ = 0.4. **R8 step crossing is at risk.**

## 5. Recovery pull (R3)

With both tracks locked (worm gears self-locking) and 50 m of tether uphill of the crew, the pull to drag the crawler out is about 53 N. The 1 kN aramid member gives a factor of 18.9 on that pull; at the required factor of 5 it covers a stuck pull of 200 N. A crawler jammed by debris cannot be bounded by calculation. The crew should never use a vehicle to pull the tether.

## 6. Power, tether and endurance (R9, R11)

*Table 5. Power while driving and profiling.*

| Quantity | Value |
| --- | --- |
| Crawler loads | 28.0 W |
| Crawler input (after 91 % buck) | 30.8 W |
| Tether loop resistance, 2 x 60 m | 3.12 Ω |
| Tether current at 48 V | 0.67 A |
| Voltage at the crawler | 45.9 V |
| Tether copper loss | 1.40 W (4.4 %) |
| Boost output | 32.2 W |
| Battery output, including 1 W of surface electronics | 36.0 W |
| Peak: tether current, crawler voltage, drop | 1.25 A, 44.1 V, 3.9 V |
| Peak battery current at 12.0 V | 5.4 A |
| Tether loss if the tether ran at 24 V | 8.24 W |
| Usable battery energy (256 Wh nominal) | 230 Wh |
| **Endurance** | **6.4 h nominal; 5.1 h derated** |

R9 (4 h) is met. At 24 V the tether would lose 8.24 W, about six times more, which supports the 48 V decision. The peak battery current of 5.4 A would blow the 5 A fuse listed at TRL 2, so the BOM now has a 10 A fuse at the battery and a 2 A fuse on the 48 V output, with the overcurrent cutoff at 1.5 A (R11).

## 7. Laser ring profiling (R5)

**The lens must see the ring at up to 70.1 degrees off axis.** With the camera 70 mm above the invert of a 900 mm pipe and the ring plane 300 mm ahead, the top of the pipe is 70.1 degrees off the camera axis (60.3 degrees in 600 mm, 35.2 degrees in 300 mm). At the v0.1 distance of 200 mm it was 76.5 degrees in 900 mm pipe, where the fisheye is least accurate. A 160 degree lens on a 16:9 frame, as assumed at TRL 2, cannot see that far vertically. The design therefore uses a 180 degree circular fisheye whose image circle fits the 1296 px sensor height, at 0.139 degree per pixel (TRL 2 assumed 0.1 degree per pixel).

The script simulates 2,000 ring measurements per case (400 in v0.1; the larger sample cuts the scatter of the 95th percentile from about 0.1 to about 0.03 percentage points): it projects the wall points in the true (tilted, offset, yawed) light plane, adds lens and centroid errors, triangulates on the nominal plane as the software would, fits an ellipse and compares the result with the true pipe.

*Table 6. Profiling error, ring plane 300 mm ahead, 95th percentile of 2,000 trials.*

| Pipe | Water depth | Mean diameter error | Vertical diameter error | Worst wall point | R5 (1 %) |
| --- | --- | --- | --- | --- | --- |
| 300 mm | 0 | 0.23 % | 0.24 % | 1.4 mm | Met |
| 600 mm | 0 | 0.43 % | 0.56 % | 4.1 mm | Met |
| 600 mm | 150 mm | 0.48 % | 0.62 % | 4.2 mm | Met |
| 900 mm | 0 | 0.71 % | 0.92 % | 9.0 mm | Met, thin margin |
| 900 mm | 150 mm | 0.73 % | 0.97 % | 9.3 mm | Met, thin margin |

For comparison, the same simulation with the v0.1 ring plane at 200 mm gives 1.49 % in 900 mm pipe with 150 mm of water (reported as 1.59 % from 400 trials in v0.1). The 300 mm plane was decided by Amish on 2026-09-25 (CVC-DDR-002) and costs a 100 mm longer boom. A 5 % deflection limit is 30 mm in a 600 mm pipe, so even a 1.5 % error would still flag a failed pipe; R5 asks for a tighter, acceptance-grade number.

With the camera at 50 frames per second and the laser on alternate frames, the crawler takes 25 profiles per second: one every 6 mm at 0.15 m/s and every 12 mm at top speed (R5 asks for 0.1 m or less).

**Signal.** A 1 mW ring spread around a 900 mm pipe puts 0.177 W/m² on the wall inside a 2 mm line. On a wall of 20 % reflectance, at f/2 and 10 ms, a 2.8 µm binned pixel collects about 272 signal electrons, a shot-noise limited SNR of about 16, enough in a dark pipe with the LEDs dimmed. Sunlight at the mouth is not modeled. A 7 mm pupil 100 mm from the cone receives about 11 µW, well under the 1 mW Class 2 limit.

## 8. Video, data link and lighting (R4, R6)

- **Video.** The LED frames of the 50 fps stream give 25 fps video, meeting R4, encoded as 1080p H.264 at about 8 Mbit/s. Laser frames go to the laptop as 1296 x 1296 grey JPEG at about 42 Mbit/s (1 bit per pixel assumed). Together they use about 53 % of the roughly 94 Mbit/s usable on 100BASE-TX. Whether a Pi 4 can capture at 50 fps and run both encoders at once cannot be verified at TRL 3.
- **Lighting.** 800 lm in a 120 degree cone gives about 255 cd: about 370 lx on the far wall of a 900 mm pipe and about 64 lx 2 m ahead down the pipe.
- **Distance (R6).** A 50 mm payout wheel with a 600-count encoder resolves 0.26 mm. The R6 tolerance at 50 m is 0.5 m. Tether slack, snaking and wheel slip set the real error and cannot be verified at TRL 3.

## 9. Hull thermal and pressure

About 11.0 W is dissipated inside the hull, which has 0.095 m² of outer area. In air (h = 8 W/(m² K)) the hull runs about 15 K above ambient, so about 55 °C at a 40 °C ambient; the Pi needs a heat path to the hull wall. In water the rise is 0.4 K. The IP68 target of 1 m is only 9.8 kPa, so hull stress is negligible; the seals, not the walls, set R7.

## 10. Cost (R12)

The BOM has 13 lines, every one priced. The total is **$906** against `budget_usd` of $910, a margin of **$4** (crawler $426, tether, reel and surface kit $450, hardware and consumables $30). The larger ballast plate adds $3 and the longer laser boom $2. Against the former $900 budget the margin was -$6; Amish accepted the v0.1 overrun of $1 as within pricing uncertainty (CVC-DDR-002) and on 2026-09-26 set the budget to $910 to cover the priced BOM. R12 is met.

## 11. Results against requirements

*Table 7. Every requirement in CVC-REQ-001 v0.4, with its calculated value and status.*

| ID | Requirement | Target | Calculated value | Status |
| --- | --- | --- | --- | --- |
| R1 | Fit | 300 to 900 mm pipe; 180 mm wide, 140 mm high or less | 170 x 106 mm, 610 mm long; 50 mm or more clearance | Met |
| R2 | Reach | 50 m in the design case with 20 % reserve | 52 m wet uphill; 56 m dry uphill; 92 to 178 m downhill; about 10 m at friction 0.45 | Met on paper, thin margin |
| R3 | Recover without entry | 1 kN, 5 times the worst stuck pull | 53 N locked-track pull; factor 18.9 | Met (jamming not calculable) |
| R4 | Video | 1080p, 25 fps or more; far wall of 900 mm pipe lit | 25 fps; 53 % link use; 370 lx | Met on paper (Pi 4 throughput not verifiable at TRL 3) |
| R5 | Profile | 1 % of diameter; every 0.1 m or less | 0.24 % (300 mm), 0.62 % (600 mm), 0.97 % (900 mm); 6 mm spacing | Met on paper (thin margin at 900 mm) |
| R6 | Locate | 1 % or 0.2 m; pitch and roll 1 degree | 0.26 mm encoder resolution; slack and slip unknown | Not verifiable at TRL 3 |
| R7 | Water and silt | 150 mm at 0.5 m/s; IP68 to 1 m | Holds with 2.5 N drag against 18.7 N; fully submerged in the design case | At risk (IP68 not verifiable at TRL 3) |
| R8 | Climb | Hold on 5 % unpowered; 40 mm step | Hold: 2.83 N against 35.4 N; step 35 to 53 mm | At risk (step) |
| R9 | Endurance | 4 h or more | 6.4 h nominal; 5.1 h derated | Met |
| R10 | Portable | 25 kg kit, 10 kg per case; setup 10 min | 18.1 kg; heaviest case 6.3 kg | Met on mass; setup time not verifiable at TRL 3 |
| R11 | Electrical and laser safety | 48 V DC, fused, cutoff, stop; Class 2 | 48 V, 2 A and 10 A fuses, 1.5 A cutoff; 11 µW at the pupil | Met by design |
| R12 | Affordable | $910 or less | $906 | Met (budget approved by Amish, 2026-09-26; not met against $900 in v0.2) |
| R13 | Open and repairable | Common parts, pluggable joints, open formats | Design review | Met by design |

Summary: 0 not met, 2 at risk (R7, R8), 1 not verifiable at TRL 3 (R6), 10 met on paper (R1, R2, R3, R4, R5, R9, R10, R11, R12, R13), of which R2 and R5 have thin margins. In v0.2, R12 was not met against the former $900 budget; in v0.1, R2 and R5 were not met.
