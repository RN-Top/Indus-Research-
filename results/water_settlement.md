# Follow the water: did people resettle on living water when the river failed?

*Exploratory. 14 October 2026. Geography, not the sign corpus, so it has nothing to do with the locked text holdout. Erin's hypothesis: because Indus life revolved around water, when the Ghaggar-Hakra system dried, people resettled on living water rather than at random.*

## Bottom line

- **The eastward shift is well supported by published counts.** After about 1900 BCE, sites fell sharply on the dried river and grew in number to the east, toward the Yamuna and Ganges, and in Gujarat.
- **One observation fits "they followed the water" directly.** In Cholistan, the surviving Late sites clustered where a channel from the Sutlej still brought water.
- **A proper statistical test of "nearer to water than chance" could not be run here.** No dated list of site locations was available, and the river map that was available leaves out the small rivers that matter. Section 4 sets out what the test needs and how to register it.
- **There is one published counterpoint.** Khan and Lemmen (2014) describe late settlements moving *away* from rivers.

## 1. The eastward shift (sourced counts)

| Region | Mature Harappan | Late Harappan | Source |
|---|---|---|---|
| Cholistan, on the dried Hakra | (not found in an accessible source) | **50 sites** | Mughal 1990, p. 1 |
| Haryana | | **297** | Mughal 1990, p. 2 |
| Eastern Punjab | | **132** | Mughal 1990, p. 2 |
| Uttar Pradesh (Ganga-Yamuna Doab) | | **130** | Mughal 1990, p. 2 |
| Himachal Pradesh and Delhi | | 4 | Mughal 1990, p. 2 |
| Kutch and Saurashtra (Gujarat) | **20** | **152** (initial Late phase; 231 in all) | Mughal 1990, p. 6 |

What other studies say:

- **Giosan et al. 2012 (*PNAS*):** "a significant shift in site numbers and density towards the east is recorded." Late Harappan site numbers rise in upper Punjab, Haryana and Uttar Pradesh, while "in lower Punjab and Sindh … the number of sites decreased." Villages proliferate along the Yamuna and the Yamuna-Ganga interfluve. They give no counts.
- **Khan and Lemmen 2014:** "At the end of the Mature phase, only along the Ghaggar-Hakra river sites disappear whereas new sites emerge in the upper Ganges reaches." By about 1500 BCE, Gujarat and Ganges sites remain while most Punjab and Baluchistan sites have gone.

**What can be quantified.**

- In the Late phase, the three eastern regions hold 559 sites, about 11 times the 50 left in Cholistan on the dried river.
- Gujarat rises from 20 sites to 152, a 7.6-fold increase.

**What cannot be quantified yet.** A clean east-versus-west change ratio needs Mature-phase counts for Haryana, Punjab and Uttar Pradesh from the same survey tradition, and they were not found in an accessible source. Survey effort also differs a great deal between India and Pakistan, and between regions, which inflates or deflates counts independently of where people actually lived (a caution Giosan et al. also give).

## 2. Did they go *to water*?

- **For:**
  - **Cholistan.** Mughal (1990, p. 1) reports that the Late Harappan (Cemetery H-related) sites lie north and north-east of Derawar Fort, in an area "fed by a channel from the Sutlej River." As the Hakra failed, the remaining settlement concentrated where water still arrived.
  - **Mughal on the cause.** He links relocations in Cholistan to "a reduction in the water supply through a channel from the Sutlej River" around 2100 BCE (p. 13).
  - **Riverbank positions.** Late sites in the east sit on rivers. Hulas is on the higher banks of Yamuna tributaries (Hindon, Krishni and others), Mitathal near a channel between the Chautang and the Yamuna, and Rojdi on the Bhadar (Wikipedia pages for each site).
  - **Giosan et al. 2012** find settlements on the Punjab interfluves "near their edges, close to the fertile, annually flooded areas."
- **Against, or complicating:**
  - **Khan and Lemmen 2014** write that "the movement of settlements away from the rivers could also have deprived the kilns of firing wood": a description of late settlement moving *away* from rivers.
  - **The east is wetter overall.** The east gets more monsoon rain, so moving east may be about rain-fed farming as much as rivers. Giosan et al. tie the eastward move to weakening monsoon floods in the west, which suits small-scale farming that relies on rain and minor floods.
  - **Petrie et al. 2017** (as cited by Qurat ul Ain) argue the Ghaggar was monsoon-fed rather than perennial. If so, the "dried river" was never a great perennial river, and the story is about rainfall as much as rivers.

**Verdict: suggestive, not shown.** The Cholistan clustering on the Sutlej channel is the clearest support. Mughal reports it, but it was not measured against chance.

