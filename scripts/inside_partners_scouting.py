"""Do inside marks change what KIND of partner a sign takes? (scouting, EXPLORATION split only)

Inner-only variant/base pairs (blind annotation; INNER = inner_line, inner_dot, crossbar; no outer/top marks).
For each token: preceded by a numeral? followed by a numeral? preceded by an opener (heading)? followed by a closer?
Statistic per feature: variant share minus base share, per pair, weighted by variant count over pairs where both occur.
Null: variant/base labels permuted within each pair's tokens (2,000 times). Two-sided p. Not a confirmatory test.
"""
import csv, sys
from collections import defaultdict
from pathlib import Path
import numpy as np
ROOT = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT / "scripts"))
from functional_slots import load  # noqa: E402
from functional_skeleton import assign  # noqa: E402
from number_system import VAL  # noqa: E402
OUTER = lambda m: m in ("enclosure_strokes", "brackets") or m.startswith("side_strokes")
INNER = lambda m: m in ("inner_line", "inner_dot", "crossbar")
TOP = lambda m: m in ("roof", "antennae") or m.startswith("top_strokes")
RNG = np.random.default_rng(20261022)
df = load(); roles, _ = assign(list(df.signs))
pairs = []
for r in csv.DictReader(open(ROOT / "data/sign_marks/marks_blind_2026-10-20.csv")):
    if r["base"] in ("self", "") or r["base"] == r["sign"]:
        continue
    ms = [m for m in r["marks"].split(";") if m]
    if any(map(INNER, ms)) and not any(map(OUTER, ms)) and not any(map(TOP, ms)):
        pairs.append((r["sign"], r["base"]))
F = ["numeral before", "numeral after", "opener before", "closer after"]
tok = defaultdict(list)
for s in df.signs:
    for k, x in enumerate(s):
        L = s[k - 1] if k else None; R = s[k + 1] if k + 1 < len(s) else None
        tok[x].append([L in VAL, R in VAL, roles.get(L) == 0, roles.get(R) == 2])
tok = {k: np.array(v, float) for k, v in tok.items()}
use = [(v, b) for v, b in pairs if v in tok and b in tok and v not in VAL and b not in VAL and b != ("G220" if "--nofish" in sys.argv else "")]
def stat(t):
    num = np.zeros(len(F)); den = 0
    for v, b in use:
        num += len(t[v]) * (t[v].mean(0) - t[b].mean(0)); den += len(t[v])
    return num / den, den
obs, n = stat(tok)
null = []
for _ in range(2000):
    t2 = dict(tok)
    for v, b in use:
        pool = RNG.permutation(np.vstack([tok[v], tok[b]])); t2[v], t2[b] = pool[:len(tok[v])], pool[len(tok[v]):]
    null.append(stat(t2)[0])
null = np.array(null)
print(f"Inner-only pairs: {len(pairs)}; both present in exploration: {len(use)}; marked tokens: {n}")
for i, f in enumerate(F):
    base = np.mean([tok[b][:, i].mean() for _, b in use])
    p = (1 + np.sum(np.abs(null[:, i]) >= abs(obs[i]))) / (len(null) + 1)
    print(f"   {f:15} marked minus plain {obs[i]:+.3f}   (two-sided p {p:.4f})")
