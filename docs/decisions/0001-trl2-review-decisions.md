---
doc_id: CVC-DDR-001
title: CulvertCrawl TRL 2 review decisions
project: CulvertCrawl
doc_type: Design decision record
version: "0.2"
status: Draft
date: '2026-09-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: Record Amish's 2026-09-25 decisions on the TRL 2 review
- version: "0.2"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002)
---

# 0001: TRL 2 review decisions

- **Date:** 2026-09-25
- **Status:** accepted (items 1 to 8); items 9 to 11 remain proposed, awaiting Amish

## Context

The TRL 2 review note (`docs/REVIEW.md`, session 2026-09-25, /populate) listed nine items as "Proposed, awaiting Amish", and the precis (CVC-PRC-001 v0.2) gave a recommendation for most of them. On 2026-09-25 Amish reviewed the review points for every portfolio repo and wrote: "proceed with all of your recommendations across all batches. Make sure we don't proceed to TRL 4 on any of them."

This record lists what that instruction decides and what it leaves open because there was no recommendation to accept. TRL 4 is on hold by Amish's instruction.

## Options considered

The options for each item are in `docs/REVIEW.md` (TRL 2 section) and in CVC-PRC-001 v0.2, "Key design choices". They are not repeated here.

## Decision

*Table 1. Decided items.*

| # | Item | Decision | Where it now lives |
| --- | --- | --- | --- |
| 1 | Budget | Decided by Amish, 2026-09-25: go with recommendation. Raise `budget_usd` from $800 to $900, keeping the 60 m wired tether and slip ring | `project.yaml`, CVC-REQ-001 R12 |
| 2 | Pipe range | Decided by Amish, 2026-09-25: go with recommendation. Keep 300 to 900 mm and check the 900 mm case early at TRL 3 (done in CVC-CAL-001: R5 not met at 900 mm) | CVC-REQ-001 R1, R5 |
| 3 | Surface battery | Decided by Amish, 2026-09-25: go with recommendation. 12.8 V 20 Ah LiFePO4 with a 48 V boost for the prototype; a SwapCell-compatible input stays a later option | CVC-PRC-001 v0.3 |
| 4 | Drive | Decided by Amish, 2026-09-25: go with recommendation. Tracks rather than wheels | CVC-PRC-001 v0.3 |
| 5 | Power architecture | Decided by Amish, 2026-09-25: go with recommendation. Surface power over the tether at 48 V DC; no battery in the crawler | CVC-PRC-001 v0.3, CVC-REQ-001 R11 |
| 6 | Profiling sensor | Decided by Amish, 2026-09-25: go with recommendation. Class 2, 520 nm laser ring ahead of a fixed fisheye camera, rather than structured light, stereo or a pan-tilt head | CVC-PRC-001 v0.3 |
| 7 | Processing | Decided by Amish, 2026-09-25: go with recommendation. Ring extraction and reports on the operator's laptop; the crawler streams video and sensor data | CVC-PRC-001 v0.3 |
| 8 | Pitch and problem wording | Decided by Amish, 2026-09-25: go with recommendation. Unchanged; the TRL 2 review recommended no rewording | `project.yaml`, `README.md` |

Notes on the portfolio-wide approvals from the same instruction:

- **SwapCell.** CulvertCrawl does not use a SwapCell pack. If the later SwapCell-compatible input is taken up, it should cite SwapCell interface v0.3, whose item W (wake on a coded INTERLOCK loop, no CAN host needed) removes the CAN heartbeat concern raised at TRL 2. A shared SwapCell pack would be priced once in the SwapCell repo and excluded from this kit budget.
- **Co-design partners** are picked per area later; the first partner stays open (item 10).

### Items that remain open

These had no recommendation to accept and stay **Proposed, awaiting Amish**:

9. **Output format first:** a PACP-style observation log, FHWA condition ratings or a deflection report. No preference was stated.
10. **First partner user group** for field trials (county road department, watershed group or university transportation program). Not named.
11. **Removable laser boom** for tight or bent pipes. Marked "proposed" in CVC-PRC-001 v0.2 without a recommendation.

The new proposals from the TRL 3 calculations (R2 reach, R5 at 900 mm and R12 cost) were decided by Amish on 2026-09-25 by accepting the recommendations; see CVC-DDR-002 (`docs/decisions/0002-recommendations-accepted.md`). Items 9 to 11 had no recommendation and stay open.

## Consequences

- `project.yaml` `budget_usd` is 900. The priced BOM is $901, so R12 is recorded as not met by $1 (CVC-CAL-001).
- R5 keeps its 1 % target over 300 to 900 mm and is recorded as not met at 900 mm.
- CVC-PRB-001, CVC-PRC-001 and CVC-REQ-001 move to version 0.3 with these decisions recorded.
- No TRL 4 work is started.
