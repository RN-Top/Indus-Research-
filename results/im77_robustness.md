# Transcription robustness: supported results rerun on Mahadevan's corpus (IM77)

*21 October 2026. Script: `scripts/im77_robustness.py`. Data (not copied here): Mahadevan 1977 / Input Data File 1980 as exported from indusscript.in (github.com/paragorth/Indus-, `data/im77`), and that project's unvalidated ICIT→Mahadevan sign bridge (`data/derived/bridge_extended.json`, 145 signs). 2,742 IM77 texts (one per object side, lines joined in order) after dropping texts with illegible passages (sign 0).*

**What this is and is not.** IM77 is an independent *transcription* of largely the *same objects*, exploration split included. A pass therefore shows a result does not depend on ICIT's reading conventions; it is not new evidence and is not counted in the confirmatory total. Each frozen test is run unchanged except that its sign lists are translated; signs without a bridge entry are dropped (coverage shown), and a sign mapped to several Mahadevan signs becomes all of them.

| Hypothesis | Kind | IM77 observed | Null | p | Support | Coverage |
|---|---|---|---|---|---|---|
| 5dbc167c | numerals on seals | 0.743 | 0.536 | 0.0005 | 864 | 5/7 signs |
| 97716181 | short vs stacked strokes | 0.550 | 0.100 | 0.0005 | 728 | 5/7; 4/4 |
| c9abe80e | jar G740 at the end | 0.680 | 0.232 | 0.0005 | 1,189 | 1/1 |
| f11252d5 | numerals not final | 0.954 | 0.756 | 0.0005 | 1,863 | 16/22 |
| 2c3faaf6 | numeral pair specificity | 1.940 | 0.702 | 0.0005 | 1,539 | 16/22 |
| 7498df9d | G32 precedes G220 | 50 | 10.7 | 0.0005 | 50 | 2/2 |
| 2e6e5589 | G400 on Harappa tablets | 0.378 | 0.226 | 0.0015 | 82 | 1/1 |
| 8404d7b4 | recurring units | 2,166 | 489 | 0.0005 | 2,166 | 62/68 units |
| ada8b343 | heading units at the start | 0.872 | 0.237 | 0.0005 | 250 | 3/3 |
| dd41a7b5 | formula units at the end | 0.907 | 0.258 | 0.0005 | 54 | 3/3 |
| 0c595386 | heading → middle → closer (non-Mohenjo-daro) | 0.796 | 0.239 | 0.0005 | 470 | 9/9; 49/57; 7/8 |
| 6c005f7c | G407 on copper | 0.097 | 0.025 | 0.0005 | 113 | **1/2** (G617 unmapped) |
| a6cd844c | end-of-middle slot | 0.931 | 0.309 | 0.0005 | 175 | 4/4; 7/7; 10/12 |
| 51b7445b | rare first sign without heading | 0.123 | −0.004 | 0.0005 | 720 | common list 115/159 |
| be9ab5ab | enclosure mark → end | 0.497 | 0.002 | 0.0005 | 23 | **1/17 pairs** |

**All 14 translatable supported results also hold in Mahadevan's transcription** (every p ≤ 0.0015).

**Weak spots.**
- The enclosure-mark rerun rests on a single bridged pair (23 tokens); the bridge lacks most marked variants. Not a meaningful replication of that result.
- The copper-closer rerun covers only G407.
- For the rare-first-sign test, 44 common signs are unbridged and so count as "rare" in both first and interior positions; this blurs the contrast rather than creating it.
- The bridge is unvalidated by its authors or by us; a wrong mapping would mostly weaken, not manufacture, a positional result.
- Not translatable here: the external tests (Proto-Elamite, Mesopotamian, genre model) and the image-label and size tests.
