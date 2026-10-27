"""The antenna fish G240 (fish with two lines sprouting from the top; Mahadevan M67). Scouting, EXPLORATION split only.
Follow-up to g55_fish_im77.md: G240 is the fish most often right before twelve strokes (G55).
Profile G240 against the plain fish G220 and the other marked fish: uses, position, role, what comes right before
and after, numerals before (Parpola's 'number + fish' star names), objects, animals."""
import csv, sys
from collections import Counter
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT)); sys.path.insert(0, str(ROOT / "scripts"))
from indus_workbench import data  # noqa: E402
from functional_skeleton import assign  # noqa: E402
from number_system import VAL  # noqa: E402
raw, _ = data.load_raw("indus_website"); md = data.load_metadata("indus_website")
comp = data.explore_only(data.build_corpus(raw, "indus_website", drop_damaged=True, metadata=md)).df
roles, _ = assign([list(s) for s in comp.signs])
full = data.explore_only(data.build_corpus(raw, "indus_website", drop_damaged=False, metadata=md)).df
full["key"] = full.signs.map(tuple); full = full.drop_duplicates("key")
seqs = [list(s) for s in full.signs]
R = {0: "opener", 1: "middle", 2: "closer"}
out = []
def prof(g):
    n = 0; L = Counter(); Rt = Counter(); numL = 0; pos = Counter()
    for s in seqs:
        for k, x in enumerate(s):
            if x != g: continue
            n += 1; l = s[k - 1] if k else None; r = s[k + 1] if k + 1 < len(s) else None
            L[l] += 1; Rt[r] += 1; numL += l in VAL
            pos["first" if k == 0 else "last" if k == len(s) - 1 else "inside"] += 1
    return n, L, Rt, numL, pos
for g in ["G240", "G220", "G235", "G233", "G231", "G232"]:
    n, L, Rt, numL, pos = prof(g)
    if not n: continue
    out.append(f"\n== {g} (role {R.get(roles.get(g), '-')}): {n} uses; first/inside/last {pos['first']}/{pos['inside']}/{pos['last']}; "
               f"numeral right before {numL/n:.0%}")
    out.append("   before: " + ", ".join(f"{k or 'START'} {v}" for k, v in L.most_common(8)))
    out.append("   after:  " + ", ".join(f"{k or 'END'} {v}" for k, v in Rt.most_common(10)))
sub = full[full.signs.map(lambda s: "G240" in s)]
out.append(f"\nG240 objects: {sub.object_type.value_counts().to_dict()}  (all: { {k: round(v, 2) for k, v in full.object_type.value_counts(normalize=True).head(4).items()} })")
out.append(f"G240 sites: {sub.site.value_counts().head(8).to_dict()}")
seals = full[full.object_type.eq("seal") & ~full.motif.isin(["unknown", "Unknown"]) & full.motif.notna()]
s240 = seals[seals.signs.map(lambda s: "G240" in s)]
out.append(f"G240 seal animals: {s240.motif.value_counts().head(8).to_dict()}; gaur {s240.motif.eq('Gaur').mean():.1%} vs all seals {seals.motif.eq('Gaur').mean():.1%}")
# recurring phrases with G240
ng = Counter()
for s in seqs:
    for n_ in (2, 3, 4):
        for i in range(len(s) - n_ + 1):
            t = tuple(s[i:i + n_])
            if "G240" in t: ng[t] += 1
out.append("\nRecurring phrases with G240 (3+): " + "; ".join(f"{' '.join(k)} {v}" for k, v in ng.most_common(40) if v >= 3))
# what follows 'G240 G55' and 'G235 G240'
out.append("\nTexts with G240 G55:")
for s in seqs:
    if any(s[i:i + 2] == ["G240", "G55"] for i in range(len(s) - 1)): out.append("   " + " ".join(s))
print("\n".join(out)); (ROOT / "results/g240_scouting_output.txt").write_text("\n".join(out) + "\n")

# --- Substitution frames: what fills G55's slot when the rest of the phrase is the same? (added after the profile)
def frames(target, seqs, w=(1, 1)):
    fr = Counter(); fill = {}
    for s in seqs:
        for k, x in enumerate(s):
            if x == target:
                l = tuple(s[max(0, k - w[0]):k]) if k >= w[0] else ("^",) + tuple(s[:k])
                r = tuple(s[k + 1:k + 1 + w[1]]) if k + w[1] < len(s) else tuple(s[k + 1:]) + ("$",)
                fr[(l, r)] += 1
    for (l, r) in fr:
        c = Counter()
        for s in seqs:
            ss = (["^"] + s + ["$"])
            for k in range(1, len(ss) - 1):
                if tuple(ss[k - len(l):k]) == l and tuple(ss[k + 1:k + 1 + len(r)]) == r and ss[k] != target:
                    c[ss[k]] += 1
        fill[(l, r)] = c
    return fr, fill
o3 = ["\n\nSlot fillers: in phrases where G55 occurs, what other signs stand in its place? (one sign each side)"]
fr, fill = frames("G55", seqs)
agg = Counter()
for key, n in fr.most_common():
    c = fill[key]; agg.update(c)
    if c: o3.append(f"  {' '.join(key[0])} [G55 x{n}] {' '.join(key[1])}  ->  " + ", ".join(f"{k} {v}" for k, v in c.most_common(6)))
o3.append("\nSigns that most often stand in G55's slots (summed): " + ", ".join(f"{k} {v}" for k, v in agg.most_common(15)))
# slot before 'G740 G90'
c = Counter()
for s in seqs:
    for k in range(len(s) - 2):
        if s[k + 1] == "G740" and s[k + 2] == "G90": c[s[k]] += 1
o3.append("\nWhat stands right before 'G740 G90' (jar + man): " + ", ".join(f"{k} {v}" for k, v in c.most_common(12)))
print("\n".join(o3)); open(ROOT / "results/g240_scouting_output.txt", "a").write("\n".join(o3) + "\n")
