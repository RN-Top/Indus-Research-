# Water result, retested against real Bronze Age sites (EXPLORATORY)

*15 October 2026. Geography only: no inscriptions are read, and nothing is registered. Script: `scripts/findspot_gazetteer_test.py`. Numbers: `findspot_gazetteer_test.json`. Printout: `findspot_gazetteer_test_output.txt`. This follows up `findspots_waterways.md`.*

## Why

The first test compared the places abroad where Indus inscriptions were found with **random land**. They were about 8 times nearer to water (17 km against 133 km). That null is too easy, because people everywhere lived by water. The fair question is whether places **with** Indus finds sit nearer to water than **other places that existed at the same time** without them.

## Data

**Comparison sites (the gazetteer):**
- Source: the Pleiades gazetteer of ancient places (CC BY, from its GitHub data release).
- Selection: location points in the same region (15–42 °N, 42–75 °E, South Asia left out) whose dated range overlaps **2600–1900 BCE**.
- That gives 70 places. 7 lie within 15 km of an Indus find-spot (Saar, Shortugai, places at Ur, and the Akkad centre point near Kish), which leaves **63 places without Indus finds**.
- By zone: 46 in Mesopotamia and western Iran, 11 on the Iranian plateau and in Central Asia, 6 in the Gulf and Arabia.

**Indus find-spots:** the 13 places abroad with Indus inscriptions. Luristan is left out because it is a region, not a site.

**Distances** are to the present sea and to major rivers (Natural Earth), as before.

## Results

| Distance to | Indus find-spots (13) | Contemporary sites without (63) | Label shuffle p | Same, matched for distance from the Indus | p |
|---|---|---|---|---|---|
| **Sea or major river** | **13 km** | 34 km | **0.04** | 13 km against **81 km** | **0.004** |
| Sea only | 198 km | 324 km | 0.02 | 198 km against 178 km | 0.57 |

## What it means

- **The water link survives a fair comparison, at a smaller size.** Places with Indus finds sit closer to the sea or a major river than contemporary places without them. The gap is 13 km against 34 km overall, and 13 km against 81 km when compared with places at similar distances from the Indus. The random-land figure (8 times nearer) overstated it.
- **The link is mostly to rivers and coasts together, not to the sea alone.** Once distance from the Indus is matched, places with finds are no nearer the sea than places without. Most finds are in river cities (Ur, Umma, Kish, Susa) and on Bahrain's coast. Mesopotamian sites with no Indus finds are mostly on the same rivers.
- **For Erin's idea:** this fits "Indus goods travelled by water and ended up at waterside towns". It is not strong enough to rule out simpler explanations:
  - big, well-dug cities sit on rivers;
  - the gazetteer leans heavily to Mesopotamia;
  - only 13 find-spots.

## Limits

- **Pleiades is thin and lopsided here:** 63 places, three quarters of them in Mesopotamia and western Iran. Very few are in the Gulf or Central Asia.
- **Dates come from Pleiades' attestation ranges,** which can be broad.
- **Same caveats as before:** modern coastline and rivers (the Gulf head was further north then), approximate coordinates for half the find-spots, and excavation bias.
- **Exploratory.** It was decided after seeing the first result.

## What would strengthen it

A fuller site gazetteer for the Gulf and the Iranian plateau. Excavation reports or regional surveys would be needed; Pleiades is weak there.
