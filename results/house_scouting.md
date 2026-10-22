# Do seals from the same house share features? (scouting, exploration only)

*21 October 2026. Script: `scripts/house_scouting.py`. House = site + excavation area + block/house from the ICIT export. 478 exploration seals in 114 houses (111 at Mohenjo-daro, 3 at Harappa) across 10 areas; houses with 2+ seals, areas with 2+ such houses. Null: house labels permuted within each area (same house vs other houses of the same area). Not a confirmatory test.*

| Feature (pairs of seals) | Same house minus other houses | Shuffled | p |
|---|---|---|---|
| Sign overlap (Jaccard) | 0.008 | 0.005 | 0.21 |
| Same opener | 0.020 | 0.012 | 0.38 |
| Same first sign | 0.011 | 0.007 | 0.21 |
| Same final sign | 0.028 | 0.019 | 0.27 |
| Same animal | 0.074 | 0.046 | 0.12 |
| Identical text | 0.000 | 0.000 | 1.00 |

**Verdict: no house signature.** Seals found in the same house are no more alike in text, opener, ending or animal than seals from other houses of the same area. No two seals in the same house share a text. Together with the area-level result (`context_scouting.md`), this means the find-spot does not predict what a seal says, at any scale we can measure: house, area, city or region.

**Caveats.** Mohenjo-daro only in practice; house labels as recorded by the early excavators; seals may have been lost or discarded away from where they were used.
