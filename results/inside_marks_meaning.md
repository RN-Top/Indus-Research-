# Do inside marks change meaning? (scouting, exploration only)

*22 October 2026. Script: `scripts/inside_marks_meaning.py` (control file: paragorth `data/derived/sign_allographs_levels.json`, not copied here). Inside marks were shown not to move signs (`mark_classes.md`). Here: does a sign with an inside mark keep different company from its plain base? Company = neighbouring signs (left and right), object type, animal on seals. Per pair: Jensen–Shannon divergence between variant and base; null = labels permuted over the pair's tokens (2,000 times). Pairs where both signs have 8+ uses. Not a confirmatory test.*

| Pairs | Pairs tested | Neighbours differ (p < 0.05) | Object type differs | Animal differs |
|---|---|---|---|---|
| Inside marks only | 12 | **11 (92%)** | 2 (17%) | 1 (8%) |
| Marks on top only | 6 | 6 (100%) | 3 (50%) | 0 |
| Outside marks only | 4 | 3 (75%) | 0 | 0 |
| **Control: "strong" allographs** (same sign drawn differently, per paragorth, validated or merged by Mahadevan) | 7 | **3 (43%)** | — | — |

Inside-marked signs keep different neighbours more often than known allographs: 11 of 12 vs 3 of 7 (Fisher one-sided p 0.04). Examples: G154 vs G151, G231 and G233 vs the fish G220, G595 vs G590, G705 and G706 vs G700, G861 vs G850 (all p ≤ 0.0005). The pair G705/G706, rated allographs of each other, does *not* differ (p 0.82), while both differ from their plain base G700.

**Reading.** An inside mark does not move a sign, but it usually makes a sign that combines with **different neighbours**, as a different word or form would, while it appears on the same kinds of objects and with the same animals. So inside marks most likely change *what* a sign says, not *where* it goes: a different unit, not a drawing variant.

**Caveats.** Small control (7 pairs) and an imported allograph list (some "strong" pairs, e.g. G806/G803, may not be allographs, which would make the control look less stable than true allographs are); neighbour divergence also reflects frequency and context mix; 12 inside pairs. A held-out test would need a frozen allograph list chosen in advance.

## Sealed prediction instead of a holdout test (22 October 2026)

Only about 8 inside-mark and 6 control pairs would have enough uses in the ICIT holdout (below the project minimum), so the claim was not run there. It is frozen as prediction **P9** for newly published inscriptions: `predictions/new_finds_P9_inside_marks_2026-10-22.json`, with the statistic, the 96 inside-mark pairs and the 18 control pairs (all "strong" drawing variants, before any use threshold) fixed in advance (tested only if at least 15 inside and 5 control pairs qualify).
