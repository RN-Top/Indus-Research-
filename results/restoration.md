# Restoring lost signs: a calibrated restorer (exploration only; holdout untouched)

*21 October 2026. Code: `indus_workbench/restore.py`; evaluation `scripts/restore_cv.py`; proposals `scripts/restore_damaged.py` → `restorations_single_gap.csv`.*

## Method

For a hidden position, every known sign is scored by: left and right sign pairs (the n-gram approach of Yadav et al. 2010, *PLoS ONE*), two-sign contexts, a positional prior (first / last / interior by text length) and object type. Settings were chosen by a sweep on exploration fold 0 (smoothing k = 0.01; weights pair 1, two-sign 0.15, position 0.25, object 0.25) and **evaluated only on folds 1–4** (5,612 hidden signs; signs unseen in training count as misses).

| Model | Top-1 | Top-5 | Top-10 |
|---|---|---|---|
| Frequency only | 10.7% | 24.0% | 32.9% |
| Sign pairs (n-gram) | 31.0% | 50.9% | 57.6% |
| **Structured** | **31.9%** | **51.4%** | **57.9%** |

- The confirmed structure adds **under one point** over sign pairs. Most of what predicts a lost sign is its neighbours; smoothing mattered more than structure.
- **Calibration** (confidence of the top guess vs how often it is right): 0–0.2 → 5%; 0.2–0.4 → 18%; 0.4–0.6 → 34%; 0.6–0.8 → 52%; 0.8–0.9 → 74%; 0.9–1.0 → **89%**. At confidence ≥ 0.8 the restorer answers 14% of gaps and is right 83% of the time.

## Proposals for real damaged texts

**Correction (21 October 2026).** The first run read damaged texts from the ICIT export in its stored order, which for right-to-left texts is the *reverse* of reading order (checked against our corpus: 83% of R/L texts match reversed, 0.2% unreversed). Those first proposals are withdrawn. The script now reverses R/L texts, keeps L/R texts, and skips others. The cross-validated accuracy above is unaffected (it uses our reading-order corpus).

63 complete, single-line texts have exactly one lost interior sign (`000`) and only known signs otherwise. Confident proposals (≥ 0.8), in reading order:

| ICIT | CISI | Site / object | Text (reading order) | Proposed | Confidence |
|---|---|---|---|---|---|
| 512.1 | H-1816 | Harappa, tablet | G413 G575 G335 **?** G33 G740 | **G711** | 1.00 |
| 600.1 | H-2005 | Harappa, tablet | G861 **?** G175 G752 G740 | **G2** | 0.98 |
| 1316.1 | — | Dholavira, seal | G820 **?** G175 G235 G320 G920 G520 | **G2** | 0.93 |
| 3247.1 | M-835 | Mohenjo-daro, seal | G817 G2 **?** G171 G35 G740 G90 | **G61** | 0.89 |
| 3085.1 | M-636 | Mohenjo-daro, seal | G216 **?** G2 G32 G220 G235 G555 G527 | **G861** | 0.87 |
| 5468.1 | — | Rakhigarhi, cylinder seal | G688 G317 **?** G2 G361 G727 | **G920** | 0.84 |
| 290.2 | H-1112 | Harappa, tablet | G255 **?** G520 | **G70** | 0.81 |

Several complete known units: heading sign + marker (G861 G2, G820 G2) and the end formula G70 G520. The full list of 63 with ranked alternatives is in `restorations_single_gap.csv`.

**Next.** Freeze the restorer and register a one-shot holdout test (top-1 accuracy above the n-gram baseline, and calibration) before using it more widely.