## 3. Why the spatial test was not run

1. **No dated site coordinates.**
   - The comprehensive lists are not openly downloadable: Possehl's gazetteer (about 3,000 sites), Randall Law's *Indus Google Earth Gazetteer*, and Green and Petrie's 2018 dataset for north-west India. The Law-based file used by Khan and Lemmen (`site_chronology.csv`) is referenced in their code but not published.
   - Fetching coordinates page by page from Wikipedia gave only a handful of Late-phase sites, too few for a test and biased toward famous excavations.
2. **The available river map is the wrong one.** Natural Earth (1:10 million) includes the Indus, Sutlej, Beas, Ravi, Chenab, Yamuna and Ganges. It omits the Ghaggar, Chautang, Hindon, Bhadar, Sabarmati and Luni, which are exactly the rivers Late sites sit on.
3. **Rivers have moved.** Modern courses are not ancient ones: the Sutlej, Yamuna and Indus have all shifted. "Distance to water" needs palaeochannel maps, such as those in Giosan et al. 2012 or Orengo and Petrie 2017.
4. **"Near water" must be defined in advance.** In the Punjab plains, most random points lie within a few tens of kilometres of some river. The null has to be built inside the settled landscape, not over the whole map, or "near water" means nothing.
5. **Dating is coarse.** Many sites are dated by pottery style, not radiocarbon. Some Late sites continue from Mature ones, so "resettled" and "stayed" are mixed.

## 4. A falsifiable version, to register before the data is seen

**W1 (water).** Within each region, sites first occupied in the Late phase lie closer to a perennial river or palaeochannel than Mature-phase sites in the same region did. The test asks whether relocation favoured water, not whether all settlement is near water.
- **Statistic:** median distance to the nearest mapped channel, Late minus Mature, computed within each region and then pooled.
- **Null:** permute the Mature and Late labels among sites within each region, which keeps survey coverage and landscape fixed.
- **Second null:** random points drawn within 25 km of known sites of either phase.
- **Pre-registered threshold:** "on water" means within 5 km of a mapped channel.
- **Sensitivity check:** repeat at 2 and 10 km.

**W2 (eastward shift).** The centre of settlement (mean longitude, weighted per site) moves east from Mature to Late phase by more than permuting phase labels predicts.
- **Robustness:** repeat with Indian and Pakistani sites analysed separately, so differences in national survey effort can't produce the shift.

**Data needed for either test:**
- one of the dated site lists: Possehl's, Law's, or Green and Petrie's (by request to the authors);
- a palaeochannel map.

Both tests would be fingerprinted and committed before the analysis, like the text hypotheses, but kept in a separate family for multiple-testing correction.

## Sources

- Mughal, M. R. (1990). "The Decline of the Indus Civilization and the Late Harappan Period in the Indus Valley." *Lahore Museum Bulletin* III(2): 1–17. [PDF](https://rafiquemughal.com/wp-content/uploads/2022/01/MUGHAL_1990_Decline-of-the-Indus_Lahore-Mus-Bulletin.pdf). Page numbers were read from running headers and may be off by one.
- Giosan, L. et al. (2012). "Fluvial landscapes of the Harappan civilization." *PNAS* 109(26). [Article](https://www.pnas.org/doi/10.1073/pnas.1112743109)
- Khan, A. and Lemmen, C. (2014). "Bricks and urbanism in the Indus Civilization." [arXiv:1303.1426](https://arxiv.org/pdf/1303.1426)
- Qurat ul Ain, *The Hakra Cultural Horizon in the Greater Indus Valley* (PhD thesis, Ca' Foscari), citing Petrie et al. 2017. [PDF](https://iris.unive.it/retrieve/b13823e4-7893-47b2-8cdf-c26a8f94402b/956395-1229871.pdf)
- Green, A. S. and Petrie, C. A. (2018). "Landscapes of Urbanization and De-Urbanization." *Journal of Field Archaeology*. [Article](https://www.tandfonline.com/doi/full/10.1080/00934690.2018.1464332). Identified but not accessible from here.
- Site pages: [Mitathal](https://en.wikipedia.org/wiki/Mitathal), [Hulas](https://en.wikipedia.org/wiki/Hulas), [Sinauli](https://en.wikipedia.org/wiki/Sinauli), [Rojdi](https://en.wikipedia.org/wiki/Rojdi), [Rangpur](https://en.wikipedia.org/wiki/Rangpur,_Gujarat), [Pirak](https://en.wikipedia.org/wiki/Pirak)
- River data checked: Natural Earth 1:10m rivers and lake centrelines (public domain), via the `nvkelso/natural-earth-vector` GitHub repository.
