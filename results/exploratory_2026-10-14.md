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
