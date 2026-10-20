# S1 and S2: suffix-like closers, prefix-like openers. Predictions frozen before measuring

*19 October 2026, committed before `scripts/affix_profile.py` is run. EXPLORATION split only. From `results/substrate_angle.md`, section 5.*

## Definitions

These use the Indus exploration split, with the frozen role lists. Openers and closers are those of the hypothesis registrations.

- **Predecessor diversity of sign x:** the Shannon entropy, in bits, of the signs immediately before x.
- **Successor diversity of sign x:** the same, for the signs immediately after x.
- **Frequency-matched control:**
  - For each target sign, take all non-role signs (not openers, not closers, not numerals) whose token count is within ±30% of the target's.
  - For each of 2,000 draws, sample the same number of tokens from them and compute the entropy.
  - The test compares the target with the mean, and the 5th and 95th percentiles, of that control.

## S1: do closers behave like grammatical suffixes?

- **Suffix-like prediction:** most closers (at least 7 of the 12) have predecessor diversity **above** the 95th percentile of their matched control. They attach to many different stems.
- **Fixed-formula prediction:** most closers sit **below** the 5th percentile. They attach to a few fixed partners, like G520 after three long strokes.
- **Mixed:** anything else. That is reported as mixed.

## S2: is there a prefix-like class at the start?

- **Prefix-like prediction:** most openers (at least 4 of the 7) have successor diversity **above** the 95th percentile of their matched control.
- **Formula prediction:** most openers sit **below** the 5th percentile. This would fit the known fact that openers are mostly followed by G2 or G60.
- **Mixed:** anything else.

## What each outcome would mean for language

| Outcome | Reading |
|---|---|
| S1 suffix-like **and** S2 not prefix-like | Fits a suffixing-only system (Dravidian, also Sumerian or Elamite), or a label format with free endings |
| S2 prefix-like | Leans towards a prefixing language (Munda / Austro-Asiatic) |
| Both formula-like | The edges are fixed formulas. They say nothing about prefixing or suffixing. |

**Caveats:**
- These are text edges, not word edges. Indus inscriptions are not divided into words.
- A non-linguistic end-of-label mark could also pass S1.
- This is exploration, not a test.
