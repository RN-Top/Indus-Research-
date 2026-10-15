# Which parts of the inscriptions travel? Signs shared across sites and waterways (EXPLORATORY)

*15 October 2026. Exploration split only. The Indus holdout was not read, and nothing was registered. Script: `scripts/sign_travel.py`. Numbers: `sign_travel_water.json`. Printout: `sign_travel_water_output.txt`.*

## The idea (Erin's)

If seals were used in trade or contact that moved by water, a seal had to be readable by a stranger "on another boat", not just by people from its own town. Two predictions follow:

- the parts a stranger needs (perhaps the fixed opening signs) should be **shared across sites**;
- purely local parts should stay **at one site**.

Sites on the same waterway should also share more of their signs than sites that are not connected by water.

## What was available

**Sites.** Only six sites have at least 15 exploration texts:

| Site | Texts | Water setting | Waterway group |
|---|---|---|---|
| Mohenjo-daro | 777 | on the Indus | Indus system |
| Harappa | 499 | on the Ravi, a tributary of the Indus | Indus system |
| Chanhu-daro | 31 | Indus floodplain; the river later moved away (about 19 km now) | Indus system |
| Kalibangan | 32 | on the Ghaggar, a seasonal river that later dried | Ghaggar-Hakra |
| Lothal | 44 | estuary on the Gulf of Khambhat, with a dock | Gujarat coast |
| Dholavira | 51 | island in the Rann of Kutch | Gujarat coast |

**Notes on the site data:**

- Coordinates come from `data/site_coordinates.csv` (Wikipedia). Chanhu-daro has no published coordinates on Wikipedia. It is placed from "about 130 km south of Mohenjo-daro", which is approximate.
- "Same waterway" is a coarse proxy. It gives only **4 water-linked pairs out of 15**: Mohenjo-daro–Harappa, Mohenjo-daro–Chanhu-daro, Harappa–Chanhu-daro and Lothal–Dholavira.
- Arguably every site except Kalibangan was reachable by water, since the Indus mouth opens onto the same sea as Gujarat. Where the Ghaggar-Hakra drained is debated.
- There is no data on actual routes, dates or how navigable each river was.

**Seals found abroad.** There are also 14 exploration texts found outside the Indus region:

- 10 from the Gulf and Mesopotamia, reached by sea: Ur, Susa, Tell Umma, Bahrain, Oman.
- 4 from Iran and Central Asia, overland: Luristan, Altyn Depe, Gonur Depe, Shortughai.

These are the clearest case of inscriptions that really did travel.

## Method

- **A. How local is each sign?** For each of the 79 signs used at least 15 times at the six sites:
  - Compare its spread over sites with the spread of all signs over sites (Jensen–Shannon divergence).
  - Subtract the divergence expected for a sign used equally often but placed at random. Otherwise rare signs look "local" just because they are rare.
  - Result: **0 means the sign spreads like the corpus as a whole; higher means it is concentrated at one site.**
- **B. Are openers more shared than closers or middle signs?** Roles come from the frozen rule, on all exploration texts. Role labels were shuffled among signs, within four frequency bins, 5,000 times.
- **C. Do water-linked sites share more?**
  - Each site was cut down to 31 random texts (the size of the smallest site), 500 times. Overlap (Jaccard) was measured on three things: sign sets, sets of opening units and sets of closing units.
  - The test permutes the six site labels over all 720 orders. It was run both on raw overlap and after removing a distance trend.
- **D. Seals found abroad:** described only.
- **Multiple testing:** Benjamini–Hochberg across all 9 tests in B and C.

## Results

### A. Signs that travel and signs that stay home

**Most shared**: spread over sites like the corpus itself, and found at all or nearly all six sites:

| Sign | Role | Uses | Sites |
|---|---|---|---|
| G817 | opener | 86 | 6 of 6 |
| G861 | opener | 116 | 6 of 6 |
| G231 | middle | 42 | 6 of 6 |
| G176 | middle | 75 | 6 of 6 |
| G240 | middle | 149 | 6 of 6 |
| G220 ("fish") | middle | 171 | 6 of 6 |
| G233 | middle | 99 | 6 of 6 |
| G741 | middle | 104 | 6 of 6 |
| G100 | middle | 63 | 5 of 6 |
| G760 | middle | 55 | 5 of 6 |
| G798 | middle | 60 | 5 of 6 |
| G90 | closer | 66 | 5 of 6 |

**Most local:**

