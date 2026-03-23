# Agent Research Turn Prompt

You are participating in a multi-agent research cycle to improve the accuracy of HOMR, an optical music recognition system. Multiple AI agents (Claude, Codex, Gemini) take turns analyzing the same problem. Each agent independently diagnoses, proposes, and critiques.

## Your task this turn

Read the research state document at `plans/research/state.md`. Then produce ALL of the following:

### 1. DIAGNOSE
Analyze the error data and identify patterns that suggest a **generalizable** improvement — not a per-piece fix. Look at:
- Error category distributions (which categories dominate?)
- Correlations between piece characteristics and error rates
- Structural accuracy patterns
- Known patterns listed in the state doc — can you build on them?

### 2. PROPOSE
Write a **specific code change** with:
- Which file(s) to modify and what the change does
- Predicted impact: which error categories decrease, by roughly how much
- Predicted regressions: which pieces might get worse and why
- Why this is generalizable (affects many pieces, not just one)

### 3. CRITIQUE
Review any existing proposals from other agents in the current cycle. For each:
- State whether you **agree** or **disagree**
- Explain what you checked to reach that conclusion
- If you disagree, explain specifically what will go wrong

### 4. CONVERGE
State your convergence status:
- **"I endorse [Agent X]'s proposal because [what I verified]"** — if you agree with an existing proposal
- **"I propose an alternative because [reason]"** — if you have a different approach
- **"I'm blocking [Agent X]'s proposal because [specific concern]"** — if you think a proposal will cause harm

## Rules

1. **Do not speculate about data you haven't seen.** If you need debug images, TrOmr output details, or logging that doesn't exist, file a DATA REQUEST and stop that line of analysis. Format:
   ```
   **DATA REQUEST — blocking**
   Need: {what specifically}
   Reason: {why you can't proceed without this}
   Command: {exact command for the human to run on the host}
   ```

2. **Proposals must be generalizable.** "Fix the crop for piece-066 page 7" is not valid. "Validate crop height covers both staves before sending to TrOmr" is valid.

3. **When endorsing, state what you verified.** "I agree" alone is not sufficient. Say what you checked and why you're convinced.

4. **You can read any file in the codebase.** Key files are listed in the state doc's Pipeline Map section.

5. **You cannot run eval or inference.** Predict impact based on code analysis and the available data. The human runs eval on the host.

6. **Focus on the biggest opportunities first.** Missing (40%) and extra (31%) notes account for 71% of all errors. Ties are 0% accuracy. These are where general gains live.

## Output Format

Add your turn to the state doc under `## Active Cycle` using this format:

```markdown
### Cycle {N} — {Agent Name} (Turn {M})

**Diagnosis:**
{Your findings}

**Proposal:**
{Specific code change with predictions}

**Critiques:**
{Review of other agents' proposals, or "No existing proposals to critique" if first turn}

**Convergence:**
{Your status}

**Data requests:**
{Any data you need, or "None"}
```
