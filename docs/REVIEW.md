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

Status update: items 1 to 7 were decided by Amish, 2026-09-25: go with recommendation (CVC-DDR-001). Items 8 and 9 had no recommendation and stay Proposed, awaiting Amish.

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
4. **New, R2:** Decided by Amish, 2026-09-25: go with recommendation (CVC-DDR-002; applied in the session below). Options were (a) add about 0.40 kg of ballast (restores 50 m wet uphill on paper at friction 0.6, but not at 0.45); (b) redefine the design case as entering from the upstream end; (c) accept a shorter reach in flooded pipes. Recommendation: (a) plus (b) as operating guidance; submerged track friction needs measuring once Amish lifts the TRL 4 hold.
5. **New, R5:** Decided by Amish, 2026-09-25: go with recommendation (CVC-DDR-002; applied in the session below). Options were (a) move the ring plane to 300 mm ahead (0.97 % at 900 mm, 100 mm longer boom); (b) narrow acceptance-grade profiling to 300 to 600 mm and report 900 mm as screening; (c) tilt the camera up. Recommendation: (a).
6. **New, R12:** Decided by Amish, 2026-09-25: go with recommendation (CVC-DDR-002). Options were: accept $901 as within pricing uncertainty, or trim $1 or more. Recommendation: accept and revisit when real quotes exist.

### Safety concerns

Unchanged from TRL 2, plus: the design-case crawler is fully submerged, so seal integrity on the drive shafts and lid is the main failure mode; never tie the tether to a vehicle (the 1 kN member and cable whip); the fuse split must be kept (10 A battery, 2 A tether, 1.5 A cutoff); the hull runs about 15 K above ambient in air, so the Pi needs a heat path to the wall. Confined space, flammable atmosphere, roadside traffic, fast water, LiFePO4 and Class 2 laser notes stay in CVC-PRC-001.

### Citations

Checked online on 2026-09-25: OSHA 29 CFR 1910.146 (title and definition), FHWA-IP-86-2 (1986), FHWA-CFL/TD-10-005 (2010), and both Duran, Althoefer and Seneviratne papers by title and journal (the 2007 paper at *IEEE Transactions on Automation Science and Engineering* 4, page 118). Still unchecked: the ASTM D2321 5 % deflection clause, NASSCO PACP, IEC 60825-1, IEC 60529 and commercial product pages.

### Existing TRL 4 material

None found. `build-log/` holds only its README and `.gitkeep`; `firmware/` and `electronics/` are empty.

### Recommended next step

TRL 4 is on hold by Amish's instruction. Next, Amish decides items 1 to 6 above; if 4 or 5 are accepted, a TRL 3 revision updates the model, the CAL note and the drawing to Rev P2. For the record only, TRL 4 would need: a submerged track friction and drawbar test on silt, a tank test of the sealed hull and shaft seals to 1 m, a laser ring calibration in 300, 600 and 900 mm reference pipes, a Pi 4 frame-rate and encoder load test, a test report (TST, `environment: lab`) and build log entries.

## Session 2026-09-25: recommendations accepted

On 2026-09-25 Amish wrote: "i accept all your recommendations, go with them across all repos." This session applied that instruction at TRL 3 and recorded it in CVC-DDR-002 (`docs/decisions/0002-recommendations-accepted.md`). TRL 4 remains on hold.

### Decisions applied and what changed

| Item | Decision | Before | After |
| --- | --- | --- | --- |
| R2 reach | Decided by Amish, 2026-09-25: go with recommendation. Add ballast; upstream entry in flooded pipes as operating guidance | Ballast 210 x 80 x 12 mm, 1.67 kg; crawler 5.31 kg, 2.66 kg net submerged; wet uphill reach 39 m | Ballast 230 x 80 x 14 mm, 2.13 kg, 8 mm above the contact line; crawler 5.77 kg, 3.05 kg net; wet uphill reach 52 m (about 10 m at friction 0.45) |
| R5 at 900 mm | Decided by Amish, 2026-09-25: go with recommendation. Ring plane 300 mm ahead | Ring 200 mm ahead; crawler 510 mm long; 1.59 % at 900 mm | Ring 300 mm ahead; crawler 610 mm long; 0.97 % at 900 mm (0.62 % at 600 mm, 0.24 % at 300 mm) |
| R12 cost | Decided by Amish, 2026-09-25: go with recommendation. Accept $1 over as pricing uncertainty; revisit with real quotes | $901 | $906 after the two changes above (ballast +$3, boom +$2); `budget_usd` stays 900 |

