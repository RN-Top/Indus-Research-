# Copper tablets: does the inscription predict the image? Pre-registered test

*Published as a preprint: Toppe (2026), "Inscription predicts image on the Mohenjo-daro copper tablets", Zenodo, [doi:10.5281/zenodo.23503497](https://doi.org/10.5281/zenodo.23503497).*

*20 October 2026. Registered in commit `baa600e` (`hypotheses/H-2026-10-20-c3207807.json`) before running. Run once on the locked holdout with `scripts/run_confirmatory.py`. Raw output: `confirmatory_2026-10-20.json`. Background: `copper_sets.md`, `parpola2005_notes.md`.*

## What was registered

**Lookup table.** From the exploration split only: for each copper-tablet text, the image label that most of its copies carry (Wells/ICIT motif codes). 30 texts.

**Claim.** In the holdout, copper objects whose text exactly matches a lookup text carry the predicted image label more often than if labels were shuffled among all holdout copper objects.

**Settings:**
- Identical tablets are **kept**. Duplicates are the point of the test.
- "unknown" labels are not scored.
- Minimum support of 15, stated in advance.
- New test kind `text_image_lookup`, with synthetic positive and negative controls in `tests/test_core.py`.

## Result

| | Holdout |
|---|---|
| Copper objects in the holdout | 29 |
| Matched a lookup text and had a usable label (support) | **18** |
| Carried the predicted image | **16 (88.9%)** |
| Expected if images were shuffled | 23.3% |
| p, one-sided, 5,000 permutations | 0.0002 |
| q (BH across all 20 confirmatory tests) | 0.0004 |
| **Verdict** | **Supported** |

**Descriptive, after the run.**
- **Hits:**
  - hare ×4;
  - elephant ×4;
  - anthropomorphic figure ×3;
  - the 26-copy "Othr" set ×3;
  - "Othr" ×2 for G905 G32 G597 G142 G617.
- **The two misses are both texts whose lookup label came out as the coarse "Othr":**

  | Tablet | Text | Holdout label | Excavation drawing of that text |
  |---|---|---|---|
  | M-1517 | G798 G240 G845 G61 G407 | tiger | tiger (Mackay XCIII-10) |
  | M-1522 | G235 G233 G222 G740 | rhinoceros | rhinoceros (Mackay XCIII-7) |

  **So the misses come from the coarse exploration labels, not from the tablets.** This observation is post hoc and does not change the registered result.

## What it means

**On unseen tablets, the inscription predicts the picture.** Copper-tablet texts are tied to specific images, at the level of the exact sign sequence:
- G706 G33 G923 G740 → elephant;
- the hare text → hare;
- and so on.

Together with the substitutions in the excavation drawings, where one sign replaces the image (G777 for the goat image, G781 for the archer; `copper_sets.md`), this is the firmest **sign-to-meaning** link available without sound values.

**Limits:**
- These are copper tablets, one genre from one city. The same signs do not name these animals on seals (`copper_sets.md`, section 3).
- **What the text says** about the image (its name, a deity, a dedication) is not decided by this test.
- The image labels are a single coding (Wells/ICIT).
