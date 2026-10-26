# Indus Script Workbench

A research tool for testing hypotheses about the undeciphered Indus script, built to survive expert scrutiny.

**Preprints:** Toppe, E. R. (2026). *Pre-registered cross-site test of the positional structure of Indus inscriptions.* Zenodo. [doi:10.5281/zenodo.23404360](https://doi.org/10.5281/zenodo.23404360); version 1.1 (adds related work): [doi:10.5281/zenodo.23564010](https://doi.org/10.5281/zenodo.23564010) (not peer-reviewed).
Toppe, E. R. (2026). *Inscription predicts image on the Mohenjo-daro copper tablets.* Zenodo. [doi:10.5281/zenodo.23503497](https://doi.org/10.5281/zenodo.23503497); version 1.1 (adds related work): [doi:10.5281/zenodo.23563601](https://doi.org/10.5281/zenodo.23563601) (not peer-reviewed).
Toppe, E. R. (2026). *The two layers of an Indus seal: held-out tests of text, image and form.* Zenodo. [doi:10.5281/zenodo.23549063](https://doi.org/10.5281/zenodo.23549063); version 1.1 (adds the held-out restorer test, corrected references): [doi:10.5281/zenodo.23549346](https://doi.org/10.5281/zenodo.23549346); version 1.2 (adds the held-out top-mark test and the second reader): [doi:10.5281/zenodo.23552468](https://doi.org/10.5281/zenodo.23552468) (not peer-reviewed).
Toppe, E. R. (2026). *An inside mark stops the Indus fish sign from being counted: a pre-registered test on held-out inscriptions.* Zenodo. [doi:10.5281/zenodo.23607038](https://doi.org/10.5281/zenodo.23607038) (not peer-reviewed).
Toppe, E. R. (2026). *Indus signs written abroad combine in ways the home script does not: two pre-registered tests on inscriptions from the Gulf and Mesopotamia.* Zenodo. [doi:10.5281/zenodo.23675897](https://doi.org/10.5281/zenodo.23675897) (not peer-reviewed).

**This app does not decipher the Indus script.** It measures patterns in transcribed sign sequences and tests each one against controls, so that any claim made with it can be checked, repeated and, if wrong, shown to be wrong.

## What it does

| Page | Purpose |
|---|---|
| Home | Choose the corpus, see its version fingerprint, exclusions and the holdout split |
| Corpus Browser | Search by site, object type and sign pattern (`^` start, `$` end, `*` any sign, `...` any run); holdout hidden by default |
| Sign Statistics | Frequencies, text lengths, positional preferences beside a shuffled control |
| Entropy Replication | Repeats Rao (2010) block entropy against negative and positive controls |
| Sequence Model | Bigram vs unigram baseline, cross-validated, with a shuffled control |
| Hypothesis Lab | Explore → register (timestamped, fingerprinted) → confirm once on the locked holdout |
| Reading Tester | Tests a proposed decipherment key against keys made by shuffling its own values |
| Robustness | Re-runs a hypothesis under every data-cleaning choice and sign-splitting scheme |
| Methods Report | Downloadable record of data version, settings, controls and results |
| References | Bibliography (also in `references.bib`) |
| Geographic Context | Map of inscription sites and the dried Ghaggar-Hakra river; river and water words that may predate Sanskrit, with sources. Context and hypothesis only, kept separate from the tested results |
| Inscription Structure | Opener → content → closer layout: which signs open and close, how well the layout transfers across sites, and agreement with the independent CISI transcription. Exploratory; credits prior work by Wells and Fuls |
| Find-spot Map | Where inscriptions were found, home and abroad, over schematic ancient waterways and the Bronze Age sea and overland routes; tap a site for its counts and closer share. Exploratory; also opens on its own at `static/findspot_map.html` |
| Sign Functions | What particular opening and closing signs seem to do (two heading families; generic and specific closers), with sign pictures and whether each finding is confirmed on the holdout or exploratory |

## Rigour built in

- **Negative controls:** within-text shuffle, corpus-wide shuffle, uniform random signs.
- **Positive controls:** synthetic grammar with known structure; planted patterns to measure test power; optional uploaded text in a known script.
- **Baseline:** order-free unigram model.
- **Locked holdout:** 20% of texts, assigned by hash, used once for confirmation.
- **Pre-registration:** hypotheses frozen with a SHA-256 fingerprint and committed to `hypotheses/` before testing.
- **Multiple-testing correction:** Benjamini-Hochberg across all registered hypotheses.
- **Provenance:** pinned data version, file fingerprint, every exclusion logged with a reason.
- **Tests:** `python -m pytest` checks that the methods find planted patterns, ignore absent ones and keep false positives near α.

Full protocol: [METHODS.md](METHODS.md).

## Data

Bundled in `data/` from [`joyboseroy/indus_decipher`](https://huggingface.co/datasets/joyboseroy/indus_decipher) on Hugging Face (MIT), and checked against a recorded SHA-256 every time the app loads them. First exploratory results are in [`results/exploratory_2026-10-14.md`](results/exploratory_2026-10-14.md). See METHODS.md for sources, licences and known limitations. Results should be repeated on a scholarly corpus such as the Interactive Corpus of Indus Texts (Wells and Fuls) before publication.

## Run it

Deploy free on [Streamlit Community Cloud](https://share.streamlit.io): sign in with GitHub, choose this repository, main file `Home.py`.

Locally:

```bash
pip install -r requirements.txt
streamlit run Home.py
python -m pytest
```

## Registering a hypothesis

1. Explore it in the Hypothesis Lab.
2. Freeze it and download the JSON file.
3. Upload the file to `hypotheses/` in this repository and commit.
4. Run the confirmatory test once; commit the results file to `results/`, whatever the outcome.

## Licence and citation

Code: MIT. Data: see METHODS.md. Fonts in `static/`: CC BY-SA 4.0, see `static/FONT_LICENSE.md`. Cite using [CITATION.cff](CITATION.cff).
