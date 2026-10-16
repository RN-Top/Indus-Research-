# Does the middle of an inscription flow in an order? (EXPLORATION, not a registered test)

*16 October 2026. Exploration split only (1,523 texts; damaged dropped, duplicates removed, unidentified signs dropped). The holdout was not read, and nothing was tested or registered. Script: `scripts/middle_flow.py`. Numbers: `middle_flow.json`. Printout: `middle_flow_output.txt`. This is description; the one shuffled comparison is given as a reference, not a test.*

## Question

The function reading treats an inscription as **[heading] + [middle] + [closer]**. The heading and closer are now described (`heading_types.md`, `closer_categories_ext.md`). Does the **middle** run in an order, the way a Mesopotamian seal's middle runs *name → title → "son of" father*? Or is it a free bag of signs?

## How the middle was cut out

- **Removed at the front:** the opening sign(s), plus G2 or G60 if it comes right after them.
- **Removed at the end:** the closing sign(s), using the frozen role rule.
- **Strict sample:** texts with both a heading and a closer. **254** have a non-empty middle.
- **Loose sample:** texts with a closer, with the heading removed if present. **998** have a non-empty middle. Most of the numbers below come from this sample, because the strict one is small.

**Middle length** in the loose sample:

| Signs in the middle | 1 | 2 | 3 | 4 | 5 | 6 or more |
|---|---|---|---|---|---|---|
| Texts | 175 | 258 | 195 | 131 | 105 | 134 |

Middles are short. Most are 1 to 4 signs.

## 1. Do some signs sit early and others late?

- **Scale:** relative position runs from 0 (just after the heading) to 1 (just before the closer). Signs used at least 15 times in middles of 2 or more signs were included: 49 signs.
- **Reading the spread:** a sign placed at random would average about 0.5, with a spread (sd) of about 0.4.

| Early in the middle | Mean position ± sd | Uses | Share first |
|---|---|---|---|
| G140 | 0.20 ± 0.33 | 24 | 71% |
| G125 | 0.24 ± 0.28 | 20 | 40% |
| G235 | 0.28 ± 0.32 | 106 | 50% |
| G368 | 0.30 ± 0.30 | 26 | 35% |
| G3 (numeral) | 0.31 ± 0.36 | 39 | 51% |
| G741 | 0.33 ± 0.24 | 85 | 27% |
| G31 (long numeral) | 0.37 ± 0.36 | 52 | 40% |
| G415 | 0.37 ± 0.27 | 52 | 29% |

| Late in the middle | Mean position ± sd | Uses | Share last |
|---|---|---|---|
| **G100** | **0.98 ± 0.11** | 53 | **98%** |
| **G760** | **0.98 ± 0.11** | 50 | **98%** |
| G923 | 0.94 ± 0.19 | 18 | 89% |
| G142 | 0.91 ± 0.24 | 24 | 83% |
| G585 | 0.86 ± 0.26 | 17 | 76% |
| G690 | 0.83 ± 0.34 | 24 | 75% |
| G176 | 0.75 ± 0.37 | 52 | 58% |

**The late end is sharp.** G100 and G760 are almost always the last sign before the closer, and G923 and G142 nearly so. These are the "suffix-like" signs already noticed in `content_grammar.md`. **The early end is softer.** No sign is reliably first apart from G140 (and G741 in the small strict sample, first 94% of 17 times).

## 2. Ordered pairs

- **Method:** for pairs of common signs that appear together in at least 10 middles, count how often each comes first.
- **Coverage:** 57 pairs qualify.

**One order wins most of the time:**

| | Observed | Same middles with signs shuffled within each text (reference) |
|---|---|---|
| Pairs with one order at least 90% of the time | **28 of 57 (49%)** | about 1% |
| Pairs with one order at least 75% of the time | **41 of 57 (72%)** | about 7% |

**Strongest pairs:**

| Pair | One way : other way | What it looks like |
|---|---|---|
| G705 → G33 | 36 : 0 | a sign before a long numeral |
| G706 → G33 | 23 : 0 | the same pattern |
| G235 → G33 | 17 : 0 | the same pattern |
| G220 → G33 | 10 : 0 | the same pattern |
| G415 → G220 | 27 : 0 | |
| G415 → G100 | 20 : 0 | |
| G255 → G435 | 19 : 0 | |
| G255 → G690 | 16 : 0 | |
| G17 → G585 | 12 : 0 | |
| G741 → G240 | 11 : 0 | |
| G590 → G390 | 34 : 2 | |

Pairs like G2 → G240 also appear. They come from texts where a heading pair sits in the middle of the text rather than at its start.

## 3. Ordered flow or free bag?

**Ordered, clearly.** Where two common middle signs appear together, one order wins most of the time, far more than shuffling produces. The pattern has three parts:

- **A sharp end-of-middle position.** G100, G760, G142 and G923 sit right before the closer. They are the best candidates for a "title" or "relation" element, or a grammatical ending.
- **Fixed pairings with numerals.** G705, G706, G235 and G220 come *before* the long numeral G33, never after. This looks like "[thing] [number]" phrases inside the middle.
- **Recurrent two-sign combinations** (G415 → G220, G255 → G435, G590 → G390), which behave like fixed phrases.

**What this does not show:**
- **Not "name → title → relation".** There is no clear early "name" class: the early signs are spread out, and many middles are only 1 or 2 signs long. The pattern looks more like **fixed phrases plus a sharp end slot** than a three-part sequence.
- **Not language.** Ordered phrases are expected of nearly any symbol system with set formulas, and Raghavendra (2026) cautions about exactly this.

## Is there a clean confirmatory hypothesis worth registering later?

**Yes, one is clean: "end-of-middle signs".**

- **Statement:** in holdout texts that end in a closer, signs G100, G760, G142 and G923 sit in the last middle position, immediately before the closer, more often than a within-text shuffle predicts.
- **Exploration rate:** about 90–98% in last position.
- **Expected holdout support:** about 35 occurrences, at 20% of the roughly 145 in exploration.
- **Power:** very high for an effect this size.
- **Caution:** part of this overlaps with what is already known (Wells and Fuls's late-medial classes; `content_grammar.md`). It would confirm a slot, not discover one.

**A second, possible one: "sign before long numeral".**
- **Statement:** G705 and G706 come before G33, not after.
- **Support:** about 12 pairs expected in the holdout, which is below the minimum of 15. **Not worth registering yet.**

**Recommendation:** if Erin wants a next locked test on the middle, register the end-of-middle slot test. Run it once, only with her go-ahead.
