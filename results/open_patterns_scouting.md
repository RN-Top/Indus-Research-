# Open-minded pattern discovery: what the data shows with no theory, and what predicts (EXPLORATION, not a registered test)

*16 October 2026. Exploration split only (1,523 texts; damaged dropped, duplicates removed, unidentified signs dropped). The holdout was not read, and nothing was registered. Script: `scripts/open_patterns.py`. Numbers: `open_patterns.json`. Printout: `open_patterns_output.txt`.*

**Caveat:** this is a fishing expedition by design. Many of the patterns below may be noise, chance or artefacts of one transcription. Only the prediction scores in Part B are cross-validated, and even those are within the exploration split.

## The approach

- No theory of language, numbers or religion.
- **Part A** lets sign classes emerge from contexts alone:
  - each sign is described by the signs on its left and right;
  - that description is weighted (PPMI), compressed (SVD to 20 dimensions) and clustered (k-means, 12 classes);
  - recurring motifs and whole-inscription templates are then listed.
- **Only afterwards** were the classes compared with what we already believe:
  - openers and closers from the frozen rule;
  - numerals by shape;
  - the end-of-middle signs G100, G760, G142 and G923.
- **Part B** asks whether structure predicts. A hidden sign is guessed using five-fold cross-validation over exploration texts, comparing three models:
  - a frequency-only baseline;
  - a bigram model (guess the sign from the one before it);
  - a two-sided model (guess it from both neighbours).

## Part A: what falls out

### Sign classes from context alone

104 signs used at least 10 times were grouped into 12 classes, ordered here by average position in the text.

| Class | Sits | Members (commonest first) | Matches what we believed? |
|---|---|---|---|
| 5 | early (starts 54%) | G861, G705, G920, G413, G35 | yes: openers |
| 7 | early (starts 32%) | G820, G741, G31, G368, G125, … | yes: openers, plus early-middle signs |
| 11 | early (starts 41%) | G33, G817, G840, G575, … | partly: opener G817 alongside numeral G33 |
| 8 | early (starts 35%) | G255, G503, G440, G495, … | partly: opener G503 |
| 10 | early-middle | **G2, G32, G1**, G350, G416, G13 | **yes: small numerals** (G2 included) |
| **4** | middle | **G220 (fish), G240, G235, G233, G803, G806, G798, G231, G236** | **new: a class with no assigned role** |
| 2 | middle | G590, G3, G4, G61, G690, G142, G692, … | mixed: numerals 3–5 with middle signs |
| 0 | middle | **G17, G55** (stacked 7 and 12), G460, G435, … | partly: the "special" stacked numbers sit together |
| **9** | late-ish (ends 27%) | **G60**, G527, G617, G892 | **unexpected: G60 groups with closers** |
| 6 | late (ends 43%) | G390, G900, G405, G407, G156, G700, G154 | yes: closers, plus the count-like items G390 and G900 |
| 3 | late (ends 45%) | **G740**, G520, G176, G415, **G100, G760, G923**, … | yes: the generic closer with the end-of-middle signs |
| 1 | last (ends 64%) | G400, G90, G140, G151, G621, … | yes: specific and post-terminal closers |

**From context alone, the method rediscovers the layout.** Opener classes sit at the front, closer classes at the back, the small numerals form their own class, and the end-of-middle signs fall in with the closer G740.

### Recurring motifs of 3–4 signs

| Motif | Uses | Reads as |
|---|---|---|
| G590 G390 G740 | 28 | item + end slot + closer |
| G415 G100 G740 | 21 | item + end-of-middle sign + closer |
| G920 G60 G741 | 19 | heading B + first middle sign |
| G255 G435 G690 (G740) | 17 (15 with G740) | a four-sign ending phrase |
| G705 G33 G520 | 17 | item + three long strokes + closer |
| G2 G32 G220 | 15 | "two long strokes + fish" |
| G840 G32 G740 | 14 | |
| G220 G740 G90 | 12 | fish + generic closer + post-terminal G90 |

### Whole inscriptions as templates

Writing each inscription as its sequence of classes gives **1,186 different shapes among 1,523 texts**. The 20 commonest cover only 11%.

