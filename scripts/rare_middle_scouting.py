"""Are the rare signs in the middle of inscriptions built from common parts? (scouting, EXPLORATION split only)

Middle = signs after the heading (frozen openers, plus G2/G60 right after them) and before the trailing frozen closers,
exactly as in H-2026-10-16-a6cd844c. Rare = 5 or fewer uses in the exploration split. "Built" = the blind annotation
(data/sign_marks/marks_blind_2026-10-20.csv) gives a base other than the sign itself: a marked variant or a ligature.

1. Among rare sign tokens: share in the middle for built vs plain rare signs (null: built labels permuted over
   rare sign types, 5,000 times).
2. Among middle tokens: share built for rare vs common signs.
3. For built rare middle signs: what are their bases (role and frequency of the base)?
"""
import csv, json, sys
from collections import Counter, defaultdict
from pathlib import Path
import numpy as np
ROOT = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT)); sys.path.insert(0, str(ROOT / "scripts"))
from indus_workbench import hypotheses as hy  # noqa: E402
from functional_slots import load  # noqa: E402
from number_system import VAL  # noqa: E402

RNG = np.random.default_rng(20261023)
h = json.load(open(ROOT / "hypotheses/H-2026-10-16-a6cd844c.json")); p = h["params"]
OP, CL, TE = set(p["openers"]), set(p["closers"]), set(p["terminals"])
ann = {r["sign"]: r for r in csv.DictReader(open(ROOT / "data/sign_marks/marks_blind_2026-10-20.csv"))}
def base_of(g):
    r = ann.get(g)
    return None if r is None or r["base"] in ("self", "") or r["base"] == g else r["base"]
def kind_of(g):
    ms = [m for m in ann[g]["marks"].split(";") if m]
    return "ligature" if "ligature" in ms else "doubled" if "doubled" in ms else "marked"

df = load(); seqs = [list(s) for s in df.signs]
use = Counter(x for s in seqs for x in s)
rare = {g for g, n in use.items() if n <= 5}
mid_flags = defaultdict(list)
for s in seqs:
    m = hy._middle(s, OP, CL, TE)
    # mark which positions are middle: _middle returns the middle slice; locate it
    inmid = [False] * len(s)
    if m:
        for i in range(len(s) - len(m) + 1):
            if s[i:i + len(m)] == m:
                for j in range(i, i + len(m)):
                    inmid[j] = True
                break
    for x, f in zip(s, inmid):
        mid_flags[x].append(f)

annot_rare = sorted(g for g in rare if g in ann)
built = {g: base_of(g) is not None for g in annot_rare}
def stat(lab):
    b = [f for g in annot_rare if lab[g] for f in mid_flags[g]]
    u = [f for g in annot_rare if not lab[g] for f in mid_flags[g]]
    return np.mean(b) - np.mean(u), np.mean(b), np.mean(u), len(b), len(u)
obs, mb, mu, nb, nu = stat(built)
keys = list(built); vals = np.array([built[k] for k in keys])
null = []
for _ in range(5000):
    perm = dict(zip(keys, RNG.permutation(vals)))
    null.append(stat(perm)[0])
p1 = (1 + np.sum(np.array(null) >= obs)) / 5001
print(f"Exploration texts {len(seqs)}; rare sign types (<=5 uses) {len(rare)}, annotated {len(annot_rare)}; built {sum(built.values())}")
print(f"1. Rare tokens in the middle: built {mb:.1%} (n {nb}) vs plain {mu:.1%} (n {nu}); diff {obs:+.3f}, p {p1:.4f}")

mt = [(x, x in rare) for s in seqs for x, f in zip(s, [ff for ff in []] or []) ]
mid_tokens = [x for x, fl in mid_flags.items() for f in fl if f for _ in [0]]
mid_tok = Counter()
for x, fl in mid_flags.items():
    mid_tok[x] += sum(fl)
def share_built(signs):
    sel = [(g, n) for g, n in signs if g in ann]
    return sum(n for g, n in sel if base_of(g)) / max(1, sum(n for g, n in sel)), sum(n for g, n in sel)
sr, nr = share_built([(g, n) for g, n in mid_tok.items() if g in rare])
sc, nc = share_built([(g, n) for g, n in mid_tok.items() if g not in rare and g not in VAL])
print(f"2. Middle tokens that are built signs: rare {sr:.1%} (n {nr}) vs common, non-numeral {sc:.1%} (n {nc})")

role = lambda g: "numeral" if g in VAL else "opener" if g in OP else "closer" if g in CL else "middle/other"
bm = [(g, base_of(g)) for g in annot_rare if built[g] and any(mid_flags[g])]
print(f"3. Built rare signs used in the middle: {len(bm)} types")
print("   kind:", dict(Counter(kind_of(g) for g, _ in bm)))
print("   base role:", dict(Counter(role(b) for _, b in bm)))
print("   base uses (median):", int(np.median([use.get(b, 0) for _, b in bm])) if bm else None)
print("   commonest bases:", Counter(b for _, b in bm).most_common(10))
json.dump(dict(obs=obs, p=p1, built_mid=mb, plain_mid=mu, rare_mid_built=sr, common_mid_built=sc,
               built_rare_middle=bm), open(ROOT / "results/rare_middle_scouting.json", "w"), indent=1)

# 4. Does a rare built sign keep its base's company? (borrowing the base's data)
# For each token of a rare built sign: is its left or right neighbour among the neighbours its BASE takes
# (base's left/right neighbour sets, from the base's own tokens)? Null: bases shuffled among the rare built signs.
nbL, nbR = defaultdict(Counter), defaultdict(Counter)
for s in seqs:
    for k, x in enumerate(s):
        nbL[x][s[k - 1] if k else "#"] += 1
        nbR[x][s[k + 1] if k + 1 < len(s) else "#"] += 1
rb = [g for g in annot_rare if built[g] and use.get(base_of(g), 0) >= 10]
def top(c, n=10):
    return {k for k, _ in c.most_common(n)}
def hit_rate(assign):
    hit = tot = 0
    for g in rb:
        b = assign[g]
        L, R = top(nbL[b]), top(nbR[b])
        for s in seqs:
            for k, x in enumerate(s):
                if x == g:
                    tot += 1
                    hit += (s[k - 1] if k else "#") in L or (s[k + 1] if k + 1 < len(s) else "#") in R
    return hit / tot, tot
own = {g: base_of(g) for g in rb}
obs4, n4 = hit_rate(own)
bases = [own[g] for g in rb]; null4 = []
for _ in range(500):
    null4.append(hit_rate(dict(zip(rb, RNG.permutation(bases))))[0])
p4 = (1 + np.sum(np.array(null4) >= obs4)) / 501
print(f"4. Rare built signs whose base has 10+ uses: {len(rb)} types, {n4} tokens. Neighbour shared with own base: "
      f"{obs4:.1%} vs {np.mean(null4):.1%} with a random other base (p {p4:.4f})")
