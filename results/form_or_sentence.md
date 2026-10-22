# Is a seal text a sentence or a form? (scouting, exploration only)

*22 October 2026. Script: `scripts/form_or_sentence.py`. Mutual information (MI) between two positions across texts, against one position shuffled among texts (5,000 times; keeps both sets of choices). Frozen opener and closer lists from `H-2026-10-16-51b7445b`. Not a confirmatory test.*

| Positions compared | Texts | MI excess over shuffled (bits) | p |
|---|---|---|---|
| Opener vs closer, framed texts (opener first, closer last) | 256 | **+0.02** | 0.25 |
| Opener vs sign just before the closer, framed texts | 256 | −0.04 | 0.82 |
| First vs last sign, all texts of 4+ signs | 1,019 | +0.16 | 0.0002 |
| First vs second sign (neighbours, for scale) | 1,019 | +1.21 | 0.0002 |
| Second-last vs last sign (neighbours, for scale) | 1,019 | +1.05 | 0.0002 |

**Reading.** Neighbouring signs depend strongly on each other (the fixed clusters Wells described, such as G920 G60 + marked jar). But once a text has the full frame, **the heading does not predict the ending**, nor the sign before it: the two ends are chosen independently, as fields on a form are, not linked as the parts of a sentence often are (agreement, government). The small first-vs-last dependency over all texts comes from mixing text types (framed, frame-less, complex), not from links inside a framed text.

**Caveats.** 256 framed texts; MI detects any dependency but has limited power for weak ones; a sentence with no agreement between its ends would look the same. A holdout version would need a bounded (equivalence) claim and has about 60 framed texts.
