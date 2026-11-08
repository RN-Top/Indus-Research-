"""Are rare Indus signs (in 1-3 texts) probably drawing variants of common signs?
Evidence A: glyph_variants.csv lists the rare sign as similar to a sign with >= COMMON texts.
Evidence B: crosswalk_G_to_P.csv maps the rare sign to a Parpola sign that is also the
mapping of a common G-sign (>= COMMON texts), i.e. two G-numbers merged into one reading.
Baseline: the same two tests applied to common signs (>= 20 texts), to see how often
similarity links exist at all.
"""
import json, ast, csv, collections, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
COMMON, RARE_MAX = 20, 3
rows = json.load(open(ROOT / "data/icit_merged_paragorth/merged-corpus-canonical.json"))
cnt = collections.Counter()
for r in rows:
    s = r["seq_strong"]; s = ast.literal_eval(s) if isinstance(s, str) else s
    for x in set(str(t) for t in s): cnt[f"G{x}"] += 1
variants = collections.defaultdict(set)
for r in csv.DictReader(open(ROOT / "data/glyph_variants.csv")):
    a, b = r["g_sign"], r["similar_to"]
    variants[a].add(b); variants[b].add(a)
cross = collections.defaultdict(set)
for r in csv.DictReader(open(ROOT / "data/crosswalk_G_to_P.csv")):
    if r["confident"] == "True": cross[r["p_sign"]].add(r["g_sign"])
def evidence(g):
    a = any(cnt.get(v, 0) >= COMMON for v in variants.get(g, ()))
    b = False
    for p, gs in cross.items():
        if g in gs and any(cnt.get(h, 0) >= COMMON for h in gs if h != g): b = True
    return a, b
rare = [g for g, n in cnt.items() if 1 <= n <= RARE_MAX]
common = [g for g, n in cnt.items() if n >= COMMON]
def summarize(signs):
    ev = [evidence(g) for g in signs]
    A = sum(a for a, _ in ev); B = sum(b for _, b in ev); E = sum(a or b for a, b in ev)
    return {"n": len(signs), "A_variant_list": A, "B_shared_P_reading": B, "A_or_B": E,
            "share_A_or_B": round(E / len(signs), 3) if signs else None}
print(json.dumps({"rare_1to3": summarize(rare), "common_20plus": summarize(common)}, indent=2))
print("rare signs with A_or_B (first 40):", sorted(g for g in rare if any(evidence(g)))[:40])
