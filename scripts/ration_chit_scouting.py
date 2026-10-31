"""Ration-chit test (scouting): do Harappa tablets whose one side reads 'N long strokes + G700' carry, on the other
side, a text that predicts N? Merged ICIT corpus (each side listed separately under the same CISI number).
Unit side: exactly [L, 700] or [700, L] with L in long strokes (31..36). Other side: any text not of that form.
Statistic: among pairs of tablets sharing the same other-side text, the share with the same N.
Null: N shuffled among tablets (10,000x). Also: mutual information between other-side first/last sign and N."""
import json, collections, random, math
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
d = json.load(open(ROOT / "data/icit_merged_paragorth/merged-corpus-canonical.json"))
LONG = {31: 1, 32: 2, 33: 3, 34: 4, 35: 5, 36: 6}
by = collections.defaultdict(list)
for x in d:
    if x["cisi"] not in ("", "-") and str(x["type"]).startswith("TAB"): by[x["cisi"]].append(x)
rows = []
for cisi, xs in by.items():
    unit = [x for x in xs if len(x["seq"]) == 2 and ((x["seq"][1] == 700 and x["seq"][0] in LONG) or (x["seq"][0] == 700 and x["seq"][1] in LONG))]
    other = [x for x in xs if x not in unit and x["seq"]]
    if len(unit) == 1 and len(other) == 1:
        u = unit[0]["seq"]; N = LONG[u[0] if u[0] in LONG else u[1]]
        rows.append((cisi, N, tuple(other[0]["seq"]), xs[0]["site"], xs[0]["type"], xs[0]["time"]))
print("two-sided tablets with a unit side and a text side:", len(rows))
print("sites/types:", collections.Counter((r[3], r[4]) for r in rows).most_common(5))
print("N distribution:", collections.Counter(r[1] for r in rows))
G = collections.defaultdict(list)
for r in rows: G[r[2]].append(r[1])
multi = {t: v for t, v in G.items() if len(v) > 1}
print("distinct other-side texts:", len(G), "; texts on 2+ tablets:", len(multi))
for t, v in sorted(multi.items(), key=lambda kv: -len(kv[1]))[:15]: print("   ", " ".join(f"G{s}" for s in t), "->", collections.Counter(v))
idx = [(i, j) for v in [[k for k, r in enumerate(rows) if r[2] == t] for t in multi] for a, i in enumerate(v) for j in v[a+1:]]
Ns = [r[1] for r in rows]
obs = sum(Ns[i] == Ns[j] for i, j in idx) / len(idx) if idx else float("nan")
rng = random.Random(20261031); null = []
for _ in range(10000):
    P = Ns[:]; rng.shuffle(P); null.append(sum(P[i] == P[j] for i, j in idx) / len(idx))
print(f"same-text pairs {len(idx)}: same N {obs:.2f} vs shuffled {sum(null)/len(null):.2f}, p = {(1+sum(n >= obs for n in null))/10001:.4f}")
def mi(pairs):
    n = len(pairs); a = collections.Counter(p for p, _ in pairs); b = collections.Counter(q for _, q in pairs); c = collections.Counter(pairs)
    return sum(v / n * math.log2(v * n / (a[p] * b[q])) for (p, q), v in c.items())
for name, f in [("first sign", lambda t: t[0]), ("last sign", lambda t: t[-1])]:
    pairs = [(f(r[2]), r[1]) for r in rows]; o = mi(pairs); nl = []
    for _ in range(2000):
        P = Ns[:]; rng.shuffle(P); nl.append(mi([(p, q) for (p, _), q in zip(pairs, P)]))
    print(f"MI({name} of text side; N) = {o:.3f} bits vs shuffled {sum(nl)/len(nl):.3f}, p = {(1+sum(v >= o for v in nl))/2001:.4f}")
# distinct texts only (one tablet per text) to avoid mould-duplicate inflation

