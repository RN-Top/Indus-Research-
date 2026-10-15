# Drafts: prepared, NOT registered

Hypothesis definitions here are **not registered** and **have not been run on the locked holdout**. They have no ID or fingerprint, and `scripts/run_confirmatory.py` only reads `hypotheses/H-*.json`, so nothing here can run by accident.

To register a draft, which needs Erin's explicit go-ahead:

1. Review it.
2. Freeze it with `hypotheses.freeze()`.
3. Save it as `hypotheses/H-<date>-<id>.json`.
4. Commit and push, which timestamps the registration.
5. Run `python scripts/run_confirmatory.py` once.

| Draft | What it tests | Source |
|---|---|---|
| `H-skeleton-transfer.DRAFT.json` | Slot order learned at Mohenjo-daro holds at every other site | `results/functional_by_site.md` D.1 and D.5; built by `scripts/prepare_skeleton_test.py` |
