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
