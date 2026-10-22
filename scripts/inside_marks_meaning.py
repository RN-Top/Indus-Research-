"""Do inside marks change what a sign means? Exploration only.
For each inside-only variant (inner line, inner dot, crossbar; no outer or top marks) with 8+ uses, compare its company
with its plain base: neighbouring signs (left and right), object type, and animal on seals. Statistic per pair:
Jensen-Shannon divergence between the variant's and the base's distributions. Null: variant/base labels permuted over
the pair's tokens (2,000 times). Same company = drawing variant (allograph); different company = a different unit."""
import sys, csv, json
from pathlib import Path
from collections import Counter
import numpy as np, pandas as pd
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from indus_workbench import data
ROOT = Path(__file__).resolve().parents[1]
raw, _ = data.load_raw("indus_website")
c = data.build_corpus(raw, "indus_website", metadata=data.load_metadata("indus_website"), drop_damaged=True, dedupe=True, drop_unidentified=True)
ex = data.explore_only(c).df   # EXPLORATION ONLY
OUTER = lambda m: m == "enclosure_strokes" or m == "brackets" or m.startswith("side_strokes")
INNER = lambda m: m in ("inner_line", "inner_dot", "crossbar")
TOP = lambda m: m in ("roof", "antennae") or m.startswith("top_strokes")
def pairs_of(kind):
    out = []
    for r in csv.DictReader(open(ROOT / "data/sign_marks/marks_blind_2026-10-20.csv")):
        if r["base"] in ("self", "") or r["base"] == r["sign"]: continue
        ms = [m for m in r["marks"].split(";") if m]
        o, i, t = any(map(OUTER, ms)), any(map(INNER, ms)), any(map(TOP, ms))
        if kind == "inner" and i and not o and not t: out.append((r["sign"], r["base"]))
        if kind == "top" and t and not o and not i: out.append((r["sign"], r["base"]))
        if kind == "outer" and o and not i and not t: out.append((r["sign"], r["base"]))
    return out
# tokens with their company
tok = {}
for s, ot, mo in zip(ex.signs, ex.object_type, ex.motif):
    s = list(s)
    for k, x in enumerate(s):
        tok.setdefault(x, []).append({"L": s[k-1] if k else "<s>", "R": s[k+1] if k < len(s)-1 else "</s>",
                                      "obj": ot, "animal": (mo.split(":")[0] if ot == "seal" and mo not in ("unknown", "") else None)})
def jsd(a, b):
    keys = set(a) | set(b); A = sum(a.values()); B = sum(b.values())
    if not A or not B: return np.nan
    p = np.array([a[k]/A for k in keys]); q = np.array([b[k]/B for k in keys]); m = (p+q)/2
    f = lambda x, y: np.sum(x[x > 0] * np.log2(x[x > 0] / y[x > 0]))
    return 0.5*f(p, m) + 0.5*f(q, m)
def feat(rows, f):
    if f == "neighbours": return Counter([("L", r["L"]) for r in rows] + [("R", r["R"]) for r in rows])
    return Counter(r[f] for r in rows if r[f] is not None)
rng = np.random.default_rng(0)
out = []
for kind in ("inner", "top", "outer"):
    for v, b in pairs_of(kind):
        tv, tb = tok.get(v, []), tok.get(b, [])
        if len(tv) < 8 or len(tb) < 8: continue
        row = {"class": kind, "variant": v, "base": b, "n_var": len(tv), "n_base": len(tb)}
        for f in ("neighbours", "obj", "animal"):
            obs = jsd(feat(tv, f), feat(tb, f))
            if obs != obs: row[f] = None; continue
            pool = tv + tb; null = []
            for _ in range(2000):
                idx = rng.permutation(len(pool)); A = [pool[i] for i in idx[:len(tv)]]; B = [pool[i] for i in idx[len(tv):]]
                null.append(jsd(feat(A, f), feat(B, f)))
            null = np.array(null); row[f] = round((1 + (null >= obs).sum()) / 2001, 4)
        out.append(row)
d = pd.DataFrame(out)
print(d.to_string(index=False))
print("\nshare of pairs whose company differs (p < 0.05), by mark class:")
for kind, g in d.groupby("class"):
    print(f"  {kind:6} pairs {len(g):2d}  neighbours {np.mean(g.neighbours < 0.05):.2f}  object {np.mean(g.obj.dropna() < 0.05):.2f}  animal {np.mean(g.animal.dropna() < 0.05):.2f}")

# --- control: pairs another project rates as strong allographs (same sign drawn differently)
lv = json.load(open(sys.argv[1])) if len(sys.argv) > 1 else None
if lv:
    ctrl = [("G%d" % m["form"], "G%d" % m["into"]) for m in lv["merges"] if m["level"] == "strong"]
    rows = []
    for v, b in ctrl:
        tv, tb = tok.get(v, []), tok.get(b, [])
        if len(tv) < 8 or len(tb) < 8: continue
        obs = jsd(feat(tv, "neighbours"), feat(tb, "neighbours")); pool = tv + tb; null = []
        for _ in range(2000):
            idx = rng.permutation(len(pool)); A = [pool[i] for i in idx[:len(tv)]]; B = [pool[i] for i in idx[len(tv):]]
            null.append(jsd(feat(A, "neighbours"), feat(B, "neighbours")))
        rows.append({"variant": v, "base": b, "n_var": len(tv), "n_base": len(tb), "neighbours_p": round((1 + (np.array(null) >= obs).sum()) / 2001, 4)})
    cd = pd.DataFrame(rows); print("\nCONTROL: strong allographs (paragorth sign_allographs_levels.json)"); print(cd.to_string(index=False))
    print(f"control pairs whose neighbours differ (p < 0.05): {np.mean(cd.neighbours_p < 0.05):.2f} of {len(cd)}")
