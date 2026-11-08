# G700 long-stroke effect within object families (2 Nov 2026, local, not committed)

Script: `scripts/g700_within_family.py`. Pre-registered in the script header before running.
Prediction: in every family with enough texts, a long stroke (G31–G36) is more often immediately followed by G700 than a short stroke (G1–G7) is, in the same direction. Falsified if a large family shows no difference or the opposite direction.
Test: one-sided Fisher exact, per object family. Data: merged corpus, `seq_strong`.

## Result

| family | long stroke → G700 | short stroke → G700 | odds ratio | one-sided p |
|---|---|---|---|---|
| TAB:B (moulded tablets) | 179/254 | 7/122 | 39 | 5e-36 |
| TAB:I (incised tablets) | 177/270 | 3/75 | 46 | 5e-24 |
| SEAL (all seal types) | 4/488 | 0/906 | ∞ | 0.015 |
| POT (all pottery) | 4/82 | 0/54 | ∞ | 0.13 |

## Reading

- **Tablets carry the effect.** Both tablet types show it strongly, so the ground is not an artefact of mixing object families.
- **Seals show the same direction but very weakly.** The seal count is small (4 hits), and the p-value is driven by a handful of texts. Treat it as consistent, not confirmed.
- **Pots are underpowered.** The direction is the same but the test can't decide it at 82 and 54 texts. The earlier "pots from Period 2" claim is not independently confirmed by this split.
- **The ground is strongest on tablets.** That fits the ration-chit result: G700 is used as a count on tablets. It does not show G700 measures anything on seals.

## Limits

- The prediction said "every family with enough texts." Seals and pots did not meet the usual bar for enough. That makes this a partial confirmation, and I'm calling it that.
- Families are coarse. A finer split (by site or period) could change the picture, and was not pre-registered.
