# Edge test across candidate languages, calibrated: predictions frozen before measuring

*20 October 2026. Committed before `scripts/edge_calibration.py` is run. Exploration only.*

## The idea

All corpora are compared **sign by sign**:
- cuneiform signs for Sumerian, Akkadian and Elamite;
- syllable (akshara) units for Old Tamil and Prakrit;
- Indus signs.

## Measures

- **W1, word level.** Only for corpora with word division. W1 = (concentration of word-final signs) ÷ (concentration of word-initial signs), over words of 2 or more signs. Concentration is the Simpson index, the chance that two random items are the same sign.
  - Above 1: endings repeat more than beginnings, which is suffix-heavy.
  - About 1 or below: prefixes or beginnings matter as much.
- **T1, text level.** Available for every corpus, including Indus. T1 = (concentration of text-final signs) ÷ (concentration of text-initial signs), over texts of 3 or more signs.

## Corpora

| Corpus | Genre |
|---|---|
| Sumerian seals | Seal legends, Old Akkadian to Old Babylonian (CDLI language = Sumerian) |
| Akkadian seals | Seal legends, same periods (language = Akkadian) |
| Sumerian royal | Royal/Monumental inscriptions |
| Akkadian royal | Royal/Monumental inscriptions |
| Elamite royal | Royal/Monumental, Middle and Neo-Elamite |
| Old Tamil | Mahadevan corpus |
| Prakrit | EIAD |
| Indus | Exploration split (T1 only) |

## Predictions

1. **W1 is above 1 for the suffixing languages:** Sumerian, Elamite, Old Tamil and Prakrit. Akkadian uses verbal prefixes, so its **W1 is lower than Sumerian's** in the same genre.
2. **Calibration check, the key step.** Across the 7 language corpora, T1 must track W1 for T1 to say anything about language: Spearman rank correlation of 0.6 or more.
   - **If it does not,** T1 reflects genre or formula, not word structure. The Indus T1 value is then **uninformative about language**, and will be reported that way.
3. **Only if the calibration passes:** the reference corpus closest to Indus on T1 is reported, with a bootstrap 95% interval over texts. It is still described as "edge pattern like X", never "speaks X".

**Excluded:** Burushaski, which has no ancient texts.
