---
doc_id: CVC-PRB-001
title: CulvertCrawl problem statement
project: CulvertCrawl
doc_type: Problem statement
version: "0.6"
status: Draft
date: '2026-09-30'
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
  change: Populate to TRL 2 (users, context, current practice, constraints, out of scope, prior work)
- version: "0.3"
  date: '2026-09-25'
  author: Amish Chadha
  change: TRL 3. Record Amish's 2026-09-25 decisions (CVC-DDR-001) on budget and pipe range; citation check
- version: "0.4"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002)
- version: "0.5"
  date: '2026-09-26'
  author: Amish Chadha
  change: Budget approved by Amish ($910, CVC-DDR-002)
- version: "0.6"
  date: '2026-09-30'
  author: Amish Chadha
  change: Priced BOM restated after the design for construction (CVC-DDR-003)
---

# CulvertCrawl problem statement

Small road culverts and storm drains, roughly 300 to 900 mm (12 to 36 in) across, are too small or too hazardous to walk through, so most of them are judged from the two ends with a flashlight. Commercial CCTV crawlers that can see and measure the inside cost tens of thousands of dollars (estimate) and are held by sewer contractors, not by the county road crews, small municipalities and watershed groups who own or survey most small culverts. CulvertCrawl is an open, garage-buildable tethered crawler that drives into the pipe, records video and measures the pipe's cross-section with a projected laser ring, so the owner can see deformation, corrosion and blockage without anyone entering the pipe.

## The problem

Culverts carry streams and runoff under roads, driveways, farm tracks and rail lines. Their failure modes develop out of sight: corrugated metal pipe rusts through at the invert, plastic pipe deflects out of round under load, joints separate and pull in soil, and sediment and debris build up until the pipe floods the road or washes out. The FHWA *Culvert Assessment and Decision-Making Procedures Manual* (FHWA-CFL/TD-10-005, 2010) rates barrel condition on exactly these features, and the older FHWA *Culvert Inspection Manual* (FHWA-IP-86-2, 1986) notes that small barrels usually have to be inspected from the ends.

Seeing the inside of a small culvert is hard for three reasons:

1. **Entry is dangerous or impossible.** A culvert is a confined space: it has limited entry and exit and is not designed for occupancy. Where it can hold a hazardous atmosphere, engulfment by water or silt, or a configuration that traps a person, it is a permit-required confined space under OSHA 29 CFR 1910.146 ([osha.gov](https://www.osha.gov/laws-regs/regulations/standardnumber/1910/1910.146)), or under 29 CFR 1926 Subpart AA in construction work, which needs an entry permit, atmospheric testing, an attendant and a rescue plan. Pipes under about 900 mm are too small for practical entry.
2. **End views miss the middle.** From the ends, an inspector sees a few meters in. A 20 to 40 m road crossing can hide a rusted-through invert, a collapsed joint or a blockage in its middle.
3. **Existing robots are expensive and specialized.** Sewer CCTV crawlers (for example the Envirosight ROVVER X, CUES and iPEK systems) do this job well, and some offer laser or multi-sensor profiling, but they are priced and supported for utility contractors. Hiring a CCTV contractor for one culvert costs several hundred to a few thousand dollars per visit (estimate), so small owners rarely do it until a failure forces the issue. Plumbers' push cameras are cheap but cannot drive, do not light a 600 mm pipe well and do not measure anything.

The missing piece is a measurement, not only a picture. Plastic pipe acceptance is judged by deflection: ASTM D2321 installation practice and state DOT specifications that follow AASHTO commonly limit installed deflection of thermoplastic pipe to about 5 % of the inside diameter, checked with a mandrel or a laser profiler. The same ring measurement shows the sag of a failing metal pipe and the depth of sediment in any pipe.

## Users and context

| User | Need | Context |
| --- | --- | --- |
| County or township road crew | Check road culverts before resurfacing, after floods and when a sinkhole appears, without calling a contractor | Two-person crew with a pickup truck, roadside ditch, traffic nearby |
| Small municipality public works | Inventory storm drain and culvert condition to plan replacements within a small budget | Mixed concrete, metal and plastic pipes, 300 to 900 mm |
| Consulting or DOT inspector | Measure deflection of newly installed plastic pipe and document defects with location | Acceptance inspection, needs a repeatable number and a report |
| Watershed or fish-passage survey group | Check culverts for blockage, perched outlets and internal barriers to fish | Rural streams, volunteers, wading access, limited funds |
| Farm, estate, rail or trail owner | See why a driveway or trail culvert floods | Occasional use, no inspection training |
| Maker or student team | Build, repair and extend an open inspection robot | Garage tools, hobby electronics |

### Operating environment

- **Pipes:** round culverts of 300 to 900 mm (12 to 36 in) inside diameter; corrugated steel or aluminium, reinforced concrete, and corrugated or smooth-wall HDPE and PVC. Straight runs of 10 to 50 m are typical of road crossings; slopes are usually a few percent.
- **Inside the pipe:** dark; standing or flowing water, often 0 to 150 mm deep; silt, sand, gravel, branches and litter; rust scale and sharp edges at holes and joints; possible wildlife.
- **At the mouth:** steep, wet ditch banks; riprap; headwalls; often a road shoulder with passing traffic.
- **Climate:** 0 to 40 °C ambient, rain and mud; equipment carried by hand from a vehicle.
- **Atmosphere:** culverts carrying streams are usually open to air, but storm drains and long or blocked pipes can hold low oxygen, hydrogen sulfide or methane. CulvertCrawl is not designed for flammable atmospheres (see the precis, CVC-PRC-001).

## Constraints

- Garage-buildable prototype, $910 USD in parts (`project.yaml`; raised from $800 to $900 by Amish on 2026-09-25, CVC-DDR-001, and to $910 on 2026-09-26 to cover the priced BOM, CVC-DDR-002). The priced BOM was $906 (CVC-CAL-001 v0.3); after the design for construction it is $1,034 (CVC-CAL-001 v0.4), and a budget change is proposed, awaiting Amish (CVC-DDR-003).
- No person enters the pipe at any stage, including recovery of a stuck crawler.
- Safe extra-low voltage only in the tether and crawler (48 V DC or less), and an eye-safe laser (Class 2 or lower) so the tool can be used by non-specialists.
- Carried by two people from a vehicle to a ditch in one trip, and set up in minutes.
- Open hardware (CERN-OHL-S-2.0) and open software (MIT), common hobby and industrial parts, and open data formats for video, profiles and observation logs.
- Observations recorded so they can be mapped to established defect codes such as the NASSCO Pipeline Assessment Certification Program (PACP, [nassco.org](https://www.nassco.org)), without claiming PACP certification.

## Out of scope

- Sanitary sewers, gas-bearing drains or any location where a flammable atmosphere may be present. The crawler is not intrinsically safe or ATEX rated.
- Pipes under 300 mm or over 900 mm, non-circular box culverts and arches (possible later variants).
- Cleaning, cutting roots or clearing blockages.
- Lateral launch, steerable camera heads with pan and tilt, sonar for full pipes, and GIS asset management software.
- Structural rating or load capacity decisions. CulvertCrawl measures shape and records condition; a qualified engineer rates the structure.

## Prior work

- **Commercial sewer CCTV crawlers.** Envirosight (ROVVER X), CUES, iPEK (ROVION) and RedZone Robotics build tethered crawlers with lights, pan-tilt cameras and, as options, laser profiling, sonar and payout counters. They set the functional benchmark and show that ring laser profiling works in practice, but cost and support model put them out of reach of small culvert owners.
- **Laser ring profiling research.** Duran, Althoefer and Seneviratne reviewed sensors for sewer inspection ("State of the art in sensor technologies for sewer inspection," *IEEE Sensors Journal* 2, no. 2, 2002) and later used a camera and ring laser profiler with a neural network to detect and classify pipe defects (*IEEE Transactions on Automation Science and Engineering* 4, no. 1, 2007). This is the measurement principle CulvertCrawl uses.
- **Open underwater ROVs.** OpenROV (2012 onward) and Blue Robotics' BlueROV2 with its Fathom tether show that a small open vehicle can stream video and control over a thin tether to a laptop, and that hobby parts can be sealed well enough for real field work.
- **Push cameras and borescopes.** Plumbing push cameras (fiberglass rod, 20 to 60 m) are cheap and widely owned but have no drive, weak lighting for 600 mm pipe and no measurement.
- **Defect coding.** NASSCO PACP gives a common vocabulary for pipe defects (deformation, cracks, joints, deposits, obstructions), and the FHWA culvert manuals give condition ratings for culvert barrels.

Sources were checked online on 2026-09-25 where possible: the OSHA 1910.146 title and confined-space definition (osha.gov), FHWA-IP-86-2 (1986) and FHWA-CFL/TD-10-005 (2010) by their FHWA and TRB catalog entries, and both Duran, Althoefer and Seneviratne papers by title and journal (the 2007 paper at volume 4, page 118). The ASTM D2321 deflection clause, the NASSCO PACP page and the product pages were not rechecked.

## Open questions

- Who is the first user group for field trials (a county road department, a watershed group or a university transportation program)? Proposed, awaiting Amish.
- The pipe range stays 300 to 900 mm (decided by Amish, 2026-09-25). With the ring plane moved to 300 mm ahead (CVC-DDR-002), CVC-CAL-001 v0.2 shows R5 met at 900 mm with a thin margin (0.97 %); users should say how often 900 mm pipes need an acceptance-grade number.
- What reach is needed? 50 m is assumed from typical two-lane and four-lane road crossings; to validate with users.
- Is an acceptance-grade deflection number (for new plastic pipe) needed, or is condition screening enough? This sets the profiling accuracy requirement.
- Should the tool produce a PACP-style report, the FHWA condition ratings, or both? Proposed, awaiting Amish.
- From which end do crews usually enter a culvert? CVC-CAL-001 v0.2 shows reach depends strongly on direction (52 m uphill against flow, more than 90 m downhill); entering flooded pipes from the upstream end is now operating guidance (CVC-DDR-002).

## User research and co-design

- [ ] Identify one or two partner users (road crew, watershed group or inspector) willing to review the concept
- [ ] Walk three to five real culverts with them and record pipe sizes, lengths, water depth, debris and access
- [ ] Validate reach, pipe range, accuracy and cost assumptions
- [ ] Revise requirements (CVC-REQ-001) from findings before freezing the design
