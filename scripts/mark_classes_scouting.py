"""Outside vs inside vs both vs top marks: where do marked signs sit compared with their plain bases? Exploration only.
Classes fixed before computing: OUTER = enclosure_strokes, brackets, side_strokes_*; INNER = inner_line, inner_dot,
crossbar; TOP = roof, antennae, top_strokes_*. A variant is outer-only, inner-only, both (outer and inner) or top-only."""
import sys, csv, json
from pathlib import Path
import numpy as np, pandas as pd
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from indus_workbench import data, hypotheses as hy
ROOT = Path(__file__).resolve().parents[1]
raw, _ = data.load_raw("indus_website")
c = data.build_corpus(raw, "indus_website", metadata=data.load_metadata("indus_website"), drop_damaged=True, dedupe=True, drop_unidentified=True)
seqs = [list(s) for s in data.explore_only(c).df.signs if len(s) >= 2]   # EXPLORATION ONLY
closers = set(json.load(open(ROOT / "hypotheses/H-2026-10-16-51b7445b.json"))["params"]["closers"])
OUTER = lambda m: m == "enclosure_strokes" or m == "brackets" or m.startswith("side_strokes")
INNER = lambda m: m in ("inner_line", "inner_dot", "crossbar")
TOP = lambda m: m in ("roof", "antennae") or m.startswith("top_strokes")
pairs = {"outer only": [], "inner only": [], "both": [], "top only": []}
for r in csv.DictReader(open(ROOT / "data/sign_marks/marks_blind_2026-10-20.csv")):
    if r["base"] in ("self", "") or r["base"] == r["sign"]:
        continue
    ms = [m for m in r["marks"].split(";") if m]
    o, i, t = any(map(OUTER, ms)), any(map(INNER, ms)), any(map(TOP, ms))
    cls = "both" if o and i else "outer only" if o else "inner only" if i else "top only" if t else None
    if cls: pairs[cls].append((r["sign"], r["base"]))
end = hy._end_region_tokens(seqs, closers)
start, relpos = {}, {}
for s in seqs:
    n = len(s)
    for k, x in enumerate(s):
        start.setdefault(x, []).append(int(k == 0)); relpos.setdefault(x, []).append(k / (n - 1))
def wdiff(flags, prs):
    num = den = 0.0; nv = 0
    for v, b in prs:
        fv, fb = flags.get(v, []), flags.get(b, [])
        if not fv or not fb: continue
        num += len(fv) * (np.mean(fv) - np.mean(fb)); den += len(fv); nv += len(fv)
    return (num / den if den else np.nan), nv
r = np.random.default_rng(0)
rows = []
for cls, prs in pairs.items():
    for name, flags in [("end region", end), ("first position", start), ("relative position", relpos)]:
        obs, nv = wdiff(flags, prs)
        null = []
        for _ in range(2000):
            f2 = dict(flags)
            for v, b in prs:
                fv, fb = flags.get(v, []), flags.get(b, [])
                if not fv or not fb: continue
                pool = r.permutation(np.array(fv + fb, dtype=float)); f2[v], f2[b] = list(pool[:len(fv)]), list(pool[len(fv):])
            null.append(wdiff(f2, prs)[0])
        null = np.array(null)
        p2 = (1 + (np.abs(null) >= abs(obs)).sum()) / 2001
        rows.append({"class": cls, "pairs used": sum(1 for v, b in prs if v in flags and b in flags), "marked tokens": nv,
                     "measure": name, "marked minus base": round(obs, 3), "p (two-sided)": round(p2, 4)})
print(pd.DataFrame(rows).to_string(index=False))

# --- consistency: per pair (marked sign with 4+ uses), does it sit later (relative position) than its base?
from scipy.stats import binomtest
print("\nper-pair consistency (marked signs with 4+ uses): later than base / earlier than base; sign test")
for cls, prs in pairs.items():
    later = earlier = 0; fam = {}
    for v, b in prs:
        if len(relpos.get(v, [])) >= 4 and b in relpos:
            d = np.mean(relpos[v]) - np.mean(relpos[b])
            later += d > 0; earlier += d < 0; fam[b] = fam.get(b, 0) + len(relpos[v])
    n = later + earlier
    p = binomtest(later, n).pvalue if n else float("nan")
    top_family = max(fam.items(), key=lambda x: x[1]) if fam else None
    print(f"  {cls:11} later {later:2d}  earlier {earlier:2d}  p {p:.3f}   largest base family {top_family} of {sum(fam.values())} marked tokens")
for cls in ("top only", "both"):
    print(cls, [(v, b, len(relpos.get(v, [])), round(np.mean(relpos[v]) - np.mean(relpos[b]), 2)) for v, b in pairs[cls] if v in relpos and b in relpos])
