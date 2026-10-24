"""Frozen test (spec: predictions/rare_compound_2026-10-23.json): rare built signs keep their own base's neighbours
on the locked holdout. Run ONCE; refuses if the result exists. --dry prints the support only.

Everything is fixed from the EXPLORATION split (same settings as scripts/rare_middle_scouting.py):
  rare built signs = 5 or fewer exploration uses, a base in the blind annotation, base with 10+ exploration uses;
  each base's neighbour sets = its 10 commonest left and 10 commonest right neighbours in exploration ('#' = edge).
Scored on the HOLDOUT: each holdout token of a rare built sign is a hit if its left neighbour is in its base's left set
or its right neighbour is in its base's right set. Statistic: hit rate with the true bases minus the mean hit rate
with bases shuffled among the rare built signs (the null, 5,000 shuffles). One-sided.
"""
import csv, hashlib, json, sys
from collections import Counter, defaultdict
from pathlib import Path
import numpy as np
ROOT = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT)); sys.path.insert(0, str(ROOT / "scripts"))
from indus_workbench import data  # noqa: E402
from functional_slots import DS  # noqa: E402
SPEC = ROOT / "predictions/rare_compound_2026-10-23.json"; OUT = ROOT / "results/rare_compound_test_2026-10-23.json"
spec = json.loads(SPEC.read_text()); body = {k: v for k, v in spec.items() if k != "sha256"}
assert hashlib.sha256(json.dumps(body, sort_keys=True).encode()).hexdigest() == spec["sha256"], "spec edited"
if OUT.exists(): sys.exit("already run once")
raw, _ = data.load_raw("indus_website")
c = data.build_corpus(raw, "indus_website", metadata=data.load_metadata("indus_website"), **DS).df
ex = [list(s) for s in c[c.split == "explore"].signs]; ho = [list(s) for s in c[c.split == "holdout"].signs]
use = Counter(x for s in ex for x in s)
ann = {r["sign"]: r for r in csv.DictReader(open(ROOT / "data/sign_marks/marks_blind_2026-10-20.csv"))}
base = {g: r["base"] for g, r in ann.items() if r["base"] not in ("self", "") and r["base"] != g}
rb = sorted(g for g in base if 0 < use[g] <= 5 and use[base[g]] >= 10)
assert rb == spec["rare_built_signs"], "list differs from the frozen one"
L, R = defaultdict(Counter), defaultdict(Counter)
for s in ex:
    for k, x in enumerate(s):
        L[x][s[k-1] if k else "#"] += 1; R[x][s[k+1] if k+1 < len(s) else "#"] += 1
topL = {b: {k for k, _ in L[b].most_common(10)} for b in set(base[g] for g in rb)}
topR = {b: {k for k, _ in R[b].most_common(10)} for b in set(base[g] for g in rb)}
toks = [(x, s[k-1] if k else "#", s[k+1] if k+1 < len(s) else "#") for s in ho for k, x in enumerate(s) if x in set(rb)]
print(f"holdout tokens of the {len(rb)} rare built signs: {len(toks)} (min support {spec['min_support']})")
if "--dry" in sys.argv: sys.exit()
def hit(assign):
    return np.mean([l in topL[assign[x]] or r_ in topR[assign[x]] for x, l, r_ in toks])
own = {g: base[g] for g in rb}; obs = hit(own)
rng = np.random.default_rng(spec["seed"]); bl = [own[g] for g in rb]
null = np.array([hit(dict(zip(rb, rng.permutation(bl)))) for _ in range(spec["n_perm"])])
p = float((1 + np.sum(null >= obs)) / (len(null) + 1))
verdict = "Inconclusive (below minimum support)" if len(toks) < spec["min_support"] else ("Supported" if p < spec["alpha"] else "Not supported")
res = dict(spec_sha256=spec["sha256"], tokens=len(toks), hit_own_base=float(obs), hit_shuffled_mean=float(null.mean()),
           difference=float(obs - null.mean()), p=p, verdict=verdict)
OUT.write_text(json.dumps(res, indent=1)); print(res)
