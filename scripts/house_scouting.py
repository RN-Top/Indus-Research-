"""Do seals found in the same house share features? Exploration only.
Usage: python3 scripts/house_scouting.py <inscriptions.csv from github.com/yajnadevam/lipi>
House = site + area-section + block-house from the ICIT export (metadata only). Null: house labels permuted within
site+area, so the comparison is same house vs other houses of the same excavation area."""
import sys, json
from pathlib import Path
import numpy as np, pandas as pd
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from indus_workbench import data
raw, _ = data.load_raw("indus_website")
c = data.build_corpus(raw, "indus_website", metadata=data.load_metadata("indus_website"), drop_damaged=True, dedupe=False, drop_unidentified=True)
ex = data.explore_only(c).df.copy()   # EXPLORATION ONLY
L = pd.read_csv(sys.argv[1], dtype=str, keep_default_na=False); L["icit"] = L.id.str.split(".").str[0]
ex["icit"] = ex.text_id.str.lstrip("S")
m = ex.merge(L.drop_duplicates("icit")[["icit", "area-section", "block-house", "room-grid"]], on="icit", how="left")
P = json.load(open(Path(__file__).resolve().parents[1] / "hypotheses/H-2026-10-16-51b7445b.json"))["params"]
O, C = set(P["openers"]), set(P["closers"])
s = m[(m.object_type == "seal") & (m.signs.map(len) >= 2)].copy()
bad = {"", "-", "--"}
s["area"] = s["area-section"].str.strip(); s["house"] = s["block-house"].str.strip()
s = s[~s.area.isin(bad) & ~s.house.isin(bad)]
s["hk"] = s.site + "|" + s.area + "|" + s.house; s["ak"] = s.site + "|" + s.area
s = s[s.hk.map(s.hk.value_counts()) >= 2]
s = s[s.ak.map(s.groupby("ak").hk.nunique()) >= 2].reset_index(drop=True)
print(f"seals in houses with 2+ seals, in areas with 2+ such houses: {len(s)}; houses {s.hk.nunique()}; areas {s.ak.nunique()}")
print(s.groupby("site").hk.nunique().to_dict())
feat = {
  "same opener": [x[0] if x[0] in O else None for x in s.signs],
  "same first sign": [x[0] for x in s.signs],
  "same final sign": [x[-1] for x in s.signs],
  "same animal": [mo.split(":")[0] if mo not in ("unknown", "") else None for mo in s.motif],
  "same text": [" ".join(x) for x in s.signs],
}
S = [set(x) for x in s.signs]; n = len(S)
iu = np.triu_indices(n, 1)
J = np.array([len(S[i] & S[j]) / len(S[i] | S[j]) for i, j in zip(*iu)])
area = s.ak.values
same_area = (area[iu[0]] == area[iu[1]])
r = np.random.default_rng(0)
def stat(vals, house):
    h = np.asarray(house); same = (h[iu[0]] == h[iu[1]]) & same_area; other = same_area & ~same
    if vals is J:
        return J[same].mean() - J[other].mean()
    v = np.array(vals, dtype=object); ok = np.array([a is not None and b is not None for a, b in zip(v[iu[0]], v[iu[1]])])
    eq = np.array([a == b for a, b in zip(v[iu[0]], v[iu[1]])])
    return eq[same & ok].mean() - eq[other & ok].mean()
house = s.hk.values
rows = []
for name, vals in [("sign overlap (Jaccard)", J)] + list(feat.items()):
    obs = stat(vals, house)
    null = []
    for _ in range(1000):
        hp = s.groupby("ak").hk.transform(lambda v: pd.Series(r.permutation(v.values), index=v.index)).values
        null.append(stat(vals, hp))
    null = np.array(null)
    rows.append({"feature": name, "same house minus other houses": round(obs, 4), "null mean": round(null.mean(), 4),
                 "p (one-sided)": round((1 + (null >= obs).sum()) / 1001, 4)})
print(pd.DataFrame(rows).to_string(index=False))
