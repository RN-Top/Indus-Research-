# Calibrated edge test: Indus against Sumerian, Akkadian, Elamite, Old Tamil and Prakrit (EXPLORATION)

*20 October 2026. The predictions were frozen first: `drafts/edge_calibration_PREDICTIONS.md`, commit 06d6eec. Script: `scripts/edge_calibration.py`. Numbers: `edge_calibration.json`. Exploration splits only. Cuneiform comes from CDLI, using its language and genre fields.*

**Measures:**
- **W1:** how much more word-final signs repeat than word-initial signs.
- **T1:** the same, for text-final against text-initial signs.
- A value above 1 means endings are more stereotyped than beginnings.

| Corpus | Texts | W1 (words) | T1 (texts) [95% CI] |
|---|---|---|---|
| Sumerian seals | 5,714 | 0.56 | 0.35 [0.32, 0.38] |
| Akkadian seals | 1,478 | 0.19 | 0.35 [0.31, 0.40] |
| Sumerian royal | 1,589 | 0.69 | 0.20 [0.18, 0.23] |
| Akkadian royal | 2,001 | 1.29 | 0.34 [0.31, 0.39] |
| Elamite royal | 12 (too few) | 1.28 | 1.20 [0.53, 2.58] |
| Old Tamil | 107 | 2.65 | 3.74 [2.11, 4.86] |
| Prakrit | 166 | 2.60 | 0.44 [0.33, 0.67] |
| **Indus** | 1,294 | n/a | **7.99 [6.60, 9.11]** |

## Against the frozen predictions

1. **W1 is above 1 for suffixing languages: only partly.** Old Tamil (2.65) and Prakrit (2.60) are above 1. **Sumerian is not** (0.56–0.69), and Akkadian royal (1.29) is above Sumerian, the reverse of the prediction.
   - The likely reason is cuneiform spelling. Determinatives such as {d} "god" and logograms sit at the **start** of written words, so word-initial signs repeat a lot whatever the grammar.
   - So sign-level W1 measures **spelling conventions as much as grammar**.
2. **Calibration fails.** Across the 7 language corpora, T1 tracks W1 only weakly: Spearman ρ = 0.54, p = 0.22, against the required 0.6.
3. **By the rule set in advance, the Indus T1 value is uninformative about language.** No "closest language" is reported.

## What does stand out

**Indus is far beyond every language corpus on T1:** 8.0, against 0.2–3.7.
- Indus inscriptions repeat their final signs about eight times more than their first signs.
- No written language here, in seals, royal texts or donation records, comes close at the sign level.
- This agrees with `opening_profile.md`, where five closing signs end 58% of Indus texts.

**Reading:** Indus endings are a small, fixed set of closing marks, more formulaic than ordinary written language, whatever the language was.

## Conclusion

- **The edge test cannot pick a language family.** The measure does not track grammar reliably even for known languages, so it cannot be used on Indus.
- **No support for Dravidian, Elamite or Sumerian here, and none against.**
- **The one robust result is that Indus closers are extraordinarily fixed.** That is a functional fact about the inscriptions: "category marks" or "end formulas". It is not a fact about language.
