# Is each kind of object written to its own template? Pre-registered test

*20 October 2026. Registered in commit `d7d7ff4` (`hypotheses/H-2026-10-20-e1aa1a49.json`) before running. Run once with `scripts/run_external_confirmatory.py`. Raw output: `confirmatory_2026-10-20_2.json`. Scouting: `genre_scouting.md`.*

## What was registered

**The model:**
- logistic regression, fitted on all exploration texts;
- it sees only the inscription's layout: length, whether it opens with a heading sign, which closer it ends in, and whether numerals are present or at an edge;
- it does not see which other signs occur.

**What it predicts:** seal, tablet or other.

**Holdout rules:**
- texts identical to any exploration text are excluded, so mould copies cannot leak across;
- one copy per text and class is kept.

**Statistic:** balanced accuracy, where chance is 33.3%. **Null:** holdout labels permuted, with the predictions fixed, 5,000 times.

## Result

| | Holdout |
|---|---|
| New texts scored | 360: 265 seals, 76 tablets, 19 other |
| Balanced accuracy | **57.7%** |
| Shuffled labels | 33.4% |
| p | 0.0002 |
| q (BH across all 21 tests) | 0.0003 |
| **Verdict** | **Supported** |

**Descriptive, after the run:**
- **Recall per class:** seals 55%, tablets 55%, other 63%.
- **The strongest cues are closers:**
  - ending in G400, G407 or G617 points to a tablet;
  - ending in G621, G151 or G154 points to a seal;
  - a heading points slightly to a seal.

## What it means

**Seals and tablets follow different templates, and the difference is visible in the layout alone, on texts never seen before.**
- Mainly the choice of closer, which acts as a genre mark.
- This turns Wells's passing remark (1998: 83) that artefact classes "have different sign sequences and inventories" into a tested result.
- It fits the earlier confirmed object-specific closers: G400 on Harappa tablets, G407/G617 on copper tablets.

**Limits:**
- The "other" class is small (19).
- Seals are often mistaken for "other" (74 of 265).
- Layout predicts the genre well above chance but far from perfectly.
