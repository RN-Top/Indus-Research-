# Spelling variants on copper tablets: does the script swap signs by sound? (scouting, exploration only)

*20 October 2026. Script: `scripts/spelling_swaps.py`. Shapes from the blind annotation `data/sign_marks/marks_blind_2026-10-20.csv`. Not a confirmatory test.*

**Logic.** Copper tablets with the same picture but slightly different texts are the same "word" written two ways. If two signs that look nothing alike swap there, *and* swap again in other otherwise-identical texts, the likeliest reason is that they sound alike: substitution by sound is a hallmark of writing that records language (heraldry, tallies and codes do not do it). Look-alike swaps (the same base with different added marks) are uninformative.

**Caveat on anchoring.** Near-identical texts are not automatically the same word: in `copper_sets.md`, G503 G615 G740 and G503 G615 G752 G740 carry *different* pictures. Only swaps between texts with the same specific picture code count; ICIT "Othr"/"Comp" are catch-all codes and do not.

## Anchored swaps (same specific picture)

| Picture | Swap | Look-alikes? | Same swap elsewhere in the corpus |
|---|---|---|---|
| Unicorn (Bull1:W) | G744 ↔ G747 | yes (jar + different marks) | 0 |
| Unicorn (Bull1:W) | G760 ↔ G717 | **no** | 0 |
| Goat | G421 ↔ G422 | yes (G420 + different marks) | 0 |
| Elephant | ± G1 (one stroke) | — (insertion) | — |

Unanchored copper swaps (catch-all picture codes): G806 ↔ G831 (unrelated shapes), G231/G220 ↔ G233 and G904 ↔ G905 (look-alikes). Each occurs only in that copper context, never elsewhere.

## Corpus-wide one-sign swaps

520 minimal-pair contexts (distinct texts identical except one position), 437 distinct swap pairs. Swaps between the same shape family: **10%** vs 2% for random sign pairs. The other 90% are between unrelated shapes, but these are overwhelmingly signs of the same **functional class**: heading ovals G817/G820/G861, tree/count signs G390/G405/G407, numerals G3/G4, middle items G176/G923/G803/G904. That is slot-filling, which languages (word paradigms) and codes (slot values) both do.

## Verdict

**Inconclusive.** Only one swap of unrelated-looking signs is anchored by a picture (G760 ↔ G717), and it never recurs. The variation inside same-picture copper sets is mostly the *marks* on a base sign changing (G744/G747, G421/G422), which fits the marks being grammatical or graphic variation rather than different words. There is no evidence here of substitution by sound; the anchored data are too few to show its absence either.

**What would make it decisive:** more picture-anchored variants. Sources: the holdout copper tablets (a frozen, one-shot test: any anchored unrelated-shape swap that also recurs elsewhere), the excavation plate drawings for the catch-all "Othr" sets (to anchor G806 ↔ G831), and CISI volume 1.
