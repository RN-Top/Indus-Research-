# Confirmatory results, 14 October 2026

Four hypotheses were frozen and committed (commit `9316be3`) before the holdout was touched, then each was tested once on the locked holdout of the full corpus (533 texts; settings locked in each hypothesis file). 5,000 permutations each; p-values corrected together with Benjamini-Hochberg. Raw output: `confirmatory_2026-10-14.json`. Script: `scripts/run_confirmatory.py`.

| Hypothesis | Observed | Control | q (BH) | Verdict |
|---|---|---|---|---|
| Positive control: jar sign G740 ends texts | 61.7% of its uses | 24.0% | 0.0002 | Supported |
| Stroke numerals (grouped by shape) are followed by another sign | 93.7% | 76.6% | 0.0002 | Supported |
| Short and long strokes are followed by different signs | 0.613 bits | 0.341 bits | 0.0002 | Supported |
| Texts with short strokes are seals | 74.7% | 57.6% | 0.0002 | Supported |

0.0002 is the smallest p-value 5,000 permutations can give.

## What this does and does not show

- The holdout comes from the same transcription as the exploration texts. These results show the patterns are not flukes of the exploration sample; they do not yet show they hold in other transcriptions. Replication on ICIT is the next requirement.
- The numeral results concern how stroke signs behave, not what they count. They are consistent with numbers preceding counted items, and with two distinct stroke systems.
- The seal association was found during exploration and contradicts a simple version of the ration-tablet idea (Rao 2017); it has now held on unseen texts.

## Second batch (commit `6fb502d` registered them; tested afterwards)

Raw output: `confirmatory_2026-10-14_2.json`. q-values are corrected across all six confirmatory tests to date.

| Hypothesis | Observed | Control | q (BH, all 6 tests) | Verdict |
|---|---|---|---|---|
| Numerals pair with particular following signs (fixed phrases) | 2.336 bits | 1.634 bits | 0.0002 | Supported |
| Two long strokes (G32) are followed by the fish sign (G220) | 11 times | 2.6 times | 0.0002 | Supported |

The holdout is smaller than the exploration split, so mutual information is higher in both the observed value and the control (small samples inflate it equally); the excess over the control is what counts (0.70 bits here, 0.96 in exploration). The G32-fish result rests on 11 occurrences, above the minimum of 5 but small; replication on a second corpus matters most for it.

## Third batch: word units and context (registered in commit `c2e3ec9`, tested afterwards)

Raw output: `confirmatory_2026-10-14_3.json`. These five used the duplicates-removed corpus (holdout: 395 distinct texts). q-values are corrected across all 11 confirmatory tests to date.

| Hypothesis | Observed | Control | q (BH, all 11) | Verdict |
|---|---|---|---|---|
| 68 learned two-sign units recur in unseen texts | 352 occurrences | 87.6 | 0.0002 | Supported |
| Opening units (G817 G2; G920 G60 G741; G692 G60) start texts | 92.7% of 41 | 26.3% | 0.0002 | Supported |
| Closing units ending in G520 end texts | 100% of 10 | 27.1% | 0.0002 | Supported |
| Within Harappa, G400 texts are tablets | 97.0% of 33 | 62.4% | 0.0002 | Supported |
| Within seals, G741/G390 texts carry the unicorn | 62.2% of 37 | 65.0% | 0.71 | **Not supported** |

## What this does and does not show

- **Word units are real.** Units learned on one set of texts recur four times more than chance in texts never examined, and the opening and closing formulas keep their slots. Inscriptions are built from recurring multi-sign units in fixed positions. The closing-unit result rests on 10 occurrences; it needs replication.
- **G400 marks the tablet genre at Harappa.** Site cannot explain it, since the test ran within Harappa. It does not hold at Mohenjo-daro in exploration, so it may be a local Harappan convention.
- **The unicorn link failed.** In exploration, G741 and G390 seemed to go with unicorn seals even within seals; on unseen seals they do not. It was most likely a chance pattern of the exploration texts, and it is withdrawn. This is the holdout doing its job.

**Running total: 11 pre-registered hypotheses tested on the holdout; 10 supported, 1 not supported.**

## Fourth batch: iconography (registered in commit `cf92e27`, tested afterwards)

| Hypothesis | Observed | Control | q (BH, all 13) | Verdict |
|---|---|---|---|---|
| Within Mohenjo-daro seals, unicorn seals use a different overall sign mix | 0.249 | 0.237 | 0.25 | Not supported |
| Within Mohenjo-daro seals, G806 texts are on non-unicorn seals | 40% of 5 | 35% | 0.63 | Not supported |

See `iconography_context.md`. **Running total: 13 tested; 10 supported, 3 not supported.**

## Fifth batch: inscription structure across sites (registered in commit `c1615e2`, tested afterwards, 15 October 2026)

Raw output: `confirmatory_2026-10-15.json`. Per-site rates (declared in advance as descriptive, no separate tests): `confirmatory_2026-10-15_per_site.json`.

