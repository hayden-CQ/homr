---
name: Grand-staff voice structure — 1 merged voice, not 2
description: Grand-staff piano pieces have 1 merged voice (not treble+bass separately) — critical for understanding bass bugs
type: project
---

**CORRECTED (2026-03-20):** Earlier understanding was wrong. Grand-staff piano pieces do NOT have 2 voices.

`create_grandstaffs()` in `brace_dot_detection.py` → `Staff.merge()` combines treble+bass staves into **1 merged Staff** with `is_grandstaff=True`. Result: `_get_number_of_voices()` returns 1.

Flow for standard grand-staff piano:
1. Each system = 1 merged Staff (10-line grid, symbols from both staves)
2. `parse_staff_image()` called once per system on the merged staff
3. TrOmr sees both staves, generates upper+lower position tokens
4. `correct_pitches()` skips lower tokens AND geo pool is contaminated (both staves' noteheads with positions relative to original 5-line staves)
5. `remove_duplicated_symbols()` runs on the concatenated single-voice stream
6. `_only_keep_lower_staff_if_there_is_a_clef()` may promote all lower→upper if bass clef delayed

**Why this matters:** Claude Turn 1's and Gemini Turn 3's proposals assumed voice 1 = bass, which doesn't exist. Fixes must operate within the single merged voice. Codex's `keep_lower_staff` fix works correctly because it gates on `is_grandstaff` from the staff objects.

**How to apply:** Any bass-handling fix must work within a single voice containing both upper+lower tokens. Can't use voice index to distinguish treble from bass — must use token position field or geo note y-coordinates.
