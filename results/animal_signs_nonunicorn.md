# Does any sign track the seal animal once unicorns are set aside? (EXPLORATORY)

*15 October 2026. Exploration split only. The Indus holdout was not read, and nothing was registered. Script: `scripts/animal_signs.py`. Numbers: `animal_signs_nonunicorn.json`. Printout: `animal_signs_nonunicorn_output.txt`.*

## Why

The closer test (`closer_category_test.md`) found no closing sign that marks the seal animal. That test was swamped by unicorns, which are 79% of seals with an animal. Here the unicorns are removed so the rarer animals get a fair test.

## The data: small

There are 1,057 exploration seals:

| Group | Seals |
|---|---|
| Unicorn | 665 |
| No animal recorded | 210 |
| **Other animals** | **182** |

The 182 seals with other animals:

| Animal | Seals |
|---|---|
| Gaur (wild ox) | 56 |
| Zebu (humped bull) | 26 |
| Elephant | 23 |
| Rhinoceros | 19 |
| Tiger | 10 |
| Goat or markhor | 8 |
| Water buffalo | 8 |
| 15 rarer types (composite animals, scenes and others) | 32, merged into "other animal" |

**Sites:** most of these seals come from Mohenjo-daro. For example, 37 of the 56 gaur seals and all 9 tiger seals whose site is Mohenjo-daro or Harappa come from Mohenjo-daro.

**Power:** with groups of 10–56 seals, only a strong link would reach significance after correction. For instance, a sign on about a third of one animal's seals and almost none of the others'.

## Method

- **Signs tested:** 27 signs present on at least 8 of the 182 seals.
- **Roles:** opener, closer and numeral, from the frozen rule (functional_by_site.md D.1), learned on all exploration texts.
- **Part 1.** For each sign, is its presence tied to the animal? Five slot tests were run the same way:
  - has an opener;
  - has a closer;
  - has a numeral;
  - which closer ends the text;
  - which opener starts it.

  The statistic is chi-square, compared with 5,000 shuffles of the animal labels. Effect sizes are Cramér's V and excess V (above what shuffles give). There are 32 tests, with BH correction.
- **Part 2.** For each animal with at least 10 seals, and each sign, is the sign more common on that animal's seals than on the other non-unicorn seals? This uses a one-sided Fisher exact test and reports lift. There are 135 tests, with BH correction.
- **Part 3.** For the strongest candidates:
  - how often the sign appears on unicorn seals;
  - whether the link survives when animal labels are shuffled only *within* each site, to rule out a site effect posing as an animal effect.

## Results

**No sign or slot survives correction.** The lowest q-value in part 1 is 0.35; in part 2 it is 0.33.

### Strongest leads, not significant

| Sign | Animal | On that animal | On other non-unicorn seals | On unicorn seals | Survives within-site shuffle? | q |
|---|---|---|---|---|---|---|
| **G820** (an opener) | rhinoceros | **6 of 19 (32%)** | 10 of 163 (6%), lift ×5.1 | 9% | **yes, p = 0.013** | 0.33 |
| G90 (a closer) | tiger | 3 of 10 (30%) | 11 of 172 (6%), lift ×4.7 | 5% | borderline, p = 0.06 | 0.92 |
| G240 | tiger | 3 of 10 (30%) | 13 of 172 (8%) | 12% | no, p = 0.10 | 0.92 |
| G1 (one stroke) | gaur | 9 of 56 (16%) | 6 of 126 (5%) | 6% | no, p = 0.29 | 0.64 |
| G233 | gaur | 9 of 56 (16%) | 6 of 126 (5%) | 7% | no, p = 0.32 | 0.64 |

**Slots:**
- "Which opener starts the text" was the strongest slot (V 0.25, p = 0.03, q = 0.50). This is largely the G820 and rhinoceros pattern again.
- Whether a seal has a closer, and which closer ends it, show no link to the animal (q ≥ 0.7).

## What this says

1. **The text mostly does not encode the animal,** even with unicorns removed. That fits the earlier reading: the picture and the writing carry different information.
2. **One lead is worth keeping: G820 on rhinoceros seals.**
   - G820 is one of the "initial signs" that Wells and Fuls describe, and one of our openers.
   - It starts about a third of rhinoceros seals, against 6–9% of other seals, unicorns included.
   - It holds up when shuffles stay within sites, so it is not just Mohenjo-daro against Harappa.
   - But it is 6 seals, it does not survive correction across 135 tests, and it was found by searching.
   - If real, it would mean the *opening heading*, not the closer, sometimes goes with the animal emblem.
3. **The closer is not an animal marker.** This confirms the closer test with a fairer sample.

## Limits

- **Exploratory, many tests, small groups.** The leads above are what one would expect to see by chance among 135 tries, unless a later test confirms them.
- **The animal labels are the source database's codes.** Some categories are mixed: "other animal" holds composite animals and scenes.
- **Most non-unicorn seals are from one site** (Mohenjo-daro), so other sites contribute little.
- Some signs appear on more seals simply because those inscriptions are longer. Presence tests do not correct for length.
- **Same transcription:** the data are ICIT-derived (METHODS.md, provenance).

## If pursued

A pre-registered test of "G820 opens rhinoceros seals more often than other seals" on the locked holdout is possible but weak.

- The holdout probably holds only about 5 rhinoceros seals, judging by its 20% share.
- With so few, even a real effect of this size would often be missed.
- It would be better to add seals from another transcription (CISI or ICIT) first, and only with Erin's go-ahead.
