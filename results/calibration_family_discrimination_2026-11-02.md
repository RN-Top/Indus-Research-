# Calibration: family signal after Indus-like re-encoding (first run, 2 Nov 2026)

Script: `scripts/calibration_family_discrimination.py` (not committed).
Controls: Tamil-Brahmi (Dravidian, 109 texts) and Prakrit (Indo-Aryan, 167 texts) from `data/`.
Encoding: each text cut to 5 tokens; a share p of word tokens replaced by a random logogram ID (one per stem, no phonetic value); other words written as characters with no word breaks.
Classifier: character-bigram naive Bayes, 5-fold CV. Null: 200 label shuffles.

## Result (raw texts, first run)

| logogram share p | n | accuracy | majority baseline | shuffled null (mean) | one-sided p |
|---|---|---|---|---|---|
| 0.0 | 276 | 0.884 | 0.605 | 0.524 | <0.005 |
| 0.3 | 267 | 0.884 | 0.603 | 0.523 | <0.005 |
| 0.6 | 261 | 0.789 | 0.613 | 0.510 | <0.005 |
| 0.9 | 255 | 0.639 | 0.620 | 0.486 | <0.005 |

## Result (diacritics folded to ASCII, check on spelling convention)

| p | accuracy | null mean |
|---|---|---|
| 0.0 | 0.855 | 0.529 |
| 0.3 | 0.869 | 0.523 |
| 0.6 | 0.789 | 0.511 |
| 0.9 | 0.667 | 0.485 |

Folding leaves the pattern unchanged, so the separation is not mainly a transliteration artefact.

## What this does NOT show

- **Genre confound, not yet ruled out.** Prakrit texts are dominated by donative formulae ("namo bhagavato ... raño"); Tamil texts are cave donation records. A classifier can separate them by formula vocabulary without any language signal. The test here cannot distinguish the two.
- **Logogram IDs are per stem.** At high p, the classifier can match stems that repeat within a corpus. That is vocabulary memorisation, not cognacy.
- **No stem lists used.** This is not the phonetic-prior matcher from Luo et al. 2021 and does not test language closeness.
- **Five-token windows are a guess** at the Indus length distribution, not a fitted match.

## Reading

Short, unsegmented, partly logographic strings still carry separable structure. That is the weak half of the calibration question. The strong half (whether a cognate matcher can separate *language families* on these strings) is untested.

## Next step to make it a real control

Match genre. Re-run using only the name and title roles (PERSONAL_NAME, TITLE_OR_OCCUPATION) from both corpora, and drop formula tokens (namo, bhagavato, dhammam, and similar) by a fixed list. If accuracy stays well above the null, the family signal is not only genre. Then add the cognate matcher on the stem lists once they exist.
