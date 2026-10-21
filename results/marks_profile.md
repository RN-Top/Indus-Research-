# Marks across all sign families, with blind annotation (EXPLORATION)

*20 October 2026. Exploration split only. Annotation: `data/sign_marks/marks_blind_2026-10-20.csv`, made blind to positions. Script: `scripts/marks_profile.py`. Numbers: `marks_profile.json`. Follows `marks_scouting.md`.*

**Method.** Each (variant, base) pair is compared on two measures:
- **end-region share**: text-final, or right before the closers;
- **mean position**: 0 = first, 1 = last.

**Caution about extremes.** A base at an extreme position, such as the jar G740 at the end, makes almost any variant look "earlier". This is regression to the mean. So the shifts were also compared with the shifts of all other marks, with mark labels permuted.

| Mark | Pairs | Variant later / earlier | Variant end-region vs base | Shift against other marks |
|---|---|---|---|---|
| **enclosure_strokes** | 17 | 10 / 7 | **55% vs 27%** | not distinct overall (p = 0.59) |
| top_strokes | 17 | 3 / 13 | 7% vs 63% | p = 0.06. Driven by the jar family only (G741–G746 on G740). |
| roof | 11 | 6 / 5 | 20% vs 34% | p = 0.16 |
| brackets | 10 | 5 / 5 | 66% vs 56% | none |
| inner_line, crossbar, antennae, doubled, inner_dot | | mixed | | none |
| ligature | 26 | 3 / 23 | 42% vs 65% | p = 0.0004. A regression artefact: bases are end-heavy signs such as G90. |

## The enclosure mark, pair by pair

**Every enclosed variant used 4 or more times sits later than its base, except one:**

| Variant (uses) | Base | Family | Variant end-region | Base end-region |
|---|---|---|---|---|
| G226 (19) | G220 | fish | 63% | 30% |
| G232 (7) | G220 | fish | 57% | 30% |
| G234 (4) | G220 | fish | 75% | 30% |
| G236 (12) | G220 | fish | 50% | 30% |
| G241 (7) | G220 | fish | 100% | 30% |
| G592 (4) | G590 | square | 50% | 22% |
| G804 (5) | G803 | leaf oval | 80% | 18% |
| G842 (4) | G840 | double oval | 100% | 22% |
| **G853 (9)** | G850 | diamond | **0%** | 14%. The exception: its strokes are diagonal, at the corners, a different-looking mark (`marks_scouting.md`). |

- **That is 8 of 9, across four families:** fish, square, leaf oval, double oval.
- **The overall test fails** because of eight single-use variants (n = 1) that point both ways and are pure noise.

## Verdict

- **The enclosure effect survives blind annotation for every variant with real data, bar one diagonal-stroke exception.** Several families agree.
- **The other marks show no consistent cross-family effect.** The jar strokes are one family only.

**Possible locked test:**
- the frozen list of enclosure_strokes variants from the blind annotation (all 17, so G853 and the singletons stay in);
- claim: on the holdout, they sit in the end region more than their bases;
- expected holdout support: about 20 tokens.
- Not registered without Erin's go-ahead.
