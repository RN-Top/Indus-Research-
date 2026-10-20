# Predictions for Indus, frozen before Indus is measured on these definitions

*19 October 2026, committed before `scripts/opening_profile.py` is run on Indus.*

## Definitions (identical for every corpus)

- **Unit:** a word for Old Tamil, Prakrit and Mesopotamian legends; a sign for Indus.
- **Texts used:** texts with 2 or more units.
- **F5, opening concentration:** the share of texts whose first unit is one of the corpus's 5 most common first units.
- **F1r, rare-first ratio:** (share of first units that are rare) ÷ (share of non-first units that are rare).
  - A unit is rare if its type occurs 5 times or fewer in that corpus.
  - The ratio cancels corpus size.
  - Above 1 means variable, name-like material is concentrated at the start.
- **F2, closing concentration:** the share of texts whose last unit is one of the 5 most common last units.

## Reference values

From `results/dravidian_language_side.md`, exploration:

| | F5 |
|---|---|
| Old Tamil caves | 14% |
| Old Tamil objects | 30% |
| Prakrit | 42% |

**F1r** is not measured yet. It is computed by the same script for all corpora.

## Predictions

| If Indus inscribes like… | F5 | F1r |
|---|---|---|
| Old Tamil | low, at or below 30% | clearly above Prakrit's value |
| Prakrit | high, at or above 35% | at or below Prakrit's value |

Anything between those is **undecided**. It will be reported as such.

**This is exploration**, on the exploration split, and the analyst already partly knows the Indus values. Even a clean match means "inscribes like X", **not** "speaks X". Religion, genre and medium differ.
