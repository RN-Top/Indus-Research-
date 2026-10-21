"""Are Wells's 'complex' texts (class SC, LC) joined units? Exploration only.
Usage: python3 scripts/complex_texts_scouting.py <inscriptions.csv from github.com/yajnadevam/lipi>
Text classes (Wells 2011) come from that ICIT export's 'class' column (not copied here)."""
import sys, json
from pathlib import Path
import numpy as np, pandas as pd
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from indus_workbench import data
raw, _ = data.load_raw("indus_website")
c = data.build_corpus(raw, "indus_website", metadata=data.load_metadata("indus_website"), drop_damaged=True, dedupe=True, drop_unidentified=True)
ex = data.explore_only(c).df.copy()   # EXPLORATION ONLY
L = pd.read_csv(sys.argv[1], dtype=str, keep_default_na=False); L["icit"] = L.id.str.split(".").str[0]
ex["icit"] = ex.text_id.str.lstrip("S"); ex = ex.merge(L.drop_duplicates("icit")[["icit", "class"]], on="icit", how="left")
P = json.load(open(Path(__file__).resolve().parents[1] / "hypotheses/H-2026-10-16-51b7445b.json"))["params"]
O, C = set(P["openers"]), set(P["closers"])
standalone = set(tuple(s) for s in ex.signs if len(s) >= 2)
grp = {"SC": "complex", "LC": "complex", "SP": "patterned", "LP": "patterned", "MS": "multi-segment", "SS": "single segment"}
ex["grp"] = ex["class"].map(grp)
ex = ex[ex.grp.notna() & (ex.signs.map(len) >= 4)]

def two_endings(s):      # a split where both parts (len>=2) end with a closer
    return any(s[k - 1] in C and s[-1] in C for k in range(2, len(s) - 1))
def both_attested(s):    # a split where both parts exist as complete texts elsewhere
    t = tuple(s)
    return any(t[:k] in standalone and t[k:] in standalone and t[:k] != t and t[k:] != t for k in range(2, len(s) - 1))
def inner_heading(s):    # an opener after position 1
    return any(x in O for x in s[1:])
r = np.random.default_rng(0)
rows = []
for g, d in ex.groupby("grp"):
    seqs = [list(s) for s in d.signs]
    obs = {f.__name__: np.mean([f(s) for s in seqs]) for f in (two_endings, both_attested, inner_heading)}
    sh = {f.__name__: [] for f in (two_endings, both_attested, inner_heading)}
    for _ in range(200):
        ss = [list(r.permutation(s)) for s in seqs]
        for f in (two_endings, both_attested, inner_heading):
            sh[f.__name__].append(np.mean([f(s) for s in ss]))
    row = {"group": g, "texts": len(seqs), "mean_len": round(d.signs.map(len).mean(), 1)}
    for k in obs:
        row[k] = f"{obs[k]:.2f} (shuffled {np.mean(sh[k]):.2f}, p {(1 + sum(v >= obs[k] for v in sh[k])) / 201:.3f})"
    rows.append(row)
print(pd.DataFrame(rows).to_string(index=False))
cx = ex[ex.grp == "complex"]
print("\nexamples of complex texts splitting into two attested texts:")
k = 0
for s in cx.signs:
    t = tuple(s)
    for j in range(2, len(s) - 1):
        if t[:j] in standalone and t[j:] in standalone:
            print("  ", " ".join(t[:j]), " | ", " ".join(t[j:])); k += 1; break
    if k >= 12: break

# --- explanation 2: reading direction. Does the reversed text fit the frame better?
def fit(s): return int(s[0] in O) + int(s[-1] in C)
print("\nframe fit (opener first + closer last, 0-2): forward vs reversed")
for g, d in ex.groupby("grp"):
    f = np.array([fit(list(s)) for s in d.signs]); b = np.array([fit(list(s)[::-1]) for s in d.signs])
    print(f"  {g:15} forward {f.mean():.2f}  reversed {b.mean():.2f}  texts fitting better reversed {np.mean(b > f):.2f}")
