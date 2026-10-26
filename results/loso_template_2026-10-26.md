# The layout holds at every major site, with roles learned without that site: pre-registered test

*26 October 2026. Registered in commit `4260284` (17:21:18 −04:00): spec `predictions/loso_template_2026-10-26.json`, script `scripts/loso_template_test.py`; run once. Raw: `loso_template_2026-10-26.json`.*

For each site, sign roles (opener, middle, closer; numerals by shape) were learned with the frozen rule from **all other sites only**, then the site's texts were tested for slot order (opener → middle → closer) against the same texts with signs shuffled within each text.

| Test site | Texts | Scored | In slot order | Shuffled | p |
|---|---|---|---|---|---|
| Mohenjo-daro | 1,046 | 762 | 74% | 20% | 0.0005 |
| Harappa | 733 | 457 | 79% | 25% | 0.0005 |
| Dholavira | 74 | 55 | 64% | 22% | 0.0005 |
| Lothal | 72 | 50 | 74% | 22% | 0.0005 |
| Kalibangan | 67 | 34 | 71% | 23% | 0.0005 |
| Chanhujo-daro | 48 | 35 | 57% | 17% | 0.0005 |
| Nausharo | 22 | 14 | 93% | 24% | 0.0005 |

**Primary (Stouffer combination): p ≈ 2 × 10⁻¹⁸. Sites with p < 0.05: 7 of 7. Verdict: Supported.** (0.0005 is the smallest p possible with 2,000 shuffles.)

**Reading.** The same writing layout, opening signs then content then closing signs, holds at every major Indus site, from Sindh (Mohenjo-daro, Chanhu-daro) and Punjab (Harappa) to Rajasthan (Kalibangan), Gujarat (Lothal, Dholavira) and Balochistan (Nausharo), even when the grammar is learned without the site being tested. One script, one layout, across the whole civilisation. Dholavira and Chanhu-daro conform less (57–64%), which may reflect local formulas or more texts with no opener.

**Limits.** Texts from the locked holdout and the held-out-from-export set were used as test data for this new question. Roles learned without Mohenjo-daro or Harappa come mostly from the other big site, so those two tests are each other's transfer.
