---
doc_id: CVC-PRC-001
title: CulvertCrawl design precis
project: CulvertCrawl
doc_type: Design precis
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
  change: Populate to TRL 2 (architecture, profiling principle, first-order numbers, safety, media)
---

# CulvertCrawl design precis

CulvertCrawl is a small tracked crawler, about 490 x 170 x 125 mm and 5.5 kg, that drives into a 300 to 900 mm culvert on a 60 m tether while an operator watches live video on a laptop at the pipe mouth. A green laser ring projected onto the pipe wall 200 mm ahead of a fisheye camera gives a cross-section every few centimeters, from which the software reports diameter, ovality (deflection) and sediment depth against distance. First-order numbers suggest about 50 m of reach in a wet 600 mm pipe, about 6 h per charge, profile accuracy of about 0.5 % of diameter in 600 mm pipe after calibration, and a parts cost of about $900, about 13 % over the $800 budget. All numbers are estimates.

![Hero render](../media/hero.png)

*Figure 1. CulvertCrawl in a sectioned 600 mm culvert, with the tether reel and surface control box at the mouth and a 1.75 m person for scale. The green line is the projected laser ring (illustrative).*

## How it works

1. **Deploy.** Two people carry the crawler, the tether reel and the surface box from the vehicle to the culvert mouth. The operator connects a laptop and gamepad to the surface box, sets the payout counter to zero at the mouth and lowers the crawler onto the invert.
2. **Power and data.** A 12.8 V LiFePO4 battery in the surface box feeds a boost converter that puts 48 V DC on two power conductors in the tether. Two twisted pairs in the same tether carry 100 Mbit/s Ethernet between the laptop and the crawler. A slip ring in the reel hub lets the drum turn while connected. The surface box holds the fuse, the overcurrent cutoff and a latching emergency stop that kills tether power.
3. **Drive.** Inside the sealed aluminium hull, a Raspberry Pi 4 runs the motor driver for two self-locking worm gear motors, one per rubber track. The operator drives with the gamepad at about 0.15 m/s while surveying. The worm gears hold the crawler on a slope with power off.
4. **See.** A 12 MP camera with a fisheye lens looks forward through an acrylic dome, lit by a ring of eight 1 W LEDs. The Pi encodes 1080p H.264 video in hardware and streams it to the laptop, which records it with distance, time and attitude overlaid. Distance comes from the payout counter at the reel, cross-checked by track odometry; pitch and roll come from an IMU in the hull.
5. **Measure.** A Class 2 laser diode at the tip of a clear boom shines onto a 90 degree conical mirror, which spreads the beam into a thin disc of light perpendicular to the crawler axis, 200 mm ahead of the lens. Where the disc meets the wall it draws a bright ring. On alternate frames the LEDs dim and the software finds the ring in the image. Because the ring plane is fixed relative to the camera, each ring pixel defines a ray that meets the plane at exactly one point, so the wall is triangulated in 3D even when the crawler is well below the pipe axis. The software fits a circle and an ellipse to each ring, and reports mean diameter, ovality, and the height of any flat sediment or water surface across the invert, every 12 mm or so of travel.
6. **Recover.** The crawler reverses out while the operator winds the reel. If it stalls or loses power, the tether's aramid strength member lets the crew pull it out by hand; nobody enters the pipe.

![Power flow](../media/flow.png)

*Figure 2. Power flow while driving and profiling, in watts. All values are estimates.*

## Main components

Numbers match the exploded view (Figure 3) and `bom/bom.csv`.

| # | Component | Proposed choice | Notes |
| --- | --- | --- | --- |
| 1 | Sealed hull and lid | 6061 aluminium box about 240 x 88 x 80 mm, 4 mm walls, O-ring lid, IP68 glands, pressure-test port | Leak check by vacuum or low pressure before each use |
| 2 | Track modules (pair) | Rubber belts about 40 mm wide over 70 mm sprockets, aluminium side plates, 130 mm track spacing | Outer track edges bear on the curved invert |
| 3 | Worm gear motors (2) | 12 V, about 80 rpm output, self-locking, Hall encoders, double lip shaft seals | Shaft seals are the main leak path |
| 4 | Electronics stack | Raspberry Pi 4 Model B 2 GB, dual motor driver, 48 to 12 V and 12 to 5 V converters, IMU, leak sensor | Pi 4 chosen for its hardware H.264 encoder |
| 5 | Fisheye camera and dome port | 12 MP IMX708-class module, M12 fisheye lens of 160 degrees or wider, 60 mm acrylic dome | Dome keeps the wide field of view if the port is wet |
| 6 | LED ring light | 8 x 1 W high-CRI white LEDs, about 800 lm (estimate), dimmable | Dimmed on laser frames |
| 7 | Laser ring projector | Class 2 (1 mW or less) 520 nm diode, 90 degree conical mirror, clear boom 200 mm ahead of the lens | Boom is removable for tight or bent pipes (proposed) |
| 8 | Ballast skid plate | Steel, about 1.6 kg, turned-up front edge | Raises traction and protects the hull |
| 9 | Tether | 60 m hybrid: 2 twisted pairs plus 2 x 0.75 mm² power, aramid member, PU jacket about 7 mm, about 55 g/m (estimate) | Also the recovery line |
| 10 | Tether reel | 320 mm flanged reel, A-frame, crank and brake, Ethernet-rated slip ring, payout encoder wheel | Payout counter gives distance |
| 11 | Surface control box | Rugged case; 12.8 V 20 Ah LiFePO4 with BMS; 12 to 48 V boost; 5 A fuse; emergency stop; overcurrent cutoff | Laptop connects by Ethernet |
| 12 | Operator gamepad | USB gamepad | Laptop is the user's own |

