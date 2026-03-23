---
name: Bass geometric pitch correction — two bugs identified
description: correct_pitches() skips bass tokens AND geo pool contaminated by merged staves — research Cycle 1 converged on fix
type: project
---

Two bugs in geometric pitch correction for grand-staff pieces:

**Bug 1:** `geometric_pitch_correction.py:174` filters `sym.position != "lower"`, skipping all bass tokens. Only "upper" tokens get corrected.

**Bug 2:** For merged grand staves, `staff.get_notes()` returns geometric noteheads from BOTH treble and bass staves. Their `Note.position` values were computed relative to original 5-line staves (pre-merge), so bass noteheads have positions 0-12 just like treble. When `correct_pitches()` interprets all with treble clef, bass noteheads produce plausible but wrong "treble" pitches, contaminating the SequenceMatcher alignment even for treble correction.

**Why:** `Staff.merge()` copies all symbols from both staves. `note_detection.py` assigns positions relative to per-staff 5-line grids before merging.

**How to apply:** For grand staves, split geo notes into treble/bass groups using y-coordinate (midpoint between lines 5 and 6 in 10-line merged grid). Run separate alignments for upper and lower tokens with appropriate clefs. Estimated 500-1000 error reduction.

**Key data:** 41% of errors on bass. 12 pieces have bass SER >10 points worse than treble. Pitch errors (step+octave+far_pitch) = 4,371 total.
