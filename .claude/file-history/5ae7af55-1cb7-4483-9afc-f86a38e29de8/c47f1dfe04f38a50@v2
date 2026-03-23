---
name: v2 eval infrastructure
description: Flat-sequence SER eval replacing broken measure-number-join methodology
type: project
---

v2 eval replaces v1's measure-number-join with flat sequence comparison using SequenceMatcher opcodes.

**Why:** v1 joined GT and output measures by measure number. If pickup detection changed numbering (M0 vs M1 start), every subsequent measure compared against the wrong GT measure, causing catastrophic SER inflation. The apparent 48%→36% improvement from pickup detection was entirely an eval artifact — actual note accuracy was unchanged.

**How to apply:** All eval work should use v2. The v2 scripts live on `feature/flat-ser-comparison-20260318` in the homr-eval repo. Key results under v2: main=32% avg SER, branch=34% avg SER — branch is actually worse.
