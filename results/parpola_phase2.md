# Phase 2: testing Parpola's readings, proposed design (NOT YET REGISTERED)

*14 October 2026. Merged to main on 14 October; status: **unverified, awaiting approval.** Nothing below has been run on the holdout. All figures come from the exploration split (1,523 distinct texts; damaged and unidentified excluded; duplicates removed).*

## 1. The readings, checked against the sources

Every reading in `data/parpola_readings.csv` was re-checked against Parpola's two free papers:

- [Parpola 2005, ICES lecture](https://www.harappa.com/sites/default/files/pdf/indusscript(2).pdf)
- [Parpola 2009, *SCRIPTA* 1](https://www.harappa.com/sites/default/files/pdf/script-indus-parpola.pdf)

Page numbers are the printed page numbers. Corrections to the paused draft:

- **Malformed row fixed.** The row for G32 had a comma inside an unquoted field.
- **Page numbers corrected.** Fish (2005) is pp. 53–54, not 52–54. Intersecting circles is 2009 pp. 56–57.
- ***nīr* "water" is implied, not stated.** The 2005 lecture reads the two-wavy-lines sign only inside the phrase *nīr-k-kaṇṭi* ("water overseer"), together with the eye sign (p. 61, n. 52). It is now marked "implied".
- **Six + fish has two readings.** In 2009, Parpola prefers *aṟu* "to cut" + *vāy* over "six" for the Pleiades name (pp. 45, 68). The 2005 lecture reads *aṟu-mīn* "six stars" (p. 54). Both are recorded.
- **Parpola's own confidence is now recorded.** He calls the crab (*kōḷ*), hind leg (*tāḷ*) and scorpion (*tēḷ*) readings tentative.

## 2. Which of our signs are his signs

Our corpus does not use Parpola's sign numbers, so each match was checked two ways: by drawing the sign, and against seals Parpola names in his papers.

| Parpola's sign | Ours | Status | Evidence |
|---|---|---|---|
| plain fish, *mīn* | G220 | verified | shape; follows six and seven on the seals below |
| fish with roof sign, *mai* | G235 | verified | shape; CISI crosswalk 13/13 |
| two long strokes, *veḷ* | G32 | verified | shape; crosswalk 22/23 |
| six strokes, *aṟu* | G16 (G6) | verified | Harappa seal H-1028 reads exactly six + fish |
| seven strokes, *eḻu* | G17 (G7, G27) | verified | Parpola: seven + fish "forms the entire inscription in one large seal from Harappa." Our Harappa seal H-9 is exactly G17 G220. |
| intersecting circles, *muruku* | G845 | verified | shape |
| two wavy lines, *nīr* | G927 | verified | shape |
| hind leg, *tāḷ* | G278 (G279) | probable | M-1690 opens G278 G220, hind leg + fish; M-71 has G279. Both seals are in his Fig. 15. |
| crab, *kōḷ* | G140? | uncertain | Shape unclear. He reports crab + fish 3 times; G140 is never followed by fish here. |
| fig, *vaṭa* | G786? or G415? | candidate only | He names M-172 as fig + fish, and our M-172 has G786 before fish. But G786 occurs twice in the whole corpus, while G415 (112 uses, 61 before fish) also looks like a branch. A specialist with Parpola's 1994 sign list is needed to settle this. |
| squirrel, scorpion, oval, dot in circle, crab-in-fig | none | not mapped | no confident match |

**Seven signs verified, one probable, two unresolved.**

## 3. The central problem: circularity

Parpola built his readings by studying the whole corpus, including the texts in our holdout. A pattern he relied on cannot then be counted as a successful prediction. For example, two long strokes are often followed by fish (our confirmed H6); he saw that too. A within-corpus test can therefore **falsify** a reading (show it is inconsistent with the texts) but cannot **confirm a decipherment**. Only evidence he could not have seen can do that: new inscriptions, a bilingual, or an independently compiled Dravidian word list.

So the proposed tests are **risky consistency tests**. Each one takes a consequence of his readings that he did not, as far as his papers show, check or report, and that could fail.

## 4. Proposed pre-registered tests

Both tests use the same rules as the other confirmatory tests:

- one-sided permutation test with 2,000 permutations;
- seed 12345, α = 0.05;
- Benjamini-Hochberg correction across all confirmatory tests ever run;
- minimum support of 5;
- data settings `{drop_damaged: true, dedupe: true, drop_unidentified: true}`;
- run once on the locked holdout of 395 distinct texts.

### P1. Star names prefer six and seven

- **Derived from:** his readings of six + fish as the Pleiades and seven + fish as Ursa Major (2005 p. 54). These rest on the Old Tamil vocabulary of star names, not on sign counts.
- **Prediction:** if numeral + fish spells star names, then among numerals directly followed by a non-numeral sign, six and seven make up a larger share before plain fish than before other signs. In ordinary counting, any number can precede anything.
- **Kind:** `pair_share` (see section 6).
- **Numerals:** short G1–G7; stacked G13–G19, G27, G28, G29, G55; long G31, G32, G33, G35.
- **Subset (six and seven):** G6, G16, G7, G17, G27.
- **Target:** G220.
- **Statistic:** share of the subset before fish, minus its share before other signs.
- **Null:** which following sign is fish, permuted among the numeral pairs.
- **Exploration result:** 5 of 73 numerals before fish are six or seven (6.8%), against 53 of 865 before other signs (6.1%). Difference +0.7 points, **p = 0.48**. No effect.
- **Power:** the holdout has about a quarter as many pairs. A "not supported" result would be weak evidence against the reading, but it would be the result we committed to.

### P2. The roof-fish sign behaves like the fish sign

- **Derived from:** his reading of roof + fish as *mai-mīn* "black star" (Saturn), a fish-star compound (2005 pp. 54–55).
- **Prediction:** G235 should be followed by the same signs as plain fish G220, more than random sign pairs of matched frequency are.
- **Kind:** `class_cohesion` (already in the app), on signs G220 and G235.
- **Exploration result:** cosine 0.49, against 0.24 for random pairs, **p = 0.12**. Pointing the right way, but not significant.
- **Caveat:** any theory in which G235 is a fish variant predicts this. Passing would not single out Dravidian, but failing would count against the reading.

### Not proposed, and why

- **Two long strokes + fish (*veḷ-mīn*):** already confirmed as H6, and Parpola saw it first. It is consistent with his reading, but not an independent test.
- **Water + eye (*nīr-k-kaṇṭi*):** the water sign occurs in only 6 texts in the exploration split, always before the jar sign. There is no eye sign next to it in this transcription.
- **Fig, crab and hind leg compounds:** the sign matches are not secure enough, and hind leg occurs only 3 times.

## 5. Honest expectation

On the exploration data, **neither prediction shows up clearly**: P1 shows no effect, and P2 is suggestive but not significant. Under the protocol we can still register both and report whatever the holdout gives. The alternatives are to record them as exploratory nulls and keep the holdout unspent.

- **Recommended: register both.** The holdout result is the only one anyone else will trust, and reporting failures is the point. Adding two tests to the correction family costs the existing results very little.
- **The alternative** is reasonable if the aim is to save the holdout for stronger hypotheses, given the low power.

## 6. Code changes on this branch

- **New test kind `pair_share`** in `indus_workbench/hypotheses.py`. It has a positive control (finds a planted preference for six and seven, p < 0.01) and a negative control (no preference, not flagged) in `tests/test_core.py`. All 41 tests pass.
- **Reading Tester "runs" mode:** reads every run of 2 or more consecutive signs that have values, for partial keys like Parpola's. This was already on the branch.
- **Cleaned data files:** `data/parpola_readings.csv` and `data/parpola_lexicon.csv`, with sources and pages on every row. Two lexicon entries were added: *vaṭamīn* and *kaṇkāṇi*.
