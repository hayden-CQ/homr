---
name: TrOmr bass hallucination
description: Decoder generates phantom bass notes where bass staff is empty — pre-existing model bias
type: project
---

TrOmr decoder hallucinates bass notes/rests for grand staff input even when the bass staff contains no notes. Confirmed on piece-063 (The Entertainer) where measures 0-1 have treble-only content but output includes phantom `staff=2 rest:whole` and full octave-doubled bass lines.

**Why:** Autoregressive decoder has learned a prior that grand staff = bass voice must exist. The hallucination is in the generated tokens, not in image processing — notehead detector correctly sees nothing there. The `symbol.coordinates` (from cross-attention weights) just show where the decoder happened to attend, not what it detected.

**How to apply:** This is pre-existing on main and branch — not caused by our changes. Affects SER significantly on pieces with sparse bass parts. Queued as next task after regression isolation. User has observed the pattern on multiple pieces.