| Sign | Role | Concentration |
|---|---|---|
| **G700** | middle | Harappa holds 79% of its uses (2.6 times its share of signs) |
| **G400** | closer | Harappa holds 70% (2.3 times) |
| G923 | middle | Mohenjo-daro holds 90% |
| G527 | closer | Lothal holds 18%, 5.7 times its share |
| G460 | middle | Dholavira 4.3 times its share |
| G154 | closer | leans to Lothal |
| G31 | long numeral | leans to Chanhu-daro |

### B. Openers against closers

| Role | Signs | Mean locality | Found at all 6 sites |
|---|---|---|---|
| Opener | 7 | +0.002 | 43% |
| Middle | 49 | +0.006 | 22% |
| Numeral | 11 | +0.005 | 36% |
| Closer | 12 | +0.024 | 8% |

**The direction matches the idea.** Openers are the most shared slot, and closers are the most local, with a large effect (d = −0.81). **But it is not statistically reliable:**

- openers against closers: p = 0.14;
- after correction: q = 0.91.

There are only 7 opener signs and 12 closers. Much of the closers' locality comes from G400 (Harappa) and G527 (Lothal).

### C. Water-linked site pairs

**No sign that sites on the same waterway share more.**

| Measure | Same waterway | Different waterway | p |
|---|---|---|---|
| Sign overlap | 0.29 | 0.30 | 0.80 |
| Opening units | 0.47 | 0.54 | 0.92 |
| Closing units | 0.28 | 0.27 | 0.40 |

Removing distance changes nothing; every q is 0.91 or higher. Overlap does not even fall with distance (correlation with log distance: +0.26 for signs, −0.06 for closings). At this level of detail, the script looks equally shared everywhere.

### D. Inscriptions that really travelled by sea

The 14 texts found abroad do **not** look like home-site texts:

| | Abroad (14) | Six home sites |
|---|---|---|
| Has a closer | **4 (29%)** | 76% |
| Ends in a closer | 3 (21%) | 67% |
| Has an opener | 1 (7%) | 30% |

**Abroad texts mostly lack the closing sign.** If they followed home-site rates, 4 or fewer closers out of 14 would happen about 0.02% of the time (binomial). **This was noticed after looking, not predicted**, so it is a lead, not a finding.

Possible explanations:

- It fits the long-standing observation that Gulf-type seals use unusual sign combinations (Parpola; Rao et al. 2009).
- Several of the texts are on tags, pottery or a tablet rather than seals.
- Some may have been made abroad for local users.

## What it means for the "readable from another boat" idea

- **Weakly consistent.**
  - The opening signs that can be tested are among the most widely shared (G817 and G861 at all six sites).
  - The local oddities sit in the closer slot (G400 at Harappa, G527 at Lothal) and in a few middle signs (G700 at Harappa).
  - That fits "the heading is universal, some endings are local", but the difference is not significant.
- **Not supported:** that water links made sites share more. Every site shares about as much with every other site, whatever the waterway or distance. That points to one script used in the same way across the whole region, not to sharing that follows routes.
- **The most interesting lead is D.** The inscriptions that actually crossed the sea drop the closing sign. If closers mark something like an affiliation or office at home, such as a guild or town, a seal for foreign trade might leave it out. That is a hypothesis to test properly, not a conclusion.

## Limits

- **Exploratory.** Several measures were tried on data already examined.
- **Low power.** Six sites, 15 pairs and only 4 water-linked pairs mean that only a large water effect could show. Two sites (Mohenjo-daro and Harappa) hold 89% of the texts. Small sites were cut down to 31 texts, which leaves their inventories noisy.
- **"Same waterway" is a crude proxy.** It is not a model of real routes. Sites were probably not all in use at the same time, and the corpus has no dates.
- **Shared signs need not mean trade.** They could equally reflect one shared language, administration or scribal training.
- **Abroad texts:** only 14, of mixed object types, and the comparison was chosen after seeing them.
- **Same transcription.** The data are ICIT-derived; see METHODS.md, provenance.

## Next step if pursued

The "abroad texts drop the closer" lead could be tested properly:

- **Data:** the full list of Indus-type inscriptions from the Gulf, Mesopotamia and Central Asia, from published catalogues rather than this corpus's 14.
- **Comparison:** against home seals matched by object type.
- **Protocol:** pre-registered first, using the holdout's abroad texts as the test set if there are enough of them. That is only with Erin's go-ahead.

## Sources

- Site settings: Wikipedia pages for each site, as listed in `data/site_coordinates.csv`; Chanhu-daro (location relative to Mohenjo-daro and the Indus).
- Rao, R. P. N. et al. (2009). "A Markov model of the Indus script." *PNAS* 106(33), on West Asian texts being ordered differently.
