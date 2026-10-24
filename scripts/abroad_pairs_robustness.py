"""Robustness after the run (descriptive): is the abroad effect only rare signs?
Same texts and reference as scripts/abroad_pairs_test.py, but only pairs whose BOTH signs are common at home
(20+ uses in home exploration texts) are scored. Not confirmatory."""
import json, sys
from collections import Counter, defaultdict
from pathlib import Path
import numpy as np
ROOT = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT))
from indus_workbench import data  # noqa: E402
spec = json.loads((ROOT / "predictions/abroad_pairs_2026-10-23.json").read_text())
ABROAD, SMALL = set(spec["abroad_sites"]), set(spec["small_home_sites"])
raw, _ = data.load_raw("indus_website")
c = data.build_corpus(raw, "indus_website", drop_damaged=False, dedupe=True, metadata=data.load_metadata("indus_website")).df
rn, _ = data.load_raw("icit_new_to_export")
n = data.build_corpus(rn, "icit_new_to_export", drop_damaged=False, dedupe=True, metadata=data.load_metadata("icit_new_to_export")).df
ex = c[c.split == "explore"]
ref_site, use_site = defaultdict(Counter), defaultdict(Counter)
for s, k in zip(ex.signs, ex.site):
    if k not in ABROAD:
        s = list(s); ref_site[k].update(zip(s, s[1:])); use_site[k].update(s)
allref, alluse = Counter(), Counter()
for k in ref_site:
    allref.update(ref_site[k]); alluse.update(use_site[k])
def score(s, ref, use):
    ps = [p for p in zip(s, s[1:]) if use[p[0]] >= 20 and use[p[1]] >= 20]
    return [ref[p] == 0 for p in ps]
A, B = [], []
for df in (c[c.split == "holdout"], n):
    for s, k in zip(df.signs, df.site):
        s = list(s)
        if len(s) < 2: continue
        if k in ABROAD: A += score(s, allref, alluse)
        elif k in SMALL: B += score(s, allref - ref_site[k], alluse - use_site[k])
A, B = np.array(A, float), np.array(B, float)
y = np.concatenate([A, B]); lab = np.array([1]*len(A) + [0]*len(B), bool); r = np.random.default_rng(1)
obs = A.mean() - B.mean(); null = [(lambda q: y[q].mean() - y[~q].mean())(r.permutation(lab)) for _ in range(5000)]
print(f"Pairs of two common signs: abroad {len(A)} pairs, unattested {A.mean():.2f}; small home sites {len(B)} pairs, {B.mean():.2f}; "
      f"diff {obs:+.2f}, p {(1+sum(np.array(null)>=obs))/5001:.4f} (pairs permuted)")
