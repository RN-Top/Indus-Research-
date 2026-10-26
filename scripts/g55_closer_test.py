"""Pre-registered test (spec predictions/g55_closer_2026-10-26.json). Run ONCE."""
import hashlib, json, sys
from pathlib import Path
import numpy as np
ROOT = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT)); sys.path.insert(0, str(ROOT / "scripts"))
from indus_workbench import data  # noqa: E402
from functional_skeleton import assign  # noqa: E402
SPEC = ROOT / "predictions/g55_closer_2026-10-26.json"; OUT = ROOT / "results/g55_closer_2026-10-26.json"
spec = json.loads(SPEC.read_text()); body = {k: v for k, v in spec.items() if k != "sha256"}
assert hashlib.sha256(json.dumps(body, sort_keys=True).encode()).hexdigest() == spec["sha256"], "spec edited"
if OUT.exists(): sys.exit("already run once")
raw, _ = data.load_raw("indus_website")
comp = data.explore_only(data.build_corpus(raw, "indus_website", drop_damaged=True, metadata=data.load_metadata("indus_website"))).df
roles, _ = assign([list(s) for s in comp.signs])
rn, _ = data.load_raw("icit_new_to_export")
df = data.build_corpus(rn, "icit_new_to_export", drop_damaged=False, metadata=data.load_metadata("icit_new_to_export")).df
seqs = list({tuple(s) for s in df.signs})
OTHER = {"G13", "G14", "G15", "G16", "G17", "G18", "G19", "G27", "G28", "G29"}
lab, clo, mid = [], [], []
for s in seqs:
    for k, x in enumerate(s[:-1]):
        if x == "G55" or x in OTHER:
            lab.append(x == "G55"); r = roles.get(s[k + 1]); clo.append(r == 2); mid.append(r == 1)
lab, clo, mid = map(np.array, (lab, clo, mid))
def d(l, y): return y[l].mean() - y[~l].mean()
obs = d(lab, clo); rng = np.random.default_rng(spec["seed"])
null = np.array([d(rng.permutation(lab), clo) for _ in range(spec["n_perm"])])
p = (1 + (null >= obs).sum()) / (1 + spec["n_perm"])
obs_m = d(lab, mid); null_m = np.array([d(rng.permutation(lab), mid) for _ in range(spec["n_perm"])])
p_m = (1 + (null_m <= obs_m).sum()) / (1 + spec["n_perm"])
ok = lab.sum() >= spec["min_g55_scored"]
out = dict(spec_sha256=spec["sha256"], g55_scored=int(lab.sum()), other_scored=int((~lab).sum()),
           g55_closer=float(clo[lab].mean()), other_closer=float(clo[~lab].mean()), diff=float(obs), null_mean=float(null.mean()), p=float(p),
           g55_middle=float(mid[lab].mean()), other_middle=float(mid[~lab].mean()), secondary_p=float(p_m),
           verdict=("Supported" if p < spec["alpha"] else "Not supported") if ok else "Inconclusive (too few)")
OUT.write_text(json.dumps(out, indent=1)); print(out)
