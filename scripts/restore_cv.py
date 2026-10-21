"""Cross-validated restoration accuracy on the exploration split (holdout untouched).
Settings were chosen by a sweep on fold 0 (k=0.01, tri=0.15, slot=0.25, obj=0.25); results are reported on folds 1-4 only.
Hide each sign of each test text in turn; rank all known signs."""
import sys
from pathlib import Path
import numpy as np, pandas as pd
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from indus_workbench import data
from indus_workbench.restore import Restorer
W = {"bi": 1.0, "tri": 0.15, "slot": 0.25, "obj": 0.25}; K = 0.01
raw, _ = data.load_raw("indus_website")
c = data.build_corpus(raw, "indus_website", metadata=data.load_metadata("indus_website"), drop_damaged=True, dedupe=True, drop_unidentified=True)
ex = data.explore_only(c).df
ex = ex[ex.signs.map(len) >= 2].reset_index(drop=True)
fold = np.random.default_rng(0).integers(0, 5, len(ex))
models = ["unigram", "ngram", "structured"]
rows, conf = {m: [] for m in models}, []
for f in range(1, 5):
    tr, te = ex[fold != f], ex[fold == f]
    R = Restorer(k=K, weights=W).fit(list(tr.signs), list(tr.object_type))
    for s, o in zip(te.signs, te.object_type):
        s = list(s)
        for i in range(len(s)):
            for m in models:
                rk = R.rank_of(s, i, o, m); rows[m].append(rk if rk else 10**6)
            best, p = R.top(s, i, o, "structured", n=1)[0]
            conf.append((p, best == s[i]))
print("folds 1-4, hidden signs:", len(rows["ngram"]))
print(pd.DataFrame([{"model": m, "top1": (np.array(r) <= 1).mean(), "top5": (np.array(r) <= 5).mean(),
                     "top10": (np.array(r) <= 10).mean()} for m, r in rows.items()]).round(3).to_string(index=False))
cf = pd.DataFrame(conf, columns=["p", "right"])
cf["band"] = pd.cut(cf.p, [0, .2, .4, .6, .8, .9, 1.0])
print("\nconfidence of the top guess vs how often it is right:")
print(cf.groupby("band", observed=True).agg(gaps=("right", "size"), right=("right", "mean")).round(2).to_string())
for th in (0.6, 0.8, 0.9):
    sel = cf[cf.p >= th]; print(f"guesses with confidence >= {th}: {len(sel)/len(cf):.0%} of gaps, right {sel.right.mean():.0%}")
