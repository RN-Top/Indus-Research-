"""Copper tablets as an answer key for marks, using Mahadevan's own picture coding (IM77). Scouting.

ICIT codes most copper-tablet pictures as "Othr" or unknown (copper_marks_scouting.md). Mahadevan (1977 / IDF 1980)
coded each copper tablet's picture in detail (fs80, 164 codes). This reruns the one-sign-difference check on his data:
when two copper texts differ by one sign, is the picture the same?

Sign relations come from the blind mark annotation (G-numbers), reached through paragorth's unvalidated
ICIT->Mahadevan bridge (bridge_extended.json), inverted. A substitution is
  mark swap  - both signs map to G-signs of the same base family;
  unrelated  - both map, to different families;
  unmapped   - either sign has no bridge entry.
Pictures compared two ways: exact fs80 description, and coarse (the animal or figure, first words of the description).

NOTE: IM77 covers the same objects as ICIT, holdout included, so after this run the ICIT holdout's copper tablets
are no longer clean for a marks-picture test. (With 29 copper objects the holdout could not carry one anyway.)

Usage: python3 scripts/copper_marks_im77.py <im77_corpus_lines.csv> <bridge_extended.json>
"""
import csv, json, re, sys
from collections import Counter, defaultdict
from itertools import combinations
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
lines = [r for r in csv.DictReader(open(sys.argv[1])) if r["object_type"] == "copper tablet"]
bridge = json.load(open(sys.argv[2]))
m2g = defaultdict(set)
for g, ms in bridge.items():
    for m in ms:
        m2g[int(m)].add("G" + g)

ann = {r["sign"]: r for r in csv.DictReader(open(ROOT / "data/sign_marks/marks_blind_2026-10-20.csv"))}
parent = {s: (s if r["base"] in ("self", "") else r["base"]) for s, r in ann.items()}


def fam(g):
    seen = set()
    while g in parent and parent[g] != g and g not in seen:
        seen.add(g); g = parent[g]
    return g


NONE = ("No Field Symbol", "", "None")


def coarse(d):
    d = d.lower()
    for k in ["ox-antelope", "goat-antelope", "hare", "elephant", "rhinoceros", "tiger", "unicorn", "short-horned bull",
              "buffalo", "fabulous animal", "standing personage", "endless knot", "double-axe", "uncertain animal"]:
        if k in d:
            return k
    return d[:20]


by_text = defaultdict(list)
for r in lines:
    by_text[r["text_no"]].append(r)
objs = []
for tn, rs in by_text.items():
    pics = [r["fs_description"] for r in rs if r["fs_description"] not in NONE and r["fs80"] not in ("0", "999")]
    toks = []
    for r in sorted(rs, key=lambda r: (r["side"], r["line"])):
        if r["line"] != "9":
            toks += [int(t) for t in r["signs_clean"].split()]
    if not pics or not toks or 0 in toks:
        continue
    objs.append((tn, tuple(toks), pics[0]))
print(f"IM77 copper tablets: {len(by_text)}; with a picture and an undamaged text: {len(objs)}")

texts = defaultdict(list)
for tn, t, p in objs:
    texts[t].append(p)
pic = {t: Counter(ps).most_common(1)[0][0] for t, ps in texts.items()}
# baseline: identical texts
same_exact = same_coarse = tot = 0
for t, ps in texts.items():
    for a, b in combinations(ps, 2):
        tot += 1; same_exact += a == b; same_coarse += coarse(a) == coarse(b)
print(f"Distinct texts: {len(texts)}. Identical-text pairs: {tot}; same picture {same_exact} exact, {same_coarse} coarse")


def relation(a, b):
    ga, gb = m2g.get(a, set()) & set(ann), m2g.get(b, set()) & set(ann)
    if not ga or not gb:
        return "unmapped", ""
    fa, fb = {fam(x) for x in ga}, {fam(x) for x in gb}
    if fa & fb:
        return "mark swap", f"{'/'.join(sorted(ga))} vs {'/'.join(sorted(gb))}"
    return "unrelated", f"{'/'.join(sorted(ga))} vs {'/'.join(sorted(gb))}"


rows = []
T = sorted(texts)
for s, t in combinations(T, 2):
    if len(s) == len(t):
        d = [k for k in range(len(s)) if s[k] != t[k]]
        if len(d) == 1:
            k = d[0]; rel, gs = relation(s[k], t[k])
            rows.append(dict(kind="substitution", rel=rel, m=f"M{s[k]}->M{t[k]}", g=gs, a=s, b=t, pa=pic[s], pb=pic[t]))
    elif abs(len(s) - len(t)) == 1:
        lo, hi = (s, t) if len(s) < len(t) else (t, s)
        for k in range(len(hi)):
            if hi[:k] + hi[k + 1:] == lo:
                rows.append(dict(kind="insertion", rel="insertion", m=f"+M{hi[k]}", g="", a=lo, b=hi, pa=pic[lo], pb=pic[hi]))
                break

print("\nOne-sign differences: same picture (exact / coarse)")
summ = {}
for rel in ("mark swap", "unrelated", "unmapped", "insertion"):
    rs = [r for r in rows if r["rel"] == rel]
    e = sum(r["pa"] == r["pb"] for r in rs); c = sum(coarse(r["pa"]) == coarse(r["pb"]) for r in rs)
    summ[rel] = dict(n=len(rs), same_exact=e, same_coarse=c)
    print(f"   {rel:10} {len(rs):3} pairs: {e} / {c}")
print("\nPairs:")
for r in sorted(rows, key=lambda r: (r["rel"], r["m"])):
    same = "SAME" if coarse(r["pa"]) == coarse(r["pb"]) else "DIFF"
    print(f"  [{r['rel']:9}] {r['m']:13} {r['g']:24} {same}  {' '.join(map(str, r['a']))} ({coarse(r['pa'])}) | "
          f"{' '.join(map(str, r['b']))} ({coarse(r['pb'])})")
json.dump(dict(summary=summ, identical=dict(pairs=tot, same_exact=same_exact, same_coarse=same_coarse),
               pairs=[{**r, "a": list(r["a"]), "b": list(r["b"])} for r in rows]),
          open(ROOT / "results/copper_marks_im77.json", "w"), indent=1)
