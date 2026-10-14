# Confirmatory results, 14 October 2026

Four hypotheses were frozen and committed (commit `9316be3`) before the holdout was touched, then each was tested once on the locked holdout of the full corpus (528 texts; settings locked in each hypothesis file). 5,000 permutations each; p-values corrected together with Benjamini-Hochberg. Raw output: `confirmatory_2026-10-14.json`. Script: `scripts/run_confirmatory.py`.

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
