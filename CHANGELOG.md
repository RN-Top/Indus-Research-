# Changelog

## Unreleased
- Added `data/fuls_sign_list.csv`, the 713-sign list from Fuls (2022) Table 2.6, and a test that every corpus sign is on it (all 11,280 tokens pass).

## 0.1.0 (2026-10-14)
- Merged the first version of the app: reading-key tester with shuffled-key null model, sign-pattern search, bibliography. Its synthetic sample data was removed.
- Bundled the full corpus and CISI variant file with SHA-256 checks; added base-sign CISI view, P000 exclusion option, ida fonts, first exploratory results.
- First release: corpus loading with provenance, locked holdout, controls, entropy replication, sequence model, hypothesis registry with permutation tests and Benjamini-Hochberg correction, robustness grid, methods report.
- Data pinned to joyboseroy/indus_decipher commit 47e8616d.
