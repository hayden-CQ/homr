---
name: Multi-agent research pipeline
description: Claude/Codex/Gemini research cycle for systematic OMR improvement — /research slash command
type: project
---

Designed a multi-agent research pipeline where Claude, Codex, and Gemini take turns diagnosing errors, proposing code changes, and critiquing each other's proposals.

**Key files:**
- `plans/research/state.md` — shared state doc, updated each turn
- `plans/omr-improvement-pipeline-design.md` — design decisions
- `.claude/commands/research.md` — `/research` slash command
- `.claude/commands/research-status.md` — `/research-status` slash command

**Process:** Human launches agent → `/research` → agent reads state, produces diagnosis/proposal/critique → commits → next agent. Max 3 cycles before human checkpoint. Agents cannot run eval — they predict impact and request debug runs when needed.

**How to apply:** When starting a research session, agents use `/research`. State doc has full error landscape, pipeline map, known patterns, and tried/rejected ideas.
