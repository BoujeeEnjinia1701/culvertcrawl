---
doc_id: CVC-DDR-002
title: CulvertCrawl recommendations accepted
project: CulvertCrawl
doc_type: Design decision record
version: "0.1"
status: Draft
date: '2026-09-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002)
---

# 0002: Recommendations accepted

- **Date:** 2026-09-25
- **Status:** accepted (items 1 to 3); items 4 to 7 remain proposed, awaiting Amish

## Context

The TRL 3 review (`docs/REVIEW.md`, session 2026-09-25, TRL 3) left six items awaiting Amish. Three had a recommendation: R2 reach, R5 accuracy at 900 mm and R12 cost. Three did not: the first output format, the first partner user group and the removable laser boom. On 2026-09-25 Amish wrote: "i accept all your recommendations, go with them across all repos."

This record lists what that instruction decides, what changed in the repo, and what stays open. TRL 4 is on hold by Amish's instruction, so every decision is applied at TRL 3 (paper design, model, drawing and calculation) only.

## Options considered

The options for each item are in `docs/REVIEW.md` (TRL 3 section, "Still awaiting Amish", items 4 to 6) and in CVC-CAL-001 v0.1. Where several options were offered, the recommended option is the decision.

## Decision

*Table 1. Items decided on 2026-09-25.*

| # | Item | Decision | What changed in the repo |
| --- | --- | --- | --- |
| 1 | R2 reach in the wet, uphill design case (was 39 m against 50 m) | Decided by Amish, 2026-09-25: go with recommendation. (a) Add about 0.40 kg of ballast, plus (b) entering flooded pipes from the upstream end as operating guidance | Ballast plate enlarged from 210 x 80 x 12 mm (1.67 kg) to 230 x 80 x 14 mm (2.13 kg), set 8 mm above the track contact line (was 10 mm): `cad/src/model.py`, STEP and STL, `bom/bom.csv` line 8 ($15 to $18). Crawler 5.31 to 5.77 kg; net submerged 2.66 to 3.05 kg. Wet uphill reach 39 to 52 m; dry uphill 52 to 56 m. Upstream entry added as operating guidance in CVC-PRC-001 v0.4 and CVC-REQ-001 v0.4. Measuring submerged track friction is TRL 4 work: decided, on hold |
| 2 | R5 accuracy at 900 mm (was 1.59 %) | Decided by Amish, 2026-09-25: go with recommendation. (a) Move the laser ring plane from 200 to 300 mm ahead of the camera | `ring_d` 200 to 300 mm in `cad/src/model.py`; boom 100 mm longer; crawler length 510 to 610 mm; `bom/bom.csv` line 7 ($45 to $47). Vertical diameter error at 900 mm 1.59 to 0.97 %; at 600 mm 0.87 to 0.62 %; at 300 mm 0.35 to 0.24 %. Calibration in reference pipes is TRL 4 work: decided, on hold |
| 3 | R12 cost ($901 against $900) | Decided by Amish, 2026-09-25: go with recommendation. Accept the $1 overrun as within pricing uncertainty and revisit when real quotes exist | `budget_usd` stays 900; R12 target text unchanged; R12 status records the accepted $1. Getting real quotes is purchasing work at TRL 4: decided, on hold |

Knock-on changes, all at TRL 3:

- CVC-CAL-001 v0.1 to v0.2: results rerun against the new model and BOM; the profiling Monte Carlo now uses 2,000 trials instead of 400 so that the 95th percentile at 900 mm is stable to about 0.03 percentage points.
- Drawing CVC-DWG-001 Rev P1 to Rev P2 (ring plane, ballast, length and mass notes).
- Concept media regenerated from the model (`media/`).
- CVC-PRB-001, CVC-PRC-001 and CVC-REQ-001 v0.3 to v0.4; CVC-DDR-001 v0.1 to v0.2; `README.md`.
- `project.yaml`: unchanged (`budget_usd: 900`, `trl: 3`, `trl_target: 3`; pitch and problem wording unchanged).

### Items that remain open

These stay **Proposed, awaiting Amish**:

4. **Output format first** (PACP-style observation log, FHWA condition ratings or a deflection report). No recommendation was made.
5. **First partner user group** for field trials. Not named; partners are picked per area later.
6. **Removable laser boom** for tight or bent pipes. No recommendation was made. The question matters more now that the boom overhangs the tracks by about 300 mm.
7. **New: the $5 added by items 1 and 2.** The priced BOM is now $906, $6 over the $900 budget. Decision 3 accepted only the original $1. Recommendation: accept the $906 total on the same basis (indicative prices, revisit with real quotes). `budget_usd` is not changed.

## Consequences

- R2 and R5 move from not met to met on paper, both with thin margins; R12 remains not met by $6, of which $1 is accepted.
- Requirement status (CVC-CAL-001 v0.2): 1 not met (R12), 2 at risk (R7, R8), 1 not verifiable at TRL 3 (R6), 9 met on paper (R1, R2, R3, R4, R5, R9, R10, R11, R13).
- The crawler is 0.46 kg heavier and 100 mm longer; kit mass rises from 17.6 to 18.1 kg (R10 still met), sprocket torque at the traction limit from 0.67 to 0.73 N·m (within the 1 N·m motor rating) and the locked-track recovery pull from 50 to 53 N (factor 18.9 on the 1 kN tether).
- No cross-repo action arises from these decisions.
- No TRL 4 work is started. `trl` and `trl_target` stay at 3.