# --- explanation 3: objects, sites, frame parts
L2 = L.drop_duplicates("icit").set_index("icit")
ex["dir"] = ex.icit.map(L2["dir."])
for col in ["object_type", "site", "dir"]:
    t = pd.crosstab(ex.grp, ex[col], normalize="index").round(2)
    print(f"\n{col}:"); print(t.loc[:, t.max() >= 0.05].to_string())
ex["opener_first"] = ex.signs.map(lambda s: s[0] in O); ex["closer_last"] = ex.signs.map(lambda s: s[-1] in C)
ex["G740"] = ex.signs.map(lambda s: "G740" in s)
print(ex.groupby("grp")[["opener_first", "closer_last", "G740"]].mean().round(2))

# --- what do complex texts end with? Is it a different ending class?
from collections import Counter
allex = data.explore_only(c).df
fin_all = Counter(s[-1] for s in allex.signs if len(s) >= 2); tot_all = Counter(x for s in allex.signs for x in s)
cx = ex[ex.grp == "complex"]
fc = Counter(s[-1] for s in cx.signs)
print("\ncomplex texts: most common final signs (share of complex texts; how often that sign is final anywhere in the corpus)")
for g, n in fc.most_common(15):
    print(f"  {g:6} {n:3} ({n/len(cx):.2f})  final-rate overall {fin_all[g]/tot_all[g]:.2f}  closer? {g in C}")
pat = ex[ex.grp == "patterned"]
print("\nlast two signs of complex texts (top):", Counter(tuple(s[-2:]) for s in cx.signs).most_common(8))
print("first signs of complex texts (top):", Counter(s[0] for s in cx.signs).most_common(10))
common = set(P["common_signs"])
print("rare (non-common) first sign: complex", round(np.mean([s[0] not in common for s in cx.signs]), 2),
      "patterned", round(np.mean([s[0] not in common for s in pat.signs]), 2))

# --- explanation 4: displaced frame. Does a rotation (move a final block to the front) restore heading-first / closer-last?
def rot_fix(s):
    return any(s[k] in O and s[k - 1] in C for k in range(1, len(s)))   # text = [..closer][opener..] -> rotate at k
print("\nrotation fix: some cut point k where s[k] is an opener and s[k-1] a closer (rotating gives opener-first, closer-last)")
for g, d in ex.groupby("grp"):
    seqs = [list(s) for s in d.signs]
    obs = np.mean([rot_fix(s) for s in seqs])
    sh = [np.mean([rot_fix(list(r.permutation(s))) for s in seqs]) for _ in range(300)]
    print(f"  {g:15} {obs:.3f}  shuffled {np.mean(sh):.3f}  p {(1 + sum(v >= obs for v in sh)) / 301:.3f}")
cx = ex[ex.grp == "complex"]
print("complex texts fixed by rotation:")
for s in cx.signs:
    s = list(s)
    for k in range(1, len(s)):
        if s[k] in O and s[k - 1] in C:
            print("   ", " ".join(s), "  ->  ", " ".join(s[k:] + s[:k])); break

# --- explanation 5: count-style (tablet-like) texts on seals?
N = set(P["numerals"])
def prof(s): return {"has_numeral": any(x in N for x in s), "numeral_last2": any(x in N for x in s[-2:]),
                     "numeral_first": s[0] in N, "jar": "G740" in s, "opener_first": s[0] in O}
print("\nprofiles (exploration, texts of 4+ signs):")
allx = data.explore_only(c).df; allx = allx[allx.signs.map(len) >= 4]
tabs = allx[allx.object_type == "tablet"]
for name, seqs in [("complex", ex[ex.grp == "complex"].signs), ("patterned", ex[ex.grp == "patterned"].signs),
                   ("single segment", ex[ex.grp == "single segment"].signs), ("all tablets", tabs.signs), ("all seals", allx[allx.object_type == "seal"].signs)]:
    d = pd.DataFrame([prof(list(s)) for s in seqs]).mean().round(2).to_dict()
    print(f"  {name:15} n={len(seqs):4} {d}")
