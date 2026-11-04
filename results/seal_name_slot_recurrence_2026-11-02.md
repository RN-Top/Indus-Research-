# Seal opener recurrence, corrected null (2 Nov 2026, local, not committed)

Script: `scripts/seal_name_slot_recurrence.py`. Data: merged corpus, `seq_strong`, seals with 3+ signs.

## Correction

The first version shuffled signs inside each seal. That destroys the fixed formulas it was meant to test, so its p-values were invalid. This version regenerates each seal from its class's unigram sign frequencies (same length, no order). That keeps common signs and removes all fixed sequences, so the test asks whether openers recur beyond what sign frequencies alone predict.

## Result (recurring = same opener on >= 5 seals)

| class | opener length | observed recurring | unigram null (mean) | p |
|---|---|---|---|---|
| SEAL:S (n = 1,296 impressions) | 2 signs | 16 | 12.3 | 0.11 |
| SEAL:S | 3 signs | 17 | 0.04 | <0.005 |
| SEAL:R (n = 301) | 2 signs | 5 | 0.1 | <0.005 |
| SEAL:R | 3 signs | 2 | 0.0 | <0.005 |

Top openers (distinct texts, SEAL:S): G861 G2 (158), G820 G2 (50), G920 G60 (46), G692 G60 (19). Top 3-sign: G920 G60 G741 (26), G861 G2 G235 (14), G861 G2 G240 (13).

## Reading

- Two-sign openers are not more common than sign frequencies predict (SEAL:S, p = 0.11). The strong result is at three signs, where fixed formulas appear.
- G861 G2 is the dominant opener. The repo's item-sign notes already treat G861 as a fixed-number element, so this is consistent with a fixed heading or formula, not a name.
- Whether the variable part after these openers is a name is untested. That is the next step.

## Limits

- The unigram null is weak for formulaic text. A better null would preserve position-specific sign frequencies. Treat the SEAL:R p-values with care, since the class is small.
- Nothing here reads any sign or matches Samar or Nanaza. It shows which openers recur, not what they say.
