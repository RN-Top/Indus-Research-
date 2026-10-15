# Do closer signs mark categories? (EXPLORATORY)

*15 October 2026. Exploration split only (1,523 distinct texts). The Indus holdout was not read, and nothing was registered. Script: `scripts/closer_categories.py`. Numbers: `closer_category_test.json`. Full printout: `closer_category_test_output.txt`.*

## Question

The working "function" reading is that inscriptions are labels, made of a fixed heading, an individual name and a category mark. If the closing sign is the category mark, then texts that end in the same closer should cluster by:

- what the object is (seal, tablet and so on);
- where it was found;
- which animal the seal shows.

They should cluster more than chance would produce.

## What was available

All fields were checked before testing.

| Field | Coverage in exploration | Used as |
|---|---|---|
| Object type | all 1,523 texts | 7 groups: seal 1,057, tablet 359, pottery 45, tag 28, rod 11, "other" 11, plus impressions and bangles merged (12; types with fewer than 10 texts) |
| Site | all 1,523 (10 "Unknown") | 8 sites with at least 10 texts; the rest merged into "other sites" |
| Seal animal (`motif_group`) | 847 of 1,057 seals | **79% unicorn**; the others are spread thinly over gaur, zebu, elephant, rhinoceros and so on, with animals under 8 seals merged |
| Material | 1,297 texts | Not tested (not in the request; it largely duplicates object type) |

**The animal field is usable but weak.** It is recorded for seals only, and unicorns dominate. As a result, only 7 of the 12 closers have at least 15 animal seals ending in them. A closer would have to be used on a rare animal very often to show up.

## Method

- **Closers** come from the frozen role rule (functional_by_site.md D.1), learned from all exploration texts: G740, G400, G520, G90, G151, G405, G527, G407, G617, G154, G156 and G621.
- **Grouping:** a text belongs to a closer's group if that closer is its **final** sign.
- **Support:** a test needs at least 15 texts in the group. G621 has 14, so it was skipped.
- **Test:** the chi-square statistic of the "ends in this closer or not" × category table was compared with 5,000 shuffles of which texts end in the closer. This is a permutation p-value.
- **Effect sizes:**
  - Cramér's V.
  - Excess V: the part of V above what shuffles give. Small groups get some V by chance.
  - The single category most over-represented in the group (largest adjusted residual) and its lift.
- **Multiple testing:** Benjamini–Hochberg across all 29 closer × field tests.
- **Confound check:** sites and object types are tangled, since Harappa holds most tablets. Each test was therefore repeated with shuffles kept *inside* each site (for object type and animal), or inside each object type (for site). This check also has its own BH.

## Results

| Closer | Texts ending in it | Object type | Site | Seal animal |
|---|---|---|---|---|
| **G400** | 129 | **tablet 69% vs 24% overall (×2.9); V 0.33; q 0.002; holds within sites** | **Harappa 71% vs 33% (×2.2); V 0.25; q 0.002; holds within object types** | n.s. (only 28 animal seals) |
| **G740** | 527 | **seal 78% vs 69% (×1.1); V 0.15; q 0.002; holds within sites** | Mohenjo-daro 58% vs 51%; q 0.08; gone within object types | n.s. (unicorn 82% vs 79%) |
| G520 | 107 | seal 87% vs 69%; q 0.08 | n.s. | zebu 9% vs 3%; q 0.13 |
| G527 | 31 | n.s. | Lothal 16% vs 3% (×5.6, 5 texts); q 0.06 | n.s. |
| G90, G151, G405, G407, G617, G154, G156 | 19–50 each | n.s. | n.s. | n.s. or too few |

*n.s. means q > 0.1. Exact values for every test are in the JSON and output files.*

### What this says

1. **One closer is a strong category marker: G400.** Texts ending in G400 are mostly **tablets** and mostly from **Harappa**. Both associations survive the confound check:
   - within each site, G400 texts are still mostly tablets;
   - within each object type, they still lean towards Harappa.

   This fits Wells and Fuls, who treat G400 as a *post-terminal* sign added after the main closer, not as a closer of the same kind as G740.
2. **The commonest closer, G740 (the "jar"), is a generic ending.** It appears on a third of all texts. It leans slightly towards seals (78% against 69%), which is statistically clear but small (V 0.15). It does not pick out a site or an animal.
3. **The other ten closers show no reliable category.** Some leads are weak and do not survive correction:
   - G520 leans towards seals and zebu seals;
   - G527 leans towards Lothal (5 texts).

   These could be followed up, but they rest on a handful of texts.
4. **Animal: no closer tracks the seal animal.** This is partly a power problem. With 79% unicorns and small groups, only a big effect would show.
   - An earlier analysis (functional_meaning.md) suggested G151 goes with unicorn seals.
   - This test does not support that: 28 of the 34 animal seals ending in G151 are unicorns (82%), against 79% for all seals.

## How this changes the "label" reading

- **The strong form is not supported:** "each closer names a category". Most closers do not sort texts by object, site or animal. Either they mark something these three fields do not record, such as an office, a commodity or a person's role, or they are not category marks.
- **The weak form is supported by one sign:** G400 does behave like a mark tied to a kind of object (tablets) and to one site (Harappa).
- The earlier joint result (closers track object, site and animal together, p = 0.002) is mostly G400 and, to a lesser degree, G740.

## Limits

- **Exploratory only.** Thirty-odd tests on data already looked at, including G400, whose tablet link was noticed before. Any claim from here needs a pre-registered holdout test.
- **Coverage:** the only fields are object type, site and animal, and material was not tested. There is no date, find context or owner. A closer could mark a category that is simply not in the metadata.
- **Grouping uses the final sign only.** Texts ending in G740 + G400 count under G400. A version using "contains this closer" could differ.
- **Same transcription:** these are ICIT-derived data (see METHODS.md, provenance).
