# Where did Indus inscriptions end up, and does it follow the water? (EXPLORATORY)

*15 October 2026. Geography only: this uses **where** inscriptions were found (site names for every record, both splits), never their signs, so the locked text holdout is untouched. Nothing was registered. Script: `scripts/findspot_routes.py`. Numbers and coordinate tables: `findspots_waterways.json`. Printout: `findspots_waterways_output.txt`.*

## The idea (Erin's)

If Indus seals travelled with trade that moved by water, the places they turn up should line up along the ancient waterways: the rivers, the coast and the sea route to the Gulf. Straight-line distance from the Indus should explain less.

## Short answer

- **The sea finds sit on the water, and in the order of the documented sea route.**
  - Twelve of the 16 inscriptions found abroad are from the sea-and-Gulf side: Oman, Bahrain, Susa, and the cities of Sumer and Akkad.
  - Those find-spots fall along the coast-following route in the order of the Mesopotamian trade texts: Meluhha (the Indus) → Magan (Oman) → Dilmun (Bahrain) → Mesopotamia.
  - Going by the route adds only 1–30% to the straight-line distance.
- **Nearness to water:** find-spots abroad are much nearer to the sea or a major river than random land at the same distance from Mohenjo-daro.
  - median 17 km, against 133 km for random land; p = 0.0001;
  - for the sea group alone: 8 km against 135 km.
- **The overland finds do not track water.** These are Altyn Depe, Gonur Depe, Shortughai and the Luristan region. They follow the land routes into Central Asia, except Shortughai, which sits on the Oxus.
- **But this does not prove "water trade".** People everywhere lived by water, so *any* set of Bronze Age sites would beat random land points. The null used here (random land) is too easy. The pattern is consistent with water-borne trade but does not single it out (see Limits).

## 1. Find-spots

**Data:**
- Inscription counts are every record in the corpus, both splits, location only.
- Home sites with coordinates are listed; 24 small home sites without coordinates (57 inscriptions) are not used.
- Distances to sea and rivers use **modern** coastline and major rivers (Natural Earth).

**Outside the Indus region**

| Find-spot | Region | Inscriptions | km from Mohenjo-daro | km to sea now | km to major river now | Coordinates |
|---|---|---|---|---|---|---|
| Ra's al-Junayz | Oman coast | 1 | 999 | 1 | — | approx. (cape) |
| Salut | interior Oman | 1 | 1,195 | 109 | — | approx. (near Bahla) |
| Qala'at al-Bahrain | Bahrain | 1 | 1,752 | 1 | — | approx. |
| Saar | Bahrain | 1 | 1,755 | 4 | — | approx. |
| Karzakan | Bahrain | 2 | 1,757 | 2 | — | Wikipedia |
| Hajar | Bahrain | 1 | 1,751 | 1 | — | approx.; the match to Al Hajar village is assumed |
| Susa | Elam (SW Iran) | 1 | 1,990 | 198 | 113 (the Karun is not in the river layer) | approx. |
| Ur | Sumer | 2 | 2,174 | 200 | 13 (Euphrates) | approx. |
| Tell Umma | Sumer | 1 | 2,203 | 261 | 20 | Wikipedia |
| Kish | Akkad | 1 | 2,336 | 417 | 32 | approx. |
| Luristan | W Iran (a **region**, not a site) | 1 | 2,045 | 345 | 169 | very approx. |
| Shortughai | N Afghanistan | 1 | 1,119 | 1,334 | 9 (Oxus) | Wikipedia |
| Altyn Depe | Turkmenistan | 1 | 1,283 | 569 | 361 | Wikipedia |
| Gonur Depe | Turkmenistan | 1 | 1,337 | 694 | 155 (the Murghab is not in the river layer) | Wikipedia |

Note on the Gulf: in the third millennium the head of the Gulf probably lay much further north, roughly along Nasiriya–Amara–Ahwaz (Sanlaville 2005). That would put Ur and Umma near the sea, not 200 km from it. The size of this shift is debated.

**Home sites, for comparison:**
- Mohenjo-daro is 4 km from the Indus, Harappa 63 km from the modern Ravi/Chenab, and Lothal 22 km from the sea.
- Kalibangan, Banawali, Bhirrana and Rakhigarhi lie on the now-dry **Ghaggar-Hakra**, which the modern river layer does not have.

The literature adds more sea-route find-spots not in our corpus (Laursen 2010): **Failaka** (2), **Janabiyah** (Bahrain) and **Girsu** (Sumer). All fit the same chain.

## 2. Test: nearer to water than chance?

**Method:**
- Each find-spot abroad was paired with random land points at the same distance from Mohenjo-daro (within 100 km), outside South Asia.
- The statistic is the median distance to the sea or a major river, against 10,000 random sets.
- Each find-spot counts once.

| Group | Find-spots | Median km to sea or major river | Random land | p | Median km to sea | Random | p |
|---|---|---|---|---|---|---|---|
| All abroad | 14 | **17** | 133 | **0.0001** | 199 | 389 | 0.048 |
| All abroad, Luristan left out | 13 | 13 | 133 | 0.0001 | 198 | 401 | 0.052 |
| Sea and Gulf group | 10 | **8** | 135 | 0.0001 | 56 | 349 | 0.0004 |
| Overland group | 4 | 162 | 144 | 0.57 | 631 | 563 | 0.57 |

**Effect size:** find-spots abroad are about **8 times nearer** to water than random land at matching distance.

**Caveat on the group split:** the "sea" and "overland" groups were assigned from geography and regional history, so those two rows are descriptive. **The first two rows are the test.**

