# Genre-matched calibration (2 Nov 2026, local, not committed)

Script: `scripts/calibration_genre_matched.py`.
Texts: name and title roles only (PERSONAL_NAME, TITLE_OR_OCCUPATION). Formula stems removed by a data rule: any stem in >= 10 texts across both corpora. Removed stems: kaṁdasiri, mahāraja, mahārāja, mahāsenāpati, mahātalavara, mahātalavari, rāja, sirivirapurisadata, vāsiṭhīputa.
Kept: 235 texts (Tamil 94, Prakrit 141). Window 5 tokens. Same encoding and classifier as the first run.

## Result

| logogram share p | n | accuracy | majority | shuffled null | one-sided p |
|---|---|---|---|---|---|
| 0.0 | 235 | 0.847 | 0.600 | 0.524 | <0.005 |
| 0.3 | 208 | 0.822 | 0.601 | 0.521 | <0.005 |
| 0.6 | 183 | 0.732 | 0.623 | 0.505 | <0.005 |
| 0.9 | 166 | 0.639 | 0.620 | 0.510 | 0.005 |

The separation survives genre matching. The first run's 88% was not mainly formula vocabulary.

## Where the signal comes from (feature check)

Word-final characters in the name and title words:

- Tamil (207 words): final "n" in 117 (56%), mostly the bigram "-an" (104). Other endings: -i, -a, -y.
- Prakrit (829 words): final "a" in 587 (71%). Common bigrams: "-sa" (390, the genitive of patronymics), "-ya", "-no", "-na".

So the classifier is mostly reading case endings: Tamil -an against Prakrit -a/-sa. These are real grammatical markers, so this is a morphological family signal, not a leak. It is still a narrow one. It depends on endings surviving in the text.

## Implication for Indus

Indus texts are short and mostly names, titles and numerals, and endings are the first thing a logo-syllabic script loses. The drop at p = 0.9 (64%) is what that looks like. A cognate matcher would have to find family signal below the ending level, and this test does not show that is possible.

## Caveats

- The Prakrit suffix split came from a different tagging agent than the Tamil one (per `data/prakrit_eiad/README` note), so the two suffix counts are not strictly comparable. The surface endings compared here are taken from the raw forms, which avoids that problem.
- Small samples: 94 Tamil and 141 Prakrit texts after filtering.
- Still no stem lists and no cognate matcher.
