# Function theory, second comparison: Mesopotamian seal legends (labels of known meaning)

*Exploratory. 15 October 2026. Script `scripts/mesopotamian_seals.py`; output in `mesopotamian_seals_output.txt` and `mesopotamian_seals.json`. Indus holdout untouched; nothing registered.*

## Data

- **Source:** seal legends from the CDLI bulk dump ([cdli-gh/data](https://github.com/cdli-gh/data), August 2022). These are inscriptions impressed on tablets (`@seal` sections) plus inscribed seal objects, from the Old Akkadian to the Old Babylonian period (about 2340–1600 BCE, overlapping the Mature Harappan).
- **Counts:** 24,937 impressions and 6,551 seal objects reduce to **10,667 distinct legends**.
- **Holdout:** a 20% holdout (hash of the legend text, salt `mes-seal-holdout-v1`; 2,097 legends) is set aside and was not read. Exploration covers **8,570**: Ur III 5,264, Old Babylonian 2,543, Early Old Babylonian 642, Old Akkadian 111, Lagash II 10.
- **Licence:** used under CDLI terms with citation; not copied into this repository.
- **Units:** one token = one transliterated word. Broken words and numbers are handled as for the Indus texts.

Their meaning is known. A typical legend reads "*kišib* (seal of) / [name] / [title, e.g. *dub-sar* scribe] / *dumu* (son of) [father] / *arad₂-zu* (your servant)", or "[name] / son of [father] / servant of [god]".

## What the unchanged Indus rule finds

The rule is `functional_by_site.md` D.1, unchanged.

| | Mesopotamian seal legends | Indus texts (`functional_meaning.md`) | Proto-Elamite accounts |
|---|---|---|---|
| Length | median 4 words | median 4 signs | median 8 tokens |
| Top openers | ***kišib*** "seal of" (95% start), king names (Šu-Suen, Ibbi-Suen, Šulgi, Amar-Suen), then common personal names | G861, G820, G817, G920 | M157 (89% start), which experts mark as the header |
| Different openers | 487 forms | **29 forms (4 cover 80%)** | 6 signs |
| Top closers | ***arad₂-zu*** "your servant" (99% end), patron gods (Amurru, Šara, Adad, Ninšubur …), titles | G740 (jar), G520, G400 | none |
| Middle that occurs only once | **83%** of legends | **86%** of texts | — |
| Ends in a number | **0%** | **3–5%** | **80%** |
| Slot order vs shuffled | 64.7% vs 26.3% (4,248 legends) | 76–78% vs about 25% | 87% vs 13% |

## What it suggests

1. **The blind rule recovers the meaning-bearing slots of a known label system.** Without being told anything, it picks *kišib* "seal of" as an opener, and "your servant" and patron gods as closers. These are the heading and the affiliation formula that scholars read in these legends. Together with Proto-Elamite (where it found the expert-marked headers), this is a second positive control: on scripts we can read, the rule's "openers" and "closers" are real functional slots.
2. **On the label signature, the Indus texts look like seal legends, not accounts:**
   - short (median 4 units);
   - a middle that is unique to almost every text (86% against 83%), like personal names and titles;
   - almost never ending in a number (3–5% against 0%; accounts: 80%).
3. **One clear difference: the Indus opener is far more fixed.** In the legends, the first slot is often the owner's own name, so it takes 487 forms. In the Indus texts, four signs do most of the opening. The Indus opener behaves less like a name and more like the fixed heading *kišib* "seal of", or a title. That fits the earlier finding that Indus openers do not track site, object or animal.
4. **Reading by analogy (a hypothesis, not a finding):** an Indus inscription may be shaped like "[fixed heading] + [individual name/title] + [affiliation or category mark]". Under that reading, the Indus closers (G740, G520, G400…) would play a role like *arad₂-zu* or a patron deity: an affiliation or category. This is consistent with the earlier result that closers track object type, site and seal animal.

## Limits

- **The unit is different:** a Mesopotamian *word* is not an Indus *sign*. The comparison assumes Indus signs act roughly like word signs.
- **Language is not tested.** The legends record Sumerian and Akkadian. Matching their *shape* does not show the Indus texts record a language, only that they do the same job in a similar layout (see Raghavendra 2026).
- **Sources are mixed:** impressions and seal objects, across about 700 years and several regions. Per-period results are not separated here.
- **Minor parsing artefacts:** a few ATF markup tokens (for example `$)`) survive cleaning, with 29 uses. They do not affect the main roles.
- **Holdouts unused:** the Mesopotamian and Proto-Elamite holdouts are kept for pre-registered tests.

**Candidate tests for later:**
- Indus openers have far fewer distinct forms than Mesopotamian seal openers, at matched sample size.
- The share of texts ending in a number orders the three systems: Proto-Elamite > Indus ≈ Mesopotamian seals.