## 3. The sea finds in route order

**The route:** a coast-following path fixed by geography alone: Indus mouth → Ras al-Hadd (the eastern tip of Arabia) → Strait of Hormuz → central Gulf → estimated third-millennium head of the Gulf. The find-spots line up along it in this order:

| Find-spot | km along route | km off route | Route ÷ straight line |
|---|---|---|---|
| Ra's al-Junayz (Magan) | 793 | 12 | 1.01 |
| Salut (Magan, inland) | 973 | 177 | 1.11 |
| Bahrain, four find-spots (Dilmun) | about 1,880 | about 130 | 1.17 |
| Ur, Umma, Kish (Sumer and Akkad) | 2,537 | 19 to 235 | 1.14 to 1.15 |
| Susa (Elam) | 2,488 | 223 | 1.30 |

This is the order of Sargon of Akkad's inscription (about 2300 BCE): "the boats of Meluhha, the boats of Magan and the boats of Dilmun, at the quay of Agade, he tied up" (RIME 2.01.01.11).

**By sea, the Gulf is cheap to reach.** It costs 1–30% extra distance, and on water rather than across the Iranian plateau. That plateau lies *nearer* to the Indus in a straight line, yet has almost no Indus inscriptions: only the Luristan item and Susa, which is reached by river from the Gulf.

The overland finds follow a different, documented route into Central Asia:
- **Shortughai**, an Indus trading colony on the Oxus near the lapis lazuli mines (Wikipedia, after Francfort);
- **Gonur Depe** and **Altyn Depe**, in the Murghab delta and on the Kopet Dag foothills.

## What it means

- **Consistent with Erin's idea.**
  - Most inscriptions that left the Indus region went by sea, along the Magan–Dilmun–Mesopotamia chain known from cuneiform texts.
  - The places they ended up hug the coast and the great rivers.
  - The other, smaller stream went overland to Central Asia.
- **The circularity problem.**
  - The routes themselves are reconstructed partly from such finds, together with the texts.
  - So "the finds lie on the routes" is partly built in.
  - The non-circular part is: (a) the test in section 2 against random land, and (b) the order and low detour along a route fixed by geography.
- **Not about the script.** Finds tracking water tells us about **trade logistics**, not about what the inscriptions say. It does give a concrete setting for the earlier lead (`sign_travel_water.md`, D): if inscriptions abroad really do lack the closer, these are the seals that went by sea.

## Limits

- **Tiny sample:** 14 find-spots abroad, mostly one inscription each, plus one region (Luristan) given as a point.
- **Easy null:** random land includes deserts and mountains where nobody lived. A fair null would be **other Bronze Age sites** in the same regions, such as all excavated Akkadian, Dilmun, Magan and BMAC sites. That data was not available here. Against that null the water effect could shrink a great deal.
- **Excavation bias:** Mesopotamian cities and Bahrain's burial mounds were dug intensively. The Iranian plateau and Makran much less so. Where seals are found partly reflects where archaeologists dug.
- **Modern geography:**
  - The coastline and rivers are present-day.
  - The head of the Gulf was further north in the third millennium (by how much is debated).
  - The Indus has shifted course, and the Ghaggar-Hakra is now dry.
  - Lothal's dock is now inland.
  - The river layer lacks the Karun, Murghab, Kokcha and Ghaggar. This makes Susa, Gonur and the Ghaggar sites look farther from water than they were.
- **Coordinates:** about half the abroad points are approximate (flagged in the table and JSON). Errors of 10–20 km do not change the picture at this scale. Luristan could be hundreds of kilometres off.

## What would make it a real test

1. **A null of real sites:** a gazetteer of third-millennium sites in Mesopotamia, the Gulf, Iran and Central Asia (for example from the ArchAtlas or Pleiades databases). Then ask whether sites *with* Indus finds are nearer to the sea than sites without them.
2. **Ancient hydrology:** palaeochannel maps for the Indus and Ghaggar-Hakra (e.g. Giosan et al. 2012) and a mid-Holocene Gulf shoreline.
3. **More find-spots:** the abroad list from Laursen 2010 and CISI (see `foreign_seals_scoping.md`).

## Sources

- Sanlaville, P. (2005). On the Gulf shoreline in the Holocene. [PDF](https://ancientportsantiques.com/wp-content/uploads/Documents/PLACES/IndOc-Gulf/Gulf-Sanlaville2005.pdf), for the maximum transgression near the Sumerian cities and the debate around it.
- Sargon of Akkad, RIME 2.01.01.11. [CDLI P461937](https://cdli.earth/artifacts/461937), for the boats of Meluhha, Magan and Dilmun.
- Laursen, S. T. (2010). [The westward transmission of Indus Valley sealing technology](https://www.harappa.com/sites/default/files/pdf/The_westward_transmission_of_Indus_Valle.pdf).
- Wikipedia: [Shortugai](https://en.wikipedia.org/wiki/Shortugai), [Gonur Depe](https://en.wikipedia.org/wiki/Gonur_Depe), [Altyndepe](https://en.wikipedia.org/wiki/Altyndepe), [Umma](https://en.wikipedia.org/wiki/Umma), [Karzakan](https://en.wikipedia.org/wiki/Karzakan), [Al Hajar, Bahrain](https://en.wikipedia.org/wiki/Al_Hajar,_Bahrain).
- [Madain Project: Salut](https://madainproject.com/archaeological_site_of_salut).
- Natural Earth (public domain): coastline 1:10m; land, rivers and lake centrelines 1:50m.
