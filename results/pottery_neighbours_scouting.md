# Pottery graffiti: closest genres, and the earliest pot writing at Harappa (scouting)

*30 October 2026. Script `scripts/pottery_neighbours_scouting.py`, output `pottery_neighbours_scouting_output.txt`. Follows `pottery_vs_seals_scouting.md`.*

## 1. Which kind of object do graffiti resemble?

Measure: sign-frequency divergence (JSD), with groups size-matched to the 226 multi-sign graffiti, 1,000 draws. Lower means more alike.

| Group | JSD from graffiti |
|---|---|
| Tablet B | 0.305 |
| Seal | 0.311 |
| Tablet I | 0.343 |
| Tag or sealing | 0.353 |
| Stamped pottery | 0.484 |
| Copper tablet | 0.518 |
| Graffiti vs themselves (resampled) | 0.111 |

- Graffiti sit about **equally close to seals and small tablets**.
- They are **far from stamped pottery**. The small stamped group (39) inflates this somewhat, but stamped pots show their own repeated texts, e.g. G510 G697 and G540 G540.
- So **potters' stamps (made before firing) and owners' scratches (made after firing) used different vocabularies.**
- Signs over-represented on graffiti: the long-stroke numerals G31 and G33, G480, and G700.

## 2. Earliest pot writing at Harappa

Uses the corpus "period" field.

| Harappa period | Pottery inscriptions | Multi-sign | Numeral tokens | Sign types also on seals |
|---|---|---|---|---|
| 2 (Kot Diji, before the cities, c. 2800–2600 BC) | 16 | 6 | **41%** | 92% |
| 3 (urban) | 107 | 53 | 30% | 90% |

The six Period 2 multi-sign texts are G700 G700, G893 G31, G697 G31, G698 G34, G700 G31 and G900 G740.

Most of them are **a sign followed by a numeral**. One already ends in the jar sign G740, the commonest seal ending. The earliest multi-sign writing on Harappa pots looks like **item + count**, which is bookkeeping, not names. Kenoyer and Meadow have argued that writing at Harappa began in Period 2. The item + count pattern is a small-sample observation (n = 6) and is not tested.

**Status.** Descriptive. Prediction P15 already covers new graffiti. A "sign + numeral" prediction for new early (pre-urban) graffiti could be added once a source of such texts is known.
