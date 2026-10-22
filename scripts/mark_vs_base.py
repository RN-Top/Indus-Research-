"""Does the mark or the base decide where a derived sign goes? Exploration only.
Derived signs with 5+ uses, classified by mark class (TOP, OUTER, INNER as in mark_classes_scouting.py; one class only)
and by root base. Position profile = (share first, share last, mean relative position). Compare pairs of derived signs
that share the mark class but not the base, with pairs that share the base but not the mark class.
Null: mark-class labels permuted among the derived signs (keeps bases)."""
import sys, csv
from pathlib import Path
from collections import Counter, defaultdict
import numpy as np
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from indus_workbench import data
ROOT = Path(__file__).resolve().parents[1]
raw, _ = data.load_raw("indus_website")
c = data.build_corpus(raw, "indus_website", metadata=data.load_metadata("indus_website"), drop_damaged=True, dedupe=True, drop_unidentified=True)
seqs = [list(s) for s in data.explore_only(c).df.signs if len(s) >= 2]   # EXPLORATION ONLY
ann = {r["sign"]: r for r in csv.DictReader(open(ROOT / "data/sign_marks/marks_blind_2026-10-20.csv"))}
def root(g):
    seen = set()
    while g in ann and ann[g]["base"] not in ("self", "", g) and g not in seen:
        seen.add(g); g = ann[g]["base"]
    return g
OUTER = lambda m: m == "enclosure_strokes" or m == "brackets" or m.startswith("side_strokes")
INNER = lambda m: m in ("inner_line", "inner_dot", "crossbar")
TOP = lambda m: m in ("roof", "antennae") or m.startswith("top_strokes")
prof = defaultdict(list)
for s in seqs:
    n = len(s)
    for i, x in enumerate(s): prof[x].append((i == 0, i == n - 1, i / (n - 1)))
items = []
for g, r in ann.items():
    if r["base"] in ("self", "", g) or len(prof.get(g, [])) < 5: continue
    ms = [m for m in r["marks"].split(";") if m]
    cls = [k for k, f in (("top", TOP), ("outer", OUTER), ("inner", INNER)) if any(map(f, ms))]
    if len(cls) != 1: continue
    p = np.array(prof[g], dtype=float).mean(0)
    items.append((g, root(g), cls[0], p))
print(f"derived signs with 5+ uses and one mark class: {len(items)}; by class {Counter(i[2] for i in items)}; bases {len(set(i[1] for i in items))}")
P = np.array([i[3] for i in items]); B = np.array([i[1] for i in items], dtype=object); M = np.array([i[2] for i in items], dtype=object)
iu = np.triu_indices(len(items), 1)
D = np.linalg.norm(P[iu[0]] - P[iu[1]], axis=1)
def stat(m):
    same_m = m[iu[0]] == m[iu[1]]; same_b = B[iu[0]] == B[iu[1]]
    a = D[same_m & ~same_b]; b = D[same_b & ~same_m]
    return b.mean() - a.mean(), a.mean(), b.mean(), len(a), len(b)
obs, a, b, na, nb = stat(M)
print(f"distance: same mark, different base {a:.3f} ({na} pairs); same base, different mark {b:.3f} ({nb} pairs); difference {obs:+.3f}")
r = np.random.default_rng(0)
null = np.array([stat(r.permutation(M))[0] for _ in range(5000)])
print(f"null mean {null.mean():+.3f}; p (mark-sharing pairs closer) {(1+(null>=obs).sum())/5001:.4f}")
# overall: same mark vs different mark, ignoring base
same_m = M[iu[0]] == M[iu[1]]
print(f"same mark class {D[same_m].mean():.3f} vs different class {D[~same_m].mean():.3f}")
