---
name: Pickup measure detection status
description: Anacrusis detection in music_xml_generator.py — current state, known limitations, and improvement ideas
type: project
---

Pickup (anacrusis) detection added in `homr/music_xml_generator.py:_first_measure_is_pickup()`.
Starts measure numbering at M0 when first measure is shorter than median measure duration.

**Current logic (commit 53f1f40, simplified):**
- `first_dur <= nominator/2` → pickup (no last-measure confirmation needed)
- Last-measure check and multi-voice consensus were tried and abandoned

**Results:** 48% → ~35% avg SER. 40 pieces improved, 21 regressed.

**Known false positives (4 pieces):** piece-067, piece-047, piece-031, piece-015
- All have first_dur = 1/3 of nominator with last_dur=0 (token stream ends with barline)
- TrOmr misplaces first barline in 3/4 time — places it after 1 beat instead of 3
- Confirmed via debug images: all notes visible in crop, this is a model-level bias
- Indistinguishable from true pickups (e.g., piece-025) by duration ratio alone

**Approaches tried and abandoned:**
1. Last-measure confirmation: most pieces have last_dur=0, doesn't help FPs
2. Sub-voice splitting (upper/lower): SymbolChord mixes positions in same chord — fundamentally broken
3. Multi-voice consensus: same SymbolChord mixing problem

**GT pickup pieces (14 of 69):** piece-008, 016, 024, 025, 027, 030, 034, 040, 041, 051, 054, 055, 065, 066

**Why:** The eval system aligns on measure number. GT M0 = pickup. Without detection, output starts M1 → every measure misaligns for pickup pieces.

**How to apply:** The 4 false positives are a TrOmr model-level issue (barline misplacement bias in 3/4 time). Cannot be fixed without retraining the model or finding a heuristic that distinguishes "TrOmr dropped beats" from "true pickup." Time-signature-aware heuristics might help (3/4 pieces are over-represented in FPs).

**Debug:** Set `HOMR_PICKUP_DEBUG=/path/to/file.log` to log decisions. Must use file path, not boolean — eval script captures subprocess stderr.
