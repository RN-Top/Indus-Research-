"""Closer signs as category marks: extension of scripts/closer_categories.py. (EXPLORATORY.)

Adds what the first test left out:
  A. material (steatite, faience, copper, clay ...), not tested before;
  B. seals only: site and material inside one object type, so tablets do not drive the result;
  C. texts that CONTAIN the closer anywhere (the first test used the final sign only).
Same machinery: chi-square against 5,000 shuffles, Cramer's V and excess V, strongest
category with lift, a stratified shuffle as the confound check, and Benjamini-Hochberg
across every test in this file. Exploration split only; nothing registered.

    python scripts/closer_categories_ext.py
"""

import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from closer_categories import MIN_SUPPORT, bh, collapse, test  # noqa: E402
from functional_skeleton import assign  # noqa: E402
from functional_slots import load  # noqa: E402


def main():
    df = load()
    assert set(df["split"]) == {"explore"}
    roles, table = assign(list(df["signs"]))
    closers = [r["sign"] for r in sorted(table, key=lambda r: -r["tokens"]) if r["role"] == "closer"]
    seqs = list(df["signs"])
    last = np.array([s[-1] if s else "" for s in seqs])
    df = df.assign(obj=collapse(df["object_type"].astype(str), 10, "other object"),
                   site_c=collapse(df["site"].astype(str), 10, "other sites"),
                   mat=collapse(df["material"].astype(str), 10, "other material"))
    mat_known = ~df["material"].astype(str).isin(["unknown", "nan", "None", ""]).to_numpy()
    seal = (df["object_type"] == "seal").to_numpy()
    animal_known = seal & ~df["motif_group"].astype(str).isin(["none", "unknown", "nan"]).to_numpy()
    animal = collapse(df["motif_group"].astype(str)[animal_known], 8, "other animal")
    obj, site, mat = df["obj"].to_numpy(), df["site_c"].to_numpy(), df["mat"].to_numpy()

    rows = []

    def run(c, part, field, member, labels, strata, keep):
        m = member[keep]
        if m.sum() < MIN_SUPPORT:
            return
        r = test(m, labels, None)
        r["stratified_p"] = test(m, labels, strata)["p"] if strata is not None else None
        r.update(closer=c, part=part, field=field)
        rows.append(r)

    for c in closers:
        ends = last == c
        has = np.array([c in s for s in seqs])
        # A. material, all texts with a known material; confound: object type
        run(c, "A ends", "material", ends, collapse(df["material"].astype(str)[mat_known], 10, "other material"),
            obj[mat_known], mat_known)
        # B. seals only: site (confound: material) and material (confound: site)
        sm = seal & mat_known
        run(c, "B seals, ends", "site", ends, site[seal], None, seal)
        run(c, "B seals, ends", "material", ends, mat[sm], site[sm], sm)
        # C. contains the closer anywhere
        run(c, "C contains", "object_type", has, obj, site, np.ones(len(df), bool))
        run(c, "C contains", "site", has, site, obj, np.ones(len(df), bool))
        run(c, "C contains", "animal", has, animal, site[animal_known], animal_known)

    q = bh([r["p"] for r in rows])
    sp = [r["stratified_p"] for r in rows if r["stratified_p"] is not None]
    qs = iter(bh(sp))
    for r, qi in zip(rows, q):
        r["q"] = float(qi)
        r["q_stratified"] = float(next(qs)) if r["stratified_p"] is not None else None
    print(f"{len(rows)} tests; BH across all of them\n")
    print(f"{'closer':7}{'part':15}{'field':12}{'n':>5}{'V':>6}{'Vexc':>6}{'q':>8}{'q_strat':>9}  strongest")
    for r in sorted(rows, key=lambda r: r["p"]):
        s = r["strongest"]
        qs_ = f"{r['q_stratified']:.4f}" if r["q_stratified"] is not None else "   -  "
        print(f"{r['closer']:7}{r['part']:15}{r['field']:12}{r['n_closer']:5}{r['cramers_v']:6.2f}{r['v_excess']:6.2f}"
              f"{r['q']:8.4f}{qs_:>9}  {s['category']} {s['with_closer']}/{r['n_closer']} "
              f"({s['share_with_closer']:.0%} vs {s['share_all']:.0%}, x{s['lift']:.1f})")
    (ROOT / "results" / "closer_categories_ext.json").write_text(json.dumps(rows, indent=1, default=int))


if __name__ == "__main__":
    main()
