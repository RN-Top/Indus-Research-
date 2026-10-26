"""Leave-one-site-out test of the inscription layout (spec: predictions/loso_template_2026-10-26.json). Run ONCE.

For each test site S (frozen list in the spec): learn sign roles (opener / middle / closer, numerals by shape) with the
frozen rule of scripts/functional_skeleton.py from the texts of ALL OTHER sites, then test on S's texts whether they follow
the slot order opener -> middle -> closer more often than the same texts with signs shuffled within each text
(hypotheses kind template_order, 2,000 shuffles). Texts: complete texts of the export (all splits) plus complete texts of
the held-out-from-export set, deduplicated, abroad sites excluded.
Primary: Stouffer's combination of the per-site one-sided p-values (one-sided). Secondary: number of sites with p < 0.05.
"""
import hashlib, json, sys
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.stats import norm
ROOT = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT)); sys.path.insert(0, str(ROOT / "scripts"))
from indus_workbench import data, hypotheses as hy  # noqa: E402
from functional_skeleton import assign  # noqa: E402
SPEC = ROOT / "predictions/loso_template_2026-10-26.json"; OUT = ROOT / "results/loso_template_2026-10-26.json"
ABROAD = set(json.loads((ROOT / "predictions/abroad_pairs_2026-10-23.json").read_text())["abroad_sites"])
def corpus():
    raw, _ = data.load_raw("indus_website")
    a = data.build_corpus(raw, "indus_website", drop_damaged=True, dedupe=False, metadata=data.load_metadata("indus_website")).df
    rn, _ = data.load_raw("icit_new_to_export")
    b = data.build_corpus(rn, "icit_new_to_export", drop_damaged=True, dedupe=False, metadata=data.load_metadata("icit_new_to_export")).df
    df = pd.concat([a[["signs", "site"]], b[["signs", "site"]]], ignore_index=True)
    df = df[~df.site.isin(ABROAD) & (df.site != "Unknown")]
    df["key"] = df.signs.map(tuple)
    return df.drop_duplicates("key").reset_index(drop=True)
df = corpus()
if "--sites" in sys.argv:  # used once, before freezing, to fix the site list (counts only)
    print(df.site.value_counts().to_dict()); sys.exit()
spec = json.loads(SPEC.read_text()); body = {k: v for k, v in spec.items() if k != "sha256"}
assert hashlib.sha256(json.dumps(body, sort_keys=True).encode()).hexdigest() == spec["sha256"], "spec edited"
if OUT.exists(): sys.exit("already run once")
res = []
for i, S in enumerate(spec["test_sites"]):
    train = [list(s) for s in df[df.site != S].signs]
    roles, _ = assign(train)
    ops = sorted(x for x, r in roles.items() if r == 0); mid = sorted(x for x, r in roles.items() if r == 1); cl = sorted(x for x, r in roles.items() if r == 2)
    h = hy.new_hypothesis("template_order", dict(openers=ops, middle=mid, closers=cl), f"LOSO {S}", n_perm=spec["n_perm"], seed=spec["seed"] + i)
    r = hy.run_test(h, df[df.site == S].reset_index(drop=True))
    res.append(dict(site=S, texts=int((df.site == S).sum()), observed=r.observed, null=r.null_mean, p=r.p_value, support=r.n_support))
    print(f"{S:16} texts {res[-1]['texts']:4}  conform {r.observed:.2f} vs shuffled {r.null_mean:.2f}  p {r.p_value:.4f}  scored {r.n_support}", flush=True)
ps = np.array([x["p"] for x in res if x["p"] == x["p"]])
z = norm.isf(np.clip(ps, 1e-12, 1)); comb = float(norm.sf(z.sum() / np.sqrt(len(z))))
out = dict(spec_sha256=spec["sha256"], sites=res, stouffer_p=comb, sites_p_below_005=int((ps < 0.05).sum()), n_sites=len(ps),
           verdict="Supported" if comb < spec["alpha"] else "Not supported")
OUT.write_text(json.dumps(out, indent=1, default=float)); print({k: v for k, v in out.items() if k != "sites"})
