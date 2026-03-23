---
name: Eval data lives outside repo
description: Historical evaluation corpus and results stored at /var/code/projects/chordquest/homr-eval/ to prevent data loss from git operations
type: project
---

Evaluation data must live outside the git repo at `/var/code/projects/chordquest/homr-eval/`.

**Why:** User lost all evaluation artifacts (page images, caches, musicxml outputs for 69 pieces) when `git clean -fd` ran during a historical eval workflow that checked out commits in-place. Untracked files inside the repo are not safe.

**How to apply:** Never store generated evaluation data inside the homr repo. Use git worktrees for running different versions instead of checkout-in-place. No symlinks inside the repo (also vulnerable to git clean).
