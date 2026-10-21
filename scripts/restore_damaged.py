"""Propose restorations for real damaged inscriptions with exactly one lost interior sign.
Usage: python3 scripts/restore_damaged.py <inscriptions.csv from github.com/yajnadevam/lipi> [min_confidence]
Trained on the exploration split only; settings as in restore_cv.py. Lost signs are '000' in the ICIT text field;
texts must be complete at both ends ('+...+'), single-line, with one '000' not at either end."""
import sys
from pathlib import Path
import numpy as np, pandas as pd
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from indus_workbench import data
from indus_workbench.restore import Restorer
raw, _ = data.load_raw("indus_website")
c = data.build_corpus(raw, "indus_website", metadata=data.load_metadata("indus_website"), drop_damaged=True, dedupe=True, drop_unidentified=True)
ex = data.explore_only(c).df
R = Restorer(k=0.01, weights={"bi": 1.0, "tri": 0.15, "slot": 0.25, "obj": 0.25}).fit(list(ex.signs), list(ex.object_type))
L = pd.read_csv(sys.argv[1], dtype=str, keep_default_na=False)
th = float(sys.argv[2]) if len(sys.argv) > 2 else 0.8
OBJ = lambda t: "seal" if t.startswith("SEAL") else "tablet" if t.startswith("TAB") else "tag" if t.startswith("TAG") else "pottery" if t.startswith("POT") else "other"
out = []
for _, r in L.iterrows():
    t = r.text
    if not (t.startswith("+") and t.endswith("+")) or "/" in t:
        continue
    toks = t.strip("+").split("-")
    if toks.count("000") != 1:
        continue
    i = toks.index("000")
    if i in (0, len(toks) - 1) or len(toks) < 3:
        continue
    s = ["G" + str(int(x)) if x != "000" else "?" for x in toks]
    if any(x != "?" and x not in R.idx for x in s):
        continue
    top = R.top(s, i, OBJ(r.type), "structured", n=3)
    out.append({"icit_id": r.id, "cisi": r.cisi, "site": r.site, "object": r.type, "text": " ".join(s),
                "best": top[0][0], "confidence": round(top[0][1], 2),
                "alternatives": "; ".join(f"{g} {p:.2f}" for g, p in top[1:])})
d = pd.DataFrame(out).sort_values("confidence", ascending=False)
print(f"single-gap texts: {len(d)}; confidence >= {th}: {(d.confidence >= th).sum()}")
d.to_csv(Path(__file__).resolve().parents[1] / "results/restorations_single_gap.csv", index=False)
print(d[d.confidence >= th].head(40).to_string(index=False))
