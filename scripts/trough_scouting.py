"""Does the feeding trough go with different texts? (scouting, EXPLORATION split only)

Mukhopadhyay (2023, HSSC 10:972, p. 17) reads the trough in front of an animal as marking a "tax-receiving" entity.
If the trough marks a role, seal texts with a trough should differ from texts without one for the same animal.
The two-layer reading (paper 3: text independent of image) predicts no difference.

Trough from the ICIT export column 'cult' ("Trough"); no trough = "None"; '-' and others excluded.
Unicorns (Bull1*) are excluded: they carry the standard, not the trough.
Statistic: size-weighted Jensen-Shannon divergence of sign-token distributions, trough vs none,
summed over animal x site cells that have both. Null: trough labels permuted within cells.
Also: mean text length difference and first/last-sign divergence.
Usage: python3 scripts/trough_scouting.py <icit inscriptions.csv>
"""
import sys
from collections import Counter
from pathlib import Path
import numpy as np, pandas as pd
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from indus_workbench import data

L = pd.read_csv(sys.argv[1], dtype=str, keep_default_na=False)
L["icit"] = L.id.str.split(".").str[0]
L = L.drop_duplicates("icit")
raw, _ = data.load_raw("indus_website")
c = data.build_corpus(raw, "indus_website", metadata=data.load_metadata("indus_website"),
                      drop_damaged=True, dedupe=True, drop_unidentified=True)
d = data.explore_only(c).df.copy()
d["icit"] = d.text_id.str.lstrip("S")
d = d.merge(L[["icit", "cult", "symbol", "type"]], on="icit", how="left")
d = d[d.object_type.isin(["seal"]) & ~d.motif.astype(str).str.startswith("Bull1") & (d.signs.map(len) >= 1)]
d = d[d.cult.isin(["Trough", "None"])].copy()
d["T"] = d.cult.eq("Trough")
d["cell"] = d.motif.astype(str) + "|" + d.site.astype(str)
print("exploration seals by animal (trough / none):")
print(d.groupby("motif").T.agg(["sum", "count"]).assign(none=lambda x: x["count"] - x["sum"]).sort_values("count", ascending=False).head(12))
d = d[d.groupby("cell").T.transform(lambda s: s.any() and not s.all())]
print("cells with both:", d.cell.nunique(), " seals:", len(d), " trough:", int(d["T"].sum()), " none:", int((~d["T"]).sum()))
print(d.groupby("cell").T.agg(["sum", "count"]))

def jsd(a, b):
    keys = set(a) | set(b); p = np.array([a[k] for k in keys], float); q = np.array([b[k] for k in keys], float)
    p /= p.sum(); q /= q.sum(); m = (p + q) / 2
    kl = lambda x, y: np.sum(x[x > 0] * np.log2(x[x > 0] / y[x > 0]))
    return 0.5 * kl(p, m) + 0.5 * kl(q, m)

def stat(T, f):
    num = den = 0.0
    for _, x in d.assign(T=T).groupby("cell"):
        a = Counter(t for s in x.signs[x["T"]] for t in f(s)); b = Counter(t for s in x.signs[~x["T"]] for t in f(s))
        if a and b:
            n = len(x); num += n * jsd(a, b); den += n
    return num / den
feats = {"all signs": lambda s: s, "first sign": lambda s: s[:1], "last sign": lambda s: s[-1:]}
rng = np.random.default_rng(20261029)
perms = [d.groupby("cell")["T"].transform(lambda s: pd.Series(rng.permutation(s.values), index=s.index)).values for _ in range(2000)]
for name, f in feats.items():
    obs = stat(d["T"].values, f); null = np.array([stat(P, f) for P in perms])
    print(f"{name:11s} JSD obs {obs:.3f} null mean {null.mean():.3f}  p(greater) {(1 + (null >= obs).sum()) / 2001:.3f}")
L_ = d.signs.map(len)
print("mean length trough %.2f vs none %.2f" % (L_[d["T"]].mean(), L_[~d["T"]].mean()))
