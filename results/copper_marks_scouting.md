# Copper tablets as an answer key for marks (scouting, exploration only)

*22 October 2026. Script: `scripts/copper_marks_scouting.py`. Output: `copper_marks_scouting_output.txt`, `copper_marks_scouting.json`. Holdout copper tablets not read. Not a confirmatory test.*

**Idea.** On the copper tablets the text predicts the picture (`copper_image_test.md`). So if two copper texts differ by one sign, and that sign differs only by a mark, the pictures say whether the mark changed the meaning (different picture) or not (same picture). Comparison: one-sign swaps between unrelated signs.

**Data.** 125 exploration copper objects, but only **50 carry a specific picture** (41 "Othr", 34 unknown); 24 distinct texts.

| One-sign difference | Pairs | Same picture |
|---|---|---|
| Mark swap | 2 | 0 |
| Unrelated swap | 0 | — |
| One sign added | 2 | 1 |

The two mark swaps:
- **G705 → G706** (both the jar with an inner line, the line drawn differently): G705 G33 G923 G740 G1 = composite animal; G706 G33 G923 G740 G1 = elephant. G705/G706 are rated allographs, and they did not differ in their neighbours (`inside_marks_meaning.md`, p 0.82), yet here the picture changes.
- **G423 → G424** (same base G420 with a crossbar; G423 adds small hooks at the top): gaur vs buffalo, in an otherwise identical 8-sign text.

**Verdict: too thin to test.** Both mark swaps go with a change of picture, which points the same way as the inside-marks result (marks change meaning), but two pairs prove nothing, and there are no unrelated swaps to compare against. "Composite animal" vs "elephant" may also be a coding difference rather than a different picture.

**What would make it work:**
- The 75 copper objects coded "Othr" or unknown need specific pictures. Marshall (1931) vol. III, Plates CXVII–CXVIII, Mackay (1937) and CISI vol. 1 draw many of them. Coding those pictures (from the drawings, blind to the texts) could roughly double the answer key.
- The holdout's 29 copper objects could then take a frozen version: "one-sign mark swaps change the picture more often than identical texts do".
- Check the G705 composite-animal tablet against its excavation drawing.

## Rerun on Mahadevan's own picture coding (IM77), 22 October 2026

*Script: `scripts/copper_marks_im77.py`; output `copper_marks_im77_output.txt`, `copper_marks_im77.json`. Data: IM77 and paragorth's unvalidated ICIT→Mahadevan sign bridge (github.com/paragorth/Indus-, MIT; not copied here). IM77 covers the same objects as ICIT, holdout included, so the ICIT holdout's copper tablets are no longer clean for a marks-picture test (at 29 objects it could not carry one anyway).*

Instead of coding the plates by hand, this uses the detailed picture coding Mahadevan already made for every copper tablet.

- 135 copper tablets; 88 with a picture and an undamaged text, but only **27 distinct texts**. Copper tablets are mostly repeated copies of a few texts.
- Identical texts carry the same animal 96% of the time (260 of 272 pairs, coarse labels).
- One-sign differences: **4 pairs** in all.
  - **Mark swap, 1:** fish G220 → G231 (fish with an inner line), same picture (goat-antelope), in an otherwise identical 7-sign text.
  - Unrelated or unmapped swap, 1: same picture.
  - One sign added, 2: one same, one different.

**Combined with ICIT:** three mark swaps. Two go with a change of picture (G705/G706; G423/G424), one does not (G220/G231).

**Verdict: this route is closed by the data itself, not by the coding.** The bottleneck is not missing picture labels. There are only about 25–30 distinct copper texts, and only a handful of pairs differ by one sign. Coding the "Othr" pictures from the excavation plates would not create more pairs, so it is not worth the effort for this question.
