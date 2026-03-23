# Session State

## Current Task
Multi-agent research pipeline for OMR improvement — Cycle 1 complete (4 turns), ready for implementation.

## Regression Isolation (Complete)
Isolated which changes from our branch cause regressions vs improvements:

| Build | Description | Avg SER | Result |
|-------|-------------|---------|--------|
| main (f0c0df3) | Baseline, model 287 | 32% | — |
| test-staffdet | main + staff_detection changes, model 287 | **29%** | Best overall |
| test-staffdet-331 | main + staff_detection + model 331 | varies | Model 331 worse on bass |
| test-dewarping | main + staff_dewarping changes | catastrophic | 9386% SER on piece-028 |
| historical (branch) | All changes + model 331 | 34% | Worse than main |

**Key findings:**
- Staff detection changes improve SER by 3% (32→29), 24 improved, 18 regressed
- Model 331 has worse bass accuracy than 287 (piece-032: 6%→75%, piece-063: 84%→152%)
- Custom dewarping rewrite is catastrophically broken in isolation
- Pickup detection irrelevant under v2 eval

**Regression categories identified:**
1. Genuine crop failures at key/tempo changes (piece-066 pages 7+)
2. Subtle pitch shifts that flat SER amplifies (piece-002, 010, 017)

## Research Pipeline Design (Complete)
Built multi-agent research pipeline:
- **Cycle structure:** Each agent diagnoses, proposes, critiques per turn. 3 agents per cycle.
- **Convergence:** All 3 agree → ready for eval. Max 3 cycles → human decides.
- **State doc:** `plans/research/state.md` — self-contained, any agent starts cold
- **Slash commands:** `/research` (run a turn), `/research-status` (check status)
- **Design doc:** `plans/omr-improvement-pipeline-design.md`

## Research Cycle 1 Status (Complete — 4 turns)
- **Claude Turn 1:** Proposed extending geometric pitch correction to bass notes
- **Codex Turn 2:** Found `_only_keep_lower_staff_if_there_is_a_clef()` bug — promotes all bass tokens to treble when bass clef missing from first 5 chords
- **Gemini Turn 3:** Endorsed unified approach of both proposals
- **Claude Turn 4:** Corrected voice structure misunderstanding — grand staves have 1 voice, not 2. Found geo pool contamination bug. Endorsed Codex's fix as priority 1, proposed corrected geometric fix as priority 2.

### Agreed Implementation Plan
1. **Change 1 (Codex's fix):** Add `keep_lower_staff` param to `remove_duplicated_symbols()`, skip `_only_keep_lower_staff_if_there_is_a_clef()` for grand-staff streams. Gate on `is_grandstaff` from staff objects.
2. **Change 2 (revised geometric fix):** In `correct_pitches()`, split geo notes by y-coordinate for grand staves, run dual alignment (upper↔treble geo, lower↔bass geo).

### Critical Correction (Turn 4)
The state doc and profile previously said "voice 0 = treble, voice 1 = bass". This is **wrong** for grand-staff piano pieces:
- `create_grandstaffs()` merges treble+bass into 1 Staff with `is_grandstaff=True`
- Result: `number_of_voices = 1`, single voice with BOTH upper and lower tokens
- `_only_keep_lower_staff_if_there_is_a_clef()` acts on this mixed stream
- `correct_pitches()` sees merged geo notes from both staves (contaminated pool)

## Test Builds Created
Located at `/var/code/projects/chordquest/homr_milestones/`:
- `homr-test-staffdet` — main + staff_detection.py + find_peaks.py + model.py
- `homr-test-staffdet-331` — above + model 331 + transformer changes
- `homr-test-dewarping` — main + staff_dewarping.py + model.py
All symlinked in `/related/homr-eval/builds/`

## Key Technical Discoveries
- `symbol.coordinates` on debug images come from cross-attention weights, not notehead detection
- TrOmr output has ZERO tie elements despite vocabulary containing tie tokens
- Ties = 0% accuracy is real (1,971/1,971 errors), not an eval bug
- Bass hallucination is pre-existing on all builds (model bias)
- Geometric pitch correction skips bass (position=="lower" filtered out)
- Model 287 configs: encoder_dim=312, structure="hybrid"
- Model 331 configs: encoder_dim=512, structure="convnext"
- **CORRECTED:** Grand-staff pieces have 1 merged voice, NOT 2 separate voices
- `create_grandstaffs()` → `Staff.merge()` combines both staves, sets `is_grandstaff=True`
- Merged staff's `get_notes()` has notes from BOTH staves with positions relative to original 5-line staves
- `correct_pitches()` interprets all geo notes with treble clef → bass noteheads produce wrong but plausible pitches → contaminates SequenceMatcher alignment
- 41% of errors are on bass staves (estimated from per_staff_ser distribution)
- 12 pieces have bass SER >10 points worse than treble
- Worst pieces cluster into 4 failure modes: hallucination, symmetric missing+extra, pitch confusion, rhythm-only

## Next Steps
1. Human decides: implement Change 1 (lower-staff heuristic fix) and/or Change 2 (geometric correction)
2. Run eval on modified build to measure impact
3. Optionally fulfill data requests from state doc (all non-blocking)

## Files Created/Modified
- `plans/omr-improvement-pipeline-design.md` — design decisions
- `plans/research/state.md` — research state doc (Cycle 1 complete, 4 turns)
- `plans/research/agent-prompt.md` — reference prompt (superseded by slash command)
- `.claude/commands/research.md` — `/research` slash command
- `.claude/commands/research-status.md` — `/research-status` slash command
- `/related/homr-eval/scripts/rediagnose_run.py` — re-diagnose old runs with v2
- `/related/homr-eval/scripts/test_v2_any_run.py` — quick v2 comparison
- Updated: `generate_html.py`, `compare_runs.py`, `run` (all in homr-eval)

---
*Saved: 2026-03-20*
