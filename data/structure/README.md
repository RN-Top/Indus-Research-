# Structural comparison: language registry

Purpose: compare the structure of Indus inscriptions with other languages, using only structure (repetition, position, diversity), never sign-to-sound values. Pre-registered in `predictions/structure_semitic_P20_2026-11-07.json`.

## Rules for adding a language

1. Add a row to `languages.csv` with the role (`target`, `comparison` or `control`), the corpus path, the source and the licence status.
2. Set `licence_status` to `checked` only after the licence page or statement has been read, and record the evidence in `licence_evidence` (URL, page, quoted text). Unknown or "no licence stated" stays excluded.
3. Commit the registry row **before** the corpus file is read. The git commit date is the record that the language was added before any reading.
4. Corpus files are CSV with columns `text_id,units`, where `units` is space-separated. Units are graphic signs or letters as recorded in the source; no transliteration is applied.
5. Adding a language after results exist is allowed, but it gets its own dated results file. Earlier results are not rewritten.

## What the battery runs

`scripts/structure_battery.py` reads this registry and runs only rows with `licence_status = checked` and a corpus file present. It computes four features on texts of 3–8 units (F1–F4 as in P20), compares Indus to each comparison and control language, and reports:

- per-feature values for every language,
- the distance from Indus to each language,
- a null from within-text shuffles of the Indus texts (length and unit inventory kept),
- Benjamini–Hochberg correction across all languages in one run.

Languages with status `not started` are skipped and listed as skipped in the output.
