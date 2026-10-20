# Old Tamil against Prakrit: language-side measurements (EXPLORATION, nothing tested)

*19 October 2026. Script: `scripts/lang_label_features.py`. Plan: `drafts/dravidian_comparison_PLAN.md`.*

**Data:**
- Old Tamil: Mahadevan's corpus of 110 inscriptions (96 with 2+ words), plus 23 object legends of 2+ words.
- Prakrit: 167 EIAD inscriptions (156 with 2+ words).

**Indus is NOT compared here.** Only the two languages are measured, to see which features tell them apart at all.

| Feature | Old Tamil, caves | Old Tamil, objects | Prakrit | Tells them apart? |
|---|---|---|---|---|
| F1: first word is a name | **60%** | 48% | **14%** | **Yes** |
| F1: last word is a name | 32% | **87%** | 8% | Yes, but the Tamil "objects" sample is tiny and mostly bare names |
| F5: top-5 first words cover | **14%** | 30% | **42%** (*siddham* "success!" opens 50 texts) | **Yes:** Prakrit opens with a fixed formula, Tamil with names and places |
| F2: top-5 last words cover | 29% (*pali* "hermitage", *kal* "stone", *atittanam* "seat") | 43% | 35% (*ti*, numbers, *danam* "gift") | **No:** both end in a fairly fixed set |
| F3: suffix stacking | 0.18 per word | 0.25 | 0.62 | **Not usable:** two different agents segmented suffixes differently |
| F4: number before or after the noun | 4 / 4 | 0 / 0 | 154 / 174 | **Not usable:** almost no Tamil numerals; Prakrit uses both orders |

## What this shows

1. **Only one dimension separates the two: how a text opens.**
   - Prakrit inscriptions open with a fixed formula (*siddham*, *namo bhagavato*).
   - Old Tamil inscriptions open with a person or place.
2. **That difference is about inscription habit, not grammar.** *Siddham* is a Buddhist and Indic scribal custom. A Tamil Jaina cave record and a Buddhist Prakrit pillar differ in **religion and genre** as well as language.
   - So even a perfect Indus match on F1 or F5 would show "inscribes like X", not "speaks X".
3. **The features that come from grammar did not survive:**
   - suffix stacking (F3);
   - number order (F4).

   These are what Dravidian actually predicts. They could not be measured comparably with this data.

## Next, before any Indus comparison

- **Re-segment the suffixes** of both corpora with **one** rule set (one agent, or code), so that F3 becomes comparable.
- **Add Mesopotamian seal legends** as a third reference. They are already in the project.
- **Write the predictions** for Indus under each language for F1 and F5 only, and commit them.
- **Then compare,** on the exploration split.
- **Any confirmatory claim** would go to the locked holdout.

**Caveat on blinding.** The Indus values of these features are already partly known to the analyst from earlier work: openers start about 30% of texts, and rare signs start heading-less texts. Any comparison is therefore exploratory unless run on the holdout.
