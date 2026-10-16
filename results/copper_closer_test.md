# Do closers G407 and G617 mark the copper tablets? Pre-registered test

*15 October 2026. Registered in commit `21128bb` (`hypotheses/H-2026-10-16-6c005f7c.json`) before running. Run once on the locked Indus holdout with `scripts/run_confirmatory.py`. Raw output: `confirmatory_2026-10-15_3.json`.*

## The lead

The extended closer test (`closer_categories_ext.md`) found that closing sign G407, and possibly G617, tends to end the small **copper tablets** of Mohenjo-daro. In exploration, 12 of the 67 texts containing either sign are copper (17.9%), against 3.1% of all texts. Both signs also appear on ordinary steatite seals.

## What was registered

- **Claim:** texts that contain G407 or G617 are copper objects more often than chance. All copper objects in the holdout turned out to be tablets.
- **Statistic:** the share of copper among texts containing either sign. **Null:** copper labels shuffled across holdout texts, 2,000 times.
- **Why "contains" and not "ends in":** "ends in" would very likely have fallen below the project's minimum support of 15 texts in the holdout. The registration says so, and states that "ends in" would be reported as a description only.
- **Correction:** Benjamini–Hochberg across every confirmatory test ever run (17).

## Result

| | Holdout |
|---|---|
| Texts in the holdout | 395 |
| Copper tablets among them | **6** |
| Texts containing G407 or G617 (support) | **20** |
| …of which copper | **3 (15%)** |
| Expected by chance | 1.6% |
| p | 0.0045 |
| q (BH, all 17 tests) | 0.0055 |
| **Verdict** | **Supported** |

**Description only (not tested):**
- 11 holdout texts end in G407 or G617, and 3 of them are copper.
- Of the 6 copper tablets, three end in one of the two signs: G407, G407 and G617. The others end in G706, G422 and G753.

## What it means

- **On unseen texts, the pattern held.** Half of the holdout's copper tablets end in G407 or G617, and texts with these signs are copper about ten times more often than chance.
- **G407/G617 is a second closer, after G400, tied to a specific kind of object:**
  - G400 goes with tablets at Harappa;
  - G407/G617 go with the copper tablets of Mohenjo-daro.

  Both are specific marks that sit on top of the generic ending G740. That fits the reading "heading + individual + category mark".
- **What is not shown:** what the mark means. It could name the object class, the issuing body, or something written specifically on copper tablets.

## Limits

- **Very small numbers.** The result rests on 3 copper texts out of 20, and only 6 copper tablets exist in the holdout. One or two different texts would change the picture a lot. The test cleared the minimum support (20 texts) but is fragile.
- **One site.** Copper tablets come almost only from Mohenjo-daro, so "copper" and "this class of tablet at Mohenjo-daro" cannot be separated.
- **Not exclusive.** Most texts containing these signs (13 of 20 in the holdout) are steatite seals, so the signs do not *mean* "copper".
- **Same transcription** (ICIT-derived).

## Next step

An independent sample would make this much firmer. Two possible sources:
- copper tablets in **CISI** (Parpola's corpus, separate from ICIT);
- copper tablets in **Mahadevan 1977**.

About 20–30 more copper tablets would be needed.
