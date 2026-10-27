"""(G2 right after an opener excluded, as in number_system.) Do numerals before fish signs behave like fixed star names (Parpola) or like ordinary counts? Scouting, EXPLORATION only.
For every sign that is preceded by numerals 10+ times (distinct texts, incomplete kept): how many different numeral values
precede it, and how concentrated they are (share of the commonest value). Names ('six stars') predict few values with one
dominant; counts predict spread. Compare the fish family with other counted signs."""
import csv, sys
from collections import Counter, defaultdict
from pathlib import Path
import numpy as np
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
raw, _ = data.load_raw("indus_website"); md = data.load_metadata("indus_website")
full = data.explore_only(data.build_corpus(raw, "indus_website", drop_damaged=False, metadata=md)).df
seqs = [list(s) for s in {tuple(s) for s in full.signs}]
comp = data.explore_only(data.build_corpus(raw, "indus_website", drop_damaged=True, metadata=md)).df
roles, _ = assign([list(x) for x in comp.signs])
def isnum(s, k):  # project rule: G2 right after an opener is a marker, not the number 2
    return s[k] in VAL and not (s[k] == "G2" and k > 0 and roles.get(s[k - 1]) == 0)
before = defaultdict(Counter); sign_of = defaultdict(Counter)
for s in seqs:
    for k in range(1, len(s)):
        if isnum(s, k - 1) and s[k] not in VAL and not (k >= 2 and isnum(s, k - 2)):
            before[s[k]][VAL[s[k - 1]]] += 1; sign_of[s[k]][s[k - 1]] += 1
rows = []
for g, c in before.items():
    n = sum(c.values())
    if n >= 10:
        p = np.array(list(c.values())) / n
        rows.append((g, n, len(c), c.most_common(1)[0], -(p * np.log2(p)).sum(), g in FISH, sign_of[g].most_common(3)))
rows.sort(key=lambda r: -r[1])
out = ["sign  n  distinct_values  top_value(share)  entropy_bits  fish?  commonest numeral signs"]
for g, n, d, (v, k), H, f, top in rows:
    out.append(f"{g:5} {n:3}  {d:2}  {v}({k/n:.0%})  {H:.2f}  {'FISH' if f else ''}  {top}")
F = [r for r in rows if r[5]]; O = [r for r in rows if not r[5]]
out.append(f"\nMean entropy: fish {np.mean([r[4] for r in F]):.2f} bits ({len(F)} signs); other counted signs {np.mean([r[4] for r in O]):.2f} ({len(O)} signs)")
out.append(f"Mean top-value share: fish {np.mean([r[3][1]/r[1] for r in F]):.0%}; others {np.mean([r[3][1]/r[1] for r in O]):.0%}")
# whole texts 'numeral + fish' (Parpola: 'seven + fish forms the entire inscription')
whole = Counter(" ".join(s) for s in seqs if len(s) == 2 and s[0] in VAL and s[1] in FISH)
out.append("Whole texts 'numeral + fish': " + str(whole.most_common(10)))
print("\n".join(out)); (ROOT / "results/fish_star_scouting_output.txt").write_text("\n".join(out) + "\n")
