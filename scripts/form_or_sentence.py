"""Is a seal text a sentence (parts depend on each other) or a form (fields filled independently)? Exploration only.
For texts that have both a frozen opener first and a frozen closer last: mutual information between opener and closer,
against texts' closers permuted among them (keeps both margins). Also: opener vs the sign just before the closer,
and the dependency between the first two and last two signs in all texts of 4+ signs."""
import sys, json, math
from pathlib import Path
from collections import Counter
import numpy as np
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from indus_workbench import data
ROOT = Path(__file__).resolve().parents[1]
raw, _ = data.load_raw("indus_website")
c = data.build_corpus(raw, "indus_website", metadata=data.load_metadata("indus_website"), drop_damaged=True, dedupe=True, drop_unidentified=True)
ex = data.explore_only(c).df   # EXPLORATION ONLY
P = json.load(open(ROOT / "hypotheses/H-2026-10-16-51b7445b.json"))["params"]
O, C = set(P["openers"]), set(P["closers"])
def mi(a, b):
    n = len(a); ca, cb, cab = Counter(a), Counter(b), Counter(zip(a, b))
    return sum(v / n * math.log2(v * n / (ca[x] * cb[y])) for (x, y), v in cab.items())
r = np.random.default_rng(0)
def test(a, b, name):
    obs = mi(a, b); null = np.array([mi(a, list(r.permutation(b))) for _ in range(5000)])
    print(f"{name}: n {len(a)}; MI {obs:.3f} bits vs shuffled {null.mean():.3f}; excess {obs-null.mean():+.3f}; p {(1+(null>=obs).sum())/5001:.4f}")
fr = [list(s) for s in ex.signs if len(s) >= 3 and s[0] in O and s[-1] in C]
test([s[0] for s in fr], [s[-1] for s in fr], "opener vs closer (framed texts)")
test([s[0] for s in fr], [s[-2] for s in fr], "opener vs sign before the closer")
l4 = [list(s) for s in ex.signs if len(s) >= 4]
test([s[0] for s in l4], [s[-1] for s in l4], "first vs last sign (all 4+ texts)")
test([s[0] for s in l4], [s[1] for s in l4], "first vs second sign (adjacent, for scale)")
test([s[-2] for s in l4], [s[-1] for s in l4], "second-last vs last sign (adjacent, for scale)")
