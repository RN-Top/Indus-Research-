"""Frozen test (spec: predictions/abroad_pairs_2026-10-23.json): inscriptions found abroad use sign pairs never seen
at home more often than texts from small home sites. Run ONCE; refuses if the result file exists.

Procedure identical to scripts/abroad_pairs_scouting.py, except which texts are scored:
  reference   = exploration texts from home sites (the export's exploration split; never test data)
  test texts  = texts of 2+ signs from sites abroad, from (a) the export's locked holdout and (b) the
                held-out-from-export set (data/icit_merged_paragorth/new_to_export_corpus.csv); damaged kept
  controls    = texts of 2+ signs from the frozen list of small home sites, from the same two sources,
                each scored against the reference minus its own site
Statistic: mean unattested-pair rate (abroad) minus (controls). Null: labels permuted over texts, 5,000 times. One-sided.
"""
import hashlib, json, sys
from collections import Counter, defaultdict
from pathlib import Path
import numpy as np
ROOT = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT))
from indus_workbench import data  # noqa: E402
SPEC = ROOT / "predictions/abroad_pairs_2026-10-23.json"; OUT = ROOT / "results/abroad_pairs_test_2026-10-23.json"
spec = json.loads(SPEC.read_text())
body = {k: v for k, v in spec.items() if k != "sha256"}
assert hashlib.sha256(json.dumps(body, sort_keys=True).encode()).hexdigest() == spec["sha256"], "spec edited after freezing"
if OUT.exists() and "--dry" not in sys.argv:
    sys.exit("already run once")
ABROAD, SMALL = set(spec["abroad_sites"]), set(spec["small_home_sites"])
raw, _ = data.load_raw("indus_website")
c = data.build_corpus(raw, "indus_website", drop_damaged=False, dedupe=True, metadata=data.load_metadata("indus_website")).df
rn, _ = data.load_raw("icit_new_to_export")
n = data.build_corpus(rn, "icit_new_to_export", drop_damaged=False, dedupe=True, metadata=data.load_metadata("icit_new_to_export")).df
pairs = lambda s: list(zip(s, s[1:]))
ref_site = defaultdict(Counter)
for s, site in zip(c[c.split == "explore"].signs, c[c.split == "explore"].site):
    if site not in ABROAD:
        ref_site[site].update(pairs(list(s)))
allref = Counter()
for v in ref_site.values():
    allref.update(v)
if "--dry" in sys.argv:  # counts only, no rates
    hold = c[c.split == "holdout"]
    for name, df in (("holdout", hold), ("new set", n)):
        a = sum(1 for s, k in zip(df.signs, df.site) if k in ABROAD and len(s) >= 2)
        b = sum(1 for s, k in zip(df.signs, df.site) if k in SMALL and len(s) >= 2)
        print(f"{name}: abroad texts {a}, small-home control texts {b}")
    sys.exit()
rate = lambda s, ref: sum(ref[p] == 0 for p in pairs(s)) / (len(s) - 1)
ab, ctl = [], []
for name, df in (("holdout", c[c.split == "holdout"]), ("new set", n)):
    for s, k in zip(df.signs, df.site):
        s = list(s)
        if len(s) < 2:
            continue
        if k in ABROAD:
            ab.append((name, k, " ".join(s), rate(s, allref)))
        elif k in SMALL:
            ctl.append((name, k, " ".join(s), rate(s, allref - ref_site[k])))
a = np.array([x[-1] for x in ab]); b = np.array([x[-1] for x in ctl])
obs = float(a.mean() - b.mean()); y = np.concatenate([a, b]); lab = np.array([1] * len(a) + [0] * len(b), bool)
r = np.random.default_rng(spec["seed"])
null = np.array([(lambda q: y[q].mean() - y[~q].mean())(r.permutation(lab)) for _ in range(spec["n_perm"])])
p = float((1 + np.sum(null >= obs)) / (len(null) + 1))
verdict = ("Inconclusive (below minimum support)" if len(a) < spec["min_abroad_texts"] else
           "Supported" if p < spec["alpha"] else "Not supported")
res = dict(spec_sha256=spec["sha256"], abroad_texts=len(a), control_texts=len(b), abroad_mean=float(a.mean()),
           control_mean=float(b.mean()), difference=obs, p=p, null_mean=float(null.mean()), verdict=verdict, abroad=ab)
OUT.write_text(json.dumps(res, indent=1))
print(f"abroad {len(a)} texts, mean {a.mean():.2f}; controls {len(b)} texts, mean {b.mean():.2f}; diff {obs:+.2f}; p {p:.4f} -> {verdict}")
for x in ab:
    print("  ", x)
