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
  - G700 opens or closes 19 Harappa texts and none at Mohenjo-daro. *(Corrected in section C: G700 does occur at Mohenjo-daro, just not first or last, and it is not a tablet marker.)*
  - Mohenjo-daro has a few closers of its own: G621 (12 against 1) and G617 (16 against 3).

**Verdict: half of the idea holds.** The skeleton is constant. On the shared medium, the seal, the signs in each slot are also largely the same at both cities. That fits one shared sign vocabulary at least as well as local variation reflecting different spoken languages, and gives no support to the latter. The real local variation is a matter of **genre**: Harappa has its own tablet tradition, marked by G400 and G700, and Mohenjo-daro a few closers of its own.

## Limits

- **Only two cities are large enough** to compare slot fillers. Harappa has 189 seals, so moderate differences could go undetected. "Not different" here means "no difference found at this sample size."
- **Small sites can only be checked for the skeleton**, not for fillers.
- **Sites differ in more than place.** They differ in date, excavation and transcription, and those differences could hide or create variation.
- **None of this bears on spoken language directly.** Shared signs in shared slots are what one script read in many languages would look like. They are also what one language would look like.

## Worth a future pre-registered test

1. **Skeleton transfer.** Roles frozen from the exploration texts of Mohenjo-daro alone; on holdout texts from all *other* sites, the slot order holds more often than within-text shuffling predicts. This is strong in exploration and tests the "function is constant" idea directly. It would need the `template_order` kind noted in `functional_reading.md`.
2. ~~G700 as a Harappa-specific marker.~~ **Dropped after checking (section C).**
3. **Not proposed:** "seal fillers are the same at both cities". Showing sameness needs an equivalence test with a pre-set margin, not the significance test used here.

## C. Follow-up: what is G700? (exploratory)

*Exploration split, duplicates removed. Numbers are in `g700_profile_output.txt`.*

**Correction first.** Section B counted G700 only as a first or last sign. Counting every position, it is **not Harappa-only**.

| | Texts with G700 |
|---|---|
| Harappa | 23 |
| Mohenjo-daro | 4 |
| Chanhu-daro | 1 |
| Lothal | 1 |
| **Total** | **29** (one G700 each) |

With duplicates and damaged texts kept, there are 59, 47 of them at Harappa. Harappa's tablets often come in duplicate sets, which inflates raw counts.

1. **It is not a tablet marker.**
   - At Harappa, 16 of 23 G700 texts are tablets (70%), against 57% for all Harappa texts (p = 0.14, 5,000 permutations).
   - For comparison, G400 texts at Harappa are 90% tablets.
   - Overall, G700 texts are 17 tablets, 7 seals, 2 pottery, 2 rods and 1 other.
2. **It has no slot of its own.**
   - It is first in 10 texts, last in 10, and inside the text in 9. Shuffled signs would give about 32% first and 32% last, so no position is favoured.
   - The role analysis classes it as a body sign.
3. **It sits next to numerals.**
   - 16 of its 29 uses are next to a known numeral (55%), against 29% for signs in general.
   - Its commonest neighbours are the long-stroke signs G33 (4 before, 4 after) and G34 (4 before), and G31 (3 after).
   - G34 has no drawing in our glyph map. It sits between G33 (three long strokes) and G35 (five long strokes) in the numbering, so it is probably four long strokes, but this is unverified. If it is a numeral, 20 of 29 uses (69%) are next to one.
   - Many G700 texts are just two signs: G700 G33, G33 G700, G700 G34.
4. **Its link to G400 is unclear.**
   - Across all texts, 4 contain both signs, against 3.1 expected if they were unrelated.
   - On Harappa tablets, 3 contain both, against 5.5 expected.
   - They are not mutually exclusive and not bound together. The counts are too small to say more.

**What G700 looks like:** a **counted thing**, a sign written with long-stroke numerals, as in "G700 × 3", common on Harappa tablets but not limited to them. The numeral appears both before and after it. That may be real, or it may reflect how the reading direction of short tablet texts was transcribed.

**Not worth a test as a Harappa tablet marker.** "G700 goes with long-stroke numerals" is suggestive, but it rests on 29 uses, and G34 must be identified first.

## D. The cross-site skeleton, tightened (exploratory)

*Exploration split only, duplicates removed unless stated. Script `scripts/functional_skeleton.py`; output in `functional_skeleton_output.txt` and `functional_skeleton.json`. Nothing registered; the holdout was not read.*

### D.1 One explicit role rule

The rule is simple enough to freeze for a later pre-registered test:

- **Numeral:** a stroke sign, from the fixed list of short, stacked and long strokes, chosen by shape.
- **Opener:** used at least **15** times in texts of two or more signs, and starts at least **40%** of them, and starts at least **1.8 times** as often as shuffling the signs within texts would give.
- **Closer:** the same thresholds, but ends at least **50%** of them.
- **Middle:** every other sign used at least 15 times.

A text **conforms** if its role-assigned signs never step backwards (opener → middle or numeral → closer). Only texts with role-assigned signs from at least two of the three ranks are scored.

**Roles learned from Mohenjo-daro alone:**

| Role | Signs (share of texts they start or end; shuffled share in brackets) |
|---|---|
| Closers (8) | G740 73% (20%), G520 75% (19%), G90 68% (18%), G400 81% (25%), G151 96% (31%), G617 64% (20%), G527 86% (25%), G407 74% (23%) |
| Openers (9) | G820 77% (20%), G861 70% (18%), G817 90% (19%), G920 74% (18%), G692 79% (17%), G503 48% (21%), G806 45% (18%), G140 42% (17%), G575 42% (18%) |

