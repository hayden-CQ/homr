# Staff Crop Validation - Design Discussion

**Status:** Early Planning
**Created:** 2026-03-19
**Participants:** Human + Claude

## Open Discussion Topics

| # | Topic | Status | Notes |
|---|-------|--------|-------|
| 1 | Core Requirements | Queued | What crop failures look like, what we're trying to catch |
| 2 | Detection Strategy | Queued | Pre-TrOmr validation vs post-TrOmr filtering vs both |
| 3 | Recovery Strategy | Queued | What to do when a bad crop is detected |
| 4 | Scope of Changes | Queued | staff_parsing.py only or also staff_detection.py fixes |
| 5 | Integration with Eval | Queued | How to measure improvement |

## Decisions Made

_None yet_

## AC Candidates

_Breadcrumbs collected during discussion. These are hints for `/spec-tasks`, not finished acceptance criteria._

## Parking Lot

- Bass hallucination filtering (separate from crop validation)
- Geometric pitch correction for bass staff (separate improvement)
- Model 287 vs 331 regression (separate investigation)

## Session Log

### 2026-03-19
- Session started
- Context: staff detection changes improve avg SER 32%→29% but cause regressions on 18 pieces
- Two regression categories identified:
  1. **Genuine crop failures** (piece-066): staff detection splits grand staves at key/tempo changes, TrOmr gets half a system
  2. **Subtle pitch shifts** (piece-002, 010, 017): similar note counts but different pitches, flat SER amplifies small differences
- Current `parse_staffs` does zero validation of crop quality
