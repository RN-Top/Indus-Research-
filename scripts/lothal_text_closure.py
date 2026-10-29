"""Does a Lothal seal stick to one kind of closure? (scouting, descriptive; data already looked at)

Sealings: Lothal TAG entries in the merged ICIT corpus (paragorth), one or more seal texts per sealing.
Closure types: Frenez & Tosi 2005, Table 1 (paragorth derived json); 'undiagnostic' and missing excluded.
Statistic: among pairs of sealings stamped by the same seal text, the share that closed the same kind of thing.
Null: closure types shuffled among the diagnostic sealings (10,000 times), keeping which seals are on which sealing.
Run with and without the box seal (G817 G2 G48 G740 / G861 G2 G48 G740 variants), which dominates.
Usage: python3 scripts/lothal_text_closure.py <frenez-tosi2005.json>
"""
import json, sys
from collections import defaultdict
from itertools import combinations
from pathlib import Path
import numpy as np
ROOT = Path(__file__).resolve().parents[1]
d = json.load(open(ROOT / "data/icit_merged_paragorth/merged-corpus-canonical.json"))
FT = {r[0]: r[2] for r in json.load(open(sys.argv[1]))["rows"]}
sl = defaultdict(set)
for x in d:
    if x["site"] == "Lothal" and x["cisi"].startswith("L-") and x["type"].startswith("TAG") and x["seq"]:
        sl[x["cisi"]].add(" ".join(f"G{s}" for s in x["seq"]))
diag = sorted(L for L in sl if FT.get(L) not in (None, "undiagnostic", "other types"))
print(f"Lothal sealings with texts: {len(sl)}; with a diagnostic closure type: {len(diag)}")
rng = np.random.default_rng(20261029)

def run(exclude):
    use = [L for L in diag if not (sl[L] & exclude)]
    idx = {L: i for i, L in enumerate(use)}
    by_seal = defaultdict(list)
    for L in use:
        for s in sl[L]: by_seal[s].append(idx[L])
    pairs = sorted({(a, b) for v in by_seal.values() for a, b in combinations(sorted(v), 2)})
    if not pairs: return None
    lab = np.array([FT[L] for L in use]); A = np.array([p[0] for p in pairs]); B = np.array([p[1] for p in pairs])
    obs = (lab[A] == lab[B]).mean()
    null = np.array([(lambda z: (z[A] == z[B]).mean())(rng.permutation(lab)) for _ in range(10000)])
    reused = sum(len(v) > 1 for v in by_seal.values())
    return len(use), reused, len(pairs), obs, null.mean(), (1 + (null >= obs).sum()) / 10001

box = {s for v in sl.values() for s in v if s.endswith("G2 G48 G740") or s.endswith("G48 G740")}
print("box-seal texts excluded in run 2:", sorted(box))
for name, ex in [("all seals", set()), ("without the box seal", box)]:
    n, reused, npairs, obs, nm, p = run(ex)
    print(f"{name:22s} sealings {n:3d}  seals used 2+ times {reused:2d}  same-seal pairs {npairs:3d}  "
          f"same closure {obs:.2f} vs chance {nm:.2f}  p {p:.4f}")