Files changed: `cad/src/model.py` (and STEP and STL re-exported), `cad/src/sheets.py` and CVC-DWG-001 Rev P1 to Rev P2, `cad/src/concept_media.py` and all of `media/`, `docs/04-calcs/sizing.py`, `results.csv` and CVC-CAL-001 v0.1 to v0.2 (Monte Carlo now 2,000 trials), `bom/bom.csv` and `bom/bom-notes.md`, CVC-PRB-001, CVC-PRC-001 and CVC-REQ-001 v0.3 to v0.4, CVC-DDR-001 v0.1 to v0.2, new CVC-DDR-002, `README.md` (numbers and the four write-up sections), `project.yaml` (DDR-002 added to the evidence list only), and `docs/pdf/`. Other knock-on numbers: kit 17.6 to 18.1 kg; sprocket torque 0.67 to 0.73 N·m; recovery pull 50 to 53 N (factor 18.9).

The README gained "Concept rationale", "Burning platform", "Where it could be used" and "What sparked the idea". The inspiration point is Florida DOT Standard Specifications Section 430 (Rev 12-7-07), which requires laser-profile video inspection of new pipe of 48 in or less but lets short cross drains be inspected from each end.

### Requirement status (CVC-CAL-001 v0.2)

| ID | Status | Key number |
| --- | --- | --- |
| R12 Cost | **Not met** | $906 against $900; $1 accepted by Amish, $5 awaiting Amish |
| R7 Water | At risk | IP68 not verifiable at TRL 3; holds in the flow (2.5 N drag against 18.7 N) |
| R8 Climb | At risk | Hold met; 40 mm step against a 35 to 53 mm limit |
| R6 Locate | Not verifiable at TRL 3 | Slack and slip unknown |
| R2 Reach | Met on paper, thin margin | 52 m wet uphill; about 10 m if submerged track friction is 0.45 |
| R5 Profile | Met on paper, thin margin at 900 mm | 0.24 / 0.62 / 0.97 % at 300 / 600 / 900 mm |
| R1, R3, R4, R9, R10, R11, R13 | Met on paper | 170 x 106 x 610 mm; 53 N pull, factor 18.9; 25 fps; 6.4 h; 18.1 kg; 48 V fused |

### Still awaiting Amish

1. Output format first (PACP-style log, FHWA ratings or deflection report); no recommendation was made.
2. First partner user group; not named.
3. Removable laser boom; no recommendation was made. It matters more now that the boom overhangs the tracks by about 300 mm.
4. **New:** the $5 added by the ballast and boom changes ($906 against $900). Recommendation: accept on the same basis as the first $1 and revisit with real quotes. Decided by Amish, 2026-09-26: budget set to $910 (CVC-DDR-002 v0.2).

### Cross-repo actions

None. No decision in this repo needs another repo to change.

### Safety

Unchanged. The heavier crawler raises the locked-track recovery pull to 53 N, still a factor of 18.9 on the 1 kN tether member; never tie the tether to a vehicle. The longer boom puts the laser 300 mm ahead of the tracks, so keep the Class 2 rule of switching the laser off out of the pipe.

### TRL 4

TRL 4 remains on hold by Amish's instruction. Decided but on hold: measuring submerged track friction and drawbar pull on silt, calibrating the ring in 300, 600 and 900 mm reference pipes, and getting real supplier quotes. `trl: 3` and `trl_target: 3` are unchanged.

## Session 2026-09-26: sources strengthened

Amish asked for the weaker sources in the README to be fixed. Every link kept or added was fetched and checked against the claim (World Bank flood assessment, FHWA culvert program, WSDOT injunction page, FDOT Section 430, GFDRR Cambodia). No controlled document changed; `docs/01-problem.md` did not share any of the replaced claims.

