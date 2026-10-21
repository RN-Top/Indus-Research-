# Find-spots and time (scouting, exploration split only)

*20 October 2026. Script: `scripts/context_scouting.py`. Context fields (excavation area, Harappan period) come from the ICIT export inside github.com/yajnadevam/lipi (`src/assets/data/inscriptions.csv`; no licence, so not copied here; its reading/translation columns are not used). All 2,521 of our texts join by ICIT id, with matching site and sign order. Not a confirmatory test.*

## 1. Do texts cluster by neighbourhood?

Sign overlap (Jaccard) between texts from the same excavation area minus texts from different areas of the same city; areas shuffled within city.

| | Texts | Areas | Same-area excess | p |
|---|---|---|---|---|
| Harappa seals | 137 | 8 | −0.002 | 0.64 |
| Mohenjo-daro seals | 691 | 13 | −0.005 | 0.96 |
| Harappa tablets | 349 | 14 | +0.032 | 0.002 |
| Mohenjo-daro tablets | 126 | 9 | +0.025 | 0.03 |
| Harappa tablets, identical copies in an area counted once | 290 | | −0.003 | 0.82 |
| Mohenjo-daro tablets, same | 72 | | +0.004 | 0.31 |

**Reading.** Seal texts show no neighbourhood vocabulary at all: what is written on a seal does not depend on where in the city it was found. Tablets cluster only because identical copies were made and dropped together (batches); once each batch counts once, the clustering vanishes. No local "dialects" of the script inside a city.

## 2. Does the writing change over time? (Harappa, Periods 3B → 3C)

> **Correction (21 October 2026).** The table below counted ambiguous "Period 3B/C" labels as 3B (the regex took the first letter) and kept duplicate texts. With strict labels (3B, 3B-n vs 3C, 3C-n; "3B/C" excluded) and duplicates removed, only 25 texts are 3B and the effect is +0.85 signs, one-sided **p 0.07**. Too few 3B texts for a holdout test (expected about 6). Treat the trend as a weak lead, not a result.

| | n | Mean length | Starts with a heading sign |
|---|---|---|---|
| Seals 3B | 49 | 4.16 | 18% |
| Seals 3C | 91 | 5.11 | 25% |
| Tablets 3B | 236 | 3.45 | 8% |
| Tablets 3C | 107 | 4.07 | 14% |

Period labels shuffled within object type: length +0.98 signs in 3C (**p 0.0005**); heading share +0.10 (p 0.04). Texts **get longer and more formally headed** over time, on seals and tablets alike.

**Caveats.** Only Harappa has usable period labels; ambiguous labels ("3B/C", "3") excluded; damaged texts were already dropped, but preservation could still differ by layer; how the export assigned periods is unverified. A confirmatory version would need the holdout's Harappa texts (expected only ~100 with clean 3B/3C labels). Prior work (Kenoyer & Meadow on Harappa inscribed objects by period) not yet checked.
