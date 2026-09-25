# Review note: CulvertCrawl

## Session 2026-09-25: /populate to a strong TRL 2

### What was done

- `docs/01-problem.md` (CVC-PRB-001 v0.2): problem, why entry and end views fail, users (road crews, public works, inspectors, watershed groups, owners, makers), operating environment, constraints, out of scope, prior work with sources, open questions and a co-design checklist.
- `docs/03-requirements.md` (CVC-REQ-001 v0.2): 13 measurable requirements (R1 to R13) with targets, verification and a first-order status for each, a defined design case, and a list of requirements not met or at risk.
- `docs/02-concept.md` (CVC-PRC-001 v0.2): how it works, numbered components, mass and buoyancy, traction and reach, power and endurance, laser ring profiling error budget, cost, design choices (all proposed), safety section, open questions and references.
- `cad/src/concept_media.py`: massing model of the crawler (hull, tracks, worm gear motors, electronics, fisheye camera and dome, LED ring, laser boom, ballast) plus tether, reel and surface box, each part with a BOM number; a sectioned 600 mm culvert and the projected laser ring are hero-only context.
- `media/`: `hero.png` (1.75 m scale figure), `concept-blueprint.png`, `.pdf` and `.svg`, `model.glb` and `viewer.html`, `exploded.png` with callouts 1 to 12, `cutaway.png` (crawler only), `flow.png` (power flow, estimates). Temporary `media/_views*` folders removed.
- `bom/bom.csv`: 13 lines, numbered to match the exploded view, with indicative USD prices; `bom/bom-notes.md` updated to match.
- `README.md`: hero image and links line inserted before "## Problem"; Problem, Concept and Key components updated to the concept.
- `docs/pdf/`: branded PDFs of the three controlled documents.
- `project.yaml`: unchanged. The pitch and problem still describe the concept correctly.

### Key results (estimates, to be checked at TRL 3)

| Quantity | Estimate | Requirement |
| --- | --- | --- |
| Crawler size and mass | 490 x 170 x 125 mm (including laser boom), about 5.5 kg | R1 met |
| Reach in the design case (600 mm, 5 % slope, wet silt, 20 % traction reserve) | about 56 m | R2 met, thin margin |
| Crawler power while driving and profiling | about 28 W; about 35 W from the battery | |
| Tether loss at 48 V over 60 m | about 1.3 W (4 %); about 3.4 V drop at 50 W peak | |
| Endurance on a 12.8 V 20 Ah LiFePO4 battery | about 6 h | R9 met |
| Profile accuracy, 300 / 600 / 900 mm pipe | about 0.2 % / 0.5 % / 0.8 to 1.2 % of diameter | R5 met to 600 mm, at risk at 900 mm |
| Profile spacing at 0.15 m/s | about 12 mm | R5 met |
| Net weight fully submerged | about 3.0 kg (traction about half of dry) | R7 partly |
| Whole kit mass | about 18 kg | R10 met on mass |
| Parts cost | about $900 (crawler about $421; tether, reel and surface kit about $450; consumables $30) | **R12 not met, about 13 % over** |

Requirements not met or at risk:

- **R12 (cost) not met:** about $900 against $800.
- **R5 at risk at 900 mm:** the top of a 900 mm pipe sits about 76 degrees off the camera axis, near the edge of the fisheye, where 1 % is marginal.
- **R7 unverified:** IP68 to 1 m with rotating shaft seals is the most likely failure; profiling works only above the water line.
- **R2 margin thin:** tether drag in bends, on corrugations or with a muddy jacket could cut reach below 50 m.
- **R4 lighting at 900 mm, R8 step crossing and R10 setup time** are unverified.

### Proposed, awaiting Amish

1. **Budget.** Options: (a) raise `budget_usd` from $800 to $900; (b) cut to $800 by shortening the tether to 30 m and dropping the slip ring (surface box rides on the reel and talks to the laptop over Wi-Fi), which reduces reach to about 25 m and adds a radio link; (c) keep $800 and treat the surface kit as shared equipment costed separately. Recommendation: (a), because reach and a wired link are central to the pitch. `project.yaml` is unchanged.
2. **Pipe range.** Keep 300 to 900 mm (R5 at risk at 900 mm) or narrow to 300 to 600 mm (R5 met throughout). Recommendation: keep 300 to 900 mm and test the 900 mm case early at TRL 3.
3. **Surface battery.** A 12.8 V LiFePO4 battery with a 48 V boost (about $90) or the portfolio's SwapCell pack (48 V class, about $370, needs a CAN host heartbeat). Recommendation: LiFePO4 for the prototype, SwapCell-compatible input as a later option.
4. Tracks rather than wheels.
5. Surface power over the tether at 48 V DC rather than a battery in the crawler.
6. Class 2, 520 nm laser ring 200 mm ahead of a fixed fisheye camera, rather than a structured-light or stereo camera or a pan-tilt head.
7. Processing and reporting on the operator's laptop rather than in the crawler.
8. Output format first: PACP-style observation log, FHWA condition ratings or a deflection report.
9. First partner user group for field trials (county road department, watershed group or university transportation program).

