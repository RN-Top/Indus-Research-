"""Twelve strokes (G55): 'the year / twelve moons' vs 'the Twelve' (a body, office or title). Exploratory comparison.
Each reading predicts different company. For each measure, G55 is ranked against all non-numeral signs of similar
frequency (15-120 uses) so 'special' means special relative to ordinary signs. Material: ICIT export (all splits) +
held-out-from-export set, deduplicated within site; everything already seen, so description, not a test.

YEAR (a counted noun of time, used in dated/administrative records):
  Y1 counted: a true numeral right before it (G2 after an opener excluded)
  Y2 records: share of its texts on tags/tablets rather than seals
  Y3 sky company: shares a text with a numeral + fish pair (Parpola's star names)
TITLE (a rank or affiliation, used with persons on high-status seals):
  T1 persons: shares a text with a man sign (G90, G91, G125)
  T2 rank: on seals showing the gaur or the W-marked unicorn
  T3 title ending: the jar G740 right after it"""
import csv, json, sys
from collections import Counter
from pathlib import Path
import numpy as np
import pandas as pd
ROOT = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT)); sys.path.insert(0, str(ROOT / "scripts"))
from indus_workbench import data  # noqa: E402
from number_system import VAL  # noqa: E402
from functional_skeleton import assign  # noqa: E402
ann = {r["sign"]: r for r in csv.DictReader(open(ROOT / "data/sign_marks/marks_blind_2026-10-20.csv"))}
par = {s: (s if r["base"] in ("self", "") else r["base"]) for s, r in ann.items()}
def fam(g):
    seen = set()
    while g in par and par[g] != g and g not in seen: seen.add(g); g = par[g]
    return g
FISH = {s for s in ann if fam(s) == "G220"} | {"G220"}
MAN = {"G90", "G91", "G125"}
parts = []
for key in ("indus_website", "icit_new_to_export"):
    raw, _ = data.load_raw(key)
    parts.append(data.build_corpus(raw, key, drop_damaged=False, metadata=data.load_metadata(key)).df)
df = pd.concat(parts, ignore_index=True); df["key"] = df.signs.map(tuple); df = df.drop_duplicates(["site", "key"]).reset_index(drop=True)
raw, _ = data.load_raw("indus_website")
comp = data.explore_only(data.build_corpus(raw, "indus_website", drop_damaged=True, metadata=data.load_metadata("indus_website"))).df
roles, _ = assign([list(s) for s in comp.signs])
def isnum(s, k): return s[k] in VAL and not (s[k] == "G2" and k > 0 and roles.get(s[k - 1]) == 0)
def starpair(s): return any(isnum(s, k) and s[k + 1] in FISH for k in range(len(s) - 1))
seqs = [list(s) for s in df.signs]
use = Counter(x for s in seqs for x in s)
cands = [g for g, n in use.items() if 15 <= n <= 120 and g not in VAL and g not in MAN] + ["G55"]
known = df.motif.notna() & ~df.motif.isin(["unknown", "Unknown"]) & df.object_type.eq("seal")
def measures(g):
    m = df.signs.map(lambda s: g in s)
    tok = [(s, k) for s in seqs for k, x in enumerate(s) if x == g]
    y1 = np.mean([k > 0 and isnum(s, k - 1) for s, k in tok])
    y2 = df[m].object_type.isin(["tag", "tablet"]).mean()
    y3 = df[m].signs.map(lambda s: starpair([x for x in s if x != g])).mean()
    t1 = df[m].signs.map(lambda s: bool(MAN & set(s))).mean()
    sk = df[m & known]
    t2 = sk.motif.isin(["Gaur", "Bull1:W"]).mean() if len(sk) >= 5 else np.nan
    t3 = np.mean([k + 1 < len(s) and s[k + 1] == "G740" for s, k in tok])
    return dict(uses=use[g], Y1_counted=y1, Y2_tags_tablets=y2, Y3_star_pair=y3, T1_man=t1, T2_gaur_or_W=t2, T3_jar_after=t3)
M = pd.DataFrame({g: measures(g) for g in cands}).T
out = [f"Comparison signs: {len(M) - 1} non-numeral signs with 15-120 uses.\n", "measure            G55     median   G55 percentile among comparison signs"]
pct = {}
for c in M.columns[1:]:
    col = M[c].dropna(); v = M.loc["G55", c]
    pct[c] = float((col < v).mean() * 100 + (col == v).mean() * 50)
    out.append(f"{c:18} {v:6.2f}  {col.median():6.2f}   {pct[c]:5.1f}")
out.append(f"\nYEAR mean percentile  {np.mean([pct[c] for c in pct if c.startswith('Y')]):.1f}")
out.append(f"TITLE mean percentile {np.mean([pct[c] for c in pct if c.startswith('T')]):.1f}")
print("\n".join(out)); (ROOT / "results/g55_year_vs_title_output.txt").write_text("\n".join(out) + "\n")
M.to_csv(ROOT / "results/g55_year_vs_title_signs.csv")
