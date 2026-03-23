---
name: Bass clef extrapolation fix
description: Reordered staff anchor fallback chain so extrapolation runs before wide search, fixing bass clef failures on small detections
type: project
---

Bass clef staff anchor failures fixed by reordering fallback chain in `find_staff_anchors` (staff_detection.py).

**Why:** Small bass clef detections (h≈62) find only 4 of 5 staff lines. The wide fallback ran first, found 5 crossing/duplicate lines, set `best_line_count=5`, and blocked the extrapolation fallback (which required `best_line_count==4`).

**How to apply:** The extrapolation-before-wide-fallback order is now committed on `feature/bass-clef-extrapolation-20260317`. When working on staff detection, keep this ordering in mind — extrapolation from N-1 clean lines is always more reliable than a wider search window that picks up noise.