### Safety concerns

- Confined space: the tool exists to avoid entry; recovery must never involve entering the pipe (OSHA 29 CFR 1910.146).
- Flammable atmospheres: the crawler is not intrinsically safe; sewers and gas-bearing drains are out of scope, and air should be checked at the mouth of any enclosed drain.
- Roadside traffic, steep wet banks and fast or rising water at culvert mouths.
- LiFePO4 battery of about 256 Wh in the surface box: BMS, fuse, matched charger, no charging when damaged or wet.
- 48 V DC on a long tether in water: fuse, overcurrent cutoff, latching emergency stop, jacket inspection.
- Class 2 laser: do not stare into the beam; switch off when out of the pipe.
- Track pinch points, reel crank kickback, tether trips, sharp rusted edges and wildlife.

### Problems and notes

- The web search budget for this batch was exhausted before this repo, and direct web fetches were blocked, so no new searches were possible. Sources are cited from well-known documents (OSHA, FHWA culvert manuals, ASTM D2321, NASSCO PACP, Duran and coauthors in IEEE journals, IEC 60825-1 and 60529) and are marked in the documents as not rechecked online. Commercial price ranges are labeled as estimates. Check every citation and link at TRL 3.
- The 5 % deflection limit is described as common practice following AASHTO and state DOT specifications; the exact clause should be confirmed.
- In the exploded view, the surface kit (items 9 to 12) is drawn displaced in front of the crawler so the crawler parts stay legible; the crawler parts are small relative to the reel and case.
- The hero view is at human scale, so the crawler is small in the image; the cutaway and exploded views show it in detail.
- The legacy `cad/src/model.py` placeholder is untouched (TRL 3 work).

### Recommended next step

Review this note and the media, then decide items 1 to 3. If approved, run `/advance-trl3` to check the traction and reach, tether power, buoyancy and laser profiling error budget by calculation, and to produce the parametric model and drawing sheet.

## Session 2026-09-25: TRL 3

Amish approved all TRL 2 recommendations on 2026-09-25 ("proceed with all of your recommendations across all batches. Make sure we don't proceed to TRL 4 on any of them."). This session ran `/advance-trl3` and stopped at TRL 3.

### What was done

- `docs/decisions/0001-trl2-review-decisions.md` (CVC-DDR-001 v0.1): eight decided items and three that stay open.
- `docs/04-calcs/01-sizing.md` (CVC-CAL-001 v0.1) with `docs/04-calcs/sizing.py` and `results.csv`: fit, mass and buoyancy, traction and reach (dry and submerged, both directions), recovery pull, tether power and endurance, a Monte Carlo profiling error budget, laser signal, video link, lighting, hull thermal and cost. The script reads `cad/src/model.py` and `bom/bom.csv`.
- `cad/src/model.py`: parametric build123d model (crawler and surface kit) exporting `cad/step/culvertcrawl-crawler.step`, `cad/step/culvertcrawl-surface-kit.step` and matching STL files.
- `cad/src/sheets.py` and `cad/drawings/CVC-DWG-001.svg`, `.pdf`, `.png`: general arrangement, Rev P1, with end-view fit checks in 300 and 900 mm pipe. The concept blueprint keeps CVC-DWG-010.
- `bom/bom.csv` and `bom/bom-notes.md`: every line priced with a supplier type; specification changes for the camera (50 fps, circular fisheye) and fuses (10 A battery, 2 A tether). Total $901.
- `cad/src/concept_media.py` now builds from the model; all media in `media/` regenerated and checked; `media/_views*` removed.
- CVC-PRB-001, CVC-PRC-001 and CVC-REQ-001 moved to v0.3; `project.yaml` (`trl: 3`, `trl_target: 3`, `budget_usd: 900`, evidence list); `README.md` updated. Pitch and problem wording unchanged, as recommended.

### Requirements (CVC-CAL-001)

3 not met, 2 at risk, 1 not verifiable at TRL 3, 7 met on paper.