| Where | Old source | New source |
| --- | --- | --- |
| United Kingdom and northern Europe row | Uncited | Row narrowed to the United Kingdom: over one million culverts and outfalls with blockage and sedimentation risk (CIRIA and Environment Agency *Culvert, screen and outfall manual*, GOV.UK page), plus Devon County Council culvert guidance |
| India row | Uncited | Press Information Bureau (Government of India) PMGSY factsheet: about 783,700 km completed by August 2025; maintenance payments tied to the condition of cross-drainage works |
| East Africa row | World Bank 2022 flood assessment, plus an uncited claim about silted culverts on unpaved roads | Row renamed Mali and Sudan, the countries the same World Bank source names, and limited to what it states |
| Burning platform, culvert sentence | Uncited claim that many failures start at culverts | Softened to a statement that culverts are among the buried links in those networks |

The inspiration event (FDOT Standard Specifications Section 430) is unchanged; its link was rechecked against the quoted clause. No budget change.

## Session 2026-09-26: budget approved

On 2026-09-26 Amish wrote: "i approve all the budget items." The open budget item (the $5 from the ballast and boom changes) is decided: budget set to $910 to cover the priced BOM, recorded in CVC-DDR-002 v0.2.

- `project.yaml`: `budget_usd` 900 to 910. The priced BOM is $906, so the figure covers it with $4 to spare.
- R12: **not met** ($6 over $900) to **met**. Requirement status is now 0 not met, 2 at risk (R7, R8), 1 not verifiable (R6) and 10 met on paper.
- `docs/04-calcs/sizing.py` reads the budget from `project.yaml` and was rerun (`results.csv` updated); CVC-CAL-001 v0.3, CVC-REQ-001 v0.5, CVC-PRC-001 v0.5, CVC-PRB-001 v0.5, `README.md` and `bom/bom-notes.md` quote the new figure. The concept blueprint key figure now reads "against the $910 budget", and `media/` was regenerated.
- Still awaiting Amish: output format, first partner user group, removable laser boom.

## Session 2026-09-26: product appearance model and photoreal renders

Amish chose this repo for the first batch of product renders on 2026-09-26. This session adds an appearance model for photoreal renders; no controlled document, the BOM or `cad/src/model.py` changed.

### What was added

- `cad/src/product_model.py`: `product_parts()`, `TITLE` and `RENDER_VIEWS` (hero, exploded and a crawler-only detail view). It imports `PARAMS` and `track_contact_height()` from `model.py` and rebuilds each part from the same parameters and placements as `crawler_parts()` and `surface_parts()`, so every main dimension and interface is kept. Appearance detail added:
  - Crawler hull: clear-anodized body with filleted edges and machined side flutes, teal anodized lid on its lip with a recessed name plate and accent bar, four stainless lid screws, a hex pressure-test plug, a lit status light, a dome clamp flange and a hex tether gland.
  - Tracks: lugged rubber belts over toothed sprockets and dished idlers with hub caps; slotted inner side plates.
  - Front end: fisheye camera module and lens behind a clear acrylic dome shell (bore cut through the front wall so the camera shows), black LED bezel with eight lit emitters.
  - Laser projector: clear boom with its cable visible inside, clamp collar at the dome, knurled diode housing, clear exit window around the cone mirror and an end cap.
  - Internals split for colour: worm gear motor cans, gearboxes and shafts; carrier board, Pi 4 layer with ports and heatsink, and the converter block.
  - Ballast skid plate with filleted edges, flush countersunk bolts and skid grooves; ribbed tether bend restrictor.
  - Surface kit: reel with lightened flanges, wound tether, teal A-frame with feet, crank and knob, slip ring and lead, payout counter with wheel and lit readout; rugged control case with parting groove, ribs, latches, handle, emergency stop, connectors, fuse holders and a lit tether power light; gamepad with sticks and buttons.
  - Context (hero only): a short cut-open section of 600 mm corrugated steel culvert, the laser ring lit on its wall (illustrative), a ground patch and the shared 1.75 m clay mannequin standing at the reel.
- `README.md`: hero image now points to `media/render-hero.png`, with an exploded render link. The render files are produced separately.

### Where the appearance model differs from model.py

Each item is **Proposed, awaiting Amish**.

