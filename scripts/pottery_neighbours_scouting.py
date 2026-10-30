"""Which genre do pottery graffiti resemble most? (scouting, descriptive)
Sign-frequency profiles (tokens of texts with 2+ signs) per object group in the merged ICIT corpus;
Jensen-Shannon divergence between groups, with a size-matched bootstrap (draw the same number of texts
from each group, 1,000x) so bigger groups are not favoured. Also: which signs are most over-represented
on graffiti relative to seals and to tablets (log-ratio, min 8 graffiti tokens)."""
import json, collections, math, random
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
d = json.load(open(ROOT / "data/icit_merged_paragorth/merged-corpus-canonical.json"))
def grp(t):
    t = str(t)
    if t.startswith("SEAL"): return "seal"
    if t.startswith("POT:T:g"): return "graffito"
    if t.startswith("POT:T:s") or t.startswith("POT:T:S"): return "stamped pot"
    if t.startswith("TAB:B"): return "tablet B"
    if t.startswith("TAB:I"): return "tablet I"
    if t.startswith("TAB:C"): return "copper tablet"
    if t.startswith("TAG"): return "tag/sealing"
    return None
G = collections.defaultdict(list)
for x in d:
    g = grp(x["type"])
    if g and len(x["seq"]) >= 2: G[g].append(x["seq"])
def jsd(a, b):
    k = set(a) | set(b); A = sum(a.values()); B = sum(b.values()); s = 0
    for t in k:
        p = a[t] / A; q = b[t] / B; m = (p + q) / 2
        if p: s += 0.5 * p * math.log2(p / m)
        if q: s += 0.5 * q * math.log2(q / m)
    return s
rng = random.Random(7); n = len(G["graffito"])
print("groups (texts 2+ signs):", {g: len(v) for g, v in G.items()})
print(f"\nJSD from graffiti (size-matched to {n} texts each, mean of 1000 draws; lower = more alike):")
res = []
for g in G:
    if g == "graffito" or len(G[g]) < 30: continue
    vals = []
    for _ in range(1000):
        A = rng.choices(G["graffito"], k=n); B = rng.choices(G[g], k=n)
        vals.append(jsd(collections.Counter(t for s in A for t in s), collections.Counter(t for s in B for t in s)))
    vals.sort(); res.append((sum(vals) / len(vals), vals[25], vals[975], g))
# baseline: graffiti vs itself (two resamples)
base = []
for _ in range(1000):
    A = rng.choices(G["graffito"], k=n); B = rng.choices(G["graffito"], k=n)
    base.append(jsd(collections.Counter(t for s in A for t in s), collections.Counter(t for s in B for t in s)))
base.sort()
for m, lo, hi, g in sorted(res): print(f"  {g:14s} {m:.3f}  [95%: {lo:.3f}-{hi:.3f}]")
print(f"  (graffiti vs graffiti resample: {sum(base)/len(base):.3f})")
gc = collections.Counter(t for s in G["graffito"] for t in s); Ng = sum(gc.values())
for ref in ("seal", "tablet B", "tablet I"):
    rc = collections.Counter(t for s in G[ref] for t in s); Nr = sum(rc.values())
    lr = sorted(((math.log2(((gc[t] + .5) / Ng) / ((rc[t] + .5) / Nr)), t, gc[t], rc[t]) for t in gc if gc[t] >= 8), reverse=True)
    print(f"\nover-represented on graffiti vs {ref}:", [(f"G{t}", g_, r_) for _, t, g_, r_ in lr[:8]])