| ID | Status | Key number |
| --- | --- | --- |
| R2 Reach | **Not met** | 39 m submerged, uphill against 0.5 m/s flow (target 50 m); 52 m dry uphill; 85 to 158 m downhill. Falls to about 3 m if submerged track friction is 0.45 |
| R5 Profile | **Not met at 900 mm** | Vertical diameter error 1.59 % at 900 mm; 0.87 % at 600 mm; 0.35 % at 300 mm; 6 mm spacing |
| R12 Cost | **Not met** | $901 against $900 |
| R7 Water | At risk | Holds in flow on paper; fully submerged in the design case; IP68 not verifiable |
| R8 Climb | At risk | Hold met; 40 mm step against a 35 to 53 mm limit |
| R6 Locate | Not verifiable at TRL 3 | Encoder resolution 0.26 mm; slack and slip unknown |
| R1, R3, R4, R9, R10, R11, R13 | Met on paper | 170 x 106 x 510 mm; 50 N pull, factor 20; 25 fps, 53 % link; 6.4 h; 17.6 kg; 48 V with 2 A and 10 A fuses |

Corrections to TRL 2 numbers: crawler 5.3 kg (was 5.5 kg) and 106 mm high (was 125 mm); tether current 0.67 A and loss 1.40 W (was 0.65 A, 1.3 W); battery draw 36.0 W and 6.4 h (was 35 W, about 6 h); reach now includes lifting the tether up the grade and full submersion; lens needs a 180 degree circular fisheye at 0.139 degree per pixel (was 0.1 degree per pixel, not achievable while seeing the pipe top); profile spacing 6 mm at 50 fps (was 12 mm, which left video at 12.5 fps and missed R4); the 5 A fuse was below the 5.4 A peak battery current.

### Decisions recorded (CVC-DDR-001)

Decided by Amish, 2026-09-25, go with recommendation: budget $900; pipe range 300 to 900 mm; LiFePO4 surface battery (SwapCell input later, citing interface v0.3); tracks; 48 V surface power; Class 2 520 nm laser ring with fixed fisheye; processing on the laptop; pitch and problem unchanged.

### Still awaiting Amish

1. Output format first (PACP-style log, FHWA ratings or deflection report); no recommendation was made.
2. First partner user group; not named (partners are picked per area later).
3. Removable laser boom; no recommendation was made.
4. **New, R2:** options are (a) add about 0.40 kg of ballast (restores 50 m wet uphill on paper at friction 0.6, but not at 0.45); (b) redefine the design case as entering from the upstream end; (c) accept a shorter reach in flooded pipes. Recommendation: (a) plus (b) as operating guidance; submerged track friction needs measuring once Amish lifts the TRL 4 hold.
5. **New, R5:** options are (a) move the ring plane to 300 mm ahead (0.97 % at 900 mm, 100 mm longer boom); (b) narrow acceptance-grade profiling to 300 to 600 mm and report 900 mm as screening; (c) tilt the camera up. Recommendation: (a).
6. **New, R12:** accept $901 as within pricing uncertainty, or trim $1 or more. Recommendation: accept and revisit when real quotes exist.

### Safety concerns

Unchanged from TRL 2, plus: the design-case crawler is fully submerged, so seal integrity on the drive shafts and lid is the main failure mode; never tie the tether to a vehicle (the 1 kN member and cable whip); the fuse split must be kept (10 A battery, 2 A tether, 1.5 A cutoff); the hull runs about 15 K above ambient in air, so the Pi needs a heat path to the wall. Confined space, flammable atmosphere, roadside traffic, fast water, LiFePO4 and Class 2 laser notes stay in CVC-PRC-001.

### Citations

Checked online on 2026-09-25: OSHA 29 CFR 1910.146 (title and definition), FHWA-IP-86-2 (1986), FHWA-CFL/TD-10-005 (2010), and both Duran, Althoefer and Seneviratne papers by title and journal (the 2007 paper at *IEEE Transactions on Automation Science and Engineering* 4, page 118). Still unchecked: the ASTM D2321 5 % deflection clause, NASSCO PACP, IEC 60825-1, IEC 60529 and commercial product pages.

### Existing TRL 4 material

None found. `build-log/` holds only its README and `.gitkeep`; `firmware/` and `electronics/` are empty.

### Recommended next step

TRL 4 is on hold by Amish's instruction. Next, Amish decides items 1 to 6 above; if 4 or 5 are accepted, a TRL 3 revision updates the model, the CAL note and the drawing to Rev P2. For the record only, TRL 4 would need: a submerged track friction and drawbar test on silt, a tank test of the sealed hull and shaft seals to 1 m, a laser ring calibration in 300, 600 and 900 mm reference pipes, a Pi 4 frame-rate and encoder load test, a test report (TST, `environment: lab`) and build log entries.
