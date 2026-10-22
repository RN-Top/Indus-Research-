# Counted items against formula items: pre-registered test

*22 October 2026. Registered in commit `a93c957` (`hypotheses/H-2026-10-22-43e7fcf9.json`) before running. Run once on the locked holdout with `scripts/run_confirmatory.py`. Raw output: `confirmatory_2026-10-22.json`. Background: `number_system_scouting.md`. New test kind `numeral_spread`, with controls in `tests/test_core.py`.*

## What was registered

**Claim.** Numerals right before the "count-like" signs G220 (fish), G390 and G900 take more different values than numerals right before the "formula-like" signs G520, G585 and G803. A real count of a thing should vary; a number fixed inside a name or title should not.

**Statistic.** Entropy (bits) of numeral-run values before count items minus before formula items. Null: the count/formula label shuffled over the scored runs (5,000 times).

**Power, stated before running:** about 49% at holdout size (exploration subsampled), likely optimistic. Planned support for the formula group was about 14 runs, below the project minimum of 15, accepted knowingly.

## Result

| | Exploration | Holdout |
|---|---|---|
| Runs before count items | 128 | 36 |
| Runs before formula items | 56 | 19 |
| Spread difference (bits) | +0.87 | **+0.65** |
| Expected if labels shuffled | +0.09 | +0.19 |
| p, one-sided | 0.0005 | **0.084** |
| q (BH across all 27 confirmatory tests) | — | 0.095 |
| **Verdict** | — | **Not supported** |

## Reading

- **The direction held, the significance did not.** Count items again took the wider spread (2, 3, 4, 6, 7 all common), formula items again clustered on 3 (10 of 19). The difference is about three quarters of the exploration size.
- With 19 formula runs this was close to a coin-flip test, as stated before running. A "Not supported" verdict here is weak evidence against the idea, not evidence that it is wrong.
- **Descriptive, after the run:** the formula side is less tidy in the holdout than in exploration (values 1, 2, 7, 10 and 12 also appear before G520/G585/G803), which is what pulled the result down.
- The claim cannot be re-tested on this holdout. It stays open for new texts, or for an independent corpus of different objects.
