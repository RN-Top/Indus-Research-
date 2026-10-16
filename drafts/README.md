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
| `H-foreign-closer.DRAFT.json` | Inscriptions found abroad contain a closer less often than home texts of the same object type | `results/sign_travel_water.md` D; scoped in `results/foreign_seals_scoping.md`. **Blocked**: needs about 15 or more newly transcribed abroad texts and a new hypothesis kind |
| `H-headless-first-rare.DRAFT.json` | In inscriptions without a heading, the first sign is rare (5 or fewer uses in exploration, or unseen) more often than interior middle signs | `results/rare_signs_as_names_scouting.md`, angle 2. Needs a new hypothesis kind (`first_sign_rarity`) with controls, and Erin's go-ahead |