The last three openers are borderline: they start under half their texts.

### D.2 The skeleton transfers to every site

Each cell shows the share of texts in order, with the number of texts scored. "Shuffled" is the within-text shuffle (200 runs), shown as mean / 95th percentile. "Chance-corrected" is (observed − shuffled) / (1 − shuffled): 0 means chance, 1 means every text in order.

| Site | Roles from Mohenjo-daro | Shuffled | Chance-corrected | Roles from Harappa | Roles from all other sites |
|---|---|---|---|---|---|
| Mohenjo-daro | 75.9% of 328\* | 20.4% / 23.8% | 0.70 | 74.9% of 546 | 73.4% of 586 |
| Harappa | 78.8% of 330 | 25.3% / 28.8% | 0.72 | 78.1% of 151\* | 79.8% of 341 |
| Dholavira | 70.3% of 37 | 26.1% / 37.8% | 0.60 | 74.2% of 31 | 71.1% of 38 |
| Lothal | 72.7% of 33 | 20.1% / 33.3% | 0.66 | 79.3% of 29 | 80.6% of 36 |
| Kalibangan | 82.6% of 23 | 26.1% / 43.5% | 0.76 | 85.0% of 20 | 82.6% of 23 |
| Chanhu-daro | 68.2% of 22 | 21.7% / 36.4% | 0.59 | 72.2% of 18 | 71.4% of 21 |
| other sites | 80.0% of 55 | 28.7% / 36.5% | 0.72 | 68.8% of 48 | 79.7% of 59 |
| **Pooled, excluding the source site** | **77.6% of 500** | 25.3% | | **74.9% of 692** | **76.0% of 1,104** |

\* Own site, scored by split-half: roles learned on half the site's texts and scored on the other half.

At every site and in every direction, the observed rate is far above the 95th percentile of the shuffle. Chance-corrected agreement is 0.59–0.78 everywhere. The small sites (18–38 scored texts) have wider uncertainty, but even their lowest value (68%) is well above their shuffle ceilings (33–45%).

### D.3 The result is robust

**Changing the thresholds** (roles from Mohenjo-daro; pooled over all other sites):

| Setting | Openers | Closers | Texts in order | Shuffled |
|---|---|---|---|---|
| Baseline rule | 9 | 8 | 77.6% of 500 | 25.1% |
| Minimum 10 uses | 9 | 12 | 77.6% of 527 | 24.5% |
| Minimum 25 uses | 6 | 6 | 79.8% of 456 | 27.4% |
| Opener share 30% | 10 | 8 | 76.0% of 508 | 25.3% |
| Opener share 50% | 5 | 8 | 82.1% of 487 | 25.9% |
| Closer share 40% or 60% | 9 | 8 | 77.6% of 500 | about 25% |
| Ratio 1.5 | 9 | 8 | 77.6% of 500 | 25.2% |
| Ratio 2.5 | 6 | 8 | 79.5% of 492 | 25.5% |
| All strict (25 uses, 50%, 60%, ratio 2.5) | 4 | 6 | 83.9% of 447 | 28.2% |

The rate stays between 76% and 84% against a shuffle of 25–28% whatever the setting. Stricter rules raise it slightly, because they drop the borderline openers.

**Duplicates kept:** 1,988 texts instead of 1,523. The pooled rate becomes 81.2% of 734, against 26.8% shuffled, and every site moves by a few points at most. Removing duplicates does not create or remove the result.

### D.4 How strong this is, honestly

- **What is shown:** the opener → content → closer order is a shared convention across the Indus sites in this corpus. The signs that open and close at Mohenjo-daro open and close at Harappa, Dholavira, Lothal, Kalibangan and Chanhu-daro too, at similar rates, about 70–85% of scorable texts against about 20–30% by chance. It holds whichever site the roles are learned from and whatever reasonable thresholds are used.
- **Partly built in:** openers are chosen for starting texts and closers for ending them. So part of the "order" is that these signs keep their positions at other sites. The within-text shuffle accounts for chance placement, but not for that design choice. The fair reading is: **the same signs hold the same positions everywhere, and the middle material sits between them.**
- **Not shown:**
  - what any slot means;
  - whether the system records a language;
  - whether the sites differ in date. Sites are not dated here, so "everywhere" could partly mean "at one period".
  - It also depends on one website transcription of the corpus. Repeating it on ICIT matters.

### D.5 The candidate for a future pre-registered test (described, not registered)

- **Hypothesis:** roles learned from Mohenjo-daro's exploration texts with the D.1 rule put holdout texts from all other sites in order more often than within-text shuffling predicts.
- **Frozen in advance:**
  - the rule and the exact role lists in D.1;
  - the data settings (damaged and unidentified texts removed, duplicates removed);
  - the pooled conformance statistic and the minimum of two ranks per text;
  - a one-sided permutation test with 2,000 within-text shuffles;
  - the minimum support of 5 texts.
- **Secondary checks, set in advance:**
  - the same test with roles learned from Harappa;
  - per-site rates, reported without a separate significance test.
- **Expected power:** the holdout should hold roughly 100–140 scorable texts from sites other than Mohenjo-daro (about a quarter of the 500 here). With a gap of about 50 points between observed and shuffled rates in exploration, power is very high.
- **Prepared (14 October), not registered:** the `template_order` test kind is now in `indus_workbench/hypotheses.py`, with synthetic controls in `tests/test_core.py` (`TemplateOrderTests`). The frozen definition is `drafts/H-skeleton-transfer.DRAFT.json`. Run on the exploration split as a check, it reproduces 77.6% of 500 scored texts in order, against 25.3% shuffled.