![Exploded view](../media/exploded.png)

*Figure 3. Exploded view with numbered callouts matching the BOM. The surface kit (9 to 12) is shown displaced in front of the crawler.*

![Cutaway](../media/cutaway.png)

*Figure 4. Cutaway of the crawler along its axis: dome and camera (left of the hull), electronics stack, worm gear motors at the rear, ballast plate underneath, and the laser boom ahead of the dome.*

## First-order numbers

All values are estimates for concept review and will be checked at TRL 3. The design case is a straight 600 mm corrugated steel culvert, 50 m long, on a 5 % slope, with a wet silt invert.

### Mass and buoyancy

| Item | Estimate | Basis |
| --- | --- | --- |
| Hull and lid | about 1.3 kg | 4 mm aluminium shell, about 0.38 L of metal |
| Tracks, sprockets, side plates | about 1.0 kg | Hobby tank track sets |
| Motors, electronics, camera, lights, laser | about 1.2 kg | Datasheet-class parts |
| Ballast plate | about 1.6 kg | 210 x 80 x 12 mm steel |
| Fasteners, glands, strain relief | about 0.4 kg | Allowance |
| **Crawler** | **about 5.5 kg** | |
| Displaced volume | about 2.5 L | Hull 1.7 L plus tracks, dome and plate |
| Net weight fully submerged | about 3.0 kg | Traction falls to about half of dry |
| Whole kit (crawler, reel with tether, surface box, gamepad) | about 18 kg | R10 (25 kg) met |

### Traction and reach

Assumptions: track-to-silt friction coefficient 0.6; track motion resistance 0.15 of weight on silt; tether-to-pipe friction coefficient 0.5; tether weight 55 g/m (0.54 N/m); 20 % of traction held in reserve.

| Quantity | Estimate | Basis | Requirement |
| --- | --- | --- | --- |
| Available traction (dry) | about 32 N | 0.6 x 5.5 kg x 9.81 m/s² | |
| Usable traction with 20 % reserve | about 26 N | 0.8 x 32 N | |
| Track resistance on silt | about 8 N | 0.15 x 54 N | |
| Grade force on 5 % | about 2.7 N | 54 N x 0.05 | |
| Tether drag per meter | about 0.27 N/m | 0.5 x 0.54 N/m | |
| **Reach, design case** | **about 56 m** | (26 minus 8 minus 2.7) N / 0.27 N/m | R2 (50 m) met, margin thin |
| Reach with no traction reserve | about 80 m | Same with 32 N | |
| Drawbar per track at the limit | about 16 N; about 0.56 N·m at a 35 mm sprocket radius | Half of 32 N | Within a small worm gear motor's rating |
| Top speed | about 0.29 m/s | 80 rpm at 35 mm radius | Survey at 0.15 m/s |

Tether drag grows with every bend (capstan effect), with a corrugated invert that snags the jacket, and when the jacket is wet and muddy. A lighter or partly buoyant tether, or feeding tether by hand at the mouth, are the main ways to add reach.

### Power and endurance

Assumptions: loads while driving and profiling are drive motors 12 W, LEDs 8 W, Pi, camera and network 6.5 W, laser, IMU and sensors 1.5 W, for 28 W in the crawler; converter efficiencies of 91 to 92 %; tether round-trip resistance 3.1 Ω (120 m of 0.75 mm² stranded copper).

| Quantity | Estimate | Basis | Requirement |
| --- | --- | --- | --- |
| Crawler input | about 30.8 W | 28 W / 0.91 buck efficiency | |
| Tether current at 48 V | about 0.65 A | 30.8 W at about 47 V at the crawler | |
| Tether copper loss | about 1.3 W (about 4 %) | 0.65² x 3.1 Ω | |
| Tether voltage drop, peak 50 W load | about 3.4 V | 1.1 A x 3.1 Ω | Well within the buck converter input range |
| Battery output | about 35 W | 32.1 W / 0.92 boost efficiency | |
| Usable battery energy | about 230 Wh | 12.8 V x 20 Ah x 90 % | |
| **Endurance** | **about 6 h** | 230 Wh / 35 W = 6.6 h, rounded down for cold and battery aging | R9 (4 h) met |

