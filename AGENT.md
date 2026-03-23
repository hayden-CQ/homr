# AGENT.md

## Purpose

This repository is being used to improve HOMR's optical music recognition accuracy through targeted debugging, regression isolation, and a multi-agent research workflow.

## User Working Style

- Prefer step-by-step collaboration over broad automation.
- Prefer ergonomic project wrappers such as `Makefile` targets and `./run` scripts over raw low-level commands.
- Value generalizable fixes over per-piece patches.
- Know the evaluation pieces well enough to spot incorrect notes by inspection.

## Current Working Context

- Primary focus is the multi-agent research pipeline for OMR improvement.
- Current best known baseline is `test-staffdet` at 29% average SER.
- That build is `main` plus staff-detection changes, using model 287.
- Research state is tracked in [plans/research/state.md](/var/code/projects/chordquest/homr/plans/research/state.md).

## Evaluation Layout

- Evaluation data lives outside this repo at `/related/homr-eval/`.
- Test builds live in `/var/code/projects/chordquest/homr_milestones/`.
- Builds are symlinked into `homr-eval/builds/`.
- The current evaluation format is v2 flat-sequence SER with structural metrics.
- The old v1 measure-number-join evaluation is deprecated and unreliable for pickup pieces.

## Preferred Eval Commands

Run these from `/related/homr-eval/`:

- `./run eval <build>`: full 69-piece evaluation
- `./run spot <piece#> <build>`: quick single-piece evaluation
- `./run debug <piece#> <build>`: single-piece run with debug images
- `./run compare <run-a> <run-b>`: side-by-side run comparison
- `./run compare-piece <piece#> <run-a> <run-b>`: deep-dive one piece
- `./run rediagnose <run>`: re-run v2 diagnosis on existing output
- `./run html`: regenerate all run HTML pages

## Research Workflow

- Slash commands are shared across agents:
  - `/research`
  - `/research-status`
- Multi-agent research is coordinated through [plans/research/state.md](/var/code/projects/chordquest/homr/plans/research/state.md).
- Each turn should diagnose, propose, critique, and converge.
- Proposals must be generalizable and should predict measurable improvement.
- If needed evidence is missing, file a concrete data request instead of guessing.

## Key Technical Facts

### Staff And Parsing

- The `StaffAnchor` system detects five parallel staff lines at known symbols such as clefs, barlines, and rests.
- `parse_staffs()` iterates by voice:
  - voice 0 processes treble staves
  - voice 1 processes bass staves
- Each physical staff is parsed independently with `parse_staff_image()`.

### TrOmr Output Semantics

- TrOmr can emit both `upper` and `lower` position tokens from a single-staff crop.
- For treble crops:
  - `upper` is the real treble staff
  - `lower` is phantom bass output
- For bass crops:
  - `lower` is the real bass staff
  - `upper` is phantom treble output
- Measures are determined from TrOmr `barline` tokens, not image-processing barline detection.
- Staff assignment comes from the decoder `position` field.

### Pitch Correction

- Geometric pitch correction only affects treble in the current implementation because `position == "lower"` is skipped.
- This makes bass correction a high-value area to inspect when bass pitch accuracy regresses.

### Debug Semantics

- `symbol.coordinates` on debug images come from cross-attention weights, not notehead detection.
- `HOMR_DIAGNOSE_STAFFS=1` enables diagnostic staff logging in `staff_detection.py`.
- `HOMR_VERBOSE=1` enables broader pipeline tracing.
- `HOMR_DISABLE_GEOMETRIC_CORRECTION=1` disables geometric pitch correction.

## Known Model And Pipeline Behavior

- Model 287 is currently the better accuracy baseline.
- Model 287 configuration:
  - `encoder_dim=312`
  - `structure="hybrid"`
- Model 331 regresses bass accuracy on some pieces.
- Model 331 configuration:
  - `encoder_dim=512`
  - `structure="convnext"`
- The model never emits tie tokens in practice, despite vocabulary support.
- Tie accuracy being 0% is a real model behavior, not an evaluation bug.
- A phantom bass pattern can appear even when bass is empty; this is a pre-existing model bias.
- TrOmr may misplace the first barline in 3/4 time.
- TrOmr tends to generate a bass template pattern at system starts.

## Regression Isolation Results

- Staff-detection changes produced a net improvement of about 3 SER points, from 32% to 29%.
- The isolated dewarping rewrite is catastrophically broken and should not be reused without matching upstream assumptions.
- Model 331 is worse than model 287 on bass-heavy problem pieces.
- Pickup detection changes do not matter under v2 flat-sequence evaluation.
- Known regression classes include:
  - crop failures around key or tempo changes
  - subtle pitch shifts that flat SER magnifies

## Practical Gotchas

- `git clean -fd` can destroy untracked evaluation artifacts if they are placed inside the repo.
- `.npy` caches are model-version-specific and should be cleared when changing model families.
- TrOmr inference can hit OOM and exit 137 in the container even when the host succeeds.
- `/related/` path resolution differs between container and host; use `/var/code/projects/chordquest/` when making symlinks.
- The evaluation scripts use `poetry run homr`, so each build needs a valid Poetry environment.
- Debug logging should go to files, not stderr, because eval captures subprocess output.

## Current Best Leads

- Bass accuracy is a major opportunity area.
- Bass hallucination exists, but not every bad bass result is hallucination-driven.
- Extending or correcting geometric pitch correction for bass outputs is a credible generalizable improvement to investigate.

## What To Preserve

- Keep fixes generalizable across shared piece characteristics.
- Prefer targeted instrumentation and comparison over speculative rewrites.
- Use the research state doc as the shared source of truth when continuing multi-agent work.

# Agent Research Turn Prompt:

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
