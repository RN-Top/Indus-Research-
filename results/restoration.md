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

70 complete, single-line ICIT texts have exactly one lost interior sign (`000`) and only known signs otherwise. Confident proposals (≥ 0.8):

| ICIT | CISI | Site / object | Text | Proposed | Confidence |
|---|---|---|---|---|---|
| 1806.1 | H-926 | Harappa, tablet | G400 G740 G840 **?** G220 | **G32** | 0.98 |
| 147.1 | — | Failaka, seal | G317 G817 **?** G90 | **G740** | 0.91 |
| 213.1 | H-1369 | Harappa, pottery | G34 **?** G33 | **G700** | 0.90 |
| 1767.2 | H-884 | Harappa, tablet | G585 **?** G32 | **G840** | 0.81 |

The full list of 70 with ranked alternatives is in `restorations_single_gap.csv`. These are checkable against photographs or drawings of the objects.

**Next.** Freeze the restorer and register a one-shot holdout test (top-1 accuracy above the n-gram baseline, and calibration) before using it more widely.
