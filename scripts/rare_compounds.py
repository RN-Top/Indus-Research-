"""Are rare signs compounds/variants of common signs? Exploration only.
Uses the blind shape annotation data/sign_marks/marks_blind_2026-10-20.csv (sign, base, marks). 'Derived' = base is
another sign (added mark, doubling, ligature)."""
import sys, csv
from pathlib import Path
from collections import Counter, defaultdict
import numpy as np, pandas as pd
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from indus_workbench import data
ROOT = Path(__file__).resolve().parents[1]
raw, _ = data.load_raw("indus_website")
c = data.build_corpus(raw, "indus_website", metadata=data.load_metadata("indus_website"), drop_damaged=True, dedupe=True, drop_unidentified=True)
seqs = [list(s) for s in data.explore_only(c).df.signs]   # EXPLORATION ONLY
cnt = Counter(x for s in seqs for x in s)
ann = {r["sign"]: r for r in csv.DictReader(open(ROOT / "data/sign_marks/marks_blind_2026-10-20.csv"))}
def base(g):
    seen = set()
    while g in ann and ann[g]["base"] not in ("self", "", g) and g not in seen:
        seen.add(g); g = ann[g]["base"]
    return g
signs = sorted(cnt)
print(f"signs used in exploration: {len(signs)}; annotated: {sum(g in ann for g in signs)}")
band = lambda n: "1 use" if n == 1 else "2-6" if n <= 6 else "7-30" if n <= 30 else "31+"
rows = []
for g in signs:
    if g not in ann: continue
    rows.append({"sign": g, "uses": cnt[g], "band": band(cnt[g]), "derived": base(g) != g,
                 "ligature": "ligature" in ann[g]["marks"]})
d = pd.DataFrame(rows)
print(d.groupby("band").agg(signs=("sign", "size"), derived=("derived", "mean"), ligature=("ligature", "mean")).round(2).reindex(["1 use", "2-6", "7-30", "31+"]))
from scipy.stats import fisher_exact
rare = d[d.uses <= 6]; com = d[d.uses > 6]
print("derived: rare (<=6 uses)", rare.derived.sum(), "/", len(rare), " vs common", com.derived.sum(), "/", len(com),
      " Fisher p", round(fisher_exact([[rare.derived.sum(), (~rare.derived).sum()], [com.derived.sum(), (~com.derived).sum()]])[1], 5))
bases = {base(g) for g in signs}
tok_bases = Counter(base(x) for s in seqs for x in s)
print(f"distinct signs {len(signs)} -> distinct base shapes {len(bases)}; tokens covered by the 100 commonest bases {sum(v for _, v in tok_bases.most_common(100))/sum(tok_bases.values()):.2f}")
# position consistency: derived signs with 2+ uses vs their base, against random frequency-matched stand-in bases
rel = defaultdict(list)
for s in seqs:
    if len(s) < 2: continue
    for i, x in enumerate(s): rel[x].append(i / (len(s) - 1))
mp = {g: np.mean(v) for g, v in rel.items()}
der = [(g, base(g)) for g in signs if base(g) != g and g in mp and base(g) in mp and cnt[g] >= 2]
obs = np.mean([abs(mp[g] - mp[b]) for g, b in der])
pool = [g for g in mp if cnt[g] >= 10]
r = np.random.default_rng(0)
null = [np.mean([abs(mp[g] - mp[r.choice(pool)]) for g, b in der]) for _ in range(2000)]
print(f"derived signs (2+ uses): {len(der)}; mean |position - base position| {obs:.3f} vs random common sign {np.mean(null):.3f}; p {(1+sum(v<=obs for v in null))/2001:.4f}")
