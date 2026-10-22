# Does the same mark do the same thing on different signs? (scouting, exploration only)

*22 October 2026. Script: `scripts/mark_consistency_scouting.py` (run plain and with `--coarse`). Output: `mark_consistency_scouting_output.txt`, `mark_consistency_scouting_coarse_output.txt` and the two JSON files. Not a confirmatory test.*

**Idea.** If a mark is a reusable modifier, like a grammatical ending or a classifier, then adding it should change a sign's company in the same direction whatever the base sign is. An inner line on a fish and an inner line on a jar would then shift towards the same kind of neighbours.

**Method.**
- Pairs: variant/base pairs from the blind annotation whose variant carries exactly one mark type, with 6+ uses for both signs. That gives 29 pairs.
- Shift: the variant's neighbour mix minus the base's (left and right neighbours, text edges counted).
- Two versions:
  - **Exact:** neighbours as individual signs.
  - **Coarse:** neighbours as classes (opener, closer, numeral, other), plus position in the text (first, middle or last third).
- Statistic: how alike the shifts are (cosine) for pairs with the same mark on different families, minus pairs with different marks. Null: mark labels shuffled over pairs (5,000 times).

| Version | Same mark minus different mark | Null | p |
|---|---|---|---|
| Exact neighbours | −0.07 | 0.00 | 1.00 |
| Coarse neighbour classes + position | −0.02 | 0.00 | 0.67 |

**Inner line (15 pairs, 101 cross-family comparisons):** no shared direction in either version (cosine −0.02 and −0.01).

**Verdict: no sign of a reusable modifier.** Adding an inner line changes each sign's company in its own way. That fits the reading from `inside_marks_meaning.md`, that inside-marked signs are separate words or units. It does not fit inside marks being one grammatical ending added to many words.

**Limits.**
- Only the inner line has enough pairs. Roof, antennae and crossbar have 2 pairs each (one comparison), and the top-stroke pairs are all jars, so there is no cross-family comparison.
- So this says nothing against the top-mark result. Top marks do move signs earlier consistently (`mark_classes.md`, held-out test), which is a consistent effect, just on position rather than on neighbours.
- Neighbour mixes at 6+ uses are noisy.
