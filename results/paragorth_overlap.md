# Overlap with the paragorth/Indus- project

*20 October 2026. Repository github.com/paragorth/Indus- (MIT licence; last commit 7 October 2026), with a Zenodo reproduction package, DOI 10.5281/zenodo.21497936 (not opened). A large computational study of the same corpus with frozen pre-registrations, 100+ logged strategies and two paper drafts (`papers/paper-A-heterogeneity.md`, `papers/paper-B-slot-grammar.md`). Read for overlap, not re-run. Its strategy numbers are cited as S-numbers.*

## The language-or-marks question: already run, undecidable

- **S363:** an 18-statistic battery against heraldry, khipu, Ur III seal legends, Proto-Elamite, Latin and Linear B. The nearest system is Proto-Elamite (accounting); heraldry fails (it closes the start, Indus closes the end).
- **S-DARK-32.1 to 32.3:** leave-one-corpus-out classifiers over 16–20 reference corpora.
  - Accuracy was at chance without numeral features.
  - **An order-2 Markov chain fitted to Indus gets the same class as Indus in every run**, so the class label carries no information.
  - Their verdict: "the typology is not decidable from this battery".
- **S-DARK-53.2:** on frequency statistics, the identifier slot sits nearer designed codes than name stocks.

**Decision for this project:** not repeated. Our own calibration rule (a measure counts only if it separates known classes and fails on surrogates) is exactly what their control failed. A rerun with the same corpora would loop.

## Overlap with this project's results

| This project | paragorth | Note |
|---|---|---|
| Copper tablets: text predicts image (held-out, `copper_image_test.md`; preprint 2) | S56: one dominant text per motif, **but some texts cross motifs** | Cite; our held-out 16/18 is consistent with "dominant", not "always" |
| Seal text independent of animal (`emblem_scouting.md`) | S167(a): animal × closer independent (P 0.38) | Cite |
| Frame: opener / middle / closer (preprint 1) | `GRAMMAR.md`, Paper B "slot grammar" with out-of-sample validation | **Must be cited in preprint 1 v1.1**; their Zenodo DOI predates ours |
| Count-like vs fixed numbers (`number_system_scouting.md`) | S23: counted signs vs fixed numbers (W585 always 7) | Same finding; cite |
| Rare first signs / names | S194–195: seal "name cores" recur on copper and moulded tablets at the same site (23 vs 10.9 expected) | Related; complementary |
| Repetition of whole texts on tablets | S363 residue: whole texts repeat more than a bigram model predicts | Matches our batch finding in `context_scouting.md` |

## Action

Add a citation to this repository and its Zenodo package to both preprints (v1.1), and to the README's related work.
