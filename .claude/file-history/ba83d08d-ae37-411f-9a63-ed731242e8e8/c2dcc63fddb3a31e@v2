---
name: Never run poetry install in container
description: Running poetry install crashes the system — only the host should manage poetry environments
type: feedback
---

NEVER run `poetry install` or any poetry dependency management commands in the container. This crashed the system.

**Why:** Poetry install pulls heavy dependencies (torch, CUDA, etc.) that exhaust container resources and cause OOM/crashes.
**How to apply:** When creating test milestone builds, the host must run `poetry install`. If a build is missing dependencies, inform the user and let them handle it on the host. The container should only read/edit code, never install packages.
