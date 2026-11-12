# Synthetic control for the P23 decision logic (11 Nov 2026)

Prediction file: predictions/synthetic_control_P23_2026-11-11.json (hash in predictions/synthetic_control_P23_2026-11-11.sha256, verified before running).
Code: results/synthetic_control_P23_2026-11-11.py (seed 20261111, 300 systems per base).

No Indus data, no licensed corpus and no real language data were used. The coder receives morpheme structure only, not the base label.

## Results
| Base | Clean | Noisy (10% of forms replaced) |
|---|---|---|
| decimal | 1.00 | 0.68 |
| vigesimal | 1.00 | 1.00 |
| quinary | 1.00 | 0.46 |
| duodecimal | 1.00 | 1.00 |
| other (no structure) | 1.00 | 1.00 |

Noisy mean across the five groups: 0.83.

## Against the pre-registered thresholds
- clean_accuracy_min 0.95: PASS (1.00).
- noisy_accuracy_min 0.80 (mean): PASS (0.83).
- per_base_min 0.90: FAIL under noise for decimal (0.68) and quinary (0.46). Applied to the clean run, all pass.

Per the falsifier, the decision logic is wrong for those two bases under noise. It is not changed in this entry. Any fix is logged as a revision, with its own hash, before any real numeral is coded.

## Why it fails (from the confusion table)
- Decimal under noise: a single variant form in the 2, 10, 20 or 100 slot breaks step 2, so the system falls to "other".
- Quinary under noise: one variant form in 5, 6–9 or 10 breaks step 3, so the system falls to "other".
- Vigesimal and duodecimal are not affected because their defining checks use fewer forms.

## Limits
- Clean accuracy of 1.00 is a sanity check on the code, not evidence. Synthetic forms follow the rule by construction.
- A real numeral system will have variants, so the noisy result matters more than the clean one.
- Nothing here says any real language or the Indus script has any base.
