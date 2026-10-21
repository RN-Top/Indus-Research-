# The enclosure mark: held-out test

*20 October 2026. Registration `hypotheses/H-2026-10-21-be9ab5ab.json` (commit `a935e82`, pushed before the run). Raw output `confirmatory_2026-10-20_3.json`. Scouting: `marks_profile.md`.*

## Question

Some Indus signs appear in two forms: a plain base, and the same base with short strokes added at its four corners or sides (the "enclosure mark"). Does adding that mark change where the sign goes in a text?

## What was locked in advance

- **Pairs:** all 17 variant/base pairs tagged `enclosure_strokes` in the blind annotation (`data/sign_marks/marks_blind_2026-10-20.csv`). No selection: singletons and lower-confidence tags included.
- **End region:** the last sign of a text, or the sign right before the trailing closers (frozen closer list from `H-2026-10-16-51b7445b`). One-sign texts excluded.
- **Statistic:** the marked form's end-region share minus its base's, weighted by how often the marked form occurs. **Null:** marked/base labels shuffled within each pair.
- **Minimum support** 15 marked tokens; one-sided; Benjamini–Hochberg over every confirmatory test so far.

## Result

| | End region | Share |
|---|---|---|
| Marked forms (holdout) | 15 of 21 | **71%** |
| Their bases (holdout) | 69 of 256 | **27%** |

Weighted difference **+0.456** (shuffled labels: +0.016); **p = 0.0002, q = 0.0003. Supported.** Exploration had shown +0.28 on 80 tokens; the holdout effect is larger, not smaller.

Per pair on the holdout (descriptive, looked at only after the test):

| Marked | Base | Marked in end region | Base in end region |
|---|---|---|---|
| G226 | G220 | 5/6 | 15/53 |
| G236 | G220 | 4/6 | 15/53 |
| G241 | G220 | 2/3 | 15/53 |
| G232 | G220 | 0/1 | 15/53 |
| G804 | G803 | 3/3 | 3/23 |
| G910 | G900 | 1/1 | 5/15 |
| G853 | G850 | 0/1 | 1/6 |

## What it means, and what it doesn't

- **Supported claim:** the four-corner strokes act like a **positional marker**: a sign that carries them tends to stand at the end of the message, where its plain form usually does not. That is the behaviour of a grammatical or functional mark (something like a case ending or a "this is the final item" flag), not of a separate word with its own meaning.
- **Narrow base on the holdout.** 16 of the 21 marked tokens come from the G220 family, 3 from G804/G803. The holdout confirms the effect where the data are, but it is mostly two families. The exploration split supported it in four families.
- **What the mark *means* is not tested.** The test shows *where* marked signs go, not what the strokes say.
- **One annotator.** The mark tags were made blind to position, but by a single reader. A second, independent reading of the 17 pairs is still the most useful check.
- **Prior work: anticipated.** Yadav & Vahia 2011 (*SCRIPTA* 3, p. 26) list modifier 906, "four vertical strokes enclosing the sign", and report that Hunter (1934) and Mahadevan (1986) said it makes a sign a "pseudo ender". Our contribution is the first pre-registered, held-out statistical test of that observation that we could find. Hunter 1934 (free at https://ufdc.ufl.edu/AA00013642/00001) and Mahadevan 1986 still to be read directly. See `prior_work_check_2026-10-20.md`.
