# BOM notes

All costs are indicative USD prices for a single prototype, not quotes. Suppliers are named by type until parts are selected.

- Line numbers 1 to 12 match the callouts in `media/exploded.png`. Line 13 (hardware and consumables) has no callout.
- Every line is priced. The total is **$901** (13 lines, line 9 at 60 m), checked by `docs/04-calcs/sizing.py` against `budget_usd: 900` in `project.yaml`. The budget of $900 was decided by Amish on 2026-09-25 (CVC-DDR-001). The total is $1 (0.1 %) over; R12 is recorded as not met in CVC-CAL-001, although the gap is well inside the pricing uncertainty.
- The softest prices are the machined hull (line 1), the hybrid tether (line 9) and the conical mirror (line 7). Each could move the total by $20 to $80.
- TRL 3 specification changes, with no price change: camera run at 50 frames per second with a circular fisheye (line 5); fuse split into 10 A at the battery and 2 A on the 48 V output (line 11).
- The operator laptop is assumed to be the user's own and is not included. No SwapCell pack is used (LiFePO4 surface battery decided); if a SwapCell input is added later, the pack is priced once in the SwapCell repo and excluded from this kit, per Amish's 2026-09-25 portfolio rule.
