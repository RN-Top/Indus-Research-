"""G55 (twelve strokes, 4/4/4) across the corpus: number, unit or name part? Scouting, EXPLORATION split only.
Abroad: 5 Gulf seals carry G55, three of them next to a man sign (data/abroad/README.md). At home, does G55 behave
like the other stacked numerals (precede a counted sign, sit mid-text) or differently (sit by man signs, end texts,
stand where names stand)? Compared with every other stacked numeral (G13-G19, G27-G29) with 10+ uses.
Neighbours use incomplete texts too; positions use complete texts only. The held-out-from-export set is not read."""
import csv, json, sys
from collections import Counter, defaultdict
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT)); sys.path.insert(0, str(ROOT / "scripts"))
from indus_workbench import data  # noqa: E402
from functional_skeleton import assign  # noqa: E402
from number_system import VAL  # noqa: E402
MAN = {"G90", "G91", "G125"}
STACK = ["G13", "G14", "G15", "G16", "G17", "G18", "G19", "G27", "G28", "G29", "G55"]
raw, _ = data.load_raw("indus_website"); md = data.load_metadata("indus_website")
full = data.explore_only(data.build_corpus(raw, "indus_website", drop_damaged=False, metadata=md)).df
comp = data.explore_only(data.build_corpus(raw, "indus_website", drop_damaged=True, metadata=md)).df
roles, _ = assign([list(s) for s in comp.signs])
R = {0: "opener", 1: "middle", 2: "closer"}
def cls(x):
    if x is None: return "edge"
    if x in VAL: return "numeral"
    if x in MAN: return "man"
    return R.get(roles.get(x), "rare/unroled")
use = Counter(x for s in full.signs for x in s)
def profile(g):
    L, Rn, Lc, Rc, sites = Counter(), Counter(), Counter(), Counter(), Counter(); pos = Counter(); n = 0
    for s, site in zip(full.signs, full.site):
        s = list(s)
        for k, x in enumerate(s):
            if x != g: continue
            n += 1; sites[site] += 1
            l = s[k - 1] if k else None; r = s[k + 1] if k + 1 < len(s) else None
            L[l] += 1; Rn[r] += 1; Lc[cls(l)] += 1; Rc[cls(r)] += 1
    for s in comp.signs:
        s = list(s)
        for k, x in enumerate(s):
            if x == g and len(s) > 1:
                pos["first" if k == 0 else "last" if k == len(s) - 1 else "inside"] += 1
    return dict(n=n, left=L, right=Rn, left_cls=Lc, right_cls=Rc, sites=sites, pos=pos)
P = {g: profile(g) for g in STACK if use[g] >= 10 or g == "G55"}
def sh(c, k): t = sum(c.values()); return c[k] / t if t else float("nan")
lines = ["Sign  uses  right=counted(middle)  right=closer  right=edge  left=opener  left=man|right=man  first/inside/last (complete)"]
for g, p in P.items():
    man = (p["left_cls"]["man"] + p["right_cls"]["man"]) / p["n"]
    lines.append(f"{g:5} {p['n']:4}  {sh(p['right_cls'],'middle'):.2f}  {sh(p['right_cls'],'closer'):.2f}  {sh(p['right_cls'],'edge'):.2f}"
                 f"  {sh(p['left_cls'],'opener'):.2f}  {man:.2f}  {p['pos']['first']}/{p['pos']['inside']}/{p['pos']['last']}")
g = P["G55"]
lines += ["", "G55 left neighbours: " + str(g["left"].most_common(10)), "G55 right neighbours: " + str(g["right"].most_common(10)),
          "G55 left classes: " + str(dict(g["left_cls"])), "G55 right classes: " + str(dict(g["right_cls"])),
          "G55 sites (exploration): " + str(dict(g["sites"])), "", "G55 texts (exploration):"]
for s, site, tid in zip(full.signs, full.site, full.text_id):
    if "G55" in s: lines.append(f"  {tid:10} {site:14} {' '.join(s)}")
lines += ["", "Abroad texts with G55:"]
for r in csv.DictReader(open(ROOT / "data/abroad/abroad_inscriptions.csv")):
    if "G55" in r["signs"].split(): lines.append(f"  {r['id']:10} {r['site']:14} {r['signs']}   man: {r['man_signs']}")
# home: G55 next to a man sign vs other stacked numerals pooled
ctl = [p for k, p in P.items() if k != "G55"]
cm = sum(p["left_cls"]["man"] + p["right_cls"]["man"] for p in ctl); cn = sum(p["n"] for p in ctl)
lines.append(f"\nHome next to a man sign: G55 {g['left_cls']['man'] + g['right_cls']['man']}/{g['n']}; other stacked numerals {cm}/{cn}")
out = "\n".join(lines); print(out); (ROOT / "results/g55_scouting_output.txt").write_text(out + "\n")
