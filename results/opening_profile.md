# Opening and closing profile: Indus against Old Tamil, Prakrit and Mesopotamian seals (EXPLORATION)

*19 October 2026. The predictions were frozen first, in `drafts/dravidian_opening_PREDICTIONS.md` (commit 2e86051). Script: `scripts/opening_profile.py`. Numbers: `opening_profile.json`. Exploration splits only; the holdout was not used.*

**Measures** (units are words, or signs for Indus):
- **F5:** share of texts opening with one of the 5 commonest first units.
- **F1r:** how much more often the first unit is rare than later units are.
- **F2:** share of texts closing with one of the 5 commonest last units.

| Corpus | Texts | F5 | F1r | F2 |
|---|---|---|---|---|
| Old Tamil, caves | 96 | 14% | 1.18 | 29% |
| Old Tamil, objects | 23 | 30% | 1.00 | 43% |
| Prakrit (EIAD) | 156 | **42%** | 1.04 | 35% |
| **Indus** | 1,510 | **23%** | **1.97** | **58%** |
| Mesopotamian seal legends | 8,570 | **11%** | **2.14** | 21% |

## Against the frozen predictions

- **F5 = 23%,** inside the "Old Tamil" band (at or below 30%), not the Prakrit band (at or above 35%).
- **F1r = 1.97,** clearly above Prakrit's 1.04.
- **By the rule written in advance, Indus falls on the Old Tamil side, not the Prakrit side.**

## But the decisive control goes against reading this as language

- **Mesopotamian seal legends sit in the same place,** and closer to Indus: F5 11%, F1r 2.14. Sumerian and Akkadian are not Dravidian.
- **What the two measures pick up is the habit of seal and label texts:**
  - a variable name near the start;
  - no fixed invocation such as *siddham*.

  They do **not** pick up the language.
- The Prakrit corpus differs mainly because it is made of Buddhist pillar records that open with an auspicious formula. That is a genre and religion effect.
- **F1r is weak for the small Tamil corpora.** Almost every word in a 600-word corpus counts as "rare" (88% and 74%), so the ratio is squeezed towards 1.

## New observation

**Indus endings are far more fixed than in any language corpus: F2 = 58%,** against 21–43%.
- Five closing signs end most Indus texts.
- No word-level corpus here comes close.
- That fits Indus closers being a small set of formulaic marks, or of suffix-like elements, more than a word-by-word language record.

## Conclusion

- **Not evidence for or against Dravidian.**
- The opening profile separates "label or seal habit" from "Buddhist donor-record habit". It does not separate languages.
- **A real test of Dravidian needs a grammar feature:**
  - suffix stacking, being re-annotated now with one rule set for both languages;
  - prefixes against suffixes.
- Even then, a match must beat the Mesopotamian control. Sumerian is agglutinative and suffixing too.
