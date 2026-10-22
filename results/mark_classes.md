# Inside, outside, both, on top: where do marked signs sit? (scouting, exploration only)

*21 October 2026. Script: `scripts/mark_classes_scouting.py`. Classes fixed before computing, from `data/sign_marks/marks_blind_2026-10-20.csv`: OUTER = enclosure strokes, brackets, side strokes; INNER = inner line, inner dot, crossbar; TOP = roof, antennae, top strokes. Prompted by the second reader's suggestion (`second_reader.md`). Each marked sign is compared with its own plain base; differences are weighted by the marked sign's uses; null = marked/base labels permuted within each pair (2,000 times). Not a confirmatory test.*

| Marks | Pairs | Marked uses | End region (marked − base) | First position | Relative position (0 = first, 1 = last) | Signs with 4+ uses: later / earlier than base |
|---|---|---|---|---|---|---|
| Inside only | 97 | 874 | +0.04 (p 0.22) | +0.01 (p 0.88) | +0.01 (p 0.61) | 23 / 16 (p 0.34) |
| Outside only | 36 | 144 | **+0.16 (p 0.001)** | +0.10 (p 0.09) | −0.08 (p 0.43) | 8 / 5 (p 0.58) |
| Both | 4 | 31 | **+0.35 (p 0.0005)** | +0.05 | **+0.18 (p 0.0005)** | 3 / 0 (all fish: G226, G232, G234) |
| On top | 30 | 547 | **−0.26 (p 0.0005)** | **+0.13 (p 0.0005)** | **−0.24 (p 0.0005)** | **10 / 2 (p 0.04)** |

## Reading

- **Inside marks do not move a sign.** The largest class (874 uses, 39 signs with 4+ uses) shows no positional effect at all.
- **Marks on top move a sign towards the start**, and this holds across families: marked jars (G741, G742, G745, G746: 0.5–0.7 earlier than the plain jar G740), fish with roof or antennae (G235, G240), G391, G703, G100. Part of it is known: Wells (1998, 2006) describes the marked jars following the opening cluster G920 G60. The general rule "a mark on top moves a sign forward" was not found stated in the sources read.
- **Outside marks push towards the end only when pooled.** Pair by pair the effect is inconsistent (8 later, 5 earlier); the pooled result leans on the four-corner pairs already tested (`marks_test.md`).
- **Outside + inside together give the strongest end shift**, but only on fish variants (G226, G232, G234; Wells 2006, Table 4.10: 226 "overwhelmingly terminal").

**Candidate for a held-out test:** "signs carrying top marks sit earlier in texts than their plain bases" (weighted relative position, labels permuted within pairs). Expected holdout support about 130 marked tokens. Caveat: two families (jar, fish) carry most tokens.

## Held-out test (22 October 2026)

Registered as `H-2026-10-22-b2aa3439` and run once: signs with marks on top sit **0.28 earlier** (relative position) than their plain bases on 116 holdout tokens (shuffled 0.01; p 0.0002, q 0.0003). **Supported.**

Per pair on the holdout (descriptive, after the test): 11 of 13 marked signs present sit earlier, across five families: jar G741 (+0.54, 29 uses), G742 (+0.45), G745 (+0.42); fish G240 (+0.15, 39), G235 (+0.16, 19); G100 vs G90 (+0.26, 12); G702, G703, G891, G903, G159 (single uses). Earlier-than-base exceptions: G161 (−0.15, 4 uses), G391 (1 use). The jar and fish families still carry most tokens.
