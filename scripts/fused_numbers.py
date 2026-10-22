"""Are stroke-marked jars fused numbers ('jar with k strokes' = 'k + jar')? Exploration only.
Units: the sequence numeral(value k) + G740, and the marked jars G741 (1 stroke), G742 (2), G745 (3).
Company of a unit = the sign before it and the sign after it (text edges as tokens), plus its relative position.
Compare each sequence 'k + jar' with each marked jar by Jensen-Shannon divergence of company."""
import sys, math
from pathlib import Path
from collections import Counter
import numpy as np
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from indus_workbench import data
raw, _ = data.load_raw("indus_website")
c = data.build_corpus(raw, "indus_website", metadata=data.load_metadata("indus_website"), drop_damaged=True, dedupe=True, drop_unidentified=True)
seqs = [list(s) for s in data.explore_only(c).df.signs]   # EXPLORATION ONLY
VAL = {"G1": 1, "G31": 1, "G2": 2, "G32": 2, "G3": 3, "G33": 3}
units = {k: [] for k in ("1+jar", "2+jar", "3+jar", "G741", "G742", "G745", "G740 alone")}
for s in seqs:
    n = len(s)
    for i, x in enumerate(s):
        if x == "G740" and i > 0 and s[i-1] in VAL:
            units[f"{VAL[s[i-1]]}+jar"].append((s[i-2] if i >= 2 else "<s>", s[i+1] if i < n-1 else "</s>", (i-1)/(n-1) if n > 1 else 0))
        elif x == "G740":
            units["G740 alone"].append((s[i-1] if i else "<s>", s[i+1] if i < n-1 else "</s>", i/(n-1) if n > 1 else 0))
        elif x in ("G741", "G742", "G745"):
            units[x].append((s[i-1] if i else "<s>", s[i+1] if i < n-1 else "</s>", i/(n-1) if n > 1 else 0))
def comp(u): return Counter([("L", a) for a, b, p in u] + [("R", b) for a, b, p in u])
def jsd(a, b):
    keys = set(a) | set(b); A = sum(a.values()); B = sum(b.values())
    p = np.array([a[k]/A for k in keys]); q = np.array([b[k]/B for k in keys]); m = (p+q)/2
    f = lambda x, y: np.sum(x[x > 0]*np.log2(x[x > 0]/y[x > 0])); return 0.5*f(p, m)+0.5*f(q, m)
for k, u in units.items():
    top = Counter([("L", a) for a, b, p in u]).most_common(3), Counter([("R", b) for a, b, p in u]).most_common(3)
    print(f"{k:11} n {len(u):3d}  mean position {np.mean([p for a,b,p in u]):.2f}  before {top[0]}  after {top[1]}")
print("\nJSD of company (lower = more alike):")
print("            " + "  ".join(f"{m:>6}" for m in ("G741", "G742", "G745", "G740 alone")))
for s in ("1+jar", "2+jar", "3+jar"):
    print(f"{s:10} " + "  ".join(f"{jsd(comp(units[s]), comp(units[m])):6.3f}" for m in ("G741", "G742", "G745", "G740 alone")))
