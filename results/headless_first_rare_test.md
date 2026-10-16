# Rare signs at the start of heading-less inscriptions: pre-registered test

*16 October 2026. Draft: `drafts/H-headless-first-rare.DRAFT.json`. Frozen and registered in commit `c355698` (`hypotheses/H-2026-10-16-51b7445b.json`) before running, then run once on the locked holdout with `scripts/run_confirmatory.py`. Raw output: `confirmatory_2026-10-16_2.json`. The lead came from `rare_signs_as_names_scouting.md` (angle 2).*

## What was tested

> In holdout inscriptions without a heading, the first sign is a rare sign (5 or fewer uses in the exploration corpus, or unseen there) more often than the interior middle signs of the same inscriptions.

- **Rarity** is fixed by a frozen list of common signs taken from **exploration counts**. Holdout frequencies were never used.
- **Texts:** the first sign is not an opener; trailing closers are removed; the middle has 3 or more signs.
- **Interior:** middle signs strictly between the first and the last, leaving out numerals and openers.
- **Statistic:** the rare share among first signs minus the rare share among interior signs. One-sided. Null: non-numeral middle signs shuffled within each text, 2,000 times.
- **New hypothesis kind:** `first_sign_rarity`, added with a positive control, a negative control, a false-positive-rate check and an extraction check. All 49 unit tests and the page smoke test passed before freezing.

## Result

| | Holdout | Exploration (for comparison) |
|---|---|---|
| Heading-less texts scored | 182 | 742 |
| **First signs that are rare** | **51 of 159 (32.1%)** | 25.0% |
| **Interior signs that are rare** | **65 of 377 (17.2%)** | 13.8% |
| Difference | **0.148** (within-text shuffles: 0.014) | 0.112 |
| p | 0.0015 | |
| q (BH across all 19 confirmatory tests) | 0.0019 | |
| **Verdict** | **Supported** (support 159) | |

Rare shares are higher in the holdout overall, because signs never seen in exploration count as rare there. The *gap* is what is tested, and it held, slightly larger than in exploration.

## Is it just "text edges attract rare signs"? (secondary, descriptive, declared in advance)

| Position | Rare in the holdout |
|---|---|
| First sign | **32.1%** (51 of 159) |
| Last middle sign (just before the closer, or the end) | 20.8% (32 of 154) |
| Interior | 17.2% (65 of 377) |

**Mostly not.** The other edge, the end of the middle, is only a little above the interior. The concentration of rare signs is specific to the **start** of heading-less inscriptions.

**Running total: 19 pre-registered tests; 16 supported, 3 not supported.**

## What it means

- **Shown, on unseen inscriptions:** when an Indus inscription has no heading, its first sign is unusually likely to be a rare sign, about twice the interior rate. The effect belongs to that position, not to text edges in general.
- **Consistent with, not established:** the reading that these first signs are often **personal names**. Mesopotamian seal legends without "seal of" open with the owner's name, which is usually rare (`rare_signs_as_names_scouting.md`).
- **Other readings remain:** some of these signs may be rare headings that the opener rule is too strict to recognise (for example G201 and G370; see `name_inventory_scouting.md`), rare words, or transcription variants. This test does not separate them.

## Limits

- **One transcription** (ICIT-derived).
- **Signs unseen in exploration count as rare.** That is the frozen definition, but it means a few holdout "rare" signs may be ordinary signs that happened to fall only in the holdout.
- **Order and rarity, not sound or meaning.**