### Laser ring profiling

The ring plane sits 200 mm ahead of the lens. A wall point at radius *r* from the camera axis is seen at an angle θ where tan θ = *r* / 200 mm, so a small angle error dθ gives a radial error of about 200 mm x (1 + tan² θ) x dθ. Assumptions: fisheye lens giving about 0.1 degree per pixel at 1920 x 1080; ring center located to 0.3 pixel; ring plane position calibrated in a reference pipe to 0.1 degree of tilt; camera about 60 to 90 mm above the invert depending on pipe size.

| Pipe | Worst wall angle (top of pipe) | Random error | Calibration residual | Total (estimate) | R5 (1 % of diameter) |
| --- | --- | --- | --- | --- | --- |
| 300 mm | about 47 degrees | about 0.2 mm | about 0.4 mm | about 0.6 mm (0.2 %) | Met |
| 600 mm | about 69 degrees | about 0.8 mm | about 2.4 mm | about 3 mm (0.5 %) | Met |
| 900 mm | about 76 degrees | about 1.9 mm | about 6 mm | about 7 to 11 mm (0.8 to 1.2 %) | **At risk** |

A 5 % deflection in a 600 mm pipe is 30 mm, so the ring resolves the plastic pipe acceptance limit with a wide margin at 300 and 600 mm. At 900 mm the top of the pipe falls near the edge of the lens, where distortion and lens calibration dominate. Moving the ring plane further ahead (for example 300 mm) or adding a camera riser for large pipes would fix this at the cost of a longer or taller crawler. The profile covers only the wall above any water surface, because the light refracts at the water line; the software reports the water or sediment chord instead.

At 0.15 m/s with the laser on every other frame at 25 frames per second, the crawler takes a profile about every 12 mm (R5 asks for 0.1 m or less).

### Cost

| Group | Indicative cost | Requirement |
| --- | --- | --- |
| Crawler (items 1 to 8) | about $421 | |
| Tether, reel and surface kit (items 9 to 12) | about $450 | |
| Hardware and consumables (item 13) | about $30 | |
| **Total** | **about $900** | R12 ($800) not met, about 13 % over |

The tether and reel (about $245) and the camera and electronics (about $170) are the largest items. The laptop is excluded.

## Key design choices

Every choice below is **Proposed, awaiting Amish**.

- **Tracks rather than wheels.** Tracks spread the load on silt and ride over corrugations and joint offsets; wheeled crawlers are simpler, cheaper and easier to seal but slip in mud. Recommendation: tracks. Proposed, awaiting Amish.
- **Power from the surface over the tether rather than a battery in the crawler.** Surface power keeps lithium cells out of the pipe, gives unlimited dive time with a battery swap at the surface and keeps the crawler small; it costs a heavier tether. Recommendation: surface power at 48 V DC. Proposed, awaiting Amish.
- **48 V on the tether.** At 48 V the tether loses about 4 % and drops about 3.4 V at peak; at 24 V the loss would be about four times higher and the drop about 7 V. 48 V stays below the 60 V DC extra-low-voltage limit. Recommendation: 48 V. Proposed, awaiting Amish.
- **Surface battery: LiFePO4 rather than the portfolio's SwapCell pack.** A 12.8 V 20 Ah LiFePO4 battery (about $90, about 256 Wh) is common and has a stable chemistry. A SwapCell pack (48 V class, about 468 Wh) would feed the tether without a boost converter and share packs with other portfolio vehicles, but costs about $370 in prototype parts and needs its CAN host heartbeat. Recommendation: LiFePO4 for the prototype, with a SwapCell-compatible input as a later option. Proposed, awaiting Amish.
- **Laser ring ahead of the camera rather than a structured-light or stereo camera.** A single ring gives a direct, well-understood cross-section and is the method commercial profilers use; stereo or depth cameras are heavier on compute and poor on wet, dark, textureless walls. Recommendation: ring laser, 520 nm, Class 2. Proposed, awaiting Amish.
- **Fixed camera rather than pan and tilt.** A fisheye camera sees the whole wall at once and has no moving seals; pan-tilt heads give better close-ups of defects but add cost and a second leak path. Recommendation: fixed fisheye for TRL 3, pan-tilt as a later option. Proposed, awaiting Amish.
- **Processing on the laptop.** The Pi streams video and logs sensors; ring extraction and reports run on the operator's laptop, so the crawler software stays small. Proposed, awaiting Amish.
- **Pipe range 300 to 900 mm.** See R5; narrowing to 300 to 600 mm would meet R5 everywhere. Proposed, awaiting Amish.
- **Budget.** The first estimate is about $900 against $800. Options are in `docs/REVIEW.md`; `project.yaml` is unchanged. Proposed, awaiting Amish.

