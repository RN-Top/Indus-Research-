"""Seals as a network: do name-like rare signs stay home, and which cities are linked? (EXPLORATION ONLY.)

A. For rare signs (<=5 uses), split into those used in a name-like slot (first sign of a
   heading-less text, or sign before the closer) and other rare signs: is each sign's set
   of texts more concentrated at one site than random placement over the corpus predicts?
   Common signs are compared by drawing the same number of their texts at random.
B. Sites as nodes (sites with 10+ texts; texts found abroad pooled as one node). For each
   pair: shared sign types, all and rare-only, against 1,000 shuffles of the site labels
   (keeps each site's number of texts). Exploration split only; nothing tested or registered.

    python scripts/seal_network.py
"""

import json
import sys
from collections import Counter, defaultdict
from itertools import combinations
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from foreign_seals_scope import REGIONS  # noqa: E402
from functional_skeleton import assign  # noqa: E402
from functional_slots import NUMERALS, load  # noqa: E402

RNG = np.random.default_rng(20261016)


def main():
    df = load(); df = df[df["signs"].map(len) > 0].reset_index(drop=True)
    seqs = [list(s) for s in df["signs"]]
    roles, _ = assign(seqs)
    site = np.array([("Abroad (W. Asia, Gulf, C. Asia)" if s in REGIONS else s) for s in df["site"]])
    tok = Counter(x for s in seqs for x in s)
    texts_of = defaultdict(set)
    name_slot = set()
    for i, s in enumerate(seqs):
        j = len(s)
        while j > 0 and roles.get(s[j - 1]) == 2:
            j -= 1
        for k, x in enumerate(s):
            texts_of[x].add(i)
            if tok[x] <= 5 and x not in NUMERALS and ((k == 0 and roles.get(x) != 0) or (k == j - 1 and j < len(s))):
                name_slot.add(x)
    out = {}

    # ---- A ----
    known = site != "Unknown"
    idx_known = np.flatnonzero(known)

    def conc(ix):
        c = Counter(site[i] for i in ix)
        return max(c.values()) / len(ix), len(c) == 1

    def null_conc(k, n=2000):
        d = [conc(RNG.choice(idx_known, k, replace=False)) for _ in range(n)]
        return np.mean([a for a, _ in d]), np.mean([b for _, b in d])
    cache = {k: null_conc(k) for k in range(2, 6)}
    groups = {"name-slot rare signs": [], "other rare signs": [], "common signs (k texts drawn at random)": []}
    for x, ix in texts_of.items():
        ix = [i for i in ix if known[i]]
        k = len(ix)
        if x in NUMERALS or k < 2:
            continue
        if tok[x] <= 5 and 2 <= k <= 5:
            g = "name-slot rare signs" if x in name_slot else "other rare signs"
            c, one = conc(ix)
            groups[g].append((k, c, one))
        elif tok[x] > 15 and k >= 10:
            for k2 in (2, 3, 4, 5):
                c, one = conc(RNG.choice(ix, k2, replace=False))
                groups["common signs (k texts drawn at random)"].append((k2, c, one))
    print("== A. Do signs stay at one site more than random placement predicts? (signs in 2-5 texts) ==")
    resA = {}
    for g, rows in groups.items():
        if not rows:
            continue
        one = np.mean([r[2] for r in rows]); one0 = np.mean([cache[r[0]][1] for r in rows])
        c = np.mean([r[1] for r in rows]); c0 = np.mean([cache[r[0]][0] for r in rows])
        resA[g] = dict(signs=len(rows), all_at_one_site=float(one), expected=float(one0), top_site_share=float(c), expected_share=float(c0))
        print(f"   {g:42} n {len(rows):4}  all at one site {one:.0%} (random {one0:.0%});  top-site share {c:.0%} (random {c0:.0%})")
    # seals only
    seal = (df["object_type"] == "seal").to_numpy() & known
    sidx = np.flatnonzero(seal)
    rows = []
    for x in name_slot:
        ix = [i for i in texts_of[x] if seal[i]]
        if 2 <= len(ix) <= 5:
            c = Counter(site[i] for i in ix); rows.append((len(ix), len(c) == 1))
    if rows:
        exp = np.mean([np.mean([len(set(site[RNG.choice(sidx, k, replace=False)])) == 1 for _ in range(1000)]) for k, _ in rows])
        print(f"   seals only, name-slot rare signs: n {len(rows)}, all at one site {np.mean([r[1] for r in rows]):.0%} (random {exp:.0%})")
        resA["seals only, name-slot rare"] = dict(signs=len(rows), all_at_one_site=float(np.mean([r[1] for r in rows])), expected=float(exp))
    out["A"] = resA

    # ---- B ----
    sc = Counter(site[known])
    nodes = [s for s, n in sc.items() if n >= 10]
    print(f"\n== B. Sites as nodes (10+ texts): {', '.join(f'{s} {sc[s]}' for s in nodes)} ==")
    nidx = {s: np.flatnonzero(site == s) for s in nodes}
    rare_set = {x for x in tok if tok[x] <= 5 and x not in NUMERALS}

    def shared(labels):
        voc = {s: set() for s in nodes}
        for i in np.flatnonzero(np.isin(labels, nodes)):
            voc[labels[i]].update(seqs[i])
        res = {}
        for a, b in combinations(nodes, 2):
            sh = voc[a] & voc[b]
            res[(a, b)] = (len(sh), len(sh & rare_set), sorted(sh & rare_set))
        return res
    obs = shared(site)
    pool = np.flatnonzero(np.isin(site, nodes))
    nulls = defaultdict(list)
    for _ in range(1000):
        lab = site.copy(); lab[pool] = RNG.permutation(site[pool])
        for k, v in shared(lab).items():
            nulls[k].append(v[:2])
    rows = []
    for (a, b), (n_all, n_rare, rare_list) in obs.items():
        arr = np.array(nulls[(a, b)])
        rows.append(dict(a=a, b=b, shared=n_all, expected=float(arr[:, 0].mean()), shared_rare=n_rare, expected_rare=float(arr[:, 1].mean()),
                         p_hi_rare=float((1 + (arr[:, 1] >= n_rare).sum()) / 1001), rare_signs=rare_list))
    rows.sort(key=lambda r: -(r["shared_rare"] - r["expected_rare"]))
    print(f"   {'pair':48} shared signs (expected)   shared RARE signs (expected)")
    for r in rows:
        print(f"   {r['a'] + ' — ' + r['b']:48} {r['shared']:4} ({r['expected']:5.1f})        {r['shared_rare']:3} ({r['expected_rare']:4.1f})  {' '.join(r['rare_signs'][:6])}")
    out["B"] = rows
    # bridging rare signs across distant nodes
    far = []
    for x in rare_set:
        ss = sorted({site[i] for i in texts_of[x] if known[i]})
        if len(ss) >= 3 or "Abroad (W. Asia, Gulf, C. Asia)" in ss:
            far.append((x, tok[x], ss))
    far.sort(key=lambda t: (-len(t[2]), -t[1]))
    print("\n   rare signs reaching 3+ sites, or abroad:")
    for x, n, ss in far[:15]:
        print(f"      {x:6} uses {n}: {', '.join(ss)}")
    out["bridges"] = far
    (ROOT / "results" / "seal_network.json").write_text(json.dumps(out, indent=1, default=str))


if __name__ == "__main__":
    main()
