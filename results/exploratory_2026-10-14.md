# Exploratory results, 14 October 2026

**Status: exploratory.** These are descriptive checks run while building the app. None was pre-registered, so none is evidence for a new claim. They show that the methods behave sensibly on the real data.

Settings: damaged texts excluded, texts with unidentified signs excluded, duplicates kept. Sequence-model and position results use the exploration split only. Entropy uses all texts (descriptive).

## 1. Sign order carries information

| Corpus | Texts | Bigram gain over order-free baseline | Same on shuffled texts (negative control) |
|---|---|---|---|
| indus_website | 2,543 | 1.37 bits/sign, 5/5 folds | −0.04 bits/sign, 0/5 folds |
| cisi_base | 98 | 0.49 bits/sign, 5/5 folds | −0.68 bits/sign, 0/5 folds |
| cisi_allograph | 98 | −0.10 bits/sign, 1/5 folds | −0.75 bits/sign, 0/5 folds |

Block entropy at block size 2 is below all three negative controls in every corpus (full corpus: 1.116 vs 1.245 within-text shuffle, 1.284 corpus shuffle, 1.419 uniform random).

**Reading:** in the full corpus and the CISI base-sign version, knowing one sign helps predict the next, and shuffling removes that. When every sign variant is treated as a separate sign, 98 seals are too few to learn from: 222 sign types, about 1.15 occurrences per sign pair. That is a sample-size limit, not evidence against structure, and it shows why results must be reported under each sign-splitting scheme.

## 2. Known-fact check: the most frequent sign ends texts

A well-established observation in Indus studies is that the most frequent sign (the "jar" sign) usually ends a text in reading order. If the app's orientation handling were wrong, this would fail.

| Corpus | Most frequent sign | Share at text end | Shuffled control | p |
|---|---|---|---|---|
| indus_website | G740 | 0.67 | 0.23 | 0.0005 |
| cisi_base | P324 | 0.85 | 0.19 | 0.0005 |

Both pass, and neither sign ever starts a text. This is a positive control on real data, not a discovery. That G740 and P324 are the jar sign is an inference from frequency and position; confirm against the sign lists before relying on it.

## Data caveats

- 81 of 179 CISI seals were excluded (damaged or containing `P000`).
- The full corpus has no object types or damage flags, so damage filtering does nothing there.

## 3. The two corpora agree with each other

161 of the 179 CISI seals also appear in the full corpus, matched by CISI catalogue number. For the 140 whose two transcriptions have the same number of signs, pairing signs position by position in reading order gives 768 sign pairs, and **96.5% agree with a single consistent G-to-P mapping**. Two independent transcriptions agreeing this closely is evidence that both are reliable, and that both corpora's reading order is handled the same way.

The resulting crosswalk (`data/crosswalk_G_to_P.csv`, built by `scripts/build_crosswalk.py`) maps 192 G-numbers. 58 are confident (3 or more pairs, 90% or more agreement), and those 58 cover 65.5% of all sign tokens in the full corpus. In three cases two G-numbers map to one P-number (for example G861 and G817 to P385), which suggests the website's sign list splits some signs that the CISI transcription treats as variants of one.

Whether the P-numbers are Parpola's (1994) sign-list numbers is not yet confirmed; it should be checked with the dataset's author before results are quoted in Parpola numbers.

## 4. Data fixes found by looking at the signs (14 October, afternoon)

Rendering the full corpus's signs with the source site's font (map in `data/glyph_map.csv`) showed two errors in the transcription as converted:

- `G0` is a line break in the source database, not a sign. It occurred 145 times in 120 texts and was being counted as the 21st most common sign. Line breaks are now removed before analysis.
- Eleven G-numbers (G12, G25, G106, G316, G376, G445, G515, G516, G546, G547, G606) are drawn with a question-mark placeholder: unidentified signs. Texts containing them are now excluded by default, like CISI's `P000`.

Object types (1,461 seals, 886 tablets, 69 pots, 62 tags and others) and materials were recovered from the same database (`data/text_metadata.csv`). Sections 1 to 3 above were computed before these fixes; their conclusions are unchanged in direction but the exact numbers will shift slightly when re-run.

## 5. Numerals (Phase 3, exploration split, 1,988 texts)

Stroke signs were grouped by **shape alone**, before looking at their behaviour: short strokes (G1–G7), stacked strokes (G13–G19, G27–G29, G55) and long strokes (G31, G32, G33, G35). 1,421 tokens in total.

| Test | Observed | Shuffled / permuted control | p |
|---|---|---|---|
| Numerals are followed by another sign (not text-final) | 94.4% | 77.7% | 0.0005 |
| Short and long strokes are followed by different signs (Jensen-Shannon divergence) | 0.486 bits | 0.159 bits | 0.0005 |
| Texts with short strokes are seals | 72.9% | 58.0% | 0.0005 |
| Texts with any numeral are tablets | 25.7% | 34.9% | 1.0 (opposite direction) |
| Long strokes share following-sign contexts (cohesion) | 0.305 | 0.172 | 0.11 |
| Short strokes share following-sign contexts (cohesion) | 0.176 | 0.193 | 0.52 |

**Reading:** numbers precede something, and the two stroke systems behave differently. The simple prediction that numerals concentrate on tablets is not supported; short strokes concentrate on seals instead. Cohesion tests were not significant: within each stroke system, different counts are followed by different signs.

