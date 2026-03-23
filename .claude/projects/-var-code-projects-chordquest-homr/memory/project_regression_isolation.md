---
name: Regression isolation results
description: Staff detection changes help (+3%), dewarping rewrite catastrophic, model 331 worse bass than 287
type: project
---

Isolated branch regression by testing changes individually against 4 diagnostic pieces (028, 032, 035, 063) then full 69-piece eval.

**Results:**
- staff_detection.py + model 287 = **29% avg SER** (best, vs 32% main)
- staff_detection.py + model 331 = worse on bass-heavy pieces (032: 6→75%, 063: 84→152%)
- staff_dewarping.py alone = catastrophic (9386% SER)
- Full branch (all changes + model 331) = 34% avg SER (worse than main)

**Why:** Model 331 (convnext, dim=512) has worse bass decoding than model 287 (hybrid, dim=312). Dewarping rewrite requires matching staff detection changes. Pickup detection irrelevant under v2 eval.

**How to apply:** Use model 287, keep staff detection changes, drop dewarping and pickup. Test builds at `/var/code/projects/chordquest/homr_milestones/homr-test-staffdet*`.
