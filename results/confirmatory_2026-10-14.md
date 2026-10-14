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

## Third batch: word units and context (registered in commit `c2e3ec9`, tested afterwards)

Raw output: `confirmatory_2026-10-14_3.json`. These five used the duplicates-removed corpus (holdout: 395 distinct texts). q-values are corrected across all 11 confirmatory tests to date.

| Hypothesis | Observed | Control | q (BH, all 11) | Verdict |
|---|---|---|---|---|
| 68 learned two-sign units recur in unseen texts | 352 occurrences | 87.6 | 0.0002 | Supported |
| Opening units (G817 G2; G920 G60 G741; G692 G60) start texts | 92.7% of 41 | 26.3% | 0.0002 | Supported |
| Closing units ending in G520 end texts | 100% of 10 | 27.1% | 0.0002 | Supported |
| Within Harappa, G400 texts are tablets | 97.0% of 33 | 62.4% | 0.0002 | Supported |
| Within seals, G741/G390 texts carry the unicorn | 62.2% of 37 | 65.0% | 0.71 | **Not supported** |

## What this does and does not show

- **Word units are real.** Units learned on one set of texts recur four times more than chance in texts never examined, and the opening and closing formulas keep their slots. Inscriptions are built from recurring multi-sign units in fixed positions. The closing-unit result rests on 10 occurrences; it needs replication.
- **G400 marks the tablet genre at Harappa.** Site cannot explain it, since the test ran within Harappa. It does not hold at Mohenjo-daro in exploration, so it may be a local Harappan convention.
- **The unicorn link failed.** In exploration, G741 and G390 seemed to go with unicorn seals even within seals; on unseen seals they do not. It was most likely a chance pattern of the exploration texts, and it is withdrawn. This is the holdout doing its job.

**Running total: 11 pre-registered hypotheses tested on the holdout; 10 supported, 1 not supported.**

## Fourth batch: iconography (registered in commit `cf92e27`, tested afterwards)

| Hypothesis | Observed | Control | q (BH, all 13) | Verdict |
|---|---|---|---|---|
| Within Mohenjo-daro seals, unicorn seals use a different overall sign mix | 0.249 | 0.237 | 0.25 | Not supported |
| Within Mohenjo-daro seals, G806 texts are on non-unicorn seals | 40% of 5 | 35% | 0.63 | Not supported |

See `iconography_context.md`. **Running total: 13 tested; 10 supported, 3 not supported.**