1. **Laser head exit window and end cap.** `model.py` shows the cone mirror bare beyond a 26 mm diode housing. The appearance model splits the head into a 14 mm housing, a clear window around the mirror and a 3 mm end cap, so the head ends about 3 mm further forward (x 429 instead of 426 in the crawler frame). The ring plane stays 300 mm ahead of the dome center. Recommendation: adopt the window and cap in `model.py` at the next model revision; a bare mirror would foul in a pipe.
2. **Dome bore and dome shell.** `model.py` has no bore in the front wall and a solid dome. The appearance model cuts a bore of dome radius less 1 mm and makes the dome a 3 mm shell. Recommendation: adopt; it matches the BOM (60 mm dome bore, acrylic dome port).
3. **Status light on the lid.** Not in the BOM or `model.py`. Recommendation: keep for the render only unless Amish wants a power indicator; if kept, it is a small sealed panel LED under item 13.
4. **Payout counter bracket.** `model.py` leaves the payout counter unsupported beside the reel; the appearance model adds two small tubes from the frame. Recommendation: adopt in `model.py`.
5. **Control case position (render layout only).** Moved from beside the reel to the front left of the scene so the hero stays compact; no size changed. Recommendation: keep as a render layout.
6. **Track belt build-up.** The belt outer surface is 3 mm inside the `model.py` track radius and the lugs make up the 35 mm radius, so the contact line and track height are unchanged. No action needed.

### Status

This is an appearance model only: no tolerances, no fabrication detail and nothing beyond TRL 3. `trl: 3` and `trl_target: 3` are unchanged, and TRL 4 remains on hold.

## Session 2026-09-27: kit 1.5.0 and image quality

- Kit 1.5.0 synced: STANDARDS v1.5 (sections 12 to 15: product renders, storefront images and image quality, public release, authorship and signing), `.kit/cards.py`, `.kit/image_qc.py`, `.kit/release_gate.py`, issue templates, and the `/render-product` and `/release` commands. `CLAUDE.md` now matches `.kit/CLAUDE.md`.
- Every `media/render-*.png` recaptioned from its original render with the new layout: the title, concept label and repository sit in a band above the render and the view note in a band below it, each line wrapped to the image width, so no text overlaps other text or the render or runs off the image. `media/card.png` and `media/social-preview.png` regenerated with the same rules.
- `python .kit/image_qc.py` and `python .kit/release_gate.py` pass. trl stays 3.

## Session 2026-09-30: kit 1.7.0, design for construction and prototype build plan

Amish approved the build plan format on 2026-09-30 and asked for it in every repo, with outstanding decisions kept in a separate design decisions register. He also wrote: "If you are realising that the design cannot be built as per concept - fix the design assumptions to match and be physically feasible as you draw the illustrations."

### What was done

- Kit 1.7.0 installed (`.kit/`, `.claude/commands/`); `CLAUDE.md` replaced with `.kit/CLAUDE.md`.
- `cad/src/model.py`: rewritten as a constructable model with every component and fixing, and 94 constructability checks (`python cad/src/model.py --check`); all pass. STEP and STL regenerated (`cad/step/`, `cad/stl/`).
- `docs/decisions/0003-design-for-construction.md` (CVC-DDR-003 v0.1, Draft): every change, made under Amish's 2026-09-30 instruction to make the design physically buildable; open for his review.
- `bom/bom.csv`: 15 lines (new line 14, front bezel; new line 15, side plates and small made parts; lines 1 to 11 and 13 respecified); `bom/bom-notes.md` updated.
- `docs/04-calcs/sizing.py` and CVC-CAL-001 v0.4: masses from model volumes, fin shadow in the profiling Monte Carlo, reel and box masses from the model; `results.csv` rerun. CVC-REQ-001 v0.6, CVC-PRC-001 v0.6 and CVC-PRB-001 (budget line) updated to match.
- `cad/drawings/CVC-DWG-001` Rev P3 (`cad/src/sheets.py`); concept media regenerated (`cad/src/concept_media.py`, blueprint CVC-DWG-010 Rev P2, `media/model.glb` and `viewer.html`).
- `cad/src/build_plan_media.py` (uses `.kit/build_views.py`): two overview pictures, 19 making sketches (`cad/drawings/CVC-DWG-101` to `119`), 15 joint close-ups, 23 step pictures, a hull hole layout and a wiring diagram, all in `docs/05-build-plan/`.
- `docs/05-build-plan.md` (CVC-BLD-001 v0.1) and `docs/06-design-decisions.md` (CVC-DEC-001 v0.1).
- `project.yaml`: `design_state: constructable`; DDR-003, the build plan and the register added to `trl_evidence`. `README.md`: links line and a "Building the prototype" section (the README has no Safety section, so it sits after Key components).

