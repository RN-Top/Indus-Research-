"""Frozen replication (spec: predictions/laursen_pairs_2026-10-23.json) of the abroad-pairs test on Laursen's (2010)
Gulf Type seals, transcribed blind (data/laursen2010/foreign_inscriptions_laursen2010.csv). Run ONCE; --dry = counts only.

Included: region 'abroad'; not flagged pseudo-script, decoration or Linear Elamite; matches_exploration_text empty;
and sharing NO adjacent sign pair with any abroad text already analysed (exploration, holdout, held-out-from-export set)
from the same site (automatic, so already-used objects drop out without being read). Pairs containing NOMATCH are not
scored; a seal needs at least one scorable pair.
Score per seal: share of scorable pairs never seen in home exploration texts (same reference as abroad_pairs_test.py).
Controls: exactly the 334 small-home-site texts of abroad_pairs_test.py, scored the same way.
Statistic: mean rate (Laursen seals) minus mean rate (controls); labels permuted, 5,000 times; one-sided.
"""
import csv, hashlib, json, sys
from collections import Counter, defaultdict
from pathlib import Path
import numpy as np
ROOT = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT))
from indus_workbench import data  # noqa: E402
SPEC = ROOT / "predictions/laursen_pairs_2026-10-23.json"; OUT = ROOT / "results/laursen_pairs_test_2026-10-23.json"
spec = json.loads(SPEC.read_text()); body = {k: v for k, v in spec.items() if k != "sha256"}
assert hashlib.sha256(json.dumps(body, sort_keys=True).encode()).hexdigest() == spec["sha256"], "spec edited"
if OUT.exists(): sys.exit("already run once")
ap = json.loads((ROOT / "predictions/abroad_pairs_2026-10-23.json").read_text())
ABROAD, SMALL = set(ap["abroad_sites"]), set(ap["small_home_sites"])
raw, _ = data.load_raw("indus_website")
c = data.build_corpus(raw, "indus_website", drop_damaged=False, dedupe=True, metadata=data.load_metadata("indus_website")).df
rn, _ = data.load_raw("icit_new_to_export")
n = data.build_corpus(rn, "icit_new_to_export", drop_damaged=False, dedupe=True, metadata=data.load_metadata("icit_new_to_export")).df
pairs = lambda s: list(zip(s, s[1:]))
ex = c[c.split == "explore"]
ref_site = defaultdict(Counter)
for s, k in zip(ex.signs, ex.site):
    if k not in ABROAD: ref_site[k].update(pairs(list(s)))
allref = Counter()
for v in ref_site.values(): allref.update(v)
seen_pairs = defaultdict(set)
for df in (c, n):
    for s, k in zip(df.signs, df.site):
        if k in ABROAD: seen_pairs[k] |= set(pairs(list(s)))
BAD = ("PSEUDO", "DECORATION", "NON-INDUS")
keep = []
for r in csv.DictReader(open(ROOT / "data/laursen2010/foreign_inscriptions_laursen2010.csv")):
    if r["region"] != "abroad" or any(b in r["flags"] for b in BAD) or r["matches_exploration_text"].strip():
        continue
    s = r["sign_sequence_reading_order"].split()
    if set(pairs(s)) & seen_pairs.get(r["site"], set()):
        continue
    sc = [p for p in pairs(s) if "NOMATCH" not in p]
    if sc:
        keep.append((r["seal_no"], r["site"], sc))
ctl = []
for df in (c[c.split == "holdout"], n):
    for s, k in zip(df.signs, df.site):
        s = list(s)
        if len(s) >= 2 and k in SMALL:
            ref = allref - ref_site[k]; ctl.append(sum(ref[p] == 0 for p in pairs(s)) / (len(s) - 1))
print(f"Laursen seals kept: {len(keep)} (min {spec['min_seals']}); controls {len(ctl)}")
if "--dry" in sys.argv: sys.exit()
a = np.array([sum(allref[p] == 0 for p in sc) / len(sc) for _, _, sc in keep]); b = np.array(ctl)
obs = float(a.mean() - b.mean()); y = np.concatenate([a, b]); lab = np.array([1]*len(a) + [0]*len(b), bool)
rng = np.random.default_rng(spec["seed"])
null = np.array([(lambda q: y[q].mean() - y[~q].mean())(rng.permutation(lab)) for _ in range(spec["n_perm"])])
p = float((1 + np.sum(null >= obs)) / (len(null) + 1))
verdict = "Inconclusive (below minimum support)" if len(a) < spec["min_seals"] else ("Supported" if p < spec["alpha"] else "Not supported")
res = dict(spec_sha256=spec["sha256"], seals=len(a), laursen_mean=float(a.mean()), control_mean=float(b.mean()),
           difference=obs, p=p, verdict=verdict, kept=[(no, site, [" ".join(x) for x in sc]) for no, site, sc in keep])
OUT.write_text(json.dumps(res, indent=1)); print({k: v for k, v in res.items() if k != "kept"})
