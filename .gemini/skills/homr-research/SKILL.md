---
name: homr-research
description: Conduct research turns and view status for the HOMR (Optical Music Recognition) improvement cycle. Use when analyzing error data, proposing code changes, or checking the current research progress.
---

# HOMR Research

This skill provides workflows for participating in the multi-agent research cycle to improve the accuracy of HOMR.

## View Research Status

Use this workflow to understand the current state of the research.

1. **Load State**: Read `plans/research/state.md`.
2. **Report**: Summarize:
   - **Current baseline**: build name, avg SER, key stats.
   - **Active cycle**: which cycle, how many turns completed, by which agents.
   - **Convergence status**: are agents agreeing? What's the leading proposal?
   - **Pending data requests**: anything blocking?
   - **Key patterns found**: top 3 findings from the research so far.
   - **Next action**: what needs to happen next (another agent turn? eval run? debug run?).

## Conduct a Research Turn

Use this workflow to contribute a new diagnosis and proposal to the research cycle.

### Step 1: Load Context

Read `plans/research/state.md` and understand:
- Current cycle number (check `## Active Cycle`).
- Other agents' contributions this cycle.
- Available vs. missing data.
- Known patterns and tried/rejected ideas.

### Step 2: Produce Your Turn

1. **DIAGNOSE**: Analyze error data and identify **generalizable** improvement patterns (look at error distributions, correlations, structural patterns).
2. **PROPOSE**: Write a **specific code change** with:
   - File(s) to modify and what the change does.
   - Predicted impact (which error categories decrease).
   - Predicted regressions.
   - Why it is generalizable.
3. **CRITIQUE**: Review existing proposals from other agents. State if you agree/disagree and why.
4. **CONVERGE**: State convergence status ("I endorse...", "I propose alternative...", "I'm blocking...").

### Step 3: Write Output

Add your turn to `plans/research/state.md` under `## Active Cycle` using the following format:

```markdown
### Cycle {N} — {Your Name} (Turn {M})

**Diagnosis:**
{Your findings — patterns, correlations, hypotheses}

**Proposal:**
{Specific code change with predicted impact and regressions}

**Critiques:**
{Review of other agents' proposals, or "No existing proposals to critique"}

**Convergence:**
{Endorse / Propose alternative / Blocking — with what you verified}

**Data requests:**
{Any data you need, or "None"}
```

## Rules

1. **No Speculation**: If data is missing, file a **DATA REQUEST — blocking** with the needed data, reason, and exact command.
2. **Generalizable Proposals**: Changes must apply to characteristics, not hardcoded to one piece.
3. **Verification**: When endorsing, explicitly state what you verified.
