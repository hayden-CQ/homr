---
name: TrOmr bass template pattern issue
description: TrOmr model generates template bass patterns (A2-E3-A3) at system starts regardless of actual image content, placing notes over rests
type: project
---

TrOmr model has a strong positional prior for bass accompaniment patterns, placing note detections at fixed relative positions within each system crop rather than reading actual image content.

**Evidence (piece-025 Für Elise):**
- M5 bass should be a whole rest (visible in score) but model outputs A2-E3-A3
- Same A2-E3-A3 pattern appears at the start of systems 1-3 (M5, M9, M13)
- Annotated debug images show "note" labels overlaid directly on whole rests
- Both main-331 and our branch produce identical wrong bass in M5 — pre-existing model issue
- M5/M6 bass content is swapped in both branches (rest and notes in wrong measures)

**Why:** TrOmr learned a strong prior for left-hand accompaniment patterns from training data. The model applies a positional template rather than reading the bass staff content for each system.

**How to apply:** This is a model inference quality issue, not a staff detection or post-processing bug. May need model retraining or post-processing heuristics (e.g., cross-referencing TrOmr detections with segnet notehead detections to catch phantom notes). Address after fixing the extra measure regression.
