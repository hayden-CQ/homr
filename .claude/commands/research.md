---
description: Run a research turn in the multi-agent OMR improvement cycle
---

# Research Turn

You are participating in a multi-agent research cycle to improve the accuracy of HOMR, an optical music recognition system. Multiple AI agents (Claude, Codex, Gemini) take turns analyzing the same problem. Each agent independently diagnoses, proposes, and critiques.

## Step 1: Load Context

Read the research state document and understand where we are:

```
plans/research/state.md
```

Identify:
- What cycle number we're on (check `## Active Cycle`)
- What other agents have already contributed this cycle
- What data is available vs what's missing
- Known patterns and tried/rejected ideas

## Step 2: Produce Your Turn

### 2.1 DIAGNOSE
Analyze the error data and identify patterns that suggest a **generalizable** improvement — not a per-piece fix. Look at:
- Error category distributions (which categories dominate?)
- Correlations between piece characteristics and error rates
- Structural accuracy patterns
- Known patterns — can you build on them or find new ones?

You may read any file in the codebase. Key files are listed in the state doc's Pipeline Map.

### 2.2 PROPOSE
Write a **specific code change** with:
- Which file(s) to modify and what the change does
- Predicted impact: which error categories decrease, by roughly how much
- Predicted regressions: which pieces might get worse and why
- Why this is generalizable (affects many pieces, not just one)

### 2.3 CRITIQUE
Review any existing proposals from other agents in the current cycle. For each:
- State whether you **agree** or **disagree**
- Explain what you checked to reach that conclusion
- If you disagree, explain specifically what will go wrong

### 2.4 CONVERGE
State your convergence status:
- **"I endorse [Agent X]'s proposal because [what I verified]"**
- **"I propose an alternative because [reason]"**
- **"I'm blocking [Agent X]'s proposal because [specific concern]"**

## Step 3: Write Output

Add your turn to `plans/research/state.md` under `## Active Cycle` using this format:

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

1. **Do not speculate about data you haven't seen.** If you need debug images, TrOmr output details, or logging that doesn't exist, file a DATA REQUEST and stop that line of analysis:
   ```
   **DATA REQUEST — blocking**
   Need: {what specifically}
   Reason: {why you can't proceed without this}
   Command: {exact command for the human to run on the host}
   ```

2. **Proposals must be generalizable.** This means: applies to all pieces sharing a characteristic, not hardcoded to one piece. Specific thresholds and concrete implementations are encouraged — derive them from data analysis. "Fix piece-066 page 7" is not valid. "Validate crop height covers both staves, reject if < 2× unit_size" is valid.

3. **When endorsing, state what you verified.** "I agree" is not sufficient.

4. **You cannot run eval or inference.** Predict impact from code analysis and available data.

5. **Focus on the biggest opportunities.** Missing (40%) and extra (31%) notes = 71% of errors. Ties = 0% accuracy.

6. **Proposals must predict measurable improvement.** Target >1% avg SER reduction or >500 total error reduction. Don't waste eval runs on trivial gains.

7. **If you agree with a prior diagnosis, also investigate at least one alternative pattern.** Divergent thinking is the point of multi-agent research. Don't anchor on the first agent's framing.

8. **Image capabilities vary by agent.** If you cannot view image files (JPG/PNG), focus on XML/data analysis and note the limitation. Request that an image-capable agent examine specific debug images if needed.

9. **Commit after your turn.** After writing to the state doc, commit the change so it's versioned:
   ```
   git add plans/research/state.md && git commit -m "research: Cycle N - {Agent Name} Turn M"
   ```

## Step 4: Summarize for the Human

After writing your turn to the state doc, give the human a brief summary:
- What you found (1-2 sentences)
- What you propose (1 sentence)
- Whether you agree with existing proposals or not
- Any data requests that need fulfilling before the next turn
