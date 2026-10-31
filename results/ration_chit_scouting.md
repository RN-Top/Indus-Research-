# The text on a unit tablet predicts how many units it carries (scouting, descriptive)

*31 Oct 2026. Script `scripts/ration_chit_scouting.py`, output `ration_chit_scouting_output.txt`. Follows `g700_measure_ground.md`. Wells (1998; 2015) calls these tablets "ration chits".*

**Data.**
- Two-sided tablets in the merged ICIT corpus where one side reads exactly `N long strokes + G700`, in either order, and the other side carries a text: **340 tablets**, all from Harappa except 2.
  - Moulded (TAB:B): 188.
  - Incised (TAB:I): 150.
- N (units): 3 → 136, 2 → 105, 4 → 95, 1 → 2, 6 → 2.

**Test.** Do tablets with the **same** text on the other side carry the **same** N more often than chance? N is shuffled 10,000 times.

| Set | Same-text pairs | Same N | Chance | p |
|---|---|---|---|---|
| All | 531 | **0.50** | 0.33 | 0.0002 |
| Incised only (each made by hand, not from a mould) | 439 | **0.48** | 0.33 | 0.0005 |
| Moulded only | 50 | **0.58** | 0.34 | 0.0009 |
| Without the commonest text (G176 G740 G400, 28 tablets) | 125 | **0.59** | 0.33 | 0.0001 |
| Each text capped at 4 tablets | 115 | **0.56** | 0.33 | 0.0001 |

- The first sign of the text side also carries information about N (mutual information 0.75 vs 0.63 bits shuffled, p = 0.0005).
- Examples:
  - G416 G861 G2 → 4 units on all 5 tablets.
  - G176 G156 → 4 on all 4.
  - G140 G1 G31 G740 → 2 on all 3.
  - G740 alone → 2 on all 4.
  - G13 G840 G740 → 3 on all 3.
  - G176 G740 G400 → mostly 3 (17), sometimes 4 (9).

**Reading.**
- On these tablets **the amount is tied to the text.** The same name, office or item goes with the same number of G700 units more often than chance, though not always.
- This is what allocation tokens look like: a fixed allotment per recipient or per commodity. It supports Wells's "ration chit" idea and the reading of G700 as a measure.
- It holds on hand-incised tablets, so it is **not** just mould duplication.

**Status.** All existing tablets have been seen, so this is sealed as prediction **P17** (`predictions/new_finds_P17_unit_tablets_2026-10-31.json`), to be tested on newly published unit tablets.

**Limits.**
- One site (Harappa).
- Some texts take two values (3 and 4), which could be two grades or two periods. Period labels are too sparse to check.
- Prior work: Wells proposed ration chits. Whether he tested text-predicts-amount is not known (Wells 2015, ch. 4, unread).

## Task 2: vessel types of pots marked with G700 + long strokes, not possible from the corpus
- The pots are H-371 (6 units), H-372 (3), H-2272 (3), M-1374 (3), M-1588 (1) and H-1550 (1, Period 2).
- None of them has a vessel shape recorded in the corpus. The shapes and sizes would have to come from the CISI catalogue entries or from Wells 2015, ch. 4.
