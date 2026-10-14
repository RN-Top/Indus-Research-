# Iconography: do the signs go with the animal on the seal?

*14 October 2026. Exploration on the 80% split, then a once-only confirmatory test of two pre-registered hypotheses.*

## What the data records

The full corpus has a motif field (from the source database's ICONOGRAPHY table). With duplicates removed there are 1,329 seals: 842 unicorn (one-horned bull), 72 gaur, 35 zebu, 26 elephant, 19 rhinoceros, 12 buffalo, 11 tiger, and 262 with no motif recorded.

**Gaps.**
- **No field records the "standing object"** in front of the unicorn.
- Unicorn seals carry **undocumented subtype codes** (W 297, J 152, S 118, I 74, L 35 and others). The source's own label list calls all of them "one-horned bull", so they may encode the standing object, carving style or something else. They are tested below as unknown subtypes only.
- **"No motif recorded"** cannot be told apart from "seal has no animal".
- Most seals of every animal come from Mohenjo-daro, so comparisons below are made **within Mohenjo-daro seals** (673 in the exploration split) to keep site and object type from explaining the result.

## Exploration (Mohenjo-daro seals, duplicates removed)

The whole-vocabulary test compares the two groups' sign frequencies (Jensen-Shannon divergence) against 1,000 permutations of the group labels.

| Comparison | Texts in smaller group | Observed | Permuted | p |
|---|---|---|---|---|
| Unicorn vs all other seals | 229 | 0.124 | 0.111 | 0.009 |
| Unicorn vs gaur | 37 | 0.218 | 0.236 | 0.85 |
| Unicorn vs zebu | 20 | 0.338 | 0.315 | 0.21 |
| Unicorn vs elephant | 16 | 0.362 | 0.344 | 0.28 |
| Unicorn vs rhinoceros | 13 | 0.404 | 0.375 | 0.21 |
| No motif recorded vs unicorn | 105 | 0.208 | 0.149 | 0.001 |
| Unicorn subtype W vs other unicorns | 148 | 0.147 | 0.135 | 0.054 |
| Unicorn subtype J vs other unicorns | 86 | 0.178 | 0.164 | 0.086 |
| Unicorn subtype S vs other unicorns | 79 | 0.183 | 0.169 | 0.094 |
| Unicorn subtype I vs other unicorns | 32 | 0.247 | 0.254 | 0.60 |

**Single signs.** Of 52 signs in 15+ Mohenjo-daro seal texts, two passed p ≤ 0.005: G806 appears less on unicorn seals (30% vs 66% overall; all its non-unicorn seals have no motif recorded), and G741 appears more (86% vs 66%).

**Not registered: G741.** G741, together with G390, was already registered as "goes with unicorn seals" and failed on the holdout (confirmatory batch 3). Re-registering G741 alone in a narrower setting after that failure would be fishing for a pass, so it is reported here as exploratory only.

**Reading.** Comparing unicorns with individual other animals, nothing is detectable, but there are only 13 to 37 seals per animal, so a real difference could be missed. The unicorn subtypes show at most weak differences. The clearest contrast is between unicorn seals and seals with no motif recorded, which may be a data-recording effect.

## Pre-registered and tested once on the holdout

Registered in the commit that added this file's first version, before holdout access. Results below.

| Hypothesis | Observed | Control | q (BH, all tests to date) | Verdict |
|---|---|---|---|---|
