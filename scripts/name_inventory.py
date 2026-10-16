"""Candidate names: rare signs in the name-like slots, and whether they behave like names. (EXPLORATION ONLY.)

Name-like slots (from results/rare_signs_as_names_scouting.md): the first sign of a
heading-less text, and the sign just before the closer. Rare = 5 or fewer uses in
exploration. For the candidates: how many, how often each repeats, whether repeats
stay at one site and one object type, which neighbours they take, and how they
compare with rare signs elsewhere in the text. Description only.

    python scripts/name_inventory.py
"""

import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from functional_skeleton import assign  # noqa: E402
from functional_slots import NUMERALS, load  # noqa: E402


def main():
    df = load(); df = df[df["signs"].map(len) > 0].reset_index(drop=True)
    seqs = [list(s) for s in df["signs"]]
    roles, _ = assign(seqs)
    tok = Counter(x for s in seqs for x in s)
    rare = lambda x: tok[x] <= 5 and x not in NUMERALS  # noqa: E731
    occ = defaultdict(list)  # sign -> [(text index, slot)]
    for i, s in enumerate(seqs):
        j = len(s)
        while j > 0 and roles.get(s[j - 1]) == 2:
            j -= 1
        for k, x in enumerate(s):
            if not rare(x):
                continue
            if k == 0 and roles.get(x) != 0:
                slot = "first (no heading)"
            elif k == j - 1 and j < len(s):
                slot = "before closer"
            else:
                slot = "elsewhere"
            occ[x].append((i, slot))
    rows = []
    for x, o in occ.items():
        slots = Counter(sl for _, sl in o)
        sites = Counter(df["site"].iloc[i] for i, _ in o)
        objs = Counter(df["object_type"].iloc[i] for i, _ in o)
        rows.append(dict(sign=x, uses=len(o), name_slot_uses=slots["first (no heading)"] + slots["before closer"],
                         slots=dict(slots), sites=dict(sites), objects=dict(objs), one_site=len(sites) == 1,
                         one_object=len(objs) == 1))
    cand = [r for r in rows if r["name_slot_uses"] > 0]
    other = [r for r in rows if r["name_slot_uses"] == 0]
    out = {"candidates": len(cand), "other_rare": len(other)}
    print(f"Rare non-numeral sign types: {len(rows)}; used at least once in a name-like slot: {len(cand)}; never: {len(other)}")
    for lab, grp in [("candidates", cand), ("other rare signs", other)]:
        rep = [r for r in grp if r["uses"] >= 2]
        print(f"   {lab}: {len(grp)} types; used once {sum(r['uses'] == 1 for r in grp)}; "
              f"repeated {len(rep)}, of which all at one site {np.mean([r['one_site'] for r in rep]):.0%}, "
              f"all on one object type {np.mean([r['one_object'] for r in rep]):.0%}" if rep else "")
        out[lab] = dict(types=len(grp), once=sum(r["uses"] == 1 for r in grp), repeated=len(rep),
                        one_site=float(np.mean([r["one_site"] for r in rep])) if rep else None,
                        one_object=float(np.mean([r["one_object"] for r in rep])) if rep else None)
    # baseline: for common middle signs with 2-5 random uses sampled, how often would all fall at one site?
    rng = np.random.default_rng(0)
    site_arr = df["site"].values
    base = []
    for r in [r for r in cand if r["uses"] >= 2]:
        idx = rng.choice(len(df), (2000, r["uses"]))
        base.append(np.mean([len(set(site_arr[row])) == 1 for row in idx]))
    print(f"   if the texts of repeated candidates were picked at random, 'all at one site' would happen {np.mean(base):.0%} of the time")
    out["one_site_chance"] = float(np.mean(base))
    # do candidates share neighbours (same heading / same closer)?
    print("\n   repeated candidates, with their sites, objects and slots:")
    for r in sorted([r for r in cand if r["uses"] >= 2], key=lambda r: -r["uses"])[:20]:
        print(f"      {r['sign']:6} uses {r['uses']}  slots {r['slots']}  sites {r['sites']}  objects {r['objects']}")
    # closers that follow candidate names
    after = Counter()
    for x in [r["sign"] for r in cand]:
        for i, sl in occ[x]:
            if sl == "before closer":
                s = seqs[i]; k = s.index(x)
                after[s[k + 1]] += 1
    print("\n   closers right after a rare sign:", after.most_common(8))
    allc = Counter(s[-1] for s in seqs if roles.get(s[-1]) == 2)
    print("   closers overall (last sign):", allc.most_common(8))
    out["closers_after_rare"] = after.most_common(12); out["closers_overall"] = allc.most_common(12)
    out["inventory"] = sorted(cand, key=lambda r: (-r["name_slot_uses"], -r["uses"]))
    (ROOT / "results" / "name_inventory.json").write_text(json.dumps(out, indent=1, default=str))


if __name__ == "__main__":
    main()