## Safety

> **Safety:** CulvertCrawl is used at roadside ditches, next to flowing water and at the mouth of a confined space. It carries a lithium battery, 48 V DC on a long cable, a laser and moving tracks. The most important rule is that nobody enters the pipe, including to recover the crawler.

- **Confined space.** A culvert is a confined space and may be a permit-required confined space under OSHA 29 CFR 1910.146 ([osha.gov](https://www.osha.gov/laws-regs/regulations/standardnumber/1910/1910.146)). The purpose of CulvertCrawl is to avoid entry. Never enter or lean into a pipe to free the crawler; pull it out by the tether, or leave it and call a qualified entry team.
- **Hazardous atmospheres.** The crawler is not intrinsically safe and is not rated for flammable atmospheres. Do not use it in sanitary sewers, in storm drains that may receive sewage or fuel, or anywhere methane or other flammable gas may be present. In any enclosed drain, check the air at the mouth with a four-gas monitor before and during work.
- **Traffic, water and banks.** Road culverts put crews on shoulders and steep, wet banks. Use temporary traffic control as the road owner requires (for example MUTCD Part 6 in the United States), high-visibility clothing and a second person as spotter. Do not work in fast or rising water; flash floods can arrive with little warning.
- **Lithium battery.** The surface box holds a 12.8 V 20 Ah LiFePO4 battery (about 256 Wh). Use a battery with a BMS, keep the output fused, charge with a matched LiFePO4 charger on a non-combustible surface, and do not charge a battery that is damaged, swollen or has been in water.
- **Electrical.** 48 V DC on the tether is extra-low voltage, but a damaged tether in water can still corrode and short. The surface box has a fuse, an overcurrent cutoff and a latching emergency stop; inspect the tether jacket before each use and retire damaged lengths.
- **Laser.** The projector must stay at Class 2 (1 mW or less, visible) under IEC 60825-1. Do not stare into the beam or look at it through optics; switch the laser off when the crawler is out of the pipe.
- **Moving parts and tether.** Tracks and sprockets can pinch fingers; the emergency stop removes drive power. The reel crank can kick back under tether tension, so use the brake. Keep the tether clear of walkways to avoid trips.
- **Sharp edges and wildlife.** Rusted metal pipe has sharp edges at holes and seams. Wear cut-resistant gloves when handling the tether at the mouth, and watch for snakes, wasps and other animals in and near culverts.

## Open questions

- Is 50 m of reach enough, and is the thin traction margin acceptable, or should the tether be lighter or partly buoyant?
- Will double lip seals on the drive shafts hold IP68, or is a magnetic coupling or a sealed motor pod needed?
- Is a Class 2 laser bright enough to find the ring on a wet, sunlit-at-the-mouth or reflective wall, or does it need a narrowband filter on the camera?
- How far can the fisheye calibration be trusted near the edge of the lens (R5 at 900 mm)?
- Should the laser boom be removable, and is a camera riser needed for 900 mm pipe?
- Which outputs do users need first: a PACP-style observation log, FHWA condition ratings, or a deflection report?

## References

- US Occupational Safety and Health Administration. 29 CFR 1910.146, *Permit-required confined spaces*; and 29 CFR 1926 Subpart AA, *Confined Spaces in Construction*.
- Federal Highway Administration. *Culvert Inspection Manual*. FHWA-IP-86-2, 1986.
- Federal Highway Administration. *Culvert Assessment and Decision-Making Procedures Manual*. FHWA-CFL/TD-10-005, 2010.
- ASTM D2321, *Standard Practice for Underground Installation of Thermoplastic Pipe for Sewers and Other Gravity-Flow Applications*.
- NASSCO. *Pipeline Assessment Certification Program (PACP)*. [nassco.org](https://www.nassco.org).
- Duran, O., K. Althoefer and L. D. Seneviratne. "State of the Art in Sensor Technologies for Sewer Inspection." *IEEE Sensors Journal* 2, no. 2 (2002).
- Duran, O., K. Althoefer and L. D. Seneviratne. "Automated Pipe Defect Detection and Categorization Using Camera/Laser-Based Profiler and Artificial Neural Network." *IEEE Transactions on Automation Science and Engineering* 4, no. 1 (2007).
- IEC 60825-1, *Safety of laser products, Part 1: Equipment classification and requirements*.
- IEC 60529, *Degrees of protection provided by enclosures (IP Code)*.

These references were cited from known documents; their editions and links were not rechecked online in this session and will be checked at TRL 3.
