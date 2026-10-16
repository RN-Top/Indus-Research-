# Do rare signs behave like names? Several angles (EXPLORATION, not a registered test)

*16 October 2026. Exploration split only (1,523 Indus texts; damaged dropped, duplicates removed, unidentified signs dropped). The holdout was not read, and nothing was tested or registered. Script: `scripts/rare_signs.py`. Numbers: `rare_signs.json`. Printout: `rare_signs_output.txt` (follow-up checks at the end).*

**Reference.** The Mesopotamian seal legends (exploration split, words as units) were analysed the same way. There we *know* where the names are: the owner's name, the title, and "son of" + the father's name.

**Caveat:** several of these angles can look name-like by coincidence. Words used only once arise in any large vocabulary, not only from names.

## Definitions

- **Rare sign:** used 5 times or fewer in the exploration corpus.
- **Slots**, from the frozen role rule:
  - *heading*: leading openers, plus G2 or G60 right after them;
  - *first middle*: the first sign after the heading, or the first sign of a text without a heading;
  - *middle*: signs between the first and last middle positions;
  - *last middle*: the sign just before the closer, or the last sign of a text without one;
  - *closer*: trailing closing signs.

## Angle 1: the frequency profile

| | Sign types | Used once | Twice | 3–5 times | Rare share of **types** | Rare share of **tokens** |
|---|---|---|---|---|---|---|
| Indus | 530 | 200 | 82 | 89 | **70%** | **9.9%** |
| Mesopotamian legends (words) | 6,428 | 4,198 | 829 | 708 | 89% | 22.4% |

**Long-tailed, as a vocabulary with many names would be:** most sign types are rare, but they make up only a tenth of what is written. The tail is thinner than in Mesopotamian legends, which are full of personal names. The profile alone cannot tell names from other rare vocabulary.

## Angle 2: where rare signs sit

**All texts:**

| Slot | Indus: share of signs that are rare | Mesopotamian reference |
|---|---|---|
| Heading | 0% (by definition: heading signs are common) | 0% (same) |
| **First middle** | **18.3%** | **42.8%** (owner names often come first) |
| Middle | 9.6% | 14.4% |
| **Last middle** (just before the closer) | **14.1%** | **30.3%** (the father's name comes before "your servant") |
| Closer | 0% (by definition) | 0% (same) |

**Control: texts that have a heading, middles of 3 or more signs:**

| | First middle (right after the heading) | Middle | Last middle |
|---|---|---|---|
| Indus | 5.6% | 6.6% | **12.8%** |
| Mesopotamian reference | 1.7% | 10.4% | **26.2%** |

- **The Indus pattern has the same shape as the Mesopotamian one, at roughly half the strength.**
  - Rare signs are **enriched just before the closer**, whether or not there is a heading. In Mesopotamia this is where the father's name sits, just before *arad₂-zu*.
  - Rare signs are **enriched at the very start of texts without a heading**. In Mesopotamia legends without "seal of" begin with the owner's name.
  - Right **after a heading, rare signs are not enriched**, in either script. In Mesopotamia a fixed title (*lugal kal-ga*, "strong king") follows a king's name.
- **This is the strongest convergent angle.** The rare signs sit where names sit in a seal script whose names we can read.

## Angle 3: object types

| | Texts | With a rare sign | Rare share of tokens | Mean length |
|---|---|---|---|---|
| Seals | 1,057 | **39%** | 9.9% | 5.0 |
| Tablets | 359 | 32% | 9.3% | 3.7 |
| Pottery | 45 | 33% | 11.9% | 2.8 |
| Tags | 28 | 29% | 7.9% | 4.5 |

**Weak support.** Seals are slightly more likely to carry a rare sign, as an owner-name reading predicts. But per sign written they are no richer, and seal texts are longer, which alone raises the chance of containing one. **Neutral to slightly for** the names reading.

## Angle 4: the frame around rare signs

- 564 texts contain a rare sign. Only **7%** have both a heading and a closer around it, against **17%** of all texts. At least one of them is present in 61%, against 72%.
- **Commonest shape:** no heading, then a rare sign first, then the rest, then a closer (129 texts).

**Mixed.** The idealised [common heading] + [rare name] + [common closer] is *less* common than average. The typical rare-sign text drops the heading and starts with the rare sign, then ends normally. In Mesopotamian terms that is a legend opening straight with the owner's name.

## Angle 5: other explanations

| Alternative | Evidence | Leans |
|---|---|---|
| **(a) Damage or garbling** | Damaged texts are removed before analysis, and the flag is empty afterwards, so this could not be checked here. Texts with rare signs are not shorter (5.0 signs against 4.4). | Not testable here; no sign of it |
| **(b) Variant forms of common signs** | Only 9 of 371 rare sign types (2%) have a common sign that the source lists as similar, about the same as for common signs (3%). But the source's variant list is short (69 pairs). | Slightly against, on thin data |
| **(c) Ligatures (two signs fused)** | Cannot be tested without looking at the sign shapes. | Open |
| **(d) Transcription habits** | Not testable within one transcription. A CISI check of the rare signs where the corpora overlap would settle part of it. | Open |

## Synthesis

**The names reading partly holds.**

- **Converges toward names:**
  - **Angle 2** is the strongest. Rare signs sit in the same places where names sit in Mesopotamian seal legends: just before the closer, and at the start of texts with no heading. Right after a heading they are no rarer than elsewhere, as in Mesopotamia. The parallel is about half as strong, but the shape is the same.
  - **Angle 4** fits the "legend opening with the owner's name" pattern.
  - **Angle 1** is compatible: a long tail of types that are each used rarely.
- **Neutral or weak:** angle 3 (seals only slightly richer in rare signs).
- **Not ruled out:** variant forms, ligatures and transcription habits (angles 5b–d). Damage could not be tested.
- **Coincidence risk:** text edges may attract unusual signs in any sign system. The Mesopotamian reference shows the pattern is *consistent* with names, not that it *must* be names.

## Worth registering later

1. **Rare signs at the start of heading-less texts (recommended).**
   - Claim: in holdout texts that do not begin with an opener, the first sign is more often a sign that is rare in exploration (5 or fewer uses, or unseen) than interior middle signs are.
   - Exploration: 18.6% against 9.6%.
   - Expected holdout support: about 180 first signs and 470 interior signs. Power for a gap of this size is roughly 80–90%.
2. **Rare signs just before the closer.**
   - Claim: rare signs are over-represented in the last middle position.
   - Exploration: 13.8% against 9.6%.
   - The gap is smaller, so power is low (about 40–50%) on the holdout. Better combined with a second transcription.

Register either only with Erin's go-ahead. Rarity must be defined from exploration counts, frozen in advance.
