"""Are rare signs local? Exploration only.
Rare = 2-6 uses in the exploration split (duplicates removed). Statistic: share of rare signs whose uses all come from
one site (and, within Mohenjo-daro/Harappa, one excavation area). Null: site (or area) labels permuted across texts,
2,000 times, which keeps each site's share of texts and each text's signs together.
Optional arg: ICIT export (github.com/yajnadevam/lipi) for excavation areas; metadata only."""
import sys, json
from pathlib import Path
from collections import Counter, defaultdict
import numpy as np, pandas as pd
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from indus_workbench import data
raw, _ = data.load_raw("indus_website")
c = data.build_corpus(raw, "indus_website", metadata=data.load_metadata("indus_website"), drop_damaged=True, dedupe=True, drop_unidentified=True)
ex = data.explore_only(c).df.reset_index(drop=True)   # EXPLORATION ONLY
cnt = Counter(x for s in ex.signs for x in s)
rare = {g for g, n in cnt.items() if 2 <= n <= 6}
print(f"texts {len(ex)}, rare signs (2-6 uses) {len(rare)}")
texts_of = defaultdict(list)
for i, s in enumerate(ex.signs):
    for g in set(s):
        if g in rare: texts_of[g].append(i)
rare = [g for g in rare if len(texts_of[g]) >= 2]     # used in 2+ different texts
def share_single(labels, signs):
    lab = np.asarray(labels)
    return np.mean([len(set(lab[texts_of[g]])) == 1 for g in signs])
r = np.random.default_rng(0)
def test(labels, signs, name, strata=None):
    obs = share_single(labels, signs); null = []
    lab = pd.Series(labels)
    for _ in range(2000):
        if strata is None: perm = r.permutation(lab.values)
        else: perm = lab.groupby(strata).transform(lambda v: pd.Series(r.permutation(v.values), index=v.index)).values
        null.append(share_single(perm, signs))
    null = np.array(null)
    print(f"{name}: rare signs used in one place only {obs:.3f} vs shuffled {null.mean():.3f}  (ratio {obs/null.mean():.2f}; p {(1+(null>=obs).sum())/2001:.4f}; n signs {len(signs)})")
    return obs, null.mean()
test(ex.site.values, rare, "SITE (all rare signs)")
# control: same test for common signs with few texts is impossible; instead compare rare signs vs mid-frequency signs (7-15 uses), split to 2-6 random uses? -> use object type as stratum to rule out object mix
test(ex.site.values, rare, "SITE, shuffled within object type", strata=ex.object_type.values)
if len(sys.argv) > 1:
    L = pd.read_csv(sys.argv[1], dtype=str, keep_default_na=False); L["icit"] = L.id.str.split(".").str[0]
    ex["icit"] = ex.text_id.str.lstrip("S"); ex = ex.merge(L.drop_duplicates("icit")[["icit", "area-section"]], on="icit", how="left")
    ex["area"] = ex["area-section"].fillna("").str.strip()
    for site in ("Mohenjo-daro", "Harappa"):
        idx = [i for i in range(len(ex)) if ex.site[i] == site and ex.area[i] not in ("", "-", "--")]
        sub = set(idx); sigs = [g for g in rare if sum(1 for t in texts_of[g] if t in sub) >= 2]
        tmp = {g: [t for t in texts_of[g] if t in sub] for g in sigs}
        lab = np.array(ex.area.values, dtype=object)
        def ss(labels): return np.mean([len(set(labels[tmp[g]])) == 1 for g in sigs])
        obs = ss(lab); null = []
        for _ in range(2000):
            l2 = lab.copy(); l2[idx] = r.permutation(lab[idx]); null.append(ss(l2))
        null = np.array(null)
        print(f"AREA within {site}: rare signs in one area only {obs:.3f} vs shuffled {null.mean():.3f} (ratio {obs/null.mean():.2f}; p {(1+(null>=obs).sum())/2001:.4f}; n signs {len(sigs)})")
