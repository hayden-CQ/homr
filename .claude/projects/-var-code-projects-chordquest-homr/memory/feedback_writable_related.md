---
name: /related/ paths are writable
description: Files at /related/ mount are writable, not read-only — don't ask user to make edits there
type: feedback
---

Files at `/related/` are writable. Don't assume read-only access or ask the user to edit files there manually.

**Why:** User corrected this assumption — "Don't you have access to that file to edit yourself? /related/"

**How to apply:** When editing eval scripts or other files under `/related/homr-eval/`, use Edit/Write tools directly.
