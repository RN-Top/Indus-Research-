# Fuller ICIT copy (merged Wells/ICIT corpus, via paragorth/Indus-)

- `merged-corpus-canonical.json`: 5,369 inscribed objects (this project's bundled corpus has 2,536). Copied unmodified from github.com/paragorth/Indus- (`data/derived/merged-corpus-canonical.json`, commit d62ec82d, 7 October 2026), by Parag Garg, MIT licence (`LICENSE_paragorth.txt`). SHA-256 `fcede2a98a210c884d02f3fcfdbddf18563e00ad896e44abfea4176ca7f19e01`.
- Underlying data: the ICIT database of Bryan K. Wells and Andreas Fuls (Wells/ICIT sign numbers). Cite ICIT (Fuls 2022; Wells 2011, 2015) when using it; the paragorth project notes the file was built from an older `inscriptions.csv` export.
- Fields per object: `cisi` (CISI number or "-"), `site`, `type` (e.g. SEAL:R, TAB:..., POT:T:g), `symbol` (field symbol), `material`, `complete` (Y/N), `period`, find-spot fields, and four sign sequences in reading order: `seq_raw` (as transcribed), `seq_strong`, `seq`, `seq_all` (with allograph merges of increasing strength). This project uses `seq_raw`.

## New to this project's export

`new_to_export.csv` (built by `scripts/build_new_to_export.py`): objects whose text does not occur anywhere in `data/indus_website_real_corpus.csv`, in either direction. **2,003 objects, 1,400 distinct texts**, never seen by any exploration or holdout analysis here.

Caveats:
- **Not independent of ICIT**: the same project transcribed them, so tests on them are "held out from my export", not out-of-corpus.
- Only 585 of the 2,003 are marked complete; many are broken.
- Some may be the same objects as in the export, transcribed slightly differently (e.g. an allograph G856 for G861), so the count is an upper bound for truly new objects.
- 1,347 of the 2,003 differ from some export text by just one sign. For short texts that is expected by chance, but some are surely the same object read slightly differently. Without object IDs in the export (its `source_ref` is mostly "unknown") the two cases cannot yet be told apart; matching by site, object type, field symbol and length is the next step.
