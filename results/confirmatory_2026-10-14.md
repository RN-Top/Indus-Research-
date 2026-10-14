# Confirmatory results, 14 October 2026

Four hypotheses were frozen and committed (commit `9316be3`) before the holdout was touched, then each was tested once on the locked holdout of the full corpus (533 texts; settings locked in each hypothesis file). 5,000 permutations each; p-values corrected together with Benjamini-Hochberg. Raw output: `confirmatory_2026-10-14.json`. Script: `scripts/run_confirmatory.py`.

| Hypothesis | Observed | Control | q (BH) | Verdict |
|---|---|---|---|---|
| Positive control: jar sign G740 ends texts | 61.7% of its uses | 24.0% | 0.0002 | Supported |
| Stroke numerals (grouped by shape) are followed by another sign | 93.7% | 76.6% | 0.0002 | Supported |
| Short and long strokes are followed by different signs | 0.613 bits | 0.341 bits | 0.0002 | Supported |
| Texts with short strokes are seals | 74.7% | 57.6% | 0.0002 | Supported |

0.0002 is the smallest p-value 5,000 permutations can give.

## What this does and does not show

- The holdout comes from the same transcription as the exploration texts. These results show the patterns are not flukes of the exploration sample; they do not yet show they hold in other transcriptions. Replication on ICIT is the next requirement.
- The numeral results concern how stroke signs behave, not what they count. They are consistent with numbers preceding counted items, and with two distinct stroke systems.
- The seal association was found during exploration and contradicts a simple version of the ration-tablet idea (Rao 2017); it has now held on unseen texts.

## Second batch (commit `6fb502d` registered them; tested afterwards)

Raw output: `confirmatory_2026-10-14_2.json`. q-values are corrected across all six confirmatory tests to date.

| Hypothesis | Observed | Control | q (BH, all 6 tests) | Verdict |
|---|---|---|---|---|
| Numerals pair with particular following signs (fixed phrases) | 2.336 bits | 1.634 bits | 0.0002 | Supported |
| Two long strokes (G32) are followed by the fish sign (G220) | 11 times | 2.6 times | 0.0002 | Supported |

The holdout is smaller than the exploration split, so mutual information is higher in both the observed value and the control (small samples inflate it equally); the excess over the control is what counts (0.70 bits here, 0.96 in exploration). The G32-fish result rests on 11 occurrences, above the minimum of 5 but small; replication on a second corpus matters most for it.
