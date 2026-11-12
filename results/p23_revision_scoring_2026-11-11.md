# P23 revision 1 (scoring): result (11 Nov 2026)

Prediction and revision text: predictions/p23_revision_scoring_2026-11-11.md (hash verified before running).
Code: results/p23_revision_scoring_2026-11-11.py. Synthetic systems only; no Indus or real-language data.

## Results
| Base | Clean (validation seed 20261112) | Noisy, 10% variant forms (validation seed 20261112) | Noisy (tuning seed 20261111) |
|---|---|---|---|
| decimal | 1.00 | 0.70 | 0.68 |
| vigesimal | 1.00 | 1.00 | 1.00 |
| quinary | 1.00 | 0.59 | 0.59 |
| duodecimal | 1.00 | 1.00 | 1.00 |
| other | 1.00 | 1.00 | 1.00 |

Noisy mean on the validation seed: 0.86.

## Against the pre-registered thresholds
- clean >= 0.95: PASS.
- noisy mean >= 0.80: PASS (0.86).
- noisy per-base >= 0.90: FAIL for decimal (0.70) and quinary (0.59).

## Decision
The revision does not pass its own per-base threshold, so it is not adopted. The original rule also stays in place. Under this noise model, neither version can be trusted for decimal or quinary until we know how real numeral variants behave.

## Limits
- The noise model replaces 10% of every form with a random root, independently. Real variation is probably not like that, so this test may be harsher than real data. We can't say how harsh until we have real numeral forms with known variants.
- The tuning seed and the validation seed give nearly the same numbers, so the failure is not seed noise.
- No further rule changes are logged. Any new attempt needs its own prediction, hash and fresh seed.
