# Are the Indus openers different kinds of heading? (EXPLORATORY)

*16 October 2026. Exploration split only; the holdout was not read and nothing was registered. Script: `scripts/heading_types.py`. Numbers: `heading_types.json`. Printout: `heading_types_output.txt`.*

## Why

Mesopotamian seal legends open in one of two ways, and each goes with a different kind of legend:
- with "seal of" (*kišib*);
- with an overlord's name (*Šu-Suen, strong king …*).

See `seal_function_comparison.md`. If the Indus heading also comes in types, the opening slot carries information, and is not just a fixed formula.

## Method

- **Texts:** the 343 exploration texts whose first sign is one of the six openers used at least 15 times: G820 (92 texts), G861 (83), G817 (78), G920 (50), G692 (25) and G503 (15).
- **Question:** does the opener predict anything about the rest of the text? Seven attributes were tested:
  - how it ends;
  - object type;
  - site;
  - seal animal;
  - length;
  - whether it has a numeral;
  - the mix of middle signs.
- **Statistics:** each test compares against 5,000 shuffles of the opener labels (1,000 for the middle-sign mix). Effect sizes are Cramér's V and excess V. Benjamini–Hochberg correction across the 7 tests.

## Results

| Attribute | Differs by opener? | V (excess) | q |
|---|---|---|---|
| Ending (which closer, or none) | no | 0.14 (0.07) | 0.25 |
| Object type | no | 0.11 (0.00) | 0.77 |
| Site | no | 0.11 (0.00) | 0.77 |
| Seal animal | no | 0.13 (0.00) | 0.77 |
| Length | **yes, modestly** | 0.18 (0.13) | 0.003 |
| Has a "numeral" | **yes, strongly**, but see below | 0.57 (0.55) | 0.001 |
| Middle signs | **yes** | JSD 0.33 against 0.22 shuffled | 0.003 |

### The real pattern: two heading families, set by the sign that follows

| Opener | Texts | Next sign is G2 | Next sign is G60 | Contains G2 | Contains G60 |
|---|---|---|---|---|---|
| G817 | 78 | **67** | 0 | 86% | 3% |
| G861 | 83 | **73** | 0 | 88% | 0% |
| G820 | 92 | **56** | 15 | 64% | 17% |
| G920 | 50 | 0 | **37** | 6% | 80% |
| G692 | 25 | 0 | **19** | 8% | 76% |
| G503 | 15 | 0 | 0 | 13% | 0% |

- **Family A, "opener + G2":** G817, G861 and mostly G820.
- **Family B, "opener + G60":** G920 and G692.
- G503 belongs to neither.
- **The strong "numeral" result is this same pattern,** not a difference in counting. G2 is a two-stroke sign, which our shape rule files as a numeral. If G2 is left out, texts in both families contain other numerals at similar rates (32–49%).
- **Middle signs:** these differ for the same reason (G2 against G60), plus some lean of later signs. Family A's next most common middle signs are G220, G240 and G390; Family B's are G741 and G220.
- **Length:** Family B texts run a little longer. G920 texts are most often 6–7 signs.
- **What does not differ:** the ending, object type, site and animal. Both families end in G740 about as often, sit on the same kinds of seals at the same sites, and carry the same animals.

## What it means

- **The Indus heading is two-part and comes in at least two types:** [opener] + G2, or [opener] + G60.
  - Wells and Fuls already describe signs 2 and 60 as "initial cluster terminal markers", the signs that close the opening cluster (`novelty_assessment.md`).
  - What this adds is the pairing: particular openers take G2 and others take G60, almost never the other way round. Whether Wells or Fuls already noted the pairing should be checked before claiming it as new.
- **Function reading:** the heading is not one fixed formula. It is a small set of formulas, like Mesopotamian "seal of …" against "[king], …". The two types do not go with different objects, sites, animals or endings. So whatever distinguishes them is not visible in the metadata. It might be different issuing offices, kinds of title, or grammar.

## Limits

- **Exploratory.** Several attributes were tested on data already looked at. The G2 and G60 split was found by looking.
- **G2 and G60 are frequent signs.** Their placement right after openers is part of what makes the openers "openers" under the rule, so the strength of the pairing is partly expected. The **exclusivity** of the pairing is not built into the rule: G817 and G861 almost never take G60, and G920 and G692 almost never take G2.
- **Same transcription** (ICIT-derived).

## Possible confirmatory test

**"In holdout texts that start with G817, G861, G920 or G692, the sign after the opener is G2 for G817/G861 and G60 for G920/G692, more often than chance."**
- Exploration gives 140 of 159 texts in the predicted pairing in family A and 56 of 75 in family B (G820 left out).
- About 50–60 such texts are expected in the holdout. With an effect this large, power would be high.
- Register first, run once, only with Erin's go-ahead.