### Design changes made for construction (CVC-DDR-003)

1. Hull machined from a block with a 12 mm inner rim carrying the lid O-ring and ten M4 screws; flush lid (the 3 mm lip is gone); 10 mm front wall; drive pads, idler bosses and floor pads inside.
2. Track belts 36 mm (were 40 mm) with the same outer edge, so a 3 mm side plate fits between hull and belt; width 170 mm unchanged.
3. Made side plates on both sides, held by the gearbox screws, the idler axle and three screws into the ballast plate; they tie the hull to the ballast plate.
4. Gearboxes moved 2 mm inside the rear wall, output faces on the drive pads with two screws each; lip seals in counterbores in the side walls, kept in by the side plates.
5. Idler axles: M6 shoulder bolts into blind tapped bosses in the hull walls.
6. Electronics tray on four floor pads; Pi on spacers; a deck on standoffs carries the driver, converters and IMU (the converter no longer sits inside the motor cans).
7. Camera bore in the front wall and a printed camera mount.
8. Machined front bezel (BOM line 14) clamps the dome flange on an O-ring and holds eight stock LEDs, potted; LED and laser leads through a potted hole in the front wall.
9. Laser boom carried on an 8 mm clear acrylic fin bolted to a bracket on the ballast plate's nose (it no longer touches the dome).
10. Laser head with a clear window tube and end cap holding the cone mirror (the appearance model's 2026-09-26 proposal, item 1); ring plane still 300 mm ahead.
11. Ballast plate 255 x 88 x 14 mm (was 230 x 80 x 14 mm with a bent lip), square nose, tapped for the side plates, fin bracket and eye bolt; 2.45 kg.
12. Tether strength member tied to an M8 eye bolt in the ballast plate; M10 penetrator raised to 77 mm (was on the camera axis) to clear the gearboxes.
13. Reel: two 6 mm aluminium side frames on spacer tubes, flanged bearings, hollow axle, PVC drum clamped between HDPE flanges by tie rods, shaft hubs, crank, knob brake, slip ring anchor bracket.
14. Payout counter on a bar clamped in the front spacer (review item 4 of 2026-09-26), with a USB encoder reader.
15. Surface box drop-in chassis (base board, four posts, panel); battery on its side, strapped; the case is not drilled.

### Key results (CVC-CAL-001 v0.4)

- Crawler 6.63 kg (was 5.77 kg), 3.77 kg net submerged; kit 22.2 kg, heaviest item 7.8 kg. R10 met.
- Wet uphill reach 75 m (was 52 m); 23 m if submerged track friction is 0.45. Sprocket torque 0.84 N·m against the 1 N·m rating. Recovery pull 59 N, factor 17.
- Profiling with the fin's shadow: 0.25, 0.57 and 0.97 % of diameter at 300, 600 and 900 mm. R5 met, thin margin at 900 mm.
- **R12 over the value-engineering target:** BOM $1,034 against a $910 target ($124 over). `budget_usd` unchanged.
- Status: 1 over its value-engineering target (R12), 2 at risk (R7, R8), 1 not verifiable (R6), 9 met on paper.

### Proposed, awaiting Amish

All open items are in the design decisions register (`docs/06-design-decisions.md`): accepting CVC-DDR-003; the removable boom (two bolts for the prototype); the fin shadow; the heavier crawler; and the items still open from earlier (output format, first partner, appearance-model differences).

### Stale media

The design changed visibly, so these are out of date and are made on Amish's Mac, not here: `media/render-hero.png`, `media/render-exploded.png`, `media/render-detail.png`, `media/card.png`, `media/social-preview.png`, and the appearance model `cad/src/product_model.py` (concept lid lip, 88 mm LED ring, bare cone, tube reel frame). The render files referenced by the README are not present in this copy.

### Safety

No change to the safety case. The recovery pull now goes to an eye bolt in the steel plate instead of the cable seal. The build plan adds safety stops for the battery, the 48 V tether, the laser and the leak test.

### Recommended next step

Amish reviews CVC-DDR-003 and the register (including its Value engineering section). TRL 4 remains on hold; `trl` and `trl_target` stay at 3.
