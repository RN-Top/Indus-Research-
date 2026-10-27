"""Twelve strokes (G55): seven readings tested side by side. Exploratory (all data already seen).
For each prediction, G55 is ranked against non-numeral signs with 15-120 uses (percentile; 50 = ordinary).
Material: ICIT export (all splits) + held-out-from-export set, deduplicated within site.
  YEAR       counted by a numeral right before it (G2 after an opener excluded)
  TITLE      shares a text with a man sign (G90, G91, G125)
  ROTATION   (a body of twelve, each member serving a month) the 3-sign window around the sign recurs in other texts
             that are otherwise different: a shared formula carried by many different holders
  GODS       (a group of deities) the text holds a copper-tablet picture-name phrase (copper_anchors.json)
  WATER      (a water god) the text holds the water sign G927 (Parpola: two wavy lines, 'water')
  RITUAL     (a ritual body) on moulded tablets, the offering-token class
  MERCHANT   (contracts and goods) on tags, labels for goods"""
import json, sys
from collections import Counter
from pathlib import Path
import numpy as np
import pandas as pd
ROOT = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT)); sys.path.insert(0, str(ROOT / "scripts"))
from indus_workbench import data  # noqa: E402
from number_system import VAL  # noqa: E402
from functional_skeleton import assign  # noqa: E402
MAN = {"G90", "G91", "G125"}
ANC = {tuple(x["anchor"].split()) for x in json.load(open(ROOT / "results/copper_anchors.json"))["anchors"]}
parts = []
for key in ("indus_website", "icit_new_to_export"):
    raw, _ = data.load_raw(key)
    parts.append(data.build_corpus(raw, key, drop_damaged=False, metadata=data.load_metadata(key)).df)
df = pd.concat(parts, ignore_index=True); df["key"] = df.signs.map(tuple); df = df.drop_duplicates(["site", "key"]).reset_index(drop=True)
raw, _ = data.load_raw("indus_website")
comp = data.explore_only(data.build_corpus(raw, "indus_website", drop_damaged=True, metadata=data.load_metadata("indus_website"))).df
roles, _ = assign([list(s) for s in comp.signs])
def isnum(s, k): return s[k] in VAL and not (s[k] == "G2" and k > 0 and roles.get(s[k - 1]) == 0)
def has_anchor(s): return any(tuple(s[i:i + n]) in ANC for n in (2, 3) for i in range(len(s) - n + 1))
seqs = [list(s) for s in df.signs]
use = Counter(x for s in seqs for x in s)
cands = [g for g, n in use.items() if 15 <= n <= 120 and g not in VAL and g not in MAN] + ["G55"]
def window(s, k): return tuple(s[max(0, k - 1):k + 2])
def measures(g):
    m = df.signs.map(lambda s: g in s); sub = df[m]
    tok = [(s, k) for s in seqs for k, x in enumerate(s) if x == g]
    wins = Counter(window(s, k) for s, k in tok)
    shared = np.mean([wins[window(s, k)] >= 2 for s, k in tok])  # texts are distinct (deduplicated), so a shared window = same formula, different rest
    return dict(
        YEAR=np.mean([k > 0 and isnum(s, k - 1) for s, k in tok]),
        TITLE=sub.signs.map(lambda s: bool(MAN & set(s))).mean(),
        ROTATION=shared,
        GODS=sub.signs.map(lambda s: has_anchor(list(s))).mean(),
        WATER=sub.signs.map(lambda s: "G927" in s).mean(),
        RITUAL=sub.object_type.eq("tablet").mean(),
        MERCHANT=sub.object_type.eq("tag").mean())
M = pd.DataFrame({g: measures(g) for g in cands}).T
out = [f"G55 ranked against {len(M) - 1} ordinary signs (15-120 uses). Percentile: 50 = ordinary.\n",
       f"{'reading':9} {'G55':>6} {'median':>7} {'pct':>6}"]
for c in M.columns:
    col = M[c]; v = M.loc["G55", c]
    pct = float((col < v).mean() * 100 + (col == v).mean() * 50)
    out.append(f"{c:9} {v:6.2f} {col.median():7.2f} {pct:6.1f}")
g = [list(s) for s in df.signs if "G55" in s]
w = Counter(window(s, k) for s in g for k, x in enumerate(s) if x == "G55")
out.append("\nShared G55 windows (formula, count of distinct texts): " + "; ".join(f"{' '.join(k)} {v}" for k, v in w.most_common(8) if v >= 2))
out.append(f"Texts with G927 (water) and G55: {[ ' '.join(s) for s in g if 'G927' in s]}")
print("\n".join(out)); (ROOT / "results/g55_group_models_output.txt").write_text("\n".join(out) + "\n")