There is **no small set of whole-text formats**. The frame (heading, closer) is fixed, but what fills it varies almost every time.

## Part B: does it predict?

Each sign was hidden in turn and guessed using a model fitted on the other four fifths of the exploration texts. Columns give the share guessed exactly (top-1), the share in the top 5 guesses (top-5), and perplexity (roughly, how many equally likely options the model is choosing among; lower is better).

| Position | Signs | Frequency only (top-1 / top-5 / perplexity) | From the sign before | From both neighbours |
|---|---|---|---|---|
| First sign | 1,523 | 1% / 7% / 246 | 6% / 22% / 333 | 18% / 40% / 201 |
| Right after an opener | 415 | 1% / 56% / 45 | **68% / 84% / 7** | 59% / 81% / 8 |
| Middle | 2,569 | 4% / 18% / 138 | 17% / 38% / 108 | 25% / 49% / 72 |
| Just before the closer | 1,014 | 11% / 19% / 148 | 25% / 45% / 70 | **38% / 61% / 30** |
| Closer (last sign) | 1,002 | 52% / 65% / 29 | 61% / 83% / 8 | **71% / 90% / 4** |
| Last sign of a text **without** a closer | 508 | 0% / 5% / 380 | 9% / 19% / 581 | 7% / 21% / 840 |
| **All positions** | 7,031 | 11% / 24% / 127 | 25% / 43% / 85 | **33% / 55% / 55** |

### Where prediction succeeds and fails

- **Structure predicts.** The two-sided model guesses the exact sign three times as often as frequency alone (33% against 11%).
- **Most predictable** are the **closer** (71% exact), the sign **right after an opener** (G2 or G60; 68%) and the sign **just before the closer** (38%). These carry little new information, because they are largely set by their slot.
- **Least predictable** are:
  - the **first sign**: which heading is chosen is genuinely variable (18%);
  - the **middle** (25%);
  - above all, **the last sign of texts that have no closer**: near-random, worse than frequency alone.
- **So the information is concentrated** in the **choice of heading** and in the **middle**. In the ~30% of texts that lack a closer, it sits at the very end too.
- In the function reading, the middle is where a name or specific content would sit. Only those parts of a text vary in ways that cannot be guessed from their neighbours.

## New, against confirmations of what we knew

**Confirmations,** found again with no theory:
- openers at the front;
- closers at the back;
- G2 or G60 right after the opener;
- the end-of-middle slot;
- small numerals as their own class;
- "two long strokes + fish".

**New or unexpected,** most of which may be noise:
1. **An "item" class.** G220 (fish), G240, G235, G233, G803, G806, G798, G231 and G236 group together from context and have no assigned role. They sit in the middle and are a little over-represented right after numerals (24% of signs that follow a numeral, against 14% of signs overall). They may be the things that are counted or named.
2. **Fixed ending phrases, not just fixed ending signs.** Whole 3–4 sign endings recur as units: G590 G390 G740 (×28), G415 G100 G740 (×21), G255 G435 G690 G740 (×15), G705 G33 G520 (×17). The end of an inscription is often a formula.
3. **G60 groups with closers** (G527, G617, G892), not with the heading signs. G60 seems to do double duty: a heading partner after G920 and G692, and also a sign used near the end.
4. **Inscriptions without a closer end on their least predictable sign.** In those texts the content runs to the very end.

## Worth registering later

1. **Fixed ending phrases (recommended).**
   - Claim: the four ending motifs G590 G390 G740, G415 G100 G740, G255 G435 G690 and G705 G33 G520 recur in holdout texts more often than when each text's signs are shuffled.
   - The project's existing `unit_recurrence` kind expresses this directly.
   - Exploration has 83 uses, so about 17 are expected in the holdout. That is above the minimum of 15, and power should be high, because shuffling almost never reassembles three-sign runs.
2. **The predictability gradient.**
   - Claim: on holdout texts, a model fitted on exploration predicts the sign just before the closer better than a middle sign.
   - This needs a new hypothesis kind. It mostly re-confirms the slot structure, so it is lower priority.

Register either only with Erin's go-ahead.
