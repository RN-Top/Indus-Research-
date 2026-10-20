# S1/S2: are Indus closers suffix-like, and are openers prefix-like? (EXPLORATION)

*19 October 2026. The predictions were frozen first: `drafts/S1_S2_PREDICTIONS.md`, commit b03a9cf. Script: `scripts/affix_profile.py`. Numbers: `affix_profile.json`. Exploration split only; the holdout was not used.*

**Method.** Each role sign is compared with non-role signs of similar frequency (±30%). Both are subsampled to the same number of neighbours, and the entropy of their neighbours is compared.

## S1: closers, predecessor diversity

| Result | Closers |
|---|---|
| Above the control (suffix-like) | G156 |
| Below the control (formula-like) | **G90**, which follows G740 in 52 of 67 cases: a fixed pair |
| Within the control | G151, G154, G405, G407, G527, G617, G621 |
| No frequency-matched controls at ±30% | **G740, G400, G520**, the three most important closers |

**Verdict by the frozen rule: MIXED** (1 above, 1 below).

**Descriptive extra, not part of the frozen rule.** Because the ±30% band left the three big closers with no controls, they were compared with the 10 commonest non-role signs, all subsampled to 52 predecessors.

| Closer | Predecessor entropy | Rank among the 10 comparison signs |
|---|---|---|
| **G740** (the jar) | 4.86 bits | Above **all 10** (they range 3.05–4.61) |
| G400 (Harappa tablets) | 3.66 bits | Middle (above 5 of 10) |
| G520 | 3.31 bits | Near the bottom (above 1 of 10). Fits its fixed pairing with "three long strokes". |

So **the jar attaches to a wider variety of signs than any common sign**, as a grammatical ending or a generic end-of-label mark would. The other closers do not; several are tied to particular partners.

## S2: openers, successor diversity

| Result | Openers |
|---|---|
| **Above the control (prefix-like)** | **none** |
| Below the control (formula-like) | G692, G820, G861 |
| Within the control | G416, G503, G817, G920 |

Mostly followed by G2 or G60:
- G817: G2 in 69 of 86 cases;
- G861: G2 in 89 of 112.

**Verdict by the frozen rule: MIXED.** Three are below, short of the required 4. But **not one opener is prefix-like**, and the large ones lean strongly towards fixed formulas.

## What this does and does not say

| Question | Answer | Weight |
|---|---|---|
| Is there a prefix-like class at the start? | **No sign of one.** Openers are fixed heading formulas (opener + G2/G60), not prefixes on varied words. | This is **against a Munda-style prefixing pattern at text starts.** It is weak, because text starts are not word starts. |
| Do closers behave like suffixes? | **Only the jar (G740) clearly does.** The other closers are mixed or formula-like. | Fits a suffixing system or a generic label ending. It **cannot separate Dravidian from Sumerian or Elamite,** which also suffix. |

**Net for the language question:**
- The edges look like "suffix yes, prefix no". That is compatible with Dravidian, Sumerian and Elamite.
- It is less comfortable for a strongly prefixing language.
- It is not evidence for Dravidian specifically.

**Next step:** the same measures on reference corpora at the word level, to calibrate what a suffixing and a prefixing language look like in short labels. This needs the re-segmented Tamil and Prakrit data, which is in progress.
