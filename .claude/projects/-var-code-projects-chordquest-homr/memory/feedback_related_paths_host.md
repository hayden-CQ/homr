---
name: /related/ paths differ on host
description: /related/* symlinks resolve differently in container vs host — milestone paths must use /var/code/projects/chordquest/ prefix
type: feedback
---

/related/ paths don't map correctly on the host. When creating milestone builds or symlinks that the host eval will use, use the full /var/code/projects/chordquest/ paths (e.g. `/var/code/projects/chordquest/homr_milestones/`), not `/related/homr_milestones/`.

**Why:** The eval runs on the host, not in the container. `/related/` is a container-only symlink.
**How to apply:** Always use `/var/code/projects/chordquest/` prefix for any path that will be resolved by host-side tooling (eval scripts, symlinks in builds/).
