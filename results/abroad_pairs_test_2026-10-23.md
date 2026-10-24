# Inscriptions found abroad use sign pairs never seen at home: pre-registered test

*23 October 2026. Registered in commit `438cde9` (20:23:38 −04:00): spec `predictions/abroad_pairs_2026-10-23.json` (sha256 inside), script `scripts/abroad_pairs_test.py`, then run once. Raw output: `abroad_pairs_test_2026-10-23.json`. Scouting: `abroad_pairs_scouting.md`.*

| | Texts | Share of sign pairs never seen in home exploration texts |
|---|---|---|
| Found abroad (Ur, Kish, Failaka, Susa, Girsu, Tello, Bahrain, Oman, Iran) | 17 | **0.83** |
| Small home sites, each scored leaving its own site out | 334 | 0.49 |
| Difference | | **+0.34 (p 0.0006)** |
| **Verdict** | | **Supported** |

Test texts: 2 from the export's locked holdout, 15 from the held-out-from-export set; none had been analysed for this question. The effect is larger than in exploration (+0.19).

**Reading.** On unseen material, Indus inscriptions found abroad combine signs in ways the home script almost never does. This confirms, with a frozen test, the long-standing observation of Hunter (1932), Parpola (1994) and Laursen (2010). It fits their explanation: abroad, the signs were used to write something other than the home texts, most likely local names in another language. If so, the signs had values (sounds or words) that could be reused for foreign words: the script was not only a set of fixed home formulas.

**Descriptive, after the run.** The human figure G90 appears in 6 of the 17 abroad texts (Ur ×3, Failaka ×2, Susa), usually next to a sign it never meets at home. Laursen (2010: 116–118) proposed that a "man" sign marks personal names on Gulf seals. G90 is also the commonest base of rare compound signs at home (`rare_middle_scouting.md`). A candidate for the next test: G90 as a name marker.

**Limits.**
- 17 texts, many broken; damaged texts were kept on both sides.
- An unattested pair can come from a rare sign as well as from an unusual combination; abroad texts may use rarer signs. A follow-up should separate the two (rate among pairs of common signs only).
- The test shows difference, not what the abroad texts say.

## Robustness after the run: not just rare signs

*`scripts/abroad_pairs_robustness.py`, output `abroad_pairs_robustness_output.txt`. Descriptive, not confirmatory.*

Scoring only pairs whose two signs are both common at home (20+ uses): abroad texts still pair them in unseen ways **67% of the time (24 pairs) vs 23% (496 pairs)** for small home sites (p 0.0002, pairs permuted). The abroad texts use familiar signs in new combinations, as expected if the same script was writing different words.
