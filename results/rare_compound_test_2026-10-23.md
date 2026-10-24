# Rare compound signs keep their base's neighbours: pre-registered holdout test

*23 October 2026. Registered in commit `33b6c8f` (22:52:57 −04:00): spec `predictions/rare_compound_2026-10-23.json`, script `scripts/rare_compound_test.py`; run once on the locked holdout. Raw: `rare_compound_test_2026-10-23.json`. Scouting: `rare_middle_scouting.md`.*

| | Exploration | Holdout |
|---|---|---|
| Uses of the 102 rare built signs | 204 | 40 |
| Neighbour shared with own base | 78.9% | **75.0%** |
| Same, with bases shuffled | 66.6% | 66.9% |
| Difference | +0.12 (p 0.002) | **+0.08 (p 0.13)** |
| **Verdict** | — | **Not supported** |

**Reading.** The direction held and the rate with the true base is close to exploration (75% vs 79%), but with 40 uses the difference is not significant. The idea stays open: "a rare compound behaves like its base" is plausible, not shown. It needs more uses of rare signs than any one held-out set here has.
