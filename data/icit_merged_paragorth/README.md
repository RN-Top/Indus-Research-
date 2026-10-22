# Fuller ICIT copy (merged Wells/ICIT corpus, via paragorth/Indus-)

- `merged-corpus-canonical.json`: 5,369 inscribed objects (this project's bundled corpus has 2,536). Copied unmodified from github.com/paragorth/Indus- (`data/derived/merged-corpus-canonical.json`, commit d62ec82d, 7 October 2026), by Parag Garg, MIT licence (`LICENSE_paragorth.txt`). SHA-256 `fcede2a98a210c884d02f3fcfdbddf18563e00ad896e44abfea4176ca7f19e01`.
- Underlying data: the ICIT database of Bryan K. Wells and Andreas Fuls (Wells/ICIT sign numbers). Cite ICIT (Fuls 2022; Wells 2011, 2015) when using it; the paragorth project notes the file was built from an older `inscriptions.csv` export.
- Fields per object: `cisi` (CISI number or "-"), `site`, `type` (e.g. SEAL:R, TAB:..., POT:T:g), `symbol` (field symbol), `material`, `complete` (Y/N), `period`, find-spot fields, and four sign sequences in reading order: `seq_raw` (as transcribed), `seq_strong`, `seq`, `seq_all` (with allograph merges of increasing strength). This project uses `seq_raw`.

## New to this project's export

`new_to_export.csv` (built by `scripts/build_new_to_export.py`): objects whose text does not occur anywhere in `data/indus_website_real_corpus.csv`, in either direction: 2,003 objects. Each has a `status`, from object identity:

| Status | Objects | How decided |
|---|---|---|
| new object (CISI not in export) | 1,518 | its CISI number is not in the export's `cisi_number` column |
| probably new (no CISI) | 270 | no CISI number (mostly Dholavira); no export object at the same site has a text of the same length within one sign |
| same object (CISI in export) | 202 | CISI number is in the export: the same object read differently. **Excluded.** |
| probable re-transcription (no CISI) | 13 | no CISI number; an export object at the same site has a text of the same length differing by one sign. **Excluded.** |

**Usable new set: 1,788 objects, 1,235 distinct texts, 1,137 with 2+ signs**, never seen by any exploration or holdout analysis here.

Caveats:
- **Not independent of ICIT**: the same project transcribed them, so tests on them are "held out from my export", not out-of-corpus.
- Only some objects are marked complete; damaged texts should be handled as in the export (the `complete` field).
- The "probably new (no CISI)" call is a heuristic.