print("\n--- by tablet type (TAB:I = incised one by one, not moulded; TAB:B = moulded, mould duplicates possible) ---")
for ty in ("TAB:I", "TAB:B"):
    R = [r for r in rows if r[4] == ty]
    GG = collections.defaultdict(list)
    for k, r in enumerate(R): GG[r[2]].append(k)
    ix = [(i, j) for v in GG.values() if len(v) > 1 for a, i in enumerate(v) for j in v[a+1:]]
    Nn = [r[1] for r in R]
    if not ix: print(ty, "no repeated texts"); continue
    o = sum(Nn[i] == Nn[j] for i, j in ix) / len(ix); nl = []
    for _ in range(10000):
        P = Nn[:]; rng.shuffle(P); nl.append(sum(P[i] == P[j] for i, j in ix) / len(ix))
    print(f"{ty}: tablets {len(R)}, repeated texts {sum(len(v)>1 for v in GG.values())}, pairs {len(ix)}: same N {o:.2f} vs shuffled {sum(nl)/len(nl):.2f}, p = {(1+sum(v >= o for v in nl))/10001:.4f}")
    print("   ", [(" ".join(f"G{s}" for s in R[v[0]][2]), dict(collections.Counter(Nn[k] for k in v))) for v in sorted(GG.values(), key=len, reverse=True)[:8] if len(v) > 1])

print("\n--- robustness: drop the commonest text (G176 G740 G400), and cap each text at 4 tablets ---")
for label, keep in [("without G176 G740 G400", lambda t: t != (176, 740, 400)), ("all texts", lambda t: True)]:
    R = [r for r in rows if keep(r[2])]
    GG = collections.defaultdict(list)
    for k, r in enumerate(R): GG[r[2]].append(k)
    for cap in (None, 4):
        groups = [v[:cap] if cap else v for v in GG.values() if len(v) > 1]
        ix = [(i, j) for v in groups for a, i in enumerate(v) for j in v[a+1:]]
        Nn = [r[1] for r in R]; o = sum(Nn[i] == Nn[j] for i, j in ix) / len(ix); nl = []
        for _ in range(10000):
            P = Nn[:]; rng.shuffle(P); nl.append(sum(P[i] == P[j] for i, j in ix) / len(ix))
        print(f"{label:24s} cap {cap}: pairs {len(ix)}, same N {o:.2f} vs {sum(nl)/len(nl):.2f}, p = {(1+sum(v >= o for v in nl))/10001:.4f}")

print("\n--- confound check: shuffle N only within the same area-section (mound) and within the same tablet type ---")
area = {}
for x in d:
    if x["cisi"] in by: area[x["cisi"]] = (x.get("area-section") or "?").strip() or "?"
strata = collections.defaultdict(list)
for k, r in enumerate(rows): strata[(area.get(r[0], "?"), r[4])].append(k)
print("strata:", sorted(((a, t, len(v)) for (a, t), v in strata.items()), key=lambda z: -z[2])[:8])
GG = collections.defaultdict(list)
for k, r in enumerate(rows): GG[r[2]].append(k)
ix = [(i, j) for v in GG.values() if len(v) > 1 for a_, i in enumerate(v) for j in v[a_+1:]]
Nn = [r[1] for r in rows]
o = sum(Nn[i] == Nn[j] for i, j in ix) / len(ix); nl = []
for _ in range(10000):
    P = Nn[:]
    for v in strata.values():
        vals = [Nn[k] for k in v]; rng.shuffle(vals)
        for k, val in zip(v, vals): P[k] = val
    nl.append(sum(P[i] == P[j] for i, j in ix) / len(ix))
print(f"within area x type: same N {o:.2f} vs {sum(nl)/len(nl):.2f}, p = {(1+sum(v >= o for v in nl))/10001:.4f}")
same_area = [(i, j) for i, j in ix if area.get(rows[i][0]) == area.get(rows[j][0]) and area.get(rows[i][0]) not in ("?", "-", "--")]
diff_area = [(i, j) for i, j in ix if area.get(rows[i][0]) != area.get(rows[j][0]) and "?" not in (area.get(rows[i][0]), area.get(rows[j][0]))]
for lab, S in [("same-text pairs from the SAME area", same_area), ("same-text pairs from DIFFERENT areas", diff_area)]:
    if S: print(f"{lab}: {len(S)} pairs, same N {sum(Nn[i]==Nn[j] for i,j in S)/len(S):.2f}")
