# Indus Script Research

A Streamlit workbench for studying the Indus (Harappan) script. The script is undeciphered, and this app does not claim to read it. It makes the inscriptions searchable, measures their structure reproducibly, and tests proposed readings against a null model.

## Run locally

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements-dev.txt
streamlit run Home.py
pytest -q
```

## Layout

```
Home.py                       overview and data checks
pages/1_Corpus_Browser.py     search by sign sequence, site, object, iconography
pages/2_Sign_Lists.py         working sign list and cross-references
pages/3_Structure.py          frequency, position, n-grams, entropy vs controls
pages/4_Hypothesis_Workbench.py  key + lexicon editor, locking, null model, held-out scoring
pages/5_References.py         bibliography from references.bib
app_common.py                 Streamlit helpers shared by pages
indus/                        analysis package, no Streamlit imports
  schema.py                   pydantic models for sites, objects, texts, signs
  io.py                       CSV loading and validation
  query.py                    sign-sequence search
  stats.py                    frequency, Zipf, position, n-grams
  entropy.py                  conditional and block entropy, artificial controls
  comparison.py               loader for data/comparison corpora
  hypothesis.py               hypotheses, locking, scoring, shuffle null model
hypotheses/                   saved hypotheses (JSON), incl. two demos
data/sample/                  open sample corpus (see its README)
data/private/                 your licensed corpora, git-ignored
scripts/make_sample.py        regenerates the sample corpus
scripts/make_demo_hypotheses.py  regenerates the two demo hypotheses
tests/                        pytest
```

## Sequence search

Signs in reading order, separated by spaces: `^` start of text, `$` end of text, `*` any one sign, `...` any run of signs. Example: `^ STROKE2 FISH ... JAR $`.

## Data and licensing

The sample contains one real object (the Mohenjo-daro tiger seal, public-domain photo, signs not yet transcribed) and 300 **synthetic** texts that exist only to exercise the app. The app shows a banner whenever synthetic texts are loaded.

Copyrighted corpora (CISI photographs, Mahadevan 1977, ICIT) must not be committed. To use them, put CSVs in the same schema in `data/private/` and pick "Private corpus" in the sidebar.

## Deploy

Streamlit Community Cloud: point a new app at this repository with `Home.py` as the entry point.

## Testing a hypothesis

1. Fill in a value for each sign and a lexicon of target-language forms, each with a source.
2. Explore on the development texts. Results are marked exploratory.
3. Lock it. This records a SHA-256 fingerprint of the key, lexicon and settings and reveals the held-out texts.
4. The score is compared with keys made by shuffling the same values among signs of similar frequency. A reading that does not beat its shuffles is not evidence.

The two demos show both outcomes on the synthetic sample: "planted key" beats every shuffle; "unrelated lexicon" does not. Neither is a reading of the Indus script.

On Streamlit Community Cloud saved files are temporary. Download each hypothesis as JSON and commit it to `hypotheses/`.