The first three rows, plus a positive control (the jar sign G740 ends texts), were frozen and committed to `hypotheses/` before the holdout was touched. They are tested once on the holdout in `results/confirmatory_2026-10-14.json`.

## 6. What the numerals count (exploration split)

For every sign used 20+ times, the share of its uses that come straight after a numeral was compared with a within-text shuffle (300 shuffles). 18 of 71 signs are counted more than chance (p < 0.01). The most strongly counted:

| Sign | Uses | After a numeral | Shuffled expectation | Usual numeral |
|---|---|---|---|---|
| G585 | 24 | 18 | 5.9 | seven stacked strokes (G17), 15 times |
| G156 | 59 | 34 | 18.6 | three short strokes (G3), 22 times |
| G700 | 59 | 31 | 15.7 | three long strokes (G33), 18 times |
| G900 | 58 | 24 | 11.1 | three short strokes (G3), 11 times |
| G220 (fish) | 219 | 82 | 30.8 | two long strokes (G32), 40 times |

**Pairing specificity.** Mutual information between a numeral and the sign after it, against numerals permuted among the same pairs (2,000 permutations):

| Numerals | Pairs | Observed | Permuted | p |
|---|---|---|---|---|
| All | 1,138 | 1.881 bits | 0.923 bits | 0.0005 |
| Short strokes | 677 | 1.124 | 0.523 | 0.0005 |
| Long strokes | 435 | 1.071 | 0.498 | 0.0005 |
| Stacked strokes | 137 | 1.934 | 0.965 | 0.0005 |

**Reading:** each counted sign tends to take its own number. That fits fixed expressions (titles, names, calendar or ritual terms, such as Parpola's proposed "seven" + star readings) better than free counting of goods. It does not rule out standard ration sizes, which would also fix the count.

The overall pairing specificity and the commonest pairing (G32 then G220) were frozen and committed before holdout testing.

## 7. Descriptive checks re-run with the data fixes

`scripts/descriptive_checks.py`, after removing line breaks and excluding unreadable signs:

| Corpus | Texts | Signs | Block entropy N=2 | Within-text shuffle | Bigram gain | Shuffled gain | Most frequent sign at end |
|---|---|---|---|---|---|---|---|
| indus_website | 2,521 | 576 | 1.115 | 1.246 | 1.35 bits (5/5) | −0.02 (1/5) | G740: 68% vs 24% |
| cisi_base | 98 | 139 | 1.124 | 1.185 | 0.49 bits (5/5) | −0.68 (0/5) | P324: 85% vs 19% |
| cisi_allograph | 98 | 222 | 1.067 | 1.099 | −0.10 (1/5) | −0.75 (0/5) | (too sparse) |

Conclusions of sections 1 and 2 are unchanged.

## 8. Word units (Phase 3, item 3; exploration split)

**Signs bind to their neighbours.** Mutual information between adjacent signs is 3.31 bits, against 2.32 bits in within-text shuffles (200 shuffles, maximum 2.36).

**Duplicates had to go first.** Many apparent units were one inscription repeated (one nine-sign text occurs 10 times). With exact duplicates removed (1,523 distinct exploration texts), 68 two-sign units and 12 three-sign units occur 10+ times and above every one of 100 within-text shuffles.

**Units sit in fixed slots.** Examples (uses in distinct texts; start / middle / end):

| Unit | Uses | Start | Middle | End |
|---|---|---|---|---|
| G817 G2 | 69 | 67 | 2 | 0 |
| G920 G60 G741 | 19 | 19 | 0 | 0 |
| G692 G60 | 22 | 19 | 3 | 0 |
| G590 G390 G740 | 28 | 2 | 1 | 25 |
| G705 G33 G520 | 17 | 1 | 2 | 14 |
| G70 G520 | 12 | 0 | 1 | 11 |

Inscriptions look built from formulas: opening phrases, a middle, and closing phrases (several of which end in the jar sign).

## 9. Context: sites, animals, objects (Phase 3, item 6; exploration split)

Every sign used in 20+ texts was tested against sites, object types and motifs (animal on the seal), with 1,000 label permutations each.

**Duplicates again changed the answer.** With duplicates kept, 72 of 910 links reached p ≤ 0.002, including striking ones (G923 with elephant seals, G892 with Kalibangan, G55 with Lothal). With duplicates removed, those lost significance: they were many copies of one inscription from one place. 26 of 888 links survive at p ≤ 0.001 with duplicates removed (about 1 expected by chance).

**Confounds checked.** Most tablets come from Harappa, and tablets carry no animal, so object, site and motif are entangled:

| Link | All texts | Within the subgroup | Verdict for registration |
|---|---|---|---|
| G400 → tablets | 64% vs 24% | within Harappa: 90% vs 57%, p 0.001 | registered (within Harappa) |
| G400 → tablets, within Mohenjo-daro | | 12% vs 9%, p 0.30 | not supported there; noted |
| G741 or G390 → unicorn seals | | within seals: 78% vs 63%, p 0.001 | registered (within seals) |
| G700 → tablets, within Harappa | | 70% vs 57%, p 0.14 | dropped |

Five hypotheses (unit recurrence, opening units, closing units, G400 and tablets within Harappa, unicorn signs within seals) were frozen with duplicates removed and committed before holdout testing.
