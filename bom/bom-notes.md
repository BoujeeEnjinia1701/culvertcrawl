# BOM notes

All costs are indicative USD prices for a single prototype, not quotes. Suppliers are named by type until parts are selected.

- Line numbers 1 to 12 match the callouts in `media/exploded.png`. Line 13 (hardware and consumables) has no callout.
- Every line is priced. The total is **$906** (13 lines, line 9 at 60 m), checked by `docs/04-calcs/sizing.py` against `budget_usd: 910` in `project.yaml`. The budget of $900 was decided by Amish on 2026-09-25 (CVC-DDR-001) and raised to $910 on 2026-09-26 to cover the priced BOM (CVC-DDR-002). The total was $901 at CVC-CAL-001 v0.1, and Amish accepted that $1 as within pricing uncertainty, to revisit with real quotes (CVC-DDR-002). The changes he approved at the same time add $5: the ballast plate grows to 230 x 80 x 14 mm (line 8, $15 to $18) and the laser boom is 100 mm longer (line 7, $45 to $47). R12 was recorded as not met by $6 in CVC-CAL-001 v0.2 and is met at $910 in CVC-CAL-001 v0.3.
- The softest prices are the machined hull (line 1), the hybrid tether (line 9) and the conical mirror (line 7). Each could move the total by $20 to $80.
- TRL 3 specification changes, with no price change: camera run at 50 frames per second with a circular fisheye (line 5); fuse split into 10 A at the battery and 2 A on the 48 V output (line 11).
- The operator laptop is assumed to be the user's own and is not included. No SwapCell pack is used (LiFePO4 surface battery decided); if a SwapCell input is added later, the pack is priced once in the SwapCell repo and excluded from this kit, per Amish's 2026-09-25 portfolio rule.
