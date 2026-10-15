"""Prepare (NOT register, NOT run on the holdout) the cross-site skeleton test.

Builds the hypothesis definition from results/functional_by_site.md D.1/D.5:
roles learned from Mohenjo-daro's EXPLORATION texts with the frozen rule, then
tested on texts from every other site. Writes drafts/H-skeleton-transfer.DRAFT.json.

The draft has no id or fingerprint. run_confirmatory.py only reads hypotheses/H-*.json,
so the draft cannot be run by accident. Registering means: review, freeze with
hypotheses.freeze(), save into hypotheses/, commit. Only with Erin's explicit go-ahead.

As a check, the draft is run on the EXPLORATION split only (where the roles were
learned), which should reproduce the exploratory result (about 77.6%).

    python scripts/prepare_skeleton_test.py
"""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))
from functional_skeleton import RULE, assign  # noqa: E402
from indus_workbench import data, hypotheses as hy  # noqa: E402

DATA_SETTINGS = {"drop_damaged": True, "dedupe": True, "drop_unidentified": True}


def main():
    raw, _ = data.load_raw("indus_website")
    c = data.build_corpus(raw, "indus_website", metadata=data.load_metadata("indus_website"), **DATA_SETTINGS)
    explore = data.explore_only(c).df  # the holdout is never loaded into a variable here
    md = list(explore[explore["site"] == "Mohenjo-daro"]["signs"])
    roles, table = assign(md, RULE)
    openers = sorted(x for x, r in roles.items() if r == 0)
    closers = sorted(x for x, r in roles.items() if r == 2)
    middle = sorted(x for x, r in roles.items() if r == 1)

    h = hy.new_hypothesis(
        "template_order",
        {"openers": openers, "middle": middle, "closers": closers,
         "exclude": [{"field": "site", "value": "Mohenjo-daro"}]},
        "Roles learned from Mohenjo-daro exploration texts (rule: >=15 uses in texts of 2+ signs; opener starts "
        ">=40% and >=1.8x the within-text-shuffle rate; closer ends >=50% and >=1.8x; numerals by shape; every "
        "other sign with >=15 uses is middle) put texts from all OTHER sites in slot order "
        "(opener -> middle -> closer) more often than within-text shuffling predicts.",
        author="Erin (RN-Top); prepared by Claude", data_settings=DATA_SETTINGS)
    h["status"] = "DRAFT - not registered, not frozen, not run on the holdout"
    h["role_rule"] = RULE
    h["roles_learned_from"] = "Mohenjo-daro texts of the exploration split (duplicates removed)"
    h["secondary_reported_without_test"] = "per-site conformance rates; the same test with roles learned from Harappa"

    check = hy.run_test(h, explore)
    h["exploration_check"] = {
        "note": "Run on the EXPLORATION split only, as a sanity check; not a confirmatory result.",
        "observed": check.observed, "null_mean": check.null_mean, "p": check.p_value,
        "scored_texts": check.n_support}

    out = ROOT / "drafts" / "H-skeleton-transfer.DRAFT.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(h, indent=2, ensure_ascii=False))
    print(f"openers ({len(openers)}): {openers}")
    print(f"closers ({len(closers)}): {closers}")
    print(f"middle: {len(middle)} signs (incl. {sum(1 for x in middle if x in hy_numerals())} numerals)")
    print(f"exploration check (other sites only): {check.observed:.1%} in order of {check.n_support} scored texts, "
          f"shuffled {check.null_mean:.1%}, p={check.p_value:.4f}")
    print("wrote", out.relative_to(ROOT))


def hy_numerals():
    from functional_slots import NUMERALS
    return NUMERALS


if __name__ == "__main__":
    main()
