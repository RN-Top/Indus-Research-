# How new is this? Prior work on Indus text structure and on testing it

*Literature note, 15 October 2026. No data or tests were touched. The search was limited to what is reachable online plus the papers in the Academia.edu bundle Erin downloaded; a specialist may know of more.*

## Short answer

- **The structure is established prior work.** Initial signs, terminal markers, post-terminal markers and the "initial cluster terminal marker" were described by Bryan Wells (2006, 2011) and charted sign by sign by Andreas Fuls (2013). Beginnings and endings of texts were also analysed statistically by Yadav et al. (2010).
- **The individual testing tools are not new either.** Held-out test sets, cross-validation and random or shuffled comparisons have been used on the Indus script since 2009 (Rao et al. 2009; Yadav et al. 2010). A 2026 preprint uses within-text shuffles, held-out splits and a list of methods fixed before scoring (Raghavendra 2026).
- **What appears uncommon, and possibly new, is the combination** applied to a *structural* claim:
  - a rule written down and timestamped publicly before testing;
  - roles learned at one site and tested on other sites;
  - a locked holdout used once;
  - a shuffle null;
  - multiple-testing correction across every test ever run.
  - This search found no Indus study doing all of these together. That is "not found", not "proven first".

## 1. What Fuls's own papers do

**Fuls, "Positional Analysis of Indus Signs" (*Voprosy epigrafiki* 7, 2013):**
- **Data:** the ICIT corpus, with duplicates (the "TAB effect") and multi-line texts removed, leaving 2,474 complete, distinct texts.
- **Method:** each sign's positions are stretched to a standard length of 10 and drawn as weighted histograms.
- **Claims:**
  - initial signs (692, 817, 820, 861, 921 and others), confirmed as distinct from look-alike signs;
  - terminal markers (after Wells 2006, pp. 198–200), about half strongly final, with sign 740 the typical one;
  - post-terminal signs 90, 400, 621 and 679, appended after terminal markers;
  - early-medial signs 2 and 60 ("Initial Cluster Terminal Markers", Wells), which close the opening cluster;
  - further mid- and late-medial classes; and signs spread evenly over all positions, as candidate syllables.
- **Statistics:** **descriptive only.** There is no held-out data, no shuffle or permutation comparison, no significance test and no pre-registration.

**Fuls, "Classifying Undeciphered Writing Systems" (*Historische Sprachforschung* 128, 2015):**
- Relates how often signs are used, and word length, to the type of writing system (fitted curves across known scripts).
- No positional or slot analysis, and no held-out testing.

**Fuls, "Comparison of Linear Elamite and Indus Writing"** (in the bundle; only searched, not read in full): no holdout, permutation or significance terms were found in it.

## 2. Other statistical work on Indus structure

| Study | What it did | Held-out data | Shuffle or random comparison | Rule set in advance | Learn at one site, test at another |
|---|---|---|---|---|---|
| Rao et al. 2009, *PNAS* (Markov model) | Sign-order model; filling in damaged signs; showed West Asian seals are "ordered differently" | Yes (cross-validation) | A random baseline | No | Partly: Indus Valley texts against West Asian texts, as a likelihood comparison |
| Yadav et al. 2010, *PLoS ONE* (n-grams) | 82 signs make up 80% of text beginnings but only 23 make up 80% of endings; splitting texts into segments | Yes (held-out portion) | A random sequence | No | No |
| Wells 2006/2011; Fuls 2013 | Positional classes of signs | No | No | No | No |
| Tiwari 2026 (NLP4DH) | Entropy, divergence and a neural sequence model; "not easily explained by random generation" | Not stated in the abstract | Some random baseline | No | No |
| Raghavendra 2026 (arXiv) | Shows a made-up non-language symbol system reproduces Indus-like statistics, including the beginning/ending contrast | Yes (grouped 70/15/15 split) | Yes, within-text shuffles | Partly: methods list closed before scoring | Partly: an "outpost" test against core strings |
| joyboseroy/indus_decipher (GitHub, 2026; our original data source) | Toolkit: shuffle controls, cross-validation, cross-site stability of sign substitutions | Cross-validation | Yes, four shuffle types | No | Cross-site overlap, described as untested |
| **This project** | Opener → middle → closer order of whole texts | **Locked 20% holdout, used once** | **Yes, within-text shuffle** | **Yes: frozen and timestamped in a public repository before the run** | **Yes: roles from Mohenjo-daro only, tested on all other sites** |

## 3. Honest positioning

- **Do not claim:** that the opener–middle–closer structure is a discovery, or that held-out or shuffle testing of Indus texts is new.
- **Can fairly say:** "We provide a pre-registered, single-use holdout confirmation that the positional structure described by Wells and Fuls transfers across Indus sites: roles learned from Mohenjo-daro alone order 76% of unseen texts from other sites, against 27% under within-text shuffling. It also agrees with an independent transcription (CISI). As far as we found, this combination of safeguards has not previously been applied to a structural claim about the Indus script."
- **Important caveat from Raghavendra (2026):** positional regularities like these are **not evidence of language**. A non-linguistic symbol system can produce them too. The result supports a stable *structure*, which is all it claims.

## Sources

- Fuls, A. (2013). "Positional Analysis of Indus Signs." *Voprosy epigrafiki* 7(1): 253ff. (PDF in Erin's Academia bundle.)
- Fuls, A. (2015 [2016]). "Classifying Undeciphered Writing Systems." *Historische Sprachforschung* 128: 42–58. (PDF in bundle.)
- Wells, B. K. (2006). *Epigraphic Approaches to Indus Writing.* PhD dissertation, Harvard. Published 2011, Oxbow.
- Rao, R. P. N. et al. (2009). "A Markov model of the Indus script." *PNAS* 106(33). [doi:10.1073/pnas.0906237106](https://www.pnas.org/doi/full/10.1073/pnas.0906237106); summary: [UW News](https://www.washington.edu/news/2009/08/03/computers-unlock-more-secrets-of-the-mysterious-indus-valley-script/)
- Yadav, N. et al. (2010). "Statistical Analysis of the Indus Script Using n-Grams." *PLoS ONE* 5(3): e9506. [PMC2841631](https://pmc.ncbi.nlm.nih.gov/articles/PMC2841631/)
- Tiwari, T. (2026). "Statistical Structure in Indus Sign Sequences." NLP4DH. [ACL Anthology](https://aclanthology.org/2026.nlp4dh-1.28/)
- Raghavendra, N. (2026). "On the Non-Specificity of Statistical Measures Used in Script Decipherment." [arXiv:2608.02999](https://arxiv.org/html/2608.02999)
- joyboseroy/indus_decipher (2026). [GitHub](https://github.com/joyboseroy/indus_decipher)
