"""Scope the "texts found abroad lack a closer" lead before any registration. (SCOPING ONLY.)

Counts how many Indus-type inscriptions found outside the Indus region are in the
corpus, by split, object type and damage, and how many home texts of each object
type exist to match them. For the locked holdout it reads ONLY the site, object
type, damage flag and split columns: sign sequences are dropped before anything
else is done, so no holdout sign is ever seen. No test is run.

    python scripts/foreign_seals_scope.py
"""

import json
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from indus_workbench import data  # noqa: E402

REGIONS = {
    "Ur": "Mesopotamia", "Kish": "Mesopotamia", "Tell Umma": "Mesopotamia", "Susa": "Iran (Elam)", "Luristan": "Iran",
    "Qala'at al-Bahrain": "Gulf (Bahrain)", "Saar": "Gulf (Bahrain)", "Karzakan": "Gulf (Bahrain)",
    "Hajar": "Gulf (Bahrain)", "Ra's al-Junayz": "Gulf (Oman)", "Salut": "Gulf (Oman)",
    "Altyn Depe": "Central Asia", "Gonur Depe": "Central Asia", "Shortughai": "Central Asia",
}
META_ONLY = ["text_id", "site", "object_type", "damaged", "split"]


def frame(**settings):
    raw, _ = data.load_raw("indus_website")
    c = data.build_corpus(raw, "indus_website", metadata=data.load_metadata("indus_website"), **settings)
    return c.df[[k for k in META_ONLY if k in c.df.columns]].copy()  # sign columns dropped here


def main():
    clean = frame(drop_damaged=True, dedupe=True, drop_unidentified=True)
    every = frame(drop_damaged=False, dedupe=False, drop_unidentified=False)
    known = sorted(set(every["site"]))
    abroad_sites = [s for s in known if s in REGIONS]
    print("All sites in the corpus:", len(known))
    print("Sites treated as abroad:", abroad_sites)
    out = {"abroad_sites": {s: REGIONS[s] for s in abroad_sites}}

    for label, df in [("analysis settings (damaged dropped, duplicates removed)", clean),
                      ("every record (damaged and duplicates kept)", every)]:
        ab = df[df["site"].isin(REGIONS)]
        t = ab.groupby(["split", "object_type"]).size().unstack(fill_value=0)
        print(f"\n== Abroad texts, {label}: {len(ab)} ==")
        print(t.to_string())
        print("   by region:", ab["site"].map(REGIONS).value_counts().to_dict())
        out[label] = dict(total=len(ab), by_split=ab["split"].value_counts().to_dict(),
                          by_split_object={f"{a}|{b}": int(v) for (a, b), v in t.stack().items() if v},
                          by_region=ab["site"].map(REGIONS).value_counts().to_dict(),
                          by_site=ab["site"].value_counts().to_dict())

    home = clean[~clean["site"].isin(REGIONS) & (clean["site"] != "Unknown")]
    hm = home.groupby(["split", "object_type"]).size().unstack(fill_value=0)
    print("\n== Home texts available for matching (analysis settings) ==")
    print(hm.to_string())
    out["home_by_split_object"] = {f"{a}|{b}": int(v) for (a, b), v in hm.stack().items() if v}

    (ROOT / "results" / "foreign_seals_scoping.json").write_text(json.dumps(out, indent=1, default=int))


if __name__ == "__main__":
    main()
