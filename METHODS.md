# Methods and protocol

This document is the protocol the workbench enforces. It is written so a sceptical reviewer can check every step.

## 1. Scope

The Indus script is undeciphered. The workbench makes no claim to decipher it. It tests specific, falsifiable statements about the *transcribed* sign sequences: which signs follow which, where signs sit in a text, which signs occur with which sites or objects, and which signs behave alike.

Transcriptions are themselves interpretations. Editors decide which marks are separate signs and which are variants. Results are therefore always reported with the corpus version, and the robustness check repeats them under different sign-splitting choices where data allow.

## 2. Data

| Key | Content | Sign IDs | Licence |
|---|---|---|---|
| `indus_website` | 2,543 inscriptions from 52 sites | G-numbers | Derived CSV MIT; underlying transcription under its source's terms |
| `cisi_primary` | 179 Mohenjo-daro unicorn seals | P-numbers, variants merged | MIT |
| `cisi_hierarchical` | same seals | variants split when seen 3+ times | MIT |
| `cisi_allograph` | same seals | every variant separate | MIT |

All files come from the Hugging Face dataset `joyboseroy/indus_decipher`, pinned to commit `47e8616dff4d1ff62343bd74f3eeefc4afbfd4d8`. The app shows the SHA-256 of the downloaded file; quote it with every result.

**Known limitations.** The G-number sign list of the large corpus is not identified by its publisher, so its signs can't yet be matched to Mahadevan (1977) or Parpola (1994) numbers. The large corpus is a website transcription, not a peer-reviewed edition. Results should be repeated on a scholarly corpus such as ICIT (Wells and Fuls) before publication.

### Cleaning

- Texts marked damaged are excluded by default (switchable).
- Exact duplicate texts can be removed (switchable). Sets of identical tokens, such as the Harappa miniature tablets, otherwise inflate counts.
- Every exclusion is logged with its reason and shown in the app.
- Orientation: rows marked R-L are used as stored and rows marked L-R are reversed, following the dataset card. This is a storage convention, not a claim about reading direction.

## 3. The locked holdout

Each text is assigned to *exploration* (80%) or *holdout* (20%) by hashing its ID with a fixed salt (`indus-workbench-holdout-v1`). The split cannot be tuned, is identical for every user, and doesn't change when texts are added. Descriptive pages and the Hypothesis Lab's exploration step use only the exploration split. The Corpus Browser hides holdout texts by default.

## 4. Controls

**Negative controls (null models):**

| Null model | Keeps | Destroys |
|---|---|---|
| Shuffle within texts | each text's signs and length | order inside texts |
| Shuffle across corpus | sign frequencies, text lengths | which signs share a text, order |
| Uniform random | alphabet, text lengths | everything else |

**Positive controls:**
- A synthetic first-order Markov "language" with known structure, matched to the corpus's size, alphabet and text lengths.
- Planted patterns: a known A→B pair inserted into shuffled texts at a chosen rate, to measure each test's power.
- Optionally, a user-supplied text in a known writing system, cut to the same length distribution.

**Baseline:** for sequence prediction, an order-free unigram model.

## 5. Hypothesis tests

| Kind | Statistic | Null distribution |
|---|---|---|
| precedes | count of A immediately followed by B | shuffle within texts |
| position | share of A's tokens at text start (or end), texts of 2+ signs | shuffle within texts |
| association | share of texts containing A that have field = value | permute field labels across texts |
| class_cohesion | mean cosine similarity of the signs' following-sign profiles | random frequency-matched sign sets |

All tests are one-sided (prediction: greater than null) permutation tests with p = (1 + #null ≥ observed) / (permutations + 1). Default 2,000 permutations, fixed seed per hypothesis. Each result reports the observed statistic, null mean, effect ratio, p, and how many occurrences it rests on. Results resting on fewer than 5 occurrences are reported as inconclusive.

The test suite checks that these tests find planted patterns, do not find absent ones, and keep the false-positive rate near α on pure noise.

## 6. Pre-registration and confirmation

1. Explore on the exploration split.
2. Freeze the hypothesis. The file records the claim, parameters, α, corpus, seed and a SHA-256 fingerprint of those fields.
3. Commit the file to `hypotheses/`. The git commit and GitHub's history are the public timestamp.
4. Run confirmation once on the holdout. Files whose fingerprint no longer matches are refused.
5. p-values across all registered hypotheses are adjusted with Benjamini-Hochberg. A claim is **supported** only if q < α and it rests on 5+ occurrences.
6. Commit the results file to `results/`, including null and inconclusive outcomes. Publishing failures is part of the protocol.

## 7. Replication target

Rao (2010) and Rao et al. (2009) reported that Indus block entropy lies between random and rigid sequences, near natural-language scripts. The Entropy Replication page recomputes this with the same normalisation (logarithm base L). The corpus differs from theirs (Mahadevan 1977), so absolute values will differ; the comparison with controls is what replicates. Sproat (2010, 2014) argued that such entropy profiles don't by themselves distinguish writing from non-linguistic symbol systems, and the app says so.

## 8. Reproducibility

- Data pinned by commit and verified by SHA-256.
- Code versioned in git; tag each release and archive it on Zenodo for a DOI.
- All randomness seeded.
- `python -m pytest` runs the test suite; GitHub Actions runs it on every push.
