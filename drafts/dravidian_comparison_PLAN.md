# Plan: does Indus structure look more like early Tamil labels than rival languages' labels? (DRAFT, nothing registered)

*19 October 2026. Written **before** any Tamil data was extracted or measured. The features and the predictions below are fixed now, so the Tamil results cannot shape them.*

## Data

| Language | Source | Status |
|---|---|---|
| **Old Tamil** (Dravidian) | Mahadevan, *Early Tamil Epigraphy* (2003). 110 cave inscriptions, plus seal, ring, coin and pottery legends. Full text supplied by Erin. | Extraction started by an agent. |
| **Prakrit** (Indo-Aryan) | *Early Inscriptions of Āndhradeśa* (DHARMA project, CC-BY): 557 TEI-encoded inscriptions, about 210 with English translations, roughly 2nd c. BCE to 4th c. CE. They come from south-east India, a neighbouring region of the same period as Tamil-Brahmi. Repository: github.com/erc-dharma/tfb-eiad-epigraphy | Cloned 19 October 2026. Not yet measured. |
| **Sumerian / Akkadian** | Mesopotamian seal legends. | Already in the project (exploration split). |
| **Indus** | Exploration split only. Any confirmatory test would use the locked holdout. | In hand |

**Genre caveat.** Comparable genres matter more than language:
- The Tamil **cave** inscriptions are donation records ("gift of X").
- The **seal, ring and pottery** legends are owner labels, the closest genre to Indus seals.
- Measures are made per genre, and the main comparison uses labels on objects.

**Time caveat.** Tamil-Brahmi is about 1,500 years after the Indus cities, so it is a descendant-era cousin, not the ancestor. A match is suggestive, never proof.

## Features. Each must be measurable the same way in every corpus, by position only.

1. **Edge variability.** Do the variable elements (rare items, names) sit at the start of a label, with fixed elements at the end, or the reverse?
   - Indus: rare first signs, with fixed closers at the end.
   - Dravidian expectation: name first, then case or title suffix, then fixed word.
2. **Fixed element at the end.** Is there a small set of closing elements, such as a genitive or "gift"?
3. **Suffix stacking.** Is there more than one small fixed element in a row at the end of a word or label (Indus: marker + closer)? Dravidian stacks suffixes. Sumerian also does; Prakrit less so in labels.
4. **Numerals before the counted item.** Dravidian: number + noun. Prakrit: mostly noun + number, or both orders.
5. **Prefix-like fixed elements.** Does a small fixed set sit *before* variable items (Indus openers)? Dravidian has no prefixes, so the opener + G2/G60 heading has to be a separate word or title for Dravidian to fit.

**Discriminating power, to be judged before testing.** For each feature, write down what each language predicts. Keep **only** features where Old Tamil and at least one rival predict differently.
- An expected problem: Prakrit donor labels ("X-sa danam") and Tamil labels ("X-a kotai") share the name + genitive + "gift" shape.
- So several features may not discriminate at all. That is a result in itself, and it will be reported.

## Rules

- Measure Tamil, Prakrit and Sumerian first. Predictions are written and committed before Indus is compared.
- Report every feature, including the ones that favour a rival, or none.
- No sound values. No readings.
