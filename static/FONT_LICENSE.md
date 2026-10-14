# ida fonts

`ida-ltr.woff2` and `ida-mono.woff2` are from **The ida fonts** v0.9.1 (pre-release) by Devajyoti Sarkar,
https://doi.org/10.5281/zenodo.7804585, licensed under Creative Commons Attribution-ShareAlike 4.0
International (https://creativecommons.org/licenses/by-sa/4.0/). Unmodified.

The fonts place Indus signs in the Unicode Private Use Area. The mapping from the corpora's sign IDs
(G-numbers, P-numbers) to these code points is not published with the data, and a test of simple
numeric offsets did not reproduce one. Glyphs are therefore not shown in the app yet: a wrong mapping
would display the wrong signs, which is worse than showing IDs. Add a verified mapping to
`data/sign_glyphs.csv` (columns: sign_id, codepoint, verified_by) to enable them.
