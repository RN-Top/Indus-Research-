# Are stroke-marked jars fused numbers? (scouting, exploration only)

*22 October 2026. Script: `scripts/fused_numbers.py`. Wells (2006, p. 153) notes numeral strokes "infixed" in signs 740 (→ 741, 742, 745, 748), 700 (→ 701, 703) and 790. Question: does the jar with k strokes (G741 = 1, G742 = 2, G745 = 3 strokes between the handles) mean the same as numeral k + jar (G1/G31, G2/G32, G3/G33 before G740)? Company = sign before and after the unit; position = relative position. Not a confirmatory test.*

| Unit | Uses | Mean position | Most common before | Most common after |
|---|---|---|---|---|
| 1 + jar | 5 | 0.64 | — | end of text (4) |
| 2 + jar | 21 | 0.64 | G840 (14) | end of text (16), G400 (4) |
| 3 + jar | 4 | 0.56 | — | end (2), G400 (2) |
| Jar alone (G740) | 736 | 0.86 | G100, G760, G176 | end of text (505) |
| G741 (1 stroke) | 110 | **0.35** | **G60 (19)**, G390, text start | G240, G590, G32 |
| G742 (2 strokes) | 24 | **0.39** | **G60 (5)**, text start | G220, G806 |
| G745 (3 strokes) | 14 | **0.22** | **text start (5)**, G60 | G235 |

Jensen–Shannon divergence of company between "k + jar" and the marked jars: 0.80–1.00 (maximum 1); between "k + jar" and the plain jar: 0.50–0.62.

**Verdict: not fused numbers.** "k + jar" behaves like the plain jar, an ending (mostly the formula G840 G32 G740). The stroke-marked jars are heading words, following the marker G60 near the start (cf. Wells's G920 G60 + marked jar; paragorth S333–S334). The strokes change the jar's word and role, not its count. This is the jar side of the confirmed top-mark result (`mark_classes.md`). The 2-stroke jar is marginally closest to "2 + jar" (0.80 vs 0.90 and 0.96), on very small numbers.
