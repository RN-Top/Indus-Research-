# Does the function stay the same across sites?

*Exploratory. 14 October 2026. Exploration split only: 1,523 distinct texts, duplicates removed. Nothing was registered and the holdout was not read. Script: `scripts/functional_by_site.py`; output in `functional_by_site_output.txt` and `functional_by_site.json`.*

**The idea (Erin's).** If the signs carry function rather than one spoken language, the functional skeleton should be the stable layer across the civilization, while the particular signs used in each slot might vary from place to place.

**Texts per site:**

| Site | Texts | Seals |
|---|---|---|
| Mohenjo-daro | 777 | 673 |
| Harappa | 499 | 189 |
| Dholavira | 51 | 44 |
| Lothal | 44 | 31 |
| Kalibangan | 32 | 22 |
| Chanhu-daro | 31 | 29 |
| other sites | 89 | 69 |

Harappa's texts are mostly tablets (283 of 499), so most comparisons are also shown for seals alone.

## A. The skeleton travels

Roles (opener, numeral, counted item, body, closer) were learned from the texts of one city. Each site's texts were then checked for whether all their role-assigned signs follow the order opener → middle → closer.

| Texts from | Roles learned at Mohenjo-daro | Roles learned at Harappa | Shuffled signs |
|---|---|---|---|
| Mohenjo-daro | 83%\* | 75% | 22–23% |
| Harappa | 79% | 80%\* | 22–31% |
| Dholavira | 70% | 74% | 27–28% |
| Lothal | 73% | 79% | 19–24% |
| Kalibangan | 83% | 85% | 24–31% |
| Chanhu-daro | 68% | 72% | 22–23% |
| other sites | 80% | 69% | 29–30% |

\* Roles learned on one half of the site's texts and scored on the other half, so no text is scored with roles taken from itself.

- **The order transfers.** Roles learned at Mohenjo-daro put 68–83% of texts in order at every other site, against 19–31% for shuffled signs. Roles learned at Harappa do the same.
- **The roles themselves agree.** Of 29 signs given a role at both cities, 24 get the same role. The 5 that differ are borderline cases (G235, G806, G220, G405, G255).
- **Seals alone tell the same story.** Transfer runs at 67–98%, against 20–37% shuffled.
- **Conformance rates are not strictly comparable across columns.** Each set of roles covers different signs, so a different set of texts is eligible to be scored. The point is that every column is far above shuffled.
- **Small sites are uncertain.** They have only 10–37 eligible texts each.

**Verdict: the functional skeleton is the same across the Indus world**, from Mohenjo-daro on the lower Indus to Kalibangan on the Ghaggar and Lothal and Dholavira in Gujarat.

## B. Do the signs filling each slot vary by place?

This compares which signs fill three slots at Mohenjo-daro and Harappa: the first sign, the last sign, and the item right after a numeral. The comparison is against a null that shuffles which city each text came from, keeping object types fixed. "Excess" is the Jensen-Shannon divergence over the shuffled value.

| Slot | Seals only | All objects (shuffled within object type) |
|---|---|---|
| first sign | excess −0.008, **p = 0.69** | excess +0.036, p = 0.002 |
| last sign | excess +0.014, **p = 0.13** | excess +0.043, p = 0.002 |
| item after a numeral | excess +0.015, **p = 0.23** | excess +0.024, p = 0.08 |
| control: any position | excess +0.011, p = 0.04 | |

- **On seals, the two cities fill the slots with the same signs.** No slot differs beyond chance, and the overall sign mix on seals differs only slightly. The handful of lopsided seal fillers rest on tiny counts (for example, G415 after a numeral, 11 at Mohenjo-daro and 0 at Harappa; G803, 18 and 1) and do not make the slot as a whole differ.
- **Across all objects, the first and last signs do differ, driven by Harappa's own text types:**
  - G400 opens 12 Harappa texts and none at Mohenjo-daro, and closes 92 at Harappa against 35. It is the already-confirmed tablet marker.
  - G700 opens or closes 19 Harappa texts and none at Mohenjo-daro.
  - Mohenjo-daro has a few closers of its own: G621 (12 against 1) and G617 (16 against 3).

**Verdict: half of the idea holds.** The skeleton is constant. On the shared medium, the seal, the signs in each slot are also largely the same at both cities. That fits one shared sign vocabulary at least as well as local variation reflecting different spoken languages, and gives no support to the latter. The real local variation is a matter of **genre**: Harappa has its own tablet tradition, marked by G400 and G700, and Mohenjo-daro a few closers of its own.

## Limits

- **Only two cities are large enough** to compare slot fillers. Harappa has 189 seals, so moderate differences could go undetected. "Not different" here means "no difference found at this sample size."
- **Small sites can only be checked for the skeleton**, not for fillers.
- **Sites differ in more than place.** They differ in date, excavation and transcription, and those differences could hide or create variation.
- **None of this bears on spoken language directly.** Shared signs in shared slots are what one script read in many languages would look like. They are also what one language would look like.

## Worth a future pre-registered test

1. **Skeleton transfer.** Roles frozen from the exploration texts of Mohenjo-daro alone; on holdout texts from all *other* sites, the slot order holds more often than within-text shuffling predicts. This is strong in exploration and tests the "function is constant" idea directly. It would need the `template_order` kind noted in `functional_reading.md`.
2. **G700 as a Harappa-specific marker**, like G400. It appears on 19 Harappa texts and no Mohenjo-daro texts, so its object type should be checked first.
3. **Not proposed:** "seal fillers are the same at both cities". Showing sameness needs an equivalence test with a pre-set margin, not the significance test used here.
