"""Registered test (predictions/fish_jar_man_2026-10-27.json). Run ONCE."""
import csv, hashlib, json, sys
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.stats import fisher_exact
ROOT = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT))
from indus_workbench import data  # noqa: E402
SPEC = ROOT / "predictions/fish_jar_man_2026-10-27.json"; OUT = ROOT / "results/fish_jar_man_2026-10-27.json"
spec = json.loads(SPEC.read_text()); body = {k: v for k, v in spec.items() if k != "sha256"}
assert hashlib.sha256(json.dumps(body, sort_keys=True).encode()).hexdigest() == spec["sha256"], "spec edited"
if OUT.exists(): sys.exit("already run once")
ann = {r["sign"]: r for r in csv.DictReader(open(ROOT / "data/sign_marks/marks_blind_2026-10-20.csv"))}
par = {s: (s if r["base"] in ("self", "") else r["base"]) for s, r in ann.items()}
def fam(g):
    seen = set()
    while g in par and par[g] != g and g not in seen: seen.add(g); g = par[g]
    return g
FISH = {s for s in ann if fam(s) == "G220"} | {"G220"}; MAN = {"G90", "G91", "G125"}
raw, _ = data.load_raw("indus_website")
a = data.build_corpus(raw, "indus_website", drop_damaged=True, metadata=data.load_metadata("indus_website")).df
a = a[a.split.eq("holdout")]
rn, _ = data.load_raw("icit_new_to_export")
b = data.build_corpus(rn, "icit_new_to_export", drop_damaged=True, metadata=data.load_metadata("icit_new_to_export")).df
exp = {tuple(s) for s in data.explore_only(data.build_corpus(raw, "indus_website", drop_damaged=True, metadata=data.load_metadata("indus_website"))).df.signs}
seqs = [list(s) for s in {tuple(s) for s in pd.concat([a.signs, b.signs])} if tuple(s) not in exp]
A = [s for s in seqs if len(s) >= 3 and s[-2] == "G740" and s[-1] in MAN]
B = [s for s in seqs if len(s) >= 2 and s[-1] == "G740"]
fa = sum(s[-3] in FISH for s in A); fb = sum(s[-2] in FISH for s in B)
odds, p = fisher_exact([[fa, len(A) - fa], [fb, len(B) - fb]], alternative="greater")
lab = np.array([1] * len(A) + [0] * len(B)); y = np.array([s[-3] in FISH for s in A] + [s[-2] in FISH for s in B])
obs = y[lab == 1].mean() - y[lab == 0].mean(); rng = np.random.default_rng(20261027); ge = 0
for _ in range(10000):
    l = rng.permutation(lab); ge += (y[l == 1].mean() - y[l == 0].mean()) >= obs
pp = (1 + ge) / 10001
ok = len(A) >= 8
out = dict(spec_sha256=spec["sha256"], texts=len(seqs), A=len(A), A_fish=fa, B=len(B), B_fish=fb, diff=float(obs), fisher_p=float(p), perm_p=float(pp),
           A_texts=[" ".join(s) for s in A], verdict=("Supported" if p < 0.05 else "Not supported") if ok else "Inconclusive (too few)")
OUT.write_text(json.dumps(out, indent=1)); print({k: v for k, v in out.items() if k != "A_texts"}); print("\n".join(out["A_texts"]))
