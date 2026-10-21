# Two kinds of seal text, and what seal size follows (scouting, exploration only)

*20 October 2026. Scripts: inline checks recorded here and `scripts/seal_size_scouting.py`. Sizes are the ICIT export's horizontal × vertical mm (geometric mean; zero = missing), Mohenjo-daro and Harappa seals, 885 with a size. Not a confirmatory test.*

## Short formulas vs long unique texts

| Seal texts (duplicates kept) | Texts | Start with a numeral | Mean length |
|---|---|---|---|
| Same text at 2+ cities | 19 | **42%** | **2.5** |
| Repeated at one city | 20 | 15% | 3.0 |
| Unique | 1,055 | 11% | **5.1** |

The cross-city texts are short formulas of two shapes: **number + item** (G3 G156 ×6 at 3 cities, G16 G390, G31 G156, G5 G405, G3 G390, G5 G900 G740, G3 G140 G100 G740) and **one sign + jar** (G61 G740 ×5 at 4 cities, G416 G740, G803 G740, G910 G740, G923 G740). Unique texts are long. Seals thus carry at least two kinds of text: shared short formulas (standard quantities or categories?) and long one-off texts (individual holders?).

## Seal size

- Size rises with text length: median 20.7 mm (2 signs), 23.6 (4), 25.5 (5), 27.3 (7), 31.5 (8+); Spearman 0.40.
- **At fixed length and city, the text's features do not predict size**: number-first −1% (p 0.71), heading +3% (p 0.32), jar −1% (p 0.51); ending with a closer −5% (p 0.02, weak).
- **The emblem does.** Relative size at fixed length and city: zebu **+20%** (22), elephant +9% (21), rhino +6% (13), unicorn +6% (583), tiger −1% (9), gaur −4% (40), no animal recorded **−20%** (163). Among unicorns, ICIT carving style **W +20%** (223); other styles −14% to +2%.
- A first "unicorn vs other +17%" contrast was mostly the small no-animal seals in the "other" group; withdrawn in favour of the per-animal table.

**Reading.** How big a seal was made depends on its emblem and its carving workshop/style, not on what its text says (beyond needing room for the signs). Size, a likely marker of importance, lives in the **image channel**, consistent with text and emblem being separate layers (`emblem_scouting.md`). The large zebu seals fit their reputation as rare, finely carved pieces; prior work on seal size and status (Kenoyer; Jamison; paragorth `strat_sealsize*.py`) still to be checked.

**Caveats.** Sizes in the export are often rounded inches (25.4, 17.8, 15.2 mm); "unknown" mixes uninscribed-motif, broken and text-only seals; period not controlled.

## Test: do the short formulas mark goods? (sealings, tags, stamped pottery)

*Added 20 October 2026; script `scripts/goods_side_scouting.py`; exploration only.* Goods-side objects: 50 tags/sealings, 11 stamped pots, 8 impressions on implements (69 objects, 48 distinct texts per site).

**Prediction:** if the short formulas are standard quantity or category marks, goods-side texts should be formulas more often than seal texts are.

| | Distinct texts | Text is a short formula | Heading (opener, or marker G2/G60 second) | Mean length |
|---|---|---|---|---|
| Seals | 1,117 | 9% | 32% | 4.9 |
| Goods side | 48 | **2% (1)** | 35% | 4.3 |

- **Prediction failed.** Formulas are, if anything, *rarer* on goods (1 of 48 against about 4 expected; one-sided p 0.06, a lean only).
- Goods were sealed by **a few seals used again and again**: Lothal `G817 G2 G48 G740` ×8 and `G705 G500 G741 G1 G55 G220 G740 G90` ×6; Kalibangan `G91 G56 G2 G417 G890 G892` ×7. These are long, individual-looking texts. Heading share on distinct texts is the same as on seals (35% vs 32%, p 0.64); repeated impressions only make headings *look* commoner.
- Only 4 of the goods texts match an exploration seal text (seals that made sealings rarely survive with them).

**Reading.** The seals that actually closed goods carried the long, one-off kind of text. The short shared formulas do not appear on goods in this sample, so they were probably not quantity labels for shipments; they may have been worn or kept as tokens or badges of a category. Small sample (48 texts, dominated by Lothal and Kalibangan).
