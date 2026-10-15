# From function to meaning: what kind of thing fills each slot?

*Exploratory. 14 October 2026. Exploration split only: 1,523 distinct texts, or 1,988 with duplicates. Nothing registered; the holdout was not read. Script `scripts/functional_meaning.py`; output in `functional_meaning_output.txt` and `functional_meaning.json`. Roles come from the rule in `functional_by_site.md` D.1, applied to all exploration texts.*

The function analysis says where each part sits. This pass asks what *kind* of meaning each part carries, without reading any sign. Different kinds of meaning leave different statistical profiles:

- **Names or identifiers:** very many different fillers, most used only once, unique to their owner.
- **Titles, offices or categories:** a modest set of fillers, repeated, tracking context such as place, object or emblem.
- **Grammatical or formulaic markers:** very few fillers, used everywhere, tracking little or nothing.

## 1. The three slots have three different profiles

| Slot | Texts | Different fillers | Texts whose filler is unique | Tracks site | Tracks object type | Tracks seal animal |
|---|---|---|---|---|---|---|
| **Opener** | 444 | 29 (4 cover 80%) | 3% | no (p = 0.58) | no (p = 0.91) | no (p = 0.16) |
| **Content** | 1,518 | 1,389 | **86%** | weakly (p = 0.03, n = 111) | weakly (p = 0.03, n = 111) | no (p = 0.35) |
| **Closer** | 1,139 | 65 (G740 alone 48%) | 2% | **yes** (p = 0.002) | **yes** (p = 0.002) | **yes** (p = 0.002) |

"Tracks" means mutual information above shuffled labels (500 permutations). It is computed only on fillers seen at least 3 times, so one-off fillers cannot inflate it.

**Reading by profile:**

- **The opener behaves like a fixed formula.** G861, G820, G817 and G920 open most texts that have an opener, at every site and on every kind of object, whatever animal is on the seal. That is the profile of a standard heading, such as a fixed word or title prefix, not a name.
- **The content behaves like an identifier.** 86% of texts have a middle that occurs nowhere else. That is the profile of names, or of specific one-off content such as who, what or how much. It is the part that makes each seal individual.
- **The closer behaves like a category marker.** It comes from a small set, and which closer is used tracks the object type (G400 on tablets), the site, and the seal's animal. On seals with an animal, G151 closes 26 unicorn seals and only 6 seals with other animals. Caution: two earlier unicorn hypotheses failed on the holdout, so this needs the same treatment before anyone relies on it.

**One sentence:** an inscription looks like **[fixed heading] + [individual content] + [category ending]**, the shape of a seal legend or label: something like "Seal of | so-and-so, three of this | type of record".

## 2. Does it behave like language?

| Fingerprint | Result | What it suggests |
|---|---|---|
| Length | Mean 4.6 signs, median 4, longest 17; 1% over 10 signs | Short. No running text, just labels or names |
| More than one "clause" | 1.3% of texts restart (an opener after a closer), against 11.9% if shuffled | One unit per inscription; clauses are not chained |
| Suffix-like glue | The jar sign G740 follows 147 different signs | Behaves like a word ending or an end-of-label mark; both fit |
| Signs locked to a slot | 13 of 68 common signs are locked to the start or end; most of the rest sit in the middle | A mix: fixed slots plus a flexible middle |
| Unique or mass-produced | Seals: 9% belong to sets of identical inscriptions. Tablets: **59%** do | Seals are individual; tablets were made in identical sets, like tokens or tallies |

**Verdict: undecided, and honestly so.**

- **Arguing against full language:** inscriptions are short, single-unit and formulaic, with no long or chained texts. That fits a labelling or naming system.
- **Not ruled out:** names and titles written in a real language look exactly like this. Seal legends in known scripts are short formulas too.
- **The sign of language** would be grammar *inside* the content slot: the same small endings recurring after many different content signs. That is the next thing to look for.
- **This file uses no comparison corpus.** Settling the question needs the same measures run on known systems: real seal legends (for example, Mesopotamian cylinder-seal inscriptions) and a non-linguistic system (for example, heraldry or potters' marks).

## 3. Dating: cannot be done with this corpus

This corpus records no period, layer or excavation level for any inscription, and neither does its source database. Whether all sites used the system at the same time cannot be checked here. It needs:

- **ICIT**, which records find contexts for many objects, or excavation reports with periods. Harappa's recent excavations (HARP) assign finds to Periods 3A–3C.
- Then the skeleton test can be repeated **within each period**. If it holds within each period as well as across sites, the shared structure is not just one moment in time.

## What this suggests for future pre-registered tests

1. **Slot profiles:** openers do not track site; closers do. This is strong in exploration (p = 0.58 against 0.002).
2. **Tablets come in identical sets far more often than seals** (59% against 9%). This is very strong, but needs duplicate-handling written into the test.
3. **G151 closes unicorn seals.** This one is suggestive only, and unicorn links have failed on the holdout before.
