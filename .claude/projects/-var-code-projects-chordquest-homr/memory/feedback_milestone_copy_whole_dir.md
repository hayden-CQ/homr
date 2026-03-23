---
name: Copy entire working dir for milestones
description: Test milestone builds should copy the whole working directory to include poetry venv, avoiding need for poetry install
type: feedback
---

When creating a new test milestone build, copy the entire working directory (not just overlay files onto an old milestone). This ensures the poetry venv, lock file, and all dependencies are already in place.

**Why:** Copying individual files onto an old milestone can cause dependency mismatches, missing modules, and requires running `poetry install` again.
**How to apply:** `cp -r /var/code/projects/chordquest/homr /var/code/projects/chordquest/homr_milestones/homr-test-<name>`, then swap in only the specific files that differ (e.g. configs.py for a different model).