**Hypothesis `H-2026-10-15-0c595386` (`template_order`).** Openers, middle signs and closers were learned from **Mohenjo-daro exploration texts only**, using the rule in `functional_by_site.md` D.1. The hypothesis: they put holdout texts from **all other sites** in slot order (opener → middle → closer) more often than shuffling each text's signs predicts.

| Holdout texts scored | In slot order | Shuffled | p | q (BH, all 14) | Verdict |
|---|---|---|---|---|---|
| 138 (from 395 distinct holdout texts, Mohenjo-daro excluded) | **76.1%** | 26.7% | 0.0005 (the minimum with 2,000 permutations) | 0.0006 | **Supported** |

**Per site** (descriptive): Harappa 71/92 (77%), Dholavira 10/11 (91%), Lothal 6/8 (75%), Chanhu-daro 6/12 (50%), Kalibangan 3/6 (50%), and 8 single texts or pairs from seven other sites plus one of unknown site, 9/9 in order.

### What this shows

- **Shown:** the signs that open and close inscriptions at Mohenjo-daro open and close them, with content between, at the other Indus sites, in texts never used to build or tune the test. The exploration estimate (77.6%) is reproduced almost exactly (76.1%).
- **Credit:** Wells and Fuls described this layout first (initial signs, the initial cluster terminal marker, terminal markers; ICIT). This result is a pre-registered statistical confirmation of it, plus a demonstration that it transfers across sites. It is not a new discovery of the layout.
- **Limits:**
  - Chanhu-daro and Kalibangan are lower (50%), on 12 and 6 texts, too few to tell whether they differ.
  - The main corpus derives from ICIT (see METHODS), so this confirms the result within one transcription tradition. The independent CISI transcription agrees on Mohenjo-daro seals (`cisi_skeleton_check.md`).
  - The test says nothing about what the slots mean or whether the script records a language.

**Running total: 14 pre-registered hypotheses tested on the holdout; 11 supported, 3 not supported.**

## Sixth batch: the comparison scripts' own holdouts (registered in commit `2a193e3`, tested afterwards, 15 October 2026)

Raw output: `confirmatory_2026-10-15_2.json`. Run by `scripts/run_external_confirmatory.py`. The source corpora are not in this repository (CDLI terms); the output records their SHA-256.

| Hypothesis | Claim | Holdout result | Exploration | p | q (BH, all 16) | Verdict |
|---|---|---|---|---|---|---|
| `H-2026-10-16-9d9defa5` | Signs the unchanged Indus role rule calls **openers** in Proto-Elamite fall inside the header that **experts marked** | **62.7%** of 59 opener tokens inside the header, on 81 unseen tablets; 9.1% when positions are shuffled within each tablet | 80.6% | 0.0005 | 0.0006 | **Supported** |
| `H-2026-10-16-12cb3aa3` | Indus **opening units** come in fewer distinct forms than Mesopotamian seal-legend openers at equal sample size | **18** distinct Indus forms in 136 holdout texts, against **76.4** for Mesopotamian legends sampled at 136; random split of the pooled units gives no difference (0.1) | 12.3 against 53.1 per 80 | 0.0005 | 0.0006 | **Supported** |

### What this shows

- **Proto-Elamite (the method check).** On tablets never looked at, the blind rule's openers land inside the header that experts marked, seven times more often than chance. The rate shrank from the exploration estimate (81% to 63%), as leads usually do, but stayed far above chance. This is the strongest evidence so far that the rule finds a real heading where one exists.
- **Indus against Mesopotamia (the function reading).** Indus opening slots repeat a small set of forms. Mesopotamian seal legends start with far more varied words, many of them personal names (the owner's name often comes first) as well as *kišib* "seal of".
  - So the Indus opener behaves like a **fixed heading**, not like a name slot.
  - **Limit:** this is partly built into the rule's output. Exploration had already found 7 Indus opener signs against 92 Mesopotamian opener words. The test confirms the difference holds on unseen texts. It does not show what the heading means.
- Neither result says what any Indus sign means or whether the script records a language.

**Running total: 16 pre-registered hypotheses tested; 13 supported, 3 not supported.**

## Seventh batch: closers on copper tablets (registered in commit `21128bb`, tested afterwards, 15 October 2026)

Raw output: `confirmatory_2026-10-15_3.json`. Write-up: `copper_closer_test.md`.

| Hypothesis | Claim | Holdout result | p | q (BH, all 17) | Verdict |
|---|---|---|---|---|---|
| `H-2026-10-16-6c005f7c` (`class_association`) | Texts containing closer G407 or G617 are copper objects more often than chance | **3 of 20** such texts are copper (15%), against 1.6% when labels are shuffled; holdout has 6 copper tablets in 395 texts | 0.0045 | 0.0055 | **Supported** (support 20) |

**Running total: 17 pre-registered hypotheses tested; 14 supported, 3 not supported.**
