---
name: No eval in container
description: Never run homr evaluation or inference from the container — always provide commands for the user to run on the host
type: feedback
---

NEVER run `./run eval`, `./run spot`, `./run debug`, `poetry run homr`, or any ONNX inference from the container. TrOmr inference OOMs (exit 137) in the container.

**Why:** Container has limited memory. TrOmr ONNX inference requires more RAM than available. Multiple incidents of wasted time waiting for OOM kills.

**How to apply:** When eval/inference is needed, write the commands and tell the user to run them on the host. Paths are shared via /related/ and /var/code/projects/chordquest/.
