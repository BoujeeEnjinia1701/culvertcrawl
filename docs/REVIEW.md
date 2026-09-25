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
